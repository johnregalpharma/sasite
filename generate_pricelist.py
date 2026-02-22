"""
Generate Sigma Audley Pricelist PDF from extracted product data.
Usage: python generate_pricelist.py
Prereq: node extract-data.js (generates pricelist-data.json)
Output: pricelist.pdf
"""

import json
import os
from datetime import datetime

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm, cm
from reportlab.lib.colors import HexColor, white, black, Color
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, KeepTogether, HRFlowable, Flowable
)

# ── Colors ──────────────────────────────────────────────────────────
DARK_BLUE = HexColor('#1e293b')
DARKER_BLUE = HexColor('#0f172a')
GREEN = HexColor('#10b981')
GREEN_DARK = HexColor('#059669')
GREEN_LIGHT = HexColor('#ecfdf5')
GREEN_100 = HexColor('#d1fae5')
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
AMBER = HexColor('#f59e0b')
AMBER_LIGHT = HexColor('#fffbeb')
RED = HexColor('#ef4444')
BLUE_LINK = HexColor('#3b82f6')

# ── Paragraph Styles ───────────────────────────────────────────────
S = {
    'cover_title': ParagraphStyle('CoverTitle', fontName='Helvetica-Bold', fontSize=32, leading=38, textColor=DARK_BLUE),
    'cover_subtitle': ParagraphStyle('CoverSub', fontName='Helvetica', fontSize=14, leading=20, textColor=GRAY_600),
    'cover_tagline': ParagraphStyle('CoverTag', fontName='Helvetica-Bold', fontSize=11, leading=16, textColor=GREEN_DARK),
    'cover_detail': ParagraphStyle('CoverDetail', fontName='Helvetica', fontSize=10, leading=15, textColor=GRAY_700),

    'cat_header': ParagraphStyle('CatH', fontName='Helvetica-Bold', fontSize=14, leading=18, textColor=WHITE),
    'cat_desc': ParagraphStyle('CatD', fontName='Helvetica', fontSize=9, leading=13, textColor=GRAY_300),
    'subcat_header': ParagraphStyle('SubH', fontName='Helvetica-Bold', fontSize=10, leading=14, textColor=DARK_BLUE, spaceBefore=10, spaceAfter=4),

    'th': ParagraphStyle('TH', fontName='Helvetica-Bold', fontSize=7, leading=10, textColor=WHITE, alignment=TA_CENTER),
    'th_left': ParagraphStyle('THL', fontName='Helvetica-Bold', fontSize=7, leading=10, textColor=WHITE, alignment=TA_LEFT),
    'td': ParagraphStyle('TD', fontName='Helvetica', fontSize=7, leading=10, textColor=GRAY_700, alignment=TA_CENTER),
    'td_left': ParagraphStyle('TDL', fontName='Helvetica', fontSize=7, leading=10, textColor=GRAY_700, alignment=TA_LEFT),
    'td_name': ParagraphStyle('TDN', fontName='Helvetica', fontSize=7, leading=10, textColor=GRAY_800, alignment=TA_LEFT),
    'td_price': ParagraphStyle('TDP', fontName='Helvetica-Bold', fontSize=7, leading=10, textColor=GRAY_800, alignment=TA_CENTER),
    'td_link': ParagraphStyle('TDLink', fontName='Helvetica-Bold', fontSize=7, leading=10, textColor=GREEN_DARK, alignment=TA_CENTER),
    'td_badge': ParagraphStyle('TDBadge', fontName='Helvetica-Bold', fontSize=5.5, leading=8, textColor=WHITE),

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


def load_data():
    json_path = os.path.join(os.path.dirname(__file__), 'pricelist-data.json')
    with open(json_path, 'r', encoding='utf-8') as f:
        return json.load(f)


# ── Helper: category header bar ────────────────────────────────────
def category_header_bar(title, description=''):
    """Full-width dark blue bar with category name."""
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


# ── Helper: format price ───────────────────────────────────────────
def fmt_price(val):
    if val is None:
        return '-'
    if isinstance(val, (int, float)):
        if val == 0:
            return 'Contact'
        if val == int(val):
            return f'${int(val)}'
        return f'${val:.2f}'
    return str(val)


# ── Helper: Janoshik link cell ─────────────────────────────────────
def janoshik_cell(url):
    if url:
        return Paragraph(f'<a href="{url}" color="#059669"><b>Verify</b></a>', S['td_link'])
    return Paragraph('-', S['td'])


# ── Helper: product name with badges ──────────────────────────────
def product_name_cell(product):
    name = product['name']
    badges = ''
    if product.get('popular'):
        badges += ' <font size="5.5" color="#ef4444"><b>[HOT]</b></font>'
    if product.get('new'):
        badges += ' <font size="5.5" color="#3b82f6"><b>[NEW]</b></font>'
    if product.get('best_value'):
        badges += ' <font size="5.5" color="#10b981"><b>[BEST]</b></font>'
    return Paragraph(f'{name}{badges}', S['td_name'])


# ── Build standard product table (peptides, orals, injectables) ───
def build_standard_table(products):
    """Table: Cat No | Product | Spec | Janoshik | Base | 10+ | 20+ | 50+"""
    # Determine which bulk tiers exist
    has_20 = any('20' in p['pricing'] for p in products)
    has_50 = any('50' in p['pricing'] for p in products)

    headers_text = ['Cat No.', 'Product Name', 'Specification', 'Janoshik', 'Price']
    if any('10' in p['pricing'] for p in products):
        headers_text.append('10+')
    if has_20:
        headers_text.append('20+')
    if has_50:
        headers_text.append('50+')

    ncols = len(headers_text)

    # Column widths
    base_cols = [38, None, 78, 42, 40]  # Cat, Name, Spec, Janoshik, Base
    extra_cols = []
    if any('10' in p['pricing'] for p in products):
        extra_cols.append(32)
    if has_20:
        extra_cols.append(32)
    if has_50:
        extra_cols.append(32)

    used = sum(c for c in base_cols if c) + sum(extra_cols)
    name_w = CONTENT_W - used
    col_widths = [base_cols[0], name_w, base_cols[2], base_cols[3], base_cols[4]] + extra_cols

    # Header row
    header_row = []
    for i, h in enumerate(headers_text):
        style = S['th_left'] if i in (0, 1, 2) else S['th']
        header_row.append(Paragraph(h, style))

    rows = [header_row]

    for p in products:
        pricing = p['pricing']
        base = pricing.get('base')
        row = [
            Paragraph(p['cat_no'], S['td_left']),
            product_name_cell(p),
            Paragraph(p.get('specification', ''), S['td_left']),
            janoshik_cell(p.get('janoshik_url')),
            Paragraph(fmt_price(base) if not p.get('contact_pricing') else 'Contact', S['td_price']),
        ]
        if any('10' in pr['pricing'] for pr in products):
            row.append(Paragraph(fmt_price(pricing.get('10')) if not p.get('contact_pricing') else '-', S['td']))
        if has_20:
            row.append(Paragraph(fmt_price(pricing.get('20')) if not p.get('contact_pricing') else '-', S['td']))
        if has_50:
            row.append(Paragraph(fmt_price(pricing.get('50')) if not p.get('contact_pricing') else '-', S['td']))
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
        ('TOPPADDING', (0, 1), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 4),
    ]
    t.setStyle(TableStyle(style_cmds))
    return t


