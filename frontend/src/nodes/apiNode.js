import React, { useState } from 'react';
import { BaseNode } from './BaseNode';
import { useStore } from '../store';

export const ApiNode = ({ id, data }) => {
  const updateNodeField = useStore((state) => state.updateNodeField);
  const [method, setMethod] = useState(data?.method || 'GET');
  const [url, setUrl] = useState(data?.url || '');

  const handleMethodChange = (e) => {
    setMethod(e.target.value);
    updateNodeField(id, 'method', e.target.value);
  };
  const handleUrlChange = (e) => {
    setUrl(e.target.value);
    updateNodeField(id, 'url', e.target.value);
  };

  return (
    <BaseNode
      id={id}
      title="API Request"
      inputs={[{ id: 'payload' }]}
      outputs={[{ id: 'response' }]}
    >
      <div className="node-field">
        <label>
          Method:
          <select value={method} onChange={handleMethodChange}>
            <option value="GET">GET</option>
            <option value="POST">POST</option>
            <option value="PUT">PUT</option>
            <option value="DELETE">DELETE</option>
          </select>
        </label>
      </div>
      <div className="node-field">
        <label>
          URL:
          <input 
            type="text" 
            value={url} 
            onChange={handleUrlChange} 
            placeholder="https://api.example.com/data"
          />
        </label>
      </div>
    </BaseNode>
  );
};
