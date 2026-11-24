---
name: soccer365-episode
description: Make one Soccer 365 satirical football cartoon Short end to end (facts → idea → scene → sound → QA → posts → push). Use whenever the owner asks for a new video, a remake ("làm lại", "nhạt", "không hấp dẫn", "lộn xộn"), or posts for one.
---
# Soccer 365 episode skill

Talk to the owner in **Vietnamese**; everything on screen and in posts is **English**. Never mention AI in posts. Act without asking; stop only for false facts, hate, real money, or posting on the owner's accounts.

## 0. Read first (once per session)
`funny-football/studio/HANDOFF.md` → `CHECKLIST.md` (every owner lesson) → `SOUND_BIBLE.md` → `SOCIAL_COPY.md`.

## 1. Facts (Rule 0)
- `toon2/epNN/facts.md`: every real detail with date and **2+ sources**; mark what is invented.
- Never show an invented quote as real. Weekdays and dates: compute, don't guess.

## 2. Idea: must be engaging, not a recap
- One-line logline: who wants what → what blocks them → surprising end.
- **One central visual gag that escalates** each beat (Ep40 v4: every missed ball flies out of the TV: crack → popcorn → ceiling → rolls out → player climbs out).
- Cold open = the strangest moment in the first second. Characters big in the first 8 s.
- Max 2 faces per shot (3 only in the final line-up); one caption at a time, ≤7 words.
- Ending: two-sided question + series promise. Plant 2+ hidden details.
- Gates: `python3 toon2/script_gate.py toon2/epNN/spec.json` and `novelty.py` (run against the registry **without** the candidate row).

## 3. Scene (`toon2/epNN/scene.html`, canvas)
- Cast: `chibi.js` body + `castimg.js` caricature heads (`CASTIMG.preload([...])`); helpers `card`, `stamp`, `CB` (copy from the previous episode).
- Camera: `shots.js` (≥5 types, never the same twice in a row). Transitions on every cut: `MOTION.cut(ctx, t, tCut, 'whip'|'flash'|'leak'|'iris')`; pop-ins with `MOTION.spring` (`motion.js`).
- Check: `node --check` on the extracted script, then `node toon2/snap.js toon2/epNN/scene.html out.jpg t1,t2,... cols` and **look** at the sheet; fix overlap, hidden faces, off-frame action.
- Pitfall: never append `// comment` mid-line in one-line functions.

## 4. Sound (`toon2/epNN/audio.py`)
- `music.py` genre not used in the last 6 episodes (registry column `music`); new seed/key.
- `fx2.py`: a signature sound per gag (`record_scratch`, `sub_boom`, `fail_horn`, `clang`, `boom`, ...). Voices `vo()`; running laugh/catchphrase grows each time. ElevenLabs only if free credits remain.

## 5. Render + QA
```
cd funny-football/toon2
node epNN/make_cover.js epNN/release/cover-9x16.jpg
SCRATCH=/tmp/claude-0 ./render_par.sh epNN audio.py /tmp/claude-0/raw.mp4 4
cp /tmp/claude-0/raw.mp4 /tmp/claude-0/c.mp4 && ./add_cover.sh /tmp/claude-0/c.mp4 epNN/release/cover-9x16.jpg
ffmpeg -y -i /tmp/claude-0/c.mp4 -c:v copy -af "loudnorm=I=-14:TP=-2:LRA=11,aresample=192000,alimiter=limit=0.6:level=false,aresample=48000" -c:a aac -b:a 192k -movflags +faststart epNN/release/<name>-9x16.mp4
python3 qa.py epNN/release/<name>-9x16.mp4      # must print QA PASS (15–30 s)
```

## 6. Records + posts + ship
- **Posts must pass `python3 funny-football/studio/post_gate.py toon2/epNN/release/POSTS.md`** (a PreToolUse hook also blocks SendUserFile on failure). When the owner corrects a post, add a CHECK to post_gate.py — a note alone is not enough.
- Update `studio/EPISODES.csv` (one row), `GAG_BANK.md`, `spec.json`; posts in `epNN/release/POSTS.md` (YouTube title + 3 hashtags incl. #shorts, description, tags, settings; TikTok; Instagram + alt text + pinned comment; X ≤280; Facebook short lines; "Cartoon parody · invented lines").
- Keep old versions as `scene_vN_<name>.html` backups. Commit with the session attribution lines, push to the working branch, send the mp4 + POSTS.md with SendUserFile, report in Vietnamese.
