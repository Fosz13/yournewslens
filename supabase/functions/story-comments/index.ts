const origins = new Set(["https://yournewslens.com", "https://www.yournewslens.com"]);
const profanity = /\b(?:fuck\w*|shit\w*|bitch\w*|cunt\w*|motherfuck\w*)\b/i;

Deno.serve(async (request) => {
  const origin = request.headers.get("origin") ?? "";
  const headers = {
    "Access-Control-Allow-Origin": origins.has(origin) ? origin : "https://yournewslens.com",
    "Access-Control-Allow-Headers": "apikey, content-type",
    "Access-Control-Allow-Methods": "POST, OPTIONS",
    "Content-Type": "application/json",
    "Vary": "Origin",
  };
  const reply = (status: number, message: string) =>
    new Response(JSON.stringify({ message }), { status, headers });

  if (!origins.has(origin)) return reply(403, "Origin not supported.");
  if (request.method === "OPTIONS") return new Response(null, { status: 204, headers });
  if (request.method !== "POST") return reply(405, "Use POST.");

  const key = Deno.env.get("OPENAI_API_KEY");
  const serviceKey = Deno.env.get("SUPABASE_SERVICE_ROLE_KEY");
  const url = Deno.env.get("SUPABASE_URL");
  if (!key || !serviceKey || !url) {
    console.error("Missing comment configuration:", !key ? "OPENAI_API_KEY" : "", !serviceKey ? "SUPABASE_SERVICE_ROLE_KEY" : "", !url ? "SUPABASE_URL" : "");
    return reply(503, "Comment posting is temporarily unavailable.");
  }

  let submission;
  try {
    const reader = request.body?.getReader();
    if (!reader) return reply(400, "Missing comment.");
    const decoder = new TextDecoder();
    let size = 0;
    let input = "";
    while (true) {
      const { done, value } = await reader.read();
      if (done) break;
      size += value.byteLength;
      if (size > 4096) {
        await reader.cancel();
        return reply(413, "Comment is too long.");
      }
      input += decoder.decode(value, { stream: true });
    }
    submission = JSON.parse(input + decoder.decode());
  } catch {
    return reply(400, "Invalid comment.");
  }
  const { id, storyId, body } = submission ?? {};
  const comment = typeof body === "string" ? body.trim() : "";
  if (typeof id !== "string" || !/^[a-f0-9]{8}-(?:[a-f0-9]{4}-){3}[a-f0-9]{12}$/i.test(id) ||
      typeof storyId !== "string" || !/^story-[a-zA-Z0-9_-]{1,100}$/.test(storyId) ||
      comment.length < 3 || comment.length > 600) {
    return reply(400, "Write a comment between 3 and 600 characters.");
  }
  const normalized = comment.normalize("NFKC").replace(/\p{Cf}/gu, "");
  if (profanity.test(normalized) || /https?:\/\/|www\.|[\w.+-]+@[\w.-]+\.[a-z]{2,}/i.test(normalized)) {
    return reply(422, "Remove explicit language, links, or email addresses and try again.");
  }

  const database = (path: string, payload: object, prefer?: string) => fetch(url + "/rest/v1/" + path, {
    method: "POST",
    headers: { apikey: serviceKey, Authorization: "Bearer " + serviceKey,
      "Content-Type": "application/json", ...(prefer ? { Prefer: prefer } : {}) },
    body: JSON.stringify(payload),
    signal: AbortSignal.timeout(6000),
  });

  try {
    const reserved = await database("rpc/reserve_story_comment", {});
    if (!reserved.ok) return reply(503, "Comment posting is temporarily unavailable.");
    if (await reserved.json() !== true) return reply(429, "Too many submissions. Try again in a minute.");
    const response = await fetch("https://api.openai.com/v1/moderations", {
      method: "POST",
      headers: { Authorization: "Bearer " + key, "Content-Type": "application/json" },
      body: JSON.stringify({ model: "omni-moderation-latest", input: normalized }),
      signal: AbortSignal.timeout(8000),
    });
    if (!response.ok) return reply(503, "Comment filtering is temporarily unavailable.");
    const result = (await response.json())?.results?.[0];
    if (result?.flagged === true) return reply(422, "This comment did not pass the community filter.");
    if (result?.flagged !== false) return reply(503, "Comment filtering is temporarily unavailable.");
    const saved = await database("story_comments?on_conflict=id",
      { id, story_id: storyId, body: comment }, "resolution=ignore-duplicates,return=minimal");
    if (!saved.ok) return reply(503, "Comment posting is temporarily unavailable.");
    return reply(200, "Comment posted.");
  } catch {
    return reply(503, "Comment posting is temporarily unavailable.");
  }
});
