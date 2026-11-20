"""Lefroy Exploration (ASX:LEX): the Mt Martin gold project on freehold Location 45, south of Kalgoorlie, WA."""

META = {
    "kind": "stock",
    "date": "2026-11-20",
    "ticker": "LEX",
    "company": "Lefroy Exploration",
    "commodity": "gold",
    "asof": "Prices: 19 Nov 2026",
    "cover": ["Kalgoorlie gold on", "*private* land"],
}

SCENES = [
    {"type": "hook", "kicker": "ASX:LEX  ·  Gold  ·  Western Australia",
     "title": "Kalgoorlie gold with *private* mineral rights",
     "chips": [{"label": "Share price", "text": "7.5c"},
               {"label": "Market cap", "value": 20, "prefix": "~A$", "suffix": "m"},
               {"label": "Stage", "text": "Scoping study"}],
     "say": "Near Kalgoorlie, this gold comes with rare private mineral rights."},

    {"type": "map", "label": "The project", "title": "On the gold capital's *doorstep*",
     "region": [120.95, -31.45, 122.2, -30.55], "inset": True,
     "pins": [{"name": "Mt Martin", "sub": "Freehold Location 45", "lat": -30.99, "lon": 121.55,
               "kind": "project", "side": "left", "dy": 0},
              {"name": "Kalgoorlie", "sub": "Super Pit, mills", "lat": -30.75, "lon": 121.47, "kind": "town", "side": "right", "dy": -20},
              {"name": "Kambalda", "sub": "Nickel and gold town", "lat": -31.20, "lon": 121.67, "kind": "town", "side": "left", "dy": 30}],
     "links": [{"from": "Mt Martin", "to": "Kalgoorlie", "label": "~30 km"}],
     "say": "Lefroy Exploration bought the mineral rights to Mt Martin, thirty kilometres south of Kalgoorlie, in twenty twenty-three."},

    {"type": "bars", "label": "The resource", "title": "460,000 ounces, *half unproven*",
     "bars": [{"label": "Indicated", "value": 200.5},
              {"label": "Inferred", "value": 259.5, "highlight": True}],
     "fmt": {"suffix": "koz", "dp": 1},
     "callout": {"text": "56%", "caption": "of the ounces are Inferred, the lowest confidence"},
     "note": "Mt Martin JORC 2012 resource, May 2026: 9.1Mt @ 1.6 g/t Au, 0.5 g/t cut-off, inside a A$7,000/oz pit shell.",
     "say": "The resource is four hundred and sixty thousand ounces. More than half is still inferred."},

    {"type": "intercept", "label": "The drilling", "title": "Gold from *twenty metres* down",
     "holes": [{"id": "East Shear", "from": 20, "width": 10, "depth": 60, "headline": "10m @ 3.80 g/t", "sub": "gold from 20m"},
               {"id": "Main Shear", "from": 35, "width": 6, "depth": 60, "headline": "6m @ 4.24 g/t", "sub": "gold from 35m"}],
     "note": "Mt Martin RC drilling, June 2026 quarter. Downhole widths. June 2026 quarterly report.",
     "say": "Drilling this year hit ten metres at three point eight grams, just twenty metres down."},

    {"type": "stats", "label": "The numbers", "title": "A small company, *thin* cash",
     "items": [{"label": "Share price", "text": "7.5c", "note": "close 19 Nov 2026"},
               {"label": "Market cap", "value": 20, "prefix": "~A$", "suffix": "m", "note": "approx., ~267m shares"},
               {"label": "Cash", "value": 2.0, "prefix": "~A$", "suffix": "m", "dp": 1, "note": "30 Sep 2026", "highlight": True},
               {"label": "Resource", "value": 460, "suffix": "koz", "note": "Mt Martin, gold"}],
     "say": "It's worth about twenty million dollars, with roughly two million in cash at the end of September."},

    {"type": "catalysts", "label": "What's next", "title": "What could *move* it",
     "items": [{"when": "Dec qtr 2026", "status": "Next up", "title": "Mt Martin scoping study, now with Burns",
                "why": "First look at mining costs and how big a mine could be"},
               {"when": "Mar qtr 2027", "title": "Lucky Strike restart (50:50 profit share)",
                "why": "Could bring in cash, if approvals land"},
               {"when": "Q1 2027", "title": "Shallow drilling at Mt Martin",
                "why": "Tests whether more ounces sit near surface"}],
     "say": "What could move it? A scoping study due this quarter, the first look at mining costs. A restart at the Lucky Strike mine early next year. Then shallow drilling at Mt Martin."},

    {"type": "versus", "label": "Both sides", "title": "The *honest* scorecard",
     "for": {"title": "Going for it", "points": ["460koz, 30 km from Kalgoorlie", "Shallow hits on three shears",
                                                 "Scoping study fully funded"]},
     "against": {"title": "Working against it", "points": ["~A$2m cash, under two quarters of spending", "56% of ounces Inferred",
                                                          "Study and restart dates have slipped"]},
     "say": "The catch: cash covered under two quarters of spending, most ounces are inferred, and key dates have already slipped once."},
]

