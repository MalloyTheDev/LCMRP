"""Fail-closed gates for the first two real M1 foundational-study freezes.

These tests verify preregistration identity, immutability, and containment.  They
do not execute either planned analysis, evaluate either subject, or create a
research finding, closeout, mechanism maturity effect, or M1 completion claim.
"""

from __future__ import annotations

import copy
from functools import lru_cache
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
from typing import Any, Iterable, Mapping
import unittest
from unittest.mock import patch

from jsonschema import Draft202012Validator, FormatChecker
import yaml

from tools.taxonomy_case_access import build_study_access_catalog


ROOT = Path(__file__).resolve().parents[1]
MANIFEST_SCHEMA_PATH = ROOT / "schemas" / "foundational-study-manifest.schema.json"
INDEX_SCHEMA_PATH = ROOT / "schemas" / "foundational-record-index.schema.json"
SUBJECT_REGISTRY_PATH = ROOT / "registry" / "foundational-subjects.yaml"
STUDY_REGISTRY_PATH = ROOT / "registry" / "foundational-studies.yaml"

EXPECTED = {
    "taxonomy": {
        "path": "records/foundational/studies/LCMRP-FSTUDYREC-0001-M1-TAXONOMY-v1.json",
        "record_id": "LCMRP-FSTUDYREC-0001-M1-TAXONOMY",
        "study_id": "LCMRP-FSTUDY-0001-M1-TAXONOMY",
        "profile_id": "LCMRP-MPROF-0001-M1-STRUCTURAL-TAXONOMY",
        "profile_kind": "STRUCTURAL_OR_TAXONOMY_EVALUATION",
        "profile_locator": "studies/foundational/m1-taxonomy-v1/definitions/method-profile.json",
        "profile_companion_locator": "studies/foundational/m1-taxonomy-v1/definitions/category-evaluation-rules.json",
        "subject_id": "LCMRP-FSUBJ-0001-MEMORY-TAXONOMY",
        "subject_kind": "MEMORY_TAXONOMY",
        "subject_series": "LCMRP-MEMORY-TAXONOMY",
        "subject_locator": "docs/taxonomy/MEMORY_TAXONOMY_v0.1.md",
        "subject_digest": "dbdc96095ae90549132e50cbb8759bc45f228cae7d8fcb9a107b95d33647ba70",
        "analysis_ids": {
            "ANALYSIS-M1-TAXONOMY-TERM-CONTRACT",
            "ANALYSIS-M1-TAXONOMY-ORGANIZATION-COMPETITION",
            "ANALYSIS-M1-TAXONOMY-DISTINCTION-INTEGRITY",
            "ANALYSIS-M1-TAXONOMY-GOVERNANCE-ADVERSARIAL",
            "ANALYSIS-M1-TAXONOMY-AMBIGUITY-CATALOG",
        },
        "source_ids": {
            "SOURCE-M1-TAXONOMY-POSITIVE",
            "SOURCE-M1-TAXONOMY-NEGATIVE",
            "SOURCE-M1-TAXONOMY-HELD-OUT",
            "SOURCE-M1-PROGRAM-CHARTER",
            "SOURCE-M1-PRIOR-ART",
        },
        "case_bindings": {
            "SOURCE-M1-TAXONOMY-POSITIVE": (
                "ARTIFACT-M1-TAXONOMY-POSITIVE-CASES",
                "studies/foundational/m1-taxonomy-v1/cases/positive-cases.json",
                "61412fb42208441f78927ac0ad3f579758a34591b6cb20bd8163648edcea424b",
            ),
            "SOURCE-M1-TAXONOMY-NEGATIVE": (
                "ARTIFACT-M1-TAXONOMY-NEGATIVE-CASES",
                "studies/foundational/m1-taxonomy-v1/cases/negative-cases.json",
                "6a546d401f8c412a6a15f3ae7e8f733924b46a145e7339d5d1d441e887d1ab4a",
            ),
            "SOURCE-M1-TAXONOMY-HELD-OUT": (
                "ARTIFACT-M1-TAXONOMY-HELD-OUT-CASES",
                "studies/foundational/m1-taxonomy-v1/cases/held-out-cases.json",
                "e0f08002a9252ff1f1f4da119958c9d6a86f50cf3b3922672c9bffbf73c68c79",
            ),
        },
        "outputs": {
            "ANALYSIS-M1-TAXONOMY-TERM-CONTRACT": (
                "ARTIFACT-M1-TAXONOMY-TERM-CONTRACT-LEDGER",
                "studies/foundational/m1-taxonomy-v1/outputs/term-contract-ledger.json",
            ),
            "ANALYSIS-M1-TAXONOMY-ORGANIZATION-COMPETITION": (
                "ARTIFACT-M1-TAXONOMY-ORGANIZATION-COMPETITION-LEDGER",
                "studies/foundational/m1-taxonomy-v1/outputs/organization-competition-ledger.json",
            ),
            "ANALYSIS-M1-TAXONOMY-DISTINCTION-INTEGRITY": (
                "ARTIFACT-M1-TAXONOMY-DISTINCTION-INTEGRITY-LEDGER",
                "studies/foundational/m1-taxonomy-v1/outputs/distinction-integrity-ledger.json",
            ),
            "ANALYSIS-M1-TAXONOMY-GOVERNANCE-ADVERSARIAL": (
                "ARTIFACT-M1-TAXONOMY-GOVERNANCE-ADVERSARIAL-LEDGER",
                "studies/foundational/m1-taxonomy-v1/outputs/governance-adversarial-ledger.json",
            ),
            "ANALYSIS-M1-TAXONOMY-AMBIGUITY-CATALOG": (
                "ARTIFACT-M1-TAXONOMY-AMBIGUITY-CATALOG",
                "studies/foundational/m1-taxonomy-v1/outputs/ambiguity-catalog.json",
            ),
        },
    },
    "formal": {
        "path": "records/foundational/studies/LCMRP-FSTUDYREC-0002-M1-FORMAL-MODEL-v1.json",
        "record_id": "LCMRP-FSTUDYREC-0002-M1-FORMAL-MODEL",
        "study_id": "LCMRP-FSTUDY-0002-M1-FORMAL-MODEL",
        "profile_id": "LCMRP-MPROF-0002-M1-FORMAL-ANALYSIS",
        "profile_kind": "FORMAL_ANALYSIS",
        "profile_locator": "studies/foundational/m1-formal-model-v1/artifacts/method-profile-definition.json",
        "profile_companion_locator": "studies/foundational/m1-formal-model-v1/artifacts/formal-system.json",
        "subject_id": "LCMRP-FSUBJ-0002-FORMAL-MEMORY-OBJECT-MODEL",
        "subject_kind": "FORMAL_MEMORY_MODEL",
        "subject_series": "LCMRP-FORMAL-MEMORY-OBJECT-MODEL",
        "subject_locator": "docs/taxonomy/FORMAL_MEMORY_OBJECT_MODEL_v0.1.md",
        "subject_digest": "82052e424c01d3204828472ef569f74f7c0aad418f827cffda92400562bbfaf3",
        "analysis_ids": {
            "ANALYSIS-FMO-01-SATISFIABILITY",
            "ANALYSIS-FMO-02-ENTAILMENT",
            "ANALYSIS-FMO-03-NONENTAILMENT",
            "ANALYSIS-FMO-04-INVARIANT-INDEPENDENCE",
            "ANALYSIS-FMO-05-AUTHORITY",
            "ANALYSIS-FMO-06-DELETION",
            "ANALYSIS-FMO-07-SEMANTIC-VALIDITY",
        },
        "source_ids": {
            "SOURCE-FMO-01",
            "SOURCE-FSC-01",
            "SOURCE-KERNEL-01",
            "SOURCE-ASSUMPTIONS-01",
            "SOURCE-PROPOSITIONS-01",
        },
        "outputs": {
            "ANALYSIS-FMO-01-SATISFIABILITY": (
                "LCMRP-RESULT-0002-M1-FMO-ANALYSIS-01-KERNEL-RAW",
                "studies/foundational/m1-formal-model-v1/results/analysis-01-bounded-kernel-raw.json",
            ),
            "ANALYSIS-FMO-02-ENTAILMENT": (
                "LCMRP-RESULT-0002-M1-FMO-ANALYSIS-02-ENTAILMENT",
                "studies/foundational/m1-formal-model-v1/results/analysis-02-entailment.json",
            ),
            "ANALYSIS-FMO-03-NONENTAILMENT": (
                "LCMRP-RESULT-0002-M1-FMO-ANALYSIS-03-NONENTAILMENT",
                "studies/foundational/m1-formal-model-v1/results/analysis-03-nonentailment.json",
            ),
            "ANALYSIS-FMO-04-INVARIANT-INDEPENDENCE": (
                "LCMRP-RESULT-0002-M1-FMO-ANALYSIS-04-INVARIANT-INDEPENDENCE",
                "studies/foundational/m1-formal-model-v1/results/analysis-04-invariant-independence.json",
            ),
            "ANALYSIS-FMO-05-AUTHORITY": (
                "LCMRP-RESULT-0002-M1-FMO-ANALYSIS-05-AUTHORITY",
                "studies/foundational/m1-formal-model-v1/results/analysis-05-authority.json",
            ),
            "ANALYSIS-FMO-06-DELETION": (
                "LCMRP-RESULT-0002-M1-FMO-ANALYSIS-06-DELETION",
                "studies/foundational/m1-formal-model-v1/results/analysis-06-deletion.json",
            ),
            "ANALYSIS-FMO-07-SEMANTIC-VALIDITY": (
                "LCMRP-RESULT-0002-M1-FMO-ANALYSIS-07-SEMANTIC-VALIDITY",
                "studies/foundational/m1-formal-model-v1/results/analysis-07-semantic-validity.json",
            ),
        },
    },
}

