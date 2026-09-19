from core.scoring import calculate, scorecard
from core.reporting import build_report, to_markdown

def test_perfect_measured_score():
    r=calculate([{"domain":"crawlability","status":"PASS","severity":"INFO"}])
    assert r.score==100.0 and r.coverage==1.0 and r.grade=="A"

def test_critical_failure_reduces_score():
    r=calculate([{"domain":"indexability","status":"FAIL","severity":"CRITICAL","affected_count":100}])
    assert r.score < 100

def test_not_available_not_pass():
    r=calculate([{"domain":"crawlability","status":"NOT_AVAILABLE","severity":"INFO"}])
    assert r.score is None and r.coverage==0.0 and r.grade=="UNSCORED"

def test_report_contains_disclaimer_and_finding():
    task={"task_id":"SEO-2026-000184","target":{"site":"https://example.com"},"mode":"AUDIT"}
    findings=[{"finding_id":"F1","rule_id":"ROBOTS-001","name":"Robots blocked","domain":"crawlability","status":"FAIL","classification":"VERIFICATION","severity":"CRITICAL","affected_count":1}]
    report=build_report(task,findings); md=to_markdown(report)
    assert "SEO Health Score" in md
    assert "not a Google metric or ranking prediction" in md
    assert "ROBOTS-001" in md
    assert report["critical_blockers"]==["F1"]

def test_scorecard_has_domains():
    s=scorecard([{"domain":"performance","status":"PASS","severity":"INFO"}])
    assert "performance" in s["domains"]
