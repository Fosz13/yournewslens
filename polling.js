/* One controller for initial cards and cards loaded from the published feed. */
(function () {
  'use strict';
  const api = 'https://vswxehmxdbtdatnlovsl.supabase.co/rest/v1';
  const apikey = 'sb_publishable_OFiISa3vk9WNRLbIp8xuIg_2emzLYRD';
  const visitorKey = 'ynlCommunityPollVisitorId';
  const savedKey = 'ynlConfirmedPollChoices';
  const pending = new Set();
  const reads = new Map();
  const snapshots = new Map();
  let saved = {};
  let visitor;
  try {
    visitor = localStorage.getItem(visitorKey);
    const previous = JSON.parse(localStorage.getItem(savedKey) || '{}');
    if (previous && typeof previous === 'object') saved = previous;
  } catch (_) {}
  if (!visitor) {
    visitor = 'ynl_' + (window.crypto && crypto.randomUUID ? crypto.randomUUID() : Date.now().toString(36) + Math.random().toString(36).slice(2));
    try { localStorage.setItem(visitorKey, visitor); } catch (_) {}
  }

  async function request(path, body, prefer) {
    const headers = { apikey, 'Content-Type': 'application/json' };
    if (prefer) headers.Prefer = prefer;
    const controller = new AbortController();
    const timeout = setTimeout(() => controller.abort(), 10000);
    try {
      const response = await fetch(api + path, { method: 'POST', headers, body: JSON.stringify(body), signal: controller.signal });
      if (!response.ok) {
        const error = new Error('Poll request returned HTTP ' + response.status);
        error.status = response.status;
        const details = await response.json().catch(() => ({}));
        error.code = details && details.code;
        throw error;
      }
      return path.startsWith('/rpc/') ? await response.json() : null;
    } finally {
      clearTimeout(timeout);
    }
  }

  function pollKey(poll) {
    const question = poll.querySelector('.take-statement-text').textContent.trim();
    const labels = Array.from(poll.querySelectorAll('.vote-label'), label => label.textContent.trim());
    const raw = [question, ...labels].join('|');
    let hash = 2166136261;
    for (let i = 0; i < raw.length; i++) hash = Math.imul(hash ^ raw.charCodeAt(i), 16777619);
    return poll.dataset.storyId + '_q' + (hash >>> 0).toString(36);
  }

  function parseResults(rows) {
    if (!Array.isArray(rows)) throw new Error('Invalid poll results');
    const result = { agree: 0, disagree: 0 };
    for (const row of rows) {
      if (!row || typeof row !== "object") throw new Error("Invalid poll count");
      const choice = String(row.choice_id || row.choice || row.vote_choice || '').toLowerCase();
      const count = Number(row.vote_count ?? row.count ?? row.total_votes ?? row.votes);
      if (!Object.hasOwn(result, choice) || !Number.isSafeInteger(count) || count < 0) {
        throw new Error('Invalid poll count');
      }
      result[choice] += count;
    }
    result.total = result.agree + result.disagree;
    return result;
  }

  function render(poll, key, result, status) {
    const choice = saved[key];
    const voted = choice === 'agree' || choice === 'disagree';
    const agreement = result?.total ? Math.round(result.agree * 100 / result.total) : 0;
    const percentages = { agree: agreement, disagree: 100 - agreement };
    const showResults = Boolean(result?.total);
    for (const button of poll.querySelectorAll('.btn-take-vote')) {
      const side = button.dataset.choice.toLowerCase();
      const selected = choice === side;
      const percentage = button.querySelector('.vote-pct');
      button.disabled = pending.has(key) || voted || choice === 'duplicate';
      button.setAttribute('aria-pressed', String(selected));
      button.classList.toggle('selected-' + side, selected);
      percentage.textContent = showResults ? percentages[side] + '%' : '';
      percentage.style.display = showResults ? 'inline-block' : 'none';
    }
    poll.classList.toggle('has-voted', voted);
    poll.querySelector('.take-consensus-track').style.display = showResults ? 'flex' : 'none';
    poll.querySelector('.take-fill-agree').style.width = agreement + '%';
    poll.querySelector('.take-fill-disagree').style.width = (100 - agreement) + '%';
    poll.querySelector('.take-total-votes').textContent = result ? 'Total votes: ' + result.total.toLocaleString() : '';
    poll.querySelector('.take-voted-msg').textContent = status || (
      !result ? 'Community results are unavailable right now.' :
      voted && showResults ? percentages[choice] + '% picked your answer.' :
      voted || choice === 'duplicate' ? 'Your vote was recorded.' :
      showResults ? 'Community results' : 'No community votes yet.'
    );
  }

  async function refresh(poll, key = pollKey(poll), afterWrite = false) {
    // A read started before a vote may contain the old count.
    if (afterWrite && reads.has(key)) await reads.get(key).catch(() => {});
    if (!reads.has(key)) {
      reads.set(key, request('/rpc/get_poll_results', { p_story_id: key })
        .then(parseResults).finally(() => reads.delete(key)));
    }
    try {
      const result = await reads.get(key);
      snapshots.set(key, result);
      if (!pending.has(key) || afterWrite) render(poll, key, result);
    } catch (_) {
      snapshots.delete(key);
      if (!pending.has(key) || afterWrite) render(poll, key, null,
        saved[key] ? 'Your vote was recorded. Community totals are temporarily unavailable.' : '');
    }
  }

  async function vote(poll, button) {
    const key = pollKey(poll);
    const choice = button.dataset.choice.toLowerCase();
    if (pending.has(key) || saved[key] || !['agree', 'disagree'].includes(choice)) return;
    pending.add(key);
    render(poll, key, snapshots.get(key), 'Submitting your vote…');
    try {
      await request('/poll_votes', {
        story_id: key, choice_id: choice, choice_label: button.querySelector('.vote-label').textContent.trim(),
        lens: 'center', voter_id: visitor
      }, 'return=minimal');
      saved[key] = choice;
      if (window.ynlRecordStoryInterest) window.ynlRecordStoryInterest(poll.dataset.storyId, 3);
    } catch (error) {
      if (error.status === 409 && error.code === '23505') saved[key] = 'duplicate';
      else {
        pending.delete(key);
        render(poll, key, snapshots.get(key), 'Vote could not be confirmed. Please try again.');
        return;
      }
    }
    try {
      localStorage.setItem(savedKey, JSON.stringify(Object.fromEntries(Object.entries(saved).slice(-300))));
    } catch (_) {}
    await refresh(poll, key, true);
    pending.delete(key);
    for (const other of document.querySelectorAll('.controversial-take-poll:not([hidden])')) {
      if (other !== poll && other.dataset.storyId === poll.dataset.storyId && pollKey(other) === key) {
        render(other, key, snapshots.get(key));
      }
    }
    if (poll.closest?.('#communityView')) return;
    const card = document.getElementById(poll.dataset.storyId);
    if (card && card.querySelector('.lens-drawer-panel') && card.dataset.hasPerspectives === 'true' && window.toggleLensDrawer) {
      const panel = card.querySelector('.lens-drawer-panel');
      if (window.getComputedStyle(panel).display === 'none' || window.getComputedStyle(panel.parentElement).display === 'none') {
        window.toggleLensDrawer(card.id);
      }
    }
  }

  const observer = typeof IntersectionObserver === 'function' ? new IntersectionObserver((entries, io) => {
    for (const entry of entries) {
      if (!entry.isIntersecting) continue;
      io.unobserve(entry.target);
      refresh(entry.target);
    }
  }, { rootMargin: '120px 0px' }) : null;

  function observe(root) {
    for (const poll of root.querySelectorAll('.controversial-take-poll:not([hidden])')) {
      const key = pollKey(poll);
      render(poll, key, snapshots.get(key), snapshots.has(key) ? '' : 'Loading community results…');
      if (observer) observer.observe(poll);
      else refresh(poll);
    }
  }

  document.addEventListener('click', event => {
    const button = event.target.closest?.('.btn-take-vote');
    const poll = button?.closest('.controversial-take-poll:not([hidden])');
    if (!poll || button.disabled) return;
    vote(poll, button);
  });
  function visiblePolls() {
    return [...document.querySelectorAll('.controversial-take-poll:not([hidden])')].filter(poll => {
      const rect = poll.getBoundingClientRect();
      return rect.width > 0 && rect.bottom > 0 && rect.top < window.innerHeight;
    });
  }

  window.ynlRefreshVisiblePolls = () => visiblePolls().forEach(poll => refresh(poll));
  let debateGeneration = 0;
  window.ynlRenderDebates = async () => {
    const generation = ++debateGeneration;
    const list = document.getElementById('communityPostsList');
    const status = document.getElementById('debateStatus');
    const polls = [...document.querySelectorAll('#storiesFeedView .controversial-take-poll:not([hidden])')]
      .sort((a, b) => Number(a.closest('.compact-card').dataset.originalIndex) -
                      Number(b.closest('.compact-card').dataset.originalIndex)).slice(0, 24);
    let filter = document.getElementById('ynlDebateOrder');
    if (!filter) {
      const label = document.createElement('label');
      label.className = 'ynl-debate-order';
      label.textContent = 'Sort polls ';
      filter = document.createElement('select');
      filter.id = 'ynlDebateOrder';
      for (const [value, title] of [['recent', 'Latest'], ['popular', 'Most voted'], ['open', 'Unanswered by you']]) {
        const option = document.createElement('option');
        option.value = value;
        option.textContent = title;
        filter.append(option);
      }
      filter.addEventListener('change', window.ynlRenderDebates);
      label.append(filter);
      status.before(label);
    }

    function display() {
      let ranked = polls.slice();
      if (filter.value === 'open') ranked = ranked.filter(poll => !saved[pollKey(poll)]);
      if (filter.value === 'popular') ranked.sort((a, b) =>
        (snapshots.get(pollKey(b))?.total || 0) - (snapshots.get(pollKey(a))?.total || 0));
      list.replaceChildren();
      for (const poll of ranked) {
        const story = poll.closest('.compact-card');
        const row = document.createElement('li');
        row.className = 'ynl-debate-card';
        const source = document.createElement('p');
        source.textContent = story.dataset.category + ' · ' + story.dataset.source;
        const button = document.createElement('button');
        button.type = 'button';
        button.className = 'ynl-story-link';
        button.textContent = story.querySelector('.story-title').textContent.trim();
        button.addEventListener('click', () => window.jumpToStoryCard(poll.dataset.storyId));
        const copy = poll.cloneNode(true);
        copy.removeAttribute('id');
        for (const element of copy.querySelectorAll('[id]')) element.removeAttribute('id');
        render(copy, pollKey(copy), snapshots.get(pollKey(copy)), snapshots.has(pollKey(copy)) ? '' : 'Loading community results…');
        row.append(source, button, copy);
        list.append(row);
      }
      status.textContent = ranked.length ? ranked.length + ' questions. Vote here or open the story for its lenses.' :
        filter.value === 'open' ? 'You’ve answered every poll in this edition.' : 'No polls in this edition yet.';
    }
    display();
    await Promise.all([...list.querySelectorAll('.controversial-take-poll')].map(poll => refresh(poll)));
    if (generation === debateGeneration && filter.value === 'popular' &&
        !list.querySelector(':focus')) display();
  };
  document.addEventListener('DOMContentLoaded', () => observe(document));
})();