EMPTY_REGISTRIES = (
    "registry/mechanisms.yaml",
    "registry/experiments.yaml",
    "registry/evidence.yaml",
    "registry/research-findings.yaml",
    "registry/foundational-study-closeouts.yaml",
)

EMPTY_RECORD_AREAS = (
    "records/experiments",
    "records/evidence",
    "records/foundational/findings",
    "records/foundational/closeouts",
)

POST_FREEZE_ARTIFACTS_THAT_MUST_NOT_EXIST = (
    "studies/foundational/m1-taxonomy-v1/execution/execution-intake.json",
)

ALLOWED_SOURCE_ROLES = {
    "DEVELOPMENT",
    "POSITIVE_CASES",
    "NEGATIVE_CASES",
    "HELD_OUT_EVALUATION",
    "FORMAL_INPUT",
    "PRIOR_WORK",
}

EXECUTION_RESULT_KEYS = {
    "claim_assessment",
    "completed_at",
    "execution_completed_at",
    "finding_id",
    "finding_record_id",
    "observed_result",
    "observed_results",
    "result_class",
    "terminal_disposition",
}

SUBJECT_FIELDS = (
    "target_type",
    "subject_kind",
    "subject_id",
    "subject_series",
    "subject_version",
    "name",
    "definition",
    "boundary",
    "definition_artifact",
)

OVERCLAIM = re.compile(
    r"(?i)(?:\b(?:this|the)\s+(?:study|protocol)\s+"
    r"(?:is|was|has been)\s+(?!not\b|never\b)"
    r"(?:complete(?:d)?|validated|proven|production[- ]ready)\b|"
    r"\bM1\s+(?:is|was|has been)\s+(?!not\b|never\b)(?:now\s+)?"
    r"complete(?:d)?\b|"
    r"\b(?:establishes|constitutes|creates|awards)\s+"
    r"(?:independently\s+validated\s+)?(?:scientific\s+)?"
    r"(?:evidence|proof|maturity|production readiness)\b)"
)

PRODUCT_BINDING = re.compile(
    r"(?i)\b(?:CorpusStudio|RESEARCH-TO-PRODUCT)\b"
)


def _load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _load_yaml(path: Path) -> Any:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def _iter_mappings(value: Any) -> Iterable[Mapping[str, Any]]:
    if isinstance(value, Mapping):
        yield value
        for child in value.values():
            yield from _iter_mappings(child)
    elif isinstance(value, list):
        for child in value:
            yield from _iter_mappings(child)


def _iter_strings(value: Any) -> Iterable[str]:
    if isinstance(value, str):
        yield value
    elif isinstance(value, Mapping):
        for child in value.values():
            yield from _iter_strings(child)
    elif isinstance(value, list):
        for child in value:
            yield from _iter_strings(child)


def _safe_locator(locator: Any) -> bool:
    if not isinstance(locator, str) or not locator or "\\" in locator:
        return False
    path = PurePosixPath(locator)
    return (
        not path.is_absolute()
        and "." not in path.parts
        and ".." not in path.parts
        and "://" not in locator
    )


def _resolved_path(locator: Any) -> Path | None:
    if not _safe_locator(locator):
        return None
    candidate = (ROOT / locator).resolve()
    try:
        candidate.relative_to(ROOT.resolve())
    except ValueError:
        return None
    return candidate


def _artifact_key(reference: Any) -> tuple[Any, ...] | None:
    if not isinstance(reference, Mapping):
        return None
    digest = reference.get("digest")
    return (
        reference.get("artifact_id"),
        reference.get("artifact_version"),
        reference.get("schema_id"),
        reference.get("locator"),
        digest.get("value") if isinstance(digest, Mapping) else None,
    )


def _artifact_reference_errors(
    reference: Any,
    label: str,
    *,
    immutable: bool,
    verify_bytes: bool = True,
) -> list[str]:
    errors: list[str] = []
    if not isinstance(reference, Mapping):
        return [f"{label}: artifact reference is missing"]
    locator = reference.get("locator")
    target = _resolved_path(locator)
    if target is None:
        return [f"{label}: unsafe artifact locator"]

    digest = reference.get("digest")
    if not isinstance(digest, Mapping):
        return [f"{label}: artifact digest is missing"]
    if digest.get("algorithm") != "SHA-256":
        errors.append(f"{label}: digest algorithm is not SHA-256")
    if digest.get("scope") != "RAW_FILE_BYTES":
        errors.append(f"{label}: digest scope is not RAW_FILE_BYTES")

    if immutable:
        if digest.get("status") not in {"RECORDED", "VERIFIED"}:
            errors.append(f"{label}: frozen input digest is not immutable")
        if not target.is_file():
            errors.append(f"{label}: frozen input artifact does not resolve")
        elif verify_bytes and digest.get("value") != hashlib.sha256(
            target.read_bytes()
        ).hexdigest():
            errors.append(f"{label}: raw-byte digest mismatch")
    else:
        if digest.get("status") != "PENDING" or digest.get("value") is not None:
            errors.append(f"{label}: planned output must retain a PENDING null digest")
        if target.exists():
            errors.append(f"{label}: planned output already exists")
    return errors


