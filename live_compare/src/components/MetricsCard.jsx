import React from 'react';
import { formatMs } from '../utils/metrics';

function MetricRow({ label, value, icon }) {
  return (
    <div className="flex items-center justify-between">
      <span className="text-gray-500 text-sm">{icon} {label}</span>
      <span className="text-gray-200 text-sm font-mono font-medium">{value}</span>
    </div>
  );
}

export default function MetricsCard({ metrics }) {
  if (!metrics) return null;
  const m = metrics;

  return (
    <div className="border-t border-gray-700/50 px-4 py-3 space-y-1.5">
      <MetricRow label="Time to First Token" value={formatMs(m.ttft)} icon={'\u26A1'} />
      <MetricRow label="Total Response Time" value={formatMs(m.totalLatency)} icon={'\u23F1'} />
      <MetricRow label="Streaming" value={m.isStreaming ? 'Yes (progressive)' : 'Blocking (full wait)'} icon={m.isStreaming ? '\u2713' : '\u2717'} />
      <MetricRow label="Steps Visible" value={m.visibleSteps !== null ? `${m.visibleSteps} steps` : '--'} icon={'\uD83D\uDD27'} />
    </div>
  );
}
