import asyncio
import time
from typing import List, Dict, Any
from execution.context import ExecutionContext
from execution.nodes.strategies import EXECUTORS

class PipelineEngine:
    def __init__(self, nodes: List[Dict[str, Any]], edges: List[Dict[str, Any]]):
        self.nodes = {node['id']: node for node in nodes}
        self.edges = edges
        self.adj_list = {node_id: [] for node_id in self.nodes}
        self.in_degree = {node_id: 0 for node_id in self.nodes}
        
        # Build graph
        for edge in edges:
            source = edge.get('source')
            target = edge.get('target')
            if source in self.adj_list and target in self.adj_list:
                self.adj_list[source].append(target)
                self.in_degree[target] += 1

    def topological_sort_layered(self) -> List[List[str]]:
        # Returns lists of nodes that can be executed in parallel (Kahn's algo)
        layers = []
        zero_in_degree = [node_id for node_id, degree in self.in_degree.items() if degree == 0]
        
        while zero_in_degree:
            layers.append(zero_in_degree)
            next_zero_in_degree = []
            for node_id in zero_in_degree:
                for neighbor in self.adj_list[node_id]:
                    self.in_degree[neighbor] -= 1
                    if self.in_degree[neighbor] == 0:
                        next_zero_in_degree.append(neighbor)
            zero_in_degree = next_zero_in_degree
            
        # Check for cycles (if not all nodes processed)
        processed_count = sum(len(layer) for layer in layers)
        if processed_count != len(self.nodes):
            raise ValueError("Cycle detected in pipeline graph. Cannot execute.")
            
        return layers

    def get_incoming_edges(self, target_id: str) -> List[Dict[str, Any]]:
        return [edge for edge in self.edges if edge.get('target') == target_id]

    async def execute_node(self, node_id: str, context: ExecutionContext):
        node_data = self.nodes[node_id]
        node_type = node_data.get('type')
        executor = EXECUTORS.get(node_type)
        
        start_time = time.perf_counter()
        if not executor:
            context.add_trace(node_id, "ERROR", 0, error=f"No executor found for node type: {node_type}")
            raise ValueError(f"Unknown node type: {node_type}")
            
        try:
            incoming_edges = self.get_incoming_edges(node_id)
            output = await executor.execute(node_data, context, incoming_edges)
            context.set_output(node_id, output)
            latency = (time.perf_counter() - start_time) * 1000
            context.add_trace(node_id, "SUCCESS", latency, output=output)
        except Exception as e:
            latency = (time.perf_counter() - start_time) * 1000
            context.add_trace(node_id, "ERROR", latency, error=str(e))
            raise RuntimeError(f"Node {node_id} failed: {str(e)}")

    async def run(self) -> ExecutionContext:
        context = ExecutionContext()
        layers = self.topological_sort_layered()
        
        for layer in layers:
            # Execute all nodes in this layer concurrently
            tasks = [self.execute_node(node_id, context) for node_id in layer]
            # If one fails, it stops execution
            await asyncio.gather(*tasks)
            
        return context
