import asyncio
from typing import Any, Dict
from execution.context import ExecutionContext
from execution.nodes.base import NodeExecutor
from config import settings
import re
import requests

# Gemini setup (only imported/used if live)
try:
    from google import genai
    gemini_client = None
    if settings.GEMINI_API_KEY:
        gemini_client = genai.Client(api_key=settings.GEMINI_API_KEY)
except ImportError:
    gemini_client = None
    pass

class InputExecutor(NodeExecutor):
    async def execute(self, node_data: Dict[str, Any], context: ExecutionContext, incoming_edges: list) -> Any:
        # Input nodes just output their configured name or an empty value
        return node_data.get('data', {}).get('inputName', 'default_input')

class OutputExecutor(NodeExecutor):
    async def execute(self, node_data: Dict[str, Any], context: ExecutionContext, incoming_edges: list) -> Any:
        # Collect values from incoming edges
        results = []
        for edge in incoming_edges:
            source_id = edge.get('source')
            results.append(context.get_output(source_id))
        return results[0] if len(results) == 1 else results

class TextExecutor(NodeExecutor):
    async def execute(self, node_data: Dict[str, Any], context: ExecutionContext, incoming_edges: list) -> Any:
        # Pass through the text, optionally replacing variables if they were connected
        text = node_data.get('data', {}).get('text', '')
        # Simple substitution from incoming edges
        for edge in incoming_edges:
            source_id = edge.get('source')
            target_handle = edge.get('targetHandle')
            val = context.get_output(source_id)
            if target_handle and val is not None:
                # Handle ID is like text-1-myvar, so extract 'myvar'
                handle_name = target_handle.split('-')[-1]
                text = text.replace(f"{{{{{handle_name}}}}}", str(val))
                text = text.replace(f"{{{{ {handle_name} }}}}", str(val))
        return text

class DocumentLoaderExecutor(NodeExecutor):
    async def execute(self, node_data: Dict[str, Any], context: ExecutionContext, incoming_edges: list) -> Any:
        doc_type = node_data.get('data', {}).get('fileType', 'PDF')
        return f"[Mocked {doc_type} Content: The quick brown fox jumps over the lazy dog.]"

class EmbeddingExecutor(NodeExecutor):
    async def execute(self, node_data: Dict[str, Any], context: ExecutionContext, incoming_edges: list) -> Any:
        # Takes incoming data and 'embeds' it
        input_data = None
        for edge in incoming_edges:
            input_data = context.get_output(edge.get('source'))
            break
            
        model = node_data.get('data', {}).get('model', 'text-embedding-ada-002')
        if settings.EXECUTION_MODE == "live":
            # Real embedding could go here
            pass
            
        # Mock embedding
        return f"[Vector Embedding from {model} for size {len(str(input_data))}]"

class VectorDBExecutor(NodeExecutor):
    async def execute(self, node_data: Dict[str, Any], context: ExecutionContext, incoming_edges: list) -> Any:
        # Mock retrieval
        collection = node_data.get('data', {}).get('collectionName', 'default_collection')
        return f"[Retrieved relevant chunks from {collection} VectorDB]"

class PromptTemplateExecutor(NodeExecutor):
    async def execute(self, node_data: Dict[str, Any], context: ExecutionContext, incoming_edges: list) -> Any:
        template = node_data.get('data', {}).get('template', '')
        for edge in incoming_edges:
            source_id = edge.get('source')
            target_handle = edge.get('targetHandle')
            val = context.get_output(source_id)
            if target_handle and val is not None:
                handle_name = target_handle.split('-')[-1]
                template = template.replace(f"{{{{{handle_name}}}}}", str(val))
                template = template.replace(f"{{{{ {handle_name} }}}}", str(val))
        return template

class ApiExecutor(NodeExecutor):
    async def execute(self, node_data: Dict[str, Any], context: ExecutionContext, incoming_edges: list) -> Any:
        method = node_data.get('data', {}).get('method', 'GET')
        url = node_data.get('data', {}).get('url', '')
        
        if not url:
            return "[API Error: Missing URL]"

        if settings.EXECUTION_MODE == "live":
            try:
                # Wrap sync request in thread pool or use aiohttp. using requests in asyncio for simplicity here
                response = await asyncio.to_thread(requests.request, method, url, timeout=5)
                return response.text
            except Exception as e:
                return f"[API Request Failed: {str(e)}]"
        else:
            return f"[Mock API {method} Response from {url}]"

class LLMExecutor(NodeExecutor):
    async def execute(self, node_data: Dict[str, Any], context: ExecutionContext, incoming_edges: list) -> Any:
        # Gather prompt from incoming
        prompt = ""
        system = ""
        for edge in incoming_edges:
            source_id = edge.get('source')
            target_handle = edge.get('targetHandle')
            val = context.get_output(source_id)
            if target_handle and target_handle.endswith('-prompt'):
                prompt = str(val)
            elif target_handle and target_handle.endswith('-system'):
                system = str(val)
                
        full_prompt = f"{system}\n\n{prompt}".strip()
        if not full_prompt:
            full_prompt = "Hello!"
            
        if settings.EXECUTION_MODE == "live" and settings.GEMINI_API_KEY and gemini_client:
            try:
                # Async generate using the new SDK syntax
                response = await gemini_client.aio.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=full_prompt
                )
                return response.text
            except Exception as e:
                raise RuntimeError(f"Gemini API Error: {str(e)}")
        else:
            await asyncio.sleep(0.5) # Simulate latency
            return f"[Mock LLM Response]\nI have processed your prompt: {full_prompt[:50]}..."

# Factory to get executors
EXECUTORS = {
    'customInput': InputExecutor(),
    'customOutput': OutputExecutor(),
    'text': TextExecutor(),
    'documentLoader': DocumentLoaderExecutor(),
    'embedding': EmbeddingExecutor(),
    'vectorDB': VectorDBExecutor(),
    'promptTemplate': PromptTemplateExecutor(),
    'api': ApiExecutor(),
    'llm': LLMExecutor()
}
