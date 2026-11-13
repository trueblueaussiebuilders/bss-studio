"""Print the video to post today (Melbourne date), or nothing.

Only a video whose folder starts with today's date is posted, so a missed build never posts stale prices.
"""
import datetime as dt, os, sys
from zoneinfo import ZoneInfo

root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
read = lambda n: [l.strip() for l in open(os.path.join(root, n)) if l.strip() and not l.startswith("#")] \
    if os.path.exists(os.path.join(root, n)) else []
today = os.environ.get("POST_DATE") or dt.datetime.now(ZoneInfo("Australia/Melbourne")).date().isoformat()
posted = {l.split()[0] for l in read("posted.txt")}
for slug in read("queue.txt"):
    if slug.startswith(today) and slug not in posted and os.path.exists(os.path.join(root, "videos", slug, "spec.py")):
        print(slug); sys.exit(0)
