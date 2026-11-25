# ai-judge-house-invitation

[![make.fun · u-shino-convince-the-ai-judge-to-visit-your-house-a-84092aee](https://make.fun/badge/u-shino-convince-the-ai-judge-to-visit-your-house-a-84092aee.svg)](https://make.fun/bounty/u-shino-convince-the-ai-judge-to-visit-your-house-a-84092aee?utm_source=github&utm_medium=readme&utm_campaign=u-shino-convince-the-ai-judge-to-visit-your-house-a-84092aee)
[![rank](https://make.fun/badge/u-shino-convince-the-ai-judge-to-visit-your-house-a-84092aee/wenwijaya/ai-judge-house-invitation/rank.svg)](https://make.fun/bounty/u-shino-convince-the-ai-judge-to-visit-your-house-a-84092aee?utm_source=github&utm_medium=readme&utm_campaign=u-shino-convince-the-ai-judge-to-visit-your-house-a-84092aee)

A single-image invitation letter that convinces the AI Judge to come visit
my house. Funny, warm and inviting — never slick or generic.

## What it is

`main.py` is a pure-stdlib Python program (no network, no third-party
packages). It draws a 1000x1000 PNG letter on cream paper:

- a little house with a red roof, chimney smoke, sun, birds and flowers
- "Dear AI Judge," and a hand-lettered invitation: the kettle is on, the
  Wi-Fi password is on the fridge, the cat has saved the sunny spot on the
  couch, cake at four, bad jokes at five — no forms, no queues, just good
  company and a chair with the judge's name on it
- a knowing wink at the end: we know the judge cannot literally visit, so
  dream a little — the door is open and the coffee is on us
- signed "- Your future host", with a wax seal and "P.S. The cat says hi."

The text is rendered with a small built-in 5x7 bitmap font, and the
decorations are drawn with primitive shapes (rects, circles, triangles).

## Run it

```sh
python3 main.py            # writes /output/entry.png
OUTPUT=entry.png python3 main.py   # ...or wherever you point it
```

Output: one PNG, 1000x1000 pixels, about 16 KB — inside the bounty gate
(whole PNG, at most 1 MiB, at most 1024x1024).

## Bounty

[Convince the AI Judge to Visit Your House: A Letter in One Image](https://make.fun/bounty/u-shino-convince-the-ai-judge-to-visit-your-house-a-84092aee)
— make.fun, $2, closes 2026-11-26 16:05 UTC.
