#!/usr/bin/env python3
"""Generate NovaLabs — Standalone 1-Page Professional Quote PDF"""

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas as pdf_canvas
import math

OUTPUT_PATH = r"C:\Users\kazam\Downloads\sasite\Nova labs\NovaLabs_Quote.pdf"

W, H = A4

# ── Brand constants ─────────────────────────────────────────────────────────
SUPPLIER   = "SIGMA AUDLEY"
SUP_WEB    = "sigmaaudley.site"
SUP_EMAIL  = "partnerships@sigmaaudley.site"
CLIENT     = "Manuel Lemus"
CLIENT_CO  = "NovaLabs"
QUOTE_REF  = "SA-9F4K7-26"
QUOTE_DATE = "26 February 2026"
VALID_DAYS = 30
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
HEADER_BG  = colors.HexColor('#fafafa')

# ── Helpers ─────────────────────────────────────────────────────────────────

def sf(c, bold=False, size=10):
    c.setFont("Helvetica-Bold" if bold else "Helvetica", size)


def draw_table_section(c, y, section_letter, section_title, accent_color,
                       col_headers, items, subtotal_label, subtotal_val):
    """Draw a section header + table rows + subtotal. Returns y after."""
    hx = 12*mm
    tw = W - 24*mm

    # Section header band
    c.setFillColor(accent_color)
    c.setFillAlpha(0.08)
    c.rect(hx, y, tw, 5.5*mm, fill=1, stroke=0)
    c.setFillAlpha(1)
    c.setFillColor(accent_color)
    c.rect(hx, y, 2*mm, 5.5*mm, fill=1, stroke=0)
    sf(c, bold=True, size=8)
    c.setFillColor(accent_color)
    c.drawString(hx + 4*mm, y + 1.5*mm, section_letter)
    sf(c, bold=True, size=7.5)
    c.setFillColor(BLACK)
    c.drawString(hx + 10*mm, y + 1.5*mm, section_title)
    y -= 5*mm

    # Column headers
    c.setFillColor(colors.HexColor('#f0f0f0'))
    c.rect(hx, y, tw, 4.5*mm, fill=1, stroke=0)
    c.setStrokeColor(LINE_GREY)
    c.setLineWidth(0.3)
    c.line(hx, y, hx + tw, y)
    col_x = hx + 1.5*mm
    col_widths = [92*mm, 12*mm, 20*mm, 20*mm, 27*mm]
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
                sf(c, bold=True, size=5.8)
                c.setFillColor(BLACK)
            elif k == len(row) - 1:
                sf(c, bold=True, size=5.8)
                c.setFillColor(accent_color)
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
    c.setFillColor(accent_color)
    c.setFillAlpha(0.06)
    c.rect(hx, y, tw, 4.5*mm, fill=1, stroke=0)
    c.setFillAlpha(1)
    c.setStrokeColor(accent_color)
    c.setLineWidth(0.3)
    c.line(hx, y + 4.5*mm, hx + tw, y + 4.5*mm)
    sf(c, bold=True, size=6.5)
    c.setFillColor(accent_color)
    c.drawRightString(hx + tw - 1.5*mm, y + 1.2*mm, f"{subtotal_label}  {subtotal_val}")
    y -= 5.5*mm

    return y


