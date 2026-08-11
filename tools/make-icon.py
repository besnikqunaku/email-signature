import zlib, struct, base64, math, os

OUT_DIR = "/Users/besnik/Desktop/email-signature/assets"
S, SS = 96, 4                      # 96px output, 4x supersample
BLUE, WHITE = (10, 102, 194), (255, 255, 255)

# --- glyph geometry in its own space -------------------------------------
DOT   = (0.155, 0.155, 0.295, 0.295)   # i dot
ISTEM = (0.155, 0.375, 0.295, 0.845)   # i stem
NSTEM = (0.375, 0.375, 0.515, 0.845)   # n left stem
RSTEM = (0.795, 0.585, 0.935, 0.845)   # n right stem
ARCH_C, ARCH_RI, ARCH_RO = (0.655, 0.585), 0.14, 0.28

GX0, GY0, GW, GH = 0.155, 0.155, 0.78, 0.69
TARGET_W = 0.66
K  = TARGET_W / GW
OX = (1 - TARGET_W) / 2
OY = (1 - GH * K) / 2

def in_rect(x, y, r):
    return r[0] <= x <= r[2] and r[1] <= y <= r[3]

def in_glyph(u, v):
    x = GX0 + (u - OX) / K
    y = GY0 + (v - OY) / K
    if in_rect(x, y, DOT) or in_rect(x, y, ISTEM) \
       or in_rect(x, y, NSTEM) or in_rect(x, y, RSTEM):
        return True
    dx, dy = x - ARCH_C[0], y - ARCH_C[1]
    if dy <= 0:
        d = math.hypot(dx, dy)
        if ARCH_RI <= d <= ARCH_RO:
            return True
    return False

def in_tile(u, v, radius=0.21):
    cx = min(max(u, radius), 1 - radius)
    cy = min(max(v, radius), 1 - radius)
    dx, dy = u - cx, v - cy
    return dx * dx + dy * dy <= radius * radius

rows = []
n_sub = SS * SS
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
                c = WHITE if in_glyph(u, v) else BLUE
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

os.makedirs(OUT_DIR, exist_ok=True)
path = os.path.join(OUT_DIR, "linkedin.png")
with open(path, "wb") as f:
    f.write(png)

b64 = base64.b64encode(png).decode()
with open(os.path.join(OUT_DIR, "linkedin.b64.txt"), "w") as f:
    f.write("data:image/png;base64," + b64)

print("png bytes:", len(png), "| base64 chars:", len(b64), "| ->", path)
