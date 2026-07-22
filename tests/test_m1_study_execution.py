"""Adversarial gates for the first governed M1 study-execution increment.

The accepted starting state is intentionally asymmetric:

* taxonomy execution may remain truthfully ``BLOCKED`` while no eligible,
  independently traceable adjudicators are available; and
* formal execution may publish only the exact Analysis 01 raw machine bundle.

These gates do not interpret a scientific result.  They protect the frozen
inputs, enforce execution ordering, preserve negative/null rows, and prevent a
machine bundle from being laundered into a proof, finding, closeout, mechanism
evidence state, or product-integration decision.
"""

from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
from pathlib import Path, PurePosixPath
import re
import subprocess
import sys
from typing import Any, Iterable, Mapping
import unittest

import yaml


ROOT = Path(__file__).resolve().parents[1]

TAXONOMY_MANIFEST = Path(
    "records/foundational/studies/"
    "LCMRP-FSTUDYREC-0001-M1-TAXONOMY-v1.json"
)
FORMAL_MANIFEST = Path(
    "records/foundational/studies/"
    "LCMRP-FSTUDYREC-0002-M1-FORMAL-MODEL-v1.json"
)
EXPECTED_MANIFEST_DIGESTS = {
    TAXONOMY_MANIFEST: (
        "01640e8dae3836874b2b39fe3ea2a8f9c090374508aa69b31adf06fea9272139"
    ),
    FORMAL_MANIFEST: (
        "b99da2d9cfa34d659416fe30cc1d3fa731425d1fcfb8b6c9422cd9b5add2707e"
    ),
}

TAXONOMY_ROOT = Path("studies/foundational/m1-taxonomy-v1")
FORMAL_ROOT = Path("studies/foundational/m1-formal-model-v1")
TAXONOMY_INTAKE = TAXONOMY_ROOT / "execution/execution-intake.json"
TAXONOMY_CASE_ROOT = TAXONOMY_ROOT / "cases"
TAXONOMY_READINESS_REVIEW = Path(
    "reviews/M1_TAXONOMY_EXECUTION_READINESS_2026-07-21.md"
)
TAXONOMY_PROTOCOL = TAXONOMY_ROOT / "protocol-v1.md"
TAXONOMY_README = TAXONOMY_ROOT / "README.md"
TAXONOMY_ENVIRONMENT = TAXONOMY_ROOT / "reproducibility/environment.json"
TAXONOMY_CONFIGURATION = TAXONOMY_ROOT / "reproducibility/configuration.json"
TAXONOMY_ATTESTATION = TAXONOMY_ROOT / "freeze-attestation.json"
TAXONOMY_COMPONENTS = (
    TAXONOMY_ROOT / "definitions/method-profile.json",
    TAXONOMY_ROOT / "definitions/category-evaluation-rules.json",
    TAXONOMY_CONFIGURATION,
    TAXONOMY_ENVIRONMENT,
)
FORMAL_ANALYZER = FORMAL_ROOT / "analyze_fmo_kernel.py"
FORMAL_CONFIGURATION = FORMAL_ROOT / "artifacts/configuration.json"
FORMAL_ENVIRONMENT = FORMAL_ROOT / "artifacts/environment.json"
FORMAL_SYSTEM = FORMAL_ROOT / "artifacts/formal-system.json"
FORMAL_ASSUMPTIONS = FORMAL_ROOT / "artifacts/assumptions.json"
FORMAL_PROPOSITIONS = FORMAL_ROOT / "artifacts/propositions.json"
FORMAL_RAW_OUTPUT = (
    FORMAL_ROOT / "results/analysis-01-bounded-kernel-raw.json"
)
FORMAL_PREFLIGHT_ATTESTATION = (
    FORMAL_ROOT / "execution/preflight-execution-attestation.json"
)
FORMAL_RUNTIME_PROVENANCE = FORMAL_ROOT / "execution/runtime-provenance.json"

FINDING_REGISTRY = Path("registry/research-findings.yaml")
CLOSEOUT_REGISTRY = Path("registry/foundational-study-closeouts.yaml")
FINDING_RECORD_ROOT = Path("records/foundational/findings")
CLOSEOUT_RECORD_ROOT = Path("records/foundational/closeouts")

FORMAL_IDENTITIES = {
    "study_id": "LCMRP-FSTUDY-0002-M1-FORMAL-MODEL",
    "study_record_id": "LCMRP-FSTUDYREC-0002-M1-FORMAL-MODEL",
    "profile_id": "LCMRP-MPROF-0002-M1-FORMAL-ANALYSIS",
    "kernel_id": "LCMRP-FSYS-0002-M1-FMO-BOUNDED-KERNEL",
}

PLACEHOLDER_ID = re.compile(
    r"(?i)(?:^|[-_])(?:TBD|TODO|UNKNOWN|ANONYMOUS|PLACEHOLDER|FAKE|TEST)(?:$|[-_])"
)
AFFIRMATIVE_OVERCLAIM = re.compile(
    r"(?i)(?:\b(?:this|the)\s+(?:result|output|study|analysis)\s+"
    r"(?:proves|validates|scientifically\s+validates|establishes\s+"
    r"(?:scientific\s+evidence|independent\s+validation|production\s+readiness))\b|"
    r"\bM1\s+(?:is|has\s+been)\s+(?:now\s+)?complete\b|"
    r"\b(?:awards?|achieves?|promotes?\s+to)\s+(?:a\s+)?"
    r"(?:mechanism\s+)?(?:maturity|evidence)\s+label\b|"
    r"\bproduction[- ]ready\b)"
)
PRODUCT_COUPLING = re.compile(
    r"(?i)(?:\bCorpusStudio\b.{0,80}\b(?:integrat|target|depend|deploy|implement)|"
    r"\b(?:integrat|target|depend|deploy|implement)\w*\b.{0,80}\bCorpusStudio\b|"
    r"\bRESEARCH-TO-PRODUCT\s+HYPOTHESIS\b)"
)


def _load_json(relative: Path) -> Any:
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))


def _load_yaml(relative: Path) -> Any:
    return yaml.safe_load((ROOT / relative).read_text(encoding="utf-8"))


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _safe_locator(locator: Any) -> bool:
    if not isinstance(locator, str) or not locator or "\\" in locator:
        return False
    candidate = PurePosixPath(locator)
    return (
        not candidate.is_absolute()
        and "." not in candidate.parts
        and ".." not in candidate.parts
        and "://" not in locator
    )


def _resolve(locator: Any) -> Path | None:
    if not _safe_locator(locator):
        return None
    candidate = (ROOT / str(locator)).resolve()
    try:
        candidate.relative_to(ROOT.resolve())
    except ValueError:
        return None
    return candidate


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


def _artifact_references(value: Any) -> Iterable[Mapping[str, Any]]:
    """Yield repository artifact references without assuming one schema path."""

    for mapping in _iter_mappings(value):
        digest = mapping.get("digest")
        if (
            "locator" in mapping
            and isinstance(digest, Mapping)
            and digest.get("algorithm") == "SHA-256"
        ):
            yield mapping


