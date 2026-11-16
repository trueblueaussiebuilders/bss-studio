"""Stellar Resources (ASX:SRZ): the Heemskirk tin project at Zeehan, western Tasmania."""

META = {
    "kind": "stock",
    "date": "2026-11-16",
    "ticker": "SRZ",
    "company": "Stellar Resources",
    "commodity": "tin",
    "asof": "Prices: 16 Nov 2026",
    "cover": ["Tin is *70%* above", "this project's study price"],
}

SCENES = [
    {"type": "hook", "kicker": "ASX:SRZ  ·  Tin  ·  Tasmania",
     "title": "Tin is *70%* above this project's study price",
     "chips": [{"label": "Share price", "text": "30c"},
               {"label": "Market cap", "value": 100, "prefix": "~A$", "suffix": "m"},
               {"label": "Stage", "text": "Pre-feasibility"}],
     "say": "Tin is trading seventy percent above this project's last study price."},

    {"type": "map", "label": "The project", "title": "Next door to Australia's *biggest* tin mine",
     "region": [143.2, -44.0, 150.2, -40.4], "inset": True,
     "pins": [{"name": "Heemskirk project", "sub": "Zeehan, western Tasmania", "lat": -41.89, "lon": 145.33,
               "kind": "project", "side": "right", "dy": 45},
              {"name": "Renison mine", "sub": "18 km away", "lat": -41.79, "lon": 145.44, "kind": "mine", "side": "right", "dy": -45},
              {"name": "Burnie", "sub": "Export port", "lat": -41.05, "lon": 145.91, "kind": "town", "side": "right", "dy": -20}],
     "say": "Stellar Resources owns Heemskirk in western Tasmania, near Renison, Australia's biggest tin mine."},

    {"type": "bars", "label": "The metal", "title": "Tin vs *the study* price",
     "bars": [{"label": "Scoping study tin price (Sep 2024)", "value": 28000},
              {"label": "LME tin cash price (13 Nov 2026)", "value": 48295, "highlight": True}],
     "fmt": {"prefix": "US$", "suffix": "/t", "dp": 0},
     "callout": {"text": "+72%", "caption": "tin price vs the scoping study assumption"},
     "note": "Study price from the Sep 2024 updated scoping study. LME cash settlement via Westmetall. Tin moves daily.",
     "say": "Its twenty twenty-four study assumed twenty-eight thousand US dollars a tonne. Tin closed Friday near forty-eight thousand."},

    {"type": "big", "label": "The resource", "title": "Small tonnes, *high grade*",
     "text": "115kt", "caption": "of contained tin, at 0.86% tin",
     "sub": "13.36Mt @ 0.86% Sn, July 2026. 8.31Mt Indicated, 5.0Mt Inferred.",
     "say": "The resource holds about a hundred and fifteen thousand tonnes of tin, at zero point eight six percent."},

    {"type": "stats", "label": "The numbers", "title": "Funded for the *next step*",
     "items": [{"label": "Share price", "text": "30c", "note": "16 Nov 2026"},
               {"label": "Market cap", "value": 100, "prefix": "~A$", "suffix": "m", "note": "approx., ~340m shares"},
               {"label": "Cash + term deposits", "value": 28.3, "prefix": "A$", "suffix": "m", "dp": 1, "note": "30 Sep 2026"},
               {"label": "Operating outflow", "value": 2.1, "prefix": "A$", "suffix": "m", "dp": 1, "note": "Sep quarter", "highlight": True}],
     "say": "The company is worth about a hundred million dollars, with twenty-eight million in cash."},

    {"type": "catalysts", "label": "What's next", "title": "What could *move* it",
     "items": [{"when": "Assays pending", "status": "Next up", "title": "850m hole below the Severn resource",
                "why": "Shows whether the tin keeps going at depth"},
               {"when": "Drilling now", "title": "Follow-up holes at Severn and Montana",
                "why": "Tests whether two deposits join up into one bigger zone"},
               {"when": "1H 2027", "title": "Pre-feasibility study",
                "why": "First detailed test of costs, capex and plant options"}],
     "say": "What could move it? Assays from an eight hundred and fifty metre hole below the resource. Holes testing whether two deposits join up. And the prefeasibility study, due in the first half of twenty twenty-seven."},

    {"type": "versus", "label": "Both sides", "title": "The *honest* scorecard",
     "for": {"title": "Going for it", "points": ["Tin far above the study price", "A$28.3m cash and term deposits",
                                                 "Next to Renison and a sealed road to port"]},
     "against": {"title": "Working against it", "points": ["PFS slipped from 2026 to 1H 2027", "Tin down ~10% since late Sep",
                                                          "Mine capex likely needs new funding"]},
     "say": "The catch: that study has slipped to next year, tin is down ten percent since late September, and a mine will need far more money."},
]

CAPTION = """Stellar Resources (ASX:SRZ) is studying a new underground tin mine at Heemskirk, near Zeehan in western Tasmania, 18 km from the Renison tin mine.

What's interesting
• Resource: 13.36Mt @ 0.86% Sn for ~115kt contained tin (July 2026), 8.31Mt of it Indicated
• The Sep 2024 updated scoping study assumed US$28,000/t tin. LME tin cash settled at US$48,295/t on 13 Nov 2026
• A$28.3m in cash and term deposits at 30 Sep 2026
• Metals X, 50% owner of Renison, held ~16% of Stellar (July 2026)

What's coming
• Assays from ZS187W3A, an 850m wedge hole below the Severn resource
• Follow-up holes ZS197 and ZM196 testing whether Severn and Montana link up
• Drilling for DFS-level metallurgical samples
• Pre-feasibility study, targeted for 1H 2027

What could go wrong
• The PFS was previously targeted for 2H 2026
• Tin fell from just above US$54,000/t at end-Sep to ~US$48,300/t by 13 Nov
• The 2024 scoping study put pre-production capex at ~A$71m, more than current cash
• 5.0Mt of the resource is Inferred

Figures from ASX announcements to 26 Oct 2026. Share price and market cap approximate, as at 16 Nov 2026. Tin prices move daily.

General information only, not financial advice. It doesn't consider your objectives, finances or needs. Speculative stocks can lose most or all of their value. We hold no position in SRZ. Do your own research.

#ASX #ASXstocks #tin #Tasmania #mining #criticalminerals #smallcaps #blackswanstocks"""

SOURCES = [
    "https://www.aspecthuntley.com.au/asxdata/20261026/pdf/03152934.pdf",  # Sept 2026 quarterly: cash, outflow, resource, PFS 1H 2027, holes, LME tin end-Sep
    "https://www.aspecthuntley.com.au/asxdata/20261007/pdf/03145335.pdf",  # Severn drilling, 7 Oct 2026
    "https://www.aspecthuntley.com.au/asxdata/20260702/pdf/03106857.pdf",  # Severn resource up 64%, 2 Jul 2026
    "https://announcements.asx.com.au/asxpdf/20240902/pdf/067d334y39ldhn.pdf",  # Updated scoping study, 2 Sep 2024 (US$28,000/t, A$71m capex, Renison 18 km)
    "https://www.miningweekly.com/article/tin-explorer-stellar-resources-expands-mineral-resource-at-heemskirk-by-64-2026-07-02",  # Metals X 16.4%
    "https://www.westmetall.com/en/markdaten.php?action=table&field=LME_Sn_cash",  # LME tin cash 13 Nov 2026
    "https://stockanalysis.com/quote/asx/SRZ/company/",  # share price 16 Nov 2026
    "https://stockanalysis.com/quote/asx/SRZ/statistics/",  # 340.02m shares
    "https://www.stellarresources.com.au/",
]
