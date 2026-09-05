import React, { useState } from 'react';
import { PRESET_QUESTIONS } from '../utils/constants';

export default function QueryInput({ onSubmit, isRunning }) {
  const [query, setQuery] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (query.trim() && !isRunning) {
      onSubmit(query.trim());
    }
  };

  const handlePreset = (q) => {
    setQuery(q.text);
    if (!isRunning) onSubmit(q.text);
  };

  return (
    <div className="space-y-3">
      <form onSubmit={handleSubmit} className="flex gap-2">
        <textarea
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          onKeyDown={(e) => { if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); handleSubmit(e); } }}
          placeholder="Ask both agents the same question..."
          rows={2}
          className="flex-1 bg-surface-light border border-gray-700 rounded-xl px-4 py-3 text-base text-gray-100 placeholder-gray-500 focus:outline-none focus:border-sf-blue/60 focus:ring-1 focus:ring-sf-blue/30 resize-none transition-all"
        />
        <button
          type="submit"
          disabled={isRunning || !query.trim()}
          className="px-6 py-3 bg-sf-blue hover:bg-sf-blue-dark disabled:bg-gray-700 disabled:text-gray-500 text-white font-semibold text-base rounded-xl transition-all self-end"
        >
          {isRunning ? (
            <span className="flex items-center gap-2">
              <svg className="animate-spin h-4 w-4" viewBox="0 0 24 24"><circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" /><path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" /></svg>
              Running
            </span>
          ) : 'Send'}
        </button>
      </form>

      <div className="flex flex-wrap gap-1.5">
        {PRESET_QUESTIONS.map((q) => (
          <button
            key={q.id}
            onClick={() => handlePreset(q)}
            disabled={isRunning}
            className="px-3 py-1.5 bg-surface-light hover:bg-surface-lighter border border-gray-700/50 rounded-lg text-sm text-gray-400 hover:text-gray-200 disabled:opacity-40 transition-all"
            title={q.text}
          >
            <span className="font-semibold text-gray-300">{q.id}</span>{' '}
            <span className="hidden sm:inline">{q.short}</span>
          </button>
        ))}
      </div>
    </div>
  );
}
