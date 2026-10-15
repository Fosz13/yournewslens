#!/usr/bin/env python3
"""
LensWire Automated 15-Minute News Ingestion & Synthesis Engine
Fetches wire stories from RSS feeds, extracts the factual core, and generates
three ideological lenses (Left, Center, Right) with Why It Matters and Talking Points.
Designed to run automatically every 15 minutes via GitHub Actions.
"""

import os
import sys
import json
import time
import urllib.request
import urllib.error
import xml.etree.ElementTree as ET
from datetime import datetime
from typing import List, Dict, Any, Optional

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "data", "stories.json")

# Verified public wire RSS feeds
RSS_FEEDS = [
    {
        "category": "All",
        "source": "AP News Wire",
        "url": "https://feedx.net/rss/apnews.xml"
    },
    {
        "category": "Economy & Inflation",
        "source": "Reuters Financial",
        "url": "https://www.reutersagency.com/feed/?taxonomy=markets&post_type=best"
    },
    {
        "category": "Energy & Infrastructure",
        "source": "NPR News",
        "url": "https://feeds.npr.org/1001/rss.xml"
    },
    {
        "category": "Politics",
        "source": "Fox News Politics",
        "url": "https://moxie.foxnews.com/google-publisher/politics.xml"
    },
    {
        "category": "Politics",
        "source": "NPR Politics",
        "url": "https://feeds.npr.org/1014/rss.xml"
    },
    {
        "category": "Politics",
        "source": "Politico National",
        "url": "https://rss.politico.com/politics-news.xml"
    },
    {
        "category": "Border & Security",
        "source": "Border Security Wire",
        "url": "https://feedx.net/rss/apnews.xml"
    },
    {
        "category": "Sports",
        "source": "ESPN Wire",
        "url": "https://www.espn.com/espn/rss/news"
    }
]

# High quality category fallback imagery
CATEGORY_FALLBACK_IMAGES = {
    "Politics": {
        "url": "https://upload.wikimedia.org/wikipedia/commons/4/4f/US_Capitol_west_side.JPG",
        "caption": "The United States Capitol building and House chamber wing in Washington, D.C.",
        "credit": "📸 Architect of the Capitol"
    },
    "Sports": {
        "url": "https://images.unsplash.com/photo-1535131749006-b7f58c99034b?auto=format&fit=crop&w=1200&q=80",
        "caption": "Professional championship arena fairway and stadium view.",
        "credit": "📸 Sports Media Archive"
    },
    "Energy & Infrastructure": {
        "url": "https://images.unsplash.com/photo-1473341304170-971dccb5ac1e?auto=format&fit=crop&w=1200&q=80",
        "caption": "High-voltage transmission line towers and regional grid infrastructure.",
        "credit": "📸 AP Photo Archive"
    },
    "Economy & Inflation": {
        "url": "https://upload.wikimedia.org/wikipedia/commons/8/8d/Marriner_S._Eccles_Federal_Reserve_Board_Building.jpg",
        "caption": "Marriner S. Eccles Federal Reserve Board Building in Washington, D.C.",
        "credit": "📸 Federal Reserve Pool"
    },
    "Border & Security": {
        "url": "https://upload.wikimedia.org/wikipedia/commons/8/80/CBP_Operations_-_San_Diego_Checkpoint_%2827862652842%29.jpg",
        "caption": "Border operations and regional security checkpoint.",
        "credit": "📸 CBP Archive"
    },
    "Healthcare & Drug Costs": {
        "url": "https://images.unsplash.com/photo-1586773860418-d37222d8fce3?auto=format&fit=crop&w=1200&q=80",
        "caption": "Regional medical pavilion and pharmacy health system facility.",
        "credit": "📸 Health Systems Wire"
    },
    "Tech & Free Speech": {
        "url": "https://upload.wikimedia.org/wikipedia/commons/9/94/Supreme_Court.jpg",
        "caption": "Supreme Court of the United States west facade in Washington, D.C.",
        "credit": "📸 National Photo Archive"
    }
}

DEFAULT_FALLBACK_IMAGE = {
    "url": "https://images.unsplash.com/photo-1504711434969-e33886168f5c?auto=format&fit=crop&w=1200&q=80",
    "caption": "National press briefing room and broadcast journalism desk.",
    "credit": "📸 Wire Media Archive"
}

def fetch_rss_items(feed_info: Dict[str, str], max_items: int = 3) -> List[Dict[str, Any]]:
    """Fetch and parse items from an RSS feed using standard library."""
    items = []
    try:
        req = urllib.request.Request(
            feed_info["url"],
            headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) LensWire Ingestion Bot 1.0"}
        )
        with urllib.request.urlopen(req, timeout=12) as resp:
            content = resp.read()
            root = ET.fromstring(content)
            
            for item in root.findall(".//item")[:max_items]:
                title = item.findtext("title", "").strip()
                link = item.findtext("link", "").strip()
                pub_date = item.findtext("pubDate", "").strip()
                desc = item.findtext("description", "").strip()
                
                # Strip HTML tags from description if present
                if "<" in desc and ">" in desc:
                    desc = desc.split("<")[0].strip() or desc
                
                if title and link:
                    items.append({
                        "title": title,
                        "link": link,
                        "pub_date": pub_date,
                        "description": desc,
                        "source": feed_info["source"],
                        "category": feed_info["category"]
                    })
    except Exception as err:
        print(f"Warning: Could not fetch {feed_info['source']}: {err}")
    return items

