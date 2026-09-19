def can_complete(record: dict) -> tuple[bool, list[str]]:
    errors=[]
    if record.get("state") not in {"VERIFIED"}: errors.append("state_not_verified")
    if record.get("unresolved_blockers"): errors.append("unresolved_blockers")
    if record.get("approval_required") and not record.get("approval_present"): errors.append("missing_approval")
    for name,status in record.get("required_checks",{}).items():
        if status != "PASS": errors.append(f"check_{name}_{status}")
    if not record.get("evidence_persisted"): errors.append("evidence_missing")
    return (not errors, errors)