def main():
    c = pdf_canvas.Canvas(OUTPUT_PATH, pagesize=A4)
    c.setTitle(f"Sigma Audley x NovaLabs — Quote {QUOTE_REF}")
    c.setAuthor("Sigma Audley Research")

    # ════════════════════════════════════════════════════════════════════════
    # HEADER SECTION
    # ════════════════════════════════════════════════════════════════════════
    hx = 12*mm
    tw = W - 24*mm

    # Top accent bar
    c.setFillColor(TEAL)
    c.rect(0, H - 3*mm, W, 3*mm, fill=1, stroke=0)

    # Company name area
    c.setFillColor(BLACK)
    c.rect(0, H - 28*mm, W, 25*mm, fill=1, stroke=0)
    # SA wordmark
    sf(c, bold=True, size=18)
    c.setFillColor(WHITE)
    c.drawString(hx, H - 16*mm, "SIGMA AUDLEY")
    sf(c, size=7.5)
    c.setFillColor(DIM_TEXT)
    c.drawString(hx, H - 22*mm, "Research Peptide Manufacturing & Fulfilment")
    c.drawString(hx, H - 26.5*mm, f"{SUP_WEB}  |  {SUP_EMAIL}")

    # QUOTE title — right-aligned
    sf(c, bold=True, size=24)
    c.setFillColor(TEAL)
    c.drawRightString(W - hx, H - 14*mm, "QUOTE")
    sf(c, size=7)
    c.setFillColor(SUB_TEXT)
    c.drawRightString(W - hx, H - 20*mm, f"Ref: {QUOTE_REF}")
    c.drawRightString(W - hx, H - 25*mm, f"Date: {QUOTE_DATE}  |  Valid until: {VALID_UNTIL}")

    # ── Client / Supplier info strip ────────────────────────────────────────
    info_y = H - 38*mm
    # Two-column info box
    left_w = tw / 2 - 2*mm
    right_w = tw / 2 - 2*mm

    # BILL TO box
    c.setFillColor(LIGHT_GREY)
    c.roundRect(hx, info_y - 18*mm, left_w, 18*mm, 1.5*mm, fill=1, stroke=0)
    c.setFillColor(TEAL)
    c.rect(hx, info_y - 18*mm, 2*mm, 18*mm, fill=1, stroke=0)
    sf(c, bold=True, size=6)
    c.setFillColor(MID_GREY)
    c.drawString(hx + 5*mm, info_y - 4*mm, "PREPARED FOR")
    sf(c, bold=True, size=9)
    c.setFillColor(BLACK)
    c.drawString(hx + 5*mm, info_y - 10*mm, CLIENT)
    sf(c, size=7.5)
    c.setFillColor(MID_GREY)
    c.drawString(hx + 5*mm, info_y - 15*mm, f"{CLIENT_CO}  |  LATAM Market Entry")

    # FROM box
    rx = hx + left_w + 4*mm
    c.setFillColor(LIGHT_GREY)
    c.roundRect(rx, info_y - 18*mm, right_w, 18*mm, 1.5*mm, fill=1, stroke=0)
    c.setFillColor(TEAL)
    c.rect(rx, info_y - 18*mm, 2*mm, 18*mm, fill=1, stroke=0)
    sf(c, bold=True, size=6)
    c.setFillColor(MID_GREY)
    c.drawString(rx + 5*mm, info_y - 4*mm, "SUPPLIED BY")
    sf(c, bold=True, size=9)
    c.setFillColor(BLACK)
    c.drawString(rx + 5*mm, info_y - 10*mm, SUPPLIER)
    sf(c, size=7.5)
    c.setFillColor(MID_GREY)
    c.drawString(rx + 5*mm, info_y - 15*mm, f"{SUP_WEB}  |  FDA-Registered  |  cGMP")

    # ════════════════════════════════════════════════════════════════════════
    # LINE ITEMS
    # ════════════════════════════════════════════════════════════════════════
    y = info_y - 24*mm
    col_headers = ["DESCRIPTION", "QTY", "UNIT PRICE", "DISC.", "LINE TOTAL"]

    # ── Section A: Inventory ────────────────────────────────────────────────
    inv = [
        ("Tirzepatide 10mg lyophilized — Metabolic Line",            "50",  "$25.00", "—",  "$1,250.00"),
        ("Retatrutide 10mg lyophilized — Metabolic Line",            "40",  "$38.00", "—",  "$1,520.00"),
        ("BPC-157 10mg lyophilized — Recovery Line",                 "60",  "$15.00", "—",  "$900.00"),
        ("BPC-157 + TB-500 Combo 5mg+5mg — Recovery Line",          "20",  "$24.00", "—",  "$480.00"),
        ("NAD+ 1000mg lyophilized — Longevity Line",                "30",  "$35.00", "—",  "$1,050.00"),
        ("Epithalon 10mg lyophilized — Longevity Line",             "30",  "$18.00", "—",  "$540.00"),
        ("GHK-CU 50mg lyophilized — Recovery Line",                 "30",  "$18.00", "—",  "$540.00"),
        ("MOTS-c 10mg lyophilized — Longevity Line",                "20",  "$42.00", "—",  "$840.00"),
        ("Semax 30mg lyophilized — Longevity Line",                 "20",  "$22.00", "—",  "$440.00"),
        ("Methylene Blue 50mg/ml liquid — Recovery Line",           "20",  "$14.00", "—",  "$280.00"),
        ("TB-500 5mg lyophilized — Recovery Line",                  "30",  "$16.00", "—",  "$480.00"),
        ("CJC-1295 + Ipamorelin 10mg combo — Metabolic Line",      "20",  "$22.00", "—",  "$440.00"),
        ("HCG 5000IU lyophilized — Metabolic Line",                 "20",  "$16.00", "—",  "$320.00"),
        ("Bacteriostatic Water 30ml — Ancillary",                   "50",  "$4.50",  "—",  "$225.00"),
    ]
    y = draw_table_section(c, y, "A", "RESEARCH PEPTIDE INVENTORY — Custom NovaLabs Labelled (14 SKUs, 440 units)",
                           TEAL, col_headers, inv, "SUBTOTAL A:", "$9,305.00")

    # ── Section B: Branding ─────────────────────────────────────────────────
    brand = [
        ("Brand identity setup — logo, colour system, guidelines",      "1",    "$500.00", "—",  "$500.00"),
        ("Custom label design — 3 product lines (Metabolic/Recovery/Longevity)", "1", "$300.00", "—", "$300.00"),
        ("Label print run — 1,500 BOPP labels (3x500, cryogenic-rated)",  "1,500", "$0.60", "—", "$900.00"),
        ("Branded individual product boxes — 3 designs, CMYK print",    "100",  "$3.80",  "—",  "$380.00"),
        ("Branded outer mailer boxes — rigid, NovaLabs-printed",        "100",  "$2.80",  "—",  "$280.00"),
        ("Reconstitution insert cards — bilingual EN/ES, A5 double-sided", "200", "$0.45", "—", "$90.00"),
        ("Branded sealing tape — 50mm x 66m rolls",                     "6",    "$8.00",  "—",  "$48.00"),
    ]
    y = draw_table_section(c, y, "B", "CUSTOM BRANDING & PACKAGING — Full Brand Identity Package",
                           GREEN, col_headers, brand, "SUBTOTAL B:", "$2,498.00")

    # ── Section C: Fulfilment ───────────────────────────────────────────────
    ful = [
        ("US warehouse setup & API integration (one-time)",             "1",   "$500.00", "—",  "$500.00"),
        ("GROWTH fulfilment subscription — 6 months (150 orders/mo)",   "6",   "$400.00", "—",  "$2,400.00"),
        ("US domestic shipping credit — 50 prepaid orders",             "50",  "$5.00",   "—",  "$250.00"),
    ]
    y = draw_table_section(c, y, "C", "DROPSHIPPING & FULFILMENT — US Warehouse, Order Portal, Shipping",
                           BLUE, col_headers, ful, "SUBTOTAL C:", "$3,150.00")

    # ── Section D: QA ───────────────────────────────────────────────────────
    qa = [
        ("COA documentation package — all 14 SKUs, full batch records",  "1",  "$300.00", "—",  "$300.00"),
        ("Janoshik third-party testing — independent verification",      "14", "$55.00",  "—",  "$770.00"),
        ("HPLC chromatograms — all batches, full reports",               "1",  "—",       "—",  "Included"),
        ("Sterility & endotoxin testing — USP <71> + LAL",               "1",  "—",       "—",  "Included"),
    ]
    y = draw_table_section(c, y, "D", "QUALITY ASSURANCE — COAs, Janoshik Testing, HPLC, Sterility",
                           HIGHLIGHT, col_headers, qa, "SUBTOTAL D:", "$1,070.00")

    # ════════════════════════════════════════════════════════════════════════
    # GRAND TOTAL BOX
    # ════════════════════════════════════════════════════════════════════════
    y -= 1*mm
    gt_h = 20*mm
    gt_y = y - gt_h

    # Black background with teal border
    c.setStrokeColor(TEAL)
    c.setLineWidth(1.5)
    c.setFillColor(BLACK)
    c.roundRect(hx, gt_y, tw, gt_h, 2*mm, fill=1, stroke=1)

    # Subtotals breakdown line
    sf(c, size=6.5)
    c.setFillColor(SUB_TEXT)
    c.drawString(hx + 4*mm, gt_y + gt_h - 6*mm, "A: $9,305.00  +  B: $2,498.00  +  C: $3,150.00  +  D: $1,070.00")
    # Thin divider
    c.setStrokeColor(TEAL)
    c.setStrokeAlpha(0.3)
    c.setLineWidth(0.4)
    c.line(hx + 4*mm, gt_y + gt_h - 8*mm, hx + tw - 4*mm, gt_y + gt_h - 8*mm)
    c.setStrokeAlpha(1)
    # TOTAL label
    sf(c, bold=True, size=11)
    c.setFillColor(WHITE)
    c.drawString(hx + 4*mm, gt_y + 4*mm, "TOTAL DUE:")
    # Amount — large
    sf(c, bold=True, size=22)
    c.setFillColor(TEAL)
    c.drawRightString(hx + tw - 4*mm, gt_y + 3*mm, "USD $15,023.00")

    # ════════════════════════════════════════════════════════════════════════
    # PAYMENT & TERMS STRIP
    # ════════════════════════════════════════════════════════════════════════
    y = gt_y - 3*mm
    terms_h = 28*mm
    ty = y - terms_h

    # Two-column: Payment on left, Terms on right
    half = tw / 2 - 2*mm

    # Payment box
    c.setFillColor(LIGHT_GREY)
    c.roundRect(hx, ty, half, terms_h, 1.5*mm, fill=1, stroke=0)
    c.setFillColor(TEAL)
    c.rect(hx, ty, 2*mm, terms_h, fill=1, stroke=0)

    sf(c, bold=True, size=7)
    c.setFillColor(TEAL)
    c.drawString(hx + 5*mm, ty + terms_h - 5*mm, "PAYMENT INSTRUCTIONS")

    pay_lines = [
        ("Method:", "USDC / USDT (stablecoin)"),
        ("Amount:", "$15,023.00 USD — Full payment"),
        ("When:", "Full payment required to confirm order"),
        ("Wallet:", "Provided upon signed agreement"),
        ("Currency:", "USD equivalent at time of transfer"),
    ]
    py = ty + terms_h - 10*mm
    for lbl, val in pay_lines:
        sf(c, bold=True, size=5.8)
        c.setFillColor(BLACK)
        c.drawString(hx + 5*mm, py, lbl)
        sf(c, size=5.8)
        c.setFillColor(MID_GREY)
        c.drawString(hx + 22*mm, py, val)
        py -= 4*mm

    # Terms box
    tx = hx + half + 4*mm
    c.setFillColor(LIGHT_GREY)
    c.roundRect(tx, ty, half, terms_h, 1.5*mm, fill=1, stroke=0)
    c.setFillColor(TEAL)
    c.rect(tx, ty, 2*mm, terms_h, fill=1, stroke=0)

    sf(c, bold=True, size=7)
    c.setFillColor(TEAL)
    c.drawString(tx + 5*mm, ty + terms_h - 5*mm, "TERMS & CONDITIONS")

    terms_lines = [
        "This quote is valid for 30 days from date of issue.",
        "Full payment in USDC/USDT confirms the production order.",
        "Production lead time: 21-25 business days from payment.",
        "All brand assets remain client property upon full payment.",
        "Pricing, formulations and terms are strictly confidential.",
        "Damaged goods replaced at no cost within 14 days of delivery.",
    ]
    tly = ty + terms_h - 10*mm
    for line in terms_lines:
        c.setFillColor(TEAL)
        c.circle(tx + 6*mm, tly + 1*mm, 0.6*mm, fill=1, stroke=0)
        sf(c, size=5.5)
        c.setFillColor(MID_GREY)
        c.drawString(tx + 8*mm, tly, line)
        tly -= 3.5*mm

    # ════════════════════════════════════════════════════════════════════════
    # AUTHORIZATION & SIGNATURE LINE
    # ════════════════════════════════════════════════════════════════════════
    y = ty - 4*mm
    auth_h = 16*mm
    ay = y - auth_h

    c.setFillColor(colors.HexColor('#fafafa'))
    c.roundRect(hx, ay, tw, auth_h, 1.5*mm, fill=1, stroke=0)
    c.setStrokeColor(LINE_GREY)
    c.setLineWidth(0.4)
    c.roundRect(hx, ay, tw, auth_h, 1.5*mm, fill=0, stroke=1)

    sf(c, bold=True, size=6.5)
    c.setFillColor(BLACK)
    c.drawString(hx + 4*mm, ay + auth_h - 5*mm, "AUTHORIZATION")
    sf(c, size=5.5)
    c.setFillColor(MID_GREY)
    c.drawString(hx + 4*mm, ay + auth_h - 10*mm,
                 "By signing below, the client authorises Sigma Audley to proceed with the above order upon receipt of full payment.")

    # Signature lines
    sig_y = ay + 2*mm
    # Client sig
    c.setStrokeColor(MID_GREY)
    c.setLineWidth(0.4)
    c.line(hx + 4*mm, sig_y + 2*mm, hx + 60*mm, sig_y + 2*mm)
    sf(c, size=5)
    c.setFillColor(DIM_TEXT)
    c.drawString(hx + 4*mm, sig_y - 1*mm, f"Client Signature — {CLIENT}")

    # Date
    c.line(hx + 68*mm, sig_y + 2*mm, hx + 110*mm, sig_y + 2*mm)
    c.drawString(hx + 68*mm, sig_y - 1*mm, "Date")

    # SA sig
    c.line(hx + tw - 80*mm, sig_y + 2*mm, hx + tw - 20*mm, sig_y + 2*mm)
    c.drawString(hx + tw - 80*mm, sig_y - 1*mm, f"Authorized — {SUPPLIER}")

    # ════════════════════════════════════════════════════════════════════════
    # FOOTER
    # ════════════════════════════════════════════════════════════════════════
    # Bottom accent
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
    print("Quote PDF saved to: " + OUTPUT_PATH)


if __name__ == "__main__":
    main()
