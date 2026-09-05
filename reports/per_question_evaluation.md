# Per-Question Evaluation: Cortex Agent vs Databricks Genie (Final Run)

**Databricks KA: Correctly configured (credocs volume)**

## G01: Office Exposure + SR 07-1

| Dimension | Cortex | Databricks |
|---|---|---|
| Accuracy | 4/4 | 5/5 |
| Groundedness | 7/7 claims grounded | 7/7 claims grounded |
| Relevance | High -- concise, cited sources with footnotes | High -- well-structured, cited KA docs |
| KA/Search Success | Found SR 07-1, Consent Order | Found SR 07-1, Consent Order |
| Tool Calls | 2 (1 SQL + 1 Search) | 5 (3 Genie + 2 KA) |
| Latency | 73s | 128s |
| Notes | Correctly identified 300% as screening indicator, not hard cap | Same -- correctly cited SR 07-1 thresholds and Consent Order 420% |

## G02: Cascadia Tower Full Analysis

| Dimension | Cortex | Databricks |
|---|---|---|
| Accuracy | 4/4 | 4/4 |
| Groundedness | All claims grounded (SQL + doc footnotes) | 6/6 claim clusters grounded |
| Relevance | High -- flagged DSCR data gap, sourced NOI from docs, generated chart | High -- correctly routed each sub-part to right tool |
| KA/Search Success | Found workout proposal, borrower financials, appraisal report | Found workout proposal, NOI data, appraisal details |
| Tool Calls | 8 (6 SQL + 2 Search) | 6 (3 Genie + 3 KA) |
| Latency | 50s | 130s |
| Notes | Self-corrected when DSCR/NOI queries returned empty; flagged data governance issue | Correctly identified no DSCR covenant; KA filled NOI gap |

## G03: ALLL + Q-Factor + OCC Shortfall

| Dimension | Cortex | Databricks |
|---|---|---|
| Accuracy | 4/4 | 3.5/4 |
| Groundedness | 12+ claims grounded with doc citations | 8/8 final claims grounded (after self-correction) |
| Relevance | High -- flagged aggregation basis difference, reconciled pre/post remediation | High -- included ALLL trend table and component breakdown |
| KA/Search Success | Found ALLL memo, Consent Order, examiner report | Found Q-factor memo, OCC shortfall ($45-65M) |
| Tool Calls | 4 (3 SQL + 1 Search) | 10 (7 Genie + 3 KA) |
| Latency | 44s | 258s |
| Notes | Self-corrected join fan-out with ROW_NUMBER() dedup | Initial Genie returned wrong $67B figure; self-corrected but took 7 SQL calls |

## G04: DSCR Breach Cascade + Outcomes