CAPTION = """Lefroy Exploration (ASX:LEX) owns the mineral rights to Location 45, freehold land about 30 km south of Kalgoorlie in WA, bought from Franco-Nevada in 2023. Its Mt Martin deposit sits on that land, inside the wider Lefroy Gold Project.

What's interesting
• Mt Martin resource (May 2026): 9.1 Mt @ 1.6 g/t gold for 460,000 oz, of which 200,500 oz Indicated and 259,500 oz Inferred
• June 2026 quarter RC drilling hit 10m @ 3.80 g/t from 20m (East Shear) and 6m @ 4.24 g/t from 35m (Main Shear)
• The Mt Martin scoping study (lead consultant Measured Group) was expanded in Sep-Nov 2026 to include high-grade zones at Burns
• Lucky Strike is a 50:50 profit share with BML Ventures; its miscellaneous licence L25/71 was granted in Sep 2026

What's coming
• Mt Martin scoping study, with Burns, targeted for the December quarter 2026
• Lucky Strike dewatering and mining restart, targeted for the March quarter 2027, subject to approvals
• Shallow drilling at Mt Martin from Q1 2027

What could go wrong
• Cash was about A$2.0m at 30 Sep 2026, about 1.4 quarters of spending, and a A$2.5m BML facility is fully drawn
• 56% of Mt Martin's ounces are Inferred, the lowest confidence category
• A scoping study is preliminary and can't support a decision to mine
• The scoping study and the Lucky Strike restart have both been pushed back before

Figures from ASX announcements to 9 Nov 2026. Share price as at 19 Nov 2026 close; market cap approximate. Cash figure from the Sep 2026 quarterly cashflow report summary.

General information only, not financial advice. It doesn't consider your objectives, finances or needs. Speculative stocks can lose most or all of their value. We hold no position in LEX. Do your own research.

#ASX #ASXstocks #gold #Kalgoorlie #WesternAustralia #miningstocks #smallcaps #blackswanstocks"""

SOURCES = [
    "https://uploads.prod01.sydney.platformos.com/instances/532/assets/LEX-June-2026-Quarterly-Activities-Report.pdf?updated=1785298296",  # 31 Jul 2026: MRE 9.1Mt @ 1.6 g/t 460koz (Ind 200.5koz, Inf 259.5koz), Mt Martin RC intercepts, cash A$3.1m
    "https://www.investsmart.com.au/security/asx/lex/lefroy-exploration-limited/announcements",  # Sep 2026 quarterly (30 Oct): cash A$2.001m, ~1.44 quarters funding, BML A$2.5m facility drawn; 9 Nov scoping study update
    "https://www.investsmart.com.au/security/asx/lex/lefroy-exploration-limited/share-price",  # close 7.5c, 19 Nov 2026
    "https://stockanalysis.com/quote/asx/LEX/statistics/",  # 267.02m shares (Aug 2026)
    "https://discoveryalert.com/asx-stock-news/mining/lex-lefroy-exploration-mt-martin-scoping-study-november-2026/",  # 9 Nov 2026: scoping study Dec qtr, Lucky Strike Mar qtr 2027, L25/71 granted, Q1 2027 drilling
    "https://kalkinemedia.com/au/news/announcements/lefroy-exploration-broadens-mt-martin-scoping-study-to-integrate-burns-gold-deposit-high-grade-zones",  # 18 Sep 2026: scope expanded to Burns, postponed to Dec qtr
    "https://www.marketopen.com.au/lefroy-exploration-asxlex-raises-3-6m-to-accelerate-mt-martin-evaluation/",  # May 2026 A$3.6m placement at 12.5c
    "https://www.lefroyex.com/projects/mt-martin",  # ~30 km south of Kalgoorlie, Location 45 freehold, rights from Franco-Nevada May 2023
]
