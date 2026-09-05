import { useState, useCallback, useRef } from 'react';
import { streamSnowflakeAgent } from '../services/snowflakeAgent';
import { callDatabricksAgent } from '../services/databricksAgent';
import { createMetricsTracker } from '../utils/metrics';

const INITIAL_STATE = {
  status: 'idle',
  statusMessage: '',
  text: '',
  steps: [],
  tables: [],
  charts: [],
  metrics: { ttft: null, totalLatency: null, isStreaming: false, wordCount: null, visibleSteps: 0 },
  error: null,
};

export function useAgentQuery() {
  const [state, setState] = useState(INITIAL_STATE);
  const trackerRef = useRef(null);
  const textDeltaCountRef = useRef(0);

  const reset = useCallback(() => {
    textDeltaCountRef.current = 0;
    setState(INITIAL_STATE);
  }, []);

  const execute = useCallback(async (query, platform, config) => {
    setState({ ...INITIAL_STATE, status: 'running', statusMessage: 'Connecting...' });
    textDeltaCountRef.current = 0;
    const tracker = createMetricsTracker();
    trackerRef.current = tracker;
    let stepCount = 0;

    const callbacks = {
      onStatus: (msg) => {
        setState(s => ({ ...s, statusMessage: msg }));
      },
      onTextDelta: (text) => {
        tracker.markFirstToken();
        textDeltaCountRef.current++;
        setState(s => ({ ...s, text: s.text + text, metrics: { ...s.metrics, ttft: tracker.getTtft() } }));
      },
      onToolUse: (tool) => {
        stepCount++;
        setState(s => ({
          ...s,
          steps: [...s.steps, { ...tool, phase: 'running', startTime: performance.now() }],
          metrics: { ...s.metrics, visibleSteps: stepCount },
        }));
      },
      onToolResult: (result) => {
        setState(s => ({
          ...s,
          steps: s.steps.map(step =>
            step.id === result.id
              ? { ...step, phase: 'done', result: result.content, resultStatus: result.status, resultSet: result.resultSet, tableData: result.tableData }
              : step
          ),
        }));
      },
      onTable: (table) => {
        setState(s => ({ ...s, tables: [...s.tables, table] }));
      },
      onChart: (chart) => {
        setState(s => ({ ...s, charts: [...s.charts, chart] }));
      },
      onComplete: () => {
        const timing = tracker.finish();
        const isStreaming = textDeltaCountRef.current > 3;

        setState(s => {
          const wordCount = s.text ? s.text.split(/\s+/).filter(Boolean).length : 0;
          return {
            ...s,
            status: 'complete',
            statusMessage: 'Complete',
            metrics: {
              ...s.metrics,
              totalLatency: timing.totalLatency,
              ttft: timing.ttft || s.metrics.ttft,
              isStreaming,
              wordCount,
            },
          };
        });
      },
      onError: (msg) => {
        setState(s => ({ ...s, status: 'error', error: msg, statusMessage: 'Error' }));
      },
    };

    try {
      if (platform === 'snowflake') {
        await streamSnowflakeAgent({
          accountUrl: config.snowflakeAccountUrl,
          agentPath: config.snowflakeAgentPath,
          pat: config.snowflakePat,
          query,
          callbacks,
        });
        if (trackerRef.current === tracker) {
          const timing = tracker.finish();
          setState(s => s.status === 'running' ? {
            ...s,
            status: 'complete',
            statusMessage: 'Complete',
            metrics: {
              ...s.metrics,
              totalLatency: timing.totalLatency,
              isStreaming: textDeltaCountRef.current > 3,
              wordCount: s.text ? s.text.split(/\s+/).filter(Boolean).length : 0,
            },
          } : s);
        }
      } else {
        await callDatabricksAgent({
          endpoint: config.databricksEndpoint,
          pat: config.databricksPat,
          query,
          callbacks,
        });
      }
    } catch (err) {
      setState(s => ({ ...s, status: 'error', error: err.message, statusMessage: 'Error' }));
    }
  }, []);

  return { ...state, execute, reset };
}
