#!/usr/bin/env python3
"""Draw the 25 November 2026 world-news front page (1024x1024 PNG).

Deterministic: fixed layout, fixed fonts, no timestamps, no randomness.
Run:  python3 draw_poster.py   -> writes entry.png beside this file.

v2: rebalanced layout so every section fits inside 1024 px — the lead
headline now spans the full width above the picture, the standfirst
sits beside the picture, sections are tightened, and the also-today
items are single lines. The bullet glyph is drawn as a triangle
because the fonts lack a ▸ glyph.
"""
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 242, 231)
INK = (17, 17, 17)
RED = (178, 34, 34)
NAVY = (24, 48, 88)
GREY = (90, 86, 78)
RULE = (150, 142, 128)
LIGHT = (238, 231, 214)
SKY = (214, 228, 240)

SERIF = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"
SERIF_B = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
SANS_B = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, width):
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def para(draw, x, y, width, text, fnt, fill=INK, leading=1.28):
    for ln in wrap(draw, text, fnt, width):
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += int(fnt.size * leading)
    return y


def rule(draw, x, y, width, weight=2, fill=RULE):
    draw.line([(x, y), (x + width, y)], fill=fill, width=weight)


def kicker(draw, x, y, text, size=15):
    draw.text((x, y), text.upper(), font=font(SANS_B, size), fill=RED)


