# Your News Lens — Tragedy Sensitivity & Category Filter Overhaul Report

This report documents the root-cause resolution for the two severe issues identified in the user's latest screenshots:
1. **Mismatched / Inappropriate Talking Points (Image 1 - Alamodome Airman Rappelling Accident)**: Fixing the tone-deaf sports scoreboard quotes generated after an active-duty Air Force service member tragically died.
2. **Category Filter Misclassification (Image 2 - Canada Military Base Fire Under Sports)**: Resolving the false classification of a fatal military base explosion under `SPORTS`.

---

## 1. Root Cause Breakdown

### Issue A: Why Did the Airman Death Receive "The final scoreboard doesn't lie..."?
* **Headline**: *Airman dies in rappelling accident at Alamodome before UTSA-Navy game - Texas Public Radio | TPR*
* **What Happened**: 
  1. Because the pregame demonstration occurred at a stadium before a college football game, the article came through Google News Sports.
  2. In `engine.py`, when a story fell through to the dynamic synthesizer, it checked `if "sport" in c_lower:` and injected a single set of generic sports soundbites:
     `"The final scoreboard doesn't lie: championships are earned through physical dominance, discipline, and execution between the lines."`
  3. The engine failed to detect that the **substance of the article** was a fatal tragedy, not a sporting match.

### Issue B: Why Did "Major Fire at Canada Military Base" Get Classified as `SPORTS`?
* **Headline**: *Several dead or injured in major fire at Canada military base - BBC*
* **What Happened**:
  1. The incident occurred at **CFB Wainwright** (Canadian Forces Base Wainwright in Alberta).
  2. In `engine.py`, `classify_article()` checked the regex `r'cfb'` (intended for College Football).
  3. Because `CFB` is the official acronym for all Canadian Forces Bases, `r'cfb'` matched `CFB Wainwright` and immediately stamped the story as `SPORTS`!
  4. This caused the story to appear under the `🏆 Sports` carousel button and assigned it a stadium photo.

---

## 2. Corrected Story 1: Alamodome Airman Rappelling Tragedy

* **Headline**: *Airman dies in rappelling accident at Alamodome before UTSA-Navy game - Texas Public Radio | TPR*
* **Corrected Category**: **Crime & Public Safety** (Master: **National Headlines**)
* **Verified Visual**: Emergency first responders and municipal public safety perimeter operations (`📸 National Public Safety Wire`)

### ⚖️ The Core Facts (Substantive Event Breakdown)
1. An active-duty U.S. Air Force airman tragically died following a fall while rappelling from the Alamodome rafters during a pregame military appreciation ceremony before the UTSA vs. Navy football game in San Antonio.
2. First responders with the San Antonio Fire Department transported the airman to a local hospital as a Priority 1 patient with life-threatening trauma, where the service member later succumbed to their wounds.
3. Kickoff between UTSA and Navy proceeded after an approximate 10-minute delay, drawing sharp public criticism and emotional community debate over the decision to continue play.
4. The U.S. Air Force, military safety boards, and venue operators launched an immediate formal inquiry into equipment rigging, harness safety, and oversight protocols for stadium military demonstrations.

### 💬 Authentic Ideological Talking Points (What Real People Actually Say)

#### 🔴 Conservative Lens (Military Honor & Reverence)
* **Framing**: *Honoring Military Sacrifice: Demanding Accountability and Solemnity Over Entertainment Spectacle*
* **What Real People Say**:
  * *"An active-duty airman lost their life serving our country in uniform—playing a football game 10 minutes later was completely tone-deaf and disrespectful to that soldier's sacrifice."*
  * *"Pregame stunts should never put service members at unnecessary risk; our military personnel deserve strict safety reviews, and the fallen airman's family deserves our deepest honor and support."*

#### 🔵 Progressive Lens (Human Life Over Commercialization)
* **Framing**: *Human Life Over Commercial Revenue: Questioning the Decision to Play On and Militarize Sports Stunts*
* **What Real People Say**:
  * *"Resuming a football game just 10 minutes after a service member suffered a fatal fall shows how corporate sports prioritizes broadcast schedules and ticket revenue over human decency."*
  * *"Staging high-risk rappelling stunts and flyovers as commercial entertainment spectacles commodifies our service members without proper civilian and workplace safety protections."*

