#!/usr/bin/env python3
"""Fix round (after the icon critic): write alternate icons.json manifests with reworded subjects.

generate.py takes --manifest, so each candidate wording gets its own manifest here and the
actual prompt sent is logged by generate.py into build/icons-src/prompts.json. Whichever variant
is adopted has its subject copied back into atr-lab-design/scripts/icons/icons.json (the
previous wording is preserved in rebuild_prompts.py so the older records stay exact).

  alt-A.json   first candidate wording  (singles, --tag fix-v1)
  alt-B.json   second candidate wording (singles, --tag fix-v2)
  alt-S.json   the alt-A wording for the four thin icons plus "heavier" rewordings of the four
               stroke-floor outliers, generated as 3x3 sheets (--tag S-v1 / S-v2)
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
BASE = json.load(open(os.path.join(ROOT, "atr-lab-design", "scripts", "icons", "icons.json")))

HEAVY = "drawn with the same heavy stroke as the reference icon's arms"

ALT_A = {
    "simulation": "a physics simulation: one large SOLID isometric cube about half the icon width standing on a single heavy diamond-shaped ground-plane outline " + HEAVY + "; no interior grid lines, no thin lines",
    "digital-twin": "a digital twin: a SOLID isometric cube at the lower left and an identical isometric cube drawn as a heavy outline at the upper right, each about 40 percent of the icon width, joined by a short heavy diagonal double-ended arrow between them; no hidden edges, no dashed lines, no thin lines",
    "partnership": "a handshake: two simplified clasped hands drawn as solid silhouettes with straight rectangular cuffs entering from the left and the right, at most three finger notches in total, one heavy negative-space line between the two hands, no knuckle detail, no thin lines",
    "ai-neural-net": "a neural network diagram: five solid hexagonal nodes in three columns (one node on the left, three nodes stacked in the middle, one node on the right), each middle node joined to the left node and to the right node by a straight connection bar about half as thick as a node is wide (the same heavy stroke as the reference icon); no thin lines",
    "flight-simulator": "a flight simulator instrument: a large octagonal dial drawn as a heavy outline, with a bold solid airplane silhouette seen from above (straight swept-back wings, a chamfered tail, nose pointing up) about 45 percent of the dial width centered inside the dial; no other marks inside the dial",
    "funding": "funding: a stack of three flat coins seen edge-on (three wide flat bars with chamfered ends, one above the other with clear gaps) on the left, and one upright octagonal coin standing to the right of the stack showing a thick inner octagon ring; no text, no currency symbol",
    "wireless-link": "a wireless signal: a small solid hexagon at the bottom center as the signal source, with three nested angular chevron signal waves (inverted V shapes, apex pointing up, increasing in width) fanning out above it, each chevron a heavy stroke with chamfered ends; no mast, no base, no other marks",
    "dataset": "a database: a vertical stack of three flat hexagonal plates (wide flat hexagons seen edge-on) one above the other, with the gaps between the plates as wide as the stroke of the reference icon so the three plates stay clearly separate",
}

ALT_B = {
    "simulation": "a physics simulation: a large solid isometric cube (about half the icon width) resting on a wide flat isometric slab drawn as a heavy diamond outline beneath it, the slab wider than the cube; all strokes as heavy as the reference icon, no grid, no thin lines",
    "digital-twin": "a digital twin: a SOLID isometric cube at the upper left and an identical isometric cube drawn as a heavy outline at the lower right, each about 40 percent of the icon width, stacked diagonally so the composition is nearly square, joined by a short heavy double-ended diagonal arrow; no hidden edges, no dashed lines, no thin lines",
    "partnership": "a handshake seen from above at a 45-degree diagonal: two simplified solid hand silhouettes clasped in the middle, the left hand entering from the lower left corner and the right hand from the upper right corner, each with a straight cuff, at most three finger notches, one heavy negative-space line between them, no knuckle detail",
    "ai-neural-net": "a neural network diagram: four solid hexagonal nodes in three columns (one node on the left, two nodes stacked in the middle, one node on the right), each middle node joined to the left node and to the right node by a straight connection bar about half as thick as a node is wide (the same heavy stroke as the reference icon); no thin lines",
    "flight-simulator": "a flight simulator instrument: a large octagonal dial outline with a heavy horizontal horizon line across its middle and a bold solid airplane silhouette seen from the front (a long straight wing bar with a short vertical tail fin rising from its center and a small solid fuselage block) about half the dial width sitting on the horizon line",
    "funding": "funding: a stack of four flat coins seen edge-on (four wide flat bars with chamfered ends, one above the other with clear gaps) with a short heavy upward-pointing arrow (straight shaft, chevron head) standing to the right of the stack; no text, no currency symbol",
    "wireless-link": "a wireless signal: a short heavy vertical antenna mast at the bottom center with no base, and three nested angular chevron signal waves (inverted V shapes with the apex pointing up, increasing in width) stacked above the top of the mast with the smallest chevron closest to the mast",
    "dataset": "a database: a vertical stack of three wide flat hexagonal plates seen edge-on, each plate drawn as a heavy outline (not filled), one above the other with clear gaps between them",
}

ALT_S = dict(ALT_A)
ALT_S.update({
    "teleoperation": "teleoperation: on the left a human operator drawn as a head-and-shoulders bust with an octagon head, on the right a small robot with a square head, two short antennas and angular shoulders, the two figures each about 40 percent of the icon width, and between them a short heavy zigzag signal line; all strokes heavy",
    "quadruped": "a quadruped robot dog seen from the side: a long solid rectangular body, a small angular head at the front right, and four heavy legs each drawn as two thick straight segments with a bent knee; all strokes as heavy as the reference icon",
    "path-planning": "path planning: a solid square start marker at the bottom left and a solid diamond goal marker at the top right, connected by one continuous heavy route line (as thick as the reference icon's arms, not dashed) made of straight segments with right-angle turns that steps around a small solid square obstacle in the middle",
    "ros-graph": "a node graph: four solid hexagonal nodes arranged as a diamond (top, left, right, bottom) connected by heavy straight edges forming the diamond's outline, plus one heavy edge from the left node to the right node; all edges as thick as the reference icon's arms",
})

SHEET_NAMES = "simulation,digital-twin,partnership,ai-neural-net,teleoperation,quadruped,path-planning,ros-graph,flight-simulator"
SINGLE_NAMES = ",".join(ALT_A)


def write(name, overrides):
    m = json.loads(json.dumps(BASE))
    for k, v in overrides.items():
        m["icons"][k]["subject"] = v
    p = os.path.join(HERE, name)
    json.dump(m, open(p, "w"), indent=1)
    print("wrote", p, len(overrides), "overrides")


if __name__ == "__main__":
    write("alt-A.json", ALT_A)
    write("alt-B.json", ALT_B)
    write("alt-S.json", ALT_S)
    print("singles:", SINGLE_NAMES)
    print("sheet:", SHEET_NAMES)

# ---- round 3 (after looking at round 1/2): the model draws outlines and connecting bars thinner than
# solid parts whatever the wording; these try "chunky band / strut / solid" phrasing and new metaphors.
ALT_C = {
    "ai-neural-net": "a neural network: four solid black hexagonal nodes (one on the left, two stacked in the middle, one on the right) where every neighbouring pair of nodes is joined by a short solid black strut as thick as the reference icon's arms, so the whole diagram is one chunky connected shape with no thin lines anywhere",
    "simulation": "a physics simulation: one large solid black isometric cube standing on a chunky diamond-shaped ground-plane frame; the frame is a thick band as thick as the reference icon's arms (not a thin outline), and the cube covers about half the icon width",
    "digital-twin": "a digital twin: a solid black isometric cube at the lower left and its twin at the upper right drawn as a chunky outlined cube whose edges are thick bands as thick as the reference icon's arms (not a thin wireframe), joined by a short heavy double-ended diagonal arrow; no hidden edges",
    "dataset": "a database: three solid black flat hexagonal plates (each a wide flat hexagon seen edge-on, filled solid black, not outlined) stacked vertically with clear green gaps between them about as wide as the stroke of the reference icon",
    "funding": "funding: a solid black money bag built only from straight segments (a wide octagonal body, a narrow tied neck and two short tie ends at the top) with a small green diamond cut out of the center of the body; no text, no currency symbol",
}
ALT_D = {
    "ai-neural-net": "a neural network drawn as one solid black chunky shape: three solid hexagonal nodes in a row in the middle (left, center, right) joined by short thick solid struts, and two more solid hexagonal nodes above and below the center node joined to it by thick solid struts, all struts as thick as the reference icon's arms, no thin lines",
    "simulation": "a physics simulation: a solid black isometric cube resting on a solid black flat isometric slab (a wide flat diamond) with a narrow green gap between the bottom of the cube and the slab so the two shapes stay separate; the slab wider than the cube; no thin lines",
    "digital-twin": "a digital twin: two identical solid black isometric cubes, one at the lower left and one at the upper right, each about 40 percent of the icon width, the upper right cube having a small green diamond cut out of its front face, joined by a short heavy double-ended diagonal arrow; no thin lines",
    "dataset": "a database: a vertical stack of three solid black hexagonal plates seen edge-on, each plate a wide flat filled hexagon, separated by clear green gaps as wide as the reference icon's stroke; the stack fills about three quarters of the icon height",
    "funding": "funding: a banknote drawn as one wide horizontal rectangle with chamfered corners as a thick outline as thick as the reference icon's arms, containing one solid octagonal coin in the center and a small solid diamond near each short end; no text, no currency symbol",
}
ROUND3_NAMES = ",".join(ALT_C)

if __name__ == "__main__":
    write("alt-C.json", ALT_C)
    write("alt-D.json", ALT_D)
    print("round 3:", ROUND3_NAMES)

# ---- round 4 (fixer pass, after the critic): the icons no earlier finalist fixes. ai-neural-net gets a
# 2x2 fully-connected topology (the 1-2-1 / diamond variants duplicate ros-graph and 2-3-2 blobs at 24 px);
# dataset, joystick, funding and camera-vision are redrawn as hollow outlines so they match the outline
# anchor instead of reading as solid blobs; lidar gets chevron arcs symmetric about the puck; haptic-glove
# gets equal fingers, a joined cuff and a clear sensor cue. --tag fix-v5 (ALT_E) and fix-v6 (ALT_F).
ARMS = "as thick as the reference icon's arms"
ALT_E = {
    "ai-neural-net": "a neural network: two columns of solid hexagonal nodes, two nodes on the left and two nodes on the right, where every left node is joined to every right node by a straight solid connection bar " + ARMS + ", so the four bars form two horizontal bars and one X crossing in the middle; no thin lines, no other marks",
    "dataset": "a database: three outlined flat hexagonal plates (wide flat hexagons seen edge-on), each drawn as a heavy hollow outline " + ARMS + " with an empty green centre, stacked vertically one above the other with small clear gaps between the plates; no filled plates, no thin lines",
    "joystick": "a joystick controller: a vertical stick topped by a solid octagonal knob, rising from a wide low trapezoid base that is drawn as a heavy hollow outline (not filled) " + ARMS + ", with one small solid square button standing on the base to the right of the stick; no thin lines",
    "lidar-sensor": "a lidar sensor: a solid octagonal sensor puck standing on a short tripod of three straight legs, emitting three nested chevron-shaped scan arcs (angular V shapes with the apex pointing left toward the puck, increasing in size) to the right of the puck, each chevron a heavy stroke " + ARMS + " and all three centred on the puck's horizontal centre line; no thin lines, no other marks",
    "haptic-glove": "a haptic glove: an open hand seen palm-out, a solid silhouette with five straight fingers of equal width and chamfered tips, the wrist cuff joined to the palm as part of the same shape, and one small solid square sensor pad sitting on top of the index fingertip, slightly wider than the finger; all parts " + ARMS + "; no other marks",
    "funding": "funding: a money bag drawn as a heavy hollow outline built only from straight segments: a wide octagonal body, a narrow tied neck with two short tie ends at the top, and a small solid diamond in the centre of the body; the outline " + ARMS + "; no text, no currency symbol, no thin lines",
    "camera-vision": "a machine vision camera seen from the front drawn as a heavy hollow outline: a wide rectangular body with chamfered corners, a large octagonal lens ring in the centre with a small solid octagon inside it, and a small rectangular bump on the top edge; every stroke " + ARMS + "; no thin lines",
}
ALT_F = {
    "ai-neural-net": "a neural network drawn as one chunky connected shape: a column of two solid hexagonal nodes on the left and a column of two solid hexagonal nodes on the right, fully connected by four straight thick struts (two horizontal struts and two diagonal struts that cross in the centre), every strut " + ARMS + "; no thin lines, no other marks",
    "dataset": "a database drawn with straight segments only: a tall upright container with a flat hexagonal top and bottom (a cylinder seen slightly from above but built from straight lines), drawn as a heavy hollow outline " + ARMS + ", divided into three bands by two heavy horizontal bars across its full width; no thin lines",
    "joystick": "a joystick controller: a vertical stick topped by a solid octagonal knob, standing on a wide low base drawn as a heavy hollow trapezoid outline " + ARMS + ", with one small solid square button on the top edge of the base to the right of the stick; no thin lines",
    "lidar-sensor": "a lidar sensor: an outlined octagonal sensor puck (hollow, heavy outline) on a short vertical stem with a small flat base, emitting three nested chevron-shaped scan arcs (angular V shapes pointing left toward the puck, increasing in size) to the right of the puck, each chevron " + ARMS + " and all three centred on the puck's horizontal centre line; no thin lines",
    "haptic-glove": "a haptic glove: an open hand seen palm-out as a solid silhouette with five straight fingers of equal width and chamfered tips, the wrist cuff joined to the palm, with two small nested chevron signal marks (angular V shapes) radiating upward from the tip of the index finger, " + ARMS + "; no other marks",
    "funding": "funding: a money bag drawn as a heavy hollow outline built only from straight segments: a wide octagonal body, a narrow tied neck with two short tie ends at the top, and a small solid hexagonal coin in the centre of the body; the outline " + ARMS + "; no text, no currency symbol, no thin lines",
    "camera-vision": "a machine vision camera seen from the front as a heavy hollow outline: a wide rectangular body with chamfered corners, a large octagonal lens ring in the centre with a smaller hollow octagon inside it, and a small solid rectangular bump on the top edge; all strokes " + ARMS + "; no thin lines",
}
ROUND4_NAMES = ",".join(ALT_E)

if __name__ == "__main__":
    write("alt-E.json", ALT_E)
    write("alt-F.json", ALT_F)
    print("round 4:", ROUND4_NAMES)
