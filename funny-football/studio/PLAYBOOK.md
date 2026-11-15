# Studio Playbook: football satire Shorts

This is the studio's living memory. After every episode, run a retro and update it (see "Retro" at the bottom).
Every rule here comes from either (U) user feedback, (R) the review room, or (W) external research. Sources are at the end.

## 0. House rules
- **All deliverables are in English** (video text, scripts, post copy, upload dossiers, studio docs) (U, 2026-11-12).

- **Accuracy first** (U, 2026-11-13). Every fact on screen and in captions must be verified before production, using the protocol in section 5. Content the user pastes (viral posts, fan pages) is treated as a lead, never as a source.

## 1. Non-negotiables (checked before every export)
- [ ] **Know who it is in 1 second, sound off** (U). For real people, use strong signifiers: kit colour and number, beard and hair silhouette, signature pose (e.g. SIUUU), height difference, big readable name tag of at least 56 px. Hand-drawn "likeness" from code alone tops out around 6/10 (U), so do not rely on it.
- [ ] **Story readable without words** (U, R). Each beat has at most 1 caption of at most 6 words in simple English. A Vietnamese 18-year-old must understand it. Ban words like "un-retire", "technically", "knockout" unless a visual explains them (R).
- [ ] **Frame 0 must stop the scroll** (performance data, Ep2 FB: 134 views but only 1 view of 3 s or more, because frame 0 was an empty stadium). Frame 0 shows the main characters big, mid-conflict, with the hook text already fully visible (no fade/pop-in) and a loud sound at 0.0 s.
- [ ] **Hook in frame 1** (W, R). The first frame must already be a clear, upright, big image plus a question or contradiction ("BOTH GOATs RETIRED. SAME YEAR?!"). Nothing static, nothing confusing (a spinning body read as an injury).
- [ ] **Follow end card** (U): every episode ends with `toon2/cta.js` (1.5 s: "+ FOLLOW" button tapped, bell, voice "Follow for more!"). Keep it at 1.5 s or less so the loop still works. Pin a comment that also asks to follow.
- [ ] **Loop** (W, R). The ending calls back to the opening (same bench or sign). Keep the CTA at 2 s or less (W).
- [ ] **Safe zones** (W). Captions and jokes must stay out of the top 120 px, the bottom 380 px and the right 150 px. Run `qa_sheet.py`. It flags bright caption pixels in danger zones; white props (goal nets, paper) can be false positives, so look at the sheet.
- [ ] **Props that carry the joke are big** (R): at least about 250 px. Never hide the joke prop behind another object (the receipt behind the wallet in v3).
- [ ] **Facts true and dated, jokes clearly parody** (U). Real quotes only if published. Show a footer "Real facts · jokes are parody" for at least 1 s at 44 px or more. No jokes about deaths, injuries or families.
- [ ] **Originality**: original characters, no logos or crests, no copied artwork from other creators (inspiration only), synthesized or royalty-free audio.

- [ ] **Every frame is factually true on its own** (R, v4 bug). Animated counters and odometers must never show a wrong intermediate value (e.g. "2022 · KO goals 1"). Tie the state change to the exact event.
- [ ] **Precise wording for real people** (R, fact check). "Retired" means "from national teams" when they still play for clubs. Comebacks nobody reported must be a question ("COMEBACK?"), not a claim.
- [ ] **Sensitivity scan** (R, fact check). Check recent personal events (e.g. a bereavement before an announcement). Soften gags that touch that moment (angry SLAM became a gentle CLICK). Keep real non-star figures (coaches) unnamed.
- [ ] **The hook shows every main character the title promises** (R): "BOTH GOATs" means both on screen in frame 1.

