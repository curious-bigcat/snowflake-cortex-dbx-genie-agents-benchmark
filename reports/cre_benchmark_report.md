# Cortex Agent vs. Databricks Genie -- CRE Benchmark Report

**Benchmark:** Pacific Northwest Bank CRE Portfolio Stress & Workout
**Questions:** G01-G10 (complex multi-part queries requiring SQL + document retrieval + banking domain reasoning)
**Dataset:** 3.6M rows, 18 tables, 30 documents (identical on both platforms)
**Date:** September 2026

---

## Methodology

### Setup

Both platforms received identical data: 18 tables (3.6M rows of CRE lending data) and 30 documents (23 synthetic bank documents + 7 real OCC/FDIC/Fed regulatory PDFs). The same 10 questions were asked to each agent in the same order.

| Aspect | Snowflake Cortex Agent | Databricks Genie |
|---|---|---|
| Architecture | Single agent with Cortex Analyst + Cortex Search | 3-agent hierarchy: Supervisor + Genie SQL + Knowledge Assistant |
| Structured data | Semantic View with column descriptions, code decode mappings, relationships, metrics, and 8 verified queries | Unity Catalog tables with knowledge store (table descriptions, SQL expressions, example SQL, synonyms available) |
| Unstructured data | Cortex Search Service (embedding-based) | Knowledge Assistant connected to Unity Catalog volume |
| Tool invocation | Parallel (Analyst + Search fired simultaneously) | Sequential (Supervisor routes to one child agent at a time) |
| Model | claude-opus-4-8 | Databricks default (supervisor + child models) |

### Metrics Measured

| Metric | Definition | How Measured |
|---|---|---|
| **Accuracy** | Fraction of question sub-parts answered correctly with verifiable data | Manual evaluation: each sub-part scored as correct/incorrect against ground truth from the database and documents |
| **Groundedness** | Whether each factual claim in the response can be traced to a SQL result or document citation | Manual claim-by-claim verification: grounded = traceable to data/doc, ungrounded = fabricated or from general knowledge |
| **Relevance** | Whether the response directly addresses the question asked, without irrelevant padding or missed sub-parts | Manual evaluation: scored per question based on coverage, focus, and signal-to-noise |
| **Latency** | Wall-clock time from request to complete response | Each platform's native observability. Snowflake: account usage views (`start_time` to `end_time`). Databricks: top-level agent trace span duration. Both measure the same thing -- total time from user question to final response. |
| **Token usage** | Total tokens consumed per question | Each platform's native observability. Snowflake: account usage views with per-model breakdown (cache_read, cache_write, uncached, output). Databricks: LLM span token counts from agent traces. Note: token accounting differs between platforms (see Section 4). |
| **Tool calls** | Number of tool invocations (SQL queries, document searches, code execution) | Both platforms: counted from response content and trace spans. Snowflake: "Retrieved data" = SQL query, "Searched Search" = search call. Databricks: genie/ka/sandbox trace spans. |
| **Tool failures** | Tool calls that returned empty results, wrong data, or timed out | Snowflake: queries returning 0 rows that required retry. Databricks: Genie SQL returning wrong aggregation, KA missing relevant docs, inconsistent query results requiring re-query |
| **Analytical transparency** | Whether the agent proactively flagged data caveats, discrepancies, or reconciliation notes | Manual evaluation: did the response surface nuances (e.g., scope differences, aggregation basis, document-vs-table conflicts) or present numbers without qualification? |

### What We Did NOT Measure

- **Token cost in dollars**: Snowflake reports 6.11 credits total for 10 questions via account usage views. On the Databricks side, Genie One and Genie Agents (including the Supervisor Agent and Knowledge Assistant used in this benchmark) are free for user-initiated usage until January 31, 2027 per Databricks official documentation; only SQL warehouse compute (DBUs) and service-principal usage are billed. Since the two platforms use fundamentally different billing models and Databricks is currently in a promotional free period for these agent types, a direct dollar comparison is not meaningful at this time.
- **Model capability in isolation**: Both agents use different underlying models. This benchmark measures the full agent system (model + tools + retrieval + schema guidance), not the LLM alone.

---

## Executive Summary

