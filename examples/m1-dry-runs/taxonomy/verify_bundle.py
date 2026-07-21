#!/usr/bin/env python3
"""Verify the isolated SYNTHETIC-DRY-RUN taxonomy contract bundle.

This checks serialization and integrity only. Passing does not create research
evidence, validate either taxonomy organization, or award a maturity label.
"""

from __future__ import annotations

import hashlib
import json
from collections.abc import Mapping
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker


BUNDLE_ROOT = Path(__file__).resolve().parent
REPO_ROOT = Path(__file__).resolve().parents[3]

SCHEMA_BINDINGS = {
    "indexes/foundational-subjects.json": "schemas/foundational-subject-registry.schema.json",
    "indexes/foundational-studies.json": "schemas/foundational-record-index.schema.json",
    "indexes/research-findings.json": "schemas/foundational-record-index.schema.json",
    "indexes/foundational-study-closeouts.json": "schemas/foundational-record-index.schema.json",
    "records/foundational/studies/study-manifest.json": "schemas/foundational-study-manifest.schema.json",
    "records/foundational/findings/organization-comparison-finding.json": "schemas/research-finding-record.schema.json",
    "records/foundational/findings/boundary-adjudication-disposition.json": "schemas/research-finding-record.schema.json",
    "records/foundational/closeouts/study-closeout.json": "schemas/foundational-study-closeout.schema.json",
}

EXPECTED_RECORD_PATHS = {
    "foundational_study_registry": {
        "records/foundational/studies/study-manifest.json"
    },
    "research_finding_registry": {
        "records/foundational/findings/organization-comparison-finding.json",
        "records/foundational/findings/boundary-adjudication-disposition.json",
    },
    "foundational_study_closeout_registry": {
        "records/foundational/closeouts/study-closeout.json"
    },
}


def reject_duplicates(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=reject_duplicates)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def contained(base: Path, relative: str) -> Path:
    path = (base / relative).resolve()
    path.relative_to(base.resolve())
    return path


def walk_mappings(value: Any):
    if isinstance(value, Mapping):
        yield value
        for child in value.values():
            yield from walk_mappings(child)
    elif isinstance(value, list):
        for child in value:
            yield from walk_mappings(child)


def immutable_identity(reference: Mapping[str, Any]) -> tuple[Any, ...]:
    digest = reference["digest"]
    return (
        reference["artifact_id"],
        reference["artifact_version"],
        reference["schema_id"],
        reference["locator"],
        digest["algorithm"],
        digest["value"],
        digest["scope"],
        reference["media_type"],
    )


def require(condition: bool, message: str, errors: list[str]) -> None:
    if not condition:
        errors.append(message)


def validate_schemas(documents: dict[str, Any], errors: list[str]) -> None:
    for relative, schema_relative in SCHEMA_BINDINGS.items():
        schema = load_json(REPO_ROOT / schema_relative)
        validator = Draft202012Validator(schema, format_checker=FormatChecker())
        for error in validator.iter_errors(documents[relative]):
            location = "/".join(str(part) for part in error.absolute_path) or "<root>"
            errors.append(f"{relative}:{location}: {error.message}")


def validate_recorded_locators(documents: dict[str, Any], errors: list[str]) -> int:
    checked = 0
    for relative, document in documents.items():
        for mapping in walk_mappings(document):
            locator = mapping.get("locator")
            digest = mapping.get("digest")
            if not isinstance(locator, str) or not isinstance(digest, Mapping):
                continue
            if digest.get("status") not in {"RECORDED", "VERIFIED"}:
                continue
            try:
                path = contained(REPO_ROOT, locator)
            except (ValueError, OSError):
                errors.append(f"{relative}: locator escapes repository: {locator}")
                continue
            if not path.is_file():
                errors.append(f"{relative}: recorded locator is missing: {locator}")
                continue
            checked += 1
            require(
                digest.get("algorithm") == "SHA-256",
                f"{relative}: non-SHA-256 recorded digest: {locator}",
                errors,
            )
            require(
                digest.get("scope") == "RAW_FILE_BYTES",
                f"{relative}: non-raw-byte digest scope: {locator}",
                errors,
            )
            require(
                digest.get("value") == sha256(path),
                f"{relative}: digest mismatch: {locator}",
                errors,
            )
    return checked


