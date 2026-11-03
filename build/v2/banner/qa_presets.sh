#!/bin/bash
# Render every banner preset to the ws1 QA folder (with safe-zone overlays).
set -u
SK=~/Active/atr-lab-design-skill-v2/atr-lab-design
PY=~/Active/.venvs/atr-design-v2/bin/python
Q=/Volumes/MARCUS-PROJECTS/_agents/scratch/2026-11-03-atr-design-v2/ws1/qa
R=/Volumes/MARCUS-PROJECTS/_agents/reports/2026-10-23-atr-discord-revamp
TEO=assets/mascot/views/teo-front.png
export PYTHONDONTWRITEBYTECODE=1
cd $SK
mkdir -p $Q
b() { echo "--- $*"; $PY $SK/scripts/banner.py "$@" --safe-zones; echo "exit $?"; }
b --preset github-header --title "Dev guidelines" --subtitle "Style guides, lint configs and Git practices" -o $Q/p-github-header.png
b --preset github-header --title "Teo Discord Bot" --subtitle "The ATR Lab's assistant on Discord, powered by Claude" --image $TEO -o $Q/p-github-header-teo.png
b --preset github-social --eyebrow "ATR Lab  ·  open source" --title "teo-discord-bot" --subtitle "The lab's assistant on Discord" -o $Q/p-github-social.png
b --preset discord-banner --title "ATR Lab community" -o $Q/p-discord-banner.png
b --preset discord-invite-splash --image $TEO -o $Q/p-discord-invite-splash.png
b --preset profile-banner --title "Teo" --subtitle "Assistant bot of the ATR Lab" --eyebrow "Mention @Teo  ·  /ask" -o $Q/p-profile-banner.png
b --preset x-header --title "Advanced Telerobotics Research Lab" --subtitle "Telepresence, tele-embodiment and Physical AI at Kent State" -o $Q/p-x-header.png
b --preset youtube-banner --title "ATR Lab" --subtitle "Telerobotics research at Kent State" -o $Q/p-youtube-banner.png
b --preset og-image --title "Physical AI workshop" --subtitle "Nov. 14, 2026  ·  Mathematical Sciences Building" -o $Q/p-og-image.png
b --preset thumbnail-square --icon email -o $Q/p-thumbnail-email.png
b --preset thumbnail-square --image assets/mascot/expressions/teo-thinking.png -o $Q/p-thumbnail-teo.png
b --preset thumbnail-square --icon milestone-flag --title "Rules" -o $Q/p-thumbnail-rules.png
b --preset slide-16x9 --eyebrow "IEEE RO-MAN 2026  ·  Sept. 23" --title "Telepresence for everyone" --subtitle "Jong-Hoon Kim, Advanced Telerobotics Research Lab" -o $Q/p-slide.png
b --preset github-header --ground white --title "Dev guidelines" --subtitle "Style guides, lint configs and Git practices" --hazard bottom -o $Q/p-github-header-white.png
b --preset github-header --ground midnight --art subtle --title "Dev guidelines" -o $Q/p-github-header-midnight-subtle.png
b --size 2400x300 --title "Very wide strip" --hazard top -o $Q/p-custom-2400x300.png
b --size 1080x1350 --icon drone --title "Drone lab" --subtitle "Open house" --hazard left -o $Q/p-custom-1080x1350.png
