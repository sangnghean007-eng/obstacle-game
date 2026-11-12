# Instagram Reels: upload dossier, "The GOATs Clock Out" (v5, final)

Confidence tags: **[OFFICIAL]** = Meta/Instagram pages · **[REFERENCE]** = third-party (2+ sources) · **[VERIFY]** = confirm in your app.

## A. Pre-upload checklist
| # | Item | Status |
|---|---|---|
| 1 | Video 1080x1920 (9:16), 21 s, MP4 | Pass |
| 2 | Key text outside UI-covered zones (`studio/qa_sheet.py`) | Pass (remaining flags are false positives: goal net, white paper) |
| 3 | Facts verified; parody label in the video | Pass |
| 4 | Original audio, no licensed music | Pass |
| 5 | Cover `cover-9x16.jpg` keeps its text in the centre (the profile grid crops the middle) | Pass |

## B. Steps in the app (Instagram → + → Reel)
1. **Select the video** → Next. Do **not** add trending music: it would cover the original audio (stamps, "ting", "boom" are part of the jokes).
2. **Edit cover**: upload `cover-9x16.jpg`. Check the square grid preview; "SAME YEAR?!" must be fully visible [VERIFY].
3. **Caption** (max 2,200 characters; only about the first 125 show before "more" [REFERENCE]). Put the searched keywords in line 1, because Instagram reads captions to decide who sees a post [REFERENCE]:
```
Messi & Ronaldo both retired from their national teams in 2026… same year?! 🐐🐐

Messi: "Retirement v2.0" (2016 says hi 👋)
Ronaldo: first World Cup knockout goal after 20 years ⚽ then a €255 fine → "keep the change" 💸

Team 10 or Team 7 — who comes back first? 👇

Real 2026 facts · parody cartoon · both still play club football.
#messi #ronaldo #footballmemes #worldcup2026 #football
```
   **Hashtags: max 5 per post**, caption and comments combined. Instagram announced this on Dec 18, 2025, replacing the old limit of 30 [REFERENCE: multiple sources quoting @creators and the Help Centre]. Do not add hashtags in comments.
4. **Tag people / Collaborators**: do not tag the players (it could look like an endorsement). If partnering with a football fan page, invite it as **Collaborator** so the Reel appears on both profiles.
5. **Location**: leave empty.
6. **Topics** (if shown): Sports / Soccer, Comedy [VERIFY].
7. **Trial reel** [REFERENCE]: shows the Reel to non-followers first for about 24 h. Recommendation: **off** for this video; the news is fresh, publish to everyone.
8. **Share to Facebook**: **off**. Post Facebook separately with `FACEBOOK.md` so the copy fits that platform.
9. **AI label** ("AI info"): **off**. Meta requires a label for photorealistic video or realistic audio that was digitally created or altered; its Help page gives cartoon-style video as an example that does not need one [OFFICIAL, VERIFY: the page currently shows a wrong title]. Turn it on if you ever use realistic likeness or voices.
10. **More options / Advanced settings** [VERIFY names]:
    - **Allow remixing / templates**: on.
    - **Allow downloads**: your call; on helps re-sharing but invites un-credited reposts.
    - **Alt text**: `Cartoon parody: Messi and Ronaldo characters retire from their national teams, a €255 fine is paid from a giant wallet, and two goats numbered 10 and 7 headbutt.`
    - **Hide like counts**: off.
    - **Comments**: on; enable Hidden words to filter insults.
11. **Share**.

## C. After publishing
| When | Action |
|---|---|
| 0–60 min | Post and pin a first comment: `Did you spot the RETIREMENT v3.0 draft? 👀 Team 10 or Team 7?` Reply to the first 5–10 comments. Share the Reel to Story with a "10 or 7?" poll sticker. |
| 24 h | Send the studio: Views, Reach, Average watch time, % non-followers, Shares, Saves, Comments [VERIFY metric names in Insights]. |
| 48 h | Studio updates `studio/scorecard.csv` and the PLAYBOOK. |
| New developments | Edit the caption if it is no longer accurate. |

## D. Risks
- **Fan wars / insults to the players**: Hidden words, hide or delete abusive comments.
- **Misinformation reports**: the caption says "both still play club football" and "parody".
- **Un-credited reposts**: the video carries the parody footer; consider turning off downloads.

## E. Sources
[Meta: when an AI label is required](https://www.meta.com/help/artificial-intelligence/1783222608822690/) · [Meta Transparency: Labeling AI content](https://transparency.meta.com/governance/tracking-impact/labeling-ai-content) · [Instagram Reels features](https://about.instagram.com/features/reels/) · 5-hashtag limit: [Later](https://later.com/blog/ultimate-guide-to-using-instagram-hashtags/), [Creator Lane](https://creatorlanehq.com/blog/instagram-5-hashtag-limit-2026), [Presly](https://presly.ai/blog/instagram-hashtag-limit) · Trial reels: [MacRumors](https://www.macrumors.com/2024/12/10/instagram-trial-reels/) · Caption length: [Sendible](https://www.sendible.com/insights/instagram-character-limit), [ClipSpeed](https://www.clipspeed.ai/blog/instagram-reels-captions.html).
