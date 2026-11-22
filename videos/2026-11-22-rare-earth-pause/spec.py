"""Sunday brief: China's pause on its wider rare earth export controls now ends 10 Jan 2027. What it covers, what stays, and the Aussie angle."""

META = {
    "kind": "macro",
    "date": "2026-11-22",
    "chip": "SUNDAY BRIEF",
    "cover_word": "CHINA",
    "commodity": "rare earths",
    "asof": "Data to 9 Nov 2026",
    "cover": ["The rare earth pause", "now ends *10 January*"],
}

SCENES = [
    {"type": "hook", "kicker": "Sunday brief  ·  Rare earths  ·  China export controls",
     "title": "China's rare earth pause now ends on *10 January*",
     "chips": [{"label": "China, mined 2025", "value": 69, "suffix": "%", "dp": 0},
               {"label": "China, refining", "text": "Up to 90%"},
               {"label": "Pause now ends", "text": "10 Jan 2027"}],
     "say": "One date hangs over rare earths: the tenth of January."},

    {"type": "bars", "label": "Who mines it", "title": "China mines *seven in ten*",
     "bars": [{"label": "China", "value": 69.2, "highlight": True},
              {"label": "United States", "value": 13.1},
              {"label": "Australia", "value": 7.4}],
     "fmt": {"suffix": "%", "dp": 1},
     "callout": {"text": "~90%", "caption": "of global rare earth refining is in China"},
     "note": "Share of 2025 rare earth mine output (GlobalData, via Mining Technology, Apr 2026). Refining share also GlobalData.",
     "say": "China mined about seventy percent of the world's rare earths last year, and refines up to ninety percent."},

    {"type": "timeline", "label": "How we got here", "title": "Rules, then a *pause*",
     "events": [{"when": "Apr 2025", "text": "Licences for seven heavy rare earths", "done": True},
                {"when": "Oct 2025", "text": "Wider controls announced", "done": True},
                {"when": "Nov 2025", "text": "Wider controls paused for a year", "done": True},
                {"when": "9 Nov 2026", "text": "Pause extended two months", "done": True},
                {"when": "10 Jan 2027", "text": "Extended pause ends", "done": False}],
     "say": "In twenty twenty-five, China put seven heavy rare earths under licence, and paused wider controls for a year. Now that pause runs to January."},

    {"type": "big", "label": "The price gap", "title": "Outside China, *scarcity* costs",
     "text": "16x", "caption": "dysprosium oxide in Europe vs the China price",
     "sub": "End of Sep qtr 2026. Benchmark Mineral Intelligence.",
     "say": "Those licences still bite. In September, dysprosium for magnets cost sixteen times more in Europe than in China."},

    {"type": "stats", "label": "The Aussie angle", "title": "Record prices for *Lynas*",
     "items": [{"label": "Lynas avg price", "value": 102.1, "prefix": "A$", "suffix": "/kg", "dp": 1, "note": "Sep qtr 2026, a record", "highlight": True},
               {"label": "Lynas revenue", "value": 310.1, "prefix": "A$", "suffix": "m", "dp": 1, "note": "up 55% on a year earlier"},
               {"label": "Under floor-price deals", "text": "Over half", "note": "of Lynas production"},
               {"label": "Iluka Eneabba refinery", "text": "2027", "note": "commissioning, WA"}],
     "say": "Here, Lynas got a record hundred and two dollars a kilo last quarter. Iluka's Eneabba refinery is due in twenty twenty-seven."},

    {"type": "catalysts", "label": "What to watch", "title": "What could *move* it next",
     "items": [{"when": "Dec qtr 2026", "status": "Next up", "title": "Lynas Malaysia plant shut for a month",
                "why": "Less supply from the biggest producer outside China"},
               {"when": "10 Jan 2027", "title": "China's extended pause ends",
                "why": "Extend again, reinstate some controls, or all of them"},
               {"when": "Late Jan 2027", "title": "December quarter reports",
                "why": "First prices and volumes since the decision"}],
     "say": "What to watch: a month-long shutdown at Lynas in Malaysia. Then the January deadline: extend again, or bring controls back. Then quarterly reports."},

    {"type": "versus", "label": "Both sides", "title": "Leverage on *both sides*",
     "for": {"title": "Helping producers outside China", "points": ["Western premiums for heavy rare earths",
                                                                   "Floor-price deals cover over half of Lynas output",
                                                                   "New refining in WA from 2027"]},
     "against": {"title": "Working against them", "points": ["Rules can change at short notice",
                                                             "China still refines up to ~90%",
                                                             "Ex-China NdPr fell under US$110/kg in Aug"]},
     "say": "The catch: China still controls most refining, and it can change the rules again at short notice."},
]

