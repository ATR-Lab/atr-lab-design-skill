# ATR Lab icon set

Forty-three original glyphs for the Advanced Telerobotics Research (ATR) Lab, Kent State University.
They are derived from the ATR mark's geometry (straight strokes, 45 and 60 degree angles, chamfered
corners, the chevron gripper) so they sit next to the logo without competing with it.

Generated with Codex image generation from a locked style prompt and a style-anchor reference
(`scripts/icons/anchor.png`), keyed from chroma green to alpha, and recolored, badged and
traced programmatically. Full pipeline and regeneration instructions: `atr-lab-design/scripts/icons/README.md`.
Prompts for every generation: `build/icons-src/prompts.json` in the ATR build repo (not shipped with the
skill); the locked style prompt is the `style` field of `scripts/icons/icons.json`, and each icon's subject is in
the table below.

## Files

| Folder | Contents | Use |
|---|---|---|
| `png/<name>-navy.png` | ATR Navy `#003976` glyph, 512 px, transparent | on white, mist and gold backgrounds |
| `png/<name>-gold.png` | ATR Gold `#EFAB00` glyph | on navy or midnight only (gold on white is 2.0:1, it fails) |
| `png/<name>-white.png` | white glyph | on navy, midnight, photos with a dark overlay |
| `png/<name>-ink.png` | Ink `#1B2533` glyph | documents and UI that use ink text |
| `badges/<name>-badge-navy.png` | white glyph in a navy circle (11.4:1) | feature grids, program cards, social tiles |
| `badges/<name>-badge-gold.png` | navy glyph in a gold circle (5.7:1) | accents on white or navy |
| `svg/<name>.svg` | single-color polygon vector, `fill="currentColor"`, default `color="#003976"` | web, print, any size; tint with CSS `color` |
| `masters/<name>-mask.png` | alpha master (black) | make any new color with `scripts/icons/recolor.py` |

All rasters are 512 x 512. Square-ish glyphs are fitted to 76 % of the canvas (12 % padding); wide or
tall glyphs are enlarged up to 88 % of the canvas so they keep the same apparent size in a
row (`chroma_key.py --fit-max/--area-min`). Measured stroke weight of the outline glyphs:
0.061-0.098 of the canvas (median 0.070; about 8-9 % of the glyph width at the 76 % fit).
Filled silhouettes (`award`, `location`, `mechanical-gear`, `partnership`, `team`; `"fill": "solid"` in `icons.json`) read
0.11-0.16 because the measure sees the whole fill; they are conventional solid
pictograms (pin, gear, people, medal, handshake) and are exempt from the outline gate. Everything else is
an outline form with a hollow interior; solid fill is used only for small details (nodes, buttons, markers).
Every outline glyph is inside the 0.06-0.10 gate.

## Usage rules

1. **Minimum size**: **24 px** (0.25 in) for 37 glyphs; **32 px** for `digital-twin`, `human-robot-interaction`, `partnership`, `path-planning`, `quadruped`, `teleoperation`.
   The manifest repeats the minimum next to every icon that needs more than 24 px (compound glyphs
   with two figures or an arrow between objects, and fine-detailed ones). Never below 20 px. These
   minimums were set from `build/qa/icons/size-24px.png` and `size-32px.png`, where every icon is
   rendered at exactly that size. Prefer the SVG above 512 px.
2. **Color pairs**: navy on white/mist/gold; white or gold on navy/midnight; ink where the text is
   ink. Never gold on white (fails contrast); never white on gold. Do not add gradients, outlines,
   shadows or a second color inside a glyph. One color per icon.
3. **Badges** are for grids of three or more; do not badge a lone icon next to a heading. Keep one
   badge color per surface.
