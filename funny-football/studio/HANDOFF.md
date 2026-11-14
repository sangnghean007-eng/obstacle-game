# HANDOFF: read this first in any new or continued session

This channel makes funny satirical football cartoon Shorts (YouTube channel **Soccer 365 – @Soccer365days**, plus TikTok, Instagram, Facebook and X).

## Who you work for and how
- Talk to the user **in Vietnamese**. Every deliverable (video text, titles, posts) is in **English**.
- Standing order: **the team decides, then builds.**
  - For every video, run the pre-production room (parallel agents), merge the best ideas, build the video, run the post-production review room, fix, and ship.
  - Do not stop to ask the user to approve a script.
- Facts must be real and checked against 2 or more sources (`toon2/epN/facts.md`). Everything else is labelled "parody".
- Never copy other creators' art or use copyrighted footage. Use inspiration only.
- Do not create PRs unless asked. Keep the user's personal details private.

## Where things are
- Branch: **`claude/new-session-e2g4yg`** (all work is here).
- `studio/PLAYBOOK.md`: all rules. The latest sections win: "v3 house style" and "Approved template (Ep4 v4)".
- `studio/REVIEW_ROOM.md`, `scorecard.csv`, `performance.csv`, `IDEAS.md`.
- Character systems:
  - `toon2/chibi.js` + `toon2/chibi_cast.js`: the **current style**, big-head chibi.
  - `toon2/toon2.js` + `cast.js`: the older style.
- Sound: `toon2/sfx/synth.py` (music and foley kit). Voices are not used by default. If one is ever needed, use `make_pico.py`.
- **Approved template:** `toon2/ep4/scene.html` (Ep4 v4 "CAN'T MOVE HIM") + `toon2/ep4/audio.py` + `toon2/ep4/release/*` (posts: YOUTUBE, TIKTOK, INSTAGRAM, FACEBOOK, X).
- Render: `node toon2/epN/render.js <outdir> 30` → ffmpeg H.264 1080x1920 30 fps + `python3 audio.py out.wav`.

## Episodes so far

| Episode | Topic | Status |
|---|---|---|
| Ep1 | "The GOATs Clock Out" (`goats/`) | Released earlier |
| Ep2 | "The GOAT Dictionary" (`toon2/ep2/`) | About 2k views on YouTube |
| Ep3 | "RETIRED?!" v4 (`toon2/ep3/`): Messi Golden Boot | Older style |
| Ep4 | v4 "CAN'T MOVE HIM" (`toon2/ep4/`): Traoré vs Cucurella | **User approved: "keep it up like this"** |

## Environment setup for a fresh container
```
apt-get install -y -q libttspico-utils espeak-ng mbrola mbrola-us2 mbrola-us3
```
Playwright, Chromium, ffmpeg, numpy and scipy are already available.

## Next
- Ep5 "SECRET PLAN" (Ronaldo reads Danilo's tactics) is done (`toon2/ep5/`). Next: Ep6.
- Use the Ep4 v4 template: hook, MISSION card, 5 hearts and 5 attempts, GAME OVER, twist, thanks + FOLLOW.
- Ask the user for platform stats after each release, and log them in `performance.csv`.

## Daily learning (scheduled task, 6:44 am Australia/Sydney)
- **What it does:** a fresh session runs every morning. It hunts 3 verified topic ideas (appended to `IDEAS.md`), learns one skill on the rotation (appended to `LEARNING_LOG.md`) and pushes to this branch.
- **Limits:** it never posts, never makes videos and never edits `PLAYBOOK.md` directly. Proposed playbook changes go in the log entry for the producer to apply.