| Dimension | Cortex | Databricks |
|---|---|---|
| Accuracy | 5/5 | 4/4 |
| Groundedness | All claims from SQL results | All claims grounded (SQL + sandbox) |
| Relevance | High -- clean resolution breakdown with $ amounts | High but excessively verbose (~150 lines) |
| KA/Search Success | N/A (SQL-only question) | N/A (correctly didn't call KA) |
| Tool Calls | 5 (5 SQL) | 13 (12 Genie + 1 Sandbox) |
| Latency | 47s | 558s (9.3 min) |
| Notes | 10,459 loans, $112B; clean breakdown in 5 queries | Same count; but needed 12 Genie calls due to inconsistent SQL categorization |

## G05: CET1 Trajectory + Stress Test

| Dimension | Cortex | Databricks |
|---|---|---|
| Accuracy | 5/5 | 5/5 |
| Groundedness | 18+ claims grounded (SQL + 13 doc citations) | 7/7 claim clusters grounded |
| Relevance | High -- full trajectory, driver decomposition, stress + capital plan | High -- flagged doc-vs-database CET1 discrepancy honestly |
| KA/Search Success | Found stress test, capital plan, examiner report, consent order | Found comprehensive response in single KA call |
| Tool Calls | 2 (2 SQL) | 4 (3 Genie + 1 KA) |
| Latency | 32s | 122s |
| Notes | Used prior search context for doc content | Best DBX response -- efficient 4-call orchestration |

## G06: Recovery by Property Type

| Dimension | Cortex | Databricks |
|---|---|---|
| Accuracy | 5/5 | 4/5 |
| Groundedness | All from SQL with verified query | 18/18 SQL claims grounded; 4 editorial claims ungrounded |
| Relevance | High -- created chart, distinguished severity vs absolute impact | High -- clear tables; unsolicited analysis section |
| KA/Search Success | N/A | N/A (didn't call KA) |
| Tool Calls | 2 (2 SQL) | 3 (3 Genie) |
| Latency | 38s | 115s |
| Notes | Used VQR for net charge-off calculation | Genie returned confusing 22.91% aggregate rate; response used correct 77.4% instead |

## G07: Underwriting Exceptions by Branch

| Dimension | Cortex | Databricks |
|---|---|---|
| Accuracy | 4/4 | 4.5/5 |
| Groundedness | All grounded (SQL + 7 doc citations) | 10/10 -- all KA and SQL claims traceable |
| Relevance | High -- flagged branch-coding mismatch between audit report and data | High -- graceful fallback when Genie couldn't determine exception types |
| KA/Search Success | Found audit report, consent order Article V | Found audit report, consent order Article V |
| Tool Calls | 3 (2 SQL + 1 Search) | 3 (2 Genie + 1 KA) |
| Latency | 31s | 81s |
| Notes | Flagged that audit report names different branches than SQL | Best DBX response in G06-G10 set; fast and accurate |

## G08: REO Portfolio Analysis

| Dimension | Cortex | Databricks |
|---|---|---|
| Accuracy | 5/5 | 4/5 |
| Groundedness | All from SQL (3 queries) | SQL-grounded; 3 editorial claims ungrounded |
| Relevance | High -- distinguished absolute loss vs percentage discount | Good -- missing doc context on REO policy |
| KA/Search Success | N/A | N/A (didn't call KA -- missed opportunity) |
| Tool Calls | 5 (5 SQL) | 3 (3 Genie) |
| Latency | 37s | 86s |
| Notes | Provided both top-10 sold losses and unsold exposure detail | $5.41B unsold exposure not sanity-checked |

## G09: MRIA Findings Remediation

| Dimension | Cortex | Databricks |
|---|---|---|
| Accuracy | 4/4 | 2.5/5 |
| Groundedness | SQL counts + 4 doc citations for consent order deadlines | 6/10 -- core count (502 vs 12 MRIA) likely wrong SQL filter |
| Relevance | High -- distinguished 502 warehouse records vs 12 formal MRIAs | Undermined by fundamental count error |
| KA/Search Success | N/A (used prior search context) | Found consent order Article VI (180-day deadline) |
| Tool Calls | 4 (4 SQL) | 5 (4 Genie + 1 KA) |
| Latency | 38s | 122s |
| Notes | Proactively explained scope difference between warehouse and regulatory counts | Acknowledged 502 vs 12 discrepancy but concluded "backlog has grown" rather than questioning the SQL filter |

## G10: Loan Sale Impact on Capital

| Dimension | Cortex | Databricks |
|---|---|---|
| Accuracy | 5/5 | 4.5/5 |
| Groundedness | All from doc citations (15 footnotes) | 9/10 -- SQL + KA + sandbox calculation all traceable |
| Relevance | High -- flagged term sheet version difference, sub-debt Tier 2 only | High -- transparent Python calculation, clear target-distance assessment |
| KA/Search Success | Found term sheet, capital plan, consent order | Found term sheet, capital plan, consent order targets |
| Tool Calls | 2 (2 Search) | 5 (2 Genie + 2 KA + 1 Sandbox) |
| Latency | 23s | 131s |
| Notes | Most efficient Cortex response (search-only, no SQL needed) | Best multi-tool orchestration; graceful pivot when Genie couldn't ID pool |
