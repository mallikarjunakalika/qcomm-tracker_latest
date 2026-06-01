"""
app.py — Flask server for ECAL Qcom Tracker
Serves the dashboard HTML and provides a JSON API for data.
Also exposes a /run endpoint to trigger the scraper.
"""

import json
import os
import subprocess
import sys
from pathlib import Path
from flask import Flask, jsonify, send_file, request, abort

app = Flask(__name__, static_folder=".", static_url_path="")

DATA_FILE = Path("data/results.json")


# ─── Routes ───────────────────────────────────────────────────────────────────

@app.route("/")
def index():
    return send_file("dashboard.html")


@app.route("/api/results")
def api_results():
    if not DATA_FILE.exists():
        return jsonify({"error": "No data yet. Run the scraper first."}), 404
    with open(DATA_FILE) as f:
        return jsonify(json.load(f))


@app.route("/api/run", methods=["POST"])
def api_run():
    """Trigger a background scraper run."""
    token = request.headers.get("X-Run-Token", "")
    expected = os.environ.get("RUN_TOKEN", "ecal2026")
    if token != expected:
        abort(403)

    platform = request.json.get("platform") if request.is_json else None
    cmd = [sys.executable, "scraper.py"]
    if platform:
        cmd += ["--platform", platform]

    # Fire and forget (non-blocking)
    subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return jsonify({"status": "started", "command": " ".join(cmd)})


@app.route("/api/status")
def api_status():
    if not DATA_FILE.exists():
        return jsonify({"status": "no_data"})
    with open(DATA_FILE) as f:
        data = json.load(f)
    meta = data.get("meta", {})
    return jsonify({
        "status": "ok",
        "last_run": meta.get("last_run"),
        "run_duration_s": meta.get("run_duration_s"),
    })


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
