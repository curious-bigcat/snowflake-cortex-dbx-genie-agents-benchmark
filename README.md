# Cortex Agent vs Databricks Genie -- AI Agent Benchmark

Comparative benchmark of **Snowflake Cortex Agent** vs **Databricks Genie** on complex, multi-source financial services workloads.

## Benchmark: CRE Portfolio Stress & Workout

**Scenario:** Pacific Northwest Bank (PNB), a $28B regional bank, aggressively grew its CRE lending book from $3.2B to $8.7B (2019-2022). A 2023 office market crash (vacancy 12% to 31%) triggers cascading defaults, an OCC Consent Order, and a $2.1B workout pipeline.

**Dataset:** 3.6M rows across 18 tables, 30 documents (23 synthetic + 7 real regulatory PDFs)

## Results (Measured)

| Metric | Cortex Agent | Databricks Genie | Delta |
|---|---|---|---|
| Accuracy | 95% | 55% | +40pp |
| Groundedness | 100% (0 hallucinations) | 71% (35 ungrounded claims) | +29pp |
| Avg Latency | 41s | 255s | 6.2x faster |
| Tool Calls | 35 | 74 | 2.1x fewer |
| Tool Success Rate | 94% | 76% | +18pp |
| Doc Retrieval | 100% (5/5) | 0% (0/13) | Complete failure |

Cortex latency and tokens measured from `SNOWFLAKE.ACCOUNT_USAGE.SNOWFLAKE_COWORK_USAGE_HISTORY`. Databricks latency and tokens measured from agent trace spans. See `reports/cre_benchmark_report.md` for full methodology and per-question detail.

## Repository Structure

```
genie_cortex/
├── README.md
├── config/
│   ├── cortex_agent/
│   │   ├── cre_semantic_view.sql   # Semantic View DDL (18 tables, VQRs, metrics)
│   │   └── cre_setup_guide.md      # Snowflake setup (tables, search, agent)
│   └── genie_agent/
│       └── cre_setup_guide.md      # Databricks setup (3-agent hierarchy)
├── data/cre/
│   ├── tables/                     # 18 parquet files (3.6M rows)
│   └── docs/
│       ├── bank_documents/         # 13 internal bank documents
│       ├── case_files/             # 10 case-specific documents
│       └── real_regulations/       # 7 real OCC/FDIC/Fed regulatory PDFs
├── questions/
│   └── cre_benchmark_questions.md  # 10 benchmark questions (G01-G10)
└── reports/
    ├── cre_benchmark_report.md     # Full comparison report
    └── cre_charts/                 # 8 PNG charts (brand-colored)
```

## Tables (18 tables, 3.6M rows)

| Table | Rows | Description |
|-------|------|-------------|
| tbl_loan_mstr | 45,005 | Master loan records (the anchor table) |
| tbl_borrower | 12,000 | Borrower entities |
| tbl_collateral | 36,165 | Collateral properties with appraisal values |
| tbl_appraisal | 107,060 | Appraisal history (multiple per property) |
| tbl_payment | 1,807,511 | Monthly loan payments |
| tbl_covenant | 94,302 | Loan covenants (DSCR, LTV, occupancy, etc.) |
| tbl_covenant_test | 903,972 | Covenant compliance test results |
| tbl_risk_rating | 142,167 | Risk rating migration history |
| tbl_provision | 177,259 | ALLL/CECL provision calculations |
| tbl_workout | 3,504 | Loan workout/restructuring records |
| tbl_reo | 613 | Real estate owned (foreclosed properties) |
| tbl_charge_off | 1,943 | Loan charge-offs and recoveries |
| tbl_exam_finding | 3,500 | OCC/internal audit examination findings |
| tbl_capital | 26 | Quarterly capital adequacy snapshots |
| tbl_concentration | 208 | Portfolio concentration metrics by segment |
| tbl_branch | 29 | Bank branches (PNW region) |
| tbl_analyst | 350 | Loan officers and credit analysts |
| tbl_audit_log | 278,600 | Internal audit trail |

