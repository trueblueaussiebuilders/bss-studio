"""Offline tests for publish/instagram.py's retry logic (no Instagram calls). Run: python3 tools/test_publish.py

Serves a real MP4 from a local web server and fakes the Graph API, checking that:
  1. a container that fails with 2207082 is retried with a fresh container and published exactly once
  2. if every attempt fails, nothing is published and the run exits non-zero
  3. a truncated / wrong-size hosted file is caught before Instagram is asked to fetch it
  4. a non-transient API error (e.g. bad token) is not retried
"""
import functools, http.server, os, sys, tempfile, threading

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "publish"))
import instagram as ig  # noqa: E402

os.environ.setdefault("IG_USER_ID", "123"); os.environ.setdefault("IG_ACCESS_TOKEN", "IGtest")
ig.time.sleep = lambda s: None            # no real waiting in tests


def serve(folder):
    class H(http.server.SimpleHTTPRequestHandler):
        def log_message(self, *a): pass
    srv = http.server.ThreadingHTTPServer(("127.0.0.1", 0), functools.partial(H, directory=folder))
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    return f"http://127.0.0.1:{srv.server_port}"


class FakeAPI:
    def __init__(self, statuses, create_error=None):
        self.statuses = list(statuses); self.containers = []; self.published = []; self.create_error = create_error
        self.covers = []

    def __call__(self, method, path, params, versioned=True):
        if method == "POST" and path.endswith("/media"):
            if self.create_error: raise self.create_error
            cid = f"c{len(self.containers) + 1}"; self.containers.append(cid); self.covers.append(params.get("cover_url"))
            self.current = self.statuses.pop(0); return {"id": cid}
        if method == "POST" and path.endswith("/media_publish"):
            self.published.append(params["creation_id"]); return {"id": "m1"}
        if method == "GET" and path.startswith("c"):
            return {"status_code": self.current, "status": "Error: Media upload has failed with error code 2207082"
                    if self.current == "ERROR" else ""}
        if method == "GET" and path == "m1":
            return {"permalink": "https://instagram.com/reel/x"}
        raise AssertionError((method, path))


def main():
    d = tempfile.mkdtemp()
    mp4 = os.path.join(d, "v.mp4")
    src = sys.argv[1] if len(sys.argv) > 1 else None
    data = open(src, "rb").read() if src else b"\x00\x00\x00\x18ftypmp42" + b"\x00" * 50000
    open(mp4, "wb").write(data); open(os.path.join(d, "c.jpg"), "wb").write(b"\xff\xd8jpeg")
    base = serve(d); url = f"{base}/v.mp4"; cover = f"{base}/c.jpg"
    fails = 0

    def check(name, cond):
        nonlocal fails
        print(("PASS " if cond else "FAIL ") + name); fails += 0 if cond else 1

    api = FakeAPI(["ERROR", "FINISHED"]); ig.call = api
    mid = ig.post(url, "cap", cover, mp4)
    check("retries a failed container and publishes once", mid == "m1" and api.containers == ["c1", "c2"] and api.published == ["c2"])
    check("keeps the custom cover when it's reachable and not the last attempt", api.covers[1] == cover)

    api = FakeAPI(["ERROR", "EXPIRED", "ERROR"]); ig.call = api
    try:
        ig.post(url, "cap", cover, mp4); check("exits when every attempt fails", False)
    except SystemExit as e:
        check("exits when every attempt fails", e.code is not None and api.published == [] and len(api.containers) == 3)
        check("last attempt drops the cover", api.covers[-1] is None)

    api = FakeAPI(["FINISHED"]); ig.call = api
    wrong = os.path.join(d, "bigger.mp4"); open(wrong, "wb").write(data + b"\x00")
    try:
        ig.post(url, "cap", cover, wrong); check("refuses a hosted file that doesn't match the local build", False)
    except SystemExit:
        check("refuses a hosted file that doesn't match the local build", api.containers == [] and api.published == [])

    api = FakeAPI(["FINISHED"], create_error=ig.ApiError("Instagram API error 400 on 123/media: bad token")); ig.call = api
    try:
        ig.post(url, "cap", cover, mp4); check("doesn't retry a non-transient error", False)
    except SystemExit:
        check("doesn't retry a non-transient error", api.published == [])

    check("missing hosted file is caught", ig.check_hosted(f"{base}/missing.mp4", tries=2, pause=0) is False)
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
