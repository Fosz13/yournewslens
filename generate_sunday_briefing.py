"""
Sunday Daily Briefing HTML Newsletter & Email Digest Generator
Compiles the 60-Second Dinner Table Cheat Sheet, verified facts, and multi-perspective
talking points across National, Sports, and Local Tampa Bay stories into an email client-ready
digest that links back to https://yournewslens.com.
"""

import os
import json
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

SUNDAY_CHEAT_SHEETS = [
    {
        "topic": "Congress & National Budget",
        "headline": "Senate Leaders Fast-Track $895B Defense & Border Spending Deal",
        "facts": [
            "Congressional leadership agreed on a $1.65T statutory discretionary budget, allocating $895B to defense/border technology and $704B for domestic programs.",
            "The bipartisan compromise averts a government shutdown while setting hard statutory negotiation deadlines across 12 agency bills."
        ],
        "conservative": "We're $36 trillion in debt and inflation is crushing regular families. Stop spending money we don't have, and don't pass any budget that doesn't actually secure the border.",
        "progressive": "Threatening to shut down the government over politics hurts working people and freezes essential food and healthcare programs. Keep the country running first, then debate.",
        "reality": "Neither side wants a costly government shutdown right before the holidays, so both parties compromised on military funding while kicking the bigger debt fight down the road.",
        "link": "https://yournewslens.com/#story-senate-appropriations-live-vote"
    },
    {
        "topic": "College Athletics & Governance",
        "headline": "College Football Playoff Weighs 24-Team Expansion Amid $20.5M Roster Cap",
        "facts": [
            "College football commissioners are reviewing a framework to expand the playoff to 24 teams by 2027, reserving 14 automatic conference bids and 10 at-large spots.",
            "The proposal comes as athletic departments prepare for the landmark $20.5M annual school player revenue-sharing cap taking effect in college sports."
        ],
        "conservative": "It ruins the regular season. When half the top 25 gets in, historic rivalries lose their do-or-die drama, and we're treating unpaid college kids like NFL crash dummies.",
        "progressive": "More playoff teams give underdog mid-majors a real shot, create incredible December games on campus, and stop four blue-blood schools from running the whole sport.",
        "reality": "TV networks and universities want the billions in playoff ad money, but playing 17 games a year wears out players and waters down regular season games.",
        "link": "https://yournewslens.com/#story-cfb-playoff-24"
    },
    {
        "topic": "Tampa Bay Regional Development",
        "headline": "Tampa Bay Rays $1.3B Ballpark & Historic Gas Plant District Enacted",
        "facts": [
            "St. Petersburg and Pinellas County approved $600M in tourist-development bed tax bonds to anchor a new 30,000-seat enclosed ballpark.",
            "The Tampa Bay Rays and Hines development partners are funding the remaining $700M+ alongside 1,200 planned affordable and workforce housing units."
        ],
        "conservative": "Billionaire team owners should build their own stadiums. Taxpayers shouldn't be paying hundreds of millions in bond debt when our roads, schools, and sewers desperately need repairs.",
        "progressive": "It keeps the Rays in St. Pete for 30 years and replaces empty parking lots with 1,200 affordable homes, local union jobs, and parks—mostly paid by tourist hotel taxes, not our property taxes.",
        "reality": "Tourist taxes soften the blow for local homeowners, but cities rarely break even on stadium deals unless the promised housing and entertainment district actually materialize.",
        "link": "https://yournewslens.com/#story-local-tampa-rays-gas-plant-agreement"
    }
]

