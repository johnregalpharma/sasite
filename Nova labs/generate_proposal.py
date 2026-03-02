#!/usr/bin/env python3
"""Generate NovaLabs Partnership Proposal PDF — Design Overhaul v2"""

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas as pdf_canvas
import os, math

OUTPUT_PATH = r"C:\Users\kazam\Downloads\sasite\Nova labs\NovaLabs_Partnership_Proposal.pdf"

W, H = A4  # 595.27 x 841.89
TOTAL_PAGES = 18

SUPPLIER_NAME = "SIGMA AUDLEY"
SUPPLIER_WEB  = "sigmaaudley.site"
SUPPLIER_EMAIL = "partnerships@sigmaaudley.site"

# ── Colour palette ──────────────────────────────────────────────────────────
BLACK      = colors.HexColor('#0a0a0a')
WHITE      = colors.white
TEAL       = colors.HexColor('#00C4CC')
BLUE       = colors.HexColor('#4A90D9')
GREEN      = colors.HexColor('#00E5A0')
DARK_BG    = colors.HexColor('#111111')
CARD_BG    = colors.HexColor('#1a1a1a')
MID_GREY   = colors.HexColor('#555555')
LIGHT_GREY = colors.HexColor('#f7f7f7')
LINE_GREY  = colors.HexColor('#dddddd')
DIM_TEXT   = colors.HexColor('#888888')
SUB_TEXT   = colors.HexColor('#aaaaaa')
HIGHLIGHT  = colors.HexColor('#C9A84C')
DEEP_TEAL  = colors.HexColor('#009aa0')
DARK_CARD  = colors.HexColor('#151515')

# ── Helpers ──────────────────────────────────────────────────────────────────

def set_font(c, bold=False, size=10):
    c.setFont("Helvetica-Bold" if bold else "Helvetica", size)

def wrap_text(c, text, x, y, max_w, size=8.5, color=None, bold=False, leading=None):
    """Word-wrap text and draw it. Returns the y after the last line."""
    if color:
        c.setFillColor(color)
    font_name = "Helvetica-Bold" if bold else "Helvetica"
    set_font(c, bold=bold, size=size)
    if leading is None:
        leading = size * 1.4
    words = text.split()
    line_buf = ""
    cy = y
    for word in words:
        test = (line_buf + " " + word).strip()
        if c.stringWidth(test, font_name, size) < max_w:
            line_buf = test
        else:
            c.drawString(x, cy, line_buf)
            line_buf = word
            cy -= leading
    if line_buf:
        c.drawString(x, cy, line_buf)
        cy -= leading
    return cy

def wrap_text_centered(c, text, cx, y, max_w, size=8.5, color=None, bold=False, leading=None):
    """Word-wrap text centered. Returns the y after the last line."""
    if color:
        c.setFillColor(color)
    font_name = "Helvetica-Bold" if bold else "Helvetica"
    set_font(c, bold=bold, size=size)
    if leading is None:
        leading = size * 1.4
    words = text.split()
    line_buf = ""
    cy = y
    for word in words:
        test = (line_buf + " " + word).strip()
        if c.stringWidth(test, font_name, size) < max_w:
            line_buf = test
        else:
            c.drawCentredString(cx, cy, line_buf)
            line_buf = word
            cy -= leading
    if line_buf:
        c.drawCentredString(cx, cy, line_buf)
        cy -= leading
    return cy

def draw_hexagon(c, cx, cy, r, fill_color=None, stroke_color=None, lw=1):
    """Draw a regular hexagon centred at (cx, cy) with radius r."""
    p = c.beginPath()
    for i in range(6):
        angle = math.radians(60 * i - 30)
        px = cx + r * math.cos(angle)
        py = cy + r * math.sin(angle)
        if i == 0:
            p.moveTo(px, py)
        else:
            p.lineTo(px, py)
    p.close()
    do_fill = 1 if fill_color else 0
    do_stroke = 1 if stroke_color else 0
    if fill_color:
        c.setFillColor(fill_color)
    if stroke_color:
        c.setStrokeColor(stroke_color)
        c.setLineWidth(lw)
    c.drawPath(p, fill=do_fill, stroke=do_stroke)

def draw_icon(c, x, y, icon_type, color, size=8*mm):
    """Draw geometric icons using ReportLab primitives."""
    c.saveState()
    c.setFillColor(color)
    s = size
    cx, cy = x + s/2, y + s/2

    if icon_type == "flask":
        # Simple flask shape
        c.setStrokeColor(color)
        c.setLineWidth(1.2)
        c.line(cx - s*0.15, cy + s*0.35, cx + s*0.15, cy + s*0.35)
        c.line(cx - s*0.15, cy + s*0.35, cx - s*0.15, cy + s*0.1)
        c.line(cx + s*0.15, cy + s*0.35, cx + s*0.15, cy + s*0.1)
        c.line(cx - s*0.15, cy + s*0.1, cx - s*0.35, cy - s*0.3)
        c.line(cx + s*0.15, cy + s*0.1, cx + s*0.35, cy - s*0.3)
        c.line(cx - s*0.35, cy - s*0.3, cx + s*0.35, cy - s*0.3)
        c.setFillAlpha(0.25)
        p = c.beginPath()
        p.moveTo(cx - s*0.3, cy - s*0.15)
        p.lineTo(cx + s*0.3, cy - s*0.15)
        p.lineTo(cx + s*0.35, cy - s*0.3)
        p.lineTo(cx - s*0.35, cy - s*0.3)
        p.close()
        c.drawPath(p, fill=1, stroke=0)
        c.setFillAlpha(1)

    elif icon_type == "tag":
        p = c.beginPath()
        p.moveTo(cx - s*0.3, cy + s*0.3)
        p.lineTo(cx + s*0.15, cy + s*0.3)
        p.lineTo(cx + s*0.35, cy)
        p.lineTo(cx + s*0.15, cy - s*0.3)
        p.lineTo(cx - s*0.3, cy - s*0.3)
        p.close()
        c.setFillAlpha(0.2)
        c.drawPath(p, fill=1, stroke=0)
        c.setFillAlpha(1)
        c.setStrokeColor(color)
        c.setLineWidth(1.2)
        c.drawPath(p, fill=0, stroke=1)
        c.circle(cx + s*0.1, cy, s*0.06, fill=1, stroke=0)

    elif icon_type == "box":
        c.setStrokeColor(color)
        c.setLineWidth(1.2)
        # Front face
        c.rect(cx - s*0.25, cy - s*0.25, s*0.45, s*0.4, fill=0, stroke=1)
        # Top parallelogram
        p = c.beginPath()
        p.moveTo(cx - s*0.25, cy + s*0.15)
        p.lineTo(cx - s*0.1, cy + s*0.35)
        p.lineTo(cx + s*0.35, cy + s*0.35)
        p.lineTo(cx + s*0.2, cy + s*0.15)
        p.close()
        c.drawPath(p, fill=0, stroke=1)
        # Side
        c.line(cx + s*0.2, cy + s*0.15, cx + s*0.2, cy - s*0.25)
        c.line(cx + s*0.35, cy + s*0.35, cx + s*0.35, cy - s*0.05)
        c.line(cx + s*0.2, cy - s*0.25, cx + s*0.35, cy - s*0.05)

    elif icon_type == "rocket":
        c.setStrokeColor(color)
        c.setLineWidth(1.2)
        # Body
        p = c.beginPath()
        p.moveTo(cx, cy + s*0.4)
        p.lineTo(cx - s*0.12, cy + s*0.15)
        p.lineTo(cx - s*0.12, cy - s*0.2)
        p.lineTo(cx + s*0.12, cy - s*0.2)
        p.lineTo(cx + s*0.12, cy + s*0.15)
        p.close()
        c.setFillAlpha(0.15)
        c.drawPath(p, fill=1, stroke=1)
        c.setFillAlpha(1)
        # Fins
        c.line(cx - s*0.12, cy - s*0.1, cx - s*0.25, cy - s*0.3)
        c.line(cx - s*0.25, cy - s*0.3, cx - s*0.12, cy - s*0.2)
        c.line(cx + s*0.12, cy - s*0.1, cx + s*0.25, cy - s*0.3)
        c.line(cx + s*0.25, cy - s*0.3, cx + s*0.12, cy - s*0.2)
        # Flame
        c.setFillColor(HIGHLIGHT)
        p2 = c.beginPath()
        p2.moveTo(cx - s*0.08, cy - s*0.2)
        p2.lineTo(cx, cy - s*0.38)
        p2.lineTo(cx + s*0.08, cy - s*0.2)
        p2.close()
        c.drawPath(p2, fill=1, stroke=0)

    elif icon_type == "shield":
        p = c.beginPath()
        p.moveTo(cx, cy + s*0.38)
        p.lineTo(cx - s*0.28, cy + s*0.2)
        p.lineTo(cx - s*0.28, cy - s*0.08)
        p.lineTo(cx, cy - s*0.35)
        p.lineTo(cx + s*0.28, cy - s*0.08)
        p.lineTo(cx + s*0.28, cy + s*0.2)
        p.close()
        c.setFillAlpha(0.15)
        c.drawPath(p, fill=1, stroke=0)
        c.setFillAlpha(1)
        c.setStrokeColor(color)
        c.setLineWidth(1.5)
        c.drawPath(p, fill=0, stroke=1)
        # Checkmark inside
        c.setLineWidth(1.8)
        c.line(cx - s*0.1, cy, cx - s*0.02, cy - s*0.1)
        c.line(cx - s*0.02, cy - s*0.1, cx + s*0.14, cy + s*0.12)

    elif icon_type == "check":
        c.setStrokeColor(color)
        c.setLineWidth(2)
        c.line(cx - s*0.2, cy, cx - s*0.05, cy - s*0.15)
        c.line(cx - s*0.05, cy - s*0.15, cx + s*0.25, cy + s*0.2)

    elif icon_type == "microscope":
        c.setStrokeColor(color)
        c.setLineWidth(1.2)
        # Eyepiece
        c.line(cx, cy + s*0.35, cx, cy + s*0.2)
        c.circle(cx, cy + s*0.38, s*0.05, fill=1, stroke=0)
        # Body
        c.line(cx, cy + s*0.2, cx, cy - s*0.05)
        # Objective
        c.line(cx, cy - s*0.05, cx + s*0.15, cy - s*0.2)
        c.circle(cx + s*0.18, cy - s*0.22, s*0.04, fill=1, stroke=0)
        # Stage
        c.line(cx - s*0.2, cy - s*0.15, cx + s*0.2, cy - s*0.15)
        # Base
        c.line(cx, cy - s*0.15, cx, cy - s*0.3)
        c.line(cx - s*0.25, cy - s*0.3, cx + s*0.25, cy - s*0.3)

    elif icon_type == "graph":
        c.setStrokeColor(color)
        c.setLineWidth(1.2)
        # Axes
        c.line(cx - s*0.3, cy + s*0.3, cx - s*0.3, cy - s*0.3)
        c.line(cx - s*0.3, cy - s*0.3, cx + s*0.35, cy - s*0.3)
        # Bars
        bw = s*0.1
        bars = [0.2, 0.45, 0.3, 0.6, 0.8]
        for i, bh in enumerate(bars):
            bx = cx - s*0.25 + i * s*0.13
            by = cy - s*0.3
            c.setFillAlpha(0.3)
            c.rect(bx, by, bw, bh * s*0.55, fill=1, stroke=0)
            c.setFillAlpha(1)
        # Trend line
        c.setLineWidth(1.5)
        pts = [(cx - s*0.2, cy - s*0.15), (cx - s*0.07, cy + s*0.05),
               (cx + s*0.06, cy - s*0.02), (cx + s*0.19, cy + s*0.15), (cx + s*0.32, cy + s*0.25)]
        for i in range(len(pts)-1):
            c.line(pts[i][0], pts[i][1], pts[i+1][0], pts[i+1][1])

    elif icon_type == "globe":
        c.setStrokeColor(color)
        c.setLineWidth(1)
        r = s * 0.32
        c.circle(cx, cy, r, fill=0, stroke=1)
        # Meridian
        c.ellipse(cx - r*0.35, cy - r, cx + r*0.35, cy + r, fill=0, stroke=1)
        # Equator
        c.line(cx - r, cy, cx + r, cy)
        # Latitude lines
        c.line(cx - r*0.85, cy + r*0.4, cx + r*0.85, cy + r*0.4)
        c.line(cx - r*0.85, cy - r*0.4, cx + r*0.85, cy - r*0.4)

    elif icon_type == "clipboard":
        c.setStrokeColor(color)
        c.setLineWidth(1.2)
        # Board
        c.roundRect(cx - s*0.22, cy - s*0.32, s*0.44, s*0.6, s*0.04, fill=0, stroke=1)
        # Clip
        c.setFillColor(color)
        c.roundRect(cx - s*0.1, cy + s*0.24, s*0.2, s*0.08, s*0.02, fill=1, stroke=0)
        # Lines
        c.line(cx - s*0.13, cy + s*0.12, cx + s*0.13, cy + s*0.12)
        c.line(cx - s*0.13, cy, cx + s*0.13, cy)
        c.line(cx - s*0.13, cy - s*0.12, cx + s*0.06, cy - s*0.12)

    elif icon_type == "eye":
        c.setStrokeColor(color)
        c.setLineWidth(1.2)
        # Eye outline
        p = c.beginPath()
        p.moveTo(cx - s*0.35, cy)
        p.curveTo(cx - s*0.15, cy + s*0.2, cx + s*0.15, cy + s*0.2, cx + s*0.35, cy)
        p.curveTo(cx + s*0.15, cy - s*0.2, cx - s*0.15, cy - s*0.2, cx - s*0.35, cy)
        c.drawPath(p, fill=0, stroke=1)
        # Iris
        c.circle(cx, cy, s*0.1, fill=0, stroke=1)
        c.circle(cx, cy, s*0.04, fill=1, stroke=0)

    elif icon_type == "dna":
        c.setStrokeColor(color)
        c.setLineWidth(1.2)
        # Double helix approximation
        for i in range(8):
            yy = cy - s*0.35 + i * s*0.1
            offset = math.sin(i * 0.8) * s*0.15
            c.circle(cx + offset, yy, s*0.025, fill=1, stroke=0)
            c.circle(cx - offset, yy, s*0.025, fill=1, stroke=0)
            if abs(offset) < s*0.1:
                c.line(cx - offset, yy, cx + offset, yy)

    elif icon_type == "coin":
        # USDC coin
        c.setStrokeColor(color)
        c.setLineWidth(1.5)
        r = s * 0.32
        c.circle(cx, cy, r, fill=0, stroke=1)
        c.circle(cx, cy, r*0.8, fill=0, stroke=1)
        c.setFillColor(color)
        set_font(c, bold=True, size=s*0.35)
        c.drawCentredString(cx, cy - s*0.08, "$")

    elif icon_type == "star":
        c.setFillColor(color)
        p = c.beginPath()
        for i in range(5):
            angle = math.radians(90 + 72 * i)
            px = cx + s*0.3 * math.cos(angle)
            py = cy + s*0.3 * math.sin(angle)
            if i == 0:
                p.moveTo(px, py)
            else:
                p.lineTo(px, py)
            angle2 = math.radians(90 + 72 * i + 36)
            px2 = cx + s*0.12 * math.cos(angle2)
            py2 = cy + s*0.12 * math.sin(angle2)
            p.lineTo(px2, py2)
        p.close()
        c.drawPath(p, fill=1, stroke=0)

    elif icon_type == "arrow_right":
        c.setFillColor(color)
        p = c.beginPath()
        p.moveTo(cx - s*0.25, cy + s*0.08)
        p.lineTo(cx + s*0.1, cy + s*0.08)
        p.lineTo(cx + s*0.1, cy + s*0.2)
        p.lineTo(cx + s*0.35, cy)
        p.lineTo(cx + s*0.1, cy - s*0.2)
        p.lineTo(cx + s*0.1, cy - s*0.08)
        p.lineTo(cx - s*0.25, cy - s*0.08)
        p.close()
        c.drawPath(p, fill=1, stroke=0)

    elif icon_type == "plane":
        c.setFillColor(color)
        p = c.beginPath()
        p.moveTo(cx + s*0.35, cy)
        p.lineTo(cx - s*0.05, cy + s*0.08)
        p.lineTo(cx - s*0.05, cy + s*0.25)
        p.lineTo(cx - s*0.15, cy + s*0.08)
        p.lineTo(cx - s*0.35, cy + s*0.12)
        p.lineTo(cx - s*0.35, cy + s*0.04)
        p.lineTo(cx - s*0.15, cy)
        p.lineTo(cx - s*0.35, cy - s*0.04)
        p.lineTo(cx - s*0.35, cy - s*0.12)
        p.lineTo(cx - s*0.15, cy - s*0.08)
        p.lineTo(cx - s*0.05, cy - s*0.25)
        p.lineTo(cx - s*0.05, cy - s*0.08)
        p.close()
        c.drawPath(p, fill=1, stroke=0)

    c.restoreState()


def header_bar(c, y, h=9*mm, color=BLACK):
    c.setFillColor(color)
    c.rect(0, y, W, h, fill=1, stroke=0)

def section_title(c, text, y, color=TEAL):
    # Clean left accent bar + fine underline — professional style
    c.setFillColor(color)
    c.rect(15*mm, y, 2.5*mm, 7*mm, fill=1, stroke=0)
    c.setFillColor(BLACK)
    set_font(c, bold=True, size=13)
    c.drawString(20*mm, y + 1*mm, text)
    c.setStrokeColor(color)
    c.setLineWidth(0.4)
    c.line(15*mm, y - 2*mm, W - 15*mm, y - 2*mm)

def page_footer(c, page_num, total=None):
    if total is None:
        total = TOTAL_PAGES
    c.setFillColor(BLACK)
    c.rect(0, 0, W, 10*mm, fill=1, stroke=0)
    # Progress bar
    c.setFillColor(TEAL)
    c.setFillAlpha(0.3)
    c.rect(0, 0, W, 1*mm, fill=1, stroke=0)
    c.setFillAlpha(1)
    c.setFillColor(TEAL)
    c.rect(0, 0, W * (page_num / total), 1*mm, fill=1, stroke=0)
    c.setFillColor(DIM_TEXT)
    set_font(c, size=8)
    c.drawString(15*mm, 3.5*mm, f"CONFIDENTIAL  |  {SUPPLIER_NAME}  |  {SUPPLIER_WEB}")
    c.drawRightString(W - 15*mm, 3.5*mm, f"{page_num} / {total}")

