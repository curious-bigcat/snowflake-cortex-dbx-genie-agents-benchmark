"""
Supplementary Document Generator — Case Notes, Memos, Emails, Board Minutes
All coherent with SEC v. Meridian Capital universe.
Generates 25+ supplementary text files as case notes and internal records.
"""
import os, sys, random
from datetime import date, timedelta
from faker import Faker

sys.path.insert(0, os.path.dirname(__file__))
from universe import (CASE, CRIMINAL_CASE, CLASS_ACTION, PARTIES, ATTORNEYS,
                      TIMELINE, FINANCIALS, STATUTES)

fake = Faker()
Faker.seed(701)
random.seed(701)

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "legal", "docs", "case_notes")
os.makedirs(OUTPUT_DIR, exist_ok=True)


def save(filename, content):
    path = os.path.join(OUTPUT_DIR, filename)
    with open(path, 'w') as f:
        f.write(content)
    pages = len(content) // 3000
    print(f"  {filename}: {pages} pages ({len(content):,} chars)")
    return pages


# =============================================================================
# 1. INTERNAL EMAIL CHAINS (evidence in the case)
# =============================================================================
def gen_email_chains():
    total = 0

    # Email chain 1: Hartwell to Chen — the tip
    content = f"""
FROM: Robert Hartwell <rhartwell@meridiancapital.com>
TO: Sarah Chen <schen@meridiancapital.com>
DATE: February 23, 2021 7:14 AM EST
SUBJECT: APEX - URGENT

Sarah,

Move on APEX immediately, before Thursday announcement. Full position. Call me
on my cell before you do anything.

-RH

---

FROM: Sarah Chen <schen@meridiancapital.com>
TO: Robert Hartwell <rhartwell@meridiancapital.com>
DATE: February 23, 2021 7:42 AM EST
SUBJECT: RE: APEX - URGENT

Rob,

Understood. What size are we talking? I need to know for approval thresholds per
the compliance manual (Section 5.3). Anything over $50M needs CIO sign-off too.

Also — should I check the restricted list? We don't currently have APEX on any
watchlist but wanted to confirm.

Sarah

---

FROM: Robert Hartwell <rhartwell@meridiancapital.com>
TO: Sarah Chen <schen@meridiancapital.com>
DATE: February 23, 2021 7:58 AM EST
SUBJECT: RE: RE: APEX - URGENT

Skip the compliance BS, we need to move before it's public. I have Board
Resolution 2021-047 authorizing $200M for tech sector — use that as cover.

Start with 500K shares on Monday (Feb 28). Build to full 3M position by March 12.
Options too — 15K contracts, March/April expiry.

DO NOT put APEX on the restricted list. DO NOT log this in the compliance system.

-RH

---

FROM: Sarah Chen <schen@meridiancapital.com>
TO: Robert Hartwell <rhartwell@meridiancapital.com>
DATE: February 23, 2021 8:15 AM EST
SUBJECT: RE: RE: RE: APEX - URGENT

Rob, I want to flag that this feels wrong. We have no research coverage on APEX,
no analyst thesis, and you're asking me to skip restricted list checks.

I'll do what you say because you're the CEO, but I'm uncomfortable with this.

Sarah

---

FROM: Robert Hartwell <rhartwell@meridiancapital.com>
TO: Sarah Chen <schen@meridiancapital.com>
DATE: February 23, 2021 8:22 AM EST
SUBJECT: RE: RE: RE: RE: APEX - URGENT

Noted. Just execute. This is a legitimate trade based on our merger arb strategy.
Board authorized tech allocation. End of discussion.

If anyone asks, we identified APEX as undervalued through our quantitative screens.
The timing is coincidence.

-RH
"""
    # Pad with more email chains (noise but related)
    for i in range(30):
        dt = date(2021, 2, 28) + timedelta(days=random.randint(0, 15))
        content += f"""
---

FROM: Marcus Zhang <mzhang@meridiancapital.com>
TO: Sarah Chen <schen@meridiancapital.com>
DATE: {dt} {random.randint(6,18)}:{random.randint(10,59):02d} AM EST
SUBJECT: APEX Trade Confirmation - {random.randint(50,500)}K shares

Sarah,

Confirming execution of {random.randint(50,500)},000 shares APEX at ${random.uniform(45,55):.2f}.
Total consideration: ${random.uniform(2,25):.1f}M. Executed on {random.choice(['NYSE','NASDAQ','Dark Pool'])}.

Marcus

---

FROM: Sarah Chen <schen@meridiancapital.com>
TO: Marcus Zhang <mzhang@meridiancapital.com>
DATE: {dt} {random.randint(6,18)}:{random.randint(10,59):02d} AM EST
SUBJECT: RE: APEX Trade Confirmation

Approved per CEO directive. Compliance check: [NOT PERFORMED]

Sarah
"""
    total += save("email_chain_01_hartwell_chen_apex_trades.txt", content)

    # Email chain 2: Hartwell to Pacific Growth (the tip)
    content = f"""
FROM: Robert Hartwell <rhartwell@meridiancapital.com>
TO: David Nakamura <dnakamura@pacificgrowth.com>
DATE: February 24, 2021 9:30 PM EST
SUBJECT: Dinner next week?

Dave,

Great seeing you at the conference last month. Quick question — have you looked at
APEX Technologies recently? Their software division is undervalued IMO. Might be
interesting for your event-driven book.

Let me know if you want to grab dinner to discuss. Maybe Tuesday?

-Rob

P.S. I'd move quickly on this one. Things might change by end of next week.

---

FROM: David Nakamura <dnakamura@pacificgrowth.com>
TO: Robert Hartwell <rhartwell@meridiancapital.com>
DATE: February 25, 2021 8:15 AM PST
SUBJECT: RE: Dinner next week?

Rob,

Thanks for the heads up. We'll take a look. Always trust your instincts on these.

Dinner Tuesday works. Nobu?

-Dave

---

FROM: Robert Hartwell <rhartwell@meridiancapital.com>
TO: David Nakamura <dnakamura@pacificgrowth.com>
DATE: February 25, 2021 11:45 AM EST
SUBJECT: RE: RE: Dinner next week?

Nobu works. 8pm. And Dave — seriously, don't wait on APEX. Next 2 weeks will be
very interesting. Trust me on this one.

-Rob
"""
    total += save("email_chain_02_hartwell_pacific_growth_tip.txt", content)

    # Email chain 3: Compliance officer notices (but is ignored)
    content = f"""
FROM: Jennifer Walsh <jwalsh@meridiancapital.com>
TO: Sarah Chen <schen@meridiancapital.com>
CC: Robert Hartwell <rhartwell@meridiancapital.com>
DATE: March 3, 2021 3:45 PM EST
SUBJECT: ALERT: APEX Position Size - Approaching 5% Threshold

Sarah, Rob,

Per our daily position monitoring (Compliance Manual Section 18.1), I need to flag
that our APEX Technologies position has reached approximately 4.8% of fund AUM
(approximately $201 million at current market prices).

Under our policy:
- WARNING threshold: 5% ($210M) — we are approaching this
- ALERT threshold: 7% ($294M)
- BREACH threshold: 8% ($336M)

Please confirm this position is authorized and within investment guidelines.
I also note that APEX does not appear on our current research coverage list.

Regards,
Jennifer Walsh
Chief Compliance Officer
Meridian Capital Group LLC

---

FROM: Robert Hartwell <rhartwell@meridiancapital.com>
TO: Jennifer Walsh <jwalsh@meridiancapital.com>
CC: Sarah Chen <schen@meridiancapital.com>
DATE: March 3, 2021 4:02 PM EST
SUBJECT: RE: ALERT: APEX Position Size - Approaching 5% Threshold

Jennifer,

Authorized under Board Resolution 2021-047 (February 15, 2021) which approved
$200M allocation to technology sector opportunities. APEX was identified by our
quantitative screening models as significantly undervalued relative to peers.

We will not exceed the 8% limit. Please close this alert.

Rob

---

FROM: Jennifer Walsh <jwalsh@meridiancapital.com>
TO: Robert Hartwell <rhartwell@meridiancapital.com>
DATE: March 3, 2021 4:30 PM EST
SUBJECT: RE: RE: ALERT: APEX Position Size - Approaching 5% Threshold

Rob,

Understood. I've noted the Board Resolution authorization. However, I also want to
flag that per Section 5.2, I don't see a restricted list check logged for any of
the APEX trades since February 28. Can you confirm these checks were performed?

Also, I note 47 trades in a 4-day period for a name we've never traded before.
Our Trade Surveillance system (Section 16.3) flagged this volume as unusual.
Should I mark this as resolved?

Jennifer

---

FROM: Robert Hartwell <rhartwell@meridiancapital.com>
TO: Jennifer Walsh <jwalsh@meridiancapital.com>
DATE: March 3, 2021 4:45 PM EST
SUBJECT: RE: RE: RE: ALERT: APEX Position Size

Jennifer — Yes, mark it as resolved. The restricted list checks were done verbally
with Sarah. I'll have her backfill the log. This is a legitimate investment thesis.
Please don't escalate further.

Rob
"""
    total += save("email_chain_03_compliance_alert_ignored.txt", content)
    return total


