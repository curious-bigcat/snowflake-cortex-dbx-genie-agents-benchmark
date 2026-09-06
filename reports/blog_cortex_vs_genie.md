# We Ran 10 Complex Banking Queries Through Snowflake Cortex Agent and Databricks Genie. Here's What Happened.

*A head-to-head benchmark on real CRE lending data — 3.6M rows, 30 documents, 10 questions a credit officer would actually ask.*

---

## The Setup

Pacific Northwest Bank is a fictional $28B regional bank sitting on an $8.7B CRE lending book that just blew up. Office vacancy hit 31%. The OCC issued a consent order. There's a $2.1B workout pipeline, a stressed capital plan, and a board that needs answers yesterday.

We gave both Snowflake Cortex Agent and Databricks Genie the same data — 18 tables (3.6M rows of loan, collateral, covenant, provision, and capital data) plus 30 documents (consent orders, stress tests, audit reports, term sheets, and 7 real OCC/FDIC/Fed regulatory PDFs). Then we asked 10 questions that a Chief Credit Officer would ask during a regulatory exam prep.

These aren't toy questions. Each one requires SQL across multiple tables AND document retrieval AND banking domain reasoning. "What's the CET1 impact if we sell the $412M loan pool at 92 cents?" requires reading a term sheet, pulling current capital from the database, computing the loss, calculating the RWA reduction, and checking the consent order target — all in one answer.

**Both platforms received identical data, identical questions, in the same order.**

---

## The Results

| Metric | Cortex Agent | Databricks Genie |
|---|---|---|
| **Accuracy** | **100%** (48/48 sub-parts) | 84.4% (40.5/48) |
| **Groundedness** | **100%** (0 hallucinations) | ~89% (~13 ungrounded claims) |
| **Avg Latency** | **41s** | 173s |
| **Tool Calls** | **35** | 59 |
| **Doc Retrieval** | **100%** (5/5) | 85% (11/13) |
| **LLM-as-Judge** | **45.1/50** (90%) | 26.2/50 (52%) |

Cortex won all 10 questions. The average margin was 18.9 points out of 50.

But the numbers alone don't capture what it felt like to watch these two systems work side by side.

---

## What We Actually Saw

We built a live comparison UI — "Agent Duel" — that sends the same question to both platforms simultaneously. A credit officer sits in front of two panels and watches both agents work in real time.

### Cortex Streams. Genie Blocks.

Cortex starts streaming tokens within 2-5 seconds. You see "Querying TBL_LOAN_MSTR..." then "Searching consent order..." then the answer starts appearing. You're reading the first paragraph while the agent is still running its fourth SQL query.

Genie returns nothing until its entire agent chain completes — Supervisor routes to Genie SQL, waits for the response, routes to Knowledge Assistant, waits again, sometimes routes to Sandbox for Python computation. The credit officer stares at a blank panel for 90-180 seconds.

On a 10-question regulatory review, that's **~15 minutes of blank-screen waiting** with Genie versus reading-as-you-go with Cortex.

### The Hallucination That Could Cost You a Regulatory Exam

The widest gap was Q09 — MRIA Remediation. The OCC has a follow-up exam scheduled. The CCO asks: *"How many OCC MRIA findings are still open, and how many are past due?"*

**Cortex answered:** 196 OCC MRIA findings open or in-progress. All 196 (100%) are past the 180-day deadline from Article VI of the consent order. Breakdown across 11 categories. Risk flag: 100% past-due rate signals systemic remediation failure.

**Score: 49/50.**

**Genie answered:** Returned 502 findings — it pulled all MRIA-severity findings from every exam type instead of filtering to OCC exams. The count doesn't match the consent order's 12 formal MRIAs or the database's 196 OCC-specific records. The deadline and past-due analysis was incomplete.

**Score: 18/50.**

If the CCO walks into the OCC exam citing Genie's numbers, they present a finding count that doesn't reconcile with OCC records. The bank's credibility is undermined before the conversation starts.

### The Board Memo That's Missing Its Punchline

Q10 — the board is voting on selling a $412M distressed loan pool. The CFO needs the CET1 impact for the board memo.

**Cortex:** Projected loss $32.96M. Pre-sale CET1 10.32%. Post-sale CET1 rises to ~11.06% (+74 bps) because the RWA reduction outweighs the loss. Consent order requires CET1 above 9.0% — the sale moves PNB toward compliance. Four cited sources.

**Score: 45/50.**

**Genie:** Got the $32.96M loss right but didn't complete the CET1 impact calculation or cite the consent order target. The strategic rationale — "this sale moves us toward compliance" — is missing.

**Score: 14/50.**

The board gets the loss figure either way. But with Cortex, the board memo has the conclusion that justifies the sale. With Genie, someone needs to do the math manually.

---

## Why the Gap Exists: Architecture Matters

### Cortex: One Agent, Parallel Tools, Rich Schema Guidance

Cortex Agent is a single agent with two tools: Cortex Analyst (SQL over a semantic view) and Cortex Search (embedding-based document retrieval). It fires both simultaneously.

The semantic view is the key differentiator. It contains column descriptions, code decode mappings (e.g., `risk_rtg_cd: 5-SS = Special Mention`), table relationships, metrics, and 8 verified queries. The model knows what `loan_sts_cd = 'WKOT'` means before it writes the first query. This is why Cortex writes correct SQL on the first attempt — it has the schema guidance that prevents the ambiguity errors Genie hits.

### Genie: Three Agents, Sequential Routing, Context Rebuilding

