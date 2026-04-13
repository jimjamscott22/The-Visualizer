import os
import pathlib
from typing import List
from visualizer.models import ProjectStructure

IGNORE_DIRS = {".git", "venv", ".venv", "__pycache__", "env", ".pytest_cache", ".mypy_cache"}

class ProjectScanner:
    def __init__(self, root_path: str):
        self.root_path = pathlib.Path(root_path).resolve()

    def scan(self) -> ProjectStructure:
        """
        Recursively traverse the directory, skip ignored directories,
        and find all python strings.
        """
        python_files = []
        for dirpath, dirnames, filenames in os.walk(self.root_path):
            # Mutate dirnames in place to skip ignored directories
            dirnames[:] = [d for d in dirnames if d not in IGNORE_DIRS and not d.startswith('.')]
            
            for f in filenames:
                if f.endswith(".py"):
                    full_path = pathlib.Path(dirpath) / f
                    # store relative path as a string
                    rel_path = str(full_path.relative_to(self.root_path))
                    python_files.append(rel_path)
                    
        return ProjectStructure(
            root_path=str(self.root_path),
            python_files=python_files
        )
