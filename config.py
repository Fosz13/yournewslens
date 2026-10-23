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
    # --- GOOGLE NEWS MASTER SECTIONS ---
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

    # --- GOOGLE NEWS TARGETED TOPIC FEEDS ---
    {
        "category": "Sports",
        "master_category": "Sports",
        "source": "Google News College Football",
        "url": "https://news.google.com/rss/search?q=college+football+rankings+OR+CFP+OR+AP+poll&hl=en-US&gl=US&ceid=US:en",
        "description": "NCAA college football top 25 rankings, games, and playoff developments."
    },
    {
        "category": "Sports",
        "master_category": "Sports",
        "source": "Google News NFL",
        "url": "https://news.google.com/rss/search?q=NFL+football+OR+quarterback+OR+touchdown&hl=en-US&gl=US&ceid=US:en",
        "description": "NFL games, injury reports, trades, and playoff standings."
    },
    {
        "category": "Sports",
        "master_category": "Sports",
        "source": "Google News MLB",
        "url": "https://news.google.com/rss/search?q=MLB+baseball+OR+World+Series+OR+NLCS+OR+ALCS&hl=en-US&gl=US&ceid=US:en",
        "description": "Major League Baseball championship pennants and scores."
    },
    {
        "category": "Sports",
        "master_category": "Sports",
        "source": "Google News NBA",
        "url": "https://news.google.com/rss/search?q=NBA+basketball+OR+Lakers+OR+Celtics&hl=en-US&gl=US&ceid=US:en",
        "description": "NBA basketball scores, player rotations, and trade deadlines."
    },
    {
        "category": "Energy & Weather",
        "master_category": "National Headlines",
        "source": "Google News Energy & Grid",
        "url": "https://news.google.com/rss/search?q=energy+OR+power+grid+OR+utilities+OR+FERC+OR+nuclear+reactor&hl=en-US&gl=US&ceid=US:en",
        "description": "Power grid infrastructure, pipelines, nuclear energy compacts, and utilities."
    },
    {
        "category": "Energy & Weather",
        "master_category": "National Headlines",
        "source": "Google News Severe Weather",
        "url": "https://news.google.com/rss/search?q=severe+weather+OR+storm+warning+OR+power+outage+OR+blizzard&hl=en-US&gl=US&ceid=US:en",
        "description": "High winds, blizzard alerts, downed lines, and emergency outages."
    },
    {
        "category": "Business & Economy",
        "master_category": "National Headlines",
        "source": "Google News Economy",
        "url": "https://news.google.com/rss/search?q=Federal+Reserve+OR+inflation+OR+interest+rates+OR+CPI+OR+jobs+report&hl=en-US&gl=US&ceid=US:en",
        "description": "Federal Reserve monetary policy, inflation data, and labor statistics."
    },
    {
        "category": "Border & Security",
        "master_category": "National Headlines",
        "source": "Google News Border & Security",
        "url": "https://news.google.com/rss/search?q=Border+Patrol+OR+immigration+asylum+OR+fentanyl+seizure+OR+CBP&hl=en-US&gl=US&ceid=US:en",
        "description": "Border enforcement, port fentanyl interdictions, and immigration courts."
    },
    {
        "category": "Science & Tech",
        "master_category": "Science & Tech",
        "source": "Google News AI & Chips",
        "url": "https://news.google.com/rss/search?q=artificial+intelligence+OR+semiconductors+OR+OpenAI+OR+Anthropic+OR+Nvidia&hl=en-US&gl=US&ceid=US:en",
        "description": "AI enterprise models, GPU computing, and semiconductor supply chains."
    },

    # --- DEDICATED SPORTS DESKS ---
    {
        "category": "Sports",
        "master_category": "Sports",
        "source": "ESPN Wire",
        "url": "https://www.espn.com/espn/rss/news",
        "description": "Dedicated 24/7 sports wire coverage across major American leagues."
    },
    {
        "category": "Sports",
        "master_category": "Sports",
        "source": "ESPN College Football",
        "url": "https://www.espn.com/espn/rss/ncf/news",
        "description": "ESPN breaking college football scores, rankings, and analysis."
    },
    {
        "category": "Sports",
        "master_category": "Sports",
        "source": "ESPN NFL",
        "url": "https://www.espn.com/espn/rss/nfl/news",
        "description": "ESPN NFL wire and franchise updates."
    },
    {
        "category": "Sports",
        "master_category": "Sports",
        "source": "ESPN MLB",
        "url": "https://www.espn.com/espn/rss/mlb/news",
        "description": "ESPN baseball pennant and World Series reports."
    },
    {
        "category": "Sports",
        "master_category": "Sports",
        "source": "CBS Sports",
        "url": "https://www.cbssports.com/rss/headlines/",
        "description": "CBS Sports wire breaking headlines."
    },
    {
        "category": "Sports",
        "master_category": "Sports",
        "source": "Fox Sports",
        "url": "https://moxie.foxnews.com/google-publisher/sports.xml",
        "description": "Fox Sports national athletics coverage."
    },

    
    # --- EXPANDED SPORTS NETWORKS & VERIFIED X REPORTERS ---
    {
        "category": "Sports",
        "master_category": "Sports",
        "source": "ESPN Top News Wire",
        "url": "https://www.espn.com/espn/rss/news",
        "description": "ESPN breaking news wire across major American and international leagues."
    },
    {
        "category": "Sports",
        "master_category": "Sports",
        "source": "ESPN NFL Insider Wire",
        "url": "https://www.espn.com/espn/rss/nfl/news",
        "description": "ESPN NFL reporting, roster moves, and game analysis."
    },
    {
        "category": "Sports",
        "master_category": "Sports",
        "source": "ESPN NBA Wire",
        "url": "https://www.espn.com/espn/rss/nba/news",
        "description": "ESPN NBA reporting, insider trade buzz, and league power rankings."
    },
    {
        "category": "Sports",
        "master_category": "Sports",
        "source": "ESPN MLB Wire",
        "url": "https://www.espn.com/espn/rss/mlb/news",
        "description": "ESPN Major League Baseball scores, pennant races, and transactions."
    },
    {
        "category": "Sports",
        "master_category": "Sports",
        "source": "ESPN College Football Wire",
        "url": "https://www.espn.com/espn/rss/ncf/news",
        "description": "ESPN College Football Playoff rankings, conference matchups, and analysis."
    },
    {
        "category": "Sports",
        "master_category": "Sports",
        "source": "ESPN Men's College Basketball",
        "url": "https://www.espn.com/espn/rss/ncb/news",
        "description": "ESPN NCAA men's basketball tournament predictions and rankings."
    },
    {
        "category": "Sports",
        "master_category": "Sports",
        "source": "ESPN Soccer & Champions League",
        "url": "https://www.espn.com/espn/rss/soccer/news",
        "description": "ESPN FC international soccer, Premier League, and Champions League wire."
    },
    {
        "category": "Sports",
        "master_category": "Sports",
        "source": "CBS Sports Wire",
        "url": "https://www.cbssports.com/rss/headlines/",
        "description": "CBS Sports national wire and breaking athletic developments."
    },
    {
        "category": "Sports",
        "master_category": "Sports",
        "source": "CBS Sports NFL",
        "url": "https://www.cbssports.com/rss/headlines/nfl/",
        "description": "CBS Sports NFL insider reports and team depth chart updates."
    },
    {
        "category": "Sports",
        "master_category": "Sports",
        "source": "CBS Sports College Football",
        "url": "https://www.cbssports.com/rss/headlines/collegefootball/",
        "description": "CBS Sports college football rankings and coaching carousel news."
    },
    {
        "category": "Sports",
        "master_category": "Sports",
        "source": "Fox Sports National",
        "url": "https://moxie.foxnews.com/google-publisher/sports.xml",
        "description": "Fox Sports national coverage across college and professional athletics."
    },
    {
        "category": "Sports",
        "master_category": "Sports",
        "source": "Yahoo Sports Wire",
        "url": "https://sports.yahoo.com/rss/",
        "description": "Yahoo Sports breaking reporting and investigative features."
    },
    {
        "category": "Sports",
        "master_category": "Sports",
        "source": "Bleacher Report Wire",
        "url": "https://bleacherreport.com/articles/feed",
        "description": "Bleacher Report real-time scores, viral highlights, and draft analysis."
    },
    {
        "category": "Sports",
        "master_category": "Sports",
        "source": "The Athletic Wire",
        "url": "https://theathletic.com/rss/",
        "description": "The Athletic premium sports journalism and beat reporting."
    },
    {
        "category": "Sports",
        "master_category": "Sports",
        "source": "X Beat Wire • Adam Schefter NFL",
        "url": "https://news.google.com/rss/search?q=%22Adam+Schefter%22+OR+%22Schefter%22+NFL&hl=en-US&gl=US&ceid=US:en",
        "description": "Verified NFL insider scoops and roster updates from ESPN's Adam Schefter via syndicated wire."
    },
    {
        "category": "Sports",
        "master_category": "Sports",
        "source": "X Beat Wire • Shams Charania NBA",
        "url": "https://news.google.com/rss/search?q=%22Shams+Charania%22+OR+%22Shams%22+NBA&hl=en-US&gl=US&ceid=US:en",
        "description": "Verified NBA insider breaking trade scoops and free agency news from Shams Charania."
    },
    {
        "category": "Sports",
        "master_category": "Sports",
        "source": "X Beat Wire • Ian Rapoport NFL",
        "url": "https://news.google.com/rss/search?q=%22Ian+Rapoport%22+NFL&hl=en-US&gl=US&ceid=US:en",
        "description": "Verified NFL Network injury updates and coaching changes from Ian Rapoport."
    },
    {
        "category": "Sports",
        "master_category": "Sports",
        "source": "X Beat Wire • Jeff Passan MLB",
        "url": "https://news.google.com/rss/search?q=%22Jeff+Passan%22+MLB&hl=en-US&gl=US&ceid=US:en",
        "description": "Verified Major League Baseball trade reporting and contract news from Jeff Passan."
    },
    {
        "category": "Sports",
        "master_category": "Sports",
        "source": "X Beat Wire • David Ornstein & Fabrizio Romano",
        "url": "https://news.google.com/rss/search?q=%22David+Ornstein%22+OR+%22Fabrizio+Romano%22+transfer&hl=en-US&gl=US&ceid=US:en",
        "description": "Verified European football transfers and injury dispatches from David Ornstein and Fabrizio Romano."
    },
    # --- PREMIER POLITICAL DESKS ---
    {
        "category": "Politics",
        "master_category": "National Headlines",
        "source": "Politico National",
        "url": "https://rss.politico.com/politics-news.xml",
        "description": "Capitol Hill, Congress, and White House political journalism."
    },
    {
        "category": "Politics",
        "master_category": "National Headlines",
        "source": "Fox News Politics",
        "url": "https://moxie.foxnews.com/google-publisher/politics.xml",
        "description": "National political and congressional news from Fox."
    },
    {
        "category": "Politics",
        "master_category": "National Headlines",
        "source": "The Hill",
        "url": "https://thehill.com/feed/",
        "description": "Bipartisan Capitol Hill legislative and policy wire."
    },

    # --- WIRE SERVICES & NATIONAL BROADCASTERS ---
    {
        "category": "National Headlines",
        "master_category": "National Headlines",
        "source": "NPR News",
        "url": "https://feeds.npr.org/1001/rss.xml",
        "description": "National public radio top investigative reporting."
    },
    {
        "category": "National Headlines",
        "master_category": "National Headlines",
        "source": "NPR National",
        "url": "https://feeds.npr.org/1003/rss.xml",
        "description": "NPR domestic and municipal community coverage."
    },
    {
        "category": "Business & Economy",
        "master_category": "National Headlines",
        "source": "NPR Business",
        "url": "https://feeds.npr.org/1006/rss.xml",
        "description": "NPR markets, workplace, and economy reporting."
    },
    {
        "category": "National Headlines",
        "master_category": "National Headlines",
        "source": "CBS News Latest",
        "url": "https://www.cbsnews.com/latest/rss/main",
        "description": "CBS News domestic news wire."
    },
    {
        "category": "World News",
        "master_category": "World News",
        "source": "BBC News US & Canada",
        "url": "https://feeds.bbci.co.uk/news/world/us_and_canada/rss.xml",
        "description": "BBC News North American international bureau coverage."
    },
    {
        "category": "World News",
        "master_category": "World News",
        "source": "BBC News World",
        "url": "https://feeds.bbci.co.uk/news/world/rss.xml",
        "description": "BBC News global diplomatic and security affairs."
    },
    {
        "category": "Business & Economy",
        "master_category": "National Headlines",
        "source": "CNBC Top News",
        "url": "https://www.cnbc.com/id/100003114/device/rss/rss.html",
        "description": "CNBC financial markets, Wall Street, and corporate earnings."
    },
    {
        "category": "Business & Economy",
        "master_category": "National Headlines",
        "source": "CNBC Markets",
        "url": "https://www.cnbc.com/id/10000664/device/rss/rss.html",
        "description": "CNBC stock exchange, interest rates, and bond yields."
    },
    {
        "category": "Science & Tech",
        "master_category": "Science & Tech",
        "source": "CNBC Tech",
        "url": "https://www.cnbc.com/id/19854910/device/rss/rss.html",
        "description": "CNBC Silicon Valley technology, semiconductor, and AI news."
    }
]

INGESTION_SETTINGS = {
    "max_items_per_feed": 12,
    "feed_retention_limit": 150,
    "min_stories_per_category": 12,
    "feed_timeout_seconds": 12,
    "ai_timeout_seconds": 25,
    "max_workers": 12
}