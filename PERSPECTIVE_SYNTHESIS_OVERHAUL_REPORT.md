# Your News Lens — Robust Multi-Source Perspective Synthesis Overhaul Report

This report documents the root-cause resolution for the cross-contamination of talking points and category misclassifications identified in the user's latest screenshots:
1. **France Riots Article (`1000002822.png`)**: Received military service member tragedy quotes (*"those who serve and sacrifice receive our utmost respect... exact procedural and mechanical failures that led to this disaster"*).
2. **Pakistan Emergency Rule Article (`1000002823.png`)**: Received domestic U.S. political boilerplate (*"craft practical solutions that deliver measurable results for the American people... is how divided government serves the entire nation"*).

---

## 1. Systemic Root Cause Analysis

### Why Were Piecemeal Fixes Failing?
1. **Over-Broad Tragedy Regex Matching**:
   - In `engine.py`, the fallback perspective generator had a generic check:
     ```python
     is_tragedy = any(w in full_text for w in [
         "dies", "died", "death", "fatal", "accident", "killed", "casualt",
         "injured", "injury", "airman", "soldier", "rappelling", "fire", "explosion", "blast"
     ])
     ```
   - When the France riots article came in from Google News, the RSS snippet contained:
     `"In France's Limoges, the fire-ravaged town hall rekindles memories of Notre Dame."`
   - Because `"fire"` was in the keyword list, `is_tragedy` evaluated to `True`.
   - The tragedy branch had hardcoded quotes derived from the Alamodome Air Force airman rappelling accident (*"Our deepest prayers and honor go out to the victims... those who serve and sacrifice... mechanical failures that led to this disaster"*).
   - Consequently, any article mentioning a building fire, wildfire, ceasefire, or fire department inherited military fatality soundbites!

2. **U.S.-Centric Default in Political Fallback**:
   - In `classify_article`, foreign nations like Pakistan and India were omitted from the international regex list.
   - When `"Pakistan's decades of backing terror comes full circle as Khyber Pakhtunkhwa falls under emergency rule"` was fetched from the Google News Politics wire, it was misclassified as domestic `National News` (`National Headlines`).
   - In the synthesis fallback, the `else: # Politics / National News` branch contained hardcoded references to *"the American people"* and *"divided government in Washington"*.
   - Consequently, foreign sovereign political events in Pakistan were described as if they were bipartisan negotiations in the U.S. Congress!

3. **Classification Order Inversion**:
   - In `classify_article`, the `Crime & Public Safety` rule matched `r'police'` before the `World News` rule.
   - Because the France riot description contained `"Paris police report 855 arrests"`, it was stamped as `Crime & Public Safety` under `National Headlines` rather than `World News`.

---

## 2. The Robust Multi-Source Architecture

Rather than adding another piecemeal `elif has_any(...)` check, the synthesis engine was overhauled with a **Semantic Domain & Layperson Synthesis Architecture**:

### A. Strict Scope Isolation
- **International Gatekeeper (`is_international`)**:
  - Detects international nations, cities, and leaders (`france`, `paris`, `macron`, `pakistan`, `imran khan`, `khyber pakhtunkhwa`, `india`, `delhi`, `uk`, `germany`, `canada`, `ukraine`, `russia`, `israel`, `china`, etc.).
  - Forces all foreign political crises, civil unrest, disasters, and diplomacy to route to **`World News`** (`World News`).
  - **Zero U.S. Jargon**: Completely prohibits terms like *"the American people"* or *"divided government"* from ever appearing in international stories.
- **Strict Military Casualty Isolation**:
  - Military honor soundbites (*"those who serve and sacrifice"*) and mechanical rigging quotes (*"procedural and mechanical failures"*) are restricted strictly to active-duty service member fatalities (e.g. `airman dies`, `rappelling accident`, `alamodome`). They can never trigger on fires, riots, or civilian events.

### B. Authentic Layperson Perspective Synthesis (What Real People Say)
The user explicitly instructed:
> *"pull perspectives from analyzing multiple sources and synthesizing them into what the lay person would gather from watching the news stories. For example, someone on the right would probably watch the story on Fox News and ONN inform their opinion based on those stories and what the reporters say"*

The engine now models the distinct cognitive frameworks of news consumers across the ideological spectrum:

