import React from 'react';
import { useStore } from './store';

export const SubmitButton = () => {
    // We only need nodes and edges for the submission
    const nodes = useStore((state) => state.nodes);
    const edges = useStore((state) => state.edges);

    const handleSubmit = async () => {
        try {
            const formData = new FormData();
            formData.append('pipeline', JSON.stringify({ nodes, edges }));

            const response = await fetch('http://localhost:8000/pipelines/parse', {
                method: 'POST',
                body: formData,
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();
            
            // Show custom alert
            alert(`Pipeline Analysis:
Number of Nodes: ${data.num_nodes}
Number of Edges: ${data.num_edges}
Is DAG: ${data.is_dag ? 'Yes' : 'No'}`);

        } catch (error) {
            console.error('Error submitting pipeline:', error);
            alert('Failed to submit pipeline. Please ensure the backend is running on http://localhost:8000.');
        }
    };

    const handleExecute = async () => {
        try {
            const formData = new FormData();
            formData.append('pipeline', JSON.stringify({ nodes, edges }));

            const response = await fetch('http://localhost:8000/pipelines/execute', {
                method: 'POST',
                body: formData,
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
            }

            const data = await response.json();
            
            // Format execution trace
            const traceText = data.trace.map(t => 
                `[${t.status}] Node ${t.node_id} (${t.latency_ms.toFixed(2)}ms)
Output: ${t.output || t.error}`
            ).join('\n\n');

            alert(`Execution Successful!\n\nTrace:\n${traceText}`);

        } catch (error) {
            console.error('Error executing pipeline:', error);
            alert(`Execution Failed:\n${error.message}`);
        }
    };

    return (
        <div className="submit-container">
            <button className="submit-btn analyze-btn" type="button" onClick={handleSubmit}>
                Submit Pipeline
            </button>
            <button className="submit-btn execute-btn" type="button" onClick={handleExecute}>
                Run Pipeline
            </button>
        </div>
    );
};
