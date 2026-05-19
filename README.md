# Bakwaas

**Explore your Twitter archive. Find the noise. Delete it.**

A browser-native, single-file tool that ingests your Twitter/X archive, indexes every tweet and like locally, and helps you find what's worth deleting. Nothing leaves your device.

**[→ Try it live](https://bakwaas.naklitechie.com)** *(deploy pending v1.0)*

## What it does

Drop your Twitter archive (folder or ZIP) and get:

- **Stats** — temporal heatmap, top hashtags, mention graph, reply / retweet / original split, engagement distribution, source clients, language mix
- **Search** — fast full-text over 200k+ tweets and likes, with filter chips for originals, replies, retweets, media, and date/engagement bounds
- **Topics** — local TF-IDF + co-occurrence clustering surfaces themes you've drifted across; bring your own LLM key (Anthropic, OpenAI, or Gemini) for semantic search and cluster labels
- **Click-to-delete** — every tweet and like links straight back to its `twitter.com` page. You delete it in X's own UI; Bakwaas marks it deleted locally

No X API. No OAuth. No accounts. No server. No telemetry.

## How to use

1. Go to [twitter.com/settings/your_archive](https://twitter.com/settings/your_archive) and request your archive
2. Wait ~24 hours for the email with the download link
3. Open Bakwaas, drop the ZIP (or the unzipped folder) onto the page
4. Wait for indexing (one-time, resumable; ~5 minutes for 200k tweets)
5. Explore. Find the regrettable bits. Click through to delete in X.

## Privacy posture

| | Bakwaas | SaaS bulk-delete tools |
|---|---|---|
| Your archive leaves your machine | Never | Yes — uploaded to their server |
| Account / billing | None | Required |
| Where state lives | Your archive folder (FSA) + browser OPFS | Their database |
| BYOK LLM key (if you bring one) | Stored locally in IndexedDB only, sent directly to provider | N/A |

## Browser support

| Browser | Mode |
|---|---|
| Chrome / Edge 120+ | Full — folder ingest with sidecar persistence, plus ZIP mode |
| Safari 17+ | ZIP mode only — state lives in OPFS |
| Firefox 125+ | ZIP mode only — state lives in OPFS |

## BYOK LLM (optional)

Topic labels, semantic search, and bulk classification work with a key you provide. Keys persist in IndexedDB on this device and are sent only directly to the provider you chose — never to any NakliTechie server, never written to the FSA sidecar.

- **Claude:** [console.anthropic.com](https://console.anthropic.com/) → API keys
- **OpenAI:** [platform.openai.com](https://platform.openai.com/api-keys) → API keys
- **Gemini:** [aistudio.google.com](https://aistudio.google.com/app/apikey) → Get API key

## What Bakwaas doesn't do (and why)

- **Auto-delete / scheduled deletion / disappearing mode** — would require a server running background jobs on your behalf. That's the SaaS pattern Bakwaas exists in opposition to. If you want continuous automated deletion, use Redact, TweetDelete, or TweetEraser; that's their shape.
- **Multi-platform support (Reddit, Discord, Facebook, etc.)** — Bakwaas is Twitter-specific by name and design.
- **DM deletion** — different threat model. DM archives contain the other party's messages too; excluded.
- **Unfollow everyone / delete followers** — out of scope. Bakwaas is about *what you've said*, not *who you're connected to*.
- **Account or login system, server-side sync** — would require a server. Out of scope forever.

## Known limitations

- Index build on a 200k-tweet archive takes ~5 minutes on an M-class machine, longer elsewhere. Resumable if interrupted.
- Click-to-delete is manual by design. Bulk mode opens up to 50 tabs at once; you work through them.
- v1.0 has no X API path. v1.1 will add a BYOK X-API mode for users with their own dev app and credit balance.

## Status

v1.0 is in active build. The current shipped capability is documented in [CHANGELOG.md] *(coming soon)*. Full v1.0 spec and roadmap live in `docs/` alongside the source.

## Tech stack

| Concern | Solution |
|---|---|
| Archive ingest | File System Access API (folder mode), JSZip (zip mode) |
| Persistence | IndexedDB for the parsed index; FSA sidecar + OPFS mirror for state |
| Full-text search | MiniSearch |
| Topic clustering | Local TF-IDF + co-occurrence; optional BYOK LLM layer |
| Build tooling | None — one HTML file |

## Part of the NakliTechie series

| Tool | What it does |
|------|--------------|
| [**VaultMind**](https://github.com/NakliTechie/VaultMind) | Obsidian vault explorer + builder — graph, ingest, RAG chat, editor |
| [**Tijori**](https://github.com/NakliTechie/Tijori) | Password vault — single-file, hardware-key-aware, multi-vault |
| [**LocalMind**](https://github.com/NakliTechie/LocalMind) | Private AI research agent — 9 tools, RAG, web search, multimodal |
| [**KoLocal**](https://github.com/NakliTechie/KoLocal) | Go (Baduk) vs MCTS AI — 9×9 / 13×13 / 19×19 |
| [**BabelLocal**](https://github.com/NakliTechie/BabelLocal) | Offline translation — 200 languages, NLLB model |

---

**Built by [Chirag Patnaik](https://github.com/NakliTechie)**

*Built with [Claude](https://claude.ai).*
