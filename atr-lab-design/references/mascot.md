# Mascot: Teo

Who Teo is, what it looks like, where it may appear, how it sounds and how to make a new pose that still looks like
Teo. The files are in `assets/mascot/` (character sheet: `assets/mascot/teo-character-sheet.png`).

**Read this when** a piece could use a friendly character (Discord, Slack, K-12 programs, event signs, stickers,
workshop handouts, the lab's bot), when someone asks for "the robot," "the bot" or "the mascot," or before you
generate any new Teo art.

## Contents

1. [Who Teo is](#1-who-teo-is)
2. [Anatomy and colors](#2-anatomy-and-colors)
3. [Where Teo may appear](#3-where-teo-may-appear)
4. [Voice](#4-voice)
5. [Making a new pose](#5-making-a-new-pose)
6. [Files](#6-files)

## 1. Who Teo is

Teo, short for "teleoperator," is an upbeat, curious lab robot who loves robots, code and the people who build
them. It is the face of the lab's Discord assistant bot (repository ATR-Lab/Teo-Discord-Bot) and a friendly
character for informal and educational pieces. Teo is an **illustration**, not one of the lab's real robots, and it
is **not a logo**: the ATR mark, lockups and roundel stay the lab's identity (references/logo-system.md).

## 2. Anatomy and colors

Teo's current look is **design 2** (Nov. 2026): a monitor-headed robot redrawn from a lab lead's reference art
(`assets/mascot/references/lead-ref-*.png`) and mapped onto the brand palette. The first design (a round white head
with an antenna) is retired; don't use it.

| Part | Look | Color |
|---|---|---|
| Head (shell) | A boxy, slightly rounded monitor or camera body, a little wider than tall, with small panel lines and bolts | Off-white `#F4F5F8`, cool gray-blue cel shading |
| Fins | Two pointed cat-ear fins on top, each with a small inner panel | Off-white, sky `#2C8ECD` panels |
| Screen face | A large dark screen filling most of the front, with one soft diagonal reflection | Navy `#003976` deepening to midnight `#00295F` at the edges |
| Face | Drawn on the screen as glowing lines: two round dot eyes and a small cat-like "ω" mouth by default; the expression lives here | Gold `#EFAB00`, tiny orange `#DC7533` blush dashes |
| Lens pods | A cylindrical camera-lens pod on each side of the head | Gray housing, glowing sky `#2C8ECD` lens |
| Hands | Small white gloves with sky cuffs, floating below or beside the head | Off-white, sky cuffs |
| Full body (optional) | A short gimbal neck joint and a compact rounded lens-barrel body with a dark lens on one end | Off-white, sky accents |
| Line art and shading | Crisp dark navy outlines, two-tone anime cel shading, no gradients except the screen | Navy `#003976` |

- **Two forms.** The **head form** (floating head and gloved hands) is the default: emoji, stickers, avatars, chat,
  small art. The **full body** (gimbal neck and lens-barrel body) is for full-figure scenes only: event signs, K-12
  material, hero illustrations.
- **Expressions** change only the face on the screen (and add hands, a "?", a "z", a sweat drop or confetti). The
  shell, fins, lens pods and colors never change. Nine are ready: happy, thinking, surprised, sorry, determined,
  laughing, confused, sleeping, excited.
- **The face is always gold on navy.** The lead's sketches tried green and white faces; the brand version uses Kent
  State gold so Teo reads as the lab's at a glance. Never put words, numbers or logos on the screen.
- **Both themes.** The navy line art keeps the off-white shell visible on light backgrounds; stickers add a white
  die-cut border.

## 3. Where Teo may appear

| Yes | No |
|---|---|
| The Discord server and Slack: avatar, emoji, stickers, banners, bot replies | Letterhead, business cards, certificates, name badges, press releases, grant documents, the website header |
| K-12 programs, camps, workshops and their handouts, slides and signs | Inside, on top of or instead of the ATR mark, a lockup or the roundel; merged with the Kent State wordmark |
| Event signage, demo-day fun, lab stickers (UCM approval still applies to printed merch) | As a photo of a real lab robot, or next to real results as if it were evidence |
| Help and how-to material, error and empty states in lab tools | With words, numbers or logos on its screen, or with a face that isn't gold |
| GitHub README headers for Teo itself (a gold ring on the lab header) | Recolored, restyled (3D, photoreal, a different cartoon style), stretched, redrawn by hand, or mixed with the retired first design |

- Teo appears **with** the lab's identity, never instead of it: a piece with Teo still carries the ATR logo (and
  the Kent State wordmark where references/logo-system.md asks for it) as separate elements.
- One Teo per composition, at a size where its face reads (at least 48 px on screens, 0.75 in in print).
- Formal, academic or sponsor-facing pieces do not use Teo. When in doubt, leave it out.
- Printed merchandise with Teo still needs UCM approval and a licensed vendor when the piece also carries an ATR or
  Kent State mark (references/print-and-merch.md, references/kent-state-compliance.md).

## 4. Voice

When Teo "speaks" (the bot, a speech bubble, a sticker caption in a post): warm, curious, dry-witted in small
doses ("let's find the e-stop on this bug"), help first and jokes second, honest about what it doesn't know, never
flattering, safety first around robots, and Kent State style (no Oxford comma). Teo never speaks for the lab or the
university and never makes commitments (admissions, funding, grades, equipment, building access). The full bot
persona lives in the Teo-Discord-Bot repository (`teo/prompt.md`).

## 5. Making a new pose

New poses come from the same generator, style lock and references, so they match the sheet. The settings and the job
ids of every shipped file are in `assets/mascot/prompts.json`.

**With Higgsfield** (the generator behind design 2): model `gpt_image_2_5`, quality `high`, resolution `2k`,
background `transparent`, aspect `1:1` for a single pose. Upload `assets/mascot/references/ref-turnaround-head.png`
and `lead-ref-stickers.png` as image references (`ref-turnaround-body.png` and `lead-ref-hero.png` for full-body
poses), and write the prompt as: "Emoji of the robot mascot Teo exactly as in the first attached turnaround image
... One single character, head form, filling about 85 percent of a square frame, readable at 32 pixels. Pose: <the
pose>. Transparent background, no text, no letters, no numbers, no logos." A pose costs about 3 credits; check the
cost first (`get_cost`) and the user's go-ahead before a batch.

**Without Higgsfield**, use the Codex CLI on chroma green and key it:

```bash
python3 scripts/atr_design.py doctor --group ai-images        # Codex CLI installed and logged in
STYLE="$(python3 -c "import json;print(json.load(open('assets/mascot/prompts.json'))['style_lock'].replace('transparent background', 'flat chroma green #00FF00 background'))")"
scripts/codex_image.sh /tmp/teo-new.png "Emoji of Teo. $STYLE The character fills about 85 percent of the frame and stays readable at 32 pixels. Pose: <describe the pose>." \
  assets/mascot/references/ref-turnaround-head.png assets/mascot/references/lead-ref-stickers.png
python3 scripts/icons/chroma_key.py /tmp/teo-new.png /tmp/teo-new-keyed.png --keep-color
```

- Describe the pose and expression only; never ask for text, logos or real robots.
- Trim to a square with even padding; export 512 px masters, 256 px emoji (under 256 KB) and 320 px stickers with a
  die-cut border (`chroma_key.py --die-cut`, under 512 KB).
- Check against the character sheet side by side: the boxy head, two cat-ear fins, two lens pods, a gold face on a
  navy screen, crisp navy line art. Discard and regenerate anything that drifts (an antenna, a round head, extra
  limbs, a green or white face, letters, a barcode).
- Record the prompt in your project's manifest (not in the skill), and keep generated poses out of the skill unless
  the lab adopts them.

## 6. Files

See `assets/mascot/README.md` for every file and size. Upload-ready sets: `assets/mascot/emoji/` (Discord and
Slack emoji) and `assets/mascot/stickers/` (Discord stickers); platform specs are in
references/community-platforms.md §2.