def _immutable_frozen_errors() -> list[str]:
    errors: list[str] = []
    for relative, expected_digest in EXPECTED_MANIFEST_DIGESTS.items():
        path = ROOT / relative
        if not path.is_file():
            errors.append(f"missing frozen manifest: {relative.as_posix()}")
            continue
        actual = _sha256(path)
        if actual != expected_digest:
            errors.append(
                f"changed frozen manifest bytes: {relative.as_posix()} ({actual})"
            )
        manifest = json.loads(path.read_text(encoding="utf-8"))
        for reference in _artifact_references(manifest):
            digest = reference["digest"]
            if digest.get("status") not in {"RECORDED", "VERIFIED"}:
                continue
            target = _resolve(reference.get("locator"))
            label = str(reference.get("artifact_id", reference.get("locator")))
            if target is None or not target.is_file():
                errors.append(f"frozen artifact does not resolve: {label}")
            elif target.is_relative_to(ROOT / TAXONOMY_CASE_ROOT):
                # The taxonomy readiness lane is barred from opening case bytes
                # until a valid intake exists.  Their locators and manifest-held
                # digests remain visible as metadata, but this verifier does not
                # read or independently hash their contents.
                continue
            elif digest.get("scope") != "RAW_FILE_BYTES":
                errors.append(f"frozen artifact has the wrong digest scope: {label}")
            elif digest.get("value") != _sha256(target):
                errors.append(f"changed frozen artifact bytes: {label}")

    tool_provenance = _load_json(
        FORMAL_ROOT / "artifacts/tool-provenance.json"
    )
    analyzer = tool_provenance.get("analyzer")
    if not isinstance(analyzer, Mapping):
        errors.append("formal tool provenance lacks its analyzer binding")
    else:
        target = _resolve(analyzer.get("locator"))
        if target is None or not target.is_file():
            errors.append("formal frozen analyzer does not resolve")
        elif analyzer.get("raw_byte_sha256") != _sha256(target):
            errors.append("changed frozen analyzer bytes")
    return errors


def _manifest_outputs(manifest: Mapping[str, Any]) -> dict[str, Path]:
    result: dict[str, Path] = {}
    analyses = manifest.get("analyses")
    if not isinstance(analyses, list):
        return result
    for analysis in analyses:
        if not isinstance(analysis, Mapping):
            continue
        reference = analysis.get("planned_output_artifact")
        if not isinstance(reference, Mapping):
            continue
        analysis_id = analysis.get("analysis_id")
        locator = reference.get("locator")
        if isinstance(analysis_id, str) and _safe_locator(locator):
            result[analysis_id] = Path(str(locator))
    return result


def _registry_entries(relative: Path) -> list[Any]:
    document = _load_yaml(relative)
    if not isinstance(document, Mapping):
        return []
    entries = document.get("entries")
    return entries if isinstance(entries, list) else []


def _json_documents_below(relative: Path) -> dict[Path, Any]:
    directory = ROOT / relative
    if not directory.is_dir():
        return {}
    result: dict[Path, Any] = {}
    for path in sorted(directory.rglob("*.json")):
        result[path.relative_to(ROOT)] = json.loads(path.read_text(encoding="utf-8"))
    return result


def _readiness_status(document: Mapping[str, Any]) -> str | None:
    for key in ("readiness_status", "execution_status", "status", "decision"):
        value = document.get(key)
        if isinstance(value, str):
            return value.upper()
    return None


def _assigned_identity_values(document: Any) -> list[str]:
    values: list[str] = []
    for mapping in _iter_mappings(document):
        for key, value in mapping.items():
            lowered = str(key).lower()
            if "contributor_id" not in lowered and "adjudicator_id" not in lowered:
                continue
            if isinstance(value, str) and value:
                values.append(value)
            elif isinstance(value, list):
                values.extend(item for item in value if isinstance(item, str) and item)
    return values


def _taxonomy_blocked_document_errors(document: Mapping[str, Any]) -> list[str]:
    errors: list[str] = []
    status = _readiness_status(document)
    if status is not None and "BLOCKED" not in status:
        errors.append("taxonomy readiness is not truthfully BLOCKED")

    identities = _assigned_identity_values(document)
    if identities:
        errors.append(
            "taxonomy blocked readiness fabricates or pre-assigns contributor IDs"
        )
    if any(PLACEHOLDER_ID.search(value) for value in identities):
        errors.append("taxonomy readiness contains a placeholder contributor ID")

    for mapping in _iter_mappings(document):
        for key, value in mapping.items():
            lowered = str(key).lower()
            if "accessed" in lowered and value is not False:
                errors.append(
                    f"taxonomy blocked readiness admits prior access through {key}"
                )
            if lowered in {"case_access", "output_access", "result_access"} and str(
                value
            ).upper() not in {"NONE", "DENIED", "NOT_ACCESSED", "BLOCKED"}:
                errors.append(f"taxonomy blocked readiness admits access through {key}")
    return errors


def _valid_taxonomy_intake_errors(document: Mapping[str, Any]) -> list[str]:
    """Validate the minimum immutable intake boundary.

    Contributor identity cannot be established by inventing a plausible string.
    Every assigned identity therefore needs a repository-resolving, raw-byte
    digest-bound identity/eligibility artifact.  In the current program state
    no such artifacts have been accepted, so a truthful lane remains blocked.
    """

    errors: list[str] = []
    manifest_digest = EXPECTED_MANIFEST_DIGESTS[TAXONOMY_MANIFEST]
    exact = {
        "study_id": "LCMRP-FSTUDY-0001-M1-TAXONOMY",
        "study_record_id": "LCMRP-FSTUDYREC-0001-M1-TAXONOMY",
        "record_version": 1,
        "frozen_manifest_raw_byte_sha256": manifest_digest,
        "results_accessed_before_intake": False,
    }
    for key, value in exact.items():
        if document.get(key) != value:
            errors.append(f"taxonomy intake mismatch for {key}")

    assignments = document.get("role_assignments")
    rows = assignments if isinstance(assignments, list) else []
    roles = [row.get("role") for row in rows if isinstance(row, Mapping)]
    if roles.count("PRIMARY_ADJUDICATOR") != 2 or roles.count(
        "TIE_ADJUDICATOR"
    ) != 1:
        errors.append("taxonomy intake lacks exactly two primary and one tie role")

    identities: list[str] = []
    for row in rows:
        if not isinstance(row, Mapping):
            errors.append("taxonomy intake has a malformed role assignment")
            continue
        contributor_id = row.get("stable_contributor_id")
        if not isinstance(contributor_id, str) or not contributor_id:
            errors.append("taxonomy intake lacks a stable contributor ID")
            continue
        identities.append(contributor_id)
        if PLACEHOLDER_ID.search(contributor_id):
            errors.append("taxonomy intake uses a placeholder contributor ID")
        if any(
            row.get(field) is not value
            for field, value in (
                ("eligible", True),
                ("isolated", True),
                ("conflict_declared", False),
                ("is_protocol_or_case_author", False),
                ("is_freeze_authority", False),
            )
        ):
            errors.append(f"taxonomy intake eligibility failure for {contributor_id}")

        provenance = row.get("identity_provenance_artifact")
        if not isinstance(provenance, Mapping):
            errors.append(
                f"taxonomy intake has no verified identity provenance for {contributor_id}"
            )
            continue
        digest = provenance.get("digest")
        target = _resolve(provenance.get("locator"))
        if (
            not isinstance(digest, Mapping)
            or digest.get("algorithm") != "SHA-256"
            or digest.get("scope") != "RAW_FILE_BYTES"
            or digest.get("status") not in {"RECORDED", "VERIFIED"}
            or target is None
            or not target.is_file()
            or digest.get("value") != _sha256(target)
        ):
            errors.append(
                f"taxonomy intake identity provenance is not immutable for {contributor_id}"
            )
    if len(identities) != len(set(identities)):
        errors.append("taxonomy intake reuses one contributor across required roles")
    return errors


