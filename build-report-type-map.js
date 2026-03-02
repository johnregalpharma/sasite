#!/usr/bin/env node
/**
 * Build report-type-map.json from _keys.txt files.
 * Sasite version: uses baseName as map key (no catNo mapping).
 *
 * Usage: node build-report-type-map.js [keys-base-dir]
 */

const fs = require('fs');
const path = require('path');
const crypto = require('crypto');

const typeMap = {
    'sterility': 'Sterility',
    'endotoxin': 'Endotoxin',
    'heavy-metals': 'Heavy_Metal'
};

const keysBaseDir = process.argv[2];
const keysData = {};

if (keysBaseDir && fs.existsSync(keysBaseDir)) {
    console.log(`Reading _keys.txt files from: ${keysBaseDir}`);
    for (const [type, folder] of Object.entries(typeMap)) {
        const keysFile = path.join(keysBaseDir, folder, '_keys.txt');
        if (fs.existsSync(keysFile)) {
            keysData[type] = {};
            const raw = fs.readFileSync(keysFile, 'utf-8');
            const lines = raw.split('\n').filter(l => l.trim() && !l.startsWith('UNIQUE_KEY'));
            for (const line of lines) {
                const parts = line.split('\t');
                if (parts.length < 5) continue;
                const uniqueKey = parts[0].trim();
                const taskNumber = parts[1].trim().replace('#', '');
                const filename = parts[3].trim();
                const verifyUrl = parts[4].trim();
                const baseName = filename.replace('.png', '');
                keysData[type][baseName] = { verifyUrl, uniqueKey, taskNumber };
            }
            console.log(`  ${type}: ${Object.keys(keysData[type]).length} keys loaded`);
        }
    }
}

const reportTypeMap = {};

for (const [type, folder] of Object.entries(typeMap)) {
    reportTypeMap[type] = {};
    const dir = path.join(__dirname, 'reports', type);

    try {
        const files = fs.readdirSync(dir).filter(f => f.endsWith('.png'));
        console.log(`Scanning ${type}: ${files.length} PNGs found`);

        for (const file of files) {
            const baseName = file.replace('.png', '');

            let verifyUrl, uniqueKey, taskNumber;
            if (keysData[type] && keysData[type][baseName]) {
                const kd = keysData[type][baseName];
                taskNumber = kd.taskNumber;
                // Derive a unique 12-char key per type from original key + type
                uniqueKey = crypto.createHash('md5').update(kd.uniqueKey + ':' + type).digest('hex').slice(0, 12).toUpperCase();
                // Build new verify URL with type-specific key
                const baseUrl = kd.verifyUrl.replace(/_[A-Z0-9]{12}$/, '');
                verifyUrl = baseUrl + '_' + uniqueKey;
            } else {
                uniqueKey = crypto.createHash('md5').update(type + ':' + file).digest('hex').slice(0, 12).toUpperCase();
                const meta = { sterility: 'ST', endotoxin: 'EN', 'heavy-metals': 'HM' };
                taskNumber = (meta[type] || 'XX') + '-' + baseName;
                verifyUrl = '';
            }

            reportTypeMap[type][baseName] = {
                filename: file,
                verifyUrl,
                uniqueKey,
                taskNumber
            };
        }
    } catch (e) {
        console.log(`Warning: Could not scan ${type} directory: ${e.message}`);
    }
}

const outputPath = path.join(__dirname, 'data', 'report-type-map.json');
fs.writeFileSync(outputPath, JSON.stringify(reportTypeMap, null, 2) + '\n');

let total = 0;
for (const type of Object.keys(reportTypeMap)) {
    const count = Object.keys(reportTypeMap[type]).length;
    total += count;
    console.log(`  ${type}: ${count} mapped entries`);
}
console.log(`\nWritten ${total} total entries to data/report-type-map.json`);
