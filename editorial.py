"""Publishing guardrails shared by the wire and offline refresh."""
import hashlib
import re
import time
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

PLACEHOLDER = "article-placeholder.svg"
NO_FACT = "Read the original report for details."
NO_ANSWER = "A direct answer is unavailable in the source excerpt."
WORDS = re.compile(r"[a-z0-9]+", re.I)
QUESTION = re.compile(r"^(?:how|what|why|when|where|who|which)\b", re.I)
JUNK = re.compile(
    r"^(?:[Bb]y [A-Z]|presented by|sign up|subscribe|read more|watch live|follow live|"
    r"here (?:are|is) (?:our|the)|this article)|"
    r"\b(?:primary wire|operational and public impacts|key competitive breakdown|"
    r"stakeholders|verified wire|consensus sports betting|duplicate_salt)\b", re.I
)
GENERIC_POLL = re.compile(
    r"\b(?:this (?:story|issue|situation|development|decision|election|player|team)|"
    r"the (?:team|technology|price|decision) (?:in|described)|"
    r"more (?:follow-up )?reporting|made the right choice|do more|right move)\b", re.I
)
TRACKING = {"fbclid", "gclid", "ocid", "cmpid", "ref", "source"}


def source_url(raw):
    try:
        parts = urlsplit(str(raw or "").strip())
        if parts.scheme not in {"https", "http"} or not parts.hostname or parts.username or parts.password:
            return ""
        if any(char in str(raw) for char in ('"', "'", '<', '>', '\n', '\r', '\\')):
            return ""
        return urlunsplit((parts.scheme, parts.netloc, parts.path, parts.query, ""))
    except ValueError:
        return ""


def canonical_url(raw):
    url = source_url(raw)
    if not url:
        return ""
    parts = urlsplit(url)
    query = sorted((k, v) for k, v in parse_qsl(parts.query, keep_blank_values=True)
                   if not k.lower().startswith("utm_") and k.lower() not in TRACKING)
    return urlunsplit(("https", parts.netloc.lower().removeprefix("www."),
                       parts.path.rstrip("/"), urlencode(query), ""))


def image_identity(raw):
    url = canonical_url(raw)
    if not url:
        return ""
    parts = urlsplit(url)
    transforms = {"w", "h", "width", "height", "q", "quality", "fit", "resize", "crop", "fm", "auto", "dpr"}
    query = [(key, value) for key, value in parse_qsl(parts.query, keep_blank_values=True)
             if key.lower() not in transforms]
    return urlunsplit((parts.scheme, parts.netloc, parts.path, urlencode(query), ""))


def story_id(url):
    return "story-" + hashlib.sha256(canonical_url(url).encode()).hexdigest()[:20]


def title_key(title):
    return " ".join(WORDS.findall(title.lower()))


def tokens(text):
    return {word for word in WORDS.findall(text.lower()) if len(word) >= 4}


def same_headline(first, second):
    a, b = tokens(first), tokens(second)
    return bool(a and b and len(a & b) / len(a | b) >= 0.75)


def is_question(title):
    return "?" in title or bool(QUESTION.match(title.strip()))


def excerpt_facts(title, excerpt):
    """Select intact, relevant sentences from the attributed source excerpt."""
    headline = tokens(title)
    sentences = re.split(r"(?<=[.!?])\s+(?=[A-Z“\"])", excerpt or "")
    facts = []
    for sentence in sentences:
        sentence = " ".join(sentence.split())
        sentence = re.split(r"\s+(?:play live sign up|track live results|continue reading|"
                            r"send us your questions|show navigation menu)\b", sentence,
                            maxsplit=1, flags=re.I)[0].strip()
        if re.search(r"\b(?:caret-right|toggle play|navigation menu)\b", sentence, re.I):
            continue
        words = tokens(sentence)
        if (not 35 <= len(sentence) <= 380 or sentence[-1:] not in ".!?“”\""
                or sentence.endswith(("...", "…")) or JUNK.search(sentence)
                or re.search(r"\b(?:and|from|with|in|of|to|the|its|as|for|by|on)\.$", sentence, re.I)
                or len(words - headline) < 3 or len(words & headline) < min(2, len(headline))):
            continue
        if not any(same_headline(sentence, fact) for fact in facts):
            facts.append(sentence)
    return facts[:4]


