"""
Generate Sigma Audley Wholesale Raw Materials Price List PDF.
Usage: python generate_wholesale.py
Output: wholesale-pricelist.pdf
"""

import json
import os
from datetime import datetime

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm, cm
from reportlab.lib.colors import HexColor, white
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, HRFlowable
)

# ── Colors ──────────────────────────────────────────────────────────
DARK_BLUE = HexColor('#1e293b')
GREEN = HexColor('#10b981')
GREEN_DARK = HexColor('#059669')
GREEN_LIGHT = HexColor('#ecfdf5')
WHITE = white
GRAY_50 = HexColor('#f8fafc')
GRAY_100 = HexColor('#f1f5f9')
GRAY_200 = HexColor('#e2e8f0')
GRAY_300 = HexColor('#cbd5e1')
GRAY_400 = HexColor('#94a3b8')
GRAY_500 = HexColor('#64748b')
GRAY_600 = HexColor('#475569')
GRAY_700 = HexColor('#334155')
GRAY_800 = HexColor('#1e293b')
BLUE_LINK = HexColor('#3b82f6')
RED = HexColor('#ef4444')

# ── Paragraph Styles ───────────────────────────────────────────────
S = {
    'cover_title': ParagraphStyle('CoverTitle', fontName='Helvetica-Bold', fontSize=32, leading=38, textColor=DARK_BLUE),
    'cover_title2': ParagraphStyle('CoverTitle2', fontName='Helvetica-Bold', fontSize=20, leading=26, textColor=GREEN_DARK),
    'cover_detail': ParagraphStyle('CoverDetail', fontName='Helvetica', fontSize=10, leading=15, textColor=GRAY_700),
    'cover_tagline': ParagraphStyle('CoverTag', fontName='Helvetica-Bold', fontSize=11, leading=16, textColor=GREEN_DARK),

    'cat_header': ParagraphStyle('CatH', fontName='Helvetica-Bold', fontSize=14, leading=18, textColor=WHITE),
    'subcat_header': ParagraphStyle('SubH', fontName='Helvetica-Bold', fontSize=10, leading=14, textColor=DARK_BLUE, spaceBefore=10, spaceAfter=4),

    'th': ParagraphStyle('TH', fontName='Helvetica-Bold', fontSize=7, leading=10, textColor=WHITE, alignment=TA_CENTER),
    'th_left': ParagraphStyle('THL', fontName='Helvetica-Bold', fontSize=7, leading=10, textColor=WHITE, alignment=TA_LEFT),
    'td': ParagraphStyle('TD', fontName='Helvetica', fontSize=7, leading=10, textColor=GRAY_700, alignment=TA_CENTER),
    'td_left': ParagraphStyle('TDL', fontName='Helvetica', fontSize=7, leading=10, textColor=GRAY_700, alignment=TA_LEFT),
    'td_name': ParagraphStyle('TDN', fontName='Helvetica', fontSize=7, leading=10, textColor=GRAY_800, alignment=TA_LEFT),
    'td_price': ParagraphStyle('TDP', fontName='Helvetica-Bold', fontSize=7, leading=10, textColor=GRAY_800, alignment=TA_CENTER),
    'td_best': ParagraphStyle('TDBest', fontName='Helvetica-Bold', fontSize=7, leading=10, textColor=GREEN_DARK, alignment=TA_CENTER),
    'td_link': ParagraphStyle('TDLink', fontName='Helvetica-Bold', fontSize=7, leading=10, textColor=GREEN_DARK, alignment=TA_CENTER),
    'td_per_g': ParagraphStyle('TDPerG', fontName='Helvetica', fontSize=5.5, leading=8, textColor=GRAY_400, alignment=TA_CENTER),
    'td_contact': ParagraphStyle('TDContact', fontName='Helvetica-Bold', fontSize=6.5, leading=9, textColor=BLUE_LINK, alignment=TA_CENTER),

    'footer': ParagraphStyle('Footer', fontName='Helvetica', fontSize=7, leading=10, textColor=GRAY_400, alignment=TA_CENTER),
    'body': ParagraphStyle('Body', fontName='Helvetica', fontSize=9, leading=14, textColor=GRAY_700),
    'body_bold': ParagraphStyle('BodyBold', fontName='Helvetica-Bold', fontSize=9, leading=14, textColor=GRAY_800),
    'body_small': ParagraphStyle('BodySm', fontName='Helvetica', fontSize=8, leading=12, textColor=GRAY_600),
    'contact_h': ParagraphStyle('ContactH', fontName='Helvetica-Bold', fontSize=12, leading=16, textColor=DARK_BLUE),
    'contact_item': ParagraphStyle('ContactItem', fontName='Helvetica', fontSize=9.5, leading=15, textColor=GRAY_700),
    'note': ParagraphStyle('Note', fontName='Helvetica-Oblique', fontSize=7.5, leading=11, textColor=GRAY_500),
}

