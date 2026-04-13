# 🧠 Project Prompt: FastAPI Codebase Visualizer

You are an expert software engineer and system designer.

Your task is to design and implement a production-quality application called:

## 🚀 Name = The-Visualizer

---

## 🎯 Objective

Build a tool that analyzes a Python FastAPI codebase and generates visual representations of:

1. Project structure
2. Route-to-service flow
3. Module dependencies
4. Request lifecycle diagrams

The tool should help developers quickly understand how a FastAPI project works internally.

---

## 🧩 Core Features

### 1. Codebase Scanner
- Recursively scan a given project directory
- Identify Python modules and folder structure
- Output a structured representation (tree format)

---

### 2. Route Detection (FastAPI-specific)
- Parse files using Python's `ast` module
- Detect FastAPI route decorators:
  - `@app.get`, `@app.post`, etc.
  - `@router.get`, `@router.post`, etc.
- Extract:
  - Route path (e.g., `/users`)
  - HTTP method
  - Function name
  - File location

---

### 3. Dependency Graph
- Analyze import statements across files
- Build a module dependency graph
- Output:
  - adjacency list (JSON)
  - optional Graphviz `.dot` file

---

### 4. Request Flow Mapping (IMPORTANT)
For each detected route:
- Trace function calls inside the route handler
- Identify:
  - service layer calls
  - database interactions (basic detection via naming or imports)
- Build a simplified flow like:

Client → Route → Service → DB → Response

---

### 5. Mermaid Diagram Generator
Generate Mermaid diagrams for:

#### A. Sequence Diagram (per route)
Example:
```mermaid
sequenceDiagram
Client->>API: POST /users
API->>Service: create_user()
Service->>DB: insert()
DB-->>Service: result
Service-->>API: response
API-->>Client: JSON