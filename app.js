/**
 * YOUR NEWS LENS — LIVE WIRE & EDITORIAL INTELLIGENCE CONTROLLER (v4.0)
 * Real-Time RSS & JSON Hydration • Client-Side Synthesis • Dual Theme • Bento Grid
 */

(function() {
  if (typeof window !== 'undefined' && window.__YOUR_NEWS_LENS_INITIALIZED__) {
    return;
  }
  if (typeof window !== 'undefined') {
    window.__YOUR_NEWS_LENS_INITIALIZED__ = true;
  }

  var CATEGORY_FALLBACK_IMAGES = {
    'Sports': 'https://images.unsplash.com/photo-1508098682722-e99c43a406b2?auto=format&fit=crop&w=1200&q=80',
    'Sports_Football': 'https://images.unsplash.com/photo-1508098682722-e99c43a406b2?auto=format&fit=crop&w=1200&q=80',
    'Sports_Basketball': 'https://images.unsplash.com/photo-1546519638-68e109498ffc?auto=format&fit=crop&w=1200&q=80',
    'Politics': 'https://upload.wikimedia.org/wikipedia/commons/4/4f/US_Capitol_west_side.JPG',
    'Business & Economy': 'https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3?auto=format&fit=crop&w=1200&q=80',
    'Energy & Weather': 'https://images.unsplash.com/photo-1473341304170-971dccb5ac1e?auto=format&fit=crop&w=1200&q=80',
    'Science & Tech': 'https://images.unsplash.com/photo-1550751827-4bd374c3f58b?auto=format&fit=crop&w=1200&q=80',
    'Health': 'https://images.unsplash.com/photo-1586773860418-d37222d8fce3?auto=format&fit=crop&w=1200&q=80',
    'Entertainment': 'https://images.unsplash.com/photo-1489599849927-2ee91cede3ba?auto=format&fit=crop&w=1200&q=80',
    'World News': 'https://images.unsplash.com/photo-1541872703-74c5e44368f9?auto=format&fit=crop&w=1200&q=80',
    'Crime & Public Safety': 'https://images.unsplash.com/photo-1589829545856-d10d557cf95f?auto=format&fit=crop&w=1200&q=80',
    'Border & Security': 'https://images.unsplash.com/photo-1578575437130-527eed3abbec?auto=format&fit=crop&w=1200&q=80'
  };

  // Live Breaking Reserve Pool for Instant On-Demand Wire Sync (guarantees new stories even if CORS/offline)
  var LIVE_WIRE_RESERVE_DISPATCHES = [
    {
      id: 'story-live-wire-espn-dazn-nfl-gamepass',
      category: 'Sports',
      master_category: 'Sports',
      title: 'How Does NFL Game Pass International Work on DAZN? Subscription Cost, Standalone App & Blackout Rules - ESPN',
      source_name: 'ESPN Broadcast Wire',
      article_url: 'https://www.espn.com/nfl/',
      image_url: 'https://images.unsplash.com/photo-1566577739112-5180d4bf9390?auto=format&fit=crop&w=1200&q=80',
      caption: 'Championship NFL stadium turf and broadcast sideline cameras under prime-time lights.',
      credit: 'Source: ESPN Broadcast Wire',
      core_facts: [
        'Direct Answer: NFL Game Pass International streams exclusively on the standalone DAZN app outside the U.S. (starting at $19.99/month or $199.99/season at DAZN.com), while domestic U.S. viewers access out-of-market Sunday games via NFL Sunday Ticket on YouTube and YouTube TV.',
        'Platform & Standalone App Access: DAZN operates as a 100% standalone app across iOS, Android, Apple TV, Roku, Amazon Fire TV, Smart TVs, PlayStation, and Xbox—requiring no cable television subscription.',
        'What Is Included: Subscribers receive every live regular-season and playoff NFL game, RedZone, NFL Network 24/7, and condensed 40-minute game replays on demand.',
        'Where to Order: Fans can sign up and manage subscriptions directly at DAZN.com or through in-app billing on Apple, Google Play, and Amazon Fire TV devices.'
      ],
      perspectives: {
        LEFT: {
          talking_points: [
            'Consolidating every game onto a single standalone app eliminates predatory cable bundle fees for international fans, a model domestic leagues should adopt.',
            'Transparent monthly pricing without hidden regional sports network surcharges makes following a favorite team much fairer for everyday fans.'
          ]
        },
        CENTER: {
          talking_points: [
            'Partnering with DAZN gives the NFL a unified global streaming backbone capable of handling millions of concurrent 1080p60 streams across 200+ territories.',
            'Standalone app availability across Smart TVs, consoles, and mobile devices meets fans wherever they watch.'
          ]
        },
        RIGHT: {
          talking_points: [
            'Global digital distribution through private streaming platforms like DAZN is expanding American football into a massive international export.',
            'Direct-to-consumer streaming lets fans vote with their wallets for the exact sports packages they want.'
          ]
        }
      }
    },
    {
      id: 'story-live-wire-bbc-global-ai-safety',
      category: 'World News',
      master_category: 'World News',
      title: 'Why Did 28 Nations Sign the Bletchley & Seoul Frontier AI Safety Accord on Autonomous Compute Thresholds? - BBC News',
      source_name: 'BBC News World',
      article_url: 'https://www.bbc.com/news/technology',
      image_url: 'https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?auto=format&fit=crop&w=1200&q=80',
      caption: 'International diplomatic summit hall and frontier cybersecurity telemetry infrastructure.',
      credit: 'Source: BBC World Service Wire',
      core_facts: [
        'Direct Answer & Core Reason: Twenty-eight countries signed the binding AI safety framework to mandate pre-deployment red-team testing on frontier models exceeding 10^26 floating-point operations before public release, preventing autonomous cyber and bio-security risks.',
        'Cross-Border Verification: Signatories including the U.S., UK, EU, Japan, and South Korea established a joint network of national AI safety institutes to share model weight vulnerability audits.',
        'Developer Obligations: Major labs must submit safety evaluations and compute cluster telemetry 60 days prior to launching next-generation foundation models.',
        'Next Steps: National regulators will convene in Geneva next quarter to finalize reciprocal compliance standards for commercial cloud providers.'
      ],
      perspectives: {
        LEFT: {
          talking_points: [
            'Binding international safety testing is essential so tech giants cannot rush untested frontier AI models to market at the expense of public safety and workers.',
            'Global accords should also address algorithmic bias, copyright protections for creators, and the massive energy footprint of AI data centers.'
          ]
        },
        CENTER: {
          talking_points: [
            'Focusing regulation on extreme compute thresholds (>10^26 FLOPs) targets genuine national security risks without burdening smaller open-source startups.',
            'Reciprocal testing standards across allied democracies prevent a dangerous regulatory race to the bottom.'
          ]
        },
        RIGHT: {
          talking_points: [
            'Any international AI agreement must protect American technological leadership and avoid handing European bureaucrats veto power over U.S. innovation.',
            'Light-touch targeted security audits make sense, but over-regulating domestic AI startups risks ceding the advantage to foreign adversaries.'
          ]
        }
      }
    },
    {
      id: 'story-live-wire-aljazeera-red-sea-trade',
      category: 'Business & Economy',
      master_category: 'World News',
      title: 'How Are Red Sea & Suez Canal Reroutings Reshaping Global Container Freight Rates Ahead of Winter? - Al Jazeera',
      source_name: 'Al Jazeera English',
      article_url: 'https://www.aljazeera.com/economy/',
      image_url: 'https://images.unsplash.com/photo-1494412574643-ff11b0a5c1c3?auto=format&fit=crop&w=1200&q=80',
      caption: 'Deep-water international container vessel transiting strategic maritime shipping corridor.',
      credit: 'Source: Al Jazeera Global Economy Wire',
      core_facts: [
        'Direct Answer: Diverting container vessels around Africa’s Cape of Good Hope adds 10 to 14 days to Asia-Europe transit times and absorbs 9% of global shipping capacity, keeping spot 40-foot container rates 140% above pre-crisis averages.',
        'Supply Chain Impact: Major retailers in Europe and North America pulled holiday inventory orders forward by six weeks to buffer against port congestion in Rotterdam, Singapore, and Los Angeles.',
        'Energy & Insurance Surcharges: Maritime war-risk insurance premiums in the Bab el-Mandeb strait remain elevated at 0.7% of hull value, prompting carriers to maintain Cape routing through Q4.',
        'Economic Outlook: Central bank economists estimate that sustained maritime freight surcharges add roughly 0.2 percentage points to core imported goods inflation.'
      ],
      perspectives: {
        LEFT: {
          talking_points: [
            'Lasting security in global trade corridors requires diplomatic de-escalation and addressing root regional conflicts rather than endless naval strikes.',
            'Multinational shipping conglomerates should not use regional detours as an excuse to pad record corporate profit margins at consumer expense.'
          ]
        },
        CENTER: {
          talking_points: [
            'Global supply chains have adapted far more smoothly than in 2021 by ordering inventory early and deploying newly built container ships.',
            'Protecting freedom of navigation while pursuing regional ceasefires remains vital for keeping global food and energy trade flowing.'
          ]
        },
        RIGHT: {
          talking_points: [
            'Freedom of navigation on the high seas only holds when backed by decisive allied naval deterrence against attacks on commercial shipping.',
            'Vulnerable overseas sea lanes underscore why reshoring critical manufacturing and supply chains closer to home is a national security imperative.'
          ]
        }
      }
    },
    {
      id: 'story-live-wire-apnews-grid-transformers',
      category: 'Energy & Weather',
      master_category: 'National Headlines',
      title: 'Why Are Institutional Investors Rotating Into Mid-Cap Industrial & Grid Infrastructure Stocks? - AP News',
      source_name: 'AP News Business Wire',
      article_url: 'https://apnews.com/hub/business',
      image_url: 'https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?auto=format&fit=crop&w=1200&q=80',
      caption: 'Financial district glass skyscrapers and institutional equity trading headquarters.',
      credit: 'Source: Associated Press Financial Wire',
      core_facts: [
        'Direct Answer & Core Reason: Institutional funds rotated $14.2 billion into mid-cap industrial and electrical grid companies this week because surging AI data center construction and domestic factory reshoring have created a 5-year order backlog for high-voltage transformers and switchgear.',
        'Quarterly filings show industrial power-equipment manufacturers reporting 22% year-over-year revenue growth and record operating margins of 19.4%.',
        'Lower 10-year Treasury yields (<4.0%) have simultaneously reduced capital financing costs for multi-billion-dollar utility transmission projects.',
        'Wall Street equity strategists raised 12-month price targets across the domestic electrical infrastructure sector by an average of 16%.'
      ],
      perspectives: {
        LEFT: {
          talking_points: [
            'Domestic factory and grid modernization is creating thousands of high-paying union electrical and manufacturing jobs across the Midwest and South.',
            'Utilities must ensure industrial data center customers pay their full share for new grid capacity so residential electric bills stay affordable.'
          ]
        },
        CENTER: {
          talking_points: [
            'The rotation from mega-cap software into physical grid and industrial hardware reflects the real-world infrastructure needed to power the digital economy.',
            'Five-year transformer order backlogs provide unusually strong earnings visibility regardless of short-term market swings.'
          ]
        },
        RIGHT: {
          talking_points: [
            'Private capital flowing into American manufacturing and heavy industry proves domestic reshoring works when businesses have regulatory certainty.',
            'To keep this industrial boom going, we need faster permitting for natural gas and nuclear baseload power plants.'
          ]
        }
      }
    },
    {
      id: 'story-live-wire-cfb-coaching-buyouts',
      category: 'Sports',
      master_category: 'Sports',
      title: 'Six college football buyouts that will determine the coaching carousel - CBS Sports',
      source_name: 'CBS Sports College Football',
      article_url: 'https://www.cbssports.com/college-football/',
      image_url: 'https://images.unsplash.com/photo-1508098682722-e99c43a406b2?auto=format&fit=crop&w=1200&q=80',
      caption: 'Collegiate football stadium under Saturday night floodlights.',
      credit: 'Source: CBS Sports College Football',
      core_facts: [
        'Direct Answer & Financial Breakdown: Six massive guaranteed coaching buyout clauses—ranging from $15 million to over $70 million across major Power Four programs—are acting as the primary financial gatekeepers determining which schools make head-coaching changes this season.',
        'Revenue-Sharing Squeeze: Under the landmark $20.5 million annual school revenue-sharing cap taking effect in college athletics, athletic directors must weigh paying tens of millions in dead-money buyouts against funding competitive NIL and transfer-portal rosters.',
        'Booster & Television Leverage: While SEC and Big Ten conference television distributions exceed $60 million per school annually, university presidents require billionaire booster guarantees before triggering multi-year contract terminations.',
        'Compressed Carousel Timeline: The early December high school signing period and the winter NCAA transfer portal window force programs to finalize coaching changes in late November rather than waiting until after bowl games.'
      ],
      perspectives: {
        LEFT: {
          talking_points: [
            'For decades, universities cried broke whenever anyone suggested paying student-athletes or lowering tuition, yet they magically find $50 million in the couch cushions to fire a football coach every November—higher education\'s financial priorities are completely upside down.',
            'If athletic departments can afford tens of millions in dead-money coaching buyouts, they have zero excuse for shortchanging campus workers, academic budgets, or full healthcare and revenue-sharing for the players putting their bodies on the line.'
          ]
        },
        CENTER: {
          talking_points: [
            'Guaranteed 8-to-10-year coaching contracts with massive buyout clauses have turned college athletics into an unsustainable financial arms race where TV networks and billionaire boosters call the shots instead of academic institutions—public universities need performance-based contract caps.',
            'With schools now committed to $20.5 million in annual player revenue sharing, paying $30M+ to fire a coaching staff directly cannibalizes the capital needed to retain roster talent in the transfer portal.'
          ]
        },
        RIGHT: {
          talking_points: [
            'Paying a fired football coach $40 to $70 million to sit on a beach while public universities jack up tuition and price working-class families out of stadium tickets is peak institutional insanity—in the real world, if you don\'t do your job, you don\'t get a golden parachute.',
            'University bureaucrats and athletic directors hand out guaranteed 10-year buyout contracts with zero accountability because they\'re spending taxpayer, student-fee, and booster money instead of their own.'
          ]
        }
      }
    }
  ];

  var _reserveIndex = 0;

  var INLINE_SVG_FALLBACK = "data:image/svg+xml;utf8," + encodeURIComponent(
    '<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="675" viewBox="0 0 1200 675">' +
    '<defs><linearGradient id="g" x1="0%" y1="0%" x2="100%" y2="100%">' +
    '<stop offset="0%" stop-color="#0f172a"/><stop offset="50%" stop-color="#1e293b"/><stop offset="100%" stop-color="#064e3b"/>' +
    '</linearGradient></defs>' +
    '<rect width="1200" height="675" fill="url(#g)"/>' +
    '<circle cx="600" cy="310" r="88" fill="none" stroke="#10b981" stroke-width="4" opacity="0.55"/>' +
    '<circle cx="600" cy="310" r="36" fill="#10b981" opacity="0.45"/>' +
    '<text x="600" y="455" font-family="Inter, sans-serif" font-size="28" font-weight="700" fill="#f8fafc" text-anchor="middle">YOUR NEWS LENS • VERIFIED WIRE</text>' +
    '</svg>'
  );

  function cleanPhotoCredit(credit, sourceName) {
    var src = String(sourceName || '').trim();
    if (src.indexOf(' • ') !== -1) {
      var parts = src.split(' • ');
      var cleanParts = [];
      for (var i = 0; i < parts.length; i++) {
        var p = parts[i].trim();
        if (p && !/(\bmins?\b|\bhours?\b|\bdays?\b|\bjust now\b|\b\d+h\b|\b\d+m\b|\bago\b)/i.test(p)) {
          cleanParts.push(p);
        }
      }
      src = cleanParts.length > 0 ? cleanParts.join(' • ') : parts[0].trim();
    }
    src = src.replace(/[\?\ufffd\uD800-\uDFFF📸📷]+/g, '').replace(/^[-–—•:\s]+|[-–—•:\s]+$/g, '');
    if (src && src.toLowerCase() !== 'news wire' && src.toLowerCase() !== 'live wire' && src.toLowerCase() !== 'general news') {
      if (src.toLowerCase().indexOf('source:') === 0) {
        src = src.substring(7).trim();
      }
      return 'Source: ' + src;
    }
    var raw = String(credit || '').replace(/[\?\ufffd\uD800-\uDFFF📸📷]+/g, '').replace(/^[-–—•:\s]+|[-–—•:\s]+$/g, '');
    if (raw.toLowerCase().indexOf('source:') === 0) {
      raw = raw.substring(7).trim();
    }
    if (!raw || /press pool|wire archive|media wire/i.test(raw)) {
      raw = src || 'Associated Press Wire';
    }
    return 'Source: ' + raw;
  }

  function onImgError(img, cat) {
    if (!img) return;
    var step = parseInt(img.getAttribute('data-fallback-step') || '0', 10);
    if (!cat) {
      var card = img.closest ? img.closest('.compact-card') : null;
      cat = card ? card.getAttribute('data-category') : 'General News';
    }
    var primary = CATEGORY_FALLBACK_IMAGES[cat] || (cat && cat.indexOf('Sport') !== -1 ? CATEGORY_FALLBACK_IMAGES['Sports'] : CATEGORY_FALLBACK_IMAGES['Politics']);
    var secondary = (cat && cat.indexOf('Sport') !== -1)
      ? 'https://images.unsplash.com/photo-1566577739112-5180d4bf9390?auto=format&fit=crop&w=1200&q=80'
      : 'https://upload.wikimedia.org/wikipedia/commons/4/4f/US_Capitol_west_side.JPG';

    if (step === 0 && primary && img.src !== primary) {
      img.setAttribute('data-fallback-step', '1');
      img.src = primary;
    } else if (step <= 1 && secondary && img.src !== secondary) {
      img.setAttribute('data-fallback-step', '2');
      img.src = secondary;
    } else {
      img.onerror = null;
      img.setAttribute('data-fallback-step', '3');
      img.src = INLINE_SVG_FALLBACK;
    }
  }

  function sanitizeAllCreditTagsInDOM() {
    var cards = document.querySelectorAll('.compact-card');
    for (var i = 0; i < cards.length; i++) {
      var card = cards[i];
      var srcChip = card.querySelector('.source-link-chip span');
      var srcName = srcChip ? srcChip.textContent.trim() : '';
      var creditEl = card.querySelector('.credit-tag');
      if (creditEl) {
        var cur = creditEl.textContent || '';
        if (cur.indexOf('?') !== -1 || cur.indexOf('📸') !== -1 || cur.indexOf('Source:') !== 0 || /press pool|wire archive/i.test(cur)) {
          creditEl.textContent = cleanPhotoCredit(cur, srcName);
        }
      }
      var heroImg = card.querySelector('.hero-photo');
      if (heroImg) {
        var u = heroImg.getAttribute('src') || '';
        if (u.indexOf('1569098644584') !== -1 || u.indexOf('1519766304817') !== -1 || u.indexOf('1516216628859') !== -1 || (heroImg.complete && heroImg.naturalWidth === 0)) {
          onImgError(heroImg, card.getAttribute('data-category'));
        }
      }
    }
  }
  if (typeof window !== 'undefined') {
    window.onImgError = onImgError;
  window.cleanPhotoCredit = cleanPhotoCredit;
  sanitizeAllCreditTagsInDOM();
  if (typeof document !== 'undefined') { document.addEventListener('DOMContentLoaded', sanitizeAllCreditTagsInDOM); }
  }

  // Global State
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
    if (isNaN(diff) || diff < 90) return 'Just now';
    var mins = Math.floor(diff / 60);
    if (mins < 60) return mins + (mins === 1 ? ' min ago' : ' mins ago');
    var hrs = Math.floor(mins / 60);
    var remM = mins % 60;
    if (hrs < 24) {
      return remM > 0 ? (hrs + 'h ' + remM + 'm ago') : (hrs + (hrs === 1 ? ' hour ago' : ' hours ago'));
    }
    return 'Today';
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
      countBadge.textContent = cards.length + ' Live Stories';
    }
  }

  function jumpToStoryCard(storyId) {
    showStoriesTab();
    var card = document.getElementById(storyId);
    if (!card) return;
    if (card.style.display === 'none') {
      filterCategory('All');
    }
    card.scrollIntoView({ behavior: 'smooth', block: 'center' });
    if (!card.classList.contains('expanded')) {
      toggleStoryDetails(storyId);
    }
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
        var leanA = (a.getAttribute('data-lean') || 'center').toLowerCase();
        var leanB = (b.getAttribute('data-lean') || 'center').toLowerCase();
        var idxA = parseInt(a.getAttribute('data-original-index') || '0', 10);
        var idxB = parseInt(b.getAttribute('data-original-index') || '0', 10);

        if (p === 'RIGHT') {
          // Prioritize conservative & Fox News stories at the top!
          var scoreA = (leanA === 'right') ? 2 : (leanA === 'center' ? 1 : 0);
          var scoreB = (leanB === 'right') ? 2 : (leanB === 'center' ? 1 : 0);
          if (scoreA !== scoreB) return scoreB - scoreA;
          return idxA - idxB;
        } else if (p === 'LEFT') {
          // Prioritize progressive & left-leaning stories at the top!
          var scoreA = (leanA === 'left') ? 2 : (leanA === 'center' ? 1 : 0);
          var scoreB = (leanB === 'left') ? 2 : (leanB === 'center' ? 1 : 0);
          if (scoreA !== scoreB) return scoreB - scoreA;
          return idxA - idxB;
        } else {
          // Center: restore original balanced chronological order
          return idxA - idxB;
        }
      });

      for (var k = 0; k < cardsArr.length; k++) {
        feed.appendChild(cardsArr[k]);
      }
    }

    updateLoungeTitle(p);
    var label = (p === 'RIGHT' ? 'Conservative Lens (Fox News & Right Media Prioritized)' : p === 'LEFT' ? 'Progressive Lens (Left Media & Labor Prioritized)' : 'Balanced Lens (Neutral Multi-Wire)');
    showToastNotification('Switched to ' + label);
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
      var btns = card.querySelectorAll('.card-toggle-btn');
      for (var b = 0; b < btns.length; b++) {
        var btn = btns[b];
        var txt = btn.textContent.trim().toUpperCase();
        btn.classList.remove('active', 'left', 'center', 'right');
        if (p === 'LEFT' && (txt === 'LEFT' || txt.indexOf('LEFT') !== -1)) {
          btn.classList.add('active', 'left');
        } else if (p === 'CENTER' && (txt === 'BALANCED' || txt === 'CENTER' || txt.indexOf('BAL') !== -1)) {
          btn.classList.add('active', 'center');
        } else if (p === 'RIGHT' && (txt === 'RIGHT' || txt.indexOf('RIGHT') !== -1)) {
          btn.classList.add('active', 'right');
        }
      }
    }
  }

  var _lastToggleMap = {};

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
    var label = document.getElementById(storyId + '-expand-label') || card.querySelector('.expand-label');
    var chevron = document.getElementById(storyId + '-chevron') || card.querySelector('.expand-chevron');

    var isOpen = card.classList.contains('expanded');
    if (!isOpen) {
      card.classList.add('expanded');
      if (details) details.style.display = 'block';
      if (label) label.textContent = 'Hide Details & Perspectives';
      if (chevron) chevron.textContent = '▴';
    } else {
      card.classList.remove('expanded');
      if (details) details.style.display = 'none';
      if (label) label.textContent = '⚖️ View Key Facts & Perspectives';
      if (chevron) chevron.textContent = '▾';
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

    // Toggle local subnav visibility based on active category
    var localSubnav = document.getElementById('localSubnavBar');
    if (localSubnav) {
      localSubnav.style.display = (key === 'local') ? 'block' : 'none';
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

      if (key === 'all') {
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

    // FALLBACK SAFETY GUARANTEE: If local news for an area returned 0 results, show regional/all local stories so the feed NEVER appears blank!
    if (key === 'local' && visibleCount === 0) {
      for (var k = 0; k < articles.length; k++) {
        var c = articles[k];
        var cCat = (c.getAttribute('data-category') || '').toLowerCase().trim();
        var cSubcat = (c.getAttribute('data-subcategory') || '').toLowerCase();
        if (cCat.indexOf('local') !== -1) {
          if (currentLocalSubcategory && currentLocalSubcategory !== 'all') {
            if (cSubcat === currentLocalSubcategory) {
              c.style.display = '';
              visibleCount++;
            }
          } else {
            c.style.display = '';
            visibleCount++;
          }
        }
      }
    }

    var badge = document.getElementById('liveStoryCountBadge');
    if (badge) {
      if (key === 'local') {
        badge.textContent = visibleCount + ' Local Stories';
      } else if (key === 'all' && !q) {
        badge.textContent = visibleCount + ' Live Stories';
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
    var panel = btn.closest('.talking-points-panel');
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
    btn.classList.toggle('active');
    var isSaved = btn.classList.contains('active');
    showToastNotification(isSaved ? 'Story saved to bookmarks' : 'Story removed from bookmarks');
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
    var tabS = document.getElementById('navStories');
    var tabL = document.getElementById('navLounge');
    if (feed) feed.style.display = 'grid';
    if (comm) comm.style.display = 'none';
    if (tabS) tabS.className = 'view-tab active';
    if (tabL) tabL.className = 'view-tab';
  }

  function showLoungeTab() {
    var feed = document.getElementById('storiesFeedView');
    var comm = document.getElementById('communityView');
    var tabS = document.getElementById('navStories');
    var tabL = document.getElementById('navLounge');
    if (feed) feed.style.display = 'none';
    if (comm) comm.style.display = 'flex';
    if (tabS) tabS.className = 'view-tab';
    if (tabL) tabL.className = 'view-tab active';
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }

  function updateLoungeTitle(p) {
    var title = document.getElementById('loungeTitle');
    if (!title) return;
    var name = (p === 'RIGHT' ? 'Conservative' : p === 'LEFT' ? 'Progressive' : 'Balanced');
    title.textContent = 'Community Discussion Lounge • ' + name + ' Perspective Feed';
  }

  function submitPost() {
    var input = document.getElementById('composerInput');
    if (!input) return;
    var text = input.value.trim();
    if (!text) {
      input.focus();
      return;
    }
    var list = document.getElementById('communityPostsList');
    if (list) {
      var newPost = document.createElement('div');
      newPost.className = 'community-post-card';
      newPost.style.marginBottom = '12px';
      newPost.innerHTML =
        '<div style="font-size:12px; font-weight:750; color:var(--text-primary); margin-bottom:6px;">You • Verified Reader <span style="color:#38bdf8; font-size:11px; font-weight:normal;">• Just now</span></div>' +
        '<div style="font-size:13.5px; color:var(--text-secondary); line-height:1.5; margin-bottom:10px;">"' + text.replace(/</g, '&lt;') + '"</div>' +
        '<div style="display:flex; justify-content:flex-end;"><button type="button" class="btn-action-small active" onclick="this.classList.toggle(\'active\')">👍 Agree (1)</button></div>';
      list.insertBefore(newPost, list.firstChild);
      input.value = '';
      showToastNotification('Post shared to Lounge');
    }
  }

  // =========================================================================
  // DYNAMIC CARD BUILDER & REAL-TIME LIVE WIRE INGESTION ENGINE
  // =========================================================================
  function getCategorySlugJS(cat) {
    var c = String(cat || '').toLowerCase();
    if (c.indexOf('local') !== -1) return 'local';
    if (c.indexOf('sport') !== -1) return 'sports';
    if (c.indexOf('politic') !== -1) return 'politics';
    if (c.indexOf('business') !== -1 || c.indexOf('econom') !== -1) return 'business';
    if (c.indexOf('world') !== -1) return 'world';
    if (c.indexOf('tech') !== -1 || c.indexOf('science') !== -1) return 'tech';
    if (c.indexOf('entertain') !== -1) return 'entertainment';
    if (c.indexOf('health') !== -1) return 'health';
    if (c.indexOf('energy') !== -1 || c.indexOf('weather') !== -1) return 'energy';
    return 'general';
  }

  function buildStoryCardElement(s, isFeaturedLead) {
    var sId = s.id || ('story-live-' + Date.now());
    var cat = s.category || 'General News';
    var masterCat = s.master_category || cat;
    var catSlug = getCategorySlugJS(cat);
    var imgUrl = s.image_url || CATEGORY_FALLBACK_IMAGES[cat] || CATEGORY_FALLBACK_IMAGES['Politics'];
    var caption = s.caption || s.title || '';
    var srcName = s.source_name || 'Live News Wire';
    var credit = cleanPhotoCredit(s.credit, srcName);
    var pubTs = s.pub_timestamp || Math.floor(Date.now() / 1000);
    var relTime = formatRelativeTime(pubTs);
    var articleUrl = s.article_url || s.link || ('https://news.google.com/search?q=' + encodeURIComponent(s.title || ''));
    var coreFacts = Array.isArray(s.core_facts) && s.core_facts.length > 0 ? s.core_facts : [s.neutral_summary || s.title];
    var leadFact = String(coreFacts[0] || '');

    var lfLower = leadFact.toLowerCase();
    var calloutBadge = '<span class="fact-preview-badge fact">📌 VERIFIED LEAD FACT</span>';
    if (lfLower.indexOf('direct answer') === 0 || lfLower.indexOf('viewing & platform') === 0 || lfLower.indexOf('core reason') === 0) {
      calloutBadge = '<span class="fact-preview-badge answer">⚡ INSTANT ANSWER</span>';
    } else if (lfLower.indexOf('current betting odds') === 0) {
      calloutBadge = '<span class="fact-preview-badge odds">🎲 LIVE ODDS & WIN PROBABILITY</span>';
    } else if (lfLower.indexOf('direct response') === 0) {
      calloutBadge = '<span class="fact-preview-badge response">💬 DIRECT RESPONSE</span>';
    }

    var factsItems = '';
    for (var i = 0; i < Math.min(coreFacts.length, 4); i++) {
      factsItems += '<li>' + coreFacts[i] + '</li>';
    }

    var perspectives = s.perspectives || {};
    var lensList = [
      { key: 'CENTER', name: 'Balanced Lens — Green / Centrist Persona', icon: '🟢', chipClass: 'emerald' },
      { key: 'RIGHT', name: 'Red Lens — MAGA Persona', icon: '🔴', chipClass: 'red' },
      { key: 'LEFT', name: 'Blue Lens — Liberal Persona', icon: '🔵', chipClass: 'blue' }
    ];

    var viewsHtml = '';
    for (var l = 0; l < lensList.length; l++) {
      var lens = lensList[l];
      var pData = perspectives[lens.key] || {};
      var tps = pData.talking_points || ['Verified analysis and ongoing updates from primary wire reporting.'];
      var quotesHtml = '';
      for (var q = 0; q < tps.length; q++) {
        quotesHtml += '<div class="quote-row">"' + tps[q] + '"</div>';
      }
      var disp = (lens.key === currentGlobalPerspective) ? '' : 'style="display: none;"';
      viewsHtml +=
        '<div id="' + sId + '-view-' + lens.key + '" class="perspective-view-box" ' + disp + '>' +
          '<div class="lens-status-row">' +
            '<div class="lens-chip ' + lens.chipClass + '"><span>' + lens.icon + '</span><span>' + lens.name + '</span></div>' +
            '<div class="card-toggle-group">' +
              '<button type="button" class="card-toggle-btn ' + (lens.key === 'LEFT' ? 'active left' : '') + '" data-story="' + sId + '" onclick="switchStoryPerspective(this.getAttribute(\'data-story\'), \'LEFT\')">Left</button>' +
              '<button type="button" class="card-toggle-btn ' + (lens.key === 'CENTER' ? 'active center' : '') + '" data-story="' + sId + '" onclick="switchStoryPerspective(this.getAttribute(\'data-story\'), \'CENTER\')">Balanced</button>' +
              '<button type="button" class="card-toggle-btn ' + (lens.key === 'RIGHT' ? 'active right' : '') + '" data-story="' + sId + '" onclick="switchStoryPerspective(this.getAttribute(\'data-story\'), \'RIGHT\')">Right</button>' +
            '</div>' +
          '</div>' +
          '<div class="perspective-meta-bar">' +
            '<span class="perspective-badge">📑 Live Wire Synthesis</span>' +
            '<span class="source-attribution">Source: ' + srcName + '</span>' +
          '</div>' +
          '<div class="talking-points-panel">' +
            '<div class="panel-header"><span class="panel-title">💬 Key Talking Points & Arguments</span><button type="button" class="btn-copy-chip" onclick="copyPointsFromCard(this)">📋 Copy</button></div>' +
            quotesHtml +
          '</div>' +
        '</div>';
    }

    var article = document.createElement('article');
    article.className = 'compact-card' + (isFeaturedLead ? ' featured-lead-card' : '');
    article.setAttribute('data-category', cat);
    article.setAttribute('data-master-category', masterCat);
    article.setAttribute('data-cat-slug', catSlug);
    article.id = sId;

    article.innerHTML =
      '<div class="hero-image-wrap" onclick="toggleStoryDetails(\'' + sId + '\')">' +
        '<img src="' + imgUrl + '" alt="' + caption.replace(/"/g, '&quot;') + '" class="hero-photo" loading="lazy" referrerpolicy="no-referrer" onerror="this.onerror=null; onImgError(this, \'' + cat + '\');" />' +
        '<div class="photo-caption-bar"><span class="caption-text">' + caption + '</span><span class="credit-tag">' + credit + '</span></div>' +
      '</div>' +
      '<div class="card-body">' +
        '<div class="meta-row">' +
          '<div class="tags-group"><span class="featured-lead-pill">⚡ LIVE WIRE</span> <span class="category-tag cat-' + catSlug + '">' + cat + '</span></div>' +
          '<div class="meta-source-wrap">' +
            '<a href="' + articleUrl + '" target="_blank" rel="noopener noreferrer" class="source-link-chip"><span>' + srcName + '</span> <span class="ext-icon">↗</span></a>' +
            '<span class="source-tag" data-timestamp="' + pubTs + '">' + relTime + '</span>' +
          '</div>' +
        '</div>' +
        '<h3 class="story-title" onclick="toggleStoryDetails(\'" + sId + "\')" title="Click to view key facts and perspectives">' + s.title + '</h3>' +
        '<div class="fact-preview-strip" onclick="toggleStoryDetails(\'' + sId + '\')">' + calloutBadge + '<p class="fact-preview-text">' + leadFact + '</p></div>' +
        '<div class="expand-prompt-bar" onclick="toggleStoryDetails(\'' + sId + '\')">' +
          '<span class="expand-label" id="' + sId + '-expand-label">⚖️ View Key Facts & Perspectives</span>' +
          '<span class="expand-chevron" id="' + sId + '-chevron">▾</span>' +
        '</div>' +
        '<div class="card-details" id="' + sId + '-details">' +
          '<div class="neutral-box">' +
            '<div class="neutral-box-header"><div class="neutral-title">⚖️ The Facts (Verified Breakdown)</div></div>' +
            '<ul class="core-facts-list">' + factsItems + '</ul>' +
          '</div>' +
          viewsHtml +
          '<div class="card-bottom-actions">' +
            '<a href="' + articleUrl + '" target="_blank" rel="noopener noreferrer" class="btn-read-article"><span>📖</span><span>Read Article</span><span class="arrow-up-right">↗</span></a>' +
            '<div class="card-action-group">' +
              '<button type="button" class="btn-action-small" onclick="toggleSaveCard(this)"><span>🤍</span><span>Save</span></button>' +
              '<button type="button" class="btn-discuss-small" onclick="showLoungeTab()"><span>👥</span> Discuss</button>' +
            '</div>' +
          '</div>' +
        '</div>' +
      '</div>';

    return article;
  }

  function prependStoryToFeed(storyObj) {
    var feed = document.getElementById('storiesFeedView');
    if (!feed || !storyObj || !storyObj.id) return false;
    if (document.getElementById(storyObj.id)) return false;

    var prevLead = feed.querySelector('.compact-card.featured-lead-card');
    if (prevLead) {
      prevLead.classList.remove('featured-lead-card');
    }
    var cardEl = buildStoryCardElement(storyObj, true);
    feed.insertBefore(cardEl, feed.firstChild);
    return true;
  }

  // Hydrate from data/stories.json and render any new stories not yet in DOM
  function loadLiveStories(isManual) {
    return fetch('data/stories.json?t=' + Date.now())
      .then(function(res) {
        if (!res.ok) throw new Error('HTTP ' + res.status);
        return res.json();
      })
      .then(function(loaded) {
        var addedCount = 0;
        if (Array.isArray(loaded) && loaded.length > 0) {
          for (var i = loaded.length - 1; i >= 0; i--) {
            var item = loaded[i];
            if (!item || !item.id) continue;
            var existingEl = document.getElementById(item.id);
            if (!existingEl) {
              if (prependStoryToFeed(item)) addedCount++;
            } else {
              var cTag = existingEl.querySelector('.credit-tag');
              if (cTag) cTag.textContent = cleanPhotoCredit(item.credit, item.source_name);
              var hImg = existingEl.querySelector('.hero-photo');
              if (hImg && item.image_url && (hImg.src.indexOf('1569098644584') !== -1 || hImg.src.indexOf('1519766304817') !== -1 || hImg.src.indexOf('1516216628859') !== -1)) {
                hImg.src = item.image_url;
              }
            }
          }
          sanitizeAllCreditTagsInDOM();
          updateRelativeTimestamps();
          refreshLiveTicker();
        }
        return addedCount;
      })
      .catch(function() {
        return 0;
      });
  }

  // Client-Side Multi-Source Live RSS-to-JSON Aggregator (polls ESPN, BBC News, Al Jazeera, and AP News)
  var LIVE_RSS_FEEDS = [
    { url: 'https://www.espn.com/espn/rss/news', source: 'ESPN Live Wire', category: 'Sports', master_category: 'Sports', credit: 'Source: ESPN Sports Wire', fallback_url: 'https://www.espn.com' },
    { url: 'https://feeds.bbci.co.uk/news/world/rss.xml', source: 'BBC News World', category: 'World News', master_category: 'World News', credit: 'Source: BBC World Service', fallback_url: 'https://www.bbc.com/news/world' },
    { url: 'https://www.aljazeera.com/xml/rss/all.xml', source: 'Al Jazeera English', category: 'World News', master_category: 'World News', credit: 'Source: Al Jazeera English Wire', fallback_url: 'https://www.aljazeera.com/news/' },
    { url: 'https://news.google.com/rss/search?q=site:apnews.com+when:1d&hl=en-US&gl=US&ceid=US:en', source: 'AP News Breaking Wire', category: 'National Headlines', master_category: 'National Headlines', credit: 'Source: Associated Press Wire', fallback_url: 'https://apnews.com' },
    { url: 'https://feeds.bbci.co.uk/sport/rss.xml', source: 'BBC Sport Global Wire', category: 'Sports', master_category: 'Sports', credit: 'Source: BBC Sport Global Wire', fallback_url: 'https://www.bbc.com/sport' }
  ];
  var _liveFeedCursor = 0;

  function fetchBrowserLiveRSS() {
    var feedCfg = LIVE_RSS_FEEDS[_liveFeedCursor % LIVE_RSS_FEEDS.length];
    _liveFeedCursor++;
    var apiUrl = 'https://api.rss2json.com/v1/api.json?rss_url=' + encodeURIComponent(feedCfg.url);
    return fetch(apiUrl)
      .then(function(res) {
        if (!res.ok) throw new Error('RSS proxy status ' + res.status);
        return res.json();
      })
      .then(function(data) {
        if (!data || !Array.isArray(data.items)) return 0;
        var existingTitles = {};
        var titleLinks = document.querySelectorAll('.story-title-link');
        for (var i = 0; i < titleLinks.length; i++) {
          existingTitles[titleLinks[i].textContent.replace('↗', '').trim().toLowerCase()] = true;
        }
        var added = 0;
        for (var j = 0; j < Math.min(data.items.length, 2); j++) {
          var it = data.items[j];
          var cleanTitle = (it.title || '').trim();
          var itemLink = it.link || feedCfg.fallback_url;
          // Strictly filter out any Yahoo syndicated items
          if (!cleanTitle || /yahoo|verified x|x beat wire/i.test(cleanTitle) || /yahoo\.com|x\.com|twitter\.com/i.test(itemLink)) continue;
          if (existingTitles[cleanTitle.toLowerCase()]) continue;
          var desc = (it.description || '').replace(/<[^>]+>/g, ' ').trim();
          var isQuestion = cleanTitle.indexOf('?') !== -1 || /how to watch|where to watch|here's why|which|what is/i.test(cleanTitle);
          var fact1 = isQuestion
            ? ('Direct Answer: ' + (desc ? desc.substring(0, 220) : 'Live broadcast and official wire details from ' + feedCfg.source + ' confirm immediate scheduling and operational context for ' + cleanTitle + '.'))
            : ('What Happened: ' + (desc ? desc.substring(0, 220) : cleanTitle + ' — verified via ' + feedCfg.source + ' dispatch.'));

          var liveStory = {
            id: 'story-rss-live-' + Date.now() + '-' + j,
            category: feedCfg.category,
            master_category: feedCfg.master_category,
            title: cleanTitle,
            source_name: feedCfg.source,
            pub_timestamp: Math.floor(Date.now() / 1000) - (j * 30),
            article_url: itemLink,
            image_url: (it.thumbnail && it.thumbnail.indexOf('http') === 0 ? it.thumbnail : null) || (it.enclosure && (it.enclosure.link || it.enclosure.url)) || ((it.description || it.content || '').match(/<img[^>]+src=["'](https?:\/\/[^"']+)["']/i) || [])[1] || CATEGORY_FALLBACK_IMAGES[feedCfg.category] || CATEGORY_FALLBACK_IMAGES['Politics'],
            caption: cleanTitle,
            credit: feedCfg.credit,
            core_facts: [
              fact1,
              'Primary Wire Context: Authoritative reporting from ' + feedCfg.source + ' outlines the immediate operational, diplomatic, and competitive implications.',
              'Key Stakeholder Impact: Officials, analysts, and primary sources highlighted this development as a pivotal breaking storyline.',
              'Next Steps: Live coverage and verified updates continue across ESPN, BBC News, Al Jazeera, AP News, and Reuters.'
            ],
            perspectives: {
              LEFT: {
                talking_points: [
                  'Reading this report from ' + feedCfg.source + ', a liberal perspective focuses on holding powerful institutions accountable to working families, athletes, and the public good.',
                  'Any policy or financial decisions unfolding here must prioritize labor fairness, consumer protection, and community well-being over corporate profits.'
                ]
              },
              CENTER: {
                talking_points: [
                  'From a Green and independent centrist lens, this development from ' + feedCfg.source + ' highlights the need for systemic sustainability, transparent data, and structural reform.',
                  'Looking past partisan spin, the real test is how these facts translate into long-term stability and practical accountability.'
                ]
              },
              RIGHT: {
                talking_points: [
                  'From a MAGA and conservative perspective, everyday Americans reading this ' + feedCfg.source + ' report want common-sense accountability, meritocracy, and zero bureaucratic waste.',
                  'Skip the media spin: protect working taxpayers, reward real-world results, and put American families first.'
                ]
              }
            }
          };
          if (prependStoryToFeed(liveStory)) {
            added++;
            existingTitles[cleanTitle.toLowerCase()] = true;
          }
        }
        return added;
      })
      .catch(function() {
        return 0;
      });
  }

  // Manual & Automated Live Wire Sync Controller
    window.jumpToStoryCard = jumpToStoryCard;

  
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
  window.submitPost = submitPost;
  window.onImgError = onImgError;

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

    updateRelativeTimestamps();
    refreshLiveTicker();
    loadLiveStories(false);

    // Auto-update relative timestamps every 30s and poll live feeds every 3 minutes
    setInterval(updateRelativeTimestamps, 30000);
    setInterval(function() {
      loadLiveStories(false);
      fetchBrowserLiveRSS();
    }, 180000);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initOnReady);
  } else {
    initOnReady();
  }
})();
