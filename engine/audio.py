"""Procedural backing track and transition whooshes, ducked under the voice.
Everything is generated here, so there are no music licensing issues.

Styles (META["music"] in a spec): "lofi" (laid-back beat, electric piano, bass), "pulse" (steady
four-on-the-floor, arpeggio, pulsing bass), "ambient" (pad, plucks and a slow heartbeat kick).
True or missing = pick a style, key and chord progression from the slug, so videos vary but a rebuild of
the same video always sounds the same. False = no music and no whooshes.
"""
import zlib
import numpy as np

SR = 24000
NOTE = lambda m: 440.0 * 2 ** ((m - 69) / 12)

# A minor-ish progression, one chord per bar
PROGRESSIONS = {
    "calm": [[45, 52, 59, 60, 64], [41, 48, 52, 57, 64], [48, 55, 59, 64, 67], [43, 50, 55, 59, 62]],   # Am9 Fmaj7 Cmaj7 G
    "bright": [[48, 55, 60, 64, 67], [45, 52, 57, 60, 64], [41, 48, 53, 57, 60], [43, 50, 55, 59, 62]],  # C Am F G
}


def _osc(f, n, detune=0.0015):
    t = np.arange(n) / SR
    s = np.zeros(n)
    for d in (-detune, 0, detune):
        ph = 2 * np.pi * f * (1 + d) * t
        s += np.sin(ph) + 0.25 * np.sin(2 * ph) + 0.08 * np.sin(3 * ph)
    return s / 3


