"""Build the public Pages artifact or package the separately published edition."""
import hashlib
import json
from pathlib import Path
import re
import shutil
import sys

ROOT = Path(__file__).resolve().parent
PUBLIC = ROOT / "dist"
ASSETS = ("styles.css", "app.js", "polling.js", "comments.js")


def write_wire(destination):
    source = ROOT / "data" / "stories.json"
    records = json.loads(source.read_text(encoding="utf-8"))
    index = (ROOT / "index.html").read_text(encoding="utf-8")
    start, end = "<!-- BEGIN STORY FEED -->", "<!-- END GENERATED STORY FEED -->"
    if index.count(start) != 1 or index.count(end) != 1:
        raise ValueError("Expected one generated story feed")
    _, _, after_start = index.partition(start)
    markup, _, _ = after_start.partition(end)
    if not records or f'id="{records[0]["id"]}"' not in markup:
        raise ValueError("Rendered feed does not match the edition")
    edition = {
        "edition": hashlib.sha256(markup.encode()).hexdigest()[:16],
        "storyCount": len(records),
        "markup": markup,
    }
    (destination / "data").mkdir(parents=True, exist_ok=True)
    (destination / "v1").mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, destination / "data" / "stories.json")
    (destination / "v1" / "edition.json").write_text(
        json.dumps(edition, ensure_ascii=False), encoding="utf-8"
    )


def build_site():
    (PUBLIC / "data").mkdir(parents=True, exist_ok=True)
    for filename in (*ASSETS, "article-placeholder.svg", "robots.txt", "CNAME"):
        shutil.copyfile(ROOT / filename, PUBLIC / filename)
    index = (ROOT / "index.html").read_text(encoding="utf-8")
    for asset in ASSETS:
        version = hashlib.sha256((ROOT / asset).read_bytes()).hexdigest()[:12]
        index = re.sub(rf'="{re.escape(asset)}(?:\?v=[0-9a-f]+)?"', f'="{asset}?v={version}"', index)
    (PUBLIC / "index.html").write_text(index, encoding="utf-8")
    feed = json.loads((ROOT / "data" / "stories.json").read_text(encoding="utf-8"))
    for record in feed:
        record.pop("source_excerpt", None)
    (PUBLIC / "data" / "stories.json").write_text(json.dumps(feed, ensure_ascii=False), encoding="utf-8")


if __name__ == "__main__":
    if len(sys.argv) == 3 and sys.argv[1] == "--wire":
        write_wire(Path(sys.argv[2]))
    else:
        build_site()
