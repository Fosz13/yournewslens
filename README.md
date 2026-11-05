# Your News Lens — Extensive Sports Stream & Multi-Network Integration Guide

## 1. Overview
This update addresses the sports feed volume and source diversity, delivering an extensive, high-volume ("almost endless stream") catalog of sports stories when filtering by **Sports**, while maintaining a clean, balanced, and even category dispersal in the main **All Stories** feed.

---

## 2. Sports Network & Verified X Reporter Integration

### Configured Network Desks (`config.py`)
The ingestion pipeline connects to dedicated RSS endpoints across major sports networks:
- **ESPN Multi-Sport Desks**:
  - `ESPN Top News Wire`: 24/7 breaking athletic headlines
  - `ESPN NFL Insider Wire`: Comprehensive NFL franchise moves and injury reports
  - `ESPN NBA Wire`: Hardwood scores, rotations, and trade buzz
  - `ESPN MLB Wire`: Postseason pennant races and transactions
  - `ESPN College Football Wire`: College Football Playoff rankings and conference matchups
  - `ESPN Men's College Basketball`: NCAA rankings and tournament bracketology
  - `ESPN Soccer & Champions League`: European football and international wire
- **CBS Sports**:
  - `CBS Sports Wire`: Real-time breaking headlines
  - `CBS Sports NFL`: Depth chart and matchup analysis
  - `CBS Sports College Football`: National rankings and coaching developments
- **Fox Sports & Yahoo Sports**:
  - `Fox Sports National`: Collegiate and professional athletics wire
  - `Yahoo Sports Wire`: Breaking investigative features and highlights
- **The Athletic & Bleacher Report**:
  - `The Athletic Wire`: In-depth beat reporting and player access
  - `Bleacher Report Wire`: Real-time highlights and draft scouting

### Verified X (Twitter) Reporter Syndication Wires
To incorporate real-time dispatches from the top news reporters on X (Twitter), the engine utilizes syndicated Google News wire feeds targeting verified scoops and insider reports:
- **Adam Schefter** (`ESPN / NFL Insider`): Contract restructures, trades, and injury timelines
- **Shams Charania** (`The Athletic / ESPN / NBA Insider`): Breaking NBA trades, rotations, and front-office negotiations
- **Ian Rapoport** (`NFL Network / NFL Insider`): Real-time practice participation, MRI imaging reports, and game-day statuses
- **Jeff Passan** (`ESPN / MLB Insider`): International postings, free-agency benchmarks, and trade market movement
- **David Ornstein & Fabrizio Romano** (`The Athletic / Sky Sports / Football Insiders`): European transfers, contract agreements, and manager reactions
- **Pete Thamel & Brett McMurphy** (`ESPN / Action Network / College Sports Insiders`): Playoff committee deliberations and conference realignment
- **Bob Harig** (`Sports Illustrated / Golf Insider`): PGA Tour and Saudi PIF commercial alliance negotiations

---

## 3. Feed Balancing & "Endless Stream" Architecture

### Even Dispersal in Main Feed ("All Stories")
- In `engine.py`, `balance_feed_by_category()` employs an interleaved round-robin category distribution:
  - Round 1: Politics, Sports, World News, Business & Economy, Science & Tech, Entertainment, Health, Energy & Weather, Crime & Public Safety, Border & Security
  - Round 2: Politics, Sports, World News, Business & Economy, etc.
- As users scroll the default main feed, they experience a balanced, diverse rotation across all major topics without any single category dominating the top cards.

### High-Volume Stream on Sports Filter
- The pre-rendered card limit in `engine.py` (`[:35]`) was removed. All 84+ stories in the database—including **46 comprehensive sports stories**—are fully pre-rendered directly into `index.html`.
- When the user taps the **Sports** category pill:
  - `filterCategory('Sports')` matches `data-category="Sports"` and `data-master-category="Sports"`.
  - Non-sports cards are hidden, immediately revealing all 46 sports stories in a continuous, endless stream with zero loading latency.

---

