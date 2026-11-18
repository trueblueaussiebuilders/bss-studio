"""Publish a Reel via the Instagram API with Instagram Login.

  python publish/instagram.py post --video-url URL --caption-file FILE   -> prints media id
  python publish/instagram.py refresh --out FILE                          -> writes refreshed token to FILE
  python publish/instagram.py check                                        -> confirms token + account

Env: IG_ACCESS_TOKEN, IG_USER_ID
"""
import argparse, json, os, sys, time, urllib.parse, urllib.request, urllib.error

def host():
    """Instagram-login tokens (IG...) use graph.instagram.com; Facebook/unified-login tokens (EA...) use graph.facebook.com."""
    if os.environ.get("IG_HOST"): return os.environ["IG_HOST"]
    return "https://graph.facebook.com" if token().startswith("EA") else "https://graph.instagram.com"
VER = os.environ.get("IG_GRAPH_VERSION", "v26.0")


class ApiError(SystemExit):
    """An Instagram API error. Subclasses SystemExit so an uncaught one still ends the run with the message."""
    def __init__(self, msg, transient=False):
        super().__init__(msg); self.transient = transient


ATTEMPTS = int(os.environ.get("IG_POST_ATTEMPTS", "3"))   # fresh containers to try before giving up
BACKOFF = [30, 90, 180]                                     # seconds to wait before attempt 2, 3, 4


def token():
    # tolerate stray whitespace / quotes from copy-paste into GitHub secrets
    return os.environ.get("IG_ACCESS_TOKEN", "").strip().strip('"').strip("'").strip()


def diagnose():
    t = token(); uid = os.environ.get("IG_USER_ID", "").strip()
    kind = {"IG": "Instagram-login token", "EA": "Facebook/unified-login token"}.get(t[:2], "unrecognised")
    print(f"token: starts '{t[:2]}', length {len(t)}, looks like {kind}; contains spaces: {' ' in t}")
    print(f"user id: length {len(uid)}, all digits: {uid.isdigit()}")


def call(method, path, params, versioned=True):
    params = dict(params, access_token=token())
    url = f"{host()}/{VER}/{path}" if versioned else f"{host()}/{path}"
    data = None
    if method in ("GET", "DELETE"):
        url += "?" + urllib.parse.urlencode(params)
    else:
        data = urllib.parse.urlencode(params).encode()
    try:
        with urllib.request.urlopen(urllib.request.Request(url, data=data, method=method), timeout=120) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        body = e.read().decode(errors="replace")
        body = body.replace(token(), "***") if token() else body
        raise ApiError(f"Instagram API error {e.code} on {path}: {body}", transient=e.code >= 500 or '"is_transient":true' in body)


def check_hosted(url, expect_size=None, tries=12, pause=10):
    """Download the hosted video and confirm it's complete before Instagram is asked to fetch it.
    A HEAD check alone passed on 16 Nov 2026 yet Instagram's fetch still failed (error 2207082)."""
    last = ""
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers={"Cache-Control": "no-cache", "User-Agent": "bss-publish"})
            with urllib.request.urlopen(req, timeout=60) as r:
                ctype = r.headers.get("Content-Type", ""); clen = r.headers.get("Content-Length")
                body = r.read()
            problems = []
            if "video/mp4" not in ctype: problems.append(f"content-type {ctype!r}")
            if clen and int(clen) != len(body): problems.append(f"got {len(body)} of {clen} bytes")
            if expect_size and len(body) != expect_size: problems.append(f"size {len(body)} != local {expect_size}")
            if body[4:8] != b"ftyp": problems.append("not an MP4 (no ftyp box)")
            if not problems:
                print(f"hosted video OK: {len(body)} bytes, {ctype}")
                return True
            last = "; ".join(problems)
        except Exception as e:                # network hiccup, 404 while Pages propagates, etc.
            last = f"{type(e).__name__}: {e}"
        print(f"hosted video not ready ({last}), check {i + 1}/{tries}")
        time.sleep(pause)
    return False


def url_ok(url):
    try:
        with urllib.request.urlopen(urllib.request.Request(url, method="HEAD"), timeout=30) as r:
            return r.status == 200
    except Exception:
        return False


def make_container(uid, video_url, caption, cover_url):
    """Create one Reels container and wait for it. Returns its id, or raises ApiError."""
    params = {"media_type": "REELS", "video_url": video_url, "caption": caption, "share_to_feed": "true"}
    if cover_url: params["cover_url"] = cover_url
    cid = call("POST", f"{uid}/media", params)["id"]; print("container", cid)
    for _ in range(60):                       # up to ~10 min for Instagram to fetch + process the video
        st = call("GET", cid, {"fields": "status_code,status"})
        code = st.get("status_code"); print("status", code)
        if code == "FINISHED": return cid
        if code in ("ERROR", "EXPIRED"): raise ApiError(f"container failed: {st}", transient=True)
        time.sleep(10)
    raise ApiError(f"timed out waiting for Instagram to process container {cid}", transient=True)


