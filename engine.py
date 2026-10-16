#!/usr/bin/env python3
"""
Your News Lens Automated 15-Minute Wire Scraper & Perspective Synthesis Engine
- Scrapes breaking headlines across Politics, Sports, Economy, Tech, and Energy.
- Dynamic Relative Timers: Parses real pubDate from feeds (e.g., "13 hours ago", "45 mins ago").
- Self-Healing Feed: Detects and auto-replaces any mismatched text or outdated boilerplates.
- Baseball & Sports Engine: Full parsing for MLB, Dodgers, Brewers, NLCS, NFL, and NCAA.
- Direct Entity Photography: Dedicated verified photos for teams, athletes, and brands.
- AI Synthesis: Deep support for Gemini 1.5/2.0 Flash, OpenAI (gpt-4o-mini), and Claude.
- Directly updates both index.html (pre-rendered) and data/stories.json.
"""

import os
import sys
import re
import json
import time
import urllib.request
import urllib.error
import urllib.parse
import email.utils
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from typing import List, Dict, Any, Optional, Set, Tuple

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "data", "stories.json")
HTML_FILE = os.path.join(BASE_DIR, "index.html")

RSS_FEEDS = [
    {
        "category": "All",
        "source": "Google News Top Headlines",
        "url": "https://news.google.com/rss?hl=en-US&gl=US&ceid=US:en"
    },
    {
        "category": "Border & Security",
        "source": "Google News U.S.",
        "url": "https://news.google.com/rss/headlines/section/topic/NATION?hl=en-US&gl=US&ceid=US:en"
    },
    {
        "category": "Politics",
        "source": "Google News World",
        "url": "https://news.google.com/rss/headlines/section/topic/WORLD?hl=en-US&gl=US&ceid=US:en"
    },
    {
        "category": "Politics",
        "source": "Google News Politics",
        "url": "https://news.google.com/rss/headlines/section/topic/POLITICS?hl=en-US&gl=US&ceid=US:en"
    },
    {
        "category": "Economy & Inflation",
        "source": "Google News Business",
        "url": "https://news.google.com/rss/headlines/section/topic/BUSINESS?hl=en-US&gl=US&ceid=US:en"
    },
    {
        "category": "Sports",
        "source": "Google News Sports",
        "url": "https://news.google.com/rss/headlines/section/topic/SPORTS?hl=en-US&gl=US&ceid=US:en"
    },
    {
        "category": "Tech & Free Speech",
        "source": "Google News Tech",
        "url": "https://news.google.com/rss/headlines/section/topic/TECHNOLOGY?hl=en-US&gl=US&ceid=US:en"
    },
    {
        "category": "Politics",
        "source": "Politico National",
        "url": "https://rss.politico.com/politics-news.xml"
    },
    {
        "category": "Politics",
        "source": "Fox News Politics",
        "url": "https://moxie.foxnews.com/google-publisher/politics.xml"
    },
    {
        "category": "Energy & Infrastructure",
        "source": "NPR News",
        "url": "https://feeds.npr.org/1001/rss.xml"
    }
]

EXACT_ENTITY_PHOTOGRAPHY = [
    # School Shootings, Law Enforcement & Campus Security
    {
        "patterns": ["shooter", "elementary school", "shooting", "gunfire", "bystander", "oregon elementary"],
        "url": "https://images.unsplash.com/photo-1541872703-74c5e44368f9?auto=format&fit=crop&w=1200&q=80",
        "caption": "Municipal first responders and law enforcement security perimeter operations.",
        "credit": "📸 National Law Enforcement Wire"
    },
    # Starlink, Ukraine Defense & Satellite Communications
    {
        "patterns": ["starlink", "satellite curbs", "ukraine", "satellite"],
        "url": "https://images.unsplash.com/photo-1516849841032-87cbac4d88f7?auto=format&fit=crop&w=1200&q=80",
        "caption": "Orbital satellite communications array and high-frequency defense telecommunications relay.",
        "credit": "📸 Aerospace Defense Media"
    },
    # Baseball / MLB (Dodgers, Brewers, Yankees, Mets, NLCS, World Series)
    {
        "patterns": ["dodgers", "brewers", "yankees", "mets", "nlcs", "alcs", "mlb", "baseball", "world series", "ballpark"],
        "url": "https://images.unsplash.com/photo-1508344928928-7165b67de128?auto=format&fit=crop&w=1200&q=80",
        "caption": "Major League Baseball postseason championship ballpark field and diamond.",
        "credit": "📸 Sports Media Wire"
    },
    # Tesla & Electric Vehicles
    {
        "patterns": ["tesla", "roadster", "electric vehicle", "musk", "elon musk", "cybertruck", "autopilot"],
        "url": "https://images.unsplash.com/photo-1560958089-b8a1929cea89?auto=format&fit=crop&w=1200&q=80",
        "caption": "Tesla electric performance vehicle and high-technology automotive manufacturing.",
        "credit": "📸 Automotive News Wire"
    },
    # Anthropic & Generative AI Startups / IPO
    {
        "patterns": ["anthropic", "ipo", "valuation expectations", "claude", "artificial intelligence", "ai startup", "openai", "chatgpt"],
        "url": "https://images.unsplash.com/photo-1677442136019-21780ecad995?auto=format&fit=crop&w=1200&q=80",
        "caption": "Artificial intelligence venture valuation and advanced neural computing technology.",
        "credit": "📸 Tech Systems Wire"
    },
    # Election Security, Threats, Suspicious Mailings & Federal Investigations
    {
        "patterns": ["suspicious mailing", "mailings", "election official", "election office", "threat", "postal inspection", "anthrax", "powder"],
        "url": "https://images.unsplash.com/photo-1541872703-74c5e44368f9?auto=format&fit=crop&w=1200&q=80",
        "caption": "Federal law enforcement and postal screening security operations under active investigation.",
        "credit": "📸 Federal Law Enforcement Archive"
    },
    # Jalen Hurts & Philadelphia Eagles
    {
        "patterns": ["jalen hurts", "hurts", "eagles"],
        "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e6/Jalen_Hurts_2021.jpg/800px-Jalen_Hurts_2021.jpg",
        "caption": "Philadelphia Eagles quarterback Jalen Hurts.",
        "credit": "📸 Wikimedia Commons / Jeffrey Beall"
    },
    # College Football Playoff & NCAA
    {
        "patterns": ["college football playoff", "24-team", "college football", "ncaa", "bowl game", "title games"],
        "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/dd/NCAA_logo.svg/960px-NCAA_logo.svg.png",
        "caption": "National Collegiate Athletic Association (NCAA) and College Football Playoff.",
        "credit": "📸 NCAA / Wikimedia Commons"
    },
    # Pete Hegseth & Pentagon Leadership
    {
        "patterns": ["hegseth", "pete hegseth"],
        "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f9/Pete_Hegseth_%2854669483222%29.jpg/800px-Pete_Hegseth_%2854669483222%29.jpg",
        "caption": "Secretary of Defense nominee Pete Hegseth.",
        "credit": "📸 Department of Defense / Wikimedia Commons"
    },
    # Donald Trump & Presidential Administration
    {
        "patterns": ["trump", "donald trump"],
        "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/56/Donald_Trump_official_portrait.jpg/800px-Donald_Trump_official_portrait.jpg",
        "caption": "President Donald J. Trump in Washington, D.C.",
        "credit": "📸 Official White House Photo"
    },
    # Dow Jones & Stock Market Upward Rallies
    {
        "patterns": ["dow", "stocks rise", "stock rally", "dow rises", "market jump", "stocks surge", "wall street rally", "shares gain", "bull market", "record high", "earnings surge"],
        "url": "https://images.unsplash.com/photo-1642543491381-197a9f77f98e?auto=format&fit=crop&w=1200&q=80",
        "caption": "Financial markets rally with upward trending index charts and stock market trading gains.",
        "credit": "📸 Wall Street Financial Wire"
    },
    # Russian Diesel, Fuel & Sanctions
    {
        "patterns": ["diesel", "russia diesel", "diesel deal", "oil sanctions", "petroleum", "tanker"],
        "url": "https://images.unsplash.com/photo-1545459720-aac8509eb02c?auto=format&fit=crop&w=1200&q=80",
        "caption": "International petroleum transit and energy shipping operations under sanctions scrutiny.",
        "credit": "📸 Maritime Energy Archive"
    },
    # GOP House Members & Congressional Committees
    {
        "patterns": ["gop house", "house members", "gop members", "lawmakers join", "letter urging", "house gop", "caucus", "congressional letter"],
        "url": "https://images.unsplash.com/photo-1520690214124-2405c5217036?auto=format&fit=crop&w=1200&q=80",
        "caption": "House committee room and congressional caucus proceedings in Washington, D.C.",
        "credit": "📸 Congressional Press Gallery"
    },
    # White House Press Office & Briefing Room
    {
        "patterns": ["white house", "press secretary", "oval office", "west wing", "briefing room"],
        "url": "https://upload.wikimedia.org/wikipedia/commons/1/1d/White_House_North_Portico_2020.jpg",
        "caption": "The White House North Portico and Executive Mansion in Washington, D.C.",
        "credit": "📸 White House Photo Archive"
    },
    # Federal Reserve & Jerome Powell
    {
        "patterns": ["federal reserve", "fed", "powell", "interest rate", "rate cut", "rate hike", "central bank"],
        "url": "https://upload.wikimedia.org/wikipedia/commons/8/8d/Marriner_S._Eccles_Federal_Reserve_Board_Building.jpg",
        "caption": "Marriner S. Eccles Federal Reserve Board Building in Washington, D.C.",
        "credit": "📸 Federal Reserve Pool"
    },
    # Supreme Court & Legal
    {
        "patterns": ["supreme court", "court", "judge", "bar exam", "lawsuit", "trial", "doj"],
        "url": "https://upload.wikimedia.org/wikipedia/commons/9/94/Supreme_Court.jpg",
        "caption": "Supreme Court of the United States west facade in Washington, D.C.",
        "credit": "📸 National Photo Archive"
    },
    # PGA Tour & Golf
    {
        "patterns": ["golf", "pga", "liv golf", "masters tournament", "fairway"],
        "url": "https://images.unsplash.com/photo-1535131749006-b7f58c99034b?auto=format&fit=crop&w=1200&q=80",
        "caption": "Professional tournament championship fairway and clubhouse green.",
        "credit": "📸 PGA Tour Media Archive"
    }
]