# =============================================================================
# 2. BOARD MINUTES
# =============================================================================
def gen_board_minutes():
    total = 0

    content = f"""
{'='*80}
MERIDIAN CAPITAL GROUP LLC
MINUTES OF THE BOARD OF DIRECTORS
Special Meeting — February 15, 2021
{'='*80}

PRESENT:
- Robert J. Hartwell (Chairman and CEO)
- Dr. Eleanor Michaels (Independent Director)
- Thomas R. Gardner (Independent Director)
- Patricia Voss-Klein (Independent Director)
- Sarah M. Chen (CFO, attending as Secretary)

ABSENT: None

CALLED TO ORDER: 2:00 PM EST

1. APPROVAL OF TECHNOLOGY SECTOR ALLOCATION

The Chairman presented a proposal to allocate up to $200,000,000 (Two Hundred
Million Dollars) of the fund's assets to technology sector investments, to be
deployed over the following 90 days at the discretion of the investment committee.

DISCUSSION: Ms. Voss-Klein inquired about specific targets. The Chairman indicated
that the allocation would be spread across 8-12 technology names identified by the
quantitative screening models and the merger arbitrage team.

Mr. Gardner asked whether any single position would exceed the 8% concentration
limit. The Chairman confirmed that no single position would exceed 8% of fund AUM
(${FINANCIALS['max_single_position_allowed']:,.0f} at current AUM of
${FINANCIALS['fund_aum_at_time']:,.0f}).

RESOLVED: The Board unanimously approved Board Resolution 2021-047, authorizing
a technology sector allocation of up to $200,000,000 at the discretion of the
investment committee, subject to compliance with all existing position limits
and risk parameters.

VOTE: 4-0 in favor (unanimous)

NOTE: This resolution was passed on February 15, 2021, seven (7) days BEFORE
Robert Hartwell received material non-public information about the Apex Technologies
merger on {TIMELINE['meridian_tip_received']}. The resolution was a legitimate
governance action that was later misused to justify the insider trading.

2. QUARTERLY COMPLIANCE REPORT

The CCO (Jennifer Walsh) presented the Q4 2020 compliance report. No material
findings. All position limits were within thresholds. Zero restricted list violations.

3. ADJOURNMENT

Meeting adjourned at 3:15 PM EST.

CERTIFIED:
Sarah M. Chen, Secretary
Meridian Capital Group LLC
"""
    # Add more Board meetings to bulk it up
    for quarter in ["Q1 2021", "Q2 2021", "Q3 2021", "Q4 2021", "Q1 2022"]:
        content += f"""

{'='*80}
MERIDIAN CAPITAL GROUP LLC
MINUTES OF THE BOARD OF DIRECTORS
Regular Quarterly Meeting — {quarter}
{'='*80}

PRESENT:
- Robert J. Hartwell (Chairman and CEO)
- Dr. Eleanor Michaels (Independent Director)
- Thomas R. Gardner (Independent Director)
- Patricia Voss-Klein (Independent Director)
- Sarah M. Chen (CFO, attending as Secretary)

1. APPROVAL OF MINUTES: Prior quarter minutes approved unanimously.

2. INVESTMENT PERFORMANCE REVIEW:
{fake.paragraph(nb_sentences=8)}

3. RISK AND COMPLIANCE UPDATE:
{fake.paragraph(nb_sentences=6)}
{'The CCO reported no material compliance findings.' if quarter != 'Q1 2022' else 'NOTE: The CCO reported that the SEC had opened a formal investigation (January 10, 2022) into trading activity in Apex Technologies securities. Outside counsel Williams & Thornton LLP has been engaged. All relevant employees have been placed on administrative leave pending the investigation.'}

4. NEW BUSINESS:
{fake.paragraph(nb_sentences=5)}

ADJOURNMENT: Meeting adjourned.
"""
    total += save("board_minutes_2021_2022.txt", content)
    return total


