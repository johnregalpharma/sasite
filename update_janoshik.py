#!/usr/bin/env python3
"""
Script to update janoshikMapping blocks and janoshik_url fields in HTML files and JSON.
Reads the new mapping from new_mapping.js and applies it to:
  - index.html, products.html, product.html (janoshikMapping block + productsData janoshik_url)
  - pricelist-data.json (janoshik_url fields)
"""

import re
import json
import os

BASE_DIR = r"C:\Users\kazam\Downloads\sasite"

def read_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

def write_file(path, content):
    with open(path, 'w', encoding='utf-8', newline='\n') as f:
        f.write(content)

# Step 1: Read the new mapping file and parse the cat_no -> URL mapping
new_mapping_path = os.path.join(BASE_DIR, "new_mapping.js")
new_mapping_raw = read_file(new_mapping_path)

# Parse the mapping: extract key-value pairs from the JS object
# Pattern matches: 'KEY': 'URL'
mapping = {}
for match in re.finditer(r"'([^']+)'\s*:\s*'([^']+)'", new_mapping_raw):
    cat_no = match.group(1)
    url = match.group(2)
    mapping[cat_no] = url

print(f"Loaded {len(mapping)} entries from new_mapping.js")

# Step 2: Process each HTML file
html_files = ["index.html", "products.html", "product.html"]

for html_file in html_files:
    filepath = os.path.join(BASE_DIR, html_file)
    content = read_file(filepath)
    original_len = len(content)

    # 2a: Replace the entire janoshikMapping block
    # The block starts with "const janoshikMapping = {" and ends with "};"
    # We need to match from "const janoshikMapping = {" to the closing "};"
    # being careful to match the right closing brace (the one at the same indentation)
    pattern = r'([ \t]*)const janoshikMapping = \{[^}]*?\n\1\};'

    # Use re.DOTALL to match across lines
    match = re.search(r'const janoshikMapping = \{', content)
    if match:
        start_pos = match.start()
        # Find the closing }; - we need to find the matching one
        # The mapping block has entries like 'key': 'value' and ends with a line that is just whitespace + };
        # Find the indentation of the const declaration
        line_start = content.rfind('\n', 0, start_pos) + 1
        indent = content[line_start:start_pos]

        # Now find the closing }; at the same indentation level
        # Search for \n<indent>}; pattern after the opening
        close_pattern = '\n' + indent + '};'
        close_pos = content.find(close_pattern, start_pos)
        if close_pos >= 0:
            end_pos = close_pos + len(close_pattern)
            old_block = content[start_pos:end_pos]
            # The new_mapping_raw already has the correct format with indentation
            new_block = new_mapping_raw.rstrip()  # Remove trailing whitespace
            content = content[:start_pos] + new_block + content[end_pos:]
            print(f"  [{html_file}] Replaced janoshikMapping block ({len(old_block)} chars -> {len(new_block)} chars)")
        else:
            print(f"  [{html_file}] WARNING: Could not find closing }}; for janoshikMapping")
    else:
        print(f"  [{html_file}] WARNING: Could not find janoshikMapping block")

    # 2b: Update all janoshik_url fields in productsData
    # Pattern: "cat_no": "XXXX" ... "janoshik_url": "old_url"
    # We need to find each cat_no and its associated janoshik_url

    url_update_count = 0
    url_skip_count = 0

    # Strategy: find each "cat_no": "XXX" and then the nearest following "janoshik_url": "..."
    # and replace the URL if the cat_no is in our mapping
    cat_no_pattern = re.compile(r'"cat_no"\s*:\s*"([^"]+)"')
    janoshik_url_pattern = re.compile(r'("janoshik_url"\s*:\s*")([^"]+)(")')

    # Find all cat_no positions
    cat_nos_found = list(cat_no_pattern.finditer(content))

    # For each cat_no, find the next janoshik_url after it and replace
    # Process in reverse order so positions don't shift
    for cat_match in reversed(cat_nos_found):
        cat_no = cat_match.group(1)
        if cat_no in mapping:
            # Find the next janoshik_url after this cat_no
            search_start = cat_match.end()
            # Look within a reasonable window (next 2000 chars should be enough for one product entry)
            search_end = min(search_start + 2000, len(content))
            url_match = janoshik_url_pattern.search(content, search_start, search_end)
            if url_match:
                old_url = url_match.group(2)
                new_url = mapping[cat_no]
                if old_url != new_url:
                    content = content[:url_match.start(2)] + new_url + content[url_match.end(2):]
                    url_update_count += 1
                else:
                    url_skip_count += 1
            else:
                # Some products might not have janoshik_url
                pass
        else:
            url_skip_count += 1

    print(f"  [{html_file}] Updated {url_update_count} janoshik_url values, skipped {url_skip_count}")

    write_file(filepath, content)
    print(f"  [{html_file}] Written ({original_len} -> {len(content)} chars)")

# Step 3: Process pricelist-data.json
json_path = os.path.join(BASE_DIR, "pricelist-data.json")
json_content = read_file(json_path)
json_data = json.loads(json_content)

json_update_count = 0
json_skip_count = 0

def update_products_in_json(obj):
    """Recursively walk the JSON structure and update janoshik_url based on cat_no."""
    global json_update_count, json_skip_count

    if isinstance(obj, dict):
        # If this dict has both cat_no and janoshik_url, update
        if "cat_no" in obj and "janoshik_url" in obj:
            cat_no = obj["cat_no"]
            if cat_no in mapping:
                old_url = obj["janoshik_url"]
                new_url = mapping[cat_no]
                if old_url != new_url:
                    obj["janoshik_url"] = new_url
                    json_update_count += 1
                else:
                    json_skip_count += 1
            else:
                json_skip_count += 1
        # Recurse into values
        for v in obj.values():
            update_products_in_json(v)
    elif isinstance(obj, list):
        for item in obj:
            update_products_in_json(item)

update_products_in_json(json_data)

# Write back with same formatting (2 spaces indent)
json_output = json.dumps(json_data, indent=2, ensure_ascii=False)
write_file(json_path, json_output + '\n')

print(f"  [pricelist-data.json] Updated {json_update_count} janoshik_url values, skipped {json_skip_count}")
print(f"  [pricelist-data.json] Written")

print("\nAll done!")
