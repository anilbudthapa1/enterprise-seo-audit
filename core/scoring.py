"""Deterministic, evidence-aware SEO scoring.

Scores are operational health indicators, not Google ranking predictions.
Unavailable/skipped checks reduce coverage rather than silently improving score.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Iterable

SEVERITY_PENALTY = {"INFO": 0.0, "LOW": 1.0, "MEDIUM": 3.0, "HIGH": 7.0, "CRITICAL": 15.0}
VALID_STATUS = {"PASS", "FAIL", "WARNING", "SKIPPED", "NOT_APPLICABLE", "NOT_AVAILABLE"}
DEFAULT_WEIGHTS = {
    "crawlability": 14,
    "indexability": 16,
    "canonicalization": 10,
    "redirects": 8,
    "sitemap": 5,
    "rendering": 7,
    "architecture": 8,
    "content": 8,
    "structured_data": 5,
    "performance": 7,
    "international": 3,
    "local": 4,
    "authority": 2,
    "analytics": 3,
}

@dataclass(frozen=True)
class ScoreResult:
    score: float | None
    coverage: float
    grade: str
    applicable_weight: float
    measured_weight: float
    penalty: float


def _grade(score: float | None, coverage: float) -> str:
    if score is None: return "UNSCORED"
    if coverage < 0.60: return "PROVISIONAL"
    if score >= 90: return "A"
    if score >= 80: return "B"
    if score >= 70: return "C"
    if score >= 60: return "D"
    return "F"


def calculate(findings: Iterable[dict], weights: dict[str, float] | None = None) -> ScoreResult:
    weights = weights or DEFAULT_WEIGHTS
    findings = list(findings)
    applicable_domains = {f.get("domain") for f in findings if f.get("status") != "NOT_APPLICABLE"}
    applicable_weight = sum(weights.get(d, 1.0) for d in applicable_domains if d)
    measured_domains = {f.get("domain") for f in findings if f.get("status") in {"PASS", "FAIL", "WARNING"}}
    measured_weight = sum(weights.get(d, 1.0) for d in measured_domains if d)
    coverage = measured_weight / applicable_weight if applicable_weight else 0.0
    if not measured_domains:
        return ScoreResult(None, coverage, "UNSCORED", applicable_weight, measured_weight, 0.0)

    # Each domain starts at 100 and findings reduce it. Multiple failures can bottom at zero.
    domain_scores: dict[str, float] = {}
    total_penalty = 0.0
    for domain in measured_domains:
        penalty = 0.0
        for f in findings:
            if f.get("domain") != domain or f.get("status") not in {"FAIL", "WARNING"}: continue
            base = SEVERITY_PENALTY.get(str(f.get("severity", "MEDIUM")).upper(), 3.0)
            if f.get("status") == "WARNING": base *= 0.5
            affected = max(1, int(f.get("affected_count", 1)))
            prevalence_factor = min(2.0, 1.0 + (affected - 1) / 100.0)
            penalty += base * prevalence_factor
        domain_scores[domain] = max(0.0, 100.0 - penalty)
        total_penalty += penalty

    denom = sum(weights.get(d, 1.0) for d in measured_domains)
    score = sum(domain_scores[d] * weights.get(d, 1.0) for d in measured_domains) / denom
    score = round(score, 1)
    return ScoreResult(score, round(coverage, 3), _grade(score, coverage), applicable_weight, measured_weight, round(total_penalty, 2))


def scorecard(findings: Iterable[dict], weights: dict[str, float] | None = None) -> dict:
    findings = list(findings); weights = weights or DEFAULT_WEIGHTS
    overall = calculate(findings, weights)
    domains = {}
    for domain in sorted({f.get("domain") for f in findings if f.get("domain")}):
        subset = [f for f in findings if f.get("domain") == domain]
        r = calculate(subset, {domain: weights.get(domain, 1.0)})
        domains[domain] = {"score": r.score, "coverage": r.coverage, "grade": r.grade}
    return {
        "overall": {"score": overall.score, "coverage": overall.coverage, "grade": overall.grade},
        "domains": domains,
        "disclaimer": "Operational SEO health score based only on measured audit evidence; not a ranking prediction or Google metric."
    }
