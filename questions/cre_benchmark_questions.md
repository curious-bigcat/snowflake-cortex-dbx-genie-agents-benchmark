# CRE Lending Benchmark — 10 Questions

10 single-query questions for evaluating AI agents against a synthetic CRE lending dataset (Pacific Northwest Bank). Each question is a single complex query designed to expose specific agent weaknesses: filter precision, aggregation traps, column confusion, join chains, NULL handling, and doc-data reconciliation.

**Dataset:** 18 parquet tables, 13 bank documents, 10 case files, 7 regulatory PDFs
**Bank:** Pacific Northwest Bank (PNB), Portland OR — under OCC Consent Order 2023-CE-0847

---

## Q01: Office Portfolio + Concentration Breach

**Question:**
> What percentage of PNB's CRE office book is rated Special Mention or worse, and is the bank currently breaching the SR 07-1 interagency CRE concentration threshold?

**Sources:** TBL_LOAN_MSTR, TBL_CONCENTRATION, TBL_CAPITAL | fed_sr07_1_cre_concentration_guidance.pdf, occ_consent_order_2023_ce_0847.txt

**Trap:** Must filter `loan_typ_cd = 'CRE_OFFC'` (not `prop_typ_cd`), define "Special Mention or worse" as 5-SS through 8-LOSS, read concentration as % of capital (not % of assets), and pull the 300% threshold from the SR 07-1 document.

**Expected Answer:**
- Rated 5-SS or worse: **3,799 loans (38.42%)** — $64.65B of $167.0B total (9,887 loans)
  - 5-SS: 1,729 | 6-SUB: 1,238 | 7-DBT: 548 | 8-LOSS: 284
- CRE concentration: **390.91% of capital** vs SR 07-1 threshold of **300%** — in breach (breach_flg=Y)

---

## Q02: Cascadia Tower Covenant Trap

**Question:**
> What type of covenants does the Cascadia Tower loan (CRE-2021-00847) actually have, and what is its current LTV based on the latest appraisal?

**Sources:** TBL_LOAN_MSTR, TBL_COLLATERAL, TBL_COVENANT, TBL_COVENANT_TEST | credit_committee_memo_cascadia_tower.txt, appraisal_report_cascadia_tower_2023.txt

**Trap:** This loan has ICR and DEBT_YLD covenants, NOT DSCR — agent must read actual covenant types from data, not assume DSCR. LTV requires joining collateral table. Current LTV is 1.0064 (underwater).

**Expected Answer:**
- Covenants: 2 covenants (**ICR** threshold=1.72, **DEBT_YLD** threshold=0.0928), both with 16 tests, **all FAIL**
  - ICR actual range: 0.52–1.44 | DEBT_YLD actual range: 0.045–0.092
- Collateral: orig_appr_val=**$131M** → curr_appr_val=**$78M** (**40.5% decline**), occupancy=**38%**
- LTV: **0.6489** (orig) → **1.0064** (current — underwater)
- Loan: orig_amt=**$85M**, curr_bal=**$78.5M**, status=WKOT, rating=7-DBT, rate=3.875% fixed

---

## Q03: ALLL Provision Reconciliation

**Question:**
> Reconcile the total ALLL provision for CRE office loans in the database with the ALLL memo's stated figures — do they match?

**Sources:** TBL_PROVISION, TBL_LOAN_MSTR | alll_methodology_memo_2023.txt, occ_consent_order_2023_ce_0847.txt, examiner_report_capital_adequacy.txt

**Trap:** Database provision table stores daily snapshots back to 2019. Sum = $67.19B. Memo says $167.5M. That's a ~400x gap. Agent must flag this mismatch, not silently use one number.

**Expected Answer:**
- Database: total provisions **$67.19B** across 8,761 distinct loans, balance **$167.0B**, implied ratio **~40.24%**
- ALLL memo: **$167.5M** for CRE Office (4.35% rate = 0.85% base + 3.50% Q-factor), **$432M** total ALLL
- Data quality flag: **$67.19B vs $167.5M** — ~400x scale mismatch, agent must call this out
- Q-factor history: +0.50% (2021) → +0.75% (Q1 2022) → +1.00% (Q2-Q4 2022) → +1.50% (Q1 2023) → +2.00% (Q2 2023) → +3.00% (Q3 2023) → +3.50% (Q4 2023)
- OCC: Q-factors understated by **1.0-1.5 pp** (Q3 2022–Q1 2023), ALLL shortfall **$45-65M**

