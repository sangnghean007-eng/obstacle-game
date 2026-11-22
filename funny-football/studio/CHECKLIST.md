# MANDATORY SELF-CHECK — run on EVERY episode before sending (owner, 22 Nov 2026: "Ghi nhớ và áp dụng chứ không phải cứ nhắc mới làm")
Every item below came from an owner complaint. They are applied by default, never waited for. If one fails → fix it, then send (Rule 0b).

## Story & comedy ("nhạt nhẽo", "hời hợt", "đơn điệu")
- [ ] One-line story, hook on frame 0, clear rule the viewer learns in 2 s.
- [ ] ESCALATION: every beat bigger than the last; no two beats with the same gag/reaction/framing.
- [ ] Each victim reacts differently and physically (spin, swell, jelly, launch, handprint, flying tooth…) — never just a head tilt.
- [ ] Impact has weight: squash, shake, flash, sound, after-effect that stays on screen.
- [ ] Twist from a TRUE fact + a button ending. Owner's story ideas are followed exactly.
## Staging (owner, 22 Nov 2026: "Nên để hình ảnh tất cả các cầu thủ chung khung hình chứ đừng đơn lẻ" · "Ghi nhớ")
- [ ] SAME FRAME: group stories keep everyone on screen together (line-up, walk along the line); victims stay visible with their after-effects so the damage piles up. No one-person-per-shot cutting.
- [ ] EVERY real person on screen looks like the real person (caricature head). Generic only if the identity can't be verified — then say so, never leave it silently.
- [ ] Bystanders REACT all the time: those waiting tremble/sweat/fear (the next one most), others laugh at the current victim; after being hit they laugh at the next one (owner, 22 Nov 2026).
- [ ] Props/graphics vary: no two score boards/cards/stamps in the same style in one episode (LED, TV bug, chalk, neon, paper, stone…).
- [ ] Camera tracks / pulls back instead of cutting between isolated two-shots; close-ups only as short punch-ins.
## Look ("vẽ cho giống", "kỳ", "hài phóng đại")
- [ ] Real people = AI caricature heads (cast/*/caric) — exaggerated, funny, recognisable; generic only when the person can't be verified with 2 sources.
- [ ] Head sits in the collar; limbs use the face's skin colour; body style matches the head.
- [ ] Every hand has fingers; boots are boots; joints never break.
- [ ] SHORT TEXT (owner, 22 Nov 2026: "Câu chữ ngắn gọn rõ ràng hơn"): every on-screen line ≤ 4–5 words, big font, one idea per card; cut every word the picture already says.
- [ ] Names printed on shirts, readable on a phone; no text over faces; nothing mirrored (numbers).
- [ ] Contacts really touch (catch, slap, hug) — arm IK, step in if out of reach.
- [ ] Nobody frozen: breathing, sway, hops, laughing crowd.
- [ ] Frame sheet every 0.5 s + full-res close-ups of every key moment checked; faces/text outside the app UI zones.
## Facts (Rule 0)
- [ ] Every real fact on screen in facts.md with ≥2 sources from the last 30 days.
- [ ] CODE LIKENESS ("Vẽ bằng code cho giống"): when no AI face is available, every real player gets a LIKE2 spec (cast/*_likeness.js) — hair type + colour first (bun, twists, sidepart, swept, fade+quiff…), beard/stubble, skin, face shape, eye colour; check against a free Commons photo when reachable; render a likeness sheet and fix before use; never hide the main cue (hair) under a hat in the key shots.
## Sound ("Âm thanh cứ lặp đi lặp lại qua các video" — 22 Nov 2026)
- [ ] NO REUSED SOUND LIBRARY. Every episode gets its own palette in ep<N>/snd/, made for that story (ElevenLabs, free credits):
      music bed (node 'music', eleven_music_v2_5, ~900 cr, transcribe-check NOT needed: prompt "No vocals" + check by envelope),
      4–6 key SFX described for THIS gag (node 'sfx', eleven_text_to_sound_v3, 50 cr each),
      1–3 short character lines (creative_generate_speech eleven_v4, ~40 cr each, premade/library voices, never cloned; vary voices per episode).
- [ ] fx2.py synth only for small fills (springs, whooshes); never as the main hit sounds. No shared channel sting at the end — end on the episode's own music button.
- [ ] PACE ("diễn biến hơi nhanh", "đọc Ronaldo bị chậm"): each beat ≥1.5 s + a reaction pause; a voice line STARTS within 0.1 s of its caption popping and the caption stays until the line ends; lines never overlap (check the vox stem envelope). Shorts may run up to 30 s — use the time.
- [ ] CATCHPHRASES ("Siuuu cho rõ"): a signature shout (SIUUU, etc.) is its own take, spelled phonetically long ("Ssssiiiiuuuuuu!"), never tacked onto another line; check the S onset (hi-freq ratio) + long vowel, show it on screen too, and hold the matching pose for the whole shout.
- [ ] Voices 5+ dB over music in their windows (check release/stems RMS), music ducked under lines; place music breaks on the big hit.
- [ ] Hits synced to frames, qa.py PASS, export release/<name>-sound.mp3. Out of credits → new fx2 parameters + a genre not used in 6 episodes, and say so.
## Posts ("hời hợt tag", "lung tung", "bỏ tiếng ả rập")
- [ ] YouTube title (3 hashtags incl. #shorts) + description + Tags field + upload settings; TikTok; Instagram (+alt text); X ≤280; Facebook in short clean lines. English only. No Arabic. No "AI" mentions in captions (owner) — just "Cartoon parody".
## Working mode
- [ ] Don't ask about defects or environment/connector changes — do them (Rule 0b, 0c). Ask only about taste.
