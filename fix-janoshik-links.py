"""
Cross-reference Janoshik links in sasite/index.html against the authoritative
all-janoshik-reports.md (Sigma Audley section) and fix all mismatches.

Strategy: Parse all janoshik.com/janoshik.net URLs from index.html,
match each to the correct Sigma Audley report from the markdown,
and do direct string replacement.
"""
import re
import os
import json

SASITE = os.path.dirname(__file__) or '.'
MD_PATH = os.path.join(os.path.expanduser("~"), "Downloads", "wwb-website", "all-janoshik-reports.md")
INDEX_PATH = os.path.join(SASITE, "index.html")
PRODUCTS_PATH = os.path.join(SASITE, "products.html")
REPORTS_PATH = os.path.join(SASITE, "test-reports.html")
PRODUCT_PATH = os.path.join(SASITE, "product.html")

# ── 1. Parse ALL Sigma Audley reports from the markdown ──────────
with open(MD_PATH, "r", encoding="utf-8") as f:
    md = f.read()

sa_start = md.index("## Sigma Audley Reports")
sa_section = md[sa_start:]

md_reports = {}  # report_name -> verify_url
for line in sa_section.split("\n"):
    m = re.match(r'\|\s*\d+\s*\|\s*(.+?)\s*\|\s*\[Verify\]\((https://verify\.janoshik\.net/tests/\S+?)\)\s*\|', line)
    if m:
        report_name = m.group(1).strip()
        verify_url = m.group(2).strip()
        md_reports[report_name] = verify_url

print(f"Parsed {len(md_reports)} Sigma Audley reports from markdown")

# ── 2. Build matching infrastructure ────────────────────────────
def normalize(name):
    """Normalize for fuzzy comparison."""
    return name.lower().replace(" ", "").replace("-", "").replace("_", "").replace("(", "").replace(")", "").replace("/", "").replace(",", "").replace("'", "").replace("+", "").replace(".", "")

# Create normalized lookup from markdown
md_by_norm = {}
for rname, url in md_reports.items():
    md_by_norm[normalize(rname)] = url

# Also index by extracting the test slug from the URL
# URL format: https://verify.janoshik.com.sigmaaudley.site/tests/51829-Test_Cypionate_250mgml_NHJNWGXP9T94
# The slug part is: Test_Cypionate_250mgml (between the ID- and the _HASH)
md_by_slug_norm = {}
for rname, url in md_reports.items():
    m = re.search(r'/tests/\d+-(.+)_[A-Z0-9]{12}$', url)
    if m:
        slug = m.group(1)
        md_by_slug_norm[normalize(slug)] = url

# ── 3. Extract all current janoshik URLs from HTML ──────────────
with open(INDEX_PATH, "r", encoding="utf-8") as f:
    html = f.read()

# Find all unique janoshik URLs (both janoshik.com and verify.janoshik.com.sigmaaudley.site)
# Match both single-quoted and double-quoted URLs
all_urls = set(re.findall(r"""https?://(?:janoshik\.com|verify\.janoshik\.net)/tests/[^"'\s,]+""", html))
print(f"Found {len(all_urls)} unique Janoshik URLs in index.html")

# ── 4. Match each current URL to the correct markdown URL ───────
url_replacements = {}  # old_url -> new_url
matched = 0
unmatched = 0

for old_url in sorted(all_urls):
    # Extract the slug from the current URL
    # janoshik.com URL format: https://janoshik.com/tests/58022-SM5semaglutide_5mg_GZY1YNSFAFPC
    # OR: https://janoshik.com/tests/64737-Test_Cyp_250mgml_Z1TGAVSXHPD7
    # verify.janoshik.com.sigmaaudley.site format: https://verify.janoshik.com.sigmaaudley.site/tests/51021-Semaglutide_5mg_7DFCK35CCQCC

    # Try to extract the product name/slug from the URL
    m = re.search(r'/tests/\d+-(.+?)_[A-Z0-9]{8,}$', old_url)
    if not m:
        # Try looser pattern
        m = re.search(r'/tests/\d+-(.+)$', old_url)

    if m:
        slug = m.group(1)
        slug_norm = normalize(slug)

        # Try to find a matching markdown URL by slug similarity
        best_match = None
        best_score = 0

        for md_norm_key, md_url in md_by_slug_norm.items():
            # Check if slugs are similar enough
            if slug_norm == md_norm_key:
                best_match = md_url
                best_score = 100
                break

            # Try partial matching - check if one contains the other
            if len(slug_norm) > 5 and len(md_norm_key) > 5:
                # Remove common prefixes like cat_no
                slug_clean = re.sub(r'^[a-z]*\d*', '', slug_norm)
                md_clean = re.sub(r'^[a-z]*\d*', '', md_norm_key)
                if slug_clean and md_clean and slug_clean == md_clean:
                    if best_score < 90:
                        best_match = md_url
                        best_score = 90

                # Check if core product name matches
                if slug_clean and md_clean:
                    if slug_clean in md_clean or md_clean in slug_clean:
                        if best_score < 70:
                            best_match = md_url
                            best_score = 70

        if best_match and old_url != best_match:
            url_replacements[old_url] = best_match
            matched += 1
        elif old_url.startswith("https://verify.janoshik.com.sigmaaudley.site/"):
            # Already a verify link, check if it matches any MD URL
            if old_url in md_reports.values():
                matched += 1  # already correct
            else:
                unmatched += 1
        else:
            unmatched += 1
    else:
        unmatched += 1

print(f"\nURL matching results:")
print(f"  Matched & need replacement: {matched}")
print(f"  Unmatched: {unmatched}")