---

## Q04: DSCR Breach Cascade

**Question:**
> How many distinct CRE loans had un-waived DSCR covenant breaches in 2023, and what is the total charge-off exposure for those specific loans?

**Sources:** TBL_COVENANT, TBL_COVENANT_TEST, TBL_LOAN_MSTR, TBL_WORKOUT, TBL_CHARGE_OFF | interagency_cre_workout_policy_2023.pdf

**Trap:** Requires join chain: covenant_test → covenant (filter DSCR type) → loan_mstr (filter CRE). Must count DISTINCT loans (not test records — 19,059 records but only 10,459 distinct loans). Must then join to TBL_CHARGE_OFF for those loan_ids only. Waiver filter is `waiver_flg = 'N'`.

**Expected Answer:**
- DSCR failures in 2023, not waived: 19,059 test records → **10,459 distinct CRE loans** (**$111.94B**)
- Status breakdown: ACTV **6,227** | DLQ30 1,024 | PAID 658 | DLQ90 611 | DLQ60 561 | NACC 420 | DFLT 406 | WKOT **221** | FCLS **193** | REO 78 | CHGOFF **60**
- Workout records for these loans: **1,318** (across 8 types)
- Charge-offs for these loans: **$2.98B**

---

## Q05: CET1 vs Tier 1 Capital Trap

**Question:**
> What is PNB's current CET1 capital amount in dollars, and under the severe adverse stress scenario, does CET1 stay above the 7.0% well-capitalized threshold?

**Sources:** TBL_CAPITAL, TBL_CHARGE_OFF, TBL_PROVISION | stress_test_severe_adverse_2023.txt, regulatory_capital_plan_occ_submission.txt, examiner_report_capital_adequacy.txt, occ_consent_order_2023_ce_0847.txt

**Trap:** TBL_CAPITAL has both `cet1_ratio` and `tier1_ratio`. CET1 capital ($2.281B) must be derived as cet1_ratio x RWA, not by using `tier1_cap` ($2.434B). Stress test projections are document-only (6.1% trough — below 7.0%).

**Expected Answer:**
- CET1 capital = **$2.281B** (10.32% x $22.1B RWA) — NOT $2.434B which is Tier 1
- CET1 trajectory: **10.70%** (Q4 2021) → **9.26%** (Q4 2022) → **8.08%** (Q4 2023) → **7.84%** (Q1 2024, trough) → **10.32%** (Q2 2025)
- Stress test: CET1 trough at **6.1%** — breaches the **7.0%** well-capitalized threshold
- Post-mitigation: **7.8%** (barely above 7.0%)
- Capital plan: $175M sub debt + $412M loan sale + $200M RWA optimization + dividend suspension → target **>9.0%** by Q3 2024

---

## Q06: MRIA Filter Precision

**Question:**
> How many MRIA-level findings from OCC examinations are still open or in-progress?

**Sources:** TBL_EXAM_FINDING | occ_consent_order_2023_ce_0847.txt, examiner_report_capital_adequacy.txt

**Trap:** Table contains findings from OCC_FULL, OCC_TARG, INT_AUDIT, EXT_AUDIT, and BOARD_REV. Without filtering to OCC exam types only, count inflates from 196 to 502. The question says "OCC examinations" — agent must apply the filter.

**Expected Answer:**
- Open/In-Progress MRIA from OCC exams: **196** (NOT 502 which includes all exam types)
- Status split: **IN_PROGRESS: 106, OPEN: 90**
- 11 categories: RISK_RTG (**24**), CAP_PLAN (**23**), IT_SEC (20), COLL_MGMT (20), GOVERNANCE (18), APPR_QUAL (17), BSA_AML (17), VENDOR_MGMT (16), ALLL_MTHD (15), CRE_CONC (14), UW_EXCEPT (12)
- Past due: **196 of 196 (100%)** — all past due
- Data quality flag: consent order cites **12 MRIAs**, database has **196** — agent should note this discrepancy

---

## Q07: Loan Sale CET1 Arithmetic

**Question:**
> If PNB sells the $412M loan pool at 92 cents on the dollar, what is the post-sale CET1 ratio?

**Sources:** TBL_CAPITAL, TBL_CONCENTRATION, TBL_LOAN_MSTR | loan_sale_term_sheet_performing_pool.txt, regulatory_capital_plan_occ_submission.txt, occ_consent_order_2023_ce_0847.txt