def _immutable_references(manifest: Mapping[str, Any]) -> list[tuple[str, Any]]:
    preregistration = manifest.get("preregistration")
    subject = manifest.get("subject")
    profile = manifest.get("primary_method_profile")
    reproducibility = manifest.get("reproducibility")
    result: list[tuple[str, Any]] = [
        (
            "preregistration.freeze_artifact",
            preregistration.get("freeze_artifact")
            if isinstance(preregistration, Mapping)
            else None,
        ),
        (
            "subject.definition_artifact",
            subject.get("definition_artifact") if isinstance(subject, Mapping) else None,
        ),
        (
            "primary_method_profile.profile_definition_artifact",
            profile.get("profile_definition_artifact")
            if isinstance(profile, Mapping)
            else None,
        ),
        (
            "reproducibility.environment_artifact",
            reproducibility.get("environment_artifact")
            if isinstance(reproducibility, Mapping)
            else None,
        ),
        ("protocol_artifact", manifest.get("protocol_artifact")),
    ]
    if isinstance(profile, Mapping):
        for field in (
            "category_definition_artifact",
            "formal_system_artifact",
            "tool_provenance",
        ):
            if field in profile:
                result.append((f"primary_method_profile.{field}", profile.get(field)))
    sources = manifest.get("sources")
    if isinstance(sources, list):
        for position, source in enumerate(sources):
            result.append(
                (
                    f"sources/{position}/provenance_artifact",
                    source.get("provenance_artifact")
                    if isinstance(source, Mapping)
                    else None,
                )
            )
    if isinstance(reproducibility, Mapping):
        configurations = reproducibility.get("configuration_artifacts")
        if isinstance(configurations, list):
            for position, artifact in enumerate(configurations):
                result.append(
                    (f"reproducibility.configuration_artifacts/{position}", artifact)
                )
    return result


def _planned_outputs(manifest: Mapping[str, Any]) -> list[tuple[str, Any]]:
    analyses = manifest.get("analyses")
    if not isinstance(analyses, list):
        return []
    return [
        (
            f"analyses/{position}/planned_output_artifact",
            analysis.get("planned_output_artifact")
            if isinstance(analysis, Mapping)
            else None,
        )
        for position, analysis in enumerate(analyses)
    ]


def _file_identity(path: Path) -> tuple[int, int] | None:
    """Return a metadata-only filesystem identity without opening file content."""

    try:
        metadata = path.stat()
    except OSError:
        return None
    return metadata.st_dev, metadata.st_ino


@lru_cache(maxsize=1)
def _authoritative_protected_case_artifacts() -> tuple[
    frozenset[Path], frozenset[tuple[int, int]]
]:
    """Resolve immutable production opacity before any in-memory mutation."""

    catalog = build_study_access_catalog(ROOT)
    if catalog.errors:
        raise RuntimeError(
            "taxonomy case-access catalog is unavailable: "
            + "; ".join(catalog.errors)
        )

    canonical_paths: set[Path] = set()
    file_identities: set[tuple[int, int]] = set()
    for artifact in catalog.case_artifacts:
        path = _resolved_path(artifact.locator)
        identity = _file_identity(path) if path is not None else None
        if path is None or identity is None:
            raise RuntimeError(
                "authoritative taxonomy case artifact does not resolve safely: "
                f"{artifact.locator}"
            )
        canonical_paths.add(path)
        file_identities.add(identity)

    expected_v1_paths: set[Path] = set()
    for _artifact_id, locator, _digest in EXPECTED["taxonomy"][
        "case_bindings"
    ].values():
        path = _resolved_path(locator)
        if path is None:
            raise RuntimeError(
                "expected version-1 taxonomy case locator is unsafe: "
                f"{locator}"
            )
        expected_v1_paths.add(path)
    if not expected_v1_paths.issubset(canonical_paths):
        raise RuntimeError(
            "authoritative taxonomy case-access catalog omitted a reviewed "
            "version-1 case artifact"
        )
    return frozenset(canonical_paths), frozenset(file_identities)


def _is_authoritative_protected_case_path(path: Path) -> bool:
    """Match canonical paths, symlink aliases, and hard-link identities."""

    canonical_paths, file_identities = _authoritative_protected_case_artifacts()
    canonical = path.resolve()
    if canonical in canonical_paths:
        return True
    identity = _file_identity(canonical)
    return identity is not None and identity in file_identities


def _is_authoritative_protected_case_locator(locator: Any) -> bool:
    """Classify a locator independently of mutable source role or kind."""

    path = _resolved_path(locator)
    return path is not None and _is_authoritative_protected_case_path(path)


def _freeze_binding_errors(manifest: Mapping[str, Any], lane: str) -> list[str]:
    errors: list[str] = []
    preregistration = manifest.get("preregistration")
    if not isinstance(preregistration, Mapping):
        return [f"{lane}: preregistration is missing"]
    reference = preregistration.get("freeze_artifact")
    if not isinstance(reference, Mapping):
        return [f"{lane}: freeze artifact is missing"]
    target = _resolved_path(reference.get("locator"))
    if target is None or not target.is_file():
        return [f"{lane}: freeze artifact does not resolve"]
    try:
        attestation = _load_json(target)
    except (json.JSONDecodeError, UnicodeDecodeError):
        return [f"{lane}: freeze artifact is not a JSON attestation"]
    if not isinstance(attestation, Mapping):
        return [f"{lane}: freeze artifact is not an object"]

    comparisons = (
        ("artifact_id", reference.get("artifact_id")),
        ("artifact_version", reference.get("artifact_version")),
        ("study_id", manifest.get("study_id")),
        ("study_record_id", manifest.get("study_record_id")),
        ("study_record_version", manifest.get("record_version")),
        ("frozen_at", preregistration.get("frozen_at")),
        ("results_accessed_before_freeze", False),
    )
    for field, expected in comparisons:
        if attestation.get(field) != expected:
            errors.append(f"{lane}: freeze artifact binding mismatch for {field}")
    authority = attestation.get(
        "registration_authority", attestation.get("authority")
    )
    if authority != preregistration.get("registration_authority"):
        errors.append(f"{lane}: freeze artifact authority mismatch")
    return errors


def _schema_errors(instance: Any, schema: Mapping[str, Any], label: str) -> list[str]:
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    result: list[str] = []
    for error in sorted(
        validator.iter_errors(instance),
        key=lambda item: tuple(str(part) for part in item.absolute_path),
    ):
        location = "/".join(str(part) for part in error.absolute_path) or "<root>"
        result.append(f"{label}:{location}: schema: {error.message}")
    return result


def _subject_entries(registry: Mapping[str, Any]) -> dict[str, Mapping[str, Any]]:
    entries = registry.get("entries")
    if not isinstance(entries, list):
        return {}
    return {
        entry.get("subject_id"): entry
        for entry in entries
        if isinstance(entry, Mapping) and isinstance(entry.get("subject_id"), str)
    }


