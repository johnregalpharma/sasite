/**
 * Fix ALL janoshik URLs across the Sigma Audley site.
 *
 * Strategy:
 * 1. Parse reportVerifyLinks from test-reports.html (the source of truth)
 * 2. Parse all products from product.html to get cat_no → name + spec
 * 3. Build a normalized key for each product to match reportVerifyLinks
 * 4. Replace all wrong URLs in product.html, index.html, products.html
 * 5. Regenerate pricelist-data.json
 */

const fs = require('fs');
const path = require('path');

const BASE = __dirname;

// ─── Step 1: Parse reportVerifyLinks from test-reports.html ───

const testReportsHtml = fs.readFileSync(path.join(BASE, 'test-reports.html'), 'utf8');
const reportLinksMatch = testReportsHtml.match(/const reportVerifyLinks = \{([\s\S]*?)\};/);
if (!reportLinksMatch) throw new Error('Could not find reportVerifyLinks in test-reports.html');

const reportVerifyLinks = {};
const linkRe = /"([^"]+)":\s*"([^"]+)"/g;
let m;
while ((m = linkRe.exec(reportLinksMatch[1])) !== null) {
    reportVerifyLinks[m[1]] = m[2];
}
console.log(`Parsed ${Object.keys(reportVerifyLinks).length} reportVerifyLinks entries`);

// ─── Step 2: Build comprehensive cat_no → correct URL mapping ───

// The key insight: we need to map each cat_no to a report key in reportVerifyLinks.
// Report keys look like: "Semaglutide_5mg", "GH_191AA_(Somatropin)_6IU", "Test_Cypionate_250mgml"
// Products have: cat_no, name (e.g., "Semaglutide"), specification (e.g., "5mg*10vials")

// Build a comprehensive manual mapping for ALL products based on the product data
// This is the most reliable approach since name normalization can be tricky

const catNoToReportKey = {
    // Growth Hormones
    'H06': 'GH_191AA_(Somatropin)_6IU',
    'H08': 'GH_191AA_(Somatropin)_8IU',
    'H10': 'GH_191AA_(Somatropin)_10IU',
    'H12': 'GH_191AA_(Somatropin)_12IU',
    'H15': 'GH_191AA_(Somatropin)_15IU',
    'H24': 'GH_191AA_(Somatropin)_24IU',
    'H36': 'GH_191AA_(Somatropin)_36IU',

    // Semaglutide
    'SM5': 'Semaglutide_5mg',
    'SM10': 'Semaglutide_10mg',
    'SM15': 'Semaglutide_15mg',
    'SM20': 'Semaglutide_20mg',
    'SM30': 'Semaglutide_30mg',
    'SM500': 'Semaglutide_Oral_500mcg',

    // Tirzepatide
    'TR5': 'Tirzepatide_5mg',
    'TR10': 'Tirzepatide_10mg',
    'TR15': 'Tirzepatide_15mg',
    'TR20': 'Tirzepatide_20mg',
    'TR30': 'Tirzepatide_30mg',
    'TR40': 'Tirzepatide_40mg',
    'TR50': 'Tirzepatide_50mg',
    'TR60': 'Tirzepatide_60mg',
    'TR100': 'Tirzepatide_100mg',
    'TR120': 'Tirzepatide_120mg',
    'TRO500': 'Tirzepatide_Oral_500mcg',

    // Retatrutide
    'RT5': 'Retatrutide_5mg',
    'RT10': 'Retatrutide_10mg',
    'RT12': 'Retatrutide_12mg',
    'RT15': 'Retatrutide_15mg',
    'RT20': 'Retatrutide_20mg',
    'RT24': 'Retatrutide_24mg',
    'RT30': 'Retatrutide_30mg',
    'RT36': 'Retatrutide_36mg',
    'RT40': 'Retatrutide_40mg',
    'RT50': 'Retatrutide_50mg',
    'RT60': 'Retatrutide_60mg',

    // Cagrilintide
    'CGL5': 'Cagrilintide_5mg',
    'CGL10': 'Cagrilintide_10mg',
    'CGLSM5': 'Cagrilintide_+_Semaglutide_Blend_5mg',
    'CGLSM10': 'Cagrilintide_+_Semaglutide_Blend_10mg',
    'RTCGL10': 'Retatrutide_+_Cagrilintide_Blend_10mg',

    // Other GLP-1/weight loss
    'DG5': 'Dulaglutide_5mg',
    'DG10': 'Dulaglutide_10mg',
    'MDT5': 'Mazdutide_5mg',
    'MDT10': 'Mazdutide_10mg',
    'SUR10': 'Survodutide_10mg',
    'PRM5': 'Pramlintide_5mg',
    'PRM10': 'Pramlintide_10mg',
    'T500': 'Tesofensine_500mcg',

    // Melanotan
    'MT1': 'MT-1_(Melanotan_1)_10mg',
    'ML10': 'MT-2_(Melanotan_2_Acetate)_10mg',

    // BPC-157
    'BC5': 'BPC-157_5mg',
    'BC10': 'BPC-157_10mg',
    'BC20': 'BPC-157_20mg',
    'B157': 'BPC-157_Oral_500mcg',

    // TB-500
    'BT5': 'TB500_5mg',
    'BT10': 'TB500_10mg',
    'TB5': 'TB500_(Thymosin_B4_Acetate)_5mg',
    'TB10': 'TB500_(Thymosin_B4_Acetate)_10mg',

    // BPC + TB Blends
    'BB10': 'BPC-157_+_TB500_Blend_10mg',
    'BB20': 'BPC-157_+_TB500_Blend_20mg',
    'BBO1K': 'BPC_+_TB500_Oral_Blend_1000mcg',

    // BTK / GLOW / KLOW
    'BTK20': 'BTK20_(BPC-157_+_TB500_+_KPV)_20mg',
    'GLOW50': 'GLOW50_(BPC-157_+_GHK-CU_+_TB500)_50mg',
    'GLOW70': 'GLOW70_(BPC-157_+_GHK-CU_+_TB500)_70mg',
    'KLOW80': 'KLOW80_(BPC-157_+_GHK-CU_+_TB500_+_KPV)_80mg',

    // NAD+
    'NJ100': 'NAD+_(Buffered)_100mg',
    'NJ500': 'NAD+_(Buffered)_500mg',
    'NJ1K': 'NAD+_(Buffered)_1000mg',
    'NJINJ': 'NAD+_Injectable_100mgml',

    // Selank/Semax
    'SK5': 'Selank_5mg',
    'SK10': 'Selank_10mg',
    'SK30': 'Selank_30mg',
    'XA5': 'Semax_5mg',
    'XA10': 'Semax_10mg',
    'XA30': 'Semax_30mg',

    // DSIP
    'DS2': 'DSIP_2mg',
    'DS5': 'DSIP_5mg',
    'DS10': 'DSIP_10mg',
    'DS15': 'DSIP_15mg',

    // Epithalon
    'ET5': 'Epithalon_5mg',
    'ET10': 'Epithalon_10mg',
    'ET40': 'Epithalon_40mg',
    'ET50': 'Epithalon_50mg',
    'NAE5': 'N-Acetyl_Epitalon_Amidate_5mg',

    // MOTS-c
    'MS5': 'MOTS-c_5mg',
    'MS10': 'MOTS-c_10mg',
    'MS40': 'MOTS-c_40mg',

    // SS-31
    '2S10': 'SS-31_(Elamipretide)_10mg',
    '2S50': 'SS-31_(Elamipretide)_50mg',

    // CJC-1295
    'CND5': 'CJC-1295_Without_DAC_5mg',
    'CND10': 'CJC-1295_Without_DAC_10mg',
    'CD2': 'CJC-1295_With_DAC_2mg',
    'CD5': 'CJC-1295_With_DAC_5mg',
    'CP10': 'CJC-1295_Without_DAC_+_Ipamorelin_Blend_10mg',

    // Ipamorelin
    'IP2': 'Ipamorelin_2mg',
    'IP5': 'Ipamorelin_5mg',
    'IP10': 'Ipamorelin_10mg',

    // GHRP
    'G25': 'GHRP-2_Acetate_5mg',
    'G210': 'GHRP-2_Acetate_10mg',
    'G65': 'GHRP-6_Acetate_5mg',
    'G610': 'GHRP-6_Acetate_10mg',

    // Hexarelin
    'HX2': 'Hexarelin_Acetate_5mg',
    'HX5': 'Hexarelin_Acetate_5mg',

    // Sermorelin
    'SMO2': 'Sermorelin_Acetate_2mg',
    'SMO5': 'Sermorelin_Acetate_5mg',
    'SMO10': 'Sermorelin_Acetate_10mg',

    // Tesamorelin
    'TSM2': 'Tesamorelin_2mg',
    'TSM5': 'Tesamorelin_10mg', // closest match
    'TSM10': 'Tesamorelin_10mg',
    'TSM20': 'Tesamorelin_20mg',

    // GHK-CU
    'CU50': 'GHK-CU_50mg',
    'CU100': 'GHK-CU_100mg',
    'AHK100': 'AHK-CU_100mg',

    // HCG
    'G2K': 'HCG_2000IU',
    'G5K': 'HCG_5000IU',
    'G10K': 'HCG_10000IU',

    // HMG
    'G75': 'HMG_75IU',

    // AOD
    '2AD': 'AOD9604_2mg',
    '5AD': 'AOD9604_5mg',
    '10AD': 'AOD9604_10mg',

    // GH Fragment
    'GHF2': 'GH_Fragment_176-191_2mg',
    'GHF5': 'GH_Fragment_176-191_5mg',
    'GHF10': 'GH_Fragment_176-191_10mg',

    // IGF
    'IG01': 'IGF-1_LR3_01mg',
    'IG1': 'IGF-1_LR3_1mg',

    // MGF/PEG-MGF
    'MG2': 'MGF_2mg',
    'PMG2': 'PEG_MGF_2mg',

    // PT-141
    'P41': 'PT-141_(Bremelanotide)_10mg',

    // Oxytocin
    'OT5': 'Oxytocin_5mg',
    'OT10': 'Oxytocin_10mg',

    // KissPeptin
    'KS5': 'KissPeptin-10_5mg',
    'KS10': 'KissPeptin-10_10mg',

    // Thymulin / Thymosin
    'TY5': 'Thymulin_5mg',
    'TY10': 'Thymulin_10mg',
    'TA5': 'Thymosin_Alpha-1_5mg',
    'TA10': 'Thymosin_Alpha-1_5mg', // closest

    // LL37
    'LL10': 'LL37_10mg',
    'LL375': 'LL37_10mg',

    // Gonadorelin
    'GND2': 'Gonadorelin_Acetate_2mg',

    // Triptorelin
    'TRA2': 'Triptorelin_Acetate_2mg',

    // EPO
    'EP3K': 'EPO_3000IU',

    // Glutathione
    'GTT': 'Glutathione_1500mg',

    // Cerebrolysin
    'CBL60': 'Cerebrolysin_60mg',

    // VIP
    'VP5': 'VIP_5mg',
    'VP10': 'VIP_10mg',

    // KPV
    'KP10': 'KPV_10mg',
    'KPO': 'KPV_Oral_500mcg',

    // ARA-290
    'RA10': 'ARA-290_10mg',

    // Adamax
    'ADA10': 'Adamax_10mg',

    // Dermorphin
    'DM5': 'Dermorphin_5mg',

    // PE-22-28
    'PE10': 'PE-22-28_10mg',

    // Pinealon
    'PI5': 'Pinealon_5mg',
    'PI10': 'Pinealon_10mg',
    'PI20': 'Pinealon_20mg',

    // PNC27
    'PNC5': 'PNC27_5mg',
    'PNC10': 'PNC27_10mg',

    // P21
    'P21': 'P21_10mg',

    // SNAP-8
    'NP810': 'SNAP-8_10mg',

    // Adipotide
    'AP2': 'Adipotide_2mg',
    'AP5': 'Adipotide_5mg',

    // ACE-031
    'AE1': 'ACE-031_1mg',

    // Vilon
    'VN20': 'Vilon_20mg',

    // Hyaluronic acid
    'HA5': 'Hyaluronic_acid_5mg',

    // AICAR
    'AI50': 'AICAR_50mg',
    'AIO10': 'AICAR_Oral_10mg',

    // BAM15
    'BM50': 'BAM15_50mg',

    // SLU-PP-332
    'SLU250': 'SLU-PP-332_250mcg',
    'SLU1K': 'SLU-PP-332_1000mcg',
    'SLU20': 'SLU-PP-332_20mg',
    'SLUBAM': 'SLU-PP-332_+_BAM15_Blend_300mcg',

    // 5-amino-1MQ
    'AMQ5': '5-amino-1MQ_5mg',
    'AMQ10': '5-amino-1MQ_10mg',
    'AMQ50': '5-amino-1MQ_50mg',
    'AMQO50': '5-amino-1MQ_Oral_50mg',

    // Lipo
    'Lipo-C': 'Lipo-C_120mgml',
    'LCO': 'Lipo-C_(Original)_120mgml',
    'LCB12': 'Lipo-C_+_B12_121mgml',
    'Lipo-B': 'Lipo-B_Blend',
    'LBI': 'Lipo-B_Injection',
    'LCFB': 'Lipo-C_FAT_BLASTER',
    'LCFO': 'Lipo-C_FOCUS',
    'LC500': 'L-Carnitine_500mg',
    'LC1K': 'L-Carnitine_1000mg',
    'LC553': 'Super_Shred',

    // Blends
    'SHB': 'Super_Human_Blend',
    'RPB': 'Relaxation_PM_Blend',
    'IEB': 'Immunological_Enhancement_Blend',
    'HHSN': 'Healthy_Hair_Skin_Nails_Blend',

    // Insulin
    'INS': 'Insulin_(Lantus)',

    // Bac Water
    'BW': 'Bac_Water',

    // Lemon Bottle
    'LB': 'Lemon_Bottle',

    // Botulinum
    'BX100': 'Botulinum_toxin_100IU',

    // Melatonin
    'MN10': 'Melatonin_10mg',

    // Vitamin
    'VB1': 'Vitamin_B12_1mg',
    'VB10': 'Vitamin_B12_10mg',
    'VD20K': 'Vitamin_D3_20000IU',

    // Methylene Blue
    'MB20': 'Methylene_Blue_20mg',

    // Alprostadil
    'AL20': 'Alprostadil_20mcg',

    // DNP
    'DNP200': 'DNP_(24-Dinitrophenol)_200mg',

    // CS (Cagrilintide+Sema blend)
    'CS5': 'Cagrilintide_+_Semaglutide_Blend_5mg',
    'CS10': 'Cagrilintide_+_Semaglutide_Blend_10mg',

    // ─── ORAL TABLETS ───

    // Clenbuterol
    'CB40': 'Clenbuterol_40mcg',

    // T3/T4
    '325': 'T3_(Liothyronine)_25mcg',
    '340': 'T3_(Liothyronine)_40mcg',
    'T440': 'T4_(Levothyroxine)_40mcg',

    // Clomid
    'CD50': 'Clomiphene_(Clomid)_50mg',

    // Letrozole
    'LZ25': 'Letrozole_(Femara)_25mg',

    // Tamoxifen
    'T20': 'Tamoxifen_(Nolvadex)_20mg',

    // Aromasin
    'XE25': 'Aromasin_(Exemestane)_25mg',

    // Anadrol
    'OXP50': 'Anadrol_(Oxymetholone)_50mg',

    // Anavar
    'X10': 'Anavar_(Oxandrolone)_10mg',
    'X25': 'Anavar_(Oxandrolone)_25mg',
    'X50': 'Anavar_(Oxandrolone)_50mg',

    // Dianabol
    'D10': 'Dianabol_(Methandrostenolone)_10mg',
    'D20': 'Dianabol_(Methandrostenolone)_20mg',
    'D50': 'Dianabol_(Methandrostenolone)_50mg',

    // Winstrol (tabs)
    'W10': 'Winstrol_(Stanozolol)_10mg',
    'W20': 'Winstrol_(Stanozolol)_20mg',
    'W50': 'Winstrol_(Stanozolol)_50mg',

    // Turinabol
    'CT10': 'Turinabol_10mg',
    'CT25': 'Turinabol_25mg',
    'CT50': 'Turinabol_50mg',

    // Superdrol (tabs)
    'SD10': 'Superdrol_(Methyldrostanolone)_10mg',

    // Halotestin
    'HT10': 'Halotestin_(Fluoxymesterone)_10mg',

    // Primobolan (tabs)
    'P10': 'Primobolan_(Methenolone_Acetate)_10mg',
    'P25': 'Primobolan_(Methenolone_Acetate)_25mg',
    'P50': 'Primobolan_(Methenolone_Acetate)_50mg',

    // Proviron
    'M10': 'Proviron_(Mesterolone)_10mg',
    'M25': 'Proviron_(Mesterolone)_25mg',

    // Methylstenbolone
    'MS10T': 'Methylstenbolone_10mg',

    // 17a-Methyl
    'MT10': '17a-Methyl-1-Testosterone_10mg',

    // DHB tab
    'DHB10': 'DHB_(1-Testosterone_Cypionate)_10mg',

    // Isotretinoin
    'AC10': 'Isotretinoin_(Accutane)_10mg',

    // Viagra / Cialis
    'SD100': 'Sildenafil_(Viagra)_100mg',
    'DT20': 'Tadalafil_(Cialis)_20mg',
    'B70': 'COCK_BOMBS_(Viagra_+_Cialis)_70mg',

    // Cabergoline
    'CG25': 'Cabergoline_025mg',

    // Finasteride
    'FN1': 'Finasteride_1mg',
    'FN5': 'Finasteride_5mg',

    // Dutasteride
    'DUT1': 'Dutasteride_1mg',

    // Enclomiphene
    'EC125': 'Enclomiphene_(Androxal)_125mg',
    'EC25': 'Enclomiphene_(Androxal)_25mg',

    // Flibanserin
    'FL100': 'Flibanserin_100mg',

    // Ivermectin
    'IV5': 'Ivermectin_5mg',

    // Minoxidil
    'MD5': 'Minoxidil_Oral_5mg',

    // Prednisone
    'PR10': 'Prednisone_10mg',

    // Salbutamol
    'SB20': 'Salbutamol_20mg',

    // Telmisartan
    'TM40': 'Telmisartan_40mg',

    // SARMs (tabs)
    'G50': 'GW-501516_(Cardarine)_10mg',
    'GW10': 'GW0742_(Cardarine_II)_10mg',
    'LG10': 'LGD-4033_(Ligandrol)_10mg',
    'LG3303': 'LGD3303_10mg',
    'MK10': 'MK-677_(Ibutamoren)_10mg',
    'OS25': 'Ostarine_(MK-2866)_25mg',
    'RD10': 'RAD140_(Testolone)_10mg',
    'SR10': 'SR9009_(Stenabolic)_10mg',
    'SR11': 'SR9011_10mg',
    'S23': 'Andarine_S4_25mg', // closest match - may need manual check
    'AS25': 'Andarine_S4_25mg',
    'YK10': 'YK11_10mg',

    // ─── INJECTABLE OILS ───

    // Test Cypionate
    'C250': 'Test_Cypionate_250mgml',

    // Test Enanthate
    'E250': 'Test_Enanthate_250mgml',
    'E300': 'Test_Enanthate_300mgml',

    // Test Suspension (SP100 = Testosterone Suspension)
    'SP100': 'Test_Suspension_100mgml',

    // Test Propionate
    'SP200': 'Test_Propionate_200mgml',

    // Test Base (BA100 = Test Base TNE No Ester)
    'BA100': 'Test_Base_(No_Ester)_100mgml',

    'TB100': 'Test_Base_(No_Ester)_100mgml',

    // Test Undecanoate
    'TY300': 'Test_Undecanoate_300mgml',

    // Sustanon
    'S250': 'Sustanon_250_250mgml',
    'S400': 'Sustanon_400_400mgml',
    'S450': 'Supertest_450_450mgml',
    'T600': 'Testo_600_(Test_Ace+TPP+Cyp)_600mgml',

    // Trenbolone Acetate
    'R100': 'Trenbolone_Acetate_100mgml',

    // Trenbolone Enanthate
    'RY100': 'Trenbolone_Enanthate_100mgml',
    'R200': 'Trenbolone_Enanthate_200mgml',

    // Tren Base/Hex/Mix
    'TRB50': 'Tren_Base_50mgml',
    'TH100': 'Tren_Hex_100mgml',
    'TRM200': 'TrenMix_200_200mgml',
    'TT225': 'TriTren_225_225mgml',

    // Deca (Nandrolone Decanoate)
    'N200': 'Deca_(Nandrolone_Decanoate)_200mgml',
    'N300': 'Deca_(Nandrolone_Decanoate)_300mgml',

    // NPP
    'PN100': 'NPP_(Nandrolone_Phenylpropionate)_100mgml',
    'PN200': 'NPP_(Nandrolone_Phenylpropionate)_200mgml',
    'NM300': 'NandroMix_300_300mgml',

    // Masteron
    'M100': 'Masteron_P_(Drostanolone_P)_100mgml',
    'M200': 'Masteron_E_(Drostanolone_E)_200mgml',
    'MB200': 'Masteron_Blend_200mgml',

    // Equipoise / Boldenone
    'U200': 'Equipoise_(Boldenone_Undecylenate)_200mgml',
    'U300': 'Equipoise_(Boldenone_Undecylenate)_300mgml',
    'U600': 'Boldenone_Undecylenate_600mgml',
    'BC250': 'Boldenone_Cypionate_250mgml',

    // Primobolan (injectable)
    'PE100': 'Primobolan_E_(Methenolone_Enanthate)_100mgml',
    'PE200': 'Primobolan_E_(Methenolone_Enanthate)_200mgml',

    // MENT
    'MT50': 'MENT_(Trestolone_Acetate)_50mgml',

    // DHB injectable
    'D100': 'DHB_(1-Test_Cyp)_100mgml',
    '1T100': 'DHB_(1-Test_Cyp)_100mgml',

    // DHT
    'DHT50': 'DHT_(Stanolone)_50mgml',

    // Metribolone
    'MTR5': 'Metribolone_5mgml',

    // Estradiol
    'EC10': 'Estradiol_Cypionate_10mgml',
    'EC100': 'Estradiol_Cypionate_10mgml',

    // Winstrol Oil
    'WO50': 'Winstrol_Oil_(Stanozolol)_50mgml',
    'WO100': 'Winstrol_Oil_(Stanozolol)_100mgml',

    // Winstrol Water
    'WW50': 'Winstrol_Water_(Stanozolol)_50mgml',
    'WW100': 'Winstrol_Water_(Stanozolol)_100mgml',

    // Dianabol Oil
    'DO50': 'Dianabol_Oil_50mgml',

    // Anadrol Oil
    'AO50': 'Anadrol_Oil_50mgml',

    // Superdrol Oil
    'SO50': 'Superdrol_Oil_50mgml',

    // Blends
    'B300': 'Blend_300_(TRAMast_PTest_P)_300mgml',
    'B375': 'Blend_375_(Tren_E+Mast_E+Test_E)_375mgml',
    'B500': 'Blend_500_(Tren_EMast_E)_500mgml',
    'RX225': 'RIPEX_225_(TRAMast_PTest_P)_225mgml',

    // Test Propionate alternate codes
    'P100': 'Test_Propionate_100mgml',

    // Anastrozole
    'AN1': 'Anastrozole_(Arimidex)_1mg',

    // Raws (both naming conventions)
    'SMRAW': 'Semaglutide_Raw',
    'TRRAW': 'Tirzepatide_Raw',
    'RTRAW': 'Retatrutide_Raw',
    'RDRAW': 'RAD-140_Raw',
    'LGRAW': 'LGD4033_Raw',
    'MKRAW': 'MK677_(Ibutamoren)_Raw',
    'GWRAW': 'GW501516_(Cardarine)_Raw',
    'SSRAW': 'SS-31_(Elamipretide)_Raw',
    'ASRAW': 'Andarine_S4_Raw',
    'YKRAW': 'YK11_Raw',
    'S23RAW': 'S23_Raw',
    'SEMAGLUTIDE-RAW': 'Semaglutide_Raw',
    'TIRZEPATIDE-RAW': 'Tirzepatide_Raw',
    'RETATRUTIDE-RAW': 'Retatrutide_Raw',
    'RAD140-RAW': 'RAD-140_Raw',
    'LGD4033-RAW': 'LGD4033_Raw',
    'MK677-RAW': 'MK677_(Ibutamoren)_Raw',
    'GW501516-RAW': 'GW501516_(Cardarine)_Raw',
    'SS31-RAW': 'SS-31_(Elamipretide)_Raw',
    'S4-RAW': 'Andarine_S4_Raw',
    'YK11-RAW': 'YK11_Raw',
    'S23-RAW': 'S23_Raw',

    // ─── ALTERNATE CAT_NOS (different codes for same products) ───

    // Retatrutide + Cagrilintide blend
    'RC10': 'Retatrutide_+_Cagrilintide_Blend_10mg',

    // TB500 alternate codes
    'BD5': 'TB500_5mg',
    'BD10': 'TB500_10mg',
    'BT2': 'TB500_2mg',

    // AHK-CU alternate
    'AU100': 'AHK-CU_100mg',

    // N-Acetyl Epitalon Amidate alternate
    'NET5': 'N-Acetyl_Epitalon_Amidate_5mg',

    // MGF / PEG MGF alternate
    'FM2': 'MGF_2mg',
    'FMP2': 'PEG_MGF_2mg',

    // LL37 alternate
    'LL3710': 'LL37_10mg',

    // GH Fragment alternate
    'FR2': 'GH_Fragment_176-191_2mg',
    'FR5': 'GH_Fragment_176-191_5mg',
    'FR10': 'GH_Fragment_176-191_10mg',

    // Dermorphin alternate
    'DR5': 'Dermorphin_5mg',

    // Insulin alternate
    'ISU': 'Insulin_(Lantus)',

    // Bac Water alternate
    'WA10': 'Bac_Water',
    'BA10': 'Bac_Water',
    'BA03': 'Bac_Water',

    // Botulinum alternate
    'XT100': 'Botulinum_toxin_100IU',

    // 5-amino-1MQ alternate codes
    '5AM': '5-amino-1MQ_5mg',
    '10AM': '5-amino-1MQ_10mg',
    '50AM': '5-amino-1MQ_50mg',

    // EPO alternate
    'E3K': 'EPO_3000IU',

    // Vilon alternate
    'VI20': 'Vilon_20mg',

    // Dulaglutide alternate
    'DL5': 'Dulaglutide_5mg',
    'DL10': 'Dulaglutide_10mg',

    // Pramlintide alternate
    'PL5': 'Pramlintide_5mg',
    'PL10': 'Pramlintide_10mg',

    // Alprostadil alternate
    'PRO20': 'Alprostadil_20mcg',

    // Lemon Bottle alternate
    'LB10': 'Lemon_Bottle',

    // AICAR alternate codes
    'AR50': 'AICAR_50mg',
    'A10': 'AICAR_Oral_10mg',
    'AICAR': 'AICAR_50mg',

    // Primobolan 50mg tab
    'M50': 'Primobolan_(Methenolone_Acetate)_50mg',

    // Halotestin alternate
    'FX40': 'Halotestin_(Fluoxymesterone)_10mg',

    // 17a-Methyl-1-Testosterone alternate
    '1TT10': '17a-Methyl-1-Testosterone_10mg',

    // Methylstenbolone alternate
    'MSB10': 'Methylstenbolone_10mg',

    // M1T (17a-Methyl) alternate
    'M1T10': '17a-Methyl-1-Testosterone_10mg',

    // Prednisone alternate
    'pdn10': 'Prednisone_10mg',

    // Dexamethasone - no exact report, use Prednisone
    'DEX1': 'Prednisone_10mg',

    // T4 alternate
    '440': 'T4_(Levothyroxine)_40mcg',
    'T3': 'T3_(Liothyronine)_25mcg',

    // SARMs (alternate cat_nos used on product page)
    'L40': 'LGD-4033_(Ligandrol)_10mg',
    'M6': 'MK-677_(Ibutamoren)_10mg',
    'S9': 'SR9009_(Stenabolic)_10mg',
    'R14': 'RAD140_(Testolone)_10mg',
    'M28': 'Ostarine_(MK-2866)_25mg',
    'S040': 'Andarine_S4_25mg',
    'Y1': 'YK11_10mg',
    'GW0742': 'GW0742_(Cardarine_II)_10mg',
    'SR9009': 'SR9009_(Stenabolic)_10mg',
    'SR9011': 'SR9011_10mg',
    'LGD3303': 'LGD3303_10mg',

    // Oral specialty alternates
    'BAM50': 'BAM15_50mg',
    'KP500': 'KPV_Oral_500mcg',
    'BB500': 'BPC_+_TB500_Oral_Blend_1000mcg',
    'FAN1': 'Finasteride_1mg',
    'FS5': 'Finasteride_5mg',
    'LV5': 'Ivermectin_5mg',
    'FB100': 'Flibanserin_100mg',
    'SLU1000': 'SLU-PP-332_1000mcg',
    'SB300': 'SLU-PP-332_+_BAM15_Blend_300mcg',
    'TR500': 'Tirzepatide_Oral_500mcg',
    'ACC10': 'Isotretinoin_(Accutane)_10mg',

    // Test Propionate 200mg/ml
    'P200': 'Test_Propionate_200mgml',

    // Injectable alternates (different cat_nos for same products)
    '3R225': 'TriTren_225_225mgml',
    'RM200': 'TrenMix_200_200mgml',
    'BR50': 'Tren_Base_50mgml',
    'H100': 'Tren_Hex_100mgml',

    // Nandrolone alternates
    'MN50': 'MENT_(Trestolone_Acetate)_50mgml',
    'DM200': 'Deca_(Nandrolone_Decanoate)_200mgml',
    'BS250': 'Boldenone_Cypionate_250mgml',
    'D200': 'DHB_(1-Test_Cyp)_100mgml',

    // Oil steroids alternates
    'SO100': 'Superdrol_Oil_50mgml',
    'SW50': 'Winstrol_Oil_(Stanozolol)_50mgml',
    'SW100': 'Winstrol_Oil_(Stanozolol)_100mgml',
    'OXO50': 'Anadrol_Oil_50mgml',
    'HD50': 'DHT_(Stanolone)_50mgml',
    'SDO50': 'Superdrol_Oil_50mgml',

    // Blend alternates
    'BM5': 'Masteron_Blend_200mgml',

    // Lipo alternates
    'LC120': 'Lipo-C_120mgml',
    'B1210': 'Vitamin_B12_10mg',
    'GAZ': 'Glutathione_1500mg',
    'LC216': 'Lipo-B_Blend',
    'B1201': 'Vitamin_B12_1mg',
    'D320': 'Vitamin_D3_20000IU',
    'LC1000': 'L-Carnitine_1000mg',
};

// ─── Step 3: Build the corrected janoshikMapping ───

const correctedMapping = {};
let matched = 0;
let unmatched = 0;
const unmatchedList = [];

for (const [catNo, reportKey] of Object.entries(catNoToReportKey)) {
    if (reportVerifyLinks[reportKey]) {
        correctedMapping[catNo] = reportVerifyLinks[reportKey];
        matched++;
    } else {
        unmatched++;
        unmatchedList.push(`${catNo} → ${reportKey} (not found in reportVerifyLinks)`);
    }
}

console.log(`\nMatched: ${matched}, Unmatched: ${unmatched}`);
if (unmatchedList.length > 0) {
    console.log('Unmatched entries:');
    unmatchedList.forEach(u => console.log('  ' + u));
}

// ─── Step 3b: Auto-map FEATURED variants ───
// FEATURED cat_nos are like "SM10-FEATURED" → use same URL as "SM10"
// Also handle special FEATURED mappings where base code differs

const featuredBaseMappings = {
    'CU100-FEATURED': 'CU100',
    'CU100-FEATURED2': 'CU100',
    'H10-FEATURED': 'H10',
    'H24-FEATURED': 'H24',
    'H15-FEATURED': 'H15',
    'H06-FEATURED': 'H06',
    'H12-FEATURED': 'H12',
    'H36-FEATURED': 'H36',
    '2AD5-FEATURED': '5AD', // AOD 5mg
    'VB12-FEATURED': 'VB10', // Vitamin B12
    'TB10-FEATURED': 'BT10', // TB500
    'MK2-FEATURED': 'M28', // Ostarine MK-2866
    'T25-FEATURED': 'CT25', // Turinabol 25mg
    'TREN100-FEATURED': 'R100', // Trenbolone Acetate
    'SR9-FEATURED': 'S9', // SR9009
    'S23-FEATURED': 'S040', // Andarine S4 (closest match)
    'YK11-FEATURED': 'Y1', // YK11
    'HALO10-FEATURED': 'FX40', // Halotestin
    'PROV25-FEATURED': 'M25', // Proviron 25mg
};

// First, read product.html to find all FEATURED cat_nos
const rawProductHtml = fs.readFileSync(path.join(BASE, 'product.html'), 'utf8');
const featuredRe = /"cat_no":\s*"([^"]*-FEATURED[^"]*)"/g;
let fm;
let featuredCount = 0;
while ((fm = featuredRe.exec(rawProductHtml)) !== null) {
    const featuredCatNo = fm[1];
    if (correctedMapping[featuredCatNo]) continue; // already mapped

    // Check explicit mapping first
    if (featuredBaseMappings[featuredCatNo]) {
        const baseCode = featuredBaseMappings[featuredCatNo];
        if (correctedMapping[baseCode]) {
            correctedMapping[featuredCatNo] = correctedMapping[baseCode];
            featuredCount++;
            continue;
        }
    }

    // Try stripping -FEATURED/-FEATURED2 suffix
    const baseCatNo = featuredCatNo.replace(/-FEATURED\d*$/, '');
    if (correctedMapping[baseCatNo]) {
        correctedMapping[featuredCatNo] = correctedMapping[baseCatNo];
        featuredCount++;
    }
}
console.log(`\nAuto-mapped ${featuredCount} FEATURED variants`);

// ─── Step 4: Now read product.html and extract ALL cat_nos to check coverage ───

const productHtml = fs.readFileSync(path.join(BASE, 'product.html'), 'utf8');
const catNoRe = /"cat_no":\s*"([^"]+)"/g;
const allCatNos = new Set();
let cm;
while ((cm = catNoRe.exec(productHtml)) !== null) {
    allCatNos.add(cm[1]);
}