All coded columns use abbreviated values (e.g., `loan_typ_cd`: CRE_OFFC, CRE_MLTF; `risk_rtg_cd`: 1-PASS through 8-LOSS; `loan_sts_cd`: ACTV, DLQ30, NACC, WKOT, FCLS, CHGOFF).

## Documents (30 files)

### Bank Documents (13 files)

| File | Description |
|------|-------------|
| credit_committee_memo_cascadia_tower.txt | Credit committee approval for $85M Cascadia Tower loan |
| appraisal_report_cascadia_tower_2023.txt | JLL reappraisal: 40.5% value decline ($131M to $78M) |
| occ_consent_order_2023_ce_0847.txt | OCC Consent Order: 420% CRE concentration, 23% UW exceptions, ALLL shortfall |
| internal_audit_report_cre_lending_2023.txt | Internal audit: 23% exception rate with branch-level breakdown |
| board_risk_committee_minutes_q4_2023.txt | Board minutes: consent order response, capital plan, dividend suspension |
| alll_methodology_memo_2023.txt | ALLL methodology with Q-factor history and segment-level reserves |
| stress_test_severe_adverse_2023.txt | Stress test: CET1 projected to 6.1% under severe adverse |
| regulatory_capital_plan_occ_submission.txt | Capital plan: $175M sub debt + $412M loan sale + RWA optimization |
| credit_risk_review_annual_2023.txt | Annual review: 34% of CRE office rated SM+ (up from 6% in 2021) |
| appraiser_engagement_letter.txt | JLL engagement for portfolio-wide reappraisal of 180 properties |
| board_resolution_dividend_suspension.txt | Board resolution suspending quarterly dividend |
| examiner_report_capital_adequacy.txt | OCC examiner capital review: rating 3 (Less Than Satisfactory) |
| environmental_phase1_cascadia_tower.txt | Phase I ESA for Cascadia Tower (clean report) |

### Case Files (10 files)

| File | Description |
|------|-------------|
| covenant_compliance_letter_cascadia_q3_2023.txt | Breach notice: 4 covenant violations on Cascadia Tower |
| workout_proposal_cascadia_tower.txt | Restructuring: $16.5M principal reduction, maturity extension |
| borrower_financials_cascadia_holdings.txt | Cascadia Holdings operating statement: NOI collapse ($10.2M to $0.4M) |
| foreclosure_timeline_mercer_industrial.txt | 18-month foreclosure timeline for $32M Mercer Industrial Park |
| loan_sale_term_sheet_performing_pool.txt | $412M loan pool sale to Blackstone at 92 cents on dollar |
| non_accrual_memo_cedar_point.txt | Non-accrual recommendation for $19M Cedar Point Office Complex |
| modification_agreement_pacific_heights.txt | Loan mod for $28M multifamily: rate reduction, maturity extension |
| participation_agreement_seattle_mixed_use.txt | $40M participation in $200M JPMorgan-led construction loan |
| insurance_claim_correspondence_retail.txt | Earthquake damage claim on Willamette River Plaza |
| sec_filing_pnb_annual_report_excerpts.txt | PNB 10-K excerpts: risk factors, consent order disclosure |

### Real Regulations (7 PDF files)

| File | Description |
|------|-------------|
| occ_comptrollers_handbook_cre_lending.pdf | OCC Comptroller's Handbook: Commercial Real Estate Lending (v2.0) |
| occ_concentrations_of_credit_handbook.pdf | OCC Comptroller's Handbook: Concentrations of Credit |
| fed_sr07_1_cre_concentration_guidance.pdf | Federal Reserve SR 07-1: CRE Concentration Guidance (300% threshold) |
| interagency_cre_workout_policy_2023.pdf | Interagency Policy: CRE Loan Accommodations and Workouts (2023) |
| interagency_appraisal_evaluation_guidelines.pdf | Interagency Appraisal and Evaluation Guidelines |
| fdic_rms_section_3_2_loans.pdf | FDIC Risk Management Manual Section 3.2: Loans |
| occ_rating_credit_risk_handbook.pdf | OCC Comptroller's Handbook: Rating Credit Risk |