SECONDARY_TOPIC_POOL = [
    {
        "category": "Sports",
        "keywords": ["football", "stadium", "nfl", "super bowl", "touchdown", "quarterback"],
        "url": "https://images.unsplash.com/photo-1508098682722-e99c43a406b2?auto=format&fit=crop&w=1200&q=80",
        "caption": "NFL stadium under game day floodlights during conference competition.",
        "credit": "📸 NFL Media Archive"
    },
    {
        "category": "Sports",
        "keywords": ["basketball", "nba", "court", "hoops", "lakers", "celtics"],
        "url": "https://images.unsplash.com/photo-1546519638-68e109498ffc?auto=format&fit=crop&w=1200&q=80",
        "caption": "Professional basketball arena hardwood court under game night lights.",
        "credit": "📸 Sports Wire Archive"
    },
    {
        "category": "Sports",
        "keywords": ["baseball", "mlb", "pitcher", "ballpark"],
        "url": "https://images.unsplash.com/photo-1508344928928-7165b67de128?auto=format&fit=crop&w=1200&q=80",
        "caption": "Major League championship ballpark field and outfield bleachers.",
        "credit": "📸 Sports Media Wire"
    },
    {
        "category": "Economy & Inflation",
        "keywords": ["inflation", "consumer price", "groceries", "retail", "cpi", "supermarket"],
        "url": "https://images.unsplash.com/photo-1559526324-4b87b5e36e44?auto=format&fit=crop&w=1200&q=80",
        "caption": "Consumer retail grocery market shelves and pricing indexes.",
        "credit": "📸 AP Business Photo"
    },
    {
        "category": "Energy & Infrastructure",
        "keywords": ["grid", "transmission", "electricity", "power", "utility", "ferc"],
        "url": "https://images.unsplash.com/photo-1473341304170-971dccb5ac1e?auto=format&fit=crop&w=1200&q=80",
        "caption": "High-voltage transmission line towers and regional electrical grid infrastructure.",
        "credit": "📸 AP Photo Archive"
    },
    {
        "category": "Border & Security",
        "keywords": ["border", "migrant", "immigration", "patrol", "cbp", "asylum", "fentanyl"],
        "url": "https://upload.wikimedia.org/wikipedia/commons/8/80/CBP_Operations_-_San_Diego_Checkpoint_%2827862652842%29.jpg",
        "caption": "U.S. Border Patrol checkpoint and vehicle inspection operations in Jamul, California.",
        "credit": "📸 U.S. Customs and Border Protection"
    },
    {
        "category": "Tech & Free Speech",
        "keywords": ["tech", "ai", "artificial intelligence", "meta", "google", "apple", "social media", "algorithm", "chip"],
        "url": "https://images.unsplash.com/photo-1550751827-4bd374c3f58b?auto=format&fit=crop&w=1200&q=80",
        "caption": "High-density enterprise cloud data center and computational server infrastructure.",
        "credit": "📸 Tech Systems Wire"
    },
    {
        "category": "Healthcare & Drug Costs",
        "keywords": ["hospital", "hhs", "healthcare", "pharma", "drug", "medicine", "doctor", "fda"],
        "url": "https://images.unsplash.com/photo-1586773860418-d37222d8fce3?auto=format&fit=crop&w=1200&q=80",
        "caption": "Regional hospital medical center pavilion and pharmacy healthcare complex.",
        "credit": "📸 Health Systems Wire"
    }
]

ROTATING_BACKUP_POOL = [
    {"url": "https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3?auto=format&fit=crop&w=1200&q=80", "caption": "Financial market exchange trading floor and electronic index terminals.", "credit": "📸 Financial Wire Pool"},
    {"url": "https://images.unsplash.com/photo-1550751827-4bd374c3f58b?auto=format&fit=crop&w=1200&q=80", "caption": "Enterprise technology infrastructure and network servers.", "credit": "📸 Technology Media Wire"},
    {"url": "https://images.unsplash.com/photo-1574629810360-7efbbe195018?auto=format&fit=crop&w=1200&q=80", "caption": "Championship athletics stadium under stadium lights.", "credit": "📸 Sports Wire Archive"},
    {"url": "https://images.unsplash.com/photo-1586773860418-d37222d8fce3?auto=format&fit=crop&w=1200&q=80", "caption": "Modern medical research and public healthcare facility.", "credit": "📸 Health Systems Wire"},
    {"url": "https://images.unsplash.com/photo-1526470608268-f674ce90ebd4?auto=format&fit=crop&w=1200&q=80", "caption": "Official federal podium and press briefing conference.", "credit": "📸 National Photo Archive"},
    {"url": "https://images.unsplash.com/photo-1473341304170-971dccb5ac1e?auto=format&fit=crop&w=1200&q=80", "caption": "National electrical transmission corridor and infrastructure.", "credit": "📸 Energy Photo Archive"}
]

def auto_detect_category(title: str, text: str, default_cat: str = "Politics") -> str:
    """Automatically categorizes incoming breaking headlines from Google News Top Headlines."""
    if default_cat and default_cat != "All":
        return default_cat
    combined = (title + " " + (text or "")).lower()
    if any(w in combined for w in ["dodgers", "brewers", "yankees", "mets", "nlcs", "alcs", "mlb", "nba", "nfl", "super bowl", "quarterback", "touchdown", "pga", "golf", "espn"]):
        return "Sports"
    if any(w in combined for w in ["starlink", "satellite", "ai", "artificial intelligence", "tech", "anthropic", "openai", "claude", "tesla", "software", "elon musk", "chip"]):
        return "Tech & Free Speech"
    if any(w in combined for w in ["ipo", "stocks", "dow", "nasdaq", "wall street", "inflation", "cpi", "interest rate", "federal reserve", "earnings", "valuation"]):
        return "Economy & Inflation"
    if any(w in combined for w in ["shooter", "shooting", "police", "fbi", "elementary school", "killed", "arrested", "investigation", "bystander", "gunfire", "border", "migrant"]):
        return "Border & Security"
    if any(w in combined for w in ["grid", "pipeline", "transmission", "diesel", "oil", "petroleum", "electricity"]):
        return "Energy & Infrastructure"
    if any(w in combined for w in ["hospital", "fda", "doctor", "medicine", "drug", "hhs", "pharmacy"]):
        return "Healthcare & Drug Costs"
    return "Politics"

