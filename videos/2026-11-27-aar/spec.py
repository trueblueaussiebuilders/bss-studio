"""Astral Resources (ASX:AAR): the Mandilla gold project, ~70 km south of Kalgoorlie, Western Australia."""

META = {
    "kind": "stock",
    "date": "2026-11-27",
    "ticker": "AAR",
    "company": "Astral Resources",
    "commodity": "gold",
    "asof": "Price: close 25 Nov 2026",
    "cover": ["Its best *gold* hit", "sits in 34 centimetres"],
}

SCENES = [
    {"type": "hook", "kicker": "ASX:AAR  ·  Gold  ·  WA Goldfields",
     "title": "Its best *gold* hit ever, mostly in 34 centimetres",
     "stat": {"value": 13.5, "suffix": " g/t", "dp": 1, "caption": "gold over 31m, incl. 0.34m @ 1,146 g/t"},
     "chips": [{"label": "Resource", "value": 1.74, "suffix": " Moz", "dp": 2},
               {"label": "Cash", "value": 59, "prefix": "A$", "suffix": "m", "dp": 0},
               {"label": "Next", "text": "DFS, Mar qtr"}],
     "say": "Its best gold hit ever. Most of it sits in thirty-four centimetres."},

    {"type": "map", "label": "The project", "title": "Gold country, *south* of Kalgoorlie",
     "region": [120.7, -31.75, 122.25, -30.45], "inset": True,
     "pins": [{"name": "Mandilla", "sub": "Theia deposit", "lat": -31.37, "lon": 121.40,
               "kind": "project", "side": "left", "dy": 30},
              {"name": "Kalgoorlie", "sub": "Goldfields hub", "lat": -30.75, "lon": 121.47, "kind": "town", "side": "right", "dy": -20},
              {"name": "Kambalda", "sub": "Mining town", "lat": -31.20, "lon": 121.66, "kind": "town", "side": "right", "dy": 20}],
     "links": [{"from": "Mandilla", "to": "Kalgoorlie", "label": "~70 km"}],
     "say": "Astral Resources owns Mandilla, about seventy kilometres south of Kalgoorlie in Western Australia."},

    {"type": "big", "label": "The resource", "title": "Big, but *low grade*",
     "value": 1.74, "suffix": " Moz", "dp": 2, "caption": "gold resource at Mandilla, April 2026",
     "sub": "53.5Mt @ 1.0 g/t. Theia is ~1.4 Moz of it.",
     "say": "It holds one point seven four million ounces of gold, at about one gram per tonne."},

    {"type": "bars", "label": "The new hits", "title": "Deep holes, *side by side*",
     "bars": [{"label": "Mandilla resource average", "value": 1.0},
              {"label": "AMRCD515, 40m from 332m", "value": 3.3},
              {"label": "AMRCD468A, 31m from 288m", "value": 13.5, "highlight": True}],
     "fmt": {"suffix": " g/t Au", "dp": 1},
     "callout": {"text": "0.34m", "caption": "at 1,146 g/t carries most of that 31m average"},
     "note": "Downhole widths. Below the April 2026 resource pit shell. ASX, 10 Nov 2026.",
     "say": "This month, one hole hit thirty-one metres at thirteen and a half grams, below the planned pit. But most of that came from one thirty-four centimetre sliver."},

    {"type": "stats", "label": "The numbers", "title": "Funded through the *study*",
     "items": [{"label": "Share price", "text": "13c", "note": "close, 25 Nov 2026"},
               {"label": "Market cap", "value": 235, "prefix": "~A$", "suffix": "m", "dp": 0, "note": "~1.81bn shares"},
               {"label": "Cash", "value": 59.0, "prefix": "A$", "suffix": "m", "dp": 1, "note": "30 Sep 2026", "highlight": True},
               {"label": "PFS output", "value": 95, "suffix": " koz/yr", "dp": 0, "note": "first 12 years, June 2025"}],
     "say": "It's valued near two hundred and thirty-five million dollars, with fifty-nine million in cash."},

    {"type": "catalysts", "label": "What's next", "title": "What could *move* it",
     "items": [{"when": "Pending", "status": "Next up", "title": "Assays for deep holes 516 and 575",
                "why": "Tests whether the deep grade repeats"},
               {"when": "Dec qtr 2026", "title": "Clearing, mine plan and works approvals lodged",
                "why": "Starts the main WA permits to build"},
               {"when": "Mar qtr 2027", "title": "Definitive feasibility study",
                "why": "First full costing, then a decision to build"}],
     "say": "What could move it? Assays for more deep holes are pending. Approval applications are planned this quarter. And the feasibility study is due by March, with a decision to build after it."},

    {"type": "versus", "label": "Both sides", "title": "The *honest* scorecard",
     "for": {"title": "Going for it", "points": ["1.74 Moz, ~70 km from Kalgoorlie", "1.08 Moz group ore reserve",
                                                 "A$59m cash, native title deal signed"]},
     "against": {"title": "Working against it", "points": ["About 1 g/t overall", "Top hit leans on 0.34 metres",
                                                          "Standalone plant needs funding"]},
     "say": "The catch: it's low grade overall, the full build cost isn't known yet, and a standalone plant would need major funding."},
]

