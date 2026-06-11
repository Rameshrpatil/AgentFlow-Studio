import React, { useState, useEffect, useRef, useCallback } from 'react';
import { BaseNode } from './BaseNode';
import { useStore } from '../store';

export const TextNode = ({ id, data }) => {
  const updateNodeField = useStore((state) => state.updateNodeField);
  const [currText, setCurrText] = useState(data?.text || '{{input}}');
  const [variables, setVariables] = useState([]);
  const [dimensions, setDimensions] = useState({ width: 250, height: 'auto' });
  const textareaRef = useRef(null);
  const hiddenRef = useRef(null);

  useEffect(() => {
    // Extract variables
    const regex = /\{\{\s*([a-zA-Z_$][a-zA-Z0-9_$]*)\s*\}\}/g;
    const matches = [...currText.matchAll(regex)];
    const uniqueVars = Array.from(new Set(matches.map(m => m[1])));
    setVariables(uniqueVars);
  }, [currText]);

  const handleTextChange = useCallback((e) => {
    setCurrText(e.target.value);
    updateNodeField(id, 'text', e.target.value);

    // Auto resize height
    const textarea = e.target;
    textarea.style.height = 'auto';
    textarea.style.height = `${textarea.scrollHeight}px`;

    // Auto resize width based on content
    if (hiddenRef.current) {
      hiddenRef.current.textContent = e.target.value || ' ';
      const newWidth = Math.max(250, Math.min(hiddenRef.current.scrollWidth + 50, 500));
      setDimensions(prev => ({ ...prev, width: newWidth }));
    }
  }, []);

  const inputs = variables.map(v => ({ id: v }));

  return (
    <BaseNode
      id={id}
      title="Text"
      inputs={inputs}
      outputs={[{ id: 'output' }]}
    >
      {/* Hidden element for measuring text width */}
      <div
        ref={hiddenRef}
        style={{
          position: 'absolute',
          visibility: 'hidden',
          whiteSpace: 'pre',
          fontFamily: 'inherit',
          fontSize: '13px',
          padding: '8px 10px',
        }}
      />
      <div className="node-field" style={{ width: dimensions.width - 50 }}>
        <label>
          Text:
          <textarea 
            ref={textareaRef}
            value={currText} 
            onChange={handleTextChange} 
            style={{ 
              width: '100%', 
              resize: 'none', 
              overflow: 'hidden', 
              minHeight: '40px',
            }}
          />
        </label>
      </div>
    </BaseNode>
  );
};