def generate_email_html():
    date_str = datetime.now().strftime("%B %d, %Y")
    
    sections_html = ""
    for idx, cs in enumerate(SUNDAY_CHEAT_SHEETS):
        facts_items = "".join([f"<li style='margin-bottom: 8px; color: #334155;'>{f}</li>" for f in cs["facts"]])
        
        sections_html += f"""
        <table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="margin-bottom: 28px; background-color: #ffffff; border: 1px solid #e2e8f0; border-radius: 12px; overflow: hidden; box-shadow: 0 2px 8px rgba(0,0,0,0.06);">
          <tr>
            <td style="padding: 18px 24px 14px; background-color: #0f172a; border-bottom: 3px solid #10b981;">
              <span style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; font-size: 11px; font-weight: 800; color: #34d399; text-transform: uppercase; letter-spacing: 0.08em;">DEBATE #{idx+1} • {cs['topic']}</span>
              <h2 style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; font-size: 19px; font-weight: 800; color: #ffffff; margin: 6px 0 0; line-height: 1.35;">{cs['headline']}</h2>
            </td>
          </tr>
          <tr>
            <td style="padding: 20px 24px;">
              <!-- The Facts -->
              <table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="margin-bottom: 16px; background-color: #f8fafc; border-left: 4px solid #38bdf8; border-radius: 6px;">
                <tr>
                  <td style="padding: 12px 16px;">
                    <strong style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; font-size: 13px; color: #0284c7; text-transform: uppercase; letter-spacing: 0.04em;">⚖️ The Facts (What Actually Happened)</strong>
                    <ul style="margin: 8px 0 0; padding-left: 20px; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; font-size: 14px; line-height: 1.55;">
                      {facts_items}
                    </ul>
                  </td>
                </tr>
              </table>

              <!-- Conservative & Progressive Talking Points -->
              <table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="margin-bottom: 16px;">
                <tr>
                  <td width="48%" valign="top" style="padding: 12px 14px; background-color: #fff1f2; border: 1px solid #fecdd3; border-radius: 8px;">
                    <div style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; font-size: 12px; font-weight: 800; color: #e11d48; text-transform: uppercase; margin-bottom: 6px;">🔴 Conservative Talking Point</div>
                    <p style="margin: 0; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; font-size: 13.5px; line-height: 1.5; color: #1e293b; font-style: italic;">“{cs['conservative']}”</p>
                  </td>
                  <td width="4%"></td>
                  <td width="48%" valign="top" style="padding: 12px 14px; background-color: #eff6ff; border: 1px solid #bfdbfe; border-radius: 8px;">
                    <div style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; font-size: 12px; font-weight: 800; color: #2563eb; text-transform: uppercase; margin-bottom: 6px;">🔵 Progressive Talking Point</div>
                    <p style="margin: 0; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; font-size: 13.5px; line-height: 1.5; color: #1e293b; font-style: italic;">“{cs['progressive']}”</p>
                  </td>
                </tr>
              </table>

              <!-- Reality Check -->
              <table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="margin-bottom: 16px; background-color: #f0fdf4; border: 1px solid #bbf7d0; border-radius: 8px;">
                <tr>
                  <td style="padding: 12px 16px;">
                    <strong style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; font-size: 12px; color: #15803d; text-transform: uppercase; letter-spacing: 0.04em;">🟢 The Reality Check & Common Ground</strong>
                    <p style="margin: 4px 0 0; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; font-size: 13.5px; line-height: 1.5; color: #1e293b;">{cs['reality']}</p>
                  </td>
                </tr>
              </table>

              <!-- Click through button -->
              <div style="text-align: right;">
                <a href="{cs['link']}" style="display: inline-block; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; font-size: 13px; font-weight: 700; color: #0284c7; text-decoration: none; padding: 6px 12px; border: 1px solid #bae6fd; border-radius: 6px; background-color: #f0f9ff;">
                  Explore full wire coverage & dossier on Your News Lens &rarr;
                </a>
              </div>
            </td>
          </tr>
        </table>
        """

    full_email = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Your News Lens — Sunday Daily Briefing</title>
