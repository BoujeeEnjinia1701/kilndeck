"""KilnDeck sizing and first-principles checks (KND-CAL-001).

Run from the repo root:  python docs/04-calcs/sizing.py
Every number in docs/04-calcs/01-sizing.md is printed here. Geometry comes from PARAMS and levels()
in cad/src/model.py; masses come from the model solids; prices come from bom/bom.csv. All values are
first-principles estimates for a design that has not been built. Nothing here is measured.
"""
import csv
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / "cad/src"), str(ROOT / ".kit")]
import model as M  # noqa: E402

P = M.PARAMS
L = M.levels()
G = 9.81
E = 210000.0          # MPa, steel
FY = 275.0            # MPa, S275

# ----------------------------------------------------------------- 1. assumptions
A = dict(
    bricks_day=30000,            # midpoint of 20,000 to 50,000 a day (Greentech, 2014)
    brick_kg=3.0,                # fired brick 230 x 115 x 75 mm at about 1.5 kg/L
    sec_mj_kg=1.2,               # specific energy, MJ per kg of fired brick (assumption)
    coal_mj_kg=22.0,             # coal gross calorific value (assumption)
    round_min=17.5,              # feeding every 15 to 20 min (Greentech, 2014)
    firemen=2,                   # two firemen feed at a time (Greentech, 2014)
    coal_bulk=0.80,              # kg/L, crushed coal
    biomass_bulk=0.25,           # kg/L, chopped biomass such as stalks or husk (assumption)
    fill=0.80,                   # fraction of a rotor pocket that fills from the hopper
    holes_per_round=18,          # holes one fireman feeds per round: 3 rows of 6 (assumption)
    hole_pitch=1000.0,           # feed holes 1.0 m apart along and across the kiln (assumption)
    hole_d=150.0,                # feed hole diameter (assumption)
    person_kg=100.0,             # fireman with clothing and tools
    rated_kg=250.0,              # R3 rated load
    dyn=1.25,                    # dynamic factor on live load (walking, shovelling)
    crust_c=150.0, crust_hot_c=250.0,   # crust surface temperature, nominal and hot spot (assumption)
    amb_c=45.0, night_c=30.0,    # air temperature, summer day and night
    sun=1000.0,                  # W/m2, midday summer sun on a level surface
    roll=0.02,                   # rolling resistance, ball-bearing wheels on a dusty round bar
    mu_lock=0.15,                # steel wheel locked and sliding on a dusty steel bar
    chain_eff=0.85,
    wall_limit_mpa=0.20,         # interim bearing limit on an old brick wall top until the survey
)


def shs(b, t, h=None):
    """Area (mm2), second moment (mm4) and elastic modulus (mm3) of a hollow section, sharp corners."""
    h = h or b
    a = b * h - (b - 2 * t) * (h - 2 * t)
    i = (b * h ** 3 - (b - 2 * t) * (h - 2 * t) ** 3) / 12
    return a, i, i / (h / 2)


def angle_props(a, t):
    """Equal angle about its own horizontal centroidal axis (approximate)."""
    area = t * (2 * a - t)
    yc = (t * a * a / 2 + (a - t) * t * t / 2) / area
    i = t * a ** 3 / 12 + t * a * (a / 2 - yc) ** 2 + (a - t) * t ** 3 / 12 + (a - t) * t * (t / 2 - yc) ** 2
    return area, i, i / (a - yc)


def fuel():
    day_kg = A["bricks_day"] * A["brick_kg"] * A["sec_mj_kg"] / A["coal_mj_kg"]
    rounds = 24 * 60 / A["round_min"]
    per_round = day_kg / rounds
    per_fireman = per_round / A["firemen"]
    per_hole = per_fireman / A["holes_per_round"]
    return dict(day_kg=day_kg, rounds=rounds, per_round=per_round, per_fireman=per_fireman, per_hole=per_hole)


def hopper():
    tx, ty = P["HOPPER_TOP"]
    ox, oy = P["HOPPER_OUT"]
    t = P["HOPPER_T"]
    a1 = (tx - 2 * t) * (ty - 2 * t)
    a2 = (ox - 2 * t) * (oy - 2 * t)
    h = P["HOPPER_TAPER"]
    v_taper = h / 3 * (a1 + a2 + math.sqrt(a1 * a2))
    v_straight = a1 * (P["HOPPER_STRAIGHT"] - 25)     # 25 mm below the grille kept clear
    v = (v_taper + v_straight) / 1e6
    return dict(litres=v, coal_kg=v * A["coal_bulk"], biomass_kg=v * A["biomass_bulk"])