## 2. Craft patterns that worked
- **Cold open with the ending** and a "How?!" question, then a short rewind of 0.3 s or less (R).
- **Zoom-punch + shake + low BOOM** on every punchline. Flash cuts between beats (R).
- **Numbers as gags**: odometer or counter (2006→2026, KO goals 0→1), absurd scale contrast (a giant receipt for €255, a fridge-sized wallet) (R).
- **Easter eggs for rewatch**: a 3-frame "v3.0 DRAFT" paper, boots hidden behind the bench in the cold open (R).
- **Comment bait as a binary choice**: "10 or 7?" beats "comment below" (R).
- **Callback twist** at the end (RETIRED → RETIRED* "*for now") instead of repeating the opening (R).

- **Show, don't tell** (U, 2026-11-13): the story must be understood from images and actions alone. Max about 3 words of on-screen text per scene (scores, dates, one punchline). No screenshots-of-text or long post cards; turn each statement into an action (planting a flag, a dictionary with a picture, swapping the flag back).
- **Voices make it funny** (U): every episode gets crowd cheers/"ooh", laughs, a SIUUU-style shout and meaningless gibberish "cursing" on reactions. All voices are synthesized (espeak-ng + pitch shifts, `toon2/sfx/make_voices.py`), never real recordings or real players' voices.