</head>
<body style="margin: 0; padding: 0; background-color: #f1f5f9; -webkit-font-smoothing: antialiased;">
  <table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background-color: #f1f5f9; padding: 24px 12px;">
    <tr>
      <td align="center">
        <!-- Main Email Container (600px width standard) -->
        <table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="max-width: 620px; text-align: left;">
          
          <!-- Header Branding -->
          <tr>
            <td style="padding: 24px 28px 20px; background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%); border-radius: 14px 14px 0 0; border-bottom: 3px solid #10b981;">
              <table role="presentation" width="100%" cellpadding="0" cellspacing="0">
                <tr>
                  <td>
                    <div style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; font-size: 26px; font-weight: 800; color: #ffffff; letter-spacing: -0.02em;">
                      <span style="color: #34d399;">Your</span> News Lens
                    </div>
                    <div style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; font-size: 13px; font-weight: 600; color: #94a3b8; margin-top: 4px;">
                      Sunday Daily Briefing • {date_str}
                    </div>
                  </td>
                  <td align="right" valign="top">
                    <span style="display: inline-block; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; font-size: 11px; font-weight: 800; color: #34d399; background: rgba(16, 185, 129, 0.2); border: 1px solid #10b981; padding: 4px 10px; border-radius: 20px; text-transform: uppercase;">
                      60-Sec Cheat Sheet
                    </span>
                  </td>
                </tr>
              </table>
              <p style="margin: 16px 0 0; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; font-size: 14px; line-height: 1.5; color: #cbd5e1;">
                Never get blindsided at family dinners or the water cooler. Here is your 2-minute conversation ammunition on the three biggest debates shaping the week.
              </p>
            </td>
          </tr>

          <!-- Body Content -->
          <tr>
            <td style="padding: 24px 20px; background-color: #f8fafc; border-left: 1px solid #cbd5e1; border-right: 1px solid #cbd5e1;">
              {sections_html}

              <!-- Sunday Interactive Challenge Callout -->
              <table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="margin-top: 12px; background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%); border-radius: 12px; text-align: center;">
                <tr>
                  <td style="padding: 26px 24px;">
                    <div style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; font-size: 11px; font-weight: 800; color: #38bdf8; text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 6px;">
                      🎯 Interactive Challenge
                    </div>
                    <h3 style="margin: 0 0 8px; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; font-size: 20px; font-weight: 800; color: #ffffff;">
                      Take the Blind Stance Challenge
                    </h3>
                    <p style="margin: 0 0 18px; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; font-size: 13.5px; line-height: 1.5; color: #94a3b8;">
                      Can you evaluate arguments without tribal bias? Vote on today's debates with party labels hidden and see how your instincts compare to real-time crowd data.
                    </p>
                    <a href="https://yournewslens.com/#blindStanceSection" style="display: inline-block; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; font-size: 14px; font-weight: 800; color: #ffffff; background: linear-gradient(135deg, #10b981 0%, #059669 100%); padding: 12px 28px; border-radius: 8px; text-decoration: none; box-shadow: 0 4px 12px rgba(16, 185, 129, 0.35);">
                      Vote in the Blind Stance Survey &rarr;
                    </a>
                  </td>
                </tr>
              </table>
            </td>
          </tr>

          <!-- Footer -->
          <tr>
            <td style="padding: 20px 28px; background-color: #0f172a; border-radius: 0 0 14px 14px; text-align: center;">
              <p style="margin: 0 0 8px; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; font-size: 12px; color: #64748b;">
                You are receiving this Sunday briefing because you subscribed to updates on <a href="https://yournewslens.com" style="color: #38bdf8; text-decoration: none;">YourNewsLens.com</a>.
              </p>
              <p style="margin: 0; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; font-size: 11px; color: #475569;">
                &copy; {datetime.now().year} Your News Lens • Verified Facts, Multi-Perspective Wire & Civic Intelligence • Tampa, FL
              </p>
            </td>
          </tr>

        </table>
      </td>
    </tr>
  </table>
</body>
</html>
"""
    return full_email

def main():
    email_content = generate_email_html()
    output_path = os.path.join(BASE_DIR, "data", "sunday_daily_briefing.html")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(email_content)
    print(f"Generated Sunday Daily Briefing email template ({len(email_content)} bytes) at {output_path}")

if __name__ == "__main__":
    main()
