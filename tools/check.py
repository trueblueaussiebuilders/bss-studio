"""Pre-flight checks for a video spec: structure, length, compliance wording, repeats and exclusions.

  python tools/check.py videos/2026-11-16-vka        -> exit 1 with reasons if anything fails
"""
import datetime as dt, importlib.util, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TYPES = {"hook", "map", "stats", "bars", "timeline", "catalysts", "versus", "list", "line", "intercept", "stack", "big", "outro"}

# Words that turn information into a recommendation or hype. Keep the account factual.
BANNED = [
    r"\bbuy\b", r"\bbuying\b", r"\bsell\b(?!-off)", r"\bselling\b", r"\bshould\b", r"\bmust\b", r"\bundervalued\b",
    r"\bovervalued\b", r"\bcheap\b", r"\bbargain\b", r"\bmoon\w*\b", r"\brocket\w*\b", r"\b\d+\s?x\s?(return|bagger)",
    r"\b(ten|multi)[- ]?bagger\b", r"\bguarantee\w*\b", r"\bcan'?t lose\b", r"\bprice target\b", r"\btarget price\b",
    r"\bnext big\b", r"\bdon'?t miss\b", r"\bget in\b", r"\bload up\b", r"\ball in\b", r"\beasy money\b",
    r"\bsure thing\b", r"\bwill (soar|explode|double|triple|rally|run)\b", r"\bupside of\b", r"\bfair value\b",
    r"\bworth (owning|a look|buying)\b", r"\bentry point\b", r"\bnot too late\b",
]
NEEDED_CAPTION = ["not financial advice", "do your own research", "#blackswanstocks"]


def load(folder):
    s = importlib.util.spec_from_file_location("spec", os.path.join(folder, "spec.py"))
    m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m


def lines(name):
    p = os.path.join(ROOT, name)
    return [l.strip() for l in open(p) if l.strip() and not l.startswith("#")] if os.path.exists(p) else []


def texts(sc):
    out = [sc.get("say", ""), sc.get("title", ""), sc.get("kicker", "")]
    for k in ("chips", "items", "bars", "events", "pins"):
        for it in sc.get(k, []) or []:
            out += [str(v) for v in (it.values() if isinstance(it, dict) else [it]) if isinstance(v, str)]
    for k in ("for", "against"):
        if k in sc: out += sc[k].get("points", [])
    return out


def main(folder):
    folder = folder.rstrip("/")
    slug = os.path.basename(folder)
    err, warn = [], []
    m = load(folder)
    meta, scenes, cap = m.META, m.SCENES, m.CAPTION
    if not slug.startswith(meta.get("date", "?")): err.append(f"folder name should start with META date {meta.get('date')}")
    if meta.get("kind") not in ("stock", "macro"): err.append("META kind must be 'stock' or 'macro'")
    types = [sc.get("type") for sc in scenes]
    if types[0] != "hook": err.append("first scene must be the hook")
    if "outro" in types: err.append("no outro scene: end on the final point (the disclaimer card is added automatically)")
    if meta.get("kind") == "stock":
        if "catalysts" not in types: err.append("stock videos need a 'catalysts' scene")
        if "versus" not in types: err.append("stock videos need a 'versus' (both sides) scene")
    first = re.split(r"(?<=[.!?])\s+", scenes[0].get("say", "").strip())[0]
    if len(first.split()) > 14: warn.append(f"hook opener is {len(first.split())} words; keep the first sentence punchy (<= 12)")
    if re.search(r"not (financial )?advice|follow for", " ".join(sc.get("say", "") for sc in scenes), re.I):
        err.append("don't say the disclaimer or a follow line in the narration; the end card covers it")
    for i, sc in enumerate(scenes):
        if sc.get("type") not in TYPES: err.append(f"scene {i}: unknown type {sc.get('type')}")
        if not sc.get("say"): err.append(f"scene {i}: no narration ('say')")
    words = sum(len(sc.get("say", "").split()) for sc in scenes)
    if not 115 <= words <= 140: warn.append(f"narration is {words} words; aim for 120-135 (~55s)")
    blob = "\n".join(t for sc in scenes for t in texts(sc)) + "\n" + cap
    for pat in BANNED:
        for hit in re.finditer(pat, blob, flags=re.I):
            ctx_ = blob[max(0, hit.start() - 30): hit.end() + 30].replace("\n", " ")
            err.append(f"compliance: '{hit.group(0)}' in ...{ctx_}...")
    low = cap.lower()
    for need in NEEDED_CAPTION:
        if need not in low: err.append(f"caption is missing '{need}'")
    if len(re.findall(r"#\w+", cap)) > 10: warn.append("more than 10 hashtags")
    if len(cap) > 2100: err.append("caption over Instagram's 2,200 character limit (keep a margin)")
    if not getattr(m, "SOURCES", None): err.append("SOURCES list is empty; every figure needs a source")
    if meta.get("kind") == "stock":
        tk = meta.get("ticker", "").upper()
        if tk in {x.split()[0].upper() for x in lines("exclusions.txt")}:
            err.append(f"{tk} is on exclusions.txt (a holding or conflict); pick another company")
        today = dt.date.fromisoformat(meta["date"])
        for l in lines("featured.txt"):
            d, t = l.split()[:2]
            if t.upper() == tk and l.split()[0] != meta["date"] and (today - dt.date.fromisoformat(d)).days < 180:
                err.append(f"{tk} was featured on {d}; no repeats within 180 days")
    for w_ in warn: print("WARN ", w_)
    for e in err: print("ERROR", e)
    print(f"{slug}: {words} words, {len(scenes)} scenes -> {'FAIL' if err else 'OK'}")
    return 1 if err else 0


if __name__ == "__main__":
    sys.exit(max(main(f) for f in sys.argv[1:]))
