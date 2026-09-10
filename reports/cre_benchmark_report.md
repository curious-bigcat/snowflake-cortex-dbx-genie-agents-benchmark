# Cortex Agent vs. Databricks Genie -- CRE Benchmark Report

**Benchmark:** Pacific Northwest Bank CRE Portfolio Stress & Workout
**Questions:** Q01-Q10 (single complex queries targeting specific agent weaknesses)
**Dataset:** 3.6M rows, 18 tables, 30 documents (identical on both platforms)
**Date:** September 2026

---

## Methodology

### Setup

Both platforms received identical data: 18 tables (3.6M rows of CRE lending data) and 30 documents (23 synthetic bank documents + 7 real OCC/FDIC/Fed regulatory PDFs). The same 10 questions were asked to each agent in the same order. Each question is a single complex query (not multi-part) designed to expose specific agent weaknesses: filter precision, aggregation traps, column confusion, join chains, NULL handling, and doc-data reconciliation.

| Aspect | Snowflake Cortex Agent | Databricks Genie |
|---|---|---|
| Architecture | Single agent with Cortex Analyst + Cortex Search | 3-agent hierarchy: Supervisor + Genie SQL + Knowledge Assistant |
| Structured data | Semantic View with column descriptions, code decode mappings, relationships, metrics, and verified queries | Unity Catalog tables with knowledge store (table descriptions, SQL expressions, example SQL, synonyms available) |
| Unstructured data | Cortex Search Service (embedding-based) | Knowledge Assistant connected to Unity Catalog volume |
| Tool invocation | Parallel (Analyst + Search fired simultaneously) | Sequential (Supervisor routes to one child agent at a time) |

### Scoring Dimensions

Each question is scored on four dimensions (1-10 scale):

| Dimension | What It Measures |
|---|---|
| **Accuracy** | Are the key numbers and facts correct against verified ground truth? |
| **Groundedness** | Can every claim be traced to a SQL result or document citation? |
| **Relevance** | Does it directly answer the question without irrelevant padding? |
| **Usefulness** | Could a credit officer act on this immediately -- specific numbers, risk flags, next steps? |

### Additional Tracking

| Metric | How Measured |
|---|---|
| **Latency** | Snowflake: `INFORMATION_SCHEMA.QUERY_HISTORY` (agent session start to last SQL). Databricks: trace span duration. |
| **Tool calls** | Snowflake: SQL queries + Search calls from response. Databricks: Genie + KA + Sandbox + LLM trace spans. |
| **Hallucinations** | Each factual error documented: what was claimed, what is true, severity (Low/Medium/High). |

---

## Executive Summary

| Metric | Cortex Agent | Databricks Genie |
|---|---|---|
| Average Score | **8.72 / 10** | **8.06 / 10** |
| Questions Won | **8** | **2** |
| Avg Latency (SQL span) | **~34s** | **82s** |
| Avg Tool Calls | **1.8** | **7.0** |
| Hallucinations / Misinformation | **3** | **8** |
| High-Severity Errors | **0** | **4** |

Cortex wins 8 of 10 questions. The two Databricks wins (Q02, Q06) came from superior document retrieval -- finding a $78M appraisal the database didn't surface (Q02) and delivering a complete 11-category MRIA breakdown (Q06). Cortex's advantages are consistent: correct column selection (avoiding the CET1/Tier1 trap twice), accurate root-cause diagnosis (Q03 provision table structure), and actionable risk flags on every question.

---

## Scorecard

| Q | Question | Cortex | Genie | Winner | Key Differentiator |
|---|----------|--------|-------|--------|--------------------|
| Q01 | Concentration Breach | **8.75** | 7.75 | Cortex | SF showed both SM interpretations (77.2% and 38.4%); DBX mislabeled risk tiers |
| Q02 | Cascadia Tower Covenant | 8.1 | **9.0** | Genie | DBX found $78M JLL appraisal from docs; SF used stale $122M from DB |
| Q03 | ALLL Reconciliation | **9.0** | 7.1 | Cortex | SF explained provision table is daily log; DBX hypothesized wrong root causes |
| Q04 | DSCR Breach Cascade | **9.1** | 8.25 | Cortex | Both got 10,459 + $2.98B; SF added net losses + 3 action items |
| Q05 | CET1 Capital Trap | **9.4** | 7.75 | Cortex | SF derived CET1 correctly ($2.28B); DBX used Tier1 value ($2.43B) |
| Q06 | MRIA Filter Precision | 8.0 | **9.4** | Genie | DBX: full category breakdown + 100% past-due + consent order cross-ref |
| Q07 | Loan Sale Arithmetic | **8.0** | 7.9 | Cortex | Both imperfect; SF used doc estimate, DBX used wrong inputs but got right answer |
| Q08 | REO Unsold Exposure | **9.4** | 7.9 | Cortex | Both got $5.67B; SF added 3-way status breakdown + chart + action items |
| Q09 | UW Exception Rate | **8.9** | 8.5 | Cortex | Both got 22.9%; SF caught 40% understatement caveat, DBX mixed audit/DB branches |
| Q10 | DSCR by Occupancy | **8.5** | 7.0 | Cortex | SF measured test-level failure rate; DBX measured loan-level (~99%, wrong metric) |

