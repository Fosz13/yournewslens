# Your News Lens v20 - engine.py with rich articles and images
import json

def run_scraper():
    print("Generating feed.json with rich articles and images...")
    data = {
        "lenses": ["Objective", "Analytical", "Critical", "Forward-Looking"],
        "articles": [
            {
                "title": "Global Semiconductor Supply Chains Reach New Milestones in 2026",
                "source": "TechWire Global",
                "perspective": "Analytical",
                "url": "https://example.com",
                "image": "https://images.unsplash.com/photo-1518770660439-4636190af475?auto=format&fit=crop&w=800&q=80",
                "summary": "Advanced manufacturing nodes and automated fabrication facilities have significantly accelerated production yields across North American and Asian markets.",
                "facts": [
                    "Wafer fabrication output increased by 22% year-over-year",
                    "Advanced packaging investments total $14B in Q3",
                    "Supply lead times reduced to historical averages"
                ]
            },
            {
                "title": "Renewable Energy Storage Breakthroughs Transform Grid Stability",
                "source": "Energy Today",
                "perspective": "Forward-Looking",
                "url": "https://example.com",
                "image": "https://images.unsplash.com/photo-1466611653911-95081537e5b7?auto=format&fit=crop&w=800&q=80",
                "summary": "Next-generation solid-state storage installations are providing unprecedented load-balancing capabilities for municipal power grids.",
                "facts": [
                    "Storage efficiency reaches 94% operational benchmark",
                    "Grid fluctuation incidents down 40% in test regions",
                    "Commercial scalability projected for late 2026"
                ]
            },
            {
                "title": "Urban Transit Modernization Projects Gain Momentum in Major Metros",
                "source": "Urban Pulse",
                "perspective": "Objective",
                "url": "https://example.com",
                "image": "https://images.unsplash.com/photo-1544620347-c4fd4a3d5957?auto=format&fit=crop&w=800&q=80",
                "summary": "Municipalities are rolling out integrated multimodal transit networks designed to reduce congestion and carbon footprints.",
                "facts": [
                    "Daily ridership up 18% following fare restructuring",
                    "Automated scheduling reduces peak wait times by 6 minutes"
                ]
            }
        ]
    }
    with open('feed.json', 'w') as f:
        json.dump(data, f, indent=2)
    print("feed.json generated successfully.")

if __name__ == '__main__':
    run_scraper()