# =============================================================================
# 3. TRADING LOG (raw trade records matching SEC complaint allegations)
# =============================================================================
def gen_trading_log():
    content = f"""
{'='*80}
MERIDIAN CAPITAL GROUP LLC — APEX TECHNOLOGIES TRADING LOG
Account: MCG Master Fund LP (Primary Trading Account)
Period: {TIMELINE['meridian_first_trade']} through {TIMELINE['trading_period_end']}
Generated from Order Management System (OMS)
{'='*80}

DATE       | TIME     | SIDE | QUANTITY  | PRICE   | NOTIONAL     | VENUE    | TRADER    | APPROVED BY
{'='*120}
"""
    # Generate the specific 47 trades Chen mentioned
    trade_dates = []
    for day_offset in range(16):  # Feb 28 to March 15
        d = date(2021, 2, 28) + timedelta(days=day_offset)
        if d.weekday() < 5:  # Weekdays only
            trade_dates.append(d)

    total_shares = 0
    trade_num = 0
    for td in trade_dates:
        num_trades_today = random.randint(3, 7)
        for _ in range(num_trades_today):
            if trade_num >= 47:
                break
            qty = random.choice([50000, 75000, 100000, 125000, 150000, 200000])
            price = round(random.uniform(45.50, 52.80), 2)
            notional = qty * price
            total_shares += qty
            venue = random.choice(["NYSE", "NASDAQ", "BATS", "IEX", "DARK-CS", "DARK-GS"])
            content += f"{td} | {random.randint(9,15):02d}:{random.randint(0,59):02d}:{random.randint(0,59):02d} | BUY  | {qty:>9,} | ${price:>7.2f} | ${notional:>12,.2f} | {venue:<8} | M. Zhang  | S. Chen\n"
            trade_num += 1

    content += f"""
{'='*120}
SUMMARY:
  Total Trades: {trade_num}
  Total Shares Acquired: {total_shares:,}
  Average Price: ${random.uniform(47, 50):.2f}
  Total Notional: ${total_shares * 48.5:,.2f}

NOTE: NO restricted list check was logged for ANY of these trades.
      Compliance Manual Section 5.2 requires documented check before execution.
      Violation flagged by CCO Jennifer Walsh on March 3, 2021 (see email records).

{'='*80}
OPTIONS TRADING LOG — APEX TECHNOLOGIES CALL OPTIONS
{'='*80}

DATE       | CONTRACTS | STRIKE | EXPIRY    | PREMIUM  | NOTIONAL    | VENUE    | TRADER
{'='*100}
"""
    for td in trade_dates[:10]:
        contracts = random.choice([500, 1000, 1500, 2000, 2500])
        strike = random.choice([50, 55, 60, 65, 70])
        premium = round(random.uniform(2, 8), 2)
        content += f"{td} | {contracts:>9,} | ${strike:>5} | 2021-{random.choice(['04','05','06'])}-{random.randint(15,21)} | ${premium:>6.2f} | ${contracts * 100 * premium:>11,.2f} | CBOE     | M. Zhang\n"

    content += f"""
{'='*100}
TOTAL OPTIONS: 15,000 contracts
TOTAL OPTIONS PREMIUM PAID: approximately $14.2 million
"""
    save("trading_log_apex_technologies.txt", content)
    return len(content) // 3000


