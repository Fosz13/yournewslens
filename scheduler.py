#!/usr/bin/env python3
"""
Your News Lens Continuous Ingestion Scheduler & Worker
Executes the scraping, AI synthesis, and feed-balancing pipeline on a recurring schedule.
Ideal for continuous local execution, VPS daemonization (systemd/screen), or continuous container workers.
"""

import time
import os
import sys
from datetime import datetime
import engine

POLL_INTERVAL_SECONDS = 900  # 15 minutes default

def run_continuous_worker(interval_seconds: int = POLL_INTERVAL_SECONDS):
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Starting Your News Lens Continuous Worker...")
    print(f"Polling Google News and Wire Feeds every {interval_seconds // 60} minutes.\n")

    while True:
        try:
            print(f"--- Ingestion Cycle Initiated at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ---")
            engine.run_pipeline()
            print(f"Cycle completed successfully. Next update in {interval_seconds // 60} minutes.\n")
        except Exception as e:
            print(f"Worker Error during cycle: {e}")
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
