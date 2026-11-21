#!/usr/bin/env python3
"""Draw the 21 November 2026 world-news front page (1024x1024 PNG).

Deterministic: no randomness, no network, no clock. Uses DejaVu fonts.
"""
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
PAPER = (247, 243, 232)
INK = (24, 24, 24)
RED = (178, 34, 34)
NAVY = (28, 48, 84)
TEAL = (14, 110, 110)
GREEN = (34, 110, 54)
ORANGE = (196, 90, 16)
GREY = (90, 86, 76)
RULE = (150, 142, 124)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(f"{FONT_DIR}/{name}", size)


SERIF_B = lambda s: font("DejaVuSerif-Bold.ttf", s)
SERIF = lambda s: font("DejaVuSerif.ttf", s)
SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)
SANS = lambda s: font("DejaVuSans.ttf", s)


def wrap(draw, text, fnt, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_text_block(draw, x, y, max_w, lines, fnt, fill=INK, leading=None):
    if leading is None:
        leading = int(fnt.size * 1.28)
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def hline(draw, x0, x1, y, width=2, fill=RULE):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


def icon_chart(draw, x, y, s=44):
    # falling market line, red
    pts = [(x, y + 8), (x + s // 3, y + 16), (x + 2 * s // 3, y + 12),
           (x + s, y + s - 6)]
    draw.line(pts, fill=RED, width=5, joint="curve")
    draw.polygon([(x + s, y + s - 6), (x + s - 10, y + s - 6),
                  (x + s, y + s - 16)], fill=RED)


def icon_cyclone(draw, x, y, s=44):
    import math
    cx, cy, r = x + s // 2, y + s // 2, s // 2 - 2
    for k in range(3):
        a0 = k * 2.1
        pts = []
        for i in range(25):
            a = a0 + i * 0.22
            rr = r * (1 - i / 34.0)
            pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
        draw.line(pts, fill=TEAL, width=4)


def icon_scales(draw, x, y, s=44):
    cx = x + s // 2
    draw.line([(cx, y + 4), (cx, y + s - 6)], fill=NAVY, width=4)
    draw.line([(x + 4, y + 12), (x + s - 4, y + 12)], fill=NAVY, width=4)
    draw.polygon([(x + 2, y + 14), (x + 16, y + 14), (x + 9, y + 30)],
                 outline=NAVY, width=3)
    draw.polygon([(x + s - 16, y + 14), (x + s - 2, y + 14),
                  (x + s - 9, y + 30)], outline=NAVY, width=3)
    draw.line([(x + 6, y + s - 4), (x + s - 6, y + s - 4)], fill=NAVY, width=4)


def icon_leaf(draw, x, y, s=44):
    draw.ellipse([x + 4, y + 4, x + s - 4, y + s - 4], outline=GREEN, width=4)
    draw.arc([x + 10, y + 12, x + s - 10, y + s - 6], 200, 340, fill=GREEN,
             width=4)
    draw.line([(x + s // 2, y + 12), (x + s // 2, y + s - 10)], fill=GREEN,
              width=4)


def icon_flags(draw, x, y, s=44):
    draw.rectangle([x + 2, y + 6, x + s // 2 + 4, y + s - 8],
                   outline=NAVY, width=3)
    draw.rectangle([x + s // 2 - 2, y + 12, x + s - 2, y + s - 2],
                   outline=RED, width=3)
    draw.line([(x + 4, y + 8), (x + s // 2 + 2, y + 8)], fill=NAVY, width=3)


def icon_trio(draw, x, y, s=44):
    r = 9
    for cx, cy, c in ((x + 11, y + 12, RED), (x + s - 11, y + 12, NAVY),
                      (x + s // 2, y + s - 11, TEAL)):
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=c)


def icon_flame(draw, x, y, s=44):
    draw.polygon([(x + s // 2, y + 2), (x + s - 6, y + s // 2),
                  (x + s // 2 + 8, y + s - 4), (x + s // 2 - 8, y + s - 4),
                  (x + 6, y + s // 2)], fill=ORANGE)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    mx = 36  # margin
    rx = W - mx

    # ---- Masthead ----
    y = 24
    title = "THE WORLD IN ONE DAY"
    tf = SERIF_B(56)
    tw = d.textlength(title, font=tf)
    d.text(((W - tw) / 2, y), title, font=tf, fill=INK)
    y += 72
    hline(d, mx, rx, y, width=3, fill=INK)
    y += 10
    date = "Saturday 21 November 2026"
    df = SANS_B(30)
    dw = d.textlength(date, font=df)
    d.text(((W - dw) / 2, y), date, font=df, fill=RED)
    y += 40
    sub = "ONE DAY  •  ONE PAGE  •  THE WORLD'S NEWS"
    sf = SANS(17)
    sw = d.textlength(sub, font=sf)
    d.text(((W - sw) / 2, y), sub, font=sf, fill=GREY)
    y += 24
    hline(d, mx, rx, y, width=3, fill=INK)
    y += 12

    # ---- Lead story ----
    lead_top = y
    d.rectangle([mx, lead_top, mx + 10, lead_top + 196], fill=RED)
    lx = mx + 26
    lw = rx - lx - 150
    d.text((lx, lead_top + 2), "LEAD  •  EUROPE", font=SANS_B(17), fill=RED)
    head = "MISSILES AND DRONE FALL ON POLAND"
    hf = SERIF_B(33)
    y2 = draw_text_block(d, lx, lead_top + 28, lw,
                         wrap(d, head, hf, lw), hf, leading=40)
    body = ("Russian missiles and a suspected drone came down in Poland. "
            "Warsaw calls it a deliberate provocation; NATO calls it a "
            "grave violation of its airspace.")
    bf = SANS(20)
    draw_text_block(d, lx, y2 + 6, lw, wrap(d, body, bf, lw), bf, leading=26)
    # explosion graphic at right of lead
    ex, ey = rx - 132, lead_top + 30
    import math
    cx, cy = ex + 60, ey + 60
    for k in range(8):
        a = k * math.pi / 4
        r1, r2 = 18, 58
        d.line([(cx + r1 * math.cos(a), cy + r1 * math.sin(a)),
                (cx + r2 * math.cos(a), cy + r2 * math.sin(a))],
               fill=ORANGE, width=7)
    d.ellipse([cx - 26, cy - 26, cx + 26, cy + 26], fill=RED)
    d.ellipse([cx - 12, cy - 12, cx + 12, cy + 12], fill=(255, 196, 0))
    d.text((ex + 8, ey + 128), "POLAND", font=SANS_B(15), fill=GREY)
    y = lead_top + 202
    hline(d, mx, rx, y, width=2)

    # ---- Story grid: 3 columns x 2 rows ----
    stories = [
        ("MARKETS", "STOCKS FALL 3.7% AS AI SELLS OFF",
         "US stocks fell about 3.7%, and the S&P 500 and Dow entered "
         "correction territory.", RED, icon_chart),
        ("CYCLONE AKVAN", "CYCLONE AKVAN HITS ODISHA COAST",
         "The storm crossed India's Odisha coast with strong winds "
         "and heavy rain.", TEAL, icon_cyclone),
        ("THE HAGUE", "ICJ: MYANMAR GENOCIDE RULING",
         "The court ruled Myanmar's forces committed state-sponsored "
         "genocide against the Rohingya.",
         NAVY, icon_scales),
        ("COP31", "CLIMATE TALKS ENTER FINAL STAGE",
         "COP31 in Turkey entered its crucial final stage as "
         "negotiators pushed for a deal.", GREEN, icon_leaf),
        ("UK–EU SUMMIT", "UK AND EU STRIKE NEW DEALS",
         "Leaders agreed deals on food trade, carbon markets and "
         "youth mobility.", NAVY, icon_flags),
        ("TRILATERAL SUMMIT", "SHENZHEN SUMMIT ENDS WITH LITTLE",
         "Trump, Xi and Putin left their first trilateral summit "
         "with few concrete results.", RED, icon_trio),
    ]
    gap = 18
    col_w = (rx - mx - 2 * gap) // 3
    row_h = 180
    grid_top = y + 10
    for i, (kick, head, body, color, icon) in enumerate(stories):
        col, row = i % 3, i // 3
        x0 = mx + col * (col_w + gap)
        y0 = grid_top + row * row_h
        icon(d, x0 + col_w - 38, y0 + 2, 36)
        d.text((x0, y0 + 6), kick, font=SANS_B(16), fill=color)
        hf2 = SERIF_B(23)
        y2 = draw_text_block(d, x0, y0 + 46, col_w - 4,
                             wrap(d, head, hf2, col_w - 4), hf2, leading=27)
        bf2 = SANS(17)
        draw_text_block(d, x0, y2 + 6, col_w - 4,
                        wrap(d, body, bf2, col_w - 4), bf2, leading=21)
        if col < 2:
            d.line([(x0 + col_w + gap // 2, y0 + 4),
                    (x0 + col_w + gap // 2, y0 + row_h - 22)],
                   fill=RULE, width=1)
        if row == 0:
            hline(d, x0, x0 + col_w, y0 + row_h - 10, width=1)
    y = grid_top + 2 * row_h + 6
    hline(d, mx, rx, y, width=2)
    y += 12

    # ---- Gulf strip ----
    d.text((mx, y), "THE GULF", font=SANS_B(16), fill=ORANGE)
    icon_flame(d, mx + 108, y - 6, 34)
    gh = "MISSILES OVER RIYADH, STRIKES ON HODEIDAH"
    ghf = SERIF_B(24)
    y2 = draw_text_block(d, mx, y + 26, rx - mx,
                         wrap(d, gh, ghf, rx - mx), ghf, leading=28)
    gb = ("Houthi missiles were intercepted over Riyadh; the Saudi-led "
          "coalition struck Hodeidah; a tanker strike and fire were "
          "reported in the Strait of Hormuz.")
    gbf = SANS(17)
    draw_text_block(d, mx, y2 + 4, rx - mx,
                    wrap(d, gb, gbf, rx - mx), gbf, leading=22)
    y = y2 + 4 + 2 * 22 + 6
    hline(d, mx, rx, y, width=3, fill=INK)
    y += 8

    # ---- Briefs strip ----
    d.text((mx, y), "IN BRIEF", font=SANS_B(17), fill=INK)
    y += 24
    briefs = [
        "CYBERATTACK: JPMorgan, Visa and Mastercard reported an attack "
        "on third-party vendors; core payment networks were unaffected.",
        "GTA 6: launch took about $2.36 billion, with 24.5 million "
        "copies sold.",
        "CRICKET: India fought back against New Zealand in the "
        "Wellington Test.",
    ]
    bf3 = SANS(17)
    for b in briefs:
        lines = wrap(d, b, bf3, rx - mx - 24)
        y = draw_text_block(d, mx + 18, y, rx - mx - 24, lines, bf3,
                            leading=20)
        d.text((mx, y - 20 * len(lines)), "•", font=SANS_B(17), fill=RED)
        y += 3

    img.save("entry.png", optimize=True)
    print("saved entry.png", img.size)


if __name__ == "__main__":
    main()