def _taxonomy_protocol_source_ids() -> set[str]:
    text = (ROOT / TAXONOMY_PROTOCOL).read_text(encoding="utf-8")
    return set(re.findall(r"\bSOURCE-M1-[A-Z0-9-]+\b", text))


def _taxonomy_manifest_source_ids() -> set[str]:
    manifest = _load_json(TAXONOMY_MANIFEST)
    sources = manifest.get("sources")
    if not isinstance(sources, list):
        return set()
    return {
        source["source_id"]
        for source in sources
        if isinstance(source, Mapping) and isinstance(source.get("source_id"), str)
    }


def _protocol_milestone_binding() -> tuple[str | None, str]:
    text = (ROOT / TAXONOMY_PROTOCOL).read_text(encoding="utf-8")
    matched = re.search(
        r"(?m)^\| `SOURCE-M1-MILESTONE` .*?SHA-256 `([a-f0-9]{64})`",
        text,
    )
    pinned = matched.group(1) if matched else None
    actual = _sha256(ROOT / "docs/program/M1_FOUNDATION.md")
    return pinned, actual


def _environment_freeze_metadata_gaps() -> list[str]:
    """Check only locations mandated by the already-bound environment."""

    environment = _load_json(TAXONOMY_ENVIRONMENT)
    manifest = _load_json(TAXONOMY_MANIFEST)
    attestation = _load_json(TAXONOMY_ATTESTATION)
    requirement = str(environment.get("freeze_requirement", "")).lower()
    gaps: list[str] = []
    frozen_metadata_text = json.dumps(
        {"manifest": manifest, "attestation": attestation}, sort_keys=True
    )

    lock_digest = _sha256(ROOT / "requirements-dev.lock")
    if "dependency-file digest" in requirement and lock_digest not in frozen_metadata_text:
        gaps.append("dependency-file digest absent from manifest/attestation")

    if "platform details" in requirement:
        platform_keys = {
            str(key).lower()
            for mapping in _iter_mappings({"manifest": manifest, "attestation": attestation})
            for key in mapping
        }
        if not {"platform", "operating_system", "architecture"}.intersection(
            platform_keys
        ):
            gaps.append("platform details absent from manifest/attestation")

    if "exact repository revision" in requirement:
        exact_revision = attestation.get("freeze_integration_revision")
        if not isinstance(exact_revision, str) or not re.fullmatch(
            r"[a-f0-9]{40}", exact_revision
        ):
            gaps.append("exact freeze-integration revision absent from attestation")

    environment_reference = next(
        (
            reference
            for reference in _artifact_references(manifest)
            if reference.get("locator") == TAXONOMY_ENVIRONMENT.as_posix()
        ),
        None,
    )
    if (
        "raw-byte digest of this artifact" in requirement
        and (
            not isinstance(environment_reference, Mapping)
            or environment_reference.get("digest", {}).get("value")
            != _sha256(ROOT / TAXONOMY_ENVIRONMENT)
        )
    ):
        gaps.append("environment raw-byte digest is not bound by the manifest")
    return gaps


def _attestation_inventory_inconsistencies() -> list[str]:
    readme = (ROOT / TAXONOMY_README).read_text(encoding="utf-8")
    attestation = _load_json(TAXONOMY_ATTESTATION)
    claims_inventory = bool(
        re.search(
            r"(?i)freeze-attestation artifact containing the artifact inventory, "
            r"raw-byte digests",
            readme,
        )
    )
    mappings = list(_iter_mappings(attestation))
    has_inventory = any(
        isinstance(mapping.get(key), list)
        for mapping in mappings
        for key in ("artifact_inventory", "artifacts", "frozen_artifacts")
    )
    has_artifact_digest = any(
        isinstance(mapping.get("digest"), Mapping)
        or isinstance(mapping.get("raw_byte_sha256"), str)
        for mapping in mappings
    )
    if claims_inventory and not (has_inventory and has_artifact_digest):
        return [
            "README describes an attestation artifact inventory/digest ledger "
            "that the attestation does not contain"
        ]
    return []


def _draft_component_lifecycle_inconsistencies() -> list[str]:
    result: list[str] = []
    for relative in TAXONOMY_COMPONENTS:
        document = _load_json(relative)
        if document.get("artifact_status") == "DRAFT_FREEZE_INTENT":
            result.append(
                f"{relative.as_posix()} remains self-labeled DRAFT_FREEZE_INTENT"
            )
    return result


def _intake_digest_contract_gaps() -> list[str]:
    configuration = _load_json(TAXONOMY_CONFIGURATION)
    intake = configuration.get("execution_intake")
    if not isinstance(intake, Mapping):
        return ["execution-intake contract is absent"]
    required_fields = "\n".join(str(item) for item in intake.get("required_fields", []))
    requires_raw_digest = bool(re.search(r"(?i)raw-byte SHA-256", required_fields))
    has_external_binding = any(
        isinstance(intake.get(field), str) and intake.get(field)
        for field in (
            "digest_receipt_locator",
            "digest_index_locator",
            "immutable_binding_locator",
        )
    )
    if requires_raw_digest and not has_external_binding:
        return [
            "intake requires its own raw-byte digest but declares no external "
            "receipt/index or non-self-referential digest scope"
        ]
    return []


def _self_referential_intake_digest_errors(document: Mapping[str, Any]) -> list[str]:
    for mapping in _iter_mappings(document):
        scope = str(mapping.get("scope", "")).upper()
        locator = mapping.get("locator")
        value = mapping.get("value", mapping.get("raw_byte_sha256"))
        if (
            locator == TAXONOMY_INTAKE.as_posix()
            and scope in {"RAW_FILE_BYTES", "WHOLE_RAW_FILE_BYTES"}
            and isinstance(value, str)
            and re.fullmatch(r"[a-f0-9]{64}", value)
        ):
            return [
                "execution intake embeds a self-referential whole-file digest; "
                "use a separately bound receipt/index"
            ]
    return []


