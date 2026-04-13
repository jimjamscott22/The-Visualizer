import ast
from typing import List, Optional
from visualizer.models import RouteModel

HTTP_METHODS = {"get", "post", "put", "delete", "patch", "options", "head"}

class RouteVisitor(ast.NodeVisitor):
    def __init__(self, file_location: str):
        self.file_location = file_location
        self.routes: List[RouteModel] = []
        # Current function context
        self.current_function = None

    def visit_FunctionDef(self, node: ast.FunctionDef):
        # Check decorators to see if this is a route
        methods = []
        path = None
        
        for decorator in node.decorator_list:
            if isinstance(decorator, ast.Call):
                # E.g. @app.get('/users')
                if isinstance(decorator.func, ast.Attribute):
                    method_name = decorator.func.attr
                    if method_name in HTTP_METHODS:
                        methods.append(method_name.upper())
                        # Extract the path from args
                        if decorator.args and isinstance(decorator.args[0], ast.Constant):
                            path = decorator.args[0].value
            
        if methods and path is not None:
            route = RouteModel(
                path=path,
                methods=methods,
                function_name=node.name,
                file_location=self.file_location
            )
            self.routes.append(route)
            
        # Continue visiting the function body if we wanted to extract deeper AST nodes, 
        # but for routes we've already done the work here.
        # Flow parser might inherit or run after this.
        self.generic_visit(node)

def detect_routes(source_code: str, file_location: str) -> List[RouteModel]:
    """Parse python source and return a list of detected routes."""
    try:
        tree = ast.parse(source_code)
    except SyntaxError:
        # If the file contains unparseable syntax, skip or raise
        return []

    visitor = RouteVisitor(file_location)
    visitor.visit(tree)
    return visitor.routes
