from pathlib import Path
from typing import Any

import yaml

from app.schemas import SecurityReference, Threat


DEFAULT_REFERENCE_PATH = Path(__file__).resolve().parents[1] / "data" / "security_references.yaml"


class ReferenceService:
    def __init__(self, reference_path: Path = DEFAULT_REFERENCE_PATH) -> None:
        self.reference_path = reference_path

    def map_threats(self, threats: list[Threat], report_language: str = "en") -> list[SecurityReference]:
        reference_map = self._load_reference_map()
        references: list[SecurityReference] = []
        seen: set[tuple[str, str, str]] = set()

        for threat in threats:
            entry = reference_map.get(threat.stride_category, {})
            for reference_entry in entry.get("references", []):
                reference = self._build_reference(threat.id, reference_entry, report_language)
                key = (reference.threat_id, reference.source, reference.reference_id)
                if key not in seen:
                    references.append(reference)
                    seen.add(key)

            cve_entry = entry.get("cve")
            if cve_entry:
                reference = self._build_reference(threat.id, cve_entry, report_language)
                key = (reference.threat_id, reference.source, reference.reference_id)
                if key not in seen:
                    references.append(reference)
                    seen.add(key)

        return references

    def _load_reference_map(self) -> dict[str, Any]:
        with self.reference_path.open(encoding="utf-8") as reference_file:
            loaded = yaml.safe_load(reference_file) or {}
        return loaded

    def _build_reference(
        self,
        threat_id: str,
        entry: dict[str, Any],
        report_language: str,
    ) -> SecurityReference:
        note = entry.get("note", "")
        if isinstance(note, dict):
            note_text = note.get(report_language) or note.get("en") or ""
        else:
            note_text = str(note)

        return SecurityReference(
            threat_id=threat_id,
            source=entry["source"],
            reference_id=entry["reference_id"],
            title=entry["title"],
            url=entry["url"],
            note=note_text,
        )
