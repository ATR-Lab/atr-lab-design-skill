# Mascot: Teo

Teo ("teleoperator") is the lab's illustrated mascot and the face of its Discord assistant bot. Usage rules,
anatomy and how to make new poses: `references/mascot.md`. Character sheet: `teo-character-sheet.png`.

| Path | What | Size |
|---|---|---|
| `teo-character-sheet.png` | Views, expressions, colors and rules on one page | 3200 × 2120 |
| `teo-avatar.png` | Profile picture: head on a navy square (crops to a circle) | 1024 × 1024 |
| `teo-profile-banner-1200x480.png` | Discord profile banner (avatar overlaps the bottom-left) | 1200 × 480 |
| `views/teo-{front,three-quarter,side,back}.png` | Head form (default), transparent, navy outline | 512 × 512 |
| `views/teo-body-{front,three-quarter,side,back}.png` | Full body, for full-figure scenes only | 512 × 512 |
| `expressions/teo-<expression>.png` | happy, thinking, surprised, sorry, determined, laughing, confused, sleeping, excited | 512 × 512 |
| `emoji/teo_<pose>.png` | Upload-ready Discord/Slack emoji: wave, think, thumbsup, party, love, sweat, estop, sleep | 256 × 256 |
| `stickers/teo-<name>.png` | Upload-ready die-cut stickers: hello, hmm, nice, party, e-stop | 320 × 320 |
| `references/` | Generation references (turnarounds and expression sheet on chroma green; use with `teo-avatar.png`) | ≤ 1024 px |
| `prompts.json` | The style lock and prompts behind every file | |

All files are illustrations generated with the Codex CLI and finished by hand-written keying scripts; none shows a
real robot. Do not edit these masters; make a new pose instead (`references/mascot.md` §5).
