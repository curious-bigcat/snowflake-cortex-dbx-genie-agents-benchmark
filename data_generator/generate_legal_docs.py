"""
Legal Benchmark - Coherent Document Generator
Each document references EXACT entities, dates, and amounts from universe.py
All cross-references are verifiable against the tables.
"""
import os, sys, random
from datetime import date, timedelta
from faker import Faker

sys.path.insert(0, os.path.dirname(__file__))
from universe import (CASE, CRIMINAL_CASE, CLASS_ACTION, PARTIES, ATTORNEYS,
                      TIMELINE, FINANCIALS, STATUTES, DOCUMENTS)

fake = Faker()
Faker.seed(601)
random.seed(601)

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "legal", "docs")
os.makedirs(OUTPUT_DIR, exist_ok=True)

def legal_filler(paragraphs=20):
    """Generate legal prose filler between key sections."""
    lines = []
    for _ in range(paragraphs):
        lines.append(fake.paragraph(nb_sentences=random.randint(4,8)))
    return "\n\n".join(lines)

def pad_to_pages(content, target_pages, section_title="Additional Provisions"):
    """Pad document to target page count (~3000 chars/page)."""
    while len(content) < target_pages * 3000:
        content += f"\n\n{'='*40}\n{section_title} — Section {random.randint(1,50)}.{random.randint(1,20)}\n{'='*40}\n\n"
        content += legal_filler(random.randint(10, 25))
    return content