- **Happy accidents** (U, Ep2): a layering "bug" put Ronaldo's SIUUU burst on Messi's head during his shocked close-up, and it read as a joke. Before "fixing" a visual glitch, ask: is it funny? Keep it if yes. Next time, try deliberate versions (a rival's catchphrase hitting the other player, captions bumping into characters).

## 3. Anti-patterns (things we got wrong)
- Static scene with tiny text (the Messi desk in v2) means swipe-away (R).
- A joke that contradicts the facts ("2030? my knees" after he had already retired) reads as an error, not irony (R).
- Long English captions and small counters in the corner are unreadable on a phone (R).
- Photo-realistic stickers on cartoon bodies: the user rejected them for style. Pure code "hand-drawn likeness" was rejected for low likeness. Use signifier-driven chibi caricatures (U).
- Taking other creators' images is not allowed. Learn principles only (U-agreed).

## 4. Process: one episode
1. **Research**: news in the last 3 months, at least 2 independent sources per fact. Write the fact list with dates.
2. **Beat sheet**: 6–8 beats over 18–22 s, one visual gag per beat, max 6 words each.
3. **Build**: reuse the engine in `goats/scene.html` (characters, props, `soft()` background, punches).
4. **Render a preview sheet**, then run `qa_sheet.py`, then fix.
5. **Review room** (see `REVIEW_ROOM.md`): at least 3 roles, scores logged in `scorecard.csv`.
6. **Fix the top 3 items from each role**, re-render, then send to the user.
7. **Retro**: add new lessons to this file (sections 1–3) with their source.

## Sources (W)
- Hook, loop and CTA length: [prepublish.ai](https://prepublish.ai/guides/youtube-shorts-retention), [virvid.ai: looping](https://virvid.ai/blog/looping-structure-shorts-retention-2026), [shortimize](https://www.shortimize.com/blog/youtube-shorts-retention-rate), [conthunt](https://conthunt.app/blog/youtube-shorts-best-practices). The thresholds in these blogs are unverified.
- Safe zones (vendor estimates, they conflict): [reap.video](https://reap.video/blog/short-form-video-safe-zones), [vidpros](https://vidpros.com/vertical-video-safe-zone/), [adaptlypost](https://adaptlypost.com/blog/social-media-safe-zones-2026-complete-guide).
- Sound-off viewing and captions: [easyviral.ai, 500 Shorts analysis](https://easyviral.ai/api/blog-md/we-analyzed-500-viral-faceless-shorts) (methodology not shown).

## 4b. Performance log
Real numbers go in `performance.csv`. Decide with retention data (average watch time, % watched, 3-second hold), not views alone. A single post with fewer than about 1,000 views is not enough evidence to change the format; run A/B tests instead.

## 5. Fact-check protocol (mandatory, every episode)
1. **Extract claims.** List every factual claim (dates, scores, scorers, minutes, quotes, numbers, who said what) in `facts.md` in the episode folder.
2. **Two independent sources per claim**, preferring primary or reputable outlets: official club/league/UEFA/FIFA pages, ESPN, Reuters/AP, BBC, Sky, Al Jazeera. Fan pages, social reposts and AI summaries do not count.
3. **Quotes.** Mark each quote VERBATIM (exact published wording, with source) or PARAPHRASED (labelled as such on screen).
4. **Precision.** Exact dates, scores and goal types (penalty, header). Rounded or relative time ("a week later") must be checked against the dates.
5. **Status column.** Each claim is VERIFIED, CORRECTED (with what changed versus the lead) or DROPPED (could not verify). Unverified claims never appear on screen.
6. **Independent check.** A fact-checker agent re-verifies `facts.md` against the final frames before release.
7. **Re-check on publish day** for anything that can change (records, retirements, transfers).

## Sound rule (from Ep3 feedback)
- Fewer sounds, each one paying off. At most one gibberish or grumble per video, right after a punchline.
- Every punchline gets a short, clear spoken English line (MBROLA via `toon2/sfx/make_lines.py`), and the bed ducks under speech.
- Keep it to one music bed; no leftover layers from older episodes.
- Visual clarity: zoom the camera (`cam()`) so the face fills the frame. Keep text outside the zoom and away from the top 120 px and bottom 380 px.

## Motion, sound and art standard (from the Ep3 v3 feedback)
- **Motion:** every shot moves.
  - Keyframed camera (`camK`/`camR`): push-ins, whip pans, dutch angles.
  - Anticipation before every action, then squash and stretch, motion trails and an impact flash with shake.
  - At least one slow-motion beat per video.
  - Particles on every hit: sand puffs, stars, sweat, steam, Zzz, fireworks.
- **Sound:** use `toon2/sfx/synth.py`.
  - Each character gets a music theme; the music style changes per scene.
  - Every on-screen action gets a matching sound (kick, net, slurp, boing, tweet, scratch, tick).
  - Voices sit on top: music ducks under speech; reverb and stereo are added.
- **Art:** the rig has two-tone shading, rim light, iris and catchlight eyes, hair and beard texture, folds and trims.
  - Use the expressions `sleep`, `angry` and `smug` for acting, not only `grin`.
- **Story:** a rule-of-three escalation, plus one absurd twist and a character contrast (here: lazy vs restless).

## Clarity and variety standard (from the Ep3 v4 feedback: "too noisy, hard to follow, monotonous")
- **Voices:** 5 short lines at most per video, using SVOX Pico (`toon2/sfx/make_pico.py`), clean with no reverb or distortion. No gibberish.
- **Story:**
  - Tell it in chronological chapters, each with a dated tag (e.g. AUG 2026 → THE PLAN → 2026 SEASON → NOV 2026 → MEANWHILE).
  - Each chapter has one action and one line of text.
  - The hook shows the ending as a question, then rewinds.
- **Cast:** every video uses supporting characters from `toon2/cast.js`: fans, kids, goalkeeper, presenter, tourists, grandpa, animals.
  - Vary body types, skin tones, hair, hats and outfits.
  - Repeated actions get different reactions (dive, face-plant, white flag).
- **Locations:** at least 3 different settings per video (stadium, beach, gym, ...), each with its own palette and music.

## Standing order: the team decides, then builds (user instruction, Nov 13 2026)
For every new video, run this pipeline automatically. Do not stop to ask the user to approve a script.
1. **Pre-production room** (parallel agents): comedy writer, retention strategist, art director, audience panel, fact checker.
   - Input: the researched facts.
   - Output: each role pitches or critiques. The producer merges the best into one optimal script, with a short "why this version" note.
2. **Build** the video to the playbook standards.
3. **Post-production review room** on the rendered frames and the audio timeline.
   - Apply every fix that 2 or more roles agree on, plus any fact error.
   - Re-render, and log the scores in `scorecard.csv`.
4. **Ship:** the video, cover, subtitles, the 4 platform dossiers and the facts sheet.
   - Send the video to the user with a short summary of what the room decided and changed.

## v3 house style (from the Ep4 "terrible" teardown, Nov 14 2026)
- **Characters:** use `toon2/chibi.js`.
  - Big heads (about 40% of height), no neck, seamless limbs.
  - Expressive eyes with lids, blinking and looking around.
  - 12 mouth shapes.
  - Characters face each other; use squash and stretch on every hit.
  - Caricature the real person affectionately, never crudely.
- **Story:**
  - One gag, escalated 3 times, then a topper; 12–16 s that loop.
  - The cartoon must show what a camera can't. Never just re-label the real clip.
- **Text:** 15 words or fewer, and one text layer at a time. No chapter tags, receipts or scrolling banners.
- **Sound:** no TTS by default. Use synthesized grunts, hums and yawns, strong foley, one music bed and a crowd.
  - Use spoken lines only when the joke is the line itself.
- **Facts:** keep them in the caption and in a small footer ("Inspired by … · parody"), not in scenes.
- **CTA:** a small FOLLOW button overlay in the second-to-last beat, instead of a separate end card, so the loop survives.

## Approved template (user approved Ep4 v4 on Nov 14 2026: "keep it up like this")
Use Ep4 v4 (`toon2/ep4/scene.html`) as the starting template for every new episode:

| Time | Beat |
|---|---|
| 0–2 s | The impact hook |
| 2 s | MISSION card plus a "Real match / real fact" line |
| 3–16 s | A 5-heart HUD and 5 different attempts. Each attempt has its own idea and its own reaction from the "boss". |
| ~16 s | Topper, then GAME OVER |
| ~18 s | Twist |
| last 2.5 s | "Thanks for watching ❤️" + FOLLOW + next-episode teaser |

The full v3 house style also applies:
- names under the shirt numbers
- chibi rig
- no TTS
- about 35 on-screen words, with one main line at a time

Talk to the user in Vietnamese; all video and post deliverables stay in English.

## Comment bait standard (user feedback Nov 14 2026: "nobody comments")
Every video carries at least 2 of these 4 hooks.
1. **Numbered vote on the end card.** For example, "Best attempt? Comment 1–5 👇" with icons. A number is the easiest comment to leave.
2. **Hidden easter egg.** For example, 3 hidden 🐐 in the background. The end card asks "Spot the hidden 🐐? 👀", which also drives rewatches.
3. **Pick a side.** For example, "Team 10 or Team 7?" or "Who wins: X or Y?".
4. **Viewers choose the next episode.** For example, "What should attempt 6 be?". Then actually use a viewer's idea and credit them in the pinned comment.

On YouTube, TikTok and Instagram, the caption's first line is the hook plus a question. The pinned comment asks a different question from the caption. Reply to every comment in the first hour, since replies count as comments too.

**Facebook:** never write "comment YES / tag a friend if…". Meta demotes engagement bait. Ask genuine questions instead.

## STORY FIRST, no fixed format (user feedback Nov 14 2026: "make it gripping by following the story; don't fix the 5-hearts format")
This section **replaces** the "Approved template (Ep4 v4)" as a rule. That template is now one option among many.
- Every episode's structure follows the **real story's own arc**: setup, then the incident, then escalation, then the real outcome, then the real aftermath or twist (quotes, club posts). Use the real moments and real lines (as speech bubbles), exaggerated visually.
- Pick the format that fits the story. Never use the same format two episodes in a row. Options:
  - a mini-movie (spy, heist, horror or romance parody)
  - a nature documentary
  - sports-commentary chaos
  - a "how it started / how it's going" piece
  - a courtroom scene
  - a game level (only when it truly fits)
- Keep these from the house style: chibi rig, a strong 0–2 s hook, names on shirts, ≤35 words, no TTS, comment bait, and the thanks + follow end card.

## X (Twitter) is the 5th platform (user instruction, Nov 14 2026)
Every release ships `X.md` next to the other 4 dossiers.

**Main post:**
- Native video upload, never a link.
- A hook line, then 3–5 short lines that tell the story, then one question.
- 280 characters or fewer, with at most 2 hashtags.

**Thread under the main post:**
- **Reply 1:** the real facts and date, plus the parody label.
- **Reply 2:** an engagement question or the easter egg (for example, the hidden 🐐).

**Rules:**
- Do not @ players or clubs.
- Quote-post the video after 24 h with a fresh angle.

## Rejected formats log
- **Ep6 "Worst Disguise in Miami"** (guess-the-player, with shirt layers peeling off as clues) was **rejected** by the user on Nov 14 2026: "not good, drop it". Do not reuse this concept.

## Emphasis standard (Ep7 v3 feedback, Nov 14 2026)
- **Every "point" or win gets a beat:** drumroll, then a slam banner, a colour flash, confetti, a punch-in, and a running tally on screen.
- **Characters always act:** the winner does a signature celebration, the loser gives a big reaction, and the idle character keeps moving. No standing still.
- **Audio hits on every key moment:** airhorn/crash + crowd roar for wins, wah-wah for losses, a driving beat under the whole video.
- **Pacing:** give each beat 5+ s; a 40–45 s total is fine when every section pays off.

## Lean review mode (user choice, Nov 14 2026, to save usage)
This section replaces the multi-agent rooms above where they conflict.
- **Pre-production:** the producer drafts the script alone. At most **1 combined agent** (writer + researcher) is used, and only if the topic needs fresh research.
- **Post-production:** **1 combined reviewer agent** (comedy + art + audience + fact check) runs on a contact sheet.
- **At most 1 fix round** after the review. Then ship. No second review unless the user asks.
- Keep check renders small: a few key frames, not full renders, until the final export.

## Goal-scene standard (Ep9 v2 feedback, Nov 14 2026)
- **Each goal gets its own shot design.** Never repeat the same wide shot. Options: a split-screen stare-down, slow motion with a freeze-frame impact, a whip pan, a tracking shot, a view from inside the net, a tilt up to the sky for crosses and corners, a low-angle leap.
- **Each goal gets a big celebration beat** (SIUUU-style or signature), escalating across the video: solo → bigger with a shockwave → team chorus → giant whole-team. Label celebrations that did not happen as parody in the facts sheet.
- **Names under the shirt numbers** for every real player, auto-fitted to the shirt (`nm()` helper in `ep9/scene.html`). Show numbers only when a lineup source confirms them; otherwise show the name only.

## YouTube upload settings (standard for every episode, Nov 14 2026)
- **Category:** Comedy (Hài kịch). The channel is cartoon parody, so not Sports. Keep it the same on every video for consistency.
- **License:** Standard YouTube License (Giấy phép chuẩn). Never Creative Commons, which would let others re-upload the videos.
- **Allow embedding:** on.
- **Audience:** not made for kids. **AI / altered content:** No.

## Social copy (user instruction, Nov 14 2026)
Before writing the 5 platform dossiers, read `studio/SOCIAL_COPY.md` and run its pre-ship checklist. In chat, give the user the ready-to-paste text for all 5 platforms, including the YouTube **tags**.

## Likeness (user feedback Nov 15 2026: "videos not well received, mainly because the players don't look like the real ones")
**Research (caricature basics):** people recognise a face by the traits that differ from average. So:
1. Write a checklist of each player's 2–3 most distinctive traits (hair shape, jaw/chin, brows, beard, skin, build, one accessory or tattoo).
2. Exaggerate those traits and keep everything else plain. Exaggerating too many traits turns it into a generic cartoon.
3. Start from simple shapes, and check the silhouette (hair + head + build).

Sources: [Proko: Caricature 101](https://www.proko.com/course-lesson/caricature-101-how-to-exaggerate), [Proko: exaggeration checklist](https://proko.com/course-lesson/solving-the-exaggeration-with-a-checklist/notes), [Adobe: how to draw a caricature](https://www.adobe.com/in/creativecloud/illustration/discover/how-to-draw-caricature.html).

**Rig v2 (`chibi.js`):**
- New head params (all optional, backward compatible): `faceW`, `faceH`, `chin`, `chinPoint`, `cheekbones`, `eyeSize`, `eyeGap`, `eyeShape` ('almond'|'round'), `lidBase`, `browArch`, `browLen`, `earSize`, `earring`, `quiff`.
- New hair styles: `fade`, `buzz`, `swept`, `styled`, `sidepart`. New beard style: `beard: 'trim'`.
- New arm tattoo: `C.tattoo = {arm, col}`.
- Per-player specs live in `window.LIKE` in `chibi_cast.js`. Comparison sheet: `toon2/likeness_sheet.html` → `toon2/likeness_v2_sheet.jpg`.

**Known limit:** likeness from code-drawn shapes tops out around 6/10 (noted earlier). Strong signifiers still carry recognition: name and number, kit, the hook text naming the player, and signature moves (SIUUU, pointing to the sky).

### Likeness method v3: the photo-reference loop (Nov 15 2026; use it for every new player)
1. **Get 1–2 reference photos** from Wikimedia Commons (CC-licensed), for study only:
   - Download: `curl -sSL -A "<descriptive UA>" -o x.jpg "https://commons.wikimedia.org/wiki/Special:FilePath/<File_name.jpg>?width=600"`.
   - Find file names with the Commons search API (`list=search`, `srnamespace=6`). It rate-limits, so wait 4–6 s between calls and send a descriptive User-Agent. en.wikipedia.org is blocked in this environment; commons.wikimedia.org works.
   - Keep the photos in the scratchpad only. **Never ship, trace or commit them.**
2. **Write the trait checklist** from the photo (proportions, not details): face length/width, jaw and chin, hairline height, hair volume and direction, brow thickness/angle/height, eye depth, nose length, beard coverage and colour, skin tone.
3. **Build the spec in `LIKE`**, render a side-by-side (photo row on top, cartoon row below), compare, fix the biggest mismatch, repeat 2–3 times.
4. **Lessons from round 1:**
   - The chibi default (round face, big round eyes, tall hair) is what kills likeness.
   - Ronaldo needed a long narrow face, LOW tight hair with a high forehead, low straight brows and a long nose. A tall quiff was wrong.
   - Messi needed hair swept back off the forehead (not a bowl) plus a big ginger-brown beard.
   - Brow angle sets the mood: inner ends raised = sad, a strong V = cartoon-angry. A slight inward dip (`browBase` about −0.15) reads "intense".
5. New rig params from this round: `browY`, `browBase`, `noseLen`, `deepEyes`, and hair styles `cr7` and `long`.

### Portrait mode (Nov 15 2026): a higher likeness ceiling for close-ups
- The user's verdict on chibi v3 was "still not similar; can't you do better?". The chibi style itself caps likeness.
- **`toon2/portrait.js`** draws semi-realistic caricature heads from measured landmarks of a reference photo (hairline, brows, eyes, nose, mouth, chin, jaw corners and ears, on a 600x620 grid), with planes/shading, tapered brows, almond eyes with creases, nose bridge + nostrils, lips and folds. Caricature = stretch the chin/jaw ~15%.
- Done: `ronaldo` (mouth: open/smile/flat), `messi`. Sheet: `toon2/portrait_v1_sheet.jpg`.
- **Use it for:** the hook frame, reaction close-ups, the end card and the cover (where likeness matters most). Keep chibi bodies for action and wide shots.
- **To add a player:**
  1. Get a reference photo.
  2. Overlay a 50 px grid with PIL and read off the landmark coordinates.
  3. Write a new face function.
  4. Compare side by side, and iterate 2–3 times.
- **Mistakes to avoid:**
  - Big soft blotches read as bruises; keep the shading subtle.
  - Thin brows and small eyes lose the intensity.
  - The neck must be as wide as the jaw for athletes.
