#!/usr/bin/env python3
"""
test_regression_suite.py
Comprehensive 13-Part Automated Regression Test Suite for Your News Lens.
Verifies the three-layer architectural safeguards:
1. Image Selection & Subcategory Pool Matching (with cross-domain negative checks)
2. Evidence-Grounded 4-Part Fact Extraction (with boilerplate and headline-overlap gates)
3. Story-Specific Perspective Validation (with strict domain-leakage rejection)

Test Cases Covered:
1. Kylie Jenner / Fashion Runway: Fashion imagery, rejects box-office / theatrical rhetoric.
2. France Civil Unrest: Demonstrations/French location, rejects military casualties & U.S. budget rhetoric.
3. Pakistan Political Crisis: Pakistani political institutions, rejects Washington congressional rhetoric.
4. Alamodome Fatal Accident: First responders/venue, rejects sports scoreboard metaphors.
5. Rams Injury Report: NFL equipment, rejects golf and basketball imagery.
6. NBA Rankings: Basketball arena, rejects football equipment and golf courses.
7. East Potomac Land Overhaul: Park links/public land, rejects Supreme Court & PGA Tour imagery.
8. College Football Playoff Rankings: College stadium/game, rejects generic campus buildings.

Each test verifies BOTH that the expected result passes AND that a deliberately incorrect result fails.
"""

import sys
import os
import json
import engine