def post(video_url, caption, cover_url=None, video_file=None, attempts=None, backoff=None):
    """Post a Reel. A failed container is never published, so a failed fetch or processing error is retried with a
    fresh container (after re-checking the hosted file). Only media_publish makes it live, and that runs once."""
    uid = os.environ["IG_USER_ID"].strip()
    attempts = attempts or ATTEMPTS; backoff = BACKOFF if backoff is None else backoff
    expect = os.path.getsize(video_file) if video_file and os.path.exists(video_file) else None
    cid, err = None, None
    for n in range(1, attempts + 1):
        if n > 1:
            wait_s = backoff[min(n - 2, len(backoff) - 1)] if backoff else 0
            print(f"retrying with a fresh container in {wait_s}s (attempt {n}/{attempts}) after: {err}")
            time.sleep(wait_s)
        if not check_hosted(video_url, expect):
            err = ApiError(f"hosted video at {video_url} never became complete", transient=True); continue
        cover = cover_url
        if cover and (n == attempts and n > 1 or not url_ok(cover)):
            print("::warning::posting without the custom cover (cover unreachable or last attempt)")
            cover = None
        try:
            cid = make_container(uid, video_url, caption, cover); break
        except ApiError as e:
            err = e; print(f"attempt {n} failed: {e}")
            if not e.transient: raise
    if not cid:
        sys.exit(f"gave up after {attempts} attempts: {err}")
    pub = call("POST", f"{uid}/media_publish", {"creation_id": cid})
    mid = pub["id"]
    info = call("GET", mid, {"fields": "permalink"})
    print("published", mid, info.get("permalink", ""))
    return mid


def wait(cid):
    for _ in range(60):
        st = call("GET", cid, {"fields": "status_code,status"})
        code = st.get("status_code"); print("status", cid, code)
        if code == "FINISHED": return
        if code in ("ERROR", "EXPIRED"): sys.exit(f"container failed: {st}")
        time.sleep(5)
    sys.exit("timed out waiting for Instagram to process the media")


def carousel(image_urls, caption):
    """Image carousel (JPEGs only, 2 to 10 images)."""
    uid = os.environ["IG_USER_ID"].strip()
    kids = []
    for u in image_urls:
        c = call("POST", f"{uid}/media", {"image_url": u, "is_carousel_item": "true"})
        wait(c["id"]); kids.append(c["id"])
    c = call("POST", f"{uid}/media", {"media_type": "CAROUSEL", "children": ",".join(kids), "caption": caption})
    wait(c["id"])
    pub = call("POST", f"{uid}/media_publish", {"creation_id": c["id"]})
    mid = pub["id"]
    print("published", mid, call("GET", mid, {"fields": "permalink"}).get("permalink", ""))
    return mid


def main():
    ap = argparse.ArgumentParser(); sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("post"); p.add_argument("--video-url", required=True); p.add_argument("--caption-file", required=True)
    p.add_argument("--id-file"); p.add_argument("--cover-url"); p.add_argument("--video-file")
    cp = sub.add_parser("carousel"); cp.add_argument("--image-urls", nargs="+", required=True)
    cp.add_argument("--caption-file", required=True); cp.add_argument("--id-file")
    r = sub.add_parser("refresh"); r.add_argument("--out", required=True)
    sub.add_parser("check")
    v = sub.add_parser("verify-hosted"); v.add_argument("--video-url", required=True); v.add_argument("--video-file")
    d = sub.add_parser("delete"); d.add_argument("media_ids", nargs="+")
    a = ap.parse_args()
    if a.cmd == "post":
        vf = a.video_file or a.caption_file.replace(".caption.txt", ".mp4")   # build/<slug>.mp4 sits beside the caption
        mid = post(a.video_url, open(a.caption_file).read().strip(), a.cover_url, vf)
        if a.id_file: open(a.id_file, "w").write(mid)
    elif a.cmd == "carousel":
        mid = carousel(a.image_urls, open(a.caption_file).read().strip())
        if a.id_file: open(a.id_file, "w").write(mid)
    elif a.cmd == "refresh":
        if token().startswith("EA"):
            print("Facebook/unified-login token: no self-refresh endpoint; check expiry in the 'check' output.")
            return
        res = call("GET", "refresh_access_token", {"grant_type": "ig_refresh_token"}, versioned=False)
        open(a.out, "w").write(res["access_token"])
        print("token refreshed, expires in", res.get("expires_in"), "s")
    elif a.cmd == "verify-hosted":           # used by dry runs: same pre-flight check a real post does, no Instagram calls
        if not check_hosted(a.video_url, os.path.getsize(a.video_file) if a.video_file else None):
            sys.exit(f"hosted video at {a.video_url} is missing, incomplete or not an MP4")
    elif a.cmd == "delete":
        for mid in a.media_ids:
            print(mid, call("DELETE", mid.strip(), {}))
    elif a.cmd == "check":
        diagnose()
        uid = os.environ["IG_USER_ID"].strip()
        if token().startswith("EA"):
            try:
                d = call("GET", "debug_token", {"input_token": token()}).get("data", {})
                exp = d.get("expires_at", 0)
                print(f"token type: {d.get('type')}, valid: {d.get('is_valid')}, expires: "
                      f"{'never' if exp == 0 else time.strftime('%Y-%m-%d', time.gmtime(exp))}, scopes: {d.get('scopes')}")
            except SystemExit as e:
                print("(couldn't inspect token)", str(e)[:200])
            me = call("GET", uid, {"fields": "username,name"})
            print("connected:", me.get("username"), "user_id", uid)
        else:
            me = call("GET", "me", {"fields": "user_id,username,account_type"})
            print("connected:", me.get("username"), me.get("account_type"), "user_id", me.get("user_id"))
        lim = call("GET", f"{os.environ['IG_USER_ID'].strip()}/content_publishing_limit", {"fields": "quota_usage,config"})
        print("publishing limit:", lim)


if __name__ == "__main__":
    main()
