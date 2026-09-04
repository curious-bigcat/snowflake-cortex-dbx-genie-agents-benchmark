# CRE Benchmark -- Snowflake Cortex Agent Setup Guide

## Prerequisites
- Snowflake account with Cortex Agent access
- ACCOUNTADMIN or role with CREATE DATABASE, CREATE CORTEX SEARCH SERVICE, CREATE AGENT privileges
- A warehouse (recommend XL or larger for data loading)

## Step 1: Create Database and Schema

```sql
CREATE DATABASE IF NOT EXISTS CRE_BENCHMARK_DB;
CREATE SCHEMA IF NOT EXISTS CRE_BENCHMARK_DB.CRE;
USE CRE_BENCHMARK_DB.CRE;
```

## Step 2: Create Stage and File Format

```sql
CREATE OR REPLACE STAGE cre_data_stage
  ENCRYPTION = (TYPE = 'SNOWFLAKE_SSE');

CREATE OR REPLACE FILE FORMAT parquet_ff
  TYPE = PARQUET;
```

Upload parquet files using Snowflake CLI or UI:
```bash
snow stage copy data/cre/tables/*.parquet @CRE_BENCHMARK_DB.CRE.cre_data_stage/tables/
```

## Step 3: Create Tables from Parquet

Note: Parquet timestamps are loaded as integers and converted via `TO_DATE(TO_TIMESTAMP(..., 6))`.

