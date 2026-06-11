import React, { useState, useEffect } from 'react';
import { BaseNode } from './BaseNode';
import { useStore } from '../store';

export const PromptTemplateNode = ({ id, data }) => {
  const updateNodeField = useStore((state) => state.updateNodeField);
  const [template, setTemplate] = useState(data?.template || '');
  const [variables, setVariables] = useState([]);

  useEffect(() => {
    // Extract variables using regex: {{ variableName }}
    const regex = /\{\{\s*([a-zA-Z_$][a-zA-Z0-9_$]*)\s*\}\}/g;
    const matches = [...template.matchAll(regex)];
    const uniqueVars = Array.from(new Set(matches.map(m => m[1])));
    setVariables(uniqueVars);
  }, [template]);

  const handleTemplateChange = (e) => {
    setTemplate(e.target.value);
    updateNodeField(id, 'template', e.target.value);
  };

  const inputs = variables.map(v => ({ id: v }));

  return (
    <BaseNode
      id={id}
      title="Prompt Template"
      inputs={inputs}
      outputs={[{ id: 'prompt' }]}
    >
      <div className="node-field">
        <label>
          Template:
          <textarea 
            value={template} 
            onChange={handleTemplateChange}
            placeholder="E.g. You are a {{ role }}. Answer {{ query }}"
            rows={4}
            style={{ width: '100%', resize: 'vertical' }}
          />
        </label>
      </div>
    </BaseNode>
  );
};
