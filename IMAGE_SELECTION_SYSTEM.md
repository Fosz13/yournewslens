# Dynamic Image Selection & Ingestion System for Your News Lens

## 1. Core Rule: Scraped / Imported Image Priority
**"If the story is scraped/imported with a usable picture, use that picture. Unless there's a reason we can't."**

When an article is ingested from RSS wire feeds, news APIs, or manual story imports:
1. **Direct Extraction**: `fetch_rss_items()` inspects `<enclosure>`, `<media:content>`, `<media:thumbnail>`, and embedded `<img src>` tags in the feed payload.
2. **Usability Verification (`is_usable_image_url`)**:
   - The picture is validated to ensure it is a real, high-resolution editorial photo (`http://` or `https://`).
   - The engine automatically filters out unusable images: tracking beacons, 1x1 analytics pixels (e.g. DoubleClick, StatCounter), ad server spacers, site favicons, and generic placeholder graphics.
3. **Domain Integrity Verification**:
   - Before accepting an RSS editorial image, the system validates that the image does not introduce cross-domain pollution (e.g. sports stories are forbidden from inheriting religious clergy images, power transmission lines, hospital rooms, or courtrooms).
4. **Preservation**: Existing curated stories in `data/stories.json` retain their imported/verified lead photos and are never overwritten with generic fallbacks.

---

## 2. The 5-Tier Domain-Protected Resolution Architecture

When a story is processed:

### **Tier 0: Direct Scraped / Imported Lead Image (Top Priority)**
If the incoming wire or import payload provides a verified, usable photograph, the engine validates its domain compatibility and adopts it with full source credit (e.g. `📸 NPR News`, `📸 Associated Press`).

### **Tier 1: Curated Exact Entity & Breaking Topic Mapping**
For marquee topics, verified high-resolution photographs are mapped directly to ensure unmistakable relevance:
- **Collegiate Sports & Football**: Big 12, SEC, Big Ten, ACC, Pac-12, NCAA Football, College Football Playoff (`📸 Big 12 / College Sports Wire`).
- **Basketball**: College Basketball (March Madness), NBA, Lakers, Celtics (`📸 NCAA / College Basketball Wire`).
- **Baseball**: MLB, Dodgers, Brewers, Yankees, Mets, NLCS, World Series (`📸 Sports Media Wire`).
- **Severe Weather / Grid Outages**: Transmission line repairs, downed tree lines, storm infrastructure (`📸 Severe Weather Photo Pool`).
- **Entertainment & Cinema**: Theatrical 70mm IMAX exhibition, Hollywood studios (`📸 Entertainment News Wire`).
- **Space & Astronomy**: Deep space observatories, exoplanets, James Webb Space Telescope (`📸 NASA / Scientific Photo Archive`).
- **Faith & Vatican**: Pope Francis, Vatican audiences (Strictly restricted to non-sports religious and diplomatic coverage; `📸 Vatican Media`).

### **Tier 2: Real-Time Named Entity Extraction with Domain-Aware Semantic Validation**
If no curated entity matches, the engine extracts named entities from the title and queries the Wikimedia REST API.
**Strict Semantic Gatekeeper (`is_wikipedia_result_relevant`)**:
- **Anti-Cross-Domain Rule**: For Sports stories, any entity describing religious offices (Pope, bishop, cardinal, priest, Vatican), political offices, mechanical tools, or medical conditions is **strictly rejected**.
- **Positive Sports Affinity**: For Sports stories, the Wikipedia description or extract MUST contain sports terminology (e.g., `sport`, `athlete`, `player`, `coach`, `football`, `basketball`, `team`, `stadium`, `tournament`).
- **Ambiguous Single-Word Filter**: Capitalized generic headline words (e.g., `Pope`, `King`, `Power`, `Rankings`, `Conference`, `Bowl`) are filtered out from single-word entity queries to prevent false resolutions to homonymous historical or religious figures.

### **Tier 3: Domain-Aligned Secondary Topic Matching**
If entity lookup yields no match, secondary topic matching checks keywords **within the story's own category**:
- Sports stories only match Sports topic photographic libraries.
- Energy stories only match Energy topic libraries.
- Politics stories only match Politics libraries.
- Single-word collisions (such as "power" in "power rankings" triggering electrical power lines) are completely eliminated.

### **Tier 4: Category-Isolated Deterministic Fallbacks (Zero Cross-Domain Leaks)**
If no keyword matches, the resolver draws exclusively from the story's category fallback pool (e.g., `CATEGORY_FALLBACK_POOLS["Sports"]` for all sports stories). A sports story will **always** receive a sports image and will **never** fall back to political buildings, utility corridors, or religious figures.

---

## 3. Automated Self-Healing Engine (`is_story_image_mismatched`)
During every 15-minute cron run, the engine audits every existing story in `data/stories.json`:
- Automatically detects and replaces any religious or papal images on stories not explicitly about the Pope or Vatican.
- Detects and replaces any non-sports images (transmission lines, courtrooms, hospital pavilions) on sports stories.
- Detects and replaces any sports stadiums or ballparks on non-sports stories.
- Guarantees 100% domain compliance across the entire published feed.
