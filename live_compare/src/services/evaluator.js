export async function evaluateResponses({ question, sfResponse, dbxResponse, sfSteps, dbxSteps, sfHasCharts, sfHasTables, dbxHasCharts, dbxHasTables, groundTruth, accountUrl, pat }) {
  const sfEvidence = formatEvidence(sfSteps);
  const dbxEvidence = formatEvidence(dbxSteps);
  const gtSection = formatGroundTruth(groundTruth);

  const prompt = `You are a senior banking examiner evaluating two AI agent responses. You need to decide: which response would I trust to act on in a real regulatory review?

You have GROUND TRUTH (the correct answer elements) and TOOL EVIDENCE (what each agent actually retrieved).

QUESTION:
${question}

${gtSection}
---
RESPONSE A (Snowflake Cortex Agent):
${(sfResponse || '(No response)').slice(0, 4000)}

Visual elements: ${sfHasCharts ? 'Contains charts/visualizations' : 'No charts'}, ${sfHasTables ? 'Contains data tables' : 'No data tables'}

TOOL EVIDENCE A:
${sfEvidence || '(No tool evidence captured)'}

---
RESPONSE B (Databricks Genie Agent):
${(dbxResponse || '(No response)').slice(0, 4000)}

Visual elements: ${dbxHasCharts ? 'Contains charts/visualizations' : 'No charts'}, ${dbxHasTables ? 'Contains data tables' : 'No data tables'}

TOOL EVIDENCE B:
${dbxEvidence || '(No tool evidence captured)'}

---
Score each response 1-10 on these 5 dimensions. Be strict -- 10 means flawless.

1. ACCURACY: Check EVERY key fact from GROUND TRUTH against the response. Did it get the right numbers? Did it answer ALL sub-parts? Did it avoid the complexity traps? Count how many key facts are correct vs wrong vs missing. Score = (correct / total key facts) * 10, rounded.

2. GROUNDEDNESS: For EVERY factual claim (numbers, thresholds, dates, percentages), verify it traces to TOOL EVIDENCE (a specific SQL result or document excerpt). Regulatory thresholds (like 300% from SR 07-1) MUST come from a retrieved document, not model knowledge. If 100% of claims are evidence-backed, score 10. Deduct 1 point per ungrounded claim, minimum 1.

3. RELEVANCE: Does it directly answer what was asked without irrelevant padding? Is it well-structured for a banking professional to act on?

4. ACTIONABILITY: Could a bank examiner or credit officer immediately act on this response? Does it provide specific numbers, clear conclusions, and next steps? Does it flag risks and recommendations? Does it present data in structured form (tables, breakdowns) rather than buried in prose?

5. VISUAL_RICHNESS: Does the response use charts, data tables, or structured formatting to make the data easy to interpret at a glance? A response with a clear table and chart scores higher than one with the same data in paragraph form.

Return ONLY a JSON object (no markdown, no code fences):
{"A":{"accuracy":N,"groundedness":N,"relevance":N,"actionability":N,"visual_richness":N,"notes":"one sentence on key strength or weakness"},"B":{"accuracy":N,"groundedness":N,"relevance":N,"actionability":N,"visual_richness":N,"notes":"one sentence on key strength or weakness"}}`;

  const body = {
    model: 'claude-sonnet-4-5',
    messages: [{ role: 'user', content: prompt }],
    max_completion_tokens: 800,
    temperature: 0,
  };

  const res = await fetch('/api/cortex-rest', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      accountUrl,
      apiPath: '/api/v2/cortex/v1/chat/completions',
      pat,
      body,
    }),
  });

  if (!res.ok) {
    const errData = await res.json().catch(() => ({}));
    throw new Error(errData.error || `Evaluation failed: HTTP ${res.status}`);
  }

  const data = await res.json();

  const content = data.choices?.[0]?.message?.content;
  if (!content) {
    throw new Error('No content in evaluation response');
  }

  return parseEvalResult(content);
}

function formatGroundTruth(gt) {
  if (!gt) return '';
  const parts = ['GROUND TRUTH (expected answer elements):'];
  if (gt.tablesRequired?.length) parts.push(`Expected tables: ${gt.tablesRequired.join(', ')}`);
  if (gt.docsRequired?.length) parts.push(`Expected documents: ${gt.docsRequired.join(', ')}`);
  if (gt.keyFacts?.length) {
    parts.push('Key facts and traps (use these to verify accuracy -- each is a checkable claim):');
    gt.keyFacts.forEach((f, i) => parts.push(`  ${i + 1}. ${f}`));
  }
  return parts.join('\n') + '\n';
}

function formatEvidence(steps) {
  if (!steps || steps.length === 0) return '';

  return steps.map((step, i) => {
    const parts = [`Step ${i + 1}: [${step.type || 'tool'}] ${step.name || ''}`];

    if (step.input) {
      const inputStr = typeof step.input === 'string' ? step.input : JSON.stringify(step.input);
      parts.push(`  Query: ${inputStr.slice(0, 300)}`);
    }

    if (step.result) {
      const resultText = Array.isArray(step.result)
        ? step.result.map(r => r.text || JSON.stringify(r.json || r)).join('\n')
        : JSON.stringify(step.result);
      parts.push(`  Result: ${resultText.slice(0, 600)}`);
    }

    if (step.resultSet?.data) {
      const cols = step.resultSet.resultSetMetaData?.rowType?.map(c => c.name) || [];
      const rows = step.resultSet.data.slice(0, 5);
      parts.push(`  Data: [${cols.join(', ')}]`);
      rows.forEach(r => parts.push(`    ${r.join(' | ')}`));
      if (step.resultSet.data.length > 5) parts.push(`    ... (${step.resultSet.data.length} total rows)`);
    }

    if (step.tableData?.data) {
      const cols = step.tableData.resultSetMetaData?.rowType?.map(c => c.name) || [];
      const rows = step.tableData.data.slice(0, 5);
      parts.push(`  Data: [${cols.join(', ')}]`);
      rows.forEach(r => parts.push(`    ${r.join(' | ')}`));
    }

    return parts.join('\n');
  }).join('\n\n').slice(0, 4000);
}

function parseEvalResult(text) {
  const jsonMatch = text.match(/\{[\s\S]*\}/);
  if (!jsonMatch) throw new Error('No JSON found in evaluation response');

  const result = JSON.parse(jsonMatch[0]);

  return {
    snowflake: {
      accuracy: clamp(result.A?.accuracy || 0),
      groundedness: clamp(result.A?.groundedness || 0),
      relevance: clamp(result.A?.relevance || 0),
      actionability: clamp(result.A?.actionability || 0),
      visual_richness: clamp(result.A?.visual_richness || 0),
      notes: result.A?.notes || '',
    },
    databricks: {
      accuracy: clamp(result.B?.accuracy || 0),
      groundedness: clamp(result.B?.groundedness || 0),
      relevance: clamp(result.B?.relevance || 0),
      actionability: clamp(result.B?.actionability || 0),
      visual_richness: clamp(result.B?.visual_richness || 0),
      notes: result.B?.notes || '',
    },
  };
}

function clamp(n) {
  return Math.max(1, Math.min(10, Math.round(n)));
}
