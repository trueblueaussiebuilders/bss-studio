# Content guide

## The two formats

**Mon / Wed / Fri: the stock breakdown.** One ASX-listed speculative mining company (explorer or early developer, roughly under A$500m market cap) with something genuinely happening. Rotate commodities and jurisdictions through the week. Never a ticker in `exclusions.txt`, never a repeat within 180 days (`featured.txt`).

**Sunday: the big picture.** One topic that moves the whole sector, explained simply: a commodity price move and why, what AISC or capex means, why the AUD matters to miners, China export controls, how a capital raise works, what a JORC resource is, what drives uranium contracts, and so on. `META["kind"] = "macro"`, no ticker, `META["chip"] = "SUNDAY BRIEF"`, `META["cover_word"]` is the big cover word (e.g. "GOLD", "AISC").

## Editorial rules (these keep the account on the right side of ASIC INFO 269)

- Factual information, not advice. Explain what the company is, what it owns, the numbers, the catalysts, and both sides. Never say or imply buy, sell, hold, cheap, undervalued, price targets or "could go 10x". `tools/check.py` blocks the common phrases, but the test is whether a reasonable viewer would take it as a recommendation.
- Make it interesting with the story, not the hype: the history, the geology, the geopolitics, the catalyst calendar. Questions in hooks are fine ("Can a 1950s mine come back?").
- Every video has a "both sides" scene (`versus`) with real risks: dilution, no resource, permitting, funding, commodity price, sovereign risk.
- Every number comes from a source listed in `SOURCES` (ASX announcements first). Put the price date in `META["asof"]`. Mark approximations ("~A$23m"). Never invent a figure; if you can't verify it, leave it out.
- Narration: 100 to 125 words (about 45 seconds). Short sentences. Say numbers the way a person would ("zero point five six percent", "twenty-three million dollar"). No "mate", no slang.
- Caption: what it is, "What's interesting" and "What could go wrong" bullets, data date line, the standard disclaimer, 6 to 8 hashtags ending with #blackswanstocks.

## Spec format (`videos/YYYY-MM-DD-slug/spec.py`)

```python
META = {"kind": "stock", "date": "2026-11-16", "ticker": "VKA", "company": "Viking Mines", "commodity": "tungsten",
        "asof": "Prices: 12 Nov 2026", "cover": ["Can a *1950s* tungsten", "mine come back?"]}
SCENES = [ {...}, ... ]   # first "hook", last "outro"; 7 to 9 scenes
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
| `timeline` | `events: [{when, text, done}]` (max 5) | catalysts |
| `versus` | `for: {title, points}`, `against: {title, points}` | both sides (always include) |
| `list` | `items: [str]` (max 5) | risks, steps, explainers |
| `big` | `value`+`prefix`/`suffix` or `text`, `caption`, `sub` | one number that matters |
| `outro` | optional `cta`, `disclaimer` | always last |
