import typer
import pathlib
import json
from rich.console import Console
from rich import print as rprint
from visualizer.scanner.project_scanner import ProjectScanner
from visualizer.parser.route_detector import detect_routes
from visualizer.parser.dependency_analyzer import analyze_dependencies
from visualizer.parser.flow_tracer import trace_flow
from visualizer.models import ModuleNode
from visualizer.generators.mermaid_gen import generate_sequence_diagram
from visualizer.generators.graph_gen import generate_adjacency_list, generate_dot_file

app = typer.Typer(help="The-Visualizer: A FastAPI codebase analysis tool.")
console = Console()

@app.command()
def analyze(
    path: str = typer.Argument(..., help="Path to the FastAPI project to analyze"),
    output_dir: str = typer.Option("output", "--output", "-o", help="Directory to save the generated diagrams and graphs"),
):
    """
    Analyze a FastAPI codebase and generate visual models for routing, flows, and dependencies.
    """
    target_path = pathlib.Path(path).resolve()
    if not target_path.exists() or not target_path.is_dir():
        console.print(f"[bold red]Error:[/bold red] The path {path} does not exist or is not a directory.")
        raise typer.Exit(code=1)

    out_path = pathlib.Path(output_dir).resolve()
    out_path.mkdir(parents=True, exist_ok=True)

    console.print(f"[bold cyan]Scanning codebase at:[/bold cyan] {target_path}")
    scanner = ProjectScanner(str(target_path))
    project_struct = scanner.scan()
    
    console.print(f"[green]Found {len(project_struct.python_files)} python files.[/green]")

    all_routes = []
    modules = []

    for rel_path in project_struct.python_files:
        full_file_path = target_path / rel_path
        try:
            with open(full_file_path, "r", encoding="utf-8") as f:
                source_code = f.read()
        except Exception as e:
            console.print(f"[yellow]Warning: Could not read {rel_path} - {e}[/yellow]")
            continue
            
        # Dependencies
        imports = analyze_dependencies(source_code)
        mod_name = str(pathlib.Path(rel_path).with_suffix("")).replace("\\", ".").replace("/", ".")
        modules.append(ModuleNode(name=mod_name, file_path=rel_path, imports=imports))
        
        # Routes
        routes = detect_routes(source_code, rel_path)
        for r in routes:
            s_calls, d_calls = trace_flow(source_code, r.function_name)
            r.service_calls = s_calls
            r.db_calls = d_calls
            all_routes.append(r)

    # Output dependencies
    adj_list_str = generate_adjacency_list(modules)
    with open(out_path / "dependencies.json", "w", encoding="utf-8") as f:
        f.write(adj_list_str)
        
    dot_str = generate_dot_file(modules)
    with open(out_path / "dependencies.dot", "w", encoding="utf-8") as f:
        f.write(dot_str)
        
    # Output diagrams
    diagrams_dir = out_path / "diagrams"
    diagrams_dir.mkdir(exist_ok=True)
    for i, r in enumerate(all_routes):
        diagram_md = generate_sequence_diagram(r)
        safe_name = f"{r.function_name}_{i}.md"
        with open(diagrams_dir / safe_name, "w", encoding="utf-8") as f:
            f.write(diagram_md)

    console.print(f"[bold green]Analysis complete.[/bold green]")
    console.print(f"Detected {len(all_routes)} routes. Outputs saved to [bold]{out_path}[/bold]")

if __name__ == "__main__":
    app()