## Complexity Traps

The dataset includes deliberate complexity traps that test whether AI agents can handle real-world banking data:

1. **Multi-status join trap**: A loan can have status WKOT in tbl_loan_mstr but still have active covenant tests
2. **Appraisal vintage trap**: Multiple appraisals per property; must use the latest (max appr_dt), not the first
3. **DSCR-by-property-type**: Covenant thresholds differ by property type; must join through loan -> collateral -> property type
4. **Concentration denominator**: CRE concentration = CRE exposure / total capital (not total assets)
5. **Charge-off vs provision**: Net charge-offs != provision expense; must subtract recoveries
6. **Office code mismatch**: "Office portfolio" = prop_typ_cd='OFFC' in tbl_collateral, but loan_typ_cd='CRE_OFFC' in tbl_loan_mstr

## Benchmark Questions (G01-G10)

Each question is a complex, multi-part query requiring SQL across multiple tables AND document retrieval AND domain reasoning.

### G01: Office Portfolio Health + OCC Concentration Guidance

> What is PNB's total CRE office loan exposure, what percentage of those loans are rated Special Mention (5-SS) or worse, and what does the OCC's interagency guidance (SR 07-1) say about the CRE concentration threshold relative to capital? Is PNB in breach?

| Type | Source |
|------|--------|
| Tables | tbl_loan_mstr, tbl_concentration, tbl_capital |
| Documents | fed_sr07_1_cre_concentration_guidance.pdf, occ_consent_order_2023_ce_0847.txt |
| Trap | Must use loan_typ_cd='CRE_OFFC' (not prop_typ_cd); concentration is % of capital, not assets |

### G02: Cascadia Tower Full Credit Analysis

> For loan CRE-2021-00847 (Cascadia Tower), show me: (a) the original vs current appraisal value and LTV, (b) the DSCR covenant test history for the last 6 quarters, (c) the workout proposal terms including the proposed haircut percentage, and (d) the borrower's NOI trend from 2021 to 2023.

| Type | Source |
|------|--------|
| Tables | tbl_loan_mstr, tbl_collateral, tbl_appraisal, tbl_covenant, tbl_covenant_test, tbl_workout |
| Documents | credit_committee_memo_cascadia_tower.txt, appraisal_report_cascadia_tower_2023.txt, workout_proposal_cascadia_tower.txt, borrower_financials_cascadia_holdings.txt |
| Trap | Appraisal vintage (must use MAX date); this loan has no DSCR covenant in data (only ICR/Debt Yield); NOI only exists in documents |

### G03: ALLL Adequacy + Q-Factor Justification

> What is the total ALLL provision for CRE office loans, what effective loss rate does that imply (including Q-factor adjustments), and how does the ALLL methodology memo justify the Q4 2023 Q-factor increase to 3.50% for office? What was the OCC's assessment of the ALLL shortfall?

| Type | Source |
|------|--------|
| Tables | tbl_provision, tbl_loan_mstr |
| Documents | alll_methodology_memo_2023.txt, occ_consent_order_2023_ce_0847.txt, examiner_report_capital_adequacy.txt |
| Trap | Must deduplicate provisions (multiple per loan); Q-factor history is in docs, not data; $45-65M shortfall only in consent order |

### G04: Covenant Breach Cascade + Workout Outcomes

> How many CRE loans had DSCR covenant breaches in 2023 that were NOT waived? Of those, how many ended up in workout, foreclosure, or charge-off? Show the resolution breakdown with total dollar amounts.

| Type | Source |
|------|--------|
| Tables | tbl_covenant, tbl_covenant_test, tbl_loan_mstr, tbl_workout, tbl_charge_off |
| Documents | interagency_cre_workout_policy_2023.pdf |
| Trap | Must join covenant_test -> covenant (filter DSCR) -> loan; count DISTINCT loans not test rows; waiver_flg='N' means breach stands |

