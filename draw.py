#!/usr/bin/env python3
"""Draw the 20 November 2026 world-news poster (1024x1024 PNG).

Build-time renderer for the make.fun news-image-20261120 entry. It uses
Pillow and the system Liberation/DejaVu fonts, draws the front page from
the verified facts in ../facts-20261120.md, and writes entry.png beside
this file. The drawing is fully deterministic: fixed geometry, fixed
text, no clocks and no randomness, so two runs give identical bytes.

The committed entry.png is what main.py copies into the grader's output
directory; this script is the source that produced it.
"""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
OUT = HERE / "entry.png"

W = 1024
MARGIN = 36

SERIF_BOLD = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
SANS_BOLD = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"

INK = (18, 18, 20)
PAPER = (250, 248, 242)
WHITE = (255, 255, 255)
RED = (163, 22, 33)
RED_DARK = (122, 14, 24)
NAVY = (16, 46, 84)
GREEN = (10, 94, 64)
ROYAL = (24, 70, 150)
AMBER = (232, 148, 10)
AMBER_INK = (32, 22, 4)
GREY = (90, 90, 96)


def font(path, size):
    return ImageFont.truetype(path, size)


def tracked(draw, xy, text, fnt, fill, tracking=3):
    """Draw text with extra letter spacing; return the end x."""
    x, y = xy
    for ch in text:
        draw.text((x, y), ch, font=fnt, fill=fill)
        x += draw.textlength(ch, font=fnt) + tracking
    return x - tracking


def tracked_width(draw, text, fnt, tracking=3):
    return sum(draw.textlength(ch, font=fnt) for ch in text) + tracking * (len(text) - 1)


def wrap(draw, text, fnt, max_width):
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = word if not cur else cur + " " + word
        if draw.textlength(trial, font=fnt) <= max_width:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def text_block(draw, x, y, text, fnt, fill, max_width, line_gap):
    for line in wrap(draw, text, fnt, max_width):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += line_gap
    return y


def chip(draw, x, y, label, value, label_fill, box_fill, f_label, f_value):
    lw = draw.textlength(label + "  ", font=f_label)
    vw = draw.textlength(value, font=f_value)
    w = lw + vw + 28
    draw.rounded_rectangle([x, y, x + w, y + 52], radius=8, fill=box_fill)
    draw.text((x + 14, y + 13), label, font=f_label, fill=label_fill)
    draw.text((x + 14 + lw, y + 9), value, font=f_value, fill=WHITE)
    return x + w + 12


def masthead(draw):
    draw.rectangle([0, 0, W, 100], fill=INK)
    f_title = font(SERIF_BOLD, 47)
    draw.text((MARGIN, 24), "THE WORLD ON FRIDAY", font=f_title, fill=WHITE)
    f_date = font(SANS_BOLD, 30)
    date = "20 NOVEMBER 2026"
    dw = draw.textlength(date, font=f_date)
    draw.rectangle([W - MARGIN - dw - 28, 18, W - MARGIN, 66], fill=RED)
    draw.text((W - MARGIN - dw - 14, 27), date, font=f_date, fill=WHITE)
    f_sub = font(SANS, 19)
    sub = "THE DAY'S NEWS IN ONE PICTURE"
    sw = tracked_width(draw, sub, f_sub, 2)
    tracked(draw, (W - MARGIN - sw, 74), sub, f_sub, (200, 200, 205), 2)
    draw.rectangle([0, 100, W, 106], fill=RED)


