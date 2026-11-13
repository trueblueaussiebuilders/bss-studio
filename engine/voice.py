"""Voiceover: Kokoro (free, local) by default; ElevenLabs when voice.json says so and the secrets are set."""
import json, os, re, subprocess, urllib.request, urllib.error
import numpy as np
from engine.style import END_HOLD

SR = 24000
KOKORO_URL = "https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/"
KOKORO_DIR = os.environ.get("KOKORO_DIR", os.path.expanduser("~/.cache/kokoro"))


def _decode(data: bytes) -> np.ndarray:
    """Any audio bytes -> mono float32 at SR, via ffmpeg."""
    out = subprocess.run(["ffmpeg", "-loglevel", "error", "-i", "pipe:0", "-f", "f32le", "-ac", "1", "-ar", str(SR), "pipe:1"],
                         input=data, capture_output=True, check=True).stdout
    return np.frombuffer(out, dtype=np.float32).copy()


ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _voice_candidates():
    cfg = json.load(open(os.path.join(ROOT, "voice.json")))
    env = os.environ.get("ELEVENLABS_VOICE_ID", "").strip()
    cands = cfg["elevenlabs_voices"]
    if env and " " not in env and len(env) >= 15:     # a real-looking override wins; placeholder text is ignored
        cands = [{"name": "secret override", "id": env}] + cands
    return cands, cfg.get("model", "eleven_multilingual_v2")


def _tts(key, voice_id, model, line, prev=None, nxt=None):
    body = {"text": line, "model_id": model,
            "voice_settings": {"stability": 0.55, "similarity_boost": 0.75, "style": 0.0, "use_speaker_boost": True}}
    if prev: body["previous_text"] = prev      # neighbouring text keeps intonation consistent across lines
    if nxt: body["next_text"] = nxt
    req = urllib.request.Request(
        f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}?output_format=mp3_44100_128",
        data=json.dumps(body).encode(), method="POST",
        headers={"xi-api-key": key, "Content-Type": "application/json", "Accept": "audio/mpeg"})
    with urllib.request.urlopen(req, timeout=120) as r:
        return _decode(r.read())


def _elevenlabs(lines):
    key = os.environ["ELEVENLABS_API_KEY"].strip().strip('"').strip("'")
    if " " in key or len(key) < 20:
        raise SystemExit(f"ELEVENLABS_API_KEY secret doesn't look like a real key (length {len(key)}). Paste the key itself.")
    cands, model = _voice_candidates()
    errors = []
    for v in cands:                      # pick the first voice this account can use
        try:
            lines = [speakable(x) for x in lines]
            first = _tts(key, v["id"], model, lines[0], nxt=lines[1] if len(lines) > 1 else None)
            print(f"ElevenLabs voice: {v['name']} ({v['id']})")
            break
        except urllib.error.HTTPError as e:
            msg = e.read().decode(errors="replace")[:200]
            errors.append(f"{v['name']}: HTTP {e.code} {msg}")
            if e.code == 401: break      # bad key, no point trying other voices
    else:
        raise SystemExit("No ElevenLabs voice worked:\n  " + "\n  ".join(errors) +
                         "\n(402 'payment_required' means the free plan can't use Voice Library voices via the API.)")
    if errors and "HTTP 401" in errors[-1]:
        raise SystemExit("ElevenLabs rejected the API key (401):\n  " + errors[-1])
    out = [first]
    for i in range(1, len(lines)):
        out.append(_tts(key, v["id"], model, lines[i], prev=lines[i - 1], nxt=lines[i + 1] if i + 1 < len(lines) else None))
    return out


def _lexicon():
    p = os.path.join(ROOT, "lexicon.json")
    return json.load(open(p)) if os.path.exists(p) else {"say": {}, "ipa": {}}


def speakable(line):
    """Text swaps from lexicon.json (acronyms, units, respellings). Applied to the audio only."""
    for pat, rep in _lexicon().get("say", {}).items():
        line = re.sub(pat, rep, line)
    return re.sub(r"\s{2,}", " ", line).strip()