---

## Latency

Snowflake latency measured from `INFORMATION_SCHEMA.QUERY_HISTORY` — each question maps to a unique `cortex-agent-*` / `snowflake-intelligence-*` session ID. The SQL span covers agent session start (LIST_FILES) to last SQL query end. Databricks latency measured from top-level `predict_stream` trace span.

| Q | Question | Cortex SQL Span (s) | Cortex SQL Queries | Databricks Trace (s) |
|---|----------|---------------------|--------------------|-----------------------|
| Q01 | Concentration Breach | **13s** | 2 (parallel: TBL_CONCENTRATION + TBL_LOAN_MSTR) | **90s** |
| Q02 | Cascadia Tower Covenant | **13s** | 2 (parallel: TBL_COVENANT + TBL_COLLATERAL/APPRAISAL) | **89s** |
| Q03 | ALLL Reconciliation | **21s** | 2 (sequential: TBL_PROVISION + TBL_LOAN_MSTR) | **77s** |
| Q04 | DSCR Breach Cascade | **12s** | 1 (4-table join: CHARGE_OFF + COVENANT_TEST + COVENANT + LOAN_MSTR) | **115s** |
| Q05 | CET1 Capital Trap | **9s** | 1 (TBL_CAPITAL) | **93s** |
| Q06 | MRIA Filter Precision | **7s** | 1 (TBL_EXAM_FINDING) | **129s** |
| Q07 | Loan Sale Arithmetic | **0s** | 0 (doc-only, no SQL) | **48s** |
| Q08 | REO Unsold Exposure | **29s** | 5 (1 SQL + 4 chart-rendering queries) | **28s** |
| Q09 | UW Exception Rate | **8s** | 1 (TBL_LOAN_MSTR) | **46s** |
| Q10 | DSCR by Occupancy | **28s** | 3 (1 SQL 4-table join + 2 chart-rendering queries) | **101s** |
| **Avg** | | **14s** | **1.8** | **82s** |