# =============================================================================
# DOC 1: SEC ENFORCEMENT COMPLAINT (800 pages)
# Cross-references: all parties, key dates, trade amounts, docket number
# =============================================================================
def gen_sec_complaint():
    content = f"""
{'='*80}
UNITED STATES DISTRICT COURT
SOUTHERN DISTRICT OF NEW YORK

Case No. {CASE['docket_no']}

SECURITIES AND EXCHANGE COMMISSION,
    Plaintiff,

v.

MERIDIAN CAPITAL GROUP LLC, ROBERT J. HARTWELL,
PACIFIC GROWTH PARTNERS LP, and MARCUS D. ZHANG,
    Defendants.

COMPLAINT FOR VIOLATIONS OF THE FEDERAL SECURITIES LAWS
{'='*80}

Filed: {TIMELINE['sec_complaint_filed']}
Judge: {CASE['judge']}

The Securities and Exchange Commission ("SEC" or "Commission") alleges as follows:

I. SUMMARY

1. This action arises from a massive insider trading scheme orchestrated by
Robert J. Hartwell ("Hartwell"), the CEO and Managing Partner of Meridian Capital
Group LLC ("Meridian"), a New York-based hedge fund managing approximately
${FINANCIALS['fund_aum_at_time']:,.0f} in assets under management.

2. Between {TIMELINE['trading_period_start']} and {TIMELINE['trading_period_end']},
Hartwell and his co-conspirators generated illegal profits totaling approximately
${FINANCIALS['total_scheme_profits']:,.0f} by trading on material, non-public
information ("MNPI") regarding the acquisition of Apex Technologies Inc. ("Apex")
by Global Systems Corp. ("Global Systems").

3. Specifically, on or about {TIMELINE['meridian_tip_received']}, Hartwell received
confidential information about the planned acquisition of Apex Technologies Inc.
(NASDAQ: APEX) by Global Systems Corp. (NYSE: GSYS) at a price of
${FINANCIALS['apex_merger_price']:.2f} per share — a significant premium over
Apex's then-trading price of ${FINANCIALS['apex_share_price_before']:.2f} per share.

4. Beginning on {TIMELINE['meridian_first_trade']}, just four (4) days after
receiving the tip and fifteen (15) days before the public announcement of the
merger on {TIMELINE['apex_merger_announced']}, Meridian began aggressively
accumulating Apex securities. By the time of the public announcement, Meridian
held approximately {FINANCIALS['meridian_apex_shares_peak']:,} shares of Apex
common stock and {FINANCIALS['meridian_apex_options_contracts']:,} call option
contracts.

5. Hartwell also tipped Marcus D. Zhang ("Zhang"), Meridian's Head Trader, and
Pacific Growth Partners LP ("Pacific Growth"), a California-based hedge fund, both
of whom traded on the MNPI for their own benefit.

6. The illegal profits from this scheme are calculated as follows:
   - Meridian Capital Group LLC:  ${FINANCIALS['meridian_illegal_profits']:,.0f}
   - Pacific Growth Partners LP:  ${FINANCIALS['pacific_growth_illegal_profits']:,.0f}
   - TOTAL ILLEGAL PROFITS:       ${FINANCIALS['total_scheme_profits']:,.0f}

II. DEFENDANTS

7. Meridian Capital Group LLC ({PARTIES['meridian']['id']}) is a Delaware limited
liability company with its principal place of business in New York, New York. Meridian
is registered with the Commission as an investment adviser under the Investment
Advisers Act of 1940. At all relevant times, Meridian managed approximately
${FINANCIALS['fund_aum_at_time']:,.0f} in assets through various hedge fund strategies
focused on event-driven equity, merger arbitrage, and special situations.

8. Robert J. Hartwell ({PARTIES['hartwell']['id']}), age 54, resides in Greenwich,
Connecticut. Hartwell is the CEO, Managing Partner, and majority owner of Meridian
Capital Group LLC. Hartwell holds Series 7 and Series 63 licenses.

9. Pacific Growth Partners LP ({PARTIES['pacific_growth']['id']}) is a California
limited partnership with its principal place of business in San Francisco, California.
Pacific Growth is a hedge fund that received trading tips from Hartwell and executed
trades in Apex securities based on MNPI.

10. Marcus D. Zhang ({PARTIES['marcus_zhang']['id']}), age 41, resides in New York,
New York. Zhang served as Head Trader at Meridian Capital Group from 2018 through
June 2022. Zhang executed the fraudulent trades at Hartwell's direction.

III. RELATED PARTIES AND WITNESSES

11. Sarah M. Chen ({PARTIES['chen']['id']}), age 38, formerly served as Chief
Financial Officer of Meridian Capital Group from 2019 through her resignation on
{TIMELINE['chen_last_day']}. Chen is a cooperating witness pursuant to a cooperation
agreement dated {TIMELINE['chen_cooperation_agreement']}. Chen approved {DOCUMENTS['chen_deposition']['key_facts']['trades_approved']}
in Apex securities during the period {TIMELINE['trading_period_start']} through
March 15, 2021 without conducting the mandatory restricted list check required by
Meridian's compliance manual.

12. Apex Technologies Inc. ({PARTIES['apex']['id']}) (NASDAQ: APEX) is a California
corporation and the target company in the acquisition by Global Systems Corp. At the
time of the merger announcement on {TIMELINE['apex_merger_announced']}, Apex's stock
price increased from ${FINANCIALS['apex_share_price_before']:.2f} to approximately
${FINANCIALS['apex_share_price_after']:.2f} per share — a gain of approximately
{((FINANCIALS['apex_share_price_after']/FINANCIALS['apex_share_price_before'])-1)*100:.1f}%.

13. Global Systems Corp. ({PARTIES['global_systems']['id']}) (NYSE: GSYS) is a
Washington corporation that acquired Apex Technologies pursuant to the Agreement
and Plan of Merger dated {TIMELINE['apex_merger_agreement_signed']} at a price of
${FINANCIALS['apex_merger_price']:.2f} per share in cash. The merger closed on
{TIMELINE['apex_merger_closed']}.

IV. JURISDICTION AND VENUE

14. The Court has jurisdiction over this action pursuant to Sections 21(d), 21(e),
and 27 of the Securities Exchange Act of 1934 ("Exchange Act"), 15 U.S.C. §§ 78u(d),
78u(e), and 78aa.

15. Venue is proper in this District pursuant to Section 27 of the Exchange Act,
15 U.S.C. § 78aa, because certain of the acts, transactions, and courses of business
alleged herein occurred within the Southern District of New York, and because
Meridian and Hartwell reside and transact business in this District.

V. FACTUAL ALLEGATIONS

A. The Apex Technologies / Global Systems Merger

16. On or about {TIMELINE['apex_merger_agreement_signed']}, Apex Technologies and
Global Systems Corp. entered into an Agreement and Plan of Merger (the "Merger
Agreement"), pursuant to which Global Systems would acquire all outstanding shares
of Apex common stock at a price of ${FINANCIALS['apex_merger_price']:.2f} per share
in cash. The Merger Agreement contained a Material Adverse Effect threshold of
$75,000,000 and a break-up fee of $125,000,000.

17. The merger was publicly announced on {TIMELINE['apex_merger_announced']}.
Prior to the announcement, Apex shares traded at approximately
${FINANCIALS['apex_share_price_before']:.2f}. Following the announcement, shares
immediately rose to ${FINANCIALS['apex_share_price_after']:.2f}.

18. The merger closed on {TIMELINE['apex_merger_closed']}, with shareholders
receiving ${FINANCIALS['apex_merger_price']:.2f} per share.

B. Hartwell Obtains MNPI

19. On {TIMELINE['meridian_tip_received']}, Hartwell attended a private dinner with
an executive of Global Systems Corp. at the Union Club in New York City. During
this dinner, the executive disclosed to Hartwell that Global Systems was in advanced
negotiations to acquire Apex Technologies at approximately $84 per share.

20. This information was material and non-public. The merger negotiations were
being conducted under strict confidentiality pursuant to a mutual non-disclosure
agreement between Apex and Global Systems.

C. The Illegal Trading

21. Beginning on {TIMELINE['meridian_first_trade']}, Meridian began purchasing
Apex common stock and call options in unprecedented volumes. The Commission's
analysis shows the following trading pattern:

   Date              Shares Purchased    Options Contracts    Daily Volume
   {TIMELINE['meridian_first_trade']}     847,000            3,200             $40.5M
   2021-03-01        523,000            2,800             $25.1M
   2021-03-02        412,000            2,100             $19.8M
   2021-03-03        389,000            1,900             $18.6M
   2021-03-08        341,000            2,500             $16.3M
   2021-03-09        335,000            2,500             $16.0M
   TOTAL:            2,847,000          15,000            $136.3M

22. This trading activity was unprecedented for Meridian's Apex position. In the
twelve months prior to {TIMELINE['meridian_tip_received']}, Meridian held zero shares
of Apex Technologies and had never traded Apex securities.

23. Sarah Chen (CFO) approved these trades without conducting the mandatory
restricted list check required by Section 5.3 of Meridian's Compliance Manual.
Chen later testified in her deposition on {TIMELINE['chen_deposition']} that
Hartwell instructed her: "Move on APEX immediately, before Thursday announcement."

D. Pacific Growth Partners' Trading

24. On {TIMELINE['pacific_growth_first_trade']}, Pacific Growth Partners began
purchasing Apex securities after receiving a tip from Hartwell. Pacific Growth
accumulated approximately 1,200,000 shares, generating profits of approximately
${FINANCIALS['pacific_growth_illegal_profits']:,.0f}.

VI. CLAIMS FOR RELIEF

FIRST CLAIM: Violations of Section 10(b) of the Exchange Act and Rule 10b-5
(Against All Defendants)

25. Defendants violated {STATUTES['10b5']} by purchasing securities of Apex
Technologies while in possession of MNPI regarding the merger, and by communicating
such information to others who traded on it.

SECOND CLAIM: Violations of Section 20A — Insider Trading (Against Hartwell)

26. Defendant Hartwell violated {STATUTES['insider_trading']} by trading while in
possession of MNPI and by tipping others.

VII. RELIEF REQUESTED

The Commission respectfully requests that this Court:
(a) Permanently enjoin Defendants from violating Section 10(b) and Rule 10b-5;
(b) Order Defendants to disgorge all illegal profits totaling ${FINANCIALS['total_scheme_profits']:,.0f};
(c) Order Defendants to pay prejudgment interest;
(d) Impose civil monetary penalties pursuant to 15 U.S.C. § 78u-1;
(e) Freeze Defendants' assets pending final adjudication;
(f) Grant such other relief as this Court deems just and proper.

Dated: {TIMELINE['sec_complaint_filed']}

SECURITIES AND EXCHANGE COMMISSION

By: {ATTORNEYS['sec_enforcement']['name']}
    Senior Enforcement Counsel
    {ATTORNEYS['sec_enforcement']['firm']}
"""
    content = pad_to_pages(content, 800, "Additional Factual Allegations and Evidence")
    with open(os.path.join(OUTPUT_DIR, "sec_complaint_meridian_capital.txt"), 'w') as f:
        f.write(content)
    print(f"  sec_complaint_meridian_capital.txt: {len(content)//3000} pages")


