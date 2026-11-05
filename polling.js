/* Your News Lens: independent, capture-phase Supabase poll controller.
   Loads before the large news controller and works for dynamically added cards. */
(function () {
  'use strict';
  if (window.__YNL_POLLING_V3__) return;
  window.__YNL_POLLING_V3__ = true;
  var URL = 'https://vswxehmxdbtdatnlovsl.supabase.co/rest/v1';
  var KEY = 'sb_publishable_OFiISa3vk9WNRLbIp8xuIg_2emzLYRD';
  var busy = Object.create(null);
  var voted = Object.create(null);
  var stats = Object.create(null);
  var visitorKey = 'ynlCommunityPollVisitorId';
  var id = '';
  try { id = localStorage.getItem(visitorKey) || ''; } catch (_) {}
  if (!id || id.length < 8) {
    id = 'ynl_' + (window.crypto && crypto.randomUUID ? crypto.randomUUID() : Date.now().toString(36) + '_' + Math.random().toString(36).slice(2));
    try { localStorage.setItem(visitorKey, id); } catch (_) {}
  }
  function request(path, payload, prefer) {
    var headers = { apikey: KEY, 'Content-Type': 'application/json' };
    if (prefer) headers.Prefer = prefer;
    return fetch(URL + path, { method: 'POST', headers: headers, body: JSON.stringify(payload) }).then(function (r) {
      if (r.ok) return r.status === 204 ? null : r.text().then(function (t) { return t ? JSON.parse(t) : null; });
      return r.text().then(function (t) { var err = new Error('Supabase HTTP ' + r.status + ': ' + t); err.status = r.status; throw err; });
    });
  }
  function counts(rows) {
    var a = 0, d = 0;
    if (!Array.isArray(rows)) throw new Error('Unexpected Supabase poll result format');
    rows.forEach(function (r) {
      var choice = String(r.choice_id || r.choice || '').toLowerCase();
      var count = Number(r.vote_count != null ? r.vote_count : (r.count != null ? r.count : r.total_votes));
      if (!Number.isFinite(count) || count < 0) return;
      if (choice === 'agree') a += count;
      if (choice === 'disagree') d += count;
    });
    return { agree: a, disagree: d, total: a + d };
  }
  function getResults(storyId) {
    return request('/rpc/get_poll_results', { p_story_id: storyId }).then(function (rows) {
      var result = counts(rows);
      stats[storyId] = result;
      return result;
    });
  }
  function show(poll, message, result, choice) {
    var footer = poll.querySelector('.take-footer-meta');
    var msg = poll.querySelector('.take-voted-msg');
    var total = poll.querySelector('.take-total-votes');
    var agree = poll.querySelector('.btn-take-agree .vote-pct');
    var disagree = poll.querySelector('.btn-take-disagree .vote-pct');
    var track = poll.querySelector('.take-consensus-track');
    var fillA = poll.querySelector('.take-fill-agree');
    var fillD = poll.querySelector('.take-fill-disagree');
    if (footer) footer.style.display = 'flex';
    if (msg) msg.textContent = message;
    if (!result) {
      if (total) total.textContent = '';
      if (agree) agree.style.display = 'none';
      if (disagree) disagree.style.display = 'none';
      if (track) track.style.display = 'none';
      return;
    }
    var ap = result.total ? Math.round(result.agree * 100 / result.total) : 0;
    var dp = result.total ? 100 - ap : 0;
    if (total) total.textContent = 'Total votes: ' + result.total.toLocaleString();
    if (agree) { agree.textContent = ap + '%'; agree.style.display = result.total ? 'inline-block' : 'none'; }
    if (disagree) { disagree.textContent = dp + '%'; disagree.style.display = result.total ? 'inline-block' : 'none'; }
    if (track) track.style.display = result.total ? 'flex' : 'none';
    if (fillA) fillA.style.width = ap + '%';
    if (fillD) fillD.style.width = dp + '%';
    if (choice) {
      poll.classList.add('has-voted');
      var btn = poll.querySelector(choice === 'agree' ? '.btn-take-agree' : '.btn-take-disagree');
      if (btn) btn.classList.add(choice === 'agree' ? 'selected-agree' : 'selected-disagree');
      if (msg) msg.textContent = result.total ? ('📊 ' + (choice === 'agree' ? ap : dp) + '% voted with you • Agree: ' + ap + '% / Disagree: ' + dp + '%') : 'Your vote was saved. No results returned yet.';
    } else if (msg) msg.textContent = result.total ? ('Agree: ' + ap + '% • Disagree: ' + dp + '%') : 'No community votes yet.';
  }
  function setBusy(poll, isBusy) {
    poll.querySelectorAll('.btn-take-vote').forEach(function (b) { b.disabled = isBusy; });
  }
  function revealLens(poll, storyId, choice) {
    var panel = document.getElementById(storyId + '-lens-panel');
    if (!panel) return;
    if (panel.parentNode !== poll) poll.appendChild(panel);
    panel.style.display = 'block';
    var lens = poll.getAttribute(choice === 'agree' ? 'data-agree-lens' : 'data-disagree-lens') || (choice === 'agree' ? 'RIGHT' : 'LEFT');
    if (typeof window.switchStoryPerspective === 'function') window.switchStoryPerspective(storyId, lens.toUpperCase());
  }
  function vote(poll, button) {
    var storyId = poll.getAttribute('data-story-id') || button.getAttribute('data-story-id');
    var choice = String(button.getAttribute('data-choice') || (button.classList.contains('btn-take-disagree') ? 'disagree' : 'agree')).toLowerCase();
    if (!storyId || (choice !== 'agree' && choice !== 'disagree') || busy[storyId]) return;
    if (voted[storyId]) { show(poll, 'You have already voted on this story.', stats[storyId] || null, voted[storyId]); return; }
    busy[storyId] = true;
    setBusy(poll, true);
    show(poll, 'Submitting your vote…', null);
    var lens = poll.getAttribute(choice === 'agree' ? 'data-agree-lens' : 'data-disagree-lens') || 'CENTER';
    var label = button.querySelector('.vote-label');
    request('/poll_votes', { story_id: storyId, choice_id: choice, choice_label: label ? label.textContent.trim() : choice, lens: lens.toLowerCase(), voter_id: id }, 'return=minimal')
      .then(function () {
        voted[storyId] = choice;
        return getResults(storyId).then(function (result) { show(poll, '', result, choice); revealLens(poll, storyId, choice); });
      })
      .catch(function (err) {
        console.error('[YNL polling] Vote failed:', err);
        var duplicate = err.status === 409 || /23505|duplicate key/i.test(err.message);
        show(poll, duplicate ? 'You have already voted on this story. Reload to view community results.' : 'Vote not saved: ' + err.message, null);
      })
      .finally(function () { busy[storyId] = false; setBusy(poll, false); });
  }
  // Capture phase deliberately runs before legacy inline handlers and bubbling listeners.
  document.addEventListener('click', function (event) {
    var button = event.target && event.target.closest ? event.target.closest('.btn-take-vote') : null;
    if (!button) return;
    var poll = button.closest('.controversial-take-poll');
    if (!poll) return;
    event.preventDefault();
    event.stopImmediatePropagation();
    vote(poll, button);
  }, true);
  window.__ynlPollControllerVersion = '3.0';
})();