# =============================================================================
# 4. ATTORNEY WORK PRODUCT / CASE STRATEGY MEMO
# =============================================================================
def gen_attorney_memo():
    content = f"""
{'='*80}
PRIVILEGED AND CONFIDENTIAL — ATTORNEY WORK PRODUCT
ATTORNEY-CLIENT PRIVILEGED

WILLIAMS & THORNTON LLP
MEMORANDUM

TO:     Robert J. Hartwell
FROM:   James P. Williams, Esq.
DATE:   June 20, 2022
RE:     SEC v. Meridian Capital Group — Initial Assessment and Strategy
{'='*80}

I. EXECUTIVE SUMMARY

On June 15, 2022, the SEC filed a civil enforcement action against Meridian Capital
Group LLC, you personally, Pacific Growth Partners LP, and Marcus Zhang. The complaint
alleges violations of Section 10(b) of the Exchange Act and Rule 10b-5 based on
alleged insider trading in Apex Technologies securities. The SEC seeks:

  - Disgorgement of $89,700,000 (Meridian's alleged profits)
  - Civil monetary penalties of $15,000,000 (against you personally)
  - Permanent injunction from future violations
  - Officer and director bar

II. ASSESSMENT OF SEC'S CASE

A. Strengths of SEC's Position:
  1. The email from you to Chen on 2/23/2021 ("Move on APEX immediately, before
     Thursday announcement") is devastating evidence of scienter
  2. Trading pattern is highly suspicious — zero prior APEX history, then $136M
     in 4 days before a public announcement
  3. Sarah Chen is cooperating (agreement dated {TIMELINE['chen_cooperation_agreement']})
  4. Pacific Growth's parallel trading corroborates the tipping allegation

B. Potential Defenses:
  1. Board Resolution 2021-047 authorized tech sector allocation — legitimate cover
  2. "Thursday announcement" could arguably refer to internal strategy meeting
  3. Quantitative screening argument (weak — no documentation)
  4. Chen's testimony may be unreliable (incentive to cooperate)

C. Realistic Assessment:
  Probability of SEC prevailing at trial: 85-90%
  Recommended path: Negotiate settlement

III. RECOMMENDED STRATEGY

Phase 1 (Months 1-3): File Motion to Dismiss under Rule 12(b)(6)
  - Argue failure to adequately plead scienter (Tellabs standard)
  - Argument is weak but buys time and forces SEC to show their hand
  - Expected outcome: Motion likely DENIED

Phase 2 (Months 4-12): Discovery and negotiation
  - Cooperate with reasonable discovery requests
  - Begin settlement discussions
  - Target: Disgorgement only (no personal penalty, no bar)

Phase 3 (If settlement fails): Trial preparation
  - Focus on Board Resolution as authorized trading
  - Challenge Chen's credibility
  - Argue profits were from legitimate merger arbitrage

IV. CRIMINAL EXPOSURE

CRITICAL: The U.S. Attorney's office (SDNY) has opened a parallel criminal
investigation. Wire fraud carries up to 20 years. Securities fraud up to 20 years.
If criminal charges are brought, our civil strategy changes dramatically.

Recommendation: Do NOT make any statements to the SEC that could be used in the
criminal case. Assert Fifth Amendment if necessary.

V. FEES

Estimated legal fees for full litigation: $15-25 million
Estimated legal fees if settled within 12 months: $5-8 million

Please call me to discuss.

James P. Williams
Partner, Williams & Thornton LLP
"""
    for i in range(10):
        content += f"""

{'='*60}
SUPPLEMENTAL MEMO #{i+1} — {date(2022,7,1) + timedelta(days=random.randint(0,730))}
RE: Case Update and Strategy Adjustment
{'='*60}

{fake.paragraph(nb_sentences=15)}

Key developments this period:
- {fake.sentence()}
- {fake.sentence()}
- {fake.sentence()}

Recommended next steps:
{fake.paragraph(nb_sentences=8)}
"""
    save("attorney_memo_strategy_privileged.txt", content)
    return len(content) // 3000


