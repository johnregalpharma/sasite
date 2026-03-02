const path = require('path');
const fs = require('fs');
const { reportKeyMap, reportTypeFiles } = require('../../data/reportKeys');

// Load product data - new_mapping.js doesn't use module.exports, so we eval it
let janoshikMapping = {};
try {
    const mappingContent = fs.readFileSync(path.join(__dirname, '..', '..', 'new_mapping.js'), 'utf8');
    const match = mappingContent.match(/const\s+janoshikMapping\s*=\s*(\{[\s\S]*?\});/);
    if (match) {
        janoshikMapping = eval('(' + match[1] + ')');
    }
} catch(e) {}

module.exports = (req, res) => {
    const catNo = req.query.catNo || '';
    if (!catNo) {
        res.writeHead(302, { Location: '/' });
        res.end();
        return;
    }

    // Build purity data from janoshikMapping
    let purity = null;
    const verifyUrl = janoshikMapping[catNo] || null;
    if (verifyUrl) {
        // Extract filename from verify URL: .../tests/sigma/{taskNumber}-{filename}_{key}
        const parts = verifyUrl.split('/').pop(); // e.g. "51979-Semaglutide_5mg_7E02EMC1VLU3"
        const lastUnderscore = parts.lastIndexOf('_');
        const withoutKey = parts.substring(parts.indexOf('-') + 1, lastUnderscore);
        purity = { filename: withoutKey + '.png', verifyUrl };
    }

    // Build sterility/endotoxin/heavy-metals data
    // For SA site, reportTypeFiles is keyed by baseName (filename without .png)
    // We need to find the matching report - check if any file in the type matches
    let sterility = null, endotoxin = null, heavyMetals = null;
    if (purity) {
        const baseName = purity.filename.replace('.png', '');
        sterility = (reportTypeFiles && reportTypeFiles.sterility && reportTypeFiles.sterility[baseName]) || null;
        endotoxin = (reportTypeFiles && reportTypeFiles.endotoxin && reportTypeFiles.endotoxin[baseName]) || null;
        heavyMetals = (reportTypeFiles && reportTypeFiles['heavy-metals'] && reportTypeFiles['heavy-metals'][baseName]) || null;
    }

    const productName = catNo; // SA doesn't have full product data server-side easily

    const html = `<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>${catNo} Test Reports | Sigma Audley</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        *, *::before, *::after { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; color: #171717; background: #fafafa; }
        .container { max-width: 1200px; margin: 0 auto; padding: 0 1.5rem; }
        .rd-hero { background: linear-gradient(160deg, #fff 0%, #eff6ff 40%, #dbeafe 100%); padding: 1.5rem 0; border-bottom: 1px solid rgba(0,0,0,0.06); }
        .rd-breadcrumb { display: flex; align-items: center; gap: 0.5rem; font-size: 0.8125rem; color: #737373; margin-bottom: 1rem; }
        .rd-breadcrumb a { color: #1e40af; text-decoration: none; font-weight: 500; }
        .rd-breadcrumb a:hover { text-decoration: underline; }
        .rd-breadcrumb i { font-size: 0.625rem; color: #a3a3a3; }
        .rd-product-header h1 { font-size: 1.75rem; font-weight: 800; letter-spacing: -0.02em; }
        .rd-grid-section { padding: 2rem 0 3rem; }
        .rd-grid-title { font-size: 1.125rem; font-weight: 700; margin-bottom: 1.25rem; display: flex; align-items: center; gap: 0.5rem; }
        .rd-grid-title i { color: #1e40af; }
        .rd-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 1.25rem; }
        .rd-card { background: #fff; border: 1px solid #e5e5e5; border-radius: 0.75rem; overflow: hidden; transition: all 0.2s; }
        .rd-card:hover { border-color: #1e40af; box-shadow: 0 2px 8px -2px rgb(0 0 0 / 0.08); }
        .rd-card-header { display: flex; align-items: center; gap: 0.75rem; padding: 1rem 1.25rem; border-bottom: 1px solid rgba(0,0,0,0.06); }
        .rd-card-icon { width: 40px; height: 40px; border-radius: 10px; display: flex; align-items: center; justify-content: center; font-size: 1.125rem; flex-shrink: 0; }
        .rd-card-icon.purity { background: linear-gradient(135deg, #f0fdfa, #ccfbf1); color: #0d9488; }
        .rd-card-icon.sterility { background: linear-gradient(135deg, #eff6ff, #dbeafe); color: #2563eb; }
        .rd-card-icon.endotoxin { background: linear-gradient(135deg, #fffbeb, #fef3c7); color: #d97706; }
        .rd-card-icon.heavy-metals { background: linear-gradient(135deg, #faf5ff, #f3e8ff); color: #9333ea; }
        .rd-card-title { font-size: 0.9375rem; font-weight: 700; }
        .rd-card-subtitle { font-size: 0.75rem; color: #737373; margin-top: 0.125rem; }
        .rd-card-status { margin-left: auto; font-size: 0.6875rem; font-weight: 600; padding: 0.2rem 0.625rem; border-radius: 999px; }
        .rd-card-status.available { background: #ecfdf5; color: #065f46; }
        .rd-card-status.coming-soon { background: #f5f5f5; color: #737373; }
        .rd-card-body { padding: 1.25rem; }
        .rd-report-preview { display: flex; gap: 1rem; align-items: flex-start; }
        .rd-report-thumb { width: 120px; flex-shrink: 0; border: 2px solid #e5e5e5; border-radius: 0.5rem; overflow: hidden; cursor: pointer; transition: all 0.2s; }
        .rd-report-thumb:hover { border-color: #1e40af; transform: scale(1.02); }
        .rd-report-thumb img { width: 100%; height: auto; display: block; }
        .rd-report-actions { display: flex; flex-direction: column; gap: 0.5rem; flex: 1; }
        .rd-action-btn { display: inline-flex; align-items: center; gap: 0.5rem; padding: 0.5rem 0.875rem; border-radius: 0.5rem; font-size: 0.8125rem; font-weight: 600; text-decoration: none; transition: all 0.2s; cursor: pointer; border: none; font-family: inherit; }
        .rd-action-btn.primary { background: #1e40af; color: #fff; }
        .rd-action-btn.primary:hover { background: #1e3a8a; }
        .rd-action-btn.secondary { background: #fff; color: #1e40af; border: 1px solid #dbeafe; }
        .rd-action-btn.secondary:hover { border-color: #1e40af; background: #eff6ff; }
        .rd-coming-soon { text-align: center; padding: 2rem 1rem; color: #a3a3a3; }
        .rd-coming-soon i { font-size: 2rem; margin-bottom: 0.75rem; display: block; }
        .rd-coming-soon p { font-size: 0.875rem; font-weight: 500; }
        .rd-coming-soon small { font-size: 0.75rem; display: block; margin-top: 0.25rem; }
        .rd-nav { padding: 1.5rem 0; background: #fff; border-top: 1px solid rgba(0,0,0,0.06); }
        .rd-nav-inner { display: flex; align-items: center; justify-content: space-between; gap: 1rem; flex-wrap: wrap; }
        .rd-nav-link { display: inline-flex; align-items: center; gap: 0.5rem; font-size: 0.875rem; font-weight: 600; color: #1e40af; text-decoration: none; }
        .rd-nav-link:hover { text-decoration: underline; }
        @media (max-width: 767px) { .rd-grid { grid-template-columns: 1fr; } .rd-product-header h1 { font-size: 1.375rem; } .rd-report-preview { flex-direction: column; } .rd-report-thumb { width: 100%; max-width: 200px; } }
    </style>
</head>
<body>
    <section class="rd-hero">
        <div class="container">
            <div class="rd-breadcrumb">
                <a href="/">Home</a><i class="fas fa-chevron-right"></i>
                <span>Reports: ${catNo}</span>
            </div>
            <div class="rd-product-header"><h1>${catNo} Test Reports</h1></div>
        </div>
    </section>
    <section class="rd-grid-section">
        <div class="container">
            <div class="rd-grid-title"><i class="fas fa-clipboard-list"></i> Test Reports</div>
            <div class="rd-grid">
                ${buildCard('Purity (HPLC)', 'High-Performance Liquid Chromatography', 'fa-flask', 'purity', purity, '')}
                ${buildCard('Sterility', 'Microbial Contamination Testing', 'fa-shield-virus', 'sterility', sterility, 'sterility/')}
                ${buildCard('Endotoxin', 'LAL Endotoxin Assay', 'fa-bacteria', 'endotoxin', endotoxin, 'endotoxin/')}
                ${buildCard('Heavy Metals', 'ICP-MS Heavy Metals Screening', 'fa-atom', 'heavy-metals', heavyMetals, 'heavy-metals/')}
            </div>
        </div>
    </section>
    <section class="rd-nav">
        <div class="container">
            <div class="rd-nav-inner">
                <a href="/" class="rd-nav-link"><i class="fas fa-arrow-left"></i> Back to Home</a>
            </div>
        </div>
    </section>
</body>
</html>`;

    res.setHeader('Content-Type', 'text/html; charset=utf-8');
    res.end(html);
};

