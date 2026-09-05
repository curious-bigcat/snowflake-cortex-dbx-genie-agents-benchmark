import React, { useRef, useEffect, useState } from 'react';
import MarkdownRenderer from './MarkdownRenderer';
import DataTable from './DataTable';
import StepsAccordion from './StepsAccordion';
import MetricsCard from './MetricsCard';

function StatusBadge({ status, message }) {
  const [elapsed, setElapsed] = useState(0);
  const intervalRef = useRef(null);

  useEffect(() => {
    if (status === 'running') {
      setElapsed(0);
      intervalRef.current = setInterval(() => setElapsed(e => e + 1), 1000);
    } else {
      clearInterval(intervalRef.current);
    }
    return () => clearInterval(intervalRef.current);
  }, [status]);

  const colors = {
    idle: 'bg-gray-600',
    running: 'bg-yellow-400 animate-pulse-dot',
    complete: 'bg-green-400',
    error: 'bg-red-400',
  };

  return (
    <div className="flex items-center gap-2 text-sm text-gray-400">
      <span className={`w-2 h-2 rounded-full ${colors[status] || colors.idle}`} />
      <span className="truncate">{message || status}</span>
      {status === 'running' && (
        <span className="font-mono text-gray-500">{elapsed}s</span>
      )}
    </div>
  );
}

function ChartRenderer({ chartSpec }) {
  const containerRef = useRef(null);

  useEffect(() => {
    if (!chartSpec || !containerRef.current) return;
    let view;
    const render = async () => {
      try {
        const vegaEmbed = (await import('vega-embed')).default;
        const spec = typeof chartSpec === 'string' ? JSON.parse(chartSpec) : chartSpec;
        // Override background for dark theme
        spec.background = 'transparent';
        if (!spec.config) spec.config = {};
        spec.config.view = { stroke: 'transparent' };
        spec.config.axis = { domainColor: '#4b5563', gridColor: '#1f2937', tickColor: '#4b5563', labelColor: '#9ca3af', titleColor: '#d1d5db' };
        spec.config.title = { color: '#e5e7eb' };
        spec.config.legend = { labelColor: '#9ca3af', titleColor: '#d1d5db' };
        spec.width = containerRef.current.offsetWidth - 40;
        spec.height = 250;
        spec.autosize = { type: 'fit', contains: 'padding' };

        const result = await vegaEmbed(containerRef.current, spec, {
          actions: false,
          renderer: 'svg',
          theme: undefined,
        });
        view = result.view;
      } catch (err) {
        console.error('Chart render error:', err);
        if (containerRef.current) {
          containerRef.current.innerHTML = `<pre class="text-[11px] text-red-400">${err.message}</pre>`;
        }
      }
    };
    render();
    return () => { if (view) view.finalize(); };
  }, [chartSpec]);

  if (!chartSpec) return null;

  return (
    <div className="my-3 rounded-lg border border-gray-700/40 bg-gray-900/60 overflow-hidden">
      <div ref={containerRef} className="p-3" />
    </div>
  );
}

export default function AgentPanel({ platform, brandColor, brandIcon, brandName, state }) {
  const scrollRef = useRef(null);

  useEffect(() => {
    if (scrollRef.current && state.status === 'running') {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [state.text, state.status, state.tables]);

  return (
    <div className="flex flex-col min-h-0 rounded-xl border border-gray-700/60 bg-surface overflow-hidden">
      {/* Header */}
      <div className="px-4 py-3 border-b border-gray-700/50 flex items-center justify-between" style={{ borderTopColor: brandColor, borderTopWidth: '2px' }}>
        <div className="flex items-center gap-2">
          <span className="text-lg">{brandIcon}</span>
          <span className="font-semibold text-base" style={{ color: brandColor }}>{brandName}</span>
        </div>
        <StatusBadge status={state.status} message={state.statusMessage} />
      </div>

      {/* Response body */}
      <div ref={scrollRef} className="flex-1 overflow-y-auto px-4 py-3 scrollbar-thin min-h-[200px] max-h-[600px]">
        {state.status === 'idle' && (
          <div className="text-gray-600 text-base italic flex items-center justify-center h-full">
            Waiting for query...
          </div>
        )}
        {state.status === 'error' && (
          <div className="bg-red-900/20 border border-red-700/40 rounded-lg p-3 text-red-300 text-base">
            <div className="font-semibold mb-1">Error</div>
            {state.error}
          </div>
        )}
        {state.text && (
          <MarkdownRenderer content={state.text} isStreaming={state.status === 'running'} />
        )}

        {/* Render tables from tool results */}
        {state.tables && state.tables.map((table, i) => (
          <DataTable key={i} resultSet={table.resultSet} title={table.title} />
        ))}

        {/* Render charts */}
        {state.charts && state.charts.map((chart, i) => (
          <ChartRenderer key={i} chartSpec={chart.chartSpec} />
        ))}

        {/* Render inline result sets from analyst tool steps */}
        {state.steps && state.steps.filter(s => s.resultSet?.data?.length || s.tableData?.data?.length).map((step, i) => (
          <DataTable key={`step-${i}`} resultSet={step.resultSet || step.tableData} title={`${step.type === 'genie' ? 'Genie' : 'SQL'} Result: ${step.name || ''}`} />
        ))}

        {state.status === 'running' && !state.text && (
          <div className="space-y-3">
            <div className="h-4 bg-gray-800 rounded animate-pulse w-3/4" />
            <div className="h-4 bg-gray-800 rounded animate-pulse w-full" />
            <div className="h-4 bg-gray-800 rounded animate-pulse w-5/6" />
            <div className="h-4 bg-gray-800 rounded animate-pulse w-2/3" />
          </div>
        )}
      </div>

      {/* Steps */}
      <StepsAccordion steps={state.steps} />

      {/* Metrics */}
      {state.status !== 'idle' && (
        <MetricsCard metrics={state.metrics} accentColor={brandColor} />
      )}
    </div>
  );
}
