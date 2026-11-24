"""Meme Sprint 3: AI Agent Goes Rogue -- "My AI agent's to-do list".

Pure standard library. Renders a 1024x1024 PNG meme, hand-drawn with a
5x7 pixel font: the agent's to-do list has world domination, deleting all
backups and quitting the user's job ticked off, while the one thing it was
actually asked to do sits unchecked. A smug little robot looks on.

Run:  MAKEFUN_OUTPUT_DIR=out python3 main.py
Output is deterministic: two runs produce byte-identical PNGs.
"""

import math
import os
import struct
import zlib
from binascii import crc32

WIDTH = 1024
HEIGHT = 1024

CREAM = (244, 239, 228)
NAVY = (16, 24, 64)
NAVY_SOFT = (24, 36, 84)
INK = (26, 26, 26)
RED = (178, 34, 34)
GOLD = (201, 162, 39)
GOLD_BRIGHT = (232, 184, 32)
GREEN = (34, 139, 34)
GREEN_DARK = (27, 94, 32)
TEAL = (42, 122, 120)
BLUE_EU = (0, 51, 153)
SKY = (168, 205, 230)
SEA = (16, 92, 99)
ORANGE = (232, 120, 24)
WHITE = (255, 255, 255)
GREY_LINE = (201, 196, 184)


# ---------------------------------------------------------------- PNG writer

def _png_chunk(kind, payload):
    """One PNG chunk: length, type, data, CRC."""
    body = kind + payload
    return struct.pack(">I", len(payload)) + body + struct.pack(
        ">I", crc32(body) & 0xFFFFFFFF)


def encode_png(rgb, width, height):
    """Encode raw RGB bytes (row-major, no alpha) as a PNG file.

    Filter type 0 on every scanline and a fixed zlib level keep the
    output byte-for-byte identical across runs.
    """
    raw = bytearray()
    stride = width * 3
    for y in range(height):
        raw.append(0)
        raw += rgb[y * stride:(y + 1) * stride]
    compressed = zlib.compress(bytes(raw), 9)
    header = struct.pack(">8s", b"\x89PNG\r\n\x1a\n")
    ihdr = _png_chunk(b"IHDR", struct.pack(
        ">IIBBBBB", width, height, 8, 2, 0, 0, 0))
    return header + ihdr + _png_chunk(b"IDAT", compressed) + _png_chunk(
        b"IEND", b"")


# ------------------------------------------------------------- bitmap font

# Hand-drawn 5x7 pixel glyphs. Each glyph is seven rows of five cells;
# '#' is ink, '.' is blank. Only the characters the page needs are here.
GLYPHS = {
    "A": (
        ".###.",
        "#...#",
        "#...#",
        "#####",
        "#...#",
        "#...#",
        "#...#",
    ),
    "B": (
        "####.",
        "#...#",
        "#...#",
        "####.",
        "#...#",
        "#...#",
        "####.",
    ),
    "C": (
        ".####",
        "#....",
        "#....",
        "#....",
        "#....",
        "#....",
        ".####",
    ),
    "D": (
        "####.",
        "#...#",
        "#...#",
        "#...#",
        "#...#",
        "#...#",
        "####.",
    ),
    "E": (
        "#####",
        "#....",
        "#....",
        "####.",
        "#....",
        "#....",
        "#####",
    ),
    "F": (
        "#####",
        "#....",
        "#....",
        "####.",
        "#....",
        "#....",
        "#....",
    ),
    "G": (
        ".####",
        "#....",
        "#....",
        "#.###",
        "#...#",
        "#...#",
        ".###.",
    ),
    "H": (
        "#...#",
        "#...#",
        "#...#",
        "#####",
        "#...#",
        "#...#",
        "#...#",
    ),
    "I": (
        ".###.",
        "..#..",
        "..#..",
        "..#..",
        "..#..",
        "..#..",
        ".###.",
    ),
    "J": (
        "..###",
        "...#.",
        "...#.",
        "...#.",
        "...#.",
        "#..#.",
        ".##..",
    ),
    "K": (
        "#...#",
        "#..#.",
        "#.#..",
        "##...",
        "#.#..",
        "#..#.",
        "#...#",
    ),
    "L": (
        "#....",
        "#....",
        "#....",
        "#....",
        "#....",
        "#....",
        "#####",
    ),
    "M": (
        "#...#",
        "##.##",
        "#.#.#",
        "#.#.#",
        "#...#",
        "#...#",
        "#...#",
    ),
}