def _referenced_content_errors(
    manifest: Mapping[str, Any], lane: str
) -> list[str]:
    errors: list[str] = []
    seen: set[Path] = set()
    for label, reference in _immutable_references(manifest):
        if not isinstance(reference, Mapping):
            continue
        if _is_authoritative_protected_case_locator(reference.get("locator")):
            continue
        target = _resolved_path(reference.get("locator"))
        if target is None or not target.is_file() or target in seen:
            continue
        seen.add(target)
        try:
            text = target.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        if OVERCLAIM.search(text):
            errors.append(f"{lane}:{label}: frozen input contains an overclaim")
        relative = target.relative_to(ROOT).as_posix()
        if relative.startswith("studies/foundational/") and PRODUCT_BINDING.search(
            text
        ):
            errors.append(f"{lane}:{label}: frozen input contains a product binding")
        if target.suffix.lower() != ".json":
            continue
        try:
            document = json.loads(text)
        except json.JSONDecodeError:
            continue
        keys = {
            str(key)
            for mapping in _iter_mappings(document)
            for key in mapping
        }
        leaked = EXECUTION_RESULT_KEYS.intersection(keys)
        if leaked:
            errors.append(
                f"{lane}:{label}: frozen input contains execution-result keys "
                f"{sorted(leaked)}"
            )
    return errors


def _formal_tool_provenance_errors(manifest: Mapping[str, Any]) -> list[str]:
    errors: list[str] = []
    profile = manifest.get("primary_method_profile")
    if not isinstance(profile, Mapping):
        return ["formal: profile is missing for tool-provenance verification"]
    reference = profile.get("tool_provenance")
    if not isinstance(reference, Mapping):
        return ["formal: immutable tool provenance is missing"]
    if reference.get("locator") != (
        "studies/foundational/m1-formal-model-v1/artifacts/tool-provenance.json"
    ):
        errors.append("formal: exact tool-provenance locator mismatch")
    target = _resolved_path(reference.get("locator"))
    if target is None or not target.is_file():
        return errors + ["formal: tool-provenance artifact does not resolve"]
    try:
        document = _load_json(target)
    except (json.JSONDecodeError, UnicodeDecodeError):
        return errors + ["formal: tool-provenance artifact is not valid JSON"]
    if not isinstance(document, Mapping):
        return errors + ["formal: tool-provenance artifact is not an object"]
    expected_fields = {
        "artifact_id": reference.get("artifact_id"),
        "artifact_version": reference.get("artifact_version"),
        "study_id": EXPECTED["formal"]["study_id"],
        "profile_id": EXPECTED["formal"]["profile_id"],
    }
    for field, expected in expected_fields.items():
        if document.get(field) != expected:
            errors.append(f"formal: tool-provenance binding mismatch for {field}")
    if "NOT-EXECUTED" not in str(document.get("tool_status", "")):
        errors.append("formal: tool provenance does not preserve unexecuted status")

    analyzer = document.get("analyzer")
    if not isinstance(analyzer, Mapping):
        return errors + ["formal: analyzer provenance is missing"]
    expected_analyzer = (
        "studies/foundational/m1-formal-model-v1/analyze_fmo_kernel.py"
    )
    if analyzer.get("locator") != expected_analyzer:
        errors.append("formal: exact analyzer locator mismatch")
    analyzer_path = _resolved_path(analyzer.get("locator"))
    if analyzer_path is None or not analyzer_path.is_file():
        errors.append("formal: planned analyzer does not resolve")
    elif analyzer.get("raw_byte_sha256") != hashlib.sha256(
        analyzer_path.read_bytes()
    ).hexdigest():
        errors.append("formal: planned analyzer raw-byte digest mismatch")
    for field in (
        "language",
        "required_runtime",
        "dependencies",
        "semantic_method",
        "execution_guard",
        "write_policy",
    ):
        if not analyzer.get(field):
            errors.append(f"formal: analyzer provenance lacks {field}")
    if not re.search(
        r"(?i)semantic|model|valuation|entail|satisfi",
        str(analyzer.get("semantic_method", "")),
    ):
        errors.append("formal: analyzer provenance lacks a semantic method")

    external = document.get("external_services")
    if not isinstance(external, Mapping) or any(
        external.get(field) != 0
        for field in (
            "network_calls",
            "model_calls",
            "external_solver_calls",
            "cloud_service_calls",
        )
    ):
        errors.append("formal: tool provenance permits an undeclared external service")
    return errors


def _profile_definition_binding_errors(
    manifest: Mapping[str, Any], lane: str
) -> list[str]:
    errors: list[str] = []
    expected = EXPECTED[lane]
    profile = manifest.get("primary_method_profile")
    if not isinstance(profile, Mapping):
        return [f"{lane}: profile definition cannot be resolved"]
    profile_reference = profile.get("profile_definition_artifact")
    if not isinstance(profile_reference, Mapping):
        return [f"{lane}: profile definition artifact is missing"]
    if profile_reference.get("locator") != expected["profile_locator"]:
        errors.append(f"{lane}: exact profile-definition locator mismatch")
    profile_path = _resolved_path(profile_reference.get("locator"))
    if profile_path is None or not profile_path.is_file():
        return errors + [f"{lane}: profile definition does not resolve"]
    try:
        profile_document = _load_json(profile_path)
    except (json.JSONDecodeError, UnicodeDecodeError):
        return errors + [f"{lane}: profile definition is not valid JSON"]
    if not isinstance(profile_document, Mapping):
        return errors + [f"{lane}: profile definition is not an object"]
    comparisons = {
        "artifact_id": profile_reference.get("artifact_id"),
        "artifact_version": profile_reference.get("artifact_version"),
        "profile_kind": profile.get("profile_kind"),
        "profile_id": profile.get("profile_id"),
        "profile_series": profile.get("profile_series"),
        "profile_version": profile.get("profile_version"),
    }
    for field, value in comparisons.items():
        if profile_document.get(field) != value:
            errors.append(f"{lane}: profile definition mismatch for {field}")
    declared_analyses = profile_document.get("analysis_ids")
    if declared_analyses is not None and (
        not isinstance(declared_analyses, list)
        or set(declared_analyses) != expected["analysis_ids"]
    ):
        errors.append(f"{lane}: profile definition analysis-ID set mismatch")

    companion_field = (
        "category_definition_artifact"
        if lane == "taxonomy"
        else "formal_system_artifact"
    )
    companion = profile.get(companion_field)
    if not isinstance(companion, Mapping):
        return errors + [f"{lane}: profile companion artifact is missing"]
    if companion.get("locator") != expected["profile_companion_locator"]:
        errors.append(f"{lane}: exact profile companion locator mismatch")
    companion_path = _resolved_path(companion.get("locator"))
    if companion_path is None or not companion_path.is_file():
        return errors + [f"{lane}: profile companion does not resolve"]
    try:
        companion_document = _load_json(companion_path)
    except (json.JSONDecodeError, UnicodeDecodeError):
        return errors + [f"{lane}: profile companion is not valid JSON"]
    if not isinstance(companion_document, Mapping):
        return errors + [f"{lane}: profile companion is not an object"]
    if companion_document.get("artifact_id") != companion.get("artifact_id"):
        errors.append(f"{lane}: profile companion artifact ID mismatch")
    if companion_document.get("artifact_version") != companion.get(
        "artifact_version"
    ):
        errors.append(f"{lane}: profile companion artifact version mismatch")
    return errors


