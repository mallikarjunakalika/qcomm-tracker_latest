# ECAL Qcom Tracker — Setup Guide

Tracks 38 cigarette SKUs across Blinkit, Swiggy Instamart, and Zepto  
for 30 Premium + Upper Mid pin codes in Kolkata.  
Runs daily at 7 AM, results viewable on any browser (iPhone/Desktop).

---

## What's in this package

| File | Purpose |
|---|---|
| `config.py` | All pin codes, SKUs, name variations |
| `scraper.py` | Playwright browser scraper (all 3 platforms) |
| `app.py` | Flask web server (serves dashboard + API) |
| `dashboard.html` | Mobile-friendly results dashboard |
| `requirements.txt` | Python dependencies |
| `Procfile` | For Railway.app deployment |
| `daily_run.sh` | Cron script for scheduled runs |

---

## OPTION A — Deploy on Railway.app (Recommended, ~₹600/month)

Railway is a simple cloud platform. No Linux knowledge needed.

### Step 1 — Create a free account
- Go to https://railway.app
- Sign up with GitHub (free account)

### Step 2 — Install Playwright in Railway
Railway uses Docker. Create a `nixpacks.toml` file in the folder:

```toml
[phases.setup]
nixPkgs = ["chromium", "playwright-driver"]

[phases.install]
cmds = ["pip install -r requirements.txt", "playwright install chromium"]
```

### Step 3 — Upload your files
- In Railway dashboard, click "New Project" → "Deploy from GitHub repo"
- Upload all files from this folder to a GitHub repository first
- OR use Railway CLI: `railway up`

### Step 4 — Set environment variable
In Railway dashboard → Variables:
```
RUN_TOKEN = ecal2026
```
(You can change this to anything — it's your password to trigger scrapes)

### Step 5 — Note your URL
Railway gives you a URL like `https://yourapp.up.railway.app`
Open this on your iPhone — that's your dashboard.

### Step 6 — Set up daily schedule
In Railway, go to your service → Settings → Cron:
```
Schedule: 0 1 * * *
Command:  python scraper.py
```
This runs at 1:00 AM UTC = 6:30 AM IST every day.

---

## OPTION B — Deploy on Render.com (Free tier available)

### Step 1 — Sign up at https://render.com

### Step 2 — New Web Service
- Connect your GitHub repo
- Build command: `pip install -r requirements.txt && playwright install chromium`
- Start command: `python app.py`

### Step 3 — Add a Cron Job service
- New → Cron Job
- Command: `python scraper.py`
- Schedule: `0 1 * * *`

### Step 4 — Access your URL
Render gives you `https://yourapp.onrender.com`

> ⚠️ Free tier spins down after inactivity. Paid (~$7/month) keeps it always on.

---

## OPTION C — Deploy on a VPS (DigitalOcean / Linode, ~₹800/month)

If you have a VPS:

```bash
# Install dependencies
sudo apt update
sudo apt install python3-pip python3-venv -y

# Set up project
cd ~
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
playwright install chromium
playwright install-deps

# Start server (background)
nohup python app.py > logs/server.log 2>&1 &

# Add cron job (runs at 7 AM IST = 1:30 AM UTC)
crontab -e
# Add this line:
30 1 * * * /root/qcom_tracker/venv/bin/python /root/qcom_tracker/scraper.py >> /root/qcom_tracker/logs/cron.log 2>&1
```

---

## Viewing on iPhone

1. Open Safari (or any browser)
2. Go to your server URL (e.g. `https://yourapp.up.railway.app`)
3. Tap the Share button → "Add to Home Screen"
4. Name it "Qcom Tracker" — it becomes an app icon on your home screen

---

## Dashboard Guide

```
Top bar:    Last run time  |  ▶ Run Now button
Summary:    Overall availability %, gap count
Tabs:       All / Blinkit / Swiggy / Zepto
Filters:    Tier (Premium/Upper Mid) | Brand | Gap filter
Table:      Pin codes × SKU index (numbered 1–38)
Legend:     SKU number → full name mapping
```

**Cell colours:**
- ✓ Green = SKU found and available
- ✗ Red = SKU not found in search results
- ! Amber = Error (location failed, site blocked)
- · Gray = Not yet checked

**Tap ▶ Run Now** to trigger an immediate scrape.  
Results update in ~8–12 minutes (30 pins × 3 platforms).

---

## Troubleshooting

### Sites are blocking the scraper
These platforms may detect automation and show CAPTCHAs.
- Set `HEADLESS = False` in `config.py` to see what's happening
- Increase `SLOW_MO_MS` to 200 in `config.py`
- If persistent, consider API interception (see advanced guide)

### Location not being set for a pin code
Check `screenshots/` folder — a screenshot is saved automatically on failure.
Common causes: the site changed its UI, or pin code doesn't have delivery coverage.

### SKU showing ✗ but it's actually available
The product name on the platform may differ from our name variants.
- Check `screenshots/` for what the search results look like
- Add the platform's exact product name to `name_variants` in `config.py`

### Server not starting
```bash
python app.py  # run directly to see error
```

---

## Updating SKU list

Edit `config.py` → `SKUS` list. Add a new entry:
```python
{
    "sku": "YOUR_SKU_ID",
    "name": "Brand Name Variant Description",
    "brand": "Brand Name",
    "segment": "KSFT",
    "search_terms": ["Primary Search Term", "Alt Search Term"],
    "name_variants": ["Exact platform name 1", "Exact platform name 2"],
},
```

---

## Adding / removing pin codes

Edit `config.py` → `PIN_CODES` dict.
Pin codes must include `area` and `tier` keys.

---

*Built for ECAL Branch — Kolkata. Covers ITC portfolio tracked on Qcom platforms.*
