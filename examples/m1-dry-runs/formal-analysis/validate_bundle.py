#!/usr/bin/env python3
"""Validate the isolated, non-evidentiary FORMAL_ANALYSIS dry-run bundle."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker


BUNDLE = Path(__file__).resolve().parent
ROOT = BUNDLE.parents[2]


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def iter_mappings(value: Any):
    if isinstance(value, dict):
        yield value
        for child in value.values():
            yield from iter_mappings(child)
    elif isinstance(value, list):
        for child in value:
            yield from iter_mappings(child)


def require(condition: bool, message: str, errors: list[str]) -> None:
    if not condition:
        errors.append(message)


def main() -> int:
    errors: list[str] = []
    schema_cases = {
        "indexes/foundational-subjects.example.json": "foundational-subject-registry.schema.json",
        "records/foundational/studies/LCMRP-FSTUDYREC-9902-SYNTHETIC-DRY-RUN-FORMAL-v1.json": "foundational-study-manifest.schema.json",
        "records/foundational/findings/LCMRP-FINDREC-9902-SYNTHETIC-DRY-RUN-SAT-v1.json": "research-finding-record.schema.json",
        "records/foundational/findings/LCMRP-FINDREC-9902-SYNTHETIC-DRY-RUN-COUNTERMODEL-v1.json": "research-finding-record.schema.json",
        "records/foundational/closeouts/LCMRP-FCLOSEREC-9902-SYNTHETIC-DRY-RUN-FORMAL-v1.json": "foundational-study-closeout.schema.json",
        "indexes/foundational-studies.example.json": "foundational-record-index.schema.json",
        "indexes/research-findings.example.json": "foundational-record-index.schema.json",
        "indexes/foundational-study-closeouts.example.json": "foundational-record-index.schema.json",
    }

    documents: dict[str, Any] = {}
    for relative, schema_name in schema_cases.items():
        path = BUNDLE / relative
        instance = load(path)
        documents[relative] = instance
        schema = load(ROOT / "schemas" / schema_name)
        validator = Draft202012Validator(schema, format_checker=FormatChecker())
        for error in validator.iter_errors(instance):
            location = "/".join(str(part) for part in error.absolute_path) or "<root>"
            errors.append(f"{relative}:{location}: {error.message}")

    for path in sorted(BUNDLE.rglob("*.json")):
        document = load(path)
        for mapping in iter_mappings(document):
            locator = mapping.get("locator")
            recorded = mapping.get("digest")
            if not isinstance(locator, str) or not isinstance(recorded, dict):
                continue
            if recorded.get("status") not in {"RECORDED", "VERIFIED"}:
                continue
            target = ROOT / locator
            require(target.is_file(), f"{path.relative_to(BUNDLE)}: missing locator {locator}", errors)
            if target.is_file():
                require(
                    recorded.get("value") == digest(target),
                    f"{path.relative_to(BUNDLE)}: digest mismatch for {locator}",
                    errors,
                )

    for index_name in (
        "indexes/foundational-studies.example.json",
        "indexes/research-findings.example.json",
        "indexes/foundational-study-closeouts.example.json",
    ):
        index = documents[index_name]
        for entry in index["entries"]:
            target = BUNDLE / entry["artifact_path"]
            require(target.is_file(), f"{index_name}: missing {entry['artifact_path']}", errors)
            if target.is_file():
                require(
                    entry["artifact_digest"]["value"] == digest(target),
                    f"{index_name}: digest mismatch for {entry['artifact_path']}",
                    errors,
                )
                artifact = load(target)
                record_id_field = (
                    "study_record_id"
                    if entry["artifact_type"] == "foundational_study_manifest"
                    else "record_id"
                )
                require(
                    artifact.get(record_id_field) == entry["record_id"]
                    and artifact.get("record_version") == entry["record_version"]
                    and artifact.get("artifact_type") == entry["artifact_type"],
                    f"{index_name}: identity mismatch for {entry['artifact_path']}",
                    errors,
                )

    subject_registry = documents["indexes/foundational-subjects.example.json"]
    manifest = documents[
        "records/foundational/studies/LCMRP-FSTUDYREC-9902-SYNTHETIC-DRY-RUN-FORMAL-v1.json"
    ]
    findings = [
        documents[
            "records/foundational/findings/LCMRP-FINDREC-9902-SYNTHETIC-DRY-RUN-SAT-v1.json"
        ],
        documents[
            "records/foundational/findings/LCMRP-FINDREC-9902-SYNTHETIC-DRY-RUN-COUNTERMODEL-v1.json"
        ],
    ]
    closeout = documents[
        "records/foundational/closeouts/LCMRP-FCLOSEREC-9902-SYNTHETIC-DRY-RUN-FORMAL-v1.json"
    ]
    registered_subject = subject_registry["entries"][0]
    for field in (
        "target_type",
        "subject_kind",
        "subject_id",
        "subject_series",
        "subject_version",
        "name",
        "definition",
        "boundary",
        "definition_artifact",
    ):
        require(
            manifest["subject"][field] == registered_subject[field],
            f"manifest subject binding mismatch: {field}",
            errors,
        )

    manifest_digest = digest(
        BUNDLE
        / "records/foundational/studies/LCMRP-FSTUDYREC-9902-SYNTHETIC-DRY-RUN-FORMAL-v1.json"
    )
    planned = {item["analysis_id"]: item["analysis_mode"] for item in manifest["analyses"]}
    expected_subject_reference = {
        key: manifest["subject"][key]
        for key in (
            "target_type",
            "subject_kind",
            "subject_id",
            "subject_series",
            "subject_version",
            "definition_artifact",
        )
    }
    profile = manifest["primary_method_profile"]
    expected_profile_reference = {
        "profile_kind": profile["profile_kind"],
        "profile_id": profile["profile_id"],
        "profile_series": profile["profile_series"],
        "profile_version": profile["profile_version"],
        "profile_artifact": profile["profile_definition_artifact"],
    }
    for finding in findings:
        require(finding["record_status"] == "PUBLISHED", "finding is not PUBLISHED", errors)
        require(
            finding["study_reference"]["manifest_artifact"]["digest"]["value"]
            == manifest_digest,
            f"finding {finding['record_id']} does not bind exact manifest bytes",
            errors,
        )
        analysis = finding["analysis_reference"]
        require(
            planned.get(analysis["analysis_id"]) == analysis["analysis_mode"],
            f"finding {finding['record_id']} analysis binding mismatch",
            errors,
        )
        require(
            finding["subject_reference"] == expected_subject_reference,
            f"finding {finding['record_id']} subject binding mismatch",
            errors,
        )
        require(
            finding["primary_method_profile_reference"] == expected_profile_reference,
            f"finding {finding['record_id']} profile binding mismatch",
            errors,
        )
        require(
            finding["mechanism_maturity_effect"]["awarded_mechanism_evidence_labels"] == [],
            f"finding {finding['record_id']} awards a mechanism label",
            errors,
        )

    ledger = closeout["analysis_dispositions"]
    require(
        set(planned) == {row["analysis_id"] for row in ledger},
        "closeout ledger is not set-equal to planned analyses",
        errors,
    )
    require(
        len(ledger) == len({row["analysis_id"] for row in ledger}),
        "closeout ledger has duplicate analysis IDs",
        errors,
    )
    require(
        closeout["study_reference"]["study_id"] == manifest["study_id"]
        and closeout["study_reference"]["study_record_id"] == manifest["study_record_id"]
        and closeout["study_reference"]["study_record_version"] == manifest["record_version"]
        and closeout["study_reference"]["manifest_artifact"]["digest"]["value"]
        == manifest_digest,
        "closeout does not bind the exact frozen manifest",
        errors,
    )
    require(
        closeout["mechanism_maturity_effect"]["awarded_mechanism_evidence_labels"] == [],
        "closeout awards a mechanism label",
        errors,
    )
    finding_by_record = {item["record_id"]: item for item in findings}
    for row in ledger:
        finding = finding_by_record.get(row["finding_record_id"])
        require(finding is not None, f"closeout finding missing: {row['finding_record_id']}", errors)
        if finding is not None:
            require(
                row["finding_id"] == finding["finding_id"]
                and row["terminal_disposition"] == finding["terminal_disposition"]
                and row["analysis_id"] == finding["analysis_reference"]["analysis_id"],
                f"closeout binding mismatch: {row['analysis_id']}",
                errors,
            )

    satisfiability = load(BUNDLE / "outputs/satisfiability-result.json")
    rows = satisfiability["enumerated_valuations"]
    expected_valuations = {
        (False, False),
        (False, True),
        (True, False),
        (True, True),
    }
    actual_valuations = {(row["A"], row["B"]) for row in rows}
    require(
        len(rows) == 4 and actual_valuations == expected_valuations,
        "satisfiability output does not enumerate the exact four-valuation domain",
        errors,
    )
    require(
        all(row["satisfies_theory"] is row["A"] for row in rows),
        "satisfiability output misapplies the frozen theory {A}",
        errors,
    )
    models = {(row["A"], row["B"]) for row in rows if row["satisfies_theory"]}
    witness = satisfiability["witness"]
    require(
        (witness["A"], witness["B"]) in models and len(models) == 2,
        "satisfiability output lacks the declared witness or exact model count",
        errors,
    )

    entailment = load(BUNDLE / "outputs/entailment-countermodel-result.json")
    entailment_models = {
        (row["A"], row["B"]): (row["PROP-9902-A"], row["PROP-9902-B"])
        for row in entailment["theory_models"]
    }
    require(
        set(entailment_models) == models
        and all(values == valuation for valuation, values in entailment_models.items()),
        "entailment output does not replay proposition truth over the exact theory models",
        errors,
    )
    countermodel = entailment["declared_non_entailment"]["countermodel"]
    require(
        entailment["intended_entailment"]["holds"] is True
        and all(values[0] for values in entailment_models.values()),
        "declared intended entailment is not supported by every retained theory model",
        errors,
    )
    require(
        entailment["declared_non_entailment"]["holds"] is True
        and (countermodel["A"], countermodel["B"]) in models
        and countermodel["B"] is False,
        "declared non-entailment lacks a valid retained countermodel",
        errors,
    )

    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print(
        "SYNTHETIC-DRY-RUN bundle validation passed: "
        "8 schema-backed records/indexes; all recorded local digests; exact subject/study/"
        "finding bindings; complete four-valuation semantic replay; 2/2 set-equal closeout "
        "dispositions; zero mechanism labels."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