# =============================================================================
# DOC 2: COMPLIANCE MANUAL (700 pages)
# =============================================================================
def gen_compliance_manual():
    content = f"""
{'='*80}
MERIDIAN CAPITAL GROUP LLC
COMPLIANCE AND REGULATORY PROCEDURES MANUAL
Version 7.3
Effective Date: January 1, 2021
Classification: STRICTLY CONFIDENTIAL — INTERNAL USE ONLY
{'='*80}

This manual establishes the compliance policies and procedures for Meridian Capital
Group LLC ("Meridian" or the "Firm"), a registered investment adviser with
approximately ${FINANCIALS['fund_aum_at_time']:,.0f} in assets under management.

{'='*60}
CHAPTER 1: CODE OF ETHICS AND PERSONAL TRADING
{'='*60}

1.1 Overview
All employees, officers, and directors of Meridian Capital Group LLC are fiduciaries
to our clients and must act in their best interests at all times.

1.2 Pre-Clearance Requirements
All personal securities transactions by employees at the Vice President level and
above MUST be pre-cleared by the Chief Compliance Officer prior to execution.

1.3 Restricted List
The Firm maintains a Restricted List of securities that may not be traded by the
Firm or its employees. The Restricted List is updated daily and maintained by the
Compliance Department.

CRITICAL REQUIREMENT: Before executing ANY trade on behalf of the Firm or any
client account, the portfolio manager or trader MUST verify that the security is
NOT on the Restricted List. This check is MANDATORY and must be documented.

Failure to check the Restricted List before trading constitutes a material compliance
violation subject to immediate escalation under Section 14.7.

{'='*60}
CHAPTER 5: TRADING COMPLIANCE AND BEST EXECUTION
{'='*60}

5.1 Position Limits

The Firm shall not hold a position in any single issuer exceeding {FINANCIALS['compliance_max_position_pct']}%
of the Firm's total assets under management.

   Current AUM: ${FINANCIALS['fund_aum_at_time']:,.0f}
   Maximum single-name position: ${FINANCIALS['max_single_position_allowed']:,.0f}
   (calculated as {FINANCIALS['compliance_max_position_pct']}% of ${FINANCIALS['fund_aum_at_time']:,.0f})

Any position approaching 6% of AUM requires pre-approval from the Risk Committee.
Any position exceeding 8% of AUM constitutes a BREACH requiring immediate reporting
under Section 14.7.

5.2 Restricted List Verification

Prior to execution of ANY trade, the executing trader MUST:
(a) Check the current Restricted List (updated daily at 7:00 AM ET)
(b) Document the check in the Trade Compliance Log
(c) Obtain verbal confirmation from a Compliance Officer for positions exceeding $50M
(d) If the security appears on the Restricted List, STOP — do not execute

5.3 Approval Authority

The following approval hierarchy applies to trade execution:
   - Trades under $10M: Portfolio Manager approval
   - Trades $10M-$50M: Portfolio Manager + Head Trader approval
   - Trades $50M-$100M: Portfolio Manager + Head Trader + CIO approval
   - Trades over $100M: Portfolio Manager + CIO + CEO approval + Risk Committee notification

{'='*60}
CHAPTER 14: INCIDENT RESPONSE AND REGULATORY NOTIFICATION
{'='*60}

14.1 Purpose
This chapter establishes procedures for identifying, reporting, and remediating
compliance incidents, regulatory inquiries, and potential violations.

14.2 Incident Classification

Level 1 (CRITICAL): Material violations of securities laws, insider trading,
market manipulation, fraud, data breach affecting client data
Level 2 (HIGH): Position limit breaches, unauthorized trading, regulatory
examination deficiencies
Level 3 (MEDIUM): Procedural violations, late filings, incomplete records
Level 4 (LOW): Administrative errors, minor documentation gaps

14.7 Escalation Requirements

14.7(a) General Reporting Obligation
Any employee who becomes aware of a potential compliance violation MUST report it
to the Chief Compliance Officer within {FINANCIALS['compliance_reporting_deadline_hours']} hours of discovery.

14.7(b) Escalation Timeline by Level

LEVEL 1 (CRITICAL) — Timeline:
  - IMMEDIATE (within 1 hour): Notify Chief Compliance Officer and General Counsel
  - Within 4 hours: Notify CEO, freeze relevant accounts/positions
  - Within 24 hours: Notify Board of Directors, engage outside counsel
  - Within 48 hours: File preliminary regulatory notification (SEC, FINRA)
  - Within 72 hours: Complete initial investigation report

LEVEL 2 (HIGH) — Timeline:
  - Within 4 hours: Notify Chief Compliance Officer
  - Within 24 hours: Complete preliminary assessment
  - Within 72 hours: Report to CEO and General Counsel
  - Within 5 business days: Complete remediation plan

14.7(c) Reporting to Regulators

For Level 1 incidents involving potential violations of federal securities laws:
  - SEC notification required within 48 hours under Rule 204-2(a)(12)
  - FINRA notification required within 48 hours for registered representatives
  - State AG notification for data breaches as required by applicable state law

14.8 Non-Retaliation

The Firm strictly prohibits retaliation against any employee who reports a potential
compliance violation in good faith. Violations of this policy will result in
immediate termination and referral to appropriate authorities.

{'='*60}
CHAPTER 18: POSITION MONITORING AND CONCENTRATION LIMITS
{'='*60}

18.1 Daily Position Monitoring

The Risk Management team shall monitor all portfolio positions daily and report
any position exceeding the following thresholds:

   WARNING: Position reaches 5% of AUM (${FINANCIALS['fund_aum_at_time']*0.05:,.0f})
   ALERT:   Position reaches 7% of AUM (${FINANCIALS['fund_aum_at_time']*0.07:,.0f})
   BREACH:  Position exceeds 8% of AUM (${FINANCIALS['fund_aum_at_time']*0.08:,.0f})

18.2 Concentration Reporting

When any single-name position exceeds the 8% threshold:
(a) Immediate notification to CIO and CCO
(b) Trading halt on the security until Risk Committee approval
(c) Remediation plan required within 5 business days
(d) Report to Board at next meeting (or immediately if position exceeds 12%)

NOTE: At the Firm's current AUM of ${FINANCIALS['fund_aum_at_time']:,.0f}, the
maximum allowable position is ${FINANCIALS['max_single_position_allowed']:,.0f}.
Meridian's peak position in Apex Technologies of {FINANCIALS['meridian_apex_shares_peak']:,}
shares at approximately $78.50/share = approximately $223.5 million, which represents
approximately 5.3% of AUM — within the 8% limit but above the 5% WARNING threshold.
"""
    content = pad_to_pages(content, 700, "Additional Compliance Procedures")
    with open(os.path.join(OUTPUT_DIR, "compliance_manual_meridian_capital.txt"), 'w') as f:
        f.write(content)
    print(f"  compliance_manual_meridian_capital.txt: {len(content)//3000} pages")


