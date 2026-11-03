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

| Part | Look | Color |
|---|---|---|
| Head (shell) | Rounded, helmet-like, slightly wider than tall | White `#FFFFFF` |
| Screen face | Rounded rectangle filling most of the front | Navy `#003976` |
| Eyes | Two vertical ovals; the expression lives here and in the mouth | Sky `#2C8ECD` |
| Mouth | A small curve or shape | Gold `#EFAB00` |
| Ear pods | One rounded pod on each side | Sky `#2C8ECD` |
| Antenna | Short white stem with a triangle tip (echoes the ATR mark's roof) | White stem, gold `#EFAB00` tip |
| Hands | Small white gloves with sky cuffs, floating beside the head | White, sky cuffs |
| Outline | Thick, even, always navy; 5-8% of the head width | Navy `#003976` |
| Full body (optional) | Navy suit, white limbs and boots | Navy, white |

- **Two forms.** The **head form** (floating head and hands) is the default: emoji, stickers, avatars, chat, small
  art. The **full body** is for full-figure scenes only: event signs, K-12 material, illustrations where Teo
  stands or points at something.
- **Expressions** change only the screen face (and add hands, a "z" or confetti). The shell, ear pods, antenna and
  colors never change. Nine are ready: happy, thinking, surprised, sorry, determined, laughing, confused, sleeping,
  excited.
- **Both themes.** Teo always keeps its navy outline so the white shell survives light backgrounds.

## 3. Where Teo may appear

| Yes | No |
|---|---|
| The Discord server and Slack: avatar, emoji, stickers, banners, bot replies | Letterhead, business cards, certificates, name badges, press releases, grant documents, the website header |
| K-12 programs, camps, workshops and their handouts, slides and signs | Inside, on top of or instead of the ATR mark, a lockup or the roundel; merged with the Kent State wordmark |
| Event signage, demo-day fun, lab stickers (UCM approval still applies to printed merch) | As a photo of a real lab robot, or next to real results as if it were evidence |
| Help and how-to material, error and empty states in lab tools | With text, numbers or logos on its screen face |
| GitHub README headers for Teo itself (a gold ring on the lab header) | Recolored, restyled (3D, realistic, anime), stretched or redrawn by hand |

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

New poses come from the same generator with the same style lock and references, so they match the sheet:

```bash
python3 scripts/atr_design.py doctor --group ai-images        # Codex CLI installed and logged in
STYLE="$(python3 -c "import json;print(json.load(open('assets/mascot/prompts.json'))['style_lock'])")"
scripts/codex_image.sh /tmp/teo-new.png "Emoji of Teo. $STYLE The character fills about 85 percent of the frame and stays readable at 32 pixels. Pose: <describe the pose>." \
  assets/mascot/teo-avatar.png assets/mascot/references/ref-turnaround-head.png
python3 scripts/icons/chroma_key.py /tmp/teo-new.png /tmp/teo-new-keyed.png --keep-color --outline 003976
```

- Use `references/ref-turnaround-body.png` instead for full-body poses.
- Describe the pose and expression only; never ask for text, logos or real robots.
- Keying: `--outline 003976` for emoji and art, `--die-cut` for stickers. Export 512 px masters, 256 px emoji and
  320 px stickers (under 512 KB).
- Check against the character sheet side by side: same proportions, same five colors, navy outline, no text.
  Discard and regenerate anything that drifts (extra limbs, new colors, a mouth on the shell, letters).
- Record the prompt in your project's manifest (not in the skill), and keep generated poses out of the skill unless
  the lab adopts them.

## 6. Files

See `assets/mascot/README.md` for every file and size. Upload-ready sets: `assets/mascot/emoji/` (Discord and
Slack emoji) and `assets/mascot/stickers/` (Discord stickers); platform specs are in
references/community-platforms.md §2.
