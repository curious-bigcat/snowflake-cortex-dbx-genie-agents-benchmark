import React, { useState, useCallback, useRef, useEffect } from 'react';
import QueryInput from './components/QueryInput';
import AgentPanel from './components/AgentPanel';
import ComparisonBar from './components/ComparisonBar';
import EvalCard from './components/EvalCard';
import SessionHistory from './components/SessionHistory';
import SettingsDrawer from './components/SettingsDrawer';
import { useAgentQuery } from './hooks/useAgentQuery';
import { evaluateResponses } from './services/evaluator';
import { BRAND, DEFAULT_CONFIG, PRESET_QUESTIONS } from './utils/constants';

export default function App() {
  const [settingsOpen, setSettingsOpen] = useState(false);
  const [config, setConfig] = useState(DEFAULT_CONFIG);
  const [history, setHistory] = useState([]);
  const [evalResult, setEvalResult] = useState(null);
  const [isEvaluating, setIsEvaluating] = useState(false);
  const [evalError, setEvalError] = useState(null);
  const sfAgent = useAgentQuery();
  const dbxAgent = useAgentQuery();
  const currentQueryRef = useRef('');
  const evalTriggeredRef = useRef(false);

  const isRunning = sfAgent.status === 'running' || dbxAgent.status === 'running';

  // Trigger evaluation when all started agents are done
  useEffect(() => {
    const sfStarted = sfAgent.status !== 'idle';
    const dbxStarted = dbxAgent.status !== 'idle';
    const sfDone = !sfStarted || sfAgent.status === 'complete' || sfAgent.status === 'error';
    const dbxDone = !dbxStarted || dbxAgent.status === 'complete' || dbxAgent.status === 'error';
    const anyStarted = sfStarted || dbxStarted;
    const allDone = sfDone && dbxDone;
    const hasResponses = sfAgent.text || dbxAgent.text;

    if (anyStarted && allDone && hasResponses && !evalTriggeredRef.current) {
      evalTriggeredRef.current = true;
      console.log('[App] Both agents done. SF text length:', sfAgent.text?.length, 'DBX text length:', dbxAgent.text?.length);

      // Add to session history
      setHistory(prev => [...prev, {
        query: currentQueryRef.current,
        timestamp: new Date().toISOString(),
        sfMetrics: sfAgent.metrics,
        dbxMetrics: dbxAgent.metrics,
      }]);

      // Run LLM evaluation if Snowflake is configured (uses Cortex REST API)
      if (config.snowflakePat && config.snowflakeAccountUrl) {
        setIsEvaluating(true);
        setEvalError(null);
        // Find ground truth if this is a preset question
        const matchingPreset = PRESET_QUESTIONS.find(q => q.text === currentQueryRef.current);
        evaluateResponses({
          question: currentQueryRef.current,
          sfResponse: sfAgent.text || '(No response)',
          dbxResponse: dbxAgent.text || '(No response)',
          sfSteps: sfAgent.steps || [],
          dbxSteps: dbxAgent.steps || [],
          sfHasCharts: (sfAgent.charts || []).length > 0,
          sfHasTables: (sfAgent.tables || []).length > 0 || (sfAgent.steps || []).some(s => s.resultSet || s.tableData),
          dbxHasCharts: false,
          dbxHasTables: (dbxAgent.steps || []).some(s => s.tableData),
          groundTruth: matchingPreset?.groundTruth || null,
          accountUrl: config.snowflakeAccountUrl,
          pat: config.snowflakePat,
        })
          .then(result => {
            setEvalResult(result);
            setIsEvaluating(false);
          })
          .catch(err => {
            setEvalError(err.message);
            setIsEvaluating(false);
          });
      }
    }
  }, [sfAgent.status, dbxAgent.status, sfAgent.text, dbxAgent.text, config]);

  const handleSubmit = useCallback((query) => {
    if (!config.snowflakePat && !config.databricksPat) {
      setSettingsOpen(true);
      return;
    }

    currentQueryRef.current = query;
    evalTriggeredRef.current = false;
    setEvalResult(null);
    setIsEvaluating(false);
    setEvalError(null);
    sfAgent.reset();
    dbxAgent.reset();

    if (config.snowflakePat && config.snowflakeAccountUrl) {
      sfAgent.execute(query, 'snowflake', config);
    }
    if (config.databricksPat && config.databricksEndpoint) {
      dbxAgent.execute(query, 'databricks', config);
    }
  }, [config, sfAgent, dbxAgent]);

  const handleExport = useCallback(() => {
    const blob = new Blob([JSON.stringify(history, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `agent-duel-session-${new Date().toISOString().slice(0, 10)}.json`;
    a.click();
    URL.revokeObjectURL(url);
  }, [history]);

  const sfConfigured = !!(config.snowflakePat && config.snowflakeAccountUrl);
  const dbxConfigured = !!(config.databricksPat && config.databricksEndpoint);

  return (
    <div className="min-h-screen bg-gray-950">
      {/* Header */}
      <header className="border-b border-gray-800 bg-gray-950/80 backdrop-blur-sm sticky top-0 z-30">
        <div className="max-w-7xl mx-auto px-4 py-3 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <span className="text-2xl">{'\u2694'}</span>
            <div>
              <h1 className="text-base font-bold text-gray-100">Agent Duel</h1>
              <p className="text-[10px] text-gray-500 uppercase tracking-wider">Cortex Agent vs Genie -- Live Comparison</p>
            </div>
          </div>
          <div className="flex items-center gap-3">
            <div className="flex gap-2 text-[10px]">
              <span className={`px-2 py-0.5 rounded-full border ${sfConfigured ? 'border-sf-blue/40 text-sf-blue bg-sf-blue/10' : 'border-gray-700 text-gray-500'}`}>
                {'\u2744'} {sfConfigured ? 'Connected' : 'Not configured'}
              </span>
              <span className={`px-2 py-0.5 rounded-full border ${dbxConfigured ? 'border-dbx-red/40 text-dbx-red bg-dbx-red/10' : 'border-gray-700 text-gray-500'}`}>
                {'\u25C6'} {dbxConfigured ? 'Connected' : 'Not configured'}
              </span>
            </div>
            <button
              onClick={() => setSettingsOpen(true)}
              className="p-2 text-gray-400 hover:text-gray-200 hover:bg-surface-light rounded-lg transition-colors"
              title="Settings"
            >
              <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
                <path strokeLinecap="round" strokeLinejoin="round" d="M9.594 3.94c.09-.542.56-.94 1.11-.94h2.593c.55 0 1.02.398 1.11.94l.213 1.281c.063.374.313.686.645.87.074.04.147.083.22.127.325.196.72.257 1.075.124l1.217-.456a1.125 1.125 0 0 1 1.37.49l1.296 2.247a1.125 1.125 0 0 1-.26 1.431l-1.003.827c-.293.241-.438.613-.43.992a7.723 7.723 0 0 1 0 .255c-.008.378.137.75.43.991l1.004.827c.424.35.534.955.26 1.43l-1.298 2.247a1.125 1.125 0 0 1-1.369.491l-1.217-.456c-.355-.133-.75-.072-1.076.124a6.47 6.47 0 0 1-.22.128c-.331.183-.581.495-.644.869l-.213 1.281c-.09.543-.56.94-1.11.94h-2.594c-.55 0-1.019-.398-1.11-.94l-.213-1.281c-.062-.374-.312-.686-.644-.87a6.52 6.52 0 0 1-.22-.127c-.325-.196-.72-.257-1.076-.124l-1.217.456a1.125 1.125 0 0 1-1.369-.49l-1.297-2.247a1.125 1.125 0 0 1 .26-1.431l1.004-.827c.292-.24.437-.613.43-.991a6.932 6.932 0 0 1 0-.255c.007-.38-.138-.751-.43-.992l-1.004-.827a1.125 1.125 0 0 1-.26-1.43l1.297-2.247a1.125 1.125 0 0 1 1.37-.491l1.216.456c.356.133.751.072 1.076-.124.072-.044.146-.086.22-.128.332-.183.582-.495.644-.869l.214-1.28Z" />
                <path strokeLinecap="round" strokeLinejoin="round" d="M15 12a3 3 0 1 1-6 0 3 3 0 0 1 6 0Z" />
              </svg>
            </button>
          </div>
        </div>
      </header>

      {/* Main content */}
      <main className="max-w-7xl mx-auto px-4 py-6 space-y-6">
        {/* Query input */}
        <QueryInput onSubmit={handleSubmit} isRunning={isRunning} />

        {/* Side-by-side panels */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
          <AgentPanel
            platform="snowflake"
            brandColor={BRAND.snowflake.color}
            brandIcon={BRAND.snowflake.icon}
            brandName={BRAND.snowflake.name}
            state={sfAgent}
          />
          <AgentPanel
            platform="databricks"
            brandColor={BRAND.databricks.color}
            brandIcon={BRAND.databricks.icon}
            brandName={BRAND.databricks.name}
            state={dbxAgent}
          />
        </div>

        {/* Comparison metrics */}
        {(sfAgent.status === 'complete' || dbxAgent.status === 'complete') && (
          <ComparisonBar sfMetrics={sfAgent.metrics} dbxMetrics={dbxAgent.metrics} />
        )}

        {/* LLM Evaluation */}
        <EvalCard evalResult={evalResult} isEvaluating={isEvaluating} evalError={evalError} />

        {/* Session history */}
        <SessionHistory history={history} onExport={handleExport} />
      </main>

      {/* Settings drawer */}
      <SettingsDrawer
        isOpen={settingsOpen}
        onClose={() => setSettingsOpen(false)}
        config={config}
        setConfig={setConfig}
      />
    </div>
  );
}