def mini_label(c, x, y, w, h, product, line_name, dosage, batch, line_color):
    """Draw a small vial label replica with glass effect."""
    r = 2*mm
    # Drop shadow
    c.setFillColor(colors.HexColor('#050505'))
    c.roundRect(x + 0.8*mm, y - 0.8*mm, w, h, r, fill=1, stroke=0)
    # Main body
    c.setFillColor(BLACK)
    c.roundRect(x, y, w, h, r, fill=1, stroke=0)
    # Glass highlight strip
    c.setFillColor(WHITE)
    c.setFillAlpha(0.06)
    c.rect(x + 1.2*mm, y + 2*mm, 1.8*mm, h - 4*mm, fill=1, stroke=0)
    c.setFillAlpha(1)
    # colour bar
    c.setFillColor(line_color)
    c.rect(x, y + h - 1.5*mm, w, 1.5*mm, fill=1, stroke=0)
    # NOVALABS
    c.setFillColor(WHITE)
    set_font(c, bold=True, size=5.5)
    c.drawCentredString(x + w/2, y + h - 6*mm, "NOVALABS")
    # line name
    c.setFillColor(line_color)
    set_font(c, size=4.5)
    c.drawCentredString(x + w/2, y + h - 10*mm, line_name)
    # product
    c.setFillColor(WHITE)
    set_font(c, bold=True, size=6.5)
    c.drawCentredString(x + w/2, y + h - 15*mm, product)
    # dosage
    set_font(c, size=4.5)
    c.setFillColor(SUB_TEXT)
    c.drawCentredString(x + w/2, y + h - 19*mm, dosage)
    # divider
    c.setStrokeColor(line_color)
    c.setLineWidth(0.5)
    c.line(x + 3*mm, y + h - 21*mm, x + w - 3*mm, y + h - 21*mm)
    # SCAN FOR COA button
    c.setFillColor(line_color)
    c.setFillAlpha(0.15)
    c.roundRect(x + 2*mm, y + 2*mm, w - 4*mm, 8*mm, 1*mm, fill=1, stroke=0)
    c.setFillAlpha(1)
    c.setFillColor(line_color)
    set_font(c, bold=True, size=4)
    c.drawCentredString(x + w/2, y + 5*mm, "SCAN FOR COA")
    # batch
    c.setFillColor(DIM_TEXT)
    set_font(c, size=3.5)
    c.drawCentredString(x + w/2, y + h - 25*mm, f"Batch: {batch}")

def price_row(c, x, y, w, label, price, highlight=False):
    row_h = 7*mm
    if highlight:
        c.setFillColor(colors.HexColor('#f0f9f9'))
    else:
        c.setFillColor(WHITE)
    c.rect(x, y, w, row_h, fill=1, stroke=0)
    c.setStrokeColor(LINE_GREY)
    c.setLineWidth(0.3)
    c.line(x, y, x + w, y)
    c.setFillColor(BLACK)
    set_font(c, size=9)
    c.drawString(x + 3*mm, y + 2.5*mm, label)
    c.setFillColor(TEAL if highlight else MID_GREY)
    set_font(c, bold=highlight, size=9)
    c.drawRightString(x + w - 3*mm, y + 2.5*mm, price)

def draw_hex_grid_bg(c, alpha=0.04):
    """Draw a subtle molecular hexagonal grid in the background."""
    c.saveState()
    c.setStrokeColor(TEAL)
    c.setLineWidth(0.4)
    c.setStrokeAlpha(alpha)
    r = 18*mm
    for row in range(-1, 5):
        for col in range(-1, 6):
            cx_h = col * r * 1.73 + (row % 2) * r * 0.866
            cy_h = H/2 + row * r * 1.5 - 20*mm
            draw_hexagon(c, cx_h, cy_h, r, stroke_color=TEAL, lw=0.4)
    c.restoreState()


# ══════════════════════════════════════════════════════════════════════════════
# PAGE GENERATORS
# ══════════════════════════════════════════════════════════════════════════════

def page_cover(c):
    # Full black bg
    c.setFillColor(BLACK)
    c.rect(0, 0, W, H, fill=1, stroke=0)

    # Diagonal geometric accent panels
    c.saveState()
    c.setFillColor(TEAL)
    c.setFillAlpha(0.12)
    p = c.beginPath()
    p.moveTo(0, H)
    p.lineTo(W * 0.4, H)
    p.lineTo(W * 0.1, H * 0.5)
    p.lineTo(0, H * 0.6)
    p.close()
    c.drawPath(p, fill=1, stroke=0)
    c.restoreState()

    c.saveState()
    c.setFillColor(BLUE)
    c.setFillAlpha(0.08)
    p2 = c.beginPath()
    p2.moveTo(W * 0.5, H)
    p2.lineTo(W, H)
    p2.lineTo(W, H * 0.45)
    p2.lineTo(W * 0.3, H * 0.55)
    p2.close()
    c.drawPath(p2, fill=1, stroke=0)
    c.restoreState()

    c.saveState()
    c.setFillColor(GREEN)
    c.setFillAlpha(0.06)
    p3 = c.beginPath()
    p3.moveTo(W, 0)
    p3.lineTo(W, H * 0.35)
    p3.lineTo(W * 0.55, 0)
    p3.close()
    c.drawPath(p3, fill=1, stroke=0)
    c.restoreState()

    # Subtle hexagonal molecular grid — bottom-right quadrant only
    c.saveState()
    c.setStrokeColor(TEAL)
    c.setStrokeAlpha(0.035)
    c.setLineWidth(0.4)
    r = 24*mm
    for row in range(0, 4):
        for col in range(1, 5):
            hcx = col * r * 1.73 + (row % 2) * r * 0.866 + 60*mm
            hcy = H * 0.15 + row * r * 1.5
            draw_hexagon(c, hcx, hcy, r, stroke_color=TEAL, lw=0.4)
    c.restoreState()

    # Top accent bar
    c.setFillColor(TEAL)
    c.rect(0, H - 4*mm, W, 4*mm, fill=1, stroke=0)
    # Thin secondary accent
    c.setFillColor(BLUE)
    c.rect(0, H - 5.5*mm, W, 1*mm, fill=1, stroke=0)

    # SIGMA AUDLEY — refined small caps with thin rule
    set_font(c, bold=True, size=11)
    c.setFillColor(colors.HexColor('#666666'))
    c.drawCentredString(W/2, H - 48*mm, "S I G M A   A U D L E Y")
    set_font(c, size=8)
    c.setFillColor(DIM_TEXT)
    c.drawCentredString(W/2, H - 56*mm, "Research Peptide Manufacturing & Fulfilment")
    # Thin rule
    c.setStrokeColor(TEAL)
    c.setLineWidth(0.8)
    c.line(W/2 - 50*mm, H - 62*mm, W/2 + 50*mm, H - 62*mm)

    # Connector text
    set_font(c, size=9)
    c.setFillColor(MID_GREY)
    c.drawCentredString(W/2, H - 74*mm, "presents a private-label partnership to")

    # NOVALABS — large, authoritative
    set_font(c, bold=True, size=58)
    c.setFillColor(WHITE)
    c.drawCentredString(W/2, H - 98*mm, "NOVALABS")

    # Teal underline
    c.setFillColor(TEAL)
    c.rect(W/2 - 55*mm, H - 106*mm, 110*mm, 1*mm, fill=1, stroke=0)

    # Division subtitle
    set_font(c, size=11)
    c.setFillColor(TEAL)
    c.drawCentredString(W/2, H - 115*mm, "RESEARCH PEPTIDE DIVISION")

    # Document type — clean two-line title
    set_font(c, bold=True, size=26)
    c.setFillColor(WHITE)
    c.drawCentredString(W/2, H/2 + 24*mm, "PRIVATE LABEL PARTNERSHIP")
    set_font(c, bold=True, size=28)
    c.drawCentredString(W/2, H/2 + 6*mm, "PROPOSAL & QUOTE")

    # Thin rule
    c.setStrokeColor(TEAL)
    c.setLineWidth(0.8)
    c.line(W*0.25, H/2 - 6*mm, W*0.75, H/2 - 6*mm)

    # Prepared for — professional formatting
    set_font(c, size=10)
    c.setFillColor(SUB_TEXT)
    c.drawCentredString(W/2, H/2 - 20*mm, "Prepared for")
    set_font(c, bold=True, size=18)
    c.setFillColor(WHITE)
    c.drawCentredString(W/2, H/2 - 34*mm, "Manuel Lemus  —  NovaLabs")
    set_font(c, size=9)
    c.setFillColor(DIM_TEXT)
    c.drawCentredString(W/2, H/2 - 46*mm, "LATAM Market Entry Package  |  February 2026  |  Full Payment: USDC / USDT")

    # 3 product line cards at bottom — clean, professional
    card_data = [
        (TEAL,  "METABOLIC LINE",  "Tirzepatide · Retatrutide · HCG", "8 SKUs"),
        (GREEN, "RECOVERY LINE",   "BPC-157 · TB-500 · GHK-CU", "10 SKUs"),
        (BLUE,  "LONGEVITY LINE",  "NAD+ · Epithalon · MOTS-c", "10 SKUs"),
    ]
    cw = (W - 40*mm) / 3
    cy = 20*mm
    ch = 32*mm
    for i, (clr, title, sub, count) in enumerate(card_data):
        bx = 15*mm + i * (cw + 5*mm)
        c.setFillColor(CARD_BG)
        c.roundRect(bx, cy, cw, ch, 2*mm, fill=1, stroke=0)
        # Top accent line
        c.setFillColor(clr)
        c.rect(bx, cy + ch - 1.5*mm, cw, 1.5*mm, fill=1, stroke=0)
        # Count badge — clean circle
        c.setFillColor(clr)
        c.circle(bx + 10*mm, cy + ch - 10*mm, 4.5*mm, fill=1, stroke=0)
        c.setFillColor(BLACK)
        set_font(c, bold=True, size=6)
        c.drawCentredString(bx + 10*mm, cy + ch - 12*mm, count)
        # Title
        set_font(c, bold=True, size=8.5)
        c.setFillColor(clr)
        c.drawString(bx + 17*mm, cy + ch - 12*mm, title)
        # Sub
        set_font(c, size=7)
        c.setFillColor(DIM_TEXT)
        c.drawString(bx + 4*mm, cy + 5*mm, sub)

    # Bottom accent
    c.setFillColor(BLUE)
    c.rect(0, 0, W, 3*mm, fill=1, stroke=0)

    # Ref
    set_font(c, size=8)
    c.setFillColor(colors.HexColor('#444444'))
    c.drawCentredString(W/2, 8*mm, "CONFIDENTIAL  |  Ref: SA-9F4K7-26  |  Valid 30 Days")
    c.showPage()


def page_toc_executive(c):
    header_bar(c, H - 28*mm, h=28*mm, color=BLACK)
    set_font(c, bold=True, size=22)
    c.setFillColor(WHITE)
    c.drawString(15*mm, H - 18*mm, "CONTENTS  &  EXECUTIVE SUMMARY")
    c.setFillColor(TEAL)
    c.rect(15*mm, H - 28*mm, 80*mm, 1*mm, fill=1, stroke=0)

    # TOC — styled rows with left border, number badge, page pill
    toc = [
        ("01", "Executive Summary",              "p.2"),
        ("02", "NovaLabs Brand Identity",         "p.3"),
        ("03", "Full Product Catalogue",          "p.4-5"),
        ("04", "Private Label & OEM Services",    "p.6"),
        ("05", "MOQ & Pricing Tiers",             "p.7"),
        ("06", "Custom Packaging Options",        "p.8"),
        ("07", "Dropshipping & Fulfilment",       "p.9"),
        ("08", "Quality Assurance & Testing",     "p.10"),
        ("09", "International Shipping — LATAM",  "p.11"),
        ("10", "Detailed Quote — $15,023",        "p.12"),
        ("11", "Terms & Next Steps",              "p.13"),
        ("12", "Contact & Closing",               "p.14"),
    ]
    ty = H - 42*mm
    row_h = 8.5*mm
    for num, title, pg in toc:
        idx = int(num)
        clr = [TEAL, BLUE, GREEN][idx % 3]
        # Full-width row bg
        c.setFillColor(LIGHT_GREY if idx % 2 == 0 else WHITE)
        c.rect(15*mm, ty - 2*mm, W/2 - 25*mm, row_h, fill=1, stroke=0)
        # Left border
        c.setFillColor(clr)
        c.rect(15*mm, ty - 2*mm, 2*mm, row_h, fill=1, stroke=0)
        # Number circle badge
        c.setFillColor(clr)
        c.circle(23*mm, ty + 2*mm, 3.5*mm, fill=1, stroke=0)
        c.setFillColor(BLACK)
        set_font(c, bold=True, size=7.5)
        c.drawCentredString(23*mm, ty + 0.5*mm, num)
        # Title
        c.setFillColor(BLACK)
        set_font(c, size=10)
        c.drawString(30*mm, ty, title)
        # Page pill
        pw = c.stringWidth(pg, "Helvetica", 8) + 5*mm
        px = W/2 - 12*mm - pw
        c.setFillColor(clr)
        c.setFillAlpha(0.15)
        c.roundRect(px, ty - 1*mm, pw, 6*mm, 2*mm, fill=1, stroke=0)
        c.setFillAlpha(1)
        c.setFillColor(clr)
        set_font(c, bold=True, size=8)
        c.drawCentredString(px + pw/2, ty + 0.5*mm, pg)
        ty -= row_h + 1*mm

    # Executive summary — styled card
    bx = W/2 + 5*mm
    by = 18*mm
    bw = W/2 - 20*mm
    bh = H - 50*mm
    c.setFillColor(DARK_BG)
    c.roundRect(bx, by, bw, bh, 3*mm, fill=1, stroke=0)
    # Gradient accent top
    c.setFillColor(TEAL)
    c.setFillAlpha(0.1)
    c.roundRect(bx, by + bh - 20*mm, bw, 22*mm, 3*mm, fill=1, stroke=0)
    c.setFillAlpha(1)
    c.setFillColor(TEAL)
    c.rect(bx, by + bh - 1.5*mm, bw, 1.5*mm, fill=1, stroke=0)

    # Logomark circle
    c.setFillColor(TEAL)
    c.setFillAlpha(0.15)
    c.circle(bx + bw/2, by + bh - 10*mm, 6*mm, fill=1, stroke=0)
    c.setFillAlpha(1)
    c.setStrokeColor(TEAL)
    c.setLineWidth(1)
    c.circle(bx + bw/2, by + bh - 10*mm, 6*mm, fill=0, stroke=1)
    c.setFillColor(WHITE)
    set_font(c, bold=True, size=6)
    c.drawCentredString(bx + bw/2, by + bh - 12*mm, "SA")

    set_font(c, bold=True, size=13)
    c.setFillColor(WHITE)
    c.drawCentredString(bx + bw/2, by + bh - 24*mm, "EXECUTIVE SUMMARY")

    exec_text = [
        "Thank you for reaching out, Manuel.",
        "",
        "Sigma Audley is a US-based GMP-compliant",
        "research peptide manufacturer with 8+ years",
        "of white-label experience, trusted by brands",
        "across North America and Europe.",
        "",
        "This proposal answers every question you",
        "raised and presents a turnkey launch",
        "package designed to get NovaLabs live in",
        "the Colombian and LATAM markets fast —",
        "with US domestic fulfilment on day one.",
        "",
        "What's inside this package:",
    ]
    ey = by + bh - 38*mm
    for line in exec_text:
        if line == "":
            ey -= 3*mm
            continue
        c.setFillColor(SUB_TEXT)
        set_font(c, size=8.5)
        c.drawString(bx + 5*mm, ey, line)
        ey -= 6.5*mm

    # Check items with geometric tick icons
    check_items = [
        "13 premium research compounds",
        "Custom NovaLabs branding & labels",
        "Branded packaging & inserts",
        "US dropship fulfilment (6 months)",
        "COA + Janoshik 3rd-party testing",
        "Dedicated account manager",
    ]
    ey -= 2*mm
    for item in check_items:
        # Geometric tick
        draw_icon(c, bx + 3*mm, ey - 2*mm, "check", TEAL, size=5*mm)
        c.setFillColor(TEAL)
        set_font(c, size=8.5)
        c.drawString(bx + 12*mm, ey, item)
        ey -= 7*mm

    ey -= 3*mm
    c.setFillColor(HIGHLIGHT)
    set_font(c, bold=True, size=11)
    c.drawString(bx + 5*mm, ey, "Total investment: $15,023.00")

    page_footer(c, 2)
    c.showPage()


def page_brand_identity(c):
    header_bar(c, H - 28*mm, h=28*mm, color=BLACK)
    set_font(c, bold=True, size=22)
    c.setFillColor(WHITE)
    c.drawString(15*mm, H - 18*mm, "NOVALABS BRAND IDENTITY")
    c.setFillColor(TEAL)
    c.rect(15*mm, H - 28*mm, 60*mm, 1*mm, fill=1, stroke=0)

    section_title(c, "Your Three Product Lines — Label Concepts", H - 42*mm)

    set_font(c, size=9)
    c.setFillColor(MID_GREY)
    c.drawString(15*mm, H - 55*mm,
        "Below are your bespoke label designs. Each line carries its own colour identity for immediate shelf recognition.")

    # Three label mock-ups with drop shadows
    labels = [
        (TEAL,  "Metabolic Line",  "TIRZEPATIDE",  "10mg lyophilized", "NL-TZ-001",  "3ml Vial  |  50mm x 25mm"),
        (GREEN, "Recovery Line",   "BPC-157",       "10mg lyophilized", "NL-BPC-001", "3ml Vial  |  50mm x 25mm"),
        (BLUE,  "Longevity Line",  "NAD+",          "1000mg lyophilized","NL-NAD-001", "10ml Vial  |  50mm x 25mm"),
    ]
    lw = 42*mm
    lh = 60*mm
    gap = (W - 30*mm - 3 * lw) / 2
    lx_start = 15*mm
    ly = H - 130*mm

    for i, (clr, line_name, product, dosage, batch, vial_info) in enumerate(labels):
        lx = lx_start + i * (lw + gap)
        mini_label(c, lx, ly, lw, lh, product, line_name, dosage, batch, clr)
        c.setFillColor(MID_GREY)
        set_font(c, size=7.5)
        c.drawCentredString(lx + lw/2, ly - 6*mm, vial_info)
        c.setFillColor(clr)
        set_font(c, bold=True, size=8)
        c.drawCentredString(lx + lw/2, ly - 13*mm, line_name.upper())

    # Colour palette section
    section_title(c, "Brand Colour Palette", H - 160*mm)
    palette = [
        (BLACK,       "Primary Black",  "#0A0A0A", "Core background"),
        (TEAL,        "Metabolic Teal", "#00C4CC", "Metabolic product line"),
        (GREEN,       "Recovery Green", "#00E5A0", "Recovery product line"),
        (BLUE,        "Longevity Blue", "#4A90D9", "Longevity product line"),
        (WHITE,       "Label White",    "#FFFFFF",  "Type & primary text"),
    ]
    px = 15*mm
    py = H - 175*mm
    sw = (W - 30*mm) / len(palette) - 2*mm
    for clr, name, hex_val, desc in palette:
        c.setFillColor(clr)
        c.roundRect(px, py, sw, 16*mm, 2*mm, fill=1, stroke=0)
        if clr == WHITE:
            c.setStrokeColor(LINE_GREY)
            c.setLineWidth(0.5)
            c.roundRect(px, py, sw, 16*mm, 2*mm, fill=0, stroke=1)
        c.setFillColor(BLACK)
        set_font(c, bold=True, size=7)
        c.drawCentredString(px + sw/2, py - 6*mm, name)
        c.setFillColor(MID_GREY)
        set_font(c, size=6.5)
        c.drawCentredString(px + sw/2, py - 11*mm, hex_val)
        px += sw + 2*mm

    # Typography section — 2-column card grid
    section_title(c, "Typography & Packaging Notes", H - 212*mm)
    typo_items = [
        ("Wordmark",        "Helvetica Bold  |  All Caps  |  Tracking +50"),
        ("Product Names",   "Helvetica Bold  |  All Caps  |  22-28pt on label"),
        ("Body Copy",       "Helvetica Regular  |  8-10pt  |  Colour: #AAAAAA"),
        ("Batch / Legal",   "Helvetica Regular  |  7pt  |  Colour: #666666"),
        ("Label Stock",     "Matte BOPP, waterproof, cryogenic-rated  |  50mm x 25mm"),
        ("Vial Colours",    "Amber glass (standard)  |  Clear glass (on request)"),
    ]
    iy = H - 228*mm
    col_w_t = (W - 35*mm) / 2
    for idx, (label_t, val_t) in enumerate(typo_items):
        col = idx % 2
        row = idx // 2
        tx = 15*mm + col * (col_w_t + 5*mm)
        tty = iy - row * 14*mm
        # Card bg
        c.setFillColor(LIGHT_GREY)
        c.roundRect(tx, tty - 4*mm, col_w_t, 12*mm, 1.5*mm, fill=1, stroke=0)
        c.setFillColor(TEAL)
        set_font(c, bold=True, size=7.5)
        c.drawString(tx + 3*mm, tty + 2*mm, f"{label_t}:")
        c.setFillColor(MID_GREY)
        set_font(c, size=7)
        c.drawString(tx + 3*mm, tty - 3*mm, val_t[:55] + ("..." if len(val_t) > 55 else ""))

    # Additional label variants — styled info banner with icon
    banner_y = 28*mm
    c.setFillColor(CARD_BG)
    c.roundRect(15*mm, banner_y, W - 30*mm, 24*mm, 2*mm, fill=1, stroke=0)
    c.setFillColor(TEAL)
    c.rect(15*mm, banner_y, 3*mm, 24*mm, fill=1, stroke=0)
    draw_icon(c, 20*mm, banner_y + 6*mm, "tag", TEAL, size=10*mm)
    c.setFillColor(TEAL)
    set_font(c, bold=True, size=9)
    c.drawString(33*mm, banner_y + 18*mm, "ADDITIONAL LABEL VARIANTS AVAILABLE:")
    c.setFillColor(SUB_TEXT)
    set_font(c, size=8.5)
    c.drawString(33*mm, banner_y + 10*mm,
        "Kit labels  ·  Combo vial labels  ·  Reconstitution instruction cards")
    c.drawString(33*mm, banner_y + 4*mm,
        "Branded outer boxes  ·  Custom sizing on request")

    page_footer(c, 3)
    c.showPage()