PAGE_W, PAGE_H = A4
MARGIN = 1.5 * cm
CONTENT_W = PAGE_W - 2 * MARGIN


# ── Wholesale pricing data ─────────────────────────────────────────
# Tiers: 100g, 250g, 500g, 1kg, 5kg, 10kg
SARMS_WHOLESALE = [
    {
        'name': 'MK677 (Ibutamoren)',
        'cat_no': 'MK677-RAW',
        'janoshik_url': 'https://verify.janoshik.com.sigmaaudley.site/tests/51044-MK677_(Ibutamoren)_Raw_F7R6677PXKBC',
        'popular': True,
        'pricing': {
            '100g': 700, '250g': 1625, '500g': 2900,
            '1kg': 5200, '5kg': 23500, '10kg': 42000,
        },
    },
    {
        'name': 'RAD-140 (Testolone)',
        'cat_no': 'RAD140-RAW',
        'janoshik_url': 'https://verify.janoshik.com.sigmaaudley.site/tests/51731-RAD-140_Raw_481DO36BXP8K',
        'popular': False,
        'pricing': {
            '100g': 1200, '250g': 2750, '500g': 5000,
            '1kg': 9200, '5kg': 42500, '10kg': 78000,
        },
    },
    {
        'name': 'LGD-4033 (Ligandrol)',
        'cat_no': 'LGD4033-RAW',
        'janoshik_url': 'https://verify.janoshik.com.sigmaaudley.site/tests/51632-LGD4033_Raw_XRVTFN7NMK39',
        'popular': False,
        'pricing': {
            '100g': 1250, '250g': 2875, '500g': 5200,
            '1kg': 9600, '5kg': 44000, '10kg': 80000,
        },
    },
    {
        'name': 'YK-11',
        'cat_no': 'YK11-RAW',
        'janoshik_url': 'https://verify.janoshik.com.sigmaaudley.site/tests/51837-YK11_Raw_WGE8CP2TOLUS',
        'popular': False,
        'pricing': {
            '100g': 1800, '250g': 4125, '500g': 7500,
            '1kg': 13500, '5kg': 60000, '10kg': 108000,
        },
    },
    {
        'name': 'S-23',
        'cat_no': 'S23-RAW',
        'janoshik_url': 'https://verify.janoshik.com.sigmaaudley.site/tests/51133-S23_Raw_4Z25MU2LI2XW',
        'popular': False,
        'pricing': {
            '100g': 2000, '250g': 4500, '500g': 8000,
            '1kg': 14500, '5kg': 65000, '10kg': 118000,
        },
    },
    {
        'name': 'GW501516 (Cardarine)',
        'cat_no': 'GW501516-RAW',
        'janoshik_url': 'https://verify.janoshik.com.sigmaaudley.site/tests/51439-GW501516_(Cardarine)_Raw_7MIMHR2SVSD1',
        'popular': False,
        'pricing': {
            '100g': 1400, '250g': 3250, '500g': 5800,
            '1kg': 10500, '5kg': 47500, '10kg': 86000,
        },
    },
    {
        'name': 'Andarine (S-4)',
        'cat_no': 'S4-RAW',
        'janoshik_url': 'https://verify.janoshik.com.sigmaaudley.site/tests/51282-Andarine_S4_Raw_48YRQWJSIM2D',
        'popular': False,
        'pricing': {
            '100g': 1500, '250g': 3500, '500g': 6200,
            '1kg': 11200, '5kg': 50000, '10kg': 90000,
        },
    },
]

