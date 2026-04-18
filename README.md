# 🧠 The-Visualizer

**The-Visualizer** is a developer tool designed to help Computer Science students and developers understand the mechanics of their Python FastAPI codebases. By parsing the underlying syntax (without executing it)—through Abstract Syntax Trees (AST)—it generates actionable visual representations of a project's internal workings. 

It reveals project structures, route-to-service flows, module dependencies, and request lifecycles.

---

## 🚀 Features

1. **Codebase Scanner**: Recursively scans a target directory for Python modules and avoids virtual environments and cache directories automatically.
2. **FastAPI Route Detection**: Parses FastAPI files using the `ast` module to accurately detect routing decorators (`@app.get`, `@router.post`, etc.).
3. **Module Dependency Graph**: Analyzes Python import statements to stitch together an application-wide module dependency graph. Outputs to JSON and Graphviz `.dot` formats.
4. **Request Flow Mapping**: Traces internal function calls inside detected FastAPI route handlers to identify service-layer implementations and database interactions.
5. **Mermaid Diagram Generator**: Automatically maps the extracted request flow into visually appealing [Mermaid](https://mermaid.js.org/) Sequence Diagrams on a per-route basis.

---

## 📦 Installation

This project is built to leverage modern Python packaging and is fully compatible with [uv](https://docs.astral.sh/uv/) or standard `pip`.

### Prerequisites
- Python 3.9+
- `uv` (Optional, but recommended)

### Option 1: Using `uv` (Recommended)
Clone the repository and sync the dependencies. `uv` will automatically create a `.venv` virtual environment and install the required tools.

```bash
# Sync dependencies
uv sync

# Run the tool
uv run visualizer --help
```

### Option 2: Using standard `pip`
Create a virtual environment manually, activate it, and install the package in editable mode.

```bash
# Create and activate virtual environment
python -m venv venv
# On Windows:
.\venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

# Install the package
pip install -e .

# Run the tool
python -m visualizer --help
```

---

## 💻 Usage

To analyze a FastAPI project codebase, point the CLI to a directory using the `analyze` command. You can optionally specify an output directory with `-o` or `--output`.

```bash
# Using uv:
uv run visualizer analyze /path/to/fastapi_app -o ./analysis_output

# Using pip:
visualizer analyze /path/to/fastapi_app -o ./analysis_output
```

### Try it with the Mock App!
The codebase includes a small mock FastAPI app inside `tests/mock_fastapi_app` to verify the installation works.

```bash
# Run the analyzer on the mock app
uv run visualizer analyze tests/mock_fastapi_app -o tests/output
```

### 🖥️ Launching the Dashboard UI
To interactively explore the dependency graphs and request flows, you can launch the local web Dashboard UI.

```bash
# Using uv:
uv run visualizer ui

# Using pip:
visualizer ui
```

---

## 🔍 Exploring the Output

When you run the tool, it will generate the following artifacts mapped into the output directory you specify:

- `dependencies.json`: An adjacency list mapping every python module to the imports inside it.
- `dependencies.dot`: A Graphviz graph representation of your module dependencies. You can render this using `dot -Tpng dependencies.dot -o graph.png`.
- `diagrams/`: A folder containing Markdown files for each detected route (e.g., `create_user_1.md`). These format the routes as Mermaid Sequence Diagrams. 

> **Tip**: You can view the `.md` diagrams by uploading them to GitHub, opening them in VS Code with a Markdown Preview extension, or pasting their content into the [Mermaid Live Editor](https://mermaid.live/).