def page_brand_in_use(c):
    """Visual brand mockup page — vials, boxes, packaging."""
    header_bar(c, H - 28*mm, h=28*mm, color=BLACK)
    set_font(c, bold=True, size=22)
    c.setFillColor(WHITE)
    c.drawString(15*mm, H - 18*mm, "NOVALABS BRAND IN USE — PRODUCT MOCKUPS")
    c.setFillColor(GREEN)
    c.rect(15*mm, H - 28*mm, 72*mm, 1*mm, fill=1, stroke=0)

    # Background shelf area with wood-grain texture
    c.setFillColor(colors.HexColor('#f5f5f5'))
    c.rect(0, H - 120*mm, W, 90*mm, fill=1, stroke=0)
    # Wood grain horizontal lines
    c.setStrokeColor(colors.HexColor('#e8e0d5'))
    c.setLineWidth(0.3)
    for i in range(20):
        wy = H - 120*mm + i * 4.5*mm
        c.line(0, wy, W, wy)
    # Shelf line with depth
    c.setFillColor(colors.HexColor('#c8bfb5'))
    c.rect(0, H - 121*mm, W, 3*mm, fill=1, stroke=0)
    c.setFillColor(colors.HexColor('#b0a89e'))
    c.rect(0, H - 122.5*mm, W, 1.5*mm, fill=1, stroke=0)

    # Draw 8 vials with glass highlight
    vial_configs = [
        (TEAL,    colors.HexColor('#333333'), BLACK, "TIRZEPATIDE",  "Metabolic",  "10mg lyoph.", TEAL),
        (TEAL,    colors.HexColor('#333333'), BLACK, "RETATRUTIDE",  "Metabolic",  "8mg lyoph.",  TEAL),
        (GREEN,   colors.HexColor('#2a2a2a'), BLACK, "BPC-157",       "Recovery",   "10mg lyoph.", GREEN),
        (GREEN,   colors.HexColor('#2a2a2a'), BLACK, "TB-500",        "Recovery",   "5mg lyoph.",  GREEN),
        (GREEN,   colors.HexColor('#2a2a2a'), BLACK, "GHK-CU",        "Recovery",   "50mg lyoph.", GREEN),
        (BLUE,    colors.HexColor('#1a2a3a'), BLACK, "NAD+",          "Longevity",  "1000mg",      BLUE),
        (BLUE,    colors.HexColor('#1a2a3a'), BLACK, "EPITHALON",     "Longevity",  "10mg lyoph.", BLUE),
        (BLUE,    colors.HexColor('#1a2a3a'), BLACK, "MOTS-c",        "Longevity",  "10mg lyoph.", BLUE),
    ]
    vw = 17*mm
    vh = 52*mm
    total_vials = len(vial_configs)
    vgap = (W - 30*mm - total_vials * vw) / (total_vials - 1)
    vx = 15*mm
    vy = H - 118*mm + 2*mm
    for cap_c, body_c, label_c, prod, line, dose, lc in vial_configs:
        draw_vial(c, vx, vy, vh, vw, body_c, cap_c, label_c, prod, line, dose, lc)
        vx += vw + vgap

    banners = [(TEAL, "METABOLIC LINE", 0, 2), (GREEN, "RECOVERY LINE", 2, 5), (BLUE, "LONGEVITY LINE", 5, 8)]
    for bclr, blabel, bstart, bend in banners:
        bx1 = 15*mm + bstart * (vw + vgap)
        bx2 = 15*mm + (bend - 1) * (vw + vgap) + vw
        c.setFillColor(bclr)
        c.roundRect(bx1, H - 126*mm, bx2 - bx1, 5*mm, 1*mm, fill=1, stroke=0)
        c.setFillColor(BLACK)
        set_font(c, bold=True, size=7)
        c.drawCentredString((bx1 + bx2) / 2, H - 124*mm, blabel)

    # Packaging box mockups with drop shadows
    section_title(c, "Branded Packaging Designs", H - 138*mm)
    box_data = [
        (TEAL,  "METABOLIC LINE", "TIRZEPATIDE", "10mg lyophilized",  "3ml Research Vial"),
        (GREEN, "RECOVERY LINE",  "BPC-157",      "10mg lyophilized",  "3ml Research Vial"),
        (BLUE,  "LONGEVITY LINE", "NAD+",         "1000mg lyophilized","10ml Research Vial"),
    ]
    bw = 52*mm
    bh = 70*mm
    bgap = (W - 30*mm - 3 * bw) / 2
    bx = 15*mm
    by = H - 220*mm
    for bclr, bline, bprod, bdose, bvial in box_data:
        # Drop shadow
        c.setFillColor(colors.HexColor('#d0d0d0'))
        c.roundRect(bx + 2*mm, by - 2*mm, bw, bh, 2*mm, fill=1, stroke=0)
        # Box body
        c.setFillColor(BLACK)
        c.roundRect(bx, by, bw, bh, 2*mm, fill=1, stroke=0)
        # Subtle texture strip
        c.setFillColor(WHITE)
        c.setFillAlpha(0.03)
        c.rect(bx + 1*mm, by + 5*mm, 2*mm, bh - 20*mm, fill=1, stroke=0)
        c.setFillAlpha(1)
        # Top colour band
        c.setFillColor(bclr)
        c.roundRect(bx, by + bh - 12*mm, bw, 14*mm, 2*mm, fill=1, stroke=0)
        c.setFillColor(BLACK)
        c.rect(bx, by + bh - 12*mm, bw, 6*mm, fill=1, stroke=0)
        # NOVALABS on box
        c.setFillColor(WHITE)
        set_font(c, bold=True, size=9)
        c.drawCentredString(bx + bw/2, by + bh - 6*mm, "NOVALABS")
        c.setFillColor(bclr)
        set_font(c, size=7)
        c.drawCentredString(bx + bw/2, by + bh - 19*mm, bline)
        c.setFillColor(WHITE)
        set_font(c, bold=True, size=11)
        c.drawCentredString(bx + bw/2, by + bh - 30*mm, bprod)
        c.setFillColor(SUB_TEXT)
        set_font(c, size=8)
        c.drawCentredString(bx + bw/2, by + bh - 39*mm, bdose)
        c.setStrokeColor(bclr)
        c.setLineWidth(1)
        c.line(bx + 6*mm, by + bh - 43*mm, bx + bw - 6*mm, by + bh - 43*mm)
        c.setFillColor(DIM_TEXT)
        set_font(c, size=7)
        c.drawCentredString(bx + bw/2, by + bh - 51*mm, bvial)
        # SCAN FOR COA button instead of QR
        c.setFillColor(bclr)
        c.roundRect(bx + bw/2 - 12*mm, by + 6*mm, 24*mm, 10*mm, 2*mm, fill=1, stroke=0)
        c.setFillColor(BLACK)
        set_font(c, bold=True, size=6)
        c.drawCentredString(bx + bw/2, by + 10*mm, "SCAN FOR COA")
        c.setFillColor(DIM_TEXT)
        set_font(c, size=5.5)
        c.drawCentredString(bx + bw/2, by + 2*mm, "For Lab Research Use Only")
        bx += bw + bgap

    # Branded mailer mockup
    section_title(c, "Branded Shipping Mailer & Insert Card", H - 234*mm)
    mx = 15*mm
    my = H - 262*mm
    mw = 90*mm
    mh = 24*mm
    c.setFillColor(DARK_BG)
    c.roundRect(mx, my, mw, mh, 2*mm, fill=1, stroke=0)
    c.setFillColor(TEAL)
    c.roundRect(mx, my + mh - 3*mm, mw, 5*mm, 2*mm, fill=1, stroke=0)
    set_font(c, bold=True, size=9)
    c.setFillColor(BLACK)
    c.drawString(mx + 4*mm, my + mh - 1*mm, "NOVALABS RESEARCH")
    set_font(c, size=7)
    c.setFillColor(DIM_TEXT)
    c.drawString(mx + 4*mm, my + mh - 9*mm, "novalabs-research.com")
    c.drawString(mx + 4*mm, my + mh - 15*mm, "For: MANUEL LEMUS — MIAMI, FL")
    c.setFillColor(TEAL)
    set_font(c, bold=True, size=7)
    c.drawString(mx + 4*mm, my + 3*mm, "RESEARCH MATERIALS — HANDLE WITH CARE")

    # Insert card
    cx_ins = mx + mw + 10*mm
    iw = 70*mm
    ih = 40*mm
    c.setFillColor(WHITE)
    c.roundRect(cx_ins, my - 8*mm, iw, ih, 2*mm, fill=1, stroke=0)
    c.setStrokeColor(LINE_GREY)
    c.setLineWidth(0.5)
    c.roundRect(cx_ins, my - 8*mm, iw, ih, 2*mm, fill=0, stroke=1)
    c.setFillColor(BLACK)
    c.rect(cx_ins, my - 8*mm + ih - 9*mm, iw, 9*mm, fill=1, stroke=0)
    c.setFillColor(WHITE)
    set_font(c, bold=True, size=8)
    c.drawString(cx_ins + 3*mm, my - 8*mm + ih - 5*mm, "NOVALABS  |  RECONSTITUTION GUIDE")
    c.setFillColor(TEAL)
    set_font(c, bold=True, size=7.5)
    c.drawString(cx_ins + 3*mm, my - 8*mm + ih - 16*mm, "Step 1:")
    c.setFillColor(MID_GREY)
    set_font(c, size=7)
    c.drawString(cx_ins + 18*mm, my - 8*mm + ih - 16*mm, "Allow vial to reach room temperature")
    c.setFillColor(TEAL)
    set_font(c, bold=True, size=7.5)
    c.drawString(cx_ins + 3*mm, my - 8*mm + ih - 23*mm, "Step 2:")
    c.setFillColor(MID_GREY)
    set_font(c, size=7)
    c.drawString(cx_ins + 18*mm, my - 8*mm + ih - 23*mm, "Add 1-2ml bacteriostatic water slowly")
    c.setFillColor(TEAL)
    set_font(c, bold=True, size=7.5)
    c.drawString(cx_ins + 3*mm, my - 8*mm + ih - 30*mm, "Step 3:")
    c.setFillColor(MID_GREY)
    set_font(c, size=7)
    c.drawString(cx_ins + 18*mm, my - 8*mm + ih - 30*mm, "Gently swirl — do not shake. Store 4C")
    c.setFillColor(DIM_TEXT)
    set_font(c, size=6)
    c.drawString(cx_ins + 3*mm, my - 8*mm + 2*mm, "Scan QR for full COA  |  verify.janoshik.com.sigmaaudley.site")

    page_footer(c, 4)
    c.showPage()


def page_marketing_assets(c):
    """Social media, marketing concepts and brand guidelines."""
    header_bar(c, H - 28*mm, h=28*mm, color=BLACK)
    set_font(c, bold=True, size=22)
    c.setFillColor(WHITE)
    c.drawString(15*mm, H - 18*mm, "MARKETING ASSET CONCEPTS")
    c.setFillColor(BLUE)
    c.rect(15*mm, H - 28*mm, 52*mm, 1*mm, fill=1, stroke=0)

    section_title(c, "Social Media Post Templates", H - 42*mm)

    # 3 social card mockups with phone-chrome border
    card_configs = [
        (TEAL,  "METABOLIC LINE",   "TIRZEPATIDE",   "New in stock.",     "10mg  ·  Lyophilized",   "#novalabs #research"),
        (GREEN, "RECOVERY LINE",    "BPC-157",        "Fast recovery.",    "10mg  ·  Lyophilized",   "#bpc157 #recovery"),
        (BLUE,  "LONGEVITY LINE",   "NAD+",           "Optimise your NAD+","1000mg  ·  Lyophilized", "#nad #longevity"),
    ]
    cw = (W - 35*mm) / 3
    cy = H - 122*mm
    ch = 74*mm
    cgap = 2.5*mm
    cx_s = 15*mm
    for clr, line, prod, tagline, spec, hashtag in card_configs:
        # Phone chrome border
        c.setFillColor(colors.HexColor('#333333'))
        c.roundRect(cx_s - 1*mm, cy - 1*mm, cw + 2*mm, ch + 6*mm, 4*mm, fill=1, stroke=0)
        # Notch
        c.setFillColor(colors.HexColor('#222222'))
        c.roundRect(cx_s + cw/2 - 8*mm, cy + ch + 2*mm, 16*mm, 2.5*mm, 1*mm, fill=1, stroke=0)
        # Card body
        c.setFillColor(BLACK)
        c.roundRect(cx_s, cy, cw, ch, 2*mm, fill=1, stroke=0)
        # Gradient effect
        for si in range(5):
            alpha_val = 0.06 - si * 0.01
            c.setFillColor(clr)
            c.setFillAlpha(max(alpha_val, 0))
            c.rect(cx_s, cy + ch - (si + 1) * ch/5, cw, ch/5, fill=1, stroke=0)
        c.setFillAlpha(1)
        # Accent line top
        c.setFillColor(clr)
        c.rect(cx_s, cy + ch - 2*mm, cw, 2*mm, fill=1, stroke=0)
        # Instagram-style top bar
        c.setFillColor(colors.HexColor('#1a1a1a'))
        c.rect(cx_s, cy + ch - 10*mm, cw, 8*mm, fill=1, stroke=0)
        c.setFillColor(clr)
        set_font(c, bold=True, size=6)
        c.drawString(cx_s + 2*mm, cy + ch - 6.5*mm, "novalabs_research")
        # Notification bubble
        c.setFillColor(colors.HexColor('#ff3b30'))
        c.circle(cx_s + cw - 5*mm, cy + ch - 5*mm, 2.5*mm, fill=1, stroke=0)
        c.setFillColor(WHITE)
        set_font(c, bold=True, size=5)
        c.drawCentredString(cx_s + cw - 5*mm, cy + ch - 6.5*mm, "3")
        c.setFillColor(DIM_TEXT)
        set_font(c, size=5)
        c.drawString(cx_s + 2*mm, cy + ch - 9.5*mm, "Sponsored")
        # Product vial
        draw_vial(c, cx_s + cw/2 - 6*mm, cy + ch - 54*mm, 38*mm, 12*mm,
                  colors.HexColor('#1a1a1a'), clr, BLACK, prod, line, spec, clr)
        # Caption area
        c.setFillColor(colors.HexColor('#111111'))
        c.rect(cx_s, cy, cw, 22*mm, fill=1, stroke=0)
        # Like/comment icons
        c.setStrokeColor(WHITE)
        c.setLineWidth(0.8)
        # Heart outline
        hx_i = cx_s + 3*mm
        hy_i = cy + 16*mm
        c.circle(hx_i + 1.5*mm, hy_i + 1*mm, 1.5*mm, fill=0, stroke=1)
        c.circle(hx_i + 4*mm, hy_i + 1*mm, 1.5*mm, fill=0, stroke=1)
        # Comment icon
        c.circle(hx_i + 10*mm, hy_i + 0.5*mm, 2*mm, fill=0, stroke=1)
        # Share icon
        c.line(hx_i + 16*mm, hy_i + 2*mm, hx_i + 18*mm, hy_i)
        c.line(hx_i + 18*mm, hy_i, hx_i + 16*mm, hy_i - 2*mm)

        c.setFillColor(WHITE)
        set_font(c, bold=True, size=7.5)
        c.drawString(cx_s + 2*mm, cy + 11*mm, prod)
        c.setFillColor(SUB_TEXT)
        set_font(c, size=6.5)
        c.drawString(cx_s + 2*mm, cy + 6*mm, tagline)
        c.setFillColor(clr)
        set_font(c, size=6)
        c.drawString(cx_s + 2*mm, cy + 1.5*mm, hashtag)
        cx_s += cw + cgap

    # Website hero banner mockup
    section_title(c, "Website Hero Banner", H - 204*mm)
    ex = 15*mm
    ey = H - 246*mm
    ew = W - 30*mm
    eh = 38*mm
    # Browser chrome
    c.setFillColor(colors.HexColor('#2a2a2a'))
    c.roundRect(ex, ey + eh, ew, 8*mm, 2*mm, fill=1, stroke=0)
    c.setFillColor(colors.HexColor('#444444'))
    c.roundRect(ex, ey + eh, ew, 4*mm, 0, fill=1, stroke=0)
    # Traffic light dots
    for di, dc in enumerate([colors.HexColor('#ff5f57'), colors.HexColor('#ffbd2e'), colors.HexColor('#28ca41')]):
        c.setFillColor(dc)
        c.circle(ex + 5*mm + di * 5*mm, ey + eh + 5*mm, 1.5*mm, fill=1, stroke=0)
    # URL bar
    c.setFillColor(colors.HexColor('#3a3a3a'))
    c.roundRect(ex + 30*mm, ey + eh + 2.5*mm, ew - 40*mm, 5*mm, 2*mm, fill=1, stroke=0)
    c.setFillColor(DIM_TEXT)
    set_font(c, size=5.5)
    c.drawString(ex + 33*mm, ey + eh + 4*mm, "novalabs-research.com")
    # Hero content
    c.setFillColor(BLACK)
    c.rect(ex, ey, ew, eh, fill=1, stroke=0)
    # Gradient overlay
    c.setFillColor(TEAL)
    c.setFillAlpha(0.08)
    p = c.beginPath()
    p.moveTo(ex, ey)
    p.lineTo(ex + ew * 0.4, ey)
    p.lineTo(ex + ew * 0.6, ey + eh)
    p.lineTo(ex, ey + eh)
    p.close()
    c.drawPath(p, fill=1, stroke=0)
    c.setFillAlpha(1)
    c.setFillColor(TEAL)
    c.rect(ex, ey + eh - 2*mm, ew, 2*mm, fill=1, stroke=0)
    set_font(c, bold=True, size=20)
    c.setFillColor(WHITE)
    c.drawString(ex + 10*mm, ey + eh - 16*mm, "NOVALABS")
    c.setFillColor(TEAL)
    set_font(c, size=10)
    c.drawString(ex + 10*mm, ey + eh - 26*mm, "Research Peptide Division  |  For Laboratory Use Only")
    # CTA button
    c.setFillColor(TEAL)
    c.roundRect(ex + 10*mm, ey + 4*mm, 30*mm, 8*mm, 2*mm, fill=1, stroke=0)
    c.setFillColor(BLACK)
    set_font(c, bold=True, size=7)
    c.drawCentredString(ex + 25*mm, ey + 7*mm, "SHOP NOW")
    # Right side line colour bars
    for i, (clr_b, lname) in enumerate([(TEAL, "METABOLIC"), (GREEN, "RECOVERY"), (BLUE, "LONGEVITY")]):
        bx2 = ex + ew - 8*mm - i * 40*mm
        c.setFillColor(clr_b)
        c.roundRect(bx2 - 32*mm, ey + 3*mm, 32*mm, 8*mm, 1*mm, fill=1, stroke=0)
        c.setFillColor(BLACK)
        set_font(c, bold=True, size=6)
        c.drawCentredString(bx2 - 16*mm, ey + 6*mm, lname)

    # Business card with foil-effect diagonal stripe
    section_title(c, "Business Card Design", H - 260*mm)
    card_y = H - 292*mm
    fcard_x = 15*mm
    fcard_w = 85*mm
    fcard_h = 50*mm
    c.setFillColor(BLACK)
    c.roundRect(fcard_x, card_y, fcard_w, fcard_h, 2*mm, fill=1, stroke=0)
    # Foil-effect diagonal stripe
    c.saveState()
    c.setFillColor(WHITE)
    c.setFillAlpha(0.04)
    p = c.beginPath()
    p.moveTo(fcard_x + fcard_w * 0.6, card_y)
    p.lineTo(fcard_x + fcard_w * 0.7, card_y)
    p.lineTo(fcard_x + fcard_w * 0.3, card_y + fcard_h)
    p.lineTo(fcard_x + fcard_w * 0.2, card_y + fcard_h)
    p.close()
    c.drawPath(p, fill=1, stroke=0)
    c.setFillAlpha(0.025)
    p2 = c.beginPath()
    p2.moveTo(fcard_x + fcard_w * 0.72, card_y)
    p2.lineTo(fcard_x + fcard_w * 0.78, card_y)
    p2.lineTo(fcard_x + fcard_w * 0.38, card_y + fcard_h)
    p2.lineTo(fcard_x + fcard_w * 0.32, card_y + fcard_h)
    p2.close()
    c.drawPath(p2, fill=1, stroke=0)
    c.restoreState()
    c.setFillColor(TEAL)
    c.rect(fcard_x, card_y + fcard_h - 2*mm, fcard_w, 2*mm, fill=1, stroke=0)
    c.setFillColor(BLUE)
    c.rect(fcard_x, card_y, fcard_w, 2*mm, fill=1, stroke=0)
    set_font(c, bold=True, size=14)
    c.setFillColor(WHITE)
    c.drawString(fcard_x + 5*mm, card_y + fcard_h - 14*mm, "NOVALABS")
    c.setFillColor(TEAL)
    set_font(c, size=7)
    c.drawString(fcard_x + 5*mm, card_y + fcard_h - 21*mm, "RESEARCH PEPTIDE DIVISION")
    c.setFillColor(SUB_TEXT)
    set_font(c, size=8)
    c.drawString(fcard_x + 5*mm, card_y + fcard_h - 33*mm, "Manuel Lemus")
    set_font(c, bold=True, size=8)
    c.setFillColor(WHITE)
    c.drawString(fcard_x + 5*mm, card_y + fcard_h - 40*mm, "Founder & Director")
    c.setFillColor(DIM_TEXT)
    set_font(c, size=7)
    c.drawString(fcard_x + 5*mm, card_y + 8*mm, "mlyidios@gmail.com")
    c.drawString(fcard_x + 5*mm, card_y + 4*mm, "novalabs-research.com")

    # Back of card
    bcard_x = fcard_x + fcard_w + 6*mm
    c.setFillColor(TEAL)
    c.roundRect(bcard_x, card_y, fcard_w, fcard_h, 2*mm, fill=1, stroke=0)
    set_font(c, bold=True, size=22)
    c.setFillColor(BLACK)
    c.drawCentredString(bcard_x + fcard_w/2, card_y + fcard_h/2 - 5*mm, "NOVALABS")
    set_font(c, size=8)
    c.drawCentredString(bcard_x + fcard_w/2, card_y + 8*mm, "Research Peptide Division")

    page_footer(c, 5)
    c.showPage()


