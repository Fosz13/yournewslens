"""Build only the files needed by the public site."""
import json
from pathlib import Path
import shutil
import sys
import urllib.request

ROOT = Path(__file__).resolve().parent
PUBLIC = ROOT / "dist"

def live_edition_matches():
    try:
        request = urllib.request.Request("https://yournewslens.com/data/stories.json",
                                         headers={"Cache-Control": "no-cache"})
        with urllib.request.urlopen(request, timeout=8) as response:
            live = json.loads(response.read(2_000_000))
        expected = json.loads((ROOT / "data" / "stories.json").read_text(encoding="utf-8"))
        return bool(live and expected and live[0].get("edition") == expected[0]["edition"])
    except (OSError, ValueError, TypeError, KeyError, IndexError):
        return False


if __name__ == "__main__":
    if sys.argv[1:] == ["--check-live"]:
        sys.exit(0 if live_edition_matches() else 1)
    (PUBLIC / "data").mkdir(parents=True, exist_ok=True)
    for filename in ("index.html", "styles.css", "app.js", "polling.js", "article-placeholder.svg", "robots.txt", "CNAME"):
        shutil.copyfile(ROOT / filename, PUBLIC / filename)
    feed = json.loads((ROOT / "data" / "stories.json").read_text(encoding="utf-8"))
    for record in feed:
        record.pop("source_excerpt", None)
    (PUBLIC / "data" / "stories.json").write_text(json.dumps(feed, ensure_ascii=False), encoding="utf-8")
