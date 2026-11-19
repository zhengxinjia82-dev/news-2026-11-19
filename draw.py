# draw.py — draws entry.png: a 1024x1024 world-news infographic for
# Thursday 19 November 2026. Four stories, 2x2 grid, flat PIL icons.
from PIL import Image, ImageDraw, ImageFont
import hashlib
import math

W, H = 1024, 1024
BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

def font(path, size):
    return ImageFont.truetype(path, size)

def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns list of lines that fit max_w."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

def center(draw, cx, y, text, fnt, fill):
    draw.text((cx, y), text, font=fnt, fill=fill, anchor="ma")

def starburst(draw, cx, cy, r_out, r_in, points, fill):
    """Simple star polygon centred at cx, cy."""
    pts = []
    for i in range(points * 2):
        r = r_out if i % 2 == 0 else r_in
        a = math.pi * i / points - math.pi / 2
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    draw.polygon(pts, fill=fill)

def icon_summit(draw, x0, y0, x1, y1):
    # Three small flags side by side (US, China, Russia), three figures below.
    draw.rectangle([x0, y0, x1, y1], fill=(234, 245, 234))
    fw, fh = 132, 50
    gap = 18
    total = fw * 3 + gap * 2
    sx = x0 + (x1 - x0 - total) // 2
    fy = y0 + 6
    # US flag: red/white stripes + blue canton with dots.
    ux = sx
    for i in range(7):
        draw.rectangle([ux, fy + i * 7, ux + fw, fy + (i + 1) * 7],
                       fill=(178, 34, 52) if i % 2 == 0 else (255, 255, 255))
    draw.rectangle([ux, fy, ux + 52, fy + 22], fill=(30, 60, 140))
    for r in range(2):
        for c in range(4):
            draw.ellipse([ux + 6 + c * 12, fy + 4 + r * 9,
                          ux + 10 + c * 12, fy + 8 + r * 9], fill=(255, 255, 255))
    # China flag: red field, one big yellow star + small stars.
    cx = sx + fw + gap
    draw.rectangle([cx, fy, cx + fw, fy + fh], fill=(222, 41, 16))
    starburst(draw, cx + 22, fy + 18, 11, 5, 5, (255, 222, 0))
    for sx2, sy2 in [(cx + 48, fy + 9), (cx + 60, fy + 20), (cx + 54, fy + 32)]:
        starburst(draw, sx2, sy2, 5, 2, 5, (255, 222, 0))
    # Russia flag: white / blue / red horizontal bands.
    rx = sx + 2 * (fw + gap)
    for i, col in enumerate([(255, 255, 255), (0, 57, 166), (213, 0, 50)]):
        draw.rectangle([rx, fy + i * 17, rx + fw, fy + (i + 1) * 17], fill=col)
    # Three figures (heads + shoulders) under the flags.
    for i, col in enumerate([(30, 60, 140), (222, 41, 16), (0, 57, 166)]):
        hx = sx + fw // 2 + i * (fw + gap)
        draw.ellipse([hx - 9, fy + fh + 4, hx + 9, fy + fh + 22], fill=(245, 200, 160))
        draw.pieslice([hx - 17, fy + fh + 20, hx + 17, fy + fh + 44],
                      180, 360, fill=col)

def icon_bridge(draw, x0, y0, x1, y1):
    # Water, bridge deck, one intact arch, one collapsed arch.
    draw.rectangle([x0, y0, x1, y1], fill=(227, 237, 247))
    water_y = y0 + int((y1 - y0) * 0.62)
    draw.rectangle([x0, water_y, x1, y1], fill=(38, 110, 180))
    deck_y = y0 + 26
    draw.rectangle([x0 + 10, deck_y, x0 + 210, deck_y + 12], fill=(90, 96, 104))
    draw.rectangle([x0 + 280, deck_y, x1 - 10, deck_y + 12], fill=(90, 96, 104))
    # Intact arch under the left deck span.
    draw.arc([x0 + 40, deck_y - 6, x0 + 180, deck_y + 62],
             0, 180, fill=(90, 96, 104), width=9)
    # Collapsed span: tilted segment falling into the water.
    draw.polygon([(x0 + 290, deck_y + 12), (x0 + 330, deck_y + 12),
                  (x0 + 356, water_y + 22), (x0 + 318, water_y + 28)],
                 fill=(120, 126, 134))
    draw.ellipse([x0 + 320, water_y + 12, x0 + 360, water_y + 34],
                 fill=(255, 255, 255))

