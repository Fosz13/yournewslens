# Your News Lens — Data Ingestion & Google News Integration Guide

## 1. Why Breaking Stories Weren't Showing Up
In previous versions, `engine.py` was only subscribed to 4 specific topical sub-feeds (`POLITICS`, `BUSINESS`, `SPORTS`, `TECHNOLOGY`), and fetched only 2 items per feed. 

When major breaking national stories break—such as the **Oregon elementary school shooting** or **Starlink battlefield restrictions in Ukraine**—Google News places them on the **Main Headlines**, **U.S. National (`NATION`)**, and **World (`WORLD`)** feeds. Because the scraper did not subscribe to those feeds, front-page breaking news was completely bypassed.

---

## 2. The New Google News Integration Architecture
`engine.py` has been re-architected with direct Google News front-page integration:

1. **Direct Google News Front-Page Feeds**:
   * **Google News Top Headlines (Breaking / Trending)**: `https://news.google.com/rss?hl=en-US&gl=US&ceid=US:en`
     *(This is the exact RSS feed powering the "Headlines" tab in the Google News mobile app).*
   * **Google News U.S. National News**: `https://news.google.com/rss/headlines/section/topic/NATION?hl=en-US&gl=US&ceid=US:en`
   * **Google News World News**: `https://news.google.com/rss/headlines/section/topic/WORLD?hl=en-US&gl=US&ceid=US:en`
   * Plus sub-topic feeds for Politics, Business, Tech, Sports, Associated Press, Reuters, and NPR.

2. **Expanded Feed Volume & Retention**:
   * Ingestion increased to **4 items per feed** across 10 feeds (up to 40 stories evaluated per 15-minute cycle).
   * Active feed capacity increased from **25 to 40 stories**.

3. **Smart Category Auto-Detection (`auto_detect_category`)**:
   * Headlines from the main trending feed are automatically classified into the appropriate category pill (`Sports`, `Economy & Inflation`, `Tech & Free Speech`, `Border & Security`, or `Politics`) so they appear under both "All" and topic-specific filters.

4. **Dynamic Publication Timers**:
   * Parses `<pubDate>` directly from the RSS feed into epoch timestamps (`pub_timestamp`).
   * A client-side JavaScript clock recalculates the elapsed time every 60 seconds (`"CNN • 1 hour ago"`, `"CNBC • 4 hours ago"`, `"ESPN Sports • 13 hours ago"`).

---

## 3. Deployment Instructions
1. Download `yournewslens_deploy.zip`.
2. Replace `engine.py`, `index.html`, and `data/stories.json` in your repository (`github.com/Fosz13/lenswire`).
3. In the **Actions** tab, trigger **Your News Lens 15-Minute News Update**.
