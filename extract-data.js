/**
 * Extract productsData from index.html → pricelist-data.json
 * Usage: node extract-data.js
 */
const fs = require('fs');
const path = require('path');
const vm = require('vm');

const html = fs.readFileSync(path.join(__dirname, 'index.html'), 'utf-8');

// Find the productsData block — starts with "const productsData = {" and we need to find the matching closing brace
const startMarker = 'const productsData = {';
const startIdx = html.indexOf(startMarker);
if (startIdx === -1) {
    console.error('Could not find productsData in index.html');
    process.exit(1);
}

// Find matching closing brace by counting braces
let braceCount = 0;
let inString = false;
let escapeNext = false;
let objStart = html.indexOf('{', startIdx);
let objEnd = -1;

for (let i = objStart; i < html.length; i++) {
    const ch = html[i];
    if (escapeNext) { escapeNext = false; continue; }
    if (ch === '\\' && inString) { escapeNext = true; continue; }
    if (ch === '"' && !escapeNext) { inString = !inString; continue; }
    if (inString) continue;
    // Skip single-line comments
    if (ch === '/' && html[i + 1] === '/') {
        const nlIdx = html.indexOf('\n', i);
        if (nlIdx !== -1) i = nlIdx;
        continue;
    }
    if (ch === '{') braceCount++;
    if (ch === '}') {
        braceCount--;
        if (braceCount === 0) { objEnd = i; break; }
    }
}

if (objEnd === -1) {
    console.error('Could not find end of productsData object');
    process.exit(1);
}

const jsCode = 'var productsData = ' + html.substring(objStart, objEnd + 1) + ';';

const sandbox = {};
vm.createContext(sandbox);
vm.runInContext(jsCode, sandbox);

const data = sandbox.productsData;

// Flatten: iterate category → subcategory → products
const categoryOrder = ['peptides', 'oral_tablets', 'injectable_oils', 'specialty_injections', 'raw_materials'];
const output = {
    company_info: data.company_info,
    categories: []
};

for (const catKey of categoryOrder) {
    const catData = data[catKey];
    if (!catData) continue;

    const category = {
        key: catKey,
        description: catData.description || catKey,
        subcategories: []
    };

    for (const [subKey, subData] of Object.entries(catData)) {
        if (subKey === 'description') continue;
        if (!subData || !subData.products) continue;

        category.subcategories.push({
            key: subKey,
            description: subData.description || subKey,
            products: subData.products.map(p => ({
                cat_no: p.cat_no,
                name: p.name,
                specification: p.specification || '',
                janoshik_url: (p.janoshik_url && p.janoshik_url !== '#') ? p.janoshik_url : null,
                pricing: p.pricing,
                popular: !!p.popular,
                new: !!p.new,
                best_value: !!p.best_value,
                contact_pricing: !!p.contact_pricing
            }))
        });
    }

    output.categories.push(category);
}

// Count totals
let totalProducts = 0;
let totalJanoshik = 0;
for (const cat of output.categories) {
    for (const sub of cat.subcategories) {
        totalProducts += sub.products.length;
        totalJanoshik += sub.products.filter(p => p.janoshik_url).length;
    }
}
output.total_products = totalProducts;
output.total_janoshik = totalJanoshik;

const outPath = path.join(__dirname, 'pricelist-data.json');
fs.writeFileSync(outPath, JSON.stringify(output, null, 2));
console.log(`Extracted ${totalProducts} products (${totalJanoshik} with Janoshik links) → ${outPath}`);