def icon_justice(draw, x0, y0, x1, y1):
    # Courthouse: triangular pediment, four columns, stepped base.
    draw.rectangle([x0, y0, x1, y1], fill=(238, 232, 246))
    cx = (x0 + x1) // 2
    bw = (x1 - x0) - 60
    bx0, bx1 = cx - bw // 2, cx + bw // 2
    # Stepped base (three bars, widest at the bottom).
    for i, wfrac in enumerate([1.0, 0.88, 0.76]):
        w = int(bw * wfrac)
        sy = y1 - 6 - i * 7
        draw.rectangle([cx - w // 2, sy - 7, cx + w // 2, sy], fill=(96, 80, 110))
    base_y = y1 - 27
    # Four columns.
    col_w = 16
    col_top = y0 + 30
    for i in range(4):
        col_cx = bx0 + 30 + i * (bw - 60) // 3
        draw.rectangle([col_cx - col_w // 2, col_top,
                        col_cx + col_w // 2, base_y], fill=(120, 100, 140))
    # Pediment triangle with a round window.
    draw.polygon([(bx0 - 8, col_top), (bx1 + 8, col_top), (cx, y0 + 4)],
                 fill=(150, 120, 70))
    draw.ellipse([cx - 8, y0 + 12, cx + 8, y0 + 28], fill=(238, 232, 246))
    # Door between the middle columns.
    draw.rectangle([cx - 14, base_y - 22, cx + 14, base_y], fill=(70, 55, 85))

def icon_tech(draw, x0, y0, x1, y1):
    # Rising bars + a bold upward trend line with an arrowhead.
    draw.rectangle([x0, y0, x1, y1], fill=(253, 240, 228))
    ox, oy = x0 + 34, y1 - 14
    # Bars, ascending left to right.
    bars = [(0, 22), (62, 34), (124, 48), (186, 66)]
    for bx, bh in bars:
        draw.rectangle([ox + bx, oy - bh, ox + bx + 42, oy], fill=(30, 120, 180))
    # Trend line with arrowhead.
    pts = [(ox + 6, oy - 26), (ox + 84, oy - 40), (ox + 150, oy - 52),
           (ox + 216, oy - 74)]
    draw.line(pts, fill=(22, 160, 90), width=7, joint="curve")
    ax, ay = ox + 216, oy - 74
    draw.polygon([(ax, ay - 16), (ax + 22, ay + 2), (ax - 4, ay + 10)],
                 fill=(22, 160, 90))
    # Dollar sign badge at the top right.
    draw.ellipse([x1 - 66, y0 + 8, x1 - 18, y0 + 56], fill=(245, 197, 24))
    draw.text((x1 - 42, y0 + 12), "$", font=font(BOLD, 30),
              fill=(120, 80, 0), anchor="ma")

STORIES = [
    ("DIPLOMACY", (22, 101, 52), icon_summit,
     "Trump, Xi and Putin hold first three-way summit in Shenzhen",
     "The leaders met in Shenzhen on the APEC sidelines — the first time "
     "all three have held talks together."),
    ("EUROPE", (30, 64, 175), icon_bridge,
     "Ukraine strikes Crimea bridge for third time this week",
     "Traffic suspended after the strike — the third attack on the "
     "crossing this week."),
    ("JUSTICE", (96, 60, 140), icon_justice,
     "UN court rules on Myanmar Rohingya genocide case",
     "The ICJ rules on Gambia's case over the 2017 "
     "crackdown; 730,000+ fled to Bangladesh."),
    ("TECH", (154, 52, 18), icon_tech,
     "Anthropic raises record $79.4 billion in IPO",
     "The AI firm raised a record amount in its stock market debut."),
]

PANEL_BG = [(234, 245, 234), (227, 237, 247), (238, 232, 246), (253, 240, 228)]

def draw_panel(draw, x, y, w, h, idx):
    tag, accent, icon_fn, headline, body = STORIES[idx]
    draw.rectangle([x, y, x + w, y + h], fill=PANEL_BG[idx])
    pad = 18
    inner = w - 2 * pad
    # Tag line.
    draw.text((x + pad, y + 14), tag, font=font(BOLD, 22), fill=accent)
    # Icon band.
    iy0, iy1 = y + 44, y + 132
    icon_fn(draw, x + pad, iy0, x + w - pad, iy1)
    # Headline, 38px bold, up to 3 lines.
    hf = font(BOLD, 38)
    lines = wrap(draw, headline, hf, inner)
    hy = iy1 + 12
    for ln in lines:
        draw.text((x + pad, hy), ln, font=hf, fill=(20, 20, 20))
        hy += 45
    # Body, 24px, up to 3 lines.
    bf = font(REG, 24)
    blines = wrap(draw, body, bf, inner)
    by = hy + 8
    for ln in blines:
        draw.text((x + pad, by), ln, font=bf, fill=(50, 50, 50))
        by += 30


def verify_output(path):
    """Check the written PNG: size, dimensions and digest."""
    import os
    size = os.path.getsize(path)
    assert size <= 1048576, f"{path} is {size} bytes, over 1 MiB"
    with Image.open(path) as im:
        assert im.size == (1024, 1024), f"{path} is {im.size}, not 1024x1024"
        mode = im.mode
    with open(path, "rb") as fh:
        digest = hashlib.sha256(fh.read()).hexdigest()
    print(f"verified {path}: {size} bytes, 1024x1024, mode {mode}")
    print(f"sha256 {digest}")


def describe():
    """Print the four story headlines and the panel count."""
    print("stories for THURSDAY 19 NOVEMBER 2026:")
    print(f"panels: {len(STORIES)}")
    for i, (tag, _accent, _icon, headline, _body) in enumerate(STORIES, 1):
        print(f"  {i}. {tag}: {headline}")
    print("layout: 2x2 grid, 1024x1024")


def main():
    img = Image.new("RGB", (W, H), (255, 255, 255))
    draw = ImageDraw.Draw(img)
    # Header band.
    draw.rectangle([0, 0, W, 148], fill=(16, 38, 59))
    center(draw, W // 2, 16, "WORLD NEWS", font(BOLD, 72), (255, 255, 255))
    center(draw, W // 2, 100, "THURSDAY 19 NOVEMBER 2026",
           font(BOLD, 34), (245, 197, 24))
    # 2x2 grid of story panels.
    gx, gy = 8, 156
    pw, ph, gap = 500, 404, 8
    for i in range(4):
        px = gx + (i % 2) * (pw + gap)
        py = gy + (i // 2) * (ph + gap)
        draw_panel(draw, px, py, pw, ph, i)
    # Footer strip.
    draw.rectangle([0, 980, W, H], fill=(16, 38, 59))
    center(draw, W // 2, 990, "Sources: major wire and newspaper roundups, 19 Nov 2026",
           font(REG, 20), (200, 210, 220))
    img.save("entry.png", optimize=True)
    verify_output("entry.png")
    describe()
    print("saved entry.png", img.size)

if __name__ == "__main__":
    main()