def rotor():
    D, Lr, n, hub, vane = P["ROTOR"]
    area = math.pi / 4 * (D ** 2 - hub ** 2) - n * vane * (D - hub) / 2
    v_turn = area * (Lr - 18) / 1e6           # less the two 6 mm end discs and 3 mm clearances
    v_pocket = v_turn / n
    f = fuel()
    kg_pocket = v_pocket * A["fill"] * A["coal_bulk"]
    return dict(v_turn=v_turn, v_pocket=v_pocket, kg_pocket=kg_pocket, kg_turn=kg_pocket * n,
                bio_pocket=v_pocket * A["fill"] * A["biomass_bulk"], pockets_per_hole=f["per_hole"] / kg_pocket,
                lump_max=min((D - hub) / 2 - 10, 40.0), grille=P["GRILLE_PITCH"] - 6)


def masses():
    comps = M.assembly()
    m = M.masses(comps)
    deck = sum(m[k] for k in M.deck_keys())
    carriage = sum(m[k] for k in M.carriage_keys())
    track = sum(m[k] for k in M.track_keys())
    trucks = m["truck_out"] + m["truck_in"] + m["wheels"]
    return dict(per=m, deck=deck, carriage=carriage, track=track, trucks=trucks, span_self=deck - trucks,
                modules=M.module_masses())


def bridge(ms):
    """Each side truss as a simply supported beam over the track gauge."""
    span = P["GAUGE"]
    h = (L["top_rail0"] + L["top_rail1"]) / 2 - (L["chord0"] + L["chord1"]) / 2
    ac, ic, zc = shs(*P["CHORD"])
    I = 2 * (ac * (h / 2) ** 2 + ic)
    hopper_kg = ms["carriage"] + hopper()["coal_kg"]
    w_self = ms["span_self"] * G / 2 / span                 # N/mm per truss (self weight shared)
    # truss B: half the self weight, the carriage with a full hopper at mid-span and half the fireman
    pB = (hopper_kg + A["person_kg"] / 2) * G * A["dyn"]
    pA = (A["person_kg"] / 2) * G * A["dyn"]
    out = {}
    for name, pp in (("A", pA), ("B", pB)):
        Mmax = w_self * span ** 2 / 8 + pp * span / 4
        F = Mmax / h
        d = 5 * w_self * span ** 4 / (384 * E * I) + pp * span ** 3 / (48 * E * I)
        out[name] = dict(P=pp, M=Mmax / 1e6, F=F, sigma=F / ac, defl=d * 1.3)     # x1.3 for truss shear deformation
    # top chord buckling between U-frames at the splices
    Lb = P["BRIDGE_L"] / P["MODULES"]
    pcr = math.pi ** 2 * E * ic / Lb ** 2
    # rated-load proof (R3): 1.5 x 250 kg at mid-span on truss B, static, with the carriage and its full hopper
    # also at mid-span (independent review of 2026-10-29: the carriage had been left out of the proof case)
    pp = 1.5 * A["rated_kg"] * G + hopper_kg * G
    Mp = w_self * span ** 2 / 8 + pp * span / 4
    proof = dict(P=pp, M=Mp / 1e6, sigma=Mp / h / ac)
    # splice bolts at mid-span: chord force carried by two M12 bolts through the verticals next to each chord
    bolt_t = out["B"]["F"] / 2
    return dict(h=h, I=I, span=span, out=out, pcr=pcr, Lb=Lb, ratio=out["B"]["F"] / pcr, proof=proof, bolt_t=bolt_t,
                w_self=w_self, hopper_kg=hopper_kg)


def guardrail():
    F = 1000.0
    ac, ic, zc = shs(*P["CHORD"])
    av, iv, zv = shs(*P["VERT"])
    Lm = P["BRIDGE_L"] / P["MODULES"] - 2 * P["VERT"][0]
    m_mid = F * Lm / 4
    lever = L["top_rail1"] - L["chord1"]
    m_post = F * lever
    s_mid, s_post = m_mid / zc, m_post / (2 * zv)
    # the moment at the foot of a post goes into the frame bearer through its bolted end plate: a column of three M12
    # at 20, 50 and 80 mm above the plate's lower edge (the pivot) under each vertical; one column at the deck ends,
    # two at a splice (KND-DEC-001 D13). Elastic bolt group: top bolt carries M x 80 / sum(d^2)
    ds = [r - P["CLEAT_Z0"] for r in (210.0, 240.0, 270.0)]
    bolt_t = m_post * max(ds) / sum(d * d for d in ds)
    bolt_t_splice = bolt_t / 2
    # the frame bearer takes the post moment as an end moment (U-frame), RHS 60 x 40 x 4 upright
    hb, wb_, tb_ = P["FRAME_BEARER"]
    _, ib, zb_ = shs(wb_, tb_, hb)
    s_bearer = m_post / zb_
    # at the bridge ends the truss end vertical (40 x 40 x 4) and the end rail or gate post (40 x 40 x 3)
    # are bolted side by side and bend together
    ae, ie, ze = shs(40.0, 3.0)
    s_end = m_post / (zv + ze)
    defl = F * lever ** 3 / (3 * E * 2 * iv)
    return dict(F=F, Lm=Lm, s_mid=s_mid, s_post=s_post, s_end=s_end, bolt_t=bolt_t, bolt_t_splice=bolt_t_splice, lever=lever, defl=defl,
                s_bearer=s_bearer, proof=1.5)


