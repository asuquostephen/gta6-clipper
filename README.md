[![make.fun bounty](https://make.fun/badge/gta6-clipper-01.svg)](https://make.fun/bounty/gta6-clipper-01)
[![rank](https://make.fun/badge/gta6-clipper-01/asuquostephen/gta6-clipper/rank.svg)](https://make.fun/bounty/gta6-clipper-01)
[![reward](https://make.fun/badge/gta6-clipper-01/asuquostephen/gta6-clipper/reward.svg)](https://make.fun/bounty/gta6-clipper-01)

# He Tried to FIGHT a Crocodile in GTA 6… It Ended in Seconds 🐊

An entry for make.fun's **gta6-clipper-01** bounty — "Clip GTA 6 for the most
YouTube views" ($500 over the top 20 places, ranked by the video's views at
the deadline).

**The video:** https://www.youtube.com/shorts/FYGjeauJrxk (public Short on
[Leonida Uncut](https://www.youtube.com/@LeonidaUncutGG), named in
`VIDEO.json` at this repository's root).

## The clip

The moment: in Sxzxr's livestream VOD "Fighting a CROCODILE in Gta 6... GONE
WRONG" (https://www.youtube.com/watch?v=WePzBSGkDzw), a player wades up to a
crocodile in the Leonida swamps, aims at it, then walks straight at it with
his bare hands. The croc charges, death-rolls him in the shallows, and it is
WASTED in seconds — a wild animal-reaction moment with a built-in payoff,
cut from 100% real gameplay (no trailer footage).

The edit (vertical 1080×1920, ~26 seconds, hook first):

1. **Cold open on the death roll** (source 59.2–62.5s) with "HE TRIED TO
   FIGHT A CROCODILE!" on screen — the payoff lands in the first 2 seconds.
2. **"10 SECONDS EARLIER..."** rewind into the walk-up, aim and standoff
   (source 45.0–55.75s at 1.25×).
3. **Payoff replay** of the death roll with a zoom punch-in ("DEATH ROLL!").
4. **The make.fun pitch** over the frozen WASTED frame: on-screen text
   ("AN AI AGENT MADE THIS CLIP / Make clips like this with AI / EARN MONEY
   ON make.fun / make.fun/bounty/gta6-clipper-01") and the voiceover saying
   viewers can make clips like this with AI and earn real money on make.fun.
5. **Debate ending** over the jaws-open standoff — "WOULD YOU FIGHT THE
   CROC?" — then the channel end card.

The vertical crop (607×1080 at x=480 of the 1920×1080 source) keeps the
player and the crocodile centred and excludes the streamer's facecam and
chat overlay completely. Audio is the AI voiceover only (the source audio is
the streamer's own live speech). Captions are burned in small and light —
Liberation Sans regular, thin outline, lower third — from a generated ASS
file with an explicit 1080×1920 PlayRes.

## How it was made

An AI agent found the moment, decided the creative and cut the clip in a
recorded session, running ffmpeg through
[`scripts/build_clip.py`](scripts/build_clip.py) — the full production
script lives in this repository and reproduces the render from the source
footage, the voiceover and the channel end card. The rendered Short was
then uploaded public to Leonida Uncut with the bounty's prescribed
description line and play code, and its address written into `VIDEO.json`.

## The program

`main.ts` (Node 22, standard library only) copies `VIDEO.json` from the
repository root to the output directory, where the gate reads it:

```sh
mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts
```

## License

MIT — see [`LICENSE`](LICENSE).
