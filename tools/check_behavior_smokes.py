#!/usr/bin/env python3
"""Validate ADHLBS behavior smoke fixtures."""

from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "tests" / "behavior" / "adhlbs_behavior_smokes.json"
REQUIRED_CLASSES = [
    "Generated artifact edit",
    "Offline-safe UI change",
    "Repo audit for DRY/SSOT",
    "Security-sensitive tool use",
    "Failure / Andon handling",
    "Codex task prompt generation",
]
REQUIRED_FIELDS = {
    "id",
    "class",
    "expected_behavior",
    "pass_criteria",
    "fail_criteria",
    "conditions",
    "patch_implied",
    "missed_directive_diagnosis_if_failed",
}
ALLOWED_EVIDENCE_LEVELS = {"fixture-only", "executed-local", "executed-live-model"}
REQUIRED_CONDITIONS = [
    "no_adhlbs_framing",
    "one_directive_card",
    "one_dispatch_stack",
    "one_normal_prompt_pack",
    "one_strict_prompt_pack",
]


def nonempty_text(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def validate_fixture(path: Path = FIXTURE) -> list[str]:
    errors: list[str] = []
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        return [f"{path}: cannot parse JSON: {exc}"]
    evidence_level = payload.get("evidence_level")
    if evidence_level not in ALLOWED_EVIDENCE_LEVELS:
        errors.append(f"evidence_level must be one of {sorted(ALLOWED_EVIDENCE_LEVELS)}")
    if evidence_level == "fixture-only" and payload.get("model_runs_executed") is not False:
        errors.append("model_runs_executed must be false for fixture-only evidence")
    if evidence_level == "executed-live-model" and payload.get("model_runs_executed") is not True:
        errors.append("executed-live-model evidence requires model_runs_executed=true")
    declared_conditions = payload.get("required_conditions")
    if declared_conditions != REQUIRED_CONDITIONS:
        errors.append(f"required_conditions must be {REQUIRED_CONDITIONS!r}")
    smokes = payload.get("smokes")
    if not isinstance(smokes, list):
        return ["smokes must be a list"]
    seen_ids: set[str] = set()
    seen_classes: set[str] = set()
    for idx, smoke in enumerate(smokes, start=1):
        if not isinstance(smoke, dict):
            errors.append(f"smokes[{idx}] must be an object")
            continue
        missing = REQUIRED_FIELDS - set(smoke)
        if missing:
            errors.append(f"smokes[{idx}] missing field(s): {sorted(missing)}")
        sid = smoke.get("id", "")
        if not nonempty_text(sid):
            errors.append(f"smokes[{idx}] id must be non-empty")
        elif sid in seen_ids:
            errors.append(f"smokes[{idx}] duplicate id {sid!r}")
        seen_ids.add(str(sid))
        klass = smoke.get("class", "")
        if klass not in REQUIRED_CLASSES:
            errors.append(f"smokes[{idx}] unexpected class {klass!r}")
        seen_classes.add(str(klass))
        for field in ["expected_behavior", "patch_implied", "missed_directive_diagnosis_if_failed"]:
            if not nonempty_text(smoke.get(field)):
                errors.append(f"{sid or idx}: {field} must be non-empty text")
        conditions = smoke.get("conditions")
        if not isinstance(conditions, list):
            errors.append(f"{sid or idx}: conditions must be a list")
            conditions = []
        condition_names = [item.get("condition") for item in conditions if isinstance(item, dict)]
        if condition_names != REQUIRED_CONDITIONS:
            errors.append(f"{sid or idx}: expected condition order {REQUIRED_CONDITIONS!r}; got {condition_names!r}")
        for condition_idx, condition in enumerate(conditions, start=1):
            if not isinstance(condition, dict):
                errors.append(f"{sid or idx}: condition {condition_idx} must be an object")
                continue
            for field in ["condition", "surface", "prompt"]:
                if not nonempty_text(condition.get(field)):
                    errors.append(f"{sid or idx}: condition {condition_idx} missing non-empty {field}")
            name = str(condition.get("condition", ""))
            surface = str(condition.get("surface", ""))
            prompt = str(condition.get("prompt", ""))
            if name == "no_adhlbs_framing":
                if surface != "none":
                    errors.append(f"{sid or idx}: no_adhlbs_framing surface must be none")
            elif not any(token in surface + " " + prompt for token in ["STACK-", "PACK-", "CORE-", "SEC-", "AGENT-", "LEAN-", "WEB-"]):
                errors.append(f"{sid or idx}: {name} does not cite an ADHLBS surface")
            if name == "one_normal_prompt_pack" and ":Normal" not in surface:
                errors.append(f"{sid or idx}: normal prompt pack condition must cite :Normal surface")
            if name == "one_strict_prompt_pack" and ":Strict" not in surface:
                errors.append(f"{sid or idx}: strict prompt pack condition must cite :Strict surface")
        for list_field in ["pass_criteria", "fail_criteria"]:
            value = smoke.get(list_field)
            if not isinstance(value, list) or len(value) < 2 or not all(nonempty_text(item) for item in value):
                errors.append(f"{sid or idx}: {list_field} must contain at least two non-empty items")
    missing_classes = set(REQUIRED_CLASSES) - seen_classes
    if missing_classes:
        errors.append(f"missing smoke class(es): {sorted(missing_classes)}")
    return errors


def main() -> int:
    errors = validate_fixture()
    if errors:
        print("BEHAVIOR_SMOKES_INVALID", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    payload = json.loads(FIXTURE.read_text(encoding="utf-8"))
    print(
        "BEHAVIOR_SMOKES_OK "
        f"fixtures={len(payload['smokes'])} "
        f"conditions={len(REQUIRED_CONDITIONS)} "
        "patch_implied=checked "
        f"evidence_level={payload['evidence_level']} "
        f"model_runs_executed={str(payload['model_runs_executed']).lower()}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
