# Review room charter

Run the room on every version before it goes to the user. Each reviewer is a separate agent that gets `brief_vN.md` (facts + timeline) and
`frames_vN.jpg` (about 22 frames in time order) plus the QA sheet. Each reviewer returns scores, its top 3 fixes and 1 "keep".

| Role | Focus | Scores |
|---|---|---|
| Comedy writer + retention strategist | jokes, hook, pacing, loop, comment bait | funny, hook, clarity (sound off), rewatch |
| Art director | recognisability, safe zones, prop size, readability | recognisability, clarity |
| Audience panel: (A) 18-year-old Vietnamese TikTok user, (B) hardcore football fan | swipe moment, what is not understood, factual nitpicks | would-share yes/no |
| Fact checker (active since v4) | every on-screen fact against 2 sources and dates, wording that could mislead, sensitivity | pass/fail per claim |

Rules: reviewers never edit files. The producer (main session) decides: apply anything that 2 or more roles agree on, plus any fact error.
Log scores in `scorecard.csv`. A version ships when hook ≥ 7, clarity ≥ 7, recognisability ≥ 7 and no fact errors, or when the user asks to see it.