4. **Do not mix icon styles.** These glyphs are heavy geometric monoline with chamfered corners.
   Rounded-corner sets (Material, Font Awesome, Phosphor, Feather) look wrong beside them.
   *Exception:* tiny utility glyphs in running text or contact lines (phone, mail, link, arrow,
   chevron, external-link, close) at 12-16 px may use **Lucide** (ISC license, `lucide-static` in the
   build's node_modules). Use Lucide there at stroke 2.5, never in feature grids, never above 20 px
   next to an ATR icon.
5. **Spacing**: leave clear space equal to the icon's padding (12 % of its box) around it; align to the
   glyph box, not to the visible ink.
6. **Meaning**: use an icon for the meaning in the table. Do not use `humanoid` or `quadruped` to
   stand for a specific real robot (imagery integrity rule: AI-generated graphics are never
   presented as real lab hardware or results).
7. **The ATR mark is not an icon.** Do not use it in an icon row or inside a badge; the `gripper`
   glyph carries the brand echo where one is wanted.
8. **Adding icons**: follow `scripts/icons/README.md`; new glyphs must be generated against the same
   anchor and pass the same QA: contact sheets at 24/32/48/64 px, stroke fraction 0.06-0.10
   for outline glyphs (normalise with `min_stroke` in `selection.json` when the generator draws
   connecting bars thin), filled silhouettes only for conventional solid pictograms. Do not
   hand-draw additions in another style.

## Manifest

Every icon's generation prompt is `Icon subject: <subject>. <style block> <reference note>` where the
style block and reference note are quoted once at the end of this file. Files per icon:
`png/<name>-{navy,gold,white,ink}.png`, `badges/<name>-badge-{navy,gold}.png`, `svg/<name>.svg`,
`masters/<name>-mask.png`. "src" is the raw generation the icon was keyed from (relative to
`build/icons-src/` in the ATR build repo); "stroke" is the measured stroke fraction of the 512 px canvas.


### Robotics and research

| Icon | Name | Meaning | Keywords | Notes | Subject line of the prompt |
|---|---|---|---|---|---|
| ![telepresence-robot](png/telepresence-robot-navy.png) | `telepresence-robot` | Telepresence robot (screen on a mast on a wheeled base) | telepresence, remote presence, mobile screen robot | stroke 0.06; src `sheets/cells/telepresence-robot-A-v1.png` | a telepresence robot: a rectangular screen head at the top of a tall vertical mast that rises from a wide low trapezoid base with two small wheels drawn as hexagons |
| ![teleoperation](png/teleoperation-navy.png) | `teleoperation` | Teleoperation: an operator linked to a remote robot | teleoperation, remote control, operator, link, tele-embodiment | min 32 px (compound); stroke 0.07; src `sheets/cells/teleoperation-A-v1.png` | teleoperation: on the left a human operator drawn as a head-and-shoulders bust (octagon head), on the right a small robot drawn as a square head with two short antenna and angular shoulders, and between them a horizontal zigzag signal line connecting the two |
| ![vr-headset](png/vr-headset-navy.png) | `vr-headset` | Virtual reality / immersive interface | VR, virtual reality, headset, HMD, immersive, XR | stroke 0.08; src `test-sheets/cells/vr-headset.png` | a virtual reality headset seen from the front: a wide visor body with chamfered corners, two square eye lenses cut out of the front, a shallow notch at the bottom center for the nose, and a short strap stub on each side |
| ![haptic-glove](png/haptic-glove-navy.png) | `haptic-glove` | Haptic feedback / wearable interface | haptic, glove, touch, tactile, wearable, hand | stroke 0.08; src `fix/haptic-glove-fix-v5.png` | a haptic glove: an open hand seen palm-out, a solid silhouette with five straight fingers of equal width and chamfered tips, the wrist cuff joined to the palm as part of the same shape, and one small solid square sensor pad sitting on top of the index fingertip, slightly wider than the finger; all parts as thick as the reference icon's arms; no other marks |
| ![robotic-arm](png/robotic-arm-navy.png) | `robotic-arm` | Robot manipulator arm | robot arm, manipulator, industrial robot, articulated, joint | stroke 0.09; src `test-sheets/cells/robotic-arm.png` | an industrial robot arm seen from the side: a flat wide base at the bottom, a vertical lower link, an angular elbow joint drawn as a small octagon, and a diagonal upper link rising to the upper right that ends in a small open two-finger gripper |
| ![gripper](png/gripper-navy.png) | `gripper` | Robot gripper / manipulation; the ATR mark's own chevron gripper. Also the set's style anchor. | gripper, claw, end effector, grasp, manipulation, ATR | style anchor; stroke 0.09; src `anchor/gripper-b.png` | a robotic parallel gripper seen from the front: a short vertical wrist stem at the top joined to a horizontal bar, with two symmetric angular finger arms hanging down and bending inward like chevrons, jaws open. The two finger arms are angular chevrons with 45-degree bends, echoing a triangle-and-chevron logo geometry |
| ![humanoid](png/humanoid-navy.png) | `humanoid` | Humanoid robot | humanoid, android, bipedal, robot body | stroke 0.07; src `test-sheets/cells/humanoid.png` | a humanoid robot standing upright facing forward: a square head with two small square eyes, a rectangular torso, two straight arms angled slightly outward, and two straight legs |
| ![quadruped](png/quadruped-navy.png) | `quadruped` | Quadruped / legged robot | quadruped, robot dog, legged robot, walking robot | min 32 px (compound); stroke 0.07; src `fix/cells/quadruped-S-v1.png` | a quadruped robot dog seen from the side: a long solid rectangular body, a small angular head at the front right, and four heavy legs each drawn as two thick straight segments with a bent knee; all strokes as heavy as the reference icon |
| ![drone-uav](png/drone-uav-navy.png) | `drone-uav` | Drone / unmanned aerial vehicle | drone, UAV, quadcopter, aerial, flight | stroke 0.07; src `test-sheets/cells/drone-uav.png` | a quadcopter drone seen from above: a small central hexagonal body with four diagonal arms at 45 degrees, each ending in a propeller rotor drawn as a diamond shape |
| ![mobile-rover](png/mobile-rover-navy.png) | `mobile-rover` | Wheeled mobile robot / rover | rover, mobile robot, wheeled, ground robot, AGV | stroke 0.09; src `sheets/cells/mobile-rover-A-v1.png` | a wheeled mobile rover seen from the side: a low rectangular chassis, two large octagonal wheels, and a short vertical sensor mast with a small square sensor head rising from the top |
| ![lidar-sensor](png/lidar-sensor-navy.png) | `lidar-sensor` | Lidar / range sensing | lidar, laser scanner, range sensor, point cloud, perception | stroke 0.07; src `fix/lidar-sensor-fix-v5.png` | a lidar sensor: a solid octagonal sensor puck standing on a short tripod of three straight legs, emitting three nested chevron-shaped scan arcs (angular V shapes with the apex pointing left toward the puck, increasing in size) to the right of the puck, each chevron a heavy stroke as thick as the reference icon's arms and all three centred on the puck's horizontal centre line; no thin lines, no other marks |
| ![camera-vision](png/camera-vision-navy.png) | `camera-vision` | Camera / computer vision | camera, vision, imaging, computer vision, perception | stroke 0.06; src `fix/camera-vision-fix-v5.png` | a machine vision camera seen from the front drawn as a heavy hollow outline: a wide rectangular body with chamfered corners, a large octagonal lens ring in the centre with a small solid octagon inside it, and a small rectangular bump on the top edge; every stroke as thick as the reference icon's arms; no thin lines |
| ![ai-neural-net](png/ai-neural-net-navy.png) | `ai-neural-net` | Artificial intelligence / machine learning | AI, neural network, machine learning, deep learning, model | stroke 0.07; src `fix/ai-neural-net-fix-v6.png` | a neural network drawn as one chunky connected shape: a column of two solid hexagonal nodes on the left and a column of two solid hexagonal nodes on the right, fully connected by four straight thick struts (two horizontal struts and two diagonal struts that cross in the centre), every strut as thick as the reference icon's arms; no thin lines, no other marks |
| ![digital-twin](png/digital-twin-navy.png) | `digital-twin` | Digital twin / simulation-to-reality | digital twin, sim2real, virtual model, mirror | min 32 px (compound); stroke 0.06; src `fix/digital-twin-fix-v3.png` | a digital twin: a solid black isometric cube at the lower left and its twin at the upper right drawn as a chunky outlined cube whose edges are thick bands as thick as the reference icon's arms (not a thin wireframe), joined by a short heavy double-ended diagonal arrow; no hidden edges |
| ![ros-graph](png/ros-graph-navy.png) | `ros-graph` | ROS computation graph / nodes and topics | ROS, graph, nodes, topics, architecture, network | stroke 0.07; src `sheets/cells/ros-graph-B-v1.png` | a node graph: four hexagonal nodes arranged as a diamond (top, left, right, bottom) connected by straight edges forming the diamond's outline, plus one edge from the left node to the right node |
| ![simulation](png/simulation-navy.png) | `simulation` | Simulation environment / physics sim | simulation, Gazebo, physics, virtual environment, sandbox | compound; stroke 0.07; src `fix/simulation-fix-v3.png` | a physics simulation: one large solid black isometric cube standing on a chunky diamond-shaped ground-plane frame; the frame is a thick band as thick as the reference icon's arms (not a thin outline), and the cube covers about half the icon width |
| ![wireless-link](png/wireless-link-navy.png) | `wireless-link` | Wireless communication / network link | wireless, signal, radio, WiFi, 5G, network, telecom | stroke 0.07; src `fix/wireless-link-fix-v1.png` | a wireless signal: a small solid hexagon at the bottom center as the signal source, with three nested angular chevron signal waves (inverted V shapes, apex pointing up, increasing in width) fanning out above it, each chevron a heavy stroke with chamfered ends; no mast, no base, no other marks |
| ![joystick](png/joystick-navy.png) | `joystick` | Joystick / manual control input | joystick, controller, input, gamepad, manual control | stroke 0.07; src `fix/joystick-fix-v6.png` | a joystick controller: a vertical stick topped by a solid octagonal knob, standing on a wide low base drawn as a heavy hollow trapezoid outline as thick as the reference icon's arms, with one small solid square button on the top edge of the base to the right of the stick; no thin lines |
| ![flight-simulator](png/flight-simulator-navy.png) | `flight-simulator` | Flight simulator / pilot training (attitude indicator) | flight simulator, pilot training, aviation, attitude indicator, cockpit | stroke 0.07; src `fix/cells/flight-simulator-S-v2.png` | a flight simulator instrument: a large octagonal dial drawn as a heavy outline, with a bold solid airplane silhouette seen from above (straight swept-back wings, a chamfered tail, nose pointing up) about 45 percent of the dial width centered inside the dial; no other marks inside the dial |
| ![path-planning](png/path-planning-navy.png) | `path-planning` | Path planning / navigation / autonomy | path planning, navigation, route, autonomy, waypoint, SLAM | min 32 px (compound); stroke 0.07; src `sheets/cells/path-planning-E-v1.png` | path planning: a solid square start marker at the bottom left and a solid diamond goal marker at the top right, connected by one continuous heavy route line (same stroke thickness as everything else, not dashed) made of straight segments with right-angle turns that steps around a small solid square obstacle in the middle |
| ![human-robot-interaction](png/human-robot-interaction-navy.png) | `human-robot-interaction` | Human-robot interaction | HRI, human robot interaction, collaboration, social robot | min 32 px (compound); stroke 0.08; src `sheets/cells/human-robot-interaction-B-v1.png` | human-robot interaction: a human head-and-shoulders bust (octagon head) on the left and a robot head-and-shoulders bust (square head with one short antenna) on the right, facing each other, with a small horizontal double-ended arrow between them at chest height |
| ![safety-shield](png/safety-shield-navy.png) | `safety-shield` | Safety / trust / security | safety, secure, protection, shield, trust, reliability | stroke 0.07; src `sheets/cells/safety-shield-B-v1.png` | a shield: a straight top edge, straight sides that angle inward and converge to a point at the bottom, with a bold checkmark drawn from straight segments inside |
| ![embedded-chip](png/embedded-chip-navy.png) | `embedded-chip` | Embedded systems / hardware / compute | chip, microcontroller, embedded, hardware, processor, electronics | stroke 0.07; src `sheets/cells/embedded-chip-B-v1.png` | a microchip: a square chip body with chamfered corners containing a smaller square die, with three short straight pin legs sticking out of each of the four sides |

### Lab and program

| Icon | Name | Meaning | Keywords | Notes | Subject line of the prompt |
|---|---|---|---|---|---|
| ![team](png/team-navy.png) | `team` | Lab members / team / people | team, people, members, group, staff, community | compound; stroke 0.12 (solid); src `sheets/cells/team-C-v1.png` | a team: three head-and-shoulders figures side by side, each with an octagon head and angular shoulders, the middle figure slightly taller and in front |
| ![student](png/student-navy.png) | `student` | Students / graduate education | student, graduate, education, degree, mortarboard, academic | stroke 0.08; src `test-sheets/cells/student.png` | a graduate: a mortarboard graduation cap (a flat wide diamond board with a short tassel hanging from its right corner) sitting on top of a head-and-shoulders bust with angular shoulders |
| ![k12-outreach](png/k12-outreach-navy.png) | `k12-outreach` | K-12 outreach / school programs | K-12, outreach, school, kids, education, community, workshop | stroke 0.08; src `sheets/cells/k12-outreach-C-v1.png` | a schoolhouse: a house-shaped pentagon building with a pitched roof, a small square bell cupola on the roof peak, a rectangular door in the middle and one square window on each side of the door |
| ![workshop-idea](png/workshop-idea-navy.png) | `workshop-idea` | Ideas / workshops / innovation | idea, lightbulb, innovation, workshop, creativity, brainstorm | stroke 0.06; src `sheets/cells/workshop-idea-C-v1.png` | an idea lightbulb: a hexagonal bulb over a screw base made of two short horizontal bars, with three short straight rays radiating from the top of the bulb |
| ![publication](png/publication-navy.png) | `publication` | Publications / papers / documents | publication, paper, document, article, journal, report | stroke 0.08; src `test-sheets/cells/publication.png` | a document page: a tall rectangle with its top-right corner chamfered off (folded corner), containing three short horizontal text lines drawn as bars |
| ![award](png/award-navy.png) | `award` | Awards / honors / competitions | award, medal, prize, honor, competition, achievement | stroke 0.11 (solid); src `sheets/cells/award-C-v1.png` | an award medal: a hexagonal medal with a small star made of straight segments inside, hanging from two angled ribbon tails that form a V above it |
| ![calendar-event](png/calendar-event-navy.png) | `calendar-event` | Events / dates / schedule | calendar, event, date, schedule, deadline, seminar | stroke 0.07; src `sheets/cells/calendar-event-C-v1.png` | a calendar page: a rectangle with two short binding tabs sticking up from the top edge, a horizontal header bar, and a 3 by 2 grid of small squares below the header with one square filled solid |
| ![location](png/location-navy.png) | `location` | Location / campus / address | location, map pin, address, campus, place, directions | stroke 0.16 (solid); src `sheets/cells/location-C-v1.png` | a map pin: an angular marker shaped like a hexagon on top tapering to a sharp point at the bottom, with a small hexagonal hole in the center of the upper part |
| ![email](png/email-navy.png) | `email` | Email / contact | email, mail, contact, message, envelope | stroke 0.07; src `test-sheets/cells/email.png` | an envelope: a wide rectangle with a V-shaped flap whose two diagonal lines run from the top corners to a point in the middle |
| ![website-globe](png/website-globe-navy.png) | `website-globe` | Website / web / global | website, web, globe, internet, online, global, URL | stroke 0.08; src `sheets/cells/website-globe-C-v1.png` | a globe drawn as a large octagon containing a vertical axis line, a horizontal equator line, and a tall narrow diamond-shaped meridian centered inside |
| ![code](png/code-navy.png) | `code` | Code / software / open source | code, software, programming, GitHub, open source, developer | stroke 0.09; src `sheets/cells/code-C-v1.png` | code brackets: a chevron pointing left on the left side, a chevron pointing right on the right side, and a steep diagonal slash between them, all drawn as bold strokes |
| ![dataset](png/dataset-navy.png) | `dataset` | Datasets / data / storage | dataset, data, database, storage, benchmark, records | stroke 0.07; src `fix/dataset-fix-v6.png` | a database drawn with straight segments only: a tall upright container with a flat hexagonal top and bottom (a cylinder seen slightly from above but built from straight lines), drawn as a heavy hollow outline as thick as the reference icon's arms, divided into three bands by two heavy horizontal bars across its full width; no thin lines |
| ![mechanical-gear](png/mechanical-gear-navy.png) | `mechanical-gear` | Mechanical / engineering / settings | gear, cog, mechanical, engineering, settings, hardware | stroke 0.15 (solid); src `test-sheets/cells/mechanical-gear.png` | a gear: an octagonal cog wheel with eight square teeth around its rim and a hexagonal hole in the center |
| ![milestone-flag](png/milestone-flag-navy.png) | `milestone-flag` | Milestones / goals / project status | milestone, flag, goal, checkpoint, status, progress | stroke 0.09; src `sheets/cells/milestone-flag-D-v2.png` | a milestone flag: a vertical pole with a pennant flag (a triangle pointing to the right) attached at the top, standing on a short horizontal base bar |
| ![launch-rocket](png/launch-rocket-navy.png) | `launch-rocket` | Launch / new project / startup | rocket, launch, start, kickoff, mission, new project | stroke 0.07; src `test-sheets/cells/launch-rocket.png` | a rocket pointing straight up: a triangular nose cone, a straight rectangular body with a small diamond window, two angled fins at the bottom sides, and a small triangular exhaust flame below |
| ![partnership](png/partnership-navy.png) | `partnership` | Partnerships / collaboration / sponsors | partnership, handshake, collaboration, sponsor, industry, agreement | min 32 px (compound); stroke 0.11 (solid); src `fix/partnership-fix-v1.png` | a handshake: two simplified clasped hands drawn as solid silhouettes with straight rectangular cuffs entering from the left and the right, at most three finger notches in total, one heavy negative-space line between the two hands, no knuckle detail, no thin lines |
| ![funding](png/funding-navy.png) | `funding` | Funding / grants / support | funding, grant, money, coins, budget, sponsor | stroke 0.07; src `fix/funding-fix-v5.png` | funding: a money bag drawn as a heavy hollow outline built only from straight segments: a wide octagonal body, a narrow tied neck with two short tie ends at the top, and a small solid diamond in the centre of the body; the outline as thick as the reference icon's arms; no text, no currency symbol, no thin lines |
| ![presentation](png/presentation-navy.png) | `presentation` | Presentations / talks / seminars | presentation, talk, slides, seminar, lecture, projector | stroke 0.07; src `sheets/cells/presentation-D-v1.png` | a presentation screen: a wide rectangular projector screen hanging from a horizontal top bar, with a small three-bar chart inside the screen and a short vertical stand with two angled legs below |
| ![results-chart](png/results-chart-navy.png) | `results-chart` | Results / metrics / data analysis | results, chart, metrics, analytics, growth, performance | stroke 0.10; src `sheets/cells/results-chart-D-v1.png` | a results chart: three vertical bars of increasing height side by side, with a diagonal upward trend arrow above them pointing to the upper right |
| ![video-demo](png/video-demo-navy.png) | `video-demo` | Video / demos / media | video, demo, media, play, YouTube, film | stroke 0.07; src `sheets/cells/video-demo-D-v1.png` | a video frame: a wide rectangle with chamfered corners containing a large right-pointing triangular play button in its center |
## Shared prompt text

Style block (identical for every icon):

> Style: a single flat geometric monoline pictogram with one uniform heavy stroke weight (each stroke about 8 percent of the icon width), built only from straight line segments meeting at 45-degree and 60-degree angles, with chamfered (beveled, cut-off) corners and no rounded corners and no curves, minimal detail so it stays readable at 24 pixels. Colors: the glyph is solid pure black (#000000) and the ENTIRE background is one perfectly flat, uniform chroma-key green (#00FF00) that fills the whole square canvas edge to edge. Absolutely no shading, no gradients, no shadows, no outlines, no highlights, no texture, no text, no letters, no numbers, no watermark, no border, no frame, no ground line, no extra background shapes. The subject is centered on a square canvas with about 12 percent empty green margin on every side.

Reference note (appended because the anchor image `scripts/icons/anchor.png` was attached to every generation):

> The attached reference image is a sibling icon from the same icon set: match its stroke thickness, chamfered corner style, angle vocabulary and overall visual density exactly, but do NOT copy its subject; draw only the subject described here.

Sheet generations wrap nine subjects in one prompt ("A 3 by 3 grid of 9 separate, unrelated icons on
ONE square canvas ... Row 1 (left to right): cell 1: <subject>; ..."); see `scripts/icons/generate.py`.
Icons regenerated in the fix rounds carry the subject line that produced the shipped file; the earlier
wordings are preserved in the build repo's `build/icons-src/prompts.json` (one record per Codex call).

## QA record

Contact sheets in `build/qa/icons/`: `set-on-white.png`, `set-on-navy.png`, `set-on-gold.png`,
`set-ink.png`, `size-24px.png`, `size-32px.png`, `size-48px.png`, `size-64px.png`, `badges.png`,
`badges-gold.png`, `svg-renders.png`, `anchor-candidates.png`, `test-sheet-vs-singles.png`, the
`compare-*.png` variant comparisons, the fix-round sheets (`fix-finalists.png`, `fix2-candidates.png`)
and `weights.csv`. Independent verification sheets and pixel checks: `build/qa/icons-verify/`.
SVG round-trip IoU against the masters: 0.984-0.997.