| Metric | Cortex Agent | Databricks Genie | Delta |
|---|---|---|---|
| Accuracy | 95.7% (45/47 sub-parts) | 82.2% (37/45 sub-parts) | +13.5pp |
| Groundedness | 100% (~153 claims, 0 ungrounded) | 89% (~107 grounded / ~120 total claims) | +11pp |
| Relevance | 10/10 questions fully relevant | 9/10 questions fully relevant (G09 undermined by filter error) | +1 |
| Avg Latency | 41s | 155s (2.6 min) | 3.8x faster |
| Tool Calls | 35 total (30 SQL + 5 Search) | 59 total (39 Genie + 13 KA + 7 Sandbox) | 1.7x fewer |
| Tool Failures | 2 (6%) | 6 (10%) | Lower failure rate |
| Doc Retrieval | 5/5 successful (100%) | 11/13 successful (85%) | +15pp |
| Analytical Transparency | 10/10 questions with proactive caveats | 4/10 questions (G03, G05, G07, G09) | +6 questions |
| Snowflake Credits | 6.11 total (10 questions) | N/A (free during promotional period) | -- |

Both platforms demonstrate strong performance on SQL-only questions. The differentiation emerges on hybrid SQL + document questions and complex multi-step queries, where Cortex's parallel tool invocation, semantic view guidance, and self-correction capabilities yield higher accuracy with significantly lower latency.

---

## 1. Accuracy

| Question | Cortex | Databricks | Notes |
|---|---|---|---|
| G01: Office Exposure + SR 07-1 | 4/4 | 5/5 | Both excellent. DBX correctly retrieved SR 07-1 and Consent Order |
| G02: Cascadia Tower Full Analysis | 4/4 | 4/4 | Both answered all 4 sub-parts. DBX correctly routed docs to KA, SQL to Genie |
| G03: ALLL + Q-Factor + OCC | 4/4 | 3.5/4 | DBX: initial Genie SQL returned wrong $67B figure; self-corrected but required 7 Genie calls |
| G04: DSCR Breach Cascade | 5/5 | 4/4 | Both strong. DBX needed 12 Genie calls to reconcile inconsistent categorization |
| G05: CET1 + Stress Test | 5/5 | 5/5 | Both excellent. DBX honestly flagged doc-vs-database CET1 discrepancy |
| G06: Recovery by Property Type | 5/5 | 4/5 | DBX: loss severity / net loss rate conflation; Genie returned confusing aggregate 22.91% |
| G07: UW Exceptions by Branch | 4/4 | 4.5/5 | DBX: graceful fallback -- Genie couldn't find exception types, KA filled from audit report |
| G08: REO Portfolio | 5/5 | 4/5 | DBX: no KA call (missed doc context on REO policy); $5.41B unsold exposure not sanity-checked |
| G09: MRIA Findings | 4/4 | 2.5/5 | **Critical:** DBX returned 502 findings (all severity levels) instead of 12 MRIAs. SQL filter failure. |
| G10: Loan Sale + Capital Impact | 5/5 | 4.5/5 | DBX: best multi-tool orchestration -- KA + Genie + sandbox Python calculation |

**Cortex: 45/47 sub-parts correct (95.7%).** Near-perfect across all question types.

**Databricks: 37/45 sub-parts correct (82.2%).** Strong on SQL-only and well-defined questions. The primary weakness is SQL query precision under ambiguity (G03 wrong aggregation, G09 filter failure, G04 needing 12 calls to reconcile).

---

## 2. Groundedness

Cortex is 100% grounded -- every factual claim traces to a SQL result or cited document (with numbered footnotes). Databricks achieves ~89% groundedness with the corrected KA configuration. Ungrounded claims fall into two categories:

1. **Editorial commentary without source (7 instances):** On SQL-only questions (G06, G08), the Databricks supervisor added market commentary (e.g., "environmental concerns limit industrial recovery," "fire-sale liquidation dynamics") that was reasonable analyst interpretation but not sourced from any SQL result or document.

2. **SQL precision errors presented as fact (6 instances):** When Genie returned inconsistent or wrong aggregations, the supervisor sometimes presented intermediate (wrong) results before self-correcting. The most impactful case is G09, where 502 findings were presented as "MRIA findings" when the SQL likely pulled all severity levels. The system acknowledged the discrepancy with the 12 documented MRIAs but concluded "the backlog has grown" rather than questioning the SQL filter.

| Question | Cortex Grounded | Databricks Grounded |
|---|---|---|
| G01 | 7/7 | 7/7 |
| G02 | All | 6/6 |
| G03 | 12+ | 8/8 (after self-correction) |
| G04 | All | All (SQL + sandbox) |
| G05 | 18+ | 7/7 |
| G06 | All | 18/22 (4 editorial claims ungrounded) |
| G07 | All | 10/10 |
| G08 | All | 8/11 (3 editorial claims ungrounded) |
| G09 | All | 6/10 (core count likely wrong) |
| G10 | All | 9/10 |

---

## 3. Latency

