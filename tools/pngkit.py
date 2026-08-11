"""
Minimal PNG writer with a supersampling rasteriser.

No image library. `save()` takes a shader — a function of unit coordinates
(u, v) in [0,1) returning an (r, g, b) tuple or None for transparent — samples
it on a subpixel grid, and writes a true-colour-with-alpha PNG.

Antialiasing comes from averaging the subsamples: colour is weighted by
coverage, alpha is the covered fraction of the pixel.
"""
import struct
import zlib


def save(path, size, shader, ss=4):
    """Render `shader` at `size`x`size` with `ss`x`ss` supersampling."""
    rows = []
    n_sub = ss * ss
    for py in range(size):
        row = bytearray()
        for px in range(size):
            ar = ag = ab = aa = 0.0
            for sy in range(ss):
                for sx in range(ss):
                    u = (px + (sx + 0.5) / ss) / size
                    v = (py + (sy + 0.5) / ss) / size
                    c = shader(u, v)
                    if c is None:
                        continue
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
           + chunk(b"IHDR", struct.pack(">IIBBBBB", size, size, 8, 6, 0, 0, 0))
           + chunk(b"IDAT", zlib.compress(raw, 9))
           + chunk(b"IEND", b""))

    with open(path, "wb") as f:
        f.write(png)
    return len(png)


def rect(u, v, x0, y0, x1, y1):
    return x0 <= u <= x1 and y0 <= v <= y1


def rounded_square(u, v, r):
    """Coverage test for a unit square with corner radius r."""
    cx = min(max(u, r), 1 - r)
    cy = min(max(v, r), 1 - r)
    return (u - cx) ** 2 + (v - cy) ** 2 <= r * r


def frame(u, v, inset, thickness):
    """Hairline rectangular frame inset from the edges."""
    a, b = inset, 1 - inset
    if not rect(u, v, a, a, b, b):
        return False
    t = thickness
    return not rect(u, v, a + t, a + t, b - t, b - t)