function buildCard(title, subtitle, icon, cssClass, data, pathPrefix) {
    const status = data ? '<span class="rd-card-status available"><i class="fas fa-check-circle"></i> Available</span>' : '<span class="rd-card-status coming-soon">Coming Soon</span>';
    let body;
    if (data) {
        body = `<div class="rd-report-preview">
            <div class="rd-report-thumb"><img src="/reports/${pathPrefix}${data.filename}" alt="${title} Report" loading="lazy"></div>
            <div class="rd-report-actions">
                <a href="/reports/${pathPrefix}${data.filename}" target="_blank" class="rd-action-btn primary"><i class="fas fa-search-plus"></i> View Full Report</a>
                ${data.verifyUrl ? '<a href="' + data.verifyUrl + '" target="_blank" rel="noopener" class="rd-action-btn secondary"><i class="fas fa-external-link-alt"></i> Verify on Janoshik</a>' : ''}
            </div>
        </div>`;
    } else {
        body = `<div class="rd-coming-soon"><i class="fas ${icon}"></i><p>${title} report coming soon</p><small>Report will be available once testing is complete</small></div>`;
    }
    return `<div class="rd-card">
        <div class="rd-card-header">
            <div class="rd-card-icon ${cssClass}"><i class="fas ${icon}"></i></div>
            <div><div class="rd-card-title">${title}</div><div class="rd-card-subtitle">${subtitle}</div></div>
            ${status}
        </div>
        <div class="rd-card-body">${body}</div>
    </div>`;
}
