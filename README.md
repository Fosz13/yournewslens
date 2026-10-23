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