PEPTIDE_WHOLESALE = [
    {
        'name': 'Semaglutide',
        'cat_no': 'SEMAGLUTIDE-RAW',
        'janoshik_url': 'https://verify.janoshik.com.sigmaaudley.site/tests/51954-Semaglutide_Raw_GTTAHC36HI52',
        'popular': True,
        'pricing': {
            '100g': 13500, '250g': 31250, '500g': 57500,
            '1kg': 105000, '5kg': 475000, '10kg': 850000,
        },
    },
    {
        'name': 'Tirzepatide',
        'cat_no': 'TIRZEPATIDE-RAW',
        'janoshik_url': 'https://verify.janoshik.com.sigmaaudley.site/tests/51902-Tirzepatide_Raw_ZHKCZEJGTGSN',
        'popular': True,
        'pricing': {
            '100g': 16000, '250g': 37500, '500g': 67500,
            '1kg': 125000, '5kg': 575000, '10kg': 1050000,
        },
    },
    {
        'name': 'Retatrutide',
        'cat_no': 'RETATRUTIDE-RAW',
        'janoshik_url': 'https://verify.janoshik.com.sigmaaudley.site/tests/51915-Retatrutide_Raw_LR0C7VZ1DQ7N',
        'popular': False,
        'pricing': {
            '100g': 31000, '250g': 72500, '500g': 135000,
            '1kg': 250000, '5kg': None, '10kg': None,
        },
    },
    {
        'name': 'SS-31 (Elamipretide)',
        'cat_no': 'SS31-RAW',
        'janoshik_url': 'https://verify.janoshik.com.sigmaaudley.site/tests/51518-SS-31_(Elamipretide)_Raw_Q7HMCL0NEXUJ',
        'popular': False,
        'pricing': {
            '100g': 46000, '250g': 106250, '500g': 195000,
            '1kg': 360000, '5kg': None, '10kg': None,
        },
    },
]

TIERS = ['100g', '250g', '500g', '1kg', '5kg', '10kg']


# ── Helpers ─────────────────────────────────────────────────────────
def fmt_price(val):
    if val is None:
        return None
    if isinstance(val, (int, float)):
        if val == 0:
            return 'Contact'
        if val >= 1000:
            return f'${val:,.0f}'
        return f'${int(val)}'
    return str(val)


def per_gram(total, grams):
    if total is None:
        return None
    return total / grams


TIER_GRAMS = {'100g': 100, '250g': 250, '500g': 500, '1kg': 1000, '5kg': 5000, '10kg': 10000}


def fmt_per_gram(total, tier):
    if total is None:
        return ''
    g = TIER_GRAMS[tier]
    pg = total / g
    if pg >= 1:
        return f'${pg:,.2f}/g'
    return f'${pg:.3f}/g'


def janoshik_cell(url):
    if url:
        return Paragraph(f'<a href="{url}" color="#059669"><b>Verify</b></a>', S['td_link'])
    return Paragraph('-', S['td'])


def category_header_bar(title, description=''):
    parts = []
    if description:
        cell = Paragraph(f'{title} <font size="8" color="#94a3b8">  {description}</font>', S['cat_header'])
    else:
        cell = Paragraph(title, S['cat_header'])

    t = Table([[cell]], colWidths=[CONTENT_W])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), DARK_BLUE),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('ROUNDEDCORNERS', [4, 4, 0, 0]),
    ]))
    parts.append(t)
    return parts


def subcategory_label(title):
    t = Table([[Paragraph(title, S['subcat_header'])]], colWidths=[CONTENT_W])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), GRAY_100),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LINEBELOW', (0, 0), (-1, -1), 1, GREEN),
    ]))
    return t


