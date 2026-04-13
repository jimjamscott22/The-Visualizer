import ast
from typing import Dict, List, Set

class ImportVisitor(ast.NodeVisitor):
    def __init__(self):
        self.imports: Set[str] = set()

    def visit_Import(self, node: ast.Import):
        for alias in node.names:
            self.imports.add(alias.name)
        self.generic_visit(node)

    def visit_ImportFrom(self, node: ast.ImportFrom):
        if node.module:
            self.imports.add(node.module)
        else:
            # Relative import, store just the level or skip for simple static grap
            # Depending on robustness, this can be expanded.
            if node.level and node.level > 0:
                self.imports.add(f"." * node.level)
        self.generic_visit(node)

def analyze_dependencies(source_code: str) -> Set[str]:
    """Parse python source and return a list of imported modules."""
    try:
        tree = ast.parse(source_code)
    except Exception:
        return set()

    visitor = ImportVisitor()
    visitor.visit(tree)
    return visitor.imports
