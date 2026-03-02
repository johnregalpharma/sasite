#!/usr/bin/env python3
"""Generate NovaLabs — Phase 1 Test Order Branding & Label Quote (1-page PDF)"""

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas as pdf_canvas

OUTPUT_PATH = r"C:\Users\kazam\Downloads\sasite\Nova labs\NovaLabs_TestOrder_Quote.pdf"

W, H = A4

# ── Brand constants ─────────────────────────────────────────────────────────
SUPPLIER   = "SIGMA AUDLEY"
SUP_WEB    = "sigmaaudley.site"
SUP_EMAIL  = "partnerships@sigmaaudley.site"
CLIENT     = "Manuel Lemus"
CLIENT_CO  = "NovaLabs"
QUOTE_REF  = "SA-T1-8R3W2"
ORDER_REF  = "SA7627IV"
QUOTE_DATE = "26 February 2026"
VALID_UNTIL = "28 March 2026"

# ── Palette ─────────────────────────────────────────────────────────────────
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

# ── Helpers ─────────────────────────────────────────────────────────────────

def sf(c, bold=False, size=10):
    c.setFont("Helvetica-Bold" if bold else "Helvetica", size)


def draw_section(c, y, letter, title, accent, col_headers, items, subtotal_label, subtotal_val):
    """Draw a section header + rows + subtotal. Returns y after."""
    hx = 12*mm
    tw = W - 24*mm

    # Section header band
    c.setFillColor(accent)
    c.setFillAlpha(0.08)
    c.rect(hx, y, tw, 5.5*mm, fill=1, stroke=0)
    c.setFillAlpha(1)
    c.setFillColor(accent)
    c.rect(hx, y, 2*mm, 5.5*mm, fill=1, stroke=0)
    sf(c, bold=True, size=8)
    c.drawString(hx + 4*mm, y + 1.5*mm, letter)
    sf(c, bold=True, size=7)
    c.setFillColor(BLACK)
    c.drawString(hx + 10*mm, y + 1.5*mm, title)
    y -= 5*mm

    # Column headers
    c.setFillColor(colors.HexColor('#f0f0f0'))
    c.rect(hx, y, tw, 4.5*mm, fill=1, stroke=0)
    c.setStrokeColor(LINE_GREY)
    c.setLineWidth(0.3)
    c.line(hx, y, hx + tw, y)
    col_x = hx + 1.5*mm
    col_widths = [100*mm, 12*mm, 22*mm, 22*mm, 15*mm]
    for i, ch in enumerate(col_headers):
        sf(c, bold=True, size=5.5)
        c.setFillColor(MID_GREY)
        if i >= 3:
            c.drawRightString(col_x + col_widths[i] - 1*mm, y + 1.3*mm, ch)
        else:
            c.drawString(col_x, y + 1.3*mm, ch)
        col_x += col_widths[i]
    y -= 4.2*mm

    # Data rows
    for j, row in enumerate(items):
        bg = LIGHT_GREY if j % 2 == 0 else WHITE
        c.setFillColor(bg)
        c.rect(hx, y, tw, 4*mm, fill=1, stroke=0)
        col_x = hx + 1.5*mm
        for k, cell in enumerate(row):
            if k == 0:
                sf(c, bold=False, size=5.8)
                c.setFillColor(BLACK)
            elif k == len(row) - 1:
                sf(c, bold=True, size=5.8)
                c.setFillColor(accent)
            else:
                sf(c, size=5.8)
                c.setFillColor(MID_GREY)
            if k >= 3:
                c.drawRightString(col_x + col_widths[k] - 1*mm, y + 1.2*mm, cell)
            else:
                c.drawString(col_x, y + 1.2*mm, cell)
            col_x += col_widths[k]
        y -= 4*mm

    # Subtotal row
    c.setFillColor(accent)
    c.setFillAlpha(0.06)
    c.rect(hx, y, tw, 4.5*mm, fill=1, stroke=0)
    c.setFillAlpha(1)
    c.setStrokeColor(accent)
    c.setLineWidth(0.3)
    c.line(hx, y + 4.5*mm, hx + tw, y + 4.5*mm)
    sf(c, bold=True, size=6.5)
    c.setFillColor(accent)
    c.drawRightString(hx + tw - 1.5*mm, y + 1.2*mm, f"{subtotal_label}  {subtotal_val}")
    y -= 5.5*mm

    return y