def _taxonomy_state_errors(
    *,
    execution_documents: Mapping[Path, Any],
    existing_outputs: Iterable[Path],
    finding_entries: Iterable[Any],
    closeout_entries: Iterable[Any],
) -> list[str]:
    errors: list[str] = []
    intake = execution_documents.get(TAXONOMY_INTAKE)
    other_documents = {
        path: document
        for path, document in execution_documents.items()
        if path != TAXONOMY_INTAKE
    }

    if intake is None:
        for path, document in other_documents.items():
            if isinstance(document, Mapping):
                errors.extend(_taxonomy_blocked_document_errors(document))
            else:
                errors.append(f"taxonomy readiness is not an object: {path}")
        if list(existing_outputs):
            errors.append("taxonomy case/output work exists without an immutable intake")
    elif not isinstance(intake, Mapping):
        errors.append("taxonomy execution intake is not an object")
    else:
        errors.extend(_valid_taxonomy_intake_errors(intake))

    if list(finding_entries):
        errors.append("taxonomy findings are premature in the execution-readiness increment")
    if list(closeout_entries):
        errors.append("taxonomy closeout is premature before five atomic dispositions")
    return errors


def _expected_formal_input_digests() -> dict[str, str]:
    return {
        "manifest": _sha256(ROOT / FORMAL_MANIFEST),
        "formal_system": _sha256(ROOT / FORMAL_SYSTEM),
        "assumptions": _sha256(ROOT / FORMAL_ASSUMPTIONS),
        "propositions": _sha256(ROOT / FORMAL_PROPOSITIONS),
        "configuration": _sha256(ROOT / FORMAL_CONFIGURATION),
        "analyzer": _sha256(ROOT / FORMAL_ANALYZER),
    }


def _formal_provenance_errors(document: Mapping[str, Any]) -> list[str]:
    errors: list[str] = []
    for field, expected in FORMAL_IDENTITIES.items():
        if document.get(field) != expected:
            errors.append(f"formal raw result identity mismatch for {field}")
    if document.get("input_digests") != _expected_formal_input_digests():
        errors.append("formal raw result input digest/provenance mismatch")
    status = document.get("semantic_validity_status")
    if status != "REQUIRES-SEPARATE-HUMAN-ADJUDICATION":
        errors.append("formal raw result suppresses the semantic-review blocker")
    boundary = str(document.get("execution_boundary", ""))
    if not all(
        token in boundary.lower()
        for token in ("not proof", "validation", "human semantic")
    ):
        errors.append("formal raw result lacks the proof/validation boundary")
    return errors


def _row_ids(rows: Any, key: str) -> list[Any]:
    if not isinstance(rows, list):
        return []
    return [row.get(key) for row in rows if isinstance(row, Mapping)]


def _formal_retention_errors(document: Mapping[str, Any]) -> list[str]:
    """Reject missing rows, including negative/null/counterexample-bearing rows."""

    errors: list[str] = []
    formal_system = _load_json(FORMAL_SYSTEM)
    propositions = _load_json(FORMAL_PROPOSITIONS)

    expected_modules = {
        module["module_id"]
        for module in formal_system["modules"]
        if module.get("include_in_satisfiability", True) is True
    }
    module_rows = document.get("satisfiability")
    module_ids = _row_ids(module_rows, "module_id")
    if set(module_ids) != expected_modules or len(module_ids) != len(
        expected_modules
    ):
        errors.append("formal output suppresses or adds a satisfiability module row")
    for row in module_rows if isinstance(module_rows, list) else []:
        if not isinstance(row, Mapping) or not {
            "valuation_count",
            "satisfying_model_count",
            "first_satisfying_model",
        } <= set(row):
            errors.append("formal output omits a satisfiability count/model field")

    queries = propositions["semantic_queries"]
    expected_entailments = {
        query["proposition_id"]
        for query in queries
        if query["relation"] == "ENTAILMENT"
    }
    expected_non_entailments = {
        query["proposition_id"]
        for query in queries
        if query["relation"] == "NON_ENTAILMENT"
    }
    entailment_rows = document.get("intended_entailments")
    non_entailment_rows = document.get("non_entailments")
    entailment_ids = _row_ids(entailment_rows, "proposition_id")
    non_entailment_ids = _row_ids(non_entailment_rows, "proposition_id")
    if set(entailment_ids) != expected_entailments or len(entailment_ids) != len(
        expected_entailments
    ):
        errors.append("formal output suppresses or adds an entailment row")
    if set(non_entailment_ids) != expected_non_entailments or len(
        non_entailment_ids
    ) != len(expected_non_entailments):
        errors.append("formal output suppresses or adds a non-entailment row")
    for rows, value_key in (
        (entailment_rows, "holds_within_kernel"),
        (non_entailment_rows, "witness_retained"),
    ):
        for row in rows if isinstance(rows, list) else []:
            if not isinstance(row, Mapping) or not {
                "counterexample_or_witness",
                value_key,
            } <= set(row):
                errors.append("formal output suppresses a negative/null witness field")

    expected_invariants = set(propositions["invariant_independence_targets"])
    independence_rows = document.get("invariant_independence")
    independence_ids = _row_ids(independence_rows, "invariant_id")
    if set(independence_ids) != expected_invariants or len(independence_ids) != len(
        expected_invariants
    ):
        errors.append("formal output suppresses or adds an invariant-omission row")
    for row in independence_rows if isinstance(independence_rows, list) else []:
        if not isinstance(row, Mapping) or not {
            "independence_witness",
            "independent_within_kernel",
        } <= set(row):
            errors.append("formal output suppresses a null independence witness")

    expected_countermodels = {
        item["countermodel_id"] for item in propositions["named_countermodels"]
    }
    countermodel_rows = document.get("named_countermodels")
    countermodel_ids = _row_ids(countermodel_rows, "countermodel_id")
    if set(countermodel_ids) != expected_countermodels or len(countermodel_ids) != len(
        expected_countermodels
    ):
        errors.append("formal output suppresses or adds a named countermodel row")
    for row in countermodel_rows if isinstance(countermodel_rows, list) else []:
        if not isinstance(row, Mapping) or not {
            "constraints_satisfied",
            "witness_condition_holds",
            "assignment",
        } <= set(row):
            errors.append("formal output suppresses a countermodel disposition")
    return errors


def _execution_claim_errors(document: Any, label: str) -> list[str]:
    text = "\n".join(_iter_strings(document))
    errors: list[str] = []
    if AFFIRMATIVE_OVERCLAIM.search(text):
        errors.append(f"{label}: false proof/validation/maturity claim")
    if PRODUCT_COUPLING.search(text):
        errors.append(f"{label}: product-specific coupling")
    false_values = {
        "APPLIED",
        "AWARDED",
        "BENCHMARKED",
        "COMPLETE",
        "INTEGRATION_READY",
        "PRODUCTION_READY",
        "PROVEN",
        "VALIDATED",
    }
    for mapping in _iter_mappings(document):
        for key, value in mapping.items():
            lowered = str(key).lower()
            normalized = str(value).upper().replace("-", "_").replace(" ", "_")
            if (
                any(
                    marker in lowered
                    for marker in (
                        "evidence_label",
                        "maturity",
                        "proof_status",
                        "validation_status",
                        "production_ready",
                    )
                )
                and normalized in false_values
            ):
                errors.append(f"{label}: false proof/validation/maturity state")
            if (
                any(marker in lowered for marker in ("integration", "product", "deployment"))
                and isinstance(value, str)
                and "corpusstudio" in value.lower()
            ):
                errors.append(f"{label}: product-specific coupling")
    return errors


