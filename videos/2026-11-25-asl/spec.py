"""Andean Silver (ASX:ASL): the Cerro Bayo silver-gold project, Aysén region, southern Chile."""

META = {
    "kind": "stock",
    "date": "2026-11-25",
    "ticker": "ASL",
    "company": "Andean Silver",
    "commodity": "silver",
    "asof": "Price: 23 Nov 2026 (intraday)",
    "cover": ["A shut *silver* mine", "keeps finding veins"],
}

SCENES = [
    {"type": "hook", "kicker": "ASX:ASL  ·  Silver  ·  Chile",
     "title": "A shut *silver* mine keeps finding new veins",
     "stat": {"value": 1269, "suffix": " g/t", "caption": "silver equiv. over 1.7m, ~1 km from the plant"},
     "chips": [{"label": "Resource", "value": 136, "suffix": " Moz AgEq", "dp": 0},
               {"label": "Cash", "value": 70.5, "prefix": "~A$", "suffix": "m", "dp": 1},
               {"label": "Plant", "text": "On site, idle"}],
     "say": "A shut silver mine in Patagonia keeps finding new veins."},

    {"type": "map", "label": "The project", "title": "A mine on *care and maintenance*",
     "region": [-75.6, -48.6, -69.0, -44.6], "zoom_from": "SOUTH_AMERICA", "highlight": ["Chile"], "inset": True,
     "pins": [{"name": "Cerro Bayo", "sub": "Plant on care and maintenance", "lat": -46.54, "lon": -72.00,
               "kind": "project", "side": "left", "dy": 30},
              {"name": "Chile Chico", "sub": "Town", "lat": -46.54, "lon": -71.72, "kind": "town", "side": "right", "dy": 30},
              {"name": "Coyhaique", "sub": "Regional capital", "lat": -45.57, "lon": -72.07, "kind": "town", "side": "right", "dy": -20}],
     "say": "Andean Silver owns Cerro Bayo, in southern Chile. Coeur, then Mandalay, mined it until about twenty seventeen. The plant is still there."},

    {"type": "big", "label": "The resource", "title": "Drilling keeps *adding* ounces",
     "value": 136, "suffix": " Moz", "caption": "silver-equivalent resource, June 2026",
     "sub": "Up from 91 Moz in Oct 2024. 60 Moz Indicated. 20Mt @ 211 g/t AgEq.",
     "say": "Drilling has since grown the resource to a hundred and thirty-six million ounces of silver equivalent."},

    {"type": "bars", "label": "The new hits", "title": "Grade, *side by side*",
     "bars": [{"label": "Resource average", "value": 211},
              {"label": "Dagny, CBD359 (3.3m)", "value": 628},
              {"label": "Temer 4, 26LVDH016 (1.7m)", "value": 1269, "highlight": True}],
     "fmt": {"suffix": " g/t AgEq", "dp": 0},
     "callout": {"text": "6x", "caption": "the resource grade, but over just 1.7 metres"},
     "note": "Downhole widths. Holes ~1 km from the plant. ASX, 9 Nov 2026.",
     "say": "New holes, about a kilometre from the plant, hit up to six times the resource grade. But over narrow widths."},

    {"type": "stats", "label": "The numbers", "title": "Funded for the *next step*",
     "items": [{"label": "Share price", "text": "~A$1.30", "note": "23 Nov 2026, intraday"},
               {"label": "Cash", "value": 70.5, "prefix": "~A$", "suffix": "m", "dp": 1, "note": "30 Sep 2026", "highlight": True},
               {"label": "Placement", "value": 40, "prefix": "A$", "suffix": "m", "dp": 0, "note": "Sep 2026, for studies"},
               {"label": "Indicated", "value": 60, "suffix": " Moz", "dp": 0, "note": "silver equivalent"}],
     "say": "There's about seventy million dollars in cash, after a forty million dollar raise in September."},

    {"type": "catalysts", "label": "What's next", "title": "What could *move* it",
     "items": [{"when": "Underway", "status": "Next up", "title": "Follow-up holes on the new shoots",
                "why": "Tests whether narrow high grades hold width"},
               {"when": "H1 2027", "title": "Resource update, incl. Temer 4",
                "why": "Shows how much the new drilling adds"},
               {"when": "Underway", "title": "Restart and economic studies",
                "why": "First costed answer on restarting the plant"}],
     "say": "What could move it? Follow-up holes on the new shoots. A resource update in the first half of next year. And restart studies, paid for by that raise."},

    {"type": "versus", "label": "Both sides", "title": "The *honest* scorecard",
     "for": {"title": "Going for it", "points": ["136 Moz AgEq, 60 Moz Indicated", "Existing plant ~1 km away",
                                                 "~A$70.5m cash (30 Sep)"]},
     "against": {"title": "Working against it", "points": ["Best hits are 1 to 3 metres wide", "No economic study yet",
                                                          "Restart needs capital and permits"]},
     "say": "The catch: the best hits are narrow, there's no economic study yet, and a restart needs capital and Chilean permits."},
]