def hero(draw):
    top, bottom = 106, 440
    draw.rectangle([0, top, W, bottom], fill=RED)
    draw.rectangle([0, bottom - 6, W, bottom], fill=RED_DARK)
    f_kick = font(SANS_BOLD, 21)
    tracked(draw, (MARGIN, top + 22), "MARKETS · TOKYO · SEOUL · TAIPEI · NEW YORK",
            f_kick, (255, 205, 190), 2)
    f_head = font(SANS_BOLD, 63)
    draw.text((MARGIN, top + 56), "AI SELL-OFF", font=f_head, fill=WHITE)
    draw.text((MARGIN, top + 122), "GOES GLOBAL", font=f_head, fill=WHITE)
    f_stand = font(SANS, 25)
    text_block(draw, MARGIN, top + 198,
               "Asia plunges as AI-boom doubts spread from Wall Street — "
               "its worst week since 2020.",
               f_stand, (255, 232, 226), 545, 32)
    # Falling chart, right side.
    cx0, cy0, cx1, cy1 = 600, top + 52, W - MARGIN, top + 226
    draw.rectangle([cx0, cy0, cx1, cy1], fill=RED_DARK)
    for i in range(1, 4):
        gy = cy0 + (cy1 - cy0) * i // 4
        draw.line([cx0 + 10, gy, cx1 - 10, gy], fill=(150, 40, 48), width=1)
    pts = [(0.04, 0.16), (0.18, 0.22), (0.32, 0.19), (0.46, 0.34),
           (0.60, 0.42), (0.72, 0.40), (0.84, 0.62), (1.0, 0.86)]
    xy = [(cx0 + 14 + fx * (cx1 - cx0 - 28), cy0 + 12 + fy * (cy1 - cy0 - 24))
          for fx, fy in pts]
    draw.line(xy, fill=WHITE, width=5, joint="curve")
    for px, py in xy:
        draw.ellipse([px - 5, py - 5, px + 5, py + 5], fill=WHITE)
    lx, ly = xy[-1]
    draw.polygon([(lx, ly), (lx - 20, ly - 4), (lx - 6, ly - 18)], fill=WHITE)
    f_cap = font(SANS_BOLD, 20)
    draw.text((cx0 + 14, cy1 - 30), "MSCI ASIA-PACIFIC  -3%", font=f_cap, fill=(255, 205, 190))
    # Stat chips along the bottom of the hero.
    f_lab = font(SANS_BOLD, 20)
    f_val = font(SANS_BOLD, 27)
    x = MARGIN
    y = bottom - 70
    for label, value in [("NIKKEI", "-4.8%"), ("KOSPI", "-4.7%"), ("TAIEX", "-6.4%"),
                         ("SOFTBANK", "-16%"), ("GOLD", "-4.2%")]:
        x = chip(draw, x, y, label, value, (255, 205, 190), RED_DARK, f_lab, f_val)


def panel(draw, box, fill, kicker, headline, body, motif):
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=fill)
    dark_text = fill == AMBER
    head_fill = AMBER_INK if dark_text else WHITE
    body_fill = (58, 42, 8) if dark_text else (225, 232, 242)
    kick_fill = (122, 66, 0) if dark_text else (170, 205, 255)
    if fill == GREEN:
        kick_fill = (160, 235, 200)
    if fill == ROYAL:
        kick_fill = (175, 205, 255)
    f_kick = font(SANS_BOLD, 18)
    tracked(draw, (x0 + 24, y0 + 15), kicker, f_kick, kick_fill, 2)
    f_head = font(SANS_BOLD, 31)
    y = text_block(draw, x0 + 24, y0 + 44, headline, f_head, head_fill, x1 - x0 - 48, 37)
    f_body = font(SANS, 22)
    text_block(draw, x0 + 24, y + 6, body, f_body, body_fill, x1 - x0 - 48, 28)
    draw.rectangle([x0 + 24, y1 - 16, x1 - 24, y1 - 13], fill=kick_fill)
    motif(draw, box)


def motif_bridge(draw, box):
    # Small bridge glyph in the panel's top-right corner.
    x0, y0, x1, y1 = box
    gx1, gy = x1 - 22, y0 + 34
    gx0 = gx1 - 76
    col = (120, 170, 225)
    draw.line([gx0, gy, gx1, gy], fill=col, width=3)
    for tx in (gx0 + 14, gx1 - 14):
        draw.line([tx, gy - 20, tx, gy], fill=col, width=3)
    draw.arc([gx0 + 14, gy - 30, gx1 - 14, gy + 12], start=180, end=360, fill=col, width=2)
    draw.arc([gx0 + 8, gy + 6, gx0 + 30, gy + 20], start=0, end=180, fill=col, width=2)
    draw.arc([gx0 + 46, gy + 6, gx0 + 68, gy + 20], start=0, end=180, fill=col, width=2)


