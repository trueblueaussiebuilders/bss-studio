"""QMines (ASX:QML): the Mt Chalmers copper-gold project, ~17 km northeast of Rockhampton, Queensland."""

META = {
    "kind": "stock",
    "date": "2026-11-23",
    "ticker": "QML",
    "company": "QMines",
    "commodity": "copper",
    "asof": "Placement price: 3 Nov 2026",
    "cover": ["*2.83%* copper beside", "an old Queensland mine"],
}

SCENES = [
    {"type": "hook", "kicker": "ASX:QML  ·  Copper  ·  Queensland",
     "title": "High-grade copper *180 metres* outside an old mine",
     "chips": [{"label": "Placement", "text": "5.2c"},
               {"label": "Funding", "value": 17.5, "prefix": "~A$", "suffix": "m", "dp": 1},
               {"label": "Stage", "text": "DFS underway"}],
     "say": "High-grade copper, a hundred and eighty metres outside an old mine."},

    {"type": "map", "label": "The project", "title": "A copper mine from *1898*",
     "region": [150.25, -23.62, 151.0, -22.98], "inset": True,
     "pins": [{"name": "Mt Chalmers", "sub": "Mined 1898 to 1982", "lat": -23.29, "lon": 150.64,
               "kind": "project", "side": "right", "dy": 30},
              {"name": "Rockhampton", "sub": "Regional city", "lat": -23.38, "lon": 150.51, "kind": "town", "side": "left", "dy": 20},
              {"name": "Yeppoon", "sub": "Coast", "lat": -23.13, "lon": 150.74, "kind": "town", "side": "right", "dy": -40}],
     "links": [{"from": "Mt Chalmers", "to": "Rockhampton", "label": "~17 km"}],
     "say": "QMines owns Mount Chalmers, near Rockhampton in Queensland. It was mined on and off from eighteen ninety-eight until nineteen eighty-two."},

    {"type": "intercept", "label": "The drilling", "title": "Today's assays, *180m* from the resource",
     "holes": [{"id": "26MCDD052", "from": 191, "width": 12, "depth": 260, "headline": "12m @ 2.83% Cu", "sub": "incl. 2m @ 7.05% Cu"}],
     "note": "Downhole width; true width not yet known. A second hole: 20m @ 0.45% Cu. ASX 23 Nov 2026.",
     "say": "Assays out today: twelve metres at two point eight three percent copper, from a hundred and ninety-one metres down."},

    {"type": "bars", "label": "The grade", "title": "Copper grade, *side by side*",
     "bars": [{"label": "Mt Chalmers resource (11.3Mt)", "value": 0.75},
              {"label": "Old mine, 1898-1982", "value": 2.0},
              {"label": "New hole (12m)", "value": 2.83, "highlight": True}],
     "fmt": {"suffix": "% Cu", "dp": 2},
     "callout": {"text": "3.8x", "caption": "the resource grade, over 12 metres of one hole"},
     "note": "Mt Chalmers resource and reserve from the PFS. Historic output 1.2Mt @ 2.0% Cu.",
     "say": "That's nearly four times the grade of the existing resource."},

    {"type": "stats", "label": "The numbers", "title": "Studied, and *funded* for now",
     "items": [{"label": "Placement price", "text": "5.2c", "note": "A$5.5m raise, 3 Nov 2026"},
               {"label": "Cash", "value": 10.7, "prefix": "~A$", "suffix": "m", "dp": 1, "note": "30 Sep 2026, no debt"},
               {"label": "Funding", "value": 17.5, "prefix": "~A$", "suffix": "m", "dp": 1, "note": "after raise, per company", "highlight": True},
               {"label": "Ore reserve", "value": 9.6, "suffix": "Mt", "dp": 1, "note": "@ 0.65% Cu"}],
     "say": "There's already a nine point six million tonne reserve, and about seventeen and a half million dollars after this month's raise."},

    {"type": "catalysts", "label": "What's next", "title": "What could *move* it",
     "items": [{"when": "Before Christmas", "status": "Next up", "title": "~15 holes of assays, incl. 4 follow-ups",
                "why": "Tests whether the new zone joins up with the deposit"},
               {"when": "End 2026 (target)", "title": "Definitive feasibility study",
                "why": "Full costing of a 1 Mtpa mine and plant"},
               {"when": "H1 2027", "title": "Environmental Authority application",
                "why": "Starts the main Queensland approval to mine"}],
     "say": "What could move it? Around fifteen holes of assays, due before Christmas. A feasibility study targeted for year end. Then an environmental approval application, first half of next year."},

    {"type": "versus", "label": "Both sides", "title": "The *honest* scorecard",
     "for": {"title": "Going for it", "points": ["2.83% Cu, 180m outside the resource", "Reserve and PFS already done",
                                                 "~A$17.5m funding, no debt"]},
     "against": {"title": "Working against it", "points": ["Two holes don't prove continuity", "True widths still unknown",
                                                          "PFS build cost ~A$192m to fund"]},
     "say": "The catch: two holes don't prove a deposit, true widths are unknown, and the study put the build cost near two hundred million dollars."},
]

