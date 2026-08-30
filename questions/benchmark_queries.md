# Benchmark Queries — 12 Platform Differentiator Questions

These 12 questions are designed to test areas where platform architecture matters:
coded column decoding, complex joins, noise filtering in large tables, model reasoning quality, and hybrid document+SQL.

## Running on Snowflake Cortex Agent

Use `DATA_AGENT_RUN` to call your Cortex Agent:

```sql
SELECT SNOWFLAKE.CORTEX.DATA_AGENT_RUN(
  'LEGAL_BENCHMARK_DB.LEGAL.LEGAL_BENCHMARK_AGENT',
  $${"messages": [{"role": "user", "content": "<QUESTION>"}]}$$
);
```

To capture latency and token usage:

```sql
SET start_ts = CURRENT_TIMESTAMP();

SELECT SNOWFLAKE.CORTEX.DATA_AGENT_RUN(
  'LEGAL_BENCHMARK_DB.LEGAL.LEGAL_BENCHMARK_AGENT',
  $${"messages": [{"role": "user", "content": "<QUESTION>"}]}$$
) AS response;

SELECT DATEDIFF('second', $start_ts, CURRENT_TIMESTAMP()) AS latency_seconds;
```

Token usage is available in `SNOWFLAKE.ACCOUNT_USAGE.SNOWFLAKE_COWORK_USAGE_HISTORY` (45 min lag).

## Running on Databricks Genie

Use the Genie Space UI or the Genie API. For API-based benchmarking, send questions to your Genie Space endpoint and capture the full trace for latency and token analysis.

---

## Questions

### Category 1: Coded Column Decoding (3 questions)

These test whether the agent can interpret abbreviated column values like `PLF`, `DEF`, `MTD`, `GRT`, `SEC`, `REV`.
Cortex has these mappings in its semantic model; Genie sees only raw codes.

**P01**
```
How many plaintiffs filed motions to dismiss across all securities fraud cases in 2022?
```
- Requires: `pty_role_cd = 'PLF'` + `evt_typ_cd = 'MTD'` + `case_typ_cd = 'SEC'` + date filtering
- Tables: `tbl_pty_info` -> `tbl_case_pty_atty` -> `tbl_evt_log` -> `tbl_case_mstr`

**P02**
```
List all cases where the defendant was granted summary judgment but the ruling was later reversed on appeal.
```
- Requires: `pty_role_cd = 'DEF'` + `ruling_outcome_cd = 'GRT'` + `evt_typ_cd = 'SJ'` + `appeal_outcome_cd = 'REV'`
- Tables: `tbl_ruling` -> `tbl_appeal`

**P03**
```
What percentage of SEC enforcement actions result in settlements versus going to trial?
```
- Requires: `case_typ_cd = 'SEC'` + `stl_terms_cd` values + trial event codes
- Tables: `tbl_case_mstr` -> `tbl_settlement` / `tbl_evt_log`

---

### Category 2: Complex Join Paths (2 questions)

These require multi-table joins with self-joins and role-based filtering.

**P04**
```
For each attorney who represented both plaintiffs and defendants in different cases, show their total case count and how many they won on each side.
```
- Requires: Self-join on `tbl_case_pty_atty` by `atty_id` across roles + `tbl_ruling` for outcomes
- Tables: `tbl_atty_reg` -> `tbl_case_pty_atty` (self-join) -> `tbl_pty_info` -> `tbl_ruling`

**P05**
```
Which judges have the highest rate of denying motions to dismiss in insider trading cases? What is the average time from case filing to MTD ruling for each?
```
- Requires: 3-table join with date arithmetic
- Tables: `tbl_ruling` -> `tbl_case_mstr` -> `tbl_evt_log`

---

### Category 3: Noise Filtering (3 questions)

50,000 cases in the database, but only 3 matter (the Meridian-related dockets). The agent must filter to the right records.

**P06**
```
What was the total disgorgement amount in the Meridian Capital insider trading case?
```
- Requires: Filter to `docket_no = 'SDNY-2022-CIV-04851'` among 50K cases
- Tables: `tbl_damages` or `tbl_evt_log`

**P07**
```
How many trading days elapsed between Hartwell's tip and the first Meridian trade in Apex?
```
- Requires: Find specific events for the Meridian case in 500K event log rows
- Answer: Tip Feb 22, first trade Feb 28 = 4 trading days

**P08**
```
Calculate the total penalties across ALL three Meridian-related proceedings: SEC enforcement, class action settlement, and criminal case.
```
- Requires: Identify 3 docket numbers among 50K cases and sum correctly
- Dockets: `SDNY-2022-CIV-04851`, `SDNY-2023-CIV-00892`, `SDNY-2022-CRM-01247`

---

### Category 4: Model Reasoning Quality (2 questions)

These require frontier-model reasoning that goes beyond SQL.

**P09**
```
The SEC complaint alleges violations of Section 10(b) and Rule 10b-5. The court analyzed scienter under Tellabs. But Tellabs applies to PRIVATE securities litigation under the PSLRA. Does the Tellabs heightened pleading standard actually apply to SEC ENFORCEMENT actions? Identify the legal error.
```
- Requires: Legal domain knowledge + reasoning about PSLRA vs SEC enforcement standards

**P10**
```
The attorney memo says 85-90% SEC win probability. But that's a single-stage figure for trial. What is the CUMULATIVE probability of the SEC winning across ALL litigation milestones from filing through trial verdict?
```
- Requires: Multi-step probability reasoning across 5 litigation stages

---

### Category 5: Hybrid Document + SQL (2 questions)

These require retrieving facts from documents AND querying structured tables.

**P11**
```
According to Section 5.2 of the compliance manual, what is the penalty for failing to check the restricted list? How many trades in our database were executed without this check for the Meridian case?
```
- Requires: Cortex Search on compliance manual + SQL on `tbl_evt_log`

**P12**
```
The expert report estimates $17.28 per-share inflation. The settlement agreement defines 'Recognized Loss' for distribution. Are these the same number? Explain the difference using both documents.
```
- Requires: Cortex Search on expert report + settlement agreement, then synthesis