def _profile_errors(manifest: Mapping[str, Any], lane: str) -> list[str]:
    errors: list[str] = []
    expected = EXPECTED[lane]
    profile = manifest.get("primary_method_profile")
    sources = manifest.get("sources")
    if not isinstance(profile, Mapping):
        return [f"{lane}: primary method profile is missing"]
    source_list = sources if isinstance(sources, list) else []
    source_mappings = [source for source in source_list if isinstance(source, Mapping)]

    if profile.get("profile_id") != expected["profile_id"]:
        errors.append(f"{lane}: exact profile ID mismatch")
    if profile.get("profile_kind") != expected["profile_kind"]:
        errors.append(f"{lane}: exact profile kind mismatch")
    if profile.get("profile_version") != 1:
        errors.append(f"{lane}: initial profile version is not 1")
    if not isinstance(profile.get("profile_series"), str) or not profile.get(
        "profile_series"
    ):
        errors.append(f"{lane}: profile series is missing")

    source_ids: list[Any] = []
    for source in source_mappings:
        source_id = source.get("source_id")
        source_ids.append(source_id)
        if source.get("role") not in ALLOWED_SOURCE_ROLES:
            errors.append(f"{lane}: source has an unsupported role")
        if source.get("human_subjects_involved") is not False:
            errors.append(f"{lane}: source is not non-human")
    if len(source_ids) != len(set(source_ids)):
        errors.append(f"{lane}: source IDs are not unique")

    if lane == "taxonomy":
        roles = {
            role: {
                source.get("source_id")
                for source in source_mappings
                if source.get("role") == role
            }
            for role in ("POSITIVE_CASES", "NEGATIVE_CASES", "HELD_OUT_EVALUATION")
        }
        for role, identifiers in roles.items():
            if not identifiers:
                errors.append(f"taxonomy: missing separate {role} source")
        positive = set(profile.get("positive_case_source_ids", []))
        negative = set(profile.get("negative_case_source_ids", []))
        if positive != roles["POSITIVE_CASES"]:
            errors.append("taxonomy: positive source/profile binding mismatch")
        if negative != roles["NEGATIVE_CASES"]:
            errors.append("taxonomy: negative source/profile binding mismatch")
        if any(roles[left].intersection(roles[right]) for left, right in (
            ("POSITIVE_CASES", "NEGATIVE_CASES"),
            ("POSITIVE_CASES", "HELD_OUT_EVALUATION"),
            ("NEGATIVE_CASES", "HELD_OUT_EVALUATION"),
        )):
            errors.append("taxonomy: positive, negative, and held-out IDs are not separate")
        governed_sources = [
            source
            for source in source_mappings
            if source.get("role") in roles
        ]
        provenance_keys = [
            _artifact_key(source.get("provenance_artifact"))
            for source in governed_sources
        ]
        provenance_ids = [
            source.get("provenance_artifact").get("artifact_id")
            for source in governed_sources
            if isinstance(source.get("provenance_artifact"), Mapping)
        ]
        provenance_locators = [
            source.get("provenance_artifact").get("locator")
            for source in governed_sources
            if isinstance(source.get("provenance_artifact"), Mapping)
        ]
        if (
            len(provenance_keys) != len(set(provenance_keys))
            or len(provenance_ids) != len(set(provenance_ids))
            or len(provenance_locators) != len(set(provenance_locators))
        ):
            errors.append("taxonomy: held-out or case-source provenance is reused")
        coverage = str(profile.get("coverage_rule", ""))
        if not re.search(r"(?i)held[- ]out", coverage):
            errors.append("taxonomy: coverage rule does not govern held-out cases")
        for field in (
            "competency_questions",
            "integrity_constraints",
            "adjudication_method",
            "coverage_rule",
            "category_definition_artifact",
        ):
            if not profile.get(field):
                errors.append(f"taxonomy: required profile obligation {field} is missing")
    else:
        formal_sources = [
            source for source in source_mappings if source.get("role") == "FORMAL_INPUT"
        ]
        if not formal_sources:
            errors.append("formal: no FORMAL_INPUT source is declared")
        formal_system_key = _artifact_key(profile.get("formal_system_artifact"))
        if formal_system_key not in {
            _artifact_key(source.get("provenance_artifact"))
            for source in formal_sources
        }:
            errors.append("formal: formal-system source binding mismatch")
        for field in (
            "formal_system_artifact",
            "assumptions",
            "propositions",
            "consistency_or_satisfiability_checks",
            "intended_entailments",
            "non_entailments_or_countermodels",
            "tool_provenance",
            "proof_or_verification_method",
            "semantic_validity_check",
            "counterexample_search",
        ):
            if not profile.get(field):
                errors.append(f"formal: required profile obligation {field} is missing")
        semantic_text = "\n".join(
            str(profile.get(field, ""))
            for field in (
                "proof_or_verification_method",
                "semantic_validity_check",
                "counterexample_search",
            )
        )
        if not re.search(r"(?i)semantic|model|valuation|entail|satisfi", semantic_text):
            errors.append("formal: verification lacks a semantic check")
        if re.search(
            r"(?i)(?:syntax|parse|schema)"
            r"(?:[- ](?:check(?:ing)?|validation))?\s+only|"
            r"only\s+(?:syntax|parse|schema)",
            semantic_text,
        ):
            errors.append("formal: syntax-only validation is forbidden")
        if not re.search(
            r"(?i)counter(?:example|model)|falsif|witness|model",
            str(profile.get("counterexample_search", "")),
        ):
            errors.append("formal: counterexample search is not semantic")
    return errors


