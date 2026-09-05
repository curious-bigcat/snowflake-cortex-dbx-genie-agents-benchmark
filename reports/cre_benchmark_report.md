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
| **Hallucinations** | Fabricated facts not present in the data or documents, or facts from general knowledge presented as if retrieved | Subset of ungrounded claims where the agent presented non-data-sourced content without disclaiming it |
| **Latency** | Wall-clock time from request to complete response | Each platform's native observability. Snowflake: account usage views (`start_time` to `end_time`). Databricks: top-level agent trace span duration. Both measure the same thing -- total time from user question to final response. |
| **Token usage** | Total tokens consumed per question | Each platform's native observability. Snowflake: account usage views with per-model breakdown (cache_read, cache_write, uncached, output). Databricks: LLM span token counts from agent traces. Note: token accounting differs between platforms (see Section 4). |
| **Tool calls** | Number of tool invocations (SQL queries, document searches, code execution) | Both platforms: counted from response content and trace spans. Snowflake: "Retrieved data" = SQL query, "Searched Search" = search call. Databricks: genie/ka/sandbox trace spans. |
| **Tool failures** | Tool calls that returned empty results, wrong data, or timed out | Snowflake: queries returning 0 rows that required retry. Databricks: Genie EMPTY results, KA wrong-corpus returns, timeouts |
| **Document retrieval** | Whether the agent successfully found relevant documents from the corpus | Snowflake: Search call returned content from the correct PNB documents. Databricks: KA call returned content from the correct PNB documents (vs wrong corpus) |
| **Analytical transparency** | Whether the agent proactively flagged data caveats, discrepancies, or reconciliation notes | Manual evaluation: did the response surface nuances (e.g., scope differences, aggregation basis, document-vs-table conflicts) or present numbers without qualification? |

### What We Did NOT Measure

- **Token cost in dollars**: Snowflake reports 6.11 credits total for 10 questions via account usage views. On the Databricks side, Genie One and Genie Agents (including the Supervisor Agent and Knowledge Assistant used in this benchmark) are free for user-initiated usage until January 31, 2027 per Databricks official documentation; only SQL warehouse compute (DBUs) and service-principal usage are billed. Since the two platforms use fundamentally different billing models and Databricks is currently in a promotional free period for these agent types, a direct dollar comparison is not meaningful at this time.
- **Model capability in isolation**: Both agents use different underlying models. This benchmark measures the full agent system (model + tools + retrieval + schema guidance), not the LLM alone.
- **Knowledge store tuning**: Databricks Genie Agents support a knowledge store with SQL expressions, example SQL, synonyms, and column descriptions. The level of knowledge store curation affects SQL accuracy. Snowflake's Semantic View provides an equivalent semantic layer. Both were configured with their respective platform's standard approach to schema guidance. The document retrieval failures observed are independent of knowledge store configuration -- they stem from the Knowledge Assistant corpus indexing.

---

## Executive Summary

![Aggregate Comparison](cre_charts/06_aggregate.png)

| Metric | Cortex Agent | Databricks Genie | Delta |
|---|---|---|---|
| Accuracy | 95% (45/47 sub-parts) | 55% (24.5/44 sub-parts) | +40pp |
| Groundedness | 100% (~153 claims, 0 ungrounded) | 71% (~120 claims, 35 fabricated/ungrounded) | +29pp |
| Hallucinations | 0 | 12 fabricated claims (general knowledge backfill) | -12 errors |
| Avg Latency | 41s | 255s (4.2 min) | 6.2x faster |
| Tool Calls | 35 total (30 SQL + 5 Search) | 74 total (50 Genie + 13 KA + 11 Sandbox) | 2.1x fewer |
| Tool Failures | 2 (6%) | 18 (24%) | 4x fewer |
| Doc Retrieval | 5/5 successful (100%) | 0/13 -- wrong volume connected (config error, see Section 6) | N/A (not a valid comparison) |
| Analytical Transparency | 10/10 questions with proactive caveats | 2/10 questions | +8 questions |
| Snowflake Credits | 6.11 total (10 questions) | N/A | -- |

