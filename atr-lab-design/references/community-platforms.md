# Community platforms: Discord, Slack and GitHub READMEs

Specs, recipes and hard-won rules for the lab's chat communities and code repositories: the Discord server, Slack
workspaces, bot profiles, custom emoji and stickers, and the README pattern every ATR-Lab repo shares.

**Read this when** you brand or reorganize the lab's Discord server or a Slack workspace, make emoji, stickers,
server icons, banners, invite backgrounds or Server Guide thumbnails, set up or restyle a bot (including Teo, the
lab mascot: references/mascot.md), or give a GitHub repo its header, badges and footer. Website, email, YouTube,
QR codes and the GitHub organization avatar are in references/web-and-digital.md; social media posts are in
references/social-media.md.

Specs were checked in November 2026. Platforms change sizes and boost tiers often; if an upload is refused, read
the platform's current help page before resizing anything.

## Contents

1. [Rules that apply to every platform](#1-rules-that-apply-to-every-platform)
2. [Discord: sizes and limits](#2-discord-sizes-and-limits)
3. [Discord: server structure the lab uses](#3-discord-server-structure-the-lab-uses)
4. [Discord: permissions that trip people up](#4-discord-permissions-that-trip-people-up)
5. [Bots on Discord and Slack](#5-bots-on-discord-and-slack)
6. [Slack](#6-slack)
7. [GitHub repository pages](#7-github-repository-pages)
8. [How to make each asset](#8-how-to-make-each-asset)

## 1. Rules that apply to every platform

- **Both themes.** Chat apps show your art on near-black (Discord dark `#313338`, Slack dark `#1A1D21`) and on
  white. White artwork vanishes on light themes and navy vanishes on dark ones: give white or navy art a contrasting
  outline (`scripts/icons/chroma_key.py --outline 003976` or `--die-cut` for stickers) and preview every asset on
  both grounds before uploading.
- **Read it at display size.** Emoji show at 22 px inline (48 px when sent alone), Server Guide thumbnails at about
  72 px, avatars at 32-40 px. Preview at that size; simplify (one glyph, no text, thick strokes) until it reads.
- **Circles crop.** Server icons, avatars and app icons are cropped to circles: keep the subject inside the central
  80% and nothing important in the corners.
- **Little or no text in tiny art.** Emoji, stickers and icons carry no words; the platform shows the name. A square
  thumbnail carries one short word at most, and only if it stays at least 11 px tall at 72 px (`banner.py` enforces
  this).
- **Logos keep their rules.** The ATR mark, lockups and the Kent State wordmark follow references/logo-system.md on
  every platform (no recoloring, no merging, minimum sizes). The mascot is not a logo; see references/mascot.md.
- **Colors.** Embeds, role colors and accents come from `assets/tokens/colors.json`. Check text-carrying colors on
  both themes with `python3 scripts/contrast.py <hex> 313338` and `python3 scripts/contrast.py <hex> ffffff`.

## 2. Discord: sizes and limits

| Asset | Size and format | Limits and notes |
|---|---|---|
| Server icon | 512 × 512 PNG/JPG (min 128); animated GIF needs boost level 1 | Cropped to a circle. Use `assets/logos/icons/atr-avatar-mark-navy.png` |
| Server banner | 960 × 540 (16:9) | Boost level 2. Shows above the channel list; keep text out of the bottom third |
| Invite background (splash) | 1920 × 1080 (16:9) | Boost level 1. **The invite card covers the center**: brand at the edges, nothing important in the middle (`banner.py --preset discord-invite-splash`) |
| Server Guide banner | 16:9 | Boost level 2 |
| Server Guide to-do and resource thumbnails | 1:1, at least 72 × 72, PNG or JPG (make 512 × 512) | One glyph on navy plus a slim hazard strip; must read at 72 px (`banner.py --preset thumbnail-square`) |
| Custom emoji | 128 × 128 PNG (GIF for animated), under 256 KB | Slots: 50 at level 0, 100 at 1, 150 at 2, 250 at 3. Names lowercase with underscores: `atr_*` brand, `teo_*` mascot |
| Stickers | 320 × 320 PNG or APNG, under 512 KB | Slots: 5 at level 0, 15 at 1, 30 at 2, 60 at 3. Die-cut look: white border plus navy outline. Each needs a related Unicode emoji tag |
| Role icons | 64 × 64 PNG, under 256 KB | Boost level 2 |
| Soundboard sounds | MP3 or OGG, up to 5.2 s, under 512 KB | Only sounds the lab made or that are CC0; never songs, film clips or Kent State athletics audio |
| Bot or user avatar | 1024 × 1024 PNG | Circle crop |
| Profile banner | 5:2, for example 1200 × 480 | The avatar overlaps the bottom-left: keep that corner calm (`banner.py --preset profile-banner`) |
| Embed accent color | `#003976` (navy) by default; `#EFAB00` (gold) for highlights such as contact cards | Embed images: 16:9 or 5:2 banners at 1600 px wide read well |

## 3. Discord: server structure the lab uses

The lab's server (Oct. 2026 revamp) is the reference design. Reuse it for any lab or program server.

**Categories** (emoji prefix and a space, sentence case): 📌 Start here · 📣 Lab news · 💬 Community · 🔬 Core lab ·
🤖 Research projects · 🎓 Classroom · 🛠️ Admin · 🗄️ Archive (always last).

**Public channels** use an emoji, a middle dot and a lowercase slug: `📜・rules`, `👋・welcome`,
`📇・contact-info`, `❓・how-to-get-help`, `🎫・tickets-and-support`, `📣・announcements`, `🚀・opportunities`,
`🙋・introductions`, `💬・general`, `❓・help-desk` (a forum). Project, class and staff channels keep plain slugs
(`2026-mini-turtlebot`). Voice rooms: `🔊 General voice`, `🔊 Meeting room`.

**Topics** on every text channel: one plain sentence in Kent State style, no Oxford comma.

**Archive, don't delete.** Inactive or finished channels move to 🗄️ Archive with their permissions unchanged and
a topic that starts "Archived Mon. D, YYYY." Log every change with before and after values so it can be rolled back.

**Pinned cards** (embeds, navy sidebar): a welcome card with a 1600 × 640 banner, the steps to get started and the
lab's links; a contact card (gold sidebar) with website, email, socials, mailing address and the department phone
labeled as the department's; a rules card. Copy only verified facts (references/brand-foundation.md §11).

**Rules.** Twelve short rules adapted from the lab's code of conduct: respect, safe for work, on topic, first-name
nickname, privacy (never name or post minors), adults never DM minors one-on-one (Kent State Policy 5-19), never post
secrets, share code and results responsibly, honesty about demos, speak for yourself, lab safety still applies,
Discord's rules. End with "Report a concern" (911, tickets, Dean of Students, Title IX, counseling) and keep the
membership-screening rules list identical to the posted rules.

**Onboarding and Server Guide.** The rules question grants the Verified role; interest roles use `atr_*` emoji.
Server Guide to-dos: read the rules, introduce yourself, catch up on lab news, say hi in general. Resource pages:
how to get help, opportunities, contact the lab, get support. Bots cannot edit the Server Guide; a person pastes it.

**AutoMod.** Block posted secrets with regex (API keys such as `sk-ant-`, `AKIA`, `ghp_`, private key headers,
Discord tokens) and alert a `🛡️・mod-log` channel; block the slurs and sexual-content keyword presets; mention-spam
limit about 8.

## 4. Discord: permissions that trip people up

- **Server Guide channels must be visible to @everyone**, and **resource pages must be read-only for @everyone**.
  A to-do that completes "when a member sends a message" also needs @everyone to be able to post there. Membership
  screening still blocks posting until someone accepts the rules, so opening a channel to @everyone does not open
  the gate.
- **Resource pages accept text channels only**, never forums. Point a "How to get help" resource at a read-only
  text channel whose pinned card links the forum.
- **Discord's editor hides the saved channel** when you reopen a resource page (the picker leaves out channels
  already in use). Saving from that dialog can unlink it; to change a resource's channel, delete and re-add it.
- **Welcome-screen channels must be readable by @everyone.**
- **Bots see what their roles see.** When a bot loses a temporary Admin role, give its own role explicit view,
  send, read-history, reactions and send-in-threads overwrites on every category it serves.
- **Role colors** need about 3:1 against both `#313338` and `#FFFFFF`; the lab's set: Professor gold `#EFAB00`,
  Researcher sky `#2C8ECD`, staff `#629AE4`, interest roles from the chart palette.

## 5. Bots on Discord and Slack

- **Identity.** The lab's bot is Teo (references/mascot.md): its avatar, banner, emoji and voice come from there.
  A new bot for a program uses the ATR mark avatar and the program name, never a new mascot.
- **Disclosure.** A bot that answers with AI says so in its profile and help command ("runs on Claude, an AI model
  by Anthropic, so it can be wrong"), says what text is sent to the model and asks people not to share personal
  information, grades, passwords or study data.
- **Young members.** Bots never move conversations with minors into DMs and never collect personal information.
- **Facts.** A bot answers lab questions only from verified facts and the lab's docs, and says plainly when a fact
  is not confirmed (the lab's room and phone, for example).
- **Formatting.** Discord renders Markdown but not tables; replies stay under about 1,200 characters with short
  paragraphs and code blocks.

## 6. Slack

| Asset | Size | Notes |
|---|---|---|
| Workspace icon | 512 × 512 (min 132) | ATR mark avatar, circle-safe |
| App or bot icon | 512-2000 px square | Teo avatar for Teo; ATR mark avatar for other lab apps |
| Custom emoji | 128 × 128 PNG, under 128 KB | Same `atr_*` and `teo_*` files as Discord |
| Channel names | lowercase, hyphens, no emoji | `#lab-news`, `#help-ros2`, `#proj-mini-turtlebot` |

## 7. GitHub repository pages

Basics (org avatar, social preview, the organization profile) are in references/web-and-digital.md §6. Every lab
repo README uses the same pattern:

1. **Header image** `.github/assets/header.png`, 1600 × 400: navy ground, horizontal ATR lockup top-left, the repo
   name as a big white title, a gold subtitle, triangle lattice on the right (and an optional mascot or icon in a
   gold ring). `python3 scripts/atr_design.py banner --preset github-header --title "Repo name" --subtitle "..."`.
2. **A bold one-sentence summary** and the affiliation line in `<sub>`: "Advanced Telerobotics Research Laboratory ·
   Department of Computer Science · Kent State University".
3. **Badges** in flat-square style, navy `003976`, slate `4A5868` for neutral facts:
   `https://img.shields.io/badge/ATR_Lab-Kent_State-003976?style=flat-square`.
4. **A "Start here" table** of two rows by three cells, each with a 44 px icon from `assets/icons/badges/`
   (resize the navy badge to 88 px for retina) linking to a section.
5. **Footer**: links to about, getting-started-atr-lab, dev-guidelines and all repositories, then the affiliation
   line and www.atr.cs.kent.edu.

## 8. How to make each asset

| Asset | Command or source |
|---|---|
| Banners, splash, profile banner, GitHub header, square thumbnails | `python3 scripts/atr_design.py banner --preset <name> ...` (`--list-presets`; `--safe-zones` to check) |
| Brand emoji (`atr_*`) | `assets/icons/badges/<name>-badge-navy.png` resized to 128 px |
| Mascot emoji and stickers (`teo_*`) | `assets/mascot/emoji/` and `assets/mascot/stickers/` (ready to upload); new poses per references/mascot.md §5 |
| Server icon, bot avatar | `assets/logos/icons/atr-avatar-mark-navy.png`; Teo: `assets/mascot/teo-avatar.png` |
| Embeds and cards | navy sidebar, a 1600 px banner image, verified facts only |
| Find any file | `python3 scripts/atr_design.py assets find <words>` |
