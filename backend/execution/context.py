class ExecutionContext:
    def __init__(self):
        # Maps node.id to its output value
        self.node_outputs = {}
        # Stores tracing metadata per node
        self.trace = []
        
    def set_output(self, node_id: str, value: any):
        self.node_outputs[node_id] = value

    def get_output(self, node_id: str) -> any:
        return self.node_outputs.get(node_id)
        
    def add_trace(self, node_id: str, status: str, latency_ms: float, output: any = None, error: str = None):
        self.trace.append({
            "node_id": node_id,
            "status": status,
            "latency_ms": latency_ms,
            "output": output,
            "error": error
        })
