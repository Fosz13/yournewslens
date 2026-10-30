import json
import os

def run():
    print("Running news scraper engine...")
    # Standard stable feed format
    data = {
        "lenses": ["Objective", "Analytical", "Critical", "Forward-Looking"],
        "articles": [
            {
                "title": "Sample News Article from Stable Engine",
                "source": "News Wire",
                "perspective": "Objective",
                "url": "https://example.com",
                "summary": "This is a stable sample article verifying the engine and button filtering logic work properly.",
                "facts": [
                    "Stable baseline architecture",
                    "Fully functional button click handlers",
                    "Clean data binding"
                ]
            }
        ]
    }
    with open('feed.json', 'w') as f:
        json.dump(data, f, indent=2)

if __name__ == '__main__':
    run()
