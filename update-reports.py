"""
Replace reportVerifyLinks in test-reports.html with the authoritative 315
Sigma Audley reports from all-janoshik-reports.md (lines 400-718).
"""
import re
import os

SASITE = os.path.dirname(__file__) or '.'
MD_PATH = os.path.join(os.path.expanduser("~"), "Downloads", "wwb-website", "all-janoshik-reports.md")

# ── 1. Parse all 315 Sigma Audley reports ────────────────────────
with open(MD_PATH, "r", encoding="utf-8") as f:
    md = f.read()

sa_start = md.index("## Sigma Audley Reports")
sa_section = md[sa_start:]

reports = []  # list of (name, url) tuples
for line in sa_section.split("\n"):
    m = re.match(r'\|\s*\d+\s*\|\s*(.+?)\s*\|\s*\[Verify\]\((https://verify\.janoshik\.net/tests/\S+?)\)\s*\|', line)
    if m:
        report_name = m.group(1).strip()
        verify_url = m.group(2).strip()
        reports.append((report_name, verify_url))

print(f"Parsed {len(reports)} Sigma Audley reports from markdown")

# ── 2. Build new reportVerifyLinks JS object ─────────────────────
def name_to_key(name):
    """Convert report name to JS key: spaces→underscores, keep other chars."""
    return name.replace(" ", "_").replace("/", "")

lines = ['const reportVerifyLinks = {']
for i, (name, url) in enumerate(reports):
    key = name_to_key(name)
    comma = "," if i < len(reports) - 1 else ""
    lines.append(f'    "{key}": "{url}"{comma}')
lines.append('};')
new_block = "\n".join(lines)

# ── 3. Replace in test-reports.html ──────────────────────────────
tr_path = os.path.join(SASITE, "test-reports.html")
with open(tr_path, "r", encoding="utf-8") as f:
    content = f.read()

# Find the old reportVerifyLinks block
old_start = content.index("const reportVerifyLinks = {")
# Find matching closing };
brace_count = 0
i = content.index("{", old_start)
while i < len(content):
    if content[i] == "{":
        brace_count += 1
    elif content[i] == "}":
        brace_count -= 1
        if brace_count == 0:
            old_end = i + 1
            # Include the semicolon
            if old_end < len(content) and content[old_end] == ";":
                old_end += 1
            break
    i += 1

old_block = content[old_start:old_end]
old_count = old_block.count('"https://verify.janoshik.net')
print(f"Old reportVerifyLinks had {old_count} entries")

content = content[:old_start] + new_block + content[old_end:]

with open(tr_path, "w", encoding="utf-8") as f:
    f.write(content)

new_count = new_block.count('"https://verify.janoshik.net')
print(f"New reportVerifyLinks has {new_count} entries")
print(f"Updated test-reports.html")

# ── 4. Verify report images exist for all keys ──────────────────
reports_dir = os.path.join(SASITE, "reports")
missing_images = []
for name, url in reports:
    key = name_to_key(name)
    img_path = os.path.join(reports_dir, f"{key}.png")
    if not os.path.exists(img_path):
        missing_images.append(key)

if missing_images:
    print(f"\n{len(missing_images)} report images missing:")
    for k in missing_images[:20]:
        print(f"  {k}.png")
    if len(missing_images) > 20:
        print(f"  ... and {len(missing_images) - 20} more")
else:
    print(f"All {len(reports)} report images present in reports/")

# ── 5. Build a URL lookup from the markdown for cross-checking ───
md_url_lookup = {}
for name, url in reports:
    md_url_lookup[url] = name

# Check all URLs in the other HTML files match markdown
for fname in ["index.html", "products.html", "product.html"]:
    fpath = os.path.join(SASITE, fname)
    if not os.path.exists(fpath):
        continue
    with open(fpath, "r", encoding="utf-8") as f:
        html = f.read()

    verify_urls = set(re.findall(r'https://verify\.janoshik\.net/tests/[^\s"\'`,]+', html))
    matched = sum(1 for u in verify_urls if u in md_url_lookup)
    # The ACE-031 placeholder URL appears many times for products without real reports
    print(f"{fname}: {len(verify_urls)} unique verify URLs, {matched} match markdown SA reports")
