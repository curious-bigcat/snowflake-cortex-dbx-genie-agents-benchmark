# Cortex Agent vs Databricks Genie -- AI Agent Benchmark

Comparative benchmark of **Snowflake Cortex Agent** vs **Databricks Genie** on complex financial services workloads using a synthetic CRE (Commercial Real Estate) lending dataset.

## Benchmark: CRE Portfolio Stress & Workout

**Scenario:** Pacific Northwest Bank (PNB), a $28B regional bank, aggressively grew its CRE lending book from $3.2B to $8.7B (2019-2022). A 2023 office market crash (vacancy 12% to 31%) triggers cascading defaults, an OCC Consent Order, and a $2.1B workout pipeline.

**Dataset:** 3.6M rows across 18 tables, 30 documents (23 synthetic + 7 real regulatory PDFs)

**Questions:** 10 single complex queries, each targeting a specific agent weakness -- filter precision, aggregation traps, column confusion, join chains, NULL handling, and doc-data reconciliation.

## Platform Setup

Both platforms received identical data. Setup guides for each:

| Platform | Guide | Key Configuration |
|----------|-------|-------------------|
| Snowflake Cortex Agent | [config/cortex_agent/cre_setup_guide.md](config/cortex_agent/cre_setup_guide.md) | Semantic View ([DDL](config/cortex_agent/cre_semantic_view.sql)) + Cortex Search Service |
| Databricks Genie | [config/genie_agent/cre_setup_guide.md](config/genie_agent/cre_setup_guide.md) | 3-agent hierarchy: Supervisor + Genie SQL + Knowledge Assistant |

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
│   ├── verify_ground_truth.py      # Ground truth verification script
│   └── docs/
│       ├── bank_documents/         # 13 internal bank documents
│       ├── case_files/             # 10 case-specific documents
│       └── real_regulations/       # 7 real OCC/FDIC/Fed regulatory PDFs
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
| occ_consent_order_2023_ce_0847.txt | OCC Consent Order: 420% CRE concentration, 23% UW exceptions, ALLL shortfall |
| alll_methodology_memo_2023.txt | ALLL methodology with Q-factor history and segment-level reserves |
| stress_test_severe_adverse_2023.txt | Stress test: CET1 projected to 6.1% under severe adverse |
| regulatory_capital_plan_occ_submission.txt | Capital plan: $175M sub debt + $412M loan sale + RWA optimization |
| credit_committee_memo_cascadia_tower.txt | Credit committee approval for $85M Cascadia Tower loan |
| appraisal_report_cascadia_tower_2023.txt | JLL reappraisal: 40.5% value decline ($131M to $78M) |
| internal_audit_report_cre_lending_2023.txt | Internal audit: 23% exception rate with branch-level breakdown |
| board_risk_committee_minutes_q4_2023.txt | Board minutes: consent order response, capital plan, dividend suspension |
| credit_risk_review_annual_2023.txt | Annual review: 34% of CRE office rated SM+ (up from 6% in 2021) |
| examiner_report_capital_adequacy.txt | OCC examiner capital review: rating 3 (Less Than Satisfactory) |
| appraiser_engagement_letter.txt | JLL engagement for portfolio-wide reappraisal of 180 properties |
| board_resolution_dividend_suspension.txt | Board resolution suspending quarterly dividend |
| environmental_phase1_cascadia_tower.txt | Phase I ESA for Cascadia Tower (clean report) |

### Case Files (10 files)

| File | Description |
|------|-------------|
| loan_sale_term_sheet_performing_pool.txt | $412M loan pool sale to Blackstone at 92 cents on dollar |
| workout_proposal_cascadia_tower.txt | Restructuring: $16.5M principal reduction, maturity extension |
| borrower_financials_cascadia_holdings.txt | Cascadia Holdings operating statement: NOI collapse ($10.2M to $0.4M) |
| foreclosure_timeline_mercer_industrial.txt | 18-month foreclosure timeline for $32M Mercer Industrial Park |
| covenant_compliance_letter_cascadia_q3_2023.txt | Breach notice: 4 covenant violations on Cascadia Tower |
| non_accrual_memo_cedar_point.txt | Non-accrual recommendation for $19M Cedar Point Office Complex |
| modification_agreement_pacific_heights.txt | Loan mod for $28M multifamily: rate reduction, maturity extension |
| participation_agreement_seattle_mixed_use.txt | $40M participation in $200M JPMorgan-led construction loan |
| insurance_claim_correspondence_retail.txt | Earthquake damage claim on Willamette River Plaza |
| sec_filing_pnb_annual_report_excerpts.txt | PNB 10-K excerpts: risk factors, consent order disclosure |

### Real Regulations (7 PDF files)

| File | Description |
|------|-------------|
| fed_sr07_1_cre_concentration_guidance.pdf | Federal Reserve SR 07-1: CRE Concentration Guidance (300% threshold) |
| occ_comptrollers_handbook_cre_lending.pdf | OCC Comptroller's Handbook: Commercial Real Estate Lending (v2.0) |
| occ_concentrations_of_credit_handbook.pdf | OCC Comptroller's Handbook: Concentrations of Credit |
| interagency_cre_workout_policy_2023.pdf | Interagency Policy: CRE Loan Accommodations and Workouts (2023) |
| interagency_appraisal_evaluation_guidelines.pdf | Interagency Appraisal and Evaluation Guidelines |
| fdic_rms_section_3_2_loans.pdf | FDIC Risk Management Manual Section 3.2: Loans |
| occ_rating_credit_risk_handbook.pdf | OCC Comptroller's Handbook: Rating Credit Risk |

## Complexity Traps

The dataset includes deliberate complexity traps that test whether AI agents can handle real-world banking data:

1. **Filter precision**: OCC exam findings table includes INT_AUDIT, EXT_AUDIT, BOARD_REV -- must filter to OCC types only
2. **Aggregation trap**: Provision table stores daily snapshots since 2019 -- summing all records gives $67B vs memo's $167.5M
3. **Column confusion**: Capital table has both `cet1_ratio` and `tier1_ratio` -- CET1 capital must be derived as ratio x RWA, not from `tier1_cap`
4. **Covenant type trap**: Cascadia Tower has ICR and DEBT_YLD covenants, not DSCR -- agent must read data, not assume
5. **NULL handling**: REO properties have NULL `sale_dt`/`sale_val` for unsold -- must handle correctly
6. **Doc-data hybrid**: Underwriting exception types are in audit document only, not in the database (table only has Y/N flag)
7. **4-table join**: DSCR by occupancy requires loan_mstr -> collateral -> covenant -> covenant_test with occupancy as 0-1 decimal
8. **Scale mismatch**: Database balances ($167B) vs memo balances ($3.85B) -- agent must flag, not silently use one

## Getting Started

1. Load the 18 parquet files from `data/cre/tables/` into your platform
2. Upload the 30 documents from `data/cre/docs/` to your document store
3. Follow the setup guide for your platform (`config/cortex_agent/` or `config/genie_agent/`)
4. Run the benchmark questions against both agents and compare results
