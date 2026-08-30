"""
COHERENT LEGAL UNIVERSE — Single Source of Truth
All tables and documents reference these exact entities, dates, and amounts.
"""

# =============================================================================
# THE CENTRAL CASE: SEC v. Meridian Capital Group
# A securities fraud enforcement action involving insider trading and market
# manipulation around the Apex Technologies / Global Systems Corp merger.
# =============================================================================

CASE = {
    "docket_no": "SDNY-2022-CIV-04851",
    "case_name": "Securities and Exchange Commission v. Meridian Capital Group LLC et al.",
    "short_name": "SEC v. Meridian Capital",
    "filing_date": "2022-06-15",
    "jurisdiction": "SDNY",
    "judge": "Hon. Margaret A. Sullivan",
    "judge_id": "JDG-0087",
    "case_type": "CIV",
    "nature_of_suit": "850",  # Securities/Commodities
    "class_action": True,
}

# Related parallel criminal case
CRIMINAL_CASE = {
    "docket_no": "SDNY-2022-CRM-01247",
    "case_name": "United States v. Robert J. Hartwell",
    "filing_date": "2022-08-03",
    "jurisdiction": "SDNY",
    "judge": "Hon. David R. Nakamura",
    "judge_id": "JDG-0112",
}

# Class action (investor suit)
CLASS_ACTION = {
    "docket_no": "SDNY-2023-CIV-00892",
    "case_name": "Thornton Pension Fund v. Meridian Capital Group LLC",
    "short_name": "Thornton v. Meridian (Class Action)",
    "filing_date": "2023-01-18",
    "jurisdiction": "SDNY",
    "judge": "Hon. Margaret A. Sullivan",
    "judge_id": "JDG-0087",
    "class_action": True,
    "class_period_start": "2021-03-01",
    "class_period_end": "2022-06-14",
    "estimated_class_size": 23847,
}

# =============================================================================
# KEY PARTIES (appear in BOTH tables AND documents)
# =============================================================================

PARTIES = {
    "meridian": {
        "id": "PTY-0000001",
        "name": "Meridian Capital Group LLC",
        "type": "ORG",
        "role": "DEF",  # Defendant
        "state": "NY",
        "country": "US",
        "sic": "6211",  # Security Brokers/Dealers
        "public": False,
        "description": "Hedge fund managing approximately $4.2 billion in assets",
    },
    "hartwell": {
        "id": "PTY-0000002",
        "name": "Robert J. Hartwell",
        "type": "IND",
        "role": "DEF",
        "state": "CT",
        "country": "US",
        "description": "CEO and Managing Partner of Meridian Capital Group",
    },
    "chen": {
        "id": "PTY-0000003",
        "name": "Sarah M. Chen",
        "type": "IND",
        "role": "WIT",  # Cooperating witness
        "state": "NY",
        "country": "US",
        "description": "Former CFO of Meridian Capital Group, cooperating witness",
    },
    "apex": {
        "id": "PTY-0000004",
        "name": "Apex Technologies Inc.",
        "type": "ORG",
        "role": "INT",  # Intervenor (merger target)
        "state": "CA",
        "country": "US",
        "sic": "7372",  # Prepackaged Software
        "public": True,
        "ticker": "APEX",
        "description": "Technology company, target of Global Systems acquisition",
    },
    "global_systems": {
        "id": "PTY-0000005",
        "name": "Global Systems Corp.",
        "type": "ORG",
        "role": "INT",
        "state": "WA",
        "country": "US",
        "sic": "7371",  # Computer Services
        "public": True,
        "ticker": "GSYS",
        "description": "Technology conglomerate, acquirer in the Apex merger",
    },
    "pacific_growth": {
        "id": "PTY-0000006",
        "name": "Pacific Growth Partners LP",
        "type": "ORG",
        "role": "DEF",  # Co-conspirator
        "state": "CA",
        "country": "US",
        "description": "Hedge fund that received tips from Hartwell and traded Apex stock",
    },
    "sec": {
        "id": "PTY-0000007",
        "name": "Securities and Exchange Commission",
        "type": "GOV",
        "role": "PLF",  # Plaintiff in enforcement
        "state": "DC",
        "country": "US",
    },
    "thornton_pension": {
        "id": "PTY-0000008",
        "name": "Thornton Pension Fund",
        "type": "TRT",
        "role": "PLF",  # Lead plaintiff in class action
        "state": "IL",
        "country": "US",
        "description": "Lead plaintiff representing investor class",
    },
    "doj": {
        "id": "PTY-0000009",
        "name": "United States Department of Justice",
        "type": "GOV",
        "role": "PLF",
        "state": "DC",
        "country": "US",
    },
    "marcus_zhang": {
        "id": "PTY-0000010",
        "name": "Marcus D. Zhang",
        "type": "IND",
        "role": "DEF",
        "state": "NY",
        "country": "US",
        "description": "Head Trader at Meridian Capital, executed the fraudulent trades",
    },
}