# ── Build wholesale table ──────────────────────────────────────────
def build_wholesale_table(products):
    """Table: Product | 100g | 250g | 500g | 1kg | 5kg | 10kg | Janoshik"""

    # Headers: Product Name, then each tier with per-gram sub-header, then Janoshik
    header_row = [Paragraph('<b>Product</b>', S['th_left'])]
    for tier in TIERS:
        header_row.append(Paragraph(f'<b>{tier}</b>', S['th']))
    header_row.append(Paragraph('<b>Janoshik</b>', S['th']))

    # Column widths
    janoshik_w = 42
    price_col_w = 58
    fixed = len(TIERS) * price_col_w + janoshik_w
    name_w = CONTENT_W - fixed
    col_widths = [name_w] + [price_col_w] * len(TIERS) + [janoshik_w]

    rows = [header_row]

    for p in products:
        pricing = p['pricing']

        # Product name with badges
        name = p['name']
        badges = ''
        if p.get('popular'):
            badges += ' <font size="5.5" color="#ef4444"><b>[HOT]</b></font>'

        # Row with price + per-gram in each cell
        row = [Paragraph(f'{name}{badges}<br/><font size="5.5" color="#94a3b8">{p["cat_no"]}</font>', S['td_name'])]

        for tier in TIERS:
            val = pricing.get(tier)
            if val is None:
                row.append(Paragraph('<font color="#3b82f6"><b>Contact</b></font>', S['td_contact']))
            else:
                price_str = fmt_price(val)
                pg_str = fmt_per_gram(val, tier)
                row.append(Paragraph(f'<b>{price_str}</b><br/><font size="5" color="#94a3b8">{pg_str}</font>', S['td_price']))

        row.append(janoshik_cell(p.get('janoshik_url')))
        rows.append(row)

    t = Table(rows, colWidths=col_widths, repeatRows=1)

    style_cmds = [
        ('BACKGROUND', (0, 0), (-1, 0), DARK_BLUE),
        ('TEXTCOLOR', (0, 0), (-1, 0), WHITE),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 7),
        ('TOPPADDING', (0, 0), (-1, 0), 6),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 4),
        ('RIGHTPADDING', (0, 0), (-1, -1), 4),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [WHITE, GRAY_50]),
        ('GRID', (0, 0), (-1, -1), 0.4, GRAY_200),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 1), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 5),
        # Highlight last price column (10kg = best value)
        ('BACKGROUND', (6, 1), (6, -1), HexColor('#f0fdf4')),
    ]
    t.setStyle(TableStyle(style_cmds))
    return t


