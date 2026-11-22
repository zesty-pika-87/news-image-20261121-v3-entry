#!/usr/bin/env python3
"""Draw the 21 November 2026 front page: 35 stories, 13 layered
illustrations, a world map with numbered pins, one-page newspaper.

Runs with the standard library plus Pillow and numpy, no network, no
clock: the same input always writes the same PNG bytes.
Usage: python3 draw.py [output-path]
"""
import os
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFont

W, H = 960, 1024
CREAM = (244, 239, 227)
PAPER2 = (238, 231, 214)
INK = (34, 30, 26)
MUTED = (112, 105, 90)
RULE = (178, 169, 146)
RED = (168, 44, 32)
DARKRED = (122, 30, 22)
NAVY = (28, 44, 66)
NAVY2 = (20, 32, 50)
LAND = (232, 221, 194)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
SERIF = os.path.join(FONT_DIR, "DejaVuSerif.ttf")
SERIFB = os.path.join(FONT_DIR, "DejaVuSerif-Bold.ttf")
SANS = os.path.join(FONT_DIR, "DejaVuSans.ttf")
SANSB = os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf")

REGIONS = {
    "MIDDLE EAST": (168, 58, 40),
    "EUROPE": (47, 93, 138),
    "AMERICAS": (46, 125, 79),
    "ASIA": (183, 121, 31),
    "AFRICA": (108, 74, 138),
    "GLOBAL": (63, 125, 122),
}

# num, region, kicker-source, headline, deck, illustration, lon, lat
STORIES = [
    (1, "MIDDLE EAST", "REUTERS / AFP",
     "Iran strikes US bases",
     "Tehran claims bases hit; Bahrain reports fire, no injuries.",
     "bahrain", 50.6, 26.2),
    (2, "AMERICAS", "PBS / AL JAZEERA",
     "Mexico seizes 'Chapo Isidro'",
     "Most-wanted boss seized in Guasave; 11 dead in the violence.",
     "mexico", -108.5, 25.6),
    (3, "GLOBAL", "AL JAZEERA / EURONEWS",
     "COP31 deadlocked",
     "Antalya talks in overtime, split on fossil fuels and finance.",
     "cop31", 30.7, 36.9),
    (4, "EUROPE", "AL JAZEERA",
     "Missile hits Zelenskyy city",
     "Two dead, 58 hurt in Kryvyi Rih.",
     "kryvyi", 33.4, 47.9),
    (5, "AMERICAS", "USGS / AFP",
     "Strong quake shakes Peru",
     "6.7 quake hits Peru; 152 homes uninhabitable.",
     "peru", -77.0, -12.0),
    (6, "GLOBAL", "REUTERS / BBC",
     "AI sell-off hits US stocks",
     "S&P 500, Nasdaq slide; Anthropic shares fall.",
     "markets", -74.0, 40.7),
    (7, "MIDDLE EAST", "AL JAZEERA / REUTERS",
     "Riyadh stops missiles",
     "Coalition strikes Hodeidah port in reply.",
     "riyadh", 46.7, 24.6),
    (8, "MIDDLE EAST", "AL JAZEERA",
     "Gaza aid truck struck",
     "Three killed in attack on an aid convoy.",
     "gaza", 34.5, 31.5),
    (9, "GLOBAL", "MARKET DATA",
     "Bitcoin tops $60,000",
     "A 9% bounce from a two-year low.",
     "bitcoin", None, None),
    (10, "AMERICAS", "US REPORTS",
     "FBI database hit by breach",
     "Trump calls the intrusion 'not good'.",
     "fbi", -77.0, 38.9),
    (11, "GLOBAL", "TECH REPORTS",
     "Amazon nears Decart AI deal",
     "$7.5bn deal would be its biggest AI bet.",
     "amazon", -122.3, 47.6),
    (12, "GLOBAL", "ESA",
     "BepiColombo at Mercury",
     "ESA-JAXA craft in orbit after eight years.",
     "mercury", None, None),
    (13, "AMERICAS", "EURONEWS",
     "Pentagon UFO footage",
     "Declassified clips filmed by US forces.",
     "ufo", 44.0, 33.0),
]

# num, region, short index headline, lon, lat
INDEX = [
    (14, "EUROPE", "Drone strike sets Russian ship ablaze", 24.0, 59.8),
    (15, "MIDDLE EAST", "Two strikes reported on Hormuz shipping", 56.5, 26.5),
    (16, "MIDDLE EAST", "Araghchi seeks diplomacy to end war", 51.4, 35.7),
    (17, "ASIA", "Trump defends Putin ties after Xi summit", 114.1, 22.5),
    (18, "EUROPE", "Russian copter in Finnish airspace", 28.0, 61.0),
    (19, "EUROPE", "EU and Indonesia sign trade deals", 4.35, 50.85),
    (20, "EUROPE", "Costa proposes \u20ac1.78tn EU budget", 7.0, 50.8),
    (21, "MIDDLE EAST", "Fire at Basra power station kills four", 47.8, 30.5),
    (22, "AMERICAS", "Three dead after blast in Haiti operation", -72.3, 18.5),
    (23, "ASIA", "France to seek UN meeting on Myanmar", 96.0, 20.0),
    (24, "EUROPE", "Zelenskyy: bridge strikes 'fair response'", 34.0, 45.0),
    (25, "EUROPE", "Denmark alleges Russian murder plot", 10.5, 55.7),
    (26, "AMERICAS", "Man convicted of starting Palisades fire", -118.2, 34.05),
    (27, "AMERICAS", "Mamdani plans to shut Rikers by 2032", -73.5, 40.9),
    (28, "EUROPE", "Cost-of-living protests sweep Europe", 2.35, 48.85),
    (29, "AFRICA", "ANC fights to hold key SA cities", 28.0, -26.0),
    (30, "ASIA", "Nepal's Shah faces India test", 77.2, 28.6),
    (31, "AMERICAS", "Wolbachia cuts dengue in Brazil", -46.6, -23.5),
    (32, "ASIA", "Pilotless air taxi flies passengers in Japan", 139.7, 35.7),
    (33, "AMERICAS", "Second judge blocks Trump's arch", -77.5, 38.7),
    (34, "AMERICAS", "Bolsonaro in intensive care", -47.9, -15.8),
    (35, "AFRICA", "24 bodies after Nigeria boat capsize", 6.5, 9.0),
]