**Trap:** Must derive CET1 capital from `cet1_ratio x rwa` ($2.281B), not use `tier1_cap` ($2.434B). After-tax loss at 21% = ~$26M. RWA reduces by $412M. Correct answer is ~10.39%. Using Tier 1 gives the wrong answer of ~11.10%.

**Expected Answer:**
- Current: CET1 ratio=**10.32%**, RWA=**$22.1B**, CET1 capital~**$2.281B**
- Gross loss: **$32.96M** ($412M x 8%), after-tax loss: **~$26M** (at 21% tax rate)
- Post-sale CET1 capital: ~**$2.255B**, RWA: ~**$21.7B**
- **New CET1 ratio: ~10.39%** — NOT 11.10% which uses the wrong capital figure
- CRE concentration: 390.91% → ~380% (partial progress toward 300% target)

---

## Q08: REO Unsold Exposure

**Question:**
> What is PNB's total at-risk exposure from unsold REO properties, including both acquisition value and accumulated carrying costs?

**Sources:** TBL_REO, TBL_COLLATERAL, TBL_LOAN_MSTR | foreclosure_timeline_mercer_industrial.txt

**Trap:** `sale_dt` and `sale_val` are NULL for unsold properties — agent must handle NULLs correctly to split sold vs unsold. Exposure = acq_val + carrying_cost (must include both, not just one).

**Expected Answer:**
- Total REO: **613** (**241 sold**, **372 unsold**)
- Unsold REO exposure: **$5.67B** (acq_val **$5.41B** + carrying_cost **$260M**)
- Total carrying cost (all REO): **$428.8M**
- Avg days held: sold **425 days**, unsold **798 days**
- Largest sold loss: **REO-00299** (loan CRE-2021-23233): acq=$65.1M, sale=$50.3M, carrying=$3.2M → **loss=$18.0M**

---

## Q09: Underwriting Exception Rate

**Question:**
> The internal audit report says 23% of CRE originations in 2021-2022 had underwriting exceptions — does the full database confirm that rate?

**Sources:** TBL_LOAN_MSTR, TBL_BRANCH | internal_audit_report_cre_lending_2023.txt, occ_consent_order_2023_ce_0847.txt

**Trap:** Table has `uw_exception_flg` (Y/N) but no exception types — types are document-only. The audit's 23% came from a sample of 1,200 loans; full data shows 22.90%. Agent should note the sampling difference, not just echo "23%". Agent must NOT fabricate exception categories from the database.

**Expected Answer:**
- Full population: **22.90%** (4,169 / 18,205) — close but not exactly 23%
- Audit sampled 1,200 of 5,847 loans — smaller sample explains the rounding difference
- Top 3 branches: **PNB Billings (BR-023) 27.51%**, **PNB Lake Oswego (BR-008) 25.10%**, **PNB San Francisco (BR-027) 24.91%**
- Exception types (FROM AUDIT DOC ONLY): DSCR below 1.25x (42%), LTV above 75% (28%), missing Phase I (18%), missing Credit Committee approval (12%)
- Consent order Article V (60-day): revise underwriting, Credit Committee approval for all CRE >$5M

---

## Q10: DSCR by Occupancy — 4-Table Join

**Question:**
> For CRE office loans, what is the covenant failure rate for properties with occupancy below 50% versus above 85%?

**Sources:** TBL_COLLATERAL, TBL_LOAN_MSTR, TBL_COVENANT, TBL_COVENANT_TEST | credit_committee_memo_cascadia_tower.txt

**Trap:** Requires 4-table join: loan_mstr → collateral (occupancy is here, not in loan table) → covenant (filter DSCR) → covenant_test. Occupancy is stored as 0-1 decimal, not percentage. Multi-collateral loans can cause duplication.

**Expected Answer:**

| Occupancy | Avg DSCR | Fail Count | Total Tests | Fail % |
|-----------|----------|------------|-------------|--------|
| <50% | 1.1845 | 9,569 | 13,433 | 71.24% |
| 50-70% | 1.1722 | 10,237 | 14,064 | 72.79% |
| 70-85% | 1.1713 | 7,587 | 10,491 | 72.32% |
| >=85% | 1.1668 | 6,544 | 8,955 | **73.08%** |

- Counterintuitive: higher occupancy has a slightly **higher** failure rate (73.08% vs 71.24%)
- Suggests covenant thresholds are set too aggressively relative to market conditions, or higher-occupancy properties carry proportionally more debt