CAPTION = """Sunday brief: China's pause on its wider rare earth export controls was due to end on 10 November. On 9 November Beijing extended it to 10 January 2027. Here's what it covers, what stays in force, and why it matters to Australian producers.

What's interesting
• China produced about 69% of the world's mined rare earths in 2025 and has up to ~90% of refining (GlobalData)
• April 2025 licensing on seven medium and heavy rare earths (samarium, gadolinium, terbium, dysprosium, lutetium, scandium, yttrium) remains in force
• The wider controls announced in October 2025 were paused for a year in November 2025; that pause now runs to 10 January 2027 (MOFCOM, via S&P Global)
• Dysprosium oxide in Europe was about 16 times the China price at the end of the September quarter (Benchmark Mineral Intelligence)
• Lynas (ASX:LYC) reported a record average price of A$102.1/kg and revenue of A$310.1m, up 55%, in the September quarter; floor-price agreements cover more than half its production
• Iluka (ASX:ILU) is preparing to commission its Eneabba rare earths refinery in WA in 2027

What's coming
• Lynas's Malaysian plant shut for about a month of scheduled maintenance in the December quarter
• 10 January 2027: the extended pause ends. Beijing could extend it, reinstate some controls, or reinstate all of them
• December quarter reports from ASX producers, late January 2027

What could go wrong
• Export rules can be changed at short notice
• China still dominates refining and magnet making
• Ex-China NdPr prices dipped below the US$110/kg floor in the US defence deals in August 2026

Figures from company reports and industry sources to 9 Nov 2026. Prices move daily.

General information only, not financial advice. It doesn't consider your objectives, finances or needs. Speculative stocks can lose most or all of their value. Do your own research.

#ASX #rareearths #criticalminerals #China #miningstocks #Lynas #blackswanstocks"""

SOURCES = [
    "https://www.spglobal.com/energy/en/news-research/latest-news/metals/110926-china-extends-rare-earth-export-suspension-to-january-2027",  # 9 Nov 2026: suspension due to end 10 Nov extended to 10 Jan 2027; seven heavy rare earths remain controlled
    "https://www.mining-technology.com/news/china-rare-earth-export-pause-nears-expiry-amid-persistent-supply-concentration/",  # Apr 2026: GlobalData 2025 output China 69.2%, US 13.1%, Australia 7.4%; up to 90% of processing; April 2025 licences on 7 elements; Oct 2025 measures paused 12 months
    "https://www.bnnbloomberg.ca/business/international/2025/11/07/china-announces-one-year-suspension-of-expanded-rare-earth-export-controls/",  # Nov 2025 one-year suspension of the Oct 2025 controls
    "https://source.benchmarkminerals.com/article/ex-china-heavy-rare-earths-continue-to-surge-q3-2026-rare-earths-price-review",  # Q3 2026: Dy oxide CIF Europe ~16.3x DDP China
    "https://www.kitco.com/news/off-the-wire/2026-10-29/lynas-posts-55-revenue-jump-record-prices-flags-plant-shutdowns",  # 29 Oct 2026: Lynas Sep qtr revenue A$310.1m (from A$200.2m), record ASP A$102.1/kg, floor-price deals > half of production, Malaysia shut a month in Dec qtr
    "https://www.businessnews.com.au/article/Iluka-swings-to-288m-loss-Eneabba-set-for-2027-commissioning",  # Feb 2026: Eneabba commissioning in 2027
    "https://source.benchmarkminerals.com/article/ex-china-ndpr-prices-slip-below-110-kg-price-floor-as-oversupply-builds",  # Aug 2026: ex-China NdPr US$95/kg, below the US$110/kg DoD floor
]
