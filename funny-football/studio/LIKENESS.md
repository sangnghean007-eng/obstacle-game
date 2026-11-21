# LIKENESS — recognition profiles + AI character sheets (overhaul 6-, started 21 Nov 2026)
Rule: exaggerate REAL traits only. A character is cleared for use when: profile written · sheet made · "cover the name" test passed · score ≥ 8/10.
Sheets: ElevenLabs gpt-image-2.5-sunburst turnaround (3 views + 6 expressions), ~190 credits each; cut into toon2/cast/<name>/{front,threequarter,side,smug,shock,angry,laugh,deadpan,cry}.png; loaded with toon2/castimg.js.

| Character | Traits (in order of importance) | Kit (date-correct) | Sheet | Score | Status |
|---|---|---|---|---|---|
| Kylian Mbappé | shaved head, wide toothy grin, round cheeks, thin moustache, crossed-arms pose | Real Madrid white #10 | toon2/cast/mbappe/sheet.png | 8.5/10 (name-covered: yes) | ✅ cleared 21 Nov |
| Lamine Yamal | tight dark curls with faded sides, youthful face, big grin, slim | Barcelona claret/blue #10 | toon2/cast/yamal/sheet.png | 9/10 (name-covered: yes — curls + ears + grin) | ✅ cleared 21 Nov |
| Cristiano Ronaldo | sharp jaw, styled quiff, perfect grin, raised brows, abs | Al Nassr yellow #7 / Portugal retired 5 Nov 2026 | toon2/cast/ronaldo/sheet.png | 9/10 (name-covered: yes — quiff + jaw + teeth) | ✅ cleared 21 Nov |
| Lionel Messi | full reddish beard, swept-back hair, short, calm eyes | Inter Miami pink #10 | — | code portrait ~7/10 | ⏳ |
| Erling Haaland | long blond hair in a bun, huge frame, square jaw | Man City / Norway #9 | — | code portrait ~6/10 | ⏳ |
| Jorge Jesus | long silver hair swept back, tanned lined face | Portugal coach tracksuit | — | code portrait ~6/10 | ⏳ |
Credits used so far: 570 of the 2,000 free-credit budget.

## Limits found (21 Nov 2026)
- ElevenLabs free plan also has a **daily image cap** (429 `free_tier_image_limit_reached` after 3 sheets in one day). Messi, Haaland, Jesus queued for 22 Nov (one-shot reminder in this session).
- Cutting: `python3 toon2/cast/cut_sheet.py toon2/cast/<name>/sheet.png` finds the 9 figures automatically (DIL=2 default; raise to 4 if curly hair splits into bits).
- Rendering: cast PNGs are file:// images, so Chromium must run with `--allow-file-access-from-files` (range_render.js does) or the canvas is tainted and style post-processing fails.
- Use in a scene: `<script src="../castimg.js">`, `CASTIMG.preload([...])`, then `headFn: CASTIMG.head(ctx, name, expr, codePortraitFallback)`. Ep32 v2 is the first episode on AI heads.