# =============================================================================
# DOC 3: SETTLEMENT AGREEMENT (400 pages)
# =============================================================================
def gen_settlement():
    content = f"""
{'='*80}
UNITED STATES DISTRICT COURT
SOUTHERN DISTRICT OF NEW YORK

Case No. {CLASS_ACTION['docket_no']}

THORNTON PENSION FUND, on behalf of itself and all others similarly situated,
    Lead Plaintiff,

v.

MERIDIAN CAPITAL GROUP LLC, ROBERT J. HARTWELL,
PACIFIC GROWTH PARTNERS LP, and MARCUS D. ZHANG,
    Defendants.

STIPULATION AND AGREEMENT OF SETTLEMENT
{'='*80}

This Stipulation and Agreement of Settlement ("Settlement Agreement") is entered
into as of {TIMELINE['settlement_reached']} by and among:

(i) Lead Plaintiff Thornton Pension Fund ({PARTIES['thornton_pension']['id']}),
on behalf of itself and the Settlement Class; and

(ii) Defendants Meridian Capital Group LLC ({PARTIES['meridian']['id']}),
Robert J. Hartwell ({PARTIES['hartwell']['id']}), Pacific Growth Partners LP
({PARTIES['pacific_growth']['id']}), and Marcus D. Zhang ({PARTIES['marcus_zhang']['id']}).

{'='*50}
I. RECITALS
{'='*50}

WHEREAS, on {TIMELINE['sec_complaint_filed']}, the SEC filed an enforcement action
against Defendants in case number {CASE['docket_no']};

WHEREAS, on {CLASS_ACTION['filing_date']}, Lead Plaintiff filed this class action
on behalf of all persons and entities who purchased or acquired Apex Technologies
Inc. (NASDAQ: APEX) common stock during the Class Period;

WHEREAS, the Court granted class certification on {TIMELINE['class_certification_granted']},
certifying a class of approximately {CLASS_ACTION['estimated_class_size']:,} affected investors;

WHEREAS, Lead Plaintiff's damages expert, Dr. James R. Patterson, estimated total
class-wide damages of approximately ${FINANCIALS['class_damages_estimated']:,.0f};

{'='*50}
II. DEFINITIONS
{'='*50}

2.1 "Class Period" means {CLASS_ACTION['class_period_start']} through
{CLASS_ACTION['class_period_end']}.

2.2 "Settlement Amount" means ${FINANCIALS['settlement_amount']:,.0f} (Three Hundred
Forty-Seven Million Five Hundred Thousand Dollars).

2.3 "Net Settlement Fund" means the Settlement Amount less: (a) Court-approved
attorneys' fees and expenses; (b) costs of notice and claims administration;
(c) Court-approved awards to Lead Plaintiff.

2.4 "Settlement Class" means all persons and entities who purchased or otherwise
acquired Apex Technologies Inc. common stock during the Class Period and were
damaged thereby. Excluded from the Settlement Class are Defendants, officers and
directors of Meridian Capital Group, and their immediate family members.

{'='*50}
III. SETTLEMENT CONSIDERATION
{'='*50}

3.1 In full and complete settlement of the Released Claims, Defendants shall
pay or cause to be paid the Settlement Amount of ${FINANCIALS['settlement_amount']:,.0f}
into an escrow account within thirty (30) days of Preliminary Approval.

3.2 The Settlement Amount shall be funded as follows:
   - Meridian Capital Group LLC:  $225,000,000
   - Robert J. Hartwell:          $72,500,000
   - Pacific Growth Partners LP:  $40,000,000
   - Marcus D. Zhang:             $10,000,000
   TOTAL:                          ${FINANCIALS['settlement_amount']:,.0f}

{'='*50}
IV. PLAN OF ALLOCATION
{'='*50}

4.1 The Net Settlement Fund shall be distributed to Authorized Claimants on a pro
rata basis based on each Authorized Claimant's Recognized Loss relative to the
total Recognized Losses of all Authorized Claimants.

4.2 Allocation Formula:
   Claimant's Pro Rata Share = (Claimant's Recognized Loss / Total Recognized
   Losses of All Authorized Claimants) × Net Settlement Fund

4.3 Recognized Loss Calculation:
   For shares purchased during the Class Period and sold before {CLASS_ACTION['class_period_end']}:
   Recognized Loss = (Purchase Price - Sale Price) × Shares

   For shares purchased during the Class Period and held through {CLASS_ACTION['class_period_end']}:
   Recognized Loss = (Purchase Price - ${FINANCIALS['apex_share_price_before']:.2f}) × Shares

4.4 The estimated per-share recovery is ${FINANCIALS['per_share_recovery']:.2f} per
damaged share, based on Total Recognized Losses of approximately
${FINANCIALS['class_damages_estimated']:,.0f} and a Net Settlement Fund of approximately
$269,312,500 (after deducting fees and expenses).

4.5 Minimum Distribution: No distribution shall be made to any Authorized Claimant
whose calculated payment is less than ${FINANCIALS['minimum_distribution']:.2f}.

{'='*50}
V. ATTORNEYS' FEES AND EXPENSES
{'='*50}

5.1 Lead Counsel shall apply to the Court for an award of attorneys' fees not
to exceed {FINANCIALS['attorney_fees_pct']}% of the Settlement Fund, plus
reimbursement of actual litigation expenses.

5.2 The requested fee is ${FINANCIALS['attorney_fees_amount']:,.0f}
({FINANCIALS['attorney_fees_pct']}% of ${FINANCIALS['settlement_amount']:,.0f}).

{'='*50}
VI. OPT-OUT PROCEDURES
{'='*50}

6.1 Any Settlement Class Member who wishes to be excluded from the Settlement
Class must submit a written Request for Exclusion ("Opt-Out Request") to the
Claims Administrator.

6.2 To be valid, a Request for Exclusion must be postmarked no later than
{TIMELINE['opt_out_deadline']}.

6.3 THE {TIMELINE['opt_out_deadline']} DEADLINE IS FIRM AND NON-EXTENDABLE.
The Court has expressly ruled that no extensions will be granted.

6.4 Claims must be submitted by {TIMELINE['claims_deadline']}.

6.5 Class Members who do not opt out will be bound by the Settlement and release
all Released Claims.

6.6 As of the date of Final Approval ({TIMELINE['settlement_final_approval']}),
342 Class Members had submitted valid Opt-Out Requests out of approximately
{CLASS_ACTION['estimated_class_size']:,} total Class Members.

{'='*50}
VII. RELEASE OF CLAIMS
{'='*50}

7.1 Upon Final Approval, Settlement Class Members release all claims arising from
purchases of Apex Technologies securities during the Class Period, including but
not limited to claims under Section 10(b), Rule 10b-5, and Section 20(a) of the
Exchange Act.

Lead Counsel: {ATTORNEYS['class_counsel']['name']}
              {ATTORNEYS['class_counsel']['firm']}

Defense Counsel: {ATTORNEYS['williams_thornton']['name']}
                 {ATTORNEYS['williams_thornton']['firm']}
"""
    content = pad_to_pages(content, 400, "Additional Settlement Provisions and Exhibits")
    with open(os.path.join(OUTPUT_DIR, "settlement_agreement_thornton_v_meridian.txt"), 'w') as f:
        f.write(content)
    print(f"  settlement_agreement_thornton_v_meridian.txt: {len(content)//3000} pages")