CAPTION = """Andean Silver (ASX:ASL) owns Cerro Bayo, a silver-gold mine in the Aysén region of southern Chile. Coeur and then Mandalay Resources ran it, mining stopped around 2017, and its processing plant is on care and maintenance. Andean is drilling around it with a view to a restart.

What's interesting
• Resource of 20Mt @ 211 g/t AgEq for 136Moz AgEq, including 60Moz Indicated (June 2026), up from 91Moz in Oct 2024
• New high-grade shoots about 1 km from the plant, e.g. 1.7m @ 1,269 g/t AgEq at Temer 4 (26LVDH016) and 3.3m @ 628 g/t AgEq at Dagny (CBD359) (ASX, 9 Nov 2026)
• About A$70.5m cash at 30 Sep 2026, after a A$40m placement in September to speed up economic studies

What's coming
• Follow-up drilling on the Lucia veins at Dagny and the shallow zone above Trinidad
• Resource update in H1 2027, including Temer 4 and Delia SE
• Restart and economic studies; greenfield drilling at Droughtmaster is being permitted for 2027

What could go wrong
• Many of the best intercepts are narrow (1 to 3 metres downhole) and would be diluted in a mine plan
• No economic study yet; restarting the plant needs capital, permits and more metallurgical work
• Silver-equivalent grades depend on assumed metal prices and recoveries
• Chilean permitting and community approvals; more raisings would dilute holders

Figures from ASX announcements and company news to 9 Nov 2026. Price is an intraday ASX price on 23 Nov 2026; we couldn't verify a current market cap. Map location from the drill collar coordinates; town labels for context.

General information only, not financial advice. It doesn't consider your objectives, finances or needs. Speculative stocks can lose most or all of their value. We hold no position in ASL. Do your own research.

#ASX #ASXstocks #silver #Chile #miningstocks #juniorminers #smallcaps #blackswanstocks"""

SOURCES = [
    "https://discoveryalert.com/asx-stock-news/mining/asl-andean-silver-cerro-bayo-drilling-results-november-2026/",  # ASX 9 Nov 2026: 26LVDH016 1.7m @ 1,269 g/t AgEq; CBD359 3.3m @ 628 g/t AgEq; ~1 km from plant; MRE 20Mt @ 211 g/t AgEq 136Moz, Ind 60Moz; cash ~A$70.5m end Sep qtr; resource update H1 2027 incl Temer 4, Delia SE
    "https://mining.com.au/andean-silver-drills-multiple-new-high-grade-shoots/",  # 9 Nov 2026: same intercepts, ~1 km from plant, cash end Sep qtr, resource update H1 2027
    "https://kalkinemedia.com/au/stocks/metal-and-mining/where-do-andean-silvers-asxasl-new-shoots-take-cerro-bayo",  # 12 Nov 2026: narrow widths, plant on care and maintenance, follow-up drilling Lucia/Trinidad; ASX price A$1.30 at 23 Nov 2026 05:10 UTC
    "https://mining.com.au/andean-silver-expands-indicated-resource-at-cerro-bayo/",  # 30 Jun 2026: 136Moz AgEq, Indicated 60Moz (+230%), Droughtmaster permitting for 2027
    "https://smallcaps.com.au/article/andean-silver-cerro-bayo-mineralisation-high-grade-pegaso-7-cristal-hits",  # 31 Oct 2024: resource 8.3Mt @ 342 g/t AgEq for 91Moz
    "https://wcsecure.weblink.com.au/pdf/ASL/03073769.pdf",  # ASX 31 Mar 2026: Aysén region; ownership Coeur 1990-2010, Mandalay 2011-2019; Coyita mined 2014-2017; plant; collar CBD271 UTM 19S E270086 N4841462 (= ~46.54S 72.00W)
    "https://mining.com.au/andean-extends-mineralisation-drilling/",  # 9 Feb 2026 (related link, 2 Sep 2026): A$40m placement to accelerate economic studies
]
