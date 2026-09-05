export async function callDatabricksAgent({ endpoint, pat, query, callbacks }) {
  const { onStatus, onTextDelta, onToolUse, onToolResult, onComplete, onError } = callbacks;

  onStatus?.('Databricks is processing...');

  const body = {
    input: [{ role: 'user', content: query }],
  };

  const res = await fetch('/api/databricks', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ endpoint, pat, body }),
  });

  if (!res.ok) {
    const err = await res.json().catch(() => ({ error: res.statusText }));
    throw new Error(err.error || `HTTP ${res.status}`);
  }

  const data = await res.json();
  onStatus?.('Processing response...');

  let finalText = '';
  const steps = [];
  let stepIndex = 0;

  // Parse Databricks Agent output format: { output: [ {type: "message"|"function_call", ...} ] }
  if (data.output && Array.isArray(data.output)) {
    for (const item of data.output) {
      if (item.type === 'function_call') {
        stepIndex++;
        const toolId = item.call_id || `tool-${stepIndex}`;
        let parsedArgs = item.arguments;
        try { parsedArgs = JSON.parse(item.arguments); } catch {}

        const step = {
          id: toolId,
          type: item.name?.includes('genie') ? 'genie' : item.name?.includes('ka-') ? 'knowledge_assistant' : 'function',
          name: item.name || 'tool',
          input: parsedArgs,
          phase: 'running',
          step: item.step,
        };
        steps.push(step);

      } else if (item.type === 'message' && item.role === 'assistant') {
        const texts = (item.content || [])
          .filter(c => c.type === 'output_text')
          .map(c => c.text);

        for (const t of texts) {
          if (item.call_id) {
            const matchingStep = steps.find(s => s.id === item.call_id);
            if (matchingStep) {
              matchingStep.phase = 'done';
              const isFailure = !t || t.trim() === '' ||
                /error|failed|unable to|cannot|can't determine|I can't|I cannot|no data|EMPTY/i.test(t);
              matchingStep.resultStatus = isFailure ? 'error' : 'success';
              matchingStep.result = [{ type: 'text', text: t || '(empty result)' }];
              if (t && t.includes('|') && t.includes('\n')) {
                matchingStep.tableData = parseGeniePipeTable(t);
                matchingStep.resultStatus = 'success';
              }
              continue;
            }
          }
          if (t.startsWith('<name>') && t.endsWith('</name>')) continue;
          finalText += (finalText ? '\n\n' : '') + t;
        }
      }
    }
  } else {
    if (data.choices?.[0]?.message?.content) {
      finalText = data.choices[0].message.content;
    } else if (data.content) {
      finalText = typeof data.content === 'string' ? data.content : JSON.stringify(data.content, null, 2);
    } else {
      finalText = JSON.stringify(data, null, 2);
    }
  }

  // Stream the final text
  if (finalText) {
    const words = finalText.split(' ');
    const chunkSize = 8;
    for (let i = 0; i < words.length; i += chunkSize) {
      const chunk = words.slice(i, i + chunkSize).join(' ') + (i + chunkSize < words.length ? ' ' : '');
      onTextDelta?.(chunk);
      await new Promise(r => setTimeout(r, 8));
    }
  }

  // Emit tool steps
  for (const step of steps) {
    if (!step.result && step.phase !== 'done') {
      step.phase = 'done';
      step.resultStatus = 'error';
      step.result = [{ type: 'text', text: '(no result returned)' }];
    }
    onToolUse?.(step);
    await new Promise(r => setTimeout(r, 50));
    onToolResult?.({
      id: step.id,
      type: step.type,
      name: step.name,
      status: step.resultStatus || 'success',
      content: step.result || [{ type: 'text', text: 'Completed' }],
      resultSet: step.resultSet,
      tableData: step.tableData,
    });
    await new Promise(r => setTimeout(r, 50));
  }

  const completeResponse = {
    role: 'assistant',
    content: [{ type: 'text', text: finalText }],
    toolCalls: steps,
  };

  onComplete?.(completeResponse);
  return completeResponse;
}

function parseGeniePipeTable(text) {
  const lines = text.trim().split('\n').filter(l => l.includes('|'));
  if (lines.length < 2) return null;

  const parseRow = (line) => line.split('|').map(c => c.trim()).filter(c => c !== '');
  const headers = parseRow(lines[0]);
  const dataStartIdx = lines[1].replace(/[|\-\s]/g, '') === '' ? 2 : 1;
  const rows = [];
  for (let i = dataStartIdx; i < lines.length; i++) {
    const cells = parseRow(lines[i]);
    if (cells.length > 0 && cells.some(c => c !== '-')) rows.push(cells);
  }

  if (headers.length === 0 || rows.length === 0) return null;

  return {
    resultSetMetaData: { numRows: rows.length, rowType: headers.map(name => ({ name, type: 'VARCHAR' })) },
    data: rows,
  };
}