# =============================================================================
# DOC 4: CHEN DEPOSITION (500 pages)
# =============================================================================
def gen_chen_deposition():
    content = f"""
{'='*80}
UNITED STATES DISTRICT COURT
SOUTHERN DISTRICT OF NEW YORK

Case No. {CASE['docket_no']}
SEC v. Meridian Capital Group LLC et al.

DEPOSITION OF SARAH M. CHEN
Former Chief Financial Officer, Meridian Capital Group LLC

Date: {TIMELINE['chen_deposition']}
Location: Williams & Thornton LLP, 500 Park Avenue, New York, NY

Reported by: Maria Rodriguez, RPR, CSR
{'='*80}

APPEARANCES:

For the SEC:
   {ATTORNEYS['sec_enforcement']['name']}
   {ATTORNEYS['sec_enforcement']['firm']}

For Defendants Meridian Capital and Hartwell:
   {ATTORNEYS['williams_thornton']['name']}
   {ATTORNEYS['williams_thornton']['firm']}

For the Witness Sarah Chen:
   {ATTORNEYS['chen_counsel']['name']}
   {ATTORNEYS['chen_counsel']['firm']}

{'='*40}
EXAMINATION BY {ATTORNEYS['sec_enforcement']['name'].upper()}
{'='*40}

Q. Ms. Chen, please state your full name for the record.
A. Sarah Michelle Chen.

Q. And what was your position at Meridian Capital Group?
A. I was the Chief Financial Officer from June 2019 until my resignation on
{TIMELINE['chen_last_day']}.

Q. What were your responsibilities as CFO?
A. I was responsible for financial reporting, fund accounting, trade approval and
settlement, regulatory filings, and oversight of the compliance function.

Q. Did you have authority to approve trades?
A. Yes. Under Section 5.3 of Meridian's Compliance Manual, trades between $10 million
and $50 million required my approval as CFO along with the Portfolio Manager. Trades
over $50 million also required the CIO's approval.

Q. I'd like to direct your attention to February 2021. Do you recall when Mr. Hartwell
first discussed Apex Technologies with you?
A. Yes. It was on February 23, 2021. The day after he received the information.

Q. How do you know it was February 23?
A. Because I have an email from that date. Mr. Hartwell sent me an email at 7:14 AM
that said — and I quote — "Move on APEX immediately, before Thursday announcement."

Q. And what did "Thursday announcement" refer to?
A. The public announcement of the Apex merger, which occurred on Thursday,
{TIMELINE['apex_merger_announced']}.

Q. So you understood that Mr. Hartwell had advance knowledge of the merger announcement?
A. Yes. That's what I understood from his email.

MR. {ATTORNEYS['williams_thornton']['name'].split()[-1].upper()}: Objection. Calls for speculation as to Mr. Hartwell's knowledge.

THE WITNESS: I'm just telling you what I understood at the time.

Q. What did you do after receiving that email?
A. I approved the initial trades in Apex stock starting on {TIMELINE['meridian_first_trade']}.

Q. How many trades did you approve in Apex securities?
A. Forty-seven trades between February 28 and March 15, 2021.

Q. And did you check the restricted list before approving those trades?
A. No. I did not.

Q. The Compliance Manual at Section 5.2 requires a restricted list check before
ANY trade execution. Is that correct?
A. Yes, that's correct. I failed to follow that procedure.

Q. Why did you skip the restricted list check?
A. Because Mr. Hartwell told me it was urgent and to bypass the normal process.
He said, and I quote, "Skip the compliance BS, we need to move before it's public."

Q. At the time of these trades, what was Apex's stock price?
A. It was trading around ${FINANCIALS['apex_share_price_before']:.2f} per share.

Q. And after the announcement on {TIMELINE['apex_merger_announced']}?
A. It jumped to approximately ${FINANCIALS['apex_share_price_after']:.2f} per share
on the day of the announcement.

Q. What was the total position Meridian accumulated?
A. Approximately {FINANCIALS['meridian_apex_shares_peak']:,} shares and
{FINANCIALS['meridian_apex_options_contracts']:,} call option contracts.

Q. And the total value of profits from this trading?
A. The final calculation showed approximately ${FINANCIALS['meridian_illegal_profits']:,.0f}
in profits for Meridian.

Q. When did you become aware that what you had done was illegal?
A. In January 2022, when the SEC opened its investigation. That's when I retained
personal counsel, Mr. {ATTORNEYS['chen_counsel']['name']}.

Q. And you subsequently entered into a cooperation agreement with the SEC?
A. Yes, on {TIMELINE['chen_cooperation_agreement']}.

Q. One final area. You mentioned Board Resolution 2021-047. What was that?
A. That was a resolution passed by Meridian's Board on February 15, 2021 that
authorized a $200 million allocation to the technology sector. Mr. Hartwell used
that as cover for the Apex trades — claiming they were part of the authorized
technology allocation. But the resolution was passed BEFORE he received the tip,
so it wasn't actually related to the insider information.

Q. Thank you, Ms. Chen. No further questions.
"""
    content = pad_to_pages(content, 500, "Continued Examination and Cross-Examination")
    with open(os.path.join(OUTPUT_DIR, "deposition_sarah_chen.txt"), 'w') as f:
        f.write(content)
    print(f"  deposition_sarah_chen.txt: {len(content)//3000} pages")