def pad(duration, bar=4.0, mood="calm", seed=3):
    n = int(duration * SR)
    out = np.zeros(n)
    prog = PROGRESSIONS.get(mood, PROGRESSIONS["calm"])
    xf = int(1.2 * SR)
    nb = int(np.ceil(duration / bar)) + 1
    for b in range(nb):
        s0 = int(b * bar * SR) - xf // 2
        L = int(bar * SR) + xf
        chord = prog[b % len(prog)]
        seg = sum(_osc(NOTE(m), L) * (0.9 if i == 0 else 0.55) for i, m in enumerate(chord))
        env = np.ones(L)
        ramp = 0.5 - 0.5 * np.cos(np.linspace(0, np.pi, xf))
        env[:xf] = ramp; env[-xf:] = ramp[::-1]
        a, b_ = max(0, s0), min(n, s0 + L)
        if a < b_: out[a:b_] += (seg * env)[a - s0:b_ - s0]
    # sparse plucks on chord tones, one octave up, with a soft echo
    rnd = np.random.default_rng(seed)
    step = 60 / 92 / 2
    k = 0
    while k * step < duration - 0.5:
        if rnd.random() < 0.42:
            chord = prog[int(k * step // bar) % len(prog)]
            f = NOTE(chord[rnd.integers(1, len(chord))] + 12)
            L = int(1.2 * SR); t = np.arange(L) / SR
            pl = np.sin(2 * np.pi * f * t) * np.exp(-t * 5.5) * 0.9
            for d, g in ((0, 1.0), (0.33, 0.35), (0.66, 0.14)):
                i = int((k * step + d) * SR)
                if i < n: out[i:i + L] += (pl * g)[:max(0, min(L, n - i))]
        k += 1
    out = out[:n]
    out /= (np.max(np.abs(out)) + 1e-9)
    fade = int(0.6 * SR); out[:fade] *= np.linspace(0, 1, fade)
    tail = int(1.8 * SR); out[-tail:] *= np.linspace(1, 0, tail)
    return out.astype(np.float32)


# ------------------------------------------------------------------ backing track ("backtune")
STYLES = {
    "lofi":    {"bpm": 84,  "swing": 0.14, "drums": "lofi",  "keys": "ep",   "bass": "half",  "arp": False, "pad": 0.25},
    "pulse":   {"bpm": 104, "swing": 0.0,  "drums": "four",  "keys": "stab", "bass": "eighth", "arp": True, "pad": 0.35},
    "ambient": {"bpm": 76,  "swing": 0.0,  "drums": "heart", "keys": None,   "bass": "whole", "arp": True,  "pad": 0.8},
}
# minor-leaning four-chord loops as scale-degree triads/7ths over A minor (MIDI); transposed per video
LOOPS = [
    [[57, 60, 64, 67], [53, 57, 60, 64], [48, 52, 55, 59], [55, 59, 62, 65]],   # Am7  Fmaj7  Cmaj7  G7
    [[57, 60, 64, 67], [55, 59, 62, 65], [53, 57, 60, 64], [52, 56, 59, 62]],   # Am7  G7  Fmaj7  E7
    [[50, 53, 57, 60], [55, 59, 62, 65], [48, 52, 55, 59], [57, 60, 64, 67]],   # Dm7  G7  Cmaj7  Am7
    [[57, 60, 64, 67], [50, 53, 57, 60], [52, 55, 59, 62], [53, 57, 60, 64]],   # Am7  Dm7  Em7  Fmaj7
]


def pick(slug, music=True):
    """Resolve META["music"] to (style, loop index, transpose). None = no music."""
    if music is False or music in ("none", "off"):
        return None
    h = zlib.crc32(slug.encode())
    style = music if isinstance(music, str) and music in STYLES else list(STYLES)[h % len(STYLES)]
    return style, (h >> 4) % len(LOOPS), ((h >> 8) % 7) - 3


def _put(out, x, t):
    i = int(t * SR)
    if i >= len(out) or i + len(x) <= 0: return
    a = max(0, -i); b = min(len(x), len(out) - i)
    out[i + a:i + b] += x[a:b]


def _kick(soft=1.0):
    n = int(0.32 * SR); t = np.arange(n) / SR
    f = 62 + 95 * np.exp(-t * 28)                       # pitch drop, kept above the 60 Hz high-pass
    ph = 2 * np.pi * np.cumsum(f) / SR
    return (np.sin(ph) * np.exp(-t * 11) * soft).astype(np.float64)


def _noise_hit(rnd, length, decay, tone=0.0, bright=1.0):
    n = int(length * SR); t = np.arange(n) / SR
    x = rnd.standard_normal(n)
    hp = np.diff(x, prepend=0) * bright + x * (1 - bright)
    hit = hp * np.exp(-t * decay)
    if tone: hit = hit * 0.6 + np.sin(2 * np.pi * tone * t) * np.exp(-t * decay * 1.5) * 0.8
    return np.convolve(hit, np.ones(3) / 3, mode="same")


def _ep(f, length):
    """Soft electric-piano note: bell partials that fade faster than the body."""
    n = int(length * SR); t = np.arange(n) / SR
    body = np.sin(2 * np.pi * f * t) + 0.35 * np.sin(2 * np.pi * 2 * f * t) * np.exp(-t * 2.5)
    bell = 0.18 * np.sin(2 * np.pi * 4.02 * f * t) * np.exp(-t * 7)
    env = np.minimum(1, t / 0.006) * np.exp(-t * 1.1)
    return (body + bell) * env


def _pluck(f, length=0.9, decay=5.0):
    n = int(length * SR); t = np.arange(n) / SR
    return (np.sin(2 * np.pi * f * t) + 0.2 * np.sin(4 * np.pi * f * t)) * np.exp(-t * decay) * np.minimum(1, t / 0.003)


def _bass(f, length):
    n = int(length * SR); t = np.arange(n) / SR
    env = np.minimum(1, t / 0.01) * np.minimum(1, (length - t) / 0.06) * (0.75 + 0.25 * np.exp(-t * 4))
    return (np.sin(2 * np.pi * f * t) + 0.3 * np.sin(4 * np.pi * f * t)) * env


def backtune(duration, style="lofi", loop=0, transpose=0, seed=0):
    """A loopable backing track for `duration` seconds, peak-normalised. Bars follow the chord loop."""
    cfg = STYLES[style]; rnd = np.random.default_rng(seed)
    n = int(duration * SR); beat = 60 / cfg["bpm"]; bar = 4 * beat
    prog = [[m + transpose for m in ch] for ch in LOOPS[loop]]
    drums, keys, bass, arp = (np.zeros(n) for _ in range(4))

    def at(b, eighth):                                   # time of an eighth note in bar b, with swing on the off-beats
        return b * bar + (eighth // 2) * beat + (eighth % 2) * beat * (0.5 + cfg["swing"])

    nb = int(np.ceil(duration / bar)) + 1
    for b in range(nb):
        ch = prog[b % len(prog)]; root = NOTE(ch[0] - 24 if ch[0] - 24 >= 33 else ch[0] - 12)
        intro = b == 0                                   # first bar: keys and bass only, the beat drops in on bar 2
        # drums
        if not intro:
            if cfg["drums"] == "lofi":
                for e in (0, 5) if b % 2 else (0, 3, 5):
                    _put(drums, _kick(0.95), at(b, e))
                for e in (2, 6):
                    _put(drums, _noise_hit(rnd, 0.22, 22, tone=190, bright=0.6) * 0.55, at(b, e))
                for e in range(8):
                    _put(drums, _noise_hit(rnd, 0.06, 70) * (0.16 if e % 2 else 0.22), at(b, e))
            elif cfg["drums"] == "four":
                for e in (0, 2, 4, 6):
                    _put(drums, _kick(0.8), at(b, e))
                for e in (1, 3, 5, 7):
                    _put(drums, _noise_hit(rnd, 0.09, 45) * 0.26, at(b, e))
                for e in (2, 6):
                    _put(drums, _noise_hit(rnd, 0.15, 30, bright=0.8) * 0.2, at(b, e))
            elif cfg["drums"] == "heart":
                _put(drums, _kick(0.7), at(b, 0)); _put(drums, _kick(0.45), at(b, 1))
        # keys
        if cfg["keys"] == "ep":
            for e, g in ((0, 1.0), (3, 0.55)) if b % 2 == 0 else ((0, 1.0), (5, 0.5)):
                for m in ch:
                    _put(keys, _ep(NOTE(m), bar * 0.9) * g / len(ch), at(b, e) + rnd.uniform(0, 0.012))
        elif cfg["keys"] == "stab":
            for e in (0, 3, 6):
                for m in ch:
                    _put(keys, _pluck(NOTE(m), 0.5, 7) * 0.8 / len(ch), at(b, e))
        # bass
        if cfg["bass"] == "half":
            _put(bass, _bass(root, beat * 1.8), at(b, 0)); _put(bass, _bass(root * (1.5 if b % 2 else 1), beat * 1.6), at(b, 4))
        elif cfg["bass"] == "eighth":
            for e in range(8):
                _put(bass, _bass(root, beat * 0.42) * (1 if e % 2 == 0 else 0.7), at(b, e))
        else:
            _put(bass, _bass(root, bar * 0.97) * 0.8, at(b, 0))
        # arpeggio
        if cfg["arp"]:
            notes = ch + [ch[1] + 12, ch[2] + 12, ch[1] + 12, ch[3]]
            step = beat / 4 if cfg["drums"] == "four" else beat / 2
            k = 0
            while k * step < bar - 1e-6:
                if cfg["drums"] == "four" or rnd.random() < 0.6:
                    _put(arp, _pluck(NOTE(notes[k % len(notes)] + 12), 0.6, 8 if cfg["drums"] == "four" else 4.5),
                         b * bar + k * step)
                k += 1
    padbed = pad(duration + 2, mood="calm", seed=seed)[:n].astype(np.float64) if cfg["pad"] else np.zeros(n)
    if cfg["pad"] and transpose:                         # keep the pad in the same key: resample by the transpose ratio
        r = 2 ** (transpose / 12); idx = np.arange(n) * r
        full = pad(duration * r + 2, mood="calm", seed=seed).astype(np.float64)
        padbed = np.interp(idx, np.arange(len(full)), full)
    # arp echo
    if cfg["arp"]:
        d = int(beat * 0.75 * SR); echo = np.zeros(n); echo[d:] = arp[:-d] * 0.35; arp = arp + echo

    def norm(x): return x / (np.sqrt(np.mean(x ** 2)) + 1e-9)
    mix_ = (0.9 * norm(drums) + 0.75 * norm(keys if cfg["keys"] else padbed) + 0.7 * norm(bass)
            + (0.45 * norm(arp) if cfg["arp"] else 0) + cfg["pad"] * 0.6 * norm(padbed))
    mix_ = np.tanh(mix_ / (np.max(np.abs(mix_)) + 1e-9) * 1.6) / np.tanh(1.6)   # gentle glue
    if style == "lofi":                                  # warm it up and add a faint vinyl bed
        mix_ = np.convolve(mix_, np.ones(4) / 4, mode="same")
        crackle = np.zeros(n); pos = rnd.integers(0, n, size=int(duration * 6))
        crackle[pos] = rnd.uniform(-0.25, 0.25, size=len(pos))
        mix_ += np.convolve(crackle, np.ones(3) / 3, mode="same") + rnd.standard_normal(n) * 0.004
    fade = int(0.25 * SR); mix_[:fade] *= np.linspace(0, 1, fade)
    tail = int(1.6 * SR); mix_[-tail:] *= np.linspace(1, 0, tail)
    return (mix_ / (np.max(np.abs(mix_)) + 1e-9)).astype(np.float32)


def whoosh(length=0.45, seed=0):
    rnd = np.random.default_rng(seed)
    n = int(length * SR)
    x = rnd.standard_normal(n)
    env = np.sin(np.linspace(0, np.pi, n)) ** 2
    # brighten towards the middle by mixing a high-passed copy
    hp = np.diff(x, prepend=0)
    y = (0.6 * x + 0.8 * hp * np.sin(np.linspace(0, np.pi, n))) * env
    y = np.convolve(y, np.ones(12) / 12, mode="same")
    return (y / (np.max(np.abs(y)) + 1e-9)).astype(np.float32)


def _envelope(x, win=0.05, attack=0.03, release=0.35):
    w = max(1, int(win * SR))
    rms = np.sqrt(np.convolve(x ** 2, np.ones(w) / w, mode="same"))
    env = np.empty_like(rms); acc = 0.0
    a_up, a_dn = 1 - np.exp(-1 / (attack * SR)), 1 - np.exp(-1 / (release * SR))
    for i in range(len(rms)):
        acc += (a_up if rms[i] > acc else a_dn) * (rms[i] - acc); env[i] = acc
    return env


MUSIC_LEVEL = 0.30     # backing track RMS relative to the voice RMS, before ducking (~-10 dB)
DUCK = 0.5             # how far the track dips while the voice is speaking (to ~-16 dB under the voice)


def mix(voice, scene_starts, mood="calm", music=True, sfx=True, slug=""):
    """voice: float32 mono at SR. music: True/False or a style name (see STYLES).
    Returns the final mono mix (pre-loudnorm)."""
    n = len(voice)
    out = voice.astype(np.float64).copy()
    active = np.abs(voice) > 0.01
    vrms = np.sqrt(np.mean(voice[active] ** 2)) if active.any() else 0.1
    choice = pick(slug, music)
    if choice:
        style, loop, tr = choice
        bed = backtune(n / SR, style, loop, tr, seed=zlib.crc32(slug.encode()) & 0xFFFF).astype(np.float64)[:n]
        if len(bed) < n: bed = np.pad(bed, (0, n - len(bed)))
        env = _envelope(voice[::4].astype(np.float64)) if n > 8 else np.zeros(1)
        env = np.repeat(env, 4)[:n]
        if len(env) < n: env = np.pad(env, (0, n - len(env)), mode="edge")
        duck = np.clip(env / (vrms + 1e-9), 0, 1)
        brms = np.sqrt(np.mean(bed ** 2)) + 1e-9
        out += bed / brms * vrms * MUSIC_LEVEL * (1 - DUCK * duck)
    if sfx:
        for k, s in enumerate(scene_starts[1:], 1):
            w = whoosh(seed=k) * vrms * 0.35
            i = max(0, int((s - 0.22) * SR))
            out[i:i + len(w)] += w[:max(0, min(len(w), n - i))]
    return out.astype(np.float32)