def validate_isolated_indexes(documents: dict[str, Any], errors: list[str]) -> None:
    index_paths = (
        "indexes/foundational-studies.json",
        "indexes/research-findings.json",
        "indexes/foundational-study-closeouts.json",
    )
    indexed_records: dict[tuple[str, int], tuple[Mapping[str, Any], Mapping[str, Any]]] = {}
    for index_path in index_paths:
        index = documents[index_path]
        registry_type = index["registry_type"]
        actual_paths = {entry["artifact_path"] for entry in index["entries"]}
        require(
            actual_paths == EXPECTED_RECORD_PATHS[registry_type],
            f"{index_path}: isolated index path set is incomplete or excessive",
            errors,
        )
        for entry in index["entries"]:
            try:
                artifact_path = contained(BUNDLE_ROOT, entry["artifact_path"])
            except (ValueError, OSError):
                errors.append(f"{index_path}: artifact path escapes bundle")
                continue
            if not artifact_path.is_file():
                errors.append(f"{index_path}: indexed artifact is missing: {entry['artifact_path']}")
                continue
            record = load_json(artifact_path)
            require(
                entry["artifact_digest"]["value"] == sha256(artifact_path),
                f"{index_path}: indexed raw-byte digest mismatch: {entry['artifact_path']}",
                errors,
            )
            id_field = "study_record_id" if entry["artifact_type"] == "foundational_study_manifest" else "record_id"
            require(record[id_field] == entry["record_id"], f"{index_path}: record ID mismatch", errors)
            require(record["record_version"] == entry["record_version"], f"{index_path}: version mismatch", errors)
            require(record["artifact_type"] == entry["artifact_type"], f"{index_path}: artifact type mismatch", errors)
            indexed_records[(entry["record_id"], entry["record_version"])] = (entry, record)

    study = documents["records/foundational/studies/study-manifest.json"]
    subject_entry = documents["indexes/foundational-subjects.json"]["entries"][0]
    subject = study["subject"]
    for field in (
        "target_type",
        "subject_kind",
        "subject_id",
        "subject_series",
        "subject_version",
        "name",
        "definition",
        "boundary",
    ):
        require(subject[field] == subject_entry[field], f"subject binding mismatch: {field}", errors)
    require(
        immutable_identity(subject["definition_artifact"])
        == immutable_identity(subject_entry["definition_artifact"]),
        "subject definition artifact binding mismatch",
        errors,
    )

    manifest_digest = sha256(BUNDLE_ROOT / "records/foundational/studies/study-manifest.json")
    findings = [
        documents["records/foundational/findings/organization-comparison-finding.json"],
        documents["records/foundational/findings/boundary-adjudication-disposition.json"],
    ]
    analysis_modes = {item["analysis_id"]: item["analysis_mode"] for item in study["analyses"]}
    for finding in findings:
        study_ref = finding["study_reference"]
        require(study_ref["study_id"] == study["study_id"], "finding study ID mismatch", errors)
        require(study_ref["study_record_id"] == study["study_record_id"], "finding study record mismatch", errors)
        require(study_ref["study_record_version"] == study["record_version"], "finding study version mismatch", errors)
        require(study_ref["manifest_artifact"]["digest"]["value"] == manifest_digest, "finding manifest digest mismatch", errors)
        subject_ref = finding["subject_reference"]
        for field in ("target_type", "subject_kind", "subject_id", "subject_series", "subject_version"):
            require(subject_ref[field] == subject[field], f"finding subject mismatch: {field}", errors)
        require(
            immutable_identity(subject_ref["definition_artifact"])
            == immutable_identity(subject["definition_artifact"]),
            "finding subject artifact mismatch",
            errors,
        )
        profile = study["primary_method_profile"]
        profile_ref = finding["primary_method_profile_reference"]
        for field in ("profile_kind", "profile_id", "profile_series", "profile_version"):
            require(profile_ref[field] == profile[field], f"finding profile mismatch: {field}", errors)
        require(
            immutable_identity(profile_ref["profile_artifact"])
            == immutable_identity(profile["profile_definition_artifact"]),
            "finding profile artifact mismatch",
            errors,
        )
        analysis_ref = finding["analysis_reference"]
        require(analysis_modes.get(analysis_ref["analysis_id"]) == analysis_ref["analysis_mode"], "finding analysis binding mismatch", errors)
        maturity = finding["mechanism_maturity_effect"]
        require(maturity["awarded_mechanism_evidence_labels"] == [], "finding awarded a mechanism label", errors)

    closeout = documents["records/foundational/closeouts/study-closeout.json"]
    planned_ids = {item["analysis_id"] for item in study["analyses"]}
    disposition_ids = [item["analysis_id"] for item in closeout["analysis_dispositions"]]
    require(len(disposition_ids) == len(set(disposition_ids)), "closeout reuses an analysis ID", errors)
    require(set(disposition_ids) == planned_ids, "closeout analysis ledger is not set-equal to the frozen plan", errors)
    finding_by_key = {(item["record_id"], item["record_version"]): item for item in findings}
    for disposition in closeout["analysis_dispositions"]:
        key = (disposition["finding_record_id"], disposition["finding_record_version"])
        finding = finding_by_key.get(key)
        require(finding is not None, f"closeout finding is absent: {key}", errors)
        if finding is None:
            continue
        require(finding["record_status"] == "PUBLISHED", f"closeout finding is not PUBLISHED: {key}", errors)
        require(finding["finding_id"] == disposition["finding_id"], f"closeout finding ID mismatch: {key}", errors)
        require(finding["terminal_disposition"] == disposition["terminal_disposition"], f"closeout terminal disposition mismatch: {key}", errors)
        locator_path = contained(REPO_ROOT, disposition["finding_artifact"]["locator"])
        require(disposition["finding_artifact"]["digest"]["value"] == sha256(locator_path), f"closeout finding digest mismatch: {key}", errors)
    require(
        closeout["mechanism_maturity_effect"]["awarded_mechanism_evidence_labels"] == [],
        "closeout awarded a mechanism label",
        errors,
    )


def main() -> int:
    errors: list[str] = []
    documents = {relative: load_json(BUNDLE_ROOT / relative) for relative in SCHEMA_BINDINGS}
    validate_schemas(documents, errors)
    digest_count = validate_recorded_locators(documents, errors)
    validate_isolated_indexes(documents, errors)

    if errors:
        print("SYNTHETIC-DRY-RUN taxonomy bundle: FAILED")
        for error in errors:
            print(f"- {error}")
        return 1

    print("SYNTHETIC-DRY-RUN taxonomy bundle: PASS (NON-EVIDENTIARY)")
    print(f"Schema-backed records validated: {len(SCHEMA_BINDINGS)}")
    print(f"Recorded local artifact digests verified: {digest_count}")
    print("Frozen analyses: 2; published atomic records: 2; closeout ledger: set-equal")
    print("Mechanism evidence labels awarded: 0")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
