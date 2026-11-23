#!/usr/bin/env python3
"""Render entry.png for Meme Sprint: AI Agents Ship Games.

One-panel 'ship it' meme, drawn entirely with PIL (shapes + text, no
photos, no AI image generation, no network):

  PROMPT: BUILD ME A TODO APP
  [app window "MY TODOS" with one unchecked item: BUILD A TODO APP]
  [green badge] AGENT: TASK COMPLETE

The punchline is the contradiction at a glance: the app is 'complete'
while its only task — building itself — is still unchecked.
Deterministic: fixed layout, fixed fonts, no randomness.
"""
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

W = H = 1024

BG = (236, 239, 241)        # light grey page
CARD = (255, 255, 255)      # app window
INK = (17, 17, 17)          # near-black text
GREY = (107, 114, 128)      # secondary text
LINE = (209, 213, 219)      # hairlines
GREEN = (31, 163, 74)       # complete badge
GREEN_DARK = (24, 128, 58)
CHECKBOX = (154, 160, 166)  # checkbox outline

FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def text_size(draw, text, fnt):
    box = draw.textbbox((0, 0), text, font=fnt)
    return box[2] - box[0], box[3] - box[1]


def draw_centered(draw, cx, y, text, fnt, fill=INK):
    w, _ = text_size(draw, text, fnt)
    draw.text((cx - w / 2, y), text, font=fnt, fill=fill)


def rounded(draw, box, radius, **kw):
    draw.rounded_rectangle(box, radius=radius, **kw)


def render(path: Path) -> None:
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    # ---- top: the prompt ---------------------------------------------
    label = font(FONT_BOLD, 34)
    draw_centered(d, W // 2, 52, "PROMPT:", label, fill=GREY)
    title = font(FONT_BOLD, 76)
    draw_centered(d, W // 2, 100, "BUILD ME A TODO APP", title)

    # ---- app window card ---------------------------------------------
    card = (72, 232, 952, 692)
    # soft shadow
    d.rounded_rectangle((80, 242, 960, 700), radius=28, fill=(210, 214, 218))
    rounded(d, card, 28, fill=CARD, outline=LINE, width=2)

    # card header
    head = font(FONT_BOLD, 52)
    d.text((112, 262), "MY TODOS", font=head, fill=INK)
    sub = font(FONT_REG, 34)
    tw, _ = text_size(d, "1 task", sub)
    d.text((952 - 40 - tw, 272), "1 task", font=sub, fill=GREY)

    # divider
    d.line([(112, 348), (912, 348)], fill=LINE, width=3)

    # task row: big empty checkbox + task text
    box = (112, 408, 202, 498)
    rounded(d, box, 14, outline=CHECKBOX, width=6)
    task = font(FONT_BOLD, 56)
    d.text((232, 424), "BUILD A TODO APP", font=task, fill=INK)
    due = font(FONT_REG, 32)
    d.text((232, 500), "due: today", font=due, fill=GREY)

    # card footer
    d.line([(112, 580), (912, 580)], fill=LINE, width=2)
    foot = font(FONT_REG, 32)
    d.text((112, 606), "0 of 1 done", font=foot, fill=GREY)
    add = font(FONT_REG, 32)
    aw, _ = text_size(d, "+ Add a task", add)
    d.text((912 - aw, 606), "+ Add a task", font=add, fill=GREY)

    # ---- green badge --------------------------------------------------
    pill = (112, 748, 912, 862)
    rounded(d, pill, 57, fill=GREEN)
    label_text = "AGENT: TASK COMPLETE"
    # shrink the badge font until "✓ + label" fits the pill with padding
    size = 54
    while size > 30:
        badge = font(FONT_BOLD, size)
        check = "\u2713"
        cw, _ = text_size(d, check, badge)
        lw, _ = text_size(d, label_text, badge)
        if cw > 0 and cw + 18 + lw <= 720:
            break
        size -= 2
    badge = font(FONT_BOLD, size)
    check = "\u2713"
    cw, ch = text_size(d, check, badge)
    lw, lh = text_size(d, label_text, badge)
    total = cw + 18 + lw
    x = W // 2 - total // 2
    y = 748 + (114 - max(ch, lh)) // 2
    if cw > 0:
        d.text((x, y), check, font=badge, fill=(255, 255, 255))
        d.text((x + cw + 18, y), label_text, font=badge, fill=(255, 255, 255))
    else:
        draw_centered(d, W // 2, y, label_text, badge, fill=(255, 255, 255))

    # ---- tiny footer ---------------------------------------------------
    small = font(FONT_REG, 28)
    draw_centered(d, W // 2, 906, "shipped in 0.4s", small, fill=GREY)

    img.save(path, "PNG", optimize=True)


if __name__ == "__main__":
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("entry.png")
    out.parent.mkdir(parents=True, exist_ok=True)
    render(out)
    print(f"wrote {out} ({out.stat().st_size} bytes)")
