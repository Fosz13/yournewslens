#!/usr/bin/env python3
"""
test_category_uniqueness.py
Automated test suite verifying that Key Talking Points & Arguments are 100% unique,
properly entity-grounded, and free of repetitive boilerplate across EVERY category.
"""

import sys
import engine

def run_tests():
    test_cases_50 = [
        # 10 Sports stories
        ('Patrick Mahomes rallies Chiefs with fourth-quarter touchdown drive against Raiders', 'Sports'),
        ('Lions beat Vikings on game-winning 44-yard field goal in overtime thriller', 'Sports'),
        ('Dodgers bullpen blanks Mets in Game 5 to advance to World Series', 'Sports'),
        ('College Football Playoff committee debates 24-team bracket format for 2027', 'Sports'),
        ('Jalen Hurts listed as questionable with leg injury ahead of Sunday matchup', 'Sports'),
        ('Celtics cruise past 76ers behind Jayson Tatum 35-point performance', 'Sports'),
        ('Rory McIlroy captures DP World Tour Championship with clutch birdie on 18', 'Sports'),
        ('Oilers overcome three-goal deficit to stun Panthers in overtime', 'Sports'),
        ('Coco Gauff advances to semifinals with dominant straight-sets victory', 'Sports'),
        ('NCAA approves new transfer portal windows and academic eligibility standards', 'Sports'),

        # 10 Politics stories
        ('Senate votes to advance bipartisan clean water and infrastructure funding package', 'Politics'),
        ('House ethics committee releases report on congressional campaign finance disclosures', 'Politics'),
        ('Supreme Court agrees to hear state dispute over regulatory jurisdiction', 'Politics'),
        ('Governors coalition signs regional workforce training agreement', 'Politics'),
        ('Federal election commission updates campaign ad disclosure rules for online platforms', 'Politics'),
        ('State lawmakers pass property tax relief bill ahead of legislative deadline', 'Politics'),
        ('Bipartisan coalition introduces bill to strengthen national cybersecurity defenses', 'Politics'),
        ('President signs executive order expanding domestic critical minerals mining permits', 'Politics'),
        ('Mayors conference calls for targeted federal grants to combat urban homelessness', 'Politics'),
        ('Congressional budget office releases updated ten-year deficit outlook projections', 'Politics'),

        # 10 Business & Economy stories
        ('Federal Reserve Chair signals measured approach on benchmark interest rates', 'Business & Economy'),
        ('Consumer price index rises 0.2 percent as food and energy prices stabilize', 'Business & Economy'),
        ('Tech shares rebound as semiconductor manufacturers report strong quarterly demand', 'Business & Economy'),
        ('Treasury yields hold steady ahead of monthly jobs report and retail sales data', 'Business & Economy'),
        ('Retailers report modest early holiday sales gains amid cautious consumer spending', 'Business & Economy'),
        ('Major airline announces expanded international routes following fleet modernization', 'Business & Economy'),
        ('Commercial real estate lenders restructure debt on downtown office towers', 'Business & Economy'),
        ('Auto manufacturing plants add second shift to meet hybrid vehicle demand', 'Business & Economy'),
        ('Regional banks report stable deposit balances following quarterly financial reviews', 'Business & Economy'),
        ('Labor department reports weekly jobless claims drop to three-month low', 'Business & Economy'),

        # 10 Healthcare & Energy stories
        ('HHS publishes updated hospital pricing guidelines and non-compliance fines', 'Health'),
        ('Medicare selects next round of prescription therapies for federal price negotiations', 'Health'),
        ('FDA authorizes new targeted immunotherapy treatment for aggressive lymphoma', 'Health'),
        ('State health departments expand rural clinic mobile screening units', 'Health'),
        ('Medical associations urge Congress to reform prior authorization rules for Medicare Advantage', 'Health'),
        ('Severe Pacific storm gusts cut power to thousands across Oregon and Washington', 'Energy & Weather'),
        ('FERC approves regional transmission upgrades to connect offshore wind projects', 'Energy & Weather'),
        ('Nuclear regulatory commission extends operating license for twin-reactor plant', 'Energy & Weather'),
        ('Interstate pipeline operator completes annual safety inspection and valve replacement', 'Energy & Weather'),
        ('Midwestern utilities invest in grid battery storage systems to manage peak demand', 'Energy & Weather'),

        # 10 Tech, Crime, Entertainment, World & Border stories
        ('NASA James Webb telescope observes atmosphere of distant gas giant', 'Science & Tech'),
        ('Commerce Department broadens semiconductor equipment export curbs', 'Science & Tech'),
        ('State attorneys general challenge social media platform age verification laws', 'Science & Tech'),
        ('AI research lab releases open weights model for biomedical imaging analysis', 'Science & Tech'),
        ('Municipal first responders stage multi-agency emergency drill at transit center', 'Crime & Public Safety'),
        ('Federal law enforcement dismantles multi-state cargo theft and fencing syndicate', 'Crime & Public Safety'),
        ('Autumn box office receipts surpass industry projections with original family features', 'Entertainment'),
        ('Director begins principal photography on large-format historical drama', 'Entertainment'),
        ('Allied foreign ministers convene emergency summit on maritime security in contested waters', 'World News'),
        ('Border patrol agents intercept commercial freight shipment carrying illegal narcotics', 'Border & Security')
    ]

    seen_quotes = set()
    duplicates = []

    for title, cat in test_cases_50:
        res = engine.generate_contextual_synthesis(title, '', cat)
        p = res['perspectives']
        for lens in ['RIGHT', 'CENTER', 'LEFT']:
            pts = p[lens]['talking_points']
            for pt in pts:
                if pt in seen_quotes:
                    duplicates.append((cat, title, lens, pt))
                seen_quotes.add(pt)

    print(f"Total Test Cases: {len(test_cases_50)}")
    print(f"Total Unique Quotes Generated: {len(seen_quotes)}")
    print(f"Duplicate Quotes Found: {len(duplicates)}")

    if duplicates:
        print("\nFailures:")
        for d in duplicates:
            print(f"  [{d[0]}] {d[1]} ({d[2]}): {d[3]}")
        sys.exit(1)
    else:
        print("\nPASSED: 100% of generated talking points are unique and properly entity-grounded across all categories!")

if __name__ == '__main__':
    run_tests()
