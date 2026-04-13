import os
import json
from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles

def create_app(output_dir: str):
    app = FastAPI(title="The-Visualizer UI")

    # Determine paths
    dashboard_dist = Path(__file__).parent.parent / "dashboard" / "dist"
    output_path = Path(output_dir).resolve()

    # Mount API
    @app.get("/api/projects")
    def get_projects():
        """Returns a hierarchical JSON tree of the generated output directory."""
        if not output_path.exists():
            return {}
        
        def scan_dir(directory: Path):
            tree = []
            for item in sorted(directory.iterdir()):
                if item.is_dir():
                    tree.append({"name": item.name, "type": "dir", "children": scan_dir(item)})
                else:
                    tree.append({"name": item.name, "type": "file", "path": str(item.relative_to(output_path))})
            return tree

        return {"name": output_path.name, "type": "dir", "children": scan_dir(output_path)}

    @app.get("/api/file")
    def get_file(path: str):
        """Returns the contents of a requested file from the output directory."""
        target_file = (output_path / path).resolve()
        
        # Security: ensure target_file is within output_path
        if not str(target_file).startswith(str(output_path)):
            raise HTTPException(status_code=403, detail="Access denied")
            
        if not target_file.exists() or not target_file.is_file():
            raise HTTPException(status_code=404, detail="File not found")

        # Just return it as text response for MD, DOT, JSON
        return FileResponse(target_file, media_type="text/plain")

    # Mount static frontend
    if dashboard_dist.exists():
        app.mount("/assets", StaticFiles(directory=dashboard_dist / "assets"), name="assets")
        
        @app.get("/{full_path:path}")
        async def catch_all(full_path: str):
            # Try to return the exact file if it exists, otherwise return index.html for SPA
            file_path = dashboard_dist / full_path
            if file_path.is_file():
                return FileResponse(file_path)
            return FileResponse(dashboard_dist / "index.html")
    else:
        @app.get("/{full_path:path}")
        async def fallback(full_path: str):
            return HTMLResponse(
                content="<h1>Dashboard Build Not Found</h1><p>The dashboard UI has not been built. Please run <code>npm run build</code> in the dashboard directory.</p>",
                status_code=404
            )

    return app
