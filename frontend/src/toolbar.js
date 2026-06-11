// toolbar.js

import { DraggableNode } from './draggableNode';

export const PipelineToolbar = () => {

    return (
        <div className="toolbar">
            <div style={{ display: 'flex', flexWrap: 'wrap', gap: '10px' }}>
                <DraggableNode type='customInput' label='Input' />
                <DraggableNode type='llm' label='LLM' />
                <DraggableNode type='customOutput' label='Output' />
                <DraggableNode type='text' label='Text' />
                <DraggableNode type='documentLoader' label='Document Loader' />
                <DraggableNode type='embedding' label='Embedding' />
                <DraggableNode type='vectorDB' label='Vector DB' />
                <DraggableNode type='promptTemplate' label='Prompt Template' />
                <DraggableNode type='api' label='API Request' />
            </div>
        </div>
    );
};
