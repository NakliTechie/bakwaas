# Bakwaas

> **बकवास** — Hindi/Urdu, *noun*. Nonsense, drivel, hot air, chitchat. The stuff you say a lot of but rarely re-read.

**A browser-native explorer for your social-media archives.** Started as a click-to-delete tool for Twitter/X — turned out the harder problem isn't deleting, it's *finding* what's worth deleting in 200,000 posts. So mostly it's now an explorer that happens to make deletion easy at the end.

Supported sources:
- **Twitter / X** — full surface (ZIP or unzipped folder via the File System Access API)
- **Mastodon** — full surface except engagement-driven cards (their export doesn't preserve fav/boost totals)
- **Bluesky** — live AppView API fetch by handle, no auth, engagement counts intact, full surface
- **Reddit** — posts + comments from the GDPR-export ZIP, no engagement counts

**[→ Try it live](https://bakwaas.naklitechie.com)**

---

## What it does

Drop your archive (or paste a Bluesky handle), wait for the one-time index pass, and explore through seven tabs:

### Stats
Counts, top hashtags / mentions / sources / languages, GitHub-contributions-style temporal heatmap spanning your full archive, hour × day-of-week heatmap, engagement distributions. Top-N panels accept a **date-range filter** at the top; **click any heatmap day** to drill into that single day's tweets in Search.

### Search
Fast full-text over tweets and likes via MiniSearch with a rich filter surface:

- **Power query syntax** in the search box: `since:2018-01-01 until:2019-12-31 from:elonmusk to:dril min_faves:10 min_rts:5 has:media has:link lang:en -crypto "exact phrase" cricket OR football`
- **Visual filter bar**: Since / Until / Min ♥ / Min ↻ / Language dropdown / Near match toggle / Reset
- **Filter chips**: Originals / Replies / Retweets / Media / Links
- **Quick-range presets**: 7d / 30d / 90d / YTD / This year / Last year / All
- **Date-range scrubber** — SVG dual-thumb range picker over a tweets-per-month histogram. Drag thumbs or the highlighted band; two-way sync with the date inputs
- **Scope toggle**: Tweets / Likes / Both
- **Near match** toggle — folds in phonetic-encoded variants so `amrika`/`umrika` find `america`, and Latin `chirag` finds Devanagari `चिराग` (phonetic indexing runs at MiniSearch-build time)
- **Semantic search** — tick **Semantic** to search by meaning rather than keywords. Runs `all-MiniLM-L6-v2` in the browser (one-time embedding pass, results cached in IndexedDB). Large archives can use the offline Python script (`scripts/embed.py`) instead — 10–50× faster, uses your machine's CPU/GPU, outputs a `.bin` file you import once via **↑ Import emb.**
- **Filters-only searches** — leave the text box empty, set `min_faves:100 since:2018`, get tweets streamed via IndexedDB cursor with the `created_at` index
- **Select-all matches** + per-result selection — adds to the global selection set

### Engagement
KPI cards (most-engaged month, most-engaged year, all-time top tweet, lifetime engagement), three side-by-side top-tweets lenses (combined / likes / RTs), engagement-over-time monthly line chart, viral-moments timeline, hashtags by avg engagement, sources by avg engagement, hour × DOW colored by avg engagement. Honest "views aren't in the archive" disclaimer.

### Patterns
Algorithmic deep analysis (no AI in the loop):

- **Activity rhythm**: longest streak, longest silence, monthly tweets line chart, activity change-points (≥2σ from rolling baseline), verbosity drift
- **Eras compared**: chronological-thirds cohort cards side-by-side (mix, avg eng, era hashtag, top hashtag, top mention, source, top tweet)
- **Era detection**: burst hashtags (≥50% of uses in one month) — `#nft Mar 2022`, `#covid Mar 2020`
- **Mood, voice & rhythm**: emoji mood timeline + word-list polarity drift (both `pos − neg` per month), style fingerprint with derived archetype ('Long-form · Asker · Emoji-heavy'), sleep / quiet-hours window per year
- **What you talk about**: top phrases (bigrams), recurring themes (bigrams in ≥3 years), hashtag-lifecycle sparklines, top link hosts you share
- **Relationships**: best friends (top 12 bubble cards with colour-coded initials — **click to drill into a "Conversation with @user"** view), distance circles (top 24 connections placed at radii inverse to interaction count, with Inner/Trusted/Acquaintances rings), top co-mention pairs, force-directed conversation graph, longest self-reply threads + a **"Browse all threads →" thread explorer modal** with text search and click-to-expand trees
- **First, last, best**: first & last original tweet of each year; top tweet per year
- **On this day**: today's-date anniversaries across years + "what were you doing then?" date picker with ±N day window
- **Cleanup candidates**: zero-engagement counts per year + sample list of 50 oldest + PII audit (regex-flagged emails / phones / SSN-shape)

### Wrapped
Pick a year or all-time, get a poster-style summary card with top tweet, top hashtag, peak month, era hashtag, posting personality. Download as **standalone HTML** (hostable anywhere) or **PNG** (postable to social). All composed locally; nothing uploaded.

### Topics
Hashtag co-occurrence clusters with an adjustable threshold. Pick a theme, drill into it via "Search this cluster".

### Selection
The deletion confirmation tray:

- **Per-card actions**: open in X, mark deleted, undo
- **Bulk actions**: "Open N tabs" (modal guard at >10, hard cap at 50), "Mark N deleted"
- **BYOK Twitter / X API delete** — paste your own 4 OAuth 1.0a credentials, Bakwaas signs DELETE /2/tweets/:id with HMAC-SHA1, handles 429 rate limits with reset-aware backoff, marks deleted in the local store automatically
- **Site-wide select buttons** — every tweet card in every tab has a small `+ select` button. Counts roll up into a floating chip visible from any tab

---

## How deletion works

**Click-to-delete is honest** *(the default)*. Bakwaas opens the tweet on X in a new tab; you delete it there in the real UI; you come back and confirm. The hard part — knowing *what* to delete — happens in Bakwaas. The actual delete happens in X's own UI.

**BYOK X API delete** *(optional)*. If you have your own X developer credentials (OAuth 1.0a Read+Write), Bakwaas can bulk-delete via `DELETE /2/tweets/:id` directly. Keys live in IndexedDB only — never the FSA sidecar, never anywhere except `api.x.com`. Honest about cost: X v2 DELETE is a paid endpoint these days.

No X API. No OAuth. No accounts. No server. Every export is a download from your browser, not an upload from it.

**One transparent exception:** Bakwaas runs Google Analytics 4 (`G-E5XCNWFXNC`) for page visits and tab opens — a basic "is anyone using this" counter for the project. **No archive content is ever sent**, only the URL and which tab you opened. `anonymize_ip` is on. Block it with uBlock / Privacy Badger if you prefer.

---

## Twitter Advanced Search parity

| Twitter Advanced Search | Bakwaas equivalent |
|---|---|
| All of these words | Free-text search (MiniSearch AND default) |
| Exact phrase | `"quoted phrase"` |
| Any of these words | `term1 OR term2 OR term3` (uppercase) |
| None of these words | `-term` |
| Hashtags | `#tag` in text or hashtag filter |
| From these accounts | `from:user` (matches tweet mentions) |
| To these accounts | `to:user` (uses `in_reply_to_screen_name`) |
| Mentioning these accounts | `@user` in text |
| Min replies / faves / RTs | `min_faves:N`, `min_rts:N` (min replies isn't in the archive) |
| Date range | `since:` / `until:` + visual inputs + scrubber + presets |
| Replies filter | Replies / Originals chips |
| Links filter | Links chip + `has:link` |
| (none) | **Near match** — phonetic + cross-script fuzziness |
| (none) | Lang filter, has:media, full power-syntax composition |

---

## Privacy posture

Everything runs locally. The archive never leaves your tab. The Bluesky path makes only the API calls you'd make yourself. The X API delete path only ever calls `api.x.com`. No NakliTechie server; no telemetry; no logging.

Where state lives:
- **IndexedDB** (origin: `bakwaas.naklitechie.com`) — the parsed index, MiniSearch serialized, all aggregation caches, BYOK X credentials, deletion state
- **OPFS** mirror at `bakwaas-state.json` — backup of phase / fingerprint state
- **FSA sidecar** at `<archive>/bakwaas-state.json` — folder-mode only, never carries BYOK keys (sidecar travels with the archive)

---

## Tech notes

- **Single-file HTML**, vanilla JS, no build step. Open with `python3 -m http.server` or any static host.
- **MiniSearch** for full-text (CDN ESM @ 7.1.2). Indexes serialised to IndexedDB. Lazy rebuild on first search.
- **JSZip** for ZIP ingestion (CDN ESM). FSA folder mode skips it entirely.
- **Palette**: [Rangrez](https://github.com/NakliTechie/rangrez) — periwinkle dark (`--accent:#6b8ef5`, `--accent-2:#f0845a` coral). Light mode via `.theme-light`. Toggle in the header persists to localStorage; auto-detects OS preference on first visit.
- **Phonetic indexing**: per-tweet `phonetic_text` field generated at index time. Cross-script transliteration covers nine non-Latin scripts — Brahmic family (**Devanagari, Bengali, Tamil, Gurmukhi, Gujarati, Telugu, Kannada, Malayalam**) via shared inherent-a/halant logic plus **Cyrillic** and **Greek** as alphabetic 1:1. CJK covered: Chinese → pinyin, Japanese kanji → kana → romaji, Korean → romaja. Latin output runs through a consonant-skeleton encoder. Result: `chirag`, `chiraag`, and `चिराग` all hash to `krg`; `america`/`amrika`/`umrika` → `mrk`.
- **Semantic search**: `@xenova/transformers@2.17.2` / `all-MiniLM-L6-v2` runs on the main thread (384-dim vectors, chunked with `setTimeout(0)` yields). Embeddings stored in IndexedDB (DB_VERSION=3, `embeddings` store). For large archives, `scripts/embed.py` generates the same vectors offline via `sentence-transformers` (batch_size=512); output is a BWEM binary (magic + uint32 header + null-separated ID block + raw float32 matrix) imported once. CSP must include `https://hf.co https://*.hf.co https://*.xethub.hf.co` — HuggingFace redirects large ONNX files to the XetHub CDN, not `huggingface.co`.
- **OAuth 1.0a signing** for the X API delete path: HMAC-SHA1 via SubtleCrypto, RFC-3986 percent-encoded base-string assembly.
- **CSP** pinned: `default-src 'self'`, `script-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net`, `connect-src` extended for BYOK provider hosts + HuggingFace / XetHub CDN for model weights.

---

## Roadmap

What's in `PENDING.md` (local-only) — the next-session work:

- **Semantic "Find more like this"** — surface the top-K semantically similar tweets on any result, now that embeddings are cached in IDB
- **Topics cluster labels** — derive 2–4 word labels from centroid embeddings per hashtag cluster (no LLM needed)
- **Arabic phonetic indexing** — different structural pattern from Brahmic (right-to-left, short vowels typically omitted); Buckwalter-style consonantal skeleton
- **Instagram archive** as a fifth provider
- **BYOK LLM** (Anthropic / OpenAI / Gemini) — natural-language → filter spec in Search; cluster labels in Topics; bulk classify in Patterns

---

## Part of the NakliTechie series

Bakwaas is a sibling of a handful of other browser-native, single-file tools by the same author. All zero-server, all your data stays on your device.

| Tool | What it does |
|---|---|
| [**Crate**](https://github.com/NakliTechie/crate) | A drop-anything organiser surface — the browser face of the `private-mesh` fabric |
| [**nakliOS**](https://naklios.dev) | The "desktop" launcher that hosts the rest of the series — apps run in iframes via a cooperative postMessage protocol |
| [**LocalMind**](https://github.com/NakliTechie/LocalMind) | Private AI research agent — 9 tools, RAG, web search, multimodal, BYOK model |
| [**VaultMind**](https://github.com/NakliTechie/VaultMind) | Obsidian vault explorer + builder — force graph, semantic search, AI chat, in-place editing |
| [**Tijori**](https://github.com/NakliTechie/Tijori) | Single-file password vault — hardware-key-aware, multi-vault, KeePass-export-compatible |

[See the full series →](https://naklitechie.github.io/)

---

**Built by [Chirag Patnaik](https://github.com/NakliTechie)**
*Built with [Claude](https://claude.ai).*
