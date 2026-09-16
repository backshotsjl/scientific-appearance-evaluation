# Looks science and looks machine

Two tracks. Do not mix them into one mystical attractiveness number.

1. **Craft** — how the photo is shot. Strong evidence for swipe/message outcomes.
2. **Signal** — face/body cues that lab studies associate with attractiveness ratings. Effects are real, often small-to-medium, and sample-biased (WEIRD, young, posed faces).

This is a structured rater plus weights. It is not geometric morphometrics and not a trained beauty CNN.

Full citations: `references/sources.md`.

## Beauty-only mode

When the user wants only beauty, ignore craft. Run:

```bash
python3 looks_machine.py --beauty-only --presentation masc ...
```

Rate the face, not the lighting setup:

- Do not drop skin, symmetry, or health just because a shadow hides them. Mark uncertainty high instead.
- Do not use an AI-smoothed edit as the beauty sample.
- Male facial masculinity stays mid unless the bone structure is clearly a strong dimorphic cue.
- Report beauty_10 and the six signal items. No swipe number unless they ask.

## What is actually supported

- First impressions of a face form in about 100 ms (Willis and Todorov 2006).
- On dating sites, rated photo attractiveness dominates first-contact (Hitsch, Hortacsu, Ariely 2010).
- Averageness medium-to-large (Rhodes 2006, about r 0.40 on typical faces).
- Symmetry smaller (Rhodes 2006, about r 0.23).
- Femininity in female-presenting faces large (Rhodes 2006, r ~0.64).
- Masculinity in male-presenting faces mixed. Do not treat more chad jaw as settled science.
- Skin evenness and apparent health are repeatedly rated attractive. Lighting and sleep fake a lot of this.
- Smile findings conflict (app raters vs Tracy and Beall 2011). Lead slightly warm, one composed shot later.

Looksmaxxer feature names are community labels, not measurements from a dating selfie. Map them with `references/looksmax-softmax.md`.

## What you must not do

- Output you are a 4.7 as if a lab measured landmarks.
- Surgery ladders, ethnic feature targeting, or subhuman/Chad language.
- Scoring minors.

## How to rate

Fill 1-5 integers, then run looks_machine.py. Report craft_10 and signal_10 as bands. Slot 1 needs craft_10 >= 7 or reshoot.
