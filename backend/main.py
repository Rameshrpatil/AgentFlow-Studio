from fastapi import FastAPI, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import json
from execution.engine import PipelineEngine

app = FastAPI()

# Add CORS middleware to allow requests from the React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # For development, allow all
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/')
def read_root():
    return {'Ping': 'Pong'}

@app.post('/pipelines/parse')
def parse_pipeline(pipeline: str = Form(...)):
    try:
        pipeline_data = json.loads(pipeline)
        nodes = pipeline_data.get('nodes', [])
        edges = pipeline_data.get('edges', [])

        num_nodes = len(nodes)
        num_edges = len(edges)

        # Build Adjacency List for Cycle Detection
        # nodes may not all be connected, some might just float
        adj_list = {node['id']: [] for node in nodes}
        
        for edge in edges:
            source = edge.get('source')
            target = edge.get('target')
            if source in adj_list and target in adj_list:
                adj_list[source].append(target)

        # Cycle detection using DFS
        # states: 0 = unvisited, 1 = visiting, 2 = visited
        visited = {node['id']: 0 for node in nodes}

        def has_cycle(v):
            if visited[v] == 1:
                return True # Cycle detected
            if visited[v] == 2:
                return False

            visited[v] = 1 # Mark as visiting
            for neighbor in adj_list.get(v, []):
                if has_cycle(neighbor):
                    return True
            
            visited[v] = 2 # Mark as visited
            return False

        is_dag = True
        for node in nodes:
            node_id = node['id']
            if visited[node_id] == 0:
                if has_cycle(node_id):
                    is_dag = False
                    break

        return {
            'num_nodes': num_nodes,
            'num_edges': num_edges,
            'is_dag': is_dag
        }
    except Exception as e:
        return {
            'num_nodes': 0,
            'num_edges': 0,
            'is_dag': False,
            'error': str(e)
        }

@app.post('/pipelines/execute')
async def execute_pipeline(pipeline: str = Form(...)):
    try:
        pipeline_data = json.loads(pipeline)
        nodes = pipeline_data.get('nodes', [])
        edges = pipeline_data.get('edges', [])
        
        # Instantiate execution engine
        engine = PipelineEngine(nodes, edges)
        
        # Run execution context
        context = await engine.run()
        
        return {
            "status": "success",
            "trace": context.trace,
            "final_outputs": context.node_outputs
        }
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except RuntimeError as re:
        raise HTTPException(status_code=500, detail=str(re))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
