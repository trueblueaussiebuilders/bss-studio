# Brand and account setup

**Look:** near-black canvas, warm white type, one red accent (the swan's beak). Instrument Serif headlines with red italic emphasis, Inter Tight for body, JetBrains Mono for numbers and labels. Each commodity has its own accent on the element tile (`engine/style.py`).

| Token | Hex |
|---|---|
| Night (background) | `#0B0B0C` |
| Paper (type) | `#F3F0EA` |
| Beak red (accent) | `#E5484D` |
| Muted | `#8E8B85` |
| Up / down | `#3DD68C` / `#F2555A` |

## Profile

- **Profile picture:** `profile_light.png` (black swan on paper). It stands out against the dark Reels grid. `profile_dark.png` is the alternative.
- **Name field (searchable):** `Black Swan Stocks | ASX junior miners`
- **Category:** Education (not "Financial service" or "Financial adviser")
- **Bio:**
  ```
  ASX junior miners, explained in 60 sec
  Mon · Wed · Fri: one stock | Sun: the big picture
  General info only, not financial advice
  ```
- **Highlights:** post each `highlight_*.png` as a story, then save to a highlight named Junior miners, Sundays, How to read, Fine print, About.
- **Pinned post:** `pinned_1.png` to `pinned_3.png` as one carousel. Pin it to the top of the grid.

## Hashtags

Rotate 6 to 8 per post: `#ASX #ASXstocks #smallcaps #mining #miningstocks #juniorminers` plus the commodity (`#gold #copper #lithium #uranium #tungsten #rareearths #criticalminerals`) and always `#blackswanstocks`.

## Motion

Maps open wide and zoom in: every map scene starts on the whole of Australia (or the continent around an overseas project, e.g. the USA for Nevada) with the target area outlined in the accent red, then eases into the region over about 1.4 seconds. The outline fades as the zoom lands and the pins, links and labels pop in straight after. Regions that are already continent-wide (AU, USA, WORLD) don't zoom. The locator inset shows Australia for Australian projects and the continent (e.g. South America) for overseas ones.

The hook lands fast: the kicker is up on the first frame, the title slides in from 0s, and the hook's headline number (`stat`) counts up in the accent red, landing by about 1.4s with a red underline sweep. The hook cuts to the next scene about a third of a second after its line, so the first cut comes at roughly 4s instead of 4.5s.

## Sound

Voice first. Under it, a generated backing track (no licensing): one of three styles, lofi (84 bpm), pulse (104 bpm) or ambient (76 bpm), in a minor-leaning four-chord loop. It sits about 16 dB under the voice while it's speaking and rises a little in the pauses. Keys and bass open the first bar and the beat drops in on bar 2. Soft whooshes on scene changes. The final mix is loudness-normalised to -14 LUFS, true peak -1.5 dBFS.
