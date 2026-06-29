SEVERITY_ORDER = {"Low": 1, "Medium": 2, "High": 3, "Critical": 4}


def sort_severity(severity: str) -> int:
    return SEVERITY_ORDER.get(severity, 0)
