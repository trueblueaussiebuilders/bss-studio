"""Procedural music bed (soft pad + sparse plucks) and transition whooshes, ducked under the voice.
Everything is generated here, so there are no music licensing issues."""
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


def mix(voice, scene_starts, mood="calm", music=True, sfx=True):
    """voice: float32 mono at SR. Returns the final mono mix (pre-loudnorm)."""
    n = len(voice)
    out = voice.astype(np.float64).copy()
    active = np.abs(voice) > 0.01
    vrms = np.sqrt(np.mean(voice[active] ** 2)) if active.any() else 0.1
    if music:
        bed = pad(n / SR, mood=mood).astype(np.float64)[:n]
        env = _envelope(voice[::4].astype(np.float64)) if n > 8 else np.zeros(1)
        env = np.repeat(env, 4)[:n]
        if len(env) < n: env = np.pad(env, (0, n - len(env)), mode="edge")
        duck = np.clip(env / (vrms + 1e-9), 0, 1)
        brms = np.sqrt(np.mean(bed ** 2)) + 1e-9
        out += bed / brms * vrms * 0.16 * (1 - 0.45 * duck)
    if sfx:
        for k, s in enumerate(scene_starts[1:], 1):
            w = whoosh(seed=k) * vrms * 0.35
            i = max(0, int((s - 0.22) * SR))
            out[i:i + len(w)] += w[:max(0, min(len(w), n - i))]
    return out.astype(np.float32)
