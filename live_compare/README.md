# Agent Duel -- Live Comparison UI

Side-by-side comparison of **Snowflake Cortex Agent** vs **Databricks Genie Agent**. Send the same query to both agents simultaneously, watch responses stream in real-time, and compare UX metrics.

## Features

- **Real-time SSE streaming** for Snowflake Cortex Agent (typewriter effect)
- **Side-by-side response panels** with markdown rendering (tables, code blocks, lists)
- **Expandable tool steps** showing SQL queries, document searches, and tool results
- **Live UX metrics**: time-to-first-token (TTFT), total latency, token count, tool calls
- **Head-to-head comparison** strip with winner indicators and ratios
- **10 preset benchmark questions** (G01-G10) from the CRE benchmark suite
- **Session history** with export to JSON
- **Dark theme** with Snowflake/Databricks brand colors

## Quick Start

```bash
# Install dependencies
npm install

# Start the CORS proxy and dev server
npm start
```

This runs:
- **Proxy server** on `http://localhost:3001` (forwards API calls to avoid CORS)
- **Vite dev server** on `http://localhost:5173` (the UI)

Open `http://localhost:5173` in your browser.

## Setup

1. Click the gear icon (top right) to open Settings
2. Configure both platforms:

### Snowflake Cortex Agent
- **Account URL**: `https://<account>.snowflakecomputing.com`
- **Agent Path**: `/api/v2/databases/CRE_BENCHMARK_DB/schemas/CRE/agents/CRE_BENCHMARK_AGENT:run` (pre-filled)
- **PAT**: Generate a Programmatic Access Token in Snowsight (User Menu > Settings > Programmatic Access Tokens)

### Databricks Genie Agent
- **Endpoint URL**: `https://adb-xxx.azuredatabricks.net/serving-endpoints/<endpoint>/invocations` (pre-filled with the benchmark endpoint)
- **PAT**: Generate from Databricks workspace (User Settings > Developer > Access Tokens)

## Architecture

```
Browser (React)  -->  Express Proxy (localhost:3001)  -->  Snowflake / Databricks APIs
```

The proxy server forwards requests with auth headers to avoid browser CORS restrictions. Credentials are stored in localStorage and sent only to the local proxy.

## Metrics Tracked

| Metric | Description | Source |
|---|---|---|
| TTFT | Time to first text token | JS timestamp |
| Total Latency | Full response time | JS timestamp |
| Tokens | Total token count | Response metadata |
| Tool Calls | Number of SQL/search/sandbox invocations | SSE events / response parsing |
| Tool Failures | Tools that returned errors | Status field from tool results |

## Tech Stack

- React 18 + Vite
- Tailwind CSS v4
- react-markdown + remark-gfm
- Express (CORS proxy)
