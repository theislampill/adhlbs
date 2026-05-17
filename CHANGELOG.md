# Changelog

## Unreleased

Release readiness checklist:

- Run atomics, build, freshness, offline, static browser parity, local Chrome/CDP browser smoke, static accessibility, source freshness, behavior fixture, directive quality, publication gate, audit-link hygiene, and Python compile checks.
- Confirm `docs/index.html` contains a current build manifest generated from atomics and tools.
- Confirm behavior smoke evidence is labeled fixture-only unless live model runs are executed.
- Confirm no GitHub release, tag, Pages setting, deploy, push, or publish action is performed without explicit owner authorization.
- Confirm license status remains clear: no license has been selected, so default copyright applies.

Suggested release title:

```text
ADHLBS audit hardening: provenance, checks, behavior fixtures
```

Draft release notes:

```text
- Add generated artifact build manifest and stricter freshness validation.
- Harden atomic validation for IDs, references, sidecars, schema/UI copy, source metadata, and duplicate IDs.
- Add static UI parity, source freshness, behavior smoke fixture, and directive quality audit checks.
- Add local Chrome/CDP browser smoke, static accessibility smoke, publication gate, and audit-link hygiene checks.
- Add generated common-task launcher and prompt-guidance-is-not-enforcement surface.
- Add completion and release-readiness audit artifacts.
```