# ── Cover page ─────────────────────────────────────────────────────
def build_cover(story, contact):
    story.append(Spacer(1, 50))

    story.append(Paragraph('SIGMA AUDLEY', S['cover_title']))
    story.append(Spacer(1, 6))
    story.append(Paragraph('Wholesale Raw Materials Price List', S['cover_title2']))
    story.append(Spacer(1, 16))

    # Contact info
    story.append(Paragraph(
        '<b>Website:</b> <a href="https://sigmaaudley.site" color="#3b82f6">https://sigmaaudley.site</a>',
        S['cover_detail']))
    story.append(Spacer(1, 4))
    story.append(Paragraph(f'<b>Email:</b> {contact["email"]}', S['cover_detail']))
    story.append(Spacer(1, 4))
    story.append(Paragraph(f'<b>Telegram:</b> {contact["telegram"]} ({contact["telegram_name"]})', S['cover_detail']))
    story.append(Spacer(1, 4))
    story.append(Paragraph(f'<b>WhatsApp:</b> {contact["whatsapp"]} ({contact["whatsapp_name"]})', S['cover_detail']))
    story.append(Spacer(1, 20))

    # Tagline
    story.append(Paragraph(
        'Janoshik Verified  |  99%+ Purity  |  MOQ 100g  |  Worldwide Shipping',
        S['cover_tagline']))
    story.append(Spacer(1, 24))

    # Key info box
    info_items = [
        '<b>Minimum Order:</b> 100g per compound',
        '<b>Purity:</b> All batches 99%+ verified by Janoshik Analytical',
        '<b>Packaging:</b> Vacuum-sealed, light-protected, desiccated',
        '<b>Shipping:</b> Worldwide express with full tracking',
        '<b>Payment:</b> Wire Transfer, Crypto (BTC, ETH, USDT), Card',
        '<b>Lead Time:</b> 3-5 business days standard, 1-2 days express',
    ]
    info_cells = [[Paragraph(item, S['body'])] for item in info_items]
    info_t = Table(info_cells, colWidths=[CONTENT_W - 24])
    info_t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), GRAY_50),
        ('LEFTPADDING', (0, 0), (-1, -1), 14),
        ('RIGHTPADDING', (0, 0), (-1, -1), 14),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LINEBEFORE', (0, 0), (0, -1), 3, GREEN),
        ('BOX', (0, 0), (-1, -1), 0.5, GRAY_200),
        ('ROUNDEDCORNERS', [4, 4, 4, 4]),
    ]))
    story.append(info_t)
    story.append(Spacer(1, 24))

    # Pricing tiers overview
    story.append(Paragraph('<b>Wholesale Pricing Tiers</b>', S['body_bold']))
    story.append(Spacer(1, 6))

    tier_data = [
        [Paragraph('<b>Quantity</b>', S['th_left']),
         Paragraph('<b>100g</b>', S['th']),
         Paragraph('<b>250g</b>', S['th']),
         Paragraph('<b>500g</b>', S['th']),
         Paragraph('<b>1kg</b>', S['th']),
         Paragraph('<b>5kg</b>', S['th']),
         Paragraph('<b>10kg</b>', S['th'])],
        [Paragraph('Discount', S['td_left']),
         Paragraph('Base', S['td']),
         Paragraph('~7%', S['td']),
         Paragraph('~17%', S['td']),
         Paragraph('~26%', S['td']),
         Paragraph('~33%', S['td']),
         Paragraph('<b>~40%</b>', S['td_best'])],
    ]
    tier_t = Table(tier_data, colWidths=[80] + [int((CONTENT_W - 80) / 6)] * 6)
    tier_t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), GREEN_DARK),
        ('TEXTCOLOR', (0, 0), (-1, 0), WHITE),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [GREEN_LIGHT]),
        ('GRID', (0, 0), (-1, -1), 0.5, GREEN),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('ROUNDEDCORNERS', [4, 4, 4, 4]),
        # Highlight best value column
        ('BACKGROUND', (6, 1), (6, -1), HexColor('#d1fae5')),
    ]))
    story.append(tier_t)
    story.append(Spacer(1, 24))

    # Janoshik note
    note_t = Table(
        [[Paragraph(
            '<b>Janoshik Verified:</b> Every batch is independently tested by Janoshik Analytical '
            'Laboratory. Click the green "Verify" links in the pricing tables to view full lab '
            'reports with purity analysis.',
            S['body'])]],
        colWidths=[CONTENT_W - 20]
    )
    note_t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), GREEN_LIGHT),
        ('LEFTPADDING', (0, 0), (-1, -1), 12),
        ('RIGHTPADDING', (0, 0), (-1, -1), 12),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ('LINEBEFORE', (0, 0), (0, -1), 3, GREEN),
        ('BOX', (0, 0), (-1, -1), 0.5, GREEN),
        ('ROUNDEDCORNERS', [4, 4, 4, 4]),
    ]))
    story.append(note_t)
    story.append(Spacer(1, 30))

    story.append(Paragraph(
        f'Generated: {datetime.now().strftime("%B %d, %Y")}  |  Prices in USD  |  All prices subject to change',
        S['note']))

    story.append(PageBreak())