```sql
-- Core Lending Tables
CREATE OR REPLACE TABLE TBL_LOAN_MSTR AS
SELECT
    "$1":loan_id::VARCHAR            AS loan_id,
    "$1":borrower_id::VARCHAR        AS borrower_id,
    "$1":analyst_id::VARCHAR         AS analyst_id,
    "$1":branch_cd::VARCHAR          AS branch_cd,
    "$1":loan_typ_cd::VARCHAR        AS loan_typ_cd,
    "$1":prop_typ_cd::VARCHAR        AS prop_typ_cd,
    "$1":rate_typ_cd::VARCHAR        AS rate_typ_cd,
    "$1":loan_sts_cd::VARCHAR        AS loan_sts_cd,
    "$1":risk_rtg_cd::VARCHAR        AS risk_rtg_cd,
    "$1":uw_exception_flg::VARCHAR   AS uw_exception_flg,
    "$1":orig_amt::DOUBLE            AS orig_amt,
    "$1":curr_bal::DOUBLE            AS curr_bal,
    "$1":int_rate::DOUBLE            AS int_rate,
    TO_DATE(TO_TIMESTAMP("$1":orig_dt::INTEGER, 6)) AS orig_dt,
    TO_DATE(TO_TIMESTAMP("$1":mat_dt::INTEGER, 6))  AS mat_dt
FROM @cre_data_stage/tables/tbl_loan_mstr.parquet (FILE_FORMAT => 'parquet_ff');

CREATE OR REPLACE TABLE TBL_BORROWER AS
SELECT
    "$1":borrower_id::VARCHAR    AS borrower_id,
    "$1":entity_nm::VARCHAR      AS entity_nm,
    "$1":entity_typ_cd::VARCHAR  AS entity_typ_cd,
    "$1":naics_cd::VARCHAR       AS naics_cd,
    "$1":risk_tier_cd::VARCHAR   AS risk_tier_cd,
    "$1":state_cd::VARCHAR       AS state_cd,
    "$1":tax_id::VARCHAR         AS tax_id
FROM @cre_data_stage/tables/tbl_borrower.parquet (FILE_FORMAT => 'parquet_ff');

CREATE OR REPLACE TABLE TBL_COLLATERAL AS
SELECT
    "$1":collateral_id::VARCHAR  AS collateral_id,
    "$1":loan_id::VARCHAR        AS loan_id,
    "$1":prop_nm::VARCHAR        AS prop_nm,
    "$1":prop_typ_cd::VARCHAR    AS prop_typ_cd,
    "$1":prop_addr::VARCHAR      AS prop_addr,
    "$1":city::VARCHAR           AS city,
    "$1":state_cd::VARCHAR       AS state_cd,
    "$1":zip_cd::VARCHAR         AS zip_cd,
    "$1":sqft::INTEGER           AS sqft,
    "$1":orig_appr_val::DOUBLE   AS orig_appr_val,
    "$1":curr_appr_val::DOUBLE   AS curr_appr_val,
    "$1":ltv_orig::DOUBLE        AS ltv_orig,
    "$1":ltv_curr::DOUBLE        AS ltv_curr,
    "$1":occup_rate::DOUBLE      AS occup_rate
FROM @cre_data_stage/tables/tbl_collateral.parquet (FILE_FORMAT => 'parquet_ff');

CREATE OR REPLACE TABLE TBL_APPRAISAL AS
SELECT
    "$1":appraisal_id::VARCHAR   AS appraisal_id,
    "$1":collateral_id::VARCHAR  AS collateral_id,
    "$1":appraiser_id::VARCHAR   AS appraiser_id,
    "$1":appraiser_nm::VARCHAR   AS appraiser_nm,
    "$1":appr_mthd_cd::VARCHAR   AS appr_mthd_cd,
    "$1":review_sts_cd::VARCHAR  AS review_sts_cd,
    "$1":appr_val::DOUBLE        AS appr_val,
    TO_DATE(TO_TIMESTAMP("$1":appr_dt::INTEGER, 6)) AS appr_dt
FROM @cre_data_stage/tables/tbl_appraisal.parquet (FILE_FORMAT => 'parquet_ff');

CREATE OR REPLACE TABLE TBL_PAYMENT AS
SELECT
    "$1":payment_id::VARCHAR     AS payment_id,
    "$1":loan_id::VARCHAR        AS loan_id,
    "$1":pmt_sts_cd::VARCHAR     AS pmt_sts_cd,
    "$1":pmt_amt::DOUBLE         AS pmt_amt,
    "$1":prin_amt::DOUBLE        AS prin_amt,
    "$1":int_amt::DOUBLE         AS int_amt,
    "$1":days_past_due::INTEGER  AS days_past_due,
    TO_DATE(TO_TIMESTAMP("$1":pmt_dt::INTEGER, 6)) AS pmt_dt
FROM @cre_data_stage/tables/tbl_payment.parquet (FILE_FORMAT => 'parquet_ff');

-- Risk & Covenant Tables
CREATE OR REPLACE TABLE TBL_COVENANT AS
SELECT
    "$1":covenant_id::VARCHAR    AS covenant_id,
    "$1":loan_id::VARCHAR        AS loan_id,
    "$1":cov_typ_cd::VARCHAR     AS cov_typ_cd,
    "$1":freq_cd::VARCHAR        AS freq_cd,
    "$1":threshold_val::DOUBLE   AS threshold_val,
    TO_DATE(TO_TIMESTAMP("$1":eff_dt::INTEGER, 6)) AS eff_dt,
    TO_DATE(TO_TIMESTAMP("$1":exp_dt::INTEGER, 6)) AS exp_dt
FROM @cre_data_stage/tables/tbl_covenant.parquet (FILE_FORMAT => 'parquet_ff');

CREATE OR REPLACE TABLE TBL_COVENANT_TEST AS
SELECT
    "$1":test_id::VARCHAR        AS test_id,
    "$1":covenant_id::VARCHAR    AS covenant_id,
    "$1":pass_fail_cd::VARCHAR   AS pass_fail_cd,
    "$1":waiver_flg::VARCHAR     AS waiver_flg,
    "$1":waiver_reason::VARCHAR  AS waiver_reason,
    "$1":actual_val::DOUBLE      AS actual_val,
    TO_DATE(TO_TIMESTAMP("$1":test_dt::INTEGER, 6)) AS test_dt
FROM @cre_data_stage/tables/tbl_covenant_test.parquet (FILE_FORMAT => 'parquet_ff');

CREATE OR REPLACE TABLE TBL_RISK_RATING AS
SELECT
    "$1":rating_id::VARCHAR      AS rating_id,
    "$1":loan_id::VARCHAR        AS loan_id,
    "$1":analyst_id::VARCHAR     AS analyst_id,
    "$1":risk_rtg_cd::VARCHAR    AS risk_rtg_cd,
    "$1":prev_rtg_cd::VARCHAR    AS prev_rtg_cd,
    "$1":migration_cd::VARCHAR   AS migration_cd,
    TO_DATE(TO_TIMESTAMP("$1":rating_dt::INTEGER, 6)) AS rating_dt
FROM @cre_data_stage/tables/tbl_risk_rating.parquet (FILE_FORMAT => 'parquet_ff');

CREATE OR REPLACE TABLE TBL_PROVISION AS
SELECT
    "$1":provision_id::VARCHAR   AS provision_id,
    "$1":loan_id::VARCHAR        AS loan_id,
    "$1":prov_mthd_cd::VARCHAR   AS prov_mthd_cd,
    "$1":prov_amt::DOUBLE        AS prov_amt,
    "$1":loss_rate::DOUBLE       AS loss_rate,
    "$1":qual_adj_pct::DOUBLE    AS qual_adj_pct,
    TO_DATE(TO_TIMESTAMP("$1":prov_dt::INTEGER, 6)) AS prov_dt
FROM @cre_data_stage/tables/tbl_provision.parquet (FILE_FORMAT => 'parquet_ff');

-- Workout & Resolution Tables
CREATE OR REPLACE TABLE TBL_WORKOUT AS
SELECT
    "$1":workout_id::VARCHAR     AS workout_id,
    "$1":loan_id::VARCHAR        AS loan_id,
    "$1":workout_typ_cd::VARCHAR AS workout_typ_cd,
    "$1":resolution_cd::VARCHAR  AS resolution_cd,
    "$1":orig_bal::DOUBLE        AS orig_bal,
    "$1":modified_bal::DOUBLE    AS modified_bal,
    "$1":haircut_pct::DOUBLE     AS haircut_pct,
    TO_DATE(TO_TIMESTAMP("$1":start_dt::INTEGER, 6))      AS start_dt,
    TO_DATE(TO_TIMESTAMP("$1":resolution_dt::INTEGER, 6))  AS resolution_dt
FROM @cre_data_stage/tables/tbl_workout.parquet (FILE_FORMAT => 'parquet_ff');

CREATE OR REPLACE TABLE TBL_REO AS
SELECT
    "$1":reo_id::VARCHAR         AS reo_id,
    "$1":loan_id::VARCHAR        AS loan_id,
    "$1":collateral_id::VARCHAR  AS collateral_id,
    "$1":reo_sts_cd::VARCHAR     AS reo_sts_cd,
    "$1":acq_val::DOUBLE         AS acq_val,
    "$1":sale_val::DOUBLE        AS sale_val,
    "$1":carrying_cost::DOUBLE   AS carrying_cost,
    TO_DATE(TO_TIMESTAMP("$1":acq_dt::INTEGER, 6))  AS acq_dt,
    TO_DATE(TO_TIMESTAMP("$1":sale_dt::INTEGER, 6)) AS sale_dt
FROM @cre_data_stage/tables/tbl_reo.parquet (FILE_FORMAT => 'parquet_ff');

CREATE OR REPLACE TABLE TBL_CHARGE_OFF AS
SELECT
    "$1":chargeoff_id::VARCHAR   AS chargeoff_id,
    "$1":loan_id::VARCHAR        AS loan_id,
    "$1":co_typ_cd::VARCHAR      AS co_typ_cd,
    "$1":co_amt::DOUBLE          AS co_amt,
    "$1":recovery_amt::DOUBLE    AS recovery_amt,
    TO_DATE(TO_TIMESTAMP("$1":co_dt::INTEGER, 6))       AS co_dt,
    TO_DATE(TO_TIMESTAMP("$1":recovery_dt::INTEGER, 6))  AS recovery_dt
FROM @cre_data_stage/tables/tbl_charge_off.parquet (FILE_FORMAT => 'parquet_ff');

-- Regulatory & Organizational Tables
CREATE OR REPLACE TABLE TBL_EXAM_FINDING AS
SELECT
    "$1":finding_id::VARCHAR             AS finding_id,
    "$1":exam_id::VARCHAR                AS exam_id,
    "$1":exam_typ_cd::VARCHAR            AS exam_typ_cd,
    "$1":category_cd::VARCHAR            AS category_cd,
    "$1":severity_cd::VARCHAR            AS severity_cd,
    "$1":remediation_sts_cd::VARCHAR     AS remediation_sts_cd,
    "$1":finding_desc::VARCHAR           AS finding_desc,
    TO_DATE(TO_TIMESTAMP("$1":finding_dt::INTEGER, 6)) AS finding_dt,
    TO_DATE(TO_TIMESTAMP("$1":due_dt::INTEGER, 6))     AS due_dt
FROM @cre_data_stage/tables/tbl_exam_finding.parquet (FILE_FORMAT => 'parquet_ff');

CREATE OR REPLACE TABLE TBL_CAPITAL AS
SELECT
    "$1":capital_id::VARCHAR     AS capital_id,
    "$1":tier1_cap::DOUBLE       AS tier1_cap,
    "$1":tier2_cap::DOUBLE       AS tier2_cap,
    "$1":rwa::DOUBLE             AS rwa,
    "$1":cet1_ratio::DOUBLE      AS cet1_ratio,
    "$1":tier1_ratio::DOUBLE     AS tier1_ratio,
    "$1":total_ratio::DOUBLE     AS total_ratio,
    "$1":leverage_ratio::DOUBLE  AS leverage_ratio,
    TO_DATE(TO_TIMESTAMP("$1":report_dt::INTEGER, 6)) AS report_dt
FROM @cre_data_stage/tables/tbl_capital.parquet (FILE_FORMAT => 'parquet_ff');

CREATE OR REPLACE TABLE TBL_CONCENTRATION AS
SELECT
    "$1":conc_id::VARCHAR        AS conc_id,
    "$1":segment_cd::VARCHAR     AS segment_cd,
    "$1":segment_val::VARCHAR    AS segment_val,
    "$1":breach_flg::VARCHAR     AS breach_flg,
    "$1":exposure_amt::DOUBLE    AS exposure_amt,
    "$1":pct_of_total::DOUBLE    AS pct_of_total,
    "$1":pct_of_capital::DOUBLE  AS pct_of_capital,
    "$1":limit_pct::INTEGER      AS limit_pct,
    TO_DATE(TO_TIMESTAMP("$1":report_dt::INTEGER, 6)) AS report_dt
FROM @cre_data_stage/tables/tbl_concentration.parquet (FILE_FORMAT => 'parquet_ff');

CREATE OR REPLACE TABLE TBL_BRANCH AS
SELECT
    "$1":branch_cd::VARCHAR      AS branch_cd,
    "$1":branch_nm::VARCHAR      AS branch_nm,
    "$1":city::VARCHAR           AS city,
    "$1":state_cd::VARCHAR       AS state_cd,
    "$1":region_cd::VARCHAR      AS region_cd,
    "$1":mgr_id::VARCHAR         AS mgr_id
FROM @cre_data_stage/tables/tbl_branch.parquet (FILE_FORMAT => 'parquet_ff');

CREATE OR REPLACE TABLE TBL_ANALYST AS
SELECT
    "$1":analyst_id::VARCHAR     AS analyst_id,
    "$1":analyst_nm::VARCHAR     AS analyst_nm,
    "$1":branch_cd::VARCHAR      AS branch_cd,
    "$1":role_cd::VARCHAR        AS role_cd,
    "$1":cert_cd::VARCHAR        AS cert_cd,
    TO_DATE(TO_TIMESTAMP("$1":hire_dt::INTEGER, 6)) AS hire_dt
FROM @cre_data_stage/tables/tbl_analyst.parquet (FILE_FORMAT => 'parquet_ff');

CREATE OR REPLACE TABLE TBL_AUDIT_LOG AS
SELECT
    "$1":audit_id::VARCHAR       AS audit_id,
    "$1":loan_id::VARCHAR        AS loan_id,
    "$1":user_id::VARCHAR        AS user_id,
    "$1":action_cd::VARCHAR      AS action_cd,
    "$1":detail_txt::VARCHAR     AS detail_txt,
    TO_DATE(TO_TIMESTAMP("$1":action_dt::INTEGER, 6)) AS action_dt
FROM @cre_data_stage/tables/tbl_audit_log.parquet (FILE_FORMAT => 'parquet_ff');
```

