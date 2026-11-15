# Likeness pipeline: every real player must look like the real player

User rule (Nov 15 2026): "make sure everyone from now on also looks alike".
**No real player appears in a video until they pass this gate.**

## Two layers
| Layer | File | Used for |
|---|---|---|
| **Portrait** (semi-realistic caricature, measured) | `toon2/portrait.js` | hook frame, reaction cut-ins, big screen, cover, end card (wherever recognition matters) |
| **Chibi body** (tuned with `LIKE` specs) | `toon2/chibi.js` + `chibi_cast.js` | action and wide shots; it must match the portrait's hair colour/shape, skin tone, beard, and name and number on the shirt |

## Steps (about 20–30 min per player)
1. **Reference:** `./fetch_ref.sh "<player name>"`, pick a frontal or 3/4 face, then `./fetch_ref.sh --get "<File>.jpg" <scratchpad>/ref`.
   - Prefer recent photos (the same look as the current season).
   - Photos stay in the scratchpad: never commit, ship or trace them.
2. **Grid:** `python3 grid.py <photo> <scratchpad>/ref/<id> L T R B`, so the face fills the 600x620 box (chin at about 450–560).
3. **Trait checklist:** write the 3 most distinctive traits first, e.g. "Ronaldo: long narrow face + low tight hair + low thick brows".
4. **Measure and spec:** read the landmarks off the grid and write a spec in `portrait.js` (copy `HOJ` and use the `generic` engine):
   - `face` outline, `earL`/`earR`, `hair` (+ `hairSharp` for spiky hair), `browL`/`browR` (6 points, inner end lower = intense)
   - `eyeL`/`eyeR` `[x, y, w, h]`, `nose` (bridge, tip, nostrils, wings), `mouth` `{x, y, w}`, colours
   - optional: beard (see the PLAYBOOK beard rules), freckles, `jawLines`
   - register it in `FACES`
5. **Caricature:** stretch the 1–2 strongest traits by 10–30% (a jaw, a chin, a hairline). Too many exaggerations = a generic cartoon.
6. **Overlay check:** `node overlay.js <name> <scratchpad>/ov.png`, then `python3 overlay_sheet.py <crop.jpg> <ov.png> <sheet.jpg>`. Look at the 55% overlay. Fix the biggest mismatch (eyes, brows, jaw, hairline, mouth) and repeat **at least 3 rounds**.
7. **Expressions:** check `siuuu`, `shock`, `smug`, `angry` (and `deadpan`) still read as the same person.
8. **Chibi match:** add a `LIKE` entry so the chibi body uses the same hair, skin and beard.
9. **Gate:** log the player below as PASS only when the overlay matches at eyes/brows/jaw/hairline and a fresh viewer can name him from the portrait alone (ask the reviewer agent or the user).

## Common mistakes (learned so far)
- **Chibi defaults kill likeness:** a round face, big round eyes and tall hair make everyone look the same.
- **Brows:** thin brows lose intensity. Inner end raised = sad; a hard V = cartoon-angry; a slight inward dip = intense.
- **Hair:** a hair "cap" with a smooth or wavy edge looks like a helmet. Use the real hairline height and an irregular, tufted edge.
- **Beards:** never outline the cheek edge. Feather it, use a gradient, and join the sideburns to the hair.
- **Mouths:** an open-mouth grin drawn too tall looks like shouting; keep a smile shallow.
- **Shading:** big soft blotches read as bruises.

## Players
| Player | Portrait | Chibi LIKE | Reference (Wikimedia Commons, CC) | Status |
|---|---|---|---|---|
| Cristiano Ronaldo | `ronaldo` (custom) | yes | "Cristiano Ronaldo, 2023.jpg"; "Cristiano_Ronaldo_2018.jpg" | PASS (user: "ổn") |
| Lionel Messi | `messi` (custom) | yes | "Lionel_Messi_20180626.jpg" | PASS (beard v2 approved) |
| Rasmus Højlund | `hojlund` (generic) | yes (spiky honey-blond) | "Rasmus Højlund with a fan.jpg" | round 3, awaiting user check |
| Højbjerg, Dias, Félix, B. Silva, D. Costa, Andersen, Veiga | — | rough | none yet | TODO before the next use |
