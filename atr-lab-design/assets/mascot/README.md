# Mascot: Teo

Teo ("teleoperator") is the lab's illustrated mascot and the face of its Discord assistant bot. This is **design 2**
(Nov. 2026): a monitor-headed robot with cat-ear fins and camera-lens pods, redrawn from a lab lead's reference art in
the brand palette. Usage rules, anatomy and how to make new poses: `references/mascot.md`. Character sheet:
`teo-character-sheet.png`.

| Path | What | Size |
|---|---|---|
| `teo-character-sheet.png` | Views, expressions, colors and rules on one page | 3200 × 2120 |
| `teo-avatar.png` | Profile picture: the head on a navy square (crops to a circle; reads at 40 px) | 1024 × 1024 |
| `teo-profile-banner-1200x480.png` | Discord profile banner (avatar overlaps the bottom-left), made with `scripts/banner.py` | 1200 × 480 |
| `views/teo-{front,three-quarter,side,back}.png` | Head form (default), transparent | 512 × 512 |
| `views/teo-body-{front,three-quarter,side,back}.png` | Full body with the gimbal neck and lens-barrel body, for full-figure scenes only | 512 × 512 |
| `expressions/teo-<expression>.png` | happy, thinking, surprised, sorry, determined, laughing, confused, sleeping, excited | 512 × 512 |
| `emoji/teo_<pose>.png` | Upload-ready Discord/Slack emoji: wave, think, thumbsup, party, love, sweat, estop, sleep | 256 × 256 |
| `stickers/teo-<name>.png` | Upload-ready die-cut stickers: hello, hmm, nice, party, e-stop | 320 × 320 |
| `references/` | The lead's reference art (`lead-ref-*.png`) and the generated turnarounds and expression sheet used as references for new poses | ≤ 1024 px |
| `rig/teo-{head,ear-left,ear-right,hand-wave,hand-rest}.png` | Puppet-rig parts for animation: each part complete where others would cover it; the head's screen is blank (the face is drawn as vector shapes). Used by `assets/motion/teo-cameo.json` | as generated |
| `prompts.json` | The style lock, generator settings, job ids and post-processing behind every file | |

All files are illustrations (Higgsfield GPT Image 2.5, finished by script); none shows a real robot. Do not edit these
masters; make a new pose instead (`references/mascot.md` §5).
