import React from 'react';
import { formatMs } from '../utils/metrics';

export default function SessionHistory({ history, onExport }) {
  if (!history || history.length === 0) return null;

  return (
    <div className="bg-surface rounded-xl border border-gray-700/60 overflow-hidden">
      <div className="px-4 py-3 border-b border-gray-700/50 flex items-center justify-between">
        <h3 className="text-base font-semibold text-gray-300">Session History</h3>
        <button
          onClick={onExport}
          className="text-sm text-gray-400 hover:text-gray-200 bg-surface-light hover:bg-surface-lighter px-3 py-1 rounded-lg border border-gray-700/50 transition-colors"
        >
          Export JSON
        </button>
      </div>
      <div className="overflow-x-auto">
        <table className="w-full text-sm">
          <thead>
            <tr className="text-gray-500 uppercase text-xs">
              <th className="px-4 py-2 text-left font-semibold">#</th>
              <th className="px-4 py-2 text-left font-semibold">Question</th>
              <th className="px-4 py-2 text-right font-semibold text-sf-blue">SF Latency</th>
              <th className="px-4 py-2 text-right font-semibold text-dbx-red">DBX Latency</th>
              <th className="px-4 py-2 text-right font-semibold">Ratio</th>
              <th className="px-4 py-2 text-center font-semibold">Winner</th>
            </tr>
          </thead>
          <tbody>
            {history.map((entry, i) => {
              const sfLat = entry.sfMetrics?.totalLatency;
              const dbxLat = entry.dbxMetrics?.totalLatency;
              const ratio = sfLat && dbxLat ? (dbxLat / sfLat).toFixed(1) : null;
              const winner = sfLat && dbxLat ? (sfLat < dbxLat ? 'SF' : 'DBX') : '--';

              return (
                <tr key={i} className="border-t border-gray-800/50 hover:bg-surface-light/50 transition-colors">
                  <td className="px-4 py-2 text-gray-500 font-mono">{i + 1}</td>
                  <td className="px-4 py-2 text-gray-300 max-w-[300px] truncate">{entry.query}</td>
                  <td className="px-4 py-2 text-right font-mono text-gray-300">{formatMs(sfLat)}</td>
                  <td className="px-4 py-2 text-right font-mono text-gray-300">{formatMs(dbxLat)}</td>
                  <td className="px-4 py-2 text-right font-mono text-gray-400">{ratio ? `${ratio}x` : '--'}</td>
                  <td className="px-4 py-2 text-center">
                    {winner === 'SF' && <span className="text-sf-blue font-semibold">Cortex</span>}
                    {winner === 'DBX' && <span className="text-dbx-red font-semibold">Genie</span>}
                    {winner === '--' && <span className="text-gray-500">--</span>}
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </div>
  );
}
