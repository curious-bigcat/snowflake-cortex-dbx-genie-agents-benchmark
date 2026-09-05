import React from 'react';

const DIMENSIONS = [
  { key: 'accuracy', label: 'Accuracy', desc: 'Correct numbers, all sub-parts answered' },
  { key: 'groundedness', label: 'Groundedness', desc: 'Claims backed by retrieved data/docs' },
  { key: 'relevance', label: 'Relevance', desc: 'Directly addresses the question' },
  { key: 'actionability', label: 'Actionability', desc: 'Clear conclusions, next steps, structured data' },
  { key: 'visual_richness', label: 'Visual Richness', desc: 'Charts, tables, structured formatting' },
];

function ScoreBar({ score, maxScore = 10, color }) {
  const pct = (score / maxScore) * 100;
  return (
    <div className="flex items-center gap-2">
      <div className="flex-1 h-2 bg-gray-800 rounded-full overflow-hidden">
        <div className="h-full rounded-full transition-all duration-700" style={{ width: `${pct}%`, backgroundColor: color }} />
      </div>
      <span className="text-sm font-mono font-semibold w-6 text-right" style={{ color }}>{score}</span>
    </div>
  );
}

function PlatformScores({ label, scores, color, icon }) {
  if (!scores) return null;
  const total = DIMENSIONS.reduce((sum, d) => sum + (scores[d.key] || 0), 0);
  return (
    <div className="space-y-2">
      <div className="flex items-center justify-between mb-2">
        <div className="flex items-center gap-2">
          <span>{icon}</span>
          <span className="text-sm font-semibold" style={{ color }}>{label}</span>
        </div>
        <span className="text-2xl font-bold font-mono" style={{ color }}>{total}<span className="text-sm text-gray-600">/50</span></span>
      </div>
      <div className="space-y-1.5">
        {DIMENSIONS.map(d => (
          <div key={d.key}>
            <div className="text-xs text-gray-500 mb-0.5">{d.label}</div>
            <ScoreBar score={scores[d.key] || 0} color={color} />
          </div>
        ))}
      </div>
      {scores.notes && (
        <p className="text-sm text-gray-500 italic mt-2 leading-relaxed">{scores.notes}</p>
      )}
    </div>
  );
}

export default function EvalCard({ evalResult, isEvaluating, evalError }) {
  if (!evalResult && !isEvaluating && !evalError) return null;

  return (
    <div className="bg-surface rounded-xl border border-gray-700/60 overflow-hidden">
      <div className="px-4 py-3 border-b border-gray-700/50 flex items-center gap-2">
        <span className="text-base">{'\uD83C\uDFAF'}</span>
        <h3 className="text-base font-semibold text-gray-300">LLM-as-Judge Evaluation</h3>
        <span className="text-xs text-gray-600">(scored against ground truth)</span>
        {isEvaluating && (
          <span className="text-[10px] text-yellow-400 flex items-center gap-1 ml-auto">
            <svg className="animate-spin h-3 w-3" viewBox="0 0 24 24"><circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" /><path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" /></svg>
            Evaluating...
          </span>
        )}
      </div>

      {evalError && (
        <div className="px-4 py-4">
          <div className="bg-red-900/20 border border-red-700/40 rounded-lg p-3 text-red-300 text-sm">
            <div className="font-semibold mb-1">Evaluation Error</div>
            <div className="text-sm text-red-400">{evalError}</div>
          </div>
        </div>
      )}

      {isEvaluating && !evalResult && (
        <div className="px-4 py-6">
          <div className="space-y-2">
            <div className="h-3 bg-gray-800 rounded animate-pulse w-3/4" />
            <div className="h-3 bg-gray-800 rounded animate-pulse w-full" />
            <div className="h-3 bg-gray-800 rounded animate-pulse w-5/6" />
            <div className="h-3 bg-gray-800 rounded animate-pulse w-2/3" />
          </div>
        </div>
      )}

      {evalResult && (
        <div className="px-4 py-4">
          <div className="grid grid-cols-2 gap-6">
            <PlatformScores label="Cortex Agent" scores={evalResult.snowflake} color="#29B5E8" icon={'\u2744'} />
            <PlatformScores label="Databricks Genie" scores={evalResult.databricks} color="#FF3621" icon={'\u25C6'} />
          </div>

          {/* Head-to-head summary */}
          {evalResult.snowflake && evalResult.databricks && (
            <div className="mt-4 pt-3 border-t border-gray-700/40">
              <div className="grid grid-cols-5 gap-2 text-center">
                {DIMENSIONS.map(d => {
                  const sfScore = evalResult.snowflake[d.key] || 0;
                  const dbxScore = evalResult.databricks[d.key] || 0;
                  const winner = sfScore > dbxScore ? 'sf' : dbxScore > sfScore ? 'dbx' : 'tie';
                  return (
                    <div key={d.key}>
                      <div className="text-xs text-gray-500 uppercase mb-1">{d.label.split(' ')[0]}</div>
                      <div className={`text-lg font-bold ${winner === 'sf' ? 'text-sf-blue' : winner === 'dbx' ? 'text-dbx-red' : 'text-gray-400'}`}>
                        {sfScore}:{dbxScore}
                      </div>
                    </div>
                  );
                })}
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
