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
  window.ynlRenderDebates = async () => {
    const list = document.getElementById('communityPostsList');
    const status = document.getElementById('debateStatus');
    const polls = [...document.querySelectorAll('.controversial-take-poll:not([hidden])')].slice(0, 12);
    status.textContent = 'Checking votes on recent polls…';
    await Promise.all(polls.map(poll => refresh(poll)));
    const ranked = polls.map(poll => ({ poll, result: snapshots.get(pollKey(poll)) }))
      .filter(item => item.result?.total > 0)
      .sort((first, second) => second.result.total - first.result.total);
    list.replaceChildren();
    for (const {poll, result} of ranked.slice(0, 5)) {
      const row = document.createElement('li');
      const button = document.createElement('button');
      button.type = 'button';
      button.className = 'btn-action-small';
      button.textContent = poll.querySelector('.take-statement-text').textContent + ' · ' +
        result.total.toLocaleString() + (result.total === 1 ? ' vote' : ' votes');
      button.addEventListener('click', () => window.jumpToStoryCard(poll.dataset.storyId));
      row.append(button);
      list.append(row);
    }
    status.textContent = ranked.length ? 'Most votes among the latest polls.' :
      polls.some(poll => !snapshots.has(pollKey(poll))) ? 'Some community totals are unavailable.' :
      'No votes on recent polls yet.';
  };
  document.addEventListener('DOMContentLoaded', () => observe(document));
})();