# ── Product pages ──────────────────────────────────────────────────
def build_product_pages(story):
    # SARMs section
    story.extend(category_header_bar('SARMS RAW POWDERS', 'Selective Androgen Receptor Modulators'))
    story.append(Spacer(1, 6))
    story.append(subcategory_label(f'SARMs Raw Materials ({len(SARMS_WHOLESALE)} products)'))
    story.append(Spacer(1, 4))
    story.append(build_wholesale_table(SARMS_WHOLESALE))
    story.append(Spacer(1, 20))

    # Peptide APIs section
    story.extend(category_header_bar('PEPTIDE API RAW POWDERS', 'Active Pharmaceutical Ingredients'))
    story.append(Spacer(1, 6))
    story.append(subcategory_label(f'Peptide APIs ({len(PEPTIDE_WHOLESALE)} products)'))
    story.append(Spacer(1, 4))
    story.append(build_wholesale_table(PEPTIDE_WHOLESALE))
    story.append(Spacer(1, 20))

    # Notes
    notes = [
        'All prices in USD. Prices are per total quantity, not per gram.',
        'Per-gram rates shown for reference below each price.',
        '"Contact" indicates custom pricing for large orders - reach out for a quote.',
        '10kg column highlighted as best per-gram value.',
        'Volume discounts may apply for recurring orders - contact for details.',
        'COA (Certificate of Analysis) provided with every shipment.',
    ]
    for i, note in enumerate(notes):
        story.append(Paragraph(f'{i + 1}. {note}', S['body_small']))
        story.append(Spacer(1, 2))

    story.append(PageBreak())


# ── Contact page ──────────────────────────────────────────────────
def build_contact_page(story, contact):
    story.append(Spacer(1, 20))
    story.extend(category_header_bar('CONTACT & ORDERING INFORMATION'))
    story.append(Spacer(1, 16))

    story.append(Paragraph('<b>Wholesale Contact</b>', S['contact_h']))
    story.append(Spacer(1, 8))

    contact_data = [
        ['Email', contact['email']],
        ['Telegram', f'{contact["telegram"]} ({contact["telegram_name"]})'],
        ['WhatsApp', f'{contact["whatsapp"]} ({contact["whatsapp_name"]})'],
        ['Website', 'https://sigmaaudley.site'],
    ]
    for label, value in contact_data:
        story.append(Paragraph(f'<b>{label}:</b>  {value}', S['contact_item']))
        story.append(Spacer(1, 3))

    story.append(Spacer(1, 16))

    # How to order
    story.append(Paragraph('<b>How to Place a Wholesale Order</b>', S['contact_h']))
    story.append(Spacer(1, 8))

    steps = [
        '<b>1.</b> Contact us via Telegram or WhatsApp with your product list and quantities.',
        '<b>2.</b> Receive a confirmed quote with shipping costs and lead time.',
        '<b>3.</b> Complete payment via wire transfer, crypto, or card.',
        '<b>4.</b> Receive tracking within 24 hours of confirmed payment.',
        '<b>5.</b> COA and Janoshik verification links included with every shipment.',
    ]
    for step in steps:
        story.append(Paragraph(step, S['contact_item']))
        story.append(Spacer(1, 3))

    story.append(Spacer(1, 16))

    # Shipping
    story.append(Paragraph('<b>Worldwide Shipping</b>', S['contact_h']))
    story.append(Spacer(1, 8))

    wh_data = [
        [Paragraph('<b>Region</b>', S['th_left']),
         Paragraph('<b>Standard</b>', S['th']),
         Paragraph('<b>Express</b>', S['th'])],
        [Paragraph('United States', S['td_left']),
         Paragraph('5-8 business days', S['td']),
         Paragraph('2-4 business days', S['td'])],
        [Paragraph('United Kingdom', S['td_left']),
         Paragraph('5-8 business days', S['td']),
         Paragraph('2-4 business days', S['td'])],
        [Paragraph('Canada', S['td_left']),
         Paragraph('5-8 business days', S['td']),
         Paragraph('2-4 business days', S['td'])],
        [Paragraph('Europe', S['td_left']),
         Paragraph('5-10 business days', S['td']),
         Paragraph('3-5 business days', S['td'])],
        [Paragraph('Australia', S['td_left']),
         Paragraph('5-10 business days', S['td']),
         Paragraph('3-5 business days', S['td'])],
        [Paragraph('Rest of World', S['td_left']),
         Paragraph('7-15 business days', S['td']),
         Paragraph('4-7 business days', S['td'])],
    ]
    wh_t = Table(wh_data, colWidths=[180, 140, 140])
    wh_t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), DARK_BLUE),
        ('TEXTCOLOR', (0, 0), (-1, 0), WHITE),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [WHITE, GRAY_50]),
        ('GRID', (0, 0), (-1, -1), 0.4, GRAY_200),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    story.append(wh_t)
    story.append(Spacer(1, 16))

    # Payment
    story.append(Paragraph('<b>Accepted Payment Methods</b>', S['contact_h']))
    story.append(Spacer(1, 6))
    story.append(Paragraph('Wire Transfer (preferred for large orders)', S['contact_item']))
    story.append(Paragraph('Cryptocurrency: Bitcoin, Ethereum, USDT, BSC', S['contact_item']))
    story.append(Paragraph('Visa, Mastercard, Apple Pay, Google Pay', S['contact_item']))
    story.append(Spacer(1, 20))

    # Lab testing note
    note_t = Table(
        [[Paragraph(
            '<b>Quality Guarantee:</b> All raw materials are independently tested by Janoshik '
            'Analytical Laboratory with 99%+ purity results. Full COA and Janoshik verification '
            'links provided with every order. We stand behind our quality with a satisfaction guarantee.',
            S['body'])]],
        colWidths=[CONTENT_W - 20]
    )
    note_t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), GREEN_LIGHT),
        ('LEFTPADDING', (0, 0), (-1, -1), 12),
        ('RIGHTPADDING', (0, 0), (-1, -1), 12),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ('LINEBEFORE', (0, 0), (0, -1), 3, GREEN),
        ('BOX', (0, 0), (-1, -1), 0.5, GREEN),
        ('ROUNDEDCORNERS', [4, 4, 4, 4]),
    ]))
    story.append(note_t)

    story.append(Spacer(1, 30))
    story.append(HRFlowable(width="100%", thickness=0.5, color=GRAY_200))
    story.append(Spacer(1, 8))
    story.append(Paragraph(
        f'Generated {datetime.now().strftime("%B %d, %Y")}  |  Sigma Audley  |  sigmaaudley.site  |  Prices in USD',
        S['footer']))
    story.append(Paragraph('All products are for research purposes only. Prices subject to change without notice.', S['footer']))