def bullet(draw, x, y, size=7):
    draw.polygon([(x, y), (x, y + 2 * size), (x + 2 * size, y + size)],
                 fill=RED)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    M = 40
    CW = W - 2 * M  # 944

    # ---- Masthead ----
    d.rectangle([0, 0, W, 100], fill=NAVY)
    d.text((M, 12), "THE DAILY GLOBE", font=font(SERIF_B, 56),
           fill=(255, 255, 255))
    d.text((W - M, 24), "ONE DAY  •  ONE PAGE", font=font(SANS_B, 16),
           fill=(200, 210, 230), anchor="ra")
    d.text((W - M, 50), "WORLD NEWS IN A SINGLE IMAGE", font=font(SANS, 14),
           fill=(200, 210, 230), anchor="ra")
    d.line([(0, 100), (W, 100)], fill=RED, width=5)

    # ---- Dateline ----
    y = 114
    d.text((M, y), "WEDNESDAY 25 NOVEMBER 2026", font=font(SANS_B, 21), fill=INK)
    d.text((W - M, y), "THE WORLD'S NEWS TODAY", font=font(SANS_B, 17),
           fill=GREY, anchor="ra")
    y += 32
    rule(d, M, y, CW, 3, INK)
    y += 10

    # ---- Lead story: full-width headline, picture + standfirst below ----
    kicker(d, M, y, "Lead story — Middle East", 15)
    y += 24
    y = para(d, M, y, CW, "HOUTHI DRONE HITS RIYADH'S TALLEST TOWER",
             font(SERIF_B, 46), leading=1.0)
    y += 8
    row_top = y
    pic_x, pic_y, pic_w, pic_h = M, y, 340, 168
    d.rectangle([pic_x, pic_y, pic_x + pic_w, pic_y + pic_h], fill=SKY,
                outline=INK, width=2)
    d.ellipse([pic_x + 252, pic_y + 14, pic_x + 292, pic_y + 54],
              fill=(240, 190, 80))
    d.ellipse([pic_x + 26, pic_y + 22, pic_x + 82, pic_y + 46],
              fill=(255, 255, 255))
    d.ellipse([pic_x + 64, pic_y + 14, pic_x + 120, pic_y + 38],
              fill=(255, 255, 255))
    for bx, bw, bh in [(14, 42, 78), (64, 34, 104), (106, 46, 66),
                       (238, 40, 88), (286, 36, 60)]:
        d.rectangle([pic_x + bx, pic_y + pic_h - bh, pic_x + bx + bw,
                     pic_y + pic_h], fill=(70, 88, 112), outline=INK)
    # the PIF tower with a red impact burst halfway up
    tx0, tw = pic_x + 168, 48
    d.polygon([(tx0, pic_y + pic_h), (tx0 + 7, pic_y + 20),
               (tx0 + tw - 7, pic_y + 20), (tx0 + tw, pic_y + pic_h)],
              fill=(38, 64, 96), outline=INK)
    for wy in range(pic_y + 36, pic_y + pic_h - 10, 14):
        d.line([(tx0 + 5, wy), (tx0 + tw - 5, wy)], fill=(150, 180, 210), width=2)
    cx, cy = tx0 + tw // 2, pic_y + 92
    for dx, dy in [(0, -22), (15, -15), (22, 0), (15, 15), (0, 22),
                   (-15, 15), (-22, 0), (-15, -15)]:
        d.line([(cx, cy), (cx + dx, cy + dy)], fill=RED, width=4)
    d.ellipse([cx - 10, cy - 10, cx + 10, cy + 10], fill=(255, 200, 60),
              outline=RED, width=3)
    d.rectangle([pic_x, pic_y, pic_x + 168, pic_y + 24], fill=NAVY)
    d.text((pic_x + 8, pic_y + 4), "RIYADH  •  PIF TOWER",
           font=font(SANS_B, 13), fill=(255, 255, 255))

    tx = M + 364
    tw_ = W - M - tx
    yy = para(d, tx, row_top, tw_,
              "Eleven people were wounded when a drone struck the "
              "385-metre Public Investment Fund tower in the Saudi "
              "capital — the second hit on the landmark in less "
              "than a week. Riyadh vowed a decisive response.",
              font(SERIF, 20), leading=1.3)
    d.text((tx, yy + 4), "Reuters  •  Saudi Civil Defence",
           font=font(SANS, 14), fill=GREY)

    y = row_top + pic_h + 12
    rule(d, M, y, CW, 2)
    y += 12

    # ---- Two secondary stories, side by side ----
    col_w = (CW - 24) // 2
    kicker(d, M, y, "United States — Cyber", 14)
    kicker(d, M + col_w + 24, y, "United States — Courts", 14)
    y += 22
    y2 = para(d, M, y, col_w, "CIA AND SPY CHIEF'S OFFICE HIT BY CYBERATTACK",
              font(SERIF_B, 27), leading=1.04)
    y2 += 3
    y2 = para(d, M, y2, col_w,
              "The CIA and the Office of the Director of National "
              "Intelligence were hit by a hack of an unclassified "
              "open-source system. No classified data was affected.",
              font(SERIF, 18), leading=1.28)
    d.text((M, y2 + 3), "CNN  •  The New York Times", font=font(SANS, 13), fill=GREY)

    x2 = M + col_w + 24
    y3 = para(d, x2, y, col_w, "HUAWEI CONVICTED ON 10 OF 12 COUNTS IN US TRIAL",
              font(SERIF_B, 27), leading=1.04)
    y3 += 3
    y3 = para(d, x2, y3, col_w,
              "A Brooklyn jury found the Chinese telecoms giant "
              "guilty of trade-secret theft, bank fraud and sanctions "
              "violations over its Iran business; racketeering cleared.",
              font(SERIF, 18), leading=1.28)
    d.text((x2, y3 + 3), "US Department of Justice  •  Reuters",
           font=font(SANS, 13), fill=GREY)

    y = max(y2, y3) + 22
    rule(d, M, y, CW, 2)
    y += 12

    # ---- Three story cards ----
    cards = [
        ("UKRAINE — WAR AT SEA",
         "Zelenskyy confirms ship strike",
         "President Zelenskyy confirmed Ukraine was behind the "
         "drone strike on the Russian cargo ship Sparta II in the "
         "Gulf of Finland. Ally Norway urged caution."),
        ("UNITED STATES — WHITE HOUSE",
         "Medal for Giuliani, pardon for turkeys",
         "President Trump awarded the Medal of Freedom to Rudy "
         "Giuliani, then pardoned Thanksgiving turkeys Freedom and "
         "Feathers."),
        ("SPORT — CRICKET",
         "England crush Australia in 2nd T20",
         "Aneurin Donald smashed 85 off 32 balls and Phil Salt 58 "
         "as England chased 185 in 13.1 overs to win by eight "
         "wickets and level the series 1–1."),
    ]
    card_w = (CW - 48) // 3
    card_top = y
    card_h = 176
    for i, (kick, head, body) in enumerate(cards):
        cx = M + i * (card_w + 24)
        d.rectangle([cx, y, cx + card_w, y + card_h], fill=LIGHT,
                    outline=RULE, width=1)
        d.rectangle([cx, y, cx + card_w, y + 7], fill=RED)
        kicker(d, cx + 13, y + 15, kick, 12)
        yy = para(d, cx + 13, y + 37, card_w - 26, head,
                  font(SERIF_B, 23), leading=1.04)
        yy += 3
        para(d, cx + 13, yy, card_w - 26, body, font(SERIF, 16), leading=1.26)
    y = card_top + card_h + 12
    rule(d, M, y, CW, 2)
    y += 10

    # ---- Also today strip: four single-line items ----
    kicker(d, M, y, "Also today", 15)
    y += 24
    items = [
        "Sarkozy corruption case sent to trial in France; first hearing April 2027.",
        "BJP and Shiromani Akali Dal reunite for the 2027 Punjab elections.",
        "WHO evacuates health workers in DR Congo amid fighting near the Ebola zone.",
        "Nvidia's Jensen Huang is back as chief executive; shares jumped on his return.",
    ]
    for it in items:
        bullet(d, M + 2, y + 5)
        d.text((M + 22, y), it, font=font(SERIF, 17), fill=INK)
        y += 23
    y += 4
    rule(d, M, y, CW, 3, INK)
    y += 8

    # ---- Footer ticker + credit ----
    d.text((M, y), "TICKER", font=font(SANS_B, 14), fill=RED)
    para(d, M + 72, y - 1, CW - 72,
         "COP31 ends with no fossil-fuel deal  •  US blacklists Megaspeed  •  "
         "Houthis near Aden  •  Gaza toll nears 75,000",
         font(SANS, 14), leading=1.25)
    d.text((M, H - 26),
           "THE DAILY GLOBE — Wednesday 25 November 2026 — drawn from the day's reporting",
           font=font(SANS, 13), fill=GREY)

    img.save("entry.png", optimize=True)
    print("saved entry.png", img.size)


if __name__ == "__main__":
    main()
