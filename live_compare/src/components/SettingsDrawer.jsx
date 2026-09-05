import React, { useEffect } from 'react';
import { DEFAULT_CONFIG } from '../utils/constants';

export default function SettingsDrawer({ isOpen, onClose, config, setConfig }) {
  useEffect(() => {
    const saved = localStorage.getItem('agentDuelConfig');
    if (saved) {
      try { setConfig(prev => ({ ...prev, ...JSON.parse(saved) })); } catch {}
    }
  }, []);

  const update = (key, value) => {
    setConfig(prev => {
      const next = { ...prev, [key]: value };
      localStorage.setItem('agentDuelConfig', JSON.stringify(next));
      return next;
    });
  };

  if (!isOpen) return null;

  return (
    <>
      <div className="fixed inset-0 bg-black/60 z-40" onClick={onClose} />
      <div className="fixed right-0 top-0 bottom-0 w-[420px] bg-gray-900 border-l border-gray-700 z-50 overflow-y-auto shadow-2xl">
        <div className="p-6">
          <div className="flex items-center justify-between mb-6">
            <h2 className="text-lg font-semibold text-gray-100">Settings</h2>
            <button onClick={onClose} className="text-gray-400 hover:text-gray-200 text-xl">&times;</button>
          </div>

          {/* Snowflake */}
          <div className="mb-6">
            <h3 className="text-sm font-semibold text-sf-blue mb-3 flex items-center gap-2">
              <span className="text-base">{'\u2744'}</span> Snowflake Cortex Agent
            </h3>
            <div className="space-y-3">
              <div>
                <label className="block text-xs text-gray-400 mb-1">Account URL</label>
                <input
                  type="text"
                  value={config.snowflakeAccountUrl}
                  onChange={(e) => update('snowflakeAccountUrl', e.target.value)}
                  placeholder="https://ACCOUNT.snowflakecomputing.com"
                  className="w-full bg-gray-800 border border-gray-700 rounded-lg px-3 py-2 text-sm text-gray-200 placeholder-gray-600 focus:outline-none focus:border-sf-blue/60"
                />
              </div>
              <div>
                <label className="block text-xs text-gray-400 mb-1">Agent Path</label>
                <input
                  type="text"
                  value={config.snowflakeAgentPath}
                  onChange={(e) => update('snowflakeAgentPath', e.target.value)}
                  className="w-full bg-gray-800 border border-gray-700 rounded-lg px-3 py-2 text-sm text-gray-200 font-mono text-[11px] focus:outline-none focus:border-sf-blue/60"
                />
              </div>
              <div>
                <label className="block text-xs text-gray-400 mb-1">PAT (Programmatic Access Token)</label>
                <input
                  type="password"
                  value={config.snowflakePat}
                  onChange={(e) => update('snowflakePat', e.target.value)}
                  placeholder="pat-..."
                  className="w-full bg-gray-800 border border-gray-700 rounded-lg px-3 py-2 text-sm text-gray-200 placeholder-gray-600 focus:outline-none focus:border-sf-blue/60"
                />
              </div>
            </div>
          </div>

          {/* Databricks */}
          <div className="mb-6">
            <h3 className="text-sm font-semibold text-dbx-red mb-3 flex items-center gap-2">
              <span className="text-base">{'\u25C6'}</span> Databricks Genie Agent
            </h3>
            <div className="space-y-3">
              <div>
                <label className="block text-xs text-gray-400 mb-1">Serving Endpoint URL</label>
                <input
                  type="text"
                  value={config.databricksEndpoint}
                  onChange={(e) => update('databricksEndpoint', e.target.value)}
                  placeholder="https://adb-xxx.azuredatabricks.net/serving-endpoints/..."
                  className="w-full bg-gray-800 border border-gray-700 rounded-lg px-3 py-2 text-sm text-gray-200 placeholder-gray-600 focus:outline-none focus:border-dbx-red/60"
                />
              </div>
              <div>
                <label className="block text-xs text-gray-400 mb-1">PAT (Personal Access Token)</label>
                <input
                  type="password"
                  value={config.databricksPat}
                  onChange={(e) => update('databricksPat', e.target.value)}
                  placeholder="dapi..."
                  className="w-full bg-gray-800 border border-gray-700 rounded-lg px-3 py-2 text-sm text-gray-200 placeholder-gray-600 focus:outline-none focus:border-dbx-red/60"
                />
              </div>
            </div>
          </div>

          <div className="border-t border-gray-700 pt-4">
            <p className="text-[11px] text-gray-500 leading-relaxed">
              Credentials are stored in your browser's localStorage and sent only to the proxy server on localhost.
              They are never sent to any third-party service.
            </p>
          </div>
        </div>
      </div>
    </>
  );
}