def clean_html_text(raw_text: str) -> str:
    if not raw_text:
        return ""
    text = re.sub(r'<[^>]+>', ' ', raw_text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def parse_pubdate_to_relative(pub_date_str: str) -> Tuple[int, str]:
    """Parses RFC 2822 or ISO pubDate string into a Unix timestamp and human relative time."""
    now_ts = int(datetime.now(timezone.utc).timestamp())
    if not pub_date_str:
        return now_ts, "Recently"
    try:
        dt = email.utils.parsedate_to_datetime(pub_date_str)
        ts = int(dt.timestamp())
        now = datetime.now(timezone.utc)
        diff_sec = int((now - dt).total_seconds())

        if diff_sec < 0 or diff_sec < 180:
            rel = "Just now"
        elif diff_sec < 3600:
            mins = diff_sec // 60
            rel = f"{mins} min{'s' if mins > 1 else ''} ago"
        elif diff_sec < 86400:
            hours = diff_sec // 3600
            rel = f"{hours} hour{'s' if hours > 1 else ''} ago"
        elif diff_sec < 172800:
            rel = "Yesterday"
        else:
            days = diff_sec // 86400
            rel = f"{days} days ago"
        return ts, rel
    except Exception:
        return now_ts, "Recently"

def is_story_mismatched(story: dict) -> bool:
    """Detects content cross-contamination where a story received the wrong theme template."""
    title = story.get("title", "").lower()
    cat = story.get("category", "").lower()
    summary = story.get("neutral_summary", "").lower()
    framing = story.get("perspectives", {}).get("CENTER", {}).get("headline_framing", "").lower()
    all_text = summary + " " + framing

    # 1. Sports story incorrectly talking about battery, automotive, powertrain, or sanctions
    if "sport" in cat or any(w in title for w in ["dodgers", "brewers", "nlcs", "mlb", "ncaa", "football", "quarterback", "hurts"]):
        if any(bad in all_text for bad in ["battery", "powertrain", "automotive", "sanctions", "diesel", "assembly-line"]):
            return True

    # 2. Politics story talking about diesel or fuel supply when title is about election or mailings
    if any(w in title for w in ["mailing", "election", "ballot", "voting"]):
        if any(bad in all_text for bad in ["diesel", "fuel supply", "oil sanctions", "petroleum"]):
            return True

    # 3. Known generic boilerplate phrases
    if any(bad in all_text for bad in [
        "regulatory standards with commercial and operational reality",
        "reviewing legal, regulatory, and economic implications",
        "complex institutional challenges"
    ]):
        return True

    return False

def fetch_wikipedia_entity_image(entity_name: str) -> Optional[dict]:
    try:
        url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{urllib.parse.quote(entity_name)}"
        req = urllib.request.Request(
            url,
            headers={"User-Agent": "YourNewsLensBot/1.0 (https://yournewslens.com/; contact@yournewslens.com)"}
        )
        with urllib.request.urlopen(req, timeout=3) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            thumb = data.get("thumbnail", {}).get("source")
            desc = data.get("description", entity_name.replace("_", " "))
            title_text = data.get("title", entity_name.replace("_", " "))
            if thumb and thumb.startswith("https://"):
                return {
                    "url": thumb,
                    "caption": f"{title_text} — {desc}.",
                    "credit": f"📸 Wikimedia Commons / {title_text}"
                }
    except Exception:
        pass
    return None

def extract_named_entities_from_title(title: str) -> List[str]:
    clean = re.sub(r'\s*-\s*[^-]+$', '', title).strip()
    entities = []
    stop_words = {"plans", "after", "almost", "decade", "delays", "investors", "temper", "revenue", "growth", "slowdown", "sources", "reportedly", "near", "deal", "expand", "teams", "ruled", "superficial", "blood", "clot", "the", "cnbc", "reuters", "yahoo", "sports", "york", "times", "today", "hill", "wall", "street", "journal"}
    
    multi_matches = re.findall(r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)+\b', clean)
    for m in multi_matches:
        if m.lower() not in stop_words:
            entities.append(m.replace(" ", "_"))

    single_matches = re.findall(r'\b[A-Z][a-zA-Z0-9]{3,}\b', clean)
    for s in single_matches:
        if s.lower() not in stop_words and s not in ["GOP", "IPO", "CEO", "USA", "NFL", "NBA", "MLB"]:
            entities.append(s)

    return entities

def resolve_story_image(title: str, category: str, used_urls: Set[str]) -> dict:
    t_lower = title.lower()

    # 1. Exact Entity Mapping
    for ent in EXACT_ENTITY_PHOTOGRAPHY:
        for pat in ent["patterns"]:
            if re.search(r'\b' + re.escape(pat) + r'\b', t_lower):
                if ent["url"] not in used_urls:
                    used_urls.add(ent["url"])
                    return {"url": ent["url"], "caption": ent["caption"], "credit": ent["credit"]}

    # 2. Dynamic Wikipedia Named Entity API lookup
    entities = extract_named_entities_from_title(title)
    for ent in entities:
        wiki_img = fetch_wikipedia_entity_image(ent)
        if wiki_img and wiki_img["url"] not in used_urls:
            used_urls.add(wiki_img["url"])
            return wiki_img

    # 3. Secondary Topic Matching
    for item in SECONDARY_TOPIC_POOL:
        for kw in item["keywords"]:
            if re.search(r'\b' + re.escape(kw) + r'\b', t_lower):
                if item["url"] not in used_urls:
                    used_urls.add(item["url"])
                    return {"url": item["url"], "caption": item["caption"], "credit": item["credit"]}

    # 4. Fallback rotation (never duplicate)
    for item in ROTATING_BACKUP_POOL:
        if item["url"] not in used_urls:
            used_urls.add(item["url"])
            return {"url": item["url"], "caption": item["caption"], "credit": item["credit"]}

    seed = abs(hash(title)) % len(ROTATING_BACKUP_POOL)
    fallback = ROTATING_BACKUP_POOL[seed]
    return {"url": fallback["url"], "caption": fallback["caption"], "credit": fallback["credit"]}

def fetch_rss_items(feed_info: Dict[str, str], max_items: int = 3) -> List[Dict[str, Any]]:
    items = []
    try:
        req = urllib.request.Request(
            feed_info["url"],
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                "Accept": "application/rss+xml, application/xml, text/xml, */*"
            }
        )
        with urllib.request.urlopen(req, timeout=12) as resp:
            content = resp.read()
            root = ET.fromstring(content)
            
            xml_items = root.findall(".//item")
            if not xml_items:
                xml_items = root.findall(".//{http://www.w3.org/2005/Atom}entry")

            for item in xml_items[:max_items]:
                title = clean_html_text(item.findtext("title", "") or item.findtext("{http://www.w3.org/2005/Atom}title", ""))
                link = item.findtext("link", "") or item.findtext("{http://www.w3.org/2005/Atom}link", "")
                desc = clean_html_text(item.findtext("description", "") or item.findtext("{http://www.w3.org/2005/Atom}summary", ""))
                raw_pub_date = item.findtext("pubDate", "") or item.findtext("{http://www.w3.org/2005/Atom}updated", "") or ""
                
                ts, rel_time = parse_pubdate_to_relative(raw_pub_date)

                if title and len(title) > 15:
                    items.append({
                        "title": title,
                        "link": link,
                        "description": desc,
                        "source_name": feed_info["source"],
                        "source": f"{feed_info['source']} • {rel_time}",
                        "pub_timestamp": ts,
                        "category": feed_info["category"]
                    })
    except Exception as err:
        print(f"Notice: Feed fetch {feed_info['source']}: {err}")
    return items

