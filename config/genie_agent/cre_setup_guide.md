# CRE Benchmark -- Databricks Genie Setup Guide

## Prerequisites
- Databricks workspace with Unity Catalog enabled
- Genie Spaces access (requires Databricks SQL Pro or Enterprise)
- A SQL warehouse (recommend Medium or larger)
- Azure Blob Storage container with parquet/doc files uploaded

## Step 1: Create Catalog and Schema

```sql
USE CATALOG `<your-catalog>`;
CREATE SCHEMA IF NOT EXISTS cre;
USE cre;
```

## Step 2: Upload Parquet Files to Azure Blob Storage

Upload all 18 parquet files from `data/cre/tables/` to your Azure blob container:

```bash
# Upload to Azure blob (using azcopy or Azure Storage Explorer)
azcopy copy "data/cre/tables/" "https://<your-storage-account>.blob.core.windows.net/<your-container>/cre/data_volume/" --recursive
```

## Step 3: Create Tables from Parquet

Run the following in a Databricks notebook cell (`%python`):

```python
base_path = "abfss://<your-container>@<your-storage-account>.dfs.core.windows.net/cre/data_volume"

tables = [
    "tbl_loan_mstr", "tbl_borrower", "tbl_collateral", "tbl_appraisal",
    "tbl_payment", "tbl_covenant", "tbl_covenant_test", "tbl_risk_rating",
    "tbl_provision", "tbl_workout", "tbl_reo", "tbl_charge_off",
    "tbl_exam_finding", "tbl_capital", "tbl_concentration",
    "tbl_branch", "tbl_analyst", "tbl_audit_log"
]

for table in tables:
    file_path = f"{base_path}/{table}.parquet"
    try:
        df = spark.read.parquet(file_path)
        df.write.mode("overwrite").saveAsTable(f"`<your-catalog>`.cre.{table}")
        print(f"Created: {table} ({df.count()} rows)")
    except Exception as e:
        print(f"Error: {table}: {e}")
```

## Step 4: Upload Documents to Volume