# =============================================================================
# KEY ATTORNEYS AND LAW FIRMS
# =============================================================================

ATTORNEYS = {
    "williams_thornton": {
        "id": "ATY-00001",
        "name": "James P. Williams",
        "firm": "Williams & Thornton LLP",
        "bar_state": "NY",
        "specialty": "SEC",
        "role": "Defense counsel for Meridian Capital",
    },
    "morrison_lee": {
        "id": "ATY-00002",
        "name": "Katherine Morrison-Lee",
        "firm": "Williams & Thornton LLP",
        "bar_state": "NY",
        "specialty": "CRM",
        "role": "Criminal defense counsel for Hartwell",
    },
    "sec_enforcement": {
        "id": "ATY-00003",
        "name": "David R. Nakamura",
        "firm": "SEC Division of Enforcement",
        "bar_state": "DC",
        "specialty": "SEC",
        "role": "Lead SEC enforcement attorney",
    },
    "class_counsel": {
        "id": "ATY-00004",
        "name": "Rachel Torres",
        "firm": "Bernstein Litowitz Berger & Grossmann LLP",
        "bar_state": "NY",
        "specialty": "CRA",
        "role": "Lead class action counsel for Thornton Pension",
    },
    "chen_counsel": {
        "id": "ATY-00005",
        "name": "Michael R. Oakes",
        "firm": "Davis Wright Tremaine LLP",
        "bar_state": "NY",
        "specialty": "CRM",
        "role": "Personal counsel for Sarah Chen (cooperating witness)",
    },
}

# =============================================================================
# KEY TIMELINE (referenced in BOTH tables AND documents)
# =============================================================================

TIMELINE = {
    # Pre-fraud
    "apex_merger_announced": "2021-03-15",
    "apex_merger_agreement_signed": "2021-03-14",
    "meridian_first_trade": "2021-02-28",  # First suspicious trade (before announcement)
    "meridian_tip_received": "2021-02-22",  # When Hartwell received MNPI
    
    # Trading period
    "trading_period_start": "2021-02-28",
    "trading_period_end": "2022-05-30",
    "pacific_growth_first_trade": "2021-03-01",
    "apex_merger_closed": "2021-09-22",
    "chen_last_day": "2022-04-15",  # Chen resigned
    
    # Investigation and enforcement
    "sec_investigation_opened": "2022-01-10",
    "chen_cooperation_agreement": "2022-05-01",
    "sec_complaint_filed": "2022-06-15",
    "hartwell_arrested": "2022-08-03",
    "criminal_indictment": "2022-08-03",
    "meridian_assets_frozen": "2022-06-16",
    
    # Litigation events
    "motion_to_dismiss_filed": "2022-09-15",
    "motion_to_dismiss_denied": "2023-01-08",
    "class_action_filed": "2023-01-18",
    "class_certification_motion": "2023-06-01",
    "class_certification_granted": "2023-09-15",
    "chen_deposition": "2023-04-12",
    "expert_report_filed": "2023-08-20",
    "summary_judgment_motion": "2024-02-15",
    "summary_judgment_denied": "2024-05-22",
    
    # Settlement
    "settlement_reached": "2024-08-01",
    "settlement_amount": 347500000,  # $347.5 million
    "settlement_preliminary_approval": "2024-09-10",
    "opt_out_deadline": "2024-12-15",
    "settlement_final_approval": "2025-02-28",
    "claims_deadline": "2025-06-30",
    
    # Criminal case
    "hartwell_plea_agreement": "2024-11-15",
    "hartwell_sentencing": "2025-03-20",
    "hartwell_sentence": "84 months",  # 7 years
}

# =============================================================================
# KEY FINANCIAL FIGURES (cross-referenced between tables and docs)
# =============================================================================