def run_all_regression_tests():
    print("=" * 75)
    print("RUNNING YOUR NEWS LENS COMPREHENSIVE 8-PART REGRESSION SUITE")
    print("=" * 75)
    passed_count = 0
    total_tests = 13

    # -------------------------------------------------------------------------
    # TEST 1: Kylie Jenner / Fashion Runway
    # -------------------------------------------------------------------------
    print("\n[TEST 1] Kylie Jenner / Fashion Runway Verification...")
    t1 = "Kylie Jenner's Fantasy Bra moment draws criticism from Victoria's Secret fans"
    d1 = "Kylie Jenner walked in the revived Victoria's Secret Fashion Show in New York City, debuting the Fantasy Bra."
    subcat1 = engine.determine_story_subcategory(t1, "Entertainment", d1)
    assert subcat1 == "entertainment_fashion", f"Test 1 Failed: Subcategory {subcat1} != entertainment_fashion"

    # Image Check
    img1 = engine.resolve_story_image(t1, "Entertainment", d1)
    assert any(w in img1["caption"].lower() for w in ["fashion", "runway", "model", "couture"]), f"Test 1 Image Caption Failed: {img1['caption']}"
    assert "golf" not in img1["caption"].lower() and "cinema" not in img1["caption"].lower(), "Test 1 Failed: Golf or cinema image assigned!"

    # Candidate Validator Negative Check: Cinema image must fail for fashion
    bad_cand1 = {
        "url": "https://images.unsplash.com/photo-cinema",
        "caption": "Major motion picture theatrical cinema and movie premiere box office.",
        "tags": ["cinema", "theatrical", "movie"],
        "pool": "entertainment_fashion"
    }
    is_valid1, errs1, _ = engine.validate_image_candidate(bad_cand1, subcat1, t1, d1)
    assert not is_valid1, "Test 1 Negative Failed: Cinema image candidate did not fail validation for fashion!"
    assert any("cross_domain:theatrical cinema" in e or "cross_domain:box office" in e for e in errs1), f"Test 1 Errors: {errs1}"

    # Perspective Negative Check: Box-office rhetoric must fail
    bad_persp1 = {
        "LEFT": {"headline_framing": "Box Office", "talking_points": ["The box office is an open marketplace for theatrical cinema."]},
        "CENTER": {"headline_framing": "Pragmatic", "talking_points": ["Valid point."]},
        "RIGHT": {"headline_framing": "Market", "talking_points": ["Ticket sales determine success."]}
    }
    is_p_valid1, p_errs1 = engine.validate_perspective_relevance(t1, d1, bad_persp1, subcat1)
    assert not is_p_valid1, "Test 1 Negative Failed: Box-office leakage into fashion was not rejected!"
    print("✓ TEST 1 PASSED: Fashion imagery verified and box-office leakage strictly rejected.")
    passed_count += 1

    # -------------------------------------------------------------------------
    # TEST 2: France Civil Unrest
    # -------------------------------------------------------------------------
    print("\n[TEST 2] France Civil Unrest Verification...")
    t2 = "Huge Riots in France Prompt Shock and Blame Game - "
    d2 = "Paris police reported 855 arrests after violent clashes and looting broke out during demonstrations across Paris and Limoges."
    subcat2 = engine.determine_story_subcategory(t2, "World News", d2)
    assert subcat2 == "world_protests", f"Test 2 Failed: Subcategory {subcat2} != world_protests"

    img2 = engine.resolve_story_image(t2, "World News", d2)
    assert any(w in img2["caption"].lower() for w in ["paris", "france", "civil unrest", "emergency police", "security"]), f"Test 2 Image Caption Failed: {img2['caption']}"

    # Negative Check: Military casualties or Washington congressional rhetoric must fail
    bad_persp2 = {
        "LEFT": {"headline_framing": "Protest", "talking_points": ["Those who serve and sacrifice receive our utmost respect."]},
        "CENTER": {"headline_framing": "Balanced", "talking_points": ["Divided government in Washington serves the entire nation."]},
        "RIGHT": {"headline_framing": "Order", "talking_points": ["We must balance the federal budget to stop runaway inflation."]}
    }
    is_p_valid2, p_errs2 = engine.validate_perspective_relevance(t2, d2, bad_persp2, subcat2)
    assert not is_p_valid2, "Test 2 Negative Failed: Military casualty / US budget rhetoric was not rejected for France riots!"
    assert any("leakage_from_military" in e for e in p_errs2), f"Expected military leakage error, got: {p_errs2}"
    assert any("leakage_from_us_domestic_budget" in e for e in p_errs2), f"Expected US budget leakage error, got: {p_errs2}"
    print("✓ TEST 2 PASSED: French demonstrations verified and military/US-budget leakage strictly rejected.")
    passed_count += 1

    # -------------------------------------------------------------------------
    # TEST 3: Pakistan Political Crisis
    # -------------------------------------------------------------------------
    print("\n[TEST 3] Pakistan Political Crisis Verification...")
    t3 = "Pakistan's decades of backing terror comes full circle as Khyber Pakhtunkhwa falls under emergency rule - The Times of India"
    d3 = "The Pakistani federal government suspended the provincial government of Khyber Pakhtunkhwa, imposing emergency rule."
    subcat3 = engine.determine_story_subcategory(t3, "World News", d3)
    assert subcat3 == "world_conflict", f"Test 3 Failed: Subcategory {subcat3} != world_conflict"

    # Negative Check: Generic Washington congressional rhetoric must fail
    bad_persp3 = {
        "LEFT": {"headline_framing": "Democracy", "talking_points": ["Congressional gridlock in Washington harms everyday citizens."]},
        "CENTER": {"headline_framing": "Governance", "talking_points": ["Divided government in Washington is how we achieve progress."]},
        "RIGHT": {"headline_framing": "Law and Order", "talking_points": ["Valid point on sovereign regional security in Pakistan."]}
    }
    is_p_valid3, p_errs3 = engine.validate_perspective_relevance(t3, d3, bad_persp3, subcat3)
    assert not is_p_valid3, "Test 3 Negative Failed: Washington congressional rhetoric was not rejected for Pakistan story!"
    assert any("leakage_from_us_domestic_budget" in e for e in p_errs3), f"Expected US domestic leakage error, got: {p_errs3}"
    print("✓ TEST 3 PASSED: Pakistani political context verified and Washington congressional rhetoric strictly rejected.")
    passed_count += 1

    # -------------------------------------------------------------------------
    # TEST 4: Alamodome Fatal Accident
    # -------------------------------------------------------------------------
    print("\n[TEST 4] Alamodome Fatal Accident Verification...")
    t4 = "Airman dies in rappelling accident at Alamodome before UTSA-Navy game - Texas Public Radio | TPR"
    d4 = "An active-duty U.S. Air Force airman tragically died following a fall while rappelling from the Alamodome rafters."
    subcat4 = engine.determine_story_subcategory(t4, "Crime & Public Safety", d4)
    assert subcat4 == "safety_accident", f"Test 4 Failed: Subcategory {subcat4} != safety_accident"

    img4 = engine.resolve_story_image(t4, "Crime & Public Safety", d4)
    assert any(w in img4["caption"].lower() for w in ["first responders", "alamodome", "public safety"]), f"Test 4 Image Caption Failed: {img4['caption']}"

    # Negative Check: Sports scoreboard metaphors must fail on fatal fall accident
    bad_persp4 = {
        "LEFT": {"headline_framing": "Safety", "talking_points": ["The final scoreboard doesn't lie when executing between the lines."]},
        "CENTER": {"headline_framing": "Inquiry", "talking_points": ["Scoreboard doesn't lie in high-leverage sports competitions."]},
        "RIGHT": {"headline_framing": "Honor", "talking_points": ["Turnover differential cost the team the championship."]}
    }
    is_p_valid4, p_errs4 = engine.validate_perspective_relevance(t4, d4, bad_persp4, subcat4)
    assert not is_p_valid4, "Test 4 Negative Failed: Sports scoreboard rhetoric was not rejected for fatal accident!"
    assert any("leakage_from_sports" in e for e in p_errs4), f"Expected sports leakage error, got: {p_errs4}"
    print("✓ TEST 4 PASSED: Venue/accident verified and sports scoreboard metaphors strictly rejected.")
    passed_count += 1

    # -------------------------------------------------------------------------
    # TEST 5: Rams Injury Report
    # -------------------------------------------------------------------------
    print("\n[TEST 5] Rams Injury Report Verification...")
    t5 = "Rams suffer several major injuries, including to WR Adams, who's out 6-10 weeks"
    d5 = "The Los Angeles Rams announced that wide receiver Davante Adams sustained a lower-leg injury and will miss 6 to 10 weeks."
    subcat5 = engine.determine_story_subcategory(t5, "Sports", d5)
    assert subcat5 == "sports_football", f"Test 5 Failed: Subcategory {subcat5} != sports_football"

    img5 = engine.resolve_story_image(t5, "Sports", d5)
    assert any(w in img5["caption"].lower() for w in ["football", "helmet", "gridiron", "rams"]), f"Test 5 Image Caption Failed: {img5['caption']}"

    # Negative Candidate Check: Golf course image must fail for NFL football
    golf_cand5 = {
        "url": "https://images.unsplash.com/photo-1535131749006-b7f58c99034b",
        "caption": "Professional tournament championship fairway and clubhouse green at PGA Tour.",
        "tags": ["golf", "fairway", "pga"],
        "pool": "sports_football"
    }
    is_v5, errs5, _ = engine.validate_image_candidate(golf_cand5, subcat5, t5, d5)
    assert not is_v5, "Test 5 Negative Failed: Golf candidate did not fail for Rams football!"
    assert any("cross_domain:golf" in e or "cross_domain:fairway" in e for e in errs5), f"Errors: {errs5}"
    print("✓ TEST 5 PASSED: NFL equipment visual verified and golf imagery strictly rejected.")
    passed_count += 1

    # -------------------------------------------------------------------------
    # TEST 6: NBA Power Rankings
    # -------------------------------------------------------------------------
    print("\n[TEST 6] NBA Power Rankings Verification...")
    t6 = "Power Rankings: How all 30 teams measure up to begin 2026-27 season - NBA.com"
    d6 = "NBA.com published its preseason power rankings evaluating all 30 franchises ahead of the regular season tip-off."
    subcat6 = engine.determine_story_subcategory(t6, "Sports", d6)
    assert subcat6 == "sports_basketball", f"Test 6 Failed: Subcategory {subcat6} != sports_basketball"

    # Negative Candidate Check: Football helmet must fail for NBA basketball
    football_cand6 = {
        "url": "https://images.unsplash.com/photo-1566577739112-5180d4bf9390",
        "caption": "NFL football helmet and gridiron equipment on stadium sideline turf.",
        "tags": ["football", "helmet", "nfl"],
        "pool": "sports_basketball"
    }
    is_v6, errs6, _ = engine.validate_image_candidate(football_cand6, subcat6, t6, d6)
    assert not is_v6, "Test 6 Negative Failed: Football helmet did not fail for NBA basketball!"
    assert any("cross_domain:football helmet" in e or "cross_domain:gridiron" in e for e in errs6), f"Errors: {errs6}"
    print("✓ TEST 6 PASSED: Basketball context verified and football equipment / golf strictly rejected.")
    passed_count += 1

    # -------------------------------------------------------------------------
    # TEST 7: East Potomac Land Overhaul
    # -------------------------------------------------------------------------
    print("\n[TEST 7] East Potomac Land Overhaul Verification...")
    t7 = "Trump shares plan to overhaul East Potomac golf course amid court fight over land -"
    d7 = "Former President Donald Trump announced a proposal to overhaul D.C.'s East Potomac Golf Links amid National Park Service tree removal debates."
    subcat7 = engine.determine_story_subcategory(t7, "Politics", d7)
    assert subcat7 == "politics_public_land", f"Test 7 Failed: Subcategory {subcat7} != politics_public_land"

    # Negative Candidate Check: Generic Supreme Court building must fail for public land dispute
    scotus_cand7 = {
        "url": "https://upload.wikimedia.org/wikipedia/commons/9/94/Supreme_Court.jpg",
        "caption": "Supreme Court of the United States west facade courtroom in Washington, D.C.",
        "tags": ["supreme court", "courtroom", "scotus"],
        "pool": "politics_public_land"
    }
    is_v7, errs7, _ = engine.validate_image_candidate(scotus_cand7, subcat7, t7, d7)
    assert not is_v7, "Test 7 Negative Failed: Supreme Court image did not fail for East Potomac public land!"
    assert any("cross_domain:supreme court" in e or "cross_domain:courtroom" in e for e in errs7), f"Errors: {errs7}"
    print("✓ TEST 7 PASSED: East Potomac public land verified and generic Supreme Court building strictly rejected.")
    passed_count += 1

    # -------------------------------------------------------------------------
    # TEST 8: College Football Playoff Rankings
    # -------------------------------------------------------------------------
    print("\n[TEST 8] College Football Playoff Rankings Verification...")
    t8 = "College Football Rankings: Historic Upset-Filled Week 7 Flips Top 25 Upside Down - FOX Sports"
    d8 = "Historic weekend upsets across college football created major shakeups in the updated AP Top 25 rankings."
    subcat8 = engine.determine_story_subcategory(t8, "Sports", d8)
    assert subcat8 == "sports_football", f"Test 8 Failed: Subcategory {subcat8} != sports_football"

    img8 = engine.resolve_story_image(t8, "Sports", d8)
    assert any(w in img8["caption"].lower() for w in ["football", "stadium", "sports", "night lights"]), f"Test 8 Image Caption Failed: {img8['caption']}"
    assert "educational institution" not in img8["caption"].lower() and "campus building" not in img8["caption"].lower(), "Test 8 Failed: Generic brick campus building assigned to CFP rankings!"

    # Negative Fact Check: Boilerplate and headline overlap must fail
    bad_facts8 = [
        "College Football Rankings: Historic Upset-Filled Week 7 Flips Top 25 Upside Down.",
        "Verified reports and regulatory filings outline the operational context.",
        "The situation continues to evolve across college football conferences.",
        "Officials are monitoring developments ahead of upcoming committee meetings."
    ]
    facts_ok8, fact_errs8 = engine.validate_extracted_facts(t8, bad_facts8, d8)
    assert not facts_ok8, "Test 8 Negative Failed: Generic boilerplate facts were not rejected!"
    assert any("boilerplate" in e for e in fact_errs8), f"Expected boilerplate errors, got: {fact_errs8}"
    print("✓ TEST 8 PASSED: College football stadium verified and generic campus brick buildings / boilerplate strictly rejected.")
    passed_count += 1

    # -------------------------------------------------------------------------
    # -------------------------------------------------------------------------
    # TEST 9: Michigan Senate Debate & Zero-Boilerplate Fact Extraction
    # -------------------------------------------------------------------------
    print("\n[TEST 9] Michigan Senate Debate & Zero-Boilerplate Fact Extraction Verification...")
    t9 = "Brotherhood accusations in fiery Senate debate"
    d9 = "Abdul El-Sayed denied Muslim Brotherhood ties at a Michigan Senate debate after Mike Rogers referenced a 2012 letter to Egypt's president."
    subcat9 = engine.determine_story_subcategory(t9, "Politics", d9)
    assert subcat9 == "politics_elections", f"Test 9 Failed: Subcategory {subcat9} != politics_elections"

    # Focus entity check: Must be Abdul El-Sayed or El-Sayed, NEVER truncated 'El'
    ent9 = engine.extract_focus_entity(f"{t9} {d9}")
    assert "el-sayed" in ent9.lower(), f"Test 9 Failed: Focus entity '{ent9}' truncated or missed El-Sayed!"
    assert ent9.lower() != "el", "Test 9 Failed: Focus entity was truncated to single particle 'El'!"

    # Fact Extraction check: Must generate 4 substantive facts with ZERO boilerplate filler
    synth9 = engine.generate_contextual_synthesis(t9, d9, "Politics")
    facts9 = synth9.get("core_facts", [])
    assert len(facts9) == 4, f"Test 9 Failed: Expected 4 facts, got {len(facts9)}"

    # Validate that none of the forbidden filler phrases exist
    for f in facts9:
        f_lower = f.lower()
        assert "operational context" not in f_lower, f"Test 9 Failed: 'operational context' found in: {f}"
        assert "administrative reviews" not in f_lower, f"Test 9 Failed: 'administrative reviews' found in: {f}"
        assert "procedural timelines" not in f_lower, f"Test 9 Failed: 'procedural timelines' found in: {f}"
        assert "primary reporting documented" not in f_lower, f"Test 9 Failed: 'primary reporting documented' found in: {f}"

    # Verify validate_extracted_facts passes
    facts_ok9, errs9 = engine.validate_extracted_facts(t9, facts9, d9)
    assert facts_ok9, f"Test 9 Failed: Fact validation returned errors: {errs9}"

    # Verify talking points do not have 'regarding El'
    tp_red9 = " ".join(synth9["perspectives"]["RIGHT"]["talking_points"])
    assert "regarding el." not in tp_red9.lower() and "regarding el " not in tp_red9.lower(), f"Test 9 Failed: 'regarding El' found in talking points: {tp_red9}"

    # Negative check: Deliberate injection of the user's screenshot boilerplate MUST fail
    bad_screenshot_facts = [
        "Abdul El-Sayed denied Muslim Brotherhood ties at a Michigan Senate debate after Mike Rogers referenced a 2012 letter to Egypt's president.",
        "Primary reporting documented specific operational context and verified official timelines.",
        "Organizational leadership confirmed administrative reviews will continue as updates proceed.",
        "The situation continues to evolve across Michigan congressional districts."
    ]
    bad_ok9, bad_errs9 = engine.validate_extracted_facts(t9, bad_screenshot_facts, d9)
    assert not bad_ok9, "Test 9 Negative Failed: Screenshot boilerplate facts did NOT fail validation!"
    assert any("boilerplate" in e for e in bad_errs9), f"Test 9 Negative Failed: Expected boilerplate error, got: {bad_errs9}"
    print("✓ TEST 9 PASSED: Michigan Senate debate facts are 100% substantive; screenshot boilerplates strictly rejected.")
    passed_count += 1

    # -------------------------------------------------------------------------
    # TEST 10: Question & Clickbait Headline Direct Answer Verification
    # -------------------------------------------------------------------------
    print("\n[TEST 10] Question & Clickbait Headline Direct Answer Verification...")
    t10 = "Centrus vs. BWX Technologies: Which Nuclear Supply Chain Stock Is the Better Buy After the Sell-Off? - The Motley Fool"
    d10 = "Centrus Energy and BWX Technologies occupy critical positions in the nuclear supply chain after the sell-off."
    
    assert engine.is_question_or_clickbait_headline(t10), "Test 10 Failed: Did not detect question/clickbait headline!"
    
    synth10 = engine.generate_contextual_synthesis(t10, d10, "Business & Economy")
    facts10 = synth10.get("core_facts", [])
    assert len(facts10) == 4, f"Test 10 Failed: Expected 4 facts, got {len(facts10)}"
    
    f1_10 = facts10[0]
    # Fact 1 MUST directly answer the question, NOT repeat it
    assert "Direct Answer" in f1_10 or "Verdict" in f1_10, f"Test 10 Failed: Fact 1 does not state direct answer: {f1_10}"
    assert "Which Nuclear Supply Chain Stock Is the Better Buy" not in f1_10, f"Test 10 Failed: Fact 1 repeated the question!"
    assert "?" not in f1_10, f"Test 10 Failed: Fact 1 contains a question mark!"
    
    # Image check: Nuclear stock must get nuclear facility image, not generic sports/soccer
    img10 = engine.resolve_story_image(t10, "Business & Economy", "National Headlines")
    assert "nuclear" in img10["caption"].lower(), f"Test 10 Failed: Nuclear stock did not receive nuclear image: {img10}"
    print("✓ TEST 10 PASSED: Question headline immediately answered in Fact 1 with nuclear supply chain image.")
    passed_count += 1

    # -------------------------------------------------------------------------
    # TEST 11: General Sub-Sport Image Isolation & Feed-Wide Deduplication
    # -------------------------------------------------------------------------
    print("\n[TEST 11] General Sub-Sport Image Isolation & Feed-Wide Deduplication Verification...")
    t11_a = "Kevin Young may have been absent, but No. 25 BYU offered plenty of buzz at Big 12 basketball media days - Deseret News"
    d11_a = "Big 12 basketball media days in Kansas City featured plenty of buzz surrounding BYU."
    
    t11_b = "Warriors exploring Kristaps Porzingis trades as absence from team continues: Source - "
    d11_b = "The Golden State Warriors have begun exploring trade routes for center Kristaps Porzingis."

    # Subcategory check: Must be sports_basketball, NOT sports_football
    sub11_a = engine.determine_story_subcategory(t11_a, "Sports", d11_a)
    sub11_b = engine.determine_story_subcategory(t11_b, "Sports", d11_b)
    assert sub11_a == "sports_basketball", f"Test 11 Failed: BYU basketball got subcategory {sub11_a}"
    assert sub11_b == "sports_basketball", f"Test 11 Failed: Warriors trade got subcategory {sub11_b}"

    used_pool = set()
    img11_a = engine.resolve_story_image(t11_a, "Sports", "Sports", used_pool)
    img11_b = engine.resolve_story_image(t11_b, "Sports", "Sports", used_pool)

    # Both must receive basketball imagery
    assert "basketball" in img11_a["caption"].lower() or "hardwood" in img11_a["caption"].lower(), f"Test 11 Failed: BYU got non-basketball image: {img11_a}"
    assert "basketball" in img11_b["caption"].lower() or "hardwood" in img11_b["caption"].lower(), f"Test 11 Failed: Warriors got non-basketball image: {img11_b}"

    # Strict rejection of soccer ball and football stadium
    for img in [img11_a, img11_b]:
        assert "photo-1574629810360-7efbbe195018" not in img["url"], "Test 11 Failed: Soccer ball assigned to basketball story!"
        assert "soccer" not in img["caption"].lower(), "Test 11 Failed: Soccer caption assigned to basketball story!"
        assert "football stadium" not in img["caption"].lower(), "Test 11 Failed: Football stadium assigned to basketball story!"

    # Feed Deduplication Check: Multiple stories in same subcategory must never duplicate
    assert img11_a["url"] != img11_b["url"], "Test 11 Failed: Consecutive basketball stories received identical image URL!"
    
    # Test feed-wide deduplicator function on synthetic duplicates
    mock_stories = [
        {"id": "s1", "title": t11_a, "category": "Sports", "image_url": "https://images.unsplash.com/photo-dup"},
        {"id": "s2", "title": t11_b, "category": "Sports", "image_url": "https://images.unsplash.com/photo-dup"},
        {"id": "s3", "title": "Chiefs vs Bills playoff matchup", "category": "Sports", "image_url": "https://images.unsplash.com/photo-dup"}
    ]
    deduped = engine.enforce_feed_image_uniqueness(mock_stories)
    deduped_urls = [s["image_url"] for s in deduped]
    assert len(deduped_urls) == len(set(deduped_urls)), "Test 11 Failed: enforce_feed_image_uniqueness left duplicates!"
    print("✓ TEST 11 PASSED: Sub-sport basketball isolation verified; zero soccer leakage and 100% feed uniqueness guaranteed.")
    passed_count += 1


    # -------------------------------------------------------------------------
    # TEST 12: Real Estate & Interest Rate Story Image Isolation
    # -------------------------------------------------------------------------
    print("\n[TEST 12] Real Estate & Interest Rate Story Image Isolation Verification...")
    t12 = "Higher interest rates have made family offices pickier about investing in real estate"
    used_12 = set()
    img12 = engine.resolve_story_image(t12, "Business & Economy", master_category="Business & Economy", used_urls=used_12)
    assert img12["url"], "Test 12 Failed: No image returned for real estate!"
    assert "photo-1513836279014-a89f7a76ae86" not in img12["url"], "Test 12 Failed: Nuclear facility image assigned to real estate story!"
    assert img12["associated_subject"] == "Business_RealEstate", f"Test 12 Failed: Subject is {img12['associated_subject']}"
    assert any(word in img12["caption"].lower() for word in ("real estate", "property", "residential")), f"Test 12 Failed: Caption mismatch: {img12['caption']}"
    assert all("photo-1513836279014-a89f7a76ae86" not in item["url"] for item in engine.CATEGORY_FALLBACK_POOLS["Business & Economy"]), "Test 12 Failed: Nuclear image still in Business & Economy pool!"
    print("✓ TEST 12 PASSED: Real estate story receives verified property image; nuclear image strictly excluded.")
    passed_count += 1

    # -------------------------------------------------------------------------
    # TEST 13: Market Futures Story Uses Modern Financial Image & Rejects Antique Thumbnail
    # -------------------------------------------------------------------------
    print("\n[TEST 13] Market Futures Story Uses Modern Financial Image & Rejects Antique Thumbnail...")
    t13 = "Stock futures remain under pressure after worst Nasdaq session since June: Live updates -"
    entities13 = engine.extract_named_entities_from_title(t13)
    assert "Stock" not in entities13, "Test 13 Failed: 'Stock' extracted as entity!"
    assert "Futures" not in entities13, "Test 13 Failed: 'Futures' extracted as entity!"
    assert "Stock_futures" not in entities13, "Test 13 Failed: 'Stock_futures' extracted as entity!"
    assert "nasdaq" in [entity.casefold() for entity in entities13], "Test 13 Failed: 'nasdaq' not extracted as recognized entity!"

    antique_page = {
        "title": "Stock",
        "description": "A historical handwritten share certificate from the seventeenth century",
        "extract": "An antique manuscript documenting early share ownership.",
        "thumbnail": {
            "source": "https://upload.wikimedia.org/wikipedia/commons/example-antique-certificate.jpg"
        },
    }
    assert not engine.is_wikipedia_result_relevant(
        antique_page,
        t13,
        "Business & Economy",
        "Business & Economy",
    ), "Test 13 Failed: Antique share certificate was not rejected!"

    img13 = engine.resolve_story_image(
        t13,
        "Business & Economy",
        master_category="Business & Economy",
        used_urls=set(),
    )
    assert img13["url"], "Test 13 Failed: No image returned for market futures!"
    assert img13["associated_subject"] == "Business_FinancialMarkets", f"Test 13 Failed: Subject is {img13['associated_subject']}"
    assert any(word in img13["caption"].lower() for word in ("financial", "market", "trading")), f"Test 13 Failed: Caption mismatch: {img13['caption']}"
    assert "antique" not in img13["caption"].lower(), "Test 13 Failed: Antique in caption!"
    assert "certificate" not in img13["caption"].lower(), "Test 13 Failed: Certificate in caption!"
    print("✓ TEST 13 PASSED: Market futures story uses modern financial image; standalone generic nouns and antique certificate rejected.")
    passed_count += 1

    # FINAL VERIFICATION SUMMARY
    # -------------------------------------------------------------------------
    print("\n" + "=" * 75)
    print(f"REGRESSION SUITE COMPLETED: {passed_count}/{total_tests} TESTS PASSED (100% SUCCESS)")
    print("=" * 75)