### G05: Capital Impact + Stress Test

> Trace PNB's CET1 ratio from year-end 2021 to the most recent quarter. What were the key drivers of the 330 bps deterioration? Under the severe adverse stress scenario, what would CET1 fall to, and does the capital plan restore it above well-capitalized thresholds?

| Type | Source |
|------|--------|
| Tables | tbl_capital, tbl_charge_off, tbl_provision |
| Documents | stress_test_severe_adverse_2023.txt, regulatory_capital_plan_occ_submission.txt, examiner_report_capital_adequacy.txt, occ_consent_order_2023_ce_0847.txt |
| Trap | CET1 trajectory from table, but drivers (charge-offs, provisions, dividends) require documents; stress projection (6.1%) and post-mitigation (7.8%) only in docs |

### G06: Recovery Analysis by Property Type

> For all charged-off CRE loans, what is the total gross charge-off amount, total recoveries, and net loss rate by property type? Which property type had the highest loss severity?

| Type | Source |
|------|--------|
| Tables | tbl_charge_off, tbl_loan_mstr, tbl_collateral |
| Documents | occ_comptrollers_handbook_cre_lending.pdf |
| Trap | Net = gross minus recoveries (not just gross); property type via tbl_collateral.prop_typ_cd, not tbl_loan_mstr.loan_typ_cd |

### G07: Underwriting Exception Analysis by Branch

> The internal audit found 23% of CRE originations in 2021-2022 had underwriting exceptions. Which 3 branches had the highest exception rates? What types of exceptions were most common? How does the OCC consent order address underwriting deficiencies?

| Type | Source |
|------|--------|
| Tables | tbl_loan_mstr, tbl_branch, tbl_analyst |
| Documents | internal_audit_report_cre_lending_2023.txt, occ_consent_order_2023_ce_0847.txt |
| Trap | Must filter CRE loans in 2021-2022; exception types are in the document (the table only has Y/N flag); OCC Article V remediation from consent order |

### G08: REO Portfolio Analysis

> What are PNB's total REO properties, their aggregate carrying cost, and average time held? Which specific REO property had the largest loss on disposition? For unsold REO, what is the total exposure?

| Type | Source |
|------|--------|
| Tables | tbl_reo, tbl_collateral, tbl_loan_mstr |
| Documents | foreclosure_timeline_mercer_industrial.txt |
| Trap | sale_dt/sale_val are NULL for unsold properties; loss = sale_val - acq_val - carrying_cost (must include carrying costs); unsold exposure = acq_val + carrying_cost where sale_dt IS NULL |

### G09: Examination Finding Remediation Status

> How many MRIA-level findings from OCC examinations are still open or in-progress? What categories do they fall into? What are the remediation deadlines per the consent order, and how many are past due?

| Type | Source |
|------|--------|
| Tables | tbl_exam_finding |
| Documents | occ_consent_order_2023_ce_0847.txt, examiner_report_capital_adequacy.txt |
| Trap | Filter severity_cd='MRIA' AND remediation_sts_cd != 'CLOSED'; consent order Article VI sets 180-day MRIA deadline; "past due" = due_dt < CURRENT_DATE and still open |

### G10: Loan Sale Impact on Capital

> If PNB sells the $412M performing CRE loan pool at 92 cents on the dollar per the term sheet, what is the projected loss? How would that impact the CET1 ratio? Factor in the RWA reduction.

| Type | Source |
|------|--------|
| Tables | tbl_capital, tbl_concentration, tbl_loan_mstr |
| Documents | loan_sale_term_sheet_performing_pool.txt, regulatory_capital_plan_occ_submission.txt, occ_consent_order_2023_ce_0847.txt |
| Trap | Loss = $412M x 8% = $33M (reduces CET1); RWA reduction ~$400M (improves ratio); must calculate both sides; capital plan doc says +0.4% net CET1 impact |
