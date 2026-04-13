from dataclasses import dataclass, field
from typing import List, Optional, Set

@dataclass
class RouteModel:
    path: str
    methods: List[str]
    function_name: str
    file_location: str
    # Information populated by the flow tracer
    service_calls: List[str] = field(default_factory=list)
    db_calls: List[str] = field(default_factory=list)

@dataclass
class ModuleNode:
    name: str
    file_path: str
    imports: Set[str] = field(default_factory=set)

@dataclass
class ProjectStructure:
    root_path: str
    python_files: List[str] = field(default_factory=list)
