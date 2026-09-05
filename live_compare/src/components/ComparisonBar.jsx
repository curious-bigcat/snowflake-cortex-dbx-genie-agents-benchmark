import React from 'react';
import { formatMs } from '../utils/metrics';

function ComparisonRow({ label, sfValue, dbxValue, sfFormatted, dbxFormatted, lowerIsBetter = true }) {
  if (sfValue === null && dbxValue === null) return null;
  const sfNum = typeof sfValue === 'number' ? sfValue : 0;
  const dbxNum = typeof dbxValue === 'number' ? dbxValue : 0;
  const sfWins = lowerIsBetter ? sfNum < dbxNum : sfNum > dbxNum;
  const dbxWins = lowerIsBetter ? dbxNum < sfNum : dbxNum > sfNum;
  const ratio = sfNum && dbxNum ? (lowerIsBetter ? (dbxNum / sfNum) : (sfNum / dbxNum)).toFixed(1) : null;

  return (
    <div className="grid grid-cols-[1fr_100px_1fr] items-center gap-2 py-1.5">
      <div className={`text-right text-sm font-mono ${sfWins ? 'text-sf-blue font-semibold' : 'text-gray-400'}`}>
        {sfFormatted || '--'}
      </div>
      <div className="text-center">
        <span className="text-xs text-gray-500 uppercase font-medium">{label}</span>
        {ratio && sfNum > 0 && dbxNum > 0 && (
          <div className={`text-xs font-semibold ${sfWins ? 'text-sf-blue' : dbxWins ? 'text-dbx-red' : 'text-gray-500'}`}>
            {sfWins ? `\u2190 ${ratio}x faster` : dbxWins ? `${ratio}x faster \u2192` : 'tie'}
          </div>
        )}
      </div>
      <div className={`text-left text-sm font-mono ${dbxWins ? 'text-dbx-red font-semibold' : 'text-gray-400'}`}>
        {dbxFormatted || '--'}
      </div>
    </div>
  );
}

function BoolRow({ label, sfValue, dbxValue }) {
  return (
    <div className="grid grid-cols-[1fr_100px_1fr] items-center gap-2 py-1.5">
      <div className={`text-right text-sm font-mono ${sfValue ? 'text-green-400' : 'text-yellow-500'}`}>
        {sfValue ? 'Progressive' : 'Blocking'}
      </div>
      <div className="text-center">
        <span className="text-xs text-gray-500 uppercase font-medium">{label}</span>
      </div>
      <div className={`text-left text-sm font-mono ${dbxValue ? 'text-green-400' : 'text-yellow-500'}`}>
        {dbxValue ? 'Progressive' : 'Blocking'}
      </div>
    </div>
  );
}

export default function ComparisonBar({ sfMetrics, dbxMetrics }) {
  if (!sfMetrics && !dbxMetrics) return null;
  const sf = sfMetrics || {};
  const dbx = dbxMetrics || {};

  return (
    <div className="bg-surface rounded-xl border border-gray-700/60 px-6 py-3">
      <div className="grid grid-cols-[1fr_100px_1fr] items-center gap-2 pb-2 border-b border-gray-700/40 mb-1">
        <div className="text-right text-xs font-semibold text-sf-blue uppercase">Cortex</div>
        <div className="text-center text-xs font-semibold text-gray-500 uppercase">UX Metric</div>
        <div className="text-left text-xs font-semibold text-dbx-red uppercase">Genie</div>
      </div>
      <ComparisonRow label="TTFT" sfValue={sf.ttft} dbxValue={dbx.ttft} sfFormatted={formatMs(sf.ttft)} dbxFormatted={formatMs(dbx.ttft)} />
      <ComparisonRow label="Response Time" sfValue={sf.totalLatency} dbxValue={dbx.totalLatency} sfFormatted={formatMs(sf.totalLatency)} dbxFormatted={formatMs(dbx.totalLatency)} />
      <BoolRow label="Delivery" sfValue={sf.isStreaming} dbxValue={dbx.isStreaming} />
      <ComparisonRow label="Transparency" sfValue={sf.visibleSteps} dbxValue={dbx.visibleSteps} sfFormatted={sf.visibleSteps != null ? `${sf.visibleSteps} steps` : '--'} dbxFormatted={dbx.visibleSteps != null ? `${dbx.visibleSteps} steps` : '--'} lowerIsBetter={false} />
    </div>
  );
}
