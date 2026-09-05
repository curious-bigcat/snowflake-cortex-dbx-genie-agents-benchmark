import React, { useState } from 'react';

const TOOL_ICONS = {
  cortex_analyst_text_to_sql: '\uD83D\uDD0D',
  cortex_search: '\uD83D\uDCC4',
  analyst_sql: '\uD83D\uDD0D',
  genie: '\uD83D\uDCCA',
  knowledge_assistant: '\uD83D\uDCDA',
  function: '\u2699',
  default: '\uD83D\uDD27',
};

function getToolIcon(type) {
  return TOOL_ICONS[type] || TOOL_ICONS.default;
}

function getToolLabel(step) {
  if (step.type === 'cortex_analyst_text_to_sql' || step.type === 'analyst_sql') return 'SQL Query';
  if (step.type === 'cortex_search') return 'Doc Search';
  if (step.type === 'genie') return 'Genie SQL';
  if (step.type === 'knowledge_assistant') return 'Knowledge Asst';
  return step.type || 'Tool';
}

function formatInput(input) {
  if (!input) return '';
  if (typeof input === 'string') return input;
  if (input.query) return input.query;
  if (input.sql) return input.sql;
  return JSON.stringify(input, null, 2);
}

function formatResult(result) {
  if (!result) return '';
  if (Array.isArray(result)) {
    return result.map(r => {
      if (r.type === 'text') return r.text;
      if (r.type === 'json') return JSON.stringify(r.json, null, 2);
      return JSON.stringify(r);
    }).join('\n');
  }
  return JSON.stringify(result, null, 2);
}

export default function StepsAccordion({ steps }) {
  const [expandedIds, setExpandedIds] = useState(new Set());

  if (!steps || steps.length === 0) return null;

  const toggle = (id) => {
    setExpandedIds(prev => {
      const next = new Set(prev);
      next.has(id) ? next.delete(id) : next.add(id);
      return next;
    });
  };

  return (
    <div className="border-t border-gray-700/50">
      <button
        onClick={() => setExpandedIds(prev => prev.size === steps.length ? new Set() : new Set(steps.map(s => s.id)))}
        className="w-full px-4 py-2 text-sm font-medium text-gray-400 hover:text-gray-200 text-left flex items-center gap-2 transition-colors"
      >
        <span className="text-[10px]">{expandedIds.size > 0 ? '\u25BC' : '\u25B6'}</span>
        Tool Steps ({steps.length})
      </button>

      {expandedIds.size > 0 && (
        <div className="px-3 pb-3 space-y-1">
          {steps.map((step, i) => {
            const isOpen = expandedIds.has(step.id);
            return (
              <div key={step.id || i} className="rounded-lg bg-gray-900/60 border border-gray-700/40 overflow-hidden">
                <button
                  onClick={() => toggle(step.id)}
                  className="w-full px-3 py-2 text-sm flex items-center gap-2 hover:bg-gray-800/50 transition-colors"
                >
                  <span>{getToolIcon(step.type)}</span>
                  <span className="font-medium text-gray-300">{getToolLabel(step)}</span>
                  <span className="text-gray-500 truncate flex-1 text-left">{step.name}</span>
                  {step.phase === 'running' && <span className="w-1.5 h-1.5 rounded-full bg-yellow-400 animate-pulse-dot" />}
                  {step.phase === 'done' && (step.resultStatus === 'success' || step.resultStatus === 'sql') && <span className="w-1.5 h-1.5 rounded-full bg-green-400" />}
                  {step.phase === 'done' && step.resultStatus === 'error' && <span className="px-1.5 py-0.5 rounded text-[9px] font-bold bg-red-900/40 text-red-400 border border-red-700/40">FAILED</span>}
                  {step.phase === 'done' && step.resultStatus !== 'success' && step.resultStatus !== 'error' && step.resultStatus !== 'sql' && <span className="w-1.5 h-1.5 rounded-full bg-gray-400" />}
                  <span className="text-[10px]">{isOpen ? '\u25BC' : '\u25B6'}</span>
                </button>
                {isOpen && (
                  <div className="px-3 pb-2 space-y-2 border-t border-gray-700/30">
                    {step.input && (
                      <div className="mt-2">
                        <div className="text-[10px] font-semibold text-gray-500 uppercase mb-1">Input</div>
                        <pre className="text-[11px] text-gray-400 bg-gray-950 rounded p-2 overflow-x-auto whitespace-pre-wrap max-h-32 overflow-y-auto">{formatInput(step.input)}</pre>
                      </div>
                    )}
                    {step.result && (
                      <div>
                        <div className={`text-[10px] font-semibold uppercase mb-1 ${step.resultStatus === 'error' ? 'text-red-400' : 'text-gray-500'}`}>
                          {step.resultStatus === 'error' ? 'Error' : 'Result'}
                        </div>
                        <pre className={`text-[11px] rounded p-2 overflow-x-auto whitespace-pre-wrap max-h-40 overflow-y-auto ${
                          step.resultStatus === 'error' ? 'text-red-300 bg-red-950/40 border border-red-800/30' : 'text-gray-400 bg-gray-950'
                        }`}>{formatResult(step.result)}</pre>
                      </div>
                    )}
                  </div>
                )}
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}
