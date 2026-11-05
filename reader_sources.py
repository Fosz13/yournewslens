"""Additional publisher feeds, public calendar listings, and sourced political lenses."""
from datetime import datetime
from html import unescape
from urllib.request import Request, urlopen
from zoneinfo import ZoneInfo
import re

import editorial

TAMPA = "Tampa Bay, FL"
CITY_CALENDAR = "https://www.tampa.gov/calendar"
MONTH = re.compile(r'class="date-part-F">([A-Za-z]+)</span>\s*<span class="date-part-j">(\d+)</span>')
EVENT = re.compile(r'<div class="calendar-item" id="event-title-\d+">\s*<div[^>]*>\s*<a href="(/events/[^"]+)"[^>]*>(.*?)</a>', re.S)
TIME = re.compile(r'views-field-nothing-2[^>]*><span class="field-content">\s*([^<]+)')

# Side is an editorial classification used only for commentary feeds.
SOURCES = [
    ("Tampa Bay Times", "https://www.tampabay.com/arc/outboundfeeds/rss/?outputType=xml", "Local News", TAMPA),
    ("WUSF", "https://www.wusf.org/index.rss", "Local News", TAMPA),
    ("Florida Phoenix", "https://floridaphoenix.com/feed/", "Local News", TAMPA),
    ("St. Pete Catalyst", "https://stpetecatalyst.com/feed/", "Local News", TAMPA),
    ("Creative Loafing Tampa Bay", "https://www.cltampa.com/tampa/Rss.xml", "Local News", TAMPA),
    ("That’s So Tampa", "https://thatssotampa.com/feed/", "Local News", TAMPA),
    ("I Love the Burg", "https://ilovetheburg.com/feed/", "Local News", TAMPA),
    ("That's So Tampa Events", "https://news.google.com/rss/search?q=site%3Athatssotampa.com+%28weekend+OR+events+OR+festival%29+when%3A7d&hl=en-US&gl=US&ceid=US%3Aen", "Local News", TAMPA),
    ("NPR", "https://feeds.npr.org/1001/rss.xml", "National News", ""),
    ("PBS NewsHour", "https://www.pbs.org/newshour/feeds/rss/headlines", "National News", ""),
    ("Associated Press", "https://flipboard.com/@AssociatedPress.rss", "National News", ""),
    ("BBC Business", "https://feeds.bbci.co.uk/news/business/rss.xml", "Business & Economy", ""),
    ("France 24", "https://www.france24.com/en/rss", "World News", ""),
    ("Deutsche Welle", "https://rss.dw.com/rdf/rss-en-all", "World News", ""),
    ("CBC World", "https://www.cbc.ca/webfeed/rss/rss-world", "World News", ""),
    ("Ars Technica", "https://feeds.arstechnica.com/arstechnica/index", "Science & Tech", ""),
    ("The Verge", "https://www.theverge.com/rss/index.xml", "Science & Tech", ""),
    ("TechCrunch", "https://techcrunch.com/feed/", "Science & Tech", ""),
    ("ScienceDaily", "https://www.sciencedaily.com/rss/top/science.xml", "Science & Tech", ""),
    ("ESPN", "https://www.espn.com/espn/rss/news", "Sports", ""),
    ("BBC Sport", "https://feeds.bbci.co.uk/sport/rss.xml", "Sports", ""),
    ("The Hollywood Reporter", "https://www.hollywoodreporter.com/feed/", "Entertainment", ""),
    ("National Review", "https://www.nationalreview.com/feed/", "Politics", "", "RIGHT"),
    ("Washington Examiner Opinion", "https://www.washingtonexaminer.com/opinion/feed", "Politics", "", "RIGHT"),
    ("New York Post Opinion", "https://nypost.com/opinion/feed/", "Politics", "", "RIGHT"),
    ("The Nation", "https://www.thenation.com/feed/", "Politics", "", "LEFT"),
    ("Mother Jones", "https://www.motherjones.com/feed/", "Politics", "", "LEFT"),
    ("Guardian US Opinion", "https://www.theguardian.com/us/commentisfree/rss", "Politics", "", "LEFT"),
]

def feeds():
    return [{"source": name, "url": url, "category": category, "metro": metro,
             "master_category": "Local News" if metro else "National Headlines",
             "sub_category": "events" if name.endswith("Events") else ""}
            for name, url, category, metro, *side in SOURCES]

