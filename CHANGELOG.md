## 4. General Image Relevance & Entity Recognition Overhaul
- **Problem**: 
  - An article regarding "5 Takeaways From The Times's Re-Examination of the O.J. Simpson Case" showed power transmission lines.
  - An article regarding "France Reels After Largest Riots in Years" showed a yellow mechanical power cord reel.
  - Non-energy articles (such as maritime fentanyl interdiction and suspicious election mailings) were occasionally falling through to power transmission lines or sports stadiums.
- **Root Causes**:
  1. **Acronym & Initialism Exclusion**: The old regex `[A-Z][a-z]+` failed on dotted names like `O.J. Simpson`, bypassing named entity recognition and falling through to the generic backup pool.
  2. **Title-Case Verb Hallucination**: Common capitalized verbs (e.g. `Reels` in "France Reels After Largest Riots in Years") were sent to Wikipedia as single nouns, returning an electrical power cord reel.
  3. **Absence of Semantic Verification**: Wikipedia API results were accepted without checking whether the page description was a mechanical tool, hardware spool, or biological taxon.
  4. **Single Blind Fallback Pool**: When a story had no exact keyword match, a single global pool rotated through images, causing non-energy stories to be assigned power lines.
- **General Fix Implemented**:
  1. **Enhanced Named Entity Normalization**: Automatically normalizes initials (`O.J.` -> `OJ`) and extracts multi-word proper nouns (`OJ_Simpson`, `France_Riots`).
  2. **150+ Headline Noise Word Filtering**: Strictly prevents headline verbs (`reels`, `takes`, `slams`, `faces`, `sparks`, `eyes`, `bids`, `steps`, `warns`, `halts`, `drops`, `rises`, `kills`, `shoots`, etc.) and generic words (`case`, `years`, `takeaways`, `largest`) from being queried as entities.
  3. **Wikipedia Semantic Relevance Filter**: Verifies that returned Wikipedia summaries are not disambiguation pages, mechanical devices, spools, tools, or hardware.
  4. **Category-Specific Fallback Pools**: Replaced the global rotating backup pool with 10 dedicated category pools. Crime & Public Safety stories always receive courtrooms, gavels, or law enforcement; World News stories always receive diplomatic summits, protests, or international shipping. Power transmission lines can ONLY ever appear for Energy & Weather stories.
  5. **Automated Self-Healing Image Loop**: Scans all stories on every run and auto-replaces any mismatched images (e.g. power lines on non-energy, stadiums on non-sports, servers on non-tech).
  6. **Curated Coverage for Featured Stories**: Added verified images for O.J. Simpson (`📸 Wikimedia Commons / Court Pool Archive`), France Riots (`📸 European News Wire Archive`), Courtrooms, Cargo Ports, Nuclear SMRs, Semiconductors, and Geneva Talks.

# Your News Lens — Release Notes & Updates

## 1. Removed "Pragmatic Implementation" Framing Section
- **User Request**: *"I want to get rid of the entire section that has the pragmatic implementation text."*
- **Changes Applied**:
  - Completely removed `<div class="framing-headline">` across all 3 perspectives (Left, Balanced, Right) in `engine.py`, `app.js`, and `index.html`.
  - The card now flows directly from the Perspective Lens selector (`[ Left | Balanced | Right ]`) into `💬 Key Talking Points & Arguments`, eliminating redundant perspective summary headlines.

## 2. Enlarged Headline Images (Reduced Cropping)
- **User Request**: *"Some of the headline images seem to be cropped a little too much. Can we make that image bigger?"*
- **Changes Applied**:
  - Increased image viewport height by over 50%: from 145px to **220px on mobile**, and from 175px to **280px on desktop**.
  - Adjusted object positioning to `center 20%` to ensure subjects, signs, and faces at the top of photos are not cropped out.
  - Added subtle hover scale micro-interaction and pointer cursor feedback.

## 3. Interactive Click-to-Expand Feed (Faster, Cleaner Browsing)
- **User Request**: *"While we're at it, maybe you should have to click on the image or headline title to get the key faxed [key facts]. That way it's easier to scroll through a bunch of stories and only click the ones that you want"*
- **Changes Applied**:
  - Implemented an accordion-style **Click-to-Expand** experience on every story card.
  - In default collapsed state, cards display only the large photo, tags, title, and a modern prompt (`Tap to view Key Facts & Perspectives ▾`), reducing card height by ~50% for fast scanning.
  - Clicking on the **headline image**, the **headline title**, or the **expand prompt bar** smoothly expands the card to reveal the 4 Core Verified Facts, the 3-Way Lens Switcher, and the Talking Points quotes.
  - Tapping again smoothly collapses the card back.