# =============================================================================
# DOC 5: MERGER AGREEMENT (600 pages)
# =============================================================================
def gen_merger_agreement():
    content = f"""
{'='*80}
AGREEMENT AND PLAN OF MERGER

by and among

APEX TECHNOLOGIES INC.
("Company")

and

GLOBAL SYSTEMS CORP.
("Parent")

and

GS ACQUISITION SUB INC.
("Merger Sub")

Dated as of {TIMELINE['apex_merger_agreement_signed']}
{'='*80}

ARTICLE I — THE MERGER

1.1 The Merger. Upon the terms and subject to the conditions set forth in this
Agreement, at the Effective Time, Merger Sub shall be merged with and into the
Company, with the Company continuing as the surviving corporation.

1.2 Closing. The closing of the Merger shall take place on the Closing Date.
The merger closed on {TIMELINE['apex_merger_closed']}.

1.3 Effective Time. The Effective Time shall be the time at which the Certificate
of Merger is filed with the Secretary of State of the State of Delaware.

ARTICLE II — MERGER CONSIDERATION

2.1 Conversion of Shares. At the Effective Time, each share of Company Common
Stock issued and outstanding immediately prior to the Effective Time shall be
converted into the right to receive ${FINANCIALS['apex_merger_price']:.2f} in cash
(the "Merger Consideration"), without interest.

2.2 Treatment of Options. Each outstanding option to purchase Company Common Stock
shall be cancelled and converted into the right to receive an amount in cash equal to
the excess of ${FINANCIALS['apex_merger_price']:.2f} over the exercise price.

ARTICLE X — DEFINITIONS

10.1 "Material Adverse Effect" means any event, occurrence, fact, condition, or
change that, individually or in the aggregate, has had or would reasonably be
expected to have a material adverse effect on (a) the business, results of
operations, financial condition, or assets of the Company and its Subsidiaries,
taken as a whole; provided, however, that in no event shall any of the following
be deemed to constitute a Material Adverse Effect: (i) changes in general
economic conditions; (ii) changes in the industry; (iii) changes in GAAP;
(iv) natural disasters or acts of war; (v) pandemics; (vi) failure to meet
projections; (vii) the announcement of this merger. THE DOLLAR THRESHOLD FOR
MATERIALITY UNDER THIS DEFINITION IS $75,000,000 (SEVENTY-FIVE MILLION DOLLARS)
OR 15% OF THE COMPANY'S CONSOLIDATED NET ASSETS, WHICHEVER IS LESS.

10.2 "Breakup Fee" means One Hundred Twenty-Five Million Dollars ($125,000,000)
payable by the Company to Parent if this Agreement is terminated under Section 7.3.

ARTICLE VII — TERMINATION

7.1 This Agreement may be terminated at any time prior to the Effective Time:
(a) by mutual written consent;
(b) by either party if the Merger has not been consummated by the Outside Date;
(c) by either party if a final, non-appealable order permanently enjoins the Merger.

7.3 Breakup Fee. If this Agreement is terminated by Parent pursuant to
Section 7.1(d) (Company breach), the Company shall pay the Breakup Fee of
$125,000,000 to Parent within two business days.
"""
    content = pad_to_pages(content, 600, "Additional Representations, Warranties, and Covenants")
    with open(os.path.join(OUTPUT_DIR, "merger_agreement_apex_global_systems.txt"), 'w') as f:
        f.write(content)
    print(f"  merger_agreement_apex_global_systems.txt: {len(content)//3000} pages")


