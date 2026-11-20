"""Offline tests for publish/insights.py (no Instagram calls). Run: python3 tools/test_insights.py

Fakes the Graph API and checks that:
  1. reels get every supported metric, watch time converted from ms to seconds
  2. a metric the API rejects (e.g. 'follows' on a Reel) is skipped, the rest still land
  3. carousels don't ask for Reels-only metrics
  4. if every media fails with a permission error, the run exits with the Meta app permission to add
  5. a media that fails this run keeps its previous numbers in insights.csv
"""
import csv, os, sys, tempfile

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "publish"))
import insights as ins  # noqa: E402
ig = ins.ig
os.environ.setdefault("IG_USER_ID", "123"); os.environ.setdefault("IG_ACCESS_TOKEN", "IGtest")

UNSUPPORTED = ig.ApiError('Instagram API error 400 on x/insights: {"error":{"message":"(#100) metric[0] must be one of the '
                          'following values: views, reach ...","code":100}}')
NO_PERM = ig.ApiError('Instagram API error 403 on x: {"error":{"message":"(#10) Application does not have permission '
                      'for this action","code":10,"type":"OAuthException"}}')


class FakeAPI:
    def __init__(self, reject=("follows",), perm=False):
        self.reject, self.perm, self.asked = set(reject), perm, []

    def __call__(self, method, path, params, versioned=True):
        if self.perm: raise NO_PERM
        mid = path.split("/")[0]
        if "/" not in path:
            kind = "CAROUSEL_ALBUM" if mid == "200" else "REELS"
            return {"media_type": kind, "media_product_type": "FEED" if kind == "CAROUSEL_ALBUM" else "REELS",
                    "permalink": f"https://instagram.com/p/{mid}", "like_count": 5, "comments_count": 1}
        wanted = params["metric"].split(","); self.asked.append((mid, wanted))
        if any(m in self.reject for m in wanted): raise UNSUPPORTED
        return {"data": [{"name": m, "values": [{"value": 12345 if "watch" in m or "total_time" in m else 7}]} for m in wanted]}


def main():
    fails = 0

    def check(name, cond):
        nonlocal fails
        print(("PASS " if cond else "FAIL ") + name); fails += 0 if cond else 1

    d = tempfile.mkdtemp(); posted = os.path.join(d, "posted.txt"); out = os.path.join(d, "insights.csv")
    open(posted, "w").write("# slug date id\ncarousel:launch  2026-11-13  200\n2026-11-14-lm1  2026-11-13  100\n")
    rows = ins.read_posted(posted)
    check("reads posted.txt and skips the comment line", [r["media_id"] for r in rows] == ["200", "100"])

    api = FakeAPI(); ig.call = api; logs = []
    got, perm, other = ins.collect(rows, log=logs.append)
    reel = [r for r in got if r["media_id"] == "100"][0]
    check("reel metrics land, watch time in seconds", reel["views"] == 7 and reel["avg_watch_time_s"] == 12.35
          and reel["total_watch_time_s"] == 12.35 and reel["saves"] == 7)
    check("unsupported metric skipped, not fatal", reel.get("follows") is None and perm == other == 0 and any("follows" in l for l in logs))
    asked200 = {m for mid, ms in api.asked if mid == "200" for m in ms}
    check("carousel doesn't ask for Reels-only metrics", not any(m.startswith("ig_reels") for m in asked200))
    ins.write_csv(got, out)
    saved = list(csv.DictReader(open(out)))
    check("csv written with a row per media", len(saved) == 2 and {r["slug"]: r["views"] for r in saved} == {"carousel:launch": "7", "2026-11-14-lm1": "7"})

    ig.call = FakeAPI(perm=True)
    old = sys.argv; sys.argv = ["insights.py", "--posted", posted, "--out", out]
    try:
        ins.main(); check("permission failure exits with the Meta permission to add", False)
    except SystemExit as e:
        check("permission failure exits with the Meta permission to add", e.code == 1)
    finally:
        sys.argv = old
    saved2 = list(csv.DictReader(open(out)))
    check("a failed run doesn't wipe insights.csv", saved2 == saved)

    class Partial(FakeAPI):
        def __call__(self, method, path, params, versioned=True):
            if path.startswith("100"): raise ig.ApiError("Instagram API error 500 on 100: oops", transient=True)
            return super().__call__(method, path, params, versioned)
    ig.call = Partial()
    got, perm, other = ins.collect(rows, log=lambda *a: None)
    ins.write_csv(got, out, previous=out)
    saved3 = {r["media_id"]: r for r in csv.DictReader(open(out))}
    check("a media that fails this run keeps its previous numbers", other == 1 and saved3["100"]["views"] == "7")

    print("all passed" if not fails else f"{fails} failed")
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
