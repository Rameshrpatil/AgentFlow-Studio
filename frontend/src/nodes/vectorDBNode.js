import React, { useState } from 'react';
import { BaseNode } from './BaseNode';
import { useStore } from '../store';

export const VectorDBNode = ({ id, data }) => {
  const updateNodeField = useStore((state) => state.updateNodeField);
  const [dbType, setDbType] = useState(data?.dbType || 'Pinecone');
  const [collectionName, setCollectionName] = useState(data?.collectionName || '');

  const handleDbTypeChange = (e) => {
    setDbType(e.target.value);
    updateNodeField(id, 'dbType', e.target.value);
  };
  const handleCollectionChange = (e) => {
    setCollectionName(e.target.value);
    updateNodeField(id, 'collectionName', e.target.value);
  };

  return (
    <BaseNode
      id={id}
      title="Vector DB"
      inputs={[{ id: 'document' }, { id: 'embedding' }]}
      outputs={[{ id: 'results' }]}
    >
      <div className="node-field">
        <label>
          Database:
          <select value={dbType} onChange={handleDbTypeChange}>
            <option value="Pinecone">Pinecone</option>
            <option value="Chroma">Chroma DB</option>
            <option value="Weaviate">Weaviate</option>
            <option value="Qdrant">Qdrant</option>
          </select>
        </label>
      </div>
      <div className="node-field">
        <label>
          Collection / Index Name:
          <input 
            type="text" 
            value={collectionName} 
            onChange={handleCollectionChange} 
            placeholder="my-index-name"
          />
        </label>
      </div>
    </BaseNode>
  );
};