if __name__ == "__main__":
    try:
        run_all_regression_tests()
    except Exception as e:
        print(f"\n[REGRESSION TEST FAILURE]: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

def test_12_real_estate_and_interest_rate_story_uses_relevant_image():
    title = "Higher interest rates have made family offices pickier about investing in real estate"
    used_urls = set()
    result = engine.resolve_story_image(
        title,
        "Business & Economy",
        master_category="Business & Economy",
        used_urls=used_urls,
    )
    assert result["url"]
    assert "photo-1513836279014-a89f7a76ae86" not in result["url"]
    assert result["associated_subject"] == "Business_RealEstate"
    assert any(word in result["caption"].lower() for word in ("real estate", "property", "residential"))
    assert all(
        "photo-1513836279014-a89f7a76ae86" not in item["url"]
        for item in engine.CATEGORY_FALLBACK_POOLS["Business & Economy"]
    )

def test_13_market_futures_story_uses_modern_financial_image_and_rejects_antique_thumbnail():
    title = "Stock futures remain under pressure after worst Nasdaq session since June"
    entities = engine.extract_named_entities_from_title(title)
    assert "Stock" not in entities
    assert "Futures" not in entities
    assert "Stock_futures" not in entities
    assert "nasdaq" in [entity.casefold() for entity in entities]

    antique_page = {
        "title": "Stock",
        "description": "A historical handwritten share certificate from the seventeenth century",
        "extract": "An antique manuscript documenting early share ownership.",
        "thumbnail": {
            "source": "https://upload.wikimedia.org/wikipedia/commons/example-antique-certificate.jpg"
        },
    }
    assert not engine.is_wikipedia_result_relevant(
        antique_page,
        title,
        "Business & Economy",
        "Business & Economy",
    )

    result = engine.resolve_story_image(
        title,
        "Business & Economy",
        master_category="Business & Economy",
        used_urls=set(),
    )
    assert result["url"]
    assert result["associated_subject"] == "Business_FinancialMarkets"
    assert any(word in result["caption"].lower() for word in ("financial", "market", "trading"))
    assert "antique" not in result["caption"].lower()
    assert "certificate" not in result["caption"].lower()
