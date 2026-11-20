"""Offline tests for the backing track in engine/audio.py. Run: python3 tools/test_audio.py

Checks every style renders cleanly (no NaN, no clipping, steady level), the slug picks the same track every
time, META["music"] = False still gives a voice-only mix, and the track sits under the voice (about -16 dB
while speaking).
"""
import os, sys
import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from engine import audio  # noqa: E402

fails = 0


def check(name, cond):
    global fails
    print(("PASS " if cond else "FAIL ") + name); fails += 0 if cond else 1


def db(x): return 20 * np.log10(np.sqrt(np.mean(np.square(x))) + 1e-12)


for style in audio.STYLES:
    for loop in range(len(audio.LOOPS)):
        x = audio.backtune(20, style, loop, transpose=-3 + loop * 2, seed=loop)
        mid = x[audio.SR * 3:audio.SR * 17]
        halves = [db(mid[:len(mid) // 2]), db(mid[len(mid) // 2:])]
        ok = (not np.isnan(x).any() and np.max(np.abs(x)) <= 1.0 and len(x) == 20 * audio.SR
              and abs(halves[0] - halves[1]) < 4 and db(mid) > -30)
        check(f"{style} loop {loop}: renders, no clipping, steady level", ok)

check("same slug picks the same track", audio.pick("2026-11-20-lex") == audio.pick("2026-11-20-lex"))
check("styles vary across slugs", len({audio.pick(f"2026-12-{d:02d}-x")[0] for d in range(1, 29)}) == len(audio.STYLES))
check("music=False means no music", audio.pick("x", False) is None)
check("a named style is honoured", audio.pick("x", "lofi")[0] == "lofi")

# fake 'voice': 0.4 s bursts of speech-band noise with 0.25 s pauses
rnd = np.random.default_rng(1); n = 12 * audio.SR
voice = np.zeros(n, dtype=np.float32)
for i in range(0, n - audio.SR, int(0.65 * audio.SR)):
    voice[i:i + int(0.4 * audio.SR)] = (np.convolve(rnd.standard_normal(int(0.4 * audio.SR)), np.ones(4) / 4, "same") * 0.15)
dry = audio.mix(voice, [0.0], music=False, sfx=False, slug="t")
check("music=False leaves the voice untouched", np.allclose(dry, voice))
wet = audio.mix(voice, [0.0], music=True, sfx=False, slug="t")
bed = wet - voice; speak = np.abs(np.convolve(voice, np.ones(400) / 400, "same")) > 0.005
rel = db(bed[speak]) - db(voice[np.abs(voice) > 0.01])
check(f"track sits under the voice ({rel:.1f} dB while speaking)", -22 < rel < -11)
check("mix doesn't clip", np.max(np.abs(wet)) < 1.0)

print("all passed" if not fails else f"{fails} failed")
sys.exit(1 if fails else 0)