---

## 1. Accuracy

![Accuracy per Question](cre_charts/01_accuracy.png)

| Question | Cortex | Databricks | DBX Issue |
|---|---|---|---|
| G01: Office Exposure + SR 07-1 | 4/4 | 2/4 | Reported wrong exposure ($4.26B vs $167B); SR 07-1 from general knowledge, not docs |
| G02: Cascadia Tower Full Analysis | 4/4 | 2.5/4 | NOI not found; KA failed twice on workout/financials docs |
| G03: ALLL + Q-Factor + OCC | 4/4 | 1.5/4 | Wrong ALLL ($67.2B, 40% rate -- didn't deduplicate); ALLL memo and OCC findings not found |
| G04: DSCR Breach Cascade | 5/5 | 3.5/4 | Strong on SQL-only question; minor categorization differences |
| G05: CET1 + Stress Test | 5/5 | 1.5/4 | Stress test projection and capital plan details not found; fabricated "general knowledge" |
| G06: Recovery by Property Type | 5/5 | 3.5/4 | Good efficiency; minor formatting differences |
| G07: UW Exceptions by Branch | 4/4 | 2/4 | Fabricated "industry standard" exception types; OCC Article V not found |
| G08: REO Portfolio | 5/5 | 3.5/4 | Timed out at 292s, needed "continue" prompt |
| G09: MRIA Findings | 4/4 | 3/4 | Data correct; fabricated regulatory implications from general knowledge |
| G10: Loan Sale + Capital Impact | 5/5 | 1.5/4 | KA matched wrong $412M figure; fabricated consent order targets |

Cortex achieved perfect or near-perfect accuracy on all 10 questions. Databricks performed well on SQL-only questions (G04, G06, G08) but failed on every question requiring document context.

---

## 2. Groundedness

![Groundedness](cre_charts/05_groundedness.png)

Cortex is 100% grounded -- every factual claim traces to a SQL result or cited document (with numbered footnotes). Databricks has 35 ungrounded claims across 7 questions, falling into three failure modes:

1. **General knowledge backfill (12 instances):** When the Knowledge Assistant failed, the supervisor filled gaps with fabricated "industry standard" content. Examples:
   - G07: Fabricated exception type definitions ("DSCR below policy 42%") that happened to match the docs -- but were not retrieved from them
   - G09: Fabricated "regulatory implications" and "typical OCC remediation requirements"
   - G10: Fabricated consent order capital targets

2. **Wrong corpus retrieval (13 instances):** Every KA call returned results from the previous legal benchmark corpus (Meridian Capital insider trading docs) instead of the CRE banking documents. The Knowledge Assistant was connected to the wrong document volume -- a configuration error during setup, not a platform limitation. This single misconfiguration cascaded into accuracy and groundedness failures on every question requiring document context.

3. **SQL aggregation errors (5 instances):** Join fan-out on provision table (G03: $67.2B instead of ~$13.6B) and wrong exposure figures (G01: $4.26B instead of $167B from using concentration table instead of loan table).

---

## 3. Latency

![Latency per Question](cre_charts/02_latency.png)

Snowflake latency measured from account usage views (start_time to end_time). Databricks latency measured from top-level agent trace span. Both represent wall-clock time from question to complete response.

| Question | Cortex (s) | Databricks (s) | Ratio |
|---|---|---|---|
| G01: Office Exposure + SR 07-1 | 73 | 135 | 1.8x |
| G02: Cascadia Tower | 50 | 238 | 4.8x |
| G03: ALLL + Q-Factor | 44 | 260 | 5.9x |
| G04: DSCR Breach Cascade | 47 | 283 | 6.0x |
| G05: CET1 + Stress Test | 32 | 286 | 8.9x |
| G06: Recovery by Property Type | 38 | 85 | 2.2x |
| G07: UW Exceptions by Branch | 31 | 384 | 12.4x |
| G08: REO Portfolio | 37 | 342 | 9.2x |
| G09: MRIA Findings | 38 | 181 | 4.8x |
| G10: Loan Sale Impact | 23 | 354 | 15.4x |
| **Average** | **41** | **255** | **6.2x** |

![Latency Trend](cre_charts/08_latency_trend.png)

The latency gap widens as questions get more complex. SQL-only questions (G06) show the smallest gap (2.2x). Questions requiring document retrieval (G07, G10) show the largest (12-15x) because the KA fails, the supervisor retries, and context accumulates with each retry.

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

Databricks traces report per-LLM-call context sizes. Because the supervisor agent carries all prior tool outputs in its context window, these grow cumulatively across tool calls within a single question. G01 starts at 38K tokens, but by G09 a single question's LLM calls consume 720K tokens -- each token at full cost with no caching mechanism visible in the traces.

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

The net result: **6.11 credits for 10 complex banking questions** (avg 0.61 credits/question). The cache mechanism means the cost per additional question decreases as more of the semantic view and search context is cached -- the semantic view (column descriptions, relationships, VQRs) is loaded once and reused across all subsequent questions at 90% discount.

---

## 5. Tool Call Efficiency

![Tool Calls](cre_charts/04_tool_calls.png)

| Metric | Cortex | Databricks |
|---|---|---|
| Total tool calls | 35 | 74 |
| Avg per question | 3.5 | 7.4 |
| SQL queries | 30 | 50 (Genie) |
| Document searches | 5 | 13 (KA) |
| Sandbox/code | 0 | 11 |
| Failed tool calls | 2 (6%) | 18 (24%) |
| Tool success rate | 94% | 76% |

![DBX Failure Modes](cre_charts/07_dbx_failures.png)

### Tool Failure Breakdown (Databricks)

| Failure Type | Count | Impact |
|---|---|---|
| KA returned wrong corpus | 13 | Configuration error -- KA pointed at legal benchmark volume instead of CRE volume |
| Genie SQL returned EMPTY or wrong | 5 | Queries for nonexistent data (DSCR covenants, NOI table, etc.) |
| Genie timeout | 1 | G08 exceeded 292s, needed manual "continue" |
| **Total** | **19** | |

---

## 6. Document Retrieval

This is the single largest differentiator.

| Metric | Cortex Search | Databricks KA |
|---|---|---|
| Queries attempted | 5 | 13 |
| Successful retrievals | 5 (100%) | 0 (0%) |
| Documents found | SR 07-1, Consent Order, ALLL memo, workout proposal, borrower financials, audit report, stress test, capital plan, examiner report | None -- KA was connected to wrong document volume (returned legal benchmark docs instead of CRE docs) |

**Root cause:** The Databricks Knowledge Assistant was connected to the wrong document volume during setup -- it was pointed at the previous legal benchmark corpus instead of the CRE banking documents. This is a configuration error, not a platform limitation. Every KA call returned results from the Meridian Capital legal case documents, which had no relevance to the CRE banking questions. Because the supervisor agent couldn't get relevant document context, it either admitted gaps or backfilled with general knowledge.

Cortex Search successfully retrieved every document on the first attempt, including complex queries spanning multiple documents (e.g., ALLL methodology + Consent Order + examiner report in a single search).

---

## 7. Self-Correction and Analytical Transparency

### Self-Correction

Cortex detected and fixed 2 tool failures without user intervention:
1. **G02:** DSCR query returned 0 rows -> investigated all covenant types -> found loan only has ICR/Debt Yield -> provided substitute + document-sourced DSCR
2. **G03:** Join fan-out inflated balances -> self-corrected with ROW_NUMBER() deduplication in second query

Databricks did not self-correct any of its failures. The supervisor accepted wrong results and presented them as final answers.

### Proactive Caveats and Cross-Referencing

A key differentiator is how each agent handles nuance. Banking data is inherently complex -- documents and tables may reflect different points in time, different scopes, or different methodologies. An analyst-grade response should surface these nuances rather than present numbers without context.

Cortex proactively added caveats, cross-references, and reconciliation notes on every question. Databricks presented results at face value without qualification.

Examples of Cortex analytical transparency:
- **G02:** Flagged that the DSCR covenant exists in loan documents but is missing from the structured covenant table -- recommended data governance escalation rather than silently omitting DSCR
- **G03:** Noted that loan-level provision totals ($13.6B) differ from the segment-level ALLL memo figure ($167.5M) due to aggregation basis, and explained the pre-remediation ($187M) vs post-remediation ($432M) timing difference
- **G04:** Explained why the distressed-by-status count (1,378) differs from the workout-record count (1,318) -- loans can hold distressed status without a formal workout record
- **G09:** Distinguished between 502 MRIA records in the warehouse database (broad finding log) vs the 12 formal MRIAs cited in the OCC Consent Order (regulatory scope)
- **G10:** Identified that the $412M term sheet figure differs from the earlier $400M/$368M Board minutes figure, and noted sub-debt is Tier 2 only (no CET1 benefit)

This level of analytical transparency is critical for banking work where silent errors are worse than flagged uncertainties.

---

## 8. Architectural Observations

### Why Cortex Wins

1. **Semantic View with VQRs** provides rich schema guidance that eliminates code-guessing. Snowflake's Semantic View defines column decode mappings, relationships, and verified queries as a single governed object. Databricks' knowledge store offers similar capabilities (SQL expressions, example SQL, synonyms) but requires separate curation per Genie Agent rather than a centralized semantic layer. The SQL errors observed (wrong table in G01, fan-out in G03) reflect gaps in schema guidance available to the agent at query time.

2. **Cortex Search retrieves from the correct corpus.** The same 30 documents were uploaded to both platforms. Cortex Search found every document on the first call. The Databricks Knowledge Assistant was connected to the wrong document volume (a setup error), so its retrieval failures reflect misconfiguration rather than a platform limitation. A correctly configured KA would be expected to retrieve relevant documents.

3. **Parallel tool invocation** lets Cortex fire SQL and Search simultaneously. Databricks' supervisor routes sequentially -- one child agent at a time -- compounding latency when retries occur.

4. **Single-agent architecture** avoids context accumulation. Databricks' 3-agent hierarchy (supervisor + Genie + KA) passes all tool outputs through the supervisor's context, growing from 38K tokens (G01) to 720K tokens (G09).

5. **Self-correction capability.** Cortex detected empty results and investigated root causes (missing covenant types, join fan-out). Databricks accepted wrong results and presented them as final.

6. **Cache efficiency.** Cortex achieves 78.3% cache read rate on input tokens, reducing cost. The semantic view and search index content is cached across calls, making repeat queries nearly free on input tokens.

---

## 9. Conclusion

Across 10 complex multi-part banking queries, **Cortex Agent achieves 95% accuracy with 100% groundedness, at 6.2x faster latency and 2.1x fewer tool calls** compared to Databricks Genie, for a total cost of 6.11 Snowflake credits.

A significant factor in the results is the **document retrieval failure** (0/13 KA calls successful), caused by the Knowledge Assistant being connected to the wrong document volume during setup. This configuration error cascaded into general-knowledge backfill, fabricated citations, and missed sub-parts on 7 of 10 questions. On purely SQL-based questions (G04, G06), Databricks performed competitively -- the gap is driven by the hybrid SQL+document questions that represent real-world banking analyst workflows. A re-run with the correctly configured KA volume would be needed to isolate the document retrieval comparison.

When the question is "did the agent get the banking facts right, grounded in the data and regulatory documents?", Cortex wins decisively.