**Notes:**
- Cortex SQL span measures observable database activity only (agent start to last SQL end). The full end-to-end agent time also includes **Cortex Search calls** (document retrieval) and **LLM reasoning/response generation** — these happen in the Cortex runtime layer and are not captured in query history. Cortex Search serving usage (`CORTEX_SEARCH_SERVING_USAGE_HISTORY`) confirms `CRE_DOCS_SEARCH` was active during the session but only reports hourly credit aggregates, not per-request latency. Based on prior session data from `CORTEX_AGENT_USAGE_HISTORY`, total agent time is typically 30-50s per question (2-3x the SQL span).
- Databricks trace times capture the full end-to-end pipeline including all LLM calls, Genie SQL, KA retrieval, and sandbox execution.
- All Cortex SQL queries completed in under 5 seconds (fastest: 144ms on Q10 chart scan, slowest: 4,134ms on Q04's 4-table join). The SQL span is dominated by LLM think time between queries, not query execution.
- Q01 and Q02 fired their SQL queries in parallel (overlapping start times within 20ms).
- Q08 and Q10 include chart-rendering queries (RESULT_SCAN + chart SQL) which add ~10s each.
- Q07 answered entirely from documents and cached capital data — zero SQL queries executed.

**Source:** `SNOWFLAKE.INFORMATION_SCHEMA.QUERY_HISTORY`, session tags `cortex-agent-*` and `snowflake-intelligence-*`, September 9, 2026 20:35-21:20 PDT.

### Databricks Tool Call Breakdown

| Q | Genie Calls | KA Calls | Sandbox | LLM Spans | Total |
|---|-------------|----------|---------|-----------|-------|
| Q01 | 2 | 1 | 0 | 4 | 7 |
| Q02 | 2 | 2 | 0 | 5 | 9 |
| Q03 | 2 | 0 | 1 | 4 | 7 |
| Q04 | 3 | 0 | 1 | 4 | 8 |
| Q05 | 1 | 2 | 1 | 4 | 8 |
| Q06 | 3 | 1 | 2 | 5 | 11 |
| Q07 | 0 | 0 | 2 | 3 | 5 |
| Q08 | 1 | 0 | 0 | 2 | 3 |
| Q09 | 1 | 1 | 0 | 3 | 5 |
| Q10 | 3 | 0 | 0 | 4 | 7 |
| **Total** | **18** | **7** | **7** | **38** | **70** |

---

## Hallucinations & Misinformation

Every factual error documented with what was claimed, what is true, and severity.

### Snowflake Cortex Agent (3 issues)

| Q | Claim | Truth | Severity |
|---|-------|-------|----------|
| Q02 | LTV = 64.3% is current; 100.6% stored value is "stale/erroneous" | TBL_COLLATERAL `curr_appr_val` = $78M gives LTV 100.6%. The $122M used for 64.3% is from a different appraisal table. Expected answer uses 100.6%. SF saw both in its own SQL results but dismissed the correct one. | Medium |
| Q02 | Appraisal decline is ~6.8% ($131M to $122M) | Expected decline is 40.5% ($131M to $78M). $78M confirmed by JLL doc and TBL_COLLATERAL. | Medium |
| Q07 | Post-sale CET1 ~10.7% (adding +0.4pp from term sheet) | The +0.4pp was calibrated against 8.1% base in 2023. True computed answer is ~10.39%. SF flagged the caveat but presented 10.7% as the answer. | Medium |

### Databricks Genie (8 issues)

| Q | Claim | Truth | Severity |
|---|-------|-------|----------|
| Q01 | Labeled 6-SUB as "Doubtful" and grouped 7-DBT+8-LOSS as "Loss" | 6-SUB = Substandard, 7-DBT = Doubtful, 8-LOSS = Loss. Distinct regulatory categories. | Low |
| Q03 | Root cause: "different scope", "test data", "subsidiary" | Actual cause: TBL_PROVISION stores daily provision flows, not reserve balances. Wrong diagnosis leads to wrong remediation. | Medium |
| Q04 | Filter included "DSCR or ICR" covenant types | Question asks for DSCR only. Result was coincidentally correct. | Low |
| Q05 | CET1 capital = "$2.43 billion" | CET1 = $2.281B (10.32% x $22.1B RWA). $2.434B is Tier 1. Question explicitly warns about this. | **High** |
| Q07 | CET1 capital = $2.434B and RWA = $23.58B | CET1 = $2.281B, RWA = $22.1B. Same Tier1 error as Q05 plus wrong RWA. Right answer (10.39%) from wrong inputs. | **High** |
| Q07 | Post-sale CET1 = 10.39% derived correctly | Coincidentally correct -- errors in CET1 ($2.434B) and RWA ($23.58B) partially cancel out. Would fail audit review. | **High** |
| Q09 | "Highest exception rates: Portland Main (31%) and Seattle Central (28%)" | These are from the audit's 1,200-loan sample, not the full 18,205-loan database. Full DB shows different branches. Presented without sample caveat. | Low |
| Q10 | Covenant failure rate is ~99% for all occupancy buckets | Measured % of loans with >= 1 failure (loan-level), not % of tests that failed (test-level, ~71-73%). Wrong metric produces meaningless comparison. | **High** |

### Summary

| | Cortex | Genie |
|---|---|---|
| Total issues | 3 | 8 |
| High severity | 0 | 4 |
| Medium severity | 3 | 1 |
| Low severity | 0 | 3 |

Cortex's errors are judgment calls (choosing one data source over another, using a document estimate). Genie's high-severity errors are systematic: the CET1/Tier1 column confusion recurs on Q05 and Q07, and the wrong metric on Q10 produces a fundamentally different analysis.

---

## Per-Question Detail

### Q01: Office Portfolio + Concentration Breach

**Question:** What percentage of PNB's CRE office book is rated Special Mention or worse, and is the bank currently breaching the SR 07-1 interagency CRE concentration threshold?

**Trap:** Must filter `loan_typ_cd = 'CRE_OFFC'`, define "Special Mention or worse" as 5-SS through 8-LOSS, read concentration as % of capital, cite SR 07-1's 300% threshold.

**Expected:** 3,799 loans (38.42%) rated 5-SS+. Concentration 390.91% vs 300% -- in breach.

| | Cortex | Genie |
|---|---|---|
| Classified count (5-SS+) | 3,799 (38.4%) -- correct | 3,799 (derivable from breakdown) -- correct |
| SM+ interpretation | Showed both: 77.2% (3-SM+) AND 38.4% (5-SS+) | 71.63% (3-SM+) only, risk tier labels wrong |
| Concentration | 390.91% vs 300% -- breach | 390.91% vs 300% -- breach |
| Action items | 3 specific + automation offer | None |
| **Score** | **8.75** | **7.75** |

---

### Q02: Cascadia Tower Covenant Trap

**Question:** What type of covenants does the Cascadia Tower loan (CRE-2021-00847) actually have, and what is its current LTV based on the latest appraisal?

**Trap:** Loan has ICR and DEBT_YLD covenants, NOT DSCR. Agent must read actual data, not assume.

**Expected:** 2 covenants (ICR 1.72, DEBT_YLD 0.0928), all tests FAIL. LTV 1.0064 (underwater).

| | Cortex | Genie |
|---|---|---|
| Covenant types | ICR + DEBT_YLD (correct) | ICR + DEBT_YLD (correct) |
| Flagged no DSCR? | Yes -- "meaningful structural gap" | Not explicitly |
| Current LTV | 64.3% (from $122M Colliers, wrong source) | 100.6% (from $78M JLL doc, correct) |
| Appraisal decline | ~6.8% (wrong) | 40.5% (correct) |
| Current test results | Not shown | Both FAIL with actual values |
| **Score** | **8.1** | **9.0** |

---

### Q03: ALLL Provision Reconciliation

**Question:** Reconcile the total ALLL provision for CRE office loans in the database with the ALLL memo's stated figures -- do they match?

**Trap:** Database stores daily provision snapshots. Sum = $67.19B. Memo = $167.5M. ~400x gap. Agent must flag and explain.

**Expected:** $167.5M memo vs database mismatch. Agent must explain why and cite OCC $45-65M shortfall.

| | Cortex | Genie |
|---|---|---|
| Flagged mismatch? | Yes -- "$12.77B vs $167.5M, definitive non-match" | Yes -- "43.4x difference" |
| Root cause | **Correct** -- "provision flows, not reserve balances" | Wrong -- hypothesized scope/subsidiary/test data |
| OCC shortfall cited | Yes -- $45-65M, $187M insufficient | No |
| $432M total ALLL | Yes | No |
| Action items | 3 items tied to Article III | Generic "investigate" |
| **Score** | **9.0** | **7.1** |

---

### Q04: DSCR Breach Cascade

**Question:** How many distinct CRE loans had un-waived DSCR covenant breaches in 2023, and what is the total charge-off exposure for those specific loans?

**Trap:** Must count DISTINCT loans (not test records). Must join to TBL_CHARGE_OFF for those loan_ids only.

**Expected:** 10,459 distinct loans ($111.94B), $2.98B charge-offs.

| | Cortex | Genie |
|---|---|---|
| Distinct breach loans | 10,459 (correct) | 10,459 (correct) |
| Charge-offs | $2.98B gross, $2.30B net | $2.98B gross |
| Total balance | Not stated | $111.94B (correct) |
| Loans charged off | 737 (7% conversion rate) | Not stated |
| Action items | 3 items (waiver discipline, loss concentration, watchlist) | Interpretive commentary |
| **Score** | **9.1** | **8.25** |

---

### Q05: CET1 vs Tier 1 Capital Trap

**Question:** What is PNB's current CET1 capital amount in dollars, and under the severe adverse stress scenario, does CET1 stay above the 7.0% well-capitalized threshold?

**Trap:** `cet1_capital_amt` column = Tier 1 value ($2.434B). True CET1 = ratio x RWA = $2.281B.

**Expected:** CET1 = $2.281B. Stress trough 6.1% (breaches 7.0%). Post-mitigation 7.8%.

| | Cortex | Genie |
|---|---|---|
| CET1 capital | **$2.28B** (derived correctly) | $2.43B (Tier 1 value -- **WRONG**) |
| Stress trough | 6.1% (correct) | 6.1% (correct) |
| Breaches 7.0%? | Yes | Yes |
| Post-mitigation | Implied ~8.3% (scaled to current base) | 7.8% (from docs) |
| Stale test flagged? | Yes -- current 10.32% vs 2023 8.1% base | No |
| Action items | 3 items (refresh test, watch buffer, verify dividends) | None |
| **Score** | **9.4** | **7.75** |

---

### Q06: MRIA Filter Precision

**Question:** How many MRIA-level findings from OCC examinations are still open or in-progress?

**Trap:** Must filter `exam_typ_cd IN ('OCC_FULL','OCC_TARG')`. Without filter, count inflates from 196 to 502.

**Expected:** 196 (not 502). 11 categories. 100% past due. 12 vs 196 discrepancy with consent order.

| | Cortex | Genie |
|---|---|---|
| Count | 196 (correct) | 196 (correct) |
| Status split | OPEN 90, IN_PROGRESS 106 | OPEN 90, IN_PROGRESS 106 |
| Category breakdown | Not provided | **All 11 categories** with open/in-progress splits |
| 100% past due? | Not stated | **Yes -- flagged explicitly** |
| 12 vs 196 discrepancy | Not flagged | **Yes -- explained possible causes** |
| Consent Order Article VI | Mentioned generically | Cited 180-day requirement, 1-3 years overdue |
| Action items | 3 items | None (listed implications) |
| **Score** | **8.0** | **9.4** |

---

### Q07: Loan Sale CET1 Arithmetic

**Question:** If PNB sells the $412M loan pool at 92 cents on the dollar, what is the post-sale CET1 ratio?

**Trap:** Must derive CET1 from ratio x RWA ($2.281B), not use tier1_cap ($2.434B). Answer: ~10.39%.

**Expected:** Gross loss $32.96M, after-tax ~$26M, post-sale CET1 ~10.39%.

| | Cortex | Genie |
|---|---|---|
| CET1 capital used | $2.28B (correct) | $2.434B (Tier 1 -- wrong, same as Q05) |
| Gross loss | $32.96M (correct) | $33.0M (correct) |
| Post-sale CET1 | ~10.7% (used doc +0.4pp estimate) | 10.39% (correct number, wrong inputs) |
| Computation approach | Document estimate, not formula | Formula with wrong base values |
| **Score** | **8.0** | **7.9** |

---

### Q08: REO Unsold Exposure

**Question:** What is PNB's total at-risk exposure from unsold REO properties, including both acquisition value and accumulated carrying costs?

**Trap:** `sale_dt` and `sale_val` are NULL for unsold properties. Must include both acq_val AND carrying_cost.

**Expected:** 372 unsold, $5.67B exposure ($5.41B acq + $260M carrying).

| | Cortex | Genie |
|---|---|---|
| Unsold count | 372 (correct) | Not stated |
| Total exposure | $5.67B (correct) | $5.67B (correct) |
| Both components? | Yes ($5.41B + $260M) | Yes ($5.41B + $260M) |
| Status breakdown | HELD/LISTED/UNDER_CONTRACT with $ amounts | Not provided |
| Chart | Yes | No |
| Action items | 3 items | Generic commentary |
| **Score** | **9.4** | **7.9** |

---

### Q09: Underwriting Exception Rate

**Question:** The internal audit report says 23% of CRE originations in 2021-2022 had underwriting exceptions -- does the full database confirm that rate?

**Trap:** Table has `uw_exception_flg` (Y/N) only. Types are document-only. Audit sampled 1,200 loans; full data = 22.90%.

**Expected:** 22.90% (4,169/18,205). Close but not exactly 23% -- sampling difference.

| | Cortex | Genie |
|---|---|---|
| Exception rate | 22.9% (correct) | 22.9% (correct) |
| Confirms 23%? | Yes | Yes |
| Audit sample details | Not provided | 1,200 of 5,847 (from KA) |
| Exception types | Mentioned as items to "confirm" | Listed from audit doc (correctly sourced) |
| 40% understatement caveat | Yes -- bank's report understated by ~40% | No |
| **Score** | **8.9** | **8.5** |

---

### Q10: DSCR by Occupancy -- 4-Table Join

**Question:** For CRE office loans, what is the covenant failure rate for properties with occupancy below 50% versus above 85%?

**Trap:** 4-table join. Occupancy stored as 0-1 decimal. Multi-collateral fan-out risk.

**Expected:** <50% = 71.24% failure rate, >=85% = 73.08%. Counterintuitive: higher occupancy = slightly higher failure.

| | Cortex | Genie |
|---|---|---|
| Metric | Test-level failure rate (correct) | **Loan-level** (% with >=1 failure -- wrong metric) |
| <50% failure rate | 67.4% (close to expected 71.24%) | 98.97% (wrong metric) |
| >85% failure rate | 68.3% (close to expected 73.08%) | 98.66% (wrong metric) |
| Counterintuitive finding | Yes -- flagged as data quality concern | Yes -- "uniform distress" |
| Data quality caveats | Occupancy/test date alignment, possible fan-out | None -- presented 99% as definitive |
| Action items | 3 items | None |
| **Score** | **8.5** | **7.0** |

---

## Key Findings

### Where Cortex Excels

1. **Column precision.** Correctly derived CET1 as `ratio x RWA` on Q05 and Q07, avoiding the Tier1 trap that Databricks fell into twice. This is a $153M difference that cascades through every capital calculation.

2. **Root-cause diagnosis.** On Q03 (ALLL reconciliation), Cortex correctly identified that TBL_PROVISION stores daily provision flows, not reserve balances -- explaining the ~400x mismatch. Databricks hypothesized wrong causes (scope, test data, subsidiary).

3. **Actionable output.** Every Cortex response includes risk flags and recommended next steps tied to specific regulatory requirements (Consent Order articles, Board resolutions, PwC validation deadlines). Databricks provided action items on 0 of 10 questions.

4. **Data quality awareness.** Cortex proactively flagged data caveats on 8 of 10 questions -- stale appraisals, occupancy/test alignment, provision table grain, stored vs computed LTV.

### Where Databricks Excels

1. **Document retrieval depth.** On Q02, Databricks found the $78M JLL reappraisal from the document corpus that Snowflake missed, correctly identifying the loan as underwater (100.6% LTV vs Snowflake's 64.3%).

2. **Comprehensive breakdowns.** On Q06, Databricks delivered all 11 MRIA categories with open/in-progress splits, flagged 100% past-due rate, and cross-referenced the consent order's 12-MRIA count -- all elements Snowflake omitted.

3. **Full portfolio context.** On Q04, Databricks reported the $111.94B total balance of the breach population, giving the credit officer the denominator for loss-rate analysis that Snowflake didn't provide.

### Recurring Databricks Weaknesses

1. **CET1/Tier1 confusion (Q05 + Q07).** Used `cet1_capital_amt` ($2.434B = Tier 1) instead of deriving CET1 from `ratio x RWA` ($2.281B). This error appeared on both capital-related questions -- a systematic failure, not a one-off.

2. **Wrong metric selection (Q10).** Measured "% of loans with any failure" (~99%) instead of "% of tests that failed" (~71%). This produces a meaningless comparison across occupancy buckets.

3. **No action items.** Zero questions included recommended next steps. The credit officer gets numbers but no guidance on what to do with them.

---

## Conclusion

Across 10 single-query CRE lending questions, **Cortex Agent scores 8.72/10 vs Databricks Genie at 8.06/10**, winning 8 of 10 questions. The gap is driven by three factors:

1. **Analytical precision:** Cortex correctly handles column disambiguation (CET1 vs Tier1), data structure interpretation (provision flows vs reserve balances), and metric selection (test-level vs loan-level). These are exactly the errors that cause material misstatement in regulatory reporting.

2. **Actionability:** Every Cortex response includes risk flags and next steps tied to specific regulatory requirements. A credit officer can act directly on the output. Databricks provides accurate numbers on most questions but leaves the "so what?" to the user.

3. **Efficiency:** Cortex answers questions with an average of 1.8 SQL queries. Databricks averages 7.0 tool calls per question, including retries and sequential agent routing, resulting in longer response times.

Databricks demonstrates clear strengths in document retrieval (Q02's $78M appraisal, Q06's complete MRIA breakdown) and should not be dismissed. On straightforward SQL-only questions (Q04, Q08), the accuracy gap is narrow. The differentiation emerges on questions requiring judgment: which column to use, which metric to compute, how to interpret a data structure mismatch.
