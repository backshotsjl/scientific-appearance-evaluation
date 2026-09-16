#!/usr/bin/env python3
"""Weighted photo scores from rater items. Not a face-measurement model."""

from __future__ import annotations

import argparse
import json
import sys

CRAFT = {
    "face_share": 1.4,
    "lighting": 1.3,
    "sharpness": 1.1,
    "eyes_visible": 1.4,
    "solo": 1.2,
    "background": 0.8,
    "expression_app": 1.0,
    "variety_role": 0.6,
}

SIGNAL = {
    "symmetry": 0.7,
    "skin": 1.1,
    "adiposity": 1.0,
    "grooming": 1.2,
    "dimorph": 0.8,
    "health_color": 1.0,
}

SLOT1_WEIGHTS = {
    "face_share": 1.2,
    "lighting": 1.6,
    "sharpness": 1.1,
    "eyes_visible": 1.6,
    "solo": 1.3,
}


def clamp(n: int) -> int:
    return max(1, min(5, n))


def weighted(vals: dict[str, int], weights: dict[str, float]) -> float:
    num = sum(vals[k] * w for k, w in weights.items())
    den = sum(5 * w for w in weights.values())
    return 10.0 * num / den


def band(score: float) -> str:
    if score >= 8:
        return "strong"
    if score >= 6:
        return "usable"
    if score >= 4:
        return "leaving_points"
    return "replace"


def gaps(vals: dict[str, int], weights: dict[str, float]) -> list[dict]:
    rows = []
    for k, w in weights.items():
        lost = (5 - vals[k]) * w
        rows.append({"item": k, "score": vals[k], "weight": w, "points_lost": round(lost, 2)})
    rows.sort(key=lambda r: r["points_lost"], reverse=True)
    return rows


def slot1_score(craft: dict[str, int]) -> float:
    s = weighted({k: craft[k] for k in SLOT1_WEIGHTS}, SLOT1_WEIGHTS)
    if craft["solo"] <= 2 or craft["eyes_visible"] <= 2 or craft["face_share"] <= 2:
        s = min(s, 4.5)
    if craft["lighting"] <= 2:
        s = min(s, 6.2)
    return round(s, 2)


def pack(presentation: str, slot: int, label: str, craft: dict[str, int], signal: dict[str, int]) -> dict:
    craft_10 = round(weighted(craft, CRAFT), 2)
    signal_10 = round(weighted(signal, SIGNAL), 2)
    slot1 = slot1_score(craft)
    grid_value = round(0.45 * craft_10 + 0.25 * signal_10 + 0.30 * craft["variety_role"] * 2, 2)
    blockers = []
    if craft["eyes_visible"] <= 2:
        blockers.append("eyes_hidden")
    if craft["solo"] <= 2:
        blockers.append("group_or_crowd")
    if craft["sharpness"] <= 2:
        blockers.append("soft_or_blur")
    if craft["lighting"] <= 2:
        blockers.append("bad_light")
    if slot == 1 and slot1 < 7:
        blockers.append("not_slot1")
    craft_gaps = gaps(craft, CRAFT)
    signal_gaps = gaps(signal, SIGNAL)
    fixes = [r["item"] for r in craft_gaps + signal_gaps if r["points_lost"] >= 1.0][:3]
    return {
        "ok": True,
        "label": label,
        "presentation": presentation,
        "slot_hint": slot,
        "craft_10": craft_10,
        "signal_10": signal_10,
        "craft_band": band(craft_10),
        "signal_band": band(signal_10),
        "slot1_suitability": slot1,
        "grid_value": grid_value,
        "blockers": blockers,
        "top_fixes": fixes,
        "craft_gaps": craft_gaps,
        "signal_gaps": signal_gaps,
        "items": {**craft, **signal},
        "beauty_10": signal_10,
        "beauty_band": band(signal_10),
        "note": "Rater-weighted heuristic. Not a lab measurement.",
    }


def parse_project(pairs: list[str], craft: dict[str, int], signal: dict[str, int]) -> tuple[dict[str, int], dict[str, int]]:
    alias = {
        "face-share": "face_share",
        "eyes-visible": "eyes_visible",
        "expression-app": "expression_app",
        "variety-role": "variety_role",
        "health-color": "health_color",
    }
    c, s = dict(craft), dict(signal)
    for raw in pairs:
        if "=" not in raw:
            continue
        k, v = raw.split("=", 1)
        key = alias.get(k.replace("_", "-"), k).replace("-", "_")
        if key in c:
            c[key] = clamp(int(v))
        elif key in s:
            s[key] = clamp(int(v))
    return c, s


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--presentation", choices=("femme", "masc", "neutral"), default="neutral")
    p.add_argument("--slot", type=int, default=0)
    p.add_argument("--label", default="")
    p.add_argument("--face-share", type=int, required=True)
    p.add_argument("--lighting", type=int, required=True)
    p.add_argument("--sharpness", type=int, required=True)
    p.add_argument("--eyes-visible", type=int, required=True)
    p.add_argument("--solo", type=int, required=True)
    p.add_argument("--background", type=int, required=True)
    p.add_argument("--expression-app", type=int, required=True)
    p.add_argument("--variety-role", type=int, required=True)
    p.add_argument("--symmetry", type=int, required=True)
    p.add_argument("--skin", type=int, required=True)
    p.add_argument("--adiposity", type=int, required=True)
    p.add_argument("--grooming", type=int, required=True)
    p.add_argument("--dimorph", type=int, required=True)
    p.add_argument("--health-color", type=int, required=True)
    p.add_argument("--project", action="append", default=[], help="item=5 after a reshoot")
    p.add_argument("--beauty-only", action="store_true")
    args = p.parse_args()

    craft = {
        "face_share": clamp(args.face_share),
        "lighting": clamp(args.lighting),
        "sharpness": clamp(args.sharpness),
        "eyes_visible": clamp(args.eyes_visible),
        "solo": clamp(args.solo),
        "background": clamp(args.background),
        "expression_app": clamp(args.expression_app),
        "variety_role": clamp(args.variety_role),
    }
    signal = {
        "symmetry": clamp(args.symmetry),
        "skin": clamp(args.skin),
        "adiposity": clamp(args.adiposity),
        "grooming": clamp(args.grooming),
        "dimorph": 3 if args.presentation == "neutral" else clamp(args.dimorph),
        "health_color": clamp(args.health_color),
    }
    out = pack(args.presentation, args.slot, args.label, craft, signal)
    if args.project:
        pc, ps = parse_project(args.project, craft, signal)
        out["projected"] = pack(args.presentation, args.slot, args.label + " projected", pc, ps)
    if args.beauty_only:
        out = {
            "ok": True,
            "mode": "beauty_only",
            "label": args.label,
            "beauty_10": out["beauty_10"],
            "beauty_band": out["beauty_band"],
            "items": signal,
            "signal_gaps": out["signal_gaps"],
            "uncertainty": "high" if craft["lighting"] <= 2 or craft["eyes_visible"] <= 2 else "medium",
            "note": "Face-signal only. Not photo craft. Not a lab measurement.",
        }
    json.dump(out, sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
