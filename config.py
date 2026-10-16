"""
Configuration settings and RSS endpoints for Your News Lens.
Pulls directly from Google News front-page feeds, ESPN, and major wire services.
"""

RSS_FEEDS = [
    {
        "category": "All",
        "source": "Google News Top Headlines",
        "url": "https://news.google.com/rss?hl=en-US&gl=US&ceid=US:en",
        "description": "Main breaking news and trending headlines from Google News front page."
    },
    {
        "category": "Border & Security",
        "source": "Google News U.S.",
        "url": "https://news.google.com/rss/headlines/section/topic/NATION?hl=en-US&gl=US&ceid=US:en",
        "description": "National domestic news coverage across the United States."
    },
    {
        "category": "Politics",
        "source": "Google News World",
        "url": "https://news.google.com/rss/headlines/section/topic/WORLD?hl=en-US&gl=US&ceid=US:en",
        "description": "Global international diplomacy, defense, and foreign affairs."
    },
    {
        "category": "Politics",
        "source": "Google News Politics",
        "url": "https://news.google.com/rss/headlines/section/topic/POLITICS?hl=en-US&gl=US&ceid=US:en",
        "description": "Congressional legislation, elections, administration, and federal courts."
    },
    {
        "category": "Economy & Inflation",
        "source": "Google News Business",
        "url": "https://news.google.com/rss/headlines/section/topic/BUSINESS?hl=en-US&gl=US&ceid=US:en",
        "description": "Financial markets, central bank policy, corporate earnings, and inflation."
    },
    {
        "category": "Sports",
        "source": "Google News Sports",
        "url": "https://news.google.com/rss/headlines/section/topic/SPORTS?hl=en-US&gl=US&ceid=US:en",
        "description": "Major League Baseball, NFL, NBA, college athletics, and golf."
    },
    {
        "category": "Sports",
        "source": "ESPN Wire",
        "url": "https://www.espn.com/espn/rss/news",
        "description": "Dedicated 24/7 sports wire coverage across major American leagues."
    },
    {
        "category": "Tech & Free Speech",
        "source": "Google News Tech",
        "url": "https://news.google.com/rss/headlines/section/topic/TECHNOLOGY?hl=en-US&gl=US&ceid=US:en",
        "description": "Artificial intelligence, space technology, software, and digital policy."
    },
    {
        "category": "Politics",
        "source": "Politico National",
        "url": "https://rss.politico.com/politics-news.xml",
        "description": "Capitol Hill and White House political journalism."
    },
    {
        "category": "Politics",
        "source": "Fox News Politics",
        "url": "https://moxie.foxnews.com/google-publisher/politics.xml",
        "description": "Conservative national political reporting."
    },
    {
        "category": "Energy & Infrastructure",
        "source": "NPR News",
        "url": "https://feeds.npr.org/1001/rss.xml",
        "description": "National public radio investigative and infrastructure reporting."
    }
]

INGESTION_SETTINGS = {
    "max_items_per_feed": 8,
    "feed_retention_limit": 60,
    "min_stories_per_category": 6,
    "feed_timeout_seconds": 12,
    "ai_timeout_seconds": 18
}