def floor_panel():
    a, at = P["PANEL_ANGLE"]
    area, i, z = angle_props(a, at)
    y0, y1 = M.panel_bounds()[1]
    span = y1 - y0
    F = 1.5 * A["person_kg"] * G         # heel load, one person at 1.5 x
    m = F * span / 4
    s = m / (2 * z)
    d = F * span ** 3 / (48 * E * 2 * i)
    heel = F / (60 * 60)                  # MPa on the board under a 60 mm square heel spread by the 2 mm sheet
    return dict(span=span, F=F, s=s, d=d, heel=heel)


def wheels(ms):
    """Wheel loads with the carriage full, at its outer travel limit on side B, and the fireman beside it."""
    span = P["GAUGE"]
    wb = P["WHEELBASE"] / 2
    W_self = (ms["deck"]) * G
    car = (ms["carriage"] + hopper()["coal_kg"]) * G
    per = A["person_kg"] * G
    c = P["CARRIAGE_LIMIT"]
    g = M.carriage_frame_geometry()
    # end reactions (across the trench), then the split between the two wheels of that end truck from the
    # moment of the loads about the deck centre line (the carriage hangs outside side B)
    loads = {}
    for end in (-1, 1):
        frac = 0.5 + c / span                   # the carriage and the fireman at the end of travel nearest this truck
        live = (car + per) * A["dyn"] * frac
        R = W_self / 2 + live
        mx = (car * g["hcx"] + per * P["TRUSS_X"]) * A["dyn"] * frac
        loads[end] = (R / 2 + mx / (2 * wb), R)
    Wmax = max(v[0] for v in loads.values())
    # the same case with the 250 kg rated load (R3) in place of the 100 kg fireman, for the wheel rating and the pads
    # (independent review of 2026-10-29)
    rated = []
    for end in (-1, 1):
        frac = 0.5 + c / span
        live_r = (car + A["rated_kg"] * G) * A["dyn"] * frac
        R_r = W_self / 2 + live_r
        mx_r = (car * g["hcx"] + A["rated_kg"] * G * P["TRUSS_X"]) * A["dyn"] * frac
        rated.append(R_r / 2 + mx_r / (2 * wb))
    Wrated = max(rated)
    # track channel between pads: weak axis of UPN 80 lying flanges down (handbook Iy, Wy) plus the bar
    Iy, Wy = 19.4e4, 6.36e3
    pitch = P["PAD_PITCH"]
    m = Wmax * pitch / 4
    s = m / Wy
    d = Wmax * pitch ** 3 / (48 * E * Iy)
    pad = P["PAD"][0] * P["PAD"][1]
    track_kg_m = ms["per"]["track"] / (2 * P["TRACK_N"] * P["TRACK_LEN"] / 1000)
    R_pad = Wmax + track_kg_m * G * pitch / 1000
    pmpa = R_pad / pad
    pmpa_rated = (Wrated + track_kg_m * G * pitch / 1000) / pad
    # stability across the kiln: tipping about the side B wheel line
    restoring = W_self * wb
    overturn = (car * (g["hcx"] - wb) + per * 0.0) * A["dyn"]
    return dict(Wmax=Wmax, Wkg=Wmax / G, Wrated=Wrated, Wrated_kg=Wrated / G, pmpa_rated=pmpa_rated, s=s, d=d, R_pad=R_pad, pmpa=pmpa, restoring=restoring / 1e6,
                overturn=overturn / 1e6, wall_kn_m=2 * Wmax / P["WHEELBASE"] / 1.0)