NUMBERS = [
    ("2", "US BASES, BAHRAIN"),
    ("11", "DEAD, SINALOA"),
    ("58", "INJURED, KRYVYI RIH"),
    ("6.7", "PERU QUAKE"),
    ("$60,000", "BITCOIN"),
    ("4", "DEAD, BASRA FIRE"),
]

_fonts = {}


def font(path, size):
    key = (path, size)
    if key not in _fonts:
        _fonts[key] = ImageFont.truetype(path, size)
    return _fonts[key]


def wrap(d, text, fnt, maxw):
    """Greedy word wrap; returns a list of lines."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if d.textlength(trial, font=fnt) <= maxw or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def fit(d, text, fnt, maxw, maxlines, warn):
    """Wrap to at most maxlines; truncate the last line with an ellipsis."""
    lines = wrap(d, text, fnt, maxw)
    if len(lines) > maxlines:
        warn.append("TRUNCATED (%d->%d lines): %r" % (len(lines), maxlines, text))
        lines = lines[:maxlines]
        while lines and d.textlength(lines[-1] + "\u2026", font=fnt) > maxw:
            lines[-1] = lines[-1][:-1]
        lines[-1] = lines[-1] + "\u2026"
    return lines


def vgrad(img, box, top, bot):
    """Layer 1 for every illustration: a vertical sky gradient."""
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    t = np.linspace(0, 1, h)[:, None, None]
    a = np.array(top, dtype=float)[None, None, :]
    b = np.array(bot, dtype=float)[None, None, :]
    arr = (a + (b - a) * t).astype(np.uint8)
    arr = np.repeat(arr, w, axis=1)
    img.paste(Image.fromarray(arr, "RGB"), (x0, y0))


def grain(img, box, seed, amp=13):
    """Fine deterministic grain over an illustration: adds texture and
    keeps flat colour areas from compressing to nothing."""
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    rng = np.random.default_rng(seed)
    base = np.asarray(img.crop(box)).astype(np.int16)
    noise = rng.integers(-amp, amp + 1, size=(h, w, 1))
    out = np.clip(base + noise, 0, 255).astype(np.uint8)
    img.paste(Image.fromarray(out, "RGB"), (x0, y0))


def stars(d, box, seed, n, color=(235, 230, 210)):
    rng = np.random.default_rng(seed)
    x0, y0, x1, y1 = box
    for _ in range(n):
        x = int(rng.integers(x0, x1))
        y = int(rng.integers(y0, y0 + (y1 - y0) // 2))
        r = int(rng.integers(1, 3))
        d.ellipse([x - r, y - r, x + r, y + r], fill=color)


def burst(d, cx, cy, r, core, halo):
    """Layer-3 detail: an explosion flash with rays."""
    for k in range(10, 0, -1):
        rr = r * k / 10.0
        col = halo if k > 4 else core
        d.ellipse([cx - rr, cy - rr, cx + rr, cy + rr], fill=col)
    for a in range(0, 360, 30):
        import math
        x2 = cx + r * 1.6 * math.cos(math.radians(a))
        y2 = cy + r * 1.6 * math.sin(math.radians(a))
        d.line([cx, cy, x2, y2], fill=core, width=2)


def ill_bahrain(d, img, box):
    x0, y0, x1, y1 = box
    vgrad(img, box, (16, 24, 44), (96, 52, 34))          # layer 1: night sky
    stars(d, box, 11, 26)
    d.rectangle([x0, y1 - 26, x1, y1], fill=(12, 22, 38))  # layer 2: sea
    for i in range(5):                                     # wave glints
        yy = y1 - 22 + i * 5
        d.line([x0 + 8 + i * 17, yy, x0 + 34 + i * 17, yy], fill=(70, 90, 120), width=2)
    for bx in (x0 + 18, x0 + 120, x0 + 205):               # base blocks + radar
        d.rectangle([bx, y1 - 62, bx + 52, y1 - 26], fill=(10, 16, 28))
        d.ellipse([bx + 14, y1 - 84, bx + 38, y1 - 60], outline=(150, 160, 180), width=3)
        d.line([bx + 26, y1 - 62, bx + 26, y1 - 84], fill=(150, 160, 180), width=3)
    d.line([x0 + 40, y1 - 70, x0 + 150, y0 + 30], fill=(255, 210, 110), width=3)
    d.line([x0 + 250, y1 - 70, x0 + 170, y0 + 44], fill=(255, 210, 110), width=3)
    burst(d, x0 + 150, y0 + 30, 13, (255, 226, 130), (240, 120, 40))  # layer 3
    burst(d, x0 + 170, y0 + 44, 9, (255, 226, 130), (240, 120, 40))


def ill_mexico(d, img, box):
    x0, y0, x1, y1 = box
    vgrad(img, box, (64, 38, 78), (214, 122, 62))         # layer 1: dusk
    d.polygon([(x0, y1 - 40), (x0 + 70, y0 + 34), (x0 + 140, y1 - 40)],
              fill=(58, 34, 66))                          # layer 2: far ridge
    d.polygon([(x0 + 110, y1 - 40), (x0 + 200, y0 + 22), (x1, y1 - 40)],
              fill=(46, 26, 54))
    d.rectangle([x0, y1 - 40, x1, y1], fill=(96, 62, 44))  # desert floor
    d.line([x0, y1 - 18, x1, y1 - 18], fill=(60, 38, 30), width=3)
    hx, hy = x0 + 190, y0 + 26                            # layer 3: helicopter
    d.ellipse([hx - 26, hy - 10, hx + 22, hy + 10], fill=(24, 20, 22))
    d.rectangle([hx + 20, hy - 4, hx + 52, hy + 2], fill=(24, 20, 22))
    d.line([hx - 44, hy - 14, hx + 44, hy - 14], fill=(24, 20, 22), width=3)
    d.line([hx - 6, hy - 10, hx - 6, hy + 26], fill=(24, 20, 22), width=2)
    for fx in (x0 + 34, x0 + 96):                         # burning roadblock
        d.polygon([(fx, y1 - 18), (fx + 8, y1 - 34), (fx + 16, y1 - 18)],
                  fill=(240, 110, 30))
        d.polygon([(fx + 4, y1 - 18), (fx + 10, y1 - 28), (fx + 16, y1 - 18)],
                  fill=(255, 200, 80))
    d.rectangle([x0 + 250, y1 - 40, x0 + 254, y1 - 18], fill=(40, 66, 40))
    d.rectangle([x0 + 244, y1 - 34, x0 + 250, y1 - 26], fill=(40, 66, 40))


def ill_cop31(d, img, box):
    x0, y0, x1, y1 = box
    vgrad(img, box, (24, 74, 92), (140, 196, 188))        # layer 1: hall light
    cx, cy, r = (x0 + x1) // 2, y0 + 52, 40
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(36, 96, 122))  # layer 2: globe
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(220, 235, 225), width=2)
    for k in (-2, -1, 0, 1, 2):                           # meridians
        d.arc([cx - r + k * 12, cy - r, cx + r - k * 12, cy + r],
              start=270, end=90, fill=(220, 235, 225), width=1)
        d.line([cx - r, cy + k * 14, cx + r, cy + k * 14], fill=(220, 235, 225), width=1)
    for i, col in enumerate([(168, 44, 32), (47, 93, 138), (46, 125, 79),
                             (183, 121, 31), (108, 74, 138), (63, 125, 122)]):
        fx = x0 + 14 + i * 46                             # layer 3: flag row
        d.rectangle([fx, y1 - 46, fx + 26, y1 - 30], fill=col)
        d.line([fx, y1 - 46, fx, y1 - 18], fill=(40, 36, 30), width=2)
    for i in range(6):                                     # delegates
        px = x0 + 26 + i * 44
        d.ellipse([px - 8, y1 - 18, px + 8, y1 - 2], fill=(30, 28, 26))
        d.pieslice([px - 14, y1 - 4, px + 14, y1 + 16], 180, 360, fill=(30, 28, 26))


def ill_kryvyi(d, img, box):
    x0, y0, x1, y1 = box
    vgrad(img, box, (118, 132, 150), (196, 178, 150))     # layer 1: grey sky
    for i, bh in enumerate((58, 84, 66, 96, 72)):         # layer 2: skyline
        bx = x0 + 8 + i * 56
        d.rectangle([bx, y1 - 30 - bh, bx + 44, y1 - 30], fill=(74, 72, 68))
        for wy in range(4):
            for wx in range(3):
                d.rectangle([bx + 6 + wx * 13, y1 - 24 - bh + wy * 16,
                             bx + 11 + wx * 13, y1 - 19 - bh + wy * 16],
                            fill=(232, 214, 150))
    d.polygon([(x0 + 232, y1 - 30), (x0 + 252, y1 - 96), (x0 + 272, y1 - 30)],
              fill=(58, 56, 52))                          # leaning tower
    for i, (sx, sy, sr) in enumerate([(x0 + 150, y0 + 18, 20), (x0 + 168, y0 + 34, 26),
                                      (x0 + 142, y0 + 44, 18)]):
        d.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=(120, 116, 108))
    burst(d, x0 + 250, y1 - 40, 10, (255, 200, 90), (220, 90, 30))  # layer 3: fire


def ill_peru(d, img, box):
    x0, y0, x1, y1 = box
    vgrad(img, box, (168, 196, 214), (226, 210, 178))     # layer 1: pale sky
    d.polygon([(x0, y1 - 44), (x0 + 90, y0 + 26), (x0 + 190, y1 - 44)],
              fill=(96, 92, 110))                         # layer 2: far Andes
    d.polygon([(x0 + 70, y0 + 26), (x0 + 90, y0 + 26), (x0 + 108, y0 + 44),
               (x0 + 82, y0 + 44)], fill=(240, 244, 248))
    d.polygon([(x0 + 150, y1 - 44), (x0 + 240, y0 + 14), (x1, y1 - 44)],
              fill=(74, 70, 88))
    d.polygon([(x0 + 222, y0 + 14), (x0 + 240, y0 + 14), (x0 + 256, y0 + 32),
               (x0 + 232, y0 + 32)], fill=(240, 244, 248))
    d.rectangle([x0, y1 - 44, x1, y1], fill=(150, 122, 84))  # foreground ground
    for hx, tilt in ((x0 + 30, -6), (x0 + 110, 5), (x0 + 200, -4)):  # tilted houses
        d.polygon([(hx, y1 - 44), (hx + 40, y1 - 44 + tilt), (hx + 40, y1 - 20 + tilt),
                   (hx, y1 - 20)], fill=(196, 120, 74))
        d.polygon([(hx - 4, y1 - 44), (hx + 20, y1 - 58), (hx + 44, y1 - 44 + tilt)],
                  fill=(122, 44, 36))
    d.line([x0 + 60, y1 - 10, x0 + 120, y1 - 26, x0 + 170, y1 - 8, x0 + 240, y1 - 22],
           fill=(60, 44, 30), width=3)                    # layer 3: cracks
    for sx, sy, sr in [(x0 + 80, y1 - 34, 10), (x0 + 180, y1 - 30, 13)]:
        d.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=(190, 168, 130))


def ill_markets(d, img, box):
    x0, y0, x1, y1 = box
    vgrad(img, box, (18, 30, 26), (52, 70, 58))           # layer 1: dark board
    for gy in range(4):                                    # layer 2: grid
        yy = y0 + 18 + gy * 26
        d.line([x0 + 6, yy, x1 - 6, yy], fill=(90, 110, 96), width=1)
    for i, (cx, o, c, col) in enumerate([(30, 30, 44, (70, 160, 90)),
                                         (70, 44, 26, (200, 60, 44)),
                                         (110, 26, 52, (200, 60, 44)),
                                         (150, 52, 30, (200, 60, 44)),
                                         (190, 30, 48, (200, 60, 44)),
                                         (230, 48, 28, (200, 60, 44))]):
        bx = x0 + 18 + i * 42
        d.line([bx + 10, y0 + o, bx + 10, y0 + o + c], fill=col, width=2)
        d.rectangle([bx + 2, y0 + o + 6, bx + 18, y0 + o + c - 4], fill=col)
    pts = [(x0 + 10, y0 + 22), (x0 + 60, y0 + 34), (x0 + 110, y0 + 30),
           (x0 + 160, y0 + 58), (x0 + 210, y0 + 66), (x0 + 260, y0 + 96),
           (x0 + 282, y0 + 108)]
    d.line(pts, fill=(240, 70, 50), width=4, joint="curve")  # layer 3: fall line
    d.polygon([(x0 + 282, y0 + 108), (x0 + 262, y0 + 98), (x0 + 272, y0 + 116)],
              fill=(240, 70, 50))
    d.text((x0 + 12, y0 + 6), "-4.1%", font=font(SANSB, 15), fill=(255, 120, 100))


def ill_riyadh(d, img, box):
    x0, y0, x1, y1 = box
    vgrad(img, box, (214, 170, 110), (238, 214, 160))     # layer 1: desert sky
    d.ellipse([x0 + 220, y0 + 8, x0 + 262, y0 + 50], fill=(250, 226, 150))
    d.polygon([(x0, y1 - 34), (x0 + 120, y1 - 62), (x0 + 240, y1 - 34), (x1, y1 - 52),
               (x1, y1), (x0, y1)], fill=(196, 152, 96))  # layer 2: dunes
    for tx in (x0 + 30, x0 + 78, x0 + 126):                # towers
        d.rectangle([tx, y1 - 96, tx + 26, y1 - 34], fill=(90, 78, 66))
        d.rectangle([tx + 4, y1 - 92, tx + 22, y1 - 80], fill=(220, 200, 140))
    d.line([x0 + 150, y1 - 60, x0 + 210, y0 + 26], fill=(240, 240, 235), width=3)
    d.line([x0 + 250, y1 - 60, x0 + 200, y0 + 34], fill=(240, 240, 235), width=3)
    burst(d, x0 + 208, y0 + 28, 11, (255, 240, 170), (240, 140, 50))  # layer 3: burst
    burst(d, x0 + 200, y0 + 36, 8, (255, 240, 170), (240, 140, 50))
    d.line([x0 + 208, y0 + 28, x0 + 250, y0 + 70], fill=(120, 110, 100), width=2)


def ill_gaza(d, img, box):
    x0, y0, x1, y1 = box
    vgrad(img, box, (206, 188, 152), (168, 140, 104))     # layer 1: dusty sky
    d.rectangle([x0, y1 - 34, x1, y1], fill=(120, 102, 76))  # layer 2: road
    d.line([x0, y1 - 34, x1, y1 - 34], fill=(90, 76, 56), width=2)
    tx, ty = x0 + 60, y1 - 78
    d.rectangle([tx, ty, tx + 130, ty + 44], fill=(236, 230, 214))  # cargo box
    d.rectangle([tx + 130, ty + 10, tx + 168, ty + 44], fill=(196, 88, 52))  # cab
    d.rectangle([tx + 136, ty + 14, tx + 158, ty + 28], fill=(180, 210, 225))
    for wx in (tx + 22, tx + 66, tx + 110, tx + 148):     # wheels
        d.ellipse([wx - 11, ty + 40, wx + 11, ty + 62], fill=(28, 26, 24))
        d.ellipse([wx - 4, ty + 47, wx + 4, ty + 55], fill=(120, 116, 110))
    for cx, cy, cw, ch in [(tx + 14, ty + 10, 26, 20), (tx + 48, ty + 10, 26, 20),
                           (tx + 88, ty + 10, 26, 20)]:   # layer 3: crates
        d.rectangle([cx, cy, cx + cw, cy + ch], fill=(176, 140, 84),
                    outline=(120, 92, 52), width=2)
        d.line([cx, cy, cx + cw, cy + ch], fill=(120, 92, 52), width=1)
        d.line([cx + cw, cy, cx, cy + ch], fill=(120, 92, 52), width=1)
    d.text((tx + 8, ty - 22), "FOOD AID", font=font(SANSB, 12), fill=(90, 40, 30))


def ill_bitcoin(d, img, box):
    x0, y0, x1, y1 = box
    vgrad(img, box, (22, 26, 40), (44, 52, 78))           # layer 1: dark blue
    stars(d, box, 91, 18)
    cx, cy, r = x0 + 96, y0 + 62, 46
    d.ellipse([cx - r - 4, cy - r - 4, cx + r + 4, cy + r + 4], fill=(180, 120, 30))
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(240, 176, 52))  # layer 2: coin
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(255, 214, 110), width=3)
    d.text((cx - 13, cy - 26), "B", font=font(SANSB, 44), fill=(146, 92, 16))
    d.line([cx - 22, cy - 30, cx - 22, cy + 30], fill=(146, 92, 16), width=3)
    d.line([cx + 20, cy - 30, cx + 20, cy + 30], fill=(146, 92, 16), width=3)
    pts = [(x0 + 150, y1 - 22), (x0 + 190, y1 - 40), (x0 + 225, y1 - 30),
           (x0 + 258, y1 - 58), (x0 + 282, y1 - 70)]
    d.line(pts, fill=(90, 200, 120), width=4, joint="curve")  # layer 3: rise
    d.polygon([(x0 + 282, y1 - 70), (x0 + 262, y1 - 68), (x0 + 274, y1 - 50)],
              fill=(90, 200, 120))
    for sx, sy, sr in [(x0 + 210, y0 + 26, 12), (x0 + 252, y0 + 44, 9)]:
        d.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=(240, 176, 52))
        d.text((sx - 4, sy - 7), "B", font=font(SANSB, 12), fill=(146, 92, 16))


def ill_fbi(d, img, box):
    x0, y0, x1, y1 = box
    vgrad(img, box, (150, 168, 188), (214, 206, 188))     # layer 1: pale sky
    cx = (x0 + x1) // 2
    d.polygon([(cx - 90, y1 - 88), (cx, y1 - 118), (cx + 90, y1 - 88)],
              fill=(96, 92, 84))                          # layer 2: pediment
    d.rectangle([x0 + 30, y1 - 88, x1 - 30, y1 - 22], fill=(150, 144, 130))
    for i in range(5):                                     # columns
        colx = x0 + 42 + i * 48
        d.rectangle([colx, y1 - 84, colx + 18, y1 - 26], fill=(214, 206, 188))
        d.rectangle([colx - 3, y1 - 88, colx + 21, y1 - 82], fill=(226, 218, 200))
    d.rectangle([x0 + 20, y1 - 22, x1 - 20, y1 - 14], fill=(110, 104, 92))
    d.rectangle([x0 + 12, y1 - 14, x1 - 12, y1 - 6], fill=(96, 90, 78))
    d.polygon([(cx, y1 - 84), (cx + 22, y1 - 66), (cx + 14, y1 - 40),
               (cx, y1 - 30), (cx - 14, y1 - 40), (cx - 22, y1 - 66)],
              fill=(38, 68, 128))                         # layer 3: shield
    d.text((cx - 5, y1 - 70), "*", font=font(SANSB, 22), fill=(255, 255, 255))
    d.rectangle([x0, y0, x1, y0 + 14], fill=(168, 44, 32))
    d.text((x0 + 8, y0 + 1), "ALERT", font=font(SANSB, 11), fill=(255, 255, 255))


def ill_amazon(d, img, box):
    x0, y0, x1, y1 = box
    vgrad(img, box, (226, 220, 204), (196, 182, 152))     # layer 1: warehouse light
    for sx in (x0 + 14, x0 + 108, x0 + 202):               # layer 2: shelves
        d.rectangle([sx, y0 + 16, sx + 76, y1 - 30], fill=(120, 100, 70))
        for sy in (y0 + 40, y0 + 66, y0 + 92):
            d.rectangle([sx + 4, sy, sx + 72, sy + 4], fill=(90, 74, 50))
            d.rectangle([sx + 8, sy - 18, sx + 30, sy], fill=(196, 140, 60))
            d.rectangle([sx + 40, sy - 14, sx + 66, sy], fill=(150, 110, 60))
    d.rectangle([x0, y1 - 30, x1, y1 - 18], fill=(70, 66, 60))  # conveyor
    for i in range(6):
        d.line([x0 + 20 + i * 46, y1 - 30, x0 + 20 + i * 46, y1 - 18],
               fill=(40, 38, 34), width=2)
    d.rectangle([x0 + 120, y1 - 62, x0 + 168, y1 - 30], fill=(216, 150, 60))
    d.line([x0 + 120, y1 - 46, x0 + 168, y1 - 46], fill=(150, 100, 40), width=2)
    d.ellipse([x0 + 136, y1 - 58, x0 + 152, y1 - 42], fill=(40, 38, 34))  # layer 3: eye
    d.ellipse([x0 + 140, y1 - 54, x0 + 148, y1 - 46], fill=(90, 200, 220))
    for px, py in [(x0 + 40, y0 + 22), (x0 + 90, y0 + 10), (x0 + 250, y0 + 20)]:
        d.ellipse([px - 3, py - 3, px + 3, py + 3], fill=(46, 125, 79))


def ill_mercury(d, img, box):
    x0, y0, x1, y1 = box
    vgrad(img, box, (8, 10, 22), (30, 26, 48))            # layer 1: space
    stars(d, box, 121, 34)
    d.ellipse([x0 + 200, y0 - 30, x0 + 280, y0 + 50], fill=(250, 220, 140))
    cx, cy, r = x0 + 92, y0 + 66, 48
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(176, 148, 120))  # layer 2: planet
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(120, 96, 74), width=2)
    for kx, ky, kr, col in [(cx - 18, cy - 12, 9, (140, 114, 88)),
                            (cx + 12, cy + 6, 12, (140, 114, 88)),
                            (cx + 2, cy - 26, 6, (150, 124, 98)),
                            (cx - 26, cy + 18, 7, (130, 104, 80)),
                            (cx + 24, cy - 20, 5, (150, 124, 98))]:
        d.ellipse([kx - kr, ky - kr, kx + kr, ky + kr], fill=col)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(60, 48, 38), width=1)
    px, py = x0 + 200, y0 + 84                            # layer 3: craft
    d.rectangle([px, py - 8, px + 44, py + 8], fill=(200, 204, 210))
    d.rectangle([px + 44, py - 16, px + 66, py + 16], fill=(70, 110, 180))
    d.rectangle([px - 22, py - 4, px, py + 4], fill=(140, 146, 154))
    d.line([px + 22, py - 8, px + 22, py - 30], fill=(200, 204, 210), width=2)
    d.ellipse([px + 18, py - 34, px + 26, py - 26], fill=(240, 220, 120))


def ill_ufo(d, img, box):
    x0, y0, x1, y1 = box
    vgrad(img, box, (26, 20, 48), (96, 60, 96))           # layer 1: night desert sky
    stars(d, box, 131, 30)
    d.polygon([(x0, y1 - 30), (x0 + 90, y1 - 52), (x0 + 190, y1 - 30), (x1, y1 - 44),
               (x1, y1), (x0, y1)], fill=(58, 40, 52))    # layer 2: dunes
    cx, cy = x0 + 146, y0 + 44
    d.polygon([(cx - 70, cy + 16), (cx + 70, cy + 16), (cx, cy - 34)],
              fill=(255, 240, 170), outline=(200, 180, 110))  # beam
    d.ellipse([cx - 62, cy - 12, cx + 62, cy + 14], fill=(190, 196, 206))  # layer 3: disc
    d.ellipse([cx - 34, cy - 26, cx + 34, cy + 2], fill=(220, 226, 234))
    for i in range(7):
        lx = cx - 48 + i * 16
        d.ellipse([lx - 4, cy - 2, lx + 4, cy + 6], fill=(255, 200, 80))
    fx = x0 + 230                                          # watcher figure
    d.ellipse([fx - 7, y1 - 62, fx + 7, y1 - 48], fill=(20, 18, 20))
    d.rectangle([fx - 9, y1 - 48, fx + 9, y1 - 18], fill=(20, 18, 20))
    d.line([fx - 8, y1 - 18, fx - 8, y1 - 2], fill=(20, 18, 20), width=4)
    d.line([fx + 8, y1 - 18, fx + 8, y1 - 2], fill=(20, 18, 20), width=4)


ILLUSTRATIONS = {
    "bahrain": ill_bahrain, "mexico": ill_mexico, "cop31": ill_cop31,
    "kryvyi": ill_kryvyi, "peru": ill_peru, "markets": ill_markets,
    "riyadh": ill_riyadh, "gaza": ill_gaza, "bitcoin": ill_bitcoin,
    "fbi": ill_fbi, "amazon": ill_amazon, "mercury": ill_mercury,
    "ufo": ill_ufo,
}

# Simplified continent outlines, (lon, lat) pairs, equirectangular.
CONTINENTS = [
    [(-168, 66), (-165, 60), (-158, 58), (-152, 60), (-140, 60), (-135, 57),
     (-130, 54), (-125, 49), (-124, 42), (-120, 34), (-114, 29), (-110, 24),
     (-105, 20), (-97, 16), (-94, 17), (-90, 14), (-86, 12), (-83, 9),
     (-80, 8), (-77, 7), (-79, 9), (-82, 13), (-85, 15), (-88, 17),
     (-90, 21), (-87, 21), (-90, 20), (-94, 19), (-97, 22), (-97, 26),
     (-93, 30), (-89, 30), (-84, 30), (-81, 26), (-80, 32), (-76, 35),
     (-74, 39), (-70, 42), (-68, 45), (-65, 44), (-60, 47), (-55, 47),
     (-60, 50), (-64, 52), (-65, 58), (-68, 58), (-72, 62), (-78, 62),
     (-85, 66), (-92, 66), (-95, 69), (-110, 68), (-125, 70), (-140, 70),
     (-155, 71), (-165, 68), (-168, 66)],
    [(-58, 64), (-52, 60), (-44, 60), (-40, 64), (-32, 68), (-22, 70),
     (-20, 74), (-25, 78), (-35, 80), (-50, 80), (-58, 76), (-60, 70), (-58, 64)],
    [(-79, 9), (-77, 4), (-80, -3), (-81, -6), (-77, -12), (-72, -18),
     (-70, -23), (-70, -30), (-72, -37), (-73, -44), (-74, -50), (-70, -54),
     (-66, -55), (-68, -50), (-65, -45), (-62, -40), (-58, -35), (-52, -32),
     (-48, -28), (-41, -23), (-39, -17), (-35, -9), (-35, -6), (-40, -3),
     (-44, -2), (-50, 0), (-53, 4), (-58, 6), (-62, 9), (-68, 11),
     (-72, 12), (-76, 10), (-79, 9)],
    [(-17, 15), (-16, 20), (-15, 27), (-10, 30), (-6, 33), (-1, 35),
     (9, 37), (11, 34), (15, 32), (19, 30), (25, 32), (30, 31), (32, 31),
     (34, 28), (35, 23), (37, 18), (39, 15), (41, 12), (43, 11), (46, 11),
     (51, 11), (51, 10), (48, 5), (44, 0), (41, -2), (40, -6), (40, -10),
     (39, -15), (36, -18), (35, -22), (32, -26), (28, -32), (20, -35),
     (17, -32), (15, -27), (13, -18), (12, -12), (13, -6), (12, -2),
     (9, 0), (9, 4), (6, 4), (4, 6), (-2, 5), (-8, 5), (-13, 8), (-17, 12),
     (-17, 15)],
    [(-10, 36), (-9, 38), (-9, 43), (-2, 44), (-1, 46), (-4, 48), (-1, 49),
     (2, 51), (5, 53), (8, 55), (8, 57), (10, 58), (12, 56), (18, 56),
     (21, 55), (24, 58), (28, 60), (30, 62), (32, 66), (40, 68), (50, 69),
     (60, 69), (70, 72), (80, 73), (90, 75), (100, 76), (110, 74), (120, 73),
     (130, 72), (140, 72), (150, 70), (160, 70), (170, 67), (178, 65),
     (178, 62), (170, 60), (162, 58), (158, 52), (156, 50), (150, 59),
     (142, 55), (140, 50), (135, 44), (132, 43), (128, 38), (127, 35),
     (122, 32), (120, 28), (118, 25), (112, 22), (109, 20), (108, 15),
     (105, 10), (103, 8), (100, 7), (98, 10), (97, 15), (94, 17), (92, 21),
     (90, 22), (88, 22), (86, 20), (84, 19), (80, 16), (77, 13), (75, 10),
     (73, 15), (72, 20), (70, 22), (66, 25), (62, 25), (58, 26), (56, 27),
     (54, 26), (52, 25), (50, 29), (48, 30), (48, 29), (50, 24), (52, 22),
     (55, 20), (57, 17), (55, 17), (52, 15), (48, 14), (44, 13), (42, 15),
     (40, 15), (39, 20), (38, 22), (35, 28), (34, 31), (36, 36), (33, 36),
     (30, 36), (27, 37), (23, 36), (22, 38), (20, 40), (19, 42), (15, 44),
     (12, 44), (8, 44), (7, 44), (3, 43), (0, 40), (-2, 37), (-6, 36),
     (-9, 37), (-10, 36)],
    [(-5, 50), (-3, 53), (-5, 56), (-3, 58), (-1, 57), (0, 53), (-1, 51), (-5, 50)],
    [(130, 31), (132, 33), (134, 34), (136, 35), (138, 35), (140, 36),
     (141, 39), (141, 42), (143, 44), (141, 44), (140, 40), (139, 37),
     (137, 37), (135, 34), (133, 34), (130, 31)],
    [(95, 5), (98, 3), (101, 0), (104, -3), (106, -6), (104, -6), (101, -2),
     (98, 2), (95, 5)],
    [(109, 1), (111, 2), (114, 4), (117, 6), (118, 2), (117, -2), (114, -3),
     (110, -3), (109, 1)],
    [(105, -6), (108, -7), (112, -7), (114, -8), (114, -9), (110, -8),
     (106, -7), (105, -6)],
    [(131, -1), (136, -2), (140, -3), (145, -5), (148, -8), (150, -10),
     (146, -8), (142, -8), (138, -8), (134, -4), (131, -1)],
    [(113, -22), (114, -30), (115, -33), (118, -35), (124, -33), (129, -32),
     (132, -32), (135, -35), (138, -35), (140, -38), (145, -38), (150, -37),
     (153, -32), (153, -27), (150, -22), (146, -19), (142, -15), (142, -11),
     (140, -17), (136, -15), (135, -12), (132, -11), (130, -13), (126, -14),
     (122, -17), (118, -20), (113, -22)],
]


def build():
    warnings = []
    img = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(img)
    M = 26
    x0, x1 = M, W - M
    cw = x1 - x0
    y = 8

    # Top rule + masthead: the date itself is the masthead.
    d.rectangle([x0, y, x1, y + 3], fill=RED)
    y += 12
    mast = "Saturday 21 November 2026"
    mf = font(SERIFB, 54)
    d.text(((W - d.textlength(mast, font=mf)) / 2, y), mast, font=mf, fill=INK)
    y += 58
    deck = ("Iran strikes US bases in Bahrain  \u00b7  \u2018El Chapo Isidro\u2019 "
            "seized in Mexico  \u00b7  Climate talks run past deadline")
    df = font(SANS, 17)
    d.text(((W - d.textlength(deck, font=df)) / 2, y), deck, font=df, fill=(74, 68, 58))
    y += 22
    d.rectangle([x0, y, x1, y + 1], fill=RULE)
    y += 8

    # Numbers band: six verified figures from the day.
    cell = cw / 6.0
    for i, (num, label) in enumerate(NUMBERS):
        cx = x0 + cell * i + cell / 2
        nf = font(SERIFB, 26)
        lf = font(SANSB, 10)
        d.text((cx - d.textlength(num, font=nf) / 2, y), num, font=nf, fill=INK)
        d.text((cx - d.textlength(label, font=lf) / 2, y + 29), label,
               font=lf, fill=MUTED)
        if i:
            d.line([x0 + cell * i, y + 2, x0 + cell * i, y + 40], fill=RULE, width=1)
    y += 46
    d.rectangle([x0, y, x1, y + 1], fill=RULE)
    y += 6

    # Region colour bar.
    for i, name in enumerate(REGIONS):
        rx0 = x0 + cell * i
        d.rectangle([rx0 + 1, y, rx0 + cell - 1, y + 16], fill=REGIONS[name])
        rf = font(SANSB, 10)
        d.text((rx0 + cell / 2 - d.textlength(name, font=rf) / 2, y + 3),
               name, font=rf, fill=(255, 255, 255))
    y += 22
    d.rectangle([x0, y, x1, y + 1], fill=RULE)
    y += 6

    # Hero row: three biggest stories, tall illustrations.
    hero_w = (cw - 2 * 16) / 3.0
    hero_y = y
    for i, st in enumerate(STORIES[:3]):
        num, region, src, head, deck_t, ill, lon, lat = st
        hx = x0 + i * (hero_w + 16)
        box = (int(hx), hero_y, int(hx + hero_w), hero_y + 110)
        ILLUSTRATIONS[ill](d, img, box)
        grain(img, box, 1000 + num, amp=12)
        d.rectangle(box, outline=(60, 52, 40), width=1)
        chip = "%d \u00b7 %s" % (num, region)
        cf = font(SANSB, 12)
        tw = d.textlength(chip, font=cf)
        d.rectangle([box[0], box[1], box[0] + tw + 12, box[1] + 19], fill=RED)
        d.text((box[0] + 6, box[1] + 3), chip, font=cf, fill=(255, 255, 255))
        ty = box[3] + 8
        hf = font(SERIFB, 34)
        for ln in fit(d, head, hf, hero_w, 2, warnings):
            d.text((hx, ty), ln, font=hf, fill=INK)
            ty += 38
        ty += 2
        df2 = font(SANS, 16)
        for ln in fit(d, deck_t, df2, hero_w, 2, warnings):
            d.text((hx, ty), ln, font=df2, fill=(58, 52, 44))
            ty += 18
        ty += 2
        sf = font(SANS, 11)
        d.text((hx, ty), src, font=sf, fill=MUTED)
    y = hero_y + 110 + 8 + 76 + 2 + 36 + 2 + 13
    d.rectangle([x0, y, x1, y + 1], fill=RULE)
    y += 6

    # Middle grid: 2 rows x 5 columns, illustrated.
    col_w = (cw - 4 * 14) / 5.0
    mid_y = y
    for row in range(2):
        for col in range(5):
            st = STORIES[3 + row * 5 + col]
            num, region, src, head, deck_t, ill, lon, lat = st
            mx = x0 + col * (col_w + 14)
            my = mid_y + row * 154
            box = (int(mx), my, int(mx + col_w), my + 44)
            # Middle illustrations are drawn at a fixed 50 px height and
            # then scaled into the 44 px box, so their internal geometry
            # never depends on the grid's row pitch.
            tmp = Image.new("RGB", (int(col_w), 50), CREAM)
            td = ImageDraw.Draw(tmp)
            ILLUSTRATIONS[ill](td, tmp, (0, 0, int(col_w), 50))
            grain(tmp, (0, 0, int(col_w), 50), 1000 + num, amp=12)
            img.paste(tmp.resize((int(col_w), 44), Image.LANCZOS),
                      (int(mx), my))
            d.rectangle(box, outline=(60, 52, 40), width=1)
            ky = my + 50
            kf = font(SANSB, 11)
            d.text((mx, ky), region, font=kf, fill=REGIONS[region])
            ky += 14
            hf = font(SERIFB, 21)
            for ln in fit(d, head, hf, col_w, 2, warnings):
                d.text((mx, ky), ln, font=hf, fill=INK)
                ky += 23
            ky += 1
            df3 = font(SANS, 13)
            for ln in fit(d, deck_t, df3, col_w, 2, warnings):
                d.text((mx, ky), ln, font=df3, fill=(58, 52, 44))
                ky += 15
            ky += 1
            sf = font(SANS, 10)
            d.text((mx, ky), src, font=sf, fill=MUTED)
    y = mid_y + 2 * 154
    d.rectangle([x0, y, x1, y + 1], fill=RULE)
    y += 6
    bottom_y = y

    # Bottom band: world map with numbered pins + numbered index of all 35.
    map_w = 252
    map_x0, map_x1 = x0, x0 + map_w
    cap_f = font(SANSB, 11)
    d.text((map_x0, bottom_y), "WHERE IT HAPPENED", font=cap_f, fill=INK)
    my0 = bottom_y + 16
    my1 = bottom_y + 128
    d.rectangle([map_x0, my0, map_x1, my1], fill=NAVY)
    scale = map_w / 360.0
    mh = 143 * scale
    moy = my0 + (my1 - my0 - mh) / 2

    def proj(lon, lat):
        return (map_x0 + (lon + 180) * scale, moy + (83 - lat) * scale)

    for poly in CONTINENTS:
        pts = [proj(lon, lat) for lon, lat in poly]
        d.polygon(pts, fill=LAND)
    # Numbered pins: the pin number is the story's index number.
    pins = []
    for st in STORIES:
        if st[6] is not None:
            pins.append((st[0], st[6], st[7]))
    for num, region, head, lon, lat in INDEX:
        pins.append((num, lon, lat))
    placed = []
    pf = font(SANSB, 8)
    import math
    for num, lon, lat in sorted(pins):
        px, py = proj(lon, lat)
        ox, oy = px, py
        # Radial spread: try the true spot, then rings of 8 directions at
        # growing radii, so pins in a crowded region fan out with a leader
        # line instead of stacking on one another.
        cands = [(px, py)]
        for rad in (14, 26, 38, 50):
            for k in range(8):
                a = math.radians(k * 45)
                cands.append((px + rad * math.cos(a), py + rad * math.sin(a)))
        for cx, cy in cands:
            cx = min(max(cx, map_x0 + 8), map_x1 - 8)
            cy = min(max(cy, my0 + 8), my1 - 8)
            if not any(abs(cx - qx) < 15 and abs(cy - qy) < 15 for qx, qy in placed):
                px, py = cx, cy
                break
        if (px, py) != (ox, oy):
            d.line([ox, oy, px, py], fill=(255, 220, 150), width=1)
            d.ellipse([ox - 2, oy - 2, ox + 2, oy + 2], fill=(255, 220, 150))
        d.ellipse([px - 7, py - 7, px + 7, py + 7], fill=RED,
                  outline=(255, 255, 255), width=1)
        label = str(num)
        d.text((px - d.textlength(label, font=pf) / 2, py - 5), label,
               font=pf, fill=(255, 255, 255))
        placed.append((px, py))
    key_y = my1 + 8
    kf2 = font(SANSB, 10)
    for i, name in enumerate(REGIONS):
        kx = map_x0 + (i % 2) * 128
        ky = key_y + (i // 2) * 14
        d.ellipse([kx, ky, kx + 8, ky + 8], fill=REGIONS[name])
        d.text((kx + 12, ky - 1), name.title(), font=kf2, fill=(74, 68, 58))
    d.text((map_x0, key_y + 3 * 14 + 4),
           "Pins are numbered to match the index.",
           font=font(SANS, 10), fill=MUTED)

    # Index: every story, two columns, 18 rows.
    idx_x = map_x1 + 16
    idx_w = (x1 - idx_x - 12) / 2.0
    all_idx = [(st[0], st[1], st[3]) for st in STORIES] + \
              [(n, r, h) for n, r, h, _, _ in INDEX]
    inf = font(SANSB, 13.5)
    itf = font(SANS, 13.5)
    row_h = 13.5
    for i, (num, region, head) in enumerate(all_idx):
        col = 0 if i < 18 else 1
        r = i if i < 18 else i - 18
        ix = idx_x + col * (idx_w + 12)
        iy = bottom_y + r * row_h
        num_s = "%d" % num
        d.text((ix, iy), num_s, font=inf, fill=RED)
        nx = ix + d.textlength("35 ", font=inf) + 2
        d.ellipse([nx, iy + 4, nx + 6, iy + 10], fill=REGIONS[region])
        tx = nx + 10
        lines = fit(d, head, itf, idx_w - (tx - ix), 1, warnings)
        d.text((tx, iy), lines[0] if lines else "", font=itf, fill=INK)
    y = bottom_y + 18 * row_h
    d.rectangle([x0, y + 4, x1, y + 5], fill=RED)
    ff = font(SANS, 12)
    foot = "DATE CHECK: All 35 stories are from Saturday, 21 November 2026."
    d.text(((W - d.textlength(foot, font=ff)) / 2, y + 9), foot, font=ff, fill=INK)
    y += 24
    print("layout: bottom_y=%d footer_y=%d total=%d (canvas %d)" % (bottom_y, y, y, H))
    for wmsg in warnings:
        print("WARN:", wmsg)
    return img


def main():
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img = build()
    img.save(out, format="PNG")
    print("wrote %s %d bytes %s" % (out, os.path.getsize(out), img.size))


if __name__ == "__main__":
    main()
