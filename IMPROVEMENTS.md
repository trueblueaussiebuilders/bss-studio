# Improvements

One tested improvement ships each run (see `tools/CLAUDE_TASK.md` / the scheduled task). Newest first.

## What's working

`insights.csv` exists from 20 Nov 2026, but only likes and comments so far: the token still lacks the insights permission (daily runs on 21 and 22 Nov still fail with error #10). Seven posts, 0 to 2 likes each and no comments: too early and too thin for patterns. Once views, watch time, shares and saves arrive, compare hooks, commodities, scene types and lengths here.

## Changelog

### 2026-11-22: Maps open on Australia and zoom into the project
- **What changed:** every `map` scene now opens zoomed out on the whole of Australia (or, overseas, the smallest continent-scale region around it, e.g. the USA for Nevada) with the target area outlined in red and a dot on the project, then eases into the region over ~1.4s (`MAP_ZOOM` in `engine/scenes.py`). The camera zooms geometrically and moves its centre so the target stays steady in view (no swing). The outline fades as the zoom lands; pins, links, town labels and the inset arrive straight after (about 0.65s later than before). Regions that are already continent-wide (AU, USA, WORLD) don't zoom. New optional spec fields: `zoom: False` and `zoom_from`. Also fixed a pre-existing bug: Fiji's ring is split at the antimeridian and drew as a thin line across any map that reached it (any AU-wide map).
- **Why:** backlog #2. Close-up maps like 2026-11-20 Mt Martin showed three pins on an empty background with no coastline, so viewers had no sense of where the project is. The zoom gives the place in the first second of the scene and adds motion in the first third of the video.
- **Tests:** `python3 tools/test_map_zoom.py`: start regions (Australia for WA, Qld, Tas and SA close-ups; USA for USA_WEST and Nevada; Africa for West Africa), no zoom for AU/USA/WORLD, `zoom_from` override, camera starts and lands exactly on the two views, no antimeridian slivers, and all 6 map scenes in videos/ render mid-zoom and at rest. `tools/check.py` and `--sheet` builds pass for all 8 videos (rest frames unchanged). Mid-zoom frames checked for ALM (Qld), LM1 (WA), SRZ (Tas), AGE (SA), LEX (WA) and VKA (USA). Full build of 2026-11-20-lex: 52.1s, unchanged, zoom smooth at 30fps. Today's video (no map) rebuilt: 57.2s, max -1.4 dB.
- **First video:** the next stock video (Monday 23 Nov 2026). Today's Sunday brief has no map.
- **Files:** `engine/scenes.py`, `engine/geo.py`, `tools/test_map_zoom.py`, `CONTENT.md` (map fields), `BRAND.md` (new Motion section), `README.md`.

### 2026-11-20 (evening, Mathew's request): A real backing track on every video
- **What changed:** `engine/audio.py` gains `backtune()`, a generated backing track in three styles: **lofi** (84 bpm, swung kick/rim/hats, electric piano, warm low-pass and faint vinyl), **pulse** (104 bpm, soft four-on-the-floor, offbeat hats, 16th-note arpeggio, pulsing bass) and **ambient** (76 bpm, pad, plucks, slow heartbeat kick). Four minor-leaning chord loops and a transpose of -3 to +3 semitones. Keys and bass open the first bar and the beat drops in on bar 2. The style, loop and key are picked from the slug (crc32), so videos vary but rebuilds are identical; `META["music"]` can name a style or be `False`. The track now sits about 16 dB under the voice while speaking (was ~-21 dB of soft low sine pad that phone speakers barely reproduce) and ~14 dB under in pauses. The build prints the choice (`music: pulse (loop 1, transpose +2)`).
- **Why:** Mathew asked for a proper backtune like the True Blue Aussie Builders videos ("doesn't have to be the same music"). The old pad was nearly inaudible on a phone.
- **Tests:** `python3 tools/test_audio.py`: all 12 style/loop combinations render with no NaN or clipping and a steady level, the pick is deterministic and covers all styles, `music: False` leaves the voice untouched, and the track measures -15.4 dB under a test voice. Full builds: 2026-11-20-lex (pulse, 52.1s, -15.3 LUFS, true peak -1.3 dBFS; measured -15.8 dB under the real voice, -14.0 dB in gaps) and 2026-11-18-age (ambient, 58.4s, -15.1 LUFS, true peak -1.4 dBFS). Video frames unchanged; durations unchanged.
- **First video:** the next one (Sunday 22 Nov 2026).
- **Files:** `engine/audio.py`, `engine/build.py`, `tools/test_audio.py`, `CONTENT.md` (documents `META["music"]`), `BRAND.md` (new Sound section), `README.md`.

### 2026-11-20: Daily insights workflow (`insights.csv`)
- **What changed:** new `.github/workflows/insights.yml` (daily at 20:17 UTC, ~7:17am Melbourne, plus workflow_dispatch) runs `publish/insights.py`, which reads every media ID in `posted.txt`, pulls each post's basic counts (likes, comments, permalink, type) and its `/insights` metrics (views, reach, likes, comments, shares, saved, follows, profile_visits, total_interactions, ig_reels_avg_watch_time, ig_reels_video_view_total_time; watch time converted to seconds), and commits `insights.csv` (one row per post, latest snapshot) to main. Metrics the API rejects for a media type are skipped one by one rather than failing the run; carousels aren't asked for Reels-only metrics. A post that fails one day keeps its previous numbers. If the token lacks the insights permission, the run still saves likes and comments, commits, then fails with the exact permission to add.
- **Why:** backlog #1. Every other improvement should be ranked on real retention data instead of guesses.
- **Status:** run 44684492990 committed `insights.csv` with likes and comments for all 6 posts, then failed as designed: the token (Facebook Login, starts `EA`) gets error #10 on `/insights`. **Mathew needs to add `instagram_manage_insights` to the Meta app's permissions, generate a new long-lived token with it ticked, and replace the `IG_ACCESS_TOKEN` secret.** No code change needed after that; the next daily run fills in the rest.
- **Tests:** `python3 tools/test_insights.py` (offline, fake Graph API): all metrics land with watch time in seconds, unsupported metric skipped, carousel metric set, permission missing exits 2 after writing likes/comments, earlier full metrics are never wiped, a failed media keeps its previous numbers. `tools/test_publish.py` still passes (instagram.py untouched).
- **First video:** n/a (tooling). Today's video, 2026-11-20-lex, is unaffected (no engine change).
- **Files:** `publish/insights.py`, `.github/workflows/insights.yml`, `tools/test_insights.py`, `README.md`.

### 2026-11-18: Publish retries with a fresh container, and a full check of the hosted video
- **What changed:** `publish/instagram.py post` now downloads the hosted MP4 before asking Instagram to fetch it and checks it is complete (HTTP 200, `video/mp4`, Content-Length matches the bytes received, size matches the local build in `build/<slug>.mp4`, starts with an `ftyp` box). If a container ends in `ERROR`/`EXPIRED` (e.g. 2207082 "Media upload has failed") or processing times out, it waits (30s, then 90s) and tries again with a fresh container, up to 3 attempts (`IG_POST_ATTEMPTS`). A failed container is never published, so retries can't double-post; `media_publish` still runs exactly once. Non-transient API errors (bad token, permissions) are not retried. If the custom cover URL is unreachable, or on the last attempt, it posts without the custom cover rather than not posting. New `verify-hosted` subcommand, run by dry runs of `post.yml`, so a dry run now tests the same pre-flight check from GitHub's runners.
- **Why:** the 16 Nov 2026 post (2026-11-16-srz) failed once with container error 2207082 after the HEAD-only URL check passed, and the run gave up with no retry.
- **Tests:** `python3 tools/test_publish.py [some.mp4]` (offline: local web server + fake Graph API): retry then publish once, give up without publishing, refuses a hosted file that doesn't match the build, doesn't retry non-transient errors.
- **Verified:** dry run of `post.yml` for 2026-11-18 (run 44247862052) passed; the runner confirmed the hosted file (6,120,784 bytes, video/mp4) matched its build.
- **First video:** 2026-11-18-age (tonight's post).
- **Files:** `publish/instagram.py`, `.github/workflows/post.yml` (dry-run verify step), `tools/test_publish.py`.

## Backlog (ranked)

1. **check.py layout guard for the bottom 20%:** a 4-item `catalysts` scene pushed its last card into the subtitle zone on 2026-11-18 (fixed in the spec by merging two items). Measure scene content height at render time and fail `--sheet` builds (or auto-tighten card spacing) when content crosses y = 80%. Same check for `big` scene `sub` text, which doesn't wrap and ran off both edges at ~85 characters. Impact: removes the most common manual fix each run.
2. **Hook number animates in + faster first cut:** count-up on the hook's headline figure and a cut to scene 2 by ~2.5s. Impact: scroll-stop in the first 1.5s.
3. **Context for inland close-up maps:** after the zoom lands, inland regions (e.g. Mt Martin, south of Kalgoorlie) still show no coastline. Draw salt lakes (Natural Earth lakes), main highways or a scale bar so the place reads at rest. Impact: clearer maps for WA Goldfields stocks, the most common jurisdiction.
4. **Insights history:** append a dated row per post per day to `insights_history.csv` so views can be compared at the same age (e.g. 48 hours) instead of latest totals, which favour older posts. Impact: fair comparisons once the permission is on.
5. **Price-history line with announcements marked:** a real 6-12 month share-price `line` scene with dated announcement markers (needs a reliable price source in the build). Impact: shows what news has moved the stock before, without predicting.
6. **Subtle sound design:** soft tick on number reveals and bar growth, a short whoosh under the map zoom, and a riser into the catalysts scene, all ducked under the voice. Impact: retention through the middle third.
7. **`big` scene count-up for text values:** "16x" or "89%" in `text` currently appears static; parse a leading number and count it up like `value`. Impact: small, more motion on Sunday briefs.
8. **Match the music to the topic:** let Sunday explainers default to ambient and stock videos to lofi/pulse, or pick by commodity, once insights show whether style affects watch time. Impact: small, data-led.
9. **"What happened next" follow-ups:** a short format revisiting a featured stock after its catalyst lands (e.g. LEX's scoping study, Dec qtr 2026; China's rare earth decision, 10 Jan 2027). Impact: series value, gives people a reason to follow.

## Tried and dropped

(none yet)