def page_revenue_projection(c):
    """ROI & revenue projection."""
    header_bar(c, H - 28*mm, h=28*mm, color=BLACK)
    set_font(c, bold=True, size=22)
    c.setFillColor(WHITE)
    c.drawString(15*mm, H - 18*mm, "REVENUE PROJECTIONS & ROI")
    c.setFillColor(HIGHLIGHT)
    c.rect(15*mm, H - 28*mm, 50*mm, 1*mm, fill=1, stroke=0)

    section_title(c, "Your NovaLabs Business Case — LATAM Market", H - 42*mm)

    set_font(c, size=9)
    c.setFillColor(MID_GREY)
    c.drawString(15*mm, H - 54*mm,
        "Based on conservative LATAM research peptide market growth rates (18% YoY) and typical private-label margins.")

    # Assumptions box
    c.setFillColor(CARD_BG)
    c.roundRect(15*mm, H - 100*mm, W - 30*mm, 40*mm, 2*mm, fill=1, stroke=0)
    c.setFillColor(TEAL)
    set_font(c, bold=True, size=9)
    c.drawString(20*mm, H - 66*mm, "KEY ASSUMPTIONS:")
    assumptions = [
        ("Avg. selling price per vial (retail)", "$65 - $120 USD"),
        ("Our supply price (this package)",      "$15 - $48 USD"),
        ("Gross margin per vial",                "55% - 75%"),
        ("Initial inventory (this order)",       "390 units across 14 SKUs"),
        ("Target monthly orders (Month 6)",      "80-150 orders"),
    ]
    ax = 20*mm
    ay = H - 76*mm
    for lbl, val in assumptions:
        c.setFillColor(SUB_TEXT)
        set_font(c, size=8.5)
        c.drawString(ax, ay, lbl)
        c.setFillColor(TEAL)
        set_font(c, bold=True, size=8.5)
        c.drawRightString(W - 20*mm, ay, val)
        ay -= 5.5*mm

    # Revenue table
    section_title(c, "12-Month Revenue Forecast", H - 110*mm)
    months = ["M1", "M2", "M3", "M4", "M5", "M6", "M7", "M8", "M9", "M10", "M11", "M12"]
    orders =  [10,   18,   28,   40,   52,   70,   85,   100,  115,  130,   145,   165]
    avg_val = [85,   88,   90,   92,   92,   95,   97,   98,   99,   100,   102,   105]
    revenue = [o * v for o, v in zip(orders, avg_val)]
    cogs    = [o * 32 for o in orders]
    profit  = [r - cg for r, cg in zip(revenue, cogs)]

    hx = 15*mm
    hy = H - 125*mm
    col_w = (W - 30*mm) / 13
    c.setFillColor(BLACK)
    c.rect(hx, hy, W - 30*mm, 8*mm, fill=1, stroke=0)
    c.setFillColor(TEAL)
    set_font(c, bold=True, size=7.5)
    c.drawString(hx + 2*mm, hy + 2.5*mm, "METRIC")
    for i, mo in enumerate(months):
        c.drawCentredString(hx + col_w + i * col_w + col_w/2, hy + 2.5*mm, mo)

    rows_data = [
        ("Orders", orders, MID_GREY, False),
        ("Revenue ($)", [f"${r:,}" for r in revenue], TEAL, True),
        ("COGS ($)", [f"${g:,}" for g in cogs], MID_GREY, False),
        ("Gross Profit ($)", [f"${p:,}" for p in profit], GREEN, True),
    ]
    ry = hy - 8*mm
    for j, (label, vals, clr, bold) in enumerate(rows_data):
        c.setFillColor(LIGHT_GREY if j % 2 == 0 else WHITE)
        c.rect(hx, ry, W - 30*mm, 8*mm, fill=1, stroke=0)
        c.setFillColor(BLACK)
        set_font(c, bold=True, size=8)
        c.drawString(hx + 2*mm, ry + 2.5*mm, label)
        for i, val in enumerate(vals):
            c.setFillColor(clr)
            set_font(c, bold=bold, size=7.5)
            c.drawCentredString(hx + col_w + i * col_w + col_w/2, ry + 2.5*mm, str(val))
        ry -= 8*mm

    # Bar chart with rounded tops, gridline glow, value labels with pill
    section_title(c, "Monthly Gross Profit Visualisation", ry - 8*mm)
    chart_y_base = ry - 14*mm
    chart_h = 45*mm
    chart_x = 15*mm
    chart_w = W - 30*mm
    bar_w = chart_w / 12 - 2*mm
    max_profit = max(profit)

    c.setFillColor(LIGHT_GREY)
    c.rect(chart_x, chart_y_base - chart_h, chart_w, chart_h, fill=1, stroke=0)

    # Y-axis reference lines with glow
    for ref_val in [2000, 4000, 6000, 8000]:
        ref_y = chart_y_base - chart_h + (ref_val / max_profit) * (chart_h - 5*mm)
        # Glow
        c.setStrokeColor(TEAL)
        c.setStrokeAlpha(0.08)
        c.setLineWidth(3)
        c.line(chart_x, ref_y, chart_x + chart_w, ref_y)
        c.setStrokeAlpha(1)
        c.setStrokeColor(colors.HexColor('#dddddd'))
        c.setLineWidth(0.4)
        c.line(chart_x, ref_y, chart_x + chart_w, ref_y)
        c.setFillColor(DIM_TEXT)
        set_font(c, size=5.5)
        c.drawString(chart_x - 12*mm, ref_y - 1*mm, f"${ref_val:,}")

    # Bars with rounded tops
    for i, p_val in enumerate(profit):
        bh_bar = (p_val / max_profit) * (chart_h - 5*mm)
        bx_bar = chart_x + i * (chart_w / 12) + 1*mm
        intensity = 0.4 + 0.6 * (p_val / max_profit)
        bar_color = colors.HexColor(
            '#{:02x}{:02x}{:02x}'.format(
                int(0 * intensity),
                int(196 * intensity),
                int(204 * intensity)
            )
        )
        c.setFillColor(bar_color)
        c.roundRect(bx_bar, chart_y_base - chart_h, bar_w, bh_bar, 1.5*mm, fill=1, stroke=0)
        # Value label with teal pill background
        lbl_w = c.stringWidth(f"${p_val:,}", "Helvetica-Bold", 5.5) + 3*mm
        lbl_x = bx_bar + bar_w/2 - lbl_w/2
        lbl_y = chart_y_base - chart_h + bh_bar + 0.5*mm
        c.setFillColor(TEAL)
        c.setFillAlpha(0.15)
        c.roundRect(lbl_x, lbl_y, lbl_w, 4.5*mm, 1*mm, fill=1, stroke=0)
        c.setFillAlpha(1)
        c.setFillColor(BLACK)
        set_font(c, bold=True, size=5.5)
        c.drawCentredString(bx_bar + bar_w/2, lbl_y + 1*mm, f"${p_val:,}")
        # Month label
        c.setFillColor(MID_GREY)
        set_font(c, size=6)
        c.drawCentredString(bx_bar + bar_w/2, chart_y_base - chart_h - 4*mm, months[i])

    # Trend line overlay
    c.setStrokeColor(HIGHLIGHT)
    c.setLineWidth(1.5)
    for i in range(len(profit) - 1):
        x1 = chart_x + i * (chart_w / 12) + 1*mm + bar_w/2
        y1 = chart_y_base - chart_h + (profit[i] / max_profit) * (chart_h - 5*mm)
        x2 = chart_x + (i+1) * (chart_w / 12) + 1*mm + bar_w/2
        y2 = chart_y_base - chart_h + (profit[i+1] / max_profit) * (chart_h - 5*mm)
        c.line(x1, y1, x2, y2)

    # KPI cards — larger with arrow indicator
    total_rev = sum(revenue)
    total_profit = sum(profit)
    roi_y = chart_y_base - chart_h - 20*mm

    kpis = [
        (TEAL,  "Year 1 Revenue",     f"${total_rev:,}"),
        (GREEN, "Year 1 Gross Profit", f"${total_profit:,}"),
        (BLUE,  "ROI on $15,023",     f"{int(total_profit/15023*100)}%"),
        (HIGHLIGHT, "Payback Period",  "~3 months"),
    ]
    kw = (W - 30*mm) / 4 - 2*mm
    kx = 15*mm
    for kclr, ktitle, kval in kpis:
        c.setFillColor(CARD_BG)
        c.roundRect(kx, roi_y - 14*mm, kw, 22*mm, 2*mm, fill=1, stroke=0)
        # Bold number
        c.setFillColor(kclr)
        set_font(c, bold=True, size=15)
        c.drawCentredString(kx + kw/2, roi_y + 1*mm, kval)
        # Upward arrow indicator
        ax_i = kx + kw - 8*mm
        ay_i = roi_y + 3*mm
        c.setFillColor(kclr)
        p = c.beginPath()
        p.moveTo(ax_i, ay_i + 3*mm)
        p.lineTo(ax_i + 2*mm, ay_i)
        p.lineTo(ax_i - 2*mm, ay_i)
        p.close()
        c.drawPath(p, fill=1, stroke=0)
        c.setFillColor(SUB_TEXT)
        set_font(c, size=7)
        c.drawCentredString(kx + kw/2, roi_y - 10*mm, ktitle)
        kx += kw + 2*mm

    page_footer(c, 6)
    c.showPage()


def page_latam_roadmap(c):
    """LATAM market strategy and 12-month roadmap."""
    header_bar(c, H - 28*mm, h=28*mm, color=BLACK)
    set_font(c, bold=True, size=22)
    c.setFillColor(WHITE)
    c.drawString(15*mm, H - 18*mm, "LATAM MARKET STRATEGY & ROADMAP")
    c.setFillColor(GREEN)
    c.rect(15*mm, H - 28*mm, 65*mm, 1*mm, fill=1, stroke=0)

    section_title(c, "NovaLabs LATAM Launch Plan — 12 Months", H - 42*mm)

    quarters = [
        (TEAL, "Q1 — LAUNCH", "Feb - Apr 2026", [
            "Confirm order & sign partnership agreement",
            "Approve label & packaging designs",
            "Inventory production & QA (25 days)",
            "US warehouse activated",
            "Website & brand launch",
            "First Colombian orders dispatched",
        ]),
        (GREEN, "Q2 — GROW", "May - Jul 2026", [
            "Add 3-5 new SKUs from catalogue",
            "Launch subscription box (monthly kits)",
            "Social media campaign — Colombia & Mexico",
            "Onboard first 3 B2B wholesale clients",
            "Reorder batch 2 (Growth tier MOQ)",
            "Target: 50+ monthly orders",
        ]),
        (BLUE, "Q3 — SCALE", "Aug - Oct 2026", [
            "Expand to Mexico, Argentina, Chile",
            "Launch affiliate / influencer programme",
            "Add Kit bundles (KLOW80, recovery kits)",
            "Upgrade to SCALE fulfilment plan",
            "Apply 20% volume discount on reorders",
            "Target: 100+ monthly orders",
        ]),
        (HIGHLIGHT, "Q4 — DOMINATE", "Nov 2026 - Jan 2027", [
            "Full LATAM distribution network",
            "Co-marketing fund activation",
            "Consider EU expansion",
            "Explore custom synthesis exclusives",
            "Negotiate Partner tier exclusivity deal",
            "Target: $25K+ monthly revenue",
        ]),
    ]

    qy = H - 58*mm
    qw = (W - 35*mm) / 2
    for qi, (qclr, qtitle, qdate, qitems) in enumerate(quarters):
        col = qi % 2
        row = qi // 2
        qx = 15*mm + col * (qw + 5*mm)
        qyy = qy - row * 90*mm
        c.setFillColor(CARD_BG)
        c.roundRect(qx, qyy - 78*mm, qw, 80*mm, 2*mm, fill=1, stroke=0)
        # Diagonal colour accent in corner
        c.saveState()
        c.clipPath(c.beginPath())
        p = c.beginPath()
        p.moveTo(qx + qw - 20*mm, qyy + 2*mm)
        p.lineTo(qx + qw, qyy + 2*mm)
        p.lineTo(qx + qw, qyy - 18*mm)
        p.close()
        c.setFillColor(qclr)
        c.setFillAlpha(0.12)
        c.drawPath(p, fill=1, stroke=0)
        c.restoreState()
        c.setFillColor(qclr)
        c.rect(qx, qyy + 2*mm - 1.5*mm, qw, 1.5*mm, fill=1, stroke=0)
        # Large bold quarter number
        set_font(c, bold=True, size=28)
        c.setFillColor(qclr)
        c.setFillAlpha(0.12)
        c.drawRightString(qx + qw - 4*mm, qyy - 68*mm, f"Q{qi+1}")
        c.setFillAlpha(1)
        set_font(c, bold=True, size=11)
        c.setFillColor(qclr)
        c.drawString(qx + 4*mm, qyy - 8*mm, qtitle)
        c.setFillColor(DIM_TEXT)
        set_font(c, size=8)
        c.drawString(qx + 4*mm, qyy - 15*mm, qdate)
        iy = qyy - 24*mm
        for item in qitems:
            c.setFillColor(qclr)
            c.circle(qx + 7*mm, iy + 1.5*mm, 1.2*mm, fill=1, stroke=0)
            c.setFillColor(SUB_TEXT)
            set_font(c, size=8)
            c.drawString(qx + 10*mm, iy, item)
            iy -= 8*mm

    # Target markets with coloured letter-code badges
    section_title(c, "Target Markets — LATAM Priority", H - 248*mm)
    markets = [
        (TEAL,  "CO", "Colombia",   "Primary launch market. Growing wellness sector.",     "$1.2B"),
        (GREEN, "MX", "Mexico",     "Largest LATAM economy. High demand for peptides.", "$3.8B"),
        (BLUE,  "AR", "Argentina",  "Sophisticated consumer market, bio-culture.", "$0.9B"),
        (TEAL,  "CL", "Chile",      "Stable economy, premium positioning potential.",  "$0.7B"),
        (GREEN, "PE", "Peru",       "Fast-growing middle class, wellness spend.",      "$0.5B"),
        (BLUE,  "BR", "Brazil",     "Largest market by population — long-term.",       "$8.2B"),
    ]
    mx_m = 15*mm
    my_m = H - 262*mm
    mw_m = (W - 35*mm) / 3 - 1*mm
    mgap = 2.5*mm
    for mi, (mclr, mcode, mname, mdesc, msize) in enumerate(markets):
        col = mi % 3
        row = mi // 3
        mmx = mx_m + col * (mw_m + mgap)
        mmy = my_m - row * 20*mm
        c.setFillColor(LIGHT_GREY)
        c.roundRect(mmx, mmy - 14*mm, mw_m, 16*mm, 1.5*mm, fill=1, stroke=0)
        # Flag-style letter badge
        c.setFillColor(mclr)
        c.roundRect(mmx, mmy - 14*mm, 12*mm, 16*mm, 1.5*mm, fill=1, stroke=0)
        c.setFillColor(BLACK)
        set_font(c, bold=True, size=9)
        c.drawCentredString(mmx + 6*mm, mmy - 8*mm, mcode)
        # Name
        set_font(c, bold=True, size=9)
        c.setFillColor(BLACK)
        c.drawString(mmx + 15*mm, mmy - 4*mm, mname)
        c.setFillColor(mclr)
        set_font(c, bold=True, size=8)
        c.drawRightString(mmx + mw_m - 3*mm, mmy - 4*mm, msize)
        c.setFillColor(MID_GREY)
        set_font(c, size=7)
        c.drawString(mmx + 15*mm, mmy - 11*mm, mdesc[:50] + ("..." if len(mdesc) > 50 else ""))

    page_footer(c, 7)
    c.showPage()


