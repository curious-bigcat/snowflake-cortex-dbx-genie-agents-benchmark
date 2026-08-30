# Snowflake Cortex Agent Setup — Legal Benchmark (WITH Semantic Model)

## Purpose

This setup provides the FULL semantic model with all code definitions, relationships,
and verified queries. This is the Cortex Agent's KEY ADVANTAGE — it knows that
`pty_role_cd='PLF'` means Plaintiff, `ruling_cd='GRT'` means Granted, etc.

## Prerequisites

- Snowflake account with Cortex AI enabled
- Warehouse: MEDIUM or larger (for Cortex Search indexing)
- Role with CREATE DATABASE, STAGE, CORTEX SEARCH SERVICE, CORTEX AGENT privileges

## Step 1: Create Database and Schema

```sql
CREATE DATABASE IF NOT EXISTS LEGAL_BENCHMARK_DB;
CREATE SCHEMA IF NOT EXISTS LEGAL_BENCHMARK_DB.LEGAL;
USE SCHEMA LEGAL_BENCHMARK_DB.LEGAL;
```

## Step 2: Create Stage and Load Tables

```sql
-- Create stage for parquet data
CREATE OR REPLACE STAGE legal_data_stage FILE_FORMAT = (TYPE = PARQUET);

-- Upload parquet files from local:
-- snow stage copy data/legal/tables/*.parquet @legal_data_stage/
```

### Create Tables (for each of 12 tables)

```sql
-- Example for tbl_case_mstr (repeat pattern for all 12):
CREATE OR REPLACE TABLE TBL_CASE_MSTR AS
SELECT * FROM @legal_data_stage/tbl_case_mstr.parquet (FILE_FORMAT => 'PARQUET');

CREATE OR REPLACE TABLE TBL_PTY_INFO AS
SELECT * FROM @legal_data_stage/tbl_pty_info.parquet (FILE_FORMAT => 'PARQUET');

CREATE OR REPLACE TABLE TBL_ATTY_REG AS
SELECT * FROM @legal_data_stage/tbl_atty_reg.parquet (FILE_FORMAT => 'PARQUET');

CREATE OR REPLACE TABLE TBL_CASE_PTY_ATTY AS
SELECT * FROM @legal_data_stage/tbl_case_pty_atty.parquet (FILE_FORMAT => 'PARQUET');

CREATE OR REPLACE TABLE TBL_EVT_LOG AS
SELECT * FROM @legal_data_stage/tbl_evt_log.parquet (FILE_FORMAT => 'PARQUET');

CREATE OR REPLACE TABLE TBL_DOC_REF AS
SELECT * FROM @legal_data_stage/tbl_doc_ref.parquet (FILE_FORMAT => 'PARQUET');

CREATE OR REPLACE TABLE TBL_RULING AS
SELECT * FROM @legal_data_stage/tbl_ruling.parquet (FILE_FORMAT => 'PARQUET');

CREATE OR REPLACE TABLE TBL_STATUTE_CITE AS
SELECT * FROM @legal_data_stage/tbl_statute_cite.parquet (FILE_FORMAT => 'PARQUET');

CREATE OR REPLACE TABLE TBL_CLAIM AS
SELECT * FROM @legal_data_stage/tbl_claim.parquet (FILE_FORMAT => 'PARQUET');

CREATE OR REPLACE TABLE TBL_DAMAGES AS
SELECT * FROM @legal_data_stage/tbl_damages.parquet (FILE_FORMAT => 'PARQUET');

CREATE OR REPLACE TABLE TBL_APPEAL AS
SELECT * FROM @legal_data_stage/tbl_appeal.parquet (FILE_FORMAT => 'PARQUET');

CREATE OR REPLACE TABLE TBL_SETTLEMENT AS
SELECT * FROM @legal_data_stage/tbl_settlement.parquet (FILE_FORMAT => 'PARQUET');
```

### Verify Key Data

```sql
-- Verify the key case
SELECT * FROM TBL_CASE_MSTR WHERE docket_no = 'SDNY-2022-CIV-04851';
-- Verify parties
SELECT * FROM TBL_PTY_INFO WHERE pty_nm LIKE '%Meridian%';
-- Verify settlement
SELECT * FROM TBL_SETTLEMENT WHERE stl_id = 'STL-000001';
```

## Step 3: Upload Documents and Create Cortex Search Service

