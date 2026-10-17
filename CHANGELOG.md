# Your News Lens — Fixes & Feature Changelog

## 1. Filter Logic Fix (National + Sports)
- **Problem**: When clicking **National** in the top master category and **Sports** in the subcategory row, the feed displayed 0 stories. However, clicking **All Stories** + **Sports** revealed the Dodgers story.
- **Root Causes**:
  1. Domestic American sports (MLB, NFL, NBA, NCAA, PGA) were classified as `master_category: "Sports"`, while the **National** filter only looked for `master_category: "National Headlines"`.
  2. The filter condition in `reapplyCategoryFilter()` did not include sports under national coverage.
  3. Story cards were rendering duplicate badges (`[SPORTS] [SPORTS]`).
- **Fixes Applied**:
  1. Updated `classify_article()` in `engine.py` so all domestic American sports are classified under `master_category: "National Headlines"` and `category: "Sports"`.
  2. Updated `reapplyCategoryFilter()` in `index.html` so clicking **National** seamlessly matches domestic sports alongside politics, economy, energy, and healthcare.
  3. Updated badge rendering so stories show `[NATIONAL] [SPORTS]` or a clean single category badge, completely eliminating the duplicate `[SPORTS] [SPORTS]` tag.

## 2. Core Facts Upgrade (3 Bulleted Facts per Story)
- **Problem**: The "Core Facts" section previously repeated the headline text and, in some cases (such as the Bo Nix / Ryan Fitzpatrick story), appended irrelevant medical injury boilerplate because of an over-broad keyword match (`"qb"`, `"quarterback"`).
- **Fixes Applied**:
  1. Narrowed specific injury regexes in `engine.py` (e.g., Jalen Hurts) strictly to `jalen hurts` and `blood clot`, preventing cross-story collisions.
  2. Added a structured `core_facts` array containing **3 distinct, verified factual bullet points** per story:
     - **Fact 1**: Primary event, action, or decision (without re-echoing the headline).
     - **Fact 2**: Specific quantitative figures, quotes, or background context.
     - **Fact 3**: Procedural status, upcoming timeline, or division/game impact.
  3. Updated the card layout in `index.html` to present the core facts as an elegant, high-contrast bulleted list (`<ul class="core-facts-list">`) under `⚖️ The Core Facts (Verified Breakdown)`.
  4. Updated AI prompts in `engine.py` for Gemini and OpenAI to enforce 3 distinct facts on future automated wire ingestion runs.

## 3. Comprehensive Synthesis & Boilerplate Elimination Fix
- **Problem**:
  1. **Core Facts**: The synthesizer was echoing the article headline as Fact 1, followed by two static boilerplate statements ("Verified reports and regulatory filings outline the specific operational context and data", "Stakeholders and affected organizations established immediate procedural timelines as developments proceed").
  2. **Why It Matters**: The section was repeating the exact same three generic points across almost every article ("Assesses the realistic legal, operational, and administrative factors required to effectively manage [headline]...", "Seeks balanced middle-ground solutions...", "Maintains institutional stability by relying on verified evidence...").
  3. **Key Talking Points**: The debate soundbites were repeating the exact same two clichés across articles ("Effective governance requires examining all facts calmly and crafting pragmatic, balanced solutions", "Extreme rhetoric solves nothing; steady institutional collaboration delivers real, sustainable progress").
- **Root Causes**:
  1. In `engine.py`, `call_ai_synthesizer()` never requested `"core_facts"` in its LLM prompt, causing the pipeline to always fall back to default boilerplate tuples.
  2. In `generate_contextual_synthesis()`, any article that didn't match an exact hardcoded keyword fell through to an `else` block that outputted the static placeholder sentences.
  3. The self-healing function `is_story_mismatched()` did not scan for those placeholder phrases and never updated `core_facts` upon re-synthesis.
- **Fixes Applied**:
  1. **Substantive Sentence & Quote Extraction (`extract_facts_from_context_and_title`)**: Built a natural language extractor that pulls 3 distinct, verified factual sentences from article context, quotes, numbers, dates, and named entities, strictly filtering out any sentence that repeats the headline.
  2. **Domain-Specific Perspectives**: Expanded `generate_contextual_synthesis()` with deep, unique analytical framing, why-it-matters breakdowns, and lay-term debate talking points across all major news categories (healthcare access & caregiver housing, congressional budget, energy grids, interest rates, sports, border security, defense, pharmaceuticals, Big Tech, and AI).
  3. **AI Synthesizer Prompt Hardening**: Updated `call_ai_synthesizer()` to explicitly demand 3 non-headline-repeating facts, 3 perspective-tailored why-it-matters bullets, and 2 conversational lay-term talking points from Gemini/OpenAI, and safely parses them into the story schema.
  4. **Self-Healing Enforcement**: Updated `is_story_mismatched()` to automatically detect and flag any generic filler phrases or headline repeats, immediately re-synthesizing `core_facts`, `neutral_summary`, and `perspectives`.
  5. **Full Feed Re-Synthesis**: Re-synthesized all 28 stories in `data/stories.json` (0 flagged stories remaining), added the NPR *"Sidewalk sleepers"* story with full tailored facts and perspectives, and pre-rendered all cards into `index.html`.
