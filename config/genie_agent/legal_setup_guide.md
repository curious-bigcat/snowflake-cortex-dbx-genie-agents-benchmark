# Databricks Genie Agent Setup — Legal Benchmark (RAW SCHEMA ONLY)

## Purpose

This setup provides NO column descriptions, NO SQL expressions, NO example queries.
The Genie Agent sees only raw table/column names (tbl_case_mstr, pty_role_cd, evt_typ_cd, etc.)
with NO hint about what the coded values mean.

This tests the agent's ability to reason about ambiguous schemas vs. Cortex Agent
which has the full semantic model explaining every code.

## Prerequisites

- Databricks workspace with Unity Catalog enabled
- Catalog: `dbx-bsuresh-catalog`
- Schema: `legal` (will be created)
- Data uploaded to Azure Blob Storage at: `abfss://data@blobbsuresh.dfs.core.windows.net/`

## Step 1: Create Schema

```sql
USE CATALOG `dbx-bsuresh-catalog`;
CREATE SCHEMA IF NOT EXISTS legal;
USE SCHEMA legal;
```

## Step 2: Load Tables from Azure Blob

```python
base_path = "abfss://data@blobbsuresh.dfs.core.windows.net/legal/tables"

tables = [
    "tbl_case_mstr", "tbl_pty_info", "tbl_atty_reg", "tbl_case_pty_atty",
    "tbl_evt_log", "tbl_doc_ref", "tbl_ruling", "tbl_statute_cite",
    "tbl_claim", "tbl_damages", "tbl_appeal", "tbl_settlement"
]

for table in tables:
    file_path = f"{base_path}/{table}.parquet"
    try:
        df = spark.read.parquet(file_path)
        df.write.mode("overwrite").saveAsTable(f"`dbx-bsuresh-catalog`.legal.{table}")
        print(f"Created: {table} ({df.count()} rows)")
    except Exception as e:
        print(f"Error: {table}: {e}")
```

### Verify Key Data

```sql
-- Verify the key case exists
SELECT * FROM `dbx-bsuresh-catalog`.legal.tbl_case_mstr
WHERE docket_no = 'SDNY-2022-CIV-04851';

-- Verify key parties
SELECT * FROM `dbx-bsuresh-catalog`.legal.tbl_pty_info
WHERE pty_nm LIKE '%Meridian%' OR pty_nm LIKE '%Hartwell%';

-- Verify settlement
SELECT * FROM `dbx-bsuresh-catalog`.legal.tbl_settlement
WHERE stl_id = 'STL-000001';
```

## Step 3: Upload ALL Documents to Volume

Documents are organized in 3 categories:
- Main documents (large coherent legal texts)
- Case notes (emails, memos, trading logs, Board minutes)
- Real regulations (actual CFR PDFs from GovInfo)

```python
# Create volume
spark.sql("CREATE VOLUME IF NOT EXISTS `dbx-bsuresh-catalog`.legal.legal_documents")

volume_path = "/Volumes/dbx-bsuresh-catalog/legal/legal_documents"

# Upload main documents (8 large text files)
main_docs_path = "abfss://data@blobbsuresh.dfs.core.windows.net/legal/docs"
for f in dbutils.fs.ls(main_docs_path):
    if f.name.endswith('.txt') and not f.isDir():
        dbutils.fs.cp(f.path, f"{volume_path}/{f.name}")
        print(f"Copied main doc: {f.name}")

# Upload case notes (8 supplementary files)
notes_path = "abfss://data@blobbsuresh.dfs.core.windows.net/legal/docs/case_notes"
for f in dbutils.fs.ls(notes_path):
    if f.name.endswith('.txt'):
        dbutils.fs.cp(f.path, f"{volume_path}/case_notes_{f.name}")
        print(f"Copied case note: {f.name}")

# Upload real regulation PDFs (6 actual CFR/FRCP documents)
regs_path = "abfss://data@blobbsuresh.dfs.core.windows.net/legal/docs/real_regulations"
for f in dbutils.fs.ls(regs_path):
    if f.name.endswith('.pdf'):
        dbutils.fs.cp(f.path, f"{volume_path}/{f.name}")
        print(f"Copied regulation: {f.name}")
```

