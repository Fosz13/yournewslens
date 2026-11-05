(function () {
  'use strict';
  const project = 'https://vswxehmxdbtdatnlovsl.supabase.co';
  const apikey = 'sb_publishable_OFiISa3vk9WNRLbIp8xuIg_2emzLYRD';

  async function loadComments(storyId, list, status) {
    const query = new URLSearchParams({
      story_id: 'eq.' + storyId, select: 'body,created_at', order: 'created_at.desc,id.desc', limit: '30'
    });
    try {
      const response = await fetch(project + '/rest/v1/story_comments?' + query, {
        headers: { apikey }, cache: 'no-store', signal: AbortSignal.timeout(8000)
      });
      if (!response.ok) throw new Error();
      const rows = await response.json();
      list.replaceChildren(...rows.map(row => {
        const item = document.createElement('li');
        item.textContent = row.body;
        return item;
      }));
      status.textContent = rows.length ? 'Showing the latest comments.' : 'Be the first to comment.';
    } catch {
      status.textContent = 'Comments are temporarily unavailable.';
    }
  }

  function addDiscussButtons() {
    for (const card of document.querySelectorAll('#storiesFeedView article.compact-card')) {
      const anchor = card.querySelector('.fact-preview-strip');
      if (!anchor || card.querySelector('.ynl-discuss')) continue;
      const panel = document.createElement('details');
      panel.className = 'ynl-story-comments';
      panel.innerHTML = '<summary>Discuss</summary><p role="status"></p><ul></ul>' +
        '<form><label>Your comment<textarea name="body" required minlength="3" maxlength="600"></textarea></label>' +
        '<small>Comments are public and checked automatically before posting.</small>' +
        '<button type="submit">Post comment</button><p role="status"></p></form>';
      panel.querySelector('summary').className = 'ynl-discuss btn-discuss-small';
      anchor.after(panel);
      const list = panel.querySelector('ul');
      const status = panel.querySelector('p');
      panel.addEventListener('toggle', () => {
        if (panel.open) loadComments(card.id, list, status);
      });
      const form = panel.querySelector('form');
      const input = form.elements.body;
      const submit = form.querySelector('button');
      const feedback = form.querySelector('[role="status"]');
      let draft;
      form.addEventListener('submit', async event => {
        event.preventDefault();
        if (submit.disabled) return;
        const body = input.value.trim();
        if (body.length < 3) {
          feedback.textContent = 'Write at least 3 characters.';
          return;
        }
        if (draft?.body !== body) draft = { id: crypto.randomUUID(), storyId: card.id, body };
        submit.disabled = true;
        feedback.textContent = 'Checking your comment…';
        try {
          const response = await fetch(project + '/functions/v1/story-comments', {
            method: 'POST', headers: { apikey, 'Content-Type': 'application/json' },
            body: JSON.stringify(draft), signal: AbortSignal.timeout(23000)
          });
          const result = await response.json();
          feedback.textContent = result.message || 'Could not post your comment.';
          if (response.ok) {
            form.reset();
            draft = undefined;
            await loadComments(card.id, list, status);
          }
        } catch {
          feedback.textContent = 'Could not confirm posting. Try again to retry the same comment.';
        } finally {
          submit.disabled = false;
        }
      });
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', addDiscussButtons, { once: true });
  } else {
    addDiscussButtons();
  }
  document.addEventListener('ynl:edition', addDiscussButtons);
})();
