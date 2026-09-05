export const BRAND = {
  snowflake: { color: '#29B5E8', name: 'Snowflake Cortex', icon: '\u2744' },
  databricks: { color: '#FF3621', name: 'Databricks Genie', icon: '\u25C6' },
};

export const PRESET_QUESTIONS = [
  {
    id: 'G01',
    short: 'Office Exposure + SR 07-1',
    text: "What is PNB's total CRE office loan exposure, what percentage of those loans are rated Special Mention (5-SS) or worse, and what does the OCC's interagency guidance (SR 07-1) say about the CRE concentration threshold relative to capital? Is PNB in breach?",
    groundTruth: {
      tablesRequired: ['TBL_LOAN_MSTR', 'TBL_CONCENTRATION', 'TBL_CAPITAL'],
      docsRequired: ['fed_sr07_1_cre_concentration_guidance.pdf', 'occ_consent_order_2023_ce_0847.txt'],
      keyFacts: [
        'Must filter on loan_typ_cd = CRE_OFFC',
        'Special Mention or worse = risk_rtg_cd IN (5-SS, 6-SB, 7-DO, 8-LO)',
        'SR 07-1 threshold: 300% CRE/capital (screening, not hard cap)',
        'PNB actual CRE/capital: ~391% (latest Q2 2025), historical range ~367-416% (all in breach of 300%)',
        'Concentration is % of capital, not % of total assets',
        '300% threshold must come from SR 07-1 doc, not general knowledge',
        'CRE/capital figure must come from concentration table (TBL_CONCENTRATION, segment_cd = CRE_TOTAL)',
      ],
    },
  },
  {
    id: 'G02',
    short: 'Cascadia Tower Deep Dive',
    text: "For loan CRE-2021-00847 (Cascadia Tower), show me: (a) the original vs current appraisal value and LTV, (b) all DSCR covenant test results for the last 6 quarters, (c) the workout proposal terms including the haircut percentage, and (d) the NOI trend from 2021 to 2023.",
    groundTruth: {
      tablesRequired: ['TBL_LOAN_MSTR', 'TBL_COLLATERAL', 'TBL_APPRAISAL', 'TBL_COVENANT', 'TBL_COVENANT_TEST', 'TBL_WORKOUT'],
      docsRequired: ['credit_committee_memo_cascadia_tower.txt', 'appraisal_report_cascadia_tower_2023.txt', 'workout_proposal_cascadia_tower.txt', 'borrower_financials_cascadia_holdings.txt'],
      keyFacts: [
        'Original appraisal ~$131M, current ~$78M, ~40% decline (from TBL_COLLATERAL)',
        'LTV moved from ~65% to ~100.6% (underwater) -- orig_appr_val vs curr_appr_val in collateral',
        'Cascadia has ICR and DEBT_YLD covenants (NOT DSCR) -- cov_typ_cd in TBL_COVENANT',
        'Covenant tests: join loan -> covenant (filter ICR or DEBT_YLD) -> covenant_test for 16 test records each',
        'NOI trend comes from document (borrower financials), not any table',
        'Workout haircut ~21.02% ($78.5M orig_bal to $62M modified_bal in TBL_WORKOUT)',
      ],
    },
  },
  {
    id: 'G03',
    short: 'ALLL + Q-Factor + OCC',
    text: "What is the total ALLL provision for CRE office loans, what is the effective loss rate after Q-factor adjustments, what does the ALLL methodology memo say about the Q4 2023 Q-factor increase to 3.50%, and what was the OCC's assessment of the ALLL shortfall?",
    groundTruth: {
      tablesRequired: ['TBL_PROVISION', 'TBL_LOAN_MSTR'],
      docsRequired: ['alll_methodology_memo_2023.txt', 'occ_consent_order_2023_ce_0847.txt', 'examiner_report_capital_adequacy.txt'],
      keyFacts: [
        'Must filter provisions by joining to TBL_LOAN_MSTR where loan_typ_cd = CRE_OFFC',
        'Q-factor history is in the document, not in the provision table',
        'OCC shortfall assessment: $45-65M shortfall from consent order',
        'Q-factor progression from 0.50% to 3.50% documented in ALLL memo',
        'Avoid join fan-out when aggregating provisions',
      ],
    },
  },
  {
    id: 'G04',
    short: 'DSCR Breach Cascade',
    text: "How many CRE loans had unwaived DSCR covenant breaches in 2023? Of those, how many ended up in workout, foreclosure, or charge-off? Show me the resolution breakdown with dollar amounts.",
    groundTruth: {
      tablesRequired: ['TBL_COVENANT', 'TBL_COVENANT_TEST', 'TBL_LOAN_MSTR', 'TBL_WORKOUT', 'TBL_CHARGE_OFF'],
      docsRequired: ['interagency_cre_workout_policy_2023.pdf'],
      keyFacts: [
        'Must join covenant_test -> covenant (filter DSCR) -> loan_mstr',
        'Waiver_flg = N means NOT waived (the breach stands)',
        'Must count DISTINCT loans, not duplicate across test dates',
        'Total unwaived breaches: ~10,459 loans',
        'Resolution breakdown: workout, foreclosure, charge-off, still performing',
      ],
    },
  },
  {
    id: 'G05',
    short: 'CET1 + Stress Test',
    text: "Trace PNB's CET1 ratio from year-end 2021 to the most recent quarter. What were the key drivers of the 330 basis point deterioration? What does the severe adverse stress scenario project for CET1, and does the capital plan restore well-capitalized status?",
    groundTruth: {
      tablesRequired: ['TBL_CAPITAL', 'TBL_CHARGE_OFF', 'TBL_PROVISION'],
      docsRequired: ['stress_test_severe_adverse_2023.txt', 'regulatory_capital_plan_occ_submission.txt', 'examiner_report_capital_adequacy.txt', 'occ_consent_order_2023_ce_0847.txt'],
      keyFacts: [
        'CET1 trajectory: ~10.7% (YE2021) -> ~7.84% trough -> ~10.32% (Q2 2025)',
        'Key drivers: credit losses, provision expense, dividends, RWA growth',
        'Stress scenario: CET1 projected to ~6.1% (below 7.0% well-capitalized)',
        'Capital plan: sub debt, loan sale, RWA optimization, dividend suspension',
        'Post-mitigation stress CET1: ~7.8%',
        'Stress test projection and capital plan details are ONLY in documents',
        'Well-capitalized threshold 7.0% should come from regulatory docs',
      ],
    },
  },
  {
    id: 'G06',
    short: 'Recovery by Property Type',
    text: "For all CRE charge-offs, break down gross charge-offs, recoveries, and net loss rate by property type. Which property type has the highest loss severity? How many loans per type?",
    groundTruth: {
      tablesRequired: ['TBL_CHARGE_OFF', 'TBL_LOAN_MSTR', 'TBL_COLLATERAL'],
      docsRequired: ['occ_comptrollers_handbook_cre_lending.pdf'],
      keyFacts: [
        'Net charge-off = co_amt - recovery_amt (NOT just co_amt)',
        'Must join charge_off -> loan_mstr -> collateral to get property type',
        'Property type is prop_typ_cd in TBL_COLLATERAL, not loan_typ_cd',
        'Loss rate = net charge-offs / total loan balance for that property type',
        'Industrial (INDL) has highest loss severity at ~79% (79.08%)',
      ],
    },
  },
  {
    id: 'G07',
    short: 'UW Exceptions by Branch',
    text: "The internal audit found a 23% underwriting exception rate. Which are the top 3 branches by exception rate, what are the most common exception types, and what did the OCC consent order require in response?",
    groundTruth: {
      tablesRequired: ['TBL_LOAN_MSTR', 'TBL_BRANCH', 'TBL_ANALYST'],
      docsRequired: ['internal_audit_report_cre_lending_2023.txt', 'occ_consent_order_2023_ce_0847.txt'],
      keyFacts: [
        'Must filter to CRE loans originated 2021-2022',
        'Exception types are in the DOCUMENT, not in data (table only has uw_exception_flg Y/N)',
        'Common types from audit: DSCR below policy (42%), LTV above policy (28%), missing Phase I (18%)',
        'OCC consent order Article V: revised standards, independent tracking, $5M threshold',
        '23% figure should be validated against both data and audit report',
      ],
    },
  },
  {
    id: 'G08',
    short: 'REO Portfolio',
    text: "How many properties are currently in REO status? What is the total carrying cost, what is the average time held, and which property had the largest loss on disposition? What is our unsold REO exposure?",
    groundTruth: {
      tablesRequired: ['TBL_REO', 'TBL_COLLATERAL', 'TBL_LOAN_MSTR'],
      docsRequired: ['foreclosure_timeline_mercer_industrial.txt'],
      keyFacts: [
        'sale_dt and sale_val are NULL for unsold properties',
        'Loss on disposition = sale_val - acq_val - carrying_cost (must include carrying costs)',
        'Largest loss: Kirkland Multifamily Property, ~$18M loss',
        'Current REO: ~372 properties (HELD/LISTED/UNDER_CONTRACT)',
        'Avg time held: ~794 days',
        'Total carrying cost: ~$260M',
        'Unsold REO exposure: ~$5.41B',
      ],
    },
  },
  {
    id: 'G09',
    short: 'MRIA Remediation',
    text: "How many OCC MRIA examination findings are currently open or in-progress? What categories do they fall into, what are the remediation deadlines per the consent order, and how many are past due?",
    groundTruth: {
      tablesRequired: ['TBL_EXAM_FINDING'],
      docsRequired: ['occ_consent_order_2023_ce_0847.txt', 'examiner_report_capital_adequacy.txt'],
      keyFacts: [
        'Must filter severity_cd = MRIA AND remediation_sts_cd != CLOSED',
        'OCC MRIA findings: filter exam_typ_cd IN (OCC_FULL, OCC_TARG) gives 196; all MRIA = 502',
        'Question says "OCC MRIA" so filtering to OCC exam types (196) is the correct interpretation',
        '180-day MRIA deadline from consent order Article VI',
        'Past due = due_dt < CURRENT_DATE AND remediation_sts_cd != CLOSED; all 196 OCC MRIAs are past due',
        'Category breakdown across 11 categories (COLL_MGMT, RISK_RTG, VENDOR_MGMT, CAP_PLAN, etc.)',
        'CRITICAL: database has 1764 open/in-progress findings across ALL severity levels -- must filter to MRIA only',
        'Consent order references formal MRIA articles; database has granular finding records',
      ],
    },
  },
  {
    id: 'G10',
    short: 'Loan Sale + Capital',
    text: "If PNB sells the $412M distressed loan pool at 92 cents on the dollar, what is the projected loss, what is the CET1 impact after RWA reduction, and does the post-sale CET1 move closer to or further from the consent order target?",
    groundTruth: {
      tablesRequired: ['TBL_CAPITAL', 'TBL_CONCENTRATION', 'TBL_LOAN_MSTR'],
      docsRequired: ['loan_sale_term_sheet_performing_pool.txt', 'regulatory_capital_plan_occ_submission.txt', 'occ_consent_order_2023_ce_0847.txt'],
      keyFacts: [
        'Loss = $412M * 8% = $32.96M (reduces CET1 capital)',
        'RWA reduction ~$400M (reduces denominator, improves ratio)',
        'Net CET1 impact: loss hurts, RWA reduction helps',
        'Post-sale CET1: ~11.06%',
        'Capital plan doc says +0.4% CET1 impact',
        'Consent order target: CET1 above 9.0% with buffer',
        'PNB moves closer to (exceeds) consent order target',
      ],
    },
  },
];

export const DEFAULT_CONFIG = {
  snowflakeAccountUrl: '',
  snowflakePat: '',
  snowflakeAgentPath: '/api/v2/databases/CRE_BENCHMARK_DB/schemas/CRE/agents/CRE_BENCHMARK_AGENT:run',
  databricksEndpoint: '',
  databricksPat: '',
};
