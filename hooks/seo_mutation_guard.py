from core.risk import Risk, classify

DENIED = {"fake_reviews","cloaking","doorway_pages","hidden_keyword_content","artificial_link_scheme"}

def authorize(change: dict) -> dict:
    operation = change.get("operation","")
    if operation in DENIED:
        return {"decision":"DENY","risk":"CRITICAL","reason":"Manipulative SEO operation prohibited."}
    risk = classify(change.get("resource",""), bool(change.get("production")), int(change.get("scope",1)), bool(change.get("reduces_access")), bool(change.get("changes_indexability")))
    if risk >= Risk.HIGH:
        return {"decision":"REQUIRE_APPROVAL","risk":risk.name}
    return {"decision":"ALLOW","risk":risk.name}
