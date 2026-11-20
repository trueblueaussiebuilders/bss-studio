"""Pull per-post metrics for everything in posted.txt and write insights.csv.

  python publish/insights.py [--posted posted.txt] [--out insights.csv]

Env: IG_ACCESS_TOKEN, IG_USER_ID (same as publish/instagram.py).

One row per posted media (the latest snapshot), sorted by slug. Metrics the API doesn't support for a
media type, or has retired, are left blank rather than failing the run. If the token can't read insights
at all, the run fails with the permission Mathew needs to add in the Meta app.
"""
import argparse, csv, datetime, os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import instagram as ig  # noqa: E402

# Graph API metric name -> CSV column. Asked for in one call first; on error, one at a time.
REEL_METRICS = {"views": "views", "reach": "reach", "likes": "likes", "comments": "comments", "shares": "shares",
                "saved": "saves", "follows": "follows", "profile_visits": "profile_visits",
                "total_interactions": "total_interactions",
                "ig_reels_avg_watch_time": "avg_watch_time_s", "ig_reels_video_view_total_time": "total_watch_time_s"}
CAROUSEL_METRICS = {k: v for k, v in REEL_METRICS.items() if not k.startswith("ig_reels")}
MS_TO_S = {"avg_watch_time_s", "total_watch_time_s"}       # the API reports watch time in milliseconds

COLUMNS = ["slug", "posted", "media_id", "media_type", "permalink", "fetched_utc"] + list(REEL_METRICS.values())

def permission_help():
    if ig.token().startswith("EA"):    # Facebook Login token (what this account uses as of Nov 2026)
        return ("The token can read posts but not insights (error #10). It's a Facebook Login token, so in the Meta app "
                "(developers.facebook.com > your app > Use cases > Instagram API / Facebook Login > Permissions) add "
                "'instagram_manage_insights' (keep instagram_basic, instagram_content_publish, pages_show_list, "
                "pages_read_engagement), then generate a new long-lived token with that permission ticked "
                "(Graph API Explorer > Generate token) and replace the IG_ACCESS_TOKEN secret.")
    return ("The token can read posts but not insights (error #10). In the Meta app (developers.facebook.com > your app > "
            "Use cases > Instagram API > API setup with Instagram login) add 'instagram_business_manage_insights', "
            "generate a new token and replace the IG_ACCESS_TOKEN secret.")


def read_posted(path):
    rows = []
    for line in open(path):
        line = line.split("#", 1)[0].strip()
        parts = line.split()
        if len(parts) >= 3 and parts[2].isdigit():
            rows.append({"slug": parts[0], "posted": parts[1], "media_id": parts[2]})
    return rows


def is_permission_error(e):
    s = str(e)
    return any(k in s for k in ('"code":10,', '"code":10}', '"code":200', "permission", "Permission"))


def values(resp):
    """Flatten an /insights response into {metric: number}."""
    out = {}
    for m in resp.get("data", []):
        v = m.get("values", [{}])
        val = v[0].get("value") if v else None
        if val is None and "total_value" in m:
            val = m["total_value"].get("value")
        if isinstance(val, (int, float)):
            out[m["name"]] = val
    return out


def fetch_metrics(mid, wanted, log):
    """Ask for every metric at once; if the API rejects the set, ask one at a time and skip the rejects."""
    try:
        return values(ig.call("GET", f"{mid}/insights", {"metric": ",".join(wanted)}))
    except ig.ApiError as e:
        if is_permission_error(e) and "metric" not in str(e).lower():
            raise
        first = str(e)
    got, skipped = {}, []
    for m in wanted:
        try:
            got.update(values(ig.call("GET", f"{mid}/insights", {"metric": m})))
        except ig.ApiError as e:
            if is_permission_error(e) and "metric" not in str(e).lower():
                raise
            skipped.append(m)
    if skipped:
        log(f"  {mid}: skipped unsupported metrics {skipped} ({first[:160]})")
    return got


def collect(posted, log=print):
    now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M")
    out, perm_fail, other_fail = [], 0, 0
    for p in posted:
        row = dict(p, fetched_utc=now)
        try:
            info = ig.call("GET", p["media_id"], {"fields": "media_type,media_product_type,permalink,like_count,comments_count"})
        except ig.ApiError as e:
            other_fail += 1
            log(f"  {p['slug']} ({p['media_id']}): {str(e)[:240]}")
            out.append(row); continue
        # basic counts work without the insights permission, so they're kept even if /insights is refused
        row["media_type"] = info.get("media_product_type") or info.get("media_type", "")
        row["permalink"] = info.get("permalink", "")
        row["likes"], row["comments"] = info.get("like_count", ""), info.get("comments_count", "")
        metrics = REEL_METRICS if row["media_type"] in ("REELS", "VIDEO", "") else CAROUSEL_METRICS
        try:
            for k, v in fetch_metrics(p["media_id"], list(metrics), log).items():
                col = metrics[k]
                row[col] = round(v / 1000, 2) if col in MS_TO_S else v
        except ig.ApiError as e:
            if is_permission_error(e):
                perm_fail += 1
            else:
                other_fail += 1
            log(f"  {p['slug']} ({p['media_id']}) insights: {str(e)[:240]}")
        out.append(row)
    return out, perm_fail, other_fail


def write_csv(rows, path, previous=None):
    """Write the rows; keep the last good numbers for a media whose fetch failed this time."""
    prev = {}
    if previous and os.path.exists(previous):
        prev = {r["media_id"]: r for r in csv.DictReader(open(previous))}
    with open(path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=COLUMNS, extrasaction="ignore")
        w.writeheader()
        for r in sorted(rows, key=lambda r: (r["posted"], r["slug"])):
            full = [c for c in REEL_METRICS.values() if c not in ("likes", "comments")]
            p = prev.get(r["media_id"])
            if p and not any(r.get(c) not in (None, "") for c in full):
                if any(p.get(c) not in (None, "") for c in full) or not any(r.get(c) not in (None, "") for c in ("likes", "comments")):
                    r = dict(p, **{c: r[c] for c in ("likes", "comments") if r.get(c) not in (None, "")})
            w.writerow({c: r.get(c, "") for c in COLUMNS})


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--posted", default="posted.txt"); ap.add_argument("--out", default="insights.csv")
    a = ap.parse_args()
    posted = read_posted(a.posted)
    print(f"{len(posted)} posted media in {a.posted}")
    rows, perm_fail, other_fail = collect(posted)
    if posted and other_fail == len(posted):
        sys.exit("no media could be read (token or account problem?): see the errors above")
    write_csv(rows, a.out, previous=a.out)
    ok = len(posted) - perm_fail - other_fail
    print(f"wrote {a.out}: full metrics for {ok}/{len(posted)}" + (f"; {perm_fail + other_fail} with likes/comments only or previous numbers" if ok < len(posted) else ""))
    if perm_fail:
        print(f"::error::{permission_help()}")
        sys.exit(2)          # csv written (likes/comments), but insights need a permission: the workflow commits, then fails

if __name__ == "__main__":
    main()
