#!/bin/bash
# daily_run.sh — called by cron at 7 AM IST
# Add to crontab: 0 1 * * * /home/user/qcom_tracker/daily_run.sh
# (1 AM UTC = 6:30 AM IST, adjust to 0 1 * * * for 6:30 IST)

cd "$(dirname "$0")"

echo "=== $(date) : Starting daily ECAL Qcom scrape ==="
python scraper.py >> logs/cron.log 2>&1
echo "=== $(date) : Done ==="