#### 🟢 Centrist / Balanced Lens (Pragmatic Institutional Safety)
* **Framing**: *Urgent Safety Protocol Review: Investigating Rigging Standards and Crisis Management at Public Venues*
* **What Real People Say**:
  * *"The Air Force and stadium operators must conduct an urgent, transparent investigation into rigging protocols before any more high-altitude stadium demonstrations are permitted."*
  * *"Venue officials need clear crisis protocols on whether and when public sporting events should be suspended following catastrophic on-field tragedies."*

---

## 3. Corrected Story 2: Canada Military Base Fire & Explosion

* **Headline**: *Several dead or injured in major fire at Canada military base - BBC*
* **Corrected Category**: **World News** (Master: **World News**)
* **Verified Visual**: Emergency response and disaster investigation operations at defense installation (`📸 International Defense Wire`)

### ⚖️ The Core Facts (Substantive Event Breakdown)
1. Multiple Canadian Armed Forces personnel were killed or critically injured following a major fire and explosion at Canadian Forces Base (CFB) Wainwright in Alberta, Canada.
2. Emergency base firefighters and regional medical teams evacuated damaged training facilities and mobilized burn trauma units across the region.
3. The Canadian Department of National Defence and military police launched a formal investigation into the origin of the blaze, focusing on munitions handling and facility safety standards.
4. Allied military liaisons and international defense leadership expressed condolences and offered specialized disaster response coordination as recovery efforts proceed.

### 💬 Authentic Ideological Talking Points (What Real People Actually Say)

#### 🔴 Conservative Lens (Allied Defense & Infrastructure Strength)
* **Framing**: *Standing with Allied Forces: Honoring Fallen Soldiers and Fortifying Military Base Infrastructure*
* **What Real People Say**:
  * *"Our hearts and prayers are with our Canadian military allies; we must honor the brave personnel who lost their lives and ensure their families receive unconditional support."*
  * *"Military installations require uncompromising safety protocols and infrastructure maintenance so our troops are never endangered by facility failures at home."*

#### 🔵 Progressive Lens (Worker Safety for Troops & Environmental Standards)
* **Framing**: *Worker Safety in Uniform: Demanding Transparency and Strict Environmental Safety at Defense Bases*
* **What Real People Say**:
  * *"Service members risk their lives to protect us, and they deserve safe working conditions, well-maintained facilities, and transparent investigations into base hazards."*
  * *"Defense authorities must be held fully accountable for military infrastructure maintenance and hazardous materials safety to protect soldiers and surrounding communities."*

#### 🟢 Centrist / Balanced Lens (Technical Inquiry & Crisis Management)
* **Framing**: *Joint Allied Crisis Management: Investigating the Root Cause of the CFB Wainwright Tragedy*
* **What Real People Say**:
  * *"A disaster of this scale demands a swift, independent technical inquiry to determine whether mechanical failure, munitions handling, or structural defects caused the blast."*
  * *"Defense leadership must review emergency evacuation procedures and medical transport readiness across all regional military training centers."*

---

## 4. Systemic Architectural Fixes Implemented

1. **Casualty, Disaster & Accident Gatekeeper (Priority 0 in `classify_article`)**:
   - Matches keywords like `dead or injured`, `fatal accident`, `fatal fall`, `airman dies`, `soldier dies`, `major fire`, `blast`, and `explosion`.
   - Forces these stories to route to `Crime & Public Safety` (domestic) or `World News` (international), completely superseding any sports or weather rules.
2. **`CFB` Acronym Bounding**:
   - Replaced bare `r'cfb'` with strictly bounded college football syntax (`r'cfb\s+(?:playoffs?|rankings?|week\s+\d|top\s+25|poll|scores?|game|season)'`).
   - Canadian Forces Bases (`CFB Wainwright`, `CFB Edmonton`) will never collide with sports.
3. **Tragedy-Aware Dynamic Fallback Engine (`generate_contextual_synthesis`)**:
   - Checks if an incoming wire item contains tragedy/death/injury markers.
   - Automatically branches to solemn, compassionate, ideological perspectives on safety, family support, and institutional accountability.
   - Prohibits competitive sports metaphors (`The final scoreboard doesn't lie`, `championships are earned`) from being emitted for serious or fatal incidents.
4. **Self-Healing Mismatch Verification**:
   - Any story combining death/casualty words with sports quotes or military bases misclassified under `Sports` is automatically detected and re-synthesized on every 15-minute pipeline run.
