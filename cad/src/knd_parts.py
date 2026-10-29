"""KilnDeck repo-specific CAD helpers (kit 1.9). Built on .kit/cad_parts.py; nothing here belongs in .kit/.

Helpers the parts library does not have (suggested kit additions are listed in docs/REVIEW.md):
    frame(origin, x_dir, z_dir)     place a part built in its own axes at any axis-aligned orientation
    hs(w, h, t, L, axis, ...)       a hollow section along X, Y or Z between two coordinates, centred on a line
    rod(d, L, axis, ...)            a round bar along an axis with chamfered ends
    plate(...)                      a flat plate in any of the three planes, with holes and rounded corners
    drill(shape, xyz, axis, dia)    a through hole along an axis
    bolted(d, grip, xyz, toward)    an ISO 4017 bolt, two ISO 7089 washers and an ISO 4032 nut on any axis
    weld(length, leg, xyz, along, leg1, leg2)  a fillet weld bead in an axis-aligned corner
    rivet(d, grip, xyz, toward)     a blind rivet (ISO 15977 style, drawn as shank and head)
    rivnut(d, xyz, toward)          a blind rivet nut set in a thin wall (head on the outer face)
    chain_loop(...)                 a roller chain drawn as its outline loop (pitch line band) between two sprockets
    sprocket(teeth, pitch, xyz, axis)  a plate sprocket drawn with its teeth as a toothed disc
All sizes in millimetres. Bolt sets are cached by size and grip, so a model with hundreds of joints builds quickly.
"""
from __future__ import annotations

import math
import sys
from functools import lru_cache
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(HERE), str(HERE.parents[1] / ".kit")]

from build123d import (Box, Circle, Compound, Cylinder, Location, Plane, Polygon, Pos, Rot, Sketch,  # noqa: E402
                       RectangleRounded, extrude, loft, Rectangle)
import cad_parts as cp  # noqa: E402

AX = {"x": (1, 0, 0), "y": (0, 1, 0), "z": (0, 0, 1)}
DIRS = {"+x": (1, 0, 0), "-x": (-1, 0, 0), "+y": (0, 1, 0), "-y": (0, -1, 0), "+z": (0, 0, 1), "-z": (0, 0, -1)}


def _v(d):
    return DIRS[d] if isinstance(d, str) else tuple(d)


def _cross(a, b):
    return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])


def frame(shape, origin, x_dir, z_dir):
    """Move a shape built in its own axes so its +X points along x_dir and its +Z along z_dir, origin at origin."""
    pl = Plane(origin=tuple(origin), x_dir=_v(x_dir), z_dir=_v(z_dir))
    return pl.location * shape


def z_to(shape, d, origin=(0, 0, 0)):
    """Turn a part built along +Z so that +Z points along d ('+x', '-y', ...), then move it to origin."""
    d = _v(d)
    x = (1, 0, 0) if abs(d[0]) < 0.5 else (0, 1, 0)
    return frame(shape, origin, x, d)


