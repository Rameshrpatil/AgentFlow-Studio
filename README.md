# VectorShift - Full Stack Pipeline Assessment

This project is a full-stack visual pipeline builder and execution engine, built as part of the VectorShift Technical Assessment. It allows users to visually construct Directed Acyclic Graphs (DAGs) representing AI workflows, configure nodes, and natively execute them against both mock and live LLM APIs.

## 🚀 Key Features Implemented

1. **Node Abstraction (Frontend)**: Reusable `BaseNode` component that wraps all graph nodes, centralizing styling, handle management, and layout logic. Includes 5 custom AI nodes: `DocumentLoaderNode`, `EmbeddingNode`, `VectorDBNode`, `PromptTemplateNode`, and `ApiNode`.
2. **Premium UI/UX**: Dark-mode glassmorphism interface featuring dynamic hover animations, glowing node handles, and unified component styling across the canvas and toolbar.
3. **Dynamic Node Logic**: The `TextNode` and `PromptTemplateNode` auto-resize horizontally and vertically based on input content. They also parse `{{ variables }}` dynamically via regex to instantiate input handles on the fly.
4. **DAG Graph Validation**: The backend implements a classic Depth-First Search (DFS) topological algorithm to detect cycles and validate that the constructed graph is a perfect DAG before execution.
5. **Asynchronous Execution Engine (Backend)**: Natively parses topological layers to concurrently execute independent nodes using `asyncio.gather`.
6. **Strategy Pattern (Backend)**: Nodes dynamically swap between "Mock" implementations and "Live" `google-genai` implementations based on environment variables.

---

## 🛠️ Tech Stack
* **Frontend**: React, React Flow (zustand state management), CSS3
* **Backend**: Python, FastAPI, Uvicorn, Google GenAI SDK (`gemini-2.5-flash`), Pydantic Settings

---

## 💻 Getting Started

### Prerequisites
- Node.js (v18+)
- Python (3.10+)

### 1. Running the Frontend
Navigate to the `frontend` directory:
```bash
cd frontend
npm install  # (Note: zustand v4.x is required for reactflow compatibility)
npm start
```
The application will be available at `http://localhost:3000`.

### 2. Running the Backend
Navigate to the `backend` directory:
```bash
cd backend
pip install -r requirements.txt 
# Or manually: pip install fastapi uvicorn python-multipart python-dotenv pydantic-settings google-genai requests
```

Create a `.env` file in the `backend/` directory:
```env
EXECUTION_MODE="mock"  # Switch to "live" for real API calls
GEMINI_API_KEY=""      # Required if EXECUTION_MODE is "live"
```

Start the Uvicorn server:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```
The backend API will be available at `http://localhost:8000`.

---

## 🧠 Execution Engine Architecture

The backend features a production-grade execution engine designed for scalability and concurrency safety:

1. **Stateless Request Scoping (`ExecutionContext`)**: 
   A unique execution context is instantiated for every `POST /pipelines/execute` request. State (`node_outputs` and `trace` data) is never stored globally, preventing race conditions during concurrent API requests.
2. **Topological Layering & Async Concurrency (`PipelineEngine`)**:
   The engine computes in-degrees to parse the DAG into layered tiers. Nodes on the same topological tier do not depend on each other and are therefore executed concurrently using `await asyncio.gather()`.
3. **Modular Strategy Pattern (`NodeExecutors`)**:
   Every node extends a `NodeExecutor` interface. The `LLMExecutor` dynamically checks `settings.EXECUTION_MODE` to decide whether to simulate a response or execute a live API call to `gemini-2.5-flash` via the official `google-genai` package.
4. **Rich Traceability**:
   Node logic is wrapped in resilient `try/except` blocks. An execution trace is returned containing the exact status, latency (in milliseconds), and text output of every step.

---

## ⚡ How to Use the App

1. Drag nodes from the top toolbar onto the canvas.
2. Connect the nodes by dragging lines between their handles (e.g., Output to Input).
3. Type `{{ my_variable }}` in a Text or Prompt Template node to automatically create new left-side handles for variable injection.
4. Click **Submit Pipeline** to receive an alert validating the number of nodes, edges, and confirming if the graph is a valid DAG.
5. Click **Run Pipeline** to execute the pipeline through the backend engine. You will receive a detailed execution trace showing the path of your data!