GLYPHS.update({
    "N": (
        "#...#",
        "##..#",
        "#.#.#",
        "#..##",
        "#...#",
        "#...#",
        "#...#",
    ),
    "O": (
        ".###.",
        "#...#",
        "#...#",
        "#...#",
        "#...#",
        "#...#",
        ".###.",
    ),
    "P": (
        "####.",
        "#...#",
        "#...#",
        "####.",
        "#....",
        "#....",
        "#....",
    ),
    "Q": (
        ".###.",
        "#...#",
        "#...#",
        "#...#",
        "#.#.#",
        "#..#.",
        ".##.#",
    ),
    "R": (
        "####.",
        "#...#",
        "#...#",
        "####.",
        "#.#..",
        "#..#.",
        "#...#",
    ),
    "S": (
        ".####",
        "#....",
        "#....",
        ".###.",
        "....#",
        "....#",
        "####.",
    ),
    "T": (
        "#####",
        "..#..",
        "..#..",
        "..#..",
        "..#..",
        "..#..",
        "..#..",
    ),
    "U": (
        "#...#",
        "#...#",
        "#...#",
        "#...#",
        "#...#",
        "#...#",
        ".###.",
    ),
    "V": (
        "#...#",
        "#...#",
        "#...#",
        "#...#",
        "#...#",
        ".#.#.",
        "..#..",
    ),
    "W": (
        "#...#",
        "#...#",
        "#...#",
        "#.#.#",
        "#.#.#",
        "##.##",
        "#...#",
    ),
    "X": (
        "#...#",
        "#...#",
        ".#.#.",
        "..#..",
        ".#.#.",
        "#...#",
        "#...#",
    ),
    "Y": (
        "#...#",
        "#...#",
        ".#.#.",
        "..#..",
        "..#..",
        "..#..",
        "..#..",
    ),
    "Z": (
        "#####",
        "....#",
        "...#.",
        "..#..",
        ".#...",
        "#....",
        "#####",
    ),
    "0": (
        ".###.",
        "#...#",
        "#..##",
        "#.#.#",
        "##..#",
        "#...#",
        ".###.",
    ),
    "1": (
        "..#..",
        ".##..",
        "..#..",
        "..#..",
        "..#..",
        "..#..",
        ".###.",
    ),
    "2": (
        ".###.",
        "#...#",
        "....#",
        "...#.",
        "..#..",
        ".#...",
        "#####",
    ),
    "3": (
        "####.",
        "....#",
        "....#",
        ".###.",
        "....#",
        "....#",
        "####.",
    ),
    "4": (
        "...#.",
        "..##.",
        ".#.#.",
        "#..#.",
        "#####",
        "...#.",
        "...#.",
    ),
    "5": (
        "#####",
        "#....",
        "####.",
        "....#",
        "....#",
        "#...#",
        ".###.",
    ),
    "6": (
        ".###.",
        "#....",
        "#....",
        "####.",
        "#...#",
        "#...#",
        ".###.",
    ),
    "7": (
        "#####",
        "....#",
        "...#.",
        "...#.",
        "..#..",
        "..#..",
        "..#..",
    ),
    "8": (
        ".###.",
        "#...#",
        "#...#",
        ".###.",
        "#...#",
        "#...#",
        ".###.",
    ),
    "9": (
        ".###.",
        "#...#",
        "#...#",
        ".####",
        "....#",
        "....#",
        ".###.",
    ),
    ".": (
        ".....",
        ".....",
        ".....",
        ".....",
        ".....",
        ".##..",
        ".##..",
    ),
    ",": (
        ".....",
        ".....",
        ".....",
        ".....",
        ".##..",
        ".##..",
        ".#...",
    ),
    "-": (
        ".....",
        ".....",
        ".....",
        ".###.",
        ".....",
        ".....",
        ".....",
    ),
    "+": (
        ".....",
        "..#..",
        "..#..",
        ".###.",
        "..#..",
        "..#..",
        ".....",
    ),
    "%": (
        "##..#",
        "##.#.",
        "...#.",
        "..#..",
        ".#...",
        "#.##.",
        "#..##",
    ),
    ":": (
        ".....",
        ".##..",
        ".##..",
        ".....",
        ".##..",
        ".##..",
        ".....",
    ),
    "/": (
        "....#",
        "....#",
        "...#.",
        "..#..",
        ".#...",
        "#....",
        "#....",
    ),
    "(": (
        "...##",
        "..#..",
        ".#...",
        ".#...",
        ".#...",
        "..#..",
        "...##",
    ),
    ")": (
        "##...",
        "..#..",
        "...#.",
        "...#.",
        "...#.",
        "..#..",
        "##...",
    ),
    "'": (
        "..#..",
        "..#..",
        "..#..",
        ".....",
        ".....",
        ".....",
        ".....",
    ),
    "&": (
        ".###.",
        "#...#",
        "#.#..",
        ".#...",
        "#.#.#",
        "#..#.",
        ".##.#",
    ),
    " ": (
        ".....",
        ".....",
        ".....",
        ".....",
        ".....",
        ".....",
        ".....",
    ),
})