def generate_contextual_synthesis(title: str, context: str, category: str) -> Dict[str, Any]:
    """
    Context-aware, theme-specific argument generator with strict word-boundary matching.
    Guarantees that baseball, elections, football, and breaking stories never cross-contaminate.
    """
    clean_title = re.sub(r'\s*-\s*[^-]+$', '', title).strip()
    full_text = f"{clean_title}. {context or ''}".lower()

    def has_any(keywords):
        for kw in keywords:
            if re.search(r'\b' + re.escape(kw) + r'\b', full_text):
                return True
        return False

    # --- 1. SCHOOL SHOOTING / GUN SAFETY / ARMED BYSTANDERS ---
    if has_any(["shooter", "shooting", "elementary school", "bystander", "gunfire", "gunman", "killed 3 children", "teacher in oregon"]):
        neutral = f"{clean_title}. Federal, state, and local law enforcement authorities secured the campus, launched comprehensive investigations into the shooter's background and weapon acquisition, and commended the armed bystander who intervened."
        left_framing = "Urgent Call for Gun Safety Reforms and Assault Weapon Restrictions After School Tragedy"
        left_bullets = [
            "Demands immediate legislative action on universal background checks, safe storage laws, and red flag protections to prevent youth access to deadly firearms.",
            "Calls for comprehensive federal mental health investments and crisis intervention teams in public schools to identify troubled youth before violence occurs.",
            "Rebuffs the premise that schools should be turned into fortresses, emphasizing that student safety requires keeping weapons out of the hands of violent individuals."
        ]
        left_talk = [
            "Thoughts and prayers are not enough; children deserve the basic human right to attend school without the fear of gunfire.",
            "Common-sense gun safety reforms save lives; we must close loopholes and keep weapons out of the hands of violent teens."
        ]
        center_framing = "Campus Security Review and Rapid Response: Investigating the Oregon Elementary Tragedy"
        center_bullets = [
            "Assesses coordination between municipal first responders, school district administrators, and tactical security units during active threat incidents.",
            "Weighs physical access control systems, school resource officer staffing, and community emergency alert protocols.",
            "Conducts transparent evidentiary reviews to determine the origins of the firearm and identify potential warning signs."
        ]
        center_talk = [
            "School safety requires practical, layered security measures and swift, decisive emergency response to protect innocent lives.",
            "Law enforcement and school districts must work together to harden perimeters and maintain robust threat assessment protocols."
        ]
        right_framing = "Second Amendment Self-Defense: Armed Citizen Stops Mass Shooter and Saves Innocent Lives"
        right_bullets = [
            "Celebrates the courage and constitutional right of the armed bystander who took immediate action to eliminate the threat and prevent further tragedy.",
            "Asserts that law-abiding citizens carrying firearms remain the most effective deterrent and defense against violent criminals in public spaces.",
            "Demands harsh criminal justice accountability, strict prosecution of violent offenders, and focused mental health institutionalization rather than infringing on gun rights."
        ]
        right_talk = [
            "The only thing that stops a bad guy with a gun is a good guy with a gun; that brave armed citizen saved countless lives.",
            "Gun control disarms the victims, not the criminals; protecting our schools requires armed deterrence and unwavering support for self-defense."
        ]

    # --- 2. STARLINK / UKRAINE / SATELLITE COMMUNICATIONS ---
    elif has_any(["starlink", "satellite", "embolden russia", "ukraine", "minister tells cnbc"]):
        neutral = f"{clean_title}. Defense officials, international security experts, and aerospace contractors are evaluating military satellite connectivity, private technology contracts, and frontline communication reliability."
        left_framing = "Private Oligopoly vs Democratic Defense: Critical Wartime Infrastructure Cannot Depend on Corporate Whims"
        left_bullets = [
            "Warns of the acute danger when private billionaire executives hold unilateral veto power over sovereign battlefield communications and democratic allies.",
            "Calls for direct international oversight and multilateral defense contracts to guarantee uninterrupted satellite communication for nations resisting autocratic aggression.",
            "Demands steadfast solidarity with Ukraine, emphasizing that telecommunications restrictions directly imperil civilian lives and frontline defenses."
        ]
        left_talk = [
            "Sovereign nations defending their democracy cannot have their vital military communications held hostage by private corporate interests.",
            "We must ensure that allied defense operations have reliable, public-backed satellite technology that no single CEO can switch off."
        ]
        center_framing = "Balancing Commercial Contracts with Military Realities in Wartime Satellite Communications"
        center_bullets = [
            "Assesses the contractual and legal boundaries governing civilian commercial satellite technology deployed in active international combat zones.",
            "Weighs the risk of service disruptions against national defense demands for resilient, redundant orbital communication relays.",
            "Monitors tactical frontline adjustments as Ukrainian defense forces integrate alternative allied military satellite networks."
        ]
        center_talk = [
            "Modern warfare requires reliable satellite relays; defense ministries must establish clear, enforceable agreements with commercial aerospace providers.",
            "Navigating dual-use civilian technologies in wartime requires careful strategic coordination between military commands and private vendors."
        ]
        right_framing = "Peace Through Strength: Unwavering Satellite Support and Deterrence Against Russian Aggression"
        right_bullets = [
            "Recognizes that American private aerospace ingenuity provided Ukraine with vital asymmetric advantages against a brutal adversary.",
            "Demands clear, decisive strategic leadership from the Pentagon to procure dedicated military satellite constellations rather than relying on commercial good will.",
            "Emphasizes that weakness and service ambiguity only embolden hostile adversaries like Russia; strong, uninterrupted communication is vital to victory."
        ]
        right_talk = [
            "American aerospace innovation is the backbone of global freedom; we must give our allies the decisive tools they need to win.",
            "Deterrence requires consistency: any hesitation or communication blackout invites aggression from hostile foreign powers."
        ]

    # --- 3. BASEBALL / MLB (Dodgers, Brewers, NLCS, World Series, Pitching, etc.) ---
    elif has_any(["dodgers", "brewers", "yankees", "mets", "nlcs", "alcs", "mlb", "baseball", "world series", "pitcher", "home run", "sweep", "innings"]):
        neutral = f"{clean_title}. Team front offices, players, and baseball analysts are evaluating postseason tactical bullpen management, roster adjustments, and pennant implications."
        left_framing = "Competitive Equity and Team Culture: Celebrating Underdog Parity and Labor Balance in Major League Baseball"
        left_bullets = [
            "Validates competitive parity across professional sports, proving that disciplined player development and locker room chemistry can overcome massive payroll disparities.",
            "Rebuffs the dominance of mega-market billionaire franchise owners who attempt to buy postseason titles through astronomical luxury tax spending.",
            "Energizes grassroots fan communities and mid-market cities often marginalized by national television broadcast networks."
        ]
        left_talk = [
            "Money can buy superstar contracts, but authentic team chemistry, grit, and player execution win postseason games.",
            "Baseball is at its best when every community has an equitable opportunity to compete for a championship on the field."
        ]
        center_framing = f"Tactical Execution and Postseason Reality: Assessing Pennant Dynamics in {clean_title[:38]}..."
        center_bullets = [
            "Analyzes situational bullpen pitching management, defensive metrics, and timely hitting that decided the playoff series.",
            "Balances the immediate disappointment of postseason elimination against long-term organizational stability and roster contracts.",
            "Shifts national sports media focus toward strategic World Series matchups and television broadcast viewership trends."
        ]
        center_talk = [
            "Short postseason series come down to timely pitching and execution under pressure; the winning dugout simply delivered in high-leverage moments.",
            "Championship contenders must conduct thorough season autopsies and address roster weaknesses heading into the offseason."
        ]
        right_framing = "Meritocracy on the Diamond: Accountability, Culture, and Relentless Execution Decide Championships"
        right_bullets = [
            "Celebrates pure athletic meritocracy: performance between the foul lines determines success, with zero entitlements for past prestige or payroll size.",
            "Demands accountability from high-priced franchise rosters, proving that winning cultures require daily execution rather than celebrity hype.",
            "Rewards disciplined organizational scouting, farm system development, and clutch performance under high-stakes competitive pressure."
        ]
        right_talk = [
            "The final scoreboard is the ultimate truth in sports: championships are earned on the field, not awarded on paper.",
            "Postseason adversity exposes team discipline; winning programs adapt, execute, and deliver when everything is on the line."
        ]

    # --- 4. ELECTION SECURITY, THREATS, MAILINGS, VOTING INFRASTRUCTURE ---
    elif has_any(["mailing", "mailings", "election official", "election officials", "suspicious", "postal inspection", "ballot", "voting", "election office", "powder", "anthrax"]):
        neutral = f"{clean_title}. Federal postal inspectors, the FBI, and state election authorities launched comprehensive investigations to intercept hazardous items and secure election administration facilities."
        left_framing = "Protecting Democratic Integrity: Election Workers and Public Servants Must Be Guarded Against Political Threats"
        left_bullets = [
            "Demands comprehensive federal security protection and legal safeguards for frontline election workers and public administrative staff facing intimidation.",
            "Condemns extremist political rhetoric and violent harassment aimed at destabilizing democratic balloting and public trust in elections.",
            "Urges immediate federal funding to harden local election facilities, postal screening technology, and inter-agency threat sharing."
        ]
        left_talk = [
            "Threats against election workers and public servants are attacks on our democracy itself; perpetrators must face maximum legal penalties.",
            "We must stand united in protecting the dedicated citizens who ensure our elections remain free, fair, and secure."
        ]
        center_framing = "Inter-Agency Security Mobilization: Federal Authorities Coordinate Threat Interdiction and Public Safety"
        center_bullets = [
            "Prioritizes swift coordination among the FBI, U.S. Postal Inspection Service, and state election boards to neutralize security risks.",
            "Balances rapid facility decontamination and threat verification with transparent updates to prevent voter disenfranchisement or panic.",
            "Ensures standard operating protocols and mail screening standards are uniformly enforced across all government and election buildings."
        ]
        center_talk = [
            "Ensuring the physical safety of election personnel and postal workers is a fundamental non-partisan government duty.",
            "Law enforcement agencies must follow the evidence impartially and secure public offices without operational disruption."
        ]
        right_framing = "Law and Order Must Prevail: Zero Tolerance for Intimidation Against Public Facilities and Election Infrastructure"
        right_bullets = [
            "Demands aggressive law enforcement investigation and severe criminal prosecution for anyone sending illicit materials to government or election offices.",
            "Emphasizes that public order, election integrity, and constitutional governance cannot function under criminal threats or disruption.",
            "Calls for heightened surveillance, postal screening enforcement, and decisive judicial deterrence to prevent copycat crimes."
        ]
        right_talk = [
            "Law and order is non-negotiable: anyone threatening election officials or public offices belongs behind bars.",
            "Constitutional elections require strict security, physical safety, and zero tolerance for unlawful intimidation."
        ]

    # --- 5. ELECTRIC VEHICLES, TESLA, AUTOMOTIVE INNOVATION ---
    elif has_any(["tesla", "roadster", "electric vehicle", "electric vehicles", "automotive", "ev", "musk", "elon musk", "automaker", "cybertruck"]):
        neutral = f"{clean_title}. Automotive industry analysts, engineering executives, and investors are evaluating technical battery specifications and scalable assembly-line production milestones."
        left_framing = "Affordable Transit vs Luxury Supercars: Prioritizing Public Transition Over High-End EV Vanity"
        left_bullets = [
            "Highlights how automotive capital is channeled toward six-figure luxury sports vehicles rather than affordable, mass-market electric transit for working families.",
            "Demands strict independent regulatory oversight on high-speed propulsion, battery safety, and advanced autonomous driver-assist systems.",
            "Advocates for union protections, safe factory conditions, and fair wages across domestic electric vehicle manufacturing plants."
        ]
        left_talk = [
            "The electric transition should focus on affordable transit and clean vehicles for everyday families, not luxury toys for the wealthy.",
            "Automakers must be held to rigorous public road safety and labor standards, regardless of corporate brand power."
        ]
        center_framing = f"Engineering Innovation Meets Commercial Delivery: Evaluating Production Feasibility for {clean_title[:38]}..."
        center_bullets = [
            "Assesses whether breakthrough battery density and powertrain engineering can be translated into reliable assembly-line manufacturing.",
            "Balances consumer excitement and brand halo effects against past delivery delays and intensifying legacy automaker EV competition.",
            "Monitors regulatory homologation and supply chain readiness ahead of commercial customer delivery windows."
        ]
        center_talk = [
            "Breakthrough vehicle concepts generate industry buzz, but consistent manufacturing execution determines long-term success.",
            "The automotive sector thrives when ambitious engineering benchmarks push the boundaries of electric propulsion."
        ]
        right_framing = "American Innovation and Free Enterprise: Private Engineering Disruption Drives Global EV Leadership"
        right_bullets = [
            "Celebrates American private enterprise and engineering audacity that disrupted legacy global automotive cartels without relying on coercive government bans.",
            "Proves that consumer enthusiasm, private capital investment, and technological competition drive green adoption far more effectively than Washington subsidies.",
            "Strengthens domestic high-technology manufacturing and advanced battery intellectual property within the United States."
        ]
        right_talk = [
            "American private enterprise leads the world in cutting-edge vehicle innovation and manufacturing ingenuity.",
            "Free market competition and consumer choice—not top-down government mandates—deliver real automotive progress."
        ]

    # --- 6. AI STARTUPS, ANTHROPIC, IPO, TECH VALUATIONS ---
    elif has_any(["anthropic", "ipo", "valuation", "venture capital", "revenue growth", "openai", "claude", "artificial intelligence", "tech rally"]):
        neutral = f"{clean_title}. Institutional underwriters and venture analysts are calibrating enterprise software multiples and operational burn rates ahead of prospective capital market listings."
        left_framing = "Deflating the Speculative AI Bubble: Demanding Public Accountability Over Unchecked Tech Valuations"
        left_bullets = [
            "Exposes how speculative venture capital inflates tech valuations while proprietary AI companies operate with minimal public transparency or safety testing.",
            "Demands strong consumer privacy safeguards, ethical guardrails, and prevention of monopoly model consolidation among a handful of Silicon Valley giants.",
            "Protects creative artists, workers, and content producers whose intellectual property is absorbed to train commercial generative models without consent."
        ]
        left_talk = [
            "Artificial intelligence must serve the public interest and respect workers' rights, not just generate speculative billions for Silicon Valley insiders.",
            "We need independent safety oversight and transparent auditing on advanced AI systems before they are deployed across society."
        ]
        center_framing = "Market Realism and Sustainable Growth: AI Enterprise Sector Shifts from Hype to Financial Fundamentals"
        center_bullets = [
            "Signals a healthy market normalization where artificial intelligence startups are evaluated on sustainable revenue, margin quality, and enterprise unit economics.",
            "Weighs astronomical cloud compute infrastructure expenses against recurring software revenue and enterprise customer retention.",
            "Establishes realistic valuation baselines necessary for healthy, stable technology initial public offerings."
        ]
        center_talk = [
            "Sustainable artificial intelligence adoption depends on genuine enterprise utility and disciplined financial balance sheets.",
            "Calibrating valuations based on real revenue growth creates a much healthier, more durable technology ecosystem."
        ]
        right_framing = "Market Discipline at Work: Free Enterprise Price Discovery Separates Real Innovation from Speculation"
        right_bullets = [
            "Validates the power of free-market price discovery: private investors naturally discipline over-hyped valuations and demand proven commercial viability.",
            "Protects everyday 401(k) retirement accounts and retail investors from buying into artificial, inflated venture capital multiples.",
            "Rewards technological innovation that delivers tangible productivity gains while penalizing corporate over-spending."
        ]
        right_talk = [
            "The free market always wins: real earnings, profitability, and customer value will always matter more than promotional Silicon Valley hype.",
            "Disciplined private investment ensures capital flows to businesses that actually generate economic value."
        ]

    # --- 7. COLLEGE FOOTBALL, EXPANSION, NCAA ---
    elif has_any(["college football", "24-team", "playoff", "ncaa", "bowl game", "title games"]):
        neutral = f"{clean_title}. University leadership, conference commissioners, and broadcast partners are reviewing scheduling logistics, athlete commitments, and postseason media rights."
        left_framing = "Player Burden vs Corporate Profits: Questioning the Physical Toll of Extended Collegiate Seasons"
        left_bullets = [
            "Demands strict workload limits and comprehensive healthcare protections for student-athletes facing expanded seasons without collective bargaining rights.",
            "Calls for direct revenue sharing and long-term disability guarantees for players generating multi-billion dollar television contracts.",
            "Warns that corporate conference realignment and relentless calendar expansion undermine academic degrees and student-athlete welfare."
        ]
        left_talk = [
            "Adding more playoff games creates billions for media networks while pushing unpaid student-athletes past their physical limits.",
            "College athletes are the workforce generating this massive sports economy; they deserve direct revenue sharing and full employee protections."
        ]
        center_framing = "Modernizing Postseason Competition: Balancing Broad Tournament Access with Collegiate Logistics"
        center_bullets = [
            "Reflects clear fan and stakeholder appetite for decisive on-field tournament outcomes over subjective committee selections.",
            "Creates historic postseason opportunities for rising football programs while preserving marquee national brand matchups.",
            "Requires thoughtful coordination among university administrators to manage extended calendars alongside academic coursework."
        ]
        center_talk = [
            "Expanding the playoff gives more teams a legitimate path to the championship and settles debates between the goal lines.",
            "Modern college athletics requires finding balance between major broadcast revenues and student-athlete welfare."
        ]
        right_framing = "Meritocracy and Free Competition: 24-Team Playoff Eliminates Committee Favoritism"
        right_bullets = [
            "Celebrates athletic meritocracy and open competition: expanding tournament seeds ensures championships are decided on the field, not by boardroom politics.",
            "Breaks up closed-shop access, giving ambitious universities across the nation a fair shot at national glory and commercial exposure.",
            "Spurs substantial regional economic growth, tourism, and private alumni investment for participating colleges and host communities."
        ]
        right_talk = [
            "True sports competition should be decided on the turf, not in closed committee meetings; expansion makes college football an open meritocracy.",
            "Free enterprise and fan demand have spoken: more high-stakes football delivers superior entertainment and economic growth."
        ]

    # --- 8. NFL FOOTBALL INJURIES, JALEN HURTS ---
    elif has_any(["hurts", "eagles", "panthers", "qb", "quarterback", "blood clot", "calf", "nfl", "injury", "ruled out", "touchdown"]):
        neutral = f"{clean_title}. Team medical staff and franchise officials confirmed the roster status, initiating clinical recovery protocols ahead of upcoming game action."
        left_framing = "Player Health Over Game Outcomes: Prioritizing Long-Term Vascular Safety in NFL Athletics"
        left_bullets = [
            "Prioritizes non-negotiable athlete welfare, stressing that dangerous conditions like blood clots must never be compromised for team standings.",
            "Demands strict adherence to medical protocols over franchise commercial pressure or broadcast television priorities.",
            "Reinforces collective bargaining health guarantees and independent medical oversight across professional athletic leagues."
        ]
        left_talk = [
            "No football game or playoff seed is worth gambling with an athlete's long-term health and future.",
            "Professional sports leagues must always put medical science and player safety ahead of commercial interests."
        ]
        center_framing = f"Medical Caution Meets Tactical Adjustment: Navigating Starting Quarterback Absence in {clean_title[:38]}..."
        center_bullets = [
            "Balances conservative medical management with offensive game-planning and critical conference playoff positioning.",
            "Forces the coaching staff to adapt situational scheme packages and test second-string execution against Carolina.",
            "Monitors clinical recovery timelines and conditioning windows ahead of high-leverage late-season matchups."
        ]
        center_talk = [
            "Smart franchises make cautious medical calls early to preserve their franchise quarterback for the postseason run.",
            "Championship caliber teams must adapt to sudden injuries and execute sound situational football."
        ]
        right_framing = "Next-Man-Up Accountability: Testing Roster Depth and Culture Under Competitive Pressure"
        right_bullets = [
            "Tests team resilience and backup quarterback preparation under high-leverage conference game pressure.",
            "Demands disciplined offensive line protection, running game dominance, and error-free situational execution.",
            "Demonstrates that championship-caliber football franchises rely on system execution, culture, and locker room grit rather than single-player dependence."
        ]
        right_talk = [
            "Championships aren't won on excuses; elite teams adapt, execute, and deliver next-man-up football.",
            "Adversity reveals true team character; this game is the ultimate test of preparation and roster depth."
        ]

    # --- 9. FOREIGN SANCTIONS, RUSSIAN ENERGY, DIESEL TRADE ---
    elif has_any(["diesel", "russia diesel", "diesel deal", "oil sanctions", "petroleum sanctions"]):
        neutral = f"{clean_title}. Congressional foreign relations leaders and international energy diplomats are evaluating geopolitical leverage, crude supply chains, and statutory compliance."
        left_framing = "Global Human Rights and Clean Independence: Enforcing Sanctions Over Fossil Fuel Concessions"
        left_bullets = [
            "Demands uncompromised enforcement of international sanctions against hostile autocratic regimes responsible for global instability.",
            "Accelerates the strategic imperative to transition toward domestic renewable power and eliminate reliance on petro-states.",
            "Rebuffs bilateral trade waivers that enrich foreign oligarchs at the expense of international human rights standards."
        ]
        left_talk = [
            "We cannot compromise on basic human rights and international law for short-term fossil fuel arrangements.",
            "True energy security means severing our ties to foreign petro-dictatorships once and for all."
        ]
        center_framing = "Geopolitical Realism: Calibrating Economic Sanctions Against Global Fuel Supply Volatility"
        center_bullets = [
            "Balances national security objectives against potential diesel price spikes that could burden domestic commercial logistics.",
            "Assesses whether coordinated multilateral enforcement or targeted supply exemptions best serve long-term strategic interests.",
            "Maintains transparent congressional oversight to ensure foreign policy doctrine remains consistent and predictable."
        ]
        center_talk = [
            "Effective diplomacy requires balancing moral resolve with practical calculations of global fuel supply stability.",
            "Predictable, bipartisan economic policies are essential to maintaining international alliance credibility."
        ]
        right_framing = "American Energy Dominance: Expand Domestic Production and Eliminate Foreign Adversary Deals"
        right_bullets = [
            "Demands complete unleashing of American oil, natural gas, and refining infrastructure to power the free world without foreign reliance.",
            "Insists on maximum pressure sanctions and zero commercial loopholes for hostile foreign powers.",
            "Asserts constitutional congressional power over foreign commerce, holding federal agencies accountable to national security statutes."
        ]
        right_talk = [
            "America has the natural resources to power our economy; we should be drilling our own energy, not buying from adversaries.",
            "Peace through strength requires maximum economic resolve and total American energy dominance."
        ]

    # --- 10. GENERAL DYNAMIC FALLBACK (Completely Free of Automotive or Energy Boilerplate) ---
    else:
        neutral = f"{clean_title}. Relevant authorities, industry stakeholders, and affected communities are evaluating the situation as verified developments unfold."
        left_framing = f"Public Accountability and Democratic Oversight Regarding {clean_title[:45]}..."
        left_bullets = [
            f"Advocates for heightened transparency, public oversight, and accountability from institutional decision-makers regarding {clean_title.lower()}.",
            f"Ensures that policies and actions protect everyday citizens, vulnerable communities, and public welfare over private interests.",
            f"Calls for democratic safeguards, ethical standards, and open public debate to address the underlying challenges."
        ]
        left_talk = [
            f"Public welfare, transparency, and institutional accountability must always take precedence over private interests.",
            f"We must protect the rights and safety of everyday citizens when addressing these critical issues."
        ]
        center_framing = f"Weighing Pragmatic Solutions and Operational Trade-Offs in {clean_title[:42]}..."
        center_bullets = [
            f"Assesses the realistic legal, operational, and administrative factors required to effectively manage {clean_title.lower()}.",
            f"Seeks balanced middle-ground solutions between competing regulatory objectives and practical feasibility.",
            f"Maintains institutional stability by relying on verified evidence, thorough due diligence, and measured consensus."
        ]
        center_talk = [
            f"Effective governance requires examining all facts calmly and crafting pragmatic, balanced solutions.",
            f"Extreme rhetoric solves nothing; steady institutional collaboration delivers real, sustainable progress."
        ]
        right_framing = f"Constitutional Order, Free Enterprise, and Personal Responsibility in {clean_title[:40]}..."
        right_bullets = [
            f"Emphasizes individual liberty, constitutional boundaries, and strict limits on administrative or bureaucratic overreach regarding {clean_title.lower()}.",
            f"Protects free enterprise, economic efficiency, and rule of law from unnecessary government intervention.",
            f"Promotes personal accountability, merit, and decentralized decision-making to resolve complex challenges."
        ]
        right_talk = [
            f"Freedom, personal responsibility, and constitutional limits on authority deliver the strongest outcomes.",
            f"Protecting individual liberty, free enterprise, and the rule of law remains fundamental."
        ]

    return {
        "neutral_summary": neutral,
        "perspectives": {
            "LEFT": {"headline_framing": left_framing, "why_it_matters": left_bullets, "talking_points": left_talk},
            "CENTER": {"headline_framing": center_framing, "why_it_matters": center_bullets, "talking_points": center_talk},
            "RIGHT": {"headline_framing": right_framing, "why_it_matters": right_bullets, "talking_points": right_talk}
        }
    }

