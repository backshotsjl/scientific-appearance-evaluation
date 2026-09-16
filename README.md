# Scientific appearance evaluation

Two-track rater for dating photos.

- **Craft** — lighting, sharpness, eyes, solo, crop. This moves swipe outcomes.
- **Signal** — symmetry proxy, skin evenness, visible adiposity, grooming, dimorphism (only after presentation is set), health color. Weighted from the face-beauty literature, not a CNN and not a caliper.

This is a structured human-in-the-loop heuristic. It is **not** geometric morphometrics and not a lab measurement.

## Run

```bash
python3 looks_machine.py --presentation masc --slot 1 --label lead \
  --face-share 4 --lighting 5 --sharpness 4 --eyes-visible 5 --solo 5 \
  --background 4 --expression-app 3 --variety-role 5 \
  --symmetry 4 --skin 3 --adiposity 3 --grooming 4 --dimorph 3 --health-color 4
```

Beauty-only (ignore swipe craft):

```bash
python3 looks_machine.py --beauty-only --presentation femme \
  --face-share 4 --lighting 2 --sharpness 4 --eyes-visible 5 --solo 5 \
  --background 3 --expression-app 4 --variety-role 3 \
  --symmetry 4 --skin 4 --adiposity 3 --grooming 4 --dimorph 4 --health-color 4
```

Items are integers 1–5. Output is JSON with `craft_10`, `signal_10`, bands, blockers, and top fixes.

## What the numbers mean

| Band | Score |
| --- | --- |
| strong | 8–10 |
| usable | 6–7.9 |
| leaving points | 4–5.9 |
| replace | below 4 |

Slot 1 needs `slot1_suitability` ≥ 7 or reshoot. Do not "add masculinity" to a dark group photo.

## Docs

- `references/looks-science.md` — what Rhodes 2006 and related papers actually support
- `references/looksmax-softmax.md` — looksmaxxer slang mapped to reversible photo fixes
- `references/sources.md` — citations
- `references/photo-guide.md` — grid order
- `references/tinder-success.md` — winning swipe profile anatomy

## Rules

- Adults only.
- Ask `femme` / `masc` / `neutral` before dimorphism weights.
- Never collapse craft + signal into one mystical looks rating.
- No millimeter bone claims from a phone pic. No surgery ladders.

Dating-app coach bot that uses this rater: `backshotsjl/dating-bot`.