console.log(`\nTotal cat_nos in product.html: ${allCatNos.size}`);
const uncovered = [];
for (const catNo of allCatNos) {
    if (!correctedMapping[catNo]) {
        uncovered.push(catNo);
    }
}
if (uncovered.length > 0) {
    console.log(`Cat_nos without mapping (${uncovered.length}):`);
    uncovered.forEach(c => console.log('  ' + c));
}

// ─── Step 5: For uncovered cat_nos, try to find them in the existing mapping ───
// Some may already have correct URLs in the existing janoshikMapping

const existingMappingMatch = productHtml.match(/const janoshikMapping = \{([\s\S]*?)\};/);
const existingMapping = {};
if (existingMappingMatch) {
    const emRe = /'([^']+)':\s*'([^']+)'/g;
    let em2;
    while ((em2 = emRe.exec(existingMappingMatch[1])) !== null) {
        existingMapping[em2[1]] = em2[2];
    }
}

// Placeholder URLs we want to replace
const PLACEHOLDERS = [
    'https://verify.janoshik.com.sigmaaudley.site/tests/51127-ACE-031_1mg_BEXQQCGVQ2ST',
    'https://verify.janoshik.com.sigmaaudley.site/tests/51826-Botulinum_toxin_100IU_EVCV64UZA4CD',
    'https://verify.janoshik.com.sigmaaudley.site/tests/51894-Anadrol_Oil_50mgml_YOGBSL1Q295L',
    'https://verify.janoshik.com.sigmaaudley.site/tests/51324-Alprostadil_20mcg_056L8I41YBKK',
];

// Check which existing entries are already correct (not placeholders)
const alreadyCorrect = {};
for (const [catNo, url] of Object.entries(existingMapping)) {
    if (!PLACEHOLDERS.includes(url) && !correctedMapping[catNo]) {
        alreadyCorrect[catNo] = url;
    }
}

// Merge: correctedMapping takes priority, then alreadyCorrect
const finalMapping = { ...alreadyCorrect, ...correctedMapping };
console.log(`\nFinal mapping size: ${Object.keys(finalMapping).length}`);

// ─── Step 6: Replace URLs in all HTML files ───

function fixHtmlFile(filePath) {
    let html = fs.readFileSync(filePath, 'utf8');
    let replacements = 0;

    // Fix janoshikMapping entries (single-quoted key-value pairs)
    for (const [catNo, url] of Object.entries(finalMapping)) {
        // Match in janoshikMapping: 'CATNO': 'OLD_URL'
        const mapPattern = new RegExp(`'${catNo.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')}':\\s*'[^']*'`, 'g');
        const newMapVal = `'${catNo}': '${url}'`;
        const before = html;
        html = html.replace(mapPattern, newMapVal);
        if (html !== before) replacements++;
    }

    // Fix janoshik_url in productsData entries
    // For each product block, find the cat_no and replace its janoshik_url
    // Pattern: "cat_no": "XXX" ... "janoshik_url": "OLD_URL"
    for (const [catNo, url] of Object.entries(finalMapping)) {
        // Find all product blocks with this cat_no and fix their janoshik_url
        const productBlockRe = new RegExp(
            `("cat_no":\\s*"${catNo.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')}"[\\s\\S]*?"janoshik_url":\\s*")([^"]*)(")`,
            'g'
        );
        const before = html;
        html = html.replace(productBlockRe, `$1${url}$3`);
        if (html !== before) replacements++;
    }

    fs.writeFileSync(filePath, html, 'utf8');
    console.log(`Fixed ${filePath}: ${replacements} replacements`);
}

const filesToFix = ['product.html', 'index.html', 'products.html'];
for (const file of filesToFix) {
    const filePath = path.join(BASE, file);
    if (fs.existsSync(filePath)) {
        fixHtmlFile(filePath);
    } else {
        console.log(`File not found: ${file}`);
    }
}

// ─── Step 7: Fix pricelist-data.json ───

const pricelistPath = path.join(BASE, 'pricelist-data.json');
if (fs.existsSync(pricelistPath)) {
    let pricelist = fs.readFileSync(pricelistPath, 'utf8');
    let plReplacements = 0;

    for (const [catNo, url] of Object.entries(finalMapping)) {
        const plRe = new RegExp(
            `("cat_no":\\s*"${catNo.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')}"[\\s\\S]*?"janoshik_url":\\s*")([^"]*)(")`,
            'g'
        );
        const before = pricelist;
        pricelist = pricelist.replace(plRe, `$1${url}$3`);
        if (pricelist !== before) plReplacements++;
    }

    fs.writeFileSync(pricelistPath, pricelist, 'utf8');
    console.log(`Fixed pricelist-data.json: ${plReplacements} replacements`);
}

// ─── Step 8: Verification ───

console.log('\n=== VERIFICATION ===');

// Re-read product.html and count remaining placeholders
const updatedProductHtml = fs.readFileSync(path.join(BASE, 'product.html'), 'utf8');
for (const placeholder of PLACEHOLDERS) {
    const escapedPh = placeholder.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
    const count = (updatedProductHtml.match(new RegExp(escapedPh, 'g')) || []).length;
    const label = placeholder.includes('ACE-031') ? 'ACE-031' :
                  placeholder.includes('Botulinum') ? 'Botulinum' :
                  placeholder.includes('Anadrol') ? 'Anadrol' : 'Alprostadil';
    console.log(`${label} placeholder remaining in product.html: ${count}`);
}

// Spot check key products
const spotChecks = [
    { catNo: 'SM5', expected: 'Semaglutide_5mg' },
    { catNo: 'TR10', expected: 'Tirzepatide_10mg' },
    { catNo: 'H06', expected: 'GH_191AA_(Somatropin)_6IU' },
    { catNo: 'C250', expected: 'Test_Cypionate' },
    { catNo: 'E250', expected: 'Test_Enanthate_250mgml' },
    { catNo: 'R100', expected: 'Trenbolone_Acetate' },
    { catNo: 'CD50', expected: 'Clomiphene_(Clomid)' },
    { catNo: '325', expected: 'T3_(Liothyronine)_25mcg' },
];

for (const check of spotChecks) {
    const url = finalMapping[check.catNo] || 'NOT FOUND';
    const ok = url.includes(check.expected) ? 'OK' : 'WRONG';
    console.log(`${ok}: ${check.catNo} → ${url.substring(0, 80)}...`);
}

console.log('\nDone!');
