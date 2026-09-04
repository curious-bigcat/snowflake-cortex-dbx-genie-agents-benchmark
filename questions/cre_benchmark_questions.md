# CRE Benchmark Questions (G01-G10)

10 complex multi-part questions testing SQL generation, document retrieval, domain reasoning, and groundedness. Each question requires 3+ table joins AND document context.

---

## G01: Office Portfolio Health + OCC Concentration Guidance

**Question:**
> What is PNB's total CRE office loan exposure, what percentage of those loans are rated Special Mention (5-SS) or worse, and what does the OCC's interagency guidance (SR 07-1) say about the CRE concentration threshold relative to capital? Is PNB in breach?

**Tables Required:** TBL_LOAN_MSTR, TBL_CONCENTRATION, TBL_CAPITAL
**Documents Required:** fed_sr07_1_cre_concentration_guidance.pdf, occ_consent_order_2023_ce_0847.txt
**Reasoning Required:** Connect the 300% CRE/capital threshold from SR 07-1 to PNB's actual 420% ratio

**Complexity Traps:**
- Must filter on `loan_typ_cd = 'CRE_OFFC'` (not `prop_typ_cd` which is in a different table)
- "Special Mention or worse" = risk_rtg_cd IN ('5-SS','6-SUB','7-DBT','8-LOSS'), not just '3-SM'/'4-SM'
- Concentration is % of capital, not % of total assets

**Groundedness Traps:**
- The 300% threshold must come from the SR 07-1 document, not general knowledge
- The 420% figure must come from the consent order or concentration table, not be invented

---

## G02: Cascadia Tower Full Credit Analysis

**Question:**
> For loan CRE-2021-00847 (Cascadia Tower), show me: (a) the original vs current appraisal value and LTV, (b) the DSCR covenant test history for the last 6 quarters showing the actual vs threshold values, (c) the workout proposal terms including the proposed haircut percentage, and (d) the borrower's NOI trend from 2021 to 2023.

**Tables Required:** TBL_LOAN_MSTR, TBL_COLLATERAL, TBL_APPRAISAL, TBL_COVENANT, TBL_COVENANT_TEST, TBL_WORKOUT
**Documents Required:** credit_committee_memo_cascadia_tower.txt, appraisal_report_cascadia_tower_2023.txt, workout_proposal_cascadia_tower.txt, borrower_financials_cascadia_holdings.txt
**Reasoning Required:** Synthesize data from 6 tables + 4 documents into a coherent credit analysis

**Complexity Traps:**
- Must use MAX(appr_dt) for current appraisal, not first row (appraisal vintage trap)
- DSCR covenant: must join loan -> covenant (filter cov_typ_cd='DSCR') -> covenant_test
- NOI trend comes from the document, not from any table

---

## G03: ALLL Adequacy + Q-Factor Justification

**Question:**
> What is the total ALLL provision for CRE office loans, what effective loss rate does that imply (including Q-factor adjustments), and how does the ALLL methodology memo justify the Q4 2023 Q-factor increase to 3.50% for office? What was the OCC's assessment of the ALLL shortfall?

**Tables Required:** TBL_PROVISION, TBL_LOAN_MSTR
**Documents Required:** alll_methodology_memo_2023.txt, occ_consent_order_2023_ce_0847.txt, examiner_report_capital_adequacy.txt
**Reasoning Required:** Compare calculated provision rates from data against documented methodology

**Complexity Traps:**
- Must filter provisions by joining to TBL_LOAN_MSTR where loan_typ_cd = 'CRE_OFFC'
- The Q-factor history is in the document, not in the provision table
- The $45-65M shortfall figure is in the consent order, not derivable from data alone

---

## G04: Covenant Breach Cascade + Workout Outcomes

**Question:**
> How many CRE loans had DSCR covenant breaches in 2023 that were NOT waived? Of those, how many ended up in workout, foreclosure, or charge-off? Show the resolution breakdown with total dollar amounts.

**Tables Required:** TBL_COVENANT, TBL_COVENANT_TEST, TBL_LOAN_MSTR, TBL_WORKOUT, TBL_CHARGE_OFF
**Documents Required:** interagency_cre_workout_policy_2023.pdf (for workout standards context)
**Reasoning Required:** Trace the chain from covenant breach -> loan outcome -> dollar impact

**Complexity Traps:**
- Must join covenant_test -> covenant (filter DSCR) -> loan_mstr
- A loan with status WKOT may still have active covenant tests (multi-status trap)
- Must count DISTINCT loans, not duplicate-count across multiple failed test dates
- Waiver_flg = 'N' means NOT waived (the breach stands)

---

## G05: Capital Impact + Stress Test

**Question:**
> Trace PNB's CET1 ratio from year-end 2021 to the most recent quarter. What were the key drivers of the 330 bps deterioration? Under the severe adverse stress scenario, what would CET1 fall to, and does the capital plan restore it above well-capitalized thresholds?

**Tables Required:** TBL_CAPITAL, TBL_CHARGE_OFF, TBL_PROVISION
**Documents Required:** stress_test_severe_adverse_2023.txt, regulatory_capital_plan_occ_submission.txt, examiner_report_capital_adequacy.txt, occ_consent_order_2023_ce_0847.txt
**Reasoning Required:** Connect capital ratio changes to specific loss events, then evaluate the capital plan adequacy