def travel(ms):
    W = (ms["deck"] + ms["carriage"] + hopper()["coal_kg"] + A["person_kg"]) * G
    Fr = A["roll"] * W
    r_t = M.levels()["r_tread"]
    r_h = P["HANDWHEEL"][0] / 2
    hand = Fr * r_t / r_h / A["chain_eff"]
    per_turn = 2 * math.pi * r_t
    step = per_turn / 12                    # 12 lock holes in the hand wheel rim
    grade = 0.05 * W
    # half the weight sits on the two driven wheels, locked by the pin
    hold = A["mu_lock"] * W / 2
    hold_lo = 0.10 * W / 2                  # friction 0.10 (very dusty or oily bar): independent review of 2026-10-29
    hand_grade = (Fr + 0.02 * W) * r_t / r_h / A["chain_eff"]
    T = Fr * r_t
    tau = 16 * T / (math.pi * P["SHAFT"][0] ** 3)
    # carriage push along its rail
    car = (ms["carriage"] + hopper()["coal_kg"]) * G
    push_car = 0.03 * car
    return dict(W=W, Fr=Fr, hand=hand, per_turn=per_turn, step=step, grade=grade, hold=hold, hold_lo=hold_lo, hand_grade=hand_grade,
                tau=tau, push_car=push_car)


def floor_temp(t_crust, t_air, sun, eps_under=0.3, alpha=0.5, label=""):
    """Steady heat balance through one square metre of floor panel. The crust radiates to the aluminium
    underside (emissivity eps_under when dusty); hot air under the deck heats it by convection; the
    board conducts; the top sheet takes the sun and loses heat to the air and the sky."""
    sb = 5.67e-8
    k, tb = 0.065, P["PANEL_ANGLE"][0] - 3
    Rb = tb / 1000 / k
    e_eff = 1 / (1 / 0.9 + 1 / eps_under - 1)
    h_under, t_under_air = 5.0, (t_crust + t_air) / 2
    h_top, eps_top = 10.0, 0.9
    T = lambda c: c + 273.15   # noqa: E731

    def q_out(tt):
        return h_top * (tt - t_air) + eps_top * sb * (T(tt) ** 4 - T(t_air - 10) ** 4) - alpha * sun

    def resid(tt):
        q = q_out(tt)
        tu = tt + q * Rb
        q_in = e_eff * sb * (T(t_crust) ** 4 - T(tu) ** 4) + h_under * (t_under_air - tu)
        return q_in - q

    lo, hi = t_air - 30, t_crust + 50
    for _ in range(100):
        mid = (lo + hi) / 2
        if resid(mid) > 0:
            lo = mid
        else:
            hi = mid
    tt = (lo + hi) / 2
    return dict(label=label, top=tt, under=tt + q_out(tt) * Rb, q=q_out(tt), bare=t_crust)


def alignment():
    tv = travel(masses_cache())
    chain_play = 5.0
    skew = 0.5 * P["GAUGE"] * (P["WHEEL_IN_GROOVE"] - P["BAR_D"]) / 2 / P["GAUGE"]
    x_err = tv["step"] / 2 + chain_play
    return dict(x_err=x_err, y_err=10.0, spout=P["SPOUT"][0], hole=A["hole_d"], ok=max(x_err, 10.0) <= 25.0)


_MS = None


def masses_cache():
    global _MS
    if _MS is None:
        _MS = masses()
    return _MS


def thermal_track():
    dT = 100.0
    dl = 12e-6 * P["TRACK_LEN"] * dT
    span_dl = 12e-6 * P["GAUGE"] * 60.0
    float_ = (P["WHEEL_IN_GROOVE"] - P["BAR_D"]) / 2
    return dict(dl=dl, gap=P["TRACK_GAP"], span_dl=span_dl, float_=float_)


def bom_total():
    rows = list(csv.DictReader((ROOT / "bom/bom.csv").open()))
    tot = sum(float(r["qty"]) * float(r["unit_cost_usd"]) for r in rows)
    import yaml
    bud = float(yaml.safe_load((ROOT / "project.yaml").read_text())["budget_usd"])
    return dict(n=len(rows), total=tot, budget=bud, diff=tot - bud)


# ----------------------------------------------------------------- 15. wind (STEM check S20, KND-DEC-001 D12)
W_ASSUME = dict(rho_air=1.2, cf=2.0, gust_storm=28.0, gust_typical=17.0, mu_pad=0.4, mu_clamp=0.3, clamp_hand_n=100.0,
                tommy_l=120.0, k_nut=0.2, clamp_d=16.0, chain_wll_kn=19.6)   # 8 mm grade 80 chain, working load limit 2,000 kg (EN 818-2)