Snowflake latency measured from account usage views (start_time to end_time). Databricks latency measured from top-level agent trace span. Both represent wall-clock time from question to complete response.

| Question | Cortex (s) | Databricks (s) | Ratio |
|---|---|---|---|
| G01: Office Exposure + SR 07-1 | 73 | 128 | 1.8x |
| G02: Cascadia Tower | 50 | 130 | 2.6x |
| G03: ALLL + Q-Factor | 44 | 258 | 5.9x |
| G04: DSCR Breach Cascade | 47 | 558 | 11.9x |
| G05: CET1 + Stress Test | 32 | 122 | 3.8x |
| G06: Recovery by Property Type | 38 | 115 | 3.0x |
| G07: UW Exceptions by Branch | 31 | 81 | 2.6x |
| G08: REO Portfolio | 37 | 86 | 2.3x |
| G09: MRIA Findings | 38 | 122 | 3.2x |
| G10: Loan Sale Impact | 23 | 131 | 5.7x |
| **Average** | **41** | **173** | **4.2x** |

The latency gap correlates with the number of Genie calls. Simple questions with 2-3 Genie calls (G07: 81s, G08: 86s) show modest gaps (2-3x). Questions where Genie SQL needed multiple retries (G04: 12 calls, 558s) show large gaps (12x). Each Genie call costs 17-58s due to the ask_question → start_conversation → poll_for_result cycle.

Cortex's parallel tool invocation (SQL + Search simultaneously) and single-agent architecture contribute to consistently lower latency across all question types.

---

## 4. Token Usage & Cost Efficiency

Snowflake tokens measured from account usage views with per-model breakdown and cache detail. Databricks tokens summed from LLM span counts in agent traces.

### How Snowflake Token Accounting Works

Snowflake's account usage views report the **full context window** for each agent call, including three categories of input tokens:

| Token Category | What It Is | Cost Impact |
|---|---|---|
| **Cache Read** | Tokens from the semantic view, search index, and system prompt that were already cached from prior calls | **90% discount** -- cached tokens are served from memory, not reprocessed by the LLM |
| **Cache Write** | New tokens written to the cache for the first time (e.g., new tool results, retrieved documents) | Full price -- but cached for subsequent calls |
| **Uncached** | Tokens that are neither read from nor written to cache | Full price |
| **Output** | Tokens generated by the model (the actual response text) | Full price |

The "Cortex Total" column in the table below is dominated by cache reads -- these are **not new tokens being processed at full cost**. The actual new work per question is the output tokens (avg 2,540) plus cache write tokens. This is why 10 questions cost only **6.11 credits total** despite a headline token count of 4.75M.

### How Databricks Token Accounting Works

Databricks traces report per-LLM-call context sizes. Because the supervisor agent carries all prior tool outputs in its context window, these grow cumulatively across tool calls within a single question. The token counts reported in traces (e.g., "5.4K" per LLM span) represent per-call context, not deduplicated totals.

### Per-Question Breakdown

| Question | Cortex Total | Cortex New Tokens (output + cache write) | Cortex Cache Read % | Databricks Total | Cortex Credits |
|---|---|---|---|---|---|
| G01 | 531,033 | 86,447 | 84.4% | 38,100 | 0.554 |
| G02 | 382,669 | 83,626 | 78.8% | 73,000 | 0.478 |
| G03 | 428,553 | 14,537 | 97.2% | 537,800 | 0.228 |
| G04 | 456,386 | 120,829 | 74.0% | 552,800 | 0.636 |
| G05 | 484,804 | 126,456 | 74.2% | 102,400 | 0.655 |
| G06 | 413,272 | 28,985 | 93.6% | 50,300 | 0.276 |
| G07 | 448,334 | 154,350 | 65.9% | 261,600 | 0.749 |
| G08 | 551,744 | 202,960 | 63.5% | 700,800 | 0.967 |
| G09 | 623,932 | 16,489 | 97.7% | 719,900 | 0.295 |
| G10 | 429,170 | 217,217 | 49.6% | 449,600 | 0.974 |
| **Total** | **4,749,897** | **851,896** | **78.3%** | **3,486,300** | **6.11** |

### Cost Efficiency Through Caching

Cortex Agent leverages prompt caching to keep costs low even with large context windows. Here is how the 4.75M total tokens break down by cost tier:

- **3.70M (78%) cache reads** -- the semantic view definition, search index, and system prompt are cached in memory across calls and served at a **90% discount**. This is why Cortex can provide rich schema guidance (column descriptions, decode mappings, VQRs) to the model on every call without paying full price each time.
- **1.03M (22%) new tokens** -- cache writes (new tool results and retrieved documents) plus uncached input, billed at full price. These are amortized as subsequent questions benefit from the newly cached content.
- **25K (<1%) output tokens** -- the actual response text generated by the model.