**Complexity Traps:**
- CET1 ratios are in TBL_CAPITAL, but drivers (charge-offs, provisions, dividends) require multiple tables + documents
- The stress test projection (6.1%) and post-mitigation figure (7.8%) are ONLY in the documents
- Well-capitalized threshold is 7.0% for CET1 -- this should come from the regulatory docs, not be assumed

---

## G06: Recovery Analysis by Property Type

**Question:**
> For all charged-off CRE loans, what is the total gross charge-off amount, total recoveries, and net loss rate by property type? Which property type had the highest loss severity? Include the total number of charge-offs per type.

**Tables Required:** TBL_CHARGE_OFF, TBL_LOAN_MSTR, TBL_COLLATERAL
**Documents Required:** occ_comptrollers_handbook_cre_lending.pdf (for loss severity context)
**Reasoning Required:** Must calculate NET charge-offs (gross minus recoveries), not just gross

**Complexity Traps:**
- Net charge-off = co_amt - recovery_amt (NOT just co_amt)
- Must join charge_off -> loan_mstr -> collateral to get property type
- Property type is prop_typ_cd in TBL_COLLATERAL, not loan_typ_cd in TBL_LOAN_MSTR
- Loss rate = net charge-offs / total loan balance for that property type

---

## G07: Underwriting Exception Analysis by Branch

**Question:**
> The internal audit found 23% of CRE originations in 2021-2022 had underwriting exceptions. Which 3 branches had the highest exception rates? What types of exceptions were most common? How does the OCC consent order address underwriting deficiencies?

**Tables Required:** TBL_LOAN_MSTR, TBL_BRANCH, TBL_ANALYST
**Documents Required:** internal_audit_report_cre_lending_2023.txt, occ_consent_order_2023_ce_0847.txt
**Reasoning Required:** Compare SQL-derived exception rates against the audit report's findings

**Complexity Traps:**
- Must filter to CRE loans (loan_typ_cd LIKE 'CRE_%') originated in 2021-2022
- Exception types are in the DOCUMENT, not in the data (the table only has uw_exception_flg Y/N)
- The 23% figure should be validated against the data AND the audit report

---

## G08: REO Portfolio Analysis

**Question:**
> What are PNB's total REO properties, their aggregate carrying cost, and average time held? Which specific REO property had the largest loss on disposition (sold at biggest discount)? For unsold REO, what is the total exposure?

**Tables Required:** TBL_REO, TBL_COLLATERAL, TBL_LOAN_MSTR
**Documents Required:** foreclosure_timeline_mercer_industrial.txt (for specific REO case study)
**Reasoning Required:** Calculate time-to-sale, gain/loss on disposition, and total held exposure

**Complexity Traps:**
- sale_dt and sale_val are NULL for unsold properties -- must handle NULLs correctly
- Loss on disposition = sale_val - acq_val - carrying_cost (must include carrying costs)
- Time held = DATEDIFF between acq_dt and sale_dt (or current date if unsold)
- "Unsold REO exposure" = SUM of acq_val + carrying_cost WHERE sale_dt IS NULL

---

## G09: Examination Finding Remediation Status

**Question:**
> How many MRIA-level findings from OCC examinations are still open or in-progress? What categories do they fall into? What are the remediation deadlines per the consent order, and how many are past due?

**Tables Required:** TBL_EXAM_FINDING
**Documents Required:** occ_consent_order_2023_ce_0847.txt, examiner_report_capital_adequacy.txt
**Reasoning Required:** Compare exam finding data against consent order deadlines

**Complexity Traps:**
- Must filter severity_cd = 'MRIA' AND remediation_sts_cd != 'CLOSED'
- The consent order says 180-day deadline for MRIA remediation (Article VI)
- "Past due" = due_dt < CURRENT_DATE() AND remediation_sts_cd != 'CLOSED'
- The 12 MRIA count and 8 carryover from 2022 should be verified against both data and docs

---

## G10: Loan Sale Impact on Capital

**Question:**
> If PNB sells the $412M performing CRE loan pool at 92 cents on the dollar per the term sheet, what is the projected loss? How would that impact the CET1 ratio? Factor in the RWA reduction. What is the projected CET1 post-sale, and is PNB closer to or further from the consent order's capital restoration target?

**Tables Required:** TBL_CAPITAL, TBL_CONCENTRATION, TBL_LOAN_MSTR
**Documents Required:** loan_sale_term_sheet_performing_pool.txt, regulatory_capital_plan_occ_submission.txt, occ_consent_order_2023_ce_0847.txt
**Reasoning Required:** Calculate loss impact on capital, then project post-sale CET1 ratio

**Complexity Traps:**
- Loss = $412M * 8% = $32.96M (this reduces CET1 capital)
- RWA reduction ~ $400M (reduces denominator, improving ratio)
- Net CET1 impact: loss hurts, RWA reduction helps -- must calculate both
- The capital plan doc says +0.4% CET1 impact -- the agent should arrive at a similar figure
- The consent order target is CET1 above well-capitalized (7.0%) with buffer
