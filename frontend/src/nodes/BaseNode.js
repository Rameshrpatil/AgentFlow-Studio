import React from 'react';
import { Handle, Position } from 'reactflow';
import { useStore } from '../store';

export const BaseNode = ({ id, title, children, inputs = [], outputs = [] }) => {
  const removeNode = useStore(state => state.removeNode);

  return (
    <div className="node-container">
      {/* Input Handles */}
      {inputs.map((input, index) => (
        <Handle
          key={`${id}-${input.id || index}-input`}
          type="target"
          position={Position.Left}
          id={`${id}-${input.id}`}
          style={{
            top: `${((index + 1) * 100) / (inputs.length + 1)}%`,
            ...input.style,
          }}
        />
      ))}

      {/* Node Content */}
      <div className="node-header">
        <span className="node-title">{title}</span>
        <button className="node-close-btn" onClick={() => removeNode(id)} title="Delete Node">×</button>
      </div>
      <div className="node-body">
        {children}
      </div>

      {/* Output Handles */}
      {outputs.map((output, index) => (
        <Handle
          key={`${id}-${output.id || index}-output`}
          type="source"
          position={Position.Right}
          id={`${id}-${output.id}`}
          style={{
            top: `${((index + 1) * 100) / (outputs.length + 1)}%`,
            ...output.style,
          }}
        />
      ))}
    </div>
  );
};
