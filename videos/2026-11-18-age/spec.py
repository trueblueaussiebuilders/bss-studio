"""Alligator Energy (ASX:AGE): the Samphire in-situ recovery uranium project near Whyalla, South Australia."""

META = {
    "kind": "stock",
    "date": "2026-11-18",
    "ticker": "AGE",
    "company": "Alligator Energy",
    "commodity": "uranium",
    "asof": "Prices: 17-18 Nov 2026",
    "cover": ["A uranium mine with", "*no pit* and no tunnels"],
}

SCENES = [
    {"type": "hook", "kicker": "ASX:AGE  ·  Uranium  ·  South Australia",
     "title": "A uranium mine with *no pit* and no tunnels",
     "chips": [{"label": "Share price", "text": "~3.1c"},
               {"label": "Market cap", "value": 150, "prefix": "~A$", "suffix": "m"},
               {"label": "Stage", "text": "Feasibility"}],
     "say": "This uranium mine would have no pit and no tunnels."},

    {"type": "map", "label": "The project", "title": "Uranium on the *steel city's* doorstep",
     "region": [135.6, -35.0, 139.4, -32.1], "inset": True,
     "pins": [{"name": "Samphire project", "sub": "~20 km from Whyalla", "lat": -33.20, "lon": 137.43,
               "kind": "project", "side": "left", "dy": 40},
              {"name": "Whyalla", "sub": "Steelworks and port", "lat": -33.03, "lon": 137.58, "kind": "town", "side": "right", "dy": -30}],
     "say": "Alligator Energy is studying Samphire, near Whyalla in South Australia."},

    {"type": "big", "label": "The method", "title": "Dissolve it, *pump it up*",
     "text": "70%", "caption": "uranium recovered in the field trial",
     "sub": "Field recovery trial, target pattern. Completed 30 Jun 2026.",
     "say": "The plan: pump a solution through the ore, and the uranium comes up dissolved. A trial recovered seventy percent."},

    {"type": "intercept", "label": "The drilling", "title": "The trend keeps *running south*",
     "holes": [{"id": "BBRM26-484", "from": 61.0, "width": 2.4, "depth": 90, "headline": "2.4m @ 2,025ppm", "sub": "eU3O8 from 61m"}],
     "note": "Downhole widths, grades from calibrated gamma logging. ASX releases 28 Jul and 7 Oct 2026.",
     "say": "New holes hit up to two thousand parts per million, further south."},

    {"type": "bars", "label": "The metal", "title": "Uranium vs *the study* price",
     "bars": [{"label": "Scoping study price (Dec 2023)", "value": 75},
              {"label": "Long-term contract price (31 Oct 2026)", "value": 99, "highlight": True}],
     "fmt": {"prefix": "US$", "suffix": "/lb", "dp": 0},
     "callout": {"text": "+32%", "caption": "long-term price vs the scoping study assumption"},
     "note": "Study price from the Dec 2023 scoping study. Long-term price: TradeTech indicator, 31 Oct 2026. U3O8 is priced per pound.",
     "say": "Its twenty twenty-three study assumed seventy-five US dollars a pound. Long-term contracts hit ninety-nine in October."},

    {"type": "stats", "label": "The numbers", "title": "Funded for the *study stage*",
     "items": [{"label": "Share price", "text": "~3.1c", "note": "17-18 Nov 2026"},
               {"label": "Market cap", "value": 150, "prefix": "~A$", "suffix": "m", "note": "approx., ~4.83bn shares"},
               {"label": "Cash", "value": 25.4, "prefix": "A$", "suffix": "m", "dp": 1, "note": "30 Sep 2026", "highlight": True},
               {"label": "Resource", "value": 30, "suffix": "Mlb", "note": "U3O8, Blackbush + Plumbush"}],
     "say": "It's worth about a hundred and fifty million dollars, with twenty-five million in cash."},

    {"type": "catalysts", "label": "What's next", "title": "What could *move* it",
     "items": [{"when": "Lodged 17 Nov", "status": "Next up", "title": "Federal environment (EPBC) referral",
                "why": "The decision sets how long federal approval takes"},
               {"when": "Late Q4 2026", "title": "End of the ~300-hole drill program",
                "why": "Tests whether Blackbush and Plumbush link up"},
               {"when": "2027 (targets)", "title": "Resource update, then feasibility study",
                "why": "First full test of costs and funding needs"}],
     "say": "What could move it? A federal environment referral, lodged this week. Results from three hundred holes by year end. Then a resource update and feasibility study in twenty twenty-seven."},

    {"type": "versus", "label": "Both sides", "title": "The *honest* scorecard",
     "for": {"title": "Going for it", "points": ["Trial hit the 70% recovery benchmark", "A$25.4m cash at 30 Sep",
                                                 "Long-term uranium above the study price"]},
     "against": {"title": "Working against it", "points": ["Mining lease still at application stage", "12Mlb of the resource is Inferred",
                                                          "Production target 2030-31, needs big funding"]},
     "say": "The catch: no mining lease yet, twelve million pounds of resource is inferred, and a mine needs far more money."},
]

