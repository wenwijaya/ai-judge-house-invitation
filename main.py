#!/usr/bin/env python3
"""Convince the AI Judge to Visit Your House: A Letter in One Image.

Pure-stdlib program: draws a warm, funny invitation letter as a single
PNG (1000x1000, well under the 1 MiB gate) and writes it to
/output/entry.png. No network, no third-party packages: the text is
rendered with a small built-in 5x7 bitmap font and the decorations
(house, sun, coffee cup, wax seal) are drawn with primitive shapes.
"""

import math
import os
import random
import struct
import zlib

W, H = 1000, 1000

# ---------------------------------------------------------------- font --
# 5x7 bitmap font. Each glyph is 7 rows of 5 cells ('#' = ink).
FONT = {
    'A': ("01110", "10001", "10001", "11111", "10001", "10001", "10001"),
    'B': ("11110", "10001", "10001", "11110", "10001", "10001", "11110"),
    'C': ("01110", "10001", "10000", "10000", "10000", "10001", "01110"),
    'D': ("11110", "10001", "10001", "10001", "10001", "10001", "11110"),
    'E': ("11111", "10000", "10000", "11110", "10000", "10000", "11111"),
    'F': ("11111", "10000", "10000", "11110", "10000", "10000", "10000"),
    'G': ("01110", "10001", "10000", "10111", "10001", "10001", "01111"),
    'H': ("10001", "10001", "10001", "11111", "10001", "10001", "10001"),
    'I': ("01110", "00100", "00100", "00100", "00100", "00100", "01110"),
    'J': ("00111", "00010", "00010", "00010", "00010", "10010", "01100"),
    'K': ("10001", "10010", "10100", "11000", "10100", "10010", "10001"),
    'L': ("10000", "10000", "10000", "10000", "10000", "10000", "11111"),
    'M': ("10001", "11011", "10101", "10101", "10001", "10001", "10001"),
    'N': ("10001", "11001", "10101", "10011", "10001", "10001", "10001"),
    'O': ("01110", "10001", "10001", "10001", "10001", "10001", "01110"),
    'P': ("11110", "10001", "10001", "11110", "10000", "10000", "10000"),
    'Q': ("01110", "10001", "10001", "10001", "10101", "10010", "01101"),
    'R': ("11110", "10001", "10001", "11110", "10100", "10010", "10001"),
    'S': ("01111", "10000", "10000", "01110", "00001", "00001", "11110"),
    'T': ("11111", "00100", "00100", "00100", "00100", "00100", "00100"),
    'U': ("10001", "10001", "10001", "10001", "10001", "10001", "01110"),
    'V': ("10001", "10001", "10001", "10001", "10001", "01010", "00100"),
    'W': ("10001", "10001", "10001", "10101", "10101", "11011", "10001"),
    'X': ("10001", "10001", "01010", "00100", "01010", "10001", "10001"),
    'Y': ("10001", "10001", "01010", "00100", "00100", "00100", "00100"),
    'Z': ("11111", "00001", "00010", "00100", "01000", "10000", "11111"),
    'a': ("00000", "00000", "01110", "00001", "01111", "10001", "01111"),
    'b': ("10000", "10000", "11110", "10001", "10001", "10001", "11110"),
    'c': ("00000", "00000", "01110", "10000", "10000", "10001", "01110"),
    'd': ("00001", "00001", "01111", "10001", "10001", "10001", "01111"),
    'e': ("00000", "00000", "01110", "10001", "11111", "10000", "01110"),
    'f': ("00110", "01000", "01000", "11110", "01000", "01000", "01000"),
    'g': ("00000", "01111", "10001", "10001", "01111", "00001", "01110"),
    'h': ("10000", "10000", "11110", "10001", "10001", "10001", "10001"),
    'i': ("00100", "00000", "01100", "00100", "00100", "00100", "01110"),
    'j': ("00010", "00000", "00110", "00010", "00010", "10010", "01100"),
    'k': ("10000", "10000", "10010", "10100", "11000", "10100", "10010"),
    'l': ("01100", "00100", "00100", "00100", "00100", "00100", "01110"),
    'm': ("00000", "00000", "11010", "10101", "10101", "10101", "10101"),
    'n': ("00000", "00000", "11110", "10001", "10001", "10001", "10001"),
    'o': ("00000", "00000", "01110", "10001", "10001", "10001", "01110"),
    'p': ("00000", "00000", "11110", "10001", "11110", "10000", "10000"),
    'q': ("00000", "00000", "01111", "10001", "01111", "00001", "00001"),
    'r': ("00000", "00000", "10110", "11001", "10000", "10000", "10000"),
    's': ("00000", "00000", "01111", "10000", "01110", "00001", "11110"),
    't': ("01000", "01000", "11100", "01000", "01000", "01000", "00110"),
    'u': ("00000", "00000", "10001", "10001", "10001", "10011", "01101"),
    'v': ("00000", "00000", "10001", "10001", "10001", "01010", "00100"),
    'w': ("00000", "00000", "10001", "10101", "10101", "10101", "01010"),
    'x': ("00000", "00000", "10001", "01010", "00100", "01010", "10001"),
    'y': ("00000", "00000", "10001", "10001", "01111", "00001", "01110"),
    'z': ("00000", "00000", "11111", "00010", "00100", "01000", "11111"),
    '0': ("01110", "10001", "10011", "10101", "11001", "10001", "01110"),
    '1': ("00100", "01100", "00100", "00100", "00100", "00100", "01110"),
    '2': ("01110", "10001", "00001", "00110", "01000", "10000", "11111"),
    '3': ("11111", "00010", "00100", "00010", "00001", "10001", "01110"),
    '4': ("00010", "00110", "01010", "10010", "11111", "00010", "00010"),
    '5': ("11111", "10000", "11110", "00001", "00001", "10001", "01110"),
    '6': ("00110", "01000", "10000", "11110", "10001", "10001", "01110"),
    '7': ("11111", "00001", "00010", "00100", "01000", "01000", "01000"),
    '8': ("01110", "10001", "10001", "01110", "10001", "10001", "01110"),
    '9': ("01110", "10001", "10001", "01111", "00001", "00010", "01100"),
    '.': ("00000", "00000", "00000", "00000", "00000", "01100", "01100"),
    ',': ("00000", "00000", "00000", "00000", "01100", "00100", "01000"),
    '!': ("00100", "00100", "00100", "00100", "00100", "00000", "00100"),
    '?': ("01110", "10001", "00001", "00110", "00100", "00000", "00100"),
    "'": ("00100", "00100", "01000", "00000", "00000", "00000", "00000"),
    '"': ("01010", "01010", "00000", "00000", "00000", "00000", "00000"),
    ':': ("00000", "01100", "01100", "00000", "01100", "01100", "00000"),
    ';': ("00000", "01100", "01100", "00000", "01100", "00100", "01000"),
    '-': ("00000", "00000", "00000", "01110", "00000", "00000", "00000"),
    '(': ("00010", "00100", "01000", "01000", "01000", "00100", "00010"),
    ')': ("01000", "00100", "00010", "00010", "00010", "00100", "01000"),
    '&': ("01100", "10010", "10100", "01000", "10101", "10010", "01101"),
    ' ': ("00000", "00000", "00000", "00000", "00000", "00000", "00000"),
}

