```mermaid
sequenceDiagram
    Client->>API: POST /users/
    API->>Service: create_user_service()
    API->>Service: post()
    Service-->>API: response
    API-->>Client: JSON
```