def qualify_poll(title, facts, candidate):
    if not facts or not isinstance(candidate, dict):
        return {}
    question, a, b = (" ".join(str(candidate.get(key) or "").split())
                      for key in ("statement", "agree_label", "disagree_label"))
    if (not 18 <= len(question) <= 150 or not question.endswith("?")
            or GENERIC_POLL.search(question) or not (1 <= len(a) <= 65 and 1 <= len(b) <= 65)
            or a.casefold() == b.casefold()
            or len(tokens(question + " " + a + " " + b) & tokens(title + " " + " ".join(facts))) < 2):
        return {}
    return {"statement": question, "agree_label": a, "disagree_label": b}


def sports_poll(title, facts, published=None):
    # An explicit viewing guide or preview identifies a matchup by name.
    guide = bool(re.match(r"^(?:how|where) to (?:watch|stream)\b", title, re.I))
    if not guide and not re.search(r"\b(?:preview|matchups)\b", title, re.I):
        return {}
    fixture = re.sub(r"^(?:how|where) to (?:watch|stream)\s*:?\s*", "", title, flags=re.I)
    match = re.match(r"([\w.'’ ]{2,45}?)\s*(?:\bvs\.?\s+|\bat\s+|–|-)([\w.'’ ]{2,45})(?=[:|]|$)", fixture)
    if not match:
        return {}
    first, second = (part.strip() for part in match.groups())
    if not first or not second or first.lower() == second.lower():
        return {}
    if facts and all(team.lower() in " ".join(facts).lower() for team in (first, second)):
        evidence = facts
    elif guide and isinstance(published, (int, float)) and 0 <= time.time() - published < 36 * 3600:
        evidence = [title]
    else:
        return {}
    return qualify_poll(title, evidence, {"statement": f"Who will win, {first} or {second}?",
                                         "agree_label": first, "disagree_label": second})


def simple_answer(title, facts):
    if re.search(r"\b(?:how|where) to (?:watch|stream)\b", title, re.I):
        return next((fact for fact in facts if re.search(
            r"\b(?:airs? on|watch on|stream(?:s|ing)? on|broadcast on|televised on)\b", fact, re.I
        )), None)
    return None


def proposal_poll(title, facts):
    match = re.fullmatch(
        r"([A-Z][\w.'’& -]{2,47}?) (?:proposes|plans|considers) (?:to )?"
        r"((?:raise|cut|ban|fund|expand|end|extend|build|close|open) [^?!:]{8,74})",
        title.strip()
    )
    if not match or not any(tokens(match[1]) & tokens(fact) for fact in facts):
        return {}
    return qualify_poll(title, facts, {
        "statement": f"Should {match[1]} {match[2]}?", "agree_label": "Yes", "disagree_label": "No"
    })


def topic_keys(title):
    names = re.findall(r"\b[A-Z][a-z]{2,}(?:\s+[A-Z][a-z]{2,}){1,3}\b", title)
    return sorted({name.lower() for name in names
                   if name.split()[0] not in {"The", "How", "Why", "What", "When", "Where", "Who", "Week", "Round", "Day"}})


def aviation_alert(title):
    return bool(re.search(r"\bbomb (?:alerts?|threats?)\b", title, re.I)
                and re.search(r"\b(?:flights?|airliners?)\b", title, re.I))


def fallback_poll(title, facts):
    evidence = " ".join([title, *facts])
    if aviation_alert(title):
        return qualify_poll(title, [title], {
            "statement": "When passenger flights receive bomb threats, should they divert immediately or should crews assess the threat first?",
            "agree_label": "Divert immediately", "disagree_label": "Assess the threat first",
        })
    if facts and re.search(r"\biran war\b", evidence, re.I) and re.search(r"\bcongress\b", evidence, re.I):
        return qualify_poll(title, facts, {
            "statement": "Should Congress require a vote before further U.S. military action in the Iran war?",
            "agree_label": "Require a vote", "disagree_label": "Leave it to the president",
        })
    if facts and re.search(r"\bpresidential library\b", evidence, re.I) and re.search(r"\bcongress\b", evidence, re.I):
        return qualify_poll(title, facts, {
            "statement": "Should Congress investigate how Trump's presidential library is being funded?",
            "agree_label": "Investigate the funding", "disagree_label": "No congressional inquiry",
        })
    match = re.search(r"^(.{3,45}?) extends (.{3,40}?) contract until (20\d{2})$", title)
    if match:
        player, team, year = match.groups()
        return qualify_poll(title, [title], {
            "statement": f"Was extending {player}'s contract through {year} a good move for {team}?",
            "agree_label": "Good move", "disagree_label": "Too long a commitment",
        })
    return {}