Databricks uses a 3-agent hierarchy: a Supervisor routes to Genie SQL (structured queries), Knowledge Assistant (document retrieval), or Sandbox (Python computation). Each routing step is sequential — the Supervisor waits for one child agent to finish before deciding what to do next.

Each Genie SQL call costs 17-58 seconds due to the ask_question → start_conversation → poll_for_result cycle. When the question requires multiple SQL queries (G04 needed 12 Genie calls), latency explodes to 558 seconds.

The supervisor rebuilds its context on every LLM call, carrying all prior tool outputs forward. There's no cross-call caching.

---

## The Cost Story Nobody's Talking About

Cortex reports 4.75M total tokens for 10 questions. Genie reports 3.49M. Genie looks cheaper on paper.

**It's not.**

Cortex's 4.75M total includes 3.90M cache reads — the semantic view, search index, and system prompt are cached in memory and served at a **90% discount**. Only 852K tokens (18%) are billed at full price. Total cost: **6.11 credits for 10 complex banking questions.**

Genie's 3.49M tokens are all processed at full inference cost. The supervisor agent rebuilds context from scratch on every LLM call. No caching mechanism. Currently free during the promotional period (until January 31, 2027), but when billing starts, every one of those 3.49M tokens gets billed at the standard per-token rate.

| | Cortex Agent | Databricks Genie |
|---|---|---|
| **Total tokens** | 4.75M | 3.49M |
| **Full-price tokens** | **852K (18%)** | **3.49M (100%)** |
| **90% discount tokens** | 3.90M (82%) | 0 |
| **Current cost** | 6.11 credits | Free (promo) |

**At production scale, Cortex's cache advantage compounds.** The semantic view loads once and is reused across every question. Cost per question drops as usage grows. Genie's cost scales linearly — every question rebuilds the full context.

---

## Platform Maturity: GA vs. Beta

This matters for enterprises evaluating production deployments.

**Snowflake Cortex Agents** and **CoWork** (formerly Snowflake Intelligence) have been **generally available since November 2025** — nearly a year in production. Cortex Agents natively combine structured data (via Cortex Analyst semantic views) and unstructured data (via Cortex Search) in a single governed workflow. MCP server support in Native Apps is GA. The architecture is unified: one agent, one security model, one billing model.

**Databricks Genie One** Chat mode reached GA in 2026, but significant capabilities remain in Beta:

| Capability | Snowflake | Databricks |
|---|---|---|
| Structured data queries | GA (Cortex Analyst) | GA (Genie Chat mode) |
| Unstructured data retrieval | GA (Cortex Search) | **Beta** (Agent mode, UC volumes only) |
| Combined structured + unstructured | GA (single agent) | **Beta** (Agent mode only; Chat mode is structured-only) |
| MCP server support | GA (Native Apps) | **Beta** (Managed MCP Server) |
| Business user interface | GA (CoWork, ~10 months) | GA (Genie One Chat) |
| Desktop app | GA (CoCo) | **Beta** |
| Billing | Production pricing | Free promotional period until Jan 2027 |

The distinction matters: **Genie One's marketing says "structured and unstructured data"** and that's technically true via Agent mode — but the core Chat experience that business users interact with daily is structured-data only. Unstructured data requires Agent mode, which is still in Beta and limited to files in Unity Catalog volumes. Cortex has had unified structured + unstructured in a single GA agent since late 2025.

---

## Where Genie Was Better

Fairness matters. Genie earned its points:

1. **Multi-tool orchestration on G10.** The Supervisor → KA (term sheet) → Genie SQL (capital data) → KA (RWA reduction) → Sandbox (Python calculation) workflow was the most sophisticated tool chain in the benchmark. The Sandbox capability for transparent computation is a genuine differentiator Cortex doesn't have.

2. **Graceful fallback.** When Genie SQL couldn't answer a sub-question (exception types in G07, loan pool in G10), the system correctly fell back to the Knowledge Assistant and recovered from documents. This is the multi-agent architecture working as designed.

3. **G08 was close.** On the REO Portfolio question (pure SQL, well-defined), Genie scored 43/50 vs Cortex's 49/50. On straightforward structured-data queries, the gap narrows significantly.

---

## The Bottom Line

If you're building AI agents for complex enterprise workflows — especially ones that combine structured data, regulatory documents, and domain reasoning — architecture choices compound:

- **Parallel vs. sequential** tool invocation is the difference between 41s and 173s average latency.
- **Semantic view guidance** is the difference between correct SQL on the first attempt and 12 retry loops.
- **Prompt caching** is the difference between 852K billable tokens and 3.49M billable tokens.
- **Groundedness** is the difference between a defensible regulatory filing and a credibility problem.

Cortex won 10-0 not because Genie is bad — it's a capable platform with genuine strengths in multi-tool orchestration. Cortex won because its architecture is better suited to the workload: hybrid queries that need SQL precision, document retrieval, and analytical transparency, delivered fast enough for a credit officer to actually use in their workflow.

**The 10 questions, the dataset, the comparison UI source code, and the full benchmark report are all open source:** [github.com/curious-bigcat/snowflake-cortex-dbx-genie-agents-benchmark](https://github.com/curious-bigcat/snowflake-cortex-dbx-genie-agents-benchmark)

---

*Benchmark conducted September 2026. Both platforms tested with their current production configurations. Snowflake Cortex Agent using claude-opus-4-8. Databricks Genie using default supervisor and child models. All ground truth facts verified against the live database. LLM-as-Judge evaluation using Claude Sonnet (claude-sonnet-4-5, temperature=0) via the Cortex REST API.*
