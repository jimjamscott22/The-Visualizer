import ast
from typing import List, Tuple

DB_KEYWORDS = {"db", "insert", "commit", "query", "session", "execute", "select"}

class FunctionCallVisitor(ast.NodeVisitor):
    def __init__(self):
        self.service_calls: List[str] = []
        self.db_calls: List[str] = []

    def visit_Call(self, node: ast.Call):
        func_name = None
        
        # Determine the name of the function being called
        if isinstance(node.func, ast.Name):
            func_name = node.func.id
        elif isinstance(node.func, ast.Attribute):
            func_name = node.func.attr
            
        if func_name:
            # Heuristic for DB calls vs Service calls
            lowered = func_name.lower()
            if any(keyword in lowered for keyword in DB_KEYWORDS):
                self.db_calls.append(func_name)
            else:
                self.service_calls.append(func_name)

        self.generic_visit(node)

def trace_calls(node: ast.FunctionDef) -> Tuple[List[str], List[str]]:
    """Take an AST function definition node and return lists of (service_calls, db_calls)."""
    visitor = FunctionCallVisitor()
    visitor.visit(node)
    
    return visitor.service_calls, visitor.db_calls

class RouteFlowTracer(ast.NodeVisitor):
    def __init__(self, target_function_name: str):
        self.target_function_name = target_function_name
        self.service_calls: List[str] = []
        self.db_calls: List[str] = []

    def visit_FunctionDef(self, node: ast.FunctionDef):
        if node.name == self.target_function_name:
            s_calls, d_calls = trace_calls(node)
            self.service_calls.extend(s_calls)
            self.db_calls.extend(d_calls)
        self.generic_visit(node)

def trace_flow(source_code: str, function_name: str) -> Tuple[List[str], List[str]]:
    """Trace the flow inside a specific function."""
    try:
        tree = ast.parse(source_code)
    except Exception:
        return [], []
        
    tracer = RouteFlowTracer(function_name)
    tracer.visit(tree)
    return tracer.service_calls, tracer.db_calls
