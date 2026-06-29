from app.schemas import ArchitectureComponent, ArchitectureFlow, ArchitectureModel, Detection


INTERNET_FACING_TYPES = {
    "api_gateway",
    "waf",
    "load_balancer",
    "edge_gateway",
    "edge_waf",
    "edge_cdn",
    "edge_ddos_protection",
    "edge_portal",
    "external_entry_point",
    "compute_load_balancer",
    "actor_user",
    "actor_admin",
}

DATA_TYPES = {"database", "cache", "object_storage", "data_database", "data_cache", "data_storage"}
SECURITY_TYPES = {"security_identity_provider", "security_key_management", "obs_audit"}
OBSERVABILITY_TYPES = {"obs_monitoring"}
EXTERNAL_TYPES = {
    "external_backend_service",
    "external_saas_service",
    "external_web_service",
    "communication_service",
}
ACTOR_TYPES = {"actor_user", "actor_admin"}
ENTRYPOINT_TYPES = {
    "api_gateway",
    "waf",
    "load_balancer",
    "edge_gateway",
    "edge_waf",
    "edge_cdn",
    "edge_ddos_protection",
    "edge_portal",
    "external_entry_point",
    "compute_load_balancer",
}
BOUNDARY_TYPES = {
    "boundary_cloud",
    "boundary_region",
    "boundary_resource_group",
    "boundary_vpc_or_vnet",
    "boundary_subnet_public",
    "boundary_subnet_private",
    "boundary_autoscaling_group",
}


class TopologyService:
    def normalize(self, detections: list[Detection]) -> ArchitectureModel:
        components: list[ArchitectureComponent] = []
        trust_boundaries: list[str] = []

        for index, detection in enumerate(detections, start=1):
            component = ArchitectureComponent(
                id=f"component_{index:03d}",
                type=detection.component_type,
                name=self._display_name(detection.component_type),
                zone=self._infer_zone(detection.component_type),
                exposure=self._infer_exposure(detection.component_type),
                confidence=detection.confidence,
                needs_human_validation=True,
            )
            components.append(component)

            if detection.component_type in BOUNDARY_TYPES:
                trust_boundaries.append(component.id)

        return ArchitectureModel(
            components=components,
            flows=self._infer_flows(components),
            trust_boundaries=trust_boundaries,
        )

    def _infer_zone(self, component_type: str) -> str:
        if component_type in {"actor_user", "actor_admin"}:
            return "internet"
        if component_type in INTERNET_FACING_TYPES:
            return "edge"
        if component_type in DATA_TYPES:
            return "data"
        if component_type in SECURITY_TYPES:
            return "security"
        if component_type in OBSERVABILITY_TYPES:
            return "observability"
        if component_type in EXTERNAL_TYPES:
            return "external_services"
        if component_type in BOUNDARY_TYPES:
            return "network_boundary"
        return "application"

    def _infer_exposure(self, component_type: str) -> str:
        if component_type in {"actor_user", "actor_admin", *EXTERNAL_TYPES}:
            return "external"
        if component_type in INTERNET_FACING_TYPES:
            return "internet-facing"
        if component_type == "boundary_subnet_public":
            return "public-network-boundary"
        if component_type in BOUNDARY_TYPES:
            return "network-boundary"
        return "internal"

    def _display_name(self, component_type: str) -> str:
        return component_type.replace("_", " ").title()

    def _infer_flows(self, components: list[ArchitectureComponent]) -> list[ArchitectureFlow]:
        actors = [component for component in components if component.type in ACTOR_TYPES]
        entrypoints = [component for component in components if component.type in ENTRYPOINT_TYPES]

        flows: list[ArchitectureFlow] = []
        for actor in actors:
            for entrypoint in entrypoints:
                flows.append(
                    ArchitectureFlow(
                        source=actor.id,
                        target=entrypoint.id,
                        protocol="HTTPS",
                        confidence="Low",
                    )
                )

        return flows
