# Black Swan Stocks studio

Automated motion-graphics Reels for [@blackswanstocks](https://instagram.com/blackswanstocks): one speculative ASX miner every Monday, Wednesday and Friday, and one big-picture topic (commodities, costs, policy) every Sunday. Roughly 55 seconds each.

## How it runs

| Who | When | What |
|---|---|---|
| Claude (scheduled task) | Mon, Wed, Fri, Sun ~4:45pm Melbourne | Researches the day's topic, writes `videos/<date>-<slug>/spec.py`, runs `tools/check.py`, renders test stills, adds the slug to `queue.txt` and `featured.txt`, pushes to `main` |
| GitHub (preview.yml) | On every push that changes `videos/` | Renders the new video and attaches it to the run (Actions → Render preview → previews.zip) |
| GitHub (post.yml) | Mon, Wed, Fri, Sun 7:30pm Melbourne | Posts **today's** video only (stale videos never post), after the compliance check passes |
| GitHub (maintenance.yml) | Weekly | Checks the Instagram connection and refreshes the 60-day token |
| GitHub (insights.yml) | Daily ~7:17am Melbourne | Pulls each post's metrics (views, reach, likes, comments, shares, saves, follows, watch time) for every media ID in `posted.txt` into `insights.csv`. Needs the insights permission on the token (see below) |

To stop a post: delete its line from `queue.txt` before 7:30pm. To pull one that's up: Actions → Delete Instagram posts → paste the media ID from `posted.txt`.

## One-time setup

1. **Repo settings → Pages → Source: GitHub Actions.**
2. **Repo settings → Secrets and variables → Actions:**

   | Secret | Where it comes from |
   |---|---|
   | `IG_ACCESS_TOKEN` | Meta developer app → Instagram → API setup with Instagram login → add the blackswanstocks account → Generate token |
   | `IG_USER_ID` | Same screen, shown next to the account |
   | `GH_PAT` (optional) | Fine-grained token, this repo only, *Secrets: read and write*. Lets the weekly job refresh the Instagram token |
   | `ELEVENLABS_API_KEY`, `ELEVENLABS_VOICE_ID` (optional) | Only if you switch `voice.json` to `elevenlabs` |

3. **Test:** Actions → *Token refresh + connection check* → Run. It should print `connected: blackswanstocks`.
4. **Insights permission:** the token must include `instagram_manage_insights` (Facebook Login tokens, starting `EA`) or `instagram_business_manage_insights` (Instagram Login tokens, starting `IG`). Without it, Actions → *Pull Instagram insights* saves likes and comments only and fails with the exact permission to add. Test with Actions → *Pull Instagram insights* → Run.
5. **Dry run:** Actions → *Post today's video* → Run with dry run ticked and a date that has a video (e.g. `2026-11-16`).

## Local build

```
bash tools/install.sh                      # or: apt ffmpeg libcairo2-dev, pip install -r requirements.txt kokoro-onnx, copy assets/fonts to ~/.fonts
python3 tools/check.py videos/2026-11-16-vka
python3 -m engine.build videos/2026-11-16-vka --out out --sheet      # contact sheet of every scene, no voice needed
python3 -m engine.build videos/2026-11-16-vka --out out              # full mp4 + caption + cover
python3 -m brand.make --out brand/out                                # profile pics, highlight covers, pinned carousel
```

See `CONTENT.md` for the spec format and editorial rules, and `BRAND.md` for the account setup.

## Files

- `engine/` renderer: `scenes.py` (all scene types), `render.py` (header, subtitles, cover), `voice.py` (Kokoro/ElevenLabs), `audio.py` (generated music bed, ducked under the voice), `geo.py` (maps)
- `assets/fonts` Inter Tight, Instrument Serif, JetBrains Mono (all SIL OFL). `assets/geo` Natural Earth outlines via world-atlas
- `publish/insights.py` writes `insights.csv` (one row per post, latest numbers; `tools/test_insights.py` tests it offline)
- `exclusions.txt` tickers never to feature (holdings and conflicts). `featured.txt` everything already featured (no repeats within 180 days)
