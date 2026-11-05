#!/usr/bin/env python3
"""Refresh a local checkout. GitHub Actions owns production publishing."""
import argparse
import time

import engine

POLL_INTERVAL_SECONDS = 900


def run_continuous_worker(interval_seconds=POLL_INTERVAL_SECONDS):
    if interval_seconds <= 0:
        raise ValueError("The refresh interval must be positive")
    while True:
        try:
            engine.run_pipeline()
        except (OSError, ValueError, RuntimeError) as error:
            print(f"[local wire] Refresh failed: {error}", flush=True)
        time.sleep(interval_seconds)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("interval", nargs="?", type=int, default=POLL_INTERVAL_SECONDS)
    run_continuous_worker(parser.parse_args().interval)