# ── Build raw materials table (weight-based pricing) ──────────────
def build_raw_table(products):
    """Table: Cat No | Product | 10g | 50g | 100g | 500g | 1kg | Janoshik"""
    # Determine which weight tiers exist
    all_tiers = set()
    for p in products:
        for k in p['pricing']:
            if k not in ('base', 'per_gram'):
                all_tiers.add(k)
        if 'per_gram' in p['pricing']:
            all_tiers.add('per_gram')

    # Order tiers logically
    tier_order = ['per_gram', '10g', '50g', '100g', '500g', '1kg']
    tiers = [t for t in tier_order if t in all_tiers]

    tier_labels = {'per_gram': '/gram', '10g': '10g', '50g': '50g', '100g': '100g', '500g': '500g', '1kg': '1kg'}

    headers_text = ['Cat No.', 'Product Name'] + [tier_labels.get(t, t) for t in tiers] + ['Janoshik']
    ncols = len(headers_text)

    price_col_w = 40
    janoshik_col_w = 42
    cat_col_w = 55
    fixed = cat_col_w + len(tiers) * price_col_w + janoshik_col_w
    name_w = CONTENT_W - fixed

    col_widths = [cat_col_w, name_w] + [price_col_w] * len(tiers) + [janoshik_col_w]

    header_row = []
    for i, h in enumerate(headers_text):
        style = S['th_left'] if i in (0, 1) else S['th']
        header_row.append(Paragraph(h, style))

    rows = [header_row]

    for p in products:
        pricing = p['pricing']
        row = [
            Paragraph(p['cat_no'], S['td_left']),
            product_name_cell(p),
        ]
        for tier in tiers:
            val = pricing.get(tier)
            row.append(Paragraph(fmt_price(val), S['td']))
        row.append(janoshik_cell(p.get('janoshik_url')))
        rows.append(row)

    t = Table(rows, colWidths=col_widths, repeatRows=1)
    t.setStyle(TableStyle([
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
        ('TOPPADDING', (0, 1), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 4),
    ]))
    return t


