#!/usr/bin/env python3
"""
Your News Lens Continuous 24/7 Automated Ingestion Daemon & Worker
Executes the scraping, multi-perspective AI synthesis, and feed-balancing pipeline
on a recurring 15-minute schedule.
Supports optional automatic Git commit & push and Netlify webhook triggers for continuous hands-free operation.
"""

import time
import os
import sys
import subprocess
import urllib.request
from datetime import datetime
import engine

POLL_INTERVAL_SECONDS = 900  # 15 minutes default

def git_commit_and_push():
    """Optionally commits and pushes updated feed files if running inside a Git repository."""
    try:
        status = subprocess.run(["git", "status", "--porcelain", "data/stories.json", "index.html"],
                                capture_output=True, text=True, check=False)
        if status.stdout.strip():
            print("[Auto-Sync] Changes detected in feed. Committing and pushing...")
            subprocess.run(["git", "add", "data/stories.json", "index.html"], check=False)
            timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
            subprocess.run(["git", "commit", "-m", f"Auto wire update: {timestamp} [deploy]"], check=False)
            push_res = subprocess.run(["git", "push"], capture_output=True, text=True, check=False)
            if push_res.returncode == 0:
                print("[Auto-Sync] Successfully pushed updates to remote Git repository.")
            else:
                print(f"[Auto-Sync Notice] Git push notice: {push_res.stderr.strip() or 'check git credentials'}")
        else:
            print("[Auto-Sync] No changes to commit.")
    except Exception as e:
        print(f"[Auto-Sync Notice] Git auto-sync skipped: {e}")

    # Optional Netlify webhook trigger
    webhook = os.environ.get("NETLIFY_BUILD_HOOK")
    if webhook:
        try:
            req = urllib.request.Request(webhook, data=b"{}", headers={"User-Agent": "YourNewsLensDaemon/1.0"})
            with urllib.request.urlopen(req, timeout=10) as resp:
                print("[Auto-Sync] Successfully triggered Netlify build webhook.")
        except Exception as err:
            print(f"[Auto-Sync Notice] Webhook trigger failed: {err}")

def run_continuous_worker(interval_seconds: int = POLL_INTERVAL_SECONDS):
    print(f"============================================================")
    print(f"  Your News Lens Continuous Automated Ingestion Daemon")
    print(f"  Polling {len(engine.RSS_FEEDS)} Wire Feeds every {interval_seconds // 60} minutes")
    print(f"  Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"============================================================\n")

    cycle_count = 0
    while True:
        cycle_count += 1
        print(f"\n--- Ingestion Cycle #{cycle_count} Initiated at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ---")
        try:
            engine.run_pipeline()
            git_commit_and_push()
            print(f"--- Cycle #{cycle_count} Completed Successfully. Next update in {interval_seconds // 60} minutes. ---\n")
        except Exception as e:
            print(f"[Worker Error] Exception during cycle #{cycle_count}: {e}")
            print("Retrying in 60 seconds...\n")
            time.sleep(60)
            continue

        time.sleep(interval_seconds)

if __name__ == "__main__":
    interval = POLL_INTERVAL_SECONDS
    if len(sys.argv) > 1:
        try:
            interval = int(sys.argv[1])
        except ValueError:
            pass
    run_continuous_worker(interval)