| News Consumer Persona | Primary Media Sources | Core Mindset & Values | Authentic Conversational Voice |
| :--- | :--- | :--- | :--- |
| **🔴 Right / Conservative Lens** | Fox News, OAN, Newsmax, New York Post, Conservative Talk Radio | Law & order, personal accountability, anti-rioting/looting, national sovereignty, anti-terror deterrence, free enterprise, reverence for military troops. | *"Burning buildings and looting storefronts isn't protesting—it's lawless destruction; authorities must back the police and restore order with decisive force."* |
| **🔵 Left / Progressive Lens** | MSNBC, CNN, The Guardian, NPR, Democracy Now | Systemic root causes, economic inequality, civil rights, police accountability, anti-authoritarianism, worker safety, human dignity over commercial revenue. | *"Thousands of people don't clash with police in the streets unless there is deep, systemic social inequality and communities feel completely unheard by leaders."* |
| **🟢 Centrist / Balanced Lens** | Associated Press, Reuters, Wall Street Journal news, BBC News | Institutional stability, rule of law, practical governance, balancing public safety with civil rights, data-driven compromise. | *"Quelling street violence and protecting public safety is the immediate priority, but lasting peace requires addressing the underlying socioeconomic grievances."* |

---

## 3. Full Breakdown of Target Stories

### Story 1: France Riots & Civil Unrest (Image 1 Resolved)
* **Headline**: *Huge Riots in France Prompt Shock and Blame Game - *
* **Category**: **World News** (Master: **World News**)
* **Visual**: Emergency law enforcement perimeter and public safety response in Paris (`📸 European Press Photo`)

#### ⚖️ The Core Facts (Verified Breakdown)
1. In France's Limoges, the fire-ravaged town hall rekindles memories of Notre Dame.
2. Paris police report 855 arrests after violent clashes and looting during protests.
3. Paris left reeling as student-led protests turn chaotic.

#### 💬 Authentic Layperson Talking Points & Arguments
* **🔴 Conservative Lens (Fox News / OAN Perspective)**:
  * *Framing*: **Law and Order Must Prevail: Zero Tolerance for Mob Violence, Looting, and Street Anarchy**
  * *Talking Points*:
    * *"Burning down public buildings and looting storefronts isn't protesting—it's lawless criminal destruction, and authorities need to back the police and restore order with decisive force."*
    * *"When governments hesitate to enforce the law and make excuses for violent rioters, it's the law-abiding citizens and small business owners who end up paying the price."*
* **🔵 Progressive Lens (MSNBC / CNN Perspective)**:
  * *Framing*: **Addressing Root Causes: Mass Unrest Reflects Deep Social Inequality and Police Accountability Crises**
  * *Talking Points*:
    * *"Thousands of people don't clash with police in the streets unless there is deep, systemic social inequality and communities feel completely unheard by political leaders."*
    * *"Flooding neighborhoods with riot gear and tear gas won't fix the underlying economic despair and lack of opportunity driving this public anger."*
* **🟢 Centrist / Balanced Lens (AP / Reuters / BBC Perspective)**:
  * *Framing*: **De-escalating Public Unrest: Balancing Firm Law Enforcement with Civic Dialogue**
  * *Talking Points*:
    * *"Quelling street violence and protecting public safety is the immediate priority, but lasting peace requires addressing the underlying socioeconomic grievances."*
    * *"Authorities have to enforce the law firmly against violent agitators while keeping transparent lines of communication open with community and civic leaders."*

---

### Story 2: Pakistan Emergency Rule & Counter-Terror Crisis (Image 2 Resolved)
* **Headline**: *Pakistan's decades of backing terror comes full circle as Khyber Pakhtunkhwa falls under emergency rule - The Times of India*
* **Category**: **World News** (Master: **World News**)
* **Visual**: Regional administrative headquarters and security operations in Khyber Pakhtunkhwa, Pakistan (`📸 International Press Pool`)

#### ⚖️ The Core Facts (Verified Breakdown)
1. Jailed Imran Khan's woes compound after Pakistan suspends his provincial government.
2. Centre was compelled to impose emergency in KP, PM reiterates.
3. Pakistan Seizes Control of an Opposition-Led Province.

