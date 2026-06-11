from typing import Any, Dict
from execution.context import ExecutionContext

class NodeExecutor:
    """Base interface for all node executors."""
    
    async def execute(self, node_data: Dict[str, Any], context: ExecutionContext, incoming_edges: list) -> Any:
        """
        Executes the logic for a single node.
        
        :param node_data: The data dictionary representing the node from the frontend.
        :param context: The ExecutionContext for this request.
        :param incoming_edges: List of edges that target this node.
        :return: The output value of this node.
        """
        raise NotImplementedError("Each node must implement the execute method.")
