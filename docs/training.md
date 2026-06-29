# Training Workflow

The training path follows the existing Mermaid notebook flow and assumes a YOLO-compatible annotated dataset.

```mermaid
flowchart TD
    A[Start in Google Colab] --> B[Enable GPU]
    B --> C[Install dependencies]
    C --> D[Mount Google Drive]
    D --> E[Download annotated dataset]
    E --> F[Validate YOLO structure]

    F --> G{Dataset valid?}
    G -- No --> H[Fix data.yaml paths]
    H --> F

    G -- Yes --> I[Load base YOLO model]
    I --> J[Train supervised model]
    J --> K[Evaluate metrics]

    K --> L{Result acceptable?}
    L -- No --> M[Adjust parameters]
    M --> J

    L -- Yes --> N[Save best.pt]
    N --> O[Test on architecture image]
    O --> P[Generate bounding boxes]
    P --> Q[Convert detections to JSON]
    Q --> R[Export JSON to backend]
    R --> S[Done]

    subgraph Dataset
        E
        F
        H
    end

    subgraph Training
        I
        J
        K
        M
        N
    end

    subgraph Integration
        O
        P
        Q
        R
    end
```

## Expected Artifact

The notebook should export:

- `models/best.pt`: trained YOLO weights.
- `models/model_metadata.json`: class names, training date, metrics, and dataset version.
- `examples/output/detected_components.json`: detector output sample for backend testing.