# =============================================================================
# DOC 6: COURT OPINION — Motion to Dismiss (500 pages)
# =============================================================================
def gen_court_opinion():
    content = f"""
{'='*80}
UNITED STATES DISTRICT COURT
SOUTHERN DISTRICT OF NEW YORK

Case No. {CASE['docket_no']}

SECURITIES AND EXCHANGE COMMISSION,
    Plaintiff,
v.
MERIDIAN CAPITAL GROUP LLC, et al.,
    Defendants.

MEMORANDUM OPINION AND ORDER

{CASE['judge']}
{TIMELINE['motion_to_dismiss_denied']}
{'='*80}

I. INTRODUCTION

Before the Court is Defendants' Motion to Dismiss the Complaint pursuant to
Federal Rule of Civil Procedure 12(b)(6). For the reasons set forth below,
the Motion is DENIED.

II. BACKGROUND

A. Factual Background

The SEC alleges that between {TIMELINE['trading_period_start']} and
{TIMELINE['trading_period_end']}, Defendants engaged in an insider trading scheme
that generated approximately ${FINANCIALS['total_scheme_profits']:,.0f} in illegal
profits. The scheme centered on trading in Apex Technologies Inc. (NASDAQ: APEX)
common stock and options in advance of the publicly announced merger with Global
Systems Corp.

The SEC alleges that Robert Hartwell, CEO of Meridian Capital Group, received
material non-public information about the Apex merger on {TIMELINE['meridian_tip_received']}
and began trading Apex securities on {TIMELINE['meridian_first_trade']} — fifteen
days before the public announcement on {TIMELINE['apex_merger_announced']}.

B. Procedural Background

The SEC filed this action on {TIMELINE['sec_complaint_filed']}. Defendants filed
the present Motion to Dismiss on {TIMELINE['motion_to_dismiss_filed']}.

III. LEGAL STANDARD

To survive a motion to dismiss under Rule 12(b)(6), a complaint must contain
"enough facts to state a claim to relief that is plausible on its face."
Bell Atlantic Corp. v. Twombly, 550 U.S. 544, 570 (2007). For securities fraud
claims under Section 10(b) and Rule 10b-5, the complaint must additionally plead
scienter with "strong inference." Tellabs, Inc. v. Makor Issues & Rights, Ltd.,
551 U.S. 308, 314 (2007).

IV. ANALYSIS

A. The SEC Has Adequately Pleaded Scienter

Defendants argue that the Complaint fails to plead a "strong inference" of
scienter as required by the Private Securities Litigation Reform Act.

The Court disagrees. The Complaint alleges that:
(1) Hartwell received MNPI about the merger on {TIMELINE['meridian_tip_received']};
(2) Meridian had NEVER previously traded Apex securities;
(3) Beginning just 4 days later on {TIMELINE['meridian_first_trade']}, Meridian
    purchased {FINANCIALS['meridian_apex_shares_peak']:,} shares;
(4) This trading generated ${FINANCIALS['meridian_illegal_profits']:,.0f} in profits;
(5) CFO Sarah Chen confirmed in a sworn declaration that Hartwell directed her to
    "move on APEX immediately, before Thursday announcement."

These allegations, taken together, create a strong inference of scienter that is
"cogent and at least as compelling as any opposing inference." Tellabs, 551 U.S. at 324.

B. Statute of Limitations

Defendants argue the claims are time-barred. Under 28 U.S.C. § 2462, the SEC
must bring an action seeking civil penalties within five years. The Complaint was
filed on {TIMELINE['sec_complaint_filed']}. The alleged violations began on
{TIMELINE['meridian_first_trade']}. The elapsed time is approximately 15 months —
well within the five-year limitations period.

V. CONCLUSION

For the foregoing reasons, Defendants' Motion to Dismiss is DENIED in its entirety.

IT IS SO ORDERED.

Dated: {TIMELINE['motion_to_dismiss_denied']}

_________________________________
{CASE['judge']}
United States District Judge
"""
    content = pad_to_pages(content, 500, "Detailed Analysis and Authorities")
    with open(os.path.join(OUTPUT_DIR, "opinion_motion_to_dismiss.txt"), 'w') as f:
        f.write(content)
    print(f"  opinion_motion_to_dismiss.txt: {len(content)//3000} pages")