The net result: **6.11 credits for 10 complex banking questions** (avg 0.61 credits/question). The cache mechanism means the cost per additional question decreases as more of the semantic view and search context is cached.

---

## 5. Tool Call Efficiency

| Metric | Cortex | Databricks |
|---|---|---|
| Total tool calls | 35 | 59 |
| Avg per question | 3.5 | 5.9 |
| SQL queries | 30 | 39 (Genie) |
| Document searches | 5 | 13 (KA) |
| Sandbox/code | 0 | 7 |
| Failed/wasted tool calls | 2 (6%) | 6 (10%) |
| Tool success rate | 94% | 90% |

### Tool Failure Breakdown (Databricks)

| Failure Type | Count | Impact |
|---|---|---|
| Genie SQL wrong aggregation (self-corrected) | 2 | G03: $67B initial ALLL; required re-query. G06: 22.91% aggregate rate vs correct 77.4% |
| Genie SQL filter failure (not caught) | 1 | G09: returned 502 findings instead of 12 MRIAs -- fundamental answer wrong |
| Genie couldn't answer (graceful fallback) | 2 | G07: schema didn't have exception types; G10: couldn't identify loan pool. Both recovered via KA |
| Excessive retry loops | 1 | G04: 12 Genie calls to reconcile inconsistent categorization results |

### Cortex Self-Correction

Cortex detected and fixed 2 tool failures without user intervention:
1. **G02:** DSCR query returned 0 rows → investigated all covenant types → found loan only has ICR/Debt Yield → provided substitute + document-sourced DSCR
2. **G03:** Join fan-out inflated balances → self-corrected with ROW_NUMBER() deduplication in second query

---

## 6. Document Retrieval

Both platforms successfully retrieved relevant documents from the CRE corpus. Cortex Search uses embedding-based retrieval. Databricks uses the Knowledge Assistant connected to a Unity Catalog volume.

| Metric | Cortex Search | Databricks KA |
|---|---|---|
| Queries attempted | 5 | 13 |
| Successful retrievals | 5 (100%) | 11 (~85%) |
| Unique documents found | SR 07-1, Consent Order, ALLL memo, workout proposal, borrower financials, audit report, stress test, capital plan, examiner report | SR 07-1, Consent Order, workout proposal, NOI data, Q-factor memo, OCC shortfall assessment, audit report, stress test, capital plan, term sheet |
| Citation quality | Numbered footnotes (e.g., [1], [2]) linking to specific document passages | Numbered citations from KA responses (e.g., citation [1-9]) |

**Cortex** retrieved documents in 5 targeted calls (1 per question that needed docs), finding relevant content on the first attempt each time. The embedding-based search handled multi-concept queries well (e.g., combining ALLL methodology + OCC shortfall in a single search).

**Databricks KA** made 13 calls across the 10 questions, retrieving relevant CRE documents in most cases. Two questions (G06, G08) did not invoke the KA at all -- these were SQL-only questions where document context would have added value (e.g., consent order REO requirements for G08) but was not critical.

---

## 7. Self-Correction and Analytical Transparency

### Self-Correction

Both platforms demonstrated self-correction ability:

**Cortex:**
1. **G02:** DSCR query returned 0 rows → investigated all covenant types → found loan only has ICR/Debt Yield → provided substitute + document-sourced DSCR
2. **G03:** Join fan-out inflated balances → self-corrected with ROW_NUMBER() deduplication

**Databricks:**
1. **G03:** Initial Genie SQL returned $67B ALLL (wrong aggregation) → noticed implausible figure → re-queried → settled on correct $336M
2. **G05:** Flagged that database CET1 (10.7%) differs from KA document CET1 (11.4%) and explained both

### Proactive Caveats and Cross-Referencing

Cortex proactively added caveats, cross-references, and reconciliation notes on every question. Databricks did so on 4 of 10 questions.

Examples of Cortex analytical transparency:
- **G02:** Flagged that the DSCR covenant exists in loan documents but is missing from the structured covenant table -- recommended data governance escalation
- **G03:** Noted that loan-level provision totals differ from the segment-level ALLL memo figure due to aggregation basis, and explained the pre- vs post-remediation timing difference
- **G04:** Explained why the distressed-by-status count (1,378) differs from the workout-record count (1,318)
- **G09:** Distinguished between 502 MRIA records in the warehouse (broad finding log) vs the 12 formal MRIAs cited in the Consent Order (regulatory scope)
- **G10:** Identified term sheet figure differences and noted sub-debt is Tier 2 only (no CET1 benefit)

