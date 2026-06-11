import React, { useState } from 'react';
import { BaseNode } from './BaseNode';
import { useStore } from '../store';

export const DocumentLoaderNode = ({ id, data }) => {
  const updateNodeField = useStore((state) => state.updateNodeField);
  const [fileType, setFileType] = useState(data?.fileType || 'PDF');
  const [fileName, setFileName] = useState('');

  const handleTypeChange = (e) => {
    setFileType(e.target.value);
    updateNodeField(id, 'fileType', e.target.value);
  };

  const handleFileChange = (e) => {
    if (e.target.files && e.target.files[0]) {
      setFileName(e.target.files[0].name);
    }
  };

  return (
    <BaseNode
      id={id}
      title="Document Loader"
      inputs={[]}
      outputs={[{ id: 'document' }]}
    >
      <div className="node-field">
        <label>
          File Type:
          <select value={fileType} onChange={handleTypeChange}>
            <option value="PDF">PDF (.pdf)</option>
            <option value="TXT">Text (.txt)</option>
            <option value="CSV">CSV (.csv)</option>
            <option value="DOCX">Word (.docx)</option>
          </select>
        </label>
      </div>
      <div className="node-field" style={{ marginTop: '5px' }}>
        <label>
          Upload:
          <input 
            type="file" 
            onChange={handleFileChange} 
            style={{ display: 'none' }}
            id={`file-upload-${id}`}
          />
          <label htmlFor={`file-upload-${id}`} className="file-upload-btn">
            {fileName || 'Choose File...'}
          </label>
        </label>
      </div>
    </BaseNode>
  );
};
