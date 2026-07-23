# Datasets

Place YOLO-compatible architecture diagram datasets here.

The repository includes only configuration examples and sample placeholders. Large training datasets should be stored outside git or downloaded by the training notebook.

## Source dataset attribution

The architecture-component dataset used as the starting reference for this project is
[`guillherms/stride-architecture-components-v1`](https://huggingface.co/datasets/guillherms/stride-architecture-components-v1)
on Hugging Face.

It provides annotated AWS and Azure architecture diagrams in YOLO format for
architecture-component detection. ThreatGraph AI uses its own training artifact and
may apply local preprocessing, validation, augmentation, or dataset extensions; this
repository does not redistribute the source dataset files.

Please refer to the source dataset card for its license, provenance, classes, and
usage terms.