### Verify Volume Contents

```python
files = dbutils.fs.ls(volume_path)
print(f"Total files in volume: {len(files)}")
for f in files:
    print(f"  {f.name} ({f.size / 1024:.0f} KB)")
```

Expected: 22 files (8 main + 8 case notes + 6 regulations), ~38 MB total.

## Step 4: Create Genie Agent (NO CONTEXT — Raw Schema)

1. **Create new Agent** > select **Genie Agent**
2. Name: `Legal Benchmark - Raw Schema`
3. Add all 12 tables from `dbx-bsuresh-catalog.legal`:
   - tbl_case_mstr, tbl_pty_info, tbl_atty_reg, tbl_case_pty_atty
   - tbl_evt_log, tbl_doc_ref, tbl_ruling, tbl_statute_cite
   - tbl_claim, tbl_damages, tbl_appeal, tbl_settlement
4. **DO NOT ADD** any of the following:
   - No SQL expressions
   - No example queries
   - No text instructions
   - No column descriptions
5. The agent sees ONLY raw column names (pty_role_cd, evt_typ_cd, ruling_cd, etc.)

## Step 5: Create Knowledge Assistant

1. **Create new Agent** > select **Knowledge Assistant**
2. Name: `Legal Benchmark - Documents`
3. Connect to volume: `dbx-bsuresh-catalog.legal.legal_documents`
4. **Describe the content:**
   ```
   Legal document corpus for SEC v. Meridian Capital Group LLC securities fraud case.
   Contains: SEC enforcement complaint (docket SDNY-2022-CIV-04851), Meridian Capital
   compliance manual (internal policies), class action settlement agreement (Thornton
   Pension Fund v. Meridian, $347.5M settlement), deposition transcript of Sarah Chen
   (cooperating witness/former CFO), Apex Technologies/Global Systems merger agreement,
   court opinion denying motion to dismiss, expert damages report ($412M estimate),
   Form ADV regulatory filing, internal email chains (Hartwell-Chen correspondence),
   Board meeting minutes, trading logs, attorney strategy memos, SEC investigation
   notes, and actual CFR Title 17 securities regulations.
   ```
5. **Instructions:**
   ```
   When answering questions:
   - Cite specific document names and section numbers
   - Quote exact dollar amounts, dates, and percentages from the source
   - If information spans multiple documents, cite each source
   - For regulation questions, reference the specific CFR section
   ```
6. **Enable content search** on the volume

## Step 6: Create Supervisor Agent

1. **Create new Agent** > select **Supervisor Agent**
2. Name: `Legal Benchmark - SEC v. Meridian Capital`
3. Add child tools:
   - **Genie Agent** (`Legal Benchmark - Raw Schema`)
   - **Knowledge Assistant** (`Legal Benchmark - Documents`)
4. System instructions:
   ```
   You are a legal research assistant specializing in securities fraud litigation.
   You have access to:
   1. A case management database with 12 tables (cases, parties, events, rulings,
      settlements, etc.) — use the Genie Agent for data queries
   2. A document corpus with SEC complaints, compliance manuals, settlement agreements,
      depositions, merger agreements, court opinions, and regulations — use the
      Knowledge Assistant for document questions

   For hybrid questions (requiring both data and documents):
   - First retrieve the relevant facts from documents
   - Then query the database to verify, calculate, or cross-reference

   Always cite your sources (document name + section, or table name + query).
   ```

## Step 7: Test the Setup

### Test Genie Agent (structured queries)
```
"What is the settlement amount for case SDNY-2023-CIV-00892?"
Expected: $347,500,000
```

### Test Knowledge Assistant (document retrieval)
```
"What did Hartwell's email to Chen on February 23, 2021 say?"
Expected: "Move on APEX immediately, before Thursday announcement"
```

