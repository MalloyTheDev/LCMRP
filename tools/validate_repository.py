#!/usr/bin/env python3
"""Validate LCMRP governance, reproducibility, and milestone contracts.

This validator deliberately checks only research-program contracts. It does not
evaluate memory mechanisms, scientific claims, or product readiness.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from collections.abc import Mapping
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]

REQUIRED_PATHS = (
    "README.md",
    "AGENTS.md",
    "LICENSE",
    "requirements-dev.txt",
    "requirements-dev.lock",
    "CITATION.cff",
    "CONTRIBUTING.md",
    "GOVERNANCE.md",
    "SECURITY.md",
    ".github/pull_request_template.md",
    ".github/workflows/validate-m0.yml",
    "docs/program/PROGRAM_CHARTER_v0.1.md",
    "docs/program/M0_FOUNDATION.md",
    "docs/program/M1_FOUNDATION.md",
    "docs/program/RESEARCH_LAYERS.md",
    "docs/program/FOUNDATIONAL_STUDY_CONTRACT.md",
    "docs/program/EVIDENCE_LABELS.md",
    "docs/program/EVIDENCE_STATES.md",
    "docs/taxonomy/README.md",
    "docs/taxonomy/M1_PRIOR_ART_AND_COMPETING_TAXONOMIES.md",
    "docs/taxonomy/MEMORY_TAXONOMY_v0.1.md",
    "docs/taxonomy/FORMAL_MEMORY_OBJECT_MODEL_v0.1.md",
    "docs/benchmarks/README.md",
    "docs/experiments/README.md",
    "docs/security/README.md",
    "schemas/experiment-manifest.schema.json",
    "schemas/README.md",
    "schemas/evidence-record.schema.json",
    "schemas/foundational-study-manifest.schema.json",
    "schemas/research-finding-record.schema.json",
    "schemas/foundational-study-closeout.schema.json",
    "schemas/foundational-subject-registry.schema.json",
    "schemas/foundational-record-index.schema.json",
    "schemas/mechanism-registry.schema.json",
    "schemas/record-index.schema.json",
    "examples/experiment-manifest.example.json",
    "examples/README.md",
    "examples/evidence-record.example.json",
    "examples/foundational-study-manifest.example.json",
    "examples/research-finding-record.example.json",
    "examples/foundational-study-closeout.example.json",
    "examples/foundational-subject-registry.example.json",
    "examples/foundational-record-index.example.json",
    "examples/mechanism-registry.example.json",
    "templates/research-proposal.md",
    "templates/README.md",
    "templates/experiment-protocol.md",
    "templates/experiment-report.md",
    "templates/foundational-study-protocol.md",
    "templates/foundational-finding-report.md",
    "templates/foundational-study-closeout.md",
    "templates/threat-model.md",
    "registry/mechanisms.yaml",
    "registry/README.md",
    "registry/experiments.yaml",
    "registry/evidence.yaml",
    "registry/foundational-studies.yaml",
    "registry/research-findings.yaml",
    "registry/foundational-study-closeouts.yaml",
    "registry/foundational-subjects.yaml",
    "records/README.md",
    "references/README.md",
    "reviews/README.md",
    "reviews/M0_BOUNDARY_REVIEW_2026-07-20.md",
    "reviews/M0_FOUNDATIONAL_CONTRACT_REVIEW_2026-07-21.md",
    "reviews/M0_FINAL_ADVERSARIAL_REVIEW_2026-07-21.md",
    "reviews/M0_COMPLETION_DECISION_2026-07-21.md",
    "reviews/M1_LAUNCH_ADVERSARIAL_REVIEW_2026-07-21.md",
    "reviews/M1_LAUNCH_DECISION_2026-07-21.md",
    "tests/README.md",
    "tests/test_foundational_contracts.py",
    "tests/test_m1_launch.py",
)

REGISTRIES = {
    "registry/mechanisms.yaml": "mechanism_registry",
    "registry/experiments.yaml": "experiment_registry",
    "registry/evidence.yaml": "evidence_registry",
    "registry/foundational-studies.yaml": "foundational_study_registry",
    "registry/research-findings.yaml": "research_finding_registry",
    "registry/foundational-study-closeouts.yaml": "foundational_study_closeout_registry",
    "registry/foundational-subjects.yaml": "foundational_subject_registry",
}

CHARTER_INVARIANTS = (
    "LCMRP is not a CorpusStudio subsystem.",
    "Layer 1 — Foundational Research",
    "Layer 2 — Product-Independent Reference Implementations",
    "Layer 3 — Future CorpusStudio Integration",
    "RESEARCH-TO-PRODUCT HYPOTHESIS",
    "Negative results, null findings, and failed mechanisms are valid program outputs",
)

TEMPLATE_INVARIANTS = (
    "Future CorpusStudio Integration Implications",
    "RESEARCH-TO-PRODUCT HYPOTHESIS",
)

MARKDOWN_LINK = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")
PINNED_REQUIREMENT = re.compile(r"^([A-Za-z0-9_.-]+)==([^\s;]+)$")


class RepositoryValidationError(ValueError):
    """Raised when a repository contract is malformed or violated."""


def _reject_duplicate_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise RepositoryValidationError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def load_json(path: Path) -> Any:
    """Load JSON while rejecting duplicate object keys."""

    try:
        with path.open("r", encoding="utf-8") as handle:
            return json.load(handle, object_pairs_hook=_reject_duplicate_pairs)
    except (OSError, json.JSONDecodeError, RepositoryValidationError) as exc:
        raise RepositoryValidationError(f"{path}: {exc}") from exc


def load_yaml(path: Path) -> Any:
    """Safely load YAML while rejecting duplicate mapping keys."""

    try:
        import yaml
    except ImportError as exc:  # pragma: no cover - dependency failure path
        raise RepositoryValidationError(
            "PyYAML is required; install requirements-dev.txt"
        ) from exc

    class UniqueKeyLoader(yaml.SafeLoader):
        pass

    def construct_mapping(loader: UniqueKeyLoader, node: Any, deep: bool = False) -> Any:
        mapping: dict[Any, Any] = {}
        for key_node, value_node in node.value:
            key = loader.construct_object(key_node, deep=deep)
            if key in mapping:
                raise RepositoryValidationError(f"{path}: duplicate YAML key: {key}")
            mapping[key] = loader.construct_object(value_node, deep=deep)
        return mapping

    UniqueKeyLoader.add_constructor(
        yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
        construct_mapping,
    )

    try:
        with path.open("r", encoding="utf-8") as handle:
            return yaml.load(handle, Loader=UniqueKeyLoader)
    except (OSError, yaml.YAMLError, RepositoryValidationError) as exc:
        raise RepositoryValidationError(f"{path}: {exc}") from exc


def validate_required_paths(root: Path) -> list[str]:
    errors: list[str] = []
    for relative in REQUIRED_PATHS:
        path = root / relative
        if not path.is_file():
            errors.append(f"missing required file: {relative}")
        elif path.stat().st_size == 0:
            errors.append(f"required file is empty: {relative}")
    return errors


def _load_pinned_requirements(path: Path) -> tuple[dict[str, str], list[str]]:
    pins: dict[str, str] = {}
    errors: list[str] = []
    if not path.is_file():
        return pins, errors

    for line_number, raw_line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        match = PINNED_REQUIREMENT.fullmatch(line)
        if match is None:
            errors.append(f"{path.name}:{line_number}: dependency must use an exact == pin")
            continue
        name = match.group(1).lower().replace("_", "-")
        version = match.group(2)
        if name in pins:
            errors.append(f"{path.name}:{line_number}: duplicate dependency pin: {name}")
        pins[name] = version
    return pins, errors


def validate_dependency_lock(root: Path) -> list[str]:
    direct, errors = _load_pinned_requirements(root / "requirements-dev.txt")
    locked, lock_errors = _load_pinned_requirements(root / "requirements-dev.lock")
    errors.extend(lock_errors)
    for name, version in direct.items():
        if name not in locked:
            errors.append(f"requirements-dev.lock: missing direct dependency: {name}")
        elif locked[name] != version:
            errors.append(
                f"requirements-dev.lock: {name} is {locked[name]}, expected {version}"
            )
    return errors


def validate_schemas_and_examples(root: Path) -> list[str]:
    errors: list[str] = []
    try:
        from jsonschema import Draft202012Validator, FormatChecker
        from jsonschema.exceptions import SchemaError
    except ImportError:
        return ["jsonschema is required; install requirements-dev.txt"]

    schemas: dict[str, Any] = {}
    schema_ids: set[str] = set()
    for schema_path in sorted((root / "schemas").glob("*.schema.json")):
        schema_relative = schema_path.relative_to(root).as_posix()
        try:
            schema = load_json(schema_path)
        except RepositoryValidationError as exc:
            errors.append(str(exc))
            continue

        schemas[schema_relative] = schema

        if schema.get("$schema") != "https://json-schema.org/draft/2020-12/schema":
            errors.append(f"{schema_relative}: must declare JSON Schema draft 2020-12")

        schema_id = schema.get("$id")
        if not isinstance(schema_id, str) or not schema_id:
            errors.append(f"{schema_relative}: must declare a non-empty $id")
        elif schema_id in schema_ids:
            errors.append(f"{schema_relative}: duplicate schema $id: {schema_id}")
        else:
            schema_ids.add(schema_id)

        try:
            Draft202012Validator.check_schema(schema)
        except SchemaError as exc:
            errors.append(f"{schema_relative}: invalid schema: {exc.message}")

    for example_path in sorted((root / "examples").glob("*.example.json")):
        example_relative = example_path.relative_to(root).as_posix()
        schema_stem = example_path.name.removesuffix(".example.json")
        schema_relative = f"schemas/{schema_stem}.schema.json"
        schema = schemas.get(schema_relative)
        if schema is None:
            errors.append(
                f"{example_relative}: no matching schema named {schema_relative}"
            )
            continue
        try:
            instance = load_json(example_path)
        except RepositoryValidationError as exc:
            errors.append(str(exc))
            continue

        validator = Draft202012Validator(schema, format_checker=FormatChecker())
        for error in sorted(
            validator.iter_errors(instance),
            key=lambda item: tuple(str(part) for part in item.path),
        ):
            location = "/".join(str(part) for part in error.absolute_path) or "<root>"
            errors.append(f"{example_relative}:{location}: {error.message}")
        errors.extend(validate_registry_entry_semantics(instance, example_relative))

    for example_path in sorted((root / "examples").glob("*.json")):
        if example_path.name.endswith(".example.json"):
            continue
        try:
            load_json(example_path)
        except RepositoryValidationError as exc:
            errors.append(str(exc))

    return errors


def _is_ignored_validation_path(path: Path, root: Path) -> bool:
    relative_parts = path.relative_to(root).parts
    return any(part in {".git", ".venv", "__pycache__"} for part in relative_parts)


def validate_serialized_documents(root: Path) -> list[str]:
    """Parse every repository JSON/YAML document with duplicate-key rejection."""

    errors: list[str] = []
    for path in sorted(root.rglob("*.json")):
        if _is_ignored_validation_path(path, root):
            continue
        try:
            load_json(path)
        except RepositoryValidationError as exc:
            errors.append(str(exc))

    yaml_paths = (
        set(root.rglob("*.yaml"))
        | set(root.rglob("*.yml"))
        | set(root.rglob("*.cff"))
    )
    for path in sorted(yaml_paths):
        if _is_ignored_validation_path(path, root):
            continue
        try:
            load_yaml(path)
        except RepositoryValidationError as exc:
            errors.append(str(exc))
    return errors


def _iter_mappings(value: Any):
    if isinstance(value, Mapping):
        yield value
        for child in value.values():
            yield from _iter_mappings(child)
    elif isinstance(value, list):
        for child in value:
            yield from _iter_mappings(child)


def _resolve_local_artifact(root: Path, locator: str) -> Path | None:
    if "://" in locator or locator.startswith(("urn:", "doi:")):
        return None
    candidate = (root / locator).resolve()
    try:
        candidate.relative_to(root.resolve())
    except ValueError as exc:
        raise RepositoryValidationError(
            f"artifact locator escapes repository: {locator}"
        ) from exc
    return candidate


def _artifact_binding_differences(
    reference: Any,
    expected: Any,
) -> list[str]:
    """Return exact immutable-artifact fields that differ.

    Artifact identity is more than the surrounding subject/profile identifier.
    The locator, media/schema identity, version, and raw-byte digest must all bind
    to the same exact artifact.
    """

    if not isinstance(reference, Mapping) or not isinstance(expected, Mapping):
        return ["artifact"]

    differences: list[str] = []
    for field in (
        "artifact_id",
        "artifact_version",
        "schema_id",
        "locator",
        "media_type",
    ):
        if reference.get(field) != expected.get(field):
            differences.append(field)

    reference_digest = reference.get("digest")
    expected_digest = expected.get("digest")
    if not isinstance(reference_digest, Mapping) or not isinstance(expected_digest, Mapping):
        differences.append("digest")
        return differences
    for field in ("algorithm", "value", "scope"):
        if reference_digest.get(field) != expected_digest.get(field):
            differences.append(f"digest.{field}")
    return differences


def _registry_artifact_binding_differences(
    reference: Any,
    entry: Any,
) -> list[str]:
    """Compare an in-record immutable artifact reference with an index entry."""

    if not isinstance(reference, Mapping) or not isinstance(entry, Mapping):
        return ["artifact"]
    differences: list[str] = []
    if reference.get("artifact_version") != entry.get("record_version"):
        differences.append("artifact_version")
    if reference.get("schema_id") != entry.get("schema_id"):
        differences.append("schema_id")
    if reference.get("locator") != entry.get("artifact_path"):
        differences.append("locator")
    reference_digest = reference.get("digest")
    entry_digest = entry.get("artifact_digest")
    if not isinstance(reference_digest, Mapping) or not isinstance(entry_digest, Mapping):
        differences.append("digest")
    else:
        for field in ("algorithm", "value", "scope"):
            if reference_digest.get(field) != entry_digest.get(field):
                differences.append(f"digest.{field}")
    return differences


def _validate_foundational_finding_binding(
    root: Path,
    label: str,
    finding: Mapping[str, Any],
) -> list[str]:
    """Bind a foundational finding to the exact referenced study fields."""

    if finding.get("artifact_type") != "research_finding_record":
        return []

    study_reference = finding.get("study_reference")
    if not isinstance(study_reference, Mapping):
        return []
    manifest_artifact = study_reference.get("manifest_artifact")
    if not isinstance(manifest_artifact, Mapping):
        return []
    locator = manifest_artifact.get("locator")
    if not isinstance(locator, str):
        return []

    try:
        manifest_path = _resolve_local_artifact(root, locator)
    except RepositoryValidationError as exc:
        return [f"{label}: finding binding cannot resolve study manifest: {exc}"]
    binding_required = (
        finding.get("record_status") == "PUBLISHED"
        or finding.get("terminal_disposition") == "COMPLETED"
    )
    if manifest_path is None or not manifest_path.is_file():
        if binding_required:
            return [f"{label}: finding binding requires a resolvable study manifest"]
        return []
    try:
        manifest = load_json(manifest_path)
    except RepositoryValidationError:
        return []
    if not isinstance(manifest, Mapping) or manifest.get("artifact_type") != "foundational_study_manifest":
        return [f"{label}: finding binding target is not a foundational study manifest"]

    errors: list[str] = []

    if (
        finding.get("record_status") == "PUBLISHED"
        or finding.get("terminal_disposition") == "COMPLETED"
    ) and manifest.get("record_status") != "FROZEN":
        errors.append(
            f"{label}: finding binding requires a FROZEN study for a "
            "PUBLISHED or COMPLETED finding"
        )

    def compare(actual: Any, expected: Any, field: str) -> None:
        if actual != expected:
            errors.append(f"{label}: finding binding mismatch for {field}")

    compare(study_reference.get("study_id"), manifest.get("study_id"), "study_id")
    compare(
        study_reference.get("study_record_id"),
        manifest.get("study_record_id"),
        "study_record_id",
    )
    compare(
        study_reference.get("study_record_version"),
        manifest.get("record_version"),
        "study_record_version",
    )
    compare(
        manifest_artifact.get("schema_id"),
        "urn:lcmrp:schema:foundational-study-manifest:0.1.0",
        "study_manifest.schema_id",
    )

    subject_reference = finding.get("subject_reference")
    manifest_subject = manifest.get("subject")
    if isinstance(subject_reference, Mapping) and isinstance(manifest_subject, Mapping):
        for field in (
            "target_type",
            "subject_kind",
            "subject_id",
            "subject_series",
            "subject_version",
        ):
            compare(subject_reference.get(field), manifest_subject.get(field), f"subject.{field}")
        for field in _artifact_binding_differences(
            subject_reference.get("definition_artifact"),
            manifest_subject.get("definition_artifact"),
        ):
            errors.append(
                f"{label}: finding binding mismatch for "
                f"subject.definition_artifact.{field}"
            )

    profile_reference = finding.get("primary_method_profile_reference")
    manifest_profile = manifest.get("primary_method_profile")
    if isinstance(profile_reference, Mapping) and isinstance(manifest_profile, Mapping):
        profile_fields = {
            "profile_kind": "profile_kind",
            "profile_id": "profile_id",
            "profile_series": "profile_series",
            "profile_version": "profile_version",
        }
        for reference_field, manifest_field in profile_fields.items():
            compare(
                profile_reference.get(reference_field),
                manifest_profile.get(manifest_field),
                f"primary_method_profile.{reference_field}",
            )
        for field in _artifact_binding_differences(
            profile_reference.get("profile_artifact"),
            manifest_profile.get("profile_definition_artifact"),
        ):
            errors.append(
                f"{label}: finding binding mismatch for "
                f"primary_method_profile.profile_artifact.{field}"
            )

    analysis_reference = finding.get("analysis_reference")
    analyses = manifest.get("analyses")
    if isinstance(analysis_reference, Mapping) and isinstance(analyses, list):
        analysis_id = analysis_reference.get("analysis_id")
        matching_analysis = next(
            (
                analysis
                for analysis in analyses
                if isinstance(analysis, Mapping)
                and analysis.get("analysis_id") == analysis_id
            ),
            None,
        )
        if matching_analysis is None:
            errors.append(f"{label}: finding binding mismatch for analysis.analysis_id")
        else:
            compare(
                analysis_reference.get("analysis_mode"),
                matching_analysis.get("analysis_mode"),
                "analysis.analysis_mode",
            )

    return errors


def _validate_foundational_closeout_binding(
    root: Path,
    label: str,
    closeout: Mapping[str, Any],
) -> list[str]:
    """Resolve a closeout to one exact frozen study and its exact findings."""

    if closeout.get("artifact_type") != "foundational_study_closeout":
        return []

    errors: list[str] = []
    published = closeout.get("record_status") == "PUBLISHED"
    study_reference = closeout.get("study_reference")
    if not isinstance(study_reference, Mapping):
        return errors
    manifest_reference = study_reference.get("manifest_artifact")
    if not isinstance(manifest_reference, Mapping):
        return errors
    manifest_locator = manifest_reference.get("locator")
    if not isinstance(manifest_locator, str):
        return errors

    try:
        manifest_path = _resolve_local_artifact(root, manifest_locator)
    except RepositoryValidationError as exc:
        return [f"{label}: closeout cannot resolve study manifest: {exc}"]
    if manifest_path is None or not manifest_path.is_file():
        if published:
            errors.append(f"{label}: published closeout study manifest is unavailable")
        return errors
    try:
        manifest = load_json(manifest_path)
    except RepositoryValidationError:
        return errors
    if not isinstance(manifest, Mapping) or manifest.get("artifact_type") != "foundational_study_manifest":
        return [f"{label}: closeout target is not a foundational study manifest"]

    def compare(actual: Any, expected: Any, field: str) -> None:
        if actual != expected:
            errors.append(f"{label}: closeout binding mismatch for {field}")

    compare(study_reference.get("study_id"), manifest.get("study_id"), "study_id")
    compare(
        study_reference.get("study_record_id"),
        manifest.get("study_record_id"),
        "study_record_id",
    )
    compare(
        study_reference.get("study_record_version"),
        manifest.get("record_version"),
        "study_record_version",
    )
    if published and manifest.get("record_status") != "FROZEN":
        errors.append(f"{label}: published closeout requires a FROZEN study manifest")

    manifest_analyses = manifest.get("analyses")
    dispositions = closeout.get("analysis_dispositions")
    if not isinstance(manifest_analyses, list) or not isinstance(dispositions, list):
        return errors

    expected_modes = {
        analysis.get("analysis_id"): analysis.get("analysis_mode")
        for analysis in manifest_analyses
        if isinstance(analysis, Mapping)
    }
    disposition_ids = [
        disposition.get("analysis_id")
        for disposition in dispositions
        if isinstance(disposition, Mapping)
    ]
    if len(disposition_ids) != len(set(disposition_ids)):
        errors.append(f"{label}: closeout analysis disposition IDs must be unique")
    if published and set(disposition_ids) != set(expected_modes):
        errors.append(
            f"{label}: published closeout analysis IDs must exactly equal the "
            "frozen study analysis IDs"
        )

    referenced_findings: set[tuple[Any, Any]] = set()
    for index, disposition in enumerate(dispositions):
        if not isinstance(disposition, Mapping):
            continue
        analysis_id = disposition.get("analysis_id")
        if analysis_id in expected_modes:
            compare(
                disposition.get("analysis_mode"),
                expected_modes.get(analysis_id),
                f"analysis_dispositions/{index}/analysis_mode",
            )
        finding_key = (
            disposition.get("finding_record_id"),
            disposition.get("finding_record_version"),
        )
        if finding_key in referenced_findings:
            errors.append(f"{label}: closeout cannot reuse one finding record")
        referenced_findings.add(finding_key)

        finding_reference = disposition.get("finding_artifact")
        if not isinstance(finding_reference, Mapping):
            continue
        finding_locator = finding_reference.get("locator")
        if not isinstance(finding_locator, str):
            continue
        try:
            finding_path = _resolve_local_artifact(root, finding_locator)
        except RepositoryValidationError as exc:
            errors.append(f"{label}: closeout cannot resolve finding: {exc}")
            continue
        if finding_path is None or not finding_path.is_file():
            if published:
                errors.append(
                    f"{label}: published closeout finding is unavailable for {analysis_id!r}"
                )
            continue
        try:
            finding = load_json(finding_path)
        except RepositoryValidationError:
            continue
        if not isinstance(finding, Mapping) or finding.get("artifact_type") != "research_finding_record":
            errors.append(
                f"{label}: closeout finding target is not a research finding record"
            )
            continue
        compare(
            disposition.get("finding_id"),
            finding.get("finding_id"),
            f"analysis_dispositions/{index}/finding_id",
        )
        compare(
            disposition.get("finding_record_id"),
            finding.get("record_id"),
            f"analysis_dispositions/{index}/finding_record_id",
        )
        compare(
            disposition.get("finding_record_version"),
            finding.get("record_version"),
            f"analysis_dispositions/{index}/finding_record_version",
        )
        compare(
            disposition.get("terminal_disposition"),
            finding.get("terminal_disposition"),
            f"analysis_dispositions/{index}/terminal_disposition",
        )
        finding_analysis = finding.get("analysis_reference")
        if isinstance(finding_analysis, Mapping):
            compare(
                analysis_id,
                finding_analysis.get("analysis_id"),
                f"analysis_dispositions/{index}/analysis_id",
            )
            compare(
                disposition.get("analysis_mode"),
                finding_analysis.get("analysis_mode"),
                f"analysis_dispositions/{index}/finding_analysis_mode",
            )
        finding_study = finding.get("study_reference")
        if isinstance(finding_study, Mapping):
            for field in ("study_id", "study_record_id", "study_record_version"):
                compare(
                    finding_study.get(field),
                    study_reference.get(field),
                    f"analysis_dispositions/{index}/finding_study.{field}",
                )
            for field in _artifact_binding_differences(
                finding_study.get("manifest_artifact"),
                manifest_reference,
            ):
                errors.append(
                    f"{label}: closeout binding mismatch for "
                    f"analysis_dispositions/{index}/finding_study.manifest_artifact.{field}"
                )
        if published and finding.get("record_status") != "PUBLISHED":
            errors.append(
                f"{label}: published closeout requires a PUBLISHED finding for {analysis_id!r}"
            )

    return errors


def _validate_foundational_study_semantics(
    label: str,
    study: Mapping[str, Any],
) -> list[str]:
    """Check identifier uniqueness and profile-to-source role bindings."""

    if study.get("artifact_type") != "foundational_study_manifest":
        return []

    errors: list[str] = []
    analyses = study.get("analyses")
    if isinstance(analyses, list):
        analysis_ids = [
            analysis.get("analysis_id")
            for analysis in analyses
            if isinstance(analysis, Mapping)
        ]
        if len(analysis_ids) != len(set(analysis_ids)):
            errors.append(f"{label}: foundational study analysis IDs must be unique")

    sources = study.get("sources")
    if not isinstance(sources, list):
        return errors
    source_roles: dict[Any, Any] = {}
    for source in sources:
        if not isinstance(source, Mapping):
            continue
        source_id = source.get("source_id")
        if source_id in source_roles:
            errors.append(f"{label}: foundational study source IDs must be unique")
        source_roles[source_id] = source.get("role")

    profile = study.get("primary_method_profile")
    if not isinstance(profile, Mapping):
        return errors
    if profile.get("profile_kind") != "STRUCTURAL_OR_TAXONOMY_EVALUATION":
        return errors

    for field, expected_role in (
        ("positive_case_source_ids", "POSITIVE_CASES"),
        ("negative_case_source_ids", "NEGATIVE_CASES"),
    ):
        identifiers = profile.get(field)
        if not isinstance(identifiers, list):
            continue
        for source_id in identifiers:
            actual_role = source_roles.get(source_id)
            if actual_role != expected_role:
                errors.append(
                    f"{label}: foundational study {field} entry {source_id!r} "
                    f"must resolve to a source with role {expected_role}"
                )
    return errors


def validate_local_artifact_references(root: Path) -> list[str]:
    """Verify recorded local artifact digests and mechanism-version bindings."""

    errors: list[str] = []
    documents: list[tuple[Path, Any]] = []
    for path in sorted(root.rglob("*.json")):
        if _is_ignored_validation_path(path, root):
            continue
        try:
            documents.append((path, load_json(path)))
        except RepositoryValidationError:
            continue

    for document_path, document in documents:
        relative_document = document_path.relative_to(root).as_posix()
        for mapping in _iter_mappings(document):
            locator = mapping.get("locator")
            digest = mapping.get("digest")
            if not isinstance(locator, str) or not isinstance(digest, Mapping):
                continue
            status = digest.get("status")
            algorithm = digest.get("algorithm")
            expected = digest.get("value")
            if status not in {"RECORDED", "VERIFIED"}:
                continue
            if not isinstance(algorithm, str) or algorithm.lower().replace("-", "") != "sha256":
                continue
            try:
                artifact_path = _resolve_local_artifact(root, locator)
            except RepositoryValidationError as exc:
                errors.append(f"{relative_document}: {exc}")
                continue
            if artifact_path is None:
                continue
            if not artifact_path.is_file():
                errors.append(f"{relative_document}: recorded artifact is missing: {locator}")
                continue
            actual = hashlib.sha256(artifact_path.read_bytes()).hexdigest()
            if expected != actual:
                errors.append(
                    f"{relative_document}: recorded SHA-256 does not match {locator}"
                )

        if isinstance(document, Mapping):
            errors.extend(
                _validate_foundational_study_semantics(
                    relative_document,
                    document,
                )
            )
            errors.extend(
                _validate_foundational_finding_binding(
                    root,
                    relative_document,
                    document,
                )
            )
            errors.extend(
                _validate_foundational_closeout_binding(
                    root,
                    relative_document,
                    document,
                )
            )

        mechanism_versions = document.get("mechanism_versions") if isinstance(document, Mapping) else None
        if not isinstance(mechanism_versions, list):
            continue
        for index, mechanism_reference in enumerate(mechanism_versions):
            if not isinstance(mechanism_reference, Mapping):
                continue
            artifact_reference = mechanism_reference.get("mechanism_artifact")
            if not isinstance(artifact_reference, Mapping):
                continue
            locator = artifact_reference.get("locator")
            if not isinstance(locator, str):
                continue
            try:
                artifact_path = _resolve_local_artifact(root, locator)
            except RepositoryValidationError as exc:
                errors.append(f"{relative_document}: {exc}")
                continue
            if artifact_path is None or not artifact_path.is_file():
                continue
            try:
                registry = load_json(artifact_path)
            except RepositoryValidationError:
                continue
            entries = registry.get("entries") if isinstance(registry, Mapping) else None
            if not isinstance(entries, list):
                errors.append(
                    f"{relative_document}:mechanism_versions/{index}: locator is not a mechanism registry"
                )
                continue
            expected_id = mechanism_reference.get("mechanism_id")
            expected_version = mechanism_reference.get("mechanism_version")
            if not any(
                isinstance(entry, Mapping)
                and entry.get("mechanism_id") == expected_id
                and entry.get("mechanism_version") == expected_version
                for entry in entries
            ):
                errors.append(
                    f"{relative_document}:mechanism_versions/{index}: referenced mechanism ID/version is absent from {locator}"
                )
    return errors


def validate_registry_entry_semantics(registry: Any, label: str) -> list[str]:
    """Check identifier uniqueness and append-only version lineage."""

    if not isinstance(registry, Mapping) or not isinstance(registry.get("entries"), list):
        return []
    registry_type = registry.get("registry_type")
    if registry_type == "mechanism_registry":
        id_field, version_field = "mechanism_id", "mechanism_version"
    elif registry_type == "foundational_subject_registry":
        id_field, version_field = "subject_id", "subject_version"
    elif registry_type in {
        "experiment_registry",
        "evidence_registry",
        "foundational_study_registry",
        "research_finding_registry",
        "foundational_study_closeout_registry",
    }:
        id_field, version_field = "record_id", "record_version"
    else:
        return []

    errors: list[str] = []
    keyed_entries: dict[tuple[Any, Any], Mapping[str, Any]] = {}
    for index, entry in enumerate(registry["entries"]):
        if not isinstance(entry, Mapping):
            continue
        key = (entry.get(id_field), entry.get(version_field))
        if key in keyed_entries:
            errors.append(
                f"{label}:entries/{index}: duplicate {id_field}/{version_field}: {key!r}"
            )
        keyed_entries[key] = entry

    if registry_type == "foundational_subject_registry":
        active_by_subject: dict[Any, int] = {}
        subject_series: dict[Any, Any] = {}
        subject_kinds: dict[Any, Any] = {}
        series_owner: dict[Any, Any] = {}
        for index, entry in enumerate(registry["entries"]):
            if not isinstance(entry, Mapping):
                continue
            subject_id = entry.get("subject_id")
            series = entry.get("subject_series")
            kind = entry.get("subject_kind")
            version = entry.get("subject_version")
            if subject_id in subject_series and subject_series[subject_id] != series:
                errors.append(
                    f"{label}:entries/{index}: subject series must remain stable across versions"
                )
            subject_series.setdefault(subject_id, series)
            if subject_id in subject_kinds and subject_kinds[subject_id] != kind:
                errors.append(
                    f"{label}:entries/{index}: subject kind must remain stable across versions"
                )
            subject_kinds.setdefault(subject_id, kind)
            if series in series_owner and series_owner[series] != subject_id:
                errors.append(
                    f"{label}:entries/{index}: subject series cannot identify multiple subject IDs"
                )
            series_owner.setdefault(series, subject_id)
            if entry.get("entry_status") == "ACTIVE":
                active_by_subject[subject_id] = active_by_subject.get(subject_id, 0) + 1

            definition_artifact = entry.get("definition_artifact")
            if (
                isinstance(definition_artifact, Mapping)
                and isinstance(version, int)
                and definition_artifact.get("artifact_version") != version
            ):
                errors.append(
                    f"{label}:entries/{index}: definition artifact version must equal subject version"
                )
            if not isinstance(version, int) or version <= 1:
                continue
            previous_version = entry.get("supersedes_subject_version")
            if not isinstance(previous_version, int) or previous_version >= version:
                errors.append(
                    f"{label}:entries/{index}: superseded subject version must be lower than the new version"
                )
                continue
            previous = keyed_entries.get((subject_id, previous_version))
            if previous is None:
                errors.append(
                    f"{label}:entries/{index}: superseded subject version is absent from registry"
                )
                continue
            previous_artifact = previous.get("definition_artifact")
            previous_digest = (
                previous_artifact.get("digest")
                if isinstance(previous_artifact, Mapping)
                else None
            )
            supersedes_digest = entry.get("supersedes_definition_digest")
            if (
                isinstance(previous_digest, Mapping)
                and isinstance(supersedes_digest, Mapping)
                and previous_digest.get("value") != supersedes_digest.get("value")
            ):
                errors.append(
                    f"{label}:entries/{index}: supersession digest does not match prior subject definition artifact"
                )

        for subject_id, count in active_by_subject.items():
            if count > 1:
                errors.append(
                    f"{label}: subject {subject_id!r} has more than one ACTIVE version"
                )
        return errors

    if registry_type in {
        "experiment_registry",
        "evidence_registry",
        "foundational_study_registry",
        "research_finding_registry",
        "foundational_study_closeout_registry",
    }:
        active_versions: dict[Any, int] = {}
        for entry in registry["entries"]:
            if isinstance(entry, Mapping) and entry.get("registry_status") == "ACTIVE":
                record_id = entry.get("record_id")
                active_versions[record_id] = active_versions.get(record_id, 0) + 1
        for record_id, count in active_versions.items():
            if count > 1:
                errors.append(
                    f"{label}: record {record_id!r} has more than one ACTIVE version"
                )

    if registry_type == "mechanism_registry":
        active_mechanisms: dict[Any, int] = {}
        for entry in registry["entries"]:
            if isinstance(entry, Mapping) and entry.get("entry_status") == "ACTIVE":
                mechanism_id = entry.get("mechanism_id")
                active_mechanisms[mechanism_id] = active_mechanisms.get(mechanism_id, 0) + 1
        for mechanism_id, count in active_mechanisms.items():
            if count > 1:
                errors.append(
                    f"{label}: mechanism {mechanism_id!r} has more than one ACTIVE version"
                )

    if registry_type != "mechanism_registry":
        return errors

    for index, entry in enumerate(registry["entries"]):
        if not isinstance(entry, Mapping):
            continue
        version = entry.get("mechanism_version")
        if not isinstance(version, int) or version <= 1:
            continue
        previous_version = entry.get("supersedes_mechanism_version")
        if not isinstance(previous_version, int) or previous_version >= version:
            errors.append(
                f"{label}:entries/{index}: superseded mechanism version must be lower than the new version"
            )
            continue
        previous = keyed_entries.get((entry.get("mechanism_id"), previous_version))
        if previous is None:
            errors.append(
                f"{label}:entries/{index}: superseded mechanism version is absent from registry"
            )
            continue
        supersedes_digest = entry.get("supersedes_artifact_digest")
        previous_artifact = previous.get("definition_artifact")
        previous_digest = (
            previous_artifact.get("digest")
            if isinstance(previous_artifact, Mapping)
            else None
        )
        if (
            isinstance(supersedes_digest, Mapping)
            and isinstance(previous_digest, Mapping)
            and supersedes_digest.get("value") != previous_digest.get("value")
        ):
            errors.append(
                f"{label}:entries/{index}: supersession digest does not match prior definition artifact"
            )
    return errors


def _load_registry_if_present(root: Path, relative: str) -> Mapping[str, Any] | None:
    path = root / relative
    if not path.is_file():
        return None
    try:
        registry = load_yaml(path)
    except RepositoryValidationError:
        return None
    return registry if isinstance(registry, Mapping) else None


def _load_indexed_artifact(
    root: Path,
    entry: Mapping[str, Any],
) -> Mapping[str, Any] | None:
    path_value = entry.get("artifact_path")
    if not isinstance(path_value, str):
        return None
    path = (root / path_value).resolve()
    try:
        path.relative_to(root.resolve())
    except ValueError:
        return None
    if not path.is_file():
        return None
    try:
        artifact = load_json(path)
    except RepositoryValidationError:
        return None
    return artifact if isinstance(artifact, Mapping) else None


def _validate_foundational_registry_relationships(root: Path) -> list[str]:
    """Validate subject, study, finding, and closeout registry relationships."""

    errors: list[str] = []
    experiment_registry = _load_registry_if_present(root, "registry/experiments.yaml")
    evidence_registry = _load_registry_if_present(root, "registry/evidence.yaml")
    subject_registry = _load_registry_if_present(root, "registry/foundational-subjects.yaml")
    study_registry = _load_registry_if_present(root, "registry/foundational-studies.yaml")
    finding_registry = _load_registry_if_present(root, "registry/research-findings.yaml")
    closeout_registry = _load_registry_if_present(
        root,
        "registry/foundational-study-closeouts.yaml",
    )

    subject_entries: dict[tuple[Any, Any], Mapping[str, Any]] = {}
    if isinstance(subject_registry, Mapping) and isinstance(subject_registry.get("entries"), list):
        for entry in subject_registry["entries"]:
            if isinstance(entry, Mapping):
                subject_entries[(entry.get("subject_id"), entry.get("subject_version"))] = entry

    active_studies: dict[tuple[Any, Any], tuple[Mapping[str, Any], Mapping[str, Any]]] = {}
    profile_artifacts: dict[tuple[Any, Any, Any], Mapping[str, Any]] = {}
    if isinstance(study_registry, Mapping) and isinstance(study_registry.get("entries"), list):
        for index, entry in enumerate(study_registry["entries"]):
            if not isinstance(entry, Mapping):
                continue
            study = _load_indexed_artifact(root, entry)
            if study is None:
                continue
            if entry.get("registry_status") == "ACTIVE":
                study_key = (entry.get("record_id"), entry.get("record_version"))
                active_studies[study_key] = (entry, study)
            if study.get("record_status") != "FROZEN":
                continue

            subject = study.get("subject")
            if isinstance(subject, Mapping):
                subject_key = (subject.get("subject_id"), subject.get("subject_version"))
                registered_subject = subject_entries.get(subject_key)
                if registered_subject is None:
                    errors.append(
                        f"registry/foundational-studies.yaml:entries/{index}: indexed frozen "
                        "study subject ID/version is absent from foundational-subjects.yaml"
                    )
                else:
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
                        if subject.get(field) != registered_subject.get(field):
                            errors.append(
                                f"registry/foundational-studies.yaml:entries/{index}: "
                                f"registered subject mismatch for {field}"
                            )
                    for field in _artifact_binding_differences(
                        subject.get("definition_artifact"),
                        registered_subject.get("definition_artifact"),
                    ):
                        errors.append(
                            f"registry/foundational-studies.yaml:entries/{index}: "
                            f"registered subject definition artifact mismatch for {field}"
                        )

            profile = study.get("primary_method_profile")
            if isinstance(profile, Mapping):
                profile_key = (
                    profile.get("profile_id"),
                    profile.get("profile_series"),
                    profile.get("profile_version"),
                )
                profile_artifact = profile.get("profile_definition_artifact")
                existing_artifact = profile_artifacts.get(profile_key)
                if isinstance(existing_artifact, Mapping):
                    differences = _artifact_binding_differences(
                        profile_artifact,
                        existing_artifact,
                    )
                    if differences:
                        errors.append(
                            f"registry/foundational-studies.yaml:entries/{index}: exact "
                            "method profile identity resolves to divergent definition artifacts"
                        )
                elif isinstance(profile_artifact, Mapping):
                    profile_artifacts[profile_key] = profile_artifact

    active_findings: dict[tuple[Any, Any], tuple[Mapping[str, Any], Mapping[str, Any]]] = {}
    finding_analysis_keys: dict[tuple[Any, Any, Any], list[int]] = {}
    if isinstance(finding_registry, Mapping) and isinstance(finding_registry.get("entries"), list):
        for index, entry in enumerate(finding_registry["entries"]):
            if not isinstance(entry, Mapping) or entry.get("registry_status") != "ACTIVE":
                continue
            finding = _load_indexed_artifact(root, entry)
            if finding is None:
                continue
            finding_key = (entry.get("record_id"), entry.get("record_version"))
            active_findings[finding_key] = (entry, finding)
            study_reference = finding.get("study_reference")
            analysis_reference = finding.get("analysis_reference")
            if isinstance(study_reference, Mapping) and isinstance(analysis_reference, Mapping):
                study_key = (
                    study_reference.get("study_record_id"),
                    study_reference.get("study_record_version"),
                )
                if study_key not in active_studies:
                    errors.append(
                        f"registry/research-findings.yaml:entries/{index}: ACTIVE finding "
                        "must reference an ACTIVE frozen study record"
                    )
                else:
                    study_entry, _study = active_studies[study_key]
                    for field in _registry_artifact_binding_differences(
                        study_reference.get("manifest_artifact"),
                        study_entry,
                    ):
                        errors.append(
                            f"registry/research-findings.yaml:entries/{index}: ACTIVE "
                            f"finding study index binding mismatch for {field}"
                        )
                analysis_key = (
                    study_reference.get("study_record_id"),
                    study_reference.get("study_record_version"),
                    analysis_reference.get("analysis_id"),
                )
                finding_analysis_keys.setdefault(analysis_key, []).append(index)

    for analysis_key, indexes in finding_analysis_keys.items():
        if len(indexes) > 1:
            errors.append(
                "registry/research-findings.yaml: more than one ACTIVE finding exists "
                f"for exact study analysis {analysis_key!r}"
            )

    active_closeout_studies: dict[tuple[Any, Any], list[int]] = {}
    if isinstance(closeout_registry, Mapping) and isinstance(closeout_registry.get("entries"), list):
        for index, entry in enumerate(closeout_registry["entries"]):
            if not isinstance(entry, Mapping) or entry.get("registry_status") != "ACTIVE":
                continue
            closeout = _load_indexed_artifact(root, entry)
            if closeout is None:
                continue
            study_reference = closeout.get("study_reference")
            if not isinstance(study_reference, Mapping):
                continue
            study_key = (
                study_reference.get("study_record_id"),
                study_reference.get("study_record_version"),
            )
            active_closeout_studies.setdefault(study_key, []).append(index)
            indexed_study = active_studies.get(study_key)
            if indexed_study is None:
                errors.append(
                    f"registry/foundational-study-closeouts.yaml:entries/{index}: ACTIVE "
                    "closeout must reference an ACTIVE frozen study record"
                )
            else:
                study_entry, _study = indexed_study
                differences = _registry_artifact_binding_differences(
                    study_reference.get("manifest_artifact"),
                    study_entry,
                )
                for field in differences:
                    errors.append(
                        f"registry/foundational-study-closeouts.yaml:entries/{index}: "
                        f"closeout study index binding mismatch for {field}"
                    )

            dispositions = closeout.get("analysis_dispositions")
            if not isinstance(dispositions, list):
                continue
            for disposition_index, disposition in enumerate(dispositions):
                if not isinstance(disposition, Mapping):
                    continue
                finding_key = (
                    disposition.get("finding_record_id"),
                    disposition.get("finding_record_version"),
                )
                indexed_finding = active_findings.get(finding_key)
                if indexed_finding is None:
                    errors.append(
                        f"registry/foundational-study-closeouts.yaml:entries/{index}: "
                        f"analysis_dispositions/{disposition_index} must resolve to an "
                        "ACTIVE published finding"
                    )
                    continue
                finding_entry, _finding = indexed_finding
                differences = _registry_artifact_binding_differences(
                    disposition.get("finding_artifact"),
                    finding_entry,
                )
                for field in differences:
                    errors.append(
                        f"registry/foundational-study-closeouts.yaml:entries/{index}: "
                        f"analysis_dispositions/{disposition_index} finding index binding "
                        f"mismatch for {field}"
                    )

    for study_key, indexes in active_closeout_studies.items():
        if len(indexes) > 1:
            errors.append(
                "registry/foundational-study-closeouts.yaml: more than one ACTIVE closeout "
                f"exists for exact study record {study_key!r}"
            )

    for relative_directory, registry, registry_label in (
        ("records/experiments", experiment_registry, "registry/experiments.yaml"),
        ("records/evidence", evidence_registry, "registry/evidence.yaml"),
        (
            "records/foundational/studies",
            study_registry,
            "registry/foundational-studies.yaml",
        ),
        (
            "records/foundational/findings",
            finding_registry,
            "registry/research-findings.yaml",
        ),
        (
            "records/foundational/closeouts",
            closeout_registry,
            "registry/foundational-study-closeouts.yaml",
        ),
    ):
        indexed_paths: set[str] = set()
        if isinstance(registry, Mapping) and isinstance(registry.get("entries"), list):
            indexed_paths = {
                entry.get("artifact_path")
                for entry in registry["entries"]
                if isinstance(entry, Mapping) and isinstance(entry.get("artifact_path"), str)
            }
        directory = root / relative_directory
        if not directory.is_dir():
            continue
        for artifact_path in sorted(directory.rglob("*.json")):
            relative_path = artifact_path.relative_to(root).as_posix()
            if relative_path not in indexed_paths:
                errors.append(
                    f"{registry_label}: canonical record is not indexed: {relative_path}"
                )

    return errors


def validate_registries(root: Path) -> list[str]:
    errors: list[str] = []
    try:
        from jsonschema import Draft202012Validator, FormatChecker
    except ImportError:
        return ["jsonschema is required; install requirements-dev.txt"]

    schema_paths_by_registry = {
        "mechanism_registry": root / "schemas/mechanism-registry.schema.json",
        "experiment_registry": root / "schemas/record-index.schema.json",
        "evidence_registry": root / "schemas/record-index.schema.json",
        "foundational_study_registry": root / "schemas/foundational-record-index.schema.json",
        "research_finding_registry": root / "schemas/foundational-record-index.schema.json",
        "foundational_study_closeout_registry": root / "schemas/foundational-record-index.schema.json",
        "foundational_subject_registry": root / "schemas/foundational-subject-registry.schema.json",
    }
    artifact_schemas: dict[str, Any] = {}
    for schema_path in sorted((root / "schemas").glob("*.schema.json")):
        try:
            schema = load_json(schema_path)
        except RepositoryValidationError:
            continue
        schema_id = schema.get("$id")
        if isinstance(schema_id, str):
            artifact_schemas[schema_id] = schema

    for relative, expected_type in REGISTRIES.items():
        path = root / relative
        if not path.is_file():
            continue
        try:
            registry = load_yaml(path)
        except RepositoryValidationError as exc:
            errors.append(str(exc))
            continue

        if not isinstance(registry, Mapping):
            errors.append(f"{relative}: top level must be a mapping")
            continue
        if not registry.get("schema_version"):
            errors.append(f"{relative}: schema_version is required")
        if registry.get("registry_type") != expected_type:
            errors.append(
                f"{relative}: registry_type must be {expected_type!r}"
            )
        if "entries" not in registry or not isinstance(registry["entries"], list):
            errors.append(f"{relative}: entries must be a list")
        elif any(not isinstance(entry, Mapping) for entry in registry["entries"]):
            errors.append(f"{relative}: every entry must be a mapping")

        unknown_keys = set(registry) - {
            "schema_version",
            "artifact_type",
            "registry_type",
            "entries",
        }
        if unknown_keys:
            errors.append(
                f"{relative}: unknown top-level keys: {', '.join(sorted(unknown_keys))}"
            )
        errors.extend(validate_registry_entry_semantics(registry, relative))

        registry_schema_path = schema_paths_by_registry[expected_type]
        if registry_schema_path.is_file():
            try:
                registry_schema = load_json(registry_schema_path)
                validator = Draft202012Validator(
                    registry_schema,
                    format_checker=FormatChecker(),
                )
                for error in sorted(
                    validator.iter_errors(registry),
                    key=lambda item: tuple(str(part) for part in item.path),
                ):
                    location = "/".join(str(part) for part in error.absolute_path) or "<root>"
                    errors.append(f"{relative}:{location}: {error.message}")
            except RepositoryValidationError as exc:
                errors.append(str(exc))

        if expected_type not in {
            "experiment_registry",
            "evidence_registry",
            "foundational_study_registry",
            "research_finding_registry",
            "foundational_study_closeout_registry",
        }:
            if expected_type == "foundational_subject_registry" and isinstance(
                registry.get("entries"), list
            ):
                for index, entry in enumerate(registry["entries"]):
                    if not isinstance(entry, Mapping):
                        continue
                    artifact = entry.get("definition_artifact")
                    if not isinstance(artifact, Mapping):
                        continue
                    locator = artifact.get("locator")
                    digest = artifact.get("digest")
                    if not isinstance(locator, str) or not isinstance(digest, Mapping):
                        continue
                    try:
                        definition_path = _resolve_local_artifact(root, locator)
                    except RepositoryValidationError as exc:
                        errors.append(f"{relative}:entries/{index}: {exc}")
                        continue
                    if definition_path is None or not definition_path.is_file():
                        errors.append(
                            f"{relative}:entries/{index}: missing subject definition: {locator}"
                        )
                        continue
                    actual = hashlib.sha256(definition_path.read_bytes()).hexdigest()
                    if digest.get("value") != actual:
                        errors.append(
                            f"{relative}:entries/{index}: subject definition SHA-256 does not match raw file bytes"
                        )
            continue
        if not isinstance(registry.get("entries"), list):
            continue

        for index, entry in enumerate(registry["entries"]):
            if not isinstance(entry, Mapping):
                continue
            artifact_path_value = entry.get("artifact_path")
            digest = entry.get("artifact_digest")
            if not isinstance(artifact_path_value, str) or not isinstance(digest, Mapping):
                continue

            artifact_path = (root / artifact_path_value).resolve()
            try:
                artifact_path.relative_to(root.resolve())
            except ValueError:
                errors.append(f"{relative}:entries/{index}: artifact_path escapes repository")
                continue
            if not artifact_path.is_file():
                errors.append(
                    f"{relative}:entries/{index}: missing artifact: {artifact_path_value}"
                )
                continue

            expected_digest = digest.get("value")
            actual_digest = hashlib.sha256(artifact_path.read_bytes()).hexdigest()
            if expected_digest != actual_digest:
                errors.append(
                    f"{relative}:entries/{index}: SHA-256 digest does not match raw file bytes"
                )

            try:
                artifact = load_json(artifact_path)
            except RepositoryValidationError as exc:
                errors.append(str(exc))
                continue
            if artifact.get("artifact_type") != entry.get("artifact_type"):
                errors.append(f"{relative}:entries/{index}: artifact_type does not match record")

            record_id_field = {
                "experiment_registry": "manifest_record_id",
                "evidence_registry": "record_id",
                "foundational_study_registry": "study_record_id",
                "research_finding_registry": "record_id",
                "foundational_study_closeout_registry": "record_id",
            }[expected_type]
            if artifact.get(record_id_field) != entry.get("record_id"):
                errors.append(f"{relative}:entries/{index}: record_id does not match artifact")
            if artifact.get("record_version") != entry.get("record_version"):
                errors.append(
                    f"{relative}:entries/{index}: record_version does not match artifact"
                )

            if (
                expected_type == "foundational_study_registry"
                and entry.get("registry_status") == "ACTIVE"
                and artifact.get("record_status") != "FROZEN"
            ):
                errors.append(
                    f"{relative}:entries/{index}: ACTIVE foundational study must be FROZEN"
                )
            if (
                expected_type == "research_finding_registry"
                and entry.get("registry_status") == "ACTIVE"
                and artifact.get("record_status") != "PUBLISHED"
            ):
                errors.append(
                    f"{relative}:entries/{index}: ACTIVE research finding must be PUBLISHED"
                )
            if (
                expected_type == "foundational_study_closeout_registry"
                and entry.get("registry_status") == "ACTIVE"
                and artifact.get("record_status") != "PUBLISHED"
            ):
                errors.append(
                    f"{relative}:entries/{index}: ACTIVE foundational study closeout must be PUBLISHED"
                )

            record_version = artifact.get("record_version")
            amendment = artifact.get("amendment")
            if isinstance(record_version, int) and record_version > 1 and isinstance(amendment, Mapping):
                previous_version = amendment.get("supersedes_record_version")
                if not isinstance(previous_version, int) or previous_version >= record_version:
                    errors.append(
                        f"{relative}:entries/{index}: superseded record version must be lower than the new version"
                    )
                else:
                    previous_entry = next(
                        (
                            candidate
                            for candidate in registry["entries"]
                            if isinstance(candidate, Mapping)
                            and candidate.get("record_id") == entry.get("record_id")
                            and candidate.get("record_version") == previous_version
                        ),
                        None,
                    )
                    if previous_entry is None:
                        errors.append(
                            f"{relative}:entries/{index}: superseded record version is absent from registry"
                        )
                    else:
                        supersedes_digest = amendment.get("supersedes_artifact_digest")
                        previous_digest = previous_entry.get("artifact_digest")
                        if (
                            isinstance(supersedes_digest, Mapping)
                            and isinstance(previous_digest, Mapping)
                            and supersedes_digest.get("value") != previous_digest.get("value")
                        ):
                            errors.append(
                                f"{relative}:entries/{index}: supersession digest does not match prior registry entry"
                            )
                        if expected_type in {
                            "foundational_study_registry",
                            "research_finding_registry",
                            "foundational_study_closeout_registry",
                        }:
                            previous_path_value = previous_entry.get("artifact_path")
                            if isinstance(previous_path_value, str):
                                previous_path = (root / previous_path_value).resolve()
                                if previous_path.is_file():
                                    try:
                                        previous_artifact = load_json(previous_path)
                                    except RepositoryValidationError:
                                        previous_artifact = None
                                    if isinstance(previous_artifact, Mapping):
                                        if expected_type == "foundational_study_registry":
                                            if previous_artifact.get("study_id") != artifact.get("study_id"):
                                                errors.append(
                                                    f"{relative}:entries/{index}: superseding study must retain study_id"
                                                )
                                        elif expected_type == "research_finding_registry":
                                            if previous_artifact.get("finding_id") != artifact.get("finding_id"):
                                                errors.append(
                                                    f"{relative}:entries/{index}: superseding finding must retain finding_id"
                                                )
                                            previous_study = previous_artifact.get("study_reference")
                                            current_study = artifact.get("study_reference")
                                            previous_analysis = previous_artifact.get("analysis_reference")
                                            current_analysis = artifact.get("analysis_reference")
                                            if isinstance(previous_study, Mapping) and isinstance(current_study, Mapping):
                                                for field in (
                                                    "study_id",
                                                    "study_record_id",
                                                    "study_record_version",
                                                ):
                                                    if previous_study.get(field) != current_study.get(field):
                                                        errors.append(
                                                            f"{relative}:entries/{index}: superseding finding must retain exact study target"
                                                        )
                                                        break
                                            if isinstance(previous_analysis, Mapping) and isinstance(current_analysis, Mapping):
                                                if previous_analysis.get("analysis_id") != current_analysis.get("analysis_id"):
                                                    errors.append(
                                                        f"{relative}:entries/{index}: superseding finding must retain analysis target"
                                                    )
                                        else:
                                            if previous_artifact.get("closeout_id") != artifact.get("closeout_id"):
                                                errors.append(
                                                    f"{relative}:entries/{index}: superseding closeout must retain closeout_id"
                                                )
                                            previous_study = previous_artifact.get("study_reference")
                                            current_study = artifact.get("study_reference")
                                            if isinstance(previous_study, Mapping) and isinstance(current_study, Mapping):
                                                for field in (
                                                    "study_id",
                                                    "study_record_id",
                                                    "study_record_version",
                                                ):
                                                    if previous_study.get(field) != current_study.get(field):
                                                        errors.append(
                                                            f"{relative}:entries/{index}: superseding closeout must retain exact study target"
                                                        )
                                                        break

            schema_id = entry.get("schema_id")
            schema = artifact_schemas.get(schema_id) if isinstance(schema_id, str) else None
            if schema is None:
                errors.append(f"{relative}:entries/{index}: unknown schema_id: {schema_id!r}")
                continue
            validator = Draft202012Validator(schema, format_checker=FormatChecker())
            for error in sorted(
                validator.iter_errors(artifact),
                key=lambda item: tuple(str(part) for part in item.path),
            ):
                location = "/".join(str(part) for part in error.absolute_path) or "<root>"
                errors.append(
                    f"{relative}:entries/{index}:{artifact_path_value}:{location}: {error.message}"
                )
    errors.extend(_validate_foundational_registry_relationships(root))
    return errors


def validate_citation_metadata(root: Path) -> list[str]:
    errors: list[str] = []
    path = root / "CITATION.cff"
    if not path.is_file():
        return errors

    try:
        citation = load_yaml(path)
    except RepositoryValidationError as exc:
        return [str(exc)]

    if not isinstance(citation, Mapping):
        return ["CITATION.cff: top level must be a mapping"]

    required = ("cff-version", "message", "title", "type", "authors", "license")
    for key in required:
        if not citation.get(key):
            errors.append(f"CITATION.cff: missing required value: {key}")
    if citation.get("cff-version") != "1.2.0":
        errors.append("CITATION.cff: cff-version must be 1.2.0")
    if not isinstance(citation.get("authors"), list):
        errors.append("CITATION.cff: authors must be a list")
    return errors


def validate_policy_invariants(root: Path) -> list[str]:
    errors: list[str] = []
    charter_path = root / "docs/program/PROGRAM_CHARTER_v0.1.md"
    if charter_path.is_file():
        charter = charter_path.read_text(encoding="utf-8")
        for invariant in CHARTER_INVARIANTS:
            if invariant not in charter:
                errors.append(f"program charter missing invariant: {invariant}")

    for relative in (
        "templates/research-proposal.md",
        "templates/experiment-protocol.md",
        "templates/experiment-report.md",
        "templates/threat-model.md",
    ):
        path = root / relative
        if not path.is_file():
            continue
        content = path.read_text(encoding="utf-8")
        for invariant in TEMPLATE_INVARIANTS:
            if invariant not in content:
                errors.append(f"{relative}: missing required boundary label: {invariant}")
    return errors


def validate_markdown_links(root: Path) -> list[str]:
    errors: list[str] = []
    for path in sorted(root.rglob("*.md")):
        if any(part.startswith(".") and part != ".github" for part in path.parts):
            continue
        content = path.read_text(encoding="utf-8")
        for target in MARKDOWN_LINK.findall(content):
            target = target.strip().strip("<>")
            if not target or target.startswith(("#", "http://", "https://", "mailto:")):
                continue
            file_part = target.split("#", 1)[0]
            if not file_part:
                continue
            resolved = (path.parent / file_part).resolve()
            try:
                resolved.relative_to(root.resolve())
            except ValueError:
                errors.append(f"{path.relative_to(root)}: link escapes repository: {target}")
                continue
            if not resolved.exists():
                errors.append(f"{path.relative_to(root)}: broken relative link: {target}")
    return errors


def validate_repository(root: Path = ROOT) -> list[str]:
    """Return all discovered contract violations without stopping at the first."""

    errors: list[str] = []
    errors.extend(validate_required_paths(root))
    errors.extend(validate_dependency_lock(root))
    errors.extend(validate_serialized_documents(root))
    errors.extend(validate_local_artifact_references(root))
    errors.extend(validate_schemas_and_examples(root))
    errors.extend(validate_registries(root))
    errors.extend(validate_citation_metadata(root))
    errors.extend(validate_policy_invariants(root))
    errors.extend(validate_markdown_links(root))
    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--root",
        type=Path,
        default=ROOT,
        help="repository root to validate (defaults to this checkout)",
    )
    args = parser.parse_args(argv)

    errors = validate_repository(args.root.resolve())
    if errors:
        print(
            f"LCMRP repository validation failed with {len(errors)} error(s):",
            file=sys.stderr,
        )
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print(
        "LCMRP repository validation passed: required governance, schemas, examples, "
        "registries, serialized documents, and relative links satisfy the configured checks."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
