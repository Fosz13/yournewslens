const assert = require('node:assert/strict');
const fs = require('node:fs');
const test = require('node:test');
const vm = require('node:vm');

function setup(options = {}) {
  const nodes = new Map();
  const newNode = (textContent = '') => ({ textContent, style: {}, classList: { toggle() {} } });
  for (const name of ['take-consensus-track', 'take-fill-agree', 'take-fill-disagree', 'take-total-votes', 'take-voted-msg']) {
    nodes.set('.' + name, newNode());
  }
  nodes.set('.take-statement-text', newNode('Who will win, Buccaneers or Bears?'));
  const buttons = ['agree', 'disagree'].map((choice, index) => {
    const label = newNode(['Buccaneers', 'Bears'][index]);
    const percent = newNode();
    return Object.assign(newNode(), {
      dataset: { choice }, attributes: {},
      setAttribute(key, value) { this.attributes[key] = value; },
      querySelector(selector) { return selector === '.vote-label' ? label : percent; },
      closest(selector) { return selector === '.btn-take-vote' ? this : poll; }
    });
  });
  const poll = {
    dataset: { storyId: 'story-fixture' }, classList: { toggle() {} },
    querySelector: selector => nodes.get(selector),
    querySelectorAll: selector => selector === '.vote-label' ? buttons.map(button => button.querySelector(selector)) : buttons
  };
  const listeners = {};
  const requests = [];
  const storage = options.storage || new Map();
  let records = options.records || [];
  let writes = 0;
  const window = { crypto: { randomUUID: () => 'test-visitor' } };
  vm.runInNewContext(fs.readFileSync('polling.js', 'utf8'), {
    window, crypto: window.crypto, AbortController, setTimeout, clearTimeout,
    localStorage: { getItem: key => storage.get(key), setItem: (key, value) => storage.set(key, value) },
    document: {
      addEventListener: (name, listener) => { listeners[name] = listener; },
      querySelectorAll: () => [poll], getElementById: () => null
    },
    fetch: async (url, request) => {
      const body = JSON.parse(request.body);
      requests.push({ url, body });
      if (url.endsWith('/poll_votes')) {
        writes++;
        if (options.writeError) return { ok: false, status: options.writeError.status, json: async () => options.writeError };
        records = [{ choice_id: body.choice_id, vote_count: 1 }];
        return { ok: true, status: 201 };
      }
      if (options.failReadAfterWrite && writes) return { ok: false, status: 503, json: async () => ({}) };
      return { ok: true, json: async () => records };
    }
  });
  listeners.DOMContentLoaded();
  return { nodes, buttons, requests, storage,
    click: (index = 0) => listeners.click({ target: { closest: () => buttons[index] } }) };
}

const settle = () => new Promise(resolve => setImmediate(resolve));
const status = page => page.nodes.get('.take-voted-msg').textContent;
const count = page => page.nodes.get('.take-total-votes').textContent;

test('same versioned poll key for reads and writes, rapid taps submit once, choice persists', async () => {
  const page = setup();
  await settle();
  assert.equal(status(page), 'No community votes yet.');
  assert.equal(count(page), 'Total votes: 0');
  page.click();
  page.click(1);
  await settle();
  const writes = page.requests.filter(request => request.url.endsWith('/poll_votes'));
  assert.equal(writes.length, 1);
  assert.equal(writes[0].body.story_id, page.requests[0].body.p_story_id);
  assert.equal(writes[0].body.choice_label, 'Buccaneers');
  assert.equal(status(page), '100% picked your answer.');
  assert.equal(count(page), 'Total votes: 1');
  const reopened = setup({ storage: page.storage, records: [{ choice_id: 'agree', vote_count: 1 }] });
  await settle();
  assert.equal(reopened.buttons[0].attributes['aria-pressed'], 'true');
  assert.equal(reopened.buttons[1].disabled, true);
});

test('write success followed by failed read still confirms the vote', async () => {
  const page = setup({ failReadAfterWrite: true });
  await settle();
  page.click();
  await settle();
  assert.match(status(page), /^Your vote was recorded/);
  assert.equal(count(page), '');
});

test('database uniqueness conflict shows real results without claiming a choice', async () => {
  const page = setup({ writeError: { status: 409, code: '23505' }, records: [{ choice_id: 'disagree', vote_count: 2 }] });
  await settle();
  page.click();
  await settle();
  assert.equal(count(page), 'Total votes: 2');
  assert.equal(page.buttons[0].attributes['aria-pressed'], 'false');
  assert.equal(page.buttons[0].disabled, true);
});

test('a rejected vote can be retried and malformed counts do not appear as zero', async () => {
  const page = setup({ writeError: { status: 403 }, records: [{ choice_id: 'agree' }] });
  await settle();
  assert.equal(count(page), '');
  assert.match(status(page), /unavailable/);
  page.click();
  await settle();
  assert.equal(page.buttons[0].disabled, false);
  assert.match(status(page), /try again/);
});