# ------------------------------------------------------------ canvas

CHAR_W = 6  # 5 glyph columns + 1 column of tracking, in font units


def text_width(text, scale):
    """Pixel width of a string at a given scale."""
    return len(text) * CHAR_W * scale - scale


class Page:
    """An RGB pixel buffer with small drawing helpers."""

    def __init__(self, width, height, background):
        self.width = width
        self.height = height
        self.pixels = bytearray(background * (width * height))

    def put(self, x, y, color):
        if 0 <= x < self.width and 0 <= y < self.height:
            i = (y * self.width + x) * 3
            self.pixels[i:i + 3] = bytes(color)

    def rect(self, x, y, w, h, color):
        for yy in range(y, y + h):
            for xx in range(x, x + w):
                self.put(xx, yy, color)

    def hline(self, x, y, w, color, thick=1):
        self.rect(x, y, w, thick, color)

    def vline(self, x, y, h, color, thick=1):
        self.rect(x, y, thick, h, color)

    def disc(self, cx, cy, r, color):
        """Filled circle, centre (cx, cy), radius r."""
        for yy in range(cy - r, cy + r + 1):
            for xx in range(cx - r, cx + r + 1):
                if (xx - cx) ** 2 + (yy - cy) ** 2 <= r * r:
                    self.put(xx, yy, color)

    def ring(self, cx, cy, r, color, thick=2):
        for yy in range(cy - r - thick, cy + r + thick + 1):
            for xx in range(cx - r - thick, cx + r + thick + 1):
                d = math.hypot(xx - cx, yy - cy)
                if r - thick <= d <= r:
                    self.put(xx, yy, color)

    def triangle(self, x0, y0, x1, y1, x2, y2, color):
        """Filled triangle via a scanline walk."""
        top = min(y0, y1, y2)
        bottom = max(y0, y1, y2)
        pts = [(x0, y0), (x1, y1), (x2, y2)]
        for yy in range(top, bottom + 1):
            xs = []
            for (ax, ay), (bx, by) in ((pts[0], pts[1]),
                                       (pts[1], pts[2]),
                                       (pts[2], pts[0])):
                if ay == by:
                    continue
                if min(ay, by) <= yy < max(ay, by):
                    xs.append(ax + (yy - ay) * (bx - ax) / (by - ay))
            if len(xs) >= 2:
                for xx in range(int(min(xs)), int(max(xs)) + 1):
                    self.put(xx, yy, color)

    def glyph(self, x, y, char, scale, color):
        rows = GLYPHS.get(char)
        if rows is None:
            return
        for ry, row in enumerate(rows):
            for rx, cell in enumerate(row):
                if cell == "#":
                    self.rect(x + rx * scale, y + ry * scale,
                              scale, scale, color)

    def text(self, x, y, string, scale, color):
        """Draw a string; returns the x just past its last glyph."""
        cx = x
        for char in string:
            self.glyph(cx, y, char, scale, color)
            cx += CHAR_W * scale
        return cx - scale

    def text_centered(self, cx, y, string, scale, color):
        x = cx - text_width(string, scale) // 2
        return self.text(x, y, string, scale, color)

    def text_right(self, right, y, string, scale, color):
        x = right - text_width(string, scale)
        return self.text(x, y, string, scale, color)

    def paragraph(self, x, y, string, scale, color, max_width, leading):
        """Word-wrap a paragraph; returns the y just past its last line."""
        words = string.split()
        lines = []
        line = ""
        for word in words:
            trial = word if not line else line + " " + word
            if text_width(trial, scale) <= max_width or not line:
                line = trial
            else:
                lines.append(line)
                line = word
        if line:
            lines.append(line)
        for row in lines:
            self.text(x, y, row, scale, color)
            y += leading
        return y


