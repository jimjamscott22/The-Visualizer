from visualizer.models import RouteModel

def generate_sequence_diagram(route: RouteModel) -> str:
    """Generate a Mermaid sequence diagram for a given RouteModel."""
    lines = []
    lines.append("```mermaid")
    lines.append("sequenceDiagram")
    
    # Client requests to API
    method = route.methods[0] if route.methods else "ANY"
    lines.append(f"    Client->>API: {method} {route.path}")
    
    # Deduplicate calls for clean diagram
    service_calls_dedup = list(dict.fromkeys(route.service_calls))
    db_calls_dedup = list(dict.fromkeys(route.db_calls))

    # API to Service
    if service_calls_dedup:
        for s_call in service_calls_dedup:
            lines.append(f"    API->>Service: {s_call}()")
    else:
        # If no explicit service calls, maybe just point directly down flow
        lines.append(f"    API->>Service: {route.function_name}()")

    # Service to DB
    if db_calls_dedup:
        for db_call in db_calls_dedup:
            lines.append(f"    Service->>DB: {db_call}()")
        lines.append("    DB-->>Service: result")
    
    # Return path
    lines.append("    Service-->>API: response")
    lines.append("    API-->>Client: JSON")
    
    lines.append("```")
    return "\n".join(lines)