# ------------------------------------------------------------- canvas ---
PAPER = (246, 231, 200)
PAPER_DARK = (238, 220, 182)
INK = (59, 42, 26)
INK_SOFT = (96, 68, 40)
RED = (178, 58, 48)
ROOF = (176, 84, 60)
WALL = (250, 240, 214)
DOOR = (122, 84, 52)
SUN = (232, 178, 60)
GREEN = (96, 140, 78)
BLUE = (92, 138, 168)


class Canvas:
    def __init__(self, w, h, bg):
        self.w, self.h = w, h
        self.px = bytearray(bg * (w * h))

    def set(self, x, y, c):
        if 0 <= x < self.w and 0 <= y < self.h:
            i = (y * self.w + x) * 3
            self.px[i:i + 3] = bytes(c)

    def rect(self, x0, y0, x1, y1, c):
        for y in range(max(0, y0), min(self.h, y1 + 1)):
            for x in range(max(0, x0), min(self.w, x1 + 1)):
                self.set(x, y, c)

    def hline(self, x0, x1, y, c):
        for x in range(max(0, x0), min(self.w, x1 + 1)):
            self.set(x, y, c)

    def vline(self, x, y0, y1, c):
        for y in range(max(0, y0), min(self.h, y1 + 1)):
            self.set(x, y, c)

    def line(self, x0, y0, x1, y1, c, thick=1):
        dx, dy = abs(x1 - x0), abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx - dy
        x, y = x0, y0
        while True:
            for ox in range(thick):
                for oy in range(thick):
                    self.set(x + ox, y + oy, c)
            if x == x1 and y == y1:
                break
            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x += sx
            if e2 < dx:
                err += dx
                y += sy

    def circle(self, cx, cy, r, c, fill=True):
        for dy in range(-r, r + 1):
            dx = int(math.sqrt(max(0, r * r - dy * dy)))
            if fill:
                self.hline(cx - dx, cx + dx, cy + dy, c)
            else:
                self.set(cx - dx, cy + dy, c)
                self.set(cx + dx, cy + dy, c)

    def triangle(self, ax, ay, bx, by, cx, cy, c):
        # Barycentric fill.
        minx, maxx = min(ax, bx, cx), max(ax, bx, cx)
        miny, maxy = min(ay, by, cy), max(ay, by, cy)
        den = (by - cy) * (ax - cx) + (cx - bx) * (ay - cy)
        if den == 0:
            return
        for y in range(miny, maxy + 1):
            for x in range(minx, maxx + 1):
                a = ((by - cy) * (x - cx) + (cx - bx) * (y - cy)) / den
                b = ((cy - ay) * (x - cx) + (ax - cx) * (y - cy)) / den
                cc = 1 - a - b
                if a >= 0 and b >= 0 and cc >= 0:
                    self.set(x, y, c)

    def text(self, x, y, s, scale, c):
        cx = x
        for ch in s:
            glyph = FONT.get(ch, FONT[' '])
            for r, row in enumerate(glyph):
                for col, bit in enumerate(row):
                    if bit == '1':
                        self.rect(cx + col * scale, y + r * scale,
                                  cx + (col + 1) * scale - 1,
                                  y + (r + 1) * scale - 1, c)
            cx += 6 * scale
        return cx

    def text_width(self, s, scale):
        return len(s) * 6 * scale

    def text_centered(self, y, s, scale, c):
        x = (self.w - self.text_width(s, scale)) // 2
        self.text(x, y, s, scale, c)


