# Dataset

The detector expects a YOLO-style dataset with architecture component labels.

## Suggested Classes

- `external_user`
- `api_gateway`
- `waf`
- `load_balancer`
- `service`
- `database`
- `cache`
- `object_storage`
- `identity_provider`
- `message_queue`
- `monitoring`
- `network_zone`
- `trust_boundary`

## Directory Layout

```text
dataset/
  images/
    train/
    val/
  labels/
    train/
    val/
  data.yaml
```

Use `datasets/data.yaml.example` as the starting point for training.
