import express from 'express';
import cors from 'cors';

const app = express();
app.use(cors());
app.use(express.json({ limit: '1mb' }));

// Snowflake Cortex Agent -- stream SSE
app.post('/api/snowflake', async (req, res) => {
  const { accountUrl, agentPath, pat, body } = req.body;
  const url = `${accountUrl}${agentPath}`;

  try {
    const upstream = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${pat}`,
        'Accept': 'text/event-stream',
      },
      body: JSON.stringify(body),
    });

    if (!upstream.ok) {
      const text = await upstream.text();
      return res.status(upstream.status).json({ error: text });
    }

    res.setHeader('Content-Type', 'text/event-stream');
    res.setHeader('Cache-Control', 'no-cache');
    res.setHeader('Connection', 'keep-alive');

    const reader = upstream.body.getReader();
    const decoder = new TextDecoder();

    const pump = async () => {
      while (true) {
        const { done, value } = await reader.read();
        if (done) { res.end(); return; }
        res.write(decoder.decode(value, { stream: true }));
      }
    };
    pump().catch(() => res.end());

    req.on('close', () => { reader.cancel(); });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// Databricks Genie Agent -- JSON passthrough
app.post('/api/databricks', async (req, res) => {
  const { endpoint, pat, body } = req.body;

  try {
    const upstream = await fetch(endpoint, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${pat}`,
      },
      body: JSON.stringify(body),
    });

    if (!upstream.ok) {
      const text = await upstream.text();
      return res.status(upstream.status).json({ error: text });
    }

    const data = await upstream.json();
    // Capture request ID for trace lookup
    const requestId = upstream.headers.get('x-request-id')
      || upstream.headers.get('x-databricks-request-id')
      || upstream.headers.get('databricks-request-id')
      || null;
    res.json({ ...data, _requestId: requestId, _responseHeaders: Object.fromEntries(upstream.headers.entries()) });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// Databricks MLflow Traces API -- fetch trace for a completed request
app.post('/api/databricks-traces', async (req, res) => {
  const { workspaceUrl, pat, requestId, endpointName } = req.body;

  try {
    // Search for traces associated with this request
    // The traces API uses the experiment tied to the serving endpoint
    const searchUrl = `${workspaceUrl}/api/2.0/mlflow/traces?filter=request_metadata.databricks_request_id%3D%27${requestId}%27&max_results=1`;

    let traceData = null;

    // Try direct trace lookup first
    const traceRes = await fetch(searchUrl, {
      headers: { 'Authorization': `Bearer ${pat}` },
    });

    if (traceRes.ok) {
      traceData = await traceRes.json();
    }

    // If no traces found by request ID, try listing recent traces for the endpoint
    if (!traceData?.traces?.length) {
      const listUrl = `${workspaceUrl}/api/2.0/mlflow/traces?max_results=5&order_by=timestamp_ms+DESC`;
      const listRes = await fetch(listUrl, {
        headers: { 'Authorization': `Bearer ${pat}` },
      });
      if (listRes.ok) {
        const listData = await listRes.json();
        // Find matching trace by looking at most recent
        traceData = listData;
      }
    }

    if (traceData?.traces?.length > 0) {
      const trace = traceData.traces[0];
      // Fetch full trace spans
      const traceId = trace.info?.request_id;
      if (traceId) {
        const spanUrl = `${workspaceUrl}/api/2.0/mlflow/traces/${traceId}`;
        const spanRes = await fetch(spanUrl, {
          headers: { 'Authorization': `Bearer ${pat}` },
        });
        if (spanRes.ok) {
          const spanData = await spanRes.json();
          return res.json(spanData);
        }
      }
      return res.json(trace);
    }

    res.json({ traces: [], message: 'No traces found' });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// Snowflake Cortex REST API (chat completions) -- JSON passthrough for evaluator
app.post('/api/cortex-rest', async (req, res) => {
  const { accountUrl, apiPath, pat, body } = req.body;
  const url = `${accountUrl}${apiPath}`;

  try {
    const upstream = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${pat}`,
      },
      body: JSON.stringify(body),
    });

    if (!upstream.ok) {
      const text = await upstream.text();
      return res.status(upstream.status).json({ error: text });
    }

    const data = await upstream.json();
    res.json(data);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

const PORT = process.env.PORT || 3001;
app.listen(PORT, () => {
  console.log(`Proxy server running on http://localhost:${PORT}`);
});