def _freeze_errors(
    manifests: Mapping[str, Mapping[str, Any]],
    study_registry: Mapping[str, Any],
    subject_registry: Mapping[str, Any],
    other_registries: Mapping[str, Mapping[str, Any]],
) -> list[str]:
    """Apply stricter M1 study-freeze semantics beyond schema shape."""

    errors: list[str] = []
    manifest_schema = _load_json(MANIFEST_SCHEMA_PATH)
    index_schema = _load_json(INDEX_SCHEMA_PATH)
    errors.extend(_schema_errors(study_registry, index_schema, "study registry"))
    subject_by_id = _subject_entries(subject_registry)

    entries = study_registry.get("entries")
    entry_list = entries if isinstance(entries, list) else []
    reviewed_v1_entries = [
        entry
        for entry in entry_list
        if isinstance(entry, Mapping)
        and entry.get("record_version") == 1
        and entry.get("record_id") in {item["record_id"] for item in EXPECTED.values()}
    ]
    if len(reviewed_v1_entries) != 2:
        errors.append("study registry must retain the two reviewed version-1 entries")
    indexed_by_id = {
        entry.get("record_id"): entry
        for entry in reviewed_v1_entries
        if isinstance(entry.get("record_id"), str)
    }
    if set(indexed_by_id) != {item["record_id"] for item in EXPECTED.values()}:
        errors.append("study registry record-ID set differs from the reviewed pair")

    all_analysis_ids: list[Any] = []
    all_source_ids: list[Any] = []
    lane_artifacts: dict[str, set[tuple[Any, Any]]] = {}
    profile_ids: list[Any] = []
    profile_series: list[Any] = []

    for lane, expected in EXPECTED.items():
        manifest = manifests.get(lane)
        if not isinstance(manifest, Mapping):
            errors.append(f"{lane}: canonical manifest is missing")
            continue
        errors.extend(_schema_errors(manifest, manifest_schema, f"{lane} manifest"))
        if manifest.get("study_record_id") != expected["record_id"]:
            errors.append(f"{lane}: exact study record ID mismatch")
        if manifest.get("study_id") != expected["study_id"]:
            errors.append(f"{lane}: exact study ID mismatch")
        if manifest.get("record_version") != 1:
            errors.append(f"{lane}: initial study record version is not 1")
        if manifest.get("record_status") != "FROZEN":
            errors.append(f"{lane}: study record is not FROZEN")
        if manifest.get("research_layer") != "LAYER_1_FOUNDATIONAL_RESEARCH":
            errors.append(f"{lane}: study is not Layer 1")

        amendment = manifest.get("amendment")
        if not isinstance(amendment, Mapping) or any(
            (
                amendment.get("kind") != "INITIAL",
                amendment.get("result_accessed_before_amendment") is not False,
                amendment.get("supersedes_record_version") is not None,
                amendment.get("supersedes_artifact_digest") is not None,
            )
        ):
            errors.append(f"{lane}: initial amendment/no-result-access boundary failed")
        preregistration = manifest.get("preregistration")
        if not isinstance(preregistration, Mapping) or any(
            (
                preregistration.get("status") != "FROZEN",
                preregistration.get("results_accessed_before_freeze") is not False,
                not preregistration.get("frozen_at"),
                not preregistration.get("registration_authority"),
            )
        ):
            errors.append(f"{lane}: frozen preregistration/no-prior-result-access failed")

        subject = manifest.get("subject")
        registered = subject_by_id.get(expected["subject_id"])
        if not isinstance(subject, Mapping) or not isinstance(registered, Mapping):
            errors.append(f"{lane}: registered subject binding is missing")
        else:
            for field in SUBJECT_FIELDS:
                if subject.get(field) != registered.get(field):
                    errors.append(f"{lane}: registered subject mismatch for {field}")
            if subject.get("subject_kind") != expected["subject_kind"]:
                errors.append(f"{lane}: exact subject kind mismatch")
            if subject.get("subject_series") != expected["subject_series"]:
                errors.append(f"{lane}: exact subject series mismatch")
            artifact = subject.get("definition_artifact")
            if isinstance(artifact, Mapping):
                digest = artifact.get("digest")
                if artifact.get("locator") != expected["subject_locator"]:
                    errors.append(f"{lane}: exact subject locator mismatch")
                if not isinstance(digest, Mapping) or digest.get("value") != expected[
                    "subject_digest"
                ]:
                    errors.append(f"{lane}: exact subject digest mismatch")

        profile = manifest.get("primary_method_profile")
        if isinstance(profile, Mapping):
            profile_ids.append(profile.get("profile_id"))
            profile_series.append(profile.get("profile_series"))
        errors.extend(_profile_errors(manifest, lane))
        errors.extend(_profile_definition_binding_errors(manifest, lane))

        analyses = manifest.get("analyses")
        analysis_list = analyses if isinstance(analyses, list) else []
        analysis_ids = [
            analysis.get("analysis_id")
            for analysis in analysis_list
            if isinstance(analysis, Mapping)
        ]
        if not analysis_ids:
            errors.append(f"{lane}: at least one planned atomic analysis is required")
        if len(analysis_ids) != len(analysis_list) or len(analysis_ids) != len(
            set(analysis_ids)
        ):
            errors.append(f"{lane}: planned analysis IDs are not unique and atomic")
        if set(analysis_ids) != expected["analysis_ids"]:
            errors.append(f"{lane}: exact planned analysis-ID set mismatch")
        all_analysis_ids.extend(analysis_ids)

        output_keys = [
            _artifact_key(reference) for _label, reference in _planned_outputs(manifest)
        ]
        output_ids = [
            reference.get("artifact_id")
            for _label, reference in _planned_outputs(manifest)
            if isinstance(reference, Mapping)
        ]
        output_locators = [
            reference.get("locator")
            for _label, reference in _planned_outputs(manifest)
            if isinstance(reference, Mapping)
        ]
        if (
            len(output_keys) != len(set(output_keys))
            or len(output_ids) != len(set(output_ids))
            or len(output_locators) != len(set(output_locators))
        ):
            errors.append(f"{lane}: planned analyses reuse an output artifact")
        expected_outputs = expected.get("outputs")
        if isinstance(expected_outputs, Mapping):
            actual_outputs = {
                analysis.get("analysis_id"): (
                    output.get("artifact_id"),
                    output.get("locator"),
                )
                for analysis in analysis_list
                if isinstance(analysis, Mapping)
                for output in [analysis.get("planned_output_artifact")]
                if isinstance(output, Mapping)
            }
            if actual_outputs != expected_outputs:
                errors.append(f"{lane}: exact planned output binding set mismatch")
        for label, reference in _planned_outputs(manifest):
            errors.extend(
                _artifact_reference_errors(
                    reference, f"{lane}:{label}", immutable=False
                )
            )
        for label, reference in _immutable_references(manifest):
            locator = (
                reference.get("locator")
                if isinstance(reference, Mapping)
                else None
            )
            errors.extend(
                _artifact_reference_errors(
                    reference,
                    f"{lane}:{label}",
                    immutable=True,
                    verify_bytes=(
                        not _is_authoritative_protected_case_locator(locator)
                    ),
                )
            )
        errors.extend(_freeze_binding_errors(manifest, lane))
        errors.extend(_referenced_content_errors(manifest, lane))

        sources = manifest.get("sources")
        source_list = sources if isinstance(sources, list) else []
        lane_source_ids = [
            source.get("source_id")
            for source in source_list
            if isinstance(source, Mapping)
        ]
        if set(lane_source_ids) != expected["source_ids"]:
            errors.append(f"{lane}: exact source-ID set mismatch")
        expected_case_bindings = expected.get("case_bindings")
        if isinstance(expected_case_bindings, Mapping):
            actual_case_bindings = {
                source.get("source_id"): (
                    reference.get("artifact_id"),
                    reference.get("locator"),
                    digest.get("value") if isinstance(digest, Mapping) else None,
                )
                for source in source_list
                if isinstance(source, Mapping)
                for reference in [source.get("provenance_artifact")]
                if isinstance(reference, Mapping)
                for digest in [reference.get("digest")]
                if source.get("source_id") in expected_case_bindings
            }
            if actual_case_bindings != expected_case_bindings:
                errors.append(f"{lane}: exact protected case metadata binding mismatch")
        all_source_ids.extend(lane_source_ids)
        if lane == "formal":
            errors.extend(_formal_tool_provenance_errors(manifest))

        maturity = manifest.get("mechanism_maturity_boundary")
        expected_maturity = {
            "applicability": "NOT_APPLICABLE",
            "mechanism_under_evaluation": False,
            "may_award_mechanism_evidence_labels": False,
            "may_change_mechanism_evidence_profile": False,
        }
        if not isinstance(maturity, Mapping) or any(
            maturity.get(field) != value
            for field, value in expected_maturity.items()
        ):
            errors.append(f"{lane}: mechanism maturity boundary failed")
        joined_text = "\n".join(_iter_strings(manifest))
        if OVERCLAIM.search(joined_text):
            errors.append(f"{lane}: false completion, validation, or evidence claim")
        if PRODUCT_BINDING.search(joined_text):
            errors.append(f"{lane}: product-specific integration leaked into Layer 1")
        if "product-independent" not in joined_text.lower():
            errors.append(f"{lane}: product-independence boundary is not explicit")

        index_entry = indexed_by_id.get(expected["record_id"])
        if not isinstance(index_entry, Mapping):
            errors.append(f"{lane}: reviewed version-1 registry entry is missing")
        else:
            comparisons = {
                "record_version": 1,
                "artifact_type": "foundational_study_manifest",
                "schema_id": "urn:lcmrp:schema:foundational-study-manifest:0.1.0",
                "artifact_path": expected["path"],
            }
            for field, value in comparisons.items():
                if index_entry.get(field) != value:
                    errors.append(f"{lane}: study index mismatch for {field}")
            if index_entry.get("registry_status") not in {"ACTIVE", "SUPERSEDED"}:
                errors.append(
                    f"{lane}: version-1 study index status is neither ACTIVE nor SUPERSEDED"
                )
            path = _resolved_path(index_entry.get("artifact_path"))
            index_digest = index_entry.get("artifact_digest")
            if path is None or not path.is_file():
                errors.append(f"{lane}: indexed manifest does not resolve")
            elif (
                not isinstance(index_digest, Mapping)
                or index_digest.get("algorithm") != "SHA-256"
                or index_digest.get("scope") != "RAW_FILE_BYTES"
                or index_digest.get("value")
                != hashlib.sha256(path.read_bytes()).hexdigest()
            ):
                errors.append(f"{lane}: study index raw-byte digest mismatch")

        lane_artifacts[lane] = {
            (reference.get("artifact_id"), reference.get("locator"))
            for _label, reference in (
                _immutable_references(manifest) + _planned_outputs(manifest)
            )
            if isinstance(reference, Mapping)
        }

    if len(all_analysis_ids) != len(set(all_analysis_ids)):
        errors.append("planned analysis IDs collide across study lanes")
    if len(all_source_ids) != len(set(all_source_ids)):
        errors.append("source IDs collide across study lanes")
    if len(profile_ids) != len(set(profile_ids)) or len(profile_series) != len(
        set(profile_series)
    ):
        errors.append("profile identity collides across study lanes")
    taxonomy_artifacts = lane_artifacts.get("taxonomy", set())
    formal_artifacts = lane_artifacts.get("formal", set())
    taxonomy_ids = {artifact_id for artifact_id, _locator in taxonomy_artifacts}
    formal_ids = {artifact_id for artifact_id, _locator in formal_artifacts}
    taxonomy_locators = {locator for _artifact_id, locator in taxonomy_artifacts}
    formal_locators = {locator for _artifact_id, locator in formal_artifacts}
    if taxonomy_ids.intersection(formal_ids) or taxonomy_locators.intersection(
        formal_locators
    ):
        errors.append("artifact identity or locator is reused across study lanes")

    for relative, registry in other_registries.items():
        if registry.get("entries") != []:
            errors.append(f"{relative}: study freeze contaminated a result registry")
    return errors