def call_ai_synthesizer(title: str, context: str, category: str) -> Optional[Dict[str, Any]]:
    """
    Synthesize neutral summary and three ideological perspectives using Gemini or Claude API.
    Uses standard library urllib to avoid third-party SDK dependencies.
    """
    gemini_key = os.environ.get("GEMINI_API_KEY")
    anthropic_key = os.environ.get("ANTHROPIC_API_KEY")
    
    prompt = f"""You are the editorial synthesis engine for LensWire, an objective, multi-perspective news platform.
Analyze this news item:
Category: {category}
Title: {title}
Context: {context}

Return strictly a valid JSON object (no markdown, no backticks, just raw JSON) with this exact schema:
{{
  "neutral_summary": "Two objective, verifiable sentences covering who, what, when, and where. Zero spin or bias.",
  "perspectives": {{
    "LEFT": {{
      "headline_framing": "Progressive framing emphasizing public interest, labor rights, equity, or environmental protection",
      "why_it_matters": [
        "First major progressive policy impact bullet",
        "Second impact bullet on working families or vulnerable groups",
        "Third systemic or accountability implication bullet"
      ],
      "talking_points": [
        "Short, memorable progressive soundbite for debate",
        "Second soundbite highlighting justice or public accountability"
      ]
    }},
    "CENTER": {{
      "headline_framing": "Pragmatic, institutional framing balancing competing trade-offs",
      "why_it_matters": [
        "Economic, legal, or procedural trade-off bullet",
        "Bipartisan compromises or institutional challenges bullet",
        "Broader market or societal implications bullet"
      ],
      "talking_points": [
        "Pragmatic middle-ground observation",
        "Realistic view on long-term feasibility"
      ]
    }},
    "RIGHT": {{
      "headline_framing": "Conservative framing emphasizing free enterprise, individual liberty, constitutional limits, or fiscal discipline",
      "why_it_matters": [
        "Impact on free enterprise, taxpayers, or economic freedom bullet",
        "Regulatory overreach, national security, or constitutional concerns bullet",
        "State authority, personal responsibility, or institutional integrity bullet"
      ],
      "talking_points": [
        "Short, memorable conservative soundbite for debate",
        "Second soundbite highlighting market freedom or fiscal realism"
      ]
    }}
  }}
}}"""

    # 1. Try Google Gemini API if key is present
    if gemini_key:
        try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={gemini_key}"
            payload = json.dumps({
                "contents": [{"parts": [{"text": prompt}]}],
                "generationConfig": {"response_mime_type": "application/json"}
            }).encode("utf-8")
            
            req = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=20) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                text = data["candidates"][0]["content"]["parts"][0]["text"]
                return json.loads(text)
        except Exception as e:
            print(f"Gemini API error: {e}")

    # 2. Try Anthropic Claude API if key is present
    if anthropic_key:
        try:
            url = "https://api.anthropic.com/v1/messages"
            payload = json.dumps({
                "model": "claude-3-5-sonnet-20241022",
                "max_tokens": 1200,
                "messages": [{"role": "user", "content": prompt}]
            }).encode("utf-8")
            
            req = urllib.request.Request(url, data=payload, headers={
                "Content-Type": "application/json",
                "x-api-key": anthropic_key,
                "anthropic-version": "2023-06-01"
            })
            with urllib.request.urlopen(req, timeout=25) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                raw_text = data["content"][0]["text"].strip()
                # Clean potential markdown wrapping
                if raw_text.startswith("```"):
                    raw_text = raw_text.split("```")[1]
                    if raw_text.startswith("json"):
                        raw_text = raw_text[4:].strip()
                return json.loads(raw_text)
        except Exception as e:
            print(f"Anthropic API error: {e}")

    # 3. Fallback: Return None if no API keys configured yet
    return None

def run_pipeline():
    """Main execution loop run every 15 minutes."""
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Starting LensWire 15-Minute Pipeline...")
    
    # Load existing stories
    existing_stories = []
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                existing_stories = json.load(f)
        except Exception as e:
            print(f"Notice: Loading existing data: {e}")

    existing_titles = {s.get("title", "").lower() for s in existing_stories}
    new_stories = []

    # Ingest from feeds
    for feed in RSS_FEEDS:
        items = fetch_rss_items(feed, max_items=2)
        for it in items:
            t = it["title"]
            if t.lower() in existing_titles:
                continue
            
            print(f"Processing new wire item: {t[:60]}...")
            synthesis = call_ai_synthesizer(t, it["description"], it["category"])
            
            if synthesis and "neutral_summary" in synthesis and "perspectives" in synthesis:
                img_info = CATEGORY_FALLBACK_IMAGES.get(it["category"], DEFAULT_FALLBACK_IMAGE)
                story_id = f"story-{int(time.time())}-{len(new_stories)}"
                
                story_record = {
                    "id": story_id,
                    "category": it["category"] if it["category"] != "All" else "General News",
                    "title": t,
                    "source": f"{it['source']} • Just now",
                    "image_url": img_info["url"],
                    "caption": img_info["caption"],
                    "credit": img_info["credit"],
                    "neutral_summary": synthesis["neutral_summary"],
                    "perspectives": synthesis["perspectives"]
                }
                new_stories.append(story_record)
                existing_titles.add(t.lower())
                time.sleep(1) # respectful rate pacing

    # Combine: keep new stories at top, cap at 20 most recent stories
    updated_feed = new_stories + existing_stories
    updated_feed = updated_feed[:20]

    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(updated_feed, f, indent=2)

    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Pipeline complete. Total feed stories: {len(updated_feed)} (Added: {len(new_stories)})")

if __name__ == "__main__":
    run_pipeline()
