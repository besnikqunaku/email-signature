"""
Generate the Krasniqi & Dedaj mark: a brass portico inside a hairline frame,
on deep forest. Square corners — a crest for a law firm should not look soft.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pngkit  # noqa: E402

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                   "assets", "lawfirm.png")

FOREST, BRASS = (28, 61, 48), (176, 143, 74)

COLS = (0.325, 0.50, 0.675)   # column centres
CW = 0.042                    # half-width of a column


def shader(u, v):
    if not pngkit.rounded_square(u, v, 0.055):
        return None
    if pngkit.frame(u, v, 0.085, 0.022):
        return BRASS
    # Lintel
    if pngkit.rect(u, v, 0.235, 0.295, 0.765, 0.365):
        return BRASS
    # Columns
    if 0.365 <= v <= 0.675:
        for c in COLS:
            if c - CW <= u <= c + CW:
                return BRASS
    # Stylobate
    if pngkit.rect(u, v, 0.235, 0.675, 0.765, 0.745):
        return BRASS
    return FOREST


os.makedirs(os.path.dirname(OUT), exist_ok=True)
n = pngkit.save(OUT, 96, shader, ss=4)
print("wrote %s (%d bytes)" % (OUT, n))