def box(x0, x1, y0, y1, z0, z1):
    return Pos((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2) * Box(x1 - x0, y1 - y0, z1 - z0)


def hs(w, h, t, a0, a1, axis, c1, c2):
    """Hollow section from a0 to a1 along axis ('x', 'y' or 'z'), centred on (c1, c2) in the other two axes in
    order (y, z for x; x, z for y; x, y for z). w is the size along the first of those axes, h along the second."""
    L = a1 - a0
    if axis == "x":
        s = cp.rhs(h, w, t, L)                       # profile X -> -Z after the turn, so pass (h, w)
        return Pos(a0, c1, c2) * Rot(0, 90, 0) * s
    if axis == "y":
        s = cp.rhs(w, h, t, L)
        return Pos(c1, a0, c2) * Rot(-90, 0, 0) * s
    s = cp.rhs(w, h, t, L)
    return Pos(c1, c2, a0) * s


def rod(d, a0, a1, axis, c1, c2, chamfer=0.5):
    """Round bar from a0 to a1 along axis, centred on (c1, c2) as in hs()."""
    s = cp.round_bar(d, a1 - a0, chamfer)
    if axis == "x":
        return Pos(a0, c1, c2) * Rot(0, 90, 0) * s
    if axis == "y":
        return Pos(c1, a0, c2) * Rot(-90, 0, 0) * s
    return Pos(c1, c2, a0) * s


def tube_round(od, t, a0, a1, axis, c1, c2):
    s = cp.round_tube(od, t, a1 - a0)
    if axis == "x":
        return Pos(a0, c1, c2) * Rot(0, 90, 0) * s
    if axis == "y":
        return Pos(c1, a0, c2) * Rot(-90, 0, 0) * s
    return Pos(c1, c2, a0) * s


def plate(normal, x0, x1, y0, y1, z0, z1, holes=(), r=3.0, edge=0.4):
    """Flat plate filling the box (x0..x1, y0..y1, z0..z1), its thickness along normal ('x', 'y' or 'z').
    holes: [(u, v, dia)] in model coordinates of the two in-plane axes (y, z for x; x, z for y; x, y for z)."""
    if normal == "z":
        w, h, t = x1 - x0, y1 - y0, z1 - z0
        cu, cv = (x0 + x1) / 2, (y0 + y1) / 2
        hl = [(u - cu, v - cv, d) for u, v, d in holes]
        return Pos(cu, cv, z0) * cp.sheet(w, h, t, holes=hl, r_corner=min(r, w / 2 - 0.1, h / 2 - 0.1), edge=min(edge, t / 3))
    if normal == "y":
        w, h, t = x1 - x0, z1 - z0, y1 - y0
        cu, cv = (x0 + x1) / 2, (z0 + z1) / 2
        hl = [(u - cu, v - cv, d) for u, v, d in holes]
        s = cp.sheet(w, h, t, holes=hl, r_corner=min(r, w / 2 - 0.1, h / 2 - 0.1), edge=min(edge, t / 3))
        # sheet lies in XY with thickness +Z; turn so its Y becomes Z and its thickness becomes +Y
        return Pos(cu, y0, cv) * Rot(90, 0, 0) * Pos(0, 0, -t) * s
    w, h, t = y1 - y0, z1 - z0, x1 - x0
    cu, cv = (y0 + y1) / 2, (z0 + z1) / 2
    hl = [(u - cu, v - cv, d) for u, v, d in holes]
    s = cp.sheet(w, h, t, holes=hl, r_corner=min(r, w / 2 - 0.1, h / 2 - 0.1), edge=min(edge, t / 3))
    return Pos(x0, cu, cv) * frame(s, (0, 0, 0), (0, 1, 0), (1, 0, 0))


def cyl(r, a0, a1, axis, c1, c2):
    L = a1 - a0
    c = Pos(0, 0, L / 2) * Cylinder(r, L)
    if axis == "x":
        return Pos(a0, c1, c2) * Rot(0, 90, 0) * c
    if axis == "y":
        return Pos(c1, a0, c2) * Rot(-90, 0, 0) * c
    return Pos(c1, c2, a0) * c


def drill(shape, xyz, axis, dia, length=400.0):
    """Subtract a through hole of diameter dia along axis, centred on xyz (both ways)."""
    x, y, z = xyz
    if axis == "x":
        return shape - cyl(dia / 2, x - length / 2, x + length / 2, "x", y, z)
    if axis == "y":
        return shape - cyl(dia / 2, y - length / 2, y + length / 2, "y", x, z)
    return shape - cyl(dia / 2, z - length / 2, z + length / 2, "z", x, y)


@lru_cache(maxsize=None)
def _bolt_set(d, grip):
    return tuple(cp.hex_bolt_set(d, grip))


def bolted(d, grip, xyz, toward, tag="", bom=None, group="fixings", explode=(0, 0, 0), material="zinc_plated"):
    """Bolt, two washers and nut clamping a joint 'grip' thick. xyz is the point on the head-side face of the
    joint where the bolt enters; toward is the direction the shank points into the joint ('+x', '-z', ...).
    Returns cad_parts.part() dicts of kind 'fastener'."""
    up = tuple(-c for c in _v(toward))
    out = []
    for name, s in _bolt_set(d, round(grip, 1)):
        out.append(cp.part(f"{name}{tag}", z_to(s, up, xyz), material, kind="fastener", bom=bom, group=group, explode=explode))
    return out


def weld(length, leg, xyz, along, leg1, leg2, tag="", group="welds", explode=(0, 0, 0)):
    """Fillet weld bead of the given leg from xyz for 'length' along 'along', its legs lying along leg1 and leg2
    (the two faces of the corner). Returns a cad_parts.part() dict of kind 'weld'."""
    a, b, c = _v(along), _v(leg1), _v(leg2)
    if _cross(a, b) != c:       # the bead is symmetric in its legs: swap them to keep a right-handed frame
        b, c = c, b
    s = frame(_bead(round(length, 2), leg), xyz, a, c)
    return cp.part(f"Fillet weld {leg:.0f} mm{tag}", s, "mild_steel", kind="weld", group=group, explode=explode)


@lru_cache(maxsize=None)
def _bead(length, leg):
    return cp.weld_fillet(length, leg)


def ring_weld(r, leg, xyz, axis, tag="", group="welds"):
    """Fillet weld round a tube or bar of radius r where it meets a face square to axis; legs on the face and the tube."""
    tri = Polygon((r, 0), (r + leg, 0), (r, leg), align=None)
    from build123d import revolve, Axis, Plane as Pl
    sk = Pl.XZ * tri
    bead = revolve(sk, Axis.Z)
    d = {"x": "+x", "y": "+y", "z": "+z", "-x": "-x", "-y": "-y", "-z": "-z"}[axis]
    return cp.part(f"Fillet weld {leg:.0f} mm{tag}", z_to(bead, d, xyz), "mild_steel", kind="weld", group=group)


def rivet(d, grip, xyz, toward, tag="", group="fixings"):
    """Blind rivet: a domed head on the entry face and a shank through the grip (the set tail drawn as a short collar)."""
    head = Pos(0, 0, d * 0.35) * Cylinder(d, d * 0.7)
    head = cp.break_edges(head, d * 0.2)
    shank = Pos(0, 0, -grip / 2) * Cylinder(d / 2, grip)
    tail = Pos(0, 0, -grip - d * 0.4) * Cylinder(d * 0.75, d * 0.8)
    up = tuple(-c for c in _v(toward))
    return cp.part(f"{d:.1f} mm blind rivet{tag}", z_to(head + shank + tail, up, xyz), "aluminium", kind="fastener", group=group)


def rivnut(d, wall, xyz, toward, tag="", group="fixings"):
    """Blind rivet nut set in a thin wall: thin flange on the entry face, knurled body below it (drawn plain)."""
    fl = Pos(0, 0, 0.75) * (Cylinder(d * 0.9, 1.5) - Cylinder(d / 2, 1.6))
    body = Pos(0, 0, -(wall + 8) / 2) * (Cylinder(d * 0.6, wall + 8) - Cylinder(d / 2, wall + 8.2))
    up = tuple(-c for c in _v(toward))
    return cp.part(f"M{d:.0f} blind rivet nut{tag}", z_to(fl + body, up, xyz), "zinc_plated", kind="fastener", group=group)


def sprocket(teeth, pitch, width, bore, xyz, axis, hub=None):
    """Plate sprocket for ISO 606 roller chain, its teeth drawn as a toothed outline, centred on xyz along axis.
    Returns (shape, pitch diameter)."""
    pd = pitch / math.sin(math.pi / teeth)
    ro, ri = pd / 2 + 0.3 * pitch, pd / 2 - 0.35 * pitch
    pts = []
    for k in range(teeth):
        a0 = 2 * math.pi * k / teeth
        for frac, r in ((0.0, ri), (0.3, ro), (0.7, ro)):
            a = a0 + frac * 2 * math.pi / teeth
            pts.append((r * math.cos(a), r * math.sin(a)))
    disc = extrude(Polygon(*pts, align=None), width) - Pos(0, 0, width / 2) * Cylinder(bore / 2, width + 2)
    disc = Pos(0, 0, -width / 2) * disc
    if hub:
        disc = disc + (Pos(0, 0, width / 2 + hub[1] / 2) * (Cylinder(hub[0] / 2, hub[1]) - Cylinder(bore / 2, hub[1] + 1)))
    d = {"x": "+x", "y": "+y", "z": "+z"}[axis]
    return z_to(disc, d, xyz), pd


def chain_loop(pd_a, pd_b, ca, cb, width, plane_axis):
    """Roller chain between two sprockets drawn as a band 8 mm deep round both pitch circles (its outline), in the plane
    square to plane_axis through points ca and cb (two of their coordinates differ)."""
    ra, rb = pd_a / 2, pd_b / 2
    band = 8.0
    # build in local XY: centre a at origin, centre b along +X at distance L
    if plane_axis == "y":
        dx, dz = cb[0] - ca[0], cb[2] - ca[2]
        L = math.hypot(dx, dz)
        ang = math.degrees(math.atan2(dz, dx))
    elif plane_axis == "x":
        dx, dz = cb[1] - ca[1], cb[2] - ca[2]
        L = math.hypot(dx, dz)
        ang = math.degrees(math.atan2(dz, dx))
    else:
        raise ValueError("plane_axis must be 'x' or 'y'")
    r = max(ra, rb)
    outer = Sketch() + Pos(L / 2, 0) * Rectangle(L, 2 * (r + band / 2)) + Circle(ra + band / 2) + Pos(L, 0) * Circle(rb + band / 2)
    inner = Sketch() + Pos(L / 2, 0) * Rectangle(L, 2 * (r - band / 2)) + Circle(ra - band / 2) + Pos(L, 0) * Circle(rb - band / 2)
    s = Pos(0, 0, -width / 2) * extrude(outer - inner, width)
    c, sn = math.cos(math.radians(ang)), math.sin(math.radians(ang))
    if plane_axis == "y":
        return frame(s, ca, (c, 0, sn), (0, 1, 0))
    return frame(s, ca, (0, c, sn), (1, 0, 0))


def lofted_shell(bot, top, z0, z1, t):
    """Hollow frustum of sheet t thick between a rectangle bot (x0, x1, y0, y1) at z0 and top at z1."""
    def rect(r, z, off):
        x0, x1, y0, y1 = r
        return Plane.XY.offset(z) * Pos((x0 + x1) / 2, (y0 + y1) / 2) * Rectangle(x1 - x0 - 2 * off, y1 - y0 - 2 * off)
    outer = loft([rect(bot, z0, 0), rect(top, z1, 0)])
    inner = loft([rect(bot, z0 - 0.5, t), rect(top, z1 + 0.5, t)])
    return outer - inner
