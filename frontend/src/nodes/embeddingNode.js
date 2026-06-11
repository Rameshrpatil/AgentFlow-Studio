import React, { useState } from 'react';
import { BaseNode } from './BaseNode';
import { useStore } from '../store';

export const EmbeddingNode = ({ id, data }) => {
  const updateNodeField = useStore((state) => state.updateNodeField);
  const [model, setModel] = useState(data?.model || 'text-embedding-ada-002');

  const handleModelChange = (e) => {
    setModel(e.target.value);
    updateNodeField(id, 'model', e.target.value);
  };

  return (
    <BaseNode
      id={id}
      title="Embedding"
      inputs={[{ id: 'data' }]}
      outputs={[{ id: 'vector' }]}
    >
      <div className="node-field">
        <label>
          Model:
          <select value={model} onChange={handleModelChange}>
            <option value="text-embedding-ada-002">text-embedding-ada-002</option>
            <option value="text-embedding-3-small">text-embedding-3-small</option>
            <option value="text-embedding-3-large">text-embedding-3-large</option>
            <option value="custom-cnn">Custom CNN</option>
          </select>
        </label>
      </div>
    </BaseNode>
  );
};
