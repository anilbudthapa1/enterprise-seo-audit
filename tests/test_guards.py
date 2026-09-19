from hooks.seo_mutation_guard import authorize
from hooks.completion_guard import can_complete
from hooks.scope_guard import compare_scope

def test_robots_block_all_requires_approval():
    r=authorize({"resource":"robots_txt","production":True,"reduces_access":True})
    assert r["decision"]=="REQUIRE_APPROVAL" and r["risk"]=="CRITICAL"

def test_mass_canonical_requires_approval():
    assert authorize({"resource":"canonical","production":True,"scope":10})["decision"]=="REQUIRE_APPROVAL"

def test_spam_denied():
    assert authorize({"operation":"fake_reviews"})["decision"]=="DENY"

def test_unverified_cannot_complete():
    ok, errors=can_complete({"state":"IMPLEMENTED_NOT_VERIFIED","required_checks":{},"evidence_persisted":True})
    assert not ok and "state_not_verified" in errors

def test_skipped_is_not_pass():
    ok, errors=can_complete({"state":"VERIFIED","required_checks":{"canonical":"SKIPPED"},"evidence_persisted":True})
    assert not ok

def test_scope_deviation():
    r=compare_scope({"frontend/navigation"},{"frontend/navigation","authentication"})
    assert r["deviation"] and "authentication" in r["unexpected"]
