#!/usr/bin/env python3
"""Generate SEO scorecard + Markdown/JSON report.
Usage: python scripts/generate_report.py task.json findings.json --out evidence/SEO-2026-000184/report
"""
import argparse, json
from core.reporting import write_reports

def main():
    p=argparse.ArgumentParser()
    p.add_argument("task")
    p.add_argument("findings")
    p.add_argument("--out",default="report")
    a=p.parse_args()
    with open(a.task,encoding="utf-8") as f: task=json.load(f)
    with open(a.findings,encoding="utf-8") as f: findings=json.load(f)
    if isinstance(findings,dict): findings=findings.get("findings",[])
    paths=write_reports(task,findings,a.out)
    print(json.dumps(paths,indent=2))
if __name__=="__main__": main()
