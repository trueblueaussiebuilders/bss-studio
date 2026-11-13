"""Alma Metals (ASX:ALM): 51% of the Briggs porphyry copper project, central Queensland."""

META = {
    "kind": "stock",
    "date": "2026-11-14",
    "ticker": "ALM",
    "company": "Alma Metals",
    "commodity": "copper",
    "asof": "Prices: 13 Nov 2026",
    "cover": ["2Mt of copper,", "an *$18m* company"],
}

SCENES = [
    {"type": "hook", "kicker": "ASX:ALM  ·  Copper  ·  Queensland",
     "title": "Two million tonnes of copper, an *$18m* company",
     "chips": [{"label": "Share price", "text": "0.7c"},
               {"label": "Market cap", "value": 18, "prefix": "~A$", "suffix": "m"},
               {"label": "Stake in Briggs", "text": "51%"}],
     "say": "One of Australia's biggest undeveloped copper deposits sits near Gladstone. Alma Metals owns just over half."},

    {"type": "map", "label": "The project", "title": "A copper giant *near a port*",
     "region": [148.2, -26.4, 153.8, -21.9], "inset": True,
     "pins": [{"name": "Briggs project", "sub": "Central Queensland", "lat": -24.10, "lon": 151.05, "kind": "project", "side": "left"},
              {"name": "Gladstone", "sub": "Port", "lat": -23.84, "lon": 151.26, "kind": "town", "dy": -20}],
     "say": "The Briggs project is in central Queensland, close to the port of Gladstone and existing infrastructure."},

    {"type": "big", "label": "The resource", "title": "Huge, but *low grade*",
     "text": "2.0Mt", "caption": "of contained copper, at about 0.21% copper",
     "sub": "932Mt @ 0.21% Cu, 0.15% cut-off. Mostly Inferred.",
     "say": "It holds about two million tonnes of copper, but at a low grade of around zero point two percent."},

    {"type": "bars", "label": "The metal", "title": "Copper vs the *study* price",
     "bars": [{"label": "Scoping study assumption (Nov 2025)", "value": 4.50},
              {"label": "COMEX copper (early Nov 2026)", "value": 6.20, "highlight": True}],
     "fmt": {"prefix": "US$", "suffix": "/lb", "dp": 2},
     "note": "Copper moves daily. Source: company scoping study; Trading Economics, Nov 2026.",
     "say": "Its scoping study assumed four fifty a pound. Copper has been trading around six twenty this month."},

    {"type": "intercept", "label": "The drilling", "title": "Long runs of *copper*",
     "holes": [{"id": "26BRD0042", "from": 10.2, "width": 383.8, "depth": 400, "headline": "384m @ 0.25%", "sub": "Cu from 10m"}],
     "dip": 70,
     "note": "Downhole length. Infill drilling, Briggs, 2026.",
     "say": "Infill drilling keeps hitting long runs, like three hundred and eighty-four metres at zero point two five percent copper."},

    {"type": "catalysts", "label": "What's next", "title": "What could *move* it",
     "items": [{"when": "Late 2026 (planned)", "status": "Next up", "title": "Updated resource estimate",
                "why": "Aims to firm up more of the deposit to Indicated"},
               {"when": "2027", "title": "Pre-feasibility study",
                "why": "The first detailed test of whether a mine stacks up"},
               {"when": "Earn-in", "title": "Stake from 51% to 70%",
                "why": "Alma's share of any future mine would rise"}],
     "say": "What could move it? An updated resource, planned for late this year. A prefeasibility study in twenty twenty-seven. And Alma lifting its stake to seventy percent."},

    {"type": "versus", "label": "Both sides", "title": "The *honest* scorecard",
     "for": {"title": "Going for it", "points": ["2Mt of contained copper", "Copper well above the study price",
                                                 "Close to a port and infrastructure"]},
     "against": {"title": "Working against it", "points": ["A$1.15m cash at 30 Sep", "Low grade needs huge scale",
                                                          "Most of the resource is Inferred"]},
     "say": "The catch: about one million dollars in cash, so a raise looks likely. And low-grade deposits need huge scale to work."},
]

CAPTION = """Alma Metals (ASX:ALM) owns 51% of the Briggs copper project near Gladstone in central Queensland, in joint venture with Canterbury Resources (ASX:CBY).

What's interesting
• Briggs resource: 932Mt @ 0.21% Cu for ~2.0Mt contained copper, plus molybdenum and silver (0.15% Cu cut-off)
• Infill drilling: 383.8m @ 0.25% Cu from 10.2m (26BRD0042) and 76.7m @ 0.34% Cu
• The Nov 2025 scoping study used US$4.50/lb copper. COMEX copper traded around US$6.20/lb in early Nov 2026

What's coming
• Updated resource estimate planned for late 2026
• Pre-feasibility study targeted for 2027
• Alma earning from 51% to 70% of Briggs

What could go wrong
• A$1.15m cash at 30 Sep 2026 (plus ~A$3.3m in listed investments), so more funding is likely
• Low-grade deposits need very large scale and capital to work
• Most of the resource is in the Inferred category

Figures from ASX announcements to 30 Oct 2026. Share price and market cap approximate, as at 13 Nov 2026. Copper prices move daily.

General information only, not financial advice. It doesn't consider your objectives, finances or needs. Speculative stocks can lose most or all of their value. We hold no position in ALM. Do your own research.

#ASX #ASXstocks #copper #coppermining #criticalminerals #juniorminers #smallcaps #blackswanstocks"""

SOURCES = [
    "https://announcements.asx.com.au/asxpdf/20260804/pdf/072dlnqnyzlt6f.pdf",
    "https://www.investsmart.com.au/investment-tools/shares/asx-price-sensitive-announcements/asx-cby/2451527",
    "https://kalkinemedia.com/au/news/announcements/canterbury-resources-advances-briggs-copper-project-drilling-ahead-of-2027-pre-feasibility-study-completion",
    "https://mining.com.au/alma-drilling-confirms-higher-grade-copper-zones-at-briggs/",
    "https://smallcaps.com.au/article/alma-metals-returns-high-grade-copper-results-from-briggs-infill-drilling-campaign",
    "https://smallcaps.com.au/article/alma-metals-mapping-a-clear-expansion-and-feasibility-pathway-as-geopolitical-and-macro-tailwinds-drive-copper-higher",
    "https://www.investsmart.com.au/investment-tools/shares/asx-price-sensitive-announcements/asx-alm/2598212",
    "https://www.investsmart.com.au/security/asx/alm/alma-metals-limited/announcements",
    "https://www.investsmart.com.au/investment-tools/shares/asx-price-sensitive-announcements/asx-alm/2518635",
    "https://tradingeconomics.com/commodity/copper/news/600135",
    "https://smallcaps.com.au/podcasts/alma-metals-asx-alm-webinar-review-briggs-copper-project-update",
]
