# Improvements

One tested improvement ships each run (see `tools/CLAUDE_TASK.md` / the scheduled task). Newest first.

## What's working

No `insights.csv` yet, so no data-driven patterns. Building the insights workflow (backlog #1) unlocks this section.

## Changelog

### 2026-11-18: Publish retries with a fresh container, and a full check of the hosted video
- **What changed:** `publish/instagram.py post` now downloads the hosted MP4 before asking Instagram to fetch it and checks it is complete (HTTP 200, `video/mp4`, Content-Length matches the bytes received, size matches the local build in `build/<slug>.mp4`, starts with an `ftyp` box). If a container ends in `ERROR`/`EXPIRED` (e.g. 2207082 "Media upload has failed") or processing times out, it waits (30s, then 90s) and tries again with a fresh container, up to 3 attempts (`IG_POST_ATTEMPTS`). A failed container is never published, so retries can't double-post; `media_publish` still runs exactly once. Non-transient API errors (bad token, permissions) are not retried. If the custom cover URL is unreachable, or on the last attempt, it posts without the custom cover rather than not posting. New `verify-hosted` subcommand, run by dry runs of `post.yml`, so a dry run now tests the same pre-flight check from GitHub's runners.
- **Why:** the 16 Nov 2026 post (2026-11-16-srz) failed once with container error 2207082 after the HEAD-only URL check passed, and the run gave up with no retry.
- **Tests:** `python3 tools/test_publish.py [some.mp4]` (offline: local web server + fake Graph API): retry then publish once, give up without publishing, refuses a hosted file that doesn't match the build, doesn't retry non-transient errors.
- **First video:** 2026-11-18-age (tonight's post).
- **Files:** `publish/instagram.py`, `.github/workflows/post.yml` (dry-run verify step), `tools/test_publish.py`.

## Backlog (ranked)

1. **Insights workflow** (`.github/workflows/insights.yml`, daily + workflow_dispatch): read media IDs from `posted.txt`, pull each Reel's metrics from the Graph API (views, reach, likes, comments, shares, saves, follows, avg and total watch time; skip unsupported metrics without failing), commit `insights.csv`. Impact: everything else in this list should be ranked by real retention data instead of guesses.
2. **check.py layout guard for the bottom 20%:** a 4-item `catalysts` scene pushed its last card into the subtitle zone on 2026-11-18 (fixed in the spec by merging two items). Measure scene content height at render time and fail `--sheet` builds (or auto-tighten card spacing) when content crosses y = 80%. Same check for `big` scene `sub` text, which doesn't wrap and ran off both edges at ~85 characters. Impact: removes the most common manual fix each run.
3. **Map zoom from Australia to the project:** open map scenes on the whole continent and ease into the region over ~1s. Close regions (under ~3 degrees wide) also show the coarse Natural Earth coastline; a higher-resolution outline for close zooms would help. Impact: more motion in the first third, clearer sense of place.
4. **Hook number animates in + faster first cut:** count-up on the hook's headline figure and a cut to scene 2 by ~2.5s. Impact: scroll-stop in the first 1.5s.
5. **Price-history line with announcements marked:** a real 6-12 month share-price `line` scene with dated announcement markers (needs a reliable price source in the build). Impact: shows what news has moved the stock before, without predicting.
6. **Subtle sound design:** soft tick on number reveals and bar growth, ducked under the voice. Impact: retention through the middle third.
7. **"What happened next" follow-ups:** a short format revisiting a featured stock after its catalyst lands. Impact: series value, gives people a reason to follow.

## Tried and dropped

(none yet)
