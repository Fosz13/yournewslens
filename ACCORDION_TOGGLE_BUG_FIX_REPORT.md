# Your News Lens — Accordion Toggle ('View Key Facts & Perspectives') Bug Fix Report

This report documents the root-cause diagnosis and systemic resolution for the issue where tapping the **"View Key Facts & Perspectives"** button produced no visible action on articles across [Your News Lens](https://yournewslens.com/).

---

## 1. Root Cause Breakdown

When users clicked **"Tap to view Key Facts & Perspectives"** (or the headline/image), the click handler executed `toggleStoryDetails(storyId)`. However, nothing opened due to three compounding defects:

1. **Missing Element IDs in Dynamic Feed Generation (`renderStoriesFeed`)**:
   - In `renderStoriesFeed()` (within both `index.html` and `app.js`), the dynamically generated card template constructed the prompt bar and details wrapper without unique IDs:
     ```javascript
     html += '    <div class="expand-prompt-bar" onclick="toggleStoryDetails(&quot;' + sId + '&quot;)">';
     html += '      <span class="expand-label">Tap to view Key Facts & Perspectives</span>';
     html += '      <span class="expand-chevron">▾</span>';
     html += '    </div>';
     html += '    <div class="card-details">';
     ```
   - As a result, the `<div class="card-details">`, `<span class="expand-label">`, and `<span class="expand-chevron">` lacked the expected IDs (`id="{sId}-details"`, `id="{sId}-expand-label"`, `id="{sId}-chevron"`).

2. **Function Shadowing & Hard Early Exit in `toggleStoryDetails`**:
   - In earlier versions, two distinct definitions of `toggleStoryDetails(storyId)` were declared in `index.html` and `app.js`.
   - The later definition at the bottom of the script shadowed the first:
     ```javascript
     function toggleStoryDetails(storyId) {
       var details = document.getElementById(storyId + '-details');
       var label = document.getElementById(storyId + '-expand-label');
       var chevron = document.getElementById(storyId + '-chevron');
       if (!details) return; // <--- FAILED SILENTLY HERE
       var isHidden = details.style.display === 'none';
       details.style.display = isHidden ? 'block' : 'none';
       ...
     }
     ```
   - Because `renderStoriesFeed` generated `<div class="card-details">` without an `id`, `document.getElementById(storyId + '-details')` returned `null`.
   - The guard clause `if (!details) return;` aborted execution immediately on every article, making the button completely non-responsive.

3. **CSS Transform Inversion on Chevron Glyphs**:
   - In `styles.css` and inline styles, `.compact-card.expanded .expand-chevron` had `transform: rotate(180deg);`.
   - Simultaneously, the JavaScript explicitly swapped the glyphs between `▾` (down arrow) and `▴` (up arrow).
   - Rotating an upward triangle `▴` by 180 degrees produced a downward triangle, causing the arrow to point in the wrong direction upon expansion.

---

## 2. Architecture of the Resolution

### A. Unified, State-Aware `toggleStoryDetails(storyId)`
The duplicate implementations were replaced with a single robust, query-safe function in both `index.html` and `app.js`:
```javascript
function toggleStoryDetails(storyId) {
  var card = document.getElementById(storyId);
  if (!card) return;

  var details = document.getElementById(storyId + '-details') || card.querySelector('.card-details');
  var label = document.getElementById(storyId + '-expand-label') || card.querySelector('.expand-label');
  var chevron = document.getElementById(storyId + '-chevron') || card.querySelector('.expand-chevron');

  var isCurrentlyOpen = card.classList.contains('expanded');
  if (details) {
    if (details.style.display === 'block') {
      isCurrentlyOpen = true;
    } else if (details.style.display === 'none') {
      isCurrentlyOpen = false;
    }
  }

  var shouldBeOpen = !isCurrentlyOpen;

  if (shouldBeOpen) {
    card.classList.add('expanded');
    if (details) details.style.display = 'block';
    if (label) label.textContent = 'Hide Key Facts & Perspectives';
    if (chevron) chevron.textContent = '▴';
  } else {
    card.classList.remove('expanded');
    if (details) details.style.display = 'none';
    if (label) label.textContent = 'Tap to view Key Facts & Perspectives';
    if (chevron) chevron.textContent = '▾';
  }
}
```
**Key Advantages**:
- **Dual Lookup Strategy**: Checks for unique IDs (`storyId + '-details'`) first, and seamlessly falls back to `card.querySelector('.card-details')` if IDs are absent.
- **Dual Display & Class Sync**: Explicitly controls `details.style.display` (`'block'` vs `'none'`) while toggling `.expanded` on the parent card, ensuring compatibility with all CSS specifications.
- **Accurate State Detection**: Correctly identifies whether the panel is currently open regardless of whether the state was driven by CSS classes or inline styles.

---

### B. Standardized Card DOM Templates
In `renderStoriesFeed()` (`index.html` and `app.js`) and `prerender_cards_html()` (`engine.py`), the card markup now standardizes unique IDs and classes:
```html
<div class="expand-prompt-bar" onclick="toggleStoryDetails('{sId}')">
  <span class="expand-label" id="{sId}-expand-label">Tap to view Key Facts & Perspectives</span>
  <span class="expand-chevron" id="{sId}-chevron">▾</span>
</div>

<div class="card-details" id="{sId}-details">
  <!-- ⚖️ Core Facts Breakdown -->
  <!-- 🟢 Balanced / 🔴 Conservative / 🔵 Progressive Perspectives -->
  <!-- 💬 Layperson Talking Points & Arguments -->
  <!-- 🔍 Analytical Conclusions & Voices -->
</div>
```

---

### C. Chevron Glyph Normalization
Removed `transform: rotate(180deg)` from `.compact-card.expanded .expand-chevron` in both `styles.css` and `index.html`. The chevron text content directly controls orientation:
- **Collapsed**: `▾` (pointing down)
- **Expanded**: `▴` (pointing up)

---

## 3. Verification & Testing

1. **Automated DOM Simulation (Node.js)**:
   - Validated click transitions with mock DOM structures both with and without child IDs:
     - **Initial state**: `expanded = false`, `display = none`, text = `"Tap to view Key Facts & Perspectives"`, chevron = `▾`.
     - **Click 1 (Open)**: `expanded = true`, `display = block`, text = `"Hide Key Facts & Perspectives"`, chevron = `▴`.
     - **Click 2 (Close)**: `expanded = false`, `display = none`, text = `"Tap to view Key Facts & Perspectives"`, chevron = `▾`.
2. **Pre-Rendered & Dynamic Feed Verification**:
   - Verified that pre-rendered static cards in `index.html` start cleanly collapsed.
   - Verified that live feed cards rendered via `loadLiveStories()` from `data/stories.json` retain full ID bindings and toggle flawlessly.
3. **Deployment Package Rebuilt**:
   - `yournewslens_deploy.zip` regenerated containing all updated files (`index.html`, `app.js`, `styles.css`, `engine.py`, and `CHANGELOG.md`).