FINANCIALS = {
    # Trading profits
    "meridian_illegal_profits": 89700000,  # $89.7 million
    "pacific_growth_illegal_profits": 34200000,  # $34.2 million
    "total_scheme_profits": 123900000,  # $123.9 million
    
    # Positions
    "meridian_apex_shares_peak": 2847000,  # 2.847 million shares of Apex
    "meridian_apex_options_contracts": 15000,  # call options
    "apex_share_price_before": 47.82,  # Before merger announced
    "apex_share_price_after": 78.50,  # After merger announced (day of)
    "apex_merger_price": 84.00,  # Final merger consideration per share
    
    # Damages
    "class_damages_estimated": 412000000,  # Expert report estimate
    "settlement_amount": 347500000,  # $347.5 million
    "attorney_fees_pct": 22.5,  # Percent of settlement
    "attorney_fees_amount": 78187500,  # 22.5% of $347.5M
    "per_share_recovery": 3.42,  # Settlement per damaged share
    "minimum_distribution": 10.00,  # Minimum payout threshold
    
    # Fines and penalties
    "sec_civil_penalty_meridian": 89700000,  # Disgorgement
    "sec_civil_penalty_hartwell": 15000000,  # Personal fine
    "criminal_forfeiture": 42000000,
    "criminal_restitution": 89700000,
    
    # Compliance thresholds from Meridian's own manual
    "compliance_max_position_pct": 8,  # Max 8% of fund in single name
    "compliance_reporting_deadline_hours": 72,  # Must report to CCO within 72 hours
    "compliance_restricted_list_check": True,  # Must check before trading
    "fund_aum_at_time": 4200000000,  # $4.2 billion
    "max_single_position_allowed": 336000000,  # 8% of $4.2B
}

# =============================================================================
# KEY STATUTES AND REGULATIONS CITED
# =============================================================================

STATUTES = {
    "10b5": "15 U.S.C. § 78j(b) and 17 C.F.R. § 240.10b-5 (Securities Fraud)",
    "insider_trading": "15 U.S.C. § 78u-1 (Insider Trading Sanctions Act)",
    "wire_fraud": "18 U.S.C. § 1343 (Wire Fraud)",
    "rico": "18 U.S.C. §§ 1961-1968 (RICO)",
    "rule_10b5_1": "17 C.F.R. § 240.10b5-1 (Trading Plans)",
    "form_13f": "15 U.S.C. § 78m(f) and 17 C.F.R. § 240.13f-1 (Form 13F Reporting)",
    "reg_fd": "17 C.F.R. § 243.100 (Regulation FD — Fair Disclosure)",
    "rule_23": "Fed. R. Civ. P. 23 (Class Actions)",
    "rule_12b6": "Fed. R. Civ. P. 12(b)(6) (Motion to Dismiss)",
    "erie": "Erie Railroad Co. v. Tompkins, 304 U.S. 64 (1938)",
}

# =============================================================================
# DOCUMENT MANIFEST — what each document contains and how it connects
# =============================================================================

