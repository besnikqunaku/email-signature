"""
Generate the LinkedIn icon: the `in` glyph on a rounded blue tile.

The glyph is composed from the primitives it is actually made of — a square
dot, two stems and a half-ring arch — then scaled and centred in the tile.
"""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pngkit  # noqa: E402

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                   "assets", "linkedin.png")

BLUE, WHITE = (10, 102, 194), (255, 255, 255)

DOT = (0.155, 0.155, 0.295, 0.295)     # i dot
ISTEM = (0.155, 0.375, 0.295, 0.845)   # i stem
NSTEM = (0.375, 0.375, 0.515, 0.845)   # n left stem
RSTEM = (0.795, 0.585, 0.935, 0.845)   # n right stem
ARCH_C, ARCH_RI, ARCH_RO = (0.655, 0.585), 0.14, 0.28

GX0, GY0, GW, GH = 0.155, 0.155, 0.78, 0.69
TARGET_W = 0.66
K = TARGET_W / GW
OX = (1 - TARGET_W) / 2
OY = (1 - GH * K) / 2


def in_glyph(u, v):
    x = GX0 + (u - OX) / K
    y = GY0 + (v - OY) / K
    for r in (DOT, ISTEM, NSTEM, RSTEM):
        if pngkit.rect(x, y, *r):
            return True
    dx, dy = x - ARCH_C[0], y - ARCH_C[1]
    return dy <= 0 and ARCH_RI <= math.hypot(dx, dy) <= ARCH_RO


def shader(u, v):
    if not pngkit.rounded_square(u, v, 0.21):
        return None
    return WHITE if in_glyph(u, v) else BLUE


os.makedirs(os.path.dirname(OUT), exist_ok=True)
n = pngkit.save(OUT, 96, shader, ss=4)
print("wrote %s (%d bytes)" % (OUT, n))
