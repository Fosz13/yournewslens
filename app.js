/**
 * YOUR NEWS LENS — LIVE WIRE & EDITORIAL INTELLIGENCE CONTROLLER (v4.0)
 * Published feed navigation, filtering, and edition refresh
 */

(function() {
  if (typeof window !== 'undefined' && window.__YOUR_NEWS_LENS_INITIALIZED__) {
    return;
  }
  if (typeof window !== 'undefined') {
    window.__YOUR_NEWS_LENS_INITIALIZED__ = true;
  }

  var currentGlobalPerspective = 'CENTER';
  try {
    var savedPref = localStorage.getItem('userLensPreference');
    if (savedPref && (savedPref === 'LEFT' || savedPref === 'CENTER' || savedPref === 'RIGHT')) {
      currentGlobalPerspective = savedPref;
    }
  } catch (e) {}

  var currentFilterCategory = 'All';
  var currentSearchQuery = '';

  // Theme Controller (Dark Obsidian Default + Light Alabaster Mode)
  function toggleThemeMode() {
    var root = document.documentElement;
    var current = root.getAttribute('data-theme') || 'dark';
    var next = (current === 'dark') ? 'light' : 'dark';
    root.setAttribute('data-theme', next);
    try {
      localStorage.setItem('userEditorialTheme', next);
    } catch (e) {}
    updateThemeButtonLabel(next);
    showToastNotification(next === 'dark' ? 'Obsidian Dark Mode enabled' : 'Editorial Light Mode enabled');
  }

  function updateThemeButtonLabel(theme) {
    var btn = document.getElementById('btnThemeToggle');
    if (!btn) return;
    btn.innerHTML = (theme === 'dark') ? '<span>☀️</span><span>Light</span>' : '<span>🌙</span><span>Dark</span>';
  }

  // Relative Timestamp Live Formatter
  function formatRelativeTime(tsSeconds) {
    var now = Math.floor(Date.now() / 1000);
    var diff = now - parseInt(tsSeconds, 10);
    if (isNaN(diff)) return 'Date unavailable';
    if (diff < -300) return 'Date unavailable';
    if (diff < 90) return 'Just now';
    var mins = Math.floor(diff / 60);
    if (mins < 60) return mins + (mins === 1 ? ' min ago' : ' mins ago');
    var hrs = Math.floor(mins / 60);
    var remM = mins % 60;
    if (hrs < 24) {
      return remM > 0 ? (hrs + 'h ' + remM + 'm ago') : (hrs + (hrs === 1 ? ' hour ago' : ' hours ago'));
    }
    return hrs < 48 ? 'Yesterday' : Math.floor(hrs / 24) + ' days ago';
  }

  function updateRelativeTimestamps() {
    var tags = document.querySelectorAll('.source-tag[data-timestamp]');
    for (var i = 0; i < tags.length; i++) {
      var ts = tags[i].getAttribute('data-timestamp');
      if (ts && !isNaN(parseInt(ts, 10))) {
        tags[i].textContent = formatRelativeTime(ts);
      }
    }
  }

  // Refresh Top Breaking Wire Ticker
  function refreshLiveTicker() {
    var countBadge = document.getElementById('liveStoryCountBadge');
    var cards = document.querySelectorAll('#storiesFeedView .compact-card');
    if (countBadge) {
      countBadge.textContent = cards.length + ' Stories';
    }
  }

  function jumpToStoryCard(storyId) {
    showStoriesTab();
    var card = document.getElementById(storyId);
    if (!card) return;
    recordStoryInterest(storyId, 1);
    if (card.style.display === 'none') {
      var search = document.getElementById('liveSearchInput');
      if (search) search.value = '';
      currentSearchQuery = '';
      filterCategory('All');
      card.style.display = '';
    }
    card.scrollIntoView({ behavior: 'smooth', block: 'center' });
    if (!card.classList.contains('expanded')) {
      toggleStoryDetails(storyId);
    }
  }


  // Publisher orientation is separate from the article's political topic/lean.
  window.jumpToStoryCard = jumpToStoryCard;

  function getPublisherBias(source) {
    var s = String(source || '').toLowerCase();
    if (/fox news|daily wire|breitbart|new york post|washington examiner|newsmax|one america news|oann|the federalist/.test(s)) return 'right';
    if (/cnn|msnbc|huffpost|the guardian|npr|democracy now|mother jones|the intercept|vox|slate/.test(s)) return 'left';
    return 'center';
  }
  function getPublisherPriority(card, perspective) {
    var category = String(card.getAttribute('data-category') || '').toLowerCase();
    // Do not politicize sports or clearly non-news verticals.
    if (!/politics|border|national|world/.test(category)) return 1;
    var source = card.getAttribute('data-source') || '';
    var sourceLink = card.querySelector('.source-link-chip');
    if (!source && sourceLink) source = sourceLink.textContent || '';
    var bias = card.getAttribute('data-publisher-bias') || getPublisherBias(source);
    if (perspective === 'RIGHT') return bias === 'right' ? 3 : (bias === 'center' ? 2 : 1);
    if (perspective === 'LEFT') return bias === 'left' ? 3 : (bias === 'center' ? 2 : 1);
    return 1;
  }

  // Global Perspective Switcher
  function setGlobalPerspective(p) {
    if (!p || (p !== 'LEFT' && p !== 'CENTER' && p !== 'RIGHT')) p = 'CENTER';
    currentGlobalPerspective = p;
    try {
      localStorage.setItem('userLensPreference', p);
    } catch (e) {}

    var btnL = document.getElementById('btnGlobalLeft');
    var btnC = document.getElementById('btnGlobalCenter');
    var btnR = document.getElementById('btnGlobalRight');
    if (btnL) btnL.className = 'seg-btn lens-btn left ' + (p === 'LEFT' ? 'active' : '');
    if (btnC) btnC.className = 'seg-btn lens-btn center ' + (p === 'CENTER' ? 'active' : '');
    if (btnR) btnR.className = 'seg-btn lens-btn right ' + (p === 'RIGHT' ? 'active' : '');

    // 1. Switch perspective views on every card
    var allCards = document.querySelectorAll('.compact-card');
    for (var i = 0; i < allCards.length; i++) {
      if (allCards[i].id) {
        switchStoryPerspective(allCards[i].id, p);
      }
    }

    // 2. DYNAMIC FEED RE-ORDERING & FEATURED STORY POOL FILTERING
    var feed = document.getElementById('storiesFeedView');
    if (feed) {
      var cardsArr = Array.prototype.slice.call(feed.querySelectorAll('.compact-card'));
      cardsArr.sort(function(a, b) {
        var idxA = parseInt(a.getAttribute('data-original-index') || '0', 10);
        var idxB = parseInt(b.getAttribute('data-original-index') || '0', 10);
        if (p === 'RIGHT') {
          var scoreA = getPublisherPriority(a, p);
          var scoreB = getPublisherPriority(b, p);
          if (scoreA !== scoreB) return scoreB - scoreA;
        } else if (p === 'LEFT') {
          var scoreA = getPublisherPriority(a, p);
          var scoreB = getPublisherPriority(b, p);
          if (scoreA !== scoreB) return scoreB - scoreA;
        }
        // Balanced mode preserves the original chronology; same-tier stories do too.
        return idxA - idxB;
      });

      for (var k = 0; k < cardsArr.length; k++) {
        feed.appendChild(cardsArr[k]);
      }
    }

    [[btnL, 'LEFT'], [btnC, 'CENTER'], [btnR, 'RIGHT']].forEach(function (entry) {
      if (entry[0]) entry[0].setAttribute('aria-pressed', String(entry[1] === p));
    });
    var label = (p === 'RIGHT' ? 'Conservative Lens (Fox News & Right Media Prioritized)' : p === 'LEFT' ? 'Progressive Lens (Left Media & Labor Prioritized)' : 'Balanced Lens (Neutral Multi-Wire)');
    if (document.readyState === 'complete') showToastNotification('Switched to ' + label);
    if (document.body.classList.contains('daily-lens-mode')) renderDailyBriefing();
  }
  window.setGlobalPerspective = setGlobalPerspective;

  function switchStoryPerspective(storyId, p) {
    if (!storyId || !p) return;
    var views = ['RIGHT', 'CENTER', 'LEFT'];
    for (var i = 0; i < views.length; i++) {
      var el = document.getElementById(storyId + '-view-' + views[i]);
      if (el) {
        el.style.display = (views[i] === p) ? 'block' : 'none';
      }
    }

    var card = document.getElementById(storyId);
    if (card && card.querySelectorAll) {
      card.querySelectorAll('.card-toggle-btn').forEach(function (button) {
        var selected = button.dataset.perspective === p;
        button.classList.toggle('active', selected);
        button.setAttribute('aria-pressed', String(selected));
      });
    }
  }

  var _lastToggleMap = {};

  function syncCardExpandedContainer(card, storyId) {
    if (!card) return;
    var details = document.getElementById(storyId + '-details') || card.querySelector('.card-details');
    var factsPanel = document.getElementById(storyId + '-facts-panel') || card.querySelector('.facts-drawer-panel');
    var factsOpen = factsPanel && factsPanel.style.display !== 'none';
    if (factsOpen) {
      card.classList.add('expanded');
      if (details) details.style.display = 'block';
    } else {
      card.classList.remove('expanded');
      if (details) details.style.display = 'none';
    }
  }

  function toggleKeyFactsDrawer(storyId, evt, btnEl) {
    var e = evt || (typeof window !== 'undefined' ? window.event : null);
    if (e) {
      if (e.__handledDrawerToggle) return;
      e.__handledDrawerToggle = true;
      if (typeof e.stopPropagation === 'function') e.stopPropagation();
    }
    var card = (btnEl && btnEl.closest ? btnEl.closest('.compact-card') : null) || (storyId ? document.getElementById(storyId) : null);
    if (!card) return;
    var sId = storyId || card.id;
    var details = document.getElementById(sId + '-details') || card.querySelector('.card-details');
    var factsPanel = document.getElementById(sId + '-facts-panel') || card.querySelector('.facts-drawer-panel');
    var lensPanel = document.getElementById(sId + '-lens-panel') || card.querySelector('.lens-drawer-panel');
    var factsBtn = document.getElementById(sId + '-btn-facts-drawer') || card.querySelector('.btn-drawer-facts');
    var label = document.getElementById(sId + '-expand-label') || (factsBtn ? factsBtn.querySelector('.expand-label') : null);
    var chevron = document.getElementById(sId + '-chevron') || (factsBtn ? factsBtn.querySelector('.expand-chevron') : null);

    if (!factsPanel) {
      toggleStoryDetails(sId, e);
      return;
    }

    var isFactsOpen = card.classList.contains('expanded') && factsPanel.style.display !== 'none';
    var preview = card.querySelector('.fact-preview-strip');
    if (preview) preview.setAttribute('aria-expanded', String(!isFactsOpen));
    if (!isFactsOpen) {
      card.classList.add('expanded', 'facts-open');
      if (details) details.style.display = 'block';
      factsPanel.style.display = 'block';
      if (lensPanel && card.dataset.hasPerspectives === 'true') lensPanel.style.display = 'block';
      if (factsBtn) factsBtn.classList.add('active');
      if (label) label.textContent = 'Hide Key Facts';
      if (chevron) chevron.textContent = '▴';
    } else {
      card.classList.remove('expanded', 'facts-open');
      if (details) details.style.display = 'none';
      if (factsBtn) factsBtn.classList.remove('active');
      if (label) label.textContent = 'Key Facts';
      if (chevron) chevron.textContent = '▾';
    }
  }
  window.toggleKeyFactsDrawer = toggleKeyFactsDrawer;

  function toggleLensDrawer(storyId, evt, btnEl) {
    var e = evt || (typeof window !== 'undefined' ? window.event : null);
    if (e) {
      if (e.__handledDrawerToggle) return;
      e.__handledDrawerToggle = true;
      if (typeof e.stopPropagation === 'function') e.stopPropagation();
    }
    var card = (btnEl && btnEl.closest ? btnEl.closest('.compact-card') : null) || (storyId ? document.getElementById(storyId) : null);
    if (!card) return;
    var sId = storyId || card.id;
    var details = document.getElementById(sId + '-details') || card.querySelector('.card-details');
    var lensPanel = document.getElementById(sId + '-lens-panel') || card.querySelector('.lens-drawer-panel');
    var lensBtn = document.getElementById(sId + '-btn-lens-drawer') || card.querySelector('.btn-drawer-lens');
    var label = document.getElementById(sId + '-lens-expand-label') || (lensBtn ? lensBtn.querySelector('.expand-lens-label') : null);
    var chevron = document.getElementById(sId + '-lens-chevron') || (lensBtn ? lensBtn.querySelector('.expand-lens-chevron') : null);

    if (!lensPanel) {
      toggleStoryDetails(sId, e);
      return;
    }

    var isLensOpen = card.classList.contains('expanded') && lensPanel.style.display === 'block';
    if (!isLensOpen) {
      card.classList.add('expanded');
      if (details) details.style.display = 'block';
      lensPanel.style.display = 'block';
      if (lensBtn) lensBtn.classList.add('active');
      if (label) label.textContent = 'Hide Lens / Persona';
      if (chevron) chevron.textContent = '▴';
    } else {
      lensPanel.style.display = 'none';
      if (lensBtn) lensBtn.classList.remove('active');
      if (label) label.textContent = 'Lens / Persona';
      if (chevron) chevron.textContent = '▾';
      syncCardExpandedContainer(card, sId);
    }
  }
  window.toggleLensDrawer = toggleLensDrawer;

  function toggleStoryDetails(storyId, evt) {
    if (!storyId) return;
    var e = evt || (typeof window !== 'undefined' ? window.event : null);
    if (e) {
      if (e.__handledStoryToggle) return;
      e.__handledStoryToggle = true;
      if (typeof e.stopPropagation === 'function') e.stopPropagation();
    }

    var now = Date.now();
    if (_lastToggleMap[storyId] && (now - _lastToggleMap[storyId] < 150)) {
      return;
    }
    _lastToggleMap[storyId] = now;

    var card = document.getElementById(storyId);
    if (!card) return;

    var details = document.getElementById(storyId + '-details') || card.querySelector('.card-details');
    var factsPanel = document.getElementById(storyId + '-facts-panel') || card.querySelector('.facts-drawer-panel');
    var lensPanel = document.getElementById(storyId + '-lens-panel') || card.querySelector('.lens-drawer-panel');
    var factsBtn = document.getElementById(storyId + '-btn-facts-drawer') || card.querySelector('.btn-drawer-facts');
    var lensBtn = document.getElementById(storyId + '-btn-lens-drawer') || card.querySelector('.btn-drawer-lens');
    var label = document.getElementById(storyId + '-expand-label') || card.querySelector('.expand-label');
    var chevron = document.getElementById(storyId + '-chevron') || card.querySelector('.expand-chevron');
    var lensLabel = document.getElementById(storyId + '-lens-expand-label') || card.querySelector('.expand-lens-label');
    var lensChev = document.getElementById(storyId + '-lens-chevron') || card.querySelector('.expand-lens-chevron');

    var isOpen = card.classList.contains('expanded');
    var preview = card.querySelector('.fact-preview-strip');
    if (preview) preview.setAttribute('aria-expanded', String(!isOpen));
    if (!isOpen) {
      card.classList.add('expanded');
      if (details) details.style.display = 'block';
      if (factsPanel) factsPanel.style.display = 'block';
      if (lensPanel && card.dataset.hasPerspectives === 'true') lensPanel.style.display = 'block';
      if (factsBtn) factsBtn.classList.add('active');
      if (lensBtn) lensBtn.classList.add('active');
      if (label) label.textContent = 'Hide Key Facts';
      if (chevron) chevron.textContent = '▴';
      if (lensLabel) lensLabel.textContent = 'Hide Lens / Persona';
      if (lensChev) lensChev.textContent = '▴';
    } else {
      card.classList.remove('expanded');
      if (details) details.style.display = 'none';
      if (factsPanel) factsPanel.style.display = 'none';
      if (lensPanel) lensPanel.style.display = 'none';
      if (factsBtn) factsBtn.classList.remove('active');
      if (lensBtn) lensBtn.classList.remove('active');
      if (label) label.textContent = 'Key Facts';
      if (chevron) chevron.textContent = '▾';
      if (lensLabel) lensLabel.textContent = 'Lens / Persona';
      if (lensChev) lensChev.textContent = '▾';
    }
  }

  function toggleFactExpansion(storyId, event) {
    var e = event || (typeof window !== 'undefined' ? window.event : null);
    if (e) {
      if (typeof e.stopPropagation === 'function') e.stopPropagation();
      if (typeof e.preventDefault === 'function') e.preventDefault();
    }
    if (!storyId) return;
    var dossier = document.getElementById(storyId + '-facts-dossier');
    var btn = document.getElementById(storyId + '-btn-facts-toggle');
    var btnText = document.getElementById(storyId + '-fact-btn-text');
    var btnChevron = document.getElementById(storyId + '-fact-btn-chevron');

    if (!dossier) return;
    var isHidden = (dossier.style.display === 'none' || dossier.style.display === '');
    if (isHidden) {
      dossier.style.display = 'block';
      if (btn) btn.classList.add('active');
      if (btnText) btnText.textContent = 'Hide Evidence';
      if (btnChevron) btnChevron.textContent = '▴';
    } else {
      dossier.style.display = 'none';
      if (btn) btn.classList.remove('active');
      if (btnText) btnText.textContent = '🔍 Deep Dive & Evidence';
      if (btnChevron) btnChevron.textContent = '▾';
    }
  }

  // Category & Live Search Filter
  function applyFilters() {
    var key = (currentFilterCategory || 'All').toLowerCase().trim();
    var q = (currentSearchQuery || '').toLowerCase().trim();
    var articles = document.querySelectorAll('#storiesFeedView .compact-card');
    var visibleCount = 0;

    var isMainFeed = (key === 'all' && !q);
    if (isMainFeed) {
      document.body.classList.remove('filtered-category');
      document.body.classList.remove('searching-mode');
    } else {
      if (key !== 'all') document.body.classList.add('filtered-category');
      if (q) document.body.classList.add('searching-mode');
    }

    // Toggle local subnav visibility based on active category
    var localSubnav = document.getElementById('localSubnavBar');
    if (localSubnav) {
      localSubnav.style.display = (key === 'local') ? 'block' : 'none';
    }

    // Toggle blind stance challenge visibility: STRICTLY ONLY on main page (All Stories, no search query)
    var blindSection = document.getElementById('blindStanceSection');
    if (blindSection) {
      blindSection.style.display = isMainFeed ? 'block' : 'none';
    }

    var curMetro = (currentLocalMetro || 'Tampa Bay, FL').toLowerCase();
    var cityCore = curMetro.split(',')[0].toLowerCase().trim();

    for (var j = 0; j < articles.length; j++) {
      var card = articles[j];
      var cat = (card.getAttribute('data-category') || '').toLowerCase().trim();
      var masterCat = (card.getAttribute('data-master-category') || '').toLowerCase().trim();
      var cardMetro = (card.getAttribute('data-metro') || '').toLowerCase();
      var cardSubcat = (card.getAttribute('data-subcategory') || '').toLowerCase();
      var match = false;

      if (key === 'following') {
        match = Boolean(_userFollowedStories[card.id]) || isRelatedToFollowed(card);
      } else if (key === 'all') {
        var cardCat = cat + ' ' + masterCat;
        // In All Stories: show all national news + local stories matching user's metro
        if (cardCat.indexOf('local') !== -1) {
          match = (!cardMetro || cardMetro.indexOf(cityCore) !== -1 || curMetro.indexOf(cardMetro) !== -1);
        } else {
          match = true;
        }
      } else if (key === 'local') {
        // Must be Local News
        if (cat.indexOf('local') !== -1 || masterCat.indexOf('local') !== -1) {
          // Check subcategory filter if active
          if (currentLocalSubcategory && currentLocalSubcategory !== 'all') {
            match = (cardSubcat === currentLocalSubcategory);
          } else {
            match = true;
          }
          // If city matches or regional fallback
          if (match && curMetro) {
            match = (!cardMetro || cardMetro.indexOf(cityCore) !== -1 || curMetro.indexOf(cardMetro) !== -1);
          }
        }
      } else if (key === 'breaking') {
        match = (card.classList.contains('featured-lead-card') || cat.indexOf('break') !== -1 || cat.indexOf('politic') !== -1);
      } else if (key === 'politics') {
        match = (cat.indexOf('politic') !== -1 || masterCat.indexOf('politic') !== -1);
      } else if (key === 'sports') {
        match = (cat.indexOf('sport') !== -1 || masterCat.indexOf('sport') !== -1);
      } else if (key === 'business') {
        match = (cat.indexOf('business') !== -1 || cat.indexOf('econom') !== -1 || cat.indexOf('inflat') !== -1 || cat.indexOf('stock') !== -1 || cat.indexOf('market') !== -1);
      } else if (key === 'energy') {
        match = (cat.indexOf('energy') !== -1 || cat.indexOf('weather') !== -1 || cat.indexOf('power') !== -1 || cat.indexOf('grid') !== -1);
      } else if (key === 'health') {
        match = (cat.indexOf('health') !== -1 || cat.indexOf('drug') !== -1 || cat.indexOf('medic') !== -1);
      } else if (key === 'tech') {
        match = (cat.indexOf('tech') !== -1 || cat.indexOf('science') !== -1 || cat.indexOf('ai') !== -1 || cat.indexOf('space') !== -1);
      } else if (key === 'world') {
        match = (cat.indexOf('world') !== -1 || cat.indexOf('geopolitic') !== -1 || masterCat.indexOf('world') !== -1);
      } else if (key === 'entertainment') {
        match = (cat.indexOf('entertain') !== -1 || cat.indexOf('movie') !== -1 || cat.indexOf('film') !== -1 || masterCat.indexOf('entertain') !== -1);
      } else if (key === 'border') {
        match = (cat.indexOf('border') !== -1 || cat.indexOf('secur') !== -1);
      } else if (key === 'crime') {
        match = (cat.indexOf('crime') !== -1 || cat.indexOf('safety') !== -1 || cat.indexOf('law') !== -1 || cat.indexOf('court') !== -1);
      } else {
        match = (cat.indexOf(key) !== -1 || masterCat.indexOf(key) !== -1);
      }

      if (match && q) {
        var textContent = (card.textContent || '').toLowerCase();
        match = (textContent.indexOf(q) !== -1);
      }

      card.style.display = match ? '' : 'none';
      if (match) visibleCount++;
    }

    var empty = document.getElementById('feedEmptyState');
    if (empty) {
      empty.hidden = visibleCount > 0;
      empty.textContent = key === 'following' ?
        'Follow a story to see it and related coverage from future editions here.' :
        'No published stories match these filters.';
    }

    var badge = document.getElementById('liveStoryCountBadge');
    if (badge) {
      if (key === 'local') {
        badge.textContent = visibleCount + ' Local Stories';
      } else if (key === 'all' && !q) {
        badge.textContent = visibleCount + ' Stories';
      } else {
        badge.textContent = visibleCount + ' Stories Matching';
      }
    }
  }

  
  // Local News Location & Metro Controller (Defaults to user's home metro: Tampa Bay, FL)
  var currentLocalMetro = 'Tampa Bay, FL';
  try {
    var savedMetro = localStorage.getItem('userLocalMetro');
    if (savedMetro) {
      currentLocalMetro = savedMetro;
    }
  } catch (e) {}

  var currentLocalSubcategory = 'all';

  function filterLocalSubcategory(subcatKey, btnEl) {
    currentLocalSubcategory = subcatKey || 'all';
    var pills = document.querySelectorAll('.subcat-pill');
    for (var i = 0; i < pills.length; i++) {
      pills[i].classList.remove('active');
    }
    if (btnEl) {
      btnEl.classList.add('active');
    }
    applyFilters();
  }
  window.filterLocalSubcategory = filterLocalSubcategory;

  function toggleCityDropdown() {
    var dd = document.getElementById('citySelectorDropdown');
    if (!dd) return;
    dd.style.display = (dd.style.display === 'none' || !dd.style.display) ? 'block' : 'none';
  }
  window.toggleCityDropdown = toggleCityDropdown;

  function selectMetro(m) {
    applyMetro(m, 'User Selected');
    showToastNotification('Local metro set to ' + m);
  }
  window.selectMetro = selectMetro;

  function applyCustomCity() {
    var input = document.getElementById('customCityInput');
    if (!input || !input.value.trim()) return;
    var custom = input.value.trim();
    applyMetro(custom, 'Custom Location');
    showToastNotification('Metro set to ' + custom);
    input.value = '';
  }
  window.applyCustomCity = applyCustomCity;

  function applyMetro(metroName, statusLabel) {
    if (!metroName) metroName = 'Tampa Bay, FL';
    currentLocalMetro = metroName;
    try {
      localStorage.setItem('userLocalMetro', metroName);
    } catch (e) {}

    var cityDisp = document.getElementById('localCityDisplay');
    if (cityDisp) cityDisp.textContent = metroName;
    var statusPill = document.getElementById('localStatusPill');
    if (statusPill && statusLabel) statusPill.textContent = statusLabel;

    var presetBtns = document.querySelectorAll('.city-preset-btn');
    for (var i = 0; i < presetBtns.length; i++) {
      if ((presetBtns[i].getAttribute('data-metro') || '').toLowerCase() === metroName.toLowerCase()) {
        presetBtns[i].classList.add('active');
      } else {
        presetBtns[i].classList.remove('active');
      }
    }

    var dd = document.getElementById('citySelectorDropdown');
    if (dd) dd.style.display = 'none';

    applyFilters();
  }
  window.applyMetro = applyMetro;

  function detectUserLocation() {
    var btn = document.getElementById('btnDetectLocation');
    if (btn) btn.innerHTML = '<span>⏳ Detecting...</span>';

    if (!navigator.geolocation) {
      applyMetro('Tampa Bay, FL', 'Default Metro');
      showToastNotification('Location set to Tampa Bay, FL');
      if (btn) btn.innerHTML = '<span>🎯 Auto-Detect City</span>';
      return;
    }

    navigator.geolocation.getCurrentPosition(
      function(position) {
        var lat = position.coords.latitude;
        var lon = position.coords.longitude;
        var detected = 'Tampa Bay, FL';

        if (lat >= 27.5 && lat <= 28.5 && lon >= -83.0 && lon <= -82.0) {
          detected = 'Tampa Bay, FL';
        } else if (lat >= 28.2 && lat <= 28.9 && lon >= -81.7 && lon <= -81.0) {
          detected = 'Orlando & Central FL';
        } else if (lat >= 25.5 && lat <= 26.5 && lon >= -80.5 && lon <= -80.0) {
          detected = 'Miami & South FL';
        } else if (lat >= 33.4 && lat <= 34.2 && lon >= -84.7 && lon <= -84.0) {
          detected = 'Atlanta Metro, GA';
        } else if (lat >= 40.5 && lat <= 41.0 && lon >= -74.3 && lon <= -73.7) {
          detected = 'New York City Metro';
        } else if (lat >= 38.7 && lat <= 39.2 && lon >= -77.3 && lon <= -76.8) {
          detected = 'Washington D.C. Metro';
        } else if (lat >= 41.6 && lat <= 42.1 && lon >= -88.0 && lon <= -87.4) {
          detected = 'Chicago & Midwest';
        } else if (lat >= 33.7 && lat <= 34.4 && lon >= -118.7 && lon <= -118.0) {
          detected = 'Los Angeles & SoCal';
        } else if (lat >= 32.5 && lat <= 33.1 && lon >= -97.2 && lon <= -96.5) {
          detected = 'Dallas-Fort Worth, TX';
        } else {
          detected = 'Tampa Bay, FL';
        }

        applyMetro(detected, '🎯 GPS Detected');
        showToastNotification('Location detected: ' + detected);
        if (btn) btn.innerHTML = '<span>🎯 Auto-Detect City</span>';
      },
      function(err) {
        applyMetro(currentLocalMetro || 'Tampa Bay, FL', 'Default Metro');
        showToastNotification('Location set to ' + (currentLocalMetro || 'Tampa Bay, FL'));
        if (btn) btn.innerHTML = '<span>🎯 Auto-Detect City</span>';
      },
      { timeout: 6000 }
    );
  }
  window.detectUserLocation = detectUserLocation;

  function filterCategory(btnOrKey, keyOrBtn) {
    var btn = null;
    var catKey = 'All';
    if (typeof btnOrKey === 'string') {
      catKey = btnOrKey;
      btn = (keyOrBtn && typeof keyOrBtn === 'object') ? keyOrBtn : null;
    } else {
      btn = btnOrKey;
      catKey = (typeof keyOrBtn === 'string') ? keyOrBtn : 'All';
    }

    currentFilterCategory = catKey || 'All';
    var isAll = (currentFilterCategory.toLowerCase().trim() === 'all');

    if (isAll) {
      document.body.classList.remove('filtered-category');
    } else {
      document.body.classList.add('filtered-category');
    }

    var blindSection = document.getElementById('blindStanceSection');
    if (blindSection) {
      blindSection.style.display = isAll ? 'block' : 'none';
    }

    var pills = document.querySelectorAll('.cat-pill');
    for (var i = 0; i < pills.length; i++) {
      pills[i].classList.remove('active');
    }
    if (btn && btn.classList) {
      btn.classList.add('active');
    } else {
      for (var k = 0; k < pills.length; k++) {
        if ((pills[k].getAttribute('data-category') || '').toLowerCase() === currentFilterCategory.toLowerCase()) {
          pills[k].classList.add('active');
          break;
        }
      }
    }
    applyFilters();
  }

  function handleLiveSearch(inputEl) {
    currentSearchQuery = inputEl ? inputEl.value : '';
    if (currentSearchQuery.trim()) {
      document.body.classList.add('searching-mode');
    } else {
      document.body.classList.remove('searching-mode');
    }
    applyFilters();
  }

  function togglePersonalizePanel() {
    var panel = document.getElementById('personalizePanel');
    if (!panel) return;
    panel.classList.toggle('open');
  }

  function applyQuickFocus(focusPreset) {
    var btns = document.querySelectorAll('.focus-preset-btn');
    for (var i = 0; i < btns.length; i++) {
      if (btns[i].getAttribute('data-focus') === focusPreset) {
        btns[i].classList.add('active');
      } else {
        btns[i].classList.remove('active');
      }
    }
    try {
      localStorage.setItem('userFeedFocus', focusPreset);
    } catch (e) {}

    var feed = document.getElementById('storiesFeedView');
    if (feed) {
      var cards = Array.prototype.slice.call(feed.querySelectorAll('.compact-card'));
      cards.sort(function(a, b) {
        return getCardRank(b, focusPreset) - getCardRank(a, focusPreset);
      });
      for (var k = 0; k < cards.length; k++) {
        cards[k].classList.remove('featured-lead-card');
        if (k === 0) cards[k].classList.add('featured-lead-card');
        feed.appendChild(cards[k]);
      }
    }
    var label = (focusPreset === 'sports') ? 'Sports' : (focusPreset === 'politics') ? 'Politics' : (focusPreset === 'business') ? 'Business' : (focusPreset === 'tech') ? 'Tech' : 'All News';
    showToastNotification('Prioritized ' + label + ' first in feed');
  }

  function getCardRank(card, focusPreset) {
    if (!focusPreset || focusPreset === 'all') return 0;
    var cat = (card.getAttribute('data-category') || '').toLowerCase();
    var master = (card.getAttribute('data-master-category') || '').toLowerCase();
    if (focusPreset === 'sports' && (cat.indexOf('sport') !== -1 || master.indexOf('sport') !== -1)) return 10;
    if (focusPreset === 'politics' && (cat.indexOf('politic') !== -1 || master.indexOf('politic') !== -1)) return 10;
    if (focusPreset === 'business' && (cat.indexOf('business') !== -1 || cat.indexOf('econom') !== -1)) return 10;
    if (focusPreset === 'tech' && (cat.indexOf('tech') !== -1 || cat.indexOf('science') !== -1)) return 10;
    return 0;
  }

  function copyPointsFromCard(btn) {
    var panel = btn.closest('.talking-points-panel') || btn.closest('.voted-talking-points-box');
    if (!panel) return;
    var rows = panel.querySelectorAll('.quote-row');
    var list = [];
    for (var i = 0; i < rows.length; i++) {
      list.push('• ' + rows[i].textContent.replace(/^"|"$/g, '').trim());
    }
    var text = list.join('\n');
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(text).then(function() {
        showToastNotification('Talking points copied');
      }).catch(function() {
        fallbackCopy(text);
      });
    } else {
      fallbackCopy(text);
    }
  }

  function fallbackCopy(text) {
    var ta = document.createElement('textarea');
    ta.value = text;
    ta.style.position = 'fixed';
    ta.style.opacity = '0';
    document.body.appendChild(ta);
    ta.select();
    try {
      document.execCommand('copy');
      showToastNotification('Talking points copied');
    } catch (err) {}
    document.body.removeChild(ta);
  }

  function toggleSaveCard(btn) {
    if (!btn) return;
    var card = btn.closest('.compact-card');
    if (card) toggleFollowStory(card.id);
  }

  function showToastNotification(msg) {
    var box = document.getElementById('toastBox');
    if (!box) return;
    box.textContent = '✓ ' + msg;
    box.classList.add('show');
    clearTimeout(window._toastTimer);
    window._toastTimer = setTimeout(function() {
      box.classList.remove('show');
    }, 2600);
  }

  function showStoriesTab() {
    var feed = document.getElementById('storiesFeedView');
    var comm = document.getElementById('communityView');
    var dailyLens = document.getElementById('dailyLensView');
    var tabS = document.getElementById('navStories');
    var tabD = document.getElementById('navDailyLens');
    var tabL = document.getElementById('navLounge');
    if (feed) feed.style.display = 'grid';
    applyFilters();
    if (comm) comm.style.display = 'none';
    if (dailyLens) dailyLens.style.display = 'none';
    if (tabS) tabS.className = 'view-tab active';
    if (tabD) tabD.className = 'view-tab';
    if (tabL) tabL.className = 'view-tab';

    document.body.classList.remove('daily-lens-mode');

    // Restore blind stance challenge only if on main All Stories view without search
    var blindSection = document.getElementById('blindStanceSection');
    var curCat = (currentFilterCategory || 'All').toLowerCase().trim();
    var curQ = (currentSearchQuery || '').toLowerCase().trim();
    if (blindSection) {
      blindSection.style.display = (curCat === 'all' && !curQ) ? 'block' : 'none';
    }
  }

  function showLoungeTab() {
    var feed = document.getElementById('storiesFeedView');
    var comm = document.getElementById('communityView');
    var dailyLens = document.getElementById('dailyLensView');
    var tabS = document.getElementById('navStories');
    var tabD = document.getElementById('navDailyLens');
    var tabL = document.getElementById('navLounge');
    if (feed) feed.style.display = 'none';
    var empty = document.getElementById('feedEmptyState');
    if (empty) empty.hidden = true;
    if (comm) comm.style.display = 'flex';
    if (window.ynlRenderDebates) window.ynlRenderDebates();
    if (dailyLens) dailyLens.style.display = 'none';
    if (tabS) tabS.className = 'view-tab';
    if (tabD) tabD.className = 'view-tab';
    if (tabL) tabL.className = 'view-tab active';

    document.body.classList.remove('daily-lens-mode');

    // Never show the blind stance challenge in Community Lounge
    var blindSection = document.getElementById('blindStanceSection');
    if (blindSection) {
      blindSection.style.display = 'none';
    }
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }

  // Global Window Event Handlers Bindings
  window.toggleStoryDetails = toggleStoryDetails;
  window.toggleFactExpansion = toggleFactExpansion;
  window.switchStoryPerspective = switchStoryPerspective;
  window.setGlobalPerspective = setGlobalPerspective;
  window.filterCategory = filterCategory;
  window.filterLocalSubcategory = filterLocalSubcategory;
  window.toggleCityDropdown = toggleCityDropdown;
  window.selectMetro = selectMetro;
  window.applyCustomCity = applyCustomCity;
  window.detectUserLocation = detectUserLocation;
  window.applyMetro = applyMetro;
  window.toggleThemeMode = toggleThemeMode;
  window.handleLiveSearch = handleLiveSearch;
  window.copyPointsFromCard = copyPointsFromCard;
  window.toggleSaveCard = toggleSaveCard;
  window.showStoriesTab = showStoriesTab;
  window.showLoungeTab = showLoungeTab;

  
  // =========================================================================
  // YOUR DAILY LENS & STORY EVOLUTION TRACKER ENGINE (v12.0)
  // =========================================================================
  var _userFollowedStories = {};

  function readTopics(card) {
    try { return JSON.parse(card.dataset.topics || '[]'); } catch (_) { return []; }
  }

  function isRelatedToFollowed(card) {
    var topics = readTopics(card);
    return topics.length > 0 && Object.values(_userFollowedStories).some(function (item) {
      return item && item.category === card.dataset.category && Array.isArray(item.topics) &&
        item.topics.some(function (topic) { return topics.includes(topic); });
    });
  }

  function updateFollowButtonsInDOM() {
    var followedIds = Object.keys(_userFollowedStories);
    var countBadge = document.getElementById('followingCountBadge');
    if (countBadge) {
      countBadge.textContent = String(followedIds.length);
    }

    // Update all follow buttons across cards
    var btns = document.querySelectorAll('.btn-follow-card, .btn-follow-story');
    for (var i = 0; i < btns.length; i++) {
      var btn = btns[i];
      var sId = btn.id.replace('follow-btn-', '').replace('daily-follow-', '');
      var isFollowing = Boolean(_userFollowedStories[sId]);
      if (isFollowing) {
        btn.classList.add('following');
        var label = btn.querySelector('.follow-label') || btn.querySelector('.follow-text');
        if (label) label.textContent = 'Following';
        var star = btn.querySelector('.follow-star') || btn.querySelector('.star-icon');
        if (star) star.textContent = '★';
      } else {
        btn.classList.remove('following');
        var label = btn.querySelector('.follow-label') || btn.querySelector('.follow-text');
        if (label) label.textContent = 'Follow';
        var star = btn.querySelector('.follow-star') || btn.querySelector('.star-icon');
        if (star) star.textContent = '⭐';
      }
    }
  }
  window.updateFollowButtonsInDOM = updateFollowButtonsInDOM;

  function toggleFollowStory(storyId, btnEl) {
    if (!storyId) return;
    var currentlyFollowing = Boolean(_userFollowedStories[storyId]);
    if (currentlyFollowing) {
      delete _userFollowedStories[storyId];
    } else {
      var card = document.getElementById(storyId);
      _userFollowedStories[storyId] = card ? {category: card.dataset.category, topics: readTopics(card)} : true;
    }

    try {
      localStorage.setItem('userFollowedStories', JSON.stringify(_userFollowedStories));
    } catch (e) {}

    updateFollowButtonsInDOM();

    var titleEl = document.querySelector('#' + storyId + ' .story-title') || document.querySelector('#daily-card-' + storyId + ' .daily-card-title');
    var sTitle = titleEl ? titleEl.textContent.trim() : storyId;

    if (_userFollowedStories[storyId]) {
      showToastNotification('⭐ Following story! You\'ll see updates & evolution in Following');
    } else {
      showToastNotification('Unfollowed story: ' + sTitle.substring(0, 40) + '...');
    }

    if (currentFilterCategory && currentFilterCategory.toLowerCase() === 'following') {
      applyFilters();
    }
  }
  window.toggleFollowStory = toggleFollowStory;

  function toggleEvolutionTimeline(storyId, ev) {
    if (ev && ev.stopPropagation) ev.stopPropagation();
    var tl = document.getElementById(storyId + '-evolution-timeline');
    var btnText = document.getElementById(storyId + '-evolution-btn-text');
    var chev = document.getElementById(storyId + '-evolution-chevron');
    if (!tl) return;

    var isHidden = (tl.style.display === 'none' || !tl.style.display);
    if (isHidden) {
      tl.style.display = 'block';
      if (btnText) btnText.textContent = 'Hide Timeline';
      if (chev) chev.textContent = '▴';
    } else {
      tl.style.display = 'none';
      if (btnText) btnText.textContent = 'View Timeline';
      if (chev) chev.textContent = '▾';
    }
  }
  window.toggleEvolutionTimeline = toggleEvolutionTimeline;

  function showDailyLensTab() {
    var feed = document.getElementById('storiesFeedView');
    var comm = document.getElementById('communityView');
    var dailyLens = document.getElementById('dailyLensView');
    var tabS = document.getElementById('navStories');
    var tabD = document.getElementById('navDailyLens');
    var tabL = document.getElementById('navLounge');
    var blindSec = document.getElementById('blindStanceSection');

    if (feed) feed.style.display = 'none';
    var empty = document.getElementById('feedEmptyState');
    if (empty) empty.hidden = true;
    if (comm) comm.style.display = 'none';
    if (dailyLens) dailyLens.style.display = 'block';
    if (blindSec) blindSec.style.display = 'none';

    if (tabS) tabS.className = 'view-tab';
    if (tabD) tabD.className = 'view-tab active';
    if (tabL) tabL.className = 'view-tab';

    document.body.classList.add('daily-lens-mode');
    renderDailyBriefing();
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }
  window.showDailyLensTab = showDailyLensTab;



  // =========================================================================
  // PULL-DOWN ON TOP BANNER (.app-header) TO REFRESH FROM ANYWHERE ON PAGE
  // =========================================================================
  var _isBannerRefreshing = false;

  function checkForEdition() {
    return fetch('data/stories.json', { cache: 'no-cache' }).then(function (response) {
      if (!response.ok) throw new Error('Edition unavailable');
      return response.json();
    }).then(function (records) {
      if (!Array.isArray(records) || !records.length) throw new Error('Invalid edition');
      var next = records[0].edition;
      if (!/^[0-9a-f]{16}$/.test(next || '')) throw new Error('Invalid edition version');
      return next !== document.getElementById('storiesFeedView').dataset.edition ? next : '';
    });
  }

  function triggerBannerRefresh() {
    if (_isBannerRefreshing) return;
    _isBannerRefreshing = true;

    var bar = document.getElementById('bannerPullRefreshBar');
    var icon = document.getElementById('bannerPullRefreshIcon');
    var txt = document.getElementById('bannerPullRefreshText');
    if (bar) {
      bar.classList.remove('pulling', 'ready-to-refresh');
      bar.classList.add('refreshing');
      bar.style.height = '42px';
      bar.style.opacity = '1';
    }
    if (icon) icon.textContent = '🔄';
    if (txt) txt.textContent = 'Refreshing live stories...';

    returnToLatestStories();
    checkForEdition().then(function (updated) {
      if (updated) {
        var url = new URL(window.location.href);
        url.hash = '';
        url.searchParams.set('edition', updated);
        try { sessionStorage.setItem('ynlRefreshToTop', '1'); } catch (_) {}
        window.location.replace(url);
      }
      else {
        if (window.ynlRefreshVisiblePolls) window.ynlRefreshVisiblePolls();
        showToastNotification('You have the latest edition.');
      }
    }).catch(function () {
      showToastNotification('Could not check for updates. Please try again.');
    }).finally(function () {
      setTimeout(function() {
        if (bar) {
          bar.classList.remove('refreshing', 'pulling', 'ready-to-refresh');
          bar.style.height = '0px';
          bar.style.opacity = '0';
        }
        _isBannerRefreshing = false;
      }, 650);
    });
  }
  window.triggerBannerRefresh = triggerBannerRefresh;

  function bindBannerPullToRefresh() {
    var headerEl = document.querySelector('.app-header');
    if (!headerEl || headerEl.__pullBound) return;
    headerEl.__pullBound = true;

    var startY = 0;
    var startX = 0;
    var pulling = false;
    var currentDy = 0;

    headerEl.addEventListener('touchstart', function(ev) {
      if (_isBannerRefreshing) return;
      if (ev.target && ev.target.tagName && ev.target.tagName.toLowerCase() === 'input') return;
      if (!ev.touches || ev.touches.length !== 1) return;
      startY = ev.touches[0].clientY;
      startX = ev.touches[0].clientX;
      pulling = true;
      currentDy = 0;
    }, { passive: true });

    headerEl.addEventListener('touchmove', function(ev) {
      if (!pulling || _isBannerRefreshing || !ev.touches || ev.touches.length !== 1) return;
      var dy = ev.touches[0].clientY - startY;
      var dx = Math.abs(ev.touches[0].clientX - startX);
      if (dy > 10 && dy > dx) {
        if (ev.cancelable) ev.preventDefault();
        currentDy = dy;
        var bar = document.getElementById('bannerPullRefreshBar');
        var icon = document.getElementById('bannerPullRefreshIcon');
        var txt = document.getElementById('bannerPullRefreshText');
        if (bar) {
          bar.classList.add('pulling');
          var h = Math.min(Math.round(dy * 0.6), 52);
          bar.style.height = h + 'px';
          bar.style.opacity = String(Math.min(dy / 45, 1));
          if (dy >= 48) {
            bar.classList.add('ready-to-refresh');
            if (icon) icon.textContent = '⚡';
            if (txt) txt.textContent = 'Release to refresh stories!';
          } else {
            bar.classList.remove('ready-to-refresh');
            if (icon) icon.textContent = '↓';
            if (txt) txt.textContent = 'Pull down on banner to refresh stories';
          }
        }
      }
    }, { passive: false });

    function finishPull() {
      if (!pulling) return;
      pulling = false;
      if (currentDy >= 48) {
        currentDy = 0;
        triggerBannerRefresh();
      } else {
        currentDy = 0;
        var bar = document.getElementById('bannerPullRefreshBar');
        if (bar && !_isBannerRefreshing) {
          bar.classList.remove('pulling', 'ready-to-refresh');
          bar.style.height = '0px';
          bar.style.opacity = '0';
        }
      }
    }

    headerEl.addEventListener('touchend', finishPull, { passive: true });
    headerEl.addEventListener('touchcancel', finishPull, { passive: true });
  }

  function returnToLatestStories() {
    var input = document.getElementById('liveSearchInput');
    if (input) input.value = '';
    currentSearchQuery = '';
    showStoriesTab();
    filterCategory('All');
    window.scrollTo({top: 0, behavior: 'instant'});
  }

  function bindCompactHeader() {
    var header = document.getElementById('topAppBanner');
    if (!header) return;
    var last = Math.max(0, window.scrollY);
    window.addEventListener('scroll', function () {
      var y = Math.max(0, window.scrollY);
      if (y < 20 || y < last - 4) header.classList.remove('ynl-header-hidden');
      else if (y > header.offsetHeight && y > last + 4 && !header.contains(document.activeElement)
               && !_isBannerRefreshing) header.classList.add('ynl-header-hidden');
      if (Math.abs(y - last) > 4 || y === 0) last = y;
    }, {passive: true});
    header.addEventListener('focusin', function () { header.classList.remove('ynl-header-hidden'); });
    var controls = header.querySelector('.header-controls');
    if (controls) {
      var help = document.createElement('details');
      help.className = 'ynl-lens-help';
      help.innerHTML = '<summary>How lenses work</summary><p>Left and Right highlight different political arguments. Balanced focuses on what is known and where accounts differ. Sports and other stories use topic-specific angles. Facts stay the same across lenses.</p>';
      controls.append(help);
    }
  }

  var readerInterests = {};
  try { readerInterests = JSON.parse(localStorage.getItem('ynlReaderInterests')) || {}; } catch (_) {}

  function recordStoryInterest(storyId, weight) {
    var card = document.getElementById(storyId);
    if (!card || !card.dataset.category) return;
    for (var key of [card.dataset.category, ...readTopics(card)]) {
      readerInterests[key] = Math.min(12, (Number(readerInterests[key]) || 0) + weight);
    }
    readerInterests = Object.fromEntries(Object.entries(readerInterests).slice(-100));
    try { localStorage.setItem('ynlReaderInterests', JSON.stringify(readerInterests)); } catch (_) {}
  }
  window.ynlRecordStoryInterest = recordStoryInterest;

  function renderDailyBriefing() {
    var grid = document.getElementById('dailyLensStoriesGrid');
    if (!grid) return;
    var cards = [...document.querySelectorAll('#storiesFeedView .compact-card')];
    var label = {LEFT: 'Left', CENTER: 'Balanced', RIGHT: 'Right'}[currentGlobalPerspective];
    var intro = document.querySelector('.daily-lens-subtitle');
    if (intro) intro.textContent = label + ' briefing · Ranked using your lens, followed stories, and reading and voting activity on this device.';
    function score(card) {
      var bias = card.dataset.publisherBias || 'center';
      var preferred = currentGlobalPerspective.toLowerCase();
      var interest = [card.dataset.category, ...readTopics(card)].reduce(function (total, key) {
        return total + (Number(readerInterests[key]) || 0);
      }, 0);
      var follow = _userFollowedStories[card.id] ? 12 : isRelatedToFollowed(card) ? 7 : 0;
      return (bias === preferred ? 6 : 0) + follow + Math.min(10, interest)
        - Number(card.dataset.originalIndex || 0) / Math.max(cards.length, 1) * 4;
    }
    cards.sort(function (a, b) { return score(b) - score(a); });
    grid.replaceChildren();
    for (var card of cards.slice(0, 6)) {
      var item = document.createElement('article');
      item.className = 'daily-lens-story-card';
      var title = document.createElement('button');
      title.type = 'button';
      title.className = 'daily-card-title ynl-story-link';
      title.textContent = card.querySelector('.story-title').textContent.trim();
      title.addEventListener('click', jumpToStoryCard.bind(null, card.id));
      var meta = document.createElement('p');
      meta.textContent = card.dataset.category + ' · ' + card.dataset.source;
      var fact = document.createElement('p');
      fact.textContent = card.querySelector('.fact-preview-text')?.textContent || '';
      item.append(meta, title, fact);
      grid.append(item);
    }
  }

  function initOnReady() {
    try {
      var savedTheme = localStorage.getItem('userEditorialTheme') || 'dark';
      document.documentElement.setAttribute('data-theme', savedTheme);
      updateThemeButtonLabel(savedTheme);
    } catch (e) {
      document.documentElement.setAttribute('data-theme', 'dark');
    }

    setGlobalPerspective(currentGlobalPerspective);
    try {
      var savedFocus = localStorage.getItem('userFeedFocus');
      if (savedFocus && savedFocus !== 'all') {
        applyQuickFocus(savedFocus);
      }
    } catch (e) {}

    var editionDate = document.getElementById('currentEditionDate');
    if (editionDate) editionDate.textContent = new Intl.DateTimeFormat('en-US', {
      dateStyle: 'full', timeZone: 'America/New_York'
    }).format(new Date());
    updateRelativeTimestamps();
    refreshLiveTicker();
    // Hydrate followed stories from localStorage
    try {
      var savedFollowed = localStorage.getItem('userFollowedStories');
      if (savedFollowed) {
        _userFollowedStories = JSON.parse(savedFollowed) || {};
      }
      updateFollowButtonsInDOM();
    } catch (e) {}

    applyFilters();
    bindBannerPullToRefresh();
    bindCompactHeader();
    if ('scrollRestoration' in history) history.scrollRestoration = 'manual';
    try {
      if (sessionStorage.getItem('ynlRefreshToTop')) {
        sessionStorage.removeItem('ynlRefreshToTop');
        returnToLatestStories();
        requestAnimationFrame(function () { window.scrollTo(0, 0); });
      }
    } catch (_) {}
    document.getElementById('storiesFeedView')?.addEventListener('click', function (event) {
      if (event.target.closest('.story-title, .fact-preview-strip, .source-link-chip, .hero-image-wrap')) {
        var card = event.target.closest('.compact-card');
        if (card) recordStoryInterest(card.id, 1);
      }
    });

    setInterval(updateRelativeTimestamps, 30000);
    setInterval(function () {
      if (document.hidden) return;
      checkForEdition().then(function (updated) {
        if (updated) {
          var refresh = document.getElementById('btnEditionRefresh');
          if (refresh) refresh.classList.add('edition-ready');
        }
      }).catch(function () {});
    }, 300000);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initOnReady);
  } else {
    initOnReady();
  }
})();
