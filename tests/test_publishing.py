from contextlib import redirect_stdout
import io
import json
from pathlib import Path
import tempfile
import time
import unittest
from unittest.mock import patch

import editorial
import engine
import publish_wire
import reader_sources

ROOT = Path(__file__).resolve().parents[1]
TITLE = "How to watch Buccaneers vs. Bears: Week Nine preview"
FACT = "The Buccaneers play the Bears on Sunday, and the game airs on CBS."
URL = "https://sports.example.com/bucs-bears-preview"


def feed_item(**overrides):
    item = {
        "title": TITLE, "link": URL, "description": FACT, "pub_timestamp": int(time.time()) - 500,
        "source_name": "Fixture Sports", "source": "Fixture Sports • 8 minutes ago",
        "category": "Sports", "metro": "", "sub_category": "",
        "scraped_image": {"url": "https://images.example.com/bucs-bears.jpg",
                          "is_original_article_image": True},
    }
    return item | overrides


class PublishingTest(unittest.TestCase):
    def test_source_answer_and_named_sports_poll(self):
        record = editorial.prepare_story({"title": TITLE, "category": "Sports", "source_excerpt": FACT})
        self.assertEqual(FACT, record["lead_fact"])
        self.assertTrue(record["has_direct_answer"])
        self.assertEqual(record["perspective_mode"], "topical")
        self.assertEqual(record["controversial_take"], {
            "statement": "Who will win, Buccaneers or Bears?",
            "agree_label": "Buccaneers", "disagree_label": "Bears"
        })

    def test_recent_source_headline_can_ground_matchup_poll_without_viewing_answer(self):
        record = editorial.prepare_story({
            "title": "How to Watch: Buccaneers at Bears | Week 9 2026",
            "category": "Sports", "source_excerpt": "", "pub_timestamp": int(time.time())
        })
        self.assertFalse(record["has_direct_answer"])
        self.assertEqual(record["controversial_take"]["statement"], "Who will win, Buccaneers or Bears?")

    def test_discards_clipped_or_unrelated_text_and_generic_poll(self):
        record = editorial.prepare_story({
            "title": TITLE, "category": "Sports",
            "source_excerpt": "The Buccaneers and Bears are scheduled to meet with. The dollar rose overnight after investors sought safety."
        }, {"poll": {"statement": "Should the team in this story do more?", "agree_label": "Yes", "disagree_label": "No"}})
        self.assertEqual(record["core_facts"], [])
        self.assertFalse(record["has_direct_answer"])
        self.assertEqual(record["controversial_take"], {})
        self.assertEqual(record["image_url"], editorial.PLACEHOLDER)

    def test_proposal_names_decision(self):
        title = "Tampa City Council proposes to build a public boat ramp"
        fact = "Tampa City Council set aside land for a public boat ramp at the park's southern end."
        poll = editorial.proposal_poll(title, [fact])
        self.assertEqual(poll["statement"], "Should Tampa City Council build a public boat ramp?")

    def test_source_matching_deduplication_and_timestamp(self):
        now = int(time.time())
        items = [feed_item(), feed_item(link=URL + "?utm_source=rss"),
                 feed_item(link="https://other.example.com/preview", pub_timestamp=now - 600),
                 feed_item(link="https://example.com/old", title="Another headline", pub_timestamp=now - 300000),
                 feed_item(link="javascript:alert(1)", title="Another headline")]
        with patch.object(engine, "scrape_article_lead_image_and_meta", return_value={}), patch.object(publish_wire, "analyze", return_value={}):
            rows, count = publish_wire.collect_stories(engine, items, [], now)
        self.assertEqual((len(rows), count), (1, 1))
        self.assertEqual(rows[0]["pub_timestamp"], items[0]["pub_timestamp"])
        self.assertEqual(rows[0]["id"], editorial.story_id(URL))

    def test_definitive_publisher_404_skips_article(self):
        with patch.object(engine, "scrape_article_lead_image_and_meta", return_value={"unavailable": True}), \
             redirect_stdout(io.StringIO()):
            rows, count = publish_wire.collect_stories(engine, [feed_item()], [], int(time.time()))
        self.assertEqual((rows, count), ([], 0))

    def test_original_image_reuse_falls_back_for_both_cards(self):
        rows = [{"image_url": f"https://example.com/photo.jpg?utm_source=rss&w={i + 300}",
                 "is_original_article_image": True} for i in range(2)]
        publish_wire.dedupe_images(rows)
        self.assertTrue(all(row["image_url"] == editorial.PLACEHOLDER for row in rows))

    def test_pipeline_writes_matching_outputs_and_is_repeatable(self):
        with tempfile.TemporaryDirectory() as directory:
            html = Path(directory, "index.html")
            data = Path(directory, "stories.json")
            html.write_text((ROOT / "index.html").read_text(), encoding="utf-8")
            data.write_text("[]", encoding="utf-8")
            with patch.object(engine, "HTML_FILE", str(html)), patch.object(engine, "DATA_FILE", str(data)), \
                 patch.object(engine, "fetch_all_feeds_concurrently", return_value=[feed_item()]), \
                 patch.object(engine, "scrape_article_lead_image_and_meta", return_value={}), \
                 patch.object(publish_wire, "analyze", return_value={}), \
                 patch.object(reader_sources, "fetch_events", return_value=[]), redirect_stdout(io.StringIO()):
                publish_wire.run(engine)
                output = html.read_bytes(), data.read_bytes()
                publish_wire.run(engine)
                self.assertEqual(output, (html.read_bytes(), data.read_bytes()))
                row = json.loads(data.read_text())[0]
                self.assertIn(f'data-edition="{row["edition"]}"', html.read_text())
                self.assertIn('Who will win, Buccaneers or Bears?', html.read_text())
                with patch.object(engine, "fetch_all_feeds_concurrently", return_value=[]):
                    with self.assertRaisesRegex(RuntimeError, "No RSS items"):
                        publish_wire.run(engine)
                self.assertEqual(output, (html.read_bytes(), data.read_bytes()))

    def test_renderer_escapes_untrusted_text(self):
        story = editorial.prepare_story({"id": "story-example", "title": 'A <script>alert("x")</script> headline',
                                         "source_name": '" onload="alert(1)', "article_url": "javascript:alert(1)"})
        rendered = engine.prerender_cards_html([story])
        self.assertNotIn("<script>", rendered)
        self.assertNotIn('href="javascript:', rendered)
        self.assertIn("&lt;script&gt;", rendered)

    def test_aviation_story_remains_interactive_without_model(self):
        story = editorial.prepare_story({
            "id": "story-flight-alert", "title": "Bomb alerts force flights to land in France, Bulgaria, Belgium",
            "source_name": "Reuters", "category": "World News",
        })
        self.assertIn("EI402", story["lead_fact"])
        self.assertIn("Airbus_A320", story["image_url"])
        self.assertIn("Assess the threat first", story["controversial_take"]["disagree_label"])
        self.assertEqual("topical", story["perspective_mode"])
        page = engine.prerender_cards_html([story])
        self.assertIn("Passenger safety", page)
        self.assertIn("File photo", page)
        self.assertIn("CC BY-SA 3.0", page)

    def test_missing_image_has_no_logo_hero(self):
        story = editorial.prepare_story({"id": "story-no-image", "title": "An article without a usable photo"})
        page = engine.prerender_cards_html([story])
        self.assertNotIn("hero-image-wrap", page)
        self.assertIn("Editorial lens", page)

    def test_city_calendar_listing_has_date_and_real_source(self):
        from datetime import datetime
        now = datetime.fromisoformat("2026-11-05T08:00:00-05:00").timestamp()
        markup = ('<span class="date-part-F">November</span> <span class="date-part-j">6</span>'
                  '<div class="views-field-nothing-2"><span class="field-content">7:00 - 9:30pm'
                  '<div class="calendar-item" id="event-title-197206"><div class="fw-bold">'
                  '<a href="/events/richards-run-life/197206">Richard&#039;s Run for Life</a>')
        [event] = reader_sources.tampa_events(markup, now)
        self.assertEqual(event["event_date"], "2026-11-06")
        self.assertEqual(event["sub_category"], "events")
        self.assertIn("7:00", event["lead_fact"])
        self.assertIn("https://www.tampa.gov/events/", event["article_url"])

    def test_blue_wave_lenses_link_to_documented_views(self):
        row = {"title": "Progressives hail blue wave victories in US midterm elections", "article_url": URL}
        reader_sources.enrich_lenses([row], [])
        right = row["perspectives"]["RIGHT"]
        self.assertIn("Jim Geraghty", right["source_attribution"])
        self.assertIn("nationalreview.com", right["source_url"])
        self.assertIn("change course", right["talking_points"][0])

    def test_old_unverified_records_are_not_published(self):
        self.assertEqual(publish_wire.refresh_existing(
            [{"title": TITLE, "article_url": URL, "pub_timestamp": int(time.time())}], int(time.time()), False
        ), [])