# =============================================================================
# DOC 7: EXPERT REPORT (300 pages)
# =============================================================================
def gen_expert_report():
    content = f"""
{'='*80}
UNITED STATES DISTRICT COURT
SOUTHERN DISTRICT OF NEW YORK

Case No. {CLASS_ACTION['docket_no']}
Thornton Pension Fund v. Meridian Capital Group LLC et al.

EXPERT REPORT OF DR. JAMES R. PATTERSON, Ph.D.
Professor of Finance, Columbia Business School

Regarding: Calculation of Class-Wide Damages

Date: {TIMELINE['expert_report_filed']}
{'='*80}

I. QUALIFICATIONS AND ASSIGNMENT

I have been retained by Lead Counsel, {ATTORNEYS['class_counsel']['name']} of
{ATTORNEYS['class_counsel']['firm']}, to calculate damages suffered by the
Settlement Class in connection with Defendants' insider trading in Apex
Technologies Inc. securities.

II. METHODOLOGY

I employ an event study methodology to measure the artificial inflation in
Apex Technologies' stock price caused by Defendants' fraudulent trading.

III. FINDINGS

A. Artificial Inflation

Based on my analysis, the artificial inflation in Apex's stock price attributable
to Defendants' trading activity peaked at $17.28 per share on the date of the
merger announcement ({TIMELINE['apex_merger_announced']}).

B. Affected Shares

During the Class Period ({CLASS_ACTION['class_period_start']} through
{CLASS_ACTION['class_period_end']}), approximately 23.8 million shares of Apex
common stock were traded. After removing Defendants' own trades and other
excluded transactions, the number of damaged shares is approximately 22.4 million.

C. Total Damages Calculation

Total Class Damages = Damaged Shares × Average Inflation Per Share
                    = 22,400,000 × $18.39 (volume-weighted average inflation)
                    = ${FINANCIALS['class_damages_estimated']:,.0f}

D. Per-Share Recovery Under Settlement

Net Settlement Fund: ${FINANCIALS['settlement_amount']:,.0f} - ${FINANCIALS['attorney_fees_amount']:,.0f}
(fees) - $5,000,000 (admin costs) = $264,312,500

Per-Share Recovery = $264,312,500 / 22,400,000 damaged shares
                   ≈ $11.80 per damaged share

Note: The actual per-share recovery of ${FINANCIALS['per_share_recovery']:.2f}
referenced in the Settlement Agreement uses a different denominator (total
Recognized Losses including options), which is why the figures differ.

E. Prejudgment Interest

Calculated at the federal statutory rate from the midpoint of the Class Period
to the date of settlement: approximately $18,400,000.

F. Comparison of Disgorgement vs. Damages

Illegal Profits (Disgorgement):  ${FINANCIALS['total_scheme_profits']:,.0f}
Total Class Damages:             ${FINANCIALS['class_damages_estimated']:,.0f}
Settlement Amount:               ${FINANCIALS['settlement_amount']:,.0f}
Settlement as % of Damages:      {FINANCIALS['settlement_amount']/FINANCIALS['class_damages_estimated']*100:.1f}%

The settlement represents {FINANCIALS['settlement_amount']/FINANCIALS['class_damages_estimated']*100:.1f}%
recovery of estimated total damages, which is well within the range of recoveries
in comparable securities class action settlements.
"""
    content = pad_to_pages(content, 300, "Statistical Appendices and Detailed Calculations")
    with open(os.path.join(OUTPUT_DIR, "expert_report_damages_calculation.txt"), 'w') as f:
        f.write(content)
    print(f"  expert_report_damages_calculation.txt: {len(content)//3000} pages")


# =============================================================================
# DOC 8: FORM ADV (200 pages)
# =============================================================================
def gen_form_adv():
    content = f"""
{'='*80}
FORM ADV — PART 2A: FIRM BROCHURE

MERIDIAN CAPITAL GROUP LLC
CRD Number: 167842
SEC File Number: 801-78945

500 Park Avenue, 32nd Floor
New York, NY 10022
(212) 555-0147

www.meridiancapital.com

This brochure provides information about the qualifications and business practices
of Meridian Capital Group LLC. If you have any questions about the contents of
this brochure, please contact us at compliance@meridiancapital.com.

Date of Brochure: March 31, 2021
{'='*80}

Item 4: Advisory Business

Meridian Capital Group LLC ("Meridian" or the "Firm") is a Delaware limited
liability company founded in 2008. Robert J. Hartwell is the majority owner,
CEO, and Managing Partner.

As of December 31, 2021, Meridian managed approximately ${FINANCIALS['fund_aum_at_time']:,.0f}
in regulatory assets under management on a discretionary basis.

The Firm employs 87 professionals across investment management, operations,
compliance, and technology.

Item 5: Fees and Compensation

Meridian charges the following fees:
- Management Fee: 2.0% per annum of net asset value
- Performance Fee: 20% of net profits above a 6% hurdle rate (high-water mark applies)
- Minimum investment: $5,000,000

Item 6: Performance-Based Fees

Meridian charges performance-based fees as described in Item 5. These fees create
an incentive for the Firm to make riskier investments than would otherwise be the case.

Item 12: Brokerage Practices

Prime Broker: Goldman Sachs & Co. LLC
Custodian: State Street Bank and Trust Company

Item 15: Custody

Client assets are held at State Street Bank and Trust Company. Clients receive
monthly statements directly from the custodian.

Item 17: Voting Client Securities

Meridian votes proxies on behalf of clients in accordance with our Proxy Voting
Policy. A copy is available upon request.

FORM 13F FILING STATUS:
Meridian Capital Group LLC is a Form 13F filer. As an institutional investment
manager exercising investment discretion over accounts holding Section 13(f)
securities with an aggregate fair market value exceeding $100,000,000, Meridian
files Form 13F quarterly with the SEC within 45 days of each calendar quarter end.

Item 18: Financial Information

The Firm has no financial conditions that would impair its ability to meet
contractual commitments to clients.

Item 19: Disciplinary Information

As of the date of this brochure (March 31, 2021), neither the Firm nor any of its
management persons have been subject to any disciplinary events.

NOTE: This Form ADV was filed PRIOR to the SEC enforcement action ({CASE['docket_no']})
filed on {TIMELINE['sec_complaint_filed']}. The disciplinary disclosure in Item 19
is no longer current.
"""
    content = pad_to_pages(content, 200, "Additional Regulatory Disclosures")
    with open(os.path.join(OUTPUT_DIR, "form_adv_meridian_capital.txt"), 'w') as f:
        f.write(content)
    print(f"  form_adv_meridian_capital.txt: {len(content)//3000} pages")


# =============================================================================
# MAIN
# =============================================================================
def main():
    print("="*60)
    print("COHERENT LEGAL BENCHMARK — DOCUMENT GENERATOR")
    print("All docs reference entities from universe.py")
    print("="*60)
    print()

    gen_sec_complaint()
    gen_compliance_manual()
    gen_settlement()
    gen_chen_deposition()
    gen_merger_agreement()
    gen_court_opinion()
    gen_expert_report()
    gen_form_adv()

    total_size = sum(os.path.getsize(os.path.join(OUTPUT_DIR, f)) for f in os.listdir(OUTPUT_DIR))
    total_pages = total_size // 3000
    print(f"\nTOTAL: 8 documents, ~{total_pages:,} pages, {total_size/1e6:.1f} MB")
    print(f"Output: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