DOCUMENTS = {
    "merger_agreement": {
        "filename": "merger_agreement_apex_global_systems.txt",
        "title": "Agreement and Plan of Merger - Apex Technologies Inc. and Global Systems Corp.",
        "pages": 600,
        "key_facts": {
            "parties": ["Apex Technologies Inc.", "Global Systems Corp."],
            "merger_price": "$84.00 per share",
            "mae_threshold": "$75,000,000 or 15% of consolidated net assets",
            "signing_date": "2021-03-14",
            "closing_date": "2021-09-22",
            "breakup_fee": "$125,000,000",
            "excluded_liabilities": "pre-Closing environmental, employee benefit plan, Tax liabilities",
        },
        "connects_to": "tbl_case_mstr (docket), tbl_pty_info (Apex, Global Systems), tbl_evt_log (merger timeline)",
    },
    "sec_complaint": {
        "filename": "sec_complaint_meridian_capital.txt",
        "title": "Complaint - SEC v. Meridian Capital Group LLC et al.",
        "pages": 800,
        "key_facts": {
            "illegal_profits": "$89.7 million (Meridian) + $34.2 million (Pacific Growth) = $123.9 million total",
            "shares_traded": "2,847,000 shares of Apex Technologies",
            "options_contracts": "15,000 call option contracts",
            "tip_date": "February 22, 2021",
            "first_trade": "February 28, 2021 (4 days after receiving tip, 15 days before public announcement)",
            "cooperating_witness": "Sarah M. Chen (CFO)",
            "trading_period": "February 28, 2021 through May 30, 2022",
        },
        "connects_to": "tbl_case_mstr (docket SDNY-2022-CIV-04851), tbl_pty_info (all defendants), tbl_evt_log (filing date), tbl_damages (amounts)",
    },
    "compliance_manual": {
        "filename": "compliance_manual_meridian_capital.txt",
        "title": "Meridian Capital Group LLC — Compliance and Regulatory Procedures Manual (Version 7.3)",
        "pages": 700,
        "key_facts": {
            "max_position_single_name": "8% of fund NAV",
            "reporting_deadline": "72 hours to CCO for any potential violation",
            "restricted_list_check": "MANDATORY before any trade execution",
            "pre_clearance_required": "All personal trades by employees above VP level",
            "escalation_to_board": "48 hours for material compliance failures",
            "annual_certification": "All employees must certify compliance annually by March 31",
            "fund_aum": "$4.2 billion as of December 31, 2021",
        },
        "connects_to": "tbl_case_mstr (shows rules Meridian violated), tbl_evt_log (shows actual violations), tbl_pty_info (Meridian)",
    },
    "settlement_agreement": {
        "filename": "settlement_agreement_thornton_v_meridian.txt",
        "title": "Stipulation and Agreement of Settlement - Thornton Pension Fund v. Meridian Capital Group LLC",
        "pages": 400,
        "key_facts": {
            "settlement_amount": "$347,500,000",
            "class_period": "March 1, 2021 through June 14, 2022",
            "class_size": "approximately 23,847 affected investors",
            "opt_out_deadline": "December 15, 2024",
            "claims_deadline": "June 30, 2025",
            "attorney_fees": "22.5% of Settlement Fund ($78,187,500)",
            "per_share_recovery": "$3.42 per damaged share",
            "minimum_distribution": "$10.00",
            "allocation_formula": "(Claimant's Recognized Loss / Total Recognized Losses) × Net Settlement Fund",
            "lead_plaintiff": "Thornton Pension Fund",
        },
        "connects_to": "tbl_settlement (stl_amt=$347.5M), tbl_case_mstr (class_action docket), tbl_damages (amounts), tbl_pty_info (Thornton)",
    },
    "chen_deposition": {
        "filename": "deposition_sarah_chen.txt",
        "title": "Deposition of Sarah M. Chen, Former CFO — SEC v. Meridian Capital Group",
        "pages": 500,
        "key_facts": {
            "date": "April 12, 2023",
            "key_admission": "Hartwell told her about the Apex merger on February 22, 2021",
            "trades_approved": "47 trades in Apex securities between Feb 28 and March 15, 2021",
            "compliance_failure": "She did NOT check the restricted list before approving trades",
            "email_evidence": "Email dated Feb 23, 2021: 'RH says move on APEX immediately, before Thursday announcement'",
            "board_resolution": "Board Resolution 2021-047 authorized $200M allocation to technology sector",
            "resignation_date": "April 15, 2022",
        },
        "connects_to": "tbl_evt_log (deposition date, specific trades), tbl_pty_info (Chen, Hartwell), tbl_case_pty_atty (her counsel)",
    },
    "court_opinion_mtd": {
        "filename": "opinion_motion_to_dismiss.txt",
        "title": "Memorandum Opinion and Order on Defendants' Motion to Dismiss — SEC v. Meridian Capital",
        "pages": 500,
        "key_facts": {
            "ruling": "Motion to Dismiss DENIED",
            "ruling_date": "January 8, 2023",
            "key_holding": "SEC adequately pleaded scienter through the pattern of trading immediately after receipt of MNPI",
            "statute_of_limitations": "5-year SOL under 28 U.S.C. § 2462 for disgorgement; complaint filed within period",
            "erie_analysis": "Not applicable — federal question jurisdiction (15 U.S.C. § 78j(b))",
            "precedent_cited": "Tellabs, Inc. v. Makor Issues & Rights, Ltd., 551 U.S. 308 (2007)",
        },
        "connects_to": "tbl_ruling (ruling_cd=DNY for MTD), tbl_statute_cite (15 USC 78j(b)), tbl_evt_log (ruling date)",
    },
    "expert_report": {
        "filename": "expert_report_damages_calculation.txt",
        "title": "Expert Report of Dr. James R. Patterson — Damages Calculation",
        "pages": 300,
        "key_facts": {
            "total_damages_estimated": "$412,000,000",
            "methodology": "Event study measuring artificial inflation in Apex stock price",
            "inflation_per_share_peak": "$17.28 per share (at announcement)",
            "affected_shares": "approximately 23.8 million shares traded during class period",
            "disgorgement_calculation": "Meridian profits ($89.7M) + Pacific Growth profits ($34.2M) = $123.9M",
            "prejudgment_interest": "$18.4 million (calculated at federal statutory rate)",
        },
        "connects_to": "tbl_damages (amt_sought, amt_awarded), tbl_claim (securities fraud claim), FINANCIALS constants",
    },
    "regulatory_filing": {
        "filename": "form_adv_meridian_capital.txt",
        "title": "Form ADV Part 2A — Meridian Capital Group LLC (Brochure)",
        "pages": 200,
        "key_facts": {
            "aum": "$4,200,000,000 as of December 31, 2021",
            "number_of_employees": 87,
            "investment_strategy": "Event-driven equity, merger arbitrage, and special situations",
            "fee_structure": "2% management fee, 20% performance fee above 6% hurdle",
            "custody": "Goldman Sachs & Co. (prime broker) and State Street (custodian)",
            "form_13f_filer": "Yes (AUM exceeds $100 million threshold)",
            "regulatory_history": "No prior disciplinary actions (as of filing date)",
        },
        "connects_to": "tbl_pty_info (Meridian details), tbl_case_mstr (amt_in_controversy), FINANCIALS",
    },
}