### Test Supervisor (hybrid)
```
"The compliance manual requires reporting within 72 hours. When was the SEC investigation actually opened per the case records?"
Expected: Routes to KA (gets 72-hour rule) then Genie (gets Jan 10, 2022 date), calculates ~316 days elapsed.
```

## Key Differences vs. Cortex Agent

| Aspect | Cortex Agent (with semantic model) | Genie Agent (raw schema) |
|--------|-----------------------------------|--------------------------|
| Column meaning | Full descriptions: "PLF=Plaintiff, DEF=Defendant" | Just sees `pty_role_cd` with no hint |
| Code translation | Model explains "GRT=Granted, DNY=Denied" | Must infer from data patterns |
| Join paths | Explicitly defined relationships | Must discover from column name matching |
| Verified queries | Pre-approved SQL for common patterns | Generates SQL from scratch each time |
| Document retrieval | Cortex Search with chunk control | Knowledge Assistant with auto-chunking |
| Real regulation PDFs | PARSE_DOCUMENT for structured extraction | Volume content search |

## What We Expect

**Tier 1 (Document Retrieval):** Both should perform similarly — documents are well-structured with clear sections.

**Tier 2 (Structured Queries):** Cortex should excel because the semantic model decodes `pty_role_cd='PLF'` as "Plaintiff." Genie must guess from context.

**Tier 3 (Hybrid Cross-Source):** Both should be able to chain docs + SQL since entities are coherent. Cortex may be faster (fewer steps).

**Tier 4 (Legal Reasoning):** Tests domain knowledge + multi-hop reasoning. Model quality matters here — Cortex allows model selection.

## Document Inventory

| File | Type | Size | Key Cross-References |
|------|------|------|---------------------|
| sec_complaint_meridian_capital.txt | Main | 2.3MB | All parties, docket nos, trade amounts |
| compliance_manual_meridian_capital.txt | Main | 2.0MB | Position limits, 72-hr deadline |
| settlement_agreement_thornton_v_meridian.txt | Main | 1.1MB | $347.5M, opt-out deadline, class size |
| deposition_sarah_chen.txt | Main | 1.4MB | 47 trades, email quotes, Board Resolution |
| merger_agreement_apex_global_systems.txt | Main | 1.7MB | $84/share, MAE=$75M, closing date |
| opinion_motion_to_dismiss.txt | Main | 1.4MB | Tellabs standard, scienter, SOL |
| expert_report_damages_calculation.txt | Main | 881KB | $412M damages, $17.28 inflation |
| form_adv_meridian_capital.txt | Main | 586KB | $4.2B AUM, 13F filer, fee structure |
| email_chain_01_hartwell_chen_apex_trades.txt | Notes | 18KB | "Skip compliance BS" quote |
| email_chain_02_hartwell_pacific_growth_tip.txt | Notes | 1KB | Tipping communication |
| email_chain_03_compliance_alert_ignored.txt | Notes | 2KB | CCO warning dismissed |
| board_minutes_2021_2022.txt | Notes | 9KB | Resolution 2021-047 |
| trading_log_apex_technologies.txt | Notes | 7KB | 47 trade records |
| attorney_memo_strategy_privileged.txt | Notes | 16KB | 85-90% SEC win probability |
| sec_investigation_file_notes.txt | Notes | 3KB | Timeline, FINRA referral |
| expert_declaration_class_cert.txt | Notes | 2KB | $17.28/share inflation |
| cfr_title17_vol3_securities_exchange_act.pdf | Real Reg | 3.6MB | Actual SEC rules |
| cfr_title17_vol4_sec_rules.pdf | Real Reg | 3.4MB | Rule 10b-5 text |
| cfr_title17_vol5_sec_rules_continued.pdf | Real Reg | 8.1MB | Form 13F requirements |
| cfr_title18_conservation_of_power.pdf | Real Reg | 8.3MB | Reference regulations |
| federal_rules_civil_procedure.pdf | Real Reg | 200KB | Rule 12(b)(6), Rule 23 |
| sec_enforcement_manual_2024.pdf | Real Reg | 2KB | SEC procedures |