## Step 4: Upload Documents and Create Cortex Search Service

```sql
CREATE OR REPLACE STAGE cre_docs_stage
  DIRECTORY = (ENABLE = TRUE)
  ENCRYPTION = (TYPE = 'SNOWFLAKE_SSE');

-- Upload all docs (TXT + PDF) via CLI or UI:
-- snow stage copy data/cre/docs/bank_documents/*.txt @CRE_BENCHMARK_DB.CRE.cre_docs_stage/bank_documents/
-- snow stage copy data/cre/docs/case_files/*.txt @CRE_BENCHMARK_DB.CRE.cre_docs_stage/case_files/
-- snow stage copy data/cre/docs/real_regulations/*.pdf @CRE_BENCHMARK_DB.CRE.cre_docs_stage/real_regulations/

-- Parse documents into a searchable table
CREATE OR REPLACE TABLE CRE_DOCS_PARSED AS
SELECT
    RELATIVE_PATH AS doc_name,
    SNOWFLAKE.CORTEX.PARSE_DOCUMENT(
        @cre_docs_stage,
        RELATIVE_PATH,
        {'mode': 'LAYOUT'}
    ):content::VARCHAR AS doc_content
FROM DIRECTORY(@cre_docs_stage)
WHERE RELATIVE_PATH LIKE '%/%';

-- Create Cortex Search Service
CREATE OR REPLACE CORTEX SEARCH SERVICE CRE_DOCS_SEARCH
  ON doc_content
  ATTRIBUTES doc_name
  WAREHOUSE = <YOUR_WAREHOUSE>
  TARGET_LAG = '1 hour'
  AS (SELECT doc_name, doc_content FROM CRE_DOCS_PARSED);
```

## Step 5: Create Semantic View

Run the full semantic view DDL from `config/cortex_agent/cre_semantic_view.sql`.

## Step 6: Create Cortex Agent

```sql
CREATE OR REPLACE CORTEX AGENT CRE_BENCHMARK_AGENT
  COMMENT = 'CRE Portfolio Stress & Workout benchmark agent for Pacific Northwest Bank'
  MODEL = 'claude-3-5-sonnet'
  TOOLS = (
    ANALYST(SEMANTIC_VIEW => 'CRE_BENCHMARK_DB.CRE.CRE_SEMANTIC_VIEW'),
    SEARCH(SEARCH_SERVICE => 'CRE_BENCHMARK_DB.CRE.CRE_DOCS_SEARCH')
  );
```

## Step 7: Test the Agent

```sql
SELECT SNOWFLAKE.CORTEX.DATA_AGENT_RUN(
  'CRE_BENCHMARK_DB.CRE.CRE_BENCHMARK_AGENT',
  $${"messages": [{"role": "user", "content": "What is PNB's total CRE office exposure and what percentage of those loans are rated Special Mention or worse?"}]}$$
);
```