# ── Cover page ─────────────────────────────────────────────────────
def build_cover(story, data):
    story.append(Spacer(1, 50))

    # Title
    story.append(Paragraph('SIGMA AUDLEY', S['cover_title']))
    story.append(Spacer(1, 6))
    story.append(Paragraph('Complete Product Price List', ParagraphStyle(
        'CoverTitle2', fontName='Helvetica-Bold', fontSize=20, leading=26, textColor=GREEN_DARK)))
    story.append(Spacer(1, 16))

    # Website & contact
    story.append(Paragraph(
        '<b>Website:</b> <a href="https://sigmaaudley.site" color="#3b82f6">https://sigmaaudley.site</a>', S['cover_detail']))
    story.append(Spacer(1, 4))
    ci = data['company_info']['contact']
    story.append(Paragraph(f'<b>Email:</b> {ci["email"]}', S['cover_detail']))
    story.append(Spacer(1, 4))
    story.append(Paragraph(f'<b>Telegram:</b> {ci["telegram"]} ({ci["telegram_name"]})', S['cover_detail']))
    story.append(Spacer(1, 4))
    story.append(Paragraph(f'<b>WhatsApp:</b> {ci["whatsapp"]} ({ci["whatsapp_name"]})', S['cover_detail']))
    story.append(Spacer(1, 20))

    # Tagline
    total = data['total_products']
    janoshik_count = data['total_janoshik']
    story.append(Paragraph(
        f'{janoshik_count} Janoshik Verified Test Reports  |  {total}+ Compounds  |  5+ Worldwide Warehouses',
        S['cover_tagline']))
    story.append(Spacer(1, 24))

    # Discount tiers box
    disc_data = [
        [Paragraph('<b>Order Value</b>', S['th_left']),
         Paragraph('<b>Discount</b>', S['th']),
         Paragraph('<b>Shipping</b>', S['th'])],
        [Paragraph('$500+', S['td_left']),
         Paragraph('5% OFF', S['td_price']),
         Paragraph('Free Express', S['td'])],
        [Paragraph('$1,000+', S['td_left']),
         Paragraph('10% OFF', S['td_price']),
         Paragraph('Free Express', S['td'])],
        [Paragraph('$2,500+', S['td_left']),
         Paragraph('20% OFF', S['td_price']),
         Paragraph('Free Express', S['td'])],
    ]
    disc_t = Table(disc_data, colWidths=[160, 120, 120])
    disc_t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), GREEN_DARK),
        ('TEXTCOLOR', (0, 0), (-1, 0), WHITE),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [GREEN_LIGHT, WHITE]),
        ('GRID', (0, 0), (-1, -1), 0.5, GREEN),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('ROUNDEDCORNERS', [4, 4, 4, 4]),
    ]))
    story.append(Paragraph('<b>Prosperity Sale  -  Volume Discounts</b>', S['body_bold']))
    story.append(Spacer(1, 6))
    story.append(disc_t)
    story.append(Spacer(1, 24))

    # Janoshik note
    note_t = Table(
        [[Paragraph(
            '<b>Janoshik Verified:</b> Click the green "Verify" links in the tables to view '
            'independent lab test reports on janoshik.com. All products are tested for purity '
            'and identity verification.',
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
    story.append(Spacer(1, 20))

    # Trust signals
    trust_items = [
        'Janoshik Lab Tested',
        '100% Delivery Guarantee',
        '60-Day Refund Policy',
        'Secure Payment (Visa, MC, Crypto)',
    ]
    trust_row = [Paragraph(f'<b>{item}</b>', ParagraphStyle(
        'Trust', fontName='Helvetica-Bold', fontSize=8, leading=12, textColor=GREEN_DARK, alignment=TA_CENTER
    )) for item in trust_items]
    trust_t = Table([trust_row], colWidths=[CONTENT_W / 4] * 4)
    trust_t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), GRAY_50),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 0.5, GRAY_200),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('ROUNDEDCORNERS', [4, 4, 4, 4]),
    ]))
    story.append(trust_t)
    story.append(Spacer(1, 30))

    # Generation info
    story.append(Paragraph(
        f'Generated: {datetime.now().strftime("%B %d, %Y")}  |  Prices in USD  |  All prices subject to change',
        S['note']))

    story.append(PageBreak())