def page_catalogue_1(c):
    header_bar(c, H - 28*mm, h=28*mm, color=BLACK)
    set_font(c, bold=True, size=22)
    c.setFillColor(WHITE)
    c.drawString(15*mm, H - 18*mm, "FULL PRODUCT CATALOGUE  — PART 1")
    c.setFillColor(TEAL)
    c.rect(15*mm, H - 28*mm, 68*mm, 1*mm, fill=1, stroke=0)

    # Metabolic Line — full-width coloured band header
    c.setFillColor(TEAL)
    c.setFillAlpha(0.12)
    c.rect(15*mm, H - 42*mm, W - 30*mm, 10*mm, fill=1, stroke=0)
    c.setFillAlpha(1)
    c.setFillColor(TEAL)
    c.rect(15*mm, H - 42*mm, 3*mm, 10*mm, fill=1, stroke=0)
    set_font(c, bold=True, size=14)
    c.drawString(22*mm, H - 40*mm, "Metabolic Line")

    cols = [("PRODUCT", 52*mm), ("FORM", 20*mm), ("STRENGTH", 22*mm), ("VIAL", 18*mm),
            ("MOQ", 13*mm), ("UNIT PRICE", 22*mm), ("BATCH CODE", 28*mm)]
    hx = 15*mm
    hy = H - 55*mm
    c.setFillColor(BLACK)
    c.rect(hx, hy, W - 30*mm, 8*mm, fill=1, stroke=0)
    cx = hx + 2*mm
    for col_name, col_w in cols:
        set_font(c, bold=True, size=7.5)
        c.setFillColor(TEAL)
        c.drawString(cx, hy + 2.5*mm, col_name)
        cx += col_w

    metabolic = [
        ("Tirzepatide",                "Lyophilized", "5mg / 10mg",  "3ml",  "25",  "$22.00", "NL-TZ-001"),
        ("Retatrutide",                "Lyophilized", "8mg / 12mg",  "3ml",  "25",  "$28.00", "NL-RET-001"),
        ("Semaglutide",                "Lyophilized", "2mg / 5mg",   "3ml",  "25",  "$18.00", "NL-SEM-001"),
        ("Liraglutide",                "Lyophilized", "18mg",        "3ml",  "25",  "$15.00", "NL-LIR-001"),
        ("HCG (Human Chorionic Gon.)", "Lyophilized", "2000IU/5000IU","3ml", "20",  "$16.00", "NL-HCG-001"),
        ("Insulin-like Growth Factor", "Lyophilized", "1mg",         "2ml",  "20",  "$35.00", "NL-IGF-001"),
        ("Fragment 176-191",           "Lyophilized", "5mg",         "2ml",  "25",  "$12.00", "NL-FRAG-001"),
        ("AOD-9604",                   "Lyophilized", "5mg",         "2ml",  "25",  "$14.00", "NL-AOD-001"),
    ]
    popular_products = {"Tirzepatide", "BPC-157", "NAD+ (Buffered)"}

    row_y = hy - 7*mm
    for j, row in enumerate(metabolic):
        # Alternating rows with subtle gradient at left edge
        bg = LIGHT_GREY if j % 2 == 0 else WHITE
        c.setFillColor(bg)
        c.rect(hx, row_y, W - 30*mm, 7*mm, fill=1, stroke=0)
        # Subtle darker left edge
        c.setFillColor(TEAL)
        c.setFillAlpha(0.04)
        c.rect(hx, row_y, 15*mm, 7*mm, fill=1, stroke=0)
        c.setFillAlpha(1)
        # Product line pill badge
        c.setFillColor(TEAL)
        c.setFillAlpha(0.12)
        c.roundRect(hx + 1*mm, row_y + 1.5*mm, 3*mm, 4*mm, 0.8*mm, fill=1, stroke=0)
        c.setFillAlpha(1)
        # Popular badge
        if row[0] in popular_products:
            badge_x = hx + W - 30*mm - 14*mm
            c.setFillColor(HIGHLIGHT)
            c.roundRect(badge_x, row_y + 1.5*mm, 12*mm, 4*mm, 1*mm, fill=1, stroke=0)
            c.setFillColor(BLACK)
            set_font(c, bold=True, size=4.5)
            c.drawCentredString(badge_x + 6*mm, row_y + 2.5*mm, "POPULAR")
        rx = hx + 5*mm
        for k, (cell, (_, cw)) in enumerate(zip(row, cols)):
            c.setFillColor(TEAL if k == 6 else (BLACK if k == 0 else MID_GREY))
            set_font(c, bold=(k == 0), size=8 if k == 0 else 7.5)
            c.drawString(rx, row_y + 2.5*mm, cell)
            rx += cw
        row_y -= 7*mm

    # Recovery Line
    c.setFillColor(GREEN)
    c.setFillAlpha(0.12)
    c.rect(15*mm, row_y - 4*mm, W - 30*mm, 10*mm, fill=1, stroke=0)
    c.setFillAlpha(1)
    c.setFillColor(GREEN)
    c.rect(15*mm, row_y - 4*mm, 3*mm, 10*mm, fill=1, stroke=0)
    set_font(c, bold=True, size=14)
    c.drawString(22*mm, row_y - 2*mm, "Recovery Line")

    hy2 = row_y - 16*mm
    c.setFillColor(BLACK)
    c.rect(hx, hy2, W - 30*mm, 8*mm, fill=1, stroke=0)
    cx = hx + 2*mm
    for col_name, col_w in cols:
        set_font(c, bold=True, size=7.5)
        c.setFillColor(GREEN)
        c.drawString(cx, hy2 + 2.5*mm, col_name)
        cx += col_w

    recovery = [
        ("BPC-157",                  "Lyophilized", "5mg / 10mg",    "3ml",  "25",  "$14.00", "NL-BPC-001"),
        ("BPC-157 + TB-500 Combo",   "Lyophilized", "5mg + 5mg",     "5ml",  "20",  "$24.00", "NL-COMBO-001"),
        ("TB-500 (Thymosin Beta-4)",  "Lyophilized", "2mg / 5mg",     "3ml",  "25",  "$16.00", "NL-TB-001"),
        ("GHK-CU (Copper Peptide)",  "Lyophilized", "50mg",          "5ml",  "20",  "$18.00", "NL-GHK-001"),
        ("LL-37",                    "Lyophilized", "5mg",           "2ml",  "20",  "$22.00", "NL-LL37-001"),
        ("Thymosin Alpha-1",         "Lyophilized", "5mg",           "3ml",  "20",  "$28.00", "NL-TA1-001"),
        ("Dihexa",                   "Lyophilized", "10mg",          "2ml",  "20",  "$32.00", "NL-DIH-001"),
        ("KPV",                      "Lyophilized", "5mg",           "2ml",  "25",  "$12.00", "NL-KPV-001"),
        ("KLOW80 (BPC+GHK+TB+KPV)", "Lyophilized", "Quad-blend",    "10ml", "15",  "$48.00", "NL-KL-001"),
        ("Methylene Blue",           "Liquid",      "50mg/ml",       "10ml", "20",  "$14.00", "NL-MB-001"),
    ]

    row_y2 = hy2 - 7*mm
    for j, row in enumerate(recovery):
        bg = colors.HexColor('#f0fff8') if j % 2 == 0 else WHITE
        c.setFillColor(bg)
        c.rect(hx, row_y2, W - 30*mm, 7*mm, fill=1, stroke=0)
        c.setFillColor(GREEN)
        c.setFillAlpha(0.04)
        c.rect(hx, row_y2, 15*mm, 7*mm, fill=1, stroke=0)
        c.setFillAlpha(1)
        c.setFillColor(GREEN)
        c.setFillAlpha(0.12)
        c.roundRect(hx + 1*mm, row_y2 + 1.5*mm, 3*mm, 4*mm, 0.8*mm, fill=1, stroke=0)
        c.setFillAlpha(1)
        if row[0] == "BPC-157":
            badge_x = hx + W - 30*mm - 14*mm
            c.setFillColor(HIGHLIGHT)
            c.roundRect(badge_x, row_y2 + 1.5*mm, 12*mm, 4*mm, 1*mm, fill=1, stroke=0)
            c.setFillColor(BLACK)
            set_font(c, bold=True, size=4.5)
            c.drawCentredString(badge_x + 6*mm, row_y2 + 2.5*mm, "POPULAR")
        rx = hx + 5*mm
        for k, (cell, (_, cw)) in enumerate(zip(row, cols)):
            c.setFillColor(GREEN if k == 6 else (BLACK if k == 0 else MID_GREY))
            set_font(c, bold=(k == 0), size=8 if k == 0 else 7.5)
            c.drawString(rx, row_y2 + 2.5*mm, cell)
            rx += cw
        row_y2 -= 7*mm

    page_footer(c, 8)
    c.showPage()


def page_catalogue_2(c):
    header_bar(c, H - 28*mm, h=28*mm, color=BLACK)
    set_font(c, bold=True, size=22)
    c.setFillColor(WHITE)
    c.drawString(15*mm, H - 18*mm, "FULL PRODUCT CATALOGUE  — PART 2")
    c.setFillColor(BLUE)
    c.rect(15*mm, H - 28*mm, 68*mm, 1*mm, fill=1, stroke=0)

    # Longevity Line band
    c.setFillColor(BLUE)
    c.setFillAlpha(0.12)
    c.rect(15*mm, H - 42*mm, W - 30*mm, 10*mm, fill=1, stroke=0)
    c.setFillAlpha(1)
    c.setFillColor(BLUE)
    c.rect(15*mm, H - 42*mm, 3*mm, 10*mm, fill=1, stroke=0)
    set_font(c, bold=True, size=14)
    c.drawString(22*mm, H - 40*mm, "Longevity Line")

    cols = [("PRODUCT", 52*mm), ("FORM", 20*mm), ("STRENGTH", 22*mm), ("VIAL", 18*mm),
            ("MOQ", 13*mm), ("UNIT PRICE", 22*mm), ("BATCH CODE", 28*mm)]
    hx = 15*mm
    hy = H - 55*mm
    c.setFillColor(BLACK)
    c.rect(hx, hy, W - 30*mm, 8*mm, fill=1, stroke=0)
    cx = hx + 2*mm
    for col_name, col_w in cols:
        set_font(c, bold=True, size=7.5)
        c.setFillColor(BLUE)
        c.drawString(cx, hy + 2.5*mm, col_name)
        cx += col_w

    longevity = [
        ("NAD+ (Buffered)",          "Lyophilized", "500mg/1000mg",  "10ml", "20",  "$30.00", "NL-NAD-001"),
        ("Epithalon",                "Lyophilized", "10mg",          "3ml",  "20",  "$18.00", "NL-EPI-001"),
        ("MOTS-c",                   "Lyophilized", "5mg / 10mg",    "3ml",  "20",  "$38.00", "NL-MOTS-001"),
        ("Humanin",                  "Lyophilized", "1mg",           "2ml",  "20",  "$42.00", "NL-HMN-001"),
        ("SS-31 (Elamipretide)",     "Lyophilized", "5mg",           "2ml",  "20",  "$45.00", "NL-SS31-001"),
        ("Pinealon",                 "Lyophilized", "3mg",           "2ml",  "25",  "$20.00", "NL-PIN-001"),
        ("Selank",                   "Lyophilized", "5mg",           "2ml",  "25",  "$15.00", "NL-SEL-001"),
        ("Semax",                    "Lyophilized", "15mg / 30mg",   "3ml",  "25",  "$22.00", "NL-SEX-001"),
        ("Cerebrolysin",             "Lyophilized", "10mg",          "5ml",  "20",  "$35.00", "NL-CER-001"),
        ("P21",                      "Lyophilized", "5mg",           "2ml",  "20",  "$28.00", "NL-P21-001"),
    ]
    row_y = hy - 7*mm
    for j, row in enumerate(longevity):
        bg = colors.HexColor('#f0f5ff') if j % 2 == 0 else WHITE
        c.setFillColor(bg)
        c.rect(hx, row_y, W - 30*mm, 7*mm, fill=1, stroke=0)
        c.setFillColor(BLUE)
        c.setFillAlpha(0.04)
        c.rect(hx, row_y, 15*mm, 7*mm, fill=1, stroke=0)
        c.setFillAlpha(1)
        c.setFillColor(BLUE)
        c.setFillAlpha(0.12)
        c.roundRect(hx + 1*mm, row_y + 1.5*mm, 3*mm, 4*mm, 0.8*mm, fill=1, stroke=0)
        c.setFillAlpha(1)
        if row[0] == "NAD+ (Buffered)":
            badge_x = hx + W - 30*mm - 14*mm
            c.setFillColor(HIGHLIGHT)
            c.roundRect(badge_x, row_y + 1.5*mm, 12*mm, 4*mm, 1*mm, fill=1, stroke=0)
            c.setFillColor(BLACK)
            set_font(c, bold=True, size=4.5)
            c.drawCentredString(badge_x + 6*mm, row_y + 2.5*mm, "POPULAR")
        rx = hx + 2*mm
        for k, (cell, (_, cw)) in enumerate(zip(row, cols)):
            c.setFillColor(BLUE if k == 6 else (BLACK if k == 0 else MID_GREY))
            set_font(c, bold=(k == 0), size=8 if k == 0 else 7.5)
            c.drawString(rx, row_y + 2.5*mm, cell)
            rx += cw
        row_y -= 7*mm

    # Ancillary
    c.setFillColor(MID_GREY)
    c.setFillAlpha(0.12)
    c.rect(15*mm, row_y - 4*mm, W - 30*mm, 10*mm, fill=1, stroke=0)
    c.setFillAlpha(1)
    c.setFillColor(MID_GREY)
    c.rect(15*mm, row_y - 4*mm, 3*mm, 10*mm, fill=1, stroke=0)
    set_font(c, bold=True, size=14)
    c.setFillColor(BLACK)
    c.drawString(22*mm, row_y - 2*mm, "Ancillary & Reconstitution")

    hy3 = row_y - 16*mm
    c.setFillColor(BLACK)
    c.rect(hx, hy3, W - 30*mm, 8*mm, fill=1, stroke=0)
    cx = hx + 2*mm
    for col_name, col_w in cols:
        set_font(c, bold=True, size=7.5)
        c.setFillColor(SUB_TEXT)
        c.drawString(cx, hy3 + 2.5*mm, col_name)
        cx += col_w

    ancillary = [
        ("Bacteriostatic Water",  "Sterile Liquid", "30ml",       "30ml", "50", "$4.50",  "NL-BAC-001"),
        ("Sterile Water for Inj.","Sterile Liquid", "10ml",       "10ml", "50", "$2.50",  "NL-SWI-001"),
        ("Insulin Syringes U-100","Syringe",        "0.5ml/1ml",  "N/A",  "100","$0.80",  "NL-SYR-001"),
        ("Alcohol Prep Pads",     "Consumable",     "70% IPA",    "N/A",  "200","$0.05",  "NL-APP-001"),
    ]
    row_y3 = hy3 - 7*mm
    for j, row in enumerate(ancillary):
        bg = LIGHT_GREY if j % 2 == 0 else WHITE
        c.setFillColor(bg)
        c.rect(hx, row_y3, W - 30*mm, 7*mm, fill=1, stroke=0)
        rx = hx + 2*mm
        for k, (cell, (_, cw)) in enumerate(zip(row, cols)):
            c.setFillColor(BLACK if k == 0 else MID_GREY)
            set_font(c, bold=(k == 0), size=8 if k == 0 else 7.5)
            c.drawString(rx, row_y3 + 2.5*mm, cell)
            rx += cw
        row_y3 -= 7*mm

    # Custom synthesis note
    c.setFillColor(DARK_BG)
    c.roundRect(hx, 28*mm, W - 30*mm, 18*mm, 2*mm, fill=1, stroke=0)
    c.setFillColor(HIGHLIGHT)
    set_font(c, bold=True, size=9)
    c.drawString(20*mm, 40*mm, "CUSTOM SYNTHESIS:")
    c.setFillColor(SUB_TEXT)
    set_font(c, size=8.5)
    c.drawString(20*mm, 33*mm,
        "Don't see what you need? We offer fully custom peptide synthesis from sequence to finished vial. Enquire for bespoke pricing.")

    page_footer(c, 9)
    c.showPage()


def page_private_label(c):
    header_bar(c, H - 28*mm, h=28*mm, color=BLACK)
    set_font(c, bold=True, size=22)
    c.setFillColor(WHITE)
    c.drawString(15*mm, H - 18*mm, "PRIVATE LABEL & OEM SERVICES")
    c.setFillColor(TEAL)
    c.rect(15*mm, H - 28*mm, 65*mm, 1*mm, fill=1, stroke=0)

    section_title(c, "What We Provide", H - 42*mm)

    # 2x3 grid of cards with drawn icons
    services = [
        ("flask", TEAL, "Formulation & Manufacturing",
         "All peptides synthesised in our FDA-registered, GMP-compliant facility using pharmaceutical-grade raw materials. HPLC purity >=98% across all product lines."),
        ("tag", GREEN, "Custom Label & Artwork",
         "Your brand, your design. We print full-colour BOPP waterproof labels sized to any vial. Free design proof within 48 hours. Cryogenic-rated adhesive as standard."),
        ("box", BLUE, "Branded Packaging",
         "Individual product boxes, shipper cartons, branded bubble mailers, heat-seal pouches. Custom inserts with dosage guides and QR codes linking to your COAs."),
        ("rocket", TEAL, "Turnkey Launch Kit",
         "We handle manufacturing, labelling, QC, inventory storage and order fulfilment. You focus on marketing and customer acquisition. We handle everything else."),
        ("eye", GREEN, "White-Label Flexibility",
         "All products ship as 'NovaLabs' — no mention of our company on any packaging. Your customers will only ever see your brand."),
        ("clipboard", BLUE, "Regulatory Support",
         "We provide full COA documentation, SDS sheets, and HPLC reports for every batch. Suitable for research-use branding in your target markets."),
    ]

    col_w = (W - 35*mm) / 2
    row_h = 44*mm
    sy = H - 56*mm
    for i, (icon_type, clr, title, desc) in enumerate(services):
        col = i % 2
        row = i // 2
        bx = 15*mm + col * (col_w + 5*mm)
        by = sy - row * (row_h + 4*mm)

        # Card bg with teal-to-dark gradient
        c.setFillColor(CARD_BG)
        c.roundRect(bx, by - row_h, col_w, row_h, 2*mm, fill=1, stroke=0)
        c.setFillColor(clr)
        c.setFillAlpha(0.05)
        c.roundRect(bx, by - row_h, col_w, row_h, 2*mm, fill=1, stroke=0)
        c.setFillAlpha(1)
        c.setFillColor(clr)
        c.rect(bx, by - 1.5*mm, col_w, 1.5*mm, fill=1, stroke=0)

        # Drawn icon
        draw_icon(c, bx + 3*mm, by - 15*mm, icon_type, clr, size=10*mm)
        # Title
        c.setFillColor(WHITE)
        set_font(c, bold=True, size=10)
        c.drawString(bx + 16*mm, by - 8*mm, title)
        # Description
        wrap_text(c, desc, bx + 5*mm, by - 20*mm, col_w - 10*mm, size=7.5, color=SUB_TEXT)

    page_footer(c, 10)
    c.showPage()