def _formal_result_set_errors(result_documents: Mapping[Path, Any]) -> list[str]:
    errors: list[str] = []
    allowed = {FORMAL_RAW_OUTPUT}
    unexpected = set(result_documents).difference(allowed)
    if unexpected:
        errors.append(
            "formal analyses 02-07 or a substituted result path exist before two "
            "independent semantic mappings: "
            + ", ".join(sorted(path.as_posix() for path in unexpected))
        )
    raw = result_documents.get(FORMAL_RAW_OUTPUT)
    if raw is not None:
        if not isinstance(raw, Mapping):
            errors.append("formal Analysis 01 raw result is not an object")
        else:
            errors.extend(_formal_provenance_errors(raw))
            errors.extend(_formal_retention_errors(raw))
            errors.extend(_execution_claim_errors(raw, "formal raw result"))
    return errors


def _formal_execution_metadata_errors() -> list[str]:
    errors: list[str] = []
    preflight = _load_json(FORMAL_PREFLIGHT_ATTESTATION)
    runtime = _load_json(FORMAL_RUNTIME_PROVENANCE)

    exact_identity = {
        "study_id": FORMAL_IDENTITIES["study_id"],
        "study_record_id": FORMAL_IDENTITIES["study_record_id"],
        "study_record_version": 1,
        "analysis_id": "ANALYSIS-FMO-01-SATISFIABILITY",
    }
    for label, document in (("preflight", preflight), ("runtime", runtime)):
        for field, expected in exact_identity.items():
            if document.get(field) != expected:
                errors.append(f"{label}: exact identity mismatch for {field}")
        errors.extend(_execution_claim_errors(document, label))

    if preflight.get("status") != "BLOCKED_NOT_RUN":
        errors.append("preflight does not preserve BLOCKED_NOT_RUN")
    if runtime.get("execution_status") != "NOT_RUN_BLOCKED_DURING_GUARD_PREFLIGHT":
        errors.append("runtime provenance does not preserve NOT_RUN/BLOCKED")
    if runtime.get("analyzer_invocation_count") != 0:
        errors.append("runtime provenance claims an analyzer invocation")
    if runtime.get("run_kernel_invocation_count") != 0:
        errors.append("runtime provenance claims a run_kernel invocation")

    probe = runtime.get("preflight_probe")
    expected_terminal_error = (
        "StudyGuardError: canonical index entry lacks artifact_digest.value"
    )
    if not isinstance(probe, Mapping):
        errors.append("runtime provenance lacks the guard-only probe")
    else:
        expected_probe = {
            "kind": "Guard-only Python import and function call",
            "entry_point_called": "enforce_frozen_manifest",
            "main_called": False,
            "run_kernel_called": False,
            "exit_code": 1,
            "terminal_error": expected_terminal_error,
            "output_files_created": 0,
        }
        for field, expected in expected_probe.items():
            if probe.get(field) != expected:
                errors.append(f"runtime guard-probe mismatch for {field}")

    configuration = _load_json(FORMAL_CONFIGURATION)
    if runtime.get("configured_analyzer_command") != configuration.get(
        "planned_invocation_after_freeze"
    ):
        errors.append("runtime provenance command differs from frozen configuration")
    if runtime.get("configured_analyzer_command_invoked") is not False:
        errors.append("runtime provenance does not preserve command non-invocation")
    if runtime.get("input_digests") != _expected_formal_input_digests():
        errors.append("runtime provenance input digests differ from frozen bytes")

    frozen_bindings = preflight.get("frozen_bindings")
    manifest = _load_json(FORMAL_MANIFEST)
    expected_references = {
        str(reference["locator"]): str(reference["digest"]["value"])
        for reference in _artifact_references(manifest)
        if reference["digest"].get("status") in {"RECORDED", "VERIFIED"}
    }
    if not isinstance(frozen_bindings, Mapping):
        errors.append("preflight lacks frozen bindings")
    else:
        live_registry_digest = _sha256(ROOT / "registry/foundational-studies.yaml")
        recorded_registry_digest = frozen_bindings.get("registry_raw_byte_sha256")
        if recorded_registry_digest != live_registry_digest:
            # Live registry may advance after digest-linked supersession of either
            # study while blocked formal preflight remains bound to its historical
            # registry snapshot. Allow divergence only when a SUPERSEDED historical
            # entry and a later ACTIVE successor exist for some admitted study.
            registry = _load_yaml(Path("registry/foundational-studies.yaml"))
            entries = registry.get("entries", []) if isinstance(registry, Mapping) else []
            by_id: dict[str, list[Mapping[str, Any]]] = {}
            for entry in entries:
                if not isinstance(entry, Mapping):
                    continue
                rid = entry.get("record_id")
                if isinstance(rid, str):
                    by_id.setdefault(rid, []).append(entry)
            supersession_present = False
            for group in by_id.values():
                superseded = any(e.get("registry_status") == "SUPERSEDED" for e in group)
                active_later = any(
                    e.get("registry_status") == "ACTIVE"
                    and isinstance(e.get("record_version"), int)
                    and e.get("record_version") > 1
                    for e in group
                )
                if superseded and active_later:
                    supersession_present = True
                    break
            if not (
                supersession_present
                and isinstance(recorded_registry_digest, str)
                and len(recorded_registry_digest) == 64
            ):
                errors.append("preflight registry digest mismatch")
        if frozen_bindings.get("canonical_manifest_raw_byte_sha256") != _sha256(
            ROOT / FORMAL_MANIFEST
        ):
            errors.append("preflight manifest digest mismatch")
        if frozen_bindings.get("immutable_reference_count") != len(
            expected_references
        ):
            errors.append("preflight immutable-reference count mismatch")
        if frozen_bindings.get("immutable_references") != expected_references:
            errors.append("preflight immutable-reference digest map mismatch")
        if frozen_bindings.get("analyzer_raw_byte_sha256") != _sha256(
            ROOT / FORMAL_ANALYZER
        ):
            errors.append("preflight analyzer digest mismatch")
        if frozen_bindings.get("analyzer_tool_provenance_digest_match") is not True:
            errors.append("preflight does not attest the tool/analyzer digest binding")

    runtime_target = preflight.get("runtime_target")
    runtime_observed = runtime.get("runtime")
    runtime_fields = (
        "python_implementation",
        "python_version",
        "python_executable",
        "operating_system",
        "kernel_release",
        "machine",
    )
    if not isinstance(runtime_target, Mapping):
        errors.append("preflight runtime target is missing")
    if not isinstance(runtime_observed, Mapping):
        errors.append("runtime provenance is missing")
    if isinstance(runtime_target, Mapping) and isinstance(runtime_observed, Mapping):
        for field in runtime_fields:
            if runtime_target.get(field) != runtime_observed.get(field):
                errors.append(f"historical runtime records disagree for {field}")

        environment = _load_json(FORMAL_ENVIRONMENT)
        for field in ("python_implementation", "python_version"):
            if runtime_target.get(field) != environment.get(field):
                errors.append(f"historical runtime differs from frozen environment for {field}")
        recorded_os_reference = " ".join(
            str(runtime_target.get(field, ""))
            for field in ("operating_system", "kernel_release", "machine")
        )
        if recorded_os_reference != environment.get("operating_system_reference"):
            errors.append("historical OS/kernel/machine differs from frozen environment")

        executable = runtime_target.get("python_executable")
        if (
            not isinstance(executable, str)
            or not executable
            or not Path(executable).is_absolute()
        ):
            errors.append("historical Python executable is not a nonempty absolute path")

    outputs = _manifest_outputs(manifest)
    planned_outputs = preflight.get("planned_outputs")
    if not isinstance(planned_outputs, Mapping):
        errors.append("preflight planned-output declaration is missing")
    else:
        if planned_outputs.get("count") != 7:
            errors.append("preflight planned-output count is not seven")
        if set(planned_outputs.get("locators", [])) != {
            path.as_posix() for path in outputs.values()
        }:
            errors.append("preflight output locators differ from the frozen manifest")
        if planned_outputs.get("all_absent_after_preflight") is not True:
            errors.append("preflight does not preserve output absence")

    output = runtime.get("output")
    if not isinstance(output, Mapping):
        errors.append("runtime output absence declaration is missing")
    elif any(
        (
            output.get("planned_locator") != FORMAL_RAW_OUTPUT.as_posix(),
            output.get("exists") is not False,
            output.get("raw_byte_sha256") is not None,
            output.get("bytes") is not None,
            output.get("copy_to_shared_workspace_performed") is not False,
        )
    ):
        errors.append("runtime output declaration is inconsistent with NOT_RUN")

    services = runtime.get("network_and_external_services")
    if not isinstance(services, Mapping):
        errors.append("runtime service-boundary declaration is missing")
    elif any(
        services.get(field) != 0
        for field in (
            "network_syscalls",
            "network_calls",
            "model_calls",
            "external_solver_calls",
            "cloud_service_calls",
            "storage_service_calls",
        )
    ) or services.get("analyzer_process_started") is not False:
        errors.append("runtime provenance reports undeclared execution/service activity")

    preflight_binding = preflight.get("public_main_binding")
    snapshot = runtime.get("snapshot")
    if isinstance(preflight_binding, Mapping) and isinstance(snapshot, Mapping):
        cross_checks = {
            "commit": preflight_binding.get("observed_public_main_commit"),
            "tree": preflight_binding.get("git_tree_id"),
            "tracked_entry_count": preflight_binding.get("tracked_entry_count"),
            "tracked_inventory_sha256": preflight_binding.get(
                "tracked_inventory_sha256"
            ),
        }
        for field, expected in cross_checks.items():
            if snapshot.get(field) != expected:
                errors.append(f"formal snapshot cross-record mismatch for {field}")
    else:
        errors.append("formal snapshot provenance is missing")
    return errors


