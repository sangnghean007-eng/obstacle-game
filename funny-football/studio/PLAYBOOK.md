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