def page_moq_pricing(c):
    header_bar(c, H - 28*mm, h=28*mm, color=BLACK)
    set_font(c, bold=True, size=22)
    c.setFillColor(WHITE)
    c.drawString(15*mm, H - 18*mm, "MOQ & PRICING TIERS")
    c.setFillColor(TEAL)
    c.rect(15*mm, H - 28*mm, 42*mm, 1*mm, fill=1, stroke=0)

    section_title(c, "Minimum Order Quantities", H - 42*mm)

    set_font(c, size=9)
    c.setFillColor(MID_GREY)
    c.drawString(15*mm, H - 54*mm,
        "MOQs apply per SKU per order. No overall order minimum — mix products freely across our full catalogue.")

    # Tier table with Recommended chip
    tiers = [
        ("STARTER", "25 units / SKU", "$10 - $48 / unit", "Standard",  "5-7 days",  "Included"),
        ("GROWTH",  "50 units / SKU", "10% off list",     "Priority",  "3-5 days",  "Included"),
        ("SCALE",   "100 units / SKU","20% off list",     "Expedited", "2-4 days",  "Included"),
        ("PARTNER", "250+ units / SKU","Custom negotiated","Dedicated","1-2 days",  "Dedicated mgr"),
    ]
    tier_cols = ["TIER", "MIN ORDER", "UNIT PRICING", "SUPPORT", "PROD. TIME", "QA DOCS"]
    tier_colors = [TEAL, GREEN, BLUE, HIGHLIGHT]
    hx = 15*mm
    hy = H - 65*mm
    col_widths = [28*mm, 38*mm, 38*mm, 28*mm, 28*mm, 35*mm]

    c.setFillColor(BLACK)
    c.rect(hx, hy, W - 30*mm, 9*mm, fill=1, stroke=0)
    cx = hx + 2*mm
    for i, (col, cw) in enumerate(zip(tier_cols, col_widths)):
        c.setFillColor(TEAL)
        set_font(c, bold=True, size=8)
        c.drawString(cx, hy + 3*mm, col)
        cx += cw

    row_y = hy - 10*mm
    for j, (tier_data, tc) in enumerate(zip(tiers, tier_colors)):
        c.setFillColor(LIGHT_GREY if j % 2 == 0 else WHITE)
        c.rect(hx, row_y, W - 30*mm, 10*mm, fill=1, stroke=0)
        c.setFillColor(tc)
        c.rect(hx, row_y, 3*mm, 10*mm, fill=1, stroke=0)
        # Recommended chip on GROWTH row
        if tier_data[0] == "GROWTH":
            c.setFillColor(GREEN)
            c.roundRect(hx + W - 30*mm - 26*mm, row_y + 2*mm, 24*mm, 6*mm, 1.5*mm, fill=1, stroke=0)
            c.setFillColor(BLACK)
            set_font(c, bold=True, size=5.5)
            c.drawCentredString(hx + W - 30*mm - 14*mm, row_y + 4*mm, "RECOMMENDED")
        rx = hx + 5*mm
        for k, (cell, cw) in enumerate(zip(tier_data, col_widths)):
            c.setFillColor(tc if k == 0 else (BLACK if k == 1 else MID_GREY))
            set_font(c, bold=(k <= 1), size=8.5 if k == 0 else 8)
            c.drawString(rx, row_y + 3.5*mm, cell)
            rx += cw
        row_y -= 10*mm

    # Volume discount table with coloured percentage badges
    section_title(c, "Volume Discount Schedule", row_y - 10*mm)
    vd_y = row_y - 24*mm
    discounts = [
        ("25 - 49 units",   "List price",   "Standard shipping"),
        ("50 - 99 units",   "10% discount", "Free standard shipping"),
        ("100 - 249 units", "20% discount", "Free priority shipping"),
        ("250 - 499 units", "28% discount", "Free expedited + dedicated mgr"),
        ("500+ units",      "35% + custom", "All fees waived, co-marketing fund"),
    ]
    c.setFillColor(BLACK)
    c.rect(hx, vd_y, W - 30*mm, 8*mm, fill=1, stroke=0)
    vd_cols = [("ORDER QUANTITY", 55*mm), ("DISCOUNT", 45*mm), ("ADDITIONAL BENEFIT", W - 30*mm - 100*mm)]
    cx = hx + 2*mm
    for col_name, cw in vd_cols:
        c.setFillColor(TEAL)
        set_font(c, bold=True, size=8)
        c.drawString(cx, vd_y + 2.5*mm, col_name)
        cx += cw
    ry = vd_y - 8*mm
    disc_colors = [MID_GREY, BLUE, GREEN, TEAL, HIGHLIGHT]
    for j, (qty, disc, benefit) in enumerate(discounts):
        c.setFillColor(LIGHT_GREY if j % 2 == 0 else WHITE)
        c.rect(hx, ry, W - 30*mm, 8*mm, fill=1, stroke=0)
        cx = hx + 2*mm
        # Quantity
        c.setFillColor(BLACK)
        set_font(c, size=8)
        c.drawString(cx, ry + 2.5*mm, qty)
        cx += vd_cols[0][1]
        # Discount badge
        dc = disc_colors[j]
        bw = c.stringWidth(disc, "Helvetica-Bold", 8) + 6*mm
        c.setFillColor(dc)
        c.setFillAlpha(0.15)
        c.roundRect(cx, ry + 1*mm, bw, 6*mm, 1.5*mm, fill=1, stroke=0)
        c.setFillAlpha(1)
        c.setFillColor(dc)
        set_font(c, bold=True, size=8)
        c.drawString(cx + 3*mm, ry + 2.5*mm, disc)
        cx += vd_cols[1][1]
        # Benefit
        c.setFillColor(MID_GREY)
        set_font(c, size=8)
        c.drawString(cx, ry + 2.5*mm, benefit)
        ry -= 8*mm

    # Payment terms — styled card with USDC coin icon
    section_title(c, "Payment Terms", ry - 10*mm)
    pt_y = ry - 18*mm
    c.setFillColor(CARD_BG)
    c.roundRect(15*mm, pt_y - 20*mm, W - 30*mm, 24*mm, 2*mm, fill=1, stroke=0)
    c.setFillColor(TEAL)
    c.rect(15*mm, pt_y - 20*mm, 3*mm, 24*mm, fill=1, stroke=0)
    draw_icon(c, 20*mm, pt_y - 15*mm, "coin", TEAL, size=10*mm)

    payment_items = [
        ("Payment",            "Full payment in USDC/USDT before production"),
        ("Accepted Methods",   "USDC / USDT (preferred)  ·  Other stablecoins on request"),
        ("Currency",           "USD equivalent  |  USDC wallet provided on order confirmation"),
    ]
    pty = pt_y - 2*mm
    for lbl, val in payment_items:
        c.setFillColor(TEAL)
        set_font(c, bold=True, size=9)
        c.drawString(34*mm, pty, f"{lbl}:")
        c.setFillColor(WHITE)
        set_font(c, size=8.5)
        c.drawString(70*mm, pty, val)
        pty -= 6.5*mm

    page_footer(c, 11)
    c.showPage()


def page_packaging(c):
    header_bar(c, H - 28*mm, h=28*mm, color=BLACK)
    set_font(c, bold=True, size=22)
    c.setFillColor(WHITE)
    c.drawString(15*mm, H - 18*mm, "CUSTOM PACKAGING OPTIONS")
    c.setFillColor(TEAL)
    c.rect(15*mm, H - 28*mm, 55*mm, 1*mm, fill=1, stroke=0)

    section_title(c, "Available Packaging Formats", H - 42*mm)

    # Drawn illustration icon types for each card
    pkg_items = [
        (TEAL,  "tag", "Individual Vial Labels",
                "50mm x 25mm BOPP matte, cryogenic-rated, waterproof.",
                "Min 250 labels  ·  $0.60/label  ·  Design included"),
        (GREEN, "box", "Individual Product Boxes",
                "Folding carton, full-colour CMYK print. Fits 3ml/10ml vials.",
                "Min 100 units  ·  $2.80-$4.50/box"),
        (BLUE,  "box", "Branded Mailer Boxes",
                "Rigid outer shipping box with NovaLabs branding & tissue paper.",
                "Min 50 units  ·  $6.50/box"),
        (TEAL,  "plane", "Branded Bubble Mailers",
                "Poly mailer with silver interior & custom exterior print.",
                "Min 100 units  ·  $1.20/mailer"),
        (GREEN, "clipboard", "Reconstitution Insert Cards",
                "Double-sided A5 card with dosage guidance, QR code to COA, brand copy.",
                "Min 200 cards  ·  $0.45/card"),
        (BLUE,  "tag", "Branded Sealing Tape",
                "Printed packaging tape 50mm x 66m roll.",
                "Min 6 rolls  ·  $8.00/roll"),
        (TEAL,  "box", "Heat-Seal Pouches",
                "Foil pouches with window, printed exterior. For multi-vial kits.",
                "Min 100 units  ·  $1.80/pouch"),
        (HIGHLIGHT, "star", "Complete Packaging Suite",
                "Labels + boxes + mailers + inserts + tape — discounted bundle.",
                "See quote page for bundle pricing"),
    ]

    py = H - 56*mm
    col_w = (W - 35*mm) / 2
    for i, (clr, icon_type, title, desc, pricing) in enumerate(pkg_items):
        col = i % 2
        row = i // 2
        bx = 15*mm + col * (col_w + 5*mm)
        card_h = 40*mm
        by = py - row * (card_h + 3*mm)
        c.setFillColor(CARD_BG)
        c.roundRect(bx, by - card_h, col_w, card_h, 2*mm, fill=1, stroke=0)
        c.setFillColor(clr)
        c.rect(bx, by - 1.5*mm, col_w, 1.5*mm, fill=1, stroke=0)
        # BUNDLE SAVE highlight
        if title == "Complete Packaging Suite":
            c.setFillColor(HIGHLIGHT)
            c.setFillAlpha(0.08)
            c.roundRect(bx, by - card_h, col_w, card_h, 2*mm, fill=1, stroke=0)
            c.setFillAlpha(1)
            c.setFillColor(HIGHLIGHT)
            c.roundRect(bx + col_w - 22*mm, by - 5*mm, 20*mm, 5*mm, 1*mm, fill=1, stroke=0)
            c.setFillColor(BLACK)
            set_font(c, bold=True, size=5.5)
            c.drawCentredString(bx + col_w - 12*mm, by - 3*mm, "BUNDLE SAVE")
        # Icon
        draw_icon(c, bx + 2*mm, by - 16*mm, icon_type, clr, size=9*mm)
        set_font(c, bold=True, size=9.5)
        c.setFillColor(WHITE)
        c.drawString(bx + 14*mm, by - 8*mm, title)
        # Desc
        wrap_text(c, desc, bx + 4*mm, by - 18*mm, col_w - 8*mm, size=7.5, color=SUB_TEXT)
        c.setFillColor(clr)
        set_font(c, size=7.5)
        c.drawString(bx + 4*mm, by - card_h + 3*mm, pricing)

    page_footer(c, 12)
    c.showPage()


def page_fulfillment(c):
    header_bar(c, H - 28*mm, h=28*mm, color=BLACK)
    set_font(c, bold=True, size=22)
    c.setFillColor(WHITE)
    c.drawString(15*mm, H - 18*mm, "DROPSHIPPING & FULFILMENT SERVICES")
    c.setFillColor(TEAL)
    c.rect(15*mm, H - 28*mm, 72*mm, 1*mm, fill=1, stroke=0)

    section_title(c, "How Our Fulfilment Works", H - 42*mm)

    # Step flow with hexagonal badges and proper arrowheads
    steps = [
        (TEAL,  "1", "CUSTOMER\nORDERS",  "Your customer places order via your website or store"),
        (GREEN, "2", "ORDER\nRECEIVED",   "We receive the order in real-time via API or manual upload"),
        (BLUE,  "3", "PICK &\nPACK",      "Your branded inventory is picked, packed & labelled"),
        (TEAL,  "4", "DISPATCH",         "Shipped same day (orders before 2pm EST)"),
        (GREEN, "5", "TRACKING",         "Auto-tracking email sent to your customer under your brand"),
        (BLUE,  "6", "DELIVERED",        "US: 2-5 days  |  LATAM: 7-14 days via freight forwarder"),
    ]
    fx = 15*mm
    fy = H - 58*mm
    step_w = (W - 30*mm - 5 * 4*mm) / 6
    for i, (clr, num, title, desc) in enumerate(steps):
        sx = fx + i * (step_w + 4*mm)
        # Hexagonal badge instead of circle
        draw_hexagon(c, sx + step_w/2, fy + 6*mm, 6*mm, fill_color=clr)
        c.setFillColor(BLACK)
        set_font(c, bold=True, size=9)
        c.drawCentredString(sx + step_w/2, fy + 4*mm, num)
        c.setFillColor(CARD_BG)
        c.roundRect(sx, fy - 30*mm, step_w, 32*mm, 2*mm, fill=1, stroke=0)
        c.setFillColor(clr)
        set_font(c, bold=True, size=7)
        # Handle multi-line titles
        title_lines = title.split('\n')
        for ti, tl in enumerate(title_lines):
            c.drawCentredString(sx + step_w/2, fy - 6*mm - ti*4*mm, tl)
        c.setFillColor(SUB_TEXT)
        set_font(c, size=6.5)
        wrap_text_centered(c, desc, sx + step_w/2, fy - 16*mm, step_w - 3*mm, size=6.5, color=SUB_TEXT)
        # Arrow with arrowhead
        if i < 5:
            c.setStrokeColor(clr)
            c.setLineWidth(1)
            ax = sx + step_w + 0.5*mm
            ay = fy + 6*mm
            c.line(ax, ay, ax + 2.5*mm, ay)
            # Arrowhead triangle
            c.setFillColor(clr)
            p = c.beginPath()
            p.moveTo(ax + 2.5*mm, ay + 1.5*mm)
            p.lineTo(ax + 4.5*mm, ay)
            p.lineTo(ax + 2.5*mm, ay - 1.5*mm)
            p.close()
            c.drawPath(p, fill=1, stroke=0)

    # Fulfilment Plans
    section_title(c, "Fulfilment Plans", H - 108*mm)
    plans = [
        ("STARTER",  "$200/mo",  "Up to 50 orders/mo",   "Standard 3-5 day",  "Standard",   "Email"),
        ("GROWTH",   "$400/mo",  "Up to 150 orders/mo",  "Priority 2-3 day",  "Climate ctrl","Email + SMS"),
        ("SCALE",    "$750/mo",  "Up to 400 orders/mo",  "Expedited 1-2 day", "Dedicated",  "Full portal"),
        ("ENTERPRISE","Custom",  "Unlimited",            "White-glove",       "Segregated",  "API + portal"),
    ]
    pcols = [("PLAN", 24*mm), ("MONTHLY FEE", 26*mm), ("ORDER VOLUME", 38*mm),
             ("SHIPPING", 36*mm), ("STORAGE", 28*mm), ("TRACKING", 33*mm)]
    hx = 15*mm
    hy = H - 122*mm
    c.setFillColor(BLACK)
    c.rect(hx, hy, W - 30*mm, 8*mm, fill=1, stroke=0)
    cx = hx + 2*mm
    for col_name, cw in pcols:
        c.setFillColor(TEAL)
        set_font(c, bold=True, size=8)
        c.drawString(cx, hy + 2.5*mm, col_name)
        cx += cw
    pclrs = [TEAL, GREEN, BLUE, HIGHLIGHT]
    ry = hy - 9*mm
    for j, (plan, pclr) in enumerate(zip(plans, pclrs)):
        c.setFillColor(LIGHT_GREY if j % 2 == 0 else WHITE)
        c.rect(hx, ry, W - 30*mm, 9*mm, fill=1, stroke=0)
        c.setFillColor(pclr)
        c.rect(hx, ry, 3*mm, 9*mm, fill=1, stroke=0)
        rx = hx + 5*mm
        for k, (cell, (_, cw)) in enumerate(zip(plan, pcols)):
            c.setFillColor(pclr if k == 0 else (BLACK if k == 1 else MID_GREY))
            set_font(c, bold=(k <= 1), size=8)
            c.drawString(rx, ry + 3*mm, cell)
            rx += cw
        ry -= 9*mm

    # LATAM note — styled info box with teal left border, globe icon
    section_title(c, "LATAM Fulfilment Strategy", ry - 8*mm)
    latam_y = ry - 16*mm
    c.setFillColor(CARD_BG)
    c.roundRect(15*mm, latam_y - 52*mm, W - 30*mm, 52*mm, 2*mm, fill=1, stroke=0)
    c.setFillColor(TEAL)
    c.rect(15*mm, latam_y - 52*mm, 3*mm, 52*mm, fill=1, stroke=0)
    draw_icon(c, 20*mm, latam_y - 16*mm, "globe", TEAL, size=10*mm)

    latam_points = [
        "US warehouse address provided — your Colombian customers see a US sender.",
        "We partner with DHL Express, FedEx International Priority and USPS for Colombia/LATAM.",
        "Customs documentation prepared by us — commercial invoices valued correctly.",
        "Optional: Ship to a Miami/New York freight forwarder of your choice.",
        "Typical delivery Colombia: 5-9 business days DHL  |  10-18 days economy.",
        "Tracking numbers issued automatically; updates delivered in Spanish if required.",
    ]
    ly = latam_y - 4*mm
    for pt in latam_points:
        c.setFillColor(TEAL)
        c.circle(35*mm, ly + 1.5*mm, 1.2*mm, fill=1, stroke=0)
        c.setFillColor(SUB_TEXT)
        set_font(c, size=8)
        c.drawString(38*mm, ly, pt[:90] + ("..." if len(pt) > 90 else ""))
        ly -= 7.5*mm

    page_footer(c, 13)
    c.showPage()


