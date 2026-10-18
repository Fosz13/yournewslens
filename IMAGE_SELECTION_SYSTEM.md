# Dynamic Image Selection & Ingestion System for Your News Lens

## 1. Core Rule: Scraped / Imported Image Priority
**"If the story is scraped/imported with a usable picture, use that picture. Unless there's a reason we can't."**

When an article is ingested from RSS wire feeds, news APIs, or manual story imports:
1. **Direct Extraction**: `fetch_rss_items()` inspects `<enclosure>`, `<media:content>`, `<media:thumbnail>`, and embedded `<img src>` tags in the feed payload.
2. **Usability Verification (`is_usable_image_url`)**:
   - The picture is validated to ensure it is a real, high-resolution editorial photo (`http://` or `https://`).
   - The engine automatically filters out unusable images: tracking beacons, 1x1 analytics pixels (e.g. DoubleClick, StatCounter), ad server spacers, site favicons, and generic placeholder graphics.
3. **Preservation**: Existing curated stories in `data/stories.json` retain their imported/verified lead photos and are never overwritten with generic fallbacks.

---

## 2. The 4-Tier Resolution Architecture

When a story is processed:

### **Tier 0: Direct Scraped / Imported Lead Image (Top Priority)**
If the incoming wire or import payload already provides a verified, usable photograph, the engine immediately adopts it with full source credit (e.g. `📸 NPR News`, `📸 Associated Press`).

### **Tier 1: Real-Time Named Entity Extraction & Wikimedia API**
If no usable picture was provided in the feed, the engine extracts key named entities (public officials, institutions, athletes, companies, e.g., `Jalen Hurts`, `NCAA`, `Jerome Powell`, `Supreme Court`) and queries the Wikimedia REST API for official public-domain archive photos.

### **Tier 2: Granular Keyword Topic Matching (50+ Specialized Photographic Rules)**
If no named entity matches, the resolver matches the headline against 50+ specialized topic photographic libraries:
- **Severe Weather / Grid Outages**: Transmission line repairs, downed tree lines, storm infrastructure.
- **Entertainment & Cinema**: Theatrical 70mm IMAX exhibition, Hollywood studios, cinema auditoriums.
- **Space & Astronomy**: Deep space observatories, exoplanets, James Webb Space Telescope data.
- **Law Enforcement & Public Safety**: First responder perimeters, official investigations.
- **Sports Breakdown**: Ballparks (Dodgers/Brewers), NFL stadiums (Eagles/Panthers), basketball arenas (Lakers), PGA fairways.

### **Tier 3: Deterministic Category-Based Round-Robin (Zero Duplication)**
For general stories without distinct keywords, each category maintains a curated pool of verified, high-resolution photographs, assigned using title-based hashing to prevent duplicate images across consecutive cards.

---

## 3. Client-Side Error Resiliency (`onerror` Fallback)
If an external image host becomes temporarily unreachable or blocks hotlinking, the browser automatically and silently recovers via `onImgError()` in `index.html` and `app.js`, gracefully displaying a neutral high-resolution editorial news fallback with zero broken image icons.
