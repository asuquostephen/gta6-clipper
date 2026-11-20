#!/usr/bin/env python3
"""
build_clip.py — production script for the gta6-clipper-01 make.fun entry clip.

Creative decisions (made by the agent in this session, per the bounty rules):
- Moment: in Sxzxr's "Fighting a CROCODILE in Gta 6... GONE WRONG"
  (https://www.youtube.com/watch?v=WePzBSGkDzw, uploaded 2026-11-18), the player
  wades up to a crocodile in the Leonida swamps, aims at it, walks straight at
  it with his bare hands, gets charged, death-rolled and WASTED. It is a fresh
  moment for the Leonida Uncut channel (not the Champs Network ocean escape,
  not the Jumbo shark, not the Rubhen925 Lucia/Jason reaction) and it fits the
  channel's best format: a wild NPC/animal reaction with a built-in payoff.
- Structure (hook first, per channel rules): cold-open on the death roll
  (source 59.2-62.5s), rewind to the walk-up (source 45.0-55.75s at 1.25x),
  replay the death roll with a zoom punch-in as the payoff (source
  58.8-61.1s), then the make.fun pitch over the frozen WASTED frame, then a
  debate-question beat over the jaws-open standoff (source 50.5-53.2s), then
  the channel end card.
- The bounty pitch (required by gta6-clipper-01): after the GTA 6 moment, the
  clip itself tells viewers they can make money on make.fun by making clips
  with AI — in the voiceover ("You can make clips like this with AI and earn
  real money on make dot fun") AND as on-screen text naming make.fun and this
  bounty's page (make.fun/bounty/gta6-clipper-01).
- Vertical crop: the source is a livestream VOD with the streamer's facecam at
  bottom-right and chat at top-right. The 607x1080 crop at x=480 keeps the
  player + crocodile centred and excludes the facecam and chat entirely.
- Audio: voiceover only. The source audio is the streamer's own live speech,
  so it is not mixed under the commentary (same call as the channel's
  ocean-escape Short, whose source was video-only).
- Captions (channel rule set 2026-11-20): SMALL and LIGHT — Liberation Sans
  regular weight, thin 2px outline, lower-third position, short chunks —
  never the old big bold style, never over faces.

Inputs (paths relative to the channel workspace):
  footage/gta6-croc-fight-sxzxr.mp4   full source VOD section (71s)
  shorts/short_clipper1-vo.mp3        AI voiceover (tts, voice avocado_v2:MAI_03;
                                      plain punctuation + speed 115 — em-dashes
                                      and ellipses made this TTS voice stall)
  shorts/endcard.png                  shared Leonida Uncut end card
Output (this rebuild writes into entry-v2, not the channel folder):
  entry-v2/render/short_clipper1.mp4  1080x1920, ~26s, plus short_clipper1.srt

Run:  python3 scripts/build_clip.py [channel_dir] [entry_v2_dir]
"""

import subprocess
import sys
from pathlib import Path

CHANNEL = Path(sys.argv[1] if len(sys.argv) > 1 else "~/workspace/youtube-channel").expanduser()
ENTRY = Path(sys.argv[2] if len(sys.argv) > 2 else "~/workspace/makefun-builds/gta6-clipper-01/entry-v2").expanduser()
SRC = CHANNEL / "footage" / "gta6-croc-fight-sxzxr.mp4"
VO = CHANNEL / "shorts" / "short_clipper1-vo.mp3"
ENDCARD = CHANNEL / "shorts" / "endcard.png"
RENDER = ENTRY / "render"
RENDER.mkdir(parents=True, exist_ok=True)
OUT = RENDER / "short_clipper1.mp4"
SRT = RENDER / "short_clipper1.srt"
# Scratch lives in the workspace, NOT /tmp: on this VM /tmp is a 512MB tmpfs
# and a CRF19 segment encode can fill it mid-write ("No space left on device").
WORK = ENTRY / "work"
WORK.mkdir(parents=True, exist_ok=True)

FONT_BOLD = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
FONT_REG = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"

