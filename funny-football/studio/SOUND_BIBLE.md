# Sound bible (user, Nov 17 2026: "the audio keeps repeating, not OK")
Problem: Ep9–Ep15 reused the same 12 voice WAVs (wail, chuckle, laugh_crowd, siu…) 4–20 times per episode and the same beat()/fight() loops.

## Rules (every episode from Ep16)
1. **No stock WAV voices.** `m.wav(...)` is banned in new episodes. Voices come from `toon2/sfx/vox2.py`: formant-synthesized, per-character profile (pitch, head size, breath, vibrato, rasp), re-seeded per episode → every laugh/cry is a new waveform.
2. **Each character has their own voice** (`PROFILES` in vox2.py). Victim vocals vary by beat: oof → yelp → wail → sob → whimper → blubber (escalate, never the same cry twice in an episode). Laughs vary: snicker, giggle, point, belly, cackle.
3. **Impacts are re-synthesized per hit** (`fx2.Mix2`: smack, thump, clang, boom, whip, squeak, spring, cork, honk, zip). Don't stack the old bonk+ding on every hit.
4. **New music style each episode; never reuse a style within 3 episodes.** Log it below. Use the setting as the instrument palette (Paris = waltz/accordion feel, Madrid = flamenco strum, heist = pizzicato…).
5. **One signature sound per episode** (the thing people remember): e.g. Ep16 shutter + bowling xylophone, Ep17 cannon BOOM + rain + kazoo sting.
6. Crowds via `m.crowd(t, kind)`: new random mix each call.

## Log
| Ep | Music | Signature | Voices |
|---|---|---|---|
| 9–15 | beat()/fight() hip-hop/fight loops (overused) | bonk+ding | stock WAVs (retired) |
| 16 Team Photo | sneaky pizzicato heist → oompah tuba + timpani roll | camera shutter, bowling xylophone run | ronaldo, kane, messi, haaland, mbappe, yamal (vox2) |
| 17 Grass Is Greener | Paris waltz vs Madrid flamenco (split screen) | ARSENAL cannon BOOM, pretzel whip, door SLAM, rain + kazoo | mbappe, kane, generic crowd (vox2) |
| 18 The Miracle | stadium drums + original brass fanfare (no real anthem) | dressing-room hum swell + power-up, noodle boings, moon slide whistle | crowd + generic voices (vox2) |
| 19 We Don't Need Him | original fado-style guitar (Portugal) vs oompah tuba (sofa) | poster rip, bulldozer rumble, popcorn burst, TV crack, card whistles | bruno, hojlund, ronaldo, crowd (vox2) |
| 20 Wrong Number | 8-bit chiptune brawl | phone rings, bus horns, record scratch, fight-cloud smack storm, SPLAT | ronaldo, messi, bruno, crowd (vox2) |
| 21 Mbappé This Season | bright ukulele-style strum → cut → tremolo strings | phone buzz, record scratch, trembling squeaks, wah-wah | mbappe, crowd (vox2) |
| 22 So Close | lounge jazz (walking bass, brushes, vibes) at the gala | tape rewind, lucky-bounce boing/ting/bonk, record scratch at the reveal, stiff claps, glass crack | mbappe, kane, crowd (vox2) |
| 23 Dream Duo | trap beat glue + per-location room tone (phone video feel) | chickens, domino clacks, header pings, ball POP, net rip, thunder | ronaldo, messi, kids, crowd (vox2) |
| 25 New Gen vs OG | original synthwave trailer → choir + epic brass for the OGs → tiptoe pizzicato | bass drop, scooter skid, car THUD, record scratch on the bump | yamal, mbappe, haaland, ronaldo, messi (vox2) |