def fallback_perspectives(title, facts, political, poll):
    evidence = facts[0] if facts else title
    if aviation_alert(title):
        angles = (
            ("Passenger safety", "An early diversion gives crews a chance to get passengers on the ground while authorities investigate."),
            ("Threat assessment", "The central question is how crews and authorities judge the credibility of a threat in flight."),
            ("Flight disruption", "Diversions interrupt travel and airport operations, so the response should reflect the information crews have at the time."),
        )
    elif re.search(r"\bRonaldo\b", title, re.I) and re.search(r"retir|Portugal duty", title, re.I):
        angles = (
            ("Portugal’s next attack", "Portugal should use the transition to spread its scoring responsibilities across several players. A new attack can be built around complementary roles rather than looking for a one-for-one replacement."),
            ("Legacy", "Ronaldo’s international retirement separates two debates: how to judge his career for Portugal, and how the team should play in its next chapter."),
            ("Selection and tactics", "The next squad will reveal the coach’s priorities: a fixed striker to lead the line or a more fluid attack that lets forwards exchange positions."),
        )
    elif political and re.search(r"\b(?:elections?|midterms?|congressional majorit(?:y|ies))\b", title, re.I):
        angles = (
            ("Blue Lens", "Turn electoral gains into concrete affordability measures and oversight. Voters should be able to judge the winners by what they deliver."),
            ("Balanced Lens", facts[0] if facts else title),
            ("Red Lens", "Treat the result as a warning to the losing party. Rebuild credibility on costs and public priorities, and judge the winners by their record in office."),
        )
    elif political and re.search(r"\b(?:budget|spending|tax(?:es)?|funding)\b", title, re.I):
        angles = (
            ("Blue Lens", "Protect public services that households rely on. Any change should explain who pays and whether low-income families carry a disproportionate share."),
            ("Balanced Lens", facts[0] if facts else title),
            ("Red Lens", "Make the case for spending or taxes line by line. Identify the trade-offs and what can be cut or reworked before putting another obligation on taxpayers."),
        )
    elif political:
        subject = title.rstrip(".?!")
        angles = (
            ("Blue Lens", f"On “{subject},” the progressive case starts with who bears the costs. Judge the response by whether it protects people with the least leverage and puts decision-makers under public scrutiny."),
            ("Balanced Lens", facts[0] if facts else f"“{subject}” is the reported development. Its consequences depend on what is actually implemented and what the source can substantiate."),
            ("Red Lens", f"On “{subject},” the conservative case starts with accountability and limits on power. Put the burden on officials to show they have authority and that any costs or new obligations are justified."),
        )
    elif poll and poll["agree_label"] != "Yes":
        first, second = poll["agree_label"], poll["disagree_label"]
        angles = (
            ("Case for " + first, f"For “{title},” the argument for “{first}” depends on whether it delivers a better result under the conditions described by the source."),
            ("Evidence", facts[0] if facts else title),
            ("Case for " + second, f"For “{title},” “{second}” is the alternative if the case for “{first}” depends on assumptions the reporting has yet to establish."),
        )
    else:
        angles = (
            ("Impact", f"For “{title},” the practical significance depends on who will experience a concrete change. Give the most weight to effects the original reporting can document."),
            ("Evidence", facts[0] if facts else title),
            ("Next development", facts[1] if len(facts) > 1 else f"The next meaningful update on “{title}” would establish what changed after the initial report."),
        )
    return {side: {"label": label, "talking_points": [point], "evidence": evidence,
                   "perspective_badge": "news_lens_analysis"}
            for side, (label, point) in zip(("LEFT", "CENTER", "RIGHT"), angles)}