## 4. Editorial Integrity & Architectural Safeguards
1. **Upcoming Event Previews**:
   - Fact 1 starts with `Current Betting Odds & Win Probability:` detailing spread, moneyline, over/under, and win percentage.
2. **Injury & Medical Emergency Reports**:
   - Strictly prohibited from betting odds (e.g. Vincent Kompany, Christian McCaffrey, Micah Parsons, Tua Tagovailoa, Joel Embiid). Fact 1 focuses on medical evaluation and rehabilitation timelines.
3. **Question & Response Headlines**:
   - Question headlines provide direct verdicts in Fact 1.
   - Response headlines provide direct quotes in Fact 1.
4. **Normal-Person Conversational Talking Points**:
   - Zero wooden constitutional slogans on sports stories; points sound like real sports fans and analysts discussing the game.
5. **100% Unique Image URLs**:
   - Domain-isolated sports photography across gridiron, hardwood, ballparks, pitches, golf links, and ice rinks with zero duplicate URLs and zero typewriter fallbacks.

---

## 5. Verification Suite
Run the 20-test automated regression suite:
```bash
python3 test_regression_suite.py
```
Expected output:
```
REGRESSION SUITE COMPLETED: 20/20 TESTS PASSED (100% SUCCESS)
```

## Mobile navigation and publisher-aware lens update

- Added a mobile-only navigation layout under 768px; desktop navigation rules remain intact.
- Search now spans the mobile header, the three-way lens selector is a compact full-width segmented control, view tabs share one row, and categories remain horizontally scrollable.
- Lens ranking now uses publisher orientation metadata rather than relying only on the article's `lean` field. Left and Right prioritize matching publishers; Balanced preserves the original chronological order.
- Added CNN, Fox News, The Guardian, HuffPost, and Washington Examiner feeds to broaden publisher coverage. Existing AP, Reuters, BBC, NPR, CBS, and other feeds remain available.
- Sports, entertainment, and weather stories are not promoted or demoted based on publisher orientation.

## Publishing and verification

The custom domain currently serves GitHub Pages. The **Ingest Wire Feeds & Update Stories** workflow publishes each changed edition to the `wire-data` branch on its 15-minute schedule or when run manually. GitHub Pages rebuilds on website changes pushed to `main`. The site fetches the live feed on page load and pull-to-refresh, and checks for a new edition every five minutes while visible. If the feed is unavailable, the bundled edition remains usable.

For the linked Netlify project, keep the production branch on `main` and exclude `wire-data` from branch deploys (select **None** or list only the branches you preview). Leave the existing build and publish settings in place. The branch also contains a `netlify.toml` ignore rule. Remove any Netlify build hook tied to feed publishing because hooks bypass ignore rules. Keep GitHub Pages set to **GitHub Actions** for the current public domain.

After merging, wait for the first workflow run to create `wire-data`. Run the workflow manually if it needs a retry. Confirm that the site displays the latest edition and that a scheduled or manual data-only run leaves `main` and the Netlify production deploy unchanged. GitHub's raw-file cache can take several minutes to expose a new edition. The repository must stay public for browser access to the feed.

- Run `python engine.py` to fetch and build a local edition. The publisher keeps an edition when all feeds fail and rejects empty output.
- Run `python -m unittest discover -s tests` and `node --test tests/polling.test.cjs` for offline regressions.
- Run `python build_site.py` to build `dist`. For a preview, use `python -m http.server --directory dist 8046`.
- Configure the existing `GEMINI_API_KEY` repository secret to enable sourced editorial analysis. Set `YNL_EDITORIAL_MODEL` only to override the default model. Each run analyzes at most six newly selected stories. With source-only publishing, only article evidence and narrowly defined polls appear.
- `scheduler.py` refreshes local files. Use GitHub Actions for production deployments. The sports-only runner uses the same source checks and rendering as the main wire.
- For voting, confirm the existing Supabase project has anonymous insert access on `poll_votes`, aggregate access through `get_poll_results(p_story_id)`, and a unique database constraint on `(story_id, voter_id)`. Test an insert and retry in a development project. Poll IDs include the current question and answer labels so revised questions start separate totals.