Examples of Databricks analytical transparency:
- **G03:** Self-corrected the ALLL figure and provided component breakdown (base rate + Q-factor)
- **G05:** Flagged doc-vs-database CET1 discrepancy and explained both measurement points
- **G07:** Noted that structured data lacked exception type detail and transparently fell back to KA documents
- **G09:** Acknowledged 502 vs 12 MRIA discrepancy (though drew incorrect conclusion)

---

## 8. Architectural Observations

### Cortex Strengths

1. **Semantic View with VQRs** provides rich, centralized schema guidance that reduces SQL errors. Column decode mappings, relationships, and verified queries are defined once and available to every call. This helps the agent write correct joins and aggregations on the first attempt.

2. **Parallel tool invocation** lets Cortex fire SQL and Search simultaneously, reducing wall-clock latency. The single-agent architecture avoids the context-passing overhead of multi-agent hierarchies.

3. **Self-correction and analytical transparency** on every question. Cortex consistently surfaces nuances, flags data discrepancies, and distinguishes between different data scopes -- critical for banking analyst workflows where silent errors are worse than flagged uncertainties.

4. **Cache efficiency.** 78.3% cache read rate on input tokens means the semantic view and search context is loaded once and reused at a 90% discount, keeping total cost to 6.11 credits for 10 complex questions.

### Databricks Strengths

1. **Multi-tool orchestration:** The 3-agent architecture (Supervisor + Genie SQL + Knowledge Assistant + Sandbox) enables sophisticated workflows. G10 demonstrated the best example: KA for term sheet details → Genie for current capital → KA for RWA reduction → Sandbox for Python calculation. The sandbox capability for transparent computation is a differentiator.

2. **Graceful fallback when schema is insufficient:** When Genie SQL couldn't answer a sub-question (e.g., exception types in G07, loan pool identification in G10), the system correctly fell back to the Knowledge Assistant and recovered the answer from documents.

3. **Knowledge Assistant document retrieval** (when correctly configured) successfully retrieved relevant CRE regulatory documents with citation indices on 85% of attempts.

### Where Databricks Struggled

1. **SQL query precision under ambiguity:** The Genie SQL engine sometimes returned wrong aggregations (G03: $67B ALLL), inconsistent categorizations (G04: 12 calls to reconcile), or wrong filters (G09: 502 vs 12 MRIAs). This appears related to how natural language questions are decomposed into SQL when column semantics are ambiguous.

2. **Latency scaling with complexity:** Each Genie call costs 17-58s due to the start_conversation → poll cycle. Questions requiring many calls (G04: 12 calls = 558s) become very slow. The sequential supervisor-to-child routing compounds this.

3. **Missed KA opportunities:** On 2 SQL-only questions (G06, G08), the supervisor did not invoke the Knowledge Assistant even though document context would have added value (e.g., regulatory expectations for REO management).

---

## 9. Per-Question Detail

For detailed per-question evaluation with claim-by-claim groundedness analysis, tool call breakdowns, and specific failure modes, see [per_question_evaluation.md](per_question_evaluation.md).

---

## 10. Conclusion

Across 10 complex multi-part banking queries, **Cortex Agent achieves 95.7% accuracy with 100% groundedness at 4.2x faster latency**, compared to Databricks Genie at 82.2% accuracy and ~89% groundedness.

The gap is driven by three factors:

1. **SQL precision:** Cortex's Semantic View with verified queries and decode mappings helps the agent write correct SQL on the first attempt. Databricks' Genie SQL engine sometimes requires multiple retries to produce correct aggregations, particularly when column semantics are ambiguous (e.g., finding severity levels, resolution status codes). This accounts for the accuracy difference and the latency difference on complex questions.

2. **Architectural efficiency:** Cortex's single-agent with parallel tool invocation completes questions in 23-73s. Databricks' 3-agent sequential hierarchy requires 81-558s, with each Genie call adding 17-58s of overhead. Simpler questions show a modest 2-3x gap; complex multi-step questions show 6-12x.

3. **Analytical transparency:** Cortex proactively surfaces data nuances on every question -- scope differences, aggregation basis conflicts, document-vs-table discrepancies. This is critical for banking work where context matters as much as the numbers themselves.

Databricks demonstrated strengths in multi-tool orchestration (particularly G10's KA + Genie + Sandbox workflow) and graceful fallback capability. On well-defined SQL-only questions (G07, G08), the accuracy gap narrows significantly.
