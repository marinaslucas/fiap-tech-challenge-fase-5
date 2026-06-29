# Architecture

This diagram mirrors the existing Mermaid project flow and shows the intended MVP pipeline.

```mermaid
flowchart TD
    A[User uploads architecture image] --> B[React and Vite frontend]
    B --> C[FastAPI backend]
    C --> D[Image upload and validation service]

    D --> E[YOLO component detector]
    E --> F[Detected components with confidence]
    F --> G[Architecture normalizer]
    G --> H[Structured architecture JSON]

    H --> I[LangGraph orchestrator]

    I --> J[Topology Agent]
    I --> K[STRIDE Threat Agent]
    I --> L[Vulnerability Mapping Agent]
    I --> M[Countermeasure Agent]
    I --> N[Report Agent]

    J --> O[Components, zones, and flows]
    K --> P[STRIDE threats]
    L --> Q[Probable vulnerabilities]
    M --> R[Recommended countermeasures]

    O --> N
    P --> N
    Q --> N
    R --> N

    N --> S[Threat modeling report]
    S --> T[Markdown]
    S --> U[PDF]
    S --> V[Frontend visualization]

    subgraph Input
        A
        B
        C
        D
    end

    subgraph Supervised Detection
        E
        F
        G
        H
    end

    subgraph Agent Workflow
        I
        J
        K
        L
        M
        N
    end

    subgraph Output
        S
        T
        U
        V
    end
```

## Backend Responsibilities

- Receive and validate uploaded diagrams.
- Run the supervised detector when a model artifact is available.
- Store raw uploads, predictions, and generated reports.
- Normalize detections into a typed architecture representation.
- Run threat modeling agents and expose report endpoints.

## Frontend Responsibilities

- Upload architecture diagrams.
- Display detected components and confidence values.
- Allow human review before analysis.
- Render the generated report, risk matrix, and threat tables.
