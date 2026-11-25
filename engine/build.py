"""Build one video: voiceover -> timings -> scenes -> mp4 (+ caption + cover).

  python -m engine.build videos/2026-11-16-abc --out out
  python -m engine.build videos/2026-11-16-abc --out out --frames 2 9.5 20     # PNG stills only (no voice needed)
  python -m engine.build videos/2026-11-16-abc --out out --sheet               # contact sheet of every scene
"""
import argparse, importlib.util, json, multiprocessing as mp, os, subprocess, tempfile
import numpy as np, soundfile as sf
from engine import render, voice, audio
from engine.style import W, H, FPS

SPEC = TL = None


def load_spec(folder):
    path = os.path.join(folder, "spec.py")
    s = importlib.util.spec_from_file_location("video_spec", path)
    m = importlib.util.module_from_spec(s); s.loader.exec_module(m)
    return m


def _render_scene(args):
    idx, outdir = args
    t0, t1 = TL.scenes[idx]
    f0, f1 = round(t0 * FPS), round(t1 * FPS)
    tmp, final = f"{outdir}/scene_{idx:02d}.tmp.mp4", f"{outdir}/scene_{idx:02d}.mp4"
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "bgr0", "-s", f"{W}x{H}",
           "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "veryfast", "-crf", "19", "-pix_fmt", "yuv420p", tmp]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    for f in range(f0, f1):
        s = render.draw_frame(SPEC, TL, f / FPS); s.flush(); p.stdin.write(bytes(s.get_data()))
    p.stdin.close()
    if p.wait() != 0: raise RuntimeError(f"scene {idx} failed")
    os.replace(tmp, final)
    return final


def _guess_timeline(spec):
    """Rough timings from word counts, for quick stills without running the voice."""
    durs, subs = [], []
    for sc in spec.SCENES:
        sents = [s for s in __import__("re").split(r"(?<=[.!?])\s+", sc.get("say", "").strip()) if s]
        t, sub = 0.15, []
        for s in sents:
            d = len(s.split()) / 2.9; sub.append((t, t + d, s)); t += d + 0.42
        first_hook = not durs and sc.get("type") == "hook"
        spoken = sub[-1][1] if sub else t
        durs.append(max(2.4, spoken + 0.45) if first_hook else max(3.2, t + 1.0)); subs.append(sub)
    durs[-1] += 2.6
    return render.Timeline(durs, subs)


def main():
    global SPEC, TL
    ap = argparse.ArgumentParser()
    ap.add_argument("folder"); ap.add_argument("--out", default="out")
    ap.add_argument("--frames", nargs="*", type=float)
    ap.add_argument("--sheet", action="store_true", help="contact sheet: the 85%% point of every scene")
    a = ap.parse_args()
    SPEC = load_spec(a.folder)
    slug = os.path.basename(os.path.normpath(a.folder))
    os.makedirs(a.out, exist_ok=True)
    tim_path = os.path.join(a.out, f"{slug}.timings.json")

    if a.frames is not None or a.sheet:
        if os.path.exists(tim_path):
            d = json.load(open(tim_path)); TL = render.Timeline(d["durations"], d["subs"])
        else:
            TL = _guess_timeline(SPEC)
        times = list(a.frames or [])
        if a.sheet:
            times += [s + 0.85 * (e - s) for s, e in TL.scenes]
        paths = []
        for t in times:
            p = os.path.join(a.out, f"{slug}_t{t:.1f}.png"); render.draw_frame(SPEC, TL, t).write_to_png(p); paths.append(p)
        render.draw_cover(SPEC, TL).write_to_png(os.path.join(a.out, f"{slug}_cover.png"))
        if a.sheet and paths:
            cols = min(5, len(paths)); rows = -(-len(paths) // cols)
            subprocess.run(["ffmpeg", "-y", "-loglevel", "error"] + sum([["-i", p] for p in paths], []) +
                           ["-filter_complex", "".join(f"[{i}]scale=360:-1[s{i}];" for i in range(len(paths))) +
                            "".join(f"[s{i}]" for i in range(len(paths))) +
                            f"xstack=inputs={len(paths)}:layout=" + "|".join(
                                f"{(i % cols) * 360}_{(i // cols) * 640}" for i in range(len(paths))) + ":fill=black",
                            os.path.join(a.out, f"{slug}_sheet.png")] if len(paths) > 1 else
                           ["-vf", "scale=360:-1", os.path.join(a.out, f"{slug}_sheet.png")], check=True)
        print(f"[{slug}] stills -> {a.out} (total ~{TL.duration:.1f}s)")
        if a.sheet:
            from engine import layout
            issues = layout.check(SPEC, TL)
            for msg in issues: print(f"[{slug}] LAYOUT {msg}")
            print(f"[{slug}] layout: {'clean' if not issues else f'{len(issues)} problem(s), fix before queueing'}")
        return

    print(f"[{slug}] voice: {voice.engine_name()}")
    hook_first = SPEC.SCENES and SPEC.SCENES[0].get("type") == "hook"
    durs, subs, track = voice.narrate([sc.get("say", "") for sc in SPEC.SCENES],
                                      first_gap=voice.HOOK_GAP if hook_first else None)
    json.dump({"durations": durs, "subs": subs}, open(tim_path, "w"))
    TL = render.Timeline(durs, subs)
    print(f"[{slug}] duration {TL.duration:.1f}s, {len(TL.scenes)} scenes")
    music = SPEC.META.get("music", True)
    choice = audio.pick(slug, music)
    if choice: print(f"[{slug}] music: {choice[0]} (loop {choice[1]}, transpose {choice[2]:+d})")
    mixed = audio.mix(track, TL.starts, mood=SPEC.META.get("mood", "calm"), music=music, sfx=music is not False, slug=slug)

    with tempfile.TemporaryDirectory() as tmp:
        sf.write(f"{tmp}/audio.wav", mixed, voice.SR)
        with mp.get_context("fork").Pool(os.cpu_count() or 2) as pool:
            files = pool.map(_render_scene, [(i, tmp) for i in range(len(TL.scenes))])
        with open(f"{tmp}/list.txt", "w") as f:
            f.writelines(f"file '{x}'\n" for x in files)
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", f"{tmp}/list.txt",
                        "-c", "copy", f"{tmp}/video.mp4"], check=True)
        final = os.path.join(a.out, f"{slug}.mp4")
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", f"{tmp}/video.mp4", "-i", f"{tmp}/audio.wav",
                        "-map", "0:v", "-map", "1:a", "-c:v", "copy",
                        "-af", "highpass=f=60,loudnorm=I=-14:TP=-1.5:LRA=11", "-ar", "48000", "-c:a", "aac", "-b:a", "160k",
                        "-shortest", "-movflags", "+faststart", final + ".tmp.mp4"], check=True)
        os.replace(final + ".tmp.mp4", final)
    open(os.path.join(a.out, f"{slug}.caption.txt"), "w").write(SPEC.CAPTION.strip() + "\n")
    png = os.path.join(a.out, f"{slug}.cover.png")
    render.draw_cover(SPEC, TL).write_to_png(png)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", png, "-q:v", "2", png[:-4] + ".jpg"], check=True)
    os.remove(png)
    print(f"[{slug}] -> {final}")


if __name__ == "__main__":
    main()