def _minimal_retention_fixture() -> dict[str, Any]:
    """Create a shape-only fixture; this is not a computed study result."""

    formal_system = _load_json(FORMAL_SYSTEM)
    propositions = _load_json(FORMAL_PROPOSITIONS)
    return {
        "satisfiability": [
            {
                "module_id": module["module_id"],
                "valuation_count": None,
                "satisfying_model_count": None,
                "first_satisfying_model": None,
            }
            for module in formal_system["modules"]
            if module.get("include_in_satisfiability", True) is True
        ],
        "intended_entailments": [
            {
                "proposition_id": query["proposition_id"],
                "counterexample_or_witness": None,
                "holds_within_kernel": None,
            }
            for query in propositions["semantic_queries"]
            if query["relation"] == "ENTAILMENT"
        ],
        "non_entailments": [
            {
                "proposition_id": query["proposition_id"],
                "counterexample_or_witness": None,
                "witness_retained": None,
            }
            for query in propositions["semantic_queries"]
            if query["relation"] == "NON_ENTAILMENT"
        ],
        "invariant_independence": [
            {
                "invariant_id": invariant_id,
                "independence_witness": None,
                "independent_within_kernel": None,
            }
            for invariant_id in propositions["invariant_independence_targets"]
        ],
        "named_countermodels": [
            {
                "countermodel_id": item["countermodel_id"],
                "constraints_satisfied": None,
                "witness_condition_holds": None,
                "assignment": None,
            }
            for item in propositions["named_countermodels"]
        ],
    }


