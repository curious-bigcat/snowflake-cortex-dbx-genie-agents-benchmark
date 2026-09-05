export function createMetricsTracker() {
  const startTime = performance.now();
  let ttft = null;

  return {
    startTime,
    markFirstToken() {
      if (ttft === null) {
        ttft = performance.now() - startTime;
      }
    },
    finish() {
      return {
        ttft: ttft !== null ? ttft : performance.now() - startTime,
        totalLatency: performance.now() - startTime,
      };
    },
    getTtft() {
      return ttft;
    },
  };
}

export function formatMs(ms) {
  if (ms === null || ms === undefined) return '--';
  if (ms < 1000) return `${Math.round(ms)}ms`;
  if (ms < 60000) return `${(ms / 1000).toFixed(1)}s`;
  return `${(ms / 60000).toFixed(1)}m`;
}

export function formatTokens(count) {
  if (count === null || count === undefined) return '--';
  if (count < 1000) return String(count);
  if (count < 1000000) return `${(count / 1000).toFixed(1)}K`;
  return `${(count / 1000000).toFixed(2)}M`;
}
