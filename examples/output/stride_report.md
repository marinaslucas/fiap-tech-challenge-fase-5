# ThreatGraph AI STRIDE Report

## Architecture Summary

- Components: 2
- Flows: 0
- Trust boundaries: 0

## Threats

### T001 - Denial of Service

- Severity: High
- Confidence: Medium
- Evidence: Detected component type: api_gateway.
- Description: API Gateway appears internet-facing and may be exposed to abusive traffic without rate limiting.

## Vulnerabilities

- T001: Missing or unvalidated rate limiting (Medium)

## Countermeasures

- T001: Validate the control with the system owner and define concrete requirements for throttling, monitoring, and alerting. Priority: High.
