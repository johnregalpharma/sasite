#!/usr/bin/env python3
"""
Update all WWB data files from the new _keys.txt download.

Reads the new _keys.txt (tab-separated), transforms verify URLs,
and rebuilds 4 output files + copies them to GYC location.
"""

import os
import json
import shutil

# === PATHS ===
KEYS_FILE = r"C:\Users\kazam\Downloads\drive-download-20260227T111809Z-1-001\Wuhan_Wansheng_Reports_COM\Wuhan_Wansheng_Reports\_keys.txt"

# Primary outputs
REPORT_KEYS_JS   = r"C:\Users\kazam\Downloads\wwb-website\data\reportKeys.js"
PRODUCTS_DATA_JS = r"C:\Users\kazam\Downloads\wwb-website\public\js\products-data.js"
VERIFY_URLS_JSON = r"C:\Users\kazam\Downloads\wwb-website\config\janoshik-verify-urls.json"
VERIFY_LINKS_JS  = r"C:\Users\kazam\Downloads\wwb-website\config\janoshik-verify-links.js"

# GYC copies
GYC_REPORT_KEYS_JS   = r"C:\Users\kazam\Downloads\GYC\wwb-website\data\reportKeys.js"
GYC_PRODUCTS_DATA_JS = r"C:\Users\kazam\Downloads\GYC\wwb-website\public\js\products-data.js"
GYC_VERIFY_URLS_JSON = r"C:\Users\kazam\Downloads\GYC\wwb-website\config\janoshik-verify-urls.json"
GYC_VERIFY_LINKS_JS  = r"C:\Users\kazam\Downloads\GYC\wwb-website\config\janoshik-verify-links.js"


def transform_url(url):
    """Transform verify.janoshik.com/tests/wuhan/ -> verify.janoshik.com.wuhanwansheng.net/tests/wuhan/"""
    return url.replace(
        "https://verify.janoshik.com/tests/wuhan/",
        "https://verify.janoshik.com.wuhanwansheng.net/tests/wuhan/"
    )


def read_keys(path):
    """Read _keys.txt and return list of dicts."""
    entries = []
    with open(path, "r", encoding="utf-8") as f:
        for i, line in enumerate(f):
            line = line.rstrip("\n").rstrip("\r")
            if i == 0:
                # Skip header row
                continue
            if not line.strip():
                continue
            parts = line.split("\t")
            if len(parts) < 5:
                print(f"WARNING: Line {i+1} has {len(parts)} fields, expected 5: {line!r}")
                continue
            unique_key, task_number, sample, filename, verify_url = parts[0], parts[1], parts[2], parts[3], parts[4]
            # Strip the '#' from task number
            task_num = task_number.lstrip("#")
            # Transform URL
            new_url = transform_url(verify_url)
            entries.append({
                "uniqueKey": unique_key,
                "taskNumber": task_num,
                "sample": sample,
                "filename": filename,
                "verifyUrl": new_url,
            })
    return entries


def filename_without_png(filename):
    """Remove .png extension from filename."""
    if filename.lower().endswith(".png"):
        return filename[:-4]
    return filename


def build_report_keys_js(entries):
    """Build reportKeys.js content."""
    lines = []
    lines.append("const reportKeys = [")
    for i, e in enumerate(entries):
        # Escape any quotes in sample name
        sample_escaped = e["sample"].replace("\\", "\\\\").replace('"', '\\"')
        filename_escaped = e["filename"].replace("\\", "\\\\").replace('"', '\\"')
        url_escaped = e["verifyUrl"].replace("\\", "\\\\").replace('"', '\\"')
        trailing = "," if i < len(entries) - 1 else ""
        lines.append(
            f'  {{ uniqueKey: "{e["uniqueKey"]}", taskNumber: "{e["taskNumber"]}", '
            f'sample: "{sample_escaped}", filename: "{filename_escaped}", '
            f'verifyUrl: "{url_escaped}" }}{trailing}'
        )
    lines.append("];")
    lines.append("")
    lines.append("const reportKeyMap = {};")
    lines.append("for (const r of reportKeys) {")
    lines.append("  reportKeyMap[r.uniqueKey] = r;")
    lines.append("}")
    lines.append("")
    lines.append("module.exports = { reportKeys, reportKeyMap };")
    lines.append("")
    return "\n".join(lines)


def build_verify_urls_json(entries):
    """Build janoshik-verify-urls.json content."""
    # Ordered dict by filename_without_png
    data = {}
    for e in entries:
        key = filename_without_png(e["filename"])
        data[key] = e["verifyUrl"]
    return json.dumps(data, indent=2, ensure_ascii=False)


def build_verify_links_js(entries):
    """Build janoshik-verify-links.js content."""
    lines = []
    lines.append("module.exports = {")
    for i, e in enumerate(entries):
        key = filename_without_png(e["filename"])
        trailing = "," if i < len(entries) - 1 else ""
        lines.append(f'  "{key}": "{e["verifyUrl"]}"{trailing}')
    lines.append("};")
    lines.append("")
    return "\n".join(lines)