CAPTION = """Astral Resources (ASX:AAR) owns the Mandilla gold project, about 70 km south of Kalgoorlie in Western Australia. Most of Mandilla's gold is in the Theia deposit. A definitive feasibility study is under way.

What's interesting
• Mandilla resource of 53.5Mt @ 1.0 g/t Au for 1.74Moz (April 2026), including ~1.4Moz at Theia; group ore reserve 36.6Mt @ 0.9 g/t for 1.08Moz (Mandilla and Feysville)
• Deep hole AMRCD468A: 31m @ 13.5 g/t from 288m, including 0.34m @ 1,146 g/t, the company's highest assay yet; AMRCD515: 40m @ 3.30 g/t from 332m, below the resource pit shell (ASX, 10 Nov 2026)
• Pre-feasibility study (June 2025): a 2.75 Mtpa plant producing ~95koz a year for the first 12 years
• A$59.0m cash at 30 Sep 2026; native title land use agreement signed

What's coming
• Assays pending for deep holes AMRCD516 and AMRCD575; the 25-hole Theia Deeps program runs into the March 2027 quarter
• Clearing permit, mine plan and works approval applications planned for the December 2026 quarter
• Definitive feasibility study targeted for the March 2027 quarter, with a final investment decision after it

What could go wrong
• Mandilla is low grade overall (about 1 g/t), so costs and the gold price matter a lot
• Most of AMRCD468A's 31m average comes from a single 0.34m interval; widths are downhole
• The full capital cost won't be known until the feasibility study; a standalone plant would need debt and/or equity, which could dilute holders
• Approvals, heritage surveys and water licences still to come

Figures from ASX announcements to 10 Nov 2026 and the September 2026 quarterly. Price is the ASX close on 25 Nov 2026; market cap is approximate (~1.81bn shares). Map location is approximate.

General information only, not financial advice. It doesn't consider your objectives, finances or needs. Speculative stocks can lose most or all of their value. We hold no position in AAR. Do your own research.

#ASX #ASXstocks #gold #Kalgoorlie #miningstocks #juniorminers #smallcaps #blackswanstocks"""

SOURCES = [
    "https://www.investsmart.com.au/security/asx/aar/astral-resources-nl/announcements",  # ASX 10 Nov 2026 "Theia Deeps Drilling Delivers Highest Ever Assay Grade": AMRCD468A 31m @ 13.5 g/t from 288m incl 0.34m @ 1,146.3 g/t; AMRCD515 40m @ 3.30 g/t from 332m below Apr 2026 MRE pit shell; 516/575 pending; 25 holes 13,400m, complete Mar qtr 2027; MRE 53.5Mt @ 1.0 g/t 1.74Moz incl 1.4Moz Theia. Sep qtr 2026 report (29 Oct 2026): cash A$59.042m; ore reserves 36.6Mt @ 0.9 g/t 1.082Moz; DFS Mar qtr 2027 then FID; NVCP/MDCP/Works Approval submissions Dec qtr 2026; LUA covers DFS tenure. ~70 km south of Kalgoorlie (28 Sep 2026)
    "https://www.aspecthuntley.com.au/asxdata/20261029/pdf/03154991.pdf",  # Sep 2026 quarterly activities and cash flow report
    "https://www.investsmart.com.au/security/asx/aar/astral-resources-nl",  # price: last close A$0.130; market cap A$226m at A$0.125 (26 Nov 2026 intraday) => ~1.81bn shares
    "https://www.fool.com.au/tickers/asx-aar",  # close A$0.13 on 25 Nov 2026; 1.81 billion shares
    "https://kalkinemedia.com/au/news/announcements/astral-resources-updates-mandilla-gold-resource-to-174-million-ounces-amid-progress-on-definitive-feasibility-study",  # 27 Jul 2026: 1.74Moz; PFS 2.75Mtpa, ~95koz/yr first 12 years; Widgiemooltha greenstone belt; Marlinyu Ghoorlie LUA
    "https://smallcaps.com.au/article/astral-resources-approaching-the-development-crossroads-in-was-goldfields",  # Apr 2026: standalone plant funding, capex and permitting risks
]
