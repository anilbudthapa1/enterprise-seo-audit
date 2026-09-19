# Changelog

## 1.1.0 — 2026-09-20
- Added repository-scoped OpenAI Codex skill adapter under `.agents/skills/enterprise-seo-audit/`.
- Added Claude Code skill adapter under `.claude/skills/enterprise-seo-audit/`.
- Added `agents/openai.yaml` interface metadata for Codex/ChatGPT skill surfaces.
- Expanded README with installation, invocation, update and practical audit/implementation examples for both agent environments.
- Kept platform adapters thin so the root `SKILL.md` remains the portable authoritative contract.

## 1.0.0 — 2026-09-20
- Initial enterprise SEO audit skill.
- Evidence-first audit lifecycle and state machine.
- Deterministic guards for robots, indexability, canonicals, redirects, scope and completion.
- Machine-readable policies and schemas.
- SEO-specific adversarial evaluations and tests.