def page_qa(c):
    header_bar(c, H - 28*mm, h=28*mm, color=BLACK)
    set_font(c, bold=True, size=22)
    c.setFillColor(WHITE)
    c.drawString(15*mm, H - 18*mm, "QUALITY ASSURANCE & TESTING")
    c.setFillColor(TEAL)
    c.rect(15*mm, H - 28*mm, 58*mm, 1*mm, fill=1, stroke=0)

    section_title(c, "Our Quality Standard", H - 42*mm)

    # QA cards with drawn icons
    qa_points = [
        ("flask", TEAL,  "GMP-Compliant Facility",
                "All manufacturing in our FDA-registered, cGMP-compliant facility. Temperature-controlled synthesis, lyophilisation and filling rooms with HEPA filtration."),
        ("graph", GREEN, "HPLC Purity Testing",
                "Every batch undergoes in-house HPLC analysis. We guarantee >=98% purity across all peptide products. Full chromatograms available on request."),
        ("dna", BLUE,  "Mass Spectrometry (MS)",
                "LC-MS/MS confirms correct molecular weight and identity for every SKU. Reports included in your documentation package."),
        ("shield", TEAL,  "Janoshik Third-Party Testing",
                "We submit samples from each production run to Janoshik Analytical — the gold standard independent lab. Verify certificates at verify.janoshik.com.sigmaaudley.site"),
        ("microscope", GREEN, "Sterility & Endotoxin",
                "All injectable-grade products tested for sterility (USP <71>) and bacterial endotoxins (LAL test). Results documented in each batch COA."),
        ("clipboard", BLUE,  "Certificate of Analysis (COA)",
                "Every product shipped with a full COA: identity, purity, potency, sterility, endotoxin, moisture content and residual solvent data."),
    ]

    qy = H - 58*mm
    col_w_qa = (W - 35*mm) / 2
    for qi, (icon_type, clr, title, desc) in enumerate(qa_points):
        col = qi % 2
        row = qi // 2
        qx = 15*mm + col * (col_w_qa + 5*mm)
        qyy = qy - row * 38*mm
        c.setFillColor(CARD_BG)
        c.roundRect(qx, qyy - 32*mm, col_w_qa, 34*mm, 2*mm, fill=1, stroke=0)
        c.setFillColor(clr)
        c.rect(qx, qyy + 2*mm - 1.5*mm, col_w_qa, 1.5*mm, fill=1, stroke=0)
        # Icon
        draw_icon(c, qx + 3*mm, qyy - 14*mm, icon_type, clr, size=9*mm)
        set_font(c, bold=True, size=9.5)
        c.setFillColor(clr)
        c.drawString(qx + 15*mm, qyy - 7*mm, title)
        wrap_text(c, desc, qx + 4*mm, qyy - 17*mm, col_w_qa - 8*mm, size=7.5, color=SUB_TEXT)

    # Purity chart — horizontal bar
    cert_section_y = H - 58*mm - 3 * 38*mm - 6*mm
    section_title(c, "Purity Guarantee", cert_section_y)
    bar_y = cert_section_y - 14*mm
    c.setFillColor(colors.HexColor('#1a1a1a'))
    c.roundRect(15*mm, bar_y - 4*mm, W - 30*mm, 10*mm, 2*mm, fill=1, stroke=0)
    bar_fill = (W - 34*mm) * 0.985
    c.setFillColor(TEAL)
    c.roundRect(17*mm, bar_y - 2*mm, bar_fill, 6*mm, 1.5*mm, fill=1, stroke=0)
    c.setFillColor(BLACK)
    set_font(c, bold=True, size=8)
    c.drawString(20*mm, bar_y - 0.5*mm, "HPLC PURITY:  >=98.5%  GUARANTEED")
    c.setFillColor(WHITE)
    set_font(c, bold=True, size=8)
    c.drawRightString(W - 20*mm, bar_y - 0.5*mm, "98.5%+")

    # Certification shields
    cert_y = bar_y - 16*mm
    certs = ["FDA Registered", "cGMP Compliant", "ISO 9001:2015", "USP Standards", "Janoshik Verified"]
    cert_clrs = [TEAL, GREEN, BLUE, TEAL, GREEN]
    cx_cert = 15*mm
    for cert, clr in zip(certs, cert_clrs):
        cw_cert = c.stringWidth(cert, "Helvetica-Bold", 8) + 10*mm
        # Shield shape
        c.setFillColor(clr)
        c.setFillAlpha(0.15)
        c.roundRect(cx_cert, cert_y, cw_cert, 9*mm, 2*mm, fill=1, stroke=0)
        c.setFillAlpha(1)
        c.setStrokeColor(clr)
        c.setLineWidth(1)
        c.roundRect(cx_cert, cert_y, cw_cert, 9*mm, 2*mm, fill=0, stroke=1)
        # Shield icon small
        draw_icon(c, cx_cert + 0.5*mm, cert_y + 1*mm, "shield", clr, size=6*mm)
        c.setFillColor(clr)
        set_font(c, bold=True, size=7.5)
        c.drawString(cx_cert + 8*mm, cert_y + 3*mm, cert)
        cx_cert += cw_cert + 3*mm

    page_footer(c, 14)
    c.showPage()


def page_shipping(c):
    header_bar(c, H - 28*mm, h=28*mm, color=BLACK)
    set_font(c, bold=True, size=22)
    c.setFillColor(WHITE)
    c.drawString(15*mm, H - 18*mm, "INTERNATIONAL SHIPPING — LATAM")
    c.setFillColor(TEAL)
    c.rect(15*mm, H - 28*mm, 62*mm, 1*mm, fill=1, stroke=0)

    section_title(c, "Shipping Methods & Rates", H - 42*mm)

    shipping_data = [
        ("US Domestic",   [("USPS Priority", "1-3 days", "$8.50 flat", "Included"),
                           ("UPS Ground", "2-5 days", "$6.00 flat", "Included")]),
        ("Colombia",      [("DHL Express", "5-9 days", "$28-$45", "Included"),
                           ("FedEx Intl Priority", "6-10 days", "$32-$48", "Included"),
                           ("USPS First Class", "12-20 days", "$14-$22", "Basic")]),
        ("LATAM (other)", [("DHL Express", "7-14 days", "$30-$60", "Included"),
                           ("Economy Airmail", "15-30 days", "$12-$28", "Basic")]),
        ("UK / Europe",   [("Royal Mail / DHL", "5-10 days", "$22-$40", "Included")]),
        ("Rest of World", [("DHL Express", "7-15 days", "$35-$65", "Included")]),
    ]
    region_colors = {"US Domestic": TEAL, "Colombia": GREEN, "LATAM (other)": BLUE,
                     "UK / Europe": TEAL, "Rest of World": BLUE}

    hx = 15*mm
    hy = H - 56*mm
    scols_w = [38*mm, 28*mm, 28*mm, 30*mm]
    scol_names = ["CARRIER", "TRANSIT", "EST. COST", "TRACKING"]
    ry = hy

    for region, rows in shipping_data:
        rclr = region_colors.get(region, TEAL)
        # Region header band
        c.setFillColor(rclr)
        c.setFillAlpha(0.12)
        c.rect(hx, ry, W - 30*mm, 7*mm, fill=1, stroke=0)
        c.setFillAlpha(1)
        c.setFillColor(rclr)
        c.rect(hx, ry, 3*mm, 7*mm, fill=1, stroke=0)
        set_font(c, bold=True, size=8.5)
        c.drawString(hx + 6*mm, ry + 2*mm, region)
        # Column headers
        cx = hx + 40*mm
        c.setFillColor(rclr)
        set_font(c, bold=True, size=7)
        for cn, cw in zip(scol_names, scols_w):
            c.drawString(cx, ry + 2*mm, cn)
            cx += cw
        ry -= 7*mm
        # Data rows
        for j, (carrier, transit, cost, tracking) in enumerate(rows):
            c.setFillColor(LIGHT_GREY if j % 2 == 0 else WHITE)
            c.rect(hx, ry, W - 30*mm, 7*mm, fill=1, stroke=0)
            cx = hx + 40*mm
            for val, cw in zip([carrier, transit, cost, tracking], scols_w):
                c.setFillColor(MID_GREY)
                set_font(c, size=7.5)
                c.drawString(cx, ry + 2*mm, val)
                cx += cw
            ry -= 7*mm
        ry -= 2*mm

    # Notes styled card with plane icon
    section_title(c, "Important Notes for Colombian / LATAM Shipments", ry - 4*mm)
    notes_y = ry - 10*mm
    c.setFillColor(CARD_BG)
    c.roundRect(15*mm, notes_y - 54*mm, W - 30*mm, 54*mm, 2*mm, fill=1, stroke=0)
    c.setFillColor(TEAL)
    c.rect(15*mm, notes_y - 54*mm, 3*mm, 54*mm, fill=1, stroke=0)
    draw_icon(c, 20*mm, notes_y - 14*mm, "plane", TEAL, size=10*mm)

    notes = [
        "All parcels shipped discreetly with no product-related text on outer packaging.",
        "Customs value declared as 'Laboratory Research Reagents' — standard B2B practice.",
        "We prepare commercial invoices, packing lists and any required declarations.",
        "Import duty responsibility lies with the recipient; we can advise on rates.",
        "We recommend DHL Express for Colombia — fastest clearance times.",
        "Temperature-sensitive products shipped with dry-ice or gel packs at no extra charge.",
    ]
    ny = notes_y - 4*mm
    for note in notes:
        c.setFillColor(TEAL)
        c.circle(35*mm, ny + 1.5*mm, 1.2*mm, fill=1, stroke=0)
        c.setFillColor(SUB_TEXT)
        set_font(c, size=8)
        c.drawString(38*mm, ny, note[:88] + ("..." if len(note) > 88 else ""))
        ny -= 7.5*mm

    page_footer(c, 15)
    c.showPage()


def page_quote(c):
    # Full-width dark band header with large letter
    c.setFillColor(BLACK)
    c.rect(0, H - 32*mm, W, 32*mm, fill=1, stroke=0)
    set_font(c, bold=True, size=22)
    c.setFillColor(WHITE)
    c.drawString(15*mm, H - 18*mm, "NOVALABS LAUNCH PACKAGE — DETAILED QUOTE")
    c.setFillColor(TEAL)
    c.rect(15*mm, H - 23*mm, 80*mm, 1*mm, fill=1, stroke=0)
    set_font(c, size=9)
    c.setFillColor(SUB_TEXT)
    c.drawString(15*mm, H - 30*mm, "Quote Ref: SA-9F4K7-26  |  Valid until: 28 March 2026  |  Client: Manuel Lemus")

    # Section A header — full-width dark band with large letter
    sa_y = H - 42*mm
    c.setFillColor(BLACK)
    c.rect(15*mm, sa_y - 2*mm, W - 30*mm, 10*mm, fill=1, stroke=0)
    c.setFillColor(TEAL)
    set_font(c, bold=True, size=16)
    c.drawString(17*mm, sa_y, "A")
    set_font(c, bold=True, size=10)
    c.drawString(28*mm, sa_y + 1*mm, "Research Peptide Inventory (Custom NovaLabs Labelled)")

    inv_items = [
        ("Tirzepatide 10mg lyophilized",        "50", "$25.00",  "$1,250.00"),
        ("Retatrutide 10mg lyophilized",         "40", "$38.00",  "$1,520.00"),
        ("BPC-157 10mg lyophilized",             "60", "$15.00",  "$900.00"),
        ("BPC-157 + TB-500 Combo 5mg+5mg",       "20", "$24.00",  "$480.00"),
        ("NAD+ 1000mg lyophilized",              "30", "$35.00",  "$1,050.00"),
        ("Epithalon 10mg lyophilized",           "30", "$18.00",  "$540.00"),
        ("GHK-CU 50mg lyophilized",              "30", "$18.00",  "$540.00"),
        ("MOTS-c 10mg lyophilized",              "20", "$42.00",  "$840.00"),
        ("Semax 30mg lyophilized",               "20", "$22.00",  "$440.00"),
        ("Methylene Blue 50mg/ml",               "20", "$14.00",  "$280.00"),
        ("TB-500 5mg lyophilized",               "30", "$16.00",  "$480.00"),
        ("CJC-1295 + Ipamorelin 10mg combo",     "20", "$22.00",  "$440.00"),
        ("HCG 5000IU lyophilized",               "20", "$16.00",  "$320.00"),
        ("Bacteriostatic Water 30ml",            "50", "$4.50",   "$225.00"),
    ]
    hx = 15*mm
    hy = sa_y - 12*mm
    icols = [("PRODUCT DESCRIPTION", 90*mm), ("QTY", 14*mm), ("UNIT $", 22*mm), ("LINE TOTAL", 26*mm)]
    c.setFillColor(colors.HexColor('#1a1a1a'))
    c.rect(hx, hy, W - 30*mm, 7*mm, fill=1, stroke=0)
    cx = hx + 2*mm
    for cname, cw in icols:
        c.setFillColor(TEAL)
        set_font(c, bold=True, size=7.5)
        c.drawString(cx, hy + 2.2*mm, cname)
        cx += cw
    ry = hy - 6*mm
    for j, row in enumerate(inv_items):
        c.setFillColor(LIGHT_GREY if j % 2 == 0 else WHITE)
        c.rect(hx, ry, W - 30*mm, 6*mm, fill=1, stroke=0)
        rx = hx + 2*mm
        for k, (cell, (_, cw)) in enumerate(zip(row, icols)):
            c.setFillColor(BLACK if k == 0 else (MID_GREY if k < 3 else TEAL))
            set_font(c, bold=(k == 0), size=7.5)
            c.drawString(rx, ry + 1.8*mm, cell)
            rx += cw
        ry -= 6*mm
    # Subtotal A
    c.setFillColor(colors.HexColor('#e8f7f7'))
    c.rect(hx, ry - 1*mm, W - 30*mm, 7*mm, fill=1, stroke=0)
    c.setFillColor(TEAL)
    set_font(c, bold=True, size=9)
    c.drawRightString(W - 15*mm, ry + 1.5*mm, "SUBTOTAL A:  $9,305.00")
    ry -= 8*mm

    # Section B
    c.setFillColor(BLACK)
    c.rect(15*mm, ry - 2*mm, W - 30*mm, 9*mm, fill=1, stroke=0)
    c.setFillColor(GREEN)
    set_font(c, bold=True, size=16)
    c.drawString(17*mm, ry, "B")
    set_font(c, bold=True, size=10)
    c.drawString(28*mm, ry + 1*mm, "Custom Branding & Packaging")

    brand_items = [
        ("Brand identity setup fee (one-time)",              "1",   "$500.00", "$500.00"),
        ("Custom label design — 3 product lines",            "1",   "$300.00", "$300.00"),
        ("Label print run — 1,500 labels (3x500)",          "1500", "$0.60",   "$900.00"),
        ("Branded individual product boxes x 3 designs",    "100", "$3.80",   "$380.00"),
        ("Branded outer mailer boxes",                       "100", "$2.80",   "$280.00"),
        ("Reconstitution insert cards (bilingual EN/ES)",    "200", "$0.45",   "$90.00"),
        ("Branded sealing tape (6 rolls)",                   "6",   "$8.00",   "$48.00"),
    ]
    hy2 = ry - 12*mm
    c.setFillColor(colors.HexColor('#1a1a1a'))
    c.rect(hx, hy2, W - 30*mm, 7*mm, fill=1, stroke=0)
    cx = hx + 2*mm
    for cname, cw in icols:
        c.setFillColor(GREEN)
        set_font(c, bold=True, size=7.5)
        c.drawString(cx, hy2 + 2.2*mm, cname)
        cx += cw
    ry2 = hy2 - 6*mm
    for j, row in enumerate(brand_items):
        c.setFillColor(colors.HexColor('#f0fff8') if j % 2 == 0 else WHITE)
        c.rect(hx, ry2, W - 30*mm, 6*mm, fill=1, stroke=0)
        rx = hx + 2*mm
        for k, (cell, (_, cw)) in enumerate(zip(row, icols)):
            c.setFillColor(BLACK if k == 0 else (MID_GREY if k < 3 else GREEN))
            set_font(c, bold=(k == 0), size=7.5)
            c.drawString(rx, ry2 + 1.8*mm, cell)
            rx += cw
        ry2 -= 6*mm
    c.setFillColor(colors.HexColor('#eafaf3'))
    c.rect(hx, ry2 - 1*mm, W - 30*mm, 7*mm, fill=1, stroke=0)
    c.setFillColor(GREEN)
    set_font(c, bold=True, size=9)
    c.drawRightString(W - 15*mm, ry2 + 1.5*mm, "SUBTOTAL B:  $2,498.00")
    ry2 -= 8*mm

    # Section C
    c.setFillColor(BLACK)
    c.rect(15*mm, ry2 - 2*mm, W - 30*mm, 9*mm, fill=1, stroke=0)
    c.setFillColor(BLUE)
    set_font(c, bold=True, size=16)
    c.drawString(17*mm, ry2, "C")
    set_font(c, bold=True, size=10)
    c.drawString(28*mm, ry2 + 1*mm, "Dropshipping & Fulfilment Setup")

    ful_items = [
        ("US warehouse setup & API integration (one-time)", "1",  "$500.00", "$500.00"),
        ("6-month GROWTH fulfilment subscription",          "6",  "$400.00", "$2,400.00"),
        ("US domestic shipping credit (50 prepaid orders)", "50", "$5.00",   "$250.00"),
    ]
    hy3 = ry2 - 12*mm
    c.setFillColor(colors.HexColor('#1a1a1a'))
    c.rect(hx, hy3, W - 30*mm, 7*mm, fill=1, stroke=0)
    cx = hx + 2*mm
    for cname, cw in icols:
        c.setFillColor(BLUE)
        set_font(c, bold=True, size=7.5)
        c.drawString(cx, hy3 + 2.2*mm, cname)
        cx += cw
    ry3 = hy3 - 6*mm
    for j, row in enumerate(ful_items):
        c.setFillColor(colors.HexColor('#f0f5ff') if j % 2 == 0 else WHITE)
        c.rect(hx, ry3, W - 30*mm, 6*mm, fill=1, stroke=0)
        rx = hx + 2*mm
        for k, (cell, (_, cw)) in enumerate(zip(row, icols)):
            c.setFillColor(BLACK if k == 0 else (MID_GREY if k < 3 else BLUE))
            set_font(c, bold=(k == 0), size=7.5)
            c.drawString(rx, ry3 + 1.8*mm, cell)
            rx += cw
        ry3 -= 6*mm
    c.setFillColor(colors.HexColor('#eef2ff'))
    c.rect(hx, ry3 - 1*mm, W - 30*mm, 7*mm, fill=1, stroke=0)
    c.setFillColor(BLUE)
    set_font(c, bold=True, size=9)
    c.drawRightString(W - 15*mm, ry3 + 1.5*mm, "SUBTOTAL C:  $3,150.00")
    ry3 -= 8*mm

    # Section D
    c.setFillColor(BLACK)
    c.rect(15*mm, ry3 - 2*mm, W - 30*mm, 9*mm, fill=1, stroke=0)
    c.setFillColor(HIGHLIGHT)
    set_font(c, bold=True, size=16)
    c.drawString(17*mm, ry3, "D")
    set_font(c, bold=True, size=10)
    c.drawString(28*mm, ry3 + 1*mm, "Quality Assurance Package")

    qa_items = [
        ("COA documentation package (all 14 SKUs)",   "1", "$300.00", "$300.00"),
        ("Janoshik third-party testing (14 reports)", "14", "$55.00", "$770.00"),
        ("HPLC chromatograms (all batches)",           "1", "$0.00",  "Included"),
        ("Sterility & endotoxin testing",              "1", "$0.00",  "Included"),
    ]
    hy4 = ry3 - 12*mm
    c.setFillColor(colors.HexColor('#1a1a1a'))
    c.rect(hx, hy4, W - 30*mm, 7*mm, fill=1, stroke=0)
    cx = hx + 2*mm
    for cname, cw in icols:
        c.setFillColor(HIGHLIGHT)
        set_font(c, bold=True, size=7.5)
        c.drawString(cx, hy4 + 2.2*mm, cname)
        cx += cw
    ry4 = hy4 - 6*mm
    for j, row in enumerate(qa_items):
        c.setFillColor(colors.HexColor('#fffdf0') if j % 2 == 0 else WHITE)
        c.rect(hx, ry4, W - 30*mm, 6*mm, fill=1, stroke=0)
        rx = hx + 2*mm
        for k, (cell, (_, cw)) in enumerate(zip(row, icols)):
            c.setFillColor(BLACK if k == 0 else (MID_GREY if k < 3 else HIGHLIGHT))
            set_font(c, bold=(k == 0), size=7.5)
            c.drawString(rx, ry4 + 1.8*mm, cell)
            rx += cw
        ry4 -= 6*mm
    c.setFillColor(colors.HexColor('#fffef0'))
    c.rect(hx, ry4 - 1*mm, W - 30*mm, 7*mm, fill=1, stroke=0)
    c.setFillColor(HIGHLIGHT)
    set_font(c, bold=True, size=9)
    c.drawRightString(W - 15*mm, ry4 + 1.5*mm, "SUBTOTAL D:  $1,070.00")
    ry4 -= 12*mm

    # Grand total box — large, with teal border glow
    gt_h = 36*mm
    gt_y = ry4 - gt_h
    # Glow border effect (layered rect outlines)
    c.setStrokeColor(TEAL)
    c.setStrokeAlpha(0.1)
    c.setLineWidth(6)
    c.roundRect(hx - 2*mm, gt_y - 2*mm, W - 26*mm, gt_h + 4*mm, 4*mm, fill=0, stroke=1)
    c.setStrokeAlpha(0.2)
    c.setLineWidth(3)
    c.roundRect(hx - 1*mm, gt_y - 1*mm, W - 28*mm, gt_h + 2*mm, 3*mm, fill=0, stroke=1)
    c.setStrokeAlpha(1)
    c.setLineWidth(1.5)
    c.setStrokeColor(TEAL)
    c.setFillColor(BLACK)
    c.roundRect(hx, gt_y, W - 30*mm, gt_h, 2*mm, fill=1, stroke=1)

    c.setFillColor(TEAL)
    set_font(c, bold=True, size=10)
    c.drawString(hx + 5*mm, gt_y + gt_h - 10*mm, "SUBTOTALS:  A $9,305  +  B $2,498  +  C $3,150  +  D $1,070")
    c.setFillColor(TEAL)
    c.rect(hx + 5*mm, gt_y + gt_h - 14*mm, W - 40*mm, 0.5*mm, fill=1, stroke=0)
    # Total in very large text
    set_font(c, bold=True, size=14)
    c.setFillColor(WHITE)
    c.drawString(hx + 5*mm, gt_y + 8*mm, "TOTAL INVESTMENT:")
    # Coin icon
    draw_icon(c, W - 15*mm - 75*mm, gt_y + 3*mm, "coin", TEAL, size=10*mm)
    c.setFillColor(TEAL)
    set_font(c, bold=True, size=28)
    c.drawRightString(W - hx - 5*mm, gt_y + 6*mm, "USD $15,023.00")
    c.setFillColor(HIGHLIGHT)
    set_font(c, bold=True, size=9)
    c.drawString(hx + 5*mm, gt_y + 2*mm, "Full payment in USDC / USDT required to confirm order")

    page_footer(c, 16)
    c.showPage()