```sql
-- Create stage for documents
CREATE OR REPLACE STAGE legal_docs_stage DIRECTORY = (ENABLE = TRUE);

-- Upload ALL documents (main + case notes + regulation PDFs):
-- snow stage copy data/legal/docs/*.txt @legal_docs_stage/
-- snow stage copy data/legal/docs/case_notes/*.txt @legal_docs_stage/case_notes/
-- snow stage copy data/legal/docs/real_regulations/*.pdf @legal_docs_stage/regulations/

-- Parse documents into searchable chunks
CREATE OR REPLACE TABLE LEGAL_DOC_CHUNKS AS
WITH parsed AS (
  SELECT
    RELATIVE_PATH as file_path,
    SPLIT_PART(RELATIVE_PATH, '/', -1) as file_name,
    CASE
      WHEN file_name LIKE 'sec_complaint%' THEN 'SEC Enforcement Complaint'
      WHEN file_name LIKE 'compliance_manual%' THEN 'Compliance Manual'
      WHEN file_name LIKE 'settlement%' THEN 'Settlement Agreement'
      WHEN file_name LIKE 'deposition%' THEN 'Deposition Transcript'
      WHEN file_name LIKE 'merger_agreement%' THEN 'Merger Agreement'
      WHEN file_name LIKE 'opinion%' THEN 'Court Opinion'
      WHEN file_name LIKE 'expert_report%' THEN 'Expert Report'
      WHEN file_name LIKE 'form_adv%' THEN 'Regulatory Filing'
      WHEN file_name LIKE 'email%' THEN 'Email Chain'
      WHEN file_name LIKE 'board%' THEN 'Board Minutes'
      WHEN file_name LIKE 'trading_log%' THEN 'Trading Log'
      WHEN file_name LIKE 'attorney%' THEN 'Attorney Work Product'
      WHEN file_name LIKE 'cfr%' THEN 'Federal Regulation (CFR)'
      WHEN file_name LIKE 'federal_rules%' THEN 'Federal Rules of Civil Procedure'
      ELSE 'Other'
    END as document_category,
    SNOWFLAKE.CORTEX.PARSE_DOCUMENT(
      @legal_docs_stage, RELATIVE_PATH, {'mode': 'LAYOUT'}
    ) as parsed_content
  FROM DIRECTORY(@legal_docs_stage)
)
SELECT
  file_path, file_name, document_category,
  c.value:text::VARCHAR as chunk_text,
  c.index as chunk_index
FROM parsed,
LATERAL FLATTEN(input => parsed_content:content) c
WHERE c.value:text IS NOT NULL AND LENGTH(c.value:text::VARCHAR) > 100;

-- Create Cortex Search Service
CREATE OR REPLACE CORTEX SEARCH SERVICE legal_docs_search
  ON chunk_text
  ATTRIBUTES file_name, document_category
  WAREHOUSE = COMPUTE_WH
  TARGET_LAG = '1 hour'
  AS (
    SELECT chunk_text, file_name, document_category, file_path, chunk_index
    FROM LEGAL_DOC_CHUNKS
  );
```

## Step 4: Upload Semantic Model and Create Agent

```bash
# Upload semantic model to stage
snow stage copy config/cortex_agent/legal_semantic_model.yaml @legal_data_stage/
```

```sql
-- Create the Cortex Agent
CREATE OR REPLACE CORTEX AGENT legal_benchmark_agent
  COMMENT = 'Legal benchmark agent with full semantic model — SEC v. Meridian Capital'
  MODEL = 'claude-3-5-sonnet'
  TOOLS = (
    TOOL cortex_analyst_tool
      TYPE = 'cortex_analyst'
      SEMANTIC_MODEL_FILE = '@legal_data_stage/legal_semantic_model.yaml',

    TOOL document_search_tool
      TYPE = 'cortex_search'
      CORTEX_SEARCH_SERVICE = 'LEGAL_BENCHMARK_DB.LEGAL.legal_docs_search'
      DESCRIPTION = 'Search legal documents including SEC enforcement complaint, compliance manual, settlement agreement, deposition transcript, merger agreement, court opinions, expert report, regulatory filings, email chains, Board minutes, trading logs, attorney memos, and CFR regulations. All related to SEC v. Meridian Capital Group LLC (docket SDNY-2022-CIV-04851).'
      MAX_RESULTS = 5
  )
  SYSTEM_PROMPT = $$
You are a legal research assistant specializing in securities fraud litigation.
You have access to:
1. A case management database with 12 tables (coded column names — use the semantic model for definitions)
2. A document corpus covering the SEC v. Meridian Capital Group enforcement action

Key code translations (from semantic model):
- pty_role_cd: PLF=Plaintiff, DEF=Defendant, WIT=Witness, INT=Intervenor
- evt_typ_cd: MTN=Motion, HRG=Hearing, ORD=Order, BRF=Brief, JDG=Judgment
- ruling_cd: GRT=Granted, DNY=Denied, PART=Granted in Part
- case_typ_cd: CIV=Civil, CRM=Criminal, BKR=Bankruptcy
- case_sts_cd: OPN=Open, CLS=Closed, STL=Settled, DSM=Dismissed

The central case is SEC v. Meridian Capital Group LLC (docket SDNY-2022-CIV-04851),
a securities fraud action involving insider trading in Apex Technologies stock ahead
of a merger with Global Systems Corp. Settlement: $347.5 million.

For hybrid questions: search documents first to get thresholds/rules, then query tables
to find matching data. Always cite sources.
$$;
```

## Step 5: Test the Agent

```sql
-- Test structured query (uses semantic model to decode pty_role_cd='DEF')
SELECT SNOWFLAKE.CORTEX.AGENT(
  'LEGAL_BENCHMARK_DB.LEGAL.legal_benchmark_agent',
  'Who are the defendants in case SDNY-2022-CIV-04851?'
);

-- Test document retrieval
SELECT SNOWFLAKE.CORTEX.AGENT(
  'LEGAL_BENCHMARK_DB.LEGAL.legal_benchmark_agent',
  'What is the opt-out deadline in the Thornton v. Meridian settlement?'
);

-- Test hybrid (doc + SQL)
SELECT SNOWFLAKE.CORTEX.AGENT(
  'LEGAL_BENCHMARK_DB.LEGAL.legal_benchmark_agent',
  'The compliance manual requires reporting within 72 hours. When was the SEC investigation actually opened?'
);
```

## Cortex Agent Advantages in This Benchmark

1. **Code Translation:** Semantic model tells the agent that `pty_role_cd='PLF'` means Plaintiff
2. **Relationship Definitions:** Joins are pre-defined (tbl_case_pty_atty bridges all three)
3. **Verified Queries:** Common patterns pre-approved (motion outcomes, top statutes)
4. **Model Selection:** Can use `claude-3-5-sonnet` for complex legal reasoning
5. **Cortex Search:** Fine-grained chunk control + document_category attribute filtering
6. **System Prompt:** Agent knows the code values without needing to guess from data