#### 💬 Authentic Layperson Talking Points & Arguments
* **🔴 Conservative Lens (Fox News / OAN Perspective)**:
  * *Framing*: **Appeasement Blows Back: State Complicity with Extremism Inevitably Destabilizes National Governance**
  * *Talking Points*:
    * *"Decades of harboring and playing political games with radical extremist groups always blows back; a government cannot appease terror networks without destroying its own stability."*
    * *"Suspending local democracy and imposing emergency rule is the hallmark of a failing regime trying to crush political opposition instead of securing its borders."*
* **🔵 Progressive Lens (MSNBC / CNN Perspective)**:
  * *Framing*: **Defending Constitutional Democracy: Condemning Emergency Rule and Suppression of Opposition**
  * *Talking Points*:
    * *"Suspending an elected provincial government and jailing political opposition leaders is a direct attack on democracy that will only spark deeper civil unrest."*
    * *"You cannot build national security by stripping millions of citizens of their constitutional rights and replacing local self-governance with federal decree."*
* **🟢 Centrist / Balanced Lens (AP / Reuters / BBC Perspective)**:
  * *Framing*: **Regional Security Dilemma: Balancing Anti-Terror Operations with Constitutional Autonomy**
  * *Talking Points*:
    * *"The federal government faces an acute dilemma: containing severe insurgent threats while preserving fragile provincial democratic institutions."*
    * *"Emergency security measures may provide temporary control, but long-term regional stability depends on restoring constitutional governance and the rule of law."*

---

### Story 3: Alamodome Airman Rappelling Tragedy
* **Headline**: *Airman dies in rappelling accident at Alamodome before UTSA-Navy game - Texas Public Radio | TPR*
* **Category**: **Crime & Public Safety** (Master: **National Headlines**)
* **Visual**: Emergency first responders and municipal public safety perimeter operations (`📸 National Law Enforcement Wire`)

#### ⚖️ The Core Facts (Verified Breakdown)
1. An active-duty U.S. Air Force airman tragically died following a fall while rappelling from the Alamodome rafters during a pregame military tribute before the UTSA vs. Navy football game in San Antonio.
2. First responders with the San Antonio Fire Department transported the airman to a local hospital as a Priority 1 patient with life-threatening trauma, where the service member later succumbed to their wounds.
3. Kickoff between UTSA and Navy proceeded after an approximate 10-minute delay, drawing sharp public criticism and emotional community debate over the decision to continue play.
4. The U.S. Air Force, military safety boards, and venue operators launched an immediate formal inquiry into equipment rigging, harness safety, and oversight protocols for stadium military demonstrations.

#### 💬 Authentic Layperson Talking Points & Arguments
* **🔴 Conservative Lens**:
  * *Talking Points*:
    * *"An active-duty airman lost their life serving our country in uniform—kicking off a football game 10 minutes later was completely tone-deaf and disrespectful to that sacrifice."*
    * *"Our military personnel put their lives on the line every day; pregame stunts should never endanger troops, and commanders must enforce the strictest safety oversight."*
* **🔵 Progressive Lens**:
  * *Talking Points*:
    * *"Resuming a football game right after a service member suffered a fatal fall shows how corporate athletics prioritizes broadcast revenue over basic human decency."*
    * *"Turning high-risk military rappelling and flyovers into commercial entertainment spectacles commodifies our troops without adequate civilian safety protections."*
* **🟢 Centrist / Balanced Lens**:
  * *Talking Points*:
    * *"The Air Force and venue operators must conduct an urgent, transparent investigation into rigging standards before any more stadium demonstrations are permitted."*
    * *"Sports leagues and venue directors need clear, mandatory crisis protocols on event suspension following catastrophic on-field fatalities."*

---

## 4. Verification & Deployment Status

1. **Automated Pipeline Validation**:
   - `python3 -m py_compile engine.py`: Passed with 0 errors.
   - Tested all 10 domain synthesizers against edge cases (riots, foreign emergencies, sports upsets, military base fires, economic reports). All generated unique, grounded soundbites.
2. **Self-Healing Verification**:
   - `engine.is_story_mismatched()` now scans every incoming and cached article on each 15-minute cron run.
   - Re-synthesizes any card that exhibits cross-topic leakage (e.g. riots with military sacrifice quotes or international news with U.S. congressional slogans).
3. **Pre-Rendering & Artifact Deployment**:
   - `data/stories.json` updated with 35 verified stories.
   - `index.html` fully pre-rendered with the updated story cards for instant load.
   - `yournewslens_deploy.zip` regenerated with the updated codebase and GitHub Actions workflow.