CAPTION = """QMines (ASX:QML) owns Mt Chalmers, a historic copper-gold mine about 17 km northeast of Rockhampton in Queensland, mined on and off from 1898 to 1982. It is now running a definitive feasibility study on restarting it.

What's interesting
• Step-out hole 26MCDD052, about 180m outside the Mt Chalmers resource, returned 12.0m @ 2.83% Cu from 191m, including 2.0m @ 7.05% Cu (ASX, 23 Nov 2026)
• Mt Chalmers resource 11.3Mt @ 0.75% Cu; ore reserve 9.6Mt @ 0.65% Cu (pre-feasibility study)
• A$5.5m placement at 5.2c in Nov 2026, with Queensland's Critical Minerals Fund among the investors; company says funding is ~A$17.5m with no debt
• 25 freehold parcels next to Mt Chalmers contracted for A$5.5m, for the planned plant, tailings and water dam (settlement pending)

What's coming
• About 15 holes at the lab, including four follow-ups around the new hit, with news flagged before Christmas
• Definitive feasibility study, targeted for completion by the end of 2026
• Environmental Authority application, targeted for the first half of 2027

What could go wrong
• Two holes can't establish continuity; true widths aren't known yet
• The PFS put project capital at ~A$191.9m, far more than the company holds
• No approvals or construction funding yet; studies and approvals can slip
• More raisings would dilute existing holders

Figures from ASX announcements and company releases to 23 Nov 2026. Price shown is the 3 Nov 2026 placement price; we couldn't verify a current closing price or market cap.

General information only, not financial advice. It doesn't consider your objectives, finances or needs. Speculative stocks can lose most or all of their value. We hold no position in QML. Do your own research.

#ASX #ASXstocks #copper #Queensland #miningstocks #juniorminers #smallcaps #blackswanstocks"""

SOURCES = [
    "https://discoveryalert.com/asx-stock-news/mining/qml-qmines-mt-chalmers-copper-discovery-november-2026/",  # ASX 23 Nov 2026: 26MCDD052 12.0m @ 2.83% Cu from 191m incl 4m @ 5.30%, 2m @ 7.05%; 26MCDD049 20m @ 0.45% from 170m; ~15 holes at lab, news before Christmas; MRE 11.3Mt @ 0.75% Cu, reserve 9.6Mt @ 0.65% Cu; historic 1.2Mt @ 2.0% Cu 1898-1982
    "https://industryqld.com.au/high-grade-hit-180m-beyond-mount-chalmers-resource-footprint/",  # 23 Nov 2026: 180m beyond resource, 20,000m program, follow-up assays pending
    "https://mining.com.au/qmines-cuts-copper-180m-beyond-mt-chalmers-resource/",  # 23 Nov 2026: ~15 holes at the lab, reserve 9.6Mt @ 0.65% Cu
    "https://discoveryalert.com/asx-stock-news/mining/qml-qmines-mt-chalmers-placement-november-2026/",  # 3 Nov 2026: A$5.5m placement at 5.2c, QCMF, funding ~A$17.5m (A$10.7m cash + placement + QDrilling), no debt, 1Mtpa initial
    "https://mining.com.au/qmines-secures-land-for-mt-chalmers-infrastructure/",  # 9 Nov 2026: 17 km NE of Rockhampton, 25 parcels A$5.5m, cash ~A$10.7m at 30 Sep, EA application H1 2027
    "https://discoveryalert.com/asx-stock-news/mining/qml-qmines-mt-chalmers-land-acquisition-november-2026/",  # 9 Nov 2026: land for plant, TSF, water dam; settlement pending
    "https://qmines.com.au/wp-content/uploads/2026/09/QML-Report-ECR-Sep-2026.pdf",  # 29 Sep 2026 (paid research, used for company facts only): PFS capex A$191.9m, DFS targeted by year-end 2026
]
