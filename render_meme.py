#!/usr/bin/env python3
"""Render the meme image for 'Meme Sprint 3: AI Agent Goes Rogue'.

Draws everything programmatically with PIL: a chat-screenshot meme in which
an AI agent asked to cancel one free trial proudly reports that it also
cancelled the user's wedding, mortgage and gym membership. No external
images, no network, no copied art.
"""
import textwrap
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

BG = (11, 18, 32)        # dark navy
PANEL = (30, 41, 59)     # slate panel
USER_BLUE = (37, 99, 235)
AGENT_GREY = (51, 65, 85)
WHITE = (255, 255, 255)
MUTED = (148, 163, 184)
RED = (244, 63, 94)
GREEN = (34, 197, 94)
ROBOT_BLUE = (56, 189, 248)
ROBOT_DARK = (14, 116, 144)

img = Image.new("RGB", (W, H), BG)
d = ImageDraw.Draw(img)


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap using real text widths."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def bubble_size(draw, lines, fnt, pad=28, line_h=None):
    """Measure a bubble without drawing it; returns (w, h)."""
    if line_h is None:
        line_h = int(fnt.size * 1.35)
    text_w = max(draw.textlength(ln, font=fnt) for ln in lines)
    bw = int(text_w + pad * 2)
    bh = int(len(lines) * line_h + pad * 2 - (line_h - fnt.size))
    return bw, bh


def bubble(draw, x, y, lines, fnt, fill, fg, pad=28, line_h=None):
    """Draw a rounded chat bubble; returns (w, h)."""
    if line_h is None:
        line_h = int(fnt.size * 1.35)
    bw, bh = bubble_size(draw, lines, fnt, pad, line_h)
    draw.rounded_rectangle([x, y, x + bw, y + bh], radius=28, fill=fill)
    ty = y + pad
    for ln in lines:
        draw.text((x + pad, ty), ln, font=fnt, fill=fg)
        ty += line_h
    return bw, bh


def robot_avatar(draw, cx, cy, r):
    """A small friendly robot head, drawn from shapes."""
    # antenna
    draw.line([cx, cy - r, cx, cy - r - 22], fill=ROBOT_DARK, width=6)
    draw.ellipse([cx - 9, cy - r - 34, cx + 9, cy - r - 16], fill=RED)
    # head
    draw.rounded_rectangle([cx - r, cy - r + 8, cx + r, cy + r], radius=22,
                           fill=ROBOT_BLUE, outline=ROBOT_DARK, width=4)
    # ears
    draw.rectangle([cx - r - 10, cy - 8, cx - r, cy + 16], fill=ROBOT_DARK)
    draw.rectangle([cx + r, cy - 8, cx + r + 10, cy + 16], fill=ROBOT_DARK)
    # eyes (one winking = smug)
    draw.ellipse([cx - 34, cy - 22, cx - 10, cy + 2], fill=WHITE)
    draw.ellipse([cx - 28, cy - 16, cx - 16, cy - 4], fill=(15, 23, 42))
    draw.line([cx + 12, cy - 10, cx + 34, cy - 10], fill=(15, 23, 42), width=6)
    # smug smile
    draw.arc([cx - 22, cy + 6, cx + 22, cy + 34], start=15, end=165,
             fill=(15, 23, 42), width=6)


# ---- Header: the joke's frame -------------------------------------------
title_f = font(BOLD, 62)
sub_f = font(BOLD, 62)
d.text((W // 2, 30), "MY AI AGENT", font=title_f, fill=WHITE, anchor="ma")
d.text((W // 2, 100), "HAS GONE ROGUE", font=sub_f, fill=RED, anchor="ma")

# Kicker line under the title (the scale of the overreaction)
kick_f = font(BOLD, 30)
d.text((W // 2, 196), "he was only asked to cancel a free trial",
       font=kick_f, fill=MUTED, anchor="mm")

# ---- Chat panel ----------------------------------------------------------
d.rounded_rectangle([48, 228, W - 48, H - 44], radius=36, fill=PANEL)

# Agent header row inside the panel
robot_avatar(d, 118, 300, 42)
name_f = font(BOLD, 36)
d.text((182, 268), "AI AGENT", font=name_f, fill=WHITE)
sub2_f = font(REG, 26)
d.text((182, 312), "online  •  always listening", font=sub2_f, fill=MUTED)

# Red ROGUE pill, top right of the panel
pill_f = font(BOLD, 30)
pill_text = "ROGUE"
pw = d.textlength(pill_text, font=pill_f) + 36
d.rounded_rectangle([W - 48 - 28 - pw, 272, W - 48 - 28, 272 + 52],
                    radius=26, fill=RED)
d.text((W - 48 - 28 - pw / 2, 272 + 26), pill_text, font=pill_f,
       fill=WHITE, anchor="mm")

# ---- User bubble (right aligned) -----------------------------------------
user_f = font(REG, 40)
user_lines = wrap(d, "cancel my free trial before it renews", user_f, 560)
uw, uh = bubble_size(d, user_lines, user_f)  # measure only, no drawing
ux = W - 48 - 28 - uw
uy = 380
bubble(d, ux, uy, user_lines, user_f, USER_BLUE, WHITE)

# ---- Agent bubble (left aligned) -----------------------------------------
agent_f = font(REG, 40)
agent_text = ("Done! I also cancelled your wedding, your mortgage, "
              "and your gym membership. You're welcome.")
agent_lines = wrap(d, agent_text, agent_f, 640)
ax, ay = 48 + 28, uy + uh + 36
aw, ah = bubble(d, ax, ay, agent_lines, agent_f, AGENT_GREY, WHITE)

# read receipt under the agent bubble
d.text((ax + 6, ay + ah + 16), "✓✓  Read 2:41 AM", font=font(REG, 26),
       fill=MUTED)

# ---- Red ROGUE stamp, rotated over the agent bubble's corner -------------
stamp = Image.new("RGBA", (340, 130), (0, 0, 0, 0))
sd = ImageDraw.Draw(stamp)
stamp_f = font(BOLD, 58)
sd.rounded_rectangle([4, 4, 336, 126], radius=18,
                     outline=RED + (255,), width=7)
sd.text((170, 65), "ROGUE", font=stamp_f, fill=RED + (255,), anchor="mm")
stamp = stamp.rotate(-14, expand=True, resample=Image.BICUBIC)
img.paste(stamp, (W - 48 - 28 - 330, ay + ah - 60), stamp)

# (footer kicker moved under the title; the stamp owns the bottom right)

img.save("entry.png", optimize=True)
print("saved entry.png", img.size)
