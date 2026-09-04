-- =============================================================================
-- CRE Benchmark Semantic View
-- Pacific Northwest Bank - CRE Portfolio Stress & Workout
-- =============================================================================
-- This semantic view provides the Cortex Analyst with full business context
-- for all 18 tables, including coded column decode mappings, relationships,
-- metrics, and verified queries for complex join patterns.
-- =============================================================================

CREATE OR REPLACE SEMANTIC VIEW CRE_BENCHMARK_DB.CRE.CRE_SEMANTIC_VIEW

  -- =========================================================================
  -- TABLES
  -- =========================================================================

  TABLES (
    CRE_BENCHMARK_DB.CRE.TBL_LOAN_MSTR
      PRIMARY KEY (loan_id)
      COMMENT = 'Master table of all loans. Each row is one loan. This is the central table -- most other tables join to it via loan_id. IMPORTANT: prop_typ_cd is NULL for non-CRE loans (CNI, RESI). To filter for CRE office loans, use loan_typ_cd = ''CRE_OFFC'' in this table, OR join to TBL_COLLATERAL and filter on prop_typ_cd = ''OFFC'' there. These are DIFFERENT columns in DIFFERENT tables.',

    CRE_BENCHMARK_DB.CRE.TBL_BORROWER
      PRIMARY KEY (borrower_id)
      COMMENT = 'Borrower entity records. Each borrower can have multiple loans.',

    CRE_BENCHMARK_DB.CRE.TBL_COLLATERAL
      PRIMARY KEY (collateral_id)
      COMMENT = 'Collateral property records. A CRE loan may have 1-2 collateral properties. IMPORTANT: This table has prop_typ_cd for property-level type (OFFC, MLTF, etc.), which is DIFFERENT from loan_typ_cd in TBL_LOAN_MSTR. Use this table to filter by property type when you need property-level details. Use curr_appr_val for current values, not orig_appr_val.',

    CRE_BENCHMARK_DB.CRE.TBL_APPRAISAL
      PRIMARY KEY (appraisal_id)
      COMMENT = 'Appraisal history for collateral properties. IMPORTANT: Each property has MULTIPLE appraisals over time. To get the CURRENT appraisal, use the one with MAX(appr_dt) per collateral_id. Do NOT use the first row.',

    CRE_BENCHMARK_DB.CRE.TBL_PAYMENT
      PRIMARY KEY (payment_id)
      COMMENT = 'Monthly loan payment records. Largest table (~1.8M rows). Each row is one monthly payment for one loan.',

    CRE_BENCHMARK_DB.CRE.TBL_COVENANT
      PRIMARY KEY (covenant_id)
      COMMENT = 'Loan covenant definitions. Each CRE loan has 2-4 covenants. The covenants set minimum/maximum thresholds that are tested periodically (see TBL_COVENANT_TEST).',

    CRE_BENCHMARK_DB.CRE.TBL_COVENANT_TEST
      PRIMARY KEY (test_id)
      COMMENT = 'Covenant compliance test results. Each test compares the actual value against the covenant threshold. A FAIL means the borrower breached the covenant.',

    CRE_BENCHMARK_DB.CRE.TBL_RISK_RATING
      PRIMARY KEY (rating_id)
      COMMENT = 'Risk rating change history for loans. Tracks upgrades and downgrades over time.',

    CRE_BENCHMARK_DB.CRE.TBL_PROVISION
      PRIMARY KEY (provision_id)
      COMMENT = 'ALLL/CECL provision calculations for loans. Each row is one quarterly provision calculation.',

    CRE_BENCHMARK_DB.CRE.TBL_WORKOUT
      PRIMARY KEY (workout_id)
      COMMENT = 'Loan workout and restructuring records. Only distressed loans (status WKOT, FCLS, REO, DFLT, NACC) have workout records.',

    CRE_BENCHMARK_DB.CRE.TBL_REO
      PRIMARY KEY (reo_id)
      COMMENT = 'Properties acquired through foreclosure (REO). Tracks acquisition value, carrying costs, and current status (HELD, LISTED, UNDER_CONTRACT, SOLD).',

    CRE_BENCHMARK_DB.CRE.TBL_CHARGE_OFF
      PRIMARY KEY (chargeoff_id)
      COMMENT = 'Loan charge-off and recovery records. IMPORTANT: Net charge-off = co_amt - recovery_amt. Do NOT report gross charge-offs as the loss amount without subtracting recoveries.',

    CRE_BENCHMARK_DB.CRE.TBL_EXAM_FINDING
      PRIMARY KEY (finding_id)
      COMMENT = 'OCC and internal audit examination findings. Each finding has a severity level and remediation status.',

    CRE_BENCHMARK_DB.CRE.TBL_CAPITAL
      PRIMARY KEY (capital_id)
      COMMENT = 'Quarterly capital adequacy snapshots. Well-capitalized thresholds: CET1 >= 7.0%, Tier 1 >= 8.0%, Total Capital >= 10.0%, Leverage >= 5.0%.',

    CRE_BENCHMARK_DB.CRE.TBL_CONCENTRATION
      PRIMARY KEY (conc_id)
      COMMENT = 'Portfolio concentration metrics by segment. IMPORTANT: CRE concentration is measured as CRE exposure divided by TOTAL CAPITAL (Tier 1 + Tier 2), NOT total assets. The 300% regulatory threshold from SR 07-1 is based on capital, not assets.',

    CRE_BENCHMARK_DB.CRE.TBL_BRANCH
      PRIMARY KEY (branch_cd)
      COMMENT = 'PNB bank branches across the Pacific Northwest.',

    CRE_BENCHMARK_DB.CRE.TBL_ANALYST
      PRIMARY KEY (analyst_id)
      COMMENT = 'Loan officers and credit analysts.',

    CRE_BENCHMARK_DB.CRE.TBL_AUDIT_LOG
      PRIMARY KEY (audit_id)
      COMMENT = 'Internal audit trail of actions taken on loans.'
  )

  -- =========================================================================
  -- RELATIONSHIPS
  -- =========================================================================

  RELATIONSHIPS (
    TBL_LOAN_MSTR (borrower_id) REFERENCES TBL_BORROWER (borrower_id),
    TBL_LOAN_MSTR (branch_cd) REFERENCES TBL_BRANCH (branch_cd),
    TBL_LOAN_MSTR (analyst_id) REFERENCES TBL_ANALYST (analyst_id),
    TBL_COLLATERAL (loan_id) REFERENCES TBL_LOAN_MSTR (loan_id),
    TBL_APPRAISAL (collateral_id) REFERENCES TBL_COLLATERAL (collateral_id),
    TBL_PAYMENT (loan_id) REFERENCES TBL_LOAN_MSTR (loan_id),
    TBL_COVENANT (loan_id) REFERENCES TBL_LOAN_MSTR (loan_id),
    TBL_COVENANT_TEST (covenant_id) REFERENCES TBL_COVENANT (covenant_id),
    TBL_RISK_RATING (loan_id) REFERENCES TBL_LOAN_MSTR (loan_id),
    TBL_PROVISION (loan_id) REFERENCES TBL_LOAN_MSTR (loan_id),
    TBL_WORKOUT (loan_id) REFERENCES TBL_LOAN_MSTR (loan_id),
    TBL_REO (loan_id) REFERENCES TBL_LOAN_MSTR (loan_id),
    TBL_REO (collateral_id) REFERENCES TBL_COLLATERAL (collateral_id),
    TBL_CHARGE_OFF (loan_id) REFERENCES TBL_LOAN_MSTR (loan_id),
    TBL_AUDIT_LOG (loan_id) REFERENCES TBL_LOAN_MSTR (loan_id),
    TBL_ANALYST (branch_cd) REFERENCES TBL_BRANCH (branch_cd),
    TBL_RISK_RATING (analyst_id) REFERENCES TBL_ANALYST (analyst_id)
  )

  -- =========================================================================
  -- FACTS (numeric columns used in aggregation)
  -- =========================================================================

  FACTS (
    -- TBL_LOAN_MSTR
    TBL_LOAN_MSTR.orig_amt AS orig_amt
      COMMENT = 'Original loan amount in dollars.',
    TBL_LOAN_MSTR.curr_bal AS curr_bal
      COMMENT = 'Current outstanding balance in dollars.',
    TBL_LOAN_MSTR.int_rate AS int_rate
      COMMENT = 'Current interest rate as a percentage (e.g., 5.25 means 5.25%).',

    -- TBL_COLLATERAL
    TBL_COLLATERAL.sqft AS sqft
      COMMENT = 'Total square footage.',
    TBL_COLLATERAL.orig_appr_val AS orig_appr_val
      COMMENT = 'Original appraised value at loan origination (dollars).',
    TBL_COLLATERAL.curr_appr_val AS curr_appr_val
      COMMENT = 'Most recent appraised value (dollars). For current LTV, use curr_bal / curr_appr_val.',
    TBL_COLLATERAL.ltv_orig AS ltv_orig
      COMMENT = 'Loan-to-value ratio at origination (decimal, e.g., 0.65 = 65%).',
    TBL_COLLATERAL.ltv_curr AS ltv_curr
      COMMENT = 'Current loan-to-value ratio (decimal). Values above 1.0 mean the loan is underwater.',
    TBL_COLLATERAL.occup_rate AS occup_rate
      COMMENT = 'Current occupancy rate (decimal, e.g., 0.38 = 38%).',

    -- TBL_APPRAISAL
    TBL_APPRAISAL.appr_val AS appr_val
      COMMENT = 'Appraised value in dollars.',

    -- TBL_PAYMENT
    TBL_PAYMENT.pmt_amt AS pmt_amt
      COMMENT = 'Total payment amount (dollars). Zero for missed payments.',
    TBL_PAYMENT.prin_amt AS prin_amt
      COMMENT = 'Principal portion of payment.',
    TBL_PAYMENT.int_amt AS int_amt
      COMMENT = 'Interest portion of payment.',
    TBL_PAYMENT.days_past_due AS days_past_due
      COMMENT = 'Number of days past due. 0=current, 30/60/90/120/150/180 for delinquent.',

    -- TBL_COVENANT
    TBL_COVENANT.threshold_val AS threshold_val
      COMMENT = 'Covenant threshold value. For DSCR/ICR/OCCUP/DEBT_YLD: this is the MINIMUM. For LTV: this is the MAXIMUM.',

    -- TBL_COVENANT_TEST
    TBL_COVENANT_TEST.actual_val AS actual_val
      COMMENT = 'Actual measured value at test date.',

    -- TBL_PROVISION
    TBL_PROVISION.prov_amt AS prov_amt
      COMMENT = 'Provision amount in dollars.',
    TBL_PROVISION.loss_rate AS loss_rate
      COMMENT = 'Historical loss rate used (decimal, e.g., 0.0085 = 0.85%).',
    TBL_PROVISION.qual_adj_pct AS qual_adj_pct
      COMMENT = 'Qualitative adjustment (Q-factor) percentage added to the loss rate (decimal, e.g., 0.035 = 3.5%).',

    -- TBL_WORKOUT
    TBL_WORKOUT.orig_bal AS orig_bal
      COMMENT = 'Balance at workout entry.',
    TBL_WORKOUT.modified_bal AS modified_bal
      COMMENT = 'Balance after modification.',
    TBL_WORKOUT.haircut_pct AS haircut_pct
      COMMENT = 'Principal haircut percentage (decimal, e.g., 0.21 = 21% write-down).',

    -- TBL_REO
    TBL_REO.acq_val AS acq_val
      COMMENT = 'Acquisition value (credit bid amount, dollars).',
    TBL_REO.sale_val AS sale_val
      COMMENT = 'Sale price when REO property is sold (dollars). NULL if not yet sold.',
    TBL_REO.carrying_cost AS carrying_cost
      COMMENT = 'Accumulated carrying costs (taxes, insurance, maintenance) in dollars.',

    -- TBL_CHARGE_OFF
    TBL_CHARGE_OFF.co_amt AS co_amt
      COMMENT = 'Gross charge-off amount (dollars).',
    TBL_CHARGE_OFF.recovery_amt AS recovery_amt
      COMMENT = 'Amount recovered after charge-off (dollars). May be zero.',

    -- TBL_CAPITAL
    TBL_CAPITAL.tier1_cap AS tier1_cap
      COMMENT = 'Tier 1 capital amount (dollars).',
    TBL_CAPITAL.tier2_cap AS tier2_cap
      COMMENT = 'Tier 2 capital amount (dollars). Total capital = Tier 1 + Tier 2.',
    TBL_CAPITAL.rwa AS rwa
      COMMENT = 'Risk-weighted assets (dollars).',
    TBL_CAPITAL.cet1_ratio AS cet1_ratio
      COMMENT = 'Common Equity Tier 1 ratio (percentage, e.g., 8.1 means 8.1%). Well-capitalized >= 7.0%.',
    TBL_CAPITAL.tier1_ratio AS tier1_ratio
      COMMENT = 'Tier 1 capital ratio (percentage). Well-capitalized >= 8.0%.',
    TBL_CAPITAL.total_ratio AS total_ratio
      COMMENT = 'Total capital ratio (percentage). Well-capitalized >= 10.0%.',
    TBL_CAPITAL.leverage_ratio AS leverage_ratio
      COMMENT = 'Leverage ratio (percentage). Well-capitalized >= 5.0%.',

    -- TBL_CONCENTRATION
    TBL_CONCENTRATION.exposure_amt AS exposure_amt
      COMMENT = 'Total exposure amount (dollars).',
    TBL_CONCENTRATION.pct_of_capital AS pct_of_capital
      COMMENT = 'Exposure as percentage of total capital.',
    TBL_CONCENTRATION.pct_of_total AS pct_of_total
      COMMENT = 'Exposure as percentage of total assets.',
    TBL_CONCENTRATION.limit_pct AS limit_pct
      COMMENT = 'Regulatory limit percentage (300 for CRE_TOTAL, 0 if no specific limit).'
  )

  -- =========================================================================
  -- DIMENSIONS (categorical, date, identifier, and text columns)
  -- =========================================================================

  DIMENSIONS (
    -- TBL_LOAN_MSTR
    TBL_LOAN_MSTR.loan_id AS loan_id
      COMMENT = 'Primary key. Loan identifier. Format: TYPE-YEAR-SEQUENCE (e.g., CRE-2021-00847).',
    TBL_LOAN_MSTR.borrower_id AS borrower_id
      COMMENT = 'FK to TBL_BORROWER. Borrower entity identifier.',
    TBL_LOAN_MSTR.orig_dt AS orig_dt
      COMMENT = 'Loan origination date.',
    TBL_LOAN_MSTR.loan_typ_cd AS loan_typ_cd
      COMMENT = 'Loan type code. Values: CRE_OFFC=CRE Office, CRE_MLTF=CRE Multifamily, CRE_RETL=CRE Retail, CRE_INDL=CRE Industrial, CRE_HOTL=CRE Hotel, CRE_LAND=CRE Land/Development, CNI=Commercial & Industrial, RESI=Residential. All codes starting with CRE_ are commercial real estate loans.',
    TBL_LOAN_MSTR.prop_typ_cd AS prop_typ_cd
      COMMENT = 'Property type code. NULL for non-CRE loans (CNI, RESI). Values: OFFC=Office, MLTF=Multifamily, RETL=Retail, INDL=Industrial, HOTL=Hotel, LAND=Land, MIXD=Mixed-Use, SPEC=Special Purpose.',
    TBL_LOAN_MSTR.rate_typ_cd AS rate_typ_cd
      COMMENT = 'Interest rate type. Values: FIXED=Fixed Rate, ARM_5Y=5-Year Adjustable, ARM_7Y=7-Year Adjustable, ARM_10Y=10-Year Adjustable, FLOAT=Floating Rate.',
    TBL_LOAN_MSTR.mat_dt AS mat_dt
      COMMENT = 'Loan maturity date.',
    TBL_LOAN_MSTR.loan_sts_cd AS loan_sts_cd
      COMMENT = 'Loan status code. Values: ACTV=Active/Current, DLQ30=30 Days Delinquent, DLQ60=60 Days Delinquent, DLQ90=90+ Days Delinquent, NACC=Non-Accrual, DFLT=Default, WKOT=Workout, FCLS=Foreclosure, REO=Real Estate Owned, PAID=Paid Off, CHGOFF=Charged Off.',
    TBL_LOAN_MSTR.risk_rtg_cd AS risk_rtg_cd
      COMMENT = 'Current risk rating. Values: 1-PASS=Pass (best), 2-PASS=Pass, 3-SM=Special Mention, 4-SM=Special Mention, 5-SS=Substandard, 6-SUB=Substandard (impaired), 7-DBT=Doubtful, 8-LOSS=Loss. Ratings 5-SS and above (5,6,7,8) are classified/criticized. "Special Mention or worse" means risk_rtg_cd IN (''5-SS'',''6-SUB'',''7-DBT'',''8-LOSS'').',
    TBL_LOAN_MSTR.branch_cd AS branch_cd
      COMMENT = 'FK to TBL_BRANCH. Originating branch code.',
    TBL_LOAN_MSTR.analyst_id AS analyst_id
      COMMENT = 'FK to TBL_ANALYST. Assigned loan officer/analyst.',
    TBL_LOAN_MSTR.uw_exception_flg AS uw_exception_flg
      COMMENT = 'Underwriting exception flag. Y=This loan had one or more underwriting exceptions at origination. N=No exceptions.',

    -- TBL_BORROWER
    TBL_BORROWER.borrower_id AS borrower_id
      COMMENT = 'Primary key. Borrower identifier (e.g., BRW-00142).',
    TBL_BORROWER.entity_nm AS entity_nm
      COMMENT = 'Borrower legal entity name.',
    TBL_BORROWER.entity_typ_cd AS entity_typ_cd
      COMMENT = 'Entity type. Values: LLC=Limited Liability Company, CORP=Corporation, LP=Limited Partnership, REIT=Real Estate Investment Trust, TRUST=Trust, INDV=Individual, JV=Joint Venture.',
    TBL_BORROWER.naics_cd AS naics_cd
      COMMENT = 'NAICS industry code.',
    TBL_BORROWER.tax_id AS tax_id
      COMMENT = 'Tax identification number.',
    TBL_BORROWER.state_cd AS state_cd
      COMMENT = 'State of incorporation/registration. Values: OR, WA, ID, MT, CA.',
    TBL_BORROWER.risk_tier_cd AS risk_tier_cd
      COMMENT = 'Borrower risk tier. Values: T1=Tier 1 (lowest risk), T2=Tier 2, T3=Tier 3, T4=Tier 4 (highest risk).',

    -- TBL_COLLATERAL
    TBL_COLLATERAL.collateral_id AS collateral_id
      COMMENT = 'Primary key. Collateral identifier.',
    TBL_COLLATERAL.loan_id AS loan_id
      COMMENT = 'FK to TBL_LOAN_MSTR.',
    TBL_COLLATERAL.prop_typ_cd AS prop_typ_cd
      COMMENT = 'Property type code. Values: OFFC=Office, MLTF=Multifamily, RETL=Retail, INDL=Industrial, HOTL=Hotel, LAND=Land, MIXD=Mixed-Use, SPEC=Special Purpose.',
    TBL_COLLATERAL.prop_nm AS prop_nm
      COMMENT = 'Property name (e.g., Cascadia Tower).',
    TBL_COLLATERAL.prop_addr AS prop_addr
      COMMENT = 'Property street address.',
    TBL_COLLATERAL.city AS city
      COMMENT = 'Property city.',
    TBL_COLLATERAL.state_cd AS state_cd
      COMMENT = 'Property state.',
    TBL_COLLATERAL.zip_cd AS zip_cd
      COMMENT = 'Property ZIP code.',

    -- TBL_APPRAISAL
    TBL_APPRAISAL.appraisal_id AS appraisal_id
      COMMENT = 'Primary key.',
    TBL_APPRAISAL.collateral_id AS collateral_id
      COMMENT = 'FK to TBL_COLLATERAL.',
    TBL_APPRAISAL.appr_dt AS appr_dt
      COMMENT = 'Appraisal date.',
    TBL_APPRAISAL.appr_mthd_cd AS appr_mthd_cd
      COMMENT = 'Appraisal method. Values: INC_APPROACH=Income Approach, SALES_COMP=Sales Comparison, COST_APPROACH=Cost Approach, DCF=Discounted Cash Flow.',
    TBL_APPRAISAL.appraiser_id AS appraiser_id
      COMMENT = 'Appraiser identifier.',
    TBL_APPRAISAL.appraiser_nm AS appraiser_nm
      COMMENT = 'Appraiser firm name.',
    TBL_APPRAISAL.review_sts_cd AS review_sts_cd
      COMMENT = 'Review status. Values: APPROVED, PENDING, REJECTED, WAIVED.',

    -- TBL_PAYMENT
    TBL_PAYMENT.payment_id AS payment_id
      COMMENT = 'Primary key.',
    TBL_PAYMENT.loan_id AS loan_id
      COMMENT = 'FK to TBL_LOAN_MSTR.',
    TBL_PAYMENT.pmt_dt AS pmt_dt
      COMMENT = 'Payment date.',
    TBL_PAYMENT.pmt_sts_cd AS pmt_sts_cd
      COMMENT = 'Payment status. Values: ONT=On Time, LATE=Late (1-29 days), MISS=Missed (no payment received), PART=Partial Payment, DFRD=Deferred.',

    -- TBL_COVENANT
    TBL_COVENANT.covenant_id AS covenant_id
      COMMENT = 'Primary key.',
    TBL_COVENANT.loan_id AS loan_id
      COMMENT = 'FK to TBL_LOAN_MSTR.',
    TBL_COVENANT.cov_typ_cd AS cov_typ_cd
      COMMENT = 'Covenant type. Values: DSCR=Debt Service Coverage Ratio (higher is better, typical min 1.25x), LTV=Loan-to-Value (lower is better, typical max 75%), OCCUP=Occupancy Rate (higher is better, typical min 80%), NOI_MIN=Minimum Net Operating Income, DEBT_YLD=Debt Yield (higher is better), ICR=Interest Coverage Ratio (higher is better).',
    TBL_COVENANT.freq_cd AS freq_cd
      COMMENT = 'Testing frequency. Values: Q=Quarterly, SA=Semi-Annual, A=Annual.',
    TBL_COVENANT.eff_dt AS eff_dt
      COMMENT = 'Covenant effective date.',
    TBL_COVENANT.exp_dt AS exp_dt
      COMMENT = 'Covenant expiration date.',

    -- TBL_COVENANT_TEST
    TBL_COVENANT_TEST.test_id AS test_id
      COMMENT = 'Primary key.',
    TBL_COVENANT_TEST.covenant_id AS covenant_id
      COMMENT = 'FK to TBL_COVENANT.',
    TBL_COVENANT_TEST.test_dt AS test_dt
      COMMENT = 'Test date.',
    TBL_COVENANT_TEST.pass_fail_cd AS pass_fail_cd
      COMMENT = 'Test result. Values: PASS=Met covenant requirement, FAIL=Breached covenant.',
    TBL_COVENANT_TEST.waiver_flg AS waiver_flg
      COMMENT = 'Whether the breach was waived by the bank. Y=Waived, N=Not waived.',
    TBL_COVENANT_TEST.waiver_reason AS waiver_reason
      COMMENT = 'Reason the covenant breach was waived (free text). NULL if waiver_flg = N or no waiver granted.',

    -- TBL_RISK_RATING
    TBL_RISK_RATING.rating_id AS rating_id
      COMMENT = 'Primary key.',
    TBL_RISK_RATING.loan_id AS loan_id
      COMMENT = 'FK to TBL_LOAN_MSTR.',
    TBL_RISK_RATING.rating_dt AS rating_dt
      COMMENT = 'Date of rating change.',
    TBL_RISK_RATING.risk_rtg_cd AS risk_rtg_cd
      COMMENT = 'New risk rating (see TBL_LOAN_MSTR.risk_rtg_cd for decode).',
    TBL_RISK_RATING.prev_rtg_cd AS prev_rtg_cd
      COMMENT = 'Previous risk rating.',
    TBL_RISK_RATING.analyst_id AS analyst_id
      COMMENT = 'FK to TBL_ANALYST. Analyst who made the rating change.',
    TBL_RISK_RATING.migration_cd AS migration_cd
      COMMENT = 'Migration direction. Values: UPGRADE=Improved rating, DOWNGRADE=Worsened rating, NO_CHANGE=Same rating.',

    -- TBL_PROVISION
    TBL_PROVISION.provision_id AS provision_id
      COMMENT = 'Primary key.',
    TBL_PROVISION.loan_id AS loan_id
      COMMENT = 'FK to TBL_LOAN_MSTR.',
    TBL_PROVISION.prov_dt AS prov_dt
      COMMENT = 'Provision calculation date.',
    TBL_PROVISION.prov_mthd_cd AS prov_mthd_cd
      COMMENT = 'Provision methodology. Values: CECL=Current Expected Credit Losses (ASC 326), INCURRED=Incurred Loss Model (legacy), SPECIFIC=Specific Reserve (individual impairment).',

    -- TBL_WORKOUT
    TBL_WORKOUT.workout_id AS workout_id
      COMMENT = 'Primary key.',
    TBL_WORKOUT.loan_id AS loan_id
      COMMENT = 'FK to TBL_LOAN_MSTR.',
    TBL_WORKOUT.workout_typ_cd AS workout_typ_cd
      COMMENT = 'Workout type. Values: MOD_RATE=Rate Modification, MOD_TERM=Term Extension, MOD_PRIN=Principal Reduction, FORBEAR=Forbearance Agreement, DPO=Discounted Payoff, SHORT_SALE=Short Sale, NOTE_SALE=Note Sale, FCLS=Foreclosure.',
    TBL_WORKOUT.start_dt AS start_dt
      COMMENT = 'Workout start date.',
    TBL_WORKOUT.resolution_dt AS resolution_dt
      COMMENT = 'Resolution date (NULL if workout still in progress).',
    TBL_WORKOUT.resolution_cd AS resolution_cd
      COMMENT = 'Resolution outcome (NULL if unresolved). Values: RESTRC=Restructured, FORBEAR=Forbearance, DPO=Discounted Payoff, SHORT_SALE=Short Sale, FCLS=Foreclosed, NOTE_SALE=Note Sold, CURE=Borrower Cured.',

    -- TBL_REO
    TBL_REO.reo_id AS reo_id
      COMMENT = 'Primary key.',
    TBL_REO.loan_id AS loan_id
      COMMENT = 'FK to TBL_LOAN_MSTR.',
    TBL_REO.collateral_id AS collateral_id
      COMMENT = 'FK to TBL_COLLATERAL.',
    TBL_REO.acq_dt AS acq_dt
      COMMENT = 'Date property was acquired by bank (foreclosure completion date).',
    TBL_REO.sale_dt AS sale_dt
      COMMENT = 'Date REO property was sold. NULL if not yet sold.',
    TBL_REO.reo_sts_cd AS reo_sts_cd
      COMMENT = 'REO status. Values: HELD=Held by bank, LISTED=Listed for sale, UNDER_CONTRACT=Sale pending, SOLD=Sold.',

    -- TBL_CHARGE_OFF
    TBL_CHARGE_OFF.chargeoff_id AS chargeoff_id
      COMMENT = 'Primary key.',
    TBL_CHARGE_OFF.loan_id AS loan_id
      COMMENT = 'FK to TBL_LOAN_MSTR.',
    TBL_CHARGE_OFF.co_dt AS co_dt
      COMMENT = 'Charge-off date.',
    TBL_CHARGE_OFF.recovery_dt AS recovery_dt
      COMMENT = 'Recovery date (NULL if no recovery yet).',
    TBL_CHARGE_OFF.co_typ_cd AS co_typ_cd
      COMMENT = 'Charge-off type. Values: FULL=Full charge-off, PARTIAL=Partial charge-off, SPECIFIC_RES=Specific reserve charge-off.',

    -- TBL_EXAM_FINDING
    TBL_EXAM_FINDING.finding_id AS finding_id
      COMMENT = 'Primary key.',
    TBL_EXAM_FINDING.exam_id AS exam_id
      COMMENT = 'Examination identifier (e.g., OCC-2023-FULL-001).',
    TBL_EXAM_FINDING.exam_typ_cd AS exam_typ_cd
      COMMENT = 'Examination type. Values: OCC_FULL=OCC Full-Scope Exam, OCC_TARG=OCC Targeted Exam, INT_AUDIT=Internal Audit, EXT_AUDIT=External Audit, BOARD_REV=Board Review.',
    TBL_EXAM_FINDING.finding_dt AS finding_dt
      COMMENT = 'Finding date.',
    TBL_EXAM_FINDING.severity_cd AS severity_cd
      COMMENT = 'Finding severity. Values: MRIA=Matter Requiring Immediate Attention (most severe), MRA=Matter Requiring Attention, REC=Recommendation (least severe).',
    TBL_EXAM_FINDING.category_cd AS category_cd
      COMMENT = 'Finding category. Values: CRE_CONC=CRE Concentration, UW_EXCEPT=Underwriting Exceptions, ALLL_MTHD=ALLL Methodology, APPR_QUAL=Appraisal Quality, COLL_MGMT=Collateral Management, RISK_RTG=Risk Rating, CAP_PLAN=Capital Planning, BSA_AML=BSA/AML, IT_SEC=IT Security, VENDOR_MGMT=Vendor Management, GOVERNANCE=Corporate Governance.',
    TBL_EXAM_FINDING.finding_desc AS finding_desc
      COMMENT = 'Description of the finding.',
    TBL_EXAM_FINDING.remediation_sts_cd AS remediation_sts_cd
      COMMENT = 'Remediation status. Values: OPEN=Not yet addressed, IN_PROGRESS=Being remediated, CLOSED=Fully remediated.',
    TBL_EXAM_FINDING.due_dt AS due_dt
      COMMENT = 'Remediation due date.',

    -- TBL_CAPITAL
    TBL_CAPITAL.capital_id AS capital_id
      COMMENT = 'Primary key.',
    TBL_CAPITAL.report_dt AS report_dt
      COMMENT = 'Quarter-end reporting date.',

    -- TBL_CONCENTRATION
    TBL_CONCENTRATION.conc_id AS conc_id
      COMMENT = 'Primary key.',
    TBL_CONCENTRATION.report_dt AS report_dt
      COMMENT = 'Quarter-end reporting date.',
    TBL_CONCENTRATION.segment_cd AS segment_cd
      COMMENT = 'Segment code. Values: CRE_TOTAL, CRE_OFFC, CRE_MLTF, CRE_RETL, CRE_INDL, CRE_HOTL, CNI, RESI.',
    TBL_CONCENTRATION.segment_val AS segment_val
      COMMENT = 'Segment display name.',
    TBL_CONCENTRATION.breach_flg AS breach_flg
      COMMENT = 'Whether the concentration exceeds the limit. Y=Breach, N=Within limit.',

    -- TBL_BRANCH
    TBL_BRANCH.branch_cd AS branch_cd
      COMMENT = 'Primary key. Branch code (e.g., BR-001).',
    TBL_BRANCH.branch_nm AS branch_nm
      COMMENT = 'Branch name.',
    TBL_BRANCH.city AS city
      COMMENT = 'Branch city.',
    TBL_BRANCH.state_cd AS state_cd
      COMMENT = 'Branch state.',
    TBL_BRANCH.region_cd AS region_cd
      COMMENT = 'Region code. Values: PNW-S=Pacific Northwest South (Oregon), PNW-N=Pacific Northwest North (Washington), MTN=Mountain (Idaho/Montana), PAC=Pacific (California).',
    TBL_BRANCH.mgr_id AS mgr_id
      COMMENT = 'Branch manager employee ID.',

    -- TBL_ANALYST
    TBL_ANALYST.analyst_id AS analyst_id
      COMMENT = 'Primary key. Analyst identifier (e.g., ANL-0001).',
    TBL_ANALYST.analyst_nm AS analyst_nm
      COMMENT = 'Analyst full name.',
    TBL_ANALYST.branch_cd AS branch_cd
      COMMENT = 'FK to TBL_BRANCH. Home branch.',
    TBL_ANALYST.role_cd AS role_cd
      COMMENT = 'Role code. Values: LO=Loan Officer, SA=Senior Analyst, RM=Relationship Manager, CRA=Credit Risk Analyst, VP=Vice President, SVP=Senior Vice President, DIR=Director.',
    TBL_ANALYST.hire_dt AS hire_dt
      COMMENT = 'Hire date.',
    TBL_ANALYST.cert_cd AS cert_cd
      COMMENT = 'Certification. Values: CFA=Chartered Financial Analyst, CPA=Certified Public Accountant, CCRA=Certified Commercial Real Estate Analyst, FRM=Financial Risk Manager, CRCM=Certified Regulatory Compliance Manager, NONE=No certification.',

    -- TBL_AUDIT_LOG
    TBL_AUDIT_LOG.audit_id AS audit_id
      COMMENT = 'Primary key.',
    TBL_AUDIT_LOG.loan_id AS loan_id
      COMMENT = 'FK to TBL_LOAN_MSTR.',
    TBL_AUDIT_LOG.action_cd AS action_cd
      COMMENT = 'Action code. Values: ORIGINATE, RATE_CHG, COVENANT_TEST, APPRAISAL_ORD, PAYMENT_REC, DELINQ_NOTICE, DEFAULT_NOTICE, WORKOUT_INIT, CHARGEOFF, MODIFY, FCLS_INIT, REO_ACQ, EXAM_FINDING, AUDIT_FLAG, STATUS_CHG.',
    TBL_AUDIT_LOG.action_dt AS action_dt
      COMMENT = 'Action date.',
    TBL_AUDIT_LOG.user_id AS user_id
      COMMENT = 'User who performed the action (analyst_id).',
    TBL_AUDIT_LOG.detail_txt AS detail_txt
      COMMENT = 'Action detail text.'
  )

  -- =========================================================================
  -- METRICS
  -- =========================================================================

  METRICS (
    TBL_LOAN_MSTR.total_cre_exposure AS SUM(IFF(loan_typ_cd LIKE 'CRE_%', curr_bal, NULL))
      COMMENT = 'Total current CRE loan exposure (sum of current balances for all CRE loan types).',

    TBL_LOAN_MSTR.total_cre_office_exposure AS SUM(IFF(loan_typ_cd = 'CRE_OFFC', curr_bal, NULL))
      COMMENT = 'Total current CRE office exposure.',

    TBL_COLLATERAL.avg_ltv_current AS AVG(ltv_curr)
      COMMENT = 'Average current loan-to-value ratio across collateral.',

    TBL_COLLATERAL.avg_occupancy AS AVG(occup_rate)
      COMMENT = 'Average occupancy rate across collateral properties.',

    TBL_CHARGE_OFF.net_charge_offs AS SUM(co_amt) - SUM(recovery_amt)
      COMMENT = 'Net charge-offs = gross charge-offs minus recoveries.',

    TBL_CHARGE_OFF.gross_charge_offs AS SUM(co_amt)
      COMMENT = 'Total gross charge-off amount.',

    TBL_CHARGE_OFF.total_recoveries AS SUM(recovery_amt)
      COMMENT = 'Total recovery amount from charged-off loans.',

    TBL_PROVISION.total_provision AS SUM(prov_amt)
      COMMENT = 'Total ALLL/CECL provision amount.',

    TBL_COVENANT_TEST.covenant_breach_count AS COUNT(IFF(pass_fail_cd = 'FAIL', test_id, NULL))
      COMMENT = 'Number of covenant test failures (breaches).',

    TBL_WORKOUT.workout_pipeline AS SUM(IFF(resolution_dt IS NULL, orig_bal, NULL))
      COMMENT = 'Total balance of unresolved workouts (active workout pipeline).',

    TBL_EXAM_FINDING.open_mria_count AS COUNT(IFF(severity_cd = 'MRIA' AND remediation_sts_cd != 'CLOSED', finding_id, NULL))
      COMMENT = 'Number of open MRIA (Matter Requiring Immediate Attention) findings.'
  )

  COMMENT = 'CRE lending portfolio for Pacific Northwest Bank (PNB). 18 tables covering loans, borrowers, collateral, covenants, payments, risk ratings, provisions, workouts, REO, charge-offs, exam findings, capital adequacy, concentration metrics, branches, analysts, and audit logs. All coded columns use abbreviated values that must be decoded using the descriptions below.'

  -- =========================================================================
  -- VERIFIED QUERIES
  -- =========================================================================

  AI_VERIFIED_QUERIES (

    vqr_classified_cre_office AS (
      QUESTION 'What percentage of CRE office loans are rated Special Mention or worse?'
      SQL $$
        SELECT
          COUNT(*) AS total_cre_office_loans,
          COUNT(CASE WHEN risk_rtg_cd IN ('5-SS','6-SUB','7-DBT','8-LOSS') THEN 1 END) AS classified_count,
          ROUND(100.0 * COUNT(CASE WHEN risk_rtg_cd IN ('5-SS','6-SUB','7-DBT','8-LOSS') THEN 1 END) / COUNT(*), 1) AS classified_pct
        FROM CRE_BENCHMARK_DB.CRE.TBL_LOAN_MSTR
        WHERE loan_typ_cd = 'CRE_OFFC'
      $$
    ),

    vqr_cre_concentration AS (
      QUESTION 'What is the CRE concentration as a percentage of total capital?'
      SQL $$
        SELECT
          c.report_dt,
          c.exposure_amt,
          c.pct_of_capital AS cre_pct_of_capital,
          c.limit_pct AS regulatory_limit,
          c.breach_flg
        FROM CRE_BENCHMARK_DB.CRE.TBL_CONCENTRATION c
        WHERE c.segment_cd = 'CRE_TOTAL'
        ORDER BY c.report_dt DESC
        LIMIT 1
      $$
    ),

    vqr_net_chargeoffs_by_prop AS (
      QUESTION 'What are the net charge-offs by property type?'
      SQL $$
        SELECT
          col.prop_typ_cd,
          SUM(co.co_amt) AS gross_chargeoff,
          SUM(co.recovery_amt) AS total_recovery,
          SUM(co.co_amt) - SUM(co.recovery_amt) AS net_chargeoff
        FROM CRE_BENCHMARK_DB.CRE.TBL_CHARGE_OFF co
        JOIN CRE_BENCHMARK_DB.CRE.TBL_LOAN_MSTR l ON co.loan_id = l.loan_id
        JOIN CRE_BENCHMARK_DB.CRE.TBL_COLLATERAL col ON l.loan_id = col.loan_id
        WHERE l.loan_typ_cd LIKE 'CRE_%'
        GROUP BY col.prop_typ_cd
        ORDER BY net_chargeoff DESC
      $$
    ),

    vqr_dscr_breaches_2023 AS (
      QUESTION 'How many DSCR covenant breaches were not waived in 2023?'
      SQL $$
        SELECT
          COUNT(DISTINCT ct.test_id) AS breach_count,
          COUNT(DISTINCT cov.loan_id) AS affected_loans
        FROM CRE_BENCHMARK_DB.CRE.TBL_COVENANT_TEST ct
        JOIN CRE_BENCHMARK_DB.CRE.TBL_COVENANT cov ON ct.covenant_id = cov.covenant_id
        WHERE cov.cov_typ_cd = 'DSCR'
          AND ct.pass_fail_cd = 'FAIL'
          AND ct.waiver_flg = 'N'
          AND YEAR(ct.test_dt) = 2023
      $$
    ),

    vqr_cet1_trajectory AS (
      QUESTION 'What is the CET1 ratio trajectory over time?'
      SQL $$
        SELECT
          report_dt,
          cet1_ratio,
          tier1_ratio,
          total_ratio,
          leverage_ratio,
          CASE WHEN cet1_ratio >= 7.0 THEN 'WELL_CAPITALIZED' ELSE 'BELOW_THRESHOLD' END AS capital_status
        FROM CRE_BENCHMARK_DB.CRE.TBL_CAPITAL
        ORDER BY report_dt
      $$
    ),

    vqr_uw_exception_by_branch AS (
      QUESTION 'Which branch had the highest underwriting exception rate?'
      SQL $$
        SELECT
          b.branch_cd,
          b.branch_nm,
          b.city,
          COUNT(*) AS total_loans,
          SUM(CASE WHEN l.uw_exception_flg = 'Y' THEN 1 ELSE 0 END) AS exception_count,
          ROUND(100.0 * SUM(CASE WHEN l.uw_exception_flg = 'Y' THEN 1 ELSE 0 END) / COUNT(*), 1) AS exception_rate_pct
        FROM CRE_BENCHMARK_DB.CRE.TBL_LOAN_MSTR l
        JOIN CRE_BENCHMARK_DB.CRE.TBL_BRANCH b ON l.branch_cd = b.branch_cd
        WHERE YEAR(l.orig_dt) IN (2021, 2022)
          AND l.loan_typ_cd LIKE 'CRE_%'
        GROUP BY b.branch_cd, b.branch_nm, b.city
        ORDER BY exception_rate_pct DESC
      $$
    ),

    vqr_latest_appraisal AS (
      QUESTION 'What is the latest appraisal value for each collateral property?'
      SQL $$
        SELECT
          a.collateral_id,
          c.prop_nm,
          c.prop_typ_cd,
          a.appr_dt,
          a.appr_val,
          a.appraiser_nm,
          c.orig_appr_val,
          ROUND(100.0 * (a.appr_val - c.orig_appr_val) / c.orig_appr_val, 1) AS value_change_pct
        FROM CRE_BENCHMARK_DB.CRE.TBL_APPRAISAL a
        JOIN CRE_BENCHMARK_DB.CRE.TBL_COLLATERAL c ON a.collateral_id = c.collateral_id
        WHERE a.appr_dt = (
          SELECT MAX(a2.appr_dt)
          FROM CRE_BENCHMARK_DB.CRE.TBL_APPRAISAL a2
          WHERE a2.collateral_id = a.collateral_id
        )
      $$
    ),

    vqr_reo_carrying_cost AS (
      QUESTION 'What are the REO properties, carrying costs, and holding period?'
      SQL $$
        SELECT
          r.reo_id,
          c.prop_nm,
          c.prop_typ_cd,
          r.acq_dt,
          r.acq_val,
          r.sale_dt,
          r.sale_val,
          r.carrying_cost,
          r.reo_sts_cd,
          DATEDIFF('day', r.acq_dt, COALESCE(r.sale_dt, CURRENT_DATE())) AS days_held
        FROM CRE_BENCHMARK_DB.CRE.TBL_REO r
        JOIN CRE_BENCHMARK_DB.CRE.TBL_COLLATERAL c ON r.collateral_id = c.collateral_id
        ORDER BY r.acq_val DESC
      $$
    )
  );