CAPTION = """Alligator Energy (ASX:AGE) is studying an in-situ recovery (ISR) uranium mine at Samphire, about 20 km from Whyalla in South Australia. ISR pumps a solution through the ore underground and brings the uranium to surface dissolved, with no open pit or tunnels.

What's interesting
• Resource: 30 Mlb U3O8 after Plumbush was added in June 2026 (Blackbush 18 Mlb, Plumbush 12 Mlb Inferred)
• The field recovery trial, completed 30 June 2026, reached 70% uranium recovery over 70 pore volumes in its target pattern
• 2026 drilling hit 2.4m @ 2,025ppm eU3O8 (BBRM26-484) and extended the Blackbush trend about 1 km further south (7 Oct 2026)
• The Dec 2023 scoping study assumed US$75/lb. TradeTech's long-term uranium indicator was US$99/lb at 31 Oct 2026
• A$25.4m cash at 30 Sep 2026, after a A$15m placement and SPP at 4.5c in Aug-Sep 2026

What's coming
• EPBC Act referral for Samphire, lodged this week, then the regulator's decision on the level of assessment
• Completion of the ~300-hole drill program by late Q4 2026
• Updated Blackbush resource estimate, Q1-Q2 2027
• Samphire feasibility study, targeted for Q3 2027

What could go wrong
• The mining lease is at application stage, and state and federal approvals are still ahead
• 12 Mlb of the 30 Mlb resource is Inferred
• The 2023 scoping study put capex at ~A$131m, well above current cash, and production is targeted for 2030-31
• The shares are trading below the 4.5c placement price

Figures from ASX announcements to 17 Nov 2026. Share price and market cap approximate, as at 17-18 Nov 2026. Uranium prices move.

General information only, not financial advice. It doesn't consider your objectives, finances or needs. Speculative stocks can lose most or all of their value. We hold no position in AGE. Do your own research.

#ASX #ASXstocks #uranium #nuclear #SouthAustralia #miningstocks #smallcaps #blackswanstocks"""

SOURCES = [
    "https://quartr.com/companies/alligator-energy-limited_18355",  # Sep 2026 quarterly (30 Oct 2026): cash A$25.435m, E&E A$4.94m
    "https://smallcaps.com.au/article/alligator-energy-targets-2030-31-samphire-uranium-production-after-completing-frt",  # FRT 70%, 30 Mlb MRE, 2023 scoping US$75/lb, A$131m capex, ML application, 2030-31, 20 km Whyalla
    "https://kalkinemedia.com/au/news/announcements/alligator-energy-expands-uranium-mineralisation-600-metres-south-of-blackbush-at-samphire-project",  # 28 Jul 2026 intercepts, ~300 holes by end Q4 2026, MRE Q1/Q2 2027
    "https://investorpa.com/announcement/354039/",  # 7 Oct 2026: mineralisation ~1 km further south
    "https://www.marketopen.com.au/alligator-energy-asx-age-raises-a-15m-placement-and-launches-a-3m-share-purchase-plan",  # A$15m placement at 4.5c, FS Q3 2027
    "https://kalkinemedia.com/au/stocks/penny/alligator-energy-asxage-pushes-ahead-on-samphire-uranium-approvals",  # EPBC referral, 18 Nov 2026, ~3c
    "https://www.investsmart.com.au/security/asx/age/alligator-energy-limited/announcements",  # announcements list incl. 17 Nov EPBC referral; 3.2c
    "https://www.tipranks.com/stocks/AU:AGE",  # 4.83bn shares
    "https://www.cruxinvestor.com/posts/record-us-99-uranium-contract-price-favors-miners-with-supply-left-to-sell",  # TradeTech LT US$99/lb, 31 Oct 2026
]
