from app.schemas import Countermeasure, Threat


class CountermeasureAgent:
    def run(self, threats: list[Threat], report_language: str = "en") -> list[Countermeasure]:
        countermeasures: list[Countermeasure] = []

        for threat in threats:
            countermeasures.append(
                Countermeasure(
                    threat_id=threat.id,
                    recommendation=self._recommend(threat, report_language),
                    priority="High" if threat.severity == "High" else "Medium",
                )
            )

        return countermeasures

    def _recommend(self, threat: Threat, report_language: str) -> str:
        recommendations = self._pt_br_recommendations() if report_language == "pt-BR" else self._en_recommendations()
        return recommendations.get(
            threat.stride_category,
            (
                "Validar o controle com o respons\u00e1vel pelo sistema e definir requisitos concretos de mitiga\u00e7\u00e3o."
                if report_language == "pt-BR"
                else "Validate the control with the system owner and define concrete mitigation requirements."
            ),
        )

    def _en_recommendations(self) -> dict[str, str]:
        return {
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

    def _pt_br_recommendations(self) -> dict[str, str]:
        return {
            "Spoofing": (
                "Validar fronteiras de autentica\u00e7\u00e3o, refor\u00e7ar verifica\u00e7\u00f5es de identidade "
                "e confirmar a valida\u00e7\u00e3o de tokens para emissor, audi\u00eancia e expira\u00e7\u00e3o."
            ),
            "Tampering": (
                "Confirmar controles de integridade como requisi\u00e7\u00f5es assinadas, logs imut\u00e1veis, "
                "escrita com menor privil\u00e9gio e prote\u00e7\u00e3o contra altera\u00e7\u00f5es de configura\u00e7\u00e3o."
            ),
            "Repudiation": (
                "Definir requisitos de auditoria com IDs de correla\u00e7\u00e3o, armazenamento imut\u00e1vel, "
                "reten\u00e7\u00e3o e respons\u00e1veis por investiga\u00e7\u00e3o."
            ),
            "Information Disclosure": (
                "Validar criptografia, pol\u00edticas de acesso, exposi\u00e7\u00e3o de rede, tratamento de "
                "segredos e mensagens de erro do componente afetado."
            ),
            "Denial of Service": (
                "Confirmar throttling, WAF ou prote\u00e7\u00f5es de borda, limites de autoscaling, "
                "timeouts, circuit breakers, monitoramento e alertas."
            ),
            "Elevation of Privilege": (
                "Revisar pap\u00e9is IAM, permiss\u00f5es de servi\u00e7o, caminhos administrativos, "
                "segrega\u00e7\u00e3o de privil\u00e9gios e controles de escalonamento."
            ),
        }