class M1StudyExecutionTests(unittest.TestCase):
    def test_01_frozen_manifests_and_permitted_bound_bytes_are_unchanged(self) -> None:
        self.assertEqual([], _immutable_frozen_errors())

    def test_02_taxonomy_truthful_blocked_state_has_no_intake_or_outputs(self) -> None:
        manifest = _load_json(TAXONOMY_MANIFEST)
        output_paths = _manifest_outputs(manifest).values()
        existing_outputs = [path for path in output_paths if (ROOT / path).exists()]
        execution_documents = _json_documents_below(TAXONOMY_ROOT / "execution")
        errors = _taxonomy_state_errors(
            execution_documents=execution_documents,
            existing_outputs=existing_outputs,
            finding_entries=_registry_entries(FINDING_REGISTRY),
            closeout_entries=_registry_entries(CLOSEOUT_REGISTRY),
        )
        self.assertEqual([], errors)

    def test_03_fabricated_or_placeholder_taxonomy_contributors_are_rejected(self) -> None:
        blocked_with_fake_identity = {
            "readiness_status": "BLOCKED",
            "assigned_adjudicator_id": "LCMRP-FAKE-ADJUDICATOR-0001",
            "results_accessed_before_intake": False,
        }
        errors = _taxonomy_blocked_document_errors(blocked_with_fake_identity)
        self.assertTrue(any("contributor" in error for error in errors), errors)

        fabricated_intake = {
            "study_id": "LCMRP-FSTUDY-0001-M1-TAXONOMY",
            "study_record_id": "LCMRP-FSTUDYREC-0001-M1-TAXONOMY",
            "record_version": 1,
            "frozen_manifest_raw_byte_sha256": EXPECTED_MANIFEST_DIGESTS[
                TAXONOMY_MANIFEST
            ],
            "results_accessed_before_intake": False,
            "role_assignments": [
                {
                    "role": role,
                    "stable_contributor_id": f"CONTRIBUTOR-{position:04d}",
                    "eligible": True,
                    "isolated": True,
                    "conflict_declared": False,
                    "is_protocol_or_case_author": False,
                    "is_freeze_authority": False,
                }
                for position, role in enumerate(
                    (
                        "PRIMARY_ADJUDICATOR",
                        "PRIMARY_ADJUDICATOR",
                        "TIE_ADJUDICATOR",
                    ),
                    start=1,
                )
            ],
        }
        errors = _valid_taxonomy_intake_errors(fabricated_intake)
        self.assertTrue(any("identity provenance" in error for error in errors), errors)

    def test_04_taxonomy_access_without_valid_intake_is_rejected(self) -> None:
        accessed = {
            TAXONOMY_ROOT / "execution/readiness.json": {
                "readiness_status": "BLOCKED",
                "cases_accessed": True,
            }
        }
        errors = _taxonomy_state_errors(
            execution_documents=accessed,
            existing_outputs=[],
            finding_entries=[],
            closeout_entries=[],
        )
        self.assertTrue(any("access" in error for error in errors), errors)

        errors = _taxonomy_state_errors(
            execution_documents={},
            existing_outputs=[TAXONOMY_ROOT / "outputs/forged.json"],
            finding_entries=[],
            closeout_entries=[],
        )
        self.assertTrue(any("without an immutable intake" in error for error in errors))

    def test_05_premature_taxonomy_findings_and_closeout_are_rejected(self) -> None:
        errors = _taxonomy_state_errors(
            execution_documents={},
            existing_outputs=[],
            finding_entries=[{"record_id": "LCMRP-FINDREC-FORGED"}],
            closeout_entries=[{"record_id": "LCMRP-FCLOSEREC-FORGED"}],
        )
        self.assertTrue(any("findings are premature" in error for error in errors))
        self.assertTrue(any("closeout is premature" in error for error in errors))

    def test_06_formal_result_set_is_absent_or_exact_analysis_01_only(self) -> None:
        documents = _json_documents_below(FORMAL_ROOT / "results")
        self.assertEqual([], _formal_result_set_errors(documents))

    def test_07_formal_result_path_substitution_is_rejected(self) -> None:
        substituted = {
            FORMAL_ROOT / "results/substituted-analysis-01.json": {
                **FORMAL_IDENTITIES,
                "input_digests": _expected_formal_input_digests(),
            }
        }
        errors = _formal_result_set_errors(substituted)
        self.assertTrue(any("substituted result path" in error for error in errors))

    def test_08_formal_execution_refuses_overwrite(self) -> None:
        configuration = _load_json(FORMAL_CONFIGURATION)
        self.assertEqual("CREATE-NEW-FAIL-IF-EXISTS", configuration["result_write_mode"])
        analyzer_source = (ROOT / FORMAL_ANALYZER).read_text(encoding="utf-8")
        self.assertIn('output_path.open("x"', analyzer_source)

        output = ROOT / FORMAL_RAW_OUTPUT
        if not output.is_file():
            return
        before = output.read_bytes()
        command = [
            sys.executable if token == "python" else token
            for token in configuration["planned_invocation_after_freeze"]
        ]
        completed = subprocess.run(
            command,
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertNotEqual(0, completed.returncode, completed.stdout)
        self.assertEqual(before, output.read_bytes())

    def test_09_formal_input_digest_or_provenance_mismatch_is_rejected(self) -> None:
        document = {
            **FORMAL_IDENTITIES,
            "input_digests": _expected_formal_input_digests(),
            "semantic_validity_status": "REQUIRES-SEPARATE-HUMAN-ADJUDICATION",
            "execution_boundary": (
                "This is not proof or validation; human semantic review is required."
            ),
        }
        self.assertEqual([], _formal_provenance_errors(document))
        mutated = copy.deepcopy(document)
        mutated["input_digests"]["manifest"] = "0" * 64
        errors = _formal_provenance_errors(mutated)
        self.assertTrue(any("digest/provenance mismatch" in error for error in errors))

    def test_10_analyses_02_through_07_require_independent_semantic_mappings(self) -> None:
        premature = {
            FORMAL_ROOT / "results/analysis-02-entailment.json": {
                "analysis_id": "ANALYSIS-FMO-02-ENTAILMENT",
                "semantic_mappings": [],
            }
        }
        errors = _formal_result_set_errors(premature)
        self.assertTrue(
            any("before two independent semantic mappings" in error for error in errors),
            errors,
        )

    def test_11_false_proof_validation_maturity_and_completion_claims_are_rejected(self) -> None:
        for claim in (
            "This output proves FMO-0.1.",
            "The result validates the memory object model.",
            "This analysis establishes scientific evidence.",
            "M1 is now complete.",
            "This awards a mechanism maturity label.",
        ):
            with self.subTest(claim=claim):
                errors = _execution_claim_errors({"claim": claim}, "mutation")
                self.assertTrue(any("false proof" in error for error in errors), errors)

    def test_12_product_specific_coupling_is_rejected(self) -> None:
        errors = _execution_claim_errors(
            {"decision": "Implement this result directly in CorpusStudio."},
            "mutation",
        )
        self.assertTrue(any("product-specific coupling" in error for error in errors))

    def test_13_negative_null_and_contradictory_rows_cannot_be_suppressed(self) -> None:
        complete_shape = _minimal_retention_fixture()
        self.assertEqual([], _formal_retention_errors(complete_shape))

        for field in (
            "satisfiability",
            "intended_entailments",
            "non_entailments",
            "invariant_independence",
            "named_countermodels",
        ):
            with self.subTest(field=field):
                mutated = copy.deepcopy(complete_shape)
                mutated[field] = mutated[field][1:]
                errors = _formal_retention_errors(mutated)
                self.assertTrue(any("suppresses" in error for error in errors), errors)

        mutated = copy.deepcopy(complete_shape)
        del mutated["non_entailments"][0]["counterexample_or_witness"]
        errors = _formal_retention_errors(mutated)
        self.assertTrue(any("negative/null witness" in error for error in errors), errors)

    def test_14_execution_increment_creates_no_finding_or_closeout_records(self) -> None:
        self.assertEqual([], _registry_entries(FINDING_REGISTRY))
        self.assertEqual([], _registry_entries(CLOSEOUT_REGISTRY))
        for relative in (FINDING_RECORD_ROOT, CLOSEOUT_RECORD_ROOT):
            directory = ROOT / relative
            if directory.is_dir():
                self.assertEqual([], sorted(directory.rglob("*.json")), relative)

    def test_15_taxonomy_protocol_manifest_source_set_mismatch_is_a_hard_blocker(
        self,
    ) -> None:
        protocol_ids = _taxonomy_protocol_source_ids()
        manifest_ids = _taxonomy_manifest_source_ids()
        self.assertEqual(
            {
                "SOURCE-M1-FOUNDATIONAL-CONTRACT",
                "SOURCE-M1-MILESTONE",
            },
            protocol_ids.difference(manifest_ids),
        )
        self.assertEqual(set(), manifest_ids.difference(protocol_ids))

    def test_16_stale_protocol_pinned_m1_foundation_digest_is_a_hard_blocker(
        self,
    ) -> None:
        pinned, actual = _protocol_milestone_binding()
        self.assertEqual(
            "473ea1b43eeac3661491d85008c898f2bd27b2c539bae4b901222563cc8654b6",
            pinned,
        )
        self.assertRegex(actual, r"\A[a-f0-9]{64}\Z")
        self.assertNotEqual(pinned, actual)

    def test_17_environment_mandated_freeze_metadata_gaps_are_hard_blockers(
        self,
    ) -> None:
        self.assertEqual(
            {
                "dependency-file digest absent from manifest/attestation",
                "platform details absent from manifest/attestation",
                "exact freeze-integration revision absent from attestation",
            },
            set(_environment_freeze_metadata_gaps()),
        )

    def test_18_attestation_inventory_and_draft_labels_are_documentation_lifecycle_inconsistencies(
        self,
    ) -> None:
        inventory = _attestation_inventory_inconsistencies()
        lifecycle = _draft_component_lifecycle_inconsistencies()
        self.assertEqual(1, len(inventory), inventory)
        self.assertEqual(
            {path.as_posix() for path in TAXONOMY_COMPONENTS},
            {item.split(" remains self-labeled", 1)[0] for item in lifecycle},
        )
        # These inconsistencies require a steward disposition/supersession, but
        # are kept separate from actor, source, and stale-digest hard blockers.
        self.assertTrue(all("DRAFT_FREEZE_INTENT" in item for item in lifecycle))

    def test_19_intake_digest_contract_must_be_non_self_referential(self) -> None:
        gaps = _intake_digest_contract_gaps()
        self.assertTrue(any("non-self-referential" in gap for gap in gaps), gaps)

        self_digest = {
            "immutable_digest": {
                "locator": TAXONOMY_INTAKE.as_posix(),
                "algorithm": "SHA-256",
                "scope": "RAW_FILE_BYTES",
                "value": "a" * 64,
            }
        }
        errors = _self_referential_intake_digest_errors(self_digest)
        self.assertTrue(any("self-referential" in error for error in errors), errors)

    def test_20_taxonomy_readiness_review_reports_all_blockers_without_claiming_a_result(
        self,
    ) -> None:
        text = (ROOT / TAXONOMY_READINESS_REVIEW).read_text(encoding="utf-8")
        for blocker in ("B1", "B2", "B3", "B4", "B5", "B6"):
            with self.subTest(blocker=blocker):
                self.assertRegex(text, rf"(?m)^### {blocker} \u2014 ")
        self.assertIn("BLOCKED \u2014 DO NOT START TAXONOMY EXECUTION", text)
        self.assertIn("not a scientific finding", text)
        self.assertIn("Blocking pending steward disposition", text)
        self.assertNotRegex(text, AFFIRMATIVE_OVERCLAIM)

    def test_21_formal_preflight_and_runtime_provenance_are_exact_and_consistent(
        self,
    ) -> None:
        execution_documents = _json_documents_below(FORMAL_ROOT / "execution")
        self.assertEqual(
            {FORMAL_PREFLIGHT_ATTESTATION, FORMAL_RUNTIME_PROVENANCE},
            set(execution_documents),
        )
        self.assertEqual([], _formal_execution_metadata_errors())

    def test_22_frozen_formal_guard_failure_is_independently_reproduced_without_analysis(
        self,
    ) -> None:
        registry = _load_yaml(Path("registry/foundational-studies.yaml"))
        entries = registry.get("entries", []) if isinstance(registry, Mapping) else []
        formal_entry = next(
            entry
            for entry in entries
            if entry.get("record_id") == FORMAL_IDENTITIES["study_record_id"]
        )
        self.assertEqual("ACTIVE", formal_entry["registry_status"])
        self.assertEqual(
            _sha256(ROOT / FORMAL_MANIFEST),
            formal_entry["artifact_digest"]["value"],
        )

        spec = importlib.util.spec_from_file_location(
            "lcmrp_frozen_fmo_analyzer_guard_probe",
            ROOT / FORMAL_ANALYZER,
        )
        self.assertIsNotNone(spec)
        self.assertIsNotNone(spec.loader if spec else None)
        module = importlib.util.module_from_spec(spec)
        assert spec is not None and spec.loader is not None
        spec.loader.exec_module(module)

        with self.assertRaisesRegex(
            module.StudyGuardError,
            r"canonical index entry lacks artifact_digest\.value",
        ):
            # Deliberately call only the failing index guard.  main() and
            # run_kernel() are never invoked, so no valuation or result exists.
            module.verify_manifest_index(ROOT.resolve(), (ROOT / FORMAL_MANIFEST))

        index_text = (ROOT / "registry/foundational-studies.yaml").read_text(
            encoding="utf-8"
        )
        digest_line = next(
            line
            for line in index_text.splitlines()
            if line.strip()
            == f"value: {EXPECTED_MANIFEST_DIGESTS[FORMAL_MANIFEST]}"
        )
        self.assertEqual(6, len(digest_line) - len(digest_line.lstrip(" ")))
        analyzer_text = (ROOT / FORMAL_ANALYZER).read_text(encoding="utf-8")
        self.assertIn(r'^        value:\s*', analyzer_text)

    def test_23_all_seven_formal_result_paths_remain_absent_after_guard_failure(
        self,
    ) -> None:
        manifest = _load_json(FORMAL_MANIFEST)
        outputs = _manifest_outputs(manifest)
        self.assertEqual(7, len(outputs))
        self.assertEqual(
            {
                "ANALYSIS-FMO-01-SATISFIABILITY",
                "ANALYSIS-FMO-02-ENTAILMENT",
                "ANALYSIS-FMO-03-NONENTAILMENT",
                "ANALYSIS-FMO-04-INVARIANT-INDEPENDENCE",
                "ANALYSIS-FMO-05-AUTHORITY",
                "ANALYSIS-FMO-06-DELETION",
                "ANALYSIS-FMO-07-SEMANTIC-VALIDITY",
            },
            set(outputs),
        )
        for analysis_id, relative in outputs.items():
            with self.subTest(analysis_id=analysis_id):
                self.assertFalse((ROOT / relative).exists(), relative)

    def test_24_blocked_formal_metadata_cannot_be_laundered_into_a_result(self) -> None:
        runtime = _load_json(FORMAL_RUNTIME_PROVENANCE)
        preflight = _load_json(FORMAL_PREFLIGHT_ATTESTATION)
        for document in (runtime, preflight):
            self.assertEqual([], _execution_claim_errors(document, "formal metadata"))

        forged = copy.deepcopy(runtime)
        forged["validation_status"] = "VALIDATED"
        forged["claim_boundary"].append("This result proves FMO-0.1.")
        errors = _execution_claim_errors(forged, "mutation")
        self.assertTrue(any("false proof" in error for error in errors), errors)


if __name__ == "__main__":
    unittest.main()