def main():
    c = pdf_canvas.Canvas(OUTPUT_PATH, pagesize=A4)
    c.setTitle(f"Sigma Audley x NovaLabs — Test Order Quote {QUOTE_REF}")
    c.setAuthor("Sigma Audley Research")

    hx = 12*mm
    tw = W - 24*mm

    # ════════════════════════════════════════════════════════════════════════
    # HEADER
    # ════════════════════════════════════════════════════════════════════════

    # Top accent bar
    c.setFillColor(TEAL)
    c.rect(0, H - 3*mm, W, 3*mm, fill=1, stroke=0)

    # Company name area
    c.setFillColor(BLACK)
    c.rect(0, H - 28*mm, W, 25*mm, fill=1, stroke=0)
    sf(c, bold=True, size=18)
    c.setFillColor(WHITE)
    c.drawString(hx, H - 16*mm, "SIGMA AUDLEY")
    sf(c, size=7.5)
    c.setFillColor(DIM_TEXT)
    c.drawString(hx, H - 22*mm, "Research Peptide Manufacturing & Fulfilment")
    c.drawString(hx, H - 26.5*mm, f"{SUP_WEB}  |  {SUP_EMAIL}")

    # QUOTE title — right
    sf(c, bold=True, size=10)
    c.setFillColor(HIGHLIGHT)
    c.drawRightString(W - hx, H - 10*mm, "PHASE 1")
    sf(c, bold=True, size=22)
    c.setFillColor(TEAL)
    c.drawRightString(W - hx, H - 18*mm, "QUOTE")
    sf(c, size=7)
    c.setFillColor(SUB_TEXT)
    c.drawRightString(W - hx, H - 23*mm, f"Ref: {QUOTE_REF}  |  Order: {ORDER_REF}")
    c.drawRightString(W - hx, H - 27*mm, f"Date: {QUOTE_DATE}  |  Valid until: {VALID_UNTIL}")

    # ════════════════════════════════════════════════════════════════════════
    # CLIENT / SUPPLIER INFO STRIP
    # ════════════════════════════════════════════════════════════════════════
    info_y = H - 35*mm
    half = tw / 2 - 2*mm

    # PREPARED FOR
    c.setFillColor(LIGHT_GREY)
    c.roundRect(hx, info_y - 15*mm, half, 15*mm, 1.5*mm, fill=1, stroke=0)
    c.setFillColor(TEAL)
    c.rect(hx, info_y - 15*mm, 2*mm, 15*mm, fill=1, stroke=0)
    sf(c, bold=True, size=5.5)
    c.setFillColor(MID_GREY)
    c.drawString(hx + 5*mm, info_y - 4*mm, "PREPARED FOR")
    sf(c, bold=True, size=9)
    c.setFillColor(BLACK)
    c.drawString(hx + 5*mm, info_y - 9.5*mm, CLIENT)
    sf(c, size=7)
    c.setFillColor(MID_GREY)
    c.drawString(hx + 5*mm, info_y - 13.5*mm, f"{CLIENT_CO}  |  LATAM Market Entry")

    # SUPPLIED BY
    rx = hx + half + 4*mm
    c.setFillColor(LIGHT_GREY)
    c.roundRect(rx, info_y - 15*mm, half, 15*mm, 1.5*mm, fill=1, stroke=0)
    c.setFillColor(TEAL)
    c.rect(rx, info_y - 15*mm, 2*mm, 15*mm, fill=1, stroke=0)
    sf(c, bold=True, size=5.5)
    c.setFillColor(MID_GREY)
    c.drawString(rx + 5*mm, info_y - 4*mm, "SUPPLIED BY")
    sf(c, bold=True, size=9)
    c.setFillColor(BLACK)
    c.drawString(rx + 5*mm, info_y - 9.5*mm, SUPPLIER)
    sf(c, size=7)
    c.setFillColor(MID_GREY)
    c.drawString(rx + 5*mm, info_y - 13.5*mm, f"{SUP_WEB}  |  FDA-Registered  |  cGMP")

    # ════════════════════════════════════════════════════════════════════════
    # SCOPE DESCRIPTION
    # ════════════════════════════════════════════════════════════════════════
    scope_y = info_y - 21*mm

    # Scope title
    c.setFillColor(TEAL)
    c.rect(hx, scope_y, 2*mm, 5*mm, fill=1, stroke=0)
    sf(c, bold=True, size=8.5)
    c.setFillColor(BLACK)
    c.drawString(hx + 5*mm, scope_y + 1.2*mm, "TEST ORDER BRANDING & LABELLING")
    sf(c, bold=True, size=7)
    c.setFillColor(HIGHLIGHT)
    c.drawRightString(hx + tw, scope_y + 1.2*mm, f"14 SKUs  |  36 Units  |  Order {ORDER_REF}")

    scope_y -= 6*mm
    sf(c, size=6.5)
    c.setFillColor(MID_GREY)
    c.drawString(hx, scope_y,
        "Full brand identity design, custom vial label artwork (50mm \u00d7 25mm) across 3 product lines, and label production for your test order.")

    # ════════════════════════════════════════════════════════════════════════
    # PRODUCT REFERENCE GRID — 2 columns × 7 rows
    # ════════════════════════════════════════════════════════════════════════
    grid_y = scope_y - 6*mm

    products = [
        ("BPC-157", "Recovery", "x3"),
        ("BPC-157 + TB-500", "Recovery", "x2"),
        ("CJC-1295 + Ipamorelin", "Metabolic", "x4"),
        ("Epithalon", "Longevity", "x4"),
        ("GHK-CU", "Recovery", "x4"),
        ("HCG", "Metabolic", "x1"),
        ("KLOW80 (Multi-Peptide)", "Recovery", "x1"),
        ("Methylene Blue", "Recovery", "x1"),
        ("MOTS-c", "Longevity", "x2"),
        ("NAD+ (Buffered)", "Longevity", "x2"),
        ("Retatrutide", "Metabolic", "x6"),
        ("Semax", "Longevity", "x2"),
        ("TB-500", "Recovery", "x1"),
        ("Bacteriostatic Water", "Ancillary", "x3"),
    ]

    line_colors = {
        "Metabolic": TEAL,
        "Recovery": GREEN,
        "Longevity": BLUE,
        "Ancillary": MID_GREY,
    }

    # Background card
    card_h = 28*mm
    c.setFillColor(colors.HexColor('#fafafa'))
    c.roundRect(hx, grid_y - card_h, tw, card_h, 1.5*mm, fill=1, stroke=0)
    c.setStrokeColor(LINE_GREY)
    c.setLineWidth(0.3)
    c.roundRect(hx, grid_y - card_h, tw, card_h, 1.5*mm, fill=0, stroke=1)

    # Header inside card
    sf(c, bold=True, size=5.5)
    c.setFillColor(DIM_TEXT)
    c.drawString(hx + 3*mm, grid_y - 3.5*mm, "PRODUCTS INCLUDED IN TEST ORDER")
    c.drawRightString(hx + tw - 3*mm, grid_y - 3.5*mm, f"Order Ref: {ORDER_REF}")

    # Thin line under header
    c.setStrokeColor(LINE_GREY)
    c.line(hx + 3*mm, grid_y - 5*mm, hx + tw - 3*mm, grid_y - 5*mm)

    col_w = (tw - 6*mm) / 2
    row_h = 3.2*mm
    py = grid_y - 7.5*mm

    for idx, (name, line, qty) in enumerate(products):
        col = idx // 7
        row = idx % 7
        cx = hx + 3*mm + col * (col_w + 2*mm)
        ry = py - row * row_h

        # Line colour dot
        lc = line_colors.get(line, MID_GREY)
        c.setFillColor(lc)
        c.circle(cx + 1.2*mm, ry + 0.8*mm, 0.7*mm, fill=1, stroke=0)

        # Product name
        sf(c, size=5.5)
        c.setFillColor(BLACK)
        c.drawString(cx + 3.5*mm, ry, name)

        # Qty
        sf(c, bold=True, size=5.5)
        c.setFillColor(lc)
        c.drawRightString(cx + col_w - 1*mm, ry, qty)

    # ════════════════════════════════════════════════════════════════════════
    # LINE ITEMS
    # ════════════════════════════════════════════════════════════════════════
    y = grid_y - card_h - 4*mm
    col_headers = ["DESCRIPTION", "QTY", "UNIT PRICE", "LINE TOTAL", ""]

    # ── Section A: Brand & Label Design ───────────────────────────────────
    design_items = [
        ("Brand identity system — logo refinement, colour palette, typography guidelines",
         "1", "$450.00", "$450.00", ""),
        ("Master vial label template — 50mm \u00d7 25mm format, 3 product lines",
         "1", "$275.00", "$275.00", ""),
        ("Per-SKU label artwork adaptation — individual product artwork",
         "14", "$35.00", "$490.00", ""),
    ]
    y = draw_section(c, y, "A", "BRAND & LABEL DESIGN", TEAL,
                     col_headers, design_items, "SUBTOTAL A:", "$1,215.00")

    # ── Section B: Label Production ───────────────────────────────────────
    prod_items = [
        ("Premium cryogenic vinyl labels — printed, die-cut, test order batch",
         "36", "$4.45", "$160.00", ""),
        ("QR code generation with COA verification linking — per SKU",
         "14", "$8.95", "$125.00", ""),
        ("Print-ready artwork files (AI, PDF, PNG) — all 14 SKUs",
         "1", "—", "Included", ""),
    ]
    y = draw_section(c, y, "B", "LABEL PRODUCTION — TEST ORDER", GREEN,
                     col_headers, prod_items, "SUBTOTAL B:", "$285.00")

    # ════════════════════════════════════════════════════════════════════════
    # GRAND TOTAL BOX
    # ════════════════════════════════════════════════════════════════════════
    y -= 1*mm
    gt_h = 18*mm
    gt_y = y - gt_h

    c.setStrokeColor(TEAL)
    c.setLineWidth(1.5)
    c.setFillColor(BLACK)
    c.roundRect(hx, gt_y, tw, gt_h, 2*mm, fill=1, stroke=1)

    # Breakdown
    sf(c, size=6.5)
    c.setFillColor(SUB_TEXT)
    c.drawString(hx + 4*mm, gt_y + gt_h - 6*mm, "A: $1,215.00  +  B: $285.00")

    # Divider
    c.setStrokeColor(TEAL)
    c.setStrokeAlpha(0.3)
    c.setLineWidth(0.4)
    c.line(hx + 4*mm, gt_y + gt_h - 8*mm, hx + tw - 4*mm, gt_y + gt_h - 8*mm)
    c.setStrokeAlpha(1)

    # Total
    sf(c, bold=True, size=11)
    c.setFillColor(WHITE)
    c.drawString(hx + 4*mm, gt_y + 4*mm, "TOTAL DUE:")
    sf(c, bold=True, size=22)
    c.setFillColor(TEAL)
    c.drawRightString(hx + tw - 4*mm, gt_y + 3*mm, "USD $1,500.00")

    # ════════════════════════════════════════════════════════════════════════
    # PAYMENT & TERMS STRIP
    # ════════════════════════════════════════════════════════════════════════
    y = gt_y - 3*mm
    terms_h = 24*mm
    ty = y - terms_h
    half = tw / 2 - 2*mm

    # Payment box
    c.setFillColor(LIGHT_GREY)
    c.roundRect(hx, ty, half, terms_h, 1.5*mm, fill=1, stroke=0)
    c.setFillColor(TEAL)
    c.rect(hx, ty, 2*mm, terms_h, fill=1, stroke=0)

    sf(c, bold=True, size=6.5)
    c.setFillColor(TEAL)
    c.drawString(hx + 5*mm, ty + terms_h - 4.5*mm, "PAYMENT INSTRUCTIONS")

    pay_lines = [
        ("Method:", "USDC / USDT (stablecoin)"),
        ("Amount:", "$1,500.00 USD — Full payment"),
        ("When:", "Full payment to confirm design work"),
        ("Wallet:", "Provided upon signed agreement"),
    ]
    py = ty + terms_h - 9*mm
    for lbl, val in pay_lines:
        sf(c, bold=True, size=5.5)
        c.setFillColor(BLACK)
        c.drawString(hx + 5*mm, py, lbl)
        sf(c, size=5.5)
        c.setFillColor(MID_GREY)
        c.drawString(hx + 20*mm, py, val)
        py -= 3.8*mm

    # Terms box
    tx = hx + half + 4*mm
    c.setFillColor(LIGHT_GREY)
    c.roundRect(tx, ty, half, terms_h, 1.5*mm, fill=1, stroke=0)
    c.setFillColor(TEAL)
    c.rect(tx, ty, 2*mm, terms_h, fill=1, stroke=0)

    sf(c, bold=True, size=6.5)
    c.setFillColor(TEAL)
    c.drawString(tx + 5*mm, ty + terms_h - 4.5*mm, "TERMS & CONDITIONS")

    terms = [
        "Quote valid for 30 days from date of issue.",
        "Full payment in USDC/USDT confirms the order.",
        "Design delivery: 7\u201310 business days from payment.",
        "All brand assets become client property upon payment.",
        "Up to 2 rounds of design revisions included.",
    ]
    tly = ty + terms_h - 9*mm
    for line in terms:
        c.setFillColor(TEAL)
        c.circle(tx + 6*mm, tly + 0.8*mm, 0.5*mm, fill=1, stroke=0)
        sf(c, size=5.2)
        c.setFillColor(MID_GREY)
        c.drawString(tx + 8*mm, tly, line)
        tly -= 3.2*mm

    # ════════════════════════════════════════════════════════════════════════
    # PHASE 2 NOTE
    # ════════════════════════════════════════════════════════════════════════
    y = ty - 3*mm
    note_h = 10*mm
    ny = y - note_h

    c.setFillColor(HIGHLIGHT)
    c.setFillAlpha(0.07)
    c.roundRect(hx, ny, tw, note_h, 1.5*mm, fill=1, stroke=0)
    c.setFillAlpha(1)
    c.setFillColor(HIGHLIGHT)
    c.rect(hx, ny, 2*mm, note_h, fill=1, stroke=0)

    sf(c, bold=True, size=7)
    c.setFillColor(HIGHLIGHT)
    c.drawString(hx + 5*mm, ny + note_h - 4*mm, "PHASE 2 — FULL PRODUCTION ORDER")
    sf(c, size=6)
    c.setFillColor(MID_GREY)
    c.drawString(hx + 5*mm, ny + 2.5*mm,
        "Upon approval of test order branding, proceed to full production partnership (440+ units, fulfilment & QA).")
    sf(c, bold=True, size=6)
    c.setFillColor(HIGHLIGHT)
    c.drawRightString(hx + tw - 4*mm, ny + 2.5*mm, f"See proposal {QUOTE_REF.replace('T1-8R3W2','9F4K7-26')}")

    # ════════════════════════════════════════════════════════════════════════
    # AUTHORIZATION
    # ════════════════════════════════════════════════════════════════════════
    y = ny - 3*mm
    auth_h = 14*mm
    ay = y - auth_h

    c.setFillColor(colors.HexColor('#fafafa'))
    c.roundRect(hx, ay, tw, auth_h, 1.5*mm, fill=1, stroke=0)
    c.setStrokeColor(LINE_GREY)
    c.setLineWidth(0.4)
    c.roundRect(hx, ay, tw, auth_h, 1.5*mm, fill=0, stroke=1)

    sf(c, bold=True, size=6.5)
    c.setFillColor(BLACK)
    c.drawString(hx + 4*mm, ay + auth_h - 4.5*mm, "AUTHORIZATION")
    sf(c, size=5.5)
    c.setFillColor(MID_GREY)
    c.drawString(hx + 4*mm, ay + auth_h - 9*mm,
        "By signing below, the client authorises Sigma Audley to proceed with test order branding upon receipt of full payment.")

    # Signature lines
    sig_y = ay + 1.5*mm
    c.setStrokeColor(MID_GREY)
    c.setLineWidth(0.4)
    c.line(hx + 4*mm, sig_y + 2*mm, hx + 58*mm, sig_y + 2*mm)
    sf(c, size=5)
    c.setFillColor(DIM_TEXT)
    c.drawString(hx + 4*mm, sig_y - 1*mm, f"Client Signature — {CLIENT}")

    c.line(hx + 64*mm, sig_y + 2*mm, hx + 100*mm, sig_y + 2*mm)
    c.drawString(hx + 64*mm, sig_y - 1*mm, "Date")

    c.line(hx + tw - 70*mm, sig_y + 2*mm, hx + tw - 15*mm, sig_y + 2*mm)
    c.drawString(hx + tw - 70*mm, sig_y - 1*mm, f"Authorized — {SUPPLIER}")

    # ════════════════════════════════════════════════════════════════════════
    # FOOTER
    # ════════════════════════════════════════════════════════════════════════
    c.setFillColor(BLACK)
    c.rect(0, 0, W, 7*mm, fill=1, stroke=0)
    c.setFillColor(TEAL)
    c.rect(0, 0, W, 1*mm, fill=1, stroke=0)
    sf(c, size=5.5)
    c.setFillColor(DIM_TEXT)
    c.drawString(hx, 2.5*mm, f"CONFIDENTIAL  |  {SUPPLIER}  |  {SUP_WEB}  |  {SUP_EMAIL}")
    c.drawRightString(W - hx, 2.5*mm, f"Quote {QUOTE_REF}  |  {QUOTE_DATE}")

    c.showPage()
    c.save()
    print(f"Test order quote saved to: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
