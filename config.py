# ─────────────────────────────────────────────
# ECAL Quick Commerce Tracker – Configuration
# ─────────────────────────────────────────────

# Premium + Upper Mid pin codes (from Zone Summary)
PIN_CODES = {
    # ── PREMIUM ──────────────────────────────
    "700156": {"area": "New Town AA II-III",          "tier": "Premium"},
    "700016": {"area": "Park Street / Camac Street",  "tier": "Premium"},
    "700106": {"area": "New Town Action Area I",       "tier": "Premium"},
    "700019": {"area": "Ballygunge",                   "tier": "Premium"},
    "700020": {"area": "Gariahat / Ballygunge Phari",  "tier": "Premium"},
    "700027": {"area": "Alipore",                      "tier": "Premium"},

    # ── UPPER MID ─────────────────────────────
    "700107": {"area": "Chinar Park / Rajarhat",       "tier": "Upper Mid"},
    "700097": {"area": "Salt Lake Sec V / Karunamoyee","tier": "Upper Mid"},
    "700064": {"area": "Salt Lake Sec I-III",          "tier": "Upper Mid"},
    "700150": {"area": "Rajarhat E",                   "tier": "Upper Mid"},
    "700053": {"area": "New Alipore",                  "tier": "Upper Mid"},
    "700033": {"area": "Tollygunge",                   "tier": "Upper Mid"},
    "700075": {"area": "Kasba",                        "tier": "Upper Mid"},
    "700072": {"area": "Jodhpur Park",                 "tier": "Upper Mid"},
    "700098": {"area": "Krishnapur / NT fringe",       "tier": "Upper Mid"},
    "700091": {"area": "Salt Lake Sec IV-V",           "tier": "Upper Mid"},
    "700073": {"area": "Anandapur / EM Bypass",        "tier": "Upper Mid"},
    "700015": {"area": "Elgin Road / Bhowanipore N",   "tier": "Upper Mid"},
    "700022": {"area": "Dhakuria / Golpark",           "tier": "Upper Mid"},
    "700021": {"area": "Lansdowne / Beck Bagan",       "tier": "Upper Mid"},
    "700032": {"area": "Jadavpur",                     "tier": "Upper Mid"},
    "700077": {"area": "Dhakuria W",                   "tier": "Upper Mid"},
    "700084": {"area": "Garia / Narendrapur fringe",   "tier": "Upper Mid"},
    "700086": {"area": "Deshapriya Park",              "tier": "Upper Mid"},
    "700026": {"area": "Southern Avenue / Lake E",     "tier": "Upper Mid"},
    "700155": {"area": "New Town Adj",                 "tier": "Upper Mid"},
    "700028": {"area": "Bhabanipur / Paddapukur",      "tier": "Upper Mid"},
    "700025": {"area": "Bhowanipore",                  "tier": "Upper Mid"},
    "700029": {"area": "Lake Gardens",                 "tier": "Upper Mid"},
    "700135": {"area": "Rajarhat Main",                "tier": "Upper Mid"},
}

