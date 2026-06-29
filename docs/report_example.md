# Report Example

## Executive Summary

The analyzed architecture exposes an internet-facing API layer and downstream data services. The main risks are potential denial of service, weak authentication assumptions, and missing validation for data boundary controls.

## Top Findings

| ID | Category | Severity | Confidence |
| --- | --- | --- | --- |
| T001 | Denial of Service | High | Medium |
| T002 | Spoofing | Medium | Medium |
| T003 | Information Disclosure | Medium | Low |

## Recommended Actions

- Confirm WAF and rate limiting configuration.
- Validate authentication and authorization controls on public APIs.
- Review data storage exposure and encryption posture.
- Add observability requirements for auditability and incident response.
