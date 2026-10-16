"""
Configuration settings and RSS endpoints for Your News Lens.
Features dedicated feeds across National Headlines, World News, Politics,
Business & Economy, Science & Tech, Entertainment, and Sports.
"""

# Master Category Hierarchy Definition
MASTER_CATEGORIES = {
    "National Headlines": [
        "National News",
        "Politics",
        "Business & Economy",
        "Energy & Weather",
        "Health",
        "Border & Security",
        "Crime & Public Safety"
    ],
    "World News": [
        "World News",
        "Geopolitics",
        "Global Affairs",
        "Foreign Conflicts"
    ],
    "Science & Tech": [
        "Science & Tech",
        "Technology",
        "Science",
        "Space & NASA",
        "Artificial Intelligence"
    ],
    "Entertainment": [
        "Entertainment",
        "Film & Cinema",
        "Music & Pop Culture",
        "Hollywood & Box Office"
    ],
    "Sports": [
        "Sports",
        "Baseball (MLB)",
        "Football (NFL/CFP)",
        "Basketball (NBA)",
        "Golf (PGA)"
    ]
}

RSS_FEEDS = [
    {
        "category": "All",
        "master_category": "All",
        "source": "Google News Top Headlines",
        "url": "https://news.google.com/rss?hl=en-US&gl=US&ceid=US:en",
        "description": "Main breaking news and trending headlines from Google News front page."
    },
    {
        "category": "National Headlines",
        "master_category": "National Headlines",
        "source": "Google News U.S.",
        "url": "https://news.google.com/rss/headlines/section/topic/NATION?hl=en-US&gl=US&ceid=US:en",
        "description": "National domestic news coverage across the United States."
    },
    {
        "category": "World News",
        "master_category": "World News",
        "source": "Google News World",
        "url": "https://news.google.com/rss/headlines/section/topic/WORLD?hl=en-US&gl=US&ceid=US:en",
        "description": "Global international diplomacy, defense, and foreign affairs."
    },
    {
        "category": "Politics",
        "master_category": "National Headlines",
        "source": "Google News Politics",
        "url": "https://news.google.com/rss/headlines/section/topic/POLITICS?hl=en-US&gl=US&ceid=US:en",
        "description": "Congressional legislation, elections, administration, and federal courts."
    },
    {
        "category": "Business & Economy",
        "master_category": "National Headlines",
        "source": "Google News Business",
        "url": "https://news.google.com/rss/headlines/section/topic/BUSINESS?hl=en-US&gl=US&ceid=US:en",
        "description": "Financial markets, central bank policy, corporate earnings, and inflation."
    },
    {
        "category": "Science & Tech",
        "master_category": "Science & Tech",
        "source": "Google News Science",
        "url": "https://news.google.com/rss/headlines/section/topic/SCIENCE?hl=en-US&gl=US&ceid=US:en",
        "description": "Scientific discoveries, NASA, space exploration, and scientific breakthroughs."
    },
    {
        "category": "Science & Tech",
        "master_category": "Science & Tech",
        "source": "Google News Tech",
        "url": "https://news.google.com/rss/headlines/section/topic/TECHNOLOGY?hl=en-US&gl=US&ceid=US:en",
        "description": "Artificial intelligence, space technology, software, and digital policy."
    },
    {
        "category": "Entertainment",
        "master_category": "Entertainment",
        "source": "Google News Entertainment",
        "url": "https://news.google.com/rss/headlines/section/topic/ENTERTAINMENT?hl=en-US&gl=US&ceid=US:en",
        "description": "Cinema, box office, Hollywood studios, music, and pop culture."
    },
    {
        "category": "Health",
        "master_category": "National Headlines",
        "source": "Google News Health",
        "url": "https://news.google.com/rss/headlines/section/topic/HEALTH?hl=en-US&gl=US&ceid=US:en",
        "description": "Healthcare policy, hospitals, FDA decisions, and medical breakthroughs."
    },
    {
        "category": "Sports",
        "master_category": "Sports",
        "source": "Google News Sports",
        "url": "https://news.google.com/rss/headlines/section/topic/SPORTS?hl=en-US&gl=US&ceid=US:en",
        "description": "Major League Baseball, NFL, NBA, college athletics, and golf."
    },
    {
        "category": "Sports",
        "master_category": "Sports",
        "source": "ESPN Wire",
        "url": "https://www.espn.com/espn/rss/news",
        "description": "Dedicated 24/7 sports wire coverage across major American leagues."
    },
    {
        "category": "Politics",
        "master_category": "National Headlines",
        "source": "Politico National",
        "url": "https://rss.politico.com/politics-news.xml",
        "description": "Capitol Hill and White House political journalism."
    },
    {
        "category": "Politics",
        "master_category": "National Headlines",
        "source": "Fox News Politics",
        "url": "https://moxie.foxnews.com/google-publisher/politics.xml",
        "description": "Conservative national political reporting."
    },
    {
        "category": "National Headlines",
        "master_category": "National Headlines",
        "source": "NPR News",
        "url": "https://feeds.npr.org/1001/rss.xml",
        "description": "National public radio investigative and infrastructure reporting."
    }
]

INGESTION_SETTINGS = {
    "max_items_per_feed": 8,
    "feed_retention_limit": 60,
    "min_stories_per_category": 4,
    "feed_timeout_seconds": 12,
    "ai_timeout_seconds": 25
}