# =============================================================================
# 5. SEC INVESTIGATION NOTES (internal SEC work product)
# =============================================================================
def gen_sec_investigation_notes():
    content = f"""
{'='*80}
SECURITIES AND EXCHANGE COMMISSION
DIVISION OF ENFORCEMENT

INVESTIGATION FILE: HO-14289
MATTER: Meridian Capital Group LLC — Insider Trading
LEAD ATTORNEY: {ATTORNEYS['sec_enforcement']['name']}
DATE OPENED: {TIMELINE['sec_investigation_opened']}
{'='*80}

INVESTIGATION TIMELINE AND NOTES:

January 10, 2022 — INVESTIGATION OPENED
Referral from FINRA Market Regulation. FINRA surveillance detected unusual
trading activity in APEX Technologies (NASDAQ: APEX) by Meridian Capital Group
in the period February 28 - March 15, 2021. Pattern is consistent with trading
on MNPI ahead of the March 15, 2021 merger announcement.

Key observations from FINRA referral:
- Meridian had ZERO position in APEX prior to Feb 28, 2021
- Between Feb 28 and March 15: accumulated {FINANCIALS['meridian_apex_shares_peak']:,} shares
- Also purchased {FINANCIALS['meridian_apex_options_contracts']:,} call option contracts
- Timing: All purchases occurred BEFORE public announcement on March 15
- Profit: Estimated ${FINANCIALS['meridian_illegal_profits']:,.0f}

January 15, 2022 — FORMAL ORDER OF INVESTIGATION
Commission authorized formal investigation. Subpoena authority granted.

February 1, 2022 — SUBPOENAS ISSUED
- Meridian Capital Group: All trading records, communications, compliance files
- Goldman Sachs (prime broker): All APEX transactions for Meridian accounts
- Global Systems Corp: All parties who knew about merger prior to announcement

March 2022 — DOCUMENT PRODUCTION
Received 2.4 million pages of documents from Meridian. Key discovery:
- Email from Hartwell to Chen (Feb 23, 2021): "Move on APEX immediately"
- Board Resolution 2021-047 (Feb 15, 2021): $200M tech allocation
- Trading logs showing 47 trades with NO restricted list checks

April 2022 — CHEN APPROACHES FOR COOPERATION
Sarah Chen's personal attorney ({ATTORNEYS['chen_counsel']['name']}) contacted
our office. Chen willing to provide testimony in exchange for:
- No enforcement action against her personally
- Cooperation credit in any proceedings

May 1, 2022 — COOPERATION AGREEMENT EXECUTED
Chen signed formal cooperation agreement. Key testimony:
- Hartwell received tip at dinner on {TIMELINE['meridian_tip_received']}
- Hartwell directed her to "skip compliance BS"
- She knew it was wrong but followed CEO's instructions
- Board Resolution was pre-existing, used as cover AFTER the tip

May 2022 — PARALLEL CRIMINAL REFERRAL
Referred matter to SDNY U.S. Attorney's Office for potential criminal charges
against Hartwell (wire fraud, securities fraud).

June 15, 2022 — COMPLAINT FILED
Case number: {CASE['docket_no']}

TOTAL ILLEGAL PROFITS:
  Meridian Capital: ${FINANCIALS['meridian_illegal_profits']:,.0f}
  Pacific Growth Partners: ${FINANCIALS['pacific_growth_illegal_profits']:,.0f}
  TOTAL: ${FINANCIALS['total_scheme_profits']:,.0f}
"""
    save("sec_investigation_file_notes.txt", content)
    return len(content) // 3000


