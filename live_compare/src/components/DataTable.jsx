import React from 'react';

export default function DataTable({ resultSet, title }) {
  if (!resultSet?.data?.length) return null;

  const columns = resultSet.resultSetMetaData?.rowType || [];
  const rows = resultSet.data;

  return (
    <div className="my-3 rounded-lg border border-gray-700/50 overflow-hidden">
      {title && (
        <div className="px-3 py-1.5 bg-gray-800/60 text-sm font-semibold text-gray-300 border-b border-gray-700/50">
          {title}
        </div>
      )}
      <div className="overflow-x-auto max-h-64 overflow-y-auto scrollbar-thin">
        <table className="w-full text-sm">
          <thead className="sticky top-0">
            <tr>
              {columns.map((col, i) => (
                <th key={i} className="px-3 py-2 text-left font-semibold text-gray-400 bg-gray-800 border-b border-gray-700 whitespace-nowrap">
                  {col.name}
                </th>
              ))}
              {columns.length === 0 && rows[0]?.map((_, i) => (
                <th key={i} className="px-3 py-2 text-left font-semibold text-gray-400 bg-gray-800 border-b border-gray-700">
                  Col {i + 1}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {rows.slice(0, 50).map((row, ri) => (
              <tr key={ri} className="hover:bg-gray-800/40 transition-colors">
                {row.map((cell, ci) => (
                  <td key={ci} className="px-3 py-1.5 text-gray-300 border-b border-gray-800/50 whitespace-nowrap font-mono">
                    {cell === null ? <span className="text-gray-600 italic">NULL</span> : String(cell)}
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
        {rows.length > 50 && (
          <div className="px-3 py-1.5 text-xs text-gray-500 bg-gray-800/40">
            Showing 50 of {rows.length} rows
          </div>
        )}
      </div>
    </div>
  );
}