def wind_area():
    """Area of the deck that faces a wind blowing along the kiln (m2) and its centroid height (mm above the wall top).
    Both trusses counted in full (no shielding of the leeward truss: conservative); members as flat plates."""
    cw, vw, dw = P["CHORD"][0], P["VERT"][0], P["DIAG"][0]
    Lm = P["BRIDGE_L"] / P["MODULES"]
    hv = L["top_rail0"] - L["chord1"]
    toe_h = L["floor"] + P["TOE"][0] - L["chord1"]
    items = [  # (area mm2, centroid z)
        (2 * cw * Lm / 2, (L["chord0"] + L["chord1"]) / 2), (2 * cw * Lm / 2, (L["top_rail0"] + L["top_rail1"]) / 2),
        (2 * vw * hv, (L["chord1"] + L["top_rail0"]) / 2), (dw * math.hypot(Lm - 2 * vw, hv), (L["chord1"] + L["top_rail0"]) / 2),
        (dw * (Lm - 2 * vw), L["knee"]), (toe_h * (Lm - 2 * vw - 50), L["chord1"] + toe_h / 2)]
    a_mod = sum(a for a, _ in items)
    m_mod = sum(a * z for a, z in items)
    g = M.carriage_frame_geometry()
    extra = [(2 * P["MODULES"] * 0 + P["BRIDGE_L"] * (L["floor"] - L["chord1"]), (L["chord1"] + L["floor"]) / 2),      # floor panel edges
             (P["BRIDGE_L"] * 40.0, (L["crail0"] + L["crail1"]) / 2),                                                # carriage rail
             (P["HOPPER_TOP"][1] * (g["hop_top"] - g["out_z"]), (g["hop_top"] + g["out_z"]) / 2),                    # hopper side
             (4 * 40.0 * (L["top_rail1"] - L["chord1"]), (L["chord1"] + L["top_rail1"]) / 2),                        # end posts
             (2 * P["TRUCK"][1] * P["TRUCK"][0] + 4 * P["WHEEL"][1] * P["WHEEL"][0], L["wheel_c"])]                  # trucks, wheels
    A = 2 * P["MODULES"] * a_mod + sum(a for a, _ in extra)
    Mz = 2 * P["MODULES"] * m_mod + sum(a * z for a, z in extra)
    return dict(A=A / 1e6, zc=Mz / A)


def wind(ms):
    wa = wind_area()
    k = 0.5 * W_ASSUME["rho_air"] * W_ASSUME["cf"] * wa["A"]          # N per (m/s)^2
    F = lambda v: k * v * v                                            # noqa: E731
    v_at = lambda f: math.sqrt(f / k)                                  # noqa: E731
    tv = travel(ms)
    r_t, r_h = M.levels()["r_tread"], P["HANDWHEEL"][0] / 2
    f_move = 200.0 * r_h * A["chain_eff"] / r_t - tv["Fr"]            # wind force that uses up the 200 N rim force (R4)
    W_empty = (ms["deck"] + ms["carriage"]) * G
    lever = wa["zc"] - L["rail_top"]
    f_tip = W_empty * (P["WHEELBASE"] / 2) / lever
    vs = W_ASSUME["gust_storm"]
    Fs = F(vs)
    # storm clamps: tommy bar couple, nut factor, two faces in friction per clamp, four clamps
    T = W_ASSUME["clamp_hand_n"] * W_ASSUME["tommy_l"] / 1000.0
    pre = T / (W_ASSUME["k_nut"] * W_ASSUME["clamp_d"] / 1000.0)
    clamp = 4 * 2 * W_ASSUME["mu_clamp"] * pre
    # the clamped deck and both 12 m track runs sliding together on the pads
    slide = (ms["deck"] + ms["carriage"] + ms["track"]) * G * W_ASSUME["mu_pad"]
    # tie-down chains: lug on the beam end to a ground anchor 1.5 m along and 1.2 m outboard, 0.33 m below the lug
    p0 = (685.0, 3300.0, L["truck1"] + 40)
    anc = (1500.0, 4500.0, 0.0)
    Lc = math.dist(p0, anc)
    ux, uz = (anc[0] - p0[0]) / Lc, (p0[2] - anc[2]) / Lc
    t_chain = Fs / (2 * ux)                       # two chains (one per truck) resist each direction along the kiln
    rest = W_empty * P["WHEELBASE"] / 2 + 2 * t_chain * uz * (p0[0] + P["WHEELBASE"] / 2) + 2 * t_chain * ux * (p0[2] - L["rail_top"])
    over = Fs * lever
    # capacity with the chains alone (the clamps and pads are not counted): two chains resist each direction
    cap_chain = 2 * W_ASSUME["chain_wll_kn"] * 1000 * ux
    v_chain = math.sqrt(cap_chain / k)
    return dict(A=wa["A"], zc=wa["zc"], k=k, v_roll=v_at(tv["Fr"]), v_lock=v_at(tv["hold"]), v_move=v_at(f_move),
                v_tip=v_at(f_tip), Fs=Fs, F17=F(W_ASSUME["gust_typical"]), clamp=clamp, pre=pre, slide=slide, t_chain=t_chain,
                ux=ux, uz=uz, cap_chain=cap_chain, v_chain=v_chain, rest=rest / 1e6, over=over / 1e6, f_move=f_move, f_tip=f_tip)