def clean(value):
    return " ".join(unescape(re.sub(r"<[^>]+>", " ", value)).split())

def tampa_events(page, now):
    local_now = datetime.fromtimestamp(now, ZoneInfo("America/New_York"))
    days = list(MONTH.finditer(page))
    found = {}
    for i, match in enumerate(days):
        month, day = match.groups()
        try:
            when = datetime.strptime(f"{month} {day} {local_now.year}", "%B %d %Y").date()
            if (when - local_now.date()).days < -300:
                when = when.replace(year=when.year + 1)
        except ValueError:
            continue
        if not 0 <= (when - local_now.date()).days <= 10:
            continue
        block = page[match.end():days[i + 1].start() if i + 1 < len(days) else len(page)]
        previous = 0
        for event in EVENT.finditer(block):
            path, raw_title = event.groups()
            title = clean(raw_title)
            times = TIME.findall(block[previous:event.start()])
            previous = event.end()
            if not title or not times or re.search(r"\b(?:committee|commission|public hearing|board meeting|advisory|city council)\b", title, re.I):
                continue
            url = "https://www.tampa.gov" + path
            date_label = f"{when:%A, %B} {when.day}"
            found.setdefault(url, {
                "id": editorial.story_id(url), "title": title, "article_url": url, "link": url,
                "source_name": "City of Tampa", "source": "City of Tampa • " + date_label,
                "pub_timestamp": int(now), "category": "Local News", "master_category": "Local News",
                "metro": TAMPA, "sub_category": "events", "event_date": when.isoformat(),
                "lead_fact": f"{date_label} · {clean(times[-1])}.", "editorial_source_checked": True,
            })
    return sorted(found.values(), key=lambda event: event["event_date"])[:12]

def fetch_events(now):
    try:
        request = Request(CITY_CALENDAR, headers={"User-Agent": "YourNewsLens/1.0"})
        with urlopen(request, timeout=8) as response:
            return tampa_events(response.read(1_500_000).decode(errors="replace"), now)
    except (OSError, ValueError):
        return []

def entry(point, source, url, label=""):
    return {"talking_points": [point], "label": label, "source_attribution": source,
            "source_url": url, "perspective_badge": "documented_commentary"}

def enrich_lenses(stories, items):
    sides = {row[0]: row[4] for row in SOURCES if len(row) == 5}
    candidates = {side: [] for side in ("LEFT", "RIGHT")}
    for item in items:
        side = sides.get(item.get("feed_name")) or sides.get(item.get("source_name"))
        facts = editorial.excerpt_facts(item["title"], item.get("description", ""))
        if side and facts:
            candidates[side].append((item, facts[0]))
    ignored = {"trump", "democrat", "democrats", "republican", "republicans", "says", "news", "with"}
    for story in stories:
        title = story["title"]
        if ((title.startswith("Progressives hail") and "midterm" in title.lower()) or
                title.startswith("Democrats prepare to take Congress after sweeping wins")):
            story["perspective_mode"] = "political"
            story["perspectives"] = {
                "LEFT": entry("Democratic leaders see the results as a chance to press their affordability agenda and hold the administration accountable.", "Hakeem Jeffries · via Reuters", "https://www.reuters.com/legal/government/democrats-seize-congress-sweeping-midterm-repudiation-trump-2026-11-04/"),
                "CENTER": entry("Democrats plan to use their congressional majorities to check Trump. The result gives them leverage and raises the prospect of two years of deadlock.", "Reuters · reporting", "https://www.reuters.com/legal/government/democrats-vow-rein-trump-he-shows-off-white-house-ballroom-2026-11-05/"),
                "RIGHT": entry("Republicans should take the loss as a verdict on Trump’s performance. Geraghty argues that the party needs to change course to win back dissatisfied voters.", "Jim Geraghty · National Review", "https://www.nationalreview.com/the-morning-jolt/the-voters-have-spoken-trump-failed/amp/"),
            }
            continue
        if story.get("perspective_mode") != "political":
            continue
        keywords = editorial.tokens(title) - ignored
        for side, rows in candidates.items():
            ranked = sorted(((len(keywords & (editorial.tokens(item["title"]) - ignored)), item, fact)
                             for item, fact in rows), key=lambda match: -match[0])
            if ranked and ranked[0][0] >= 3:
                _, item, fact = ranked[0]
                if editorial.source_url(item.get("link")):
                    story.setdefault("perspectives", {})[side] = entry(fact, item["source_name"], item["link"])
