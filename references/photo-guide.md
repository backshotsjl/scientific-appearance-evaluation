# Photo guide

## Order

1. Face, eyes visible, single subject, standing or seated mid-shot, daylight or soft indoor light. Crop-safe for Tinder's tall card.
2. Full body, real outfit, uncluttered background
3. Activity that matches the bio
4. Social photo where they are easy to spot (color, circle crop note, or "I'm the one in the green jacket")
5. Personality closer — pet, kitchen, mountain, instrument, ridiculous souvenir
6. Second face angle or golden-hour variant, not a duplicate of slot 1

Fill remaining slots with variety, not duplicates of the same face angle.

Winning-grid rules and the slot-1 pass/fail test live in `references/tinder-success.md`.

## Reject or demote

- First-slot group shot
- Sunglasses as the only face
- Bathroom mirror, car selfie with dead light, gym mirror flex as shot 1
- Cropped logos, dirty room, toilet, laundry pile
- All photos from the same night
- Filters that change skin or face shape
- Heavily other-people-centered grids
- Ultra-wide 0.5x selfie that balloons the nose and shrinks the jaw
- Lead photo that dies after the app's center crop

For beauty / science scoring use `references/looks-science.md`, `references/looksmax-softmax.md`, and `looks_machine.py`.
Craft first, then signal. Slot 1 is a craft problem until craft is good.

## Review format

For each photo the user shares:

- Keep / move / drop
- Why (one line)
- Suggested slot (1–6)
- Craft band + signal band if they asked for looks / Bildbewertung

Then output a recommended sequence.

## Shot list if they need new pictures

Give a weekend shot list they can execute with a friend, 30–40 minutes:

- Doorway daylight portrait (slot-1 candidate)
- Walking shot, two frames
- Hobby in progress
- Cafe table, hands and face
- One full-body street photo

Do not generate a photorealistic fake of the user. Style-reference images of lighting and composition are fine.
