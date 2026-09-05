export async function streamSnowflakeAgent({ accountUrl, agentPath, pat, query, callbacks }) {
  const { onStatus, onTextDelta, onToolUse, onToolResult, onTable, onChart, onComplete, onError } = callbacks;

  const body = {
    messages: [{ role: 'user', content: [{ type: 'text', text: query }] }],
    stream: true,
  };

  const res = await fetch('/api/snowflake', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ accountUrl, agentPath, pat, body }),
  });

  if (!res.ok) {
    const err = await res.json().catch(() => ({ error: res.statusText }));
    throw new Error(err.error || `HTTP ${res.status}`);
  }

  const reader = res.body.getReader();
  const decoder = new TextDecoder();
  let buffer = '';

  while (true) {
    const { done, value } = await reader.read();
    if (done) break;
    buffer += decoder.decode(value, { stream: true });

    // Process complete SSE blocks (separated by double newlines)
    const blocks = buffer.split('\n\n');
    buffer = blocks.pop() || ''; // keep incomplete block in buffer

    for (const block of blocks) {
      if (!block.trim()) continue;

      let eventName = null;
      let dataStr = '';

      for (const line of block.split('\n')) {
        if (line.startsWith('event: ')) {
          eventName = line.slice(7).trim();
        } else if (line.startsWith('data: ')) {
          dataStr += line.slice(6);
        } else if (line.startsWith('data:')) {
          dataStr += line.slice(5);
        }
      }

      if (eventName && dataStr) {
        try {
          const data = JSON.parse(dataStr);
          if (eventName === 'response') {
            console.log('[SF] Final response event received, metadata:', JSON.stringify(data.metadata?.usage || 'none').slice(0, 500));
          }
          handleEvent(eventName, data, callbacks);
        } catch (e) {
          console.warn('[SF] Failed to parse SSE data for event:', eventName, e.message, 'data length:', dataStr.length);
        }
      }
    }
  }

  // Process any remaining buffer
  if (buffer.trim()) {
    let eventName = null;
    let dataStr = '';
    for (const line of buffer.split('\n')) {
      if (line.startsWith('event: ')) eventName = line.slice(7).trim();
      else if (line.startsWith('data: ')) dataStr += line.slice(6);
      else if (line.startsWith('data:')) dataStr += line.slice(5);
    }
    if (eventName && dataStr) {
      try {
        const data = JSON.parse(dataStr);
        if (eventName === 'response') {
          console.log('[SF] Final response from remaining buffer, metadata:', JSON.stringify(data.metadata?.usage || 'none').slice(0, 500));
        }
        handleEvent(eventName, data, callbacks);
      } catch (e) {
        console.warn('[SF] Failed to parse remaining buffer:', e.message);
      }
    }
  }
}

function handleEvent(event, data, callbacks) {
  const { onStatus, onTextDelta, onToolUse, onToolResult, onTable, onChart, onComplete } = callbacks;

  switch (event) {
    case 'response.status':
      onStatus?.(data.message || data.status);
      break;

    case 'response.text.delta':
      onTextDelta?.(data.text);
      break;

    case 'response.text':
      break;

    case 'response.tool_use':
      onToolUse?.({
        id: data.tool_use_id,
        type: data.type,
        name: data.name,
        input: data.input,
      });
      break;

    case 'response.tool_result':
      onToolResult?.({
        id: data.tool_use_id,
        type: data.type,
        name: data.name,
        status: data.status,
        content: data.content,
      });
      break;

    case 'response.tool_result.status':
      onStatus?.(data.message || data.status);
      break;

    case 'response.tool_result.analyst.delta':
      if (data.delta?.sql) {
        onToolResult?.({
          id: data.tool_use_id,
          type: 'analyst_sql',
          name: data.tool_name,
          status: 'sql',
          content: [{ type: 'text', text: data.delta.sql }],
          resultSet: data.delta.result_set,
        });
      }
      break;

    case 'response.table':
      onTable?.({
        id: data.tool_use_id,
        title: data.title,
        resultSet: data.result_set,
      });
      break;

    case 'response.chart':
      onChart?.({
        id: data.tool_use_id,
        chartSpec: data.chart_spec,
      });
      break;

    case 'response':
      onComplete?.(data);
      break;

    case 'error':
      callbacks.onError?.(data.message || 'Unknown error');
      break;
  }
}
