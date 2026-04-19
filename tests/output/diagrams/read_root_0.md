```mermaid.js
sequenceDiagram
    Client->>API: GET /
    API->>Service: get()
    Service-->>API: response
    API-->>Client: JSON
```