# ── 5. Hardcoded manual corrections for tricky products ──────────
# These have very different naming between janoshik.com and verify.janoshik.com.sigmaaudley.site
MANUAL_URL_MAP = {
    'https://janoshik.com/tests/42647-XA11_clearblue_top_vial_TJKSD8YJ3I57': 'https://verify.janoshik.com.sigmaaudley.site/tests/51881-Triptorelin_Acetate_2mg_HLWG71TXM6WZ',
    'https://janoshik.com/tests/42648-TSM10_white_top_vial_1LYUSNTHET18': 'https://verify.janoshik.com.sigmaaudley.site/tests/51137-Tesamorelin_10mg_QI3Z64X4H33F',
    'https://janoshik.com/tests/42649-IP10_cleargold_top_vial_QD7QLRIFEP6J': 'https://verify.janoshik.com.sigmaaudley.site/tests/51339-Ipamorelin_10mg_XNUJVEV77E7F',
    'https://janoshik.com/tests/42650-MS10_cleargold_top_vial_I27UCAXRCDSJ': 'https://verify.janoshik.com.sigmaaudley.site/tests/51715-MOTS-c_10mg_EXECQN7URXF9',
    'https://janoshik.com/tests/44880-CJC1295_Whitout_DAC_ERNL7N1TFEPM': 'https://verify.janoshik.com.sigmaaudley.site/tests/51772-CJC-1295_Without_DAC_5mg_PYWQ0I0LFIQN',
    'https://janoshik.com/tests/58858-Dsip10_V4QWLC4Z1YY5': 'https://verify.janoshik.com.sigmaaudley.site/tests/51662-DSIP_10mg_RHAKSB45LTHW',
    'https://janoshik.com/tests/58859-CjC_dac_5_39SQGPKXIEHN': 'https://verify.janoshik.com.sigmaaudley.site/tests/51606-CJC-1295_With_DAC_5mg_AXCZGRUJACB2',
    'https://janoshik.com/tests/58860-Tesa_5_Y96Q2JHKQT7H': 'https://verify.janoshik.com.sigmaaudley.site/tests/51266-Tesamorelin_5mg_427ZZR2P58JM',
    'https://janoshik.com/tests/58861-Glow70_JU2BFDL9HNP9': 'https://verify.janoshik.com.sigmaaudley.site/tests/51927-GLOW70_(BPC-157_+_GHK-CU_+_TB500)_70mg_S2E1JFIZW1MU',
    'https://janoshik.com/tests/61134-LC120LipoC_CE7V8AY9KF2H': 'https://verify.janoshik.com.sigmaaudley.site/tests/51813-Lipo-C_120mgml_XBZJZFXVNRSQ',
    'https://janoshik.com/tests/67327-LipoB_LC216_63ZZGHE2G39P': 'https://verify.janoshik.com.sigmaaudley.site/tests/51239-Lipo-B_216mg_4JG25QWGRBKH',
    'https://janoshik.com/tests/67328-SUPER_SHRED_LC553_9R8UEH93WVNH': 'https://verify.janoshik.com.sigmaaudley.site/tests/51868-Super_Shred_L7ZGMD60UVDB',
}

# Also try slug-based matching for any remaining
for old_url in sorted(all_urls):
    if old_url in url_replacements or old_url in MANUAL_URL_MAP:
        continue
    if old_url.startswith("https://verify.janoshik.com.sigmaaudley.site/"):
        continue

    m = re.search(r'/tests/\d+-(.+?)_[A-Z0-9]{8,}$', old_url)
    if not m:
        continue
    slug = m.group(1)

    slug_clean = re.sub(r'^[A-Z]+\d+', '', slug)
    if slug_clean:
        nk = normalize(slug_clean)
        if nk in md_by_slug_norm:
            MANUAL_URL_MAP[old_url] = md_by_slug_norm[nk]

# Merge manual into replacements
for old, new in MANUAL_URL_MAP.items():
    if old not in url_replacements:
        url_replacements[old] = new

print(f"  Additional manual matches: {len(MANUAL_URL_MAP)}")
print(f"  Total replacements: {len(url_replacements)}")

# ── 6. Apply all replacements to all HTML files ─────────────────
files_to_fix = [INDEX_PATH]
for extra in [PRODUCTS_PATH, REPORTS_PATH, PRODUCT_PATH]:
    if os.path.exists(extra):
        files_to_fix.append(extra)

total_changes = 0
for filepath in files_to_fix:
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    original = content
    changes = 0
    for old_url, new_url in url_replacements.items():
        count = content.count(old_url)
        if count > 0:
            content = content.replace(old_url, new_url)
            changes += count

    if content != original:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        fname = os.path.basename(filepath)
        print(f"  {fname}: {changes} URL replacements")
        total_changes += changes

print(f"\nTotal: {total_changes} URL replacements across {len(files_to_fix)} files")

# ── 7. Show remaining unmatched URLs ────────────────────────────
remaining = []
for old_url in sorted(all_urls):
    if old_url not in url_replacements and not old_url.startswith("https://verify.janoshik.com.sigmaaudley.site/"):
        remaining.append(old_url)

if remaining:
    print(f"\n{len(remaining)} janoshik.com URLs still unmatched:")
    for u in remaining[:20]:
        m = re.search(r'/tests/\d+-(.+?)_[A-Z0-9]{8,}$', u)
        slug = m.group(1) if m else "?"
        print(f"  {slug}: {u}")
    if len(remaining) > 20:
        print(f"  ... and {len(remaining) - 20} more")