def build_janoshik_verify_links_block(entries):
    """Build the janoshikVerifyLinks var block for products-data.js."""
    lines = []
    lines.append("var janoshikVerifyLinks = {")
    for i, e in enumerate(entries):
        key = filename_without_png(e["filename"])
        trailing = "," if i < len(entries) - 1 else ""
        lines.append(f'  "{key}": "{e["verifyUrl"]}"{trailing}')
    lines.append("};")
    return "\n".join(lines)


def update_products_data_js(path, entries):
    """Update the janoshikVerifyLinks block in products-data.js, preserving everything else."""
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    # Find the start of 'var janoshikVerifyLinks = {'
    start_marker = "var janoshikVerifyLinks = {"
    start_idx = content.find(start_marker)
    if start_idx == -1:
        raise ValueError(f"Could not find '{start_marker}' in {path}")

    # Find the closing '};' for this block
    # We need the first '};\n' after the start
    end_marker = "};"
    search_from = start_idx + len(start_marker)
    end_idx = content.find(end_marker, search_from)
    if end_idx == -1:
        raise ValueError(f"Could not find closing '}}; ' for janoshikVerifyLinks in {path}")
    end_idx += len(end_marker)  # include the '};'

    # Build new block
    new_block = build_janoshik_verify_links_block(entries)

    # Replace
    new_content = content[:start_idx] + new_block + content[end_idx:]
    return new_content


def write_file(path, content):
    """Write content to file."""
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(content)
    print(f"  Written: {path} ({len(content):,} bytes)")


def main():
    print("=" * 60)
    print("WWB Data Files Updater")
    print("=" * 60)

    # 1. Read new keys
    print(f"\n[1] Reading keys from: {KEYS_FILE}")
    entries = read_keys(KEYS_FILE)
    print(f"    Found {len(entries)} entries (excluding header)")

    # 2. Build reportKeys.js
    print("\n[2] Building reportKeys.js...")
    report_keys_content = build_report_keys_js(entries)
    write_file(REPORT_KEYS_JS, report_keys_content)

    # 3. Update products-data.js (janoshikVerifyLinks block only)
    print("\n[3] Updating products-data.js (janoshikVerifyLinks block)...")
    products_data_content = update_products_data_js(PRODUCTS_DATA_JS, entries)
    write_file(PRODUCTS_DATA_JS, products_data_content)

    # 4. Build janoshik-verify-urls.json
    print("\n[4] Building janoshik-verify-urls.json...")
    verify_urls_content = build_verify_urls_json(entries)
    write_file(VERIFY_URLS_JSON, verify_urls_content)

    # 5. Build janoshik-verify-links.js
    print("\n[5] Building janoshik-verify-links.js...")
    verify_links_content = build_verify_links_js(entries)
    write_file(VERIFY_LINKS_JS, verify_links_content)

    # 6. Copy all 4 files to GYC location
    print("\n[6] Copying files to GYC/wwb-website...")
    copies = [
        (REPORT_KEYS_JS,   GYC_REPORT_KEYS_JS),
        (PRODUCTS_DATA_JS, GYC_PRODUCTS_DATA_JS),
        (VERIFY_URLS_JSON, GYC_VERIFY_URLS_JSON),
        (VERIFY_LINKS_JS,  GYC_VERIFY_LINKS_JS),
    ]
    for src, dst in copies:
        shutil.copy2(src, dst)
        print(f"  Copied: {os.path.basename(src)} -> {dst}")

    # 7. Verification summary
    print("\n" + "=" * 60)
    print("VERIFICATION")
    print("=" * 60)
    print(f"\nTotal entries in _keys.txt: {len(entries)}")

    # Count lines in each output
    for label, path in [
        ("reportKeys.js", REPORT_KEYS_JS),
        ("products-data.js", PRODUCTS_DATA_JS),
        ("janoshik-verify-urls.json", VERIFY_URLS_JSON),
        ("janoshik-verify-links.js", VERIFY_LINKS_JS),
    ]:
        with open(path, "r", encoding="utf-8") as f:
            line_count = sum(1 for _ in f)
        file_size = os.path.getsize(path)
        print(f"  {label}: {line_count} lines, {file_size:,} bytes")

    # Verify GYC copies match
    print("\nGYC copy verification:")
    all_match = True
    for src, dst in copies:
        src_size = os.path.getsize(src)
        dst_size = os.path.getsize(dst)
        match = src_size == dst_size
        status = "OK" if match else "MISMATCH"
        print(f"  {os.path.basename(src)}: src={src_size:,} dst={dst_size:,} [{status}]")
        if not match:
            all_match = False

    if all_match:
        print("\nAll files updated and copies verified successfully!")
    else:
        print("\nWARNING: Some GYC copies do not match source files!")

    # Show first and last entry as sanity check
    print(f"\nFirst entry: {entries[0]['uniqueKey']} -> {entries[0]['sample']}")
    print(f"Last entry:  {entries[-1]['uniqueKey']} -> {entries[-1]['sample']}")
    print(f"First URL:   {entries[0]['verifyUrl']}")


if __name__ == "__main__":
    main()
