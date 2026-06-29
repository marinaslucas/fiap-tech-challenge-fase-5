# STRIDE Methodology

ThreatGraph AI uses STRIDE as a structured checklist for each component and data flow.

| Category | Security Question | Example Risk |
| --- | --- | --- |
| Spoofing | Can an attacker pretend to be this actor or service? | Missing identity validation on an exposed API. |
| Tampering | Can data or configuration be modified without authorization? | Unsigned messages or mutable object storage. |
| Repudiation | Can actions be denied because audit evidence is missing? | Missing request logging. |
| Information Disclosure | Can sensitive information be exposed? | Public bucket, weak transport protection, verbose errors. |
| Denial of Service | Can availability be degraded? | Public endpoint without throttling or circuit breakers. |
| Elevation of Privilege | Can an actor gain broader permissions? | Overprivileged service role or weak admin boundary. |

## Confidence Rules

- High confidence requires evidence from the diagram or explicit user context.
- Medium confidence means the diagram implies a risk but requires validation.
- Low confidence means the risk is a hypothesis that should be reviewed manually.

Every generated threat should include evidence and validation questions.