VO_TEXT = (
    "He tried to fight a crocodile in GTA 6, bare hands. "
    "Look at the size of this thing. "
    "Jaws open, and he still walks straight at it. "
    "Bad idea. "
    "The croc charges, and it is over in seconds. "
    "Death roll. Wasted. "
    "Now the crazy part. "
    "An AI agent cut this clip. "
    "You can make clips like this with AI and earn real money on make dot fun. "
    "Link in the description. "
    "Would you fight the croc? "
    "Subscribe for daily GTA 6 clips."
)
VO_DUR = 23.808  # measured from the generated voiceover file


def run(cmd):
    r = subprocess.run([str(c) for c in cmd], capture_output=True, text=True)
    if r.returncode != 0:
        print(r.stderr[-3000:])
        raise SystemExit(f"command failed: {' '.join(str(c) for c in cmd[:8])}")


def fmt(t):
    h = int(t // 3600); m = int((t % 3600) // 60); s = int(t % 60)
    ms = int(round((t - int(t)) * 1000))
    if ms == 1000:
        s += 1; ms = 0
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def caption_chunks():
    """Word-proportional caption timings, 5-word chunks (short lines)."""
    words = VO_TEXT.split()
    chunks = [" ".join(words[i:i + 5]) for i in range(0, len(words), 5)]
    total = sum(len(c.split()) for c in chunks)
    out, t = [], 0.0
    for c in chunks:
        d = VO_DUR * len(c.split()) / total
        out.append((t, t + d, c))
        t += d
    return out


def write_srt():
    lines = []
    for i, (a, b, c) in enumerate(caption_chunks()):
        lines.append(f"{i + 1}\n{fmt(a)} --> {fmt(b)}\n{c}\n")
    SRT.write_text("\n".join(lines))


def write_ass():
    """The burn-in caption file. An explicit PlayRes of 1080x1920 is
    essential: force_style FontSize on an SRT is read against libass's
    384x288 default PlayRes, which blew the captions up to ~280px tall in
    the first render — exactly the 'words block the view' failure the
    channel rule exists to prevent. At PlayRes 1080x1920, FontSize 44 is
    genuinely small, regular weight, thin outline, lower third."""
    def afmt(t):
        h = int(t // 3600); m = int((t % 3600) // 60); s = t % 60
        return f"{h}:{m:02d}:{s:05.2f}"
    lines = [
        "[Script Info]",
        "ScriptType: v4.00+",
        "PlayResX: 1080",
        "PlayResY: 1920",
        "ScaledBorderAndShadow: yes",
        "",
        "[V4+ Styles]",
        "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, "
        "OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, "
        "ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, "
        "Alignment, MarginL, MarginR, MarginV, Encoding",
        "Style: Default,Liberation Sans,44,&H00FFFFFF,&H00FFFFFF,&H00000000,"
        "&H00000000,0,0,0,0,100,100,0,0,1,2,0,2,40,40,150,1",
        "",
        "[Events]",
        "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text",
    ]
    for a, b, c in caption_chunks():
        lines.append(f"Dialogue: 0,{afmt(a)},{afmt(b)},Default,,0,0,0,,{c}")
    p = WORK / "captions.ass"
    p.write_text("\n".join(lines) + "\n")
    return p


def dt(text, font, size, x, y, enable=None):
    s = (
        f"drawtext=fontfile={font}:text='{text}':fontsize={size}:fontcolor=white"
        f":borderw=3:bordercolor=black:x={x}:y={y}"
    )
    if enable:
        s += f":enable='{enable}'"
    return s


CROP = "crop=607:1080:480:0,scale=1080:1920"
NORM = "fps=30,format=yuv420p,setsar=1"
# NOTE: no colon in drawtext strings — this ffmpeg build's parser ends the
# text option at a colon even inside quotes, so the credit uses a hyphen.
CREDIT = dt("Gameplay - Sxzxr", FONT_REG, 30, 24, 36)


def cut(name, start, dur, vf):
    out = WORK / name
    run(["ffmpeg", "-y", "-v", "error", "-ss", start, "-i", SRC, "-t", dur,
         "-vf", vf, "-an", "-c:v", "libx264", "-preset", "veryfast", "-crf", "19", out])
    return out


write_srt()

# A — hook: the death roll, cold open (source 59.2-62.5)
a = cut("seg_a.mp4", 59.2, 3.3, ",".join([
    CROP, dt("HE TRIED TO FIGHT A CROCODILE!", FONT_BOLD, 46, "(w-text_w)/2", 150), CREDIT, NORM]))
# B — story: walk-up, aim, standoff (source 45.0-55.75 at 1.25x).
# Two steps: setpts on the input-seek pass silently kept full length in
# practice (the segment came out 10.77s, not 8.6s), so cut at normal speed
# first, then speed the cut file, where setpts works reliably.
b = cut("seg_b_raw.mp4", 45.0, 10.75, ",".join([
    CROP,
    dt("10 SECONDS EARLIER...", FONT_BOLD, 38, "(w-text_w)/2", 150, "between(t,0,2.0)"),
    CREDIT, NORM]))
b_fast = WORK / "seg_b.mp4"
run(["ffmpeg", "-y", "-v", "error", "-i", b,
     "-vf", f"setpts=PTS/1.25,{NORM}", "-t", "8.6",
     "-c:v", "libx264", "-preset", "veryfast", "-crf", "19", b_fast])
b = b_fast
# C — payoff replay: death roll with a zoom punch-in (source 58.8-61.1)
c = cut("seg_c.mp4", 58.8, 2.3, ",".join([
    "crop=500:1080:620:0,scale=1080:1920",
    dt("DEATH ROLL!", FONT_BOLD, 46, "(w-text_w)/2", 150), CREDIT, NORM]))
# D — pitch card: frozen WASTED frame (source 63.8s), darkened, pitch text
frame = WORK / "wasted.png"
run(["ffmpeg", "-y", "-v", "error", "-ss", 63.8, "-i", SRC, "-frames:v", "1",
     "-vf", f"{CROP},eq=brightness=-0.28:saturation=0.7", frame])
d = WORK / "seg_d.mp4"
run(["ffmpeg", "-y", "-v", "error", "-loop", "1", "-i", frame, "-t", 6.9,
     "-vf", ",".join([
         dt("AN AI AGENT MADE THIS CLIP", FONT_BOLD, 34, "(w-text_w)/2", 700),
         dt("Make clips like this with AI", FONT_REG, 38, "(w-text_w)/2", 790),
         dt("EARN MONEY ON make.fun", FONT_BOLD, 46, "(w-text_w)/2", 880),
         dt("make.fun/bounty/gta6-clipper-01", FONT_REG, 32, "(w-text_w)/2", 980),
         NORM]),
     "-c:v", "libx264", "-preset", "veryfast", "-crf", "19", d])
# E — debate beat: jaws-open standoff (source 50.5-53.2)
e = cut("seg_e.mp4", 50.5, 2.7, ",".join([
    CROP, dt("WOULD YOU FIGHT THE CROC?", FONT_BOLD, 44, "(w-text_w)/2", 150), CREDIT, NORM]))
# F — channel end card, 2.4s
f = WORK / "seg_f.mp4"
run(["ffmpeg", "-y", "-v", "error", "-loop", "1", "-i", ENDCARD, "-t", 2.4,
     "-vf", f"scale=1080:1920,{NORM}",
     "-c:v", "libx264", "-preset", "veryfast", "-crf", "19", f])

# Assemble: concat the six segments, burn the (small, light) captions, add
# VO padded with silence so the end card survives (a plain -shortest cut
# the first render at the VO's 23.808s and ate the end card).
ASS = write_ass()
run([
    "ffmpeg", "-y", "-v", "error",
    "-i", a, "-i", b, "-i", c, "-i", d, "-i", e, "-i", f, "-i", VO,
    "-filter_complex",
    "[0:v][1:v][2:v][3:v][4:v][5:v]concat=n=6:v=1:a=0,"
    f"subtitles={ASS}[vout];[6:a]apad=whole_dur=26.4[aout]",
    "-map", "[vout]", "-map", "[aout]",
    "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p",
    "-c:a", "aac", "-b:a", "128k", "-t", "26.3", OUT,
])
print("wrote", OUT)
