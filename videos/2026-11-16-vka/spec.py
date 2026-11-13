"""Viking Mines (ASX:VKA): restarting the Linka tungsten mines, Nevada."""

META = {
    "kind": "stock",
    "date": "2026-11-16",
    "ticker": "VKA",
    "company": "Viking Mines",
    "commodity": "tungsten",
    "asof": "Prices: 12 Nov 2026",
    "cover": ["Can a *1950s* tungsten", "mine come back?"],
}

SCENES = [
    {"type": "hook", "kicker": "ASX:VKA  ·  Tungsten  ·  Nevada, USA",
     "title": "Can a *1950s* tungsten mine come back to life?",
     "chips": [{"label": "Share price", "text": "0.9c"},
               {"label": "Market cap", "value": 23, "prefix": "~A$", "suffix": "m"},
               {"label": "Stage", "text": "Drilling"}],
     "say": "China controls most of the world's tungsten. This tiny explorer wants to bring an old American mine back."},

    {"type": "bars", "label": "The metal", "title": "The West is paying *a premium*",
     "bars": [{"label": "Rotterdam APT (Western price)", "value": 278.22, "highlight": True},
              {"label": "China ex-works APT", "value": 74.43}],
     "fmt": {"prefix": "US$", "suffix": "/kg", "dp": 0},
     "callout": {"text": "3.7x", "caption": "what Western buyers paid over the Chinese price"},
     "note": "October 2026 averages. Source: Canadian Mining Journal.",
     "say": "Since China tightened exports, Western buyers have paid almost four times the Chinese price for tungsten."},

    {"type": "map", "label": "The project", "title": "Three old mines, *one* restart plan", "region": "USA_WEST",
     "highlight": ["United States of America"], "areas": ["Nevada"],
     "pins": [{"name": "Linka project", "sub": "Lander County, Nevada", "lat": 39.32, "lon": -116.83, "kind": "project"},
              {"name": "Reno", "lat": 39.53, "lon": -119.81, "kind": "town", "side": "left"},
              {"name": "Las Vegas", "lat": 36.17, "lon": -115.14, "kind": "town"}],
     "say": "Viking Mines' Linka project is three old mines that last produced in nineteen fifty-six."},

    {"type": "intercept", "label": "The drilling", "title": "Grades in line with *the old mine*",
     "holes": [{"id": "LKRC0002", "from": 40, "width": 14, "depth": 90, "headline": "14m @ 0.56%", "sub": "WO3 from 40m"},
               {"id": "LKRC0005", "from": 62, "width": 18, "depth": 100, "headline": "18m @ 0.42%", "sub": "WO3 from 62m"}],
     "note": "Downhole widths. Historic production ~0.49% WO3. ASX releases 10 and 24 Sep 2026.",
     "say": "First drilling hit fourteen metres at zero point five six percent, in line with what was mined before."},

    {"type": "stats", "label": "The numbers", "title": "Small company, *big* to-do list",
     "items": [{"label": "Share price", "text": "0.9c", "note": "12 Nov close"},
               {"label": "Market cap", "value": 23, "prefix": "~A$", "suffix": "m", "note": "approx."},
               {"label": "Cash", "value": 3.2, "prefix": "A$", "suffix": "m", "dp": 1, "note": "30 Sep 2026"},
               {"label": "JORC resource", "text": "None yet", "highlight": True, "note": "still drilling"}],
     "say": "It's worth about twenty-three million dollars, with three million in cash and no resource yet."},

    {"type": "catalysts", "label": "What's next", "title": "What could *move* it",
     "items": [{"when": "Pending", "status": "Next up", "title": "Assays from ~40 more holes",
                "why": "Shows whether the grades continue beyond the first holes"},
               {"when": "Approved Aug 2026", "title": "907 tonne bulk sample",
                "why": "Tests whether the ore makes a saleable tungsten concentrate"},
               {"when": "1 Jan 2027", "title": "US defence ban on Chinese tungsten",
                "why": "Defence suppliers can't use tungsten mined or refined in China"}],
     "say": "So what could move it? Assays from about forty more holes. A bulk sample to test the ore. And from January, US defence suppliers can't use Chinese tungsten."},

    {"type": "versus", "label": "Both sides", "title": "The *honest* scorecard",
     "for": {"title": "Going for it", "points": ["Record Western tungsten prices", "US push for non-Chinese supply",
                                                 "Early grades match past production"]},
     "against": {"title": "Working against it", "points": ["No JORC resource yet", "Small cash balance, raise likely",
                                                          "Permits still to come"]},
     "say": "The risks are real, though. A capital raise looks likely, and a mining permit is over a year away."},
]

CAPTION = """Viking Mines (ASX:VKA) is trying to restart the Linka tungsten mines in Nevada, which last produced in 1956.

What's interesting
• Western tungsten prices: Rotterdam APT averaged ~3.7x China ex-works in Oct 2026
• Maiden drilling: 14m @ 0.56% WO3 (LKRC0002) and 18m @ 0.42% WO3 (LKRC0005)

What's coming
• Assays from around 40 more holes
• 907t bulk sample to test saleable concentrate
• From 1 Jan 2027, US defence suppliers can't use tungsten mined or refined in China
• Mining permit application targeted for late 2027

What could go wrong
• No JORC resource yet
• ~A$3.2m cash at 30 Sep, so more funding is likely
• Permitting, metallurgy and tungsten price risk

Figures from ASX announcements to 3 Nov 2026. Share price and market cap approximate, as at 12 Nov 2026.

General information only, not financial advice. It doesn't consider your objectives, finances or needs. Speculative stocks can lose most or all of their value. We hold no position in VKA. Do your own research.

#ASX #ASXstocks #tungsten #mining #criticalminerals #smallcaps #blackswanstocks"""

SOURCES = [
    "https://announcements.asx.com.au/asxpdf/20260910/pdf/073yfcbvvdy03h.pdf",
    "https://announcements.asx.com.au/asxpdf/20260924/pdf/074gdw0p4hmgnr.pdf",
    "https://announcements.asx.com.au/asxpdf/20261103/pdf/0765grjjxl75py.pdf",
    "https://announcements.asx.com.au/asxpdf/20260827/pdf/0739vmj0gcnth5.pdf",
    "https://www.canadianminingjournal.com/?p=1003791730",
    "https://westernmininghistory.com/mine-detail/10008793",
    "https://public-inspection.federalregister.gov/2024-11513.pdf",
]