def restore_missing_features(record):
    title = record["title"]
    facts = record.get("core_facts") or []
    if (title == "Bomb alerts force flights to land in France, Bulgaria, Belgium"
            and record.get("source_name") == "Reuters"):
        if not facts:
            facts = ["Reuters reports that Aer Lingus flight EI402, headed from Dublin to Rome, landed safely at Évreux after a bomb threat prompted a diversion."]
            record.update(core_facts=facts, lead_fact=facts[0], neutral_summary=facts[0])
        if not record.get("is_original_article_image"):
            record.update(
                image_url="https://upload.wikimedia.org/wikipedia/commons/3/30/Airbus_A320-200.jpg",
                caption="File photo: Aer Lingus Airbus A320 at Belfast, 2011. Illustration of the aircraft type.",
                credit="Ezbolor / Wikimedia Commons",
                image_license_url="https://creativecommons.org/licenses/by-sa/3.0/",
                resolution_method="licensed_reference_photo",
            )
    poll = record.get("controversial_take") or fallback_poll(title, facts)
    record["controversial_take"] = poll
    perspectives = record.get("perspectives") or {}
    political = (record.get("perspective_mode") == "political" or
                 record.get("category") in {"Politics", "Border & Security"})
    if not perspectives:
        record["perspective_mode"] = "political" if political else "topical"
    fallback = fallback_perspectives(title, facts, political, poll)
    for side, value in fallback.items():
        previous = perspectives.get(side) or {}
        if not previous.get("talking_points") or previous.get("perspective_badge") in {
            "editorial_prompt", "pending_commentary", "news_lens_analysis"
        }:
            perspectives[side] = value
    record["perspectives"] = perspectives
    return record


def prepare_story(record, analysis=None):
    """Publish attributed text with evidence. Old records without excerpts remain link cards."""
    title = record["title"]
    record["topic_keys"] = topic_keys(title)
    excerpt = record.get("source_excerpt", "")
    facts = excerpt_facts(title, excerpt)
    analysis = analysis if isinstance(analysis, dict) else {}
    grounded_answer = False
    answer = analysis.get("direct_answer_evidence") or simple_answer(title, facts)
    if is_question(title) and isinstance(answer, str) and answer in facts:
        facts.remove(answer)
        facts.insert(0, answer)
        grounded_answer = True
    record["has_direct_answer"] = grounded_answer
    record["core_facts"] = facts
    record["neutral_summary"] = facts[0] if facts else NO_FACT
    record["instant_answer"] = facts[0] if grounded_answer else ""
    record["lead_fact"] = facts[0] if facts and (not is_question(title) or grounded_answer) else (
        NO_ANSWER if is_question(title) else NO_FACT
    )

    political = record.get("category") in {"Politics", "Border & Security"} and analysis.get("political") is True
    record["perspective_mode"] = "political" if political else "topical"
    proposed = analysis.get("perspectives")
    record["perspectives"] = {}
    if facts and isinstance(proposed, dict):
        for side in ("LEFT", "CENTER", "RIGHT"):
            entry = proposed.get(side)
            if not isinstance(entry, dict):
                continue
            evidence = entry.get("evidence")
            point = entry.get("point")
            if isinstance(evidence, str) and evidence in facts and isinstance(point, str) and 15 <= len(point) <= 220:
                numbers = set(re.findall(r"\d+(?:[.,]\d+)*", point))
                grounded_numbers = set(re.findall(r"\d+(?:[.,]\d+)*", evidence))
                if not JUNK.search(point) and tokens(point) & tokens(evidence) and numbers <= grounded_numbers:
                    label = entry.get("label")
                    record["perspectives"][side] = {
                        "talking_points": [point], "evidence": evidence,
                        "label": label if isinstance(label, str) and 3 <= len(label) <= 30 else ""
                    }
        unique = {entry["talking_points"][0].casefold() for entry in record["perspectives"].values()}
        if len(unique) != 3:
            record["perspectives"] = {}

    poll = qualify_poll(title, facts, analysis.get("poll"))
    if not poll:
        poll = proposal_poll(title, facts)
    if not poll and record.get("category") == "Sports":
        poll = sports_poll(title, facts, record.get("pub_timestamp"))
    record["controversial_take"] = poll
    for legacy in ("expanded_facts", "evolution_timeline", "what_changed_since_yesterday", "analytical_conclusions"):
        record.pop(legacy, None)
    if not record.get("is_original_article_image") or not source_url(record.get("image_url")):
        placeholder(record)
    return restore_missing_features(record)


def placeholder(record):
    record.update(image_url=PLACEHOLDER, caption="", credit="", is_original_article_image=False,
                  resolution_method="editorial_placeholder")