## 5. Robust Fix for Cross-Domain Image Mismatches (e.g., Big 12 Football & The Pope)
- **Problem**: 
  - An article regarding "Big 12 football" was assigned a photograph of Pope Francis.
  - Potential cross-domain image pollution where sports stories could inherit religious clergy, courtroom gavels, or power transmission lines, and vice versa.
- **Root Causes Identified**:
  1. **Sports Term Omission in Classifier**: In `classify_article()`, standard collegiate and general sports terms (`football`, `college football`, `big 12`, `sec`, `big ten`, `acc`, `cfb`, `heisman`, `basketball`, etc.) were missing, causing Big 12 football stories to fall through to generic `National News`.
  2. **Zero Domain Checking on Wikipedia Results**: In `is_wikipedia_result_relevant()`, the `category` parameter was completely unused. If a headline contained a person named Pope (e.g. coach Mark Pope) or homonymous proper nouns, Wikipedia returned Pope Francis ("Head of the Catholic Church and bishop of Rome"), and the engine accepted it without checking domain compatibility.
  3. **Single Capitalized Word Extraction**: `extract_named_entities_from_title()` extracted isolated capitalized single words from title-case headlines (like `"Pope"`), querying them against Wikipedia instead of requiring multi-word context or domain validation.
  4. **Cross-Domain Topic Keyword Collisions**: In `SECONDARY_TOPIC_POOL`, the word `"power"` was listed under Energy & Weather, causing sports "power rankings" to match and inherit electrical transmission line towers when primary photos were unavailable.
  5. **Cross-Category Fallback Bleed**: Fallback resolution previously allowed stories in one category to fall back to generic national or political photos if category slots were full.
- **Robust Multi-Layer Architectural Fix Implemented**:
  1. **Sports Classifier Expansion**: Added comprehensive collegiate, professional, and Olympic sports keywords to `classify_article()` (`football`, `big 12`, `sec`, `big ten`, `acc`, `cfb`, `heisman`, `touchdown`, `bowl game`, `basketball`, `college basketball`, `ncaa`, `march madness`, etc.).
  2. **Domain-Enforcing Semantic Gatekeeper (`is_wikipedia_result_relevant`)**:
     - **Strict Religious/Pope Firewall**: Any Wikipedia entity describing the Pope, Papacy, Vatican, Bishop of Rome, Holy See, or Catholic clergy is **strictly forbidden** for Sports, Tech, and Energy stories. Pope images are ONLY permitted if the headline explicitly mentions religious keywords (`pope`, `vatican`, `papal`, `pontiff`, `holy see`) and the category is not sports.
     - **Positive Sports Affinity Requirement**: For Sports stories, the Wikipedia description or extract **must** contain positive sports terminology (`sport`, `athlete`, `player`, `coach`, `football`, `basketball`, `baseball`, `team`, `stadium`, `tournament`, etc.). Any entity without verified sports context is rejected immediately.
  3. **Headline Noise Word & Ambiguous Noun Filtering**: Added ambiguous single words (`pope`, `king`, `power`, `rankings`, `conference`, `division`, `bowl`, `game`, `state`, etc.) to `HEADLINE_NOISE_WORDS` so they are never queried as isolated single-word entities, while preserving multi-word entities (`Mark_Pope`, `Big_12_Conference`, `Pope_Francis`).
  4. **Dedicated Exact Entity Coverage**: Added dedicated mappings in `EXACT_ENTITY_PHOTOGRAPHY` for Big 12 Football & Athletics (`📸 Big 12 / College Sports Wire`), College Football & Conferences (`📸 NCAA / College Football Media`), and College Basketball (`📸 NCAA / College Basketball Wire`).
  5. **Domain-Aligned Secondary Topic Matcher**: Enforces strict category affinity so Sports stories only match Sports topic photographic libraries, completely eliminating "power rankings" collisions.
  6. **Isolated Category Fallbacks**: Each category draws exclusively from its own curated photographic pool (`CATEGORY_FALLBACK_POOLS["Sports"]` for sports), guaranteeing zero cross-domain leakage.
  7. **Automated Self-Healing Image Audit**: `is_story_image_mismatched()` proactively audits all existing and newly ingested stories, automatically replacing any papal, religious, or cross-domain images on stories that do not belong to that domain.
