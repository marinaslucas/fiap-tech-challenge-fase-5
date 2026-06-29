from app.schemas import Countermeasure, Threat


class CountermeasureAgent:
    def run(self, threats: list[Threat]) -> list[Countermeasure]:
        countermeasures: list[Countermeasure] = []

        for threat in threats:
            countermeasures.append(
                Countermeasure(
                    threat_id=threat.id,
                    recommendation=self._recommend(threat),
                    priority="High" if threat.severity == "High" else "Medium",
                )
            )

        return countermeasures

    def _recommend(self, threat: Threat) -> str:
        recommendations = {
            "Spoofing": (
                "Validate authentication boundaries, enforce strong identity checks, "
                "and confirm token validation for issuer, audience, and expiration."
            ),
            "Tampering": (
                "Confirm integrity controls such as signed requests, immutable logs, "
                "least-privilege writes, and protected configuration changes."
            ),
            "Repudiation": (
                "Define audit logging requirements with correlation IDs, immutable "
                "storage, retention, and ownership for investigation workflows."
            ),
            "Information Disclosure": (
                "Validate encryption, access policies, network exposure, secret "
                "handling, and error-message hygiene for the affected component."
            ),
            "Denial of Service": (
                "Confirm throttling, WAF or edge protections, autoscaling limits, "
                "timeouts, circuit breakers, monitoring, and alerting."
            ),
            "Elevation of Privilege": (
                "Review IAM roles, service permissions, admin paths, privilege "
                "separation, and escalation controls."
            ),
        }
        return recommendations.get(
            threat.stride_category,
            "Validate the control with the system owner and define concrete mitigation requirements.",
        )
