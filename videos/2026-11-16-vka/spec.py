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
     "say": "Viking Mines is a twenty-three million dollar explorer trying to restart an old tungsten mine in Nevada."},

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
     "say": "Linka is three old mines that last produced in nineteen fifty-six."},

    {"type": "intercept", "label": "The drilling", "title": "Grades in line with *the old mine*",
     "holes": [{"id": "LKRC0002", "from": 40, "width": 14, "depth": 90, "headline": "14m @ 0.56%", "sub": "WO3 from 40m"},
               {"id": "LKRC0005", "from": 62, "width": 18, "depth": 100, "headline": "18m @ 0.42%", "sub": "WO3 from 62m"}],
     "note": "Downhole widths. Historic production ~0.49% WO3. ASX releases 10 and 24 Sep 2026.",
     "say": "First drilling hit fourteen metres at zero point five six percent. That's in line with the old mine."},

    {"type": "stats", "label": "The numbers", "title": "Small company, *big* to-do list",
     "items": [{"label": "Share price", "text": "0.9c", "note": "12 Nov close"},
               {"label": "Market cap", "value": 23, "prefix": "~A$", "suffix": "m", "note": "approx."},
               {"label": "Cash", "value": 3.2, "prefix": "A$", "suffix": "m", "dp": 1, "note": "30 Sep 2026"},
               {"label": "JORC resource", "text": "None yet", "highlight": True, "note": "still drilling"}],
     "say": "But there's no resource yet, and with about three million in cash, it will likely need to raise money."},

    {"type": "timeline", "label": "What's next", "title": "The catalysts *to watch*",
     "events": [{"when": "Aug 2026", "text": "907 tonne bulk sample approved", "done": True},
                {"when": "Sep 2026", "text": "First assays: 14m @ 0.56% WO3", "done": True},
                {"when": "Pending", "text": "Assays from around 40 more holes"},
                {"when": "Late 2027", "text": "Mining permit application (target)"}],
     "say": "Next: assays from around forty holes, a bulk sample, and a mining permit push."},

    {"type": "versus", "label": "Both sides", "title": "The *honest* scorecard",
     "for": {"title": "Going for it", "points": ["Record Western tungsten prices", "US push for non-Chinese supply",
                                                 "Early grades match past production"]},
     "against": {"title": "Working against it", "points": ["No JORC resource yet", "Small cash balance, raise likely",
                                                          "Permits still to come"]},
     "say": "Tailwinds are price and US supply policy. Risks are dilution and permitting."},

    {"type": "outro", "say": "Not advice. Just the breakdown. Follow for the next one."},
]

CAPTION = """Viking Mines (ASX:VKA) is trying to restart the Linka tungsten mines in Nevada, which last produced in 1956.

What's interesting
• Western tungsten prices: Rotterdam APT averaged ~3.7x China ex-works in Oct 2026
• Maiden drilling: 14m @ 0.56% WO3 (LKRC0002) and 18m @ 0.42% WO3 (LKRC0005)
• 907t bulk sample approved; mining permit application targeted for late 2027

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
]