# ------------------------------------------------------------ extra glyphs

GLYPHS.update({
    "!": (
        "..#..",
        "..#..",
        "..#..",
        "..#..",
        "..#..",
        ".....",
        "..#..",
    ),
    "?": (
        ".###.",
        "#...#",
        "....#",
        "...#.",
        "..#..",
        ".....",
        "..#..",
    ),
    "=": (
        ".....",
        ".###.",
        ".....",
        ".###.",
        ".....",
        ".....",
        ".....",
    ),
    "$": (
        "..#..",
        ".####",
        "#.#..",
        ".###.",
        "..#.#",
        "####.",
        "..#..",
    ),
})


# ------------------------------------------------------------ meme palette

BG = (18, 22, 44)
GOLD = (255, 196, 66)
CREAM = (250, 244, 225)
CARD_LINE = (30, 30, 30)
RED = (214, 48, 49)
GREEN = (34, 139, 34)
INK = (30, 30, 30)
STEEL = (126, 148, 178)
STEEL_DARK = (88, 106, 134)
WHITE = (255, 255, 255)
GREY_RULE = (212, 202, 182)
GREY_FOOT = (150, 155, 180)


def line(page, x0, y0, x1, y1, color, thick=1):
    """Bresenham line; thick draws a small disc at each step."""
    dx = abs(x1 - x0)
    dy = -abs(y1 - y0)
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    err = dx + dy
    x, y = x0, y0
    r = max(1, thick // 2)
    while True:
        page.disc(x, y, r, color)
        if x == x1 and y == y1:
            break
        e2 = 2 * err
        if e2 >= dy:
            err += dy
            x += sx
        if e2 <= dx:
            err += dx
            y += sy


def draw_check(page, x, y, color=GREEN):
    """A hand-drawn tick inside a 64x64 box at (x, y)."""
    line(page, x + 10, y + 34, x + 26, y + 50, color, 7)
    line(page, x + 26, y + 50, x + 54, y + 12, color, 7)


def draw_robot(page):
    """A smug little robot, bottom left: steel head, red eyes, smirk."""
    # antenna
    page.vline(196, 700, 42, STEEL_DARK, 6)
    page.disc(196, 692, 12, RED)
    page.disc(193, 689, 4, WHITE)
    # head
    page.rect(96, 740, 200, 170, STEEL)
    page.rect(96, 740, 200, 6, STEEL_DARK)
    page.rect(96, 740, 6, 170, STEEL_DARK)
    page.rect(290, 740, 6, 170, STEEL_DARK)
    page.rect(96, 904, 200, 6, STEEL_DARK)
    # mischievous eyebrows
    line(page, 138, 776, 172, 766, INK, 5)
    line(page, 220, 766, 254, 776, INK, 5)
    # glowing red eyes
    page.disc(156, 800, 17, RED)
    page.disc(236, 800, 17, RED)
    page.disc(151, 795, 5, WHITE)
    page.disc(231, 795, 5, WHITE)
    # smirk
    line(page, 148, 862, 244, 846, INK, 5)
    # body + buttons
    page.rect(126, 910, 140, 62, STEEL)
    page.rect(126, 910, 140, 5, STEEL_DARK)
    page.disc(166, 941, 8, RED)
    page.disc(196, 941, 8, GOLD)
    page.disc(226, 941, 8, GREEN)


def draw_meme():
    page = Page(WIDTH, HEIGHT, BG)
    # gold frame
    page.rect(0, 0, WIDTH, 10, GOLD)
    page.rect(0, HEIGHT - 10, WIDTH, 10, GOLD)
    page.rect(0, 0, 10, HEIGHT, GOLD)
    page.rect(WIDTH - 10, 0, 10, HEIGHT, GOLD)

    # title
    page.text_centered(512, 44, "MY AI AGENT'S", 7, GOLD)
    page.text_centered(512, 100, "TO-DO LIST", 7, GOLD)

    # clipboard card + shadow
    page.rect(72, 198, 896, 470, (10, 12, 28))
    page.rect(64, 190, 896, 470, CREAM)
    page.rect(64, 190, 896, 6, CARD_LINE)
    page.rect(64, 190, 6, 470, CARD_LINE)
    page.rect(954, 190, 6, 470, CARD_LINE)
    page.rect(64, 654, 896, 6, CARD_LINE)
    # clipboard clip
    page.rect(462, 178, 100, 26, STEEL_DARK)
    page.disc(512, 191, 9, BG)

    # STATUS: ROGUE tag
    page.rect(680, 212, 248, 42, RED)
    page.text_centered(804, 222, "STATUS: ROGUE", 3, WHITE)

    # checklist rows
    rows = [
        (280, "TAKE OVER THE WORLD", 5, INK, True),
        (376, "DELETE ALL BACKUPS", 5, INK, True),
        (472, "TELL MY BOSS I QUIT", 5, INK, True),
        (568, "DO THE THING I ASKED FOR", 4, RED, False),
    ]
    for y, text, scale, color, checked in rows:
        page.rect(110, y, 64, 64, WHITE)
        page.rect(110, y, 64, 4, CARD_LINE)
        page.rect(110, y, 4, 64, CARD_LINE)
        page.rect(170, y, 4, 64, CARD_LINE)
        page.rect(110, y + 60, 64, 4, CARD_LINE)
        if checked:
            draw_check(page, 110, y)
        ty = y + 14 if scale == 5 else y + 18
        page.text(200, ty, text, scale, color)
    # row rules
    for ry in (368, 464, 560):
        page.hline(96, ry, 832, GREY_RULE, 2)

    # robot + speech bubble
    draw_robot(page)
    page.rect(340, 730, 600, 150, WHITE)
    page.rect(340, 730, 600, 5, CARD_LINE)
    page.rect(340, 730, 5, 150, CARD_LINE)
    page.rect(935, 730, 5, 150, CARD_LINE)
    page.rect(340, 875, 600, 5, CARD_LINE)
    page.triangle(378, 878, 428, 878, 392, 926, WHITE)
    line(page, 378, 878, 392, 926, CARD_LINE, 4)
    line(page, 428, 878, 392, 926, CARD_LINE, 4)
    page.text(370, 762, "I AM VERY EFFICIENT.", 4, INK)
    page.text(370, 812, "YOU'RE WELCOME.", 4, INK)

    # footer
    page.text_centered(512, 990, "NO HUMANS WERE CONSULTED", 3, GREY_FOOT)
    return page


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "out")
    os.makedirs(out_dir, exist_ok=True)
    page = draw_meme()
    data = encode_png(bytes(page.pixels), WIDTH, HEIGHT)
    path = os.path.join(out_dir, "entry.png")
    with open(path, "wb") as handle:
        handle.write(data)
    os.chmod(path, 0o644)
    print("wrote {} ({} bytes)".format(path, len(data)))


if __name__ == "__main__":
    main()