def _kokoro(lines):
    from kokoro_onnx import Kokoro
    os.makedirs(KOKORO_DIR, exist_ok=True)
    for f in ("kokoro-v1.0.onnx", "voices-v1.0.bin"):
        p = os.path.join(KOKORO_DIR, f)
        if not os.path.exists(p):
            print("downloading", f); urllib.request.urlretrieve(KOKORO_URL + f, p)
    k = Kokoro(os.path.join(KOKORO_DIR, "kokoro-v1.0.onnx"), os.path.join(KOKORO_DIR, "voices-v1.0.bin"))
    voice = os.environ.get("KOKORO_VOICE") or _cfg().get("kokoro_voice", "bf_emma")
    speed = _cfg().get("kokoro_speed", 1.0)
    lang = _cfg().get("kokoro_lang") or ("en-gb" if voice[:1] == "b" else "en-us")
    ipa = _lexicon().get("ipa", {})
    out = []
    for line in lines:
        text = speakable(line)
        ph = k.tokenizer.phonemize(text, lang)
        for word, target in ipa.items():
            if re.search(rf"\b{re.escape(word)}\b", text):
                default = k.tokenizer.phonemize(word, lang).strip()
                if default and default in ph:
                    ph = ph.replace(default, target)
                else:
                    print(f"lexicon: couldn't place '{word}' in: {text}")
        a = k.create(ph, voice=voice, speed=speed, lang=lang, is_phonemes=True,
                     clause_pause=0.06, sentence_pause=0.2)[0].astype(np.float32)
        out.append(_tighten(a))
    return out


def _tighten(a, max_gap=None, thresh=0.012):
    """Shorten any silence inside a sentence to max_gap, so the read flows without odd mid-phrase stops."""
    max_gap = _cfg().get("max_gap", 0.2) if max_gap is None else max_gap
    win = int(0.01 * SR)
    env = np.convolve(np.abs(a), np.ones(win) / win, mode="same")
    quiet = env < thresh
    keep, i, n = np.ones(len(a), bool), 0, len(a)
    lim = int(max_gap * SR)
    while i < n:
        if quiet[i]:
            j = i
            while j < n and quiet[j]: j += 1
            if i > 0 and j < n and j - i > lim:
                cut0 = i + lim // 2
                keep[cut0: cut0 + (j - i - lim)] = False
            i = j
        else:
            i += 1
    return a[keep]


def _cfg():
    return json.load(open(os.path.join(ROOT, "voice.json")))


def engine_name():
    """voice.json decides. ElevenLabs is only used when chosen there and a key is set."""
    eng = os.environ.get("VOICE_ENGINE") or _cfg().get("engine", "kokoro")
    if eng == "elevenlabs" and not os.environ.get("ELEVENLABS_API_KEY", "").strip():
        return "kokoro"
    return eng


def synth(lines):
    return {"elevenlabs": _elevenlabs}.get(engine_name(), _kokoro)(lines)


def _trim(a, thresh=0.01):
    """Strip leading/trailing silence so timings are tight regardless of engine."""
    idx = np.where(np.abs(a) > thresh)[0]
    if len(idx) == 0: return a
    return a[max(0, idx[0] - int(0.03 * SR)): idx[-1] + int(0.08 * SR)]


LEAD = 0.15   # voice starts this long after each scene starts


def _tempo(a, factor):
    if abs(factor - 1.0) < 1e-3: return a
    raw = subprocess.run(["ffmpeg", "-loglevel", "error", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", "pipe:0",
                          "-af", f"atempo={factor}", "-f", "f32le", "-ar", str(SR), "-ac", "1", "pipe:1"],
                         input=a.astype(np.float32).tobytes(), capture_output=True, check=True).stdout
    return np.frombuffer(raw, dtype=np.float32).copy()


def narrate(lines, gap=None):
    """lines: one narration string per scene.
    Returns (durations, subtitles, track): per-scene seconds, per-scene [(start, end, sentence)], float32 audio."""
    ecfg = _cfg().get(engine_name(), {}) if isinstance(_cfg().get(engine_name()), dict) else {}
    tempo = ecfg.get("tempo", 1.0)
    gap = ecfg.get("line_gap", 0.35) if gap is None else gap
    sg = _cfg().get("sentence_gap", 0.28)
    split = [[x for x in re.split(r"(?<=[.!?])\s+", (line or "").strip()) if x] for line in lines]
    flat = [x for parts in split for x in parts]
    audio = iter(_tempo(_trim(a), tempo) for a in synth(flat)) if flat else iter(())
    durs, subs, clips = [], [], []
    for k, parts in enumerate(split):
        t, chunks, sub = LEAD, [], []
        for i, sent in enumerate(parts):
            if i:
                chunks.append(np.zeros(int(sg * SR), dtype=np.float32)); t += sg
            a = next(audio); chunks.append(a)
            sub.append((round(t, 3), round(t + len(a) / SR, 3), sent)); t += len(a) / SR
        clip = np.concatenate(chunks) if chunks else np.zeros(1, dtype=np.float32)
        last = k == len(split) - 1
        durs.append(round(max(3.2, t + (END_HOLD if last else gap)), 3))
        subs.append(sub); clips.append(clip)
    total = sum(durs)
    track = np.zeros(int((total + 0.5) * SR), dtype=np.float32)
    t = 0.0
    for d, c in zip(durs, clips):
        i = int((t + LEAD) * SR); track[i:i + len(c)] += c; t += d
    return durs, subs, track[:int(total * SR)]