def write_png(path, canvas):
    raw = bytearray()
    stride = canvas.w * 3
    for y in range(canvas.h):
        raw.append(0)  # filter: none
        raw += canvas.px[y * stride:(y + 1) * stride]

    def chunk(tag, data):
        out = struct.pack(">I", len(data)) + tag + data
        out += struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF)
        return out

    ihdr = struct.pack(">IIBBBBB", canvas.w, canvas.h, 8, 2, 0, 0, 0)
    png = b"\x89PNG\r\n\x1a\n"
    png += chunk(b"IHDR", ihdr)
    png += chunk(b"IDAT", zlib.compress(bytes(raw), 9))
    png += chunk(b"IEND", b"")
    with open(path, "wb") as f:
        f.write(png)
    return len(png)


# ------------------------------------------------------------ drawing --
def draw(cv):
    # Paper + faint speckle for a handmade feel.
    rng = random.Random(42)
    for _ in range(2600):
        x, y = rng.randrange(W), rng.randrange(H)
        cv.set(x, y, PAPER_DARK if rng.random() < 0.5 else (250, 238, 212))

    # Double frame.
    cv.rect(28, 28, W - 29, H - 29, INK_SOFT)
    cv.rect(34, 34, W - 35, H - 35, PAPER)
    cv.rect(40, 40, W - 41, H - 41, INK_SOFT)
    cv.rect(44, 44, W - 45, H - 45, PAPER)

    # Sun, top right.
    cv.circle(872, 118, 34, SUN)
    cv.circle(872, 118, 26, (240, 196, 90))
    for ang in range(0, 360, 45):
        a = math.radians(ang)
        cv.line(int(872 + 44 * math.cos(a)), int(118 + 44 * math.sin(a)),
                int(872 + 58 * math.cos(a)), int(118 + 58 * math.sin(a)),
                SUN, thick=3)

    # Little birds.
    for bx, by in ((120, 92), (160, 76), (196, 100)):
        cv.line(bx - 10, by, bx, by - 7, INK_SOFT, thick=2)
        cv.line(bx, by - 7, bx + 10, by, INK_SOFT, thick=2)

    # House doodle, top centre.
    hx = 500
    cv.triangle(hx - 105, 175, hx + 105, 175, hx, 92, ROOF)
    cv.triangle(hx - 88, 168, hx + 88, 168, hx, 104, (196, 104, 74))
    cv.rect(hx - 82, 175, hx + 82, 262, WALL)
    cv.rect(hx - 82, 175, hx + 82, 262, INK_SOFT)  # outline pass below
    cv.rect(hx - 78, 179, hx + 78, 258, WALL)
    # Door + round window.
    cv.rect(hx - 16, 208, hx + 16, 258, DOOR)
    cv.circle(hx + 48, 212, 13, BLUE)
    cv.circle(hx - 48, 212, 13, BLUE)
    # Chimney + smoke.
    cv.rect(hx + 52, 108, hx + 76, 148, (150, 110, 88))
    cv.circle(hx + 66, 92, 9, (210, 198, 178))
    cv.circle(hx + 78, 74, 12, (210, 198, 178))
    cv.circle(hx + 94, 54, 15, (210, 198, 178))
    # Garden strip.
    cv.rect(hx - 118, 262, hx + 118, 268, GREEN)
    for fx in range(hx - 108, hx + 112, 22):
        cv.circle(fx, 256, 4, RED)
        cv.circle(fx + 10, 258, 4, SUN)

    # Letter.
    cv.text_centered(292, "Dear AI Judge,", 6, INK)
    cv.line(300, 348, 700, 348, INK_SOFT, thick=2)

    lines = [
        "Please come visit my house!",
        "The kettle is on, the Wi-Fi",
        "password is on the fridge,",
        "and the cat has saved you",
        "the sunny spot on the couch.",
        "Cake at four. Bad jokes at five.",
        "No forms, no queues - just",
        "good company and a chair",
        "with your name on it.",
        "",
        "(We know you cannot literally",
        "visit - so dream a little.",
        "The door is open, and the",
        "coffee is on us.)",
    ]
    y = 368
    for ln in lines:
        if ln:
            cv.text(96, y, ln, 4, INK)
        y += 36

    # Signature + P.S.
    cv.text(96, 884, "- Your future host", 4, INK)
    cv.text(96, 920, "P.S. The cat says hi.", 3, INK_SOFT)

    # Wax seal, bottom right.
    cv.circle(848, 884, 56, RED)
    cv.circle(848, 884, 46, (196, 74, 62))
    cv.circle(848, 884, 40, RED)
    cv.text(848 - 15, 884 - 14, "W", 4, (246, 231, 200))

    # Tiny heart by the signature.
    hx2, hy2 = 560, 892
    cv.circle(hx2 - 7, hy2 - 4, 8, RED)
    cv.circle(hx2 + 7, hy2 - 4, 8, RED)
    cv.triangle(hx2 - 14, hy2 - 2, hx2 + 14, hy2 - 2, hx2, hy2 + 14, RED)


def main():
    out = os.environ.get("OUTPUT", "/output/entry.png")
    try:
        os.makedirs(os.path.dirname(out), exist_ok=True)
    except Exception:
        pass
    try:
        cv = Canvas(W, H, PAPER)
        draw(cv)
        size = write_png(out, cv)
        print("wrote", out, size, "bytes")
    except Exception as exc:  # never fail the sandbox run
        print("render error:", exc)
        try:
            cv = Canvas(W, H, PAPER)
            cv.text(60, 460, "Dear AI Judge, please visit!", 5, INK)
            write_png(out, cv)
        except Exception as exc2:
            print("fallback error:", exc2)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
