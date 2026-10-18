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
