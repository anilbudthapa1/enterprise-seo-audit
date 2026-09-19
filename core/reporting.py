"""Generate deterministic Markdown/JSON reports from normalized audit evidence."""
from __future__ import annotations
import json
from datetime import datetime, timezone
from pathlib import Path
from core.scoring import scorecard

SEVERITY_ORDER = {"CRITICAL":0,"HIGH":1,"MEDIUM":2,"LOW":3,"INFO":4}

def build_report(task: dict, findings: list[dict]) -> dict:
    scores = scorecard(findings)
    ordered = sorted(findings, key=lambda f:(SEVERITY_ORDER.get(str(f.get("severity","INFO")).upper(),9), str(f.get("domain","")), str(f.get("rule_id",""))))
    counts = {k: sum(1 for f in findings if str(f.get("severity","")).upper()==k and f.get("status") in {"FAIL","WARNING"}) for k in SEVERITY_ORDER}
    blockers = [f for f in ordered if str(f.get("severity","")).upper()=="CRITICAL" and f.get("status")=="FAIL"]
    return {
        "schema_version":"1.0",
        "generated_at":datetime.now(timezone.utc).isoformat(),
        "task_id":task.get("task_id"),
        "target":task.get("target",{}),
        "mode":task.get("mode","AUDIT"),
        "scorecard":scores,
        "finding_counts":counts,
        "critical_blockers":[f.get("finding_id") for f in blockers],
        "findings":ordered,
        "limitations":task.get("limitations",[]),
        "evidence_sources":task.get("evidence_sources",[]),
    }

def to_markdown(report: dict) -> str:
    s=report["scorecard"]["overall"]
    target=report.get("target",{}).get("site","Unknown")
    lines=[
        "# Enterprise SEO Audit Report", "",
        f"**Task:** `{report.get('task_id')}`  ", f"**Target:** {target}  ",
        f"**Generated:** {report.get('generated_at')}  ", "",
        "## Executive Scorecard", "",
        f"**SEO Health Score:** {s['score'] if s['score'] is not None else 'UNSCORED'}/100  ",
        f"**Evidence Coverage:** {round(s['coverage']*100,1)}%  ", f"**Grade:** {s['grade']}  ", "",
        "> This is an operational health score based on measured audit evidence. It is not a Google metric or ranking prediction.", "",
        "### Domain Scores", "", "| Domain | Score | Coverage | Grade |", "|---|---:|---:|---|"
    ]
    for d,v in report["scorecard"]["domains"].items():
        score="UNSCORED" if v["score"] is None else v["score"]
        lines.append(f"| {d} | {score} | {round(v['coverage']*100,1)}% | {v['grade']} |")
    lines += ["", "## Findings", ""]
    for f in report["findings"]:
        lines += [f"### [{f.get('severity','INFO')}] {f.get('rule_id','UNRULED')} — {f.get('name',f.get('finding_id','Finding'))}", "",
                  f"- **Domain:** {f.get('domain','unknown')}", f"- **Status:** {f.get('status','UNKNOWN')}", f"- **Classification:** {f.get('classification','UNKNOWN')}"]
        if f.get("summary"): lines.append(f"- **Summary:** {f['summary']}")
        if f.get("affected_count") is not None: lines.append(f"- **Affected:** {f['affected_count']}")
        if f.get("remediation"): lines.append(f"- **Remediation:** {f['remediation'] if isinstance(f['remediation'],str) else json.dumps(f['remediation'],ensure_ascii=False)}")
        lines.append("")
    if report.get("limitations"):
        lines += ["## Limitations", ""] + [f"- {x}" for x in report["limitations"]] + [""]
    lines += ["## Evidence & Auditability", "", "Findings should be traced to collected evidence. `SKIPPED` and `NOT_AVAILABLE` checks are not treated as PASS.", ""]
    return "\n".join(lines)

def write_reports(task: dict, findings: list[dict], output_dir: str | Path) -> dict:
    out=Path(output_dir); out.mkdir(parents=True,exist_ok=True)
    report=build_report(task,findings)
    json_path=out/"seo-audit-report.json"; md_path=out/"seo-audit-report.md"
    json_path.write_text(json.dumps(report,indent=2,ensure_ascii=False),encoding="utf-8")
    md_path.write_text(to_markdown(report),encoding="utf-8")
    return {"json":str(json_path),"markdown":str(md_path)}