# ── Category display names ─────────────────────────────────────────
CATEGORY_NAMES = {
    'peptides': 'PEPTIDES',
    'oral_tablets': 'ORAL TABLETS',
    'injectable_oils': 'INJECTABLE OILS',
    'specialty_injections': 'SPECIALTY INJECTIONS',
    'raw_materials': 'RAW MATERIALS',
}

SUBCATEGORY_NAMES = {
    'growth_hormones': 'Growth Hormones & HGH',
    'weight_loss': 'Weight Loss & GLP-1',
    'healing': 'Healing & Recovery',
    'nad_longevity': 'NAD+ & Longevity',
    'research_peptides': 'Research & Enhancement Peptides',
    'anabolic_steroids': 'Anabolic Steroids',
    'pct': 'PCT & Anti-Estrogen',
    'fat_loss': 'Fat Loss & Cutting',
    'sarms': 'SARMs',
    'enhancement': 'Enhancement & ED Support',
    'specialty': 'Specialty Compounds',
    'testosterone': 'Testosterone',
    'trenbolone': 'Trenbolone',
    'other_injectables': 'Other Injectables',
    'nandrolone': 'Nandrolone & NPP',
    'lipotropic': 'Lipotropic & Fat Loss',
    'wellness': 'Health & Wellness',
    'peptides': 'Peptide Raw Materials',
}


# ── Build product pages ───────────────────────────────────────────
def build_product_pages(story, data):
    for cat in data['categories']:
        cat_key = cat['key']
        cat_name = CATEGORY_NAMES.get(cat_key, cat_key.upper().replace('_', ' '))
        cat_desc = cat.get('description', '')

        # Category header bar
        story.extend(category_header_bar(cat_name, cat_desc))
        story.append(Spacer(1, 8))

        is_raw = cat_key == 'raw_materials'

        for sub in cat['subcategories']:
            products = sub['products']
            if not products:
                continue

            sub_name = SUBCATEGORY_NAMES.get(sub['key'], sub.get('description', sub['key']))

            # Subcategory label
            story.append(subcategory_label(f'{sub_name} ({len(products)} products)'))
            story.append(Spacer(1, 4))

            # Build appropriate table
            if is_raw:
                story.append(build_raw_table(products))
            else:
                story.append(build_standard_table(products))

            story.append(Spacer(1, 10))

        story.append(PageBreak())