# ─── SKU master list ──────────────────────────────────────────────────────────
# search_terms: tried in order; first match wins. Variations handle how
# each platform names the same product differently.
SKUS = [
    # American Club
    {
        "sku": "AMCLUBCLOVEMINT10",
        "name": "American Club Clove Mint 10",
        "brand": "American Club",
        "segment": "KSFT",
        "search_terms": ["American Club Clove Mint", "American Club Clove"],
        "name_variants": ["American Club Clove Mint 10", "Am Club Clove Mint"],
    },
    {
        "sku": "AMCNYCOOLSLKFTK20",
        "name": "American Club NY Cool 20",
        "brand": "American Club",
        "segment": "Super KSFT",
        "search_terms": ["American Club NY Cool", "American Club New York Cool"],
        "name_variants": ["American Club NY Cool 20", "American Club New York Cool"],
    },

    # Benson & Hedges
    {
        "sku": "B&HFTKGB20",
        "name": "Benson & Hedges Blue Gold 20",
        "brand": "Benson & Hedges",
        "segment": "KSFT",
        "search_terms": ["Benson Hedges Blue Gold", "B&H Blue Gold", "Benson Blue Gold"],
        "name_variants": ["Benson & Hedges Blue Gold 20", "B&H Blue Gold 20",
                          "Benson And Hedges Blue Gold"],
    },
    {
        "sku": "B&HFTKSPL20",
        "name": "Benson & Hedges Special 20",
        "brand": "Benson & Hedges",
        "segment": "KSFT",
        "search_terms": ["Benson Hedges Special", "B&H Special"],
        "name_variants": ["Benson & Hedges Special 20", "B&H Special 20",
                          "Benson And Hedges Special"],
    },

    # Classic
    {
        "sku": "CLALPHATECFK20",
        "name": "Classic Alphatec 20",
        "brand": "Classic",
        "segment": "KSFT",
        "search_terms": ["Classic Alphatec"],
        "name_variants": ["Classic Alphatec 20", "Classic Alpha Tec 20"],
    },
    {
        "sku": "CLFLKBT10",
        "name": "Classic Balanced Taste (Milds) 10",
        "brand": "Classic",
        "segment": "KSFT",
        "search_terms": ["Classic Balanced Taste 10", "Classic Milds 10"],
        "name_variants": ["Classic Balanced Taste 10", "Classic Milds 10",
                          "Classic BT 10", "Classic (Milds) 10"],
    },
    {
        "sku": "CLFTKT20",
        "name": "Classic Balanced Taste (Milds) 20",
        "brand": "Classic",
        "segment": "KSFT",
        "search_terms": ["Classic Balanced Taste 20", "Classic Milds 20"],
        "name_variants": ["Classic Balanced Taste 20", "Classic Milds 20",
                          "Classic BT 20", "Classic (Milds) 20"],
    },
    {
        "sku": "CLCLOVEFTK12",
        "name": "Classic Clove 12",
        "brand": "Classic",
        "segment": "Super KSFT",
        "search_terms": ["Classic Clove"],
        "name_variants": ["Classic Clove 12", "Classic Clove"],
    },
    {
        "sku": "CLASSICCONNECTFK20",
        "name": "Classic Connect 20",
        "brand": "Classic",
        "segment": "KSFT",
        "search_terms": ["Classic Connect"],
        "name_variants": ["Classic Connect 20", "Classic Connect"],
    },
    {
        "sku": "CLDOUBLEBURST10",
        "name": "Classic Double Burst 10",
        "brand": "Classic",
        "segment": "KSFT",
        "search_terms": ["Classic Double Burst 10"],
        "name_variants": ["Classic Double Burst 10"],
    },
    {
        "sku": "CLDOUBLEBURST20",
        "name": "Classic Double Burst 20",
        "brand": "Classic",
        "segment": "KSFT",
        "search_terms": ["Classic Double Burst 20"],
        "name_variants": ["Classic Double Burst 20"],
    },
    {
        "sku": "CLFINTASTLOWSMEL20",
        "name": "Classic Fine Taste Low Smell 20",
        "brand": "Classic",
        "segment": "KSFT",
        "search_terms": ["Classic Fine Taste"],
        "name_variants": ["Classic Fine Taste Low Smell 20", "Classic Fine Taste 20"],
    },
    {
        "sku": "CLASSICICEBURST10",
        "name": "Classic Ice Burst 10",
        "brand": "Classic",
        "segment": "KSFT",
        "search_terms": ["Classic Ice Burst 10"],
        "name_variants": ["Classic Ice Burst 10"],
    },
    {
        "sku": "CLASSICICEBURST20",
        "name": "Classic Ice Burst 20",
        "brand": "Classic",
        "segment": "KSFT",
        "search_terms": ["Classic Ice Burst 20"],
        "name_variants": ["Classic Ice Burst 20"],
    },
    {
        "sku": "CLFTKREFT10",
        "name": "Classic Refined Taste (Ultra mild) 10",
        "brand": "Classic",
        "segment": "KSFT",
        "search_terms": ["Classic Refined Taste 10", "Classic Ultra Mild 10"],
        "name_variants": ["Classic Refined Taste 10", "Classic Ultra Mild 10",
                          "Classic (Ultra Mild) 10", "Classic RT 10"],
    },
    {
        "sku": "CLFTLREFT20",
        "name": "Classic Refined Taste (Ultra mild) 20",
        "brand": "Classic",
        "segment": "KSFT",
        "search_terms": ["Classic Refined Taste 20", "Classic Ultra Mild 20"],
        "name_variants": ["Classic Refined Taste 20", "Classic Ultra Mild 20",
                          "Classic (Ultra Mild) 20", "Classic RT 20"],
    },
    {
        "sku": "CLFTKRT10",
        "name": "Classic Rich Taste 10 (Regular)",
        "brand": "Classic",
        "segment": "KSFT",
        "search_terms": ["Classic Rich Taste 10", "Classic Regular 10"],
        "name_variants": ["Classic Rich Taste 10", "Classic (Regular) 10",
                          "Classic Regular 10"],
    },
    {
        "sku": "CLFTKRT20",
        "name": "Classic Rich Taste 20 (Regular)",
        "brand": "Classic",
        "segment": "KSFT",
        "search_terms": ["Classic Rich Taste 20", "Classic Regular 20"],
        "name_variants": ["Classic Rich Taste 20", "Classic (Regular) 20",
                          "Classic Regular 20"],
    },
    {
        "sku": "CLFTKV16CP",
        "name": "Classic Verve 16",
        "brand": "Classic",
        "segment": "KSFT",
        "search_terms": ["Classic Verve 16"],
        "name_variants": ["Classic Verve 16"],
    },
    {
        "sku": "CLFTKVRBT16CP",
        "name": "Classic Verve Balance Taste 16",
        "brand": "Classic",
        "segment": "KSFT",
        "search_terms": ["Classic Verve Balance", "Classic Verve BT"],
        "name_variants": ["Classic Verve Balance Taste 16", "Classic Verve BT 16",
                          "Classic Verve Balanced"],
    },

    # Flake
    {
        "sku": "FLSPLDST10",
        "name": "Flake Special 10",
        "brand": "Flake",
        "segment": "DSFT",
        "search_terms": ["Flake Special"],
        "name_variants": ["Flake Special 10", "ITC Flake Special 10"],
    },

    # Gold Flake
    {
        "sku": "GFFTKBLUE10",
        "name": "Gold Flake Blue 10",
        "brand": "Gold Flake",
        "segment": "KSFT",
        "search_terms": ["Gold Flake Blue 10"],
        "name_variants": ["Gold Flake Blue 10", "Gold Flake Kings Blue 10"],
    },
    {
        "sku": "GFFTKBLUE20",
        "name": "Gold Flake Blue 20",
        "brand": "Gold Flake",
        "segment": "KSFT",
        "search_terms": ["Gold Flake Blue 20"],
        "name_variants": ["Gold Flake Blue 20", "Gold Flake Kings Blue 20"],
    },
    {
        "sku": "GFINDIEMINTFT10",
        "name": "Gold Flake Indie Mint 10",
        "brand": "Gold Flake",
        "segment": "RSFT",
        "search_terms": ["Gold Flake Indie Mint"],
        "name_variants": ["Gold Flake Indie Mint 10", "GF Indie Mint 10"],
    },
    {
        "sku": "GFKMIXPOD10",
        "name": "Gold Flake Mixpod 10",
        "brand": "Gold Flake",
        "segment": "KSFT",
        "search_terms": ["Gold Flake Mixpod 10"],
        "name_variants": ["Gold Flake Mixpod 10", "GF Mixpod 10"],
    },
    {
        "sku": "GFKMIXPOD20",
        "name": "Gold Flake Mixpod 20",
        "brand": "Gold Flake",
        "segment": "KSFT",
        "search_terms": ["Gold Flake Mixpod 20"],
        "name_variants": ["Gold Flake Mixpod 20", "GF Mixpod 20"],
    },
    {
        "sku": "GFPRFT10",
        "name": "Gold Flake Premium Filter 10",
        "brand": "Gold Flake",
        "segment": "RSFT",
        "search_terms": ["Gold Flake Premium Filter", "Gold Flake Premium 10"],
        "name_variants": ["Gold Flake Premium Filter 10", "Gold Flake Premium 10",
                          "GF Premium Filter 10"],
    },
    {
        "sku": "GFFTK10",
        "name": "Gold Flake Red 10",
        "brand": "Gold Flake",
        "segment": "KSFT",
        "search_terms": ["Gold Flake Kings 10", "Gold Flake Red 10"],
        "name_variants": ["Gold Flake Kings 10", "Gold Flake Red 10",
                          "Gold Flake 10"],
    },
    {
        "sku": "GFFTK20",
        "name": "Gold Flake Red 20",
        "brand": "Gold Flake",
        "segment": "KSFT",
        "search_terms": ["Gold Flake Kings 20", "Gold Flake Red 20"],
        "name_variants": ["Gold Flake Kings 20", "Gold Flake Red 20",
                          "Gold Flake 20"],
    },
    {
        "sku": "GFSLFTK16CP",
        "name": "Gold Flake SLK 16",
        "brand": "Gold Flake",
        "segment": "KSFT",
        "search_terms": ["Gold Flake SLK", "Gold Flake Silk"],
        "name_variants": ["Gold Flake SLK 16", "Gold Flake Silk 16",
                          "Gold Flake Super Light King 16"],
    },
    {
        "sku": "GFSPSTRDST10-VAR2",
        "name": "Gold Flake Super Star V2 10",
        "brand": "Gold Flake",
        "segment": "DSFT",
        "search_terms": ["Gold Flake Super Star", "Gold Flake Superstar"],
        "name_variants": ["Gold Flake Super Star V2 10", "Gold Flake Superstar 10",
                          "Gold Flake Super Star 10"],
    },
    {
        "sku": "GFTKTWINPOD10",
        "name": "Gold Flake Twinpod 10",
        "brand": "Gold Flake",
        "segment": "KSFT",
        "search_terms": ["Gold Flake Twinpod 10"],
        "name_variants": ["Gold Flake Twinpod 10", "GF Twinpod 10"],
    },
    {
        "sku": "GFTKTWINPOD20",
        "name": "Gold Flake Twinpod 20",
        "brand": "Gold Flake",
        "segment": "KSFT",
        "search_terms": ["Gold Flake Twinpod 20"],
        "name_variants": ["Gold Flake Twinpod 20", "GF Twinpod 20"],
    },

    # India Kings
    {
        "sku": "IKFTKWHITEGOLD20",
        "name": "India Kings White Gold 20",
        "brand": "India Kings",
        "segment": "KSFT",
        "search_terms": ["India Kings White Gold"],
        "name_variants": ["India Kings White Gold 20", "IK White Gold 20"],
    },
    {
        "sku": "IKFTKRICHGOLD20",
        "name": "India Kings Rich Gold 20",
        "brand": "India Kings",
        "segment": "KSFT",
        "search_terms": ["India Kings Rich Gold"],
        "name_variants": ["India Kings Rich Gold 20", "IK Rich Gold 20"],
    },

    # Navy Cut
    {
        "sku": "NC10",
        "name": "Navy Cut 10",
        "brand": "Navy Cut",
        "segment": "Longs",
        "search_terms": ["Navy Cut"],
        "name_variants": ["Navy Cut 10", "Wills Navy Cut 10", "Wills Navy Cut"],
    },

    # SilkCut
    {
        "sku": "SCBLUEDST10",
        "name": "Silkcut Blue 10",
        "brand": "SilkCut",
        "segment": "DSFT",
        "search_terms": ["Silkcut Blue", "Silk Cut Blue"],
        "name_variants": ["Silkcut Blue 10", "Silk Cut Blue 10",
                          "Silkcut Special Blue 10", "SilkCut Blue 10"],
    },
    {
        "sku": "SCDST10",
        "name": "Silkcut Special 10",
        "brand": "SilkCut",
        "segment": "DSFT",
        "search_terms": ["Silkcut Special", "Silk Cut Special"],
        "name_variants": ["Silkcut Special 10", "Silk Cut Special 10",
                          "SilkCut Special 10"],
    },
]

# Brand-level search groupings (used to batch platform searches)
# We search at brand level; then match results to individual SKUs
BRAND_SEARCH_TERMS = {
    "American Club": ["American Club"],
    "Benson & Hedges": ["Benson Hedges", "B&H"],
    "Classic":        ["Classic cigarette", "Classic ITC"],
    "Flake":          ["Flake cigarette", "Flake ITC"],
    "Gold Flake":     ["Gold Flake", "GF Kings"],
    "India Kings":    ["India Kings"],
    "Navy Cut":       ["Navy Cut", "Wills Navy Cut"],
    "SilkCut":        ["Silkcut", "Silk Cut"],
}

# Scraper settings
HEADLESS = True            # Set False for debugging (shows browser window)
SLOW_MO_MS = 80            # Delay between actions in ms; increase if sites block fast access
PAGE_TIMEOUT_MS = 30_000   # Max wait per page load
SEARCH_WAIT_MS = 3_000     # Wait for search results
SCREENSHOT_ON_ERROR = True # Save screenshot when scrape fails for a pin code
