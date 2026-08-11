"""
Generate the Kestrel Aviation mark: an amber double chevron on an ink tile.

Writes the PNG directly with zlib — no image library. Shapes are drawn as
geometry and rasterised with 4x supersampling for antialiased edges.
"""
import zlib, struct, math, os

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                   "assets", "kestrel.png")
S, SS = 96, 4
INK, AMBER = (10, 14, 20), (240, 162, 2)

# Double chevron, apex up. Each band is the region between two parallel V's.
SLOPE, THICK = 0.85, 0.145
BANDS = (0.22, 0.45)
U0, U1 = 0.17, 0.83


def in_mark(u, v):
    if not (U0 <= u <= U1):
        return False
    f = SLOPE * abs(u - 0.5)
    return any(c + f <= v <= c + f + THICK for c in BANDS)


def in_tile(u, v, r=0.20):
    cx = min(max(u, r), 1 - r)
    cy = min(max(v, r), 1 - r)
    return (u - cx) ** 2 + (v - cy) ** 2 <= r * r


rows, n_sub = [], SS * SS
for py in range(S):
    row = bytearray()
    for px in range(S):
        ar = ag = ab = aa = 0.0
        for sy in range(SS):
            for sx in range(SS):
                u = (px + (sx + 0.5) / SS) / S
                v = (py + (sy + 0.5) / SS) / S
                if not in_tile(u, v):
                    continue
                c = AMBER if in_mark(u, v) else INK
                ar += c[0]; ag += c[1]; ab += c[2]; aa += 1.0
        if aa == 0:
            row += bytes((0, 0, 0, 0))
        else:
            row += bytes((round(ar / aa), round(ag / aa), round(ab / aa),
                          round(255 * aa / n_sub)))
    rows.append(row)

raw = b"".join(b"\x00" + bytes(r) for r in rows)


def chunk(tag, data):
    return (struct.pack(">I", len(data)) + tag + data
            + struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF))


png = (b"\x89PNG\r\n\x1a\n"
       + chunk(b"IHDR", struct.pack(">IIBBBBB", S, S, 8, 6, 0, 0, 0))
       + chunk(b"IDAT", zlib.compress(raw, 9))
       + chunk(b"IEND", b""))

os.makedirs(os.path.dirname(OUT), exist_ok=True)
with open(OUT, "wb") as f:
    f.write(png)
print("wrote %s (%d bytes)" % (OUT, len(png)))