def motif_globe(draw, box):
    # Small globe glyph in the panel's top-right corner.
    x0, y0, x1, y1 = box
    cx, cy, r = x1 - 48, y0 + 26, 17
    col = (150, 230, 195)
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=col, width=3)
    draw.ellipse([cx - 7, cy - r, cx + 7, cy + r], outline=col, width=2)
    draw.line([cx - r, cy, cx + r, cy], fill=col, width=2)


def motif_circles(draw, box):
    # Two overlapping rings in the panel's top-right corner.
    x0, y0, x1, y1 = box
    cy = y0 + 26
    draw.ellipse([x1 - 96, cy - 16, x1 - 64, cy + 16], outline=(165, 200, 255), width=3)
    draw.ellipse([x1 - 74, cy - 16, x1 - 42, cy + 16], outline=(255, 205, 90), width=3)


def motif_placards(draw, box):
    # Two small placards in the panel's top-right corner.
    x0, y0, x1, y1 = box
    col = (122, 66, 0)
    for px, py, w, h in [(x1 - 96, y0 + 8, 34, 20), (x1 - 54, y0 + 12, 30, 17)]:
        draw.rectangle([px, py, px + w, py + h], outline=col, width=3)
        draw.line([px + w // 2, py + h, px + w // 2, y0 + 42], fill=col, width=3)


def briefs(draw):
    top = 910
    draw.rectangle([0, top, W, W], fill=INK)
    f_lab = font(SANS_BOLD, 21)
    draw.rectangle([MARGIN, top + 16, MARGIN + 118, top + 58], fill=RED)
    tw = draw.textlength("IN BRIEF", font=f_lab)
    draw.text((MARGIN + (118 - tw) / 2, top + 26), "IN BRIEF", font=f_lab, fill=WHITE)
    f_b = font(SANS, 19)
    items = [
        "Trump posthumously pardons baseball great Pete Rose",
        "Fiji & Tonga declare disasters as El Niño drought bites",
        "Record flooding on Florida's St. Johns River",
        "Marathon champion Jepchirchir banned 3 years for doping",
    ]
    col_x = [MARGIN + 140, 592]
    row_y = [top + 12, top + 64]
    for i, item in enumerate(items):
        x = col_x[i % 2]
        y = row_y[i // 2]
        draw.ellipse([x, y + 7, x + 7, y + 14], fill=RED)
        text_block(draw, x + 16, y, item, f_b, (232, 232, 236), 372, 24)


def main():
    img = Image.new("RGB", (W, W), PAPER)
    draw = ImageDraw.Draw(img)
    masthead(draw)
    hero(draw)
    gap = 8
    row1_y = 440 + gap
    row_h = 224
    half = (W - 2 * MARGIN - 12) // 2
    left = (MARGIN, row1_y, MARGIN + half, row1_y + row_h)
    right = (MARGIN + half + 12, row1_y, W - MARGIN, row1_y + row_h)
    panel(draw, left, NAVY, "UKRAINE · KYIV", "MISSILES HIT KYIV'S DNIPRO BRIDGES",
          "Russian strikes damage three river crossings — the biggest "
          "bridge attack of the war: 3 killed, 15 injured.", motif_bridge)
    panel(draw, right, GREEN, "CLIMATE · ANTALYA", "COP31 FINAL DAY: NO DEAL IN SIGHT",
          "Nearly 200 nations divided as the draft deal drops every "
          "mention of fossil fuels; talks head into overtime.",
          motif_globe)
    row2_y = row1_y + row_h + gap
    left2 = (MARGIN, row2_y, MARGIN + half, row2_y + row_h)
    right2 = (MARGIN + half + 12, row2_y, W - MARGIN, row2_y + row_h)
    panel(draw, left2, ROYAL, "BRUSSELS · UK–EU SUMMIT", "BREXIT RESET: 100,000 YOUTH VISAS A YEAR",
          "The biggest UK–EU deal since Brexit: youth mobility both "
          "ways, food checks end, carbon markets link.",
          motif_circles)
    panel(draw, right2, AMBER, "EUROPE · 25+ COUNTRIES", "'FIGHT FOR OUR FUTURE, NOT THEIR WAR'",
          "Young people march across Europe over living costs, housing "
          "and arms spending; Italy holds a general strike.",
          motif_placards)
    briefs(draw)
    img.save(OUT, format="PNG", optimize=True)
    print("wrote", OUT)


if __name__ == "__main__":
    main()
