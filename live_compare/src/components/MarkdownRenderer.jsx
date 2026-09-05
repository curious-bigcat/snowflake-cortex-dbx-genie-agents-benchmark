import React from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';

export default function MarkdownRenderer({ content, isStreaming }) {
  return (
    <div className={`markdown-body text-base text-gray-200 leading-relaxed ${isStreaming ? 'typing-cursor' : ''}`}>
      <ReactMarkdown remarkPlugins={[remarkGfm]}>
        {content || ''}
      </ReactMarkdown>
    </div>
  );
}