# ── Page number footer ─────────────────────────────────────────────
def add_page_number(canvas, doc):
    page_num = canvas.getPageNumber()
    text = f'sigmaaudley.site  |  Wholesale Price List  |  Page {page_num}'
    canvas.saveState()
    canvas.setFont('Helvetica', 7)
    canvas.setFillColor(GRAY_400)
    canvas.drawCentredString(PAGE_W / 2, MARGIN - 8 * mm, text)
    canvas.restoreState()


# ── Main ───────────────────────────────────────────────────────────
def main():
    # Load contact info from pricelist-data.json
    json_path = os.path.join(os.path.dirname(__file__), 'pricelist-data.json')
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    contact = data['company_info']['contact']

    output_path = os.path.join(os.path.dirname(__file__), 'wholesale-pricelist.pdf')

    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        topMargin=MARGIN,
        bottomMargin=MARGIN + 5 * mm,
        leftMargin=MARGIN,
        rightMargin=MARGIN,
        title='Sigma Audley - Wholesale Raw Materials Price List',
        author='Sigma Audley',
    )

    story = []
    build_cover(story, contact)
    build_product_pages(story)
    build_contact_page(story, contact)

    doc.build(story, onFirstPage=add_page_number, onLaterPages=add_page_number)
    print(f'PDF generated: {output_path}')
    total = len(SARMS_WHOLESALE) + len(PEPTIDE_WHOLESALE)
    print(f'Products: {total} | Tiers: {", ".join(TIERS)}')


if __name__ == '__main__':
    main()