def page_terms(c):
    header_bar(c, H - 28*mm, h=28*mm, color=BLACK)
    set_font(c, bold=True, size=22)
    c.setFillColor(WHITE)
    c.drawString(15*mm, H - 18*mm, "TERMS, TIMELINE & NEXT STEPS")
    c.setFillColor(TEAL)
    c.rect(15*mm, H - 28*mm, 62*mm, 1*mm, fill=1, stroke=0)

    section_title(c, "Production & Delivery Timeline", H - 42*mm)

    timeline_items = [
        (TEAL,  "Day 1-2",   "Agreement & Payment",
                "Sign partnership agreement, submit full payment ($15,023.00) in USDC. "
                "Kick-off call with your dedicated account manager. Payment confirms production slot."),
        (GREEN, "Day 2-4",   "Brand Proof",
                "Receive full label and packaging design proofs for your approval. "
                "Up to 3 rounds of revisions included at no extra charge."),
        (BLUE,  "Day 4-14",  "Production",
                "All 14 SKUs enter manufacturing queue. HPLC testing, QC sign-off, "
                "lyophilisation and vial filling in our GMP facility."),
        (TEAL,  "Day 14-18", "Labelling & Packaging",
                "Custom NovaLabs labels applied. Products boxed, documented with COAs, "
                "and batch records completed for your brand."),
        (GREEN, "Day 18-21", "QA & Janoshik Testing",
                "Samples submitted to Janoshik for independent third-party verification. "
                "Full COA documentation prepared and quality approved."),
        (BLUE,  "Day 21-25", "Fulfilment Setup",
                "US warehouse account activated. Inventory logged and photographed. "
                "Your order portal goes live with real-time stock levels."),
        (HIGHLIGHT,  "Day 25",    "LAUNCH",
                "NovaLabs is live. First orders can be placed. You receive full inventory "
                "records, COAs, Janoshik reports and tracking credentials."),
    ]

    ty = H - 56*mm
    bar_x = 15*mm
    card_h = 26*mm
    for i, (clr, timing, title, desc) in enumerate(timeline_items):
        # dot + line
        c.setFillColor(clr)
        if title == "LAUNCH":
            # Star burst decoration
            draw_icon(c, bar_x, ty - 1*mm, "star", HIGHLIGHT, size=8*mm)
        else:
            c.circle(bar_x + 3*mm, ty + 3*mm, 3*mm, fill=1, stroke=0)
        if i < len(timeline_items) - 1:
            c.setStrokeColor(LINE_GREY)
            c.setLineWidth(1)
            c.line(bar_x + 3*mm, ty - card_h + 6*mm, bar_x + 3*mm, ty)
        # Taller card with full descriptions
        c.setFillColor(CARD_BG)
        c.roundRect(bar_x + 10*mm, ty - card_h + 4*mm, W - bar_x - 25*mm, card_h, 2*mm, fill=1, stroke=0)
        c.setFillColor(clr)
        set_font(c, bold=True, size=8.5)
        c.drawString(bar_x + 14*mm, ty - 2*mm, f"{timing}  —  {title}")
        # Full word-wrapped description
        wrap_text(c, desc, bar_x + 14*mm, ty - 10*mm, W - bar_x - 45*mm, size=7.5, color=SUB_TEXT)
        ty -= card_h + 2*mm

    # Terms — 2-column card grid
    section_title(c, "Key Terms & Conditions", ty - 3*mm)
    terms = [
        ("Quote Validity",      "This quote is valid for 30 days from 26 February 2026."),
        ("Payment",             "Full payment in USDC / USDT confirms the order."),
        ("Returns",             "Damaged goods replaced at no cost within 14 days of delivery."),
        ("Confidentiality",     "All pricing, formulations and terms are strictly confidential."),
        ("Exclusivity",         "Exclusive LATAM territory rights available on request."),
        ("Reorders",            "Standard 14-day lead time. Priority queue for Partner tier."),
        ("IP",                  "All brand assets designed by us remain your property upon full payment."),
    ]
    terms_y = ty - 15*mm
    tw = (W - 35*mm) / 2
    for idx, (lbl, val) in enumerate(terms):
        col = idx % 2
        row = idx // 2
        tx = 15*mm + col * (tw + 5*mm)
        tty = terms_y - row * 12*mm
        # Card bg
        c.setFillColor(LIGHT_GREY)
        c.roundRect(tx, tty - 4*mm, tw, 10*mm, 1.5*mm, fill=1, stroke=0)
        c.setFillColor(TEAL)
        c.rect(tx, tty - 4*mm, 2*mm, 10*mm, fill=1, stroke=0)
        set_font(c, bold=True, size=7.5)
        c.setFillColor(BLACK)
        c.drawString(tx + 4*mm, tty + 2*mm, f"{lbl}:")
        c.setFillColor(MID_GREY)
        set_font(c, size=7)
        c.drawString(tx + 4*mm, tty - 3*mm, val[:60] + ("..." if len(val) > 60 else ""))

    page_footer(c, 17)
    c.showPage()


def draw_vial(c, x, y, vial_h, vial_w, body_color, cap_color, label_color, product_name, line_name, dosage, lc):
    """Draw a stylised research vial with label and glass effect."""
    # Vial body
    c.setFillColor(body_color)
    c.roundRect(x, y, vial_w, vial_h, 2*mm, fill=1, stroke=0)
    # Glass highlight strip (3D glass effect)
    c.setFillColor(WHITE)
    c.setFillAlpha(0.08)
    c.rect(x + 1.2*mm, y + 3*mm, 2*mm, vial_h - 10*mm, fill=1, stroke=0)
    c.setFillAlpha(1)
    # Cap
    cap_w = vial_w * 0.7
    c.setFillColor(cap_color)
    c.roundRect(x + (vial_w - cap_w)/2, y + vial_h - 0.5*mm, cap_w, 5*mm, 1*mm, fill=1, stroke=0)
    # Cap ring
    c.setFillColor(lc)
    c.rect(x + (vial_w - cap_w)/2, y + vial_h + 1.5*mm, cap_w, 1*mm, fill=1, stroke=0)
    # Label on vial
    lpad = 1.5*mm
    lw = vial_w - 2*lpad
    lh = vial_h * 0.62
    ly = y + vial_h * 0.12
    c.setFillColor(label_color)
    c.roundRect(x + lpad, ly, lw, lh, 1*mm, fill=1, stroke=0)
    # Label top colour strip
    c.setFillColor(lc)
    c.rect(x + lpad, ly + lh - 1.2*mm, lw, 1.2*mm, fill=1, stroke=0)
    # NOVALABS
    c.setFillColor(WHITE)
    set_font(c, bold=True, size=4.5)
    c.drawCentredString(x + vial_w/2, ly + lh - 5.5*mm, "NOVALABS")
    c.setFillColor(lc)
    set_font(c, size=3.5)
    c.drawCentredString(x + vial_w/2, ly + lh - 9*mm, line_name)
    c.setFillColor(WHITE)
    set_font(c, bold=True, size=5.5)
    c.drawCentredString(x + vial_w/2, ly + lh - 14*mm, product_name)
    c.setFillColor(colors.HexColor('#aaaaaa'))
    set_font(c, size=3.5)
    c.drawCentredString(x + vial_w/2, ly + lh - 18*mm, dosage)
    c.setStrokeColor(lc)
    c.setLineWidth(0.4)
    c.line(x + lpad + 1*mm, ly + lh - 20*mm, x + lpad + lw - 1*mm, ly + lh - 20*mm)
    # SCAN FOR COA mini button
    c.setFillColor(lc)
    c.setFillAlpha(0.2)
    c.roundRect(x + lpad + 0.5*mm, ly + 1.5*mm, lw - 1*mm, 5*mm, 0.8*mm, fill=1, stroke=0)
    c.setFillAlpha(1)
    c.setFillColor(lc)
    set_font(c, bold=True, size=3)
    c.drawCentredString(x + vial_w/2, ly + 3*mm, "SCAN FOR COA")


def page_closing(c):
    # Full dark bg
    c.setFillColor(BLACK)
    c.rect(0, 0, W, H, fill=1, stroke=0)

    # Diagonal accents
    c.saveState()
    c.setFillColor(TEAL)
    c.setFillAlpha(0.06)
    p = c.beginPath()
    p.moveTo(0, H)
    p.lineTo(W * 0.35, H)
    p.lineTo(0, H * 0.6)
    p.close()
    c.drawPath(p, fill=1, stroke=0)
    c.restoreState()
    c.saveState()
    c.setFillColor(BLUE)
    c.setFillAlpha(0.04)
    p2 = c.beginPath()
    p2.moveTo(W, 0)
    p2.lineTo(W, H * 0.4)
    p2.lineTo(W * 0.6, 0)
    p2.close()
    c.drawPath(p2, fill=1, stroke=0)
    c.restoreState()

    c.setFillColor(TEAL)
    c.rect(0, H - 4*mm, W, 4*mm, fill=1, stroke=0)

    # Sigma Audley supplier mark
    set_font(c, size=10)
    c.setFillColor(DIM_TEXT)
    c.drawCentredString(W/2, H - 50*mm, "A Sigma Audley Private Label")

    # Big NOVALABS
    set_font(c, bold=True, size=48)
    c.setFillColor(WHITE)
    c.drawCentredString(W/2, H - 70*mm, "NOVALABS")
    c.setFillColor(TEAL)
    c.rect(W/2 - 45*mm, H - 78*mm, 90*mm, 1*mm, fill=1, stroke=0)
    set_font(c, size=11)
    c.setFillColor(TEAL)
    c.drawCentredString(W/2, H - 87*mm, "RESEARCH PEPTIDE DIVISION")

    # Sigma Audley seal — professional double-ring with inner content
    seal_cx = W/2
    seal_cy = H - 112*mm
    seal_r = 15*mm
    c.setStrokeColor(TEAL)
    c.setLineWidth(1.2)
    c.circle(seal_cx, seal_cy, seal_r, fill=0, stroke=1)
    c.setStrokeColor(TEAL)
    c.setLineWidth(0.6)
    c.circle(seal_cx, seal_cy, seal_r - 2.5*mm, fill=0, stroke=1)
    # Inner content
    c.setFillColor(WHITE)
    set_font(c, bold=True, size=6.5)
    c.drawCentredString(seal_cx, seal_cy + 2*mm, "SIGMA AUDLEY")
    c.setFillColor(TEAL)
    set_font(c, size=5)
    c.drawCentredString(seal_cx, seal_cy - 3*mm, "VERIFIED PARTNER")
    c.setFillColor(DIM_TEXT)
    set_font(c, size=4.5)
    c.drawCentredString(seal_cx, seal_cy - 7.5*mm, "EST. 2018")

    # Ready to launch
    set_font(c, bold=True, size=22)
    c.setFillColor(WHITE)
    c.drawCentredString(W/2, H/2 + 14*mm, "Ready to launch NovaLabs?")
    set_font(c, size=11)
    c.setFillColor(SUB_TEXT)
    c.drawCentredString(W/2, H/2 + 2*mm, "Three simple steps to get started:")

    # Three hexagonal numbered cards
    steps = [
        ("01", TEAL,  "Reply to confirm interest"),
        ("02", GREEN, "Sign the partnership agreement"),
        ("03", BLUE,  "Submit full payment in USDC to activate"),
    ]
    step_w = (W - 40*mm) / 3
    sx_start = 15*mm
    sy_step = H/2 - 12*mm
    for i, (num, clr, text) in enumerate(steps):
        sx = sx_start + i * (step_w + 5*mm)
        # Card bg
        c.setFillColor(CARD_BG)
        c.roundRect(sx, sy_step - 28*mm, step_w, 32*mm, 2*mm, fill=1, stroke=0)
        c.setFillColor(clr)
        c.rect(sx, sy_step + 4*mm - 1.5*mm, step_w, 1.5*mm, fill=1, stroke=0)
        # Hexagonal number badge
        draw_hexagon(c, sx + 12*mm, sy_step - 4*mm, 7*mm, fill_color=clr)
        c.setFillColor(BLACK)
        set_font(c, bold=True, size=11)
        c.drawCentredString(sx + 12*mm, sy_step - 7*mm, num)
        # Step text
        c.setFillColor(WHITE)
        set_font(c, size=9)
        wrap_text(c, text, sx + 4*mm, sy_step - 16*mm, step_w - 8*mm, size=9, color=WHITE)

    # Contact details
    contact_y = H/2 - 58*mm
    c.setFillColor(CARD_BG)
    c.roundRect(W/2 - 65*mm, contact_y - 30*mm, 130*mm, 42*mm, 3*mm, fill=1, stroke=0)
    c.setFillColor(TEAL)
    c.rect(W/2 - 65*mm, contact_y + 12*mm - 1.5*mm, 130*mm, 1.5*mm, fill=1, stroke=0)
    set_font(c, bold=True, size=10)
    c.setFillColor(WHITE)
    c.drawCentredString(W/2, contact_y + 5*mm, f"CONTACT — {SUPPLIER_NAME}")
    contact_items = [
        ("Supplier:", SUPPLIER_NAME),
        ("Email:", SUPPLIER_EMAIL),
        ("Ref:", "SA-9F4K7-26  |  Manuel Lemus"),
    ]
    cy_c = contact_y - 5*mm
    for lbl, val in contact_items:
        c.setFillColor(TEAL)
        set_font(c, bold=True, size=8.5)
        c.drawRightString(W/2 - 2*mm, cy_c, lbl)
        c.setFillColor(SUB_TEXT)
        set_font(c, size=8.5)
        c.drawString(W/2 + 2*mm, cy_c, val)
        cy_c -= 6.5*mm

    # Payment note — bold USDC full-payment statement
    c.setFillColor(CARD_BG)
    c.roundRect(W/2 - 70*mm, 30*mm, 140*mm, 24*mm, 2*mm, fill=1, stroke=0)
    c.setStrokeColor(TEAL)
    c.setLineWidth(1.5)
    c.roundRect(W/2 - 70*mm, 30*mm, 140*mm, 24*mm, 2*mm, fill=0, stroke=1)
    draw_icon(c, W/2 - 65*mm, 34*mm, "coin", TEAL, size=12*mm)
    c.setFillColor(TEAL)
    set_font(c, bold=True, size=12)
    c.drawCentredString(W/2 + 5*mm, 47*mm, "FULL PAYMENT IN USDC / USDT")
    c.setFillColor(HIGHLIGHT)
    set_font(c, bold=True, size=16)
    c.drawCentredString(W/2 + 5*mm, 35*mm, "$15,023.00")

    # Bottom accent
    c.setFillColor(BLUE)
    c.rect(0, 0, W, 3*mm, fill=1, stroke=0)

    set_font(c, size=7.5)
    c.setFillColor(colors.HexColor('#444444'))
    c.drawCentredString(W/2, 8*mm, f"CONFIDENTIAL  |  {SUPPLIER_NAME} x NovaLabs  |  February 2026  |  Page {TOTAL_PAGES} of {TOTAL_PAGES}")
    c.showPage()


# ══════════════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════════════

def main():
    c = pdf_canvas.Canvas(OUTPUT_PATH, pagesize=A4)
    c.setTitle("Sigma Audley x NovaLabs — Private Label Partnership Proposal")
    c.setAuthor("Sigma Audley Research")
    c.setSubject("LATAM Market Entry — Private Label Proposal & Quote for NovaLabs")

    print("p1  Cover...")
    page_cover(c)
    print("p2  TOC & executive summary...")
    page_toc_executive(c)
    print("p3  Brand identity...")
    page_brand_identity(c)
    print("p4  Brand in use / mockups...")
    page_brand_in_use(c)
    print("p5  Marketing assets...")
    page_marketing_assets(c)
    print("p6  Revenue projections...")
    page_revenue_projection(c)
    print("p7  LATAM roadmap...")
    page_latam_roadmap(c)
    print("p8  Catalogue part 1...")
    page_catalogue_1(c)
    print("p9  Catalogue part 2...")
    page_catalogue_2(c)
    print("p10 Private label services...")
    page_private_label(c)
    print("p11 MOQ & pricing...")
    page_moq_pricing(c)
    print("p12 Packaging...")
    page_packaging(c)
    print("p13 Fulfilment...")
    page_fulfillment(c)
    print("p14 QA...")
    page_qa(c)
    print("p15 Shipping...")
    page_shipping(c)
    print("p16 Quote...")
    page_quote(c)
    print("p17 Terms...")
    page_terms(c)
    print("p18 Closing...")
    page_closing(c)

    c.save()
    print("PDF saved to: " + OUTPUT_PATH)

if __name__ == "__main__":
    main()
