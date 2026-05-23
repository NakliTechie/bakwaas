#!/usr/bin/env python3
"""
Bakwaas offline embedder
========================
Reads a Twitter/X archive and writes a bakwaas-emb.bin file you can import
into Bakwaas via the "Import embeddings" button in the Search tab.

Much faster than in-browser embedding: uses native Python + PyTorch and can
use your GPU if available.

Usage:
    python3 scripts/embed.py /path/to/twitter-archive.zip
    python3 scripts/embed.py /path/to/twitter-archive-folder/
    python3 scripts/embed.py /path/to/archive.zip  my-output.bin   # custom output name

Requires:
    pip install sentence-transformers

Output:
    bakwaas-emb.bin  (~310 MB for 200k tweets)

Binary format (BWEM v1):
    [0-3]   "BWEM"            magic
    [4-7]   uint32 LE         num_tweets
    [8-11]  uint32 LE         dim (384 for all-MiniLM-L6-v2)
    [12-15] uint32 LE         id_block_size (bytes, padded to 4-byte boundary)
    [16 .. 16+id_block_size]  null-separated tweet ID strings
    [16+id_block_size ..]     float32 LE embeddings, row-major (num_tweets × dim)
"""

import sys
import json
import re
import struct
import zipfile
import os
from pathlib import Path


# ── helpers ──────────────────────────────────────────────────────────────────

def strip_js_wrapper(content: str) -> str:
    """Strip 'window.YTD.tweets.part0 = ' prefix from Twitter JS files."""
    content = content.strip()
    m = re.match(r'^[^=\[]*=\s*', content)
    if m:
        content = content[m.end():]
    return content


def extract_tweets(items: list) -> list[tuple[str, str]]:
    """Pull (id, text) pairs out of a parsed tweets-part*.js array."""
    out = []
    for item in items:
        tw = item.get('tweet', item)
        tweet_id = tw.get('id_str') or tw.get('id')
        text = tw.get('full_text') or tw.get('text', '')
        if tweet_id and text:
            # Decode HTML entities Twitter uses
            text = text.replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>').replace('&quot;', '"')
            out.append((str(tweet_id), text))
    return out


def parse_file(content: str) -> list[tuple[str, str]]:
    try:
        items = json.loads(strip_js_wrapper(content))
        return extract_tweets(items)
    except Exception as e:
        print(f'  Warning: parse error: {e}')
        return []


# ── loaders ──────────────────────────────────────────────────────────────────

def load_from_zip(zip_path: str) -> list[tuple[str, str]]:
    tweets = []
    seen_ids = set()
    with zipfile.ZipFile(zip_path, 'r') as z:
        names = z.namelist()
        # Match Twitter archive tweet part files
        tweet_files = sorted(
            [n for n in names if re.search(r'data/tweets.*\.js$', n)],
            key=lambda p: (p, int(re.search(r'\d+', p.split('/')[-1]).group() if re.search(r'\d+', p.split('/')[-1]) else '0'))
        )
        if not tweet_files:
            sys.exit('No tweets-part*.js found. Is this a Twitter/X archive ZIP?')
        print(f'  Found {len(tweet_files)} tweet file(s) in ZIP')
        for fname in tweet_files:
            with z.open(fname) as f:
                content = f.read().decode('utf-8', errors='replace')
            batch = parse_file(content)
            new = [(i, t) for i, t in batch if i not in seen_ids]
            seen_ids.update(i for i, _ in new)
            tweets.extend(new)
            print(f'  {fname}: {len(new)} tweets')
    return tweets


def load_from_folder(folder: str) -> list[tuple[str, str]]:
    tweets = []
    seen_ids = set()
    data_dir = Path(folder) / 'data'
    if not data_dir.exists():
        data_dir = Path(folder)
    tweet_files = sorted(data_dir.glob('tweets*.js'))
    if not tweet_files:
        sys.exit(f'No tweets*.js found in {data_dir}. Is this a Twitter/X archive folder?')
    print(f'  Found {len(tweet_files)} tweet file(s) in folder')
    for p in tweet_files:
        content = p.read_text(encoding='utf-8', errors='replace')
        batch = parse_file(content)
        new = [(i, t) for i, t in batch if i not in seen_ids]
        seen_ids.update(i for i, _ in new)
        tweets.extend(new)
        print(f'  {p.name}: {len(new)} tweets')
    return tweets


# ── writer ───────────────────────────────────────────────────────────────────

def write_bin(output_path: str, ids: list[str], embeddings) -> None:
    import numpy as np

    num_tweets = len(ids)
    dim = embeddings.shape[1]

    # ID block: null-separated, padded to 4-byte boundary
    id_block = '\x00'.join(ids).encode('utf-8') + b'\x00'
    while len(id_block) % 4:
        id_block += b'\x00'
    id_block_size = len(id_block)

    with open(output_path, 'wb') as f:
        f.write(b'BWEM')
        f.write(struct.pack('<III', num_tweets, dim, id_block_size))
        f.write(id_block)
        f.write(embeddings.astype('<f4').tobytes())

    size_mb = os.path.getsize(output_path) / 1024 / 1024
    print(f'\nWrote {output_path}  ({size_mb:.0f} MB, {num_tweets:,} tweets × {dim}d)')


# ── main ─────────────────────────────────────────────────────────────────────

def main():
    if len(sys.argv) < 2 or sys.argv[1] in ('-h', '--help'):
        print(__doc__)
        sys.exit(0)

    archive_path = sys.argv[1]
    output_path  = sys.argv[2] if len(sys.argv) > 2 else 'bakwaas-emb.bin'

    print(f'Loading archive: {archive_path}')

    if zipfile.is_zipfile(archive_path):
        tweets = load_from_zip(archive_path)
    else:
        tweets = load_from_folder(archive_path)

    if not tweets:
        sys.exit('No tweets found.')

    print(f'\n{len(tweets):,} tweets loaded.')

    # Embedding
    try:
        from sentence_transformers import SentenceTransformer
    except ImportError:
        sys.exit('\nMissing dependency:\n  pip install sentence-transformers\n')

    print('Loading model (all-MiniLM-L6-v2) …')
    model = SentenceTransformer('all-MiniLM-L6-v2')

    ids   = [t[0] for t in tweets]
    texts = [t[1] for t in tweets]

    print(f'Embedding {len(texts):,} tweets … (batch_size=512)')
    embeddings = model.encode(
        texts,
        normalize_embeddings=True,
        batch_size=512,
        show_progress_bar=True,
        convert_to_numpy=True,
    )

    write_bin(output_path, ids, embeddings)

    print('\nImport it in Bakwaas:')
    print('  Search tab → "Import embeddings" button → pick the .bin file')


if __name__ == '__main__':
    main()