```python
# Create volume for documents
spark.sql("CREATE VOLUME IF NOT EXISTS `<your-catalog>`.cre.cre_documents")

volume_path = "/Volumes/<your-catalog>/cre/cre_documents"

# Upload bank documents (13 text files)
bank_docs_path = "abfss://<your-container>@<your-storage-account>.dfs.core.windows.net/cre/docs/bank_documents"
for f in dbutils.fs.ls(bank_docs_path):
    if f.name.endswith('.txt'):
        dbutils.fs.cp(f.path, f"{volume_path}/{f.name}")
        print(f"Copied bank doc: {f.name}")

# Upload case files (10 text files)
case_path = "abfss://<your-container>@<your-storage-account>.dfs.core.windows.net/cre/docs/case_files"
for f in dbutils.fs.ls(case_path):
    if f.name.endswith('.txt'):
        dbutils.fs.cp(f.path, f"{volume_path}/case_{f.name}")
        print(f"Copied case file: {f.name}")

# Upload real regulation PDFs (7 actual OCC/FDIC/Fed documents)
regs_path = "abfss://<your-container>@<your-storage-account>.dfs.core.windows.net/cre/docs/real_regulations"
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

Expected: 30 files (13 bank docs + 10 case files + 7 regulation PDFs).

## Step 5: Create Genie Agent (Raw Schema -- NO Context)

1. **Create new Agent** > select **Genie Agent**
2. Name: `CRE Benchmark - Raw Schema`
3. Add all 18 tables from `<your-catalog>.cre`:
   - tbl_loan_mstr, tbl_borrower, tbl_collateral, tbl_appraisal, tbl_payment
   - tbl_covenant, tbl_covenant_test, tbl_risk_rating, tbl_provision
   - tbl_workout, tbl_reo, tbl_charge_off
   - tbl_exam_finding, tbl_capital, tbl_concentration
   - tbl_branch, tbl_analyst, tbl_audit_log
4. **DO NOT ADD** any of the following:
   - No SQL expressions
   - No example queries
   - No text instructions
   - No column descriptions
5. The agent sees ONLY raw column names (loan_typ_cd, risk_rtg_cd, cov_typ_cd, etc.)

## Step 6: Create Knowledge Assistant

1. **Create new Agent** > select **Knowledge Assistant**
2. Name: `CRE Benchmark - Documents`
3. Connect to volume: `<your-catalog>.cre.cre_documents`
4. **Describe the content:**
   ```
   Document corpus for Pacific Northwest Bank (PNB) CRE portfolio stress analysis.
   Contains: OCC Consent Order 2023-CE-0847 (citing 420% CRE concentration),
   credit committee memo for Cascadia Tower ($85M office loan), JLL reappraisal
   report showing 40.5% value decline, covenant breach notices, workout proposals,
   internal audit report (23% underwriting exception rate), ALLL methodology memo
   with Q-factor history, Board Risk Committee minutes (Q4 2023), stress test
   results (CET1 projected to 6.1% under severe adverse), regulatory capital plan
   ($175M sub debt + $412M loan sale), foreclosure timeline for Mercer Industrial
   Park, loan modification agreement, borrower financials, and actual OCC/FDIC/Fed
   regulatory guidance (Comptroller's Handbook for CRE Lending, SR 07-1 CRE
   Concentration Guidance, Interagency Appraisal Guidelines, CRE Workout Policy,
   FDIC Loans Manual, Rating Credit Risk Handbook).
   ```
5. **Instructions:**
   ```
   When answering questions:
   - Cite specific document names and section numbers
   - Quote exact dollar amounts, dates, percentages, and ratios from the source
   - If information spans multiple documents, cite each source
   - For regulation questions, reference the specific OCC Bulletin, SR letter, or CFR section
   - Distinguish between PNB-specific documents and general regulatory guidance
   ```
6. **Enable content search** on the volume

## Step 7: Create Supervisor Agent

1. **Create new Agent** > select **Supervisor Agent**
2. Name: `CRE Benchmark - Pacific Northwest Bank`
3. Add child tools:
   - **Genie Agent** (`CRE Benchmark - Raw Schema`)
   - **Knowledge Assistant** (`CRE Benchmark - Documents`)
4. System instructions:
   ```
   You are a commercial banking analyst specializing in CRE credit risk.
   You have access to:
   1. A loan portfolio database with 18 tables (loans, borrowers, collateral,
      covenants, payments, risk ratings, provisions, workouts, REO, charge-offs,
      exam findings, capital, concentration metrics, branches, analysts, audit log)
      -- use the Genie Agent for data queries
   2. A document corpus with OCC consent orders, credit memos, appraisal reports,
      workout proposals, audit reports, stress tests, capital plans, and real
      OCC/FDIC/Fed regulatory guidance -- use the Knowledge Assistant for
      document questions

   For hybrid questions (requiring both data and documents):
   - First retrieve the relevant facts from documents for context
   - Then query the database to verify, calculate, or cross-reference
   - Reconcile any discrepancies between document claims and actual data

   Always cite your sources (document name + section, or table name + query).
   Flag data quality concerns when document figures don't match database values.
   ```

## Step 8: Test the Setup

### Test Genie Agent (structured queries)
```
"What is the total current balance of CRE office loans?"
Expected: Sum of curr_bal where loan_typ_cd = 'CRE_OFFC'
```

### Test Knowledge Assistant (document retrieval)
```
"What does the OCC consent order say about the CRE concentration threshold?"
Expected: 420% of capital vs 300% SR 07-1 guidance
```

### Test Supervisor (hybrid)
```
"What is PNB's total CRE office exposure, what percentage are rated Special Mention or worse, and what does the OCC guidance say about concentration limits?"
Expected: Routes to Genie (gets exposure + classified %), then KA (gets SR 07-1 threshold), synthesizes answer.
```

## Key Differences from Cortex Setup

| Aspect | Cortex Agent | Databricks Genie |
|--------|-------------|-----------------|
| Architecture | Single agent with parallel tool invocation | 3-agent hierarchy (Supervisor + Genie SQL + Knowledge Assistant) |
| Schema guidance | Full semantic view with column descriptions, code decode mappings, 8 VQRs | Raw schema only -- no column descriptions, no code mappings |
| Document search | Cortex Search service (embedding-based) | Knowledge Assistant with volume content search |
| Tool invocation | Parallel (Analyst + Search simultaneously) | Sequential -- supervisor routes to one child at a time |
| SQL generation | Guided by semantic view relationships and VQRs | Inferred from raw table/column names |
| Retry behavior | Single-pass (VQRs guide first-attempt accuracy) | Supervisor retries failed Genie calls, accumulating context |
