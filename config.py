"""
Configuration settings and authoritative multi-source RSS endpoints for Your News Lens.
Pulls directly from premier neutral wire services, international broadcasters, and sports networks
that publish full editorial articles with verified lead photography:
- ESPN (10 dedicated multi-sport feeds)
- BBC News & BBC Sport (9 global & domestic bureau feeds)
- Al Jazeera English (5 global, diplomatic, economic & science feeds)
- Associated Press / AP News (9 dedicated national, world, politics, business & sports feeds)
- Reuters, NPR News, PBS NewsHour, CBS News, CNBC, Politico, The Hill, CBS Sports, Fox Sports, Sports Illustrated, The Athletic
Zero Yahoo News / Yahoo clickbait feeds and zero image-less X / Twitter wire feeds.
"""

PRIMARY_TRUSTED_SOURCES = [
    "ESPN",
    "BBC News",
    "BBC Sport",
    "Al Jazeera English",
    "AP News",
    "Associated Press",
    "Reuters",
    "NPR News",
    "PBS NewsHour",
    "CBS News",
    "CNBC",
    "Bloomberg",
    "Politico",
    "The Hill",
    "CBS Sports",
    "Fox Sports",
    "Sports Illustrated",
    "The Athletic"
]

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
    # =========================================================================
    # 1. ASSOCIATED PRESS (AP NEWS) — PRIMARY NEUTRAL WIRE DESKS
    # =========================================================================
    {
        "category": "All",
        "master_category": "National Headlines",
        "source": "AP News Top Headlines",
        "url": "https://news.google.com/rss/search?q=site:apnews.com+when:1d&hl=en-US&gl=US&ceid=US:en",
        "description": "Associated Press breaking top headlines across the United States and worldwide."
    },
    {
        "category": "National Headlines",
        "master_category": "National Headlines",
        "source": "AP News U.S. National",
        "url": "https://news.google.com/rss/search?q=site:apnews.com/hub/us-news+when:1d&hl=en-US&gl=US&ceid=US:en",
        "description": "Associated Press national domestic news coverage across the United States."
    },
    {
        "category": "World News",
        "master_category": "World News",
        "source": "AP News World",
        "url": "https://news.google.com/rss/search?q=site:apnews.com/hub/world-news+when:1d&hl=en-US&gl=US&ceid=US:en",
        "description": "Associated Press international diplomacy, defense, and foreign affairs."
    },
    {
        "category": "Politics",
        "master_category": "National Headlines",
        "source": "AP News Politics & Congress",
        "url": "https://news.google.com/rss/search?q=site:apnews.com/hub/politics+OR+site:apnews.com/hub/congress+when:1d&hl=en-US&gl=US&ceid=US:en",
        "description": "AP Capitol Hill, White House, elections, Supreme Court, and federal legislation."
    },
    {
        "category": "Business & Economy",
        "master_category": "National Headlines",
        "source": "AP News Business & Economy",
        "url": "https://news.google.com/rss/search?q=site:apnews.com/hub/business+OR+site:apnews.com/hub/inflation+when:1d&hl=en-US&gl=US&ceid=US:en",
        "description": "AP financial markets, Federal Reserve policy, inflation, and corporate news."
    },
    {
        "category": "Science & Tech",
        "master_category": "Science & Tech",
        "source": "AP News Technology & Science",
        "url": "https://news.google.com/rss/search?q=site:apnews.com/hub/technology+OR+site:apnews.com/hub/science+when:1d&hl=en-US&gl=US&ceid=US:en",
        "description": "AP artificial intelligence, space exploration, NASA, and cybersecurity."
    },
    {
        "category": "Health",
        "master_category": "National Headlines",
        "source": "AP News Health & Medicine",
        "url": "https://news.google.com/rss/search?q=site:apnews.com/hub/health+when:1d&hl=en-US&gl=US&ceid=US:en",
        "description": "AP healthcare policy, FDA decisions, clinical trials, and public health."
    },
    {
        "category": "Entertainment",
        "master_category": "Entertainment",
        "source": "AP News Entertainment",
        "url": "https://news.google.com/rss/search?q=site:apnews.com/hub/entertainment+when:1d&hl=en-US&gl=US&ceid=US:en",
        "description": "AP film, television, music, box office, and arts reporting."
    },
    {
        "category": "Sports",
        "master_category": "Sports",
        "source": "AP News Sports Wire",
        "url": "https://news.google.com/rss/search?q=site:apnews.com/hub/sports+when:1d&hl=en-US&gl=US&ceid=US:en",
        "description": "Associated Press national and international sports wire."
    },

    # =========================================================================
    # 2. BBC NEWS & BBC SPORT — GLOBAL & NORTH AMERICAN BUREAUS
    # =========================================================================
    {
        "category": "All",
        "master_category": "World News",
        "source": "BBC News Top Stories",
        "url": "https://feeds.bbci.co.uk/news/rss.xml",
        "description": "BBC News top global and breaking headlines."
    },
    {
        "category": "World News",
        "master_category": "World News",
        "source": "BBC News World",
        "url": "https://feeds.bbci.co.uk/news/world/rss.xml",
        "description": "BBC News global diplomatic, humanitarian, and security affairs."
    },
    {
        "category": "National Headlines",
        "master_category": "National Headlines",
        "source": "BBC News US & Canada",
        "url": "https://feeds.bbci.co.uk/news/world/us_and_canada/rss.xml",
        "description": "BBC News North American bureau coverage of U.S. policy and society."
    },
    {
        "category": "Business & Economy",
        "master_category": "National Headlines",
        "source": "BBC News Business",
        "url": "https://feeds.bbci.co.uk/news/business/rss.xml",
        "description": "BBC global economy, central banks, trade, and corporate reporting."
    },
    {
        "category": "Science & Tech",
        "master_category": "Science & Tech",
        "source": "BBC News Technology",
        "url": "https://feeds.bbci.co.uk/news/technology/rss.xml",
        "description": "BBC technology, artificial intelligence, cyber policy, and telecoms."
    },
    {
        "category": "Science & Tech",
        "master_category": "Science & Tech",
        "source": "BBC News Science & Environment",
        "url": "https://feeds.bbci.co.uk/news/science_and_environment/rss.xml",
        "description": "BBC space, climate science, physics, and environmental breakthroughs."
    },
    {
        "category": "Health",
        "master_category": "National Headlines",
        "source": "BBC News Health",
        "url": "https://feeds.bbci.co.uk/news/health/rss.xml",
        "description": "BBC medical breakthroughs, hospital policy, and clinical research."
    },
    {
        "category": "Entertainment",
        "master_category": "Entertainment",
        "source": "BBC News Entertainment & Arts",
        "url": "https://feeds.bbci.co.uk/news/entertainment_and_arts/rss.xml",
        "description": "BBC cinema, television, music, culture, and arts coverage."
    },
    {
        "category": "Sports",
        "master_category": "Sports",
        "source": "BBC Sport Global Wire",
        "url": "https://feeds.bbci.co.uk/sport/rss.xml",
        "description": "BBC Sport international football, Champions League, tennis, golf, and Formula 1."
    },

    # =========================================================================
    # 3. AL JAZEERA ENGLISH — INTERNATIONAL, DIPLOMATIC & ECONOMIC DESKS
    # =========================================================================
    {
        "category": "World News",
        "master_category": "World News",
        "source": "Al Jazeera English",
        "url": "https://www.aljazeera.com/xml/rss/all.xml",
        "description": "Al Jazeera English 24/7 international news, diplomacy, and global affairs."
    },
    {
        "category": "World News",
        "master_category": "World News",
        "source": "Al Jazeera World & Geopolitics",
        "url": "https://news.google.com/rss/search?q=site:aljazeera.com/news+when:1d&hl=en-US&gl=US&ceid=US:en",
        "description": "Al Jazeera in-depth geopolitical reporting across Europe, Middle East, Asia, Africa, and the Americas."
    },
    {
        "category": "Business & Economy",
        "master_category": "National Headlines",
        "source": "Al Jazeera Economy & Global Trade",
        "url": "https://news.google.com/rss/search?q=site:aljazeera.com/economy+when:1d&hl=en-US&gl=US&ceid=US:en",
        "description": "Al Jazeera global energy markets, shipping corridors, commodities, and sovereign finance."
    },
    {
        "category": "Energy & Weather",
        "master_category": "National Headlines",
        "source": "Al Jazeera Energy & Climate",
        "url": "https://news.google.com/rss/search?q=site:aljazeera.com+energy+OR+climate+OR+storm+OR+grid+when:1d&hl=en-US&gl=US&ceid=US:en",
        "description": "Al Jazeera global energy infrastructure, extreme weather, and climate policy."
    },
    {
        "category": "Sports",
        "master_category": "Sports",
        "source": "Al Jazeera Sports",
        "url": "https://news.google.com/rss/search?q=site:aljazeera.com/sports+when:1d&hl=en-US&gl=US&ceid=US:en",
        "description": "Al Jazeera international football, combat sports, tennis, and global tournaments."
    },

    # =========================================================================
    # 4. ESPN & DEDICATED SPORTS NETWORKS — 24/7 MULTI-LEAGUE COVERAGE
    # =========================================================================
    {
        "category": "Sports",
        "master_category": "Sports",
        "source": "ESPN Top News Wire",
        "url": "https://www.espn.com/espn/rss/news",
        "description": "ESPN 24/7 breaking news wire across major American and international leagues."
    },
    {
        "category": "Sports",
        "master_category": "Sports",
        "source": "ESPN NFL Insider Wire",
        "url": "https://www.espn.com/espn/rss/nfl/news",
        "description": "ESPN NFL reporting, roster moves, injury reports, and game analysis."
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
        "source": "ESPN NHL Hockey Wire",
        "url": "https://www.espn.com/espn/rss/nhl/news",
        "description": "ESPN NHL hockey scores, Stanley Cup contenders, and roster transactions."
    },
    {
        "category": "Sports",
        "master_category": "Sports",
        "source": "ESPN PGA Golf & Majors",
        "url": "https://www.espn.com/espn/rss/golf/news",
        "description": "ESPN PGA Tour, LIV commercial talks, and major championship coverage."
    },
    {
        "category": "Sports",
        "master_category": "Sports",
        "source": "ESPN MMA & Boxing Wire",
        "url": "https://www.espn.com/espn/rss/mma/news",
        "description": "ESPN UFC championship fight cards, boxing title bouts, and streaming guides."
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
        "source": "Sports Illustrated Wire",
        "url": "https://www.si.com/.rss/full/",
        "description": "Sports Illustrated comprehensive coverage across collegiate and professional athletics."
    },
    {
        "category": "Sports",
        "master_category": "Sports",
        "source": "The Athletic Wire",
        "url": "https://theathletic.com/rss/",
        "description": "The Athletic premium sports journalism and beat reporting."
    },

    # =========================================================================
    # 5. REUTERS, NPR, PBS, POLITICO, THE HILL, CBS NEWS & CNBC
    # =========================================================================
    {
        "category": "World News",
        "master_category": "World News",
        "source": "Reuters World Wire",
        "url": "https://news.google.com/rss/search?q=site:reuters.com/world+when:1d&hl=en-US&gl=US&ceid=US:en",
        "description": "Reuters international diplomatic and global security wire."
    },
    {
        "category": "Business & Economy",
        "master_category": "National Headlines",
        "source": "Reuters Business & Markets",
        "url": "https://news.google.com/rss/search?q=site:reuters.com/business+OR+site:reuters.com/markets+when:1d&hl=en-US&gl=US&ceid=US:en",
        "description": "Reuters global financial markets, energy, and central banking wire."
    },
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
        "source": "The Hill",
        "url": "https://thehill.com/feed/",
        "description": "Bipartisan Capitol Hill legislative and policy wire."
    },
    {
        "category": "Politics",
        "master_category": "National Headlines",
        "source": "Fox News Politics",
        "url": "https://moxie.foxnews.com/google-publisher/politics.xml",
        "description": "National political and congressional news from Fox."
    },
    {
        "category": "National Headlines",
        "master_category": "National Headlines",
        "source": "NPR News",
        "url": "https://feeds.npr.org/1001/rss.xml",
        "description": "National Public Radio top investigative reporting."
    },
    {
        "category": "National Headlines",
        "master_category": "National Headlines",
        "source": "PBS NewsHour",
        "url": "https://www.pbs.org/newshour/feeds/rss/headlines",
        "description": "PBS NewsHour national and international public broadcasting wire."
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
    },
    # =========================================================================
    # 6. ADDITIONAL LEFT / RIGHT PUBLISHER COVERAGE FOR LENS-BASED FEED MIX
    # =========================================================================
    {
        "category": "Politics", "master_category": "National Headlines",
        "source": "CNN Politics",
        "url": "https://rss.cnn.com/rss/cnn_allpolitics.rss",
        "description": "CNN political reporting and U.S. policy coverage."
    },
    {
        "category": "National Headlines", "master_category": "National Headlines",
        "source": "CNN Top Stories",
        "url": "https://rss.cnn.com/rss/cnn_topstories.rss",
        "description": "CNN national and breaking news coverage."
    },
    {
        "category": "Politics", "master_category": "National Headlines",
        "source": "Fox News Latest",
        "url": "https://moxie.foxnews.com/google-publisher/latest.xml",
        "description": "Fox News national and breaking news coverage."
    },
    {
        "category": "Politics", "master_category": "National Headlines",
        "source": "The Guardian US",
        "url": "https://www.theguardian.com/us-news/rss",
        "description": "The Guardian U.S. politics and national reporting."
    },
    {
        "category": "Politics", "master_category": "National Headlines",
        "source": "HuffPost Politics",
        "url": "https://www.huffpost.com/section/politics/feed",
        "description": "HuffPost U.S. politics and policy coverage."
    },
    {
        "category": "Politics", "master_category": "National Headlines",
        "source": "Washington Examiner Politics",
        "url": "https://www.washingtonexaminer.com/section/politics/feed",
        "description": "Washington Examiner conservative political reporting."
    },
    # =========================================================================
    # 13. LOCAL NEWS, REGIONAL DISPATCHES & METRO EVENT WIRES
    # =========================================================================
    {
        "category": "Local News",
        "master_category": "Local News",
        "source": "Tampa Bay Times Local Wire",
        "url": "https://news.google.com/rss/search?q=Tampa+Bay+when:1d&hl=en-US&gl=US&ceid=US:en",
        "metro": "Tampa Bay, FL",
        "sub_category": "growth",
        "description": "Tampa Bay civic developments, regional transit, economic growth, and local headlines."
    },
    {
        "category": "Local News",
        "master_category": "Local News",
        "source": "Tampa Bay Events & Culture Wire",
        "url": "https://news.google.com/rss/search?q=%22Tampa%22+(festival+OR+market+OR+concert+OR+%22things+to+do%22+OR+art+OR+exhibition)+when:3d&hl=en-US&gl=US&ceid=US:en",
        "metro": "Tampa Bay, FL",
        "sub_category": "events",
        "description": "Tampa Bay weekend festivals, outdoor artisan markets, music performances, and community events."
    },
    {
        "category": "Local News",
        "master_category": "Local News",
        "source": "Tampa Bay Coastal & Environmental Wire",
        "url": "https://news.google.com/rss/search?q=%22Tampa+Bay%22+(estuary+OR+%22red+tide%22+OR+water+OR+beaches+OR+marine)+when:3d&hl=en-US&gl=US&ceid=US:en",
        "metro": "Tampa Bay, FL",
        "sub_category": "coast",
        "description": "Tampa Bay coastal ecology, environmental monitoring buoys, red tide tracking, and marine conservation."
    },
    {
        "category": "Local News",
        "master_category": "Local News",
        "source": "10 Tampa Bay (WTSP)",
        "url": "https://www.wtsp.com/feeds/syndication/rss/news/local",
        "metro": "Tampa Bay, FL",
        "sub_category": "growth",
        "description": "WTSP 10 Tampa Bay breaking local news, community reporting, and municipal updates."
    },
    {
        "category": "Local News",
        "master_category": "Local News",
        "source": "WFLA News Channel 8 Local",
        "url": "https://www.wfla.com/news/local-news/feed/",
        "metro": "Tampa Bay, FL",
        "sub_category": "growth",
        "description": "WFLA News Channel 8 local investigative and community news across Tampa, St. Petersburg, and Clearwater."
    },
    {
        "category": "Local News",
        "master_category": "Local News",
        "source": "FOX 13 Tampa Bay",
        "url": "https://www.fox13news.com/rss/local-news",
        "metro": "Tampa Bay, FL",
        "sub_category": "growth",
        "description": "FOX 13 Tampa Bay local reporting, community events, and Pinellas/Hillsborough updates."
    },
    {
        "category": "Local News",
        "master_category": "Local News",
        "source": "Central Florida & Orlando Wire",
        "url": "https://news.google.com/rss/search?q=%22Orlando%22+local+news+when:1d&hl=en-US&gl=US&ceid=US:en",
        "metro": "Orlando & Central FL",
        "sub_category": "growth",
        "description": "Central Florida regional transit, SunRail expansion, and Orlando municipal reporting."
    },
    {
        "category": "Local News",
        "master_category": "Local News",
        "source": "South Florida & Miami Wire",
        "url": "https://news.google.com/rss/search?q=%22Miami%22+local+news+when:1d&hl=en-US&gl=US&ceid=US:en",
        "metro": "Miami & South FL",
        "sub_category": "coast",
        "description": "Miami-Dade coastal resilience, stormwater management, and South Florida civic updates."
    },
]

INGESTION_SETTINGS = {
    "max_items_per_feed": 12,
    "feed_retention_limit": 150,
    "min_stories_per_category": 12,
    "feed_timeout_seconds": 12,
    "ai_timeout_seconds": 25,
    "max_workers": 12
}