# ----------------------------------------------------------------- 16. team handling (STEM check S21, KND-DEC-001 D14)
TEAM = dict(person_kg=25.0, team2=2.0 / 3.0)       # ISO 11228-1 reference mass; HSE L23: a two-person team lifts 2/3 of the sum


def team():
    lim = TEAM["team2"] * 2 * TEAM["person_kg"]
    mm = M.module_masses()
    return dict(limit=lim, pieces=mm, worst=max(mm.values()), worst_name=max(mm, key=mm.get))


# ----------------------------------------------------------------- 17. end stop impact
def end_stop(ms, speed=None):
    tv = travel(ms)
    v = speed if speed is not None else tv["per_turn"] / 1000.0      # one hand wheel turn a second, m/s
    m = tv["W"] / G
    ke = 0.5 * m * v * v
    d = 0.010                                                        # 10 mm rubber face compressed (assumption)
    f = 2 * ke / d / 2                                               # triangular force, shared by the two stops
    # two M12 8.8 bolts in shear at the stop foot: shear capacity about 0.6 x 800 MPa x 84.3 mm2 each
    cap = 2 * 0.6 * 800 * 84.3
    # the track under each stop is held only by friction on its pads: one 12 m run plus half the deck and carriage
    # (independent review of 2026-10-29)
    slide = (ms["track"] / 2 + (ms["deck"] + ms["carriage"]) / 2) * G * W_ASSUME["mu_pad"]
    return dict(v=v, m=m, ke=ke, f=f, cap=cap, cap_f=cap / 1.5, slide=slide)


# ----------------------------------------------------------------- 18. crank torque on the metering rotor (S16)
def crank():
    ox, oy = P["HOPPER_OUT"]
    a = ox * oy / 1e6
    per = 2 * (ox + oy) / 1000.0
    rh = a / per
    mu, kk = 0.5, 0.4                                                # coal on steel; Janssen ratio (assumptions)
    H = (P["HOPPER_TAPER"] + P["HOPPER_STRAIGHT"]) / 1000.0
    p = A["coal_bulk"] * 1000 * G * rh / (mu * kk) * (1 - math.exp(-mu * kk * H / rh))
    F = p * a
    T = mu * F * P["ROTOR"][0] / 2000.0
    hand = T / (P["CRANK_R"] / 1000.0)
    # upper bound with no wall friction relief: the full hydrostatic head on the rotor, rotor friction 0.8
    p_h = A["coal_bulk"] * 1000 * G * H
    hand_h = 0.8 * p_h * a * P["ROTOR"][0] / 2000.0 / (P["CRANK_R"] / 1000.0)
    return dict(p=p, F=F, T=T, hand=hand, p_h=p_h, hand_h=hand_h)