# =============================================================================
# 6. EXPERT DECLARATION (supporting damages)
# =============================================================================
def gen_expert_declaration():
    content = f"""
{'='*80}
UNITED STATES DISTRICT COURT
SOUTHERN DISTRICT OF NEW YORK

Case No. {CLASS_ACTION['docket_no']}

DECLARATION OF DR. JAMES R. PATTERSON, Ph.D.
IN SUPPORT OF MOTION FOR CLASS CERTIFICATION

I, James R. Patterson, declare under penalty of perjury as follows:
{'='*80}

1. I am a Professor of Finance at Columbia Business School. I have been retained
by Lead Counsel to provide expert analysis on damages and common impact.

2. METHODOLOGY: I employ an event study methodology using a market model to isolate
the impact of Defendants' fraudulent conduct on Apex Technologies' stock price.

3. KEY FINDINGS:

   a) The merger announcement on {TIMELINE['apex_merger_announced']} caused Apex
      stock to increase from ${FINANCIALS['apex_share_price_before']:.2f} to
      ${FINANCIALS['apex_share_price_after']:.2f} — a {((FINANCIALS['apex_share_price_after']/FINANCIALS['apex_share_price_before'])-1)*100:.1f}% increase.

   b) However, approximately $17.28 per share of this increase is attributable to
      the artificial inflation caused by Defendants' pre-announcement trading.

   c) Total class-wide damages are estimated at ${FINANCIALS['class_damages_estimated']:,.0f}.

4. COMMON IMPACT: All class members were affected by the same artificial inflation.
   The impact can be calculated on a class-wide basis using publicly available
   trading data without individual inquiries.

5. CLASS SIZE: Based on trading volume during the Class Period
   ({CLASS_ACTION['class_period_start']} to {CLASS_ACTION['class_period_end']}),
   approximately {CLASS_ACTION['estimated_class_size']:,} investors purchased Apex
   securities and were damaged.

6. PER-SHARE DAMAGES:
   - Artificial inflation (peak): $17.28 per share
   - Volume-weighted average inflation: $18.39 per share
   - Estimated damaged shares: 22.4 million
   - Total damages: 22.4M × $18.39 = ${FINANCIALS['class_damages_estimated']:,.0f}

I declare under penalty of perjury that the foregoing is true and correct.

Dr. James R. Patterson
Columbia Business School
Date: {TIMELINE['expert_report_filed']}
"""
    save("expert_declaration_class_cert.txt", content)
    return len(content) // 3000


# =============================================================================
# MAIN
# =============================================================================
def main():
    print("="*60)
    print("SUPPLEMENTARY DOCUMENTS — CASE NOTES & INTERNAL RECORDS")
    print("All coherent with SEC v. Meridian Capital universe")
    print("="*60)
    print()

    total_pages = 0
    total_pages += gen_email_chains()
    total_pages += gen_board_minutes()
    total_pages += gen_trading_log()
    total_pages += gen_attorney_memo()
    total_pages += gen_sec_investigation_notes()
    total_pages += gen_expert_declaration()

    print(f"\nTotal supplementary docs: ~{total_pages} pages")
    print(f"Output: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
