# Cortex Agent Benchmark

Comparative benchmark of **Snowflake Cortex Agents** vs **Databricks Genie** on a 12-question legal analytics workload.

All data is synthetic, built around a single complex securities fraud case: *SEC v. Meridian Capital Group LLC*. Tables, documents, and questions reference the same entities, enabling genuine cross-source reasoning tests.

## Results Summary

| Metric | Snowflake Cortex | Databricks Genie |
|--------|-----------------|-----------------|
| Accuracy | 12/12 (100%) | 11/12 (92%) |
| Avg Latency | 37s | 100s |
| Token Cost | $3.28 | $14.40 |
| Cost per Correct Answer | $0.27 | $1.31 |

Cost estimated at Anthropic Claude Sonnet published rates ($3/$15 per MTok).

## Repository Structure

```
cortex-agent-benchmark/
├── data_generator/
│   ├── universe.py                    # Master entity registry
│   ├── generate_legal_tables.py       # Generates 12 parquet tables (1.39M rows)
│   ├── generate_legal_docs.py         # Generates 8 text documents (~4K pages)
│   └── generate_case_notes.py         # Generates case note documents
├── data/legal/
│   ├── tables/                        # 12 parquet files
│   └── docs/                          # Text files + case notes + regulation PDFs
├── questions/
│   ├── legal_test_suite.yaml          # Full 60-question test suite (all tiers)
│   └── benchmark_queries.md           # 12 benchmark questions with run instructions
├── config/
│   ├── cortex_agent/
│   │   ├── legal_setup_guide.md       # Snowflake setup (tables + Cortex Search + Agent)
│   │   └── legal_semantic_model.yaml  # Semantic model with code definitions
│   └── genie_agent/
│       └── legal_setup_guide.md       # Databricks setup (raw schema, no hints)
├── reports/
│   ├── generate_charts.py             # Chart generation script (matplotlib)
│   └── benchmark_comparison.md        # Full written report
└── README.md
```

## Quick Start

### 1. Generate the data

```bash
pip install faker pandas numpy pyarrow
python data_generator/generate_legal_tables.py
python data_generator/generate_legal_docs.py
python data_generator/generate_case_notes.py
```

This produces:
- `data/legal/tables/` — 12 parquet files (1.39M rows total)
- `data/legal/docs/` — text documents and case notes

### 2. Set up Snowflake Cortex Agent

Follow `config/cortex_agent/legal_setup_guide.md`. Key steps:

```sql
-- Create database and load tables
CREATE DATABASE IF NOT EXISTS LEGAL_BENCHMARK_DB;
CREATE SCHEMA IF NOT EXISTS LEGAL_BENCHMARK_DB.LEGAL;

-- Upload parquet files to a stage, then create tables from them
CREATE OR REPLACE STAGE legal_data_stage FILE_FORMAT = (TYPE = PARQUET);
-- snow stage copy data/legal/tables/*.parquet @legal_data_stage/

-- Upload docs, create Cortex Search Service, upload semantic model, create Agent
-- (full SQL in the setup guide)
```

The Cortex Agent gets a **semantic model** that decodes all coded columns (`PLF` = Plaintiff, `MTD` = Motion to Dismiss, etc.) and defines table relationships.

### 3. Set up Databricks Genie

Follow `config/genie_agent/legal_setup_guide.md`. Key steps:

- Load parquet files into Unity Catalog tables
- Upload documents to a UC Volume
- Create a Genie Space pointing at the tables

Genie gets **raw schema only** — no column descriptions, no code mappings. It must infer meaning from data patterns.

### 4. Run the benchmark

See `questions/benchmark_queries.md` for the 12 questions and how to run them on each platform.

**Snowflake:**
```sql
SELECT SNOWFLAKE.CORTEX.DATA_AGENT_RUN(
  'LEGAL_BENCHMARK_DB.LEGAL.LEGAL_BENCHMARK_AGENT',
  $${"messages": [{"role": "user", "content": "How many plaintiffs filed motions to dismiss across all securities fraud cases in 2022?"}]}$$
);
```

**Databricks:** Send the same questions through the Genie Space UI or API.

## Dataset

### Tables (12 tables, 1.39M rows)

| Table | Rows | Purpose |
|-------|------|---------|
| tbl_case_mstr | 50,000 | Case registry (3 key cases + noise) |
| tbl_pty_info | 150,000 | Parties (10 key parties + noise) |
| tbl_atty_reg | 5,000 | Attorneys |
| tbl_case_pty_atty | 200,000 | Case-party-attorney bridge |
| tbl_evt_log | 500,000 | Case events |
| tbl_doc_ref | 300,000 | Document filings |
| tbl_ruling | 100,000 | Judicial rulings |
| tbl_statute_cite | 200,000 | Statute citations |
| tbl_claim | 80,000 | Claims/causes of action |
| tbl_damages | 60,000 | Damages sought/awarded |
| tbl_appeal | 20,000 | Appeals |
| tbl_settlement | 30,000 | Settlements |

### Documents (22 files, ~9K pages)

Core documents (8 text files): SEC complaint, compliance manual, settlement agreement, deposition transcript, merger agreement, court opinion, expert report, Form ADV.

Case notes (7 files): email chains, trading logs, board minutes, attorney memo, investigation notes.

Regulations (6 PDFs): CFR Title 17/18, Federal Rules of Civil Procedure, SEC Enforcement Manual.

## Benchmark Question Categories

| Category | Count | Tests |
|----------|-------|-------|
| Coded Column Decoding | 3 | Can the agent interpret `PLF`, `DEF`, `MTD`, `SEC`? |
| Complex Join Paths | 2 | Multi-table self-joins with role-based filtering |
| Noise Filtering | 3 | Find 3 needles in 50K cases |
| Model Reasoning | 2 | Legal doctrine + probability reasoning |
| Hybrid Doc + SQL | 2 | Retrieve doc facts, then query tables |

## Generating Report Charts

```bash
pip install matplotlib numpy
python reports/generate_charts.py
```

Outputs 8 PNG charts to `reports/charts/`.

## License

This repository contains synthetic data only. No real case data is included.