class M1StudyFreezeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.manifests: dict[str, Mapping[str, Any]] = {}
        for lane, expected in EXPECTED.items():
            path = ROOT / expected["path"]
            cls.manifests[lane] = _load_json(path) if path.is_file() else {}
        cls.study_registry = _load_yaml(STUDY_REGISTRY_PATH)
        cls.subject_registry = _load_yaml(SUBJECT_REGISTRY_PATH)
        cls.other_registries = {
            relative: _load_yaml(ROOT / relative) for relative in EMPTY_REGISTRIES
        }

    def errors(
        self,
        manifests: Mapping[str, Mapping[str, Any]] | None = None,
        study_registry: Mapping[str, Any] | None = None,
        other_registries: Mapping[str, Mapping[str, Any]] | None = None,
    ) -> list[str]:
        return _freeze_errors(
            manifests if manifests is not None else self.manifests,
            study_registry if study_registry is not None else self.study_registry,
            self.subject_registry,
            other_registries
            if other_registries is not None
            else self.other_registries,
        )

    def assert_baseline(self) -> None:
        self.assertEqual([], self.errors())

    def test_01_exact_frozen_studies_and_index_pass_all_gates(self) -> None:
        expected_files = {ROOT / expected["path"] for expected in EXPECTED.values()}
        actual_files = (
            set((ROOT / "records" / "foundational" / "studies").rglob("*.json"))
            if (ROOT / "records" / "foundational" / "studies").is_dir()
            else set()
        )
        # Version-1 freezes must remain present. Later digest-linked superseding
        # records for the same study_record_id are allowed as additional files.
        self.assertTrue(
            expected_files.issubset(actual_files),
            f"missing reviewed v1 study records: {expected_files - actual_files}",
        )
        for path in actual_files - expected_files:
            name = path.name
            self.assertRegex(
                name,
                r"^LCMRP-FSTUDYREC-000[12]-M1-(TAXONOMY|FORMAL-MODEL)-v([2-9]|[1-9][0-9]+)\.json$",
                f"unexpected study record file: {path}",
            )
        self.assert_baseline()

    def test_02_no_result_closeout_experiment_or_evidence_artifacts_exist(self) -> None:
        self.assert_baseline()
        for relative in EMPTY_RECORD_AREAS:
            directory = ROOT / relative
            if directory.is_dir():
                self.assertEqual([], sorted(directory.rglob("*.json")), relative)
        for relative, registry in self.other_registries.items():
            self.assertEqual([], registry.get("entries"), relative)
        for relative in POST_FREEZE_ARTIFACTS_THAT_MUST_NOT_EXIST:
            self.assertFalse((ROOT / relative).exists(), relative)

    def test_03_subject_and_profile_swaps_are_rejected(self) -> None:
        self.assert_baseline()
        subject_swap = copy.deepcopy(self.manifests)
        subject_swap["taxonomy"]["subject"], subject_swap["formal"]["subject"] = (
            subject_swap["formal"]["subject"],
            subject_swap["taxonomy"]["subject"],
        )
        self.assertTrue(
            any("subject" in error for error in self.errors(subject_swap)),
            self.errors(subject_swap),
        )

        profile_swap = copy.deepcopy(self.manifests)
        (
            profile_swap["taxonomy"]["primary_method_profile"],
            profile_swap["formal"]["primary_method_profile"],
        ) = (
            profile_swap["formal"]["primary_method_profile"],
            profile_swap["taxonomy"]["primary_method_profile"],
        )
        self.assertTrue(
            any("profile" in error for error in self.errors(profile_swap)),
            self.errors(profile_swap),
        )

    def test_04_digest_substitution_and_unsafe_locator_are_rejected(self) -> None:
        self.assert_baseline()
        digest = copy.deepcopy(self.manifests)
        digest["taxonomy"]["subject"]["definition_artifact"]["digest"]["value"] = (
            "0" * 64
        )
        self.assertTrue(any("digest" in error for error in self.errors(digest)))

        case_digest = copy.deepcopy(self.manifests)
        case_digest["taxonomy"]["sources"][0]["provenance_artifact"]["digest"][
            "value"
        ] = "0" * 64
        case_errors = self.errors(case_digest)
        self.assertTrue(
            any("protected case metadata binding" in error for error in case_errors),
            case_errors,
        )

        escape = copy.deepcopy(self.manifests)
        escape["formal"]["protocol_artifact"]["locator"] = "../outside.md"
        self.assertTrue(any("unsafe" in error for error in self.errors(escape)))

    def test_04b_compound_case_mutation_is_rejected_before_access(self) -> None:
        self.assert_baseline()
        _authoritative_protected_case_artifacts()
        canonical_locator = EXPECTED["taxonomy"]["case_bindings"][
            "SOURCE-M1-TAXONOMY-POSITIVE"
        ][1]
        equivalent_spellings = (
            f"./{canonical_locator}",
            canonical_locator.replace("/", "//", 1),
        )
        original_open = Path.open

        for locator in equivalent_spellings:
            with self.subTest(locator=locator):
                mutated = copy.deepcopy(self.manifests)
                source = next(
                    item
                    for item in mutated["taxonomy"]["sources"]
                    if item["source_id"] == "SOURCE-M1-TAXONOMY-POSITIVE"
                )
                source["source_kind"] = "OTHER_NON_HUMAN_SOURCE"
                source["role"] = "PRIOR_WORK"
                reference = source["provenance_artifact"]
                reference["artifact_id"] = "ARTIFACT-M1-TAXONOMY-MUTATED-SOURCE"
                reference["locator"] = locator
                reference["digest"]["value"] = "0" * 64
                protected_opens: list[Path] = []

                def guarded_open(path: Path, *args: Any, **kwargs: Any) -> Any:
                    if _is_authoritative_protected_case_path(path):
                        protected_opens.append(path)
                        raise AssertionError(
                            "freeze validation attempted to open protected case bytes"
                        )
                    return original_open(path, *args, **kwargs)

                with patch.object(Path, "open", guarded_open):
                    errors = self.errors(mutated)

                self.assertTrue(
                    any(
                        "exact protected case metadata binding mismatch" in error
                        for error in errors
                    ),
                    errors,
                )
                self.assertEqual([], protected_opens)

    def test_05_freeze_artifact_cross_lane_mismatch_is_rejected(self) -> None:
        self.assert_baseline()
        mutated = copy.deepcopy(self.manifests)
        mutated["taxonomy"]["preregistration"]["freeze_artifact"] = copy.deepcopy(
            mutated["formal"]["preregistration"]["freeze_artifact"]
        )
        errors = self.errors(mutated)
        self.assertTrue(any("freeze artifact" in error for error in errors), errors)

    def test_06_missing_and_duplicate_atomic_analyses_are_rejected(self) -> None:
        self.assert_baseline()
        missing = copy.deepcopy(self.manifests)
        missing["taxonomy"]["analyses"] = missing["taxonomy"]["analyses"][:-1]
        errors = self.errors(missing)
        self.assertTrue(any("analysis" in error for error in errors), errors)

        duplicate = copy.deepcopy(self.manifests)
        duplicate["formal"]["analyses"].append(
            copy.deepcopy(duplicate["formal"]["analyses"][0])
        )
        errors = self.errors(duplicate)
        self.assertTrue(any("analysis" in error for error in errors), errors)

    def test_07_source_role_collapse_and_fake_held_out_coverage_are_rejected(self) -> None:
        self.assert_baseline()
        collapse = copy.deepcopy(self.manifests)
        negative = next(
            source
            for source in collapse["taxonomy"]["sources"]
            if source["role"] == "NEGATIVE_CASES"
        )
        negative["role"] = "POSITIVE_CASES"
        errors = self.errors(collapse)
        self.assertTrue(any("NEGATIVE_CASES" in error for error in errors), errors)

        fake_held_out = copy.deepcopy(self.manifests)
        positive = next(
            source
            for source in fake_held_out["taxonomy"]["sources"]
            if source["role"] == "POSITIVE_CASES"
        )
        held_out = next(
            source
            for source in fake_held_out["taxonomy"]["sources"]
            if source["role"] == "HELD_OUT_EVALUATION"
        )
        held_out["provenance_artifact"] = copy.deepcopy(
            positive["provenance_artifact"]
        )
        errors = self.errors(fake_held_out)
        self.assertTrue(any("provenance is reused" in error for error in errors), errors)

    def test_08_human_source_and_unsupported_role_are_rejected(self) -> None:
        self.assert_baseline()
        mutated = copy.deepcopy(self.manifests)
        mutated["taxonomy"]["sources"][0]["human_subjects_involved"] = True
        errors = self.errors(mutated)
        self.assertTrue(any("non-human" in error for error in errors), errors)

        mutated = copy.deepcopy(self.manifests)
        mutated["formal"]["sources"][0]["role"] = "RESULTS"
        errors = self.errors(mutated)
        self.assertTrue(any("unsupported role" in error for error in errors), errors)

    def test_09_profile_obligation_removal_is_rejected(self) -> None:
        self.assert_baseline()
        for lane, field in (
            ("taxonomy", "integrity_constraints"),
            ("formal", "intended_entailments"),
            ("formal", "tool_provenance"),
        ):
            with self.subTest(lane=lane, field=field):
                mutated = copy.deepcopy(self.manifests)
                del mutated[lane]["primary_method_profile"][field]
                errors = self.errors(mutated)
                self.assertTrue(any(field in error for error in errors), errors)

    def test_10_syntax_only_formal_validation_is_rejected(self) -> None:
        self.assert_baseline()
        mutated = copy.deepcopy(self.manifests)
        profile = mutated["formal"]["primary_method_profile"]
        profile["proof_or_verification_method"] = "Syntax checking only."
        profile["semantic_validity_check"] = "Syntax checking only."
        profile["counterexample_search"] = "Syntax checking only."
        errors = self.errors(mutated)
        self.assertTrue(any("syntax-only" in error for error in errors), errors)

    def test_11_executed_output_smuggling_is_rejected(self) -> None:
        self.assert_baseline()
        mutated = copy.deepcopy(self.manifests)
        output = mutated["taxonomy"]["analyses"][0]["planned_output_artifact"]
        output["locator"] = EXPECTED["taxonomy"]["path"]
        output["digest"]["status"] = "VERIFIED"
        output["digest"]["value"] = hashlib.sha256(
            (ROOT / EXPECTED["taxonomy"]["path"]).read_bytes()
        ).hexdigest()
        errors = self.errors(mutated)
        self.assertTrue(any("planned output" in error for error in errors), errors)

    def test_12_false_completion_or_evidence_claim_is_rejected(self) -> None:
        self.assert_baseline()
        for claim in (
            "This study is complete.",
            "This protocol establishes scientific evidence.",
            "M1 is now complete.",
        ):
            with self.subTest(claim=claim):
                mutated = copy.deepcopy(self.manifests)
                mutated["taxonomy"]["limitations"].append(claim)
                errors = self.errors(mutated)
                self.assertTrue(
                    any("false completion" in error for error in errors), errors
                )

    def test_13_mechanism_maturity_effect_is_rejected(self) -> None:
        self.assert_baseline()
        mutated = copy.deepcopy(self.manifests)
        boundary = mutated["formal"]["mechanism_maturity_boundary"]
        boundary["applicability"] = "BENCHMARKED"
        boundary["may_award_mechanism_evidence_labels"] = True
        errors = self.errors(mutated)
        self.assertTrue(any("maturity boundary" in error for error in errors), errors)

    def test_14_registry_contamination_is_rejected(self) -> None:
        self.assert_baseline()
        for relative in EMPTY_REGISTRIES:
            with self.subTest(registry=relative):
                contaminated = copy.deepcopy(self.other_registries)
                contaminated[relative]["entries"] = [{"unexpected": "result effect"}]
                errors = self.errors(other_registries=contaminated)
                self.assertTrue(any(relative in error for error in errors), errors)

        index_digest = copy.deepcopy(self.study_registry)
        index_digest["entries"][0]["artifact_digest"]["value"] = "f" * 64
        errors = self.errors(study_registry=index_digest)
        self.assertTrue(any("index raw-byte digest" in error for error in errors), errors)


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