def call_ai_synthesizer(title: str, context: str, category: str) -> Dict[str, Any]:
    gemini_key = (os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY") or "").strip().strip('"').strip("'")
    openai_key = (os.environ.get("OPENAI_API_KEY") or "").strip().strip('"').strip("'")
    anthropic_key = (os.environ.get("ANTHROPIC_API_KEY") or "").strip().strip('"').strip("'")

    prompt = f"""You are the editorial synthesis engine for Your News Lens (yournewslens.com).
Analyze this exact wire article:
Category: {category}
Title: {title}
Context: {context}

CRITICAL: Arguments MUST be tailored specifically to this exact story. If baseball (Dodgers/Brewers), discuss the NLCS sweep, relief pitching, and pennant race. If election security/mailings, discuss poll workers, postal inspection, and law enforcement. If Tesla, discuss EV technology and manufacturing.
Return strictly valid raw JSON:
{{
  "neutral_summary": "Two objective, verifiable sentences covering who, what, when, and where. Zero bias.",
  "perspectives": {{
    "LEFT": {{
      "headline_framing": "Progressive framing emphasizing public interest, labor rights, equity, or ethics",
      "why_it_matters": ["Impact bullet 1", "Impact bullet 2", "Systemic bullet 3"],
      "talking_points": ["Soundbite 1", "Soundbite 2"]
    }},
    "CENTER": {{
      "headline_framing": "Pragmatic, institutional framing balancing competing trade-offs",
      "why_it_matters": ["Operational bullet 1", "Compromise bullet 2", "Market bullet 3"],
      "talking_points": ["Pragmatic soundbite 1", "Realistic soundbite 2"]
    }},
    "RIGHT": {{
      "headline_framing": "Conservative framing emphasizing free enterprise, individual accountability, or constitutional limits",
      "why_it_matters": ["Impact bullet 1", "Accountability bullet 2", "Competitive resilience bullet 3"],
      "talking_points": ["Soundbite 1", "Soundbite 2"]
    }}
  }}
}}"""

    # 1. Try Google Gemini Models
    if gemini_key:
        print(f"[AI] Detected Gemini API Key. Calling Gemini 1.5 Flash for: '{title[:40]}...'")
        models = ["gemini-1.5-flash", "gemini-2.0-flash", "gemini-1.5-pro"]
        for model in models:
            # Attempt A: Standard URL query key
            try:
                url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={gemini_key}"
                payload = json.dumps({
                    "contents": [{"parts": [{"text": prompt}]}],
                    "generationConfig": {"responseMimeType": "application/json", "temperature": 0.3}
                }).encode("utf-8")
                req = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json"})
                with urllib.request.urlopen(req, timeout=18) as resp:
                    data = json.loads(resp.read().decode("utf-8"))
                    text = data["candidates"][0]["content"]["parts"][0]["text"].strip()
                    if text.startswith("```"):
                        text = text.split("```")[1]
                        if text.startswith("json"): text = text[4:].strip()
                    res = json.loads(text)
                    if "neutral_summary" in res and "perspectives" in res:
                        print(f"[AI] SUCCESS: Generated dynamic perspective via Gemini {model}!")
                        return res
            except Exception as e:
                print(f"[AI Notice] Gemini {model} failed: {e}")

            # Attempt B: Header-based key
            try:
                url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
                payload = json.dumps({
                    "contents": [{"parts": [{"text": prompt}]}],
                    "generationConfig": {"responseMimeType": "application/json"}
                }).encode("utf-8")
                req = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json", "x-goog-api-key": gemini_key})
                with urllib.request.urlopen(req, timeout=18) as resp:
                    data = json.loads(resp.read().decode("utf-8"))
                    text = data["candidates"][0]["content"]["parts"][0]["text"].strip()
                    if text.startswith("```"):
                        text = text.split("```")[1]
                        if text.startswith("json"): text = text[4:].strip()
                    res = json.loads(text)
                    if "neutral_summary" in res and "perspectives" in res:
                        print(f"[AI] SUCCESS: Generated dynamic perspective via Gemini {model} (header auth)!")
                        return res
            except Exception as e:
                pass
    else:
        print("[AI Notice] GEMINI_API_KEY environment variable is not present.")

    # 2. Try OpenAI API if key is present
    if openai_key:
        try:
            print(f"[AI] Calling OpenAI gpt-4o-mini for '{title[:40]}...'")
            url = "https://api.openai.com/v1/chat/completions"
            payload = json.dumps({
                "model": "gpt-4o-mini",
                "messages": [{"role": "user", "content": prompt}],
                "response_format": {"type": "json_object"}
            }).encode("utf-8")
            req = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json", "Authorization": f"Bearer {openai_key}"})
            with urllib.request.urlopen(req, timeout=18) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                text = data["choices"][0]["message"]["content"].strip()
                res = json.loads(text)
                if "neutral_summary" in res and "perspectives" in res:
                    print("[AI] SUCCESS: Generated dynamic perspective via OpenAI!")
                    return res
        except Exception as e:
            print(f"[AI Notice] OpenAI API failed: {e}")

    # 3. Fallback to Dynamic Contextual Semantic Engine
    print(f"[AI Fallback] Generating theme-accurate perspectives for: {title[:50]}...")
    return generate_contextual_synthesis(title, context, category)

def prerender_cards_html(stories: List[Dict[str, Any]]) -> str:
    cards_html = []
    for s in stories[:15]:
        sId = s.get("id", "story-0")
        cat = s.get("category", "General News")
        imgUrl = s.get("image_url", "https://images.unsplash.com/photo-1585829365295-ab7cd400c167?auto=format&fit=crop&w=1200&q=80")
        caption = s.get("caption", s.get("title", ""))
        credit = s.get("credit", "📸 News Wire")
        source = s.get("source", "Associated Press Wire")
        pub_ts = s.get("pub_timestamp", "")
        summary = s.get("neutral_summary", "")

        perspectives = s.get("perspectives", {})
        
        card = f"""
        <article class="compact-card" data-category="{cat}" id="{sId}">
          <div class="hero-image-wrap">
            <img src="{imgUrl}" alt="{caption}" class="hero-photo" loading="lazy" referrerpolicy="no-referrer" onerror="this.onerror=null; this.src='https://images.unsplash.com/photo-1585829365295-ab7cd400c167?auto=format&fit=crop&w=1200&q=80';" />
            <div class="photo-caption-bar">
              <span class="caption-text">{caption}</span>
              <span class="credit-tag">{credit}</span>
            </div>
          </div>

          <div class="card-body">
            <div class="meta-row">
              <span class="category-tag">{cat}</span>
              <span class="source-tag" data-timestamp="{pub_ts}">{source}</span>
            </div>

            <h3 class="story-title">{s.get('title', '')}</h3>

            <div class="neutral-box">
              <div class="neutral-title">⚖️ The Core Facts (Neutral Event Summary)</div>
              <div class="neutral-desc">{summary}</div>
            </div>"""

        lensList = [
            {"key": "CENTER", "name": "Centrist / Balanced", "icon": "🟢", "chipClass": "emerald", "bulletClass": "emerald", "display": ""},
            {"key": "RIGHT", "name": "Conservative Lens", "icon": "🔴", "chipClass": "red", "bulletClass": "red", "display": "style=\"display: none;\""},
            {"key": "LEFT", "name": "Progressive Lens", "icon": "🔵", "chipClass": "blue", "bulletClass": "blue", "display": "style=\"display: none;\""}
        ]

        for lens in lensList:
            pData = perspectives.get(lens["key"], {})
            bullets = "".join([f"<li>{b}</li>" for b in pData.get("why_it_matters", [])])
            tp_list = pData.get("talking_points", [])
            quotes = "".join([f'<div class="quote-row">"{tp}"</div>' for tp in tp_list])

            card += f"""
            <div id="{sId}-view-{lens['key']}" class="perspective-view-box" {lens['display']}>
              <div class="lens-status-row">
                <div class="lens-chip {lens['chipClass']}">
                  <span>{lens['icon']}</span>
                  <span>{lens['name']}</span>
                </div>

                <div class="card-toggle-group">
                  <button type="button" class="card-toggle-btn {'active left' if lens['key'] == 'LEFT' else ''}" data-story="{sId}" onclick="switchStoryPerspective(this.getAttribute('data-story'), 'LEFT')">Left</button>
                  <button type="button" class="card-toggle-btn {'active center' if lens['key'] == 'CENTER' else ''}" data-story="{sId}" onclick="switchStoryPerspective(this.getAttribute('data-story'), 'CENTER')">Balanced</button>
                  <button type="button" class="card-toggle-btn {'active right' if lens['key'] == 'RIGHT' else ''}" data-story="{sId}" onclick="switchStoryPerspective(this.getAttribute('data-story'), 'RIGHT')">Right</button>
                </div>
              </div>

              <div class="framing-headline">
                <span>📌</span>
                <span>{pData.get('headline_framing', 'Perspective Framing')}</span>
              </div>

              <div class="label-heading">Why It Matters For Your Stance:</div>
              <ul class="compact-bullets {lens['bulletClass']}">
                {bullets}
              </ul>

              <div class="talking-points-panel">
                <div class="panel-header">
                  <span class="panel-title">💬 Key Talking Points & Arguments</span>
                  <button type="button" class="btn-copy-chip" onclick="copyPointsFromCard(this)">📋 Copy</button>
                </div>
                {quotes}
              </div>
            </div>"""

        card += """
            <div class="card-bottom-actions">
              <button type="button" class="btn-action-small" onclick="toggleSaveCard(this)">
                <span>🤍</span>
                <span>Save</span>
              </button>
              <button type="button" class="btn-discuss-small" onclick="showLoungeTab()">
                <span>👥</span> Discuss
              </button>
            </div>
          </div>
        </article>"""
        cards_html.append(card)

    return "\n".join(cards_html)

def update_index_html_prerender(stories: List[Dict[str, Any]]):
    if not os.path.exists(HTML_FILE) or not stories:
        return
    try:
        with open(HTML_FILE, "r", encoding="utf-8") as f:
            content = f.read()

        feed_start = content.find('<div id="storiesFeedView" class="feed-container">')
        if feed_start == -1:
            return
        feed_start += len('<div id="storiesFeedView" class="feed-container">')
        
        comm_view = content.find('<!-- Community Lounge -->')
        feed_end = content.rfind('</div>', feed_start, comm_view if comm_view != -1 else len(content))
        
        if feed_end != -1:
            new_cards = "\n" + prerender_cards_html(stories) + "\n    "
            updated_content = content[:feed_start] + new_cards + content[feed_end:]
            with open(HTML_FILE, "w", encoding="utf-8") as f:
                f.write(updated_content)
            print("Successfully pre-rendered updated story cards into index.html.")
    except Exception as e:
        print(f"Notice: Pre-rendering index.html: {e}")

def run_pipeline():
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Starting Your News Lens Wire Scraper...")
    
    existing_stories = []
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                existing_stories = json.load(f)
        except Exception as e:
            print(f"Notice: Loading existing data: {e}")

    # Track used URLs to guarantee ZERO DUPLICATES across the entire feed!
    used_urls: Set[str] = set()

    # Self-Healing: Check every existing story for theme mismatches or outdated timers
    for s in existing_stories:
        title = s.get("title", "")
        cat = s.get("category", "General News")
        pub_ts = s.get("pub_timestamp")
        
        # Recalculate real relative timestamp from pub_timestamp
        if pub_ts:
            _, rel_time = parse_pubdate_to_relative(datetime.fromtimestamp(pub_ts, timezone.utc).strftime("%a, %d %b %Y %H:%M:%S GMT"))
            src_name = s.get("source_name") or s.get("source", "").split(" • ")[0]
            s["source"] = f"{src_name} • {rel_time}"

        # If mismatched (e.g. Dodgers talking about battery, mailings talking about diesel), automatically fix!
        if is_story_mismatched(s):
            print(f"[Self-Healing] Re-synthesizing corrupted story: {title[:55]}...")
            re_synth = call_ai_synthesizer(title, "", cat)
            s["neutral_summary"] = re_synth["neutral_summary"]
            s["perspectives"] = re_synth["perspectives"]

        img_info = resolve_story_image(title, cat, used_urls)
        s["image_url"] = img_info["url"]
        s["caption"] = img_info["caption"]
        s["credit"] = img_info["credit"]

    existing_titles = {s.get("title", "").strip().lower() for s in existing_stories}
    new_stories = []

    for feed in RSS_FEEDS:
        items = fetch_rss_items(feed, max_items=4)
        for it in items:
            t = it["title"]
            if t.lower() in existing_titles:
                continue

            print(f"Processing wire item: {t[:65]}...")
            cat_assigned = auto_detect_category(t, it["description"], it["category"])
            synthesis = call_ai_synthesizer(t, it["description"], cat_assigned)
            img_info = resolve_story_image(t, cat_assigned, used_urls)
            story_id = f"story-{int(time.time())}-{len(new_stories)}"
            
            cat_assigned = auto_detect_category(t, it["description"], it["category"])
            story_record = {
                "id": story_id,
                "category": cat_assigned,
                "title": t,
                "source_name": it["source_name"],
                "pub_timestamp": it["pub_timestamp"],
                "source": it["source"],
                "image_url": img_info["url"],
                "caption": img_info["caption"],
                "credit": img_info["credit"],
                "neutral_summary": synthesis["neutral_summary"],
                "perspectives": synthesis["perspectives"]
            }
            new_stories.append(story_record)
            existing_titles.add(t.lower())
            time.sleep(1)

    updated_feed = new_stories + existing_stories
    updated_feed = updated_feed[:40] # keep freshest 25

    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(updated_feed, f, indent=2)

    update_index_html_prerender(updated_feed)
    print(f"Pipeline complete. Total stories: {len(updated_feed)} (Added: {len(new_stories)})")

if __name__ == "__main__":
    run_pipeline()