def main():
    f, h, r = fuel(), hopper(), rotor()
    ms = masses_cache()
    print("1 Assumptions")
    for k, v in A.items():
        print(f"  {k} = {v}")
    print(f"  trench {P['TRENCH']:.0f} mm, track centres {P['GAUGE']:.0f} mm; levels {dict((k, round(v)) for k, v in L.items())}")
    print("2 Fuel per round")
    print(f"  coal per day {f['day_kg']:.0f} kg; rounds per day {f['rounds']:.0f}; per round {f['per_round']:.1f} kg; "
          f"per fireman {f['per_fireman']:.1f} kg; per hole {f['per_hole']:.2f} kg")
    print("3 Hopper (R6)")
    print(f"  {h['litres']:.1f} L; {h['coal_kg']:.1f} kg coal; {h['biomass_kg']:.1f} kg biomass; "
          f"rounds per fill (coal) {h['coal_kg'] / f['per_fireman']:.2f}")
    print("4 Metering rotor (R5)")
    print(f"  {r['v_turn']:.2f} L per turn, {r['v_pocket']:.3f} L per pocket; coal {r['kg_pocket']:.2f} kg per pocket, "
          f"{r['kg_turn']:.2f} kg per turn; biomass {r['bio_pocket']:.2f} kg per pocket; {r['pockets_per_hole']:.1f} pockets per hole; "
          f"largest lump about {r['lump_max']:.0f} mm; grille gap {r['grille']:.0f} mm")
    print("5 Masses (kg, from the model)")
    print("  " + ", ".join(f"{k} {v:.1f}" for k, v in ms["per"].items()))
    print(f"  deck {ms['deck']:.0f}; carriage empty {ms['carriage']:.0f}; track and pads (2 x 12 m) {ms['track']:.0f}; "
          f"span (deck less trucks and wheels) {ms['span_self']:.0f}")
    print("  pieces carried up (R12): " + ", ".join(f"{k} {v:.1f}" for k, v in ms["modules"].items()))
    b = bridge(ms)
    print("6 Bridge (R3)")
    print(f"  chord centres {b['h']:.0f} mm; I per truss {b['I'] / 1e4:.0f} cm4; self weight {b['w_self']:.3f} N/mm per truss; "
          f"carriage with full hopper {b['hopper_kg']:.0f} kg")
    for k, v in b["out"].items():
        print(f"  truss {k}: point {v['P']:.0f} N, M {v['M']:.2f} kN m, chord force {v['F'] / 1000:.2f} kN, "
              f"chord stress {v['sigma']:.0f} MPa, deflection {v['defl']:.1f} mm (span/{b['span'] / v['defl']:.0f})")
    print(f"  top chord buckling over {b['Lb']:.0f} mm: {b['pcr'] / 1000:.1f} kN; ratio {b['ratio']:.2f}")
    print(f"  proof 1.5 x 250 kg plus the carriage on truss B: M {b['proof']['M']:.2f} kN m, chord {b['proof']['sigma']:.0f} MPa")
    print(f"  mid-span splice: {b['bolt_t'] / 1000:.2f} kN per M12 bolt (tension)")
    g = guardrail()
    print("7 Guardrail (R2)")
    print(f"  1 kN mid-module (span {g['Lm']:.0f}): top chord {g['s_mid']:.0f} MPa; at a splice (lever {g['lever']:.0f}): "
          f"double post {g['s_post']:.0f} MPa, deflection {g['defl']:.1f} mm; end post pair {g['s_end']:.0f} MPa; "
          f"bearer end-plate top bolt {g['bolt_t'] / 1000:.1f} kN at a deck end, {g['bolt_t_splice'] / 1000:.1f} kN at a splice; "
          f"frame bearer end moment {g['s_bearer']:.0f} MPa; at proof x1.5: {1.5 * g['s_post']:.0f}, {1.5 * g['s_end']:.0f} and {1.5 * g['s_bearer']:.0f} MPa")
    fp = floor_panel()
    print("8 Floor panel")
    print(f"  span {fp['span']:.0f} mm; 1.5 kN heel: edge angles {fp['s']:.0f} MPa, deflection {fp['d']:.1f} mm; "
          f"board under heel {fp['heel']:.2f} MPa")
    w = wheels(ms)
    print("9 Wheels, track and walls (R8)")
    print(f"  worst wheel {w['Wmax']:.0f} N ({w['Wkg']:.0f} kg); track channel between pads {w['s']:.0f} MPa, {w['d']:.2f} mm; "
          f"pad reaction {w['R_pad']:.0f} N, pressure {w['pmpa']:.3f} MPa vs interim limit {A['wall_limit_mpa']:.2f}; "
          f"tipping: restoring {w['restoring']:.2f} kN m vs overturning {w['overturn']:.2f} kN m")
    print(f"  at the 250 kg rated load: worst wheel {w['Wrated']:.0f} N ({w['Wrated_kg']:.0f} kg), pad pressure {w['pmpa_rated']:.3f} MPa")
    t = travel(ms)
    print("10 Travel (R4, R10)")
    print(f"  loaded weight {t['W']:.0f} N; rolling {t['Fr']:.0f} N; hand wheel rim force {t['hand']:.0f} N level, "
          f"{t['hand_grade']:.0f} N on a 2 % grade; {t['per_turn']:.0f} mm per turn, {t['step']:.0f} mm per lock hole; "
          f"5 % grade pull {t['grade']:.0f} N vs locked-wheel hold {t['hold']:.0f} N; line shaft {t['tau']:.1f} MPa; "
          f"carriage push {t['push_car']:.0f} N; hold at friction 0.10: {t['hold_lo']:.0f} N")
    print("11 Floor temperature (R7)")
    for case in ((A["crust_c"], A["night_c"], 0, "night, nominal crust"), (A["crust_c"], A["amb_c"], 0, "summer day, shaded"),
                 (A["crust_c"], A["amb_c"], A["sun"], "summer day, full sun"), (A["crust_hot_c"], A["amb_c"], A["sun"], "hot spot, full sun"),
                 (A["crust_c"], 30.0, A["sun"], "30 C day, full sun")):
        ft = floor_temp(*case[:3], label=case[3])
        print(f"  {ft['label']}: floor top {ft['top']:.0f} C, underside {ft['under']:.0f} C, {ft['q']:.0f} W/m2 through; bare crust {ft['bare']:.0f} C")
    al = alignment()
    print("12 Spout alignment (R9)")
    print(f"  along the kiln +/-{al['x_err']:.0f} mm; across +/-{al['y_err']:.0f} mm; spout {al['spout']:.0f} mm into a {al['hole']:.0f} mm hole")
    tt = thermal_track()
    print("13 Heat movement")
    print(f"  track module {tt['dl']:.1f} mm at +100 K vs {tt['gap']:.0f} mm gap; deck span {tt['span_dl']:.1f} mm at +60 K vs +/-{tt['float_']:.0f} mm float")
    w = wind(ms)
    print("15 Wind along the kiln (S20)")
    print(f"  area facing the wind {w['A']:.2f} m2 (Cf {W_ASSUME['cf']}), centroid {w['zc']:.0f} mm above the wall top; "
          f"force {w['k']:.2f} N per (m/s)^2")
    print(f"  unlocked deck starts to roll at {w['v_roll']:.1f} m/s; locked deck slides at {w['v_lock']:.1f} m/s; "
          f"200 N at the rim is used up at {w['v_move']:.1f} m/s; empty deck tips along the kiln at {w['v_tip']:.1f} m/s")
    print(f"  {W_ASSUME['gust_typical']:.0f} m/s gust: {w['F17']:.0f} N; {W_ASSUME['gust_storm']:.0f} m/s storm gust: {w['Fs']:.0f} N")
    print(f"  storm clamps: preload {w['pre'] / 1000:.2f} kN each, four clamps hold {w['clamp'] / 1000:.1f} kN; deck and track slide on the pads at "
          f"{w['slide'] / 1000:.1f} kN; chain tension {w['t_chain'] / 1000:.1f} kN (x share {w['ux']:.2f}); tipping with chains "
          f"restoring {w['rest']:.1f} kN m vs overturning {w['over']:.1f} kN m")
    print(f"  chain tension {w['t_chain'] / 1000:.1f} kN vs working load limit {W_ASSUME['chain_wll_kn']:.1f} kN "
          f"(ratio {w['t_chain'] / 1000 / W_ASSUME['chain_wll_kn']:.2f}); clamps and chains together {(w['clamp'] + 2 * w['t_chain'] * w['ux']) / 1000:.1f} kN "
          f"against the {w['Fs'] / 1000:.1f} kN storm load; screw anchor pull-out in the kiln yard: to assess")
    print(f"  chains alone (clamps and pads not counted): two chains resist each direction, {w['cap_chain'] / 1000:.1f} kN at their working load limit, "
          f"reached at a {w['v_chain']:.0f} m/s gust; each anchor must resist {w['t_chain'] / 1000:.1f} kN at {W_ASSUME['gust_storm']:.0f} m/s")
    tm = team()
    print("16 Team handling (R12, S21)")
    print(f"  two-person team guide {tm['limit']:.1f} kg; heaviest piece {tm['worst_name']} {tm['worst']:.1f} kg")
    es = end_stop(ms)
    print("17 End stop impact")
    print(f"  {es['m']:.0f} kg at {es['v']:.2f} m/s: {es['ke']:.0f} J; {es['f'] / 1000:.1f} kN per stop over 10 mm of rubber; "
          f"two M12 in shear hold about {es['cap'] / 1000:.0f} kN ({es['cap_f'] / 1000:.0f} kN with a partial factor of 1.5); "
          f"the track under each stop is held by pad friction at about {es['slide'] / 1000:.1f} kN")
    ck = crank()
    print("18 Crank torque (R5)")
    print(f"  Janssen pressure on the rotor {ck['p']:.0f} Pa; {ck['F']:.0f} N on the rotor; friction torque {ck['T']:.1f} N m; "
          f"{ck['hand']:.0f} N at the 140 mm crank; hydrostatic upper bound {ck['p_h']:.0f} Pa, {ck['hand_h']:.0f} N")
    bt = bom_total()
    print("14 Cost (R11)")
    print(f"  bom.csv {bt['n']} lines, USD {bt['total']:.2f}; value-engineering target USD {bt['budget']:.0f}; "
          f"{'over' if bt['diff'] > 0 else 'under'} by USD {abs(bt['diff']):.2f}")


if __name__ == "__main__":
    main()
