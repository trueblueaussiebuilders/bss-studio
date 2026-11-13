# Content guide

## The two formats

**Mon / Wed / Fri: the stock breakdown (~55 s).** Typical order: hook → the metal or the angle → map → drilling or resource → numbers → catalysts → both sides (ends the video). One ASX-listed speculative mining company (explorer or early developer, roughly under A$500m market cap) with something genuinely happening. Rotate commodities and jurisdictions through the week. Never a ticker in `exclusions.txt`, never a repeat within 180 days (`featured.txt`).

**Sunday: the big picture.** One topic that moves the whole sector, explained simply: a commodity price move and why, what AISC or capex means, why the AUD matters to miners, China export controls, how a capital raise works, what a JORC resource is, what drives uranium contracts, and so on. `META["kind"] = "macro"`, no ticker, `META["chip"] = "SUNDAY BRIEF"`, `META["cover_word"]` is the big cover word (e.g. "GOLD", "AISC").

## Editorial rules (these keep the account on the right side of ASIC INFO 269)

- Factual information, not advice. Explain what the company is, what it owns, the numbers, the catalysts, and both sides. Never say or imply buy, sell, hold, cheap, undervalued, price targets or "could go 10x". `tools/check.py` blocks the common phrases, but the test is whether a reasonable viewer would take it as a recommendation.
- Make it interesting with the story, not the hype: the history, the geology, the geopolitics, the catalyst calendar. Questions in hooks are fine ("Can a 1950s mine come back?").
- **Open with a hook sentence** (12 words or fewer) that makes people stay: a tension, a contrast or a surprising fact, not the company name. "China controls most of the world's tungsten. This tiny explorer wants to bring an old American mine back." Then introduce the company.
- **Catalysts get real airtime** (about a quarter of the narration). Use a `catalysts` scene with 3 or 4 dated events and, for each, one plain line on why it matters (what it would prove or change). Where there's a factual precedent (a peer's share price reaction to the same kind of news, with source and date), a `bars` scene showing it is a strong addition. Describe what could move the story; never predict that it will.
- Every stock video has a "both sides" scene (`versus`) with real risks: dilution, no resource, permitting, funding, commodity price, sovereign risk.
- **End on the final point.** No spoken sign-off, no "not advice", no "follow for more". The last scene's narration is the last real point (usually the risks), and the disclaimer card appears at the bottom automatically.
- Every number comes from a source listed in `SOURCES` (ASX announcements first). Put the price date in `META["asof"]`. Mark approximations ("~A$23m"). Never invent a figure; if you can't verify it, leave it out.
- Narration: 120 to 135 words (about 55 seconds). The engine paces the graphics slowly; don't cram. Short sentences. Say numbers the way a person would ("zero point five six percent", "twenty-three million dollar"). No "mate", no slang.
- Caption: what it is, "What's interesting" and "What could go wrong" bullets, data date line, the standard disclaimer, 6 to 8 hashtags ending with #blackswanstocks.

## Spec format (`videos/YYYY-MM-DD-slug/spec.py`)

```python
META = {"kind": "stock", "date": "2026-11-16", "ticker": "VKA", "company": "Viking Mines", "commodity": "tungsten",
        "asof": "Prices: 12 Nov 2026", "cover": ["Can a *1950s* tungsten", "mine come back?"]}
SCENES = [ {...}, ... ]   # "hook" first, 6 to 8 scenes, no "outro" (the disclaimer end card is automatic)
CAPTION = """..."""
SOURCES = ["https://...", ...]
```

`*word*` in any title turns that word into red italic. Every scene has `say` (narration); most have `label` (small section label) and `title`.

| type | data | use it for |
|---|---|---|
| `hook` | `kicker`, `title`, `chips: [{label, text} or {label, value, prefix, suffix, dp}]` (max 3) | opener with the element tile |
| `map` | `region` (AU, WA, WA_SOUTH, GOLDFIELDS, PILBARA, QLD, NSW_VIC, SA_NT, USA, USA_WEST, NEVADA, CANADA, AFRICA, WEST_AFRICA, SOUTH_AMERICA, EUROPE, WORLD or `[lon0, lat0, lon1, lat1]`), `pins: [{name, sub, lat, lon, kind: project/mine/town, side, dy}]`, `links: [{from, to, label}]`, `areas: ["Nevada"]`, `highlight: [country]`, `inset: true` | where the project is, neighbours, distances |
| `stats` | `items: [{label, value, prefix, suffix, dp, note, highlight} or {label, text, ...}]` (2 to 6) | price, market cap, cash, EV, resource |
| `bars` | `bars: [{label, value, highlight}]`, `fmt`, `callout: {text, caption}`, `note` | peer comparisons, EV per ounce, price gaps |
| `line` | `series: [[label, value], ...]`, `fmt`, `annotations: [{at, text, above}]`, `color: "commodity"`, `note` | price history, commodity trends (only real data points) |
| `intercept` | `holes: [{id, from, width, depth, headline, sub}]` (max 2), `dip`, `note` | drill results |
| `stack` | `items: [{label, value}]`, `price: {label, value}`, `fmt`, `total_label`, `margin_label` | cost stacks vs price (great for Sundays) |
| `catalysts` | `items: [{when, title, why, status}]` (3 to 4) | what's coming and why each matters (required for stock videos) |
| `timeline` | `events: [{when, text, done}]` (max 5) | history or a longer calendar |
| `versus` | `for: {title, points}`, `against: {title, points}` | both sides (always include) |
| `list` | `items: [str]` (max 5) | risks, steps, explainers |
| `big` | `value`+`prefix`/`suffix` or `text`, `caption`, `sub` | one number that matters |
| `outro` | optional `cta`, `disclaimer` | not used any more (kept for old videos) |
