def compare_scope(expected:set[str], observed:set[str]) -> dict:
    extra=sorted(observed-expected)
    missing=sorted(expected-observed)
    return {"deviation":bool(extra), "unexpected":extra, "expected_not_observed":missing}
