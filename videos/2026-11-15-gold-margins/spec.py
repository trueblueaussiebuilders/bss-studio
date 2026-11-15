"""Sunday brief: gold is ~30% off its January record, but miners' margins are still wide. AISC explained."""

META = {
    "kind": "macro",
    "date": "2026-11-15",
    "chip": "SUNDAY BRIEF",
    "cover_word": "AISC",
    "commodity": "gold",
    "asof": "Prices: 13 Nov 2026",
    "cover": ["Gold fell *30%* but", "miners still profit"],
}

SCENES = [
    {"type": "hook", "kicker": "Sunday brief  ·  Gold  ·  Costs and margins",
     "title": "Gold is down *30%* but miners are still making money",
     "chips": [{"label": "Gold, 13 Nov", "value": 3882, "prefix": "US$", "suffix": "/oz", "dp": 0},
               {"label": "From Jan record", "text": "Down ~30%"},
               {"label": "Avg AISC, Jun qtr", "value": 1930, "prefix": "US$", "suffix": "/oz", "dp": 0}],
     "say": "Gold has lost about thirty percent since January. Yet miners are still making money."},

    {"type": "bars", "label": "The fall", "title": "From record to *a one-year low*",
     "bars": [{"label": "Jan 2026 record (intraday)", "value": 5595},
              {"label": "June quarter average", "value": 4512},
              {"label": "September quarter average", "value": 4266},
              {"label": "Close, 13 Nov 2026", "value": 3882, "highlight": True}],
     "fmt": {"prefix": "US$", "suffix": "/oz", "dp": 0},
     "note": "Spot gold, US$ per ounce. Sources: World Gold Council; Trading Economics.",
     "say": "It peaked near fifty-six hundred US dollars an ounce. On Friday it closed under thirty-nine hundred."},

    {"type": "big", "label": "The trigger", "title": "Rates are *going up*",
     "text": "89%", "caption": "market odds of a US rate hike in December",
     "sub": "CME FedWatch via Reuters, 13 Nov 2026, after hotter US inflation data.",
     "say": "The trigger: hot US inflation, and bets the Fed lifts rates in December."},

    {"type": "stack", "label": "The costs", "title": "What it costs to *mine an ounce*",
     "items": [{"label": "Cash operating costs", "value": 1215},
               {"label": "Royalties and taxes", "value": 185},
               {"label": "Sustaining capital", "value": 441},
               {"label": "Corporate and other", "value": 89}],
     "price": {"label": "Gold 13 Nov", "value": 3882},
     "fmt": {"prefix": "US$", "dp": 0},
     "total_label": "Avg AISC", "margin_label": "Margin",
     "note": "Global average all-in sustaining cost, June qtr 2026 (World Gold Council).",
     "say": "But the average all-in cost to produce an ounce is about nineteen hundred and thirty US dollars. That still leaves nearly two thousand in margin."},

    {"type": "stats", "label": "The Aussie angle", "title": "A weaker dollar *cushions* the fall",
     "items": [{"label": "Aussie dollar", "text": "~US68c", "note": "lowest since late Jan"},
               {"label": "Gold in A$", "value": 5700, "prefix": "~A$", "dp": 0, "note": "approx., 13 Nov", "highlight": True},
               {"label": "Northern Star AISC", "value": 3217, "prefix": "A$", "dp": 0, "note": "Sep qtr 2026"},
               {"label": "NST realised price", "value": 4999, "prefix": "A$", "dp": 0, "note": "Sep qtr 2026"}],
     "say": "Here, a weaker Aussie dollar helps. Gold is still around fifty-seven hundred Australian dollars."},

    {"type": "catalysts", "label": "What to watch", "title": "What could *move* it next",
     "items": [{"when": "8 Dec 2026", "status": "Next up", "title": "RBA rate decision",
                "why": "Moves the Aussie dollar, and with it the local gold price"},
               {"when": "9 Dec 2026 (US)", "title": "Fed rate decision",
                "why": "Higher rates raise the cost of holding gold, which pays no interest"},
               {"when": "Late Jan 2027", "title": "December quarter reports",
                "why": "First full quarter of miners' costs at lower gold prices"}],
     "say": "What to watch: rate decisions from the Reserve Bank and the Fed in early December. Then quarterly reports in January, the first full quarter at lower prices."},

    {"type": "versus", "label": "Both sides", "title": "Squeezed from *both ends*",
     "for": {"title": "Still working for miners", "points": ["Gold still about 2x average AISC",
                                                             "Weaker A$ props up local prices",
                                                             "NST: ~A$1,780/oz margin, Sep qtr"]},
     "against": {"title": "Working against them", "points": ["AISC up y/y for 29 straight quarters",
                                                             "More US rate hikes being priced in",
                                                             "Explorers rely on investors for cash"]},
     "say": "The catch: costs keep climbing, and explorers without revenue depend on investors to keep drilling."},
]

CAPTION = """Sunday brief: gold has fallen about 30% from its January record. Here's why the average miner is still making money, and what AISC (all-in sustaining cost) means.

What's interesting
• Gold closed near US$3,882/oz on 13 Nov 2026, down from an intraday record of ~US$5,595/oz in January
• The global average AISC hit a record US$1,930/oz in the June quarter (World Gold Council), leaving a margin of roughly US$1,950/oz at Friday's price
• The Aussie dollar is near US68c, its lowest since late January, so gold is still about A$5,700/oz (approx.)
• Northern Star (ASX:NST) reported AISC of A$3,217/oz against a realised A$4,999/oz in the September quarter

What's coming
• RBA rate decision, 8 Dec 2026
• US Federal Reserve decision, 9 Dec 2026 (markets priced ~89% odds of a hike on 13 Nov)
• December quarter reports from ASX miners, late January 2027

What could go wrong
• AISC has risen year on year for 29 straight quarters
• Further US rate hikes could keep pressure on gold
• Explorers with no revenue depend on investors to fund drilling

AISC components and averages from the World Gold Council (June qtr 2026). Prices approximate, as at 13 Nov 2026. Gold and currencies move daily.

General information only, not financial advice. It doesn't consider your objectives, finances or needs. Speculative stocks can lose most or all of their value. Do your own research.

#ASX #gold #goldmining #AISC #juniorminers #mining #blackswanstocks"""

SOURCES = [
    "https://www.gold.org/goldhub/gold-focus/2026/11/gold-miners-remain-resilient-despite-tighter-margins-q226",
    "https://www.gold.org/goldhub/gold-focus/2026/08/record-gold-prices-outpace-rising-mining-costs-q126",
    "https://tradingeconomics.com/commodity/gold",
    "https://www.kitco.com/news/off-the-wire/2026-11-13/rate-hike-bets-keep-gold-track-its-worst-week-four-months",
    "https://announcements.asx.com.au/asxpdf/20261021/pdf/075kqk1cjqhjtp.pdf",
    "https://tradingeconomics.com/australia/currency/news/600183",
    "https://www.stonex.com/en-gb/news-and-analysis/aud-usd-outlook-historic-yield-squeeze-leaves-aussie-bears-in-control-2026-11-13/",
    "https://www.rba.gov.au/media-releases/2025/mr-25-02.html",
    "https://www.federalreserve.gov/newsevents/2026-december.htm",
]
