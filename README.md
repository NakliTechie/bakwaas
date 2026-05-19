# Bakwaas

> **बकवास** — Hindi/Urdu, *noun*. Nonsense, drivel, hot air, chitchat. The stuff you say a lot of but rarely re-read.

**A browser-native explorer for your Twitter/X archive.** Started as a click-to-delete tool — turned out the harder problem isn't deleting, it's *finding* what's worth deleting in 200,000 tweets. So mostly it's now an explorer that happens to make deletion easy at the end.

**[→ Try it live](https://bakwaas.naklitechie.com)**

## What it does

Drop your Twitter archive (folder or ZIP), wait for the one-time index pass, and explore:

- **Stats** — counts, top hashtags / mentions / sources / languages, GitHub-contributions-style temporal heatmap spanning your full archive, hour × day-of-week heatmap, engagement distributions
- **Search** — MiniSearch full-text over tweets and likes, filter chips for originals / replies / retweets / media, scope toggle between tweets / likes / both
- **Patterns** — algorithmic deep analysis: viral tweets, hashtag & source ROI (which themes worked, which client lands), burst hashtags (your `#nft` 2022 era, your `#covid` Mar 2020), activity change-points, longest streak & longest silence, verbosity drift over time, self-reply thread roots, co-mention pairs, zero-engagement cleanup pile
- **Topics** — hashtag co-occurrence clusters with an adjustable threshold; pick a theme, drill into it
- **Selection** — confirmation tray for the click-to-delete workflow: everything you've opened or marked deleted lives here

**Click-to-delete is honest.** Bakwaas never calls X's API. To delete a tweet you click it open in X's real UI, do it there, come back, confirm. The hard part — knowing *what* to delete — happens here. The actual delete happens in X's own UI.

No X API. No OAuth. No accounts. No server. No telemetry.

## How to use

1. Go to [x.com/settings/download_your_data](https://x.com/settings/download_your_data) and request your archive
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

## BYOK LLM (coming in Phase 8)

The Patterns and Topics views already produce a lot without any model in the loop. A future BYOK layer will optionally add cluster labels, semantic search, and bulk classification — your key, stored locally in IndexedDB, sent only directly to the provider you chose, never to NakliTechie infrastructure, never written to the FSA sidecar.

Providers planned:
- **Claude** via [console.anthropic.com](https://console.anthropic.com/)
- **OpenAI** via [platform.openai.com](https://platform.openai.com/api-keys)
- **Gemini** via [aistudio.google.com](https://aistudio.google.com/app/apikey)

The whole CSP is already pinned so this slots in without a policy change.

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
