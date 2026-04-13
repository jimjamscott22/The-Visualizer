import json
from typing import Dict, List
from visualizer.models import ModuleNode

def generate_adjacency_list(modules: List[ModuleNode]) -> str:
    """Generate a JSON adjacency list for the module dependencies."""
    adj_list = {}
    for mod in modules:
        adj_list[mod.name] = list(mod.imports)
    return json.dumps(adj_list, indent=4)

def generate_dot_file(modules: List[ModuleNode]) -> str:
    """Generate a Graphviz .dot file string for the modules."""
    lines = []
    lines.append("digraph ProjectDependencies {")
    lines.append("    rankdir=LR;")
    lines.append("    node [shape=box, style=filled, fillcolor=lightgrey];")
    
    for mod in modules:
        # Clean module names to avoid syntax errors in dot
        safe_name = mod.name.replace(".", "_").replace("-", "_")
        lines.append(f'    "{safe_name}" [label="{mod.name}"];')
        for imp in mod.imports:
            safe_imp = imp.replace(".", "_").replace("-", "_")
            lines.append(f'    "{safe_name}" -> "{safe_imp}";')
            
    lines.append("}")
    return "\n".join(lines)
