"""Leeuwin Metals (ASX:LM1): Marda gold project, WA, and Forrestania's growing stake."""

META = {
    "kind": "stock",
    "date": "2026-11-14",
    "ticker": "LM1",
    "company": "Leeuwin Metals",
    "commodity": "gold",
    "asof": "Prices: 13 Nov 2026",
    "cover": ["A gold producer is", "*buying in*"],
}

SCENES = [
    {"type": "hook", "kicker": "ASX:LM1  ·  Gold  ·  WA",
     "title": "Why is a gold miner building a stake in *this* explorer?",
     "chips": [{"label": "Share price", "text": "21c"},
               {"label": "Market cap", "value": 27, "prefix": "~A$", "suffix": "m"},
               {"label": "Gold resource", "text": "379koz"}],
     "say": "A soon-to-be gold producer has been building a stake in this explorer."},

    {"type": "map", "label": "The project", "title": "Old pits, *new* ounces",
     "region": [115.6, -33.2, 123.2, -28.6], "inset": True,
     "pins": [{"name": "Marda project", "sub": "~100 km N of Southern Cross", "lat": -30.33, "lon": 119.30, "kind": "project"},
              {"name": "Southern Cross", "lat": -31.23, "lon": 119.33, "kind": "town", "side": "right", "dy": 10},
              {"name": "Edna May mill", "sub": "Forrestania", "lat": -31.30, "lon": 118.69, "kind": "mine", "side": "left", "dy": 70}],
     "say": "Leeuwin Metals' Marda project sits about a hundred kilometres north of Southern Cross, around old open pits."},

    {"type": "bars", "label": "The resource", "title": "The resource is *growing*",
     "bars": [{"label": "Maiden resource (Dec 2025)", "value": 342.3},
              {"label": "Updated resource (Jul 2026)", "value": 378.6, "highlight": True}],
     "fmt": {"suffix": "koz", "dp": 0},
     "callout": {"text": "+142k", "caption": "to 186koz exploration target outside the resource. Not yet a resource."},
     "note": "Marda MRE 11.4Mt @ 1.03 g/t Au. ASX releases 10 Dec 2025, 29 Jul and 1 Sep 2026.",
     "say": "Drilling has grown its gold resource to about three hundred and seventy-nine thousand ounces."},

    {"type": "bars", "label": "The neighbour", "title": "Forrestania's stake, *rising*",
     "bars": [{"label": "June 2026", "value": 7.03},
              {"label": "24 August 2026", "value": 11.46},
              {"label": "28 August 2026", "value": 12.71, "highlight": True}],
     "fmt": {"suffix": "%", "dp": 1},
     "note": "ASX substantial holder notices. Further notices were filed in Oct and Nov 2026.",
     "say": "Forrestania, which is restarting two gold mills in WA, lifted its stake from seven to almost thirteen percent by late August."},

    {"type": "stats", "label": "The numbers", "title": "Small, and *still* exploring",
     "items": [{"label": "Share price", "text": "21c", "note": "13 Nov close"},
               {"label": "Market cap", "value": 27, "prefix": "~A$", "suffix": "m", "note": "approx."},
               {"label": "Cash", "value": 2.5, "prefix": "A$", "suffix": "m", "dp": 1, "note": "30 Sep 2026"},
               {"label": "Funding", "text": "~2 qtrs", "highlight": True, "note": "company estimate"}],
     "say": "Leeuwin is worth about twenty-seven million dollars, with two and a half million in cash."},

    {"type": "catalysts", "label": "What's next", "title": "What could *move* it",
     "items": [{"when": "Ongoing", "status": "Watch", "title": "Forrestania's next move",
                "why": "Changes of 1% or more are disclosed to the ASX"},
               {"when": "Second half 2026", "title": "Drilling outside the resource",
                "why": "Tests regional targets like Red Boomerang"},
               {"when": "Company aim", "title": "Path to 500,000 ounces",
                "why": "The exploration target hints at more gold, but it isn't proven"}],
     "say": "So what could move it? Changes to Forrestania's stake, which have to be disclosed. Drilling outside the current resource. And the push toward half a million ounces."},

    {"type": "versus", "label": "Both sides", "title": "The *honest* scorecard",
     "for": {"title": "Going for it", "points": ["Resource up 11% this year", "A future producer on the register",
                                                 "Gold project with old pits on site"]},
     "against": {"title": "Working against it", "points": ["About two quarters of cash", "Exploration target isn't a resource",
                                                          "A big holder doesn't mean a deal"]},
     "say": "But with about two quarters of cash, another raise looks likely. And a big shareholder doesn't mean a takeover is coming."},
]

CAPTION = """Leeuwin Metals (ASX:LM1) is growing a gold resource at Marda, about 100km north of Southern Cross in WA. A would-be producer has been building a stake.

What's interesting
• Marda resource up from 342,300oz (Dec 2025) to 378,600oz @ 1.03 g/t (Jul 2026)
• Exploration target of 142,000 to 186,000oz outside the resource (an exploration target is not a resource)
• Forrestania Resources, restarting the Edna May and Lake Johnston mills, lifted its stake from 7.0% (Jun) to 12.7% (late Aug 2026). Further notices filed Oct and Nov

What's coming
• Any change in Forrestania's stake (disclosed via ASX notices)
• Regional drilling outside the resource
• The company's stated aim of 500,000oz+

What could go wrong
• ~A$2.5m cash at 30 Sep (company estimates ~2 quarters of funding), so a raise is likely
• Exploration targets may never become resources
• A large shareholder doesn't mean a takeover is coming

Figures from ASX announcements to 3 Nov 2026. Share price and market cap approximate, as at 13 Nov 2026.

General information only, not financial advice. It doesn't consider your objectives, finances or needs. Speculative stocks can lose most or all of their value. We hold no position in LM1. Do your own research.

#ASX #ASXstocks #gold #goldstocks #WAgold #juniorminers #smallcaps #blackswanstocks"""

SOURCES = [
    "https://bulletin.webull.com/qbd/announcement/20251210/499501828/2391c48dfc05892b706e99de398402f7.pdf",
    "https://kalkinemedia.com/au/news/announcements/leeuwin-metals-boosts-marda-gold-project-resource-to-378600oz-with-evanston-deposit-up-22-in-six-months",
    "https://bulletin.webull.com/qbd/announcement/20260901/499501828/548d31df8b07e9989e98a6b08225c46e.pdf",
    "https://bulletin.webull.com/qbd/announcement/20260612/499501828/4ce4b1f0e48145ff49c45070fc1826fb.pdf",
    "https://bulletin.webull.com/qbd/announcement/20260825/499501828/7fd65d8c317a9f5cf6356c97d7255dad.pdf",
    "https://bulletin.webull.com/qbd/announcement/20260902/499501005/b2aaa6bad14f31f0bf6c0cb9d6cb0758.pdf",
    "https://www.investsmart.com.au/security/asx/lm1/leeuwin-metals-ltd",
    "https://announcements.asx.com.au/asxpdf/20260924/pdf/074gxtv1lyy5xn.pdf",
    "https://bulletin.webull.com/qbd/announcement/20260728/499501828/46a798b46acf80d21492f2a9b4e7180f.pdf",
    "https://www.businessnews.com.au/article/Forrestania-fast-tracks-WA-gold-production-for-December",
]