# ── Last page: contact & ordering info ─────────────────────────────
def build_contact_page(story, data):
    ci = data['company_info']['contact']

    story.append(Spacer(1, 20))
    story.extend(category_header_bar('CONTACT & ORDERING INFORMATION'))
    story.append(Spacer(1, 16))

    # Contact details
    story.append(Paragraph('<b>Contact Us</b>', S['contact_h']))
    story.append(Spacer(1, 8))

    contact_data = [
        ['Email', ci['email']],
        ['Telegram', f'{ci["telegram"]} ({ci["telegram_name"]})'],
        ['WhatsApp', f'{ci["whatsapp"]} ({ci["whatsapp_name"]})'],
        ['Website', 'https://sigmaaudley.site'],
    ]
    for label, value in contact_data:
        story.append(Paragraph(f'<b>{label}:</b>  {value}', S['contact_item']))
        story.append(Spacer(1, 3))

    story.append(Spacer(1, 16))

    # Warehouse locations
    story.append(Paragraph('<b>Worldwide Warehouse Locations</b>', S['contact_h']))
    story.append(Spacer(1, 8))

    wh_data = [
        [Paragraph('<b>Location</b>', S['th_left']),
         Paragraph('<b>Standard Shipping</b>', S['th']),
         Paragraph('<b>Express Shipping</b>', S['th'])],
        [Paragraph('United States (Los Angeles)', S['td_left']),
         Paragraph('2-5 business days', S['td']),
         Paragraph('1-3 business days', S['td'])],
        [Paragraph('United Kingdom (London)', S['td_left']),
         Paragraph('3-5 business days', S['td']),
         Paragraph('Next day by 1pm', S['td'])],
        [Paragraph('Canada (Toronto)', S['td_left']),
         Paragraph('2-5 business days', S['td']),
         Paragraph('1-3 business days', S['td'])],
        [Paragraph('Europe / Germany (Berlin)', S['td_left']),
         Paragraph('4-7 business days', S['td']),
         Paragraph('2-3 business days', S['td'])],
        [Paragraph('Australia (Sydney)', S['td_left']),
         Paragraph('2-7 business days', S['td']),
         Paragraph('1-3 business days', S['td'])],
        [Paragraph('China (Wuhan) - Global', S['td_left']),
         Paragraph('7-15 business days', S['td']),
         Paragraph('3-6 business days', S['td'])],
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

    # Shipping costs
    story.append(Paragraph('<b>Shipping Costs</b>', S['contact_h']))
    story.append(Spacer(1, 6))
    story.append(Paragraph('Standard: $25 (FREE on orders $250+)', S['contact_item']))
    story.append(Paragraph('Express Priority: $50 (FREE on orders $500+)', S['contact_item']))
    story.append(Spacer(1, 16))

    # Volume discount summary
    story.append(Paragraph('<b>Volume Discount Tiers</b>', S['contact_h']))
    story.append(Spacer(1, 6))
    story.append(Paragraph('$500+  =  5% OFF entire order + FREE Express Shipping', S['contact_item']))
    story.append(Paragraph('$1,000+  =  10% OFF entire order + FREE Express Shipping', S['contact_item']))
    story.append(Paragraph('$2,500+  =  20% OFF entire order + FREE Express Shipping', S['contact_item']))
    story.append(Spacer(1, 16))

    # Payment methods
    story.append(Paragraph('<b>Accepted Payment Methods</b>', S['contact_h']))
    story.append(Spacer(1, 6))
    story.append(Paragraph('Visa, Mastercard, Apple Pay, Google Pay, PayPal', S['contact_item']))
    story.append(Paragraph('Cryptocurrency: Bitcoin, Ethereum, USDT, BSC', S['contact_item']))
    story.append(Spacer(1, 20))

    # Janoshik verification note
    note_t = Table(
        [[Paragraph(
            '<b>Independent Lab Testing:</b> All products are independently tested by Janoshik Analytical '
            'Laboratory. Purity results consistently show 99.5%+ across all product lines. Click the "Verify" '
            'links in the product tables above to view full lab reports.',
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
    text = f'sigmaaudley.site  |  Page {page_num}'
    canvas.saveState()
    canvas.setFont('Helvetica', 7)
    canvas.setFillColor(GRAY_400)
    canvas.drawCentredString(PAGE_W / 2, MARGIN - 8 * mm, text)
    canvas.restoreState()


# ── Main ───────────────────────────────────────────────────────────
def main():
    data = load_data()
    output_path = os.path.join(os.path.dirname(__file__), 'pricelist.pdf')

    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        topMargin=MARGIN,
        bottomMargin=MARGIN + 5 * mm,
        leftMargin=MARGIN,
        rightMargin=MARGIN,
        title='Sigma Audley - Complete Price List',
        author='Sigma Audley',
    )

    story = []

    # Page 1: Cover
    build_cover(story, data)

    # Pages 2+: Product tables by category
    build_product_pages(story, data)

    # Last page: Contact info
    build_contact_page(story, data)

    doc.build(story, onFirstPage=add_page_number, onLaterPages=add_page_number)
    print(f'PDF generated: {output_path}')
    print(f'Products: {data["total_products"]} | Janoshik links: {data["total_janoshik"]}')


if __name__ == '__main__':
    main()
