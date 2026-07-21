"""Independent adversarial gates for the two M1 non-evidentiary dry runs.

The dry runs exercise M0's foundational-study record graph; they are not
scientific studies.  These tests therefore verify exact bytes, identities,
registry targets, lifecycle states, and terminal-ledger completeness.  They do
not infer taxonomy quality, formal soundness, novelty, external validity, or
independent validation from schema conformance.

Known test limits are intentional and documented here rather than hidden:

* The required bundle topology can reject an equivalent layout that does not
  expose one local subject registry and one local index of each record kind
  (false-positive risk).
* Text checks catch explicit product/vendor bindings and completion rhetoric,
  but cannot prove that every indirect or euphemistic claim is harmless
  (false-negative risk).
* SHA-256 checks establish byte identity, not truth, authorship, or scientific
  validity.  JSON Schema checks establish contract shape, not correctness.
* Human-data checks cover the governed structured flags plus obvious content
  patterns; they are not a privacy classifier or a substitute for human review.

No gate below is based on word count.
"""

from __future__ import annotations

import copy
from dataclasses import dataclass
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
from typing import Any, Iterable, Mapping
import unittest

from jsonschema import Draft202012Validator, FormatChecker
import yaml


ROOT = Path(__file__).resolve().parents[1]
BUNDLE_ROOT = ROOT / "examples" / "m1-dry-runs"
BUNDLE_PATHS = {
    "taxonomy": BUNDLE_ROOT / "taxonomy",
    "formal-analysis": BUNDLE_ROOT / "formal-analysis",
}

SCHEMA_PATHS = {
    "foundational_subject_registry": ROOT
    / "schemas"
    / "foundational-subject-registry.schema.json",
    "foundational_study_manifest": ROOT
    / "schemas"
    / "foundational-study-manifest.schema.json",
    "research_finding_record": ROOT
    / "schemas"
    / "research-finding-record.schema.json",
    "foundational_study_closeout": ROOT
    / "schemas"
    / "foundational-study-closeout.schema.json",
    "foundational_record_index": ROOT
    / "schemas"
    / "foundational-record-index.schema.json",
}

EXPECTED_PROFILE = {
    "taxonomy": "STRUCTURAL_OR_TAXONOMY_EVALUATION",
    "formal-analysis": "FORMAL_ANALYSIS",
}
EXPECTED_SUBJECT_KIND = {
    "taxonomy": "MEMORY_TAXONOMY",
    "formal-analysis": "FORMAL_MEMORY_MODEL",
}
EXPECTED_INDEX_TARGET = {
    "foundational_study_registry": (
        "foundational_study_manifest",
        "urn:lcmrp:schema:foundational-study-manifest:0.1.0",
    ),
    "research_finding_registry": (
        "research_finding_record",
        "urn:lcmrp:schema:research-finding-record:0.1.0",
    ),
    "foundational_study_closeout_registry": (
        "foundational_study_closeout",
        "urn:lcmrp:schema:foundational-study-closeout:0.1.0",
    ),
}

PRODUCTION_REGISTRIES = (
    "registry/mechanisms.yaml",
    "registry/experiments.yaml",
    "registry/evidence.yaml",
    "registry/foundational-subjects.yaml",
    "registry/foundational-studies.yaml",
    "registry/research-findings.yaml",
    "registry/foundational-study-closeouts.yaml",
)

ADMITTED_REAL_SUBJECT_IDS = {
    "LCMRP-FSUBJ-0001-MEMORY-TAXONOMY",
    "LCMRP-FSUBJ-0002-FORMAL-MEMORY-OBJECT-MODEL",
}

HIGH_LEVEL_ID_FIELDS = {
    "subject_id",
    "study_id",
    "study_record_id",
    "finding_id",
    "record_id",
    "closeout_id",
    "profile_id",
}

SYNTHETIC_ID = re.compile(r"(?i)(?:SYNTHETIC|DRY[._-]?RUN)")
NON_EVIDENCE = re.compile(
    r"(?i)(?:non[- ]evidentiary|not (?:research |scientific |empirical )?evidence|"
    r"supports? no (?:research |scientific |empirical )?(?:claim|finding|evidence)|"
    r"not (?:a )?(?:real|empirical|scientific) (?:study|finding|result|claim)|"
    r"dry[- ]run)"
)
FALSE_COMPLETION = re.compile(
    r"(?i)\b(?:the|this)\s+(?:research\s+)?study\s+"
    r"(?:is|was|has been)\s+(?:successfully\s+)?completed\b"
)
CORPUSSTUDIO = re.compile(r"(?i)\bcorpusstudio\b")
SPECIFIC_TECHNOLOGY = re.compile(
    r"(?i)\b(?:openai|anthropic|gemini|pinecone|weaviate|chroma|faiss|"
    r"pgvector|qdrant|milvus|postgresql|redis|dynamodb|aws|azure)\b"
)
POSITIVE_COUPLING = re.compile(
    r"(?i)\b(?:requires?|depends?\s+on|assumes?|must\s+use|shall\s+use)\b"
    r"[^.\n]{0,120}\b(?:vendor|provider|vector\s+database|embedding\s+model|"
    r"application\s+schema|product|user\s+interface|cloud)\b"
)


def _load_serialized(path: Path) -> Any:
    text = path.read_text(encoding="utf-8")
    if path.suffix == ".json":
        return json.loads(text)
    return yaml.safe_load(text)


def _relative(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


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


def _artifact_differences(reference: Any, expected: Any) -> list[str]:
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
    left_digest = reference.get("digest")
    right_digest = expected.get("digest")
    if not isinstance(left_digest, Mapping) or not isinstance(right_digest, Mapping):
        return differences + ["digest"]
    for field in ("algorithm", "value", "scope"):
        if left_digest.get(field) != right_digest.get(field):
            differences.append(f"digest.{field}")
    return differences


def _canonical_index_target(bundle: "BundleSnapshot", artifact_path: Any) -> str | None:
    """Resolve an isolated index path without allowing it to escape its bundle.

    The record-index schema's ``artifact_path`` is repository-relative in the
    production registries.  The two isolated example registries deliberately
    use paths relative to their bundle root.  Both notations identify the same
    byte target after normalization; neither may escape the dry-run directory.
    """

    if not isinstance(artifact_path, str) or not _safe_local_locator(artifact_path):
        return None
    bundle_prefix = _relative(bundle.base).rstrip("/") + "/"
    candidate = (
        (ROOT / artifact_path).resolve()
        if artifact_path.startswith(bundle_prefix)
        else (bundle.base / artifact_path).resolve()
    )
    try:
        candidate.relative_to(bundle.base.resolve())
    except ValueError:
        return None
    return _relative(candidate)


def _index_reference_differences(
    reference: Any,
    entry: Any,
    bundle: "BundleSnapshot" | None = None,
) -> list[str]:
    if not isinstance(reference, Mapping) or not isinstance(entry, Mapping):
        return ["artifact"]
    differences: list[str] = []
    pairs = (("artifact_version", "record_version"), ("schema_id", "schema_id"))
    for reference_field, entry_field in pairs:
        if reference.get(reference_field) != entry.get(entry_field):
            differences.append(reference_field)
    if bundle is None:
        if reference.get("locator") != entry.get("artifact_path"):
            differences.append("locator")
    else:
        locator = reference.get("locator")
        canonical_target = _canonical_index_target(bundle, entry.get("artifact_path"))
        if not isinstance(locator, str) or locator != canonical_target:
            differences.append("locator")
    digest = reference.get("digest")
    index_digest = entry.get("artifact_digest")
    if not isinstance(digest, Mapping) or not isinstance(index_digest, Mapping):
        return differences + ["digest"]
    for field in ("algorithm", "value", "scope"):
        if digest.get(field) != index_digest.get(field):
            differences.append(f"digest.{field}")
    return differences


@dataclass
class BundleSnapshot:
    name: str
    base: Path
    documents: dict[str, Any]
    raw_files: dict[str, bytes]

    @classmethod
    def load(cls, name: str, base: Path) -> "BundleSnapshot":
        documents: dict[str, Any] = {}
        raw_files: dict[str, bytes] = {}
        if base.is_dir():
            for path in sorted(base.rglob("*")):
                if not path.is_file():
                    continue
                if "__pycache__" in path.parts or path.suffix == ".pyc":
                    continue
                relative = _relative(path)
                raw_files[relative] = path.read_bytes()
                if path.suffix in {".json", ".yaml", ".yml"}:
                    documents[relative] = _load_serialized(path)
        return cls(name=name, base=base, documents=documents, raw_files=raw_files)

    def clone(self) -> "BundleSnapshot":
        return copy.deepcopy(self)

    def records(self, artifact_type: str) -> list[tuple[str, Mapping[str, Any]]]:
        return [
            (path, document)
            for path, document in self.documents.items()
            if isinstance(document, Mapping)
            and document.get("artifact_type") == artifact_type
        ]

    def indexes(self) -> dict[str, tuple[str, Mapping[str, Any]]]:
        result: dict[str, tuple[str, Mapping[str, Any]]] = {}
        for path, document in self.records("foundational_record_index"):
            registry_type = document.get("registry_type")
            if isinstance(registry_type, str):
                result[registry_type] = (path, document)
        return result

    def bytes_for(self, locator: str) -> bytes | None:
        if locator in self.raw_files:
            return self.raw_files[locator]
        candidate = (ROOT / locator).resolve()
        try:
            candidate.relative_to(ROOT.resolve())
        except ValueError:
            return None
        return candidate.read_bytes() if candidate.is_file() else None


def _schema_errors(bundle: BundleSnapshot) -> list[str]:
    errors: list[str] = []
    schemas = {
        artifact_type: json.loads(path.read_text(encoding="utf-8"))
        for artifact_type, path in SCHEMA_PATHS.items()
    }
    for path, document in bundle.documents.items():
        if not isinstance(document, Mapping):
            continue
        artifact_type = document.get("artifact_type")
        if artifact_type not in schemas:
            continue
        validator = Draft202012Validator(
            schemas[artifact_type], format_checker=FormatChecker()
        )
        for error in sorted(
            validator.iter_errors(document),
            key=lambda item: tuple(str(part) for part in item.absolute_path),
        ):
            location = "/".join(str(part) for part in error.absolute_path) or "<root>"
            errors.append(f"{path}:{location}: schema: {error.message}")
    return errors


def _safe_local_locator(locator: str) -> bool:
    path = PurePosixPath(locator)
    return (
        bool(locator)
        and not path.is_absolute()
        and ".." not in path.parts
        and "://" not in locator
        and not locator.startswith(("urn:", "doi:"))
    )


def _digest_errors(bundle: BundleSnapshot) -> list[str]:
    errors: list[str] = []
    for document_path, document in bundle.documents.items():
        for mapping in _iter_mappings(document):
            locator = mapping.get("locator")
            digest = mapping.get("digest")
            if not isinstance(locator, str) or not isinstance(digest, Mapping):
                continue
            status = digest.get("status")
            if status not in {"RECORDED", "VERIFIED"}:
                continue
            if not _safe_local_locator(locator):
                errors.append(f"{document_path}: unsafe or non-local locator {locator!r}")
                continue
            raw = bundle.bytes_for(locator)
            if raw is None:
                errors.append(f"{document_path}: recorded artifact is missing: {locator}")
                continue
            if digest.get("algorithm") != "SHA-256":
                errors.append(f"{document_path}: digest algorithm is not SHA-256")
            if digest.get("scope") != "RAW_FILE_BYTES":
                errors.append(f"{document_path}: digest scope is not RAW_FILE_BYTES")
            actual = hashlib.sha256(raw).hexdigest()
            if digest.get("value") != actual:
                errors.append(
                    f"{document_path}: raw-byte SHA-256 mismatch for {locator}"
                )
    return errors


def _core(bundle: BundleSnapshot, artifact_type: str) -> tuple[str, Mapping[str, Any]] | None:
    records = bundle.records(artifact_type)
    return records[0] if len(records) == 1 else None


def _topology_errors(bundle: BundleSnapshot) -> list[str]:
    errors: list[str] = []
    if not bundle.base.is_dir():
        return [f"missing dry-run bundle: {_relative(bundle.base)}"]
    if not bundle.raw_files:
        errors.append(f"{bundle.name}: dry-run bundle is empty")

    required_counts = {
        "foundational_subject_registry": 1,
        "foundational_study_manifest": 1,
        "foundational_study_closeout": 1,
    }
    for artifact_type, expected_count in required_counts.items():
        actual = len(bundle.records(artifact_type))
        if actual != expected_count:
            errors.append(
                f"{bundle.name}: expected {expected_count} {artifact_type}, found {actual}"
            )
    if not bundle.records("research_finding_record"):
        errors.append(f"{bundle.name}: no atomic research_finding_record is present")

    indexes = bundle.indexes()
    for registry_type in EXPECTED_INDEX_TARGET:
        matches = [
            document
            for _path, document in bundle.records("foundational_record_index")
            if document.get("registry_type") == registry_type
        ]
        if len(matches) != 1:
            errors.append(
                f"{bundle.name}: expected one local {registry_type}, found {len(matches)}"
            )
    if len(indexes) != 3 or len(bundle.records("foundational_record_index")) != 3:
        errors.append(f"{bundle.name}: local indexes must contain exactly three registry types")

    # A bundle-local checker is supporting audit infrastructure, not a memory
    # implementation.  Executable research mechanisms remain out of scope, but
    # the helper is allowed so long as the content gates below find no product,
    # vendor, storage, model, or application binding.
    allowed_suffixes = {".json", ".yaml", ".yml", ".md", ".txt", ".py"}
    for relative in bundle.raw_files:
        if Path(relative).suffix.lower() not in allowed_suffixes:
            errors.append(
                f"{bundle.name}: executable or implementation artifact is out of scope: {relative}"
            )
    return errors


def _index_errors(bundle: BundleSnapshot) -> list[str]:
    errors: list[str] = []
    indexes = bundle.indexes()
    indexed_paths: set[str] = set()

    for registry_type, (index_path, index) in indexes.items():
        if registry_type not in EXPECTED_INDEX_TARGET:
            errors.append(f"{index_path}: unexpected registry type {registry_type!r}")
            continue
        expected_artifact_type, expected_schema_id = EXPECTED_INDEX_TARGET[registry_type]
        entries = index.get("entries")
        if not isinstance(entries, list):
            continue
        active_by_record: dict[Any, int] = {}
        active_entries = [
            entry
            for entry in entries
            if isinstance(entry, Mapping) and entry.get("registry_status") == "ACTIVE"
        ]
        if not active_entries:
            errors.append(f"{index_path}: dry-run index has no ACTIVE target")
        for position, entry in enumerate(entries):
            if not isinstance(entry, Mapping):
                continue
            label = f"{index_path}:entries/{position}"
            record_id = entry.get("record_id")
            if entry.get("registry_status") == "ACTIVE":
                active_by_record[record_id] = active_by_record.get(record_id, 0) + 1
            if entry.get("artifact_type") != expected_artifact_type:
                errors.append(f"{label}: artifact type does not match registry type")
            if entry.get("schema_id") != expected_schema_id:
                errors.append(f"{label}: schema ID does not match registry type")
            artifact_path = entry.get("artifact_path")
            canonical_target = _canonical_index_target(bundle, artifact_path)
            if canonical_target is None:
                errors.append(f"{label}: target path is not canonical within its bundle")
                continue
            indexed_paths.add(canonical_target)
            raw = bundle.bytes_for(canonical_target)
            target = bundle.documents.get(canonical_target)
            if raw is None or not isinstance(target, Mapping):
                errors.append(f"{label}: indexed target is missing or is not a record")
                continue
            index_digest = entry.get("artifact_digest")
            actual_digest = hashlib.sha256(raw).hexdigest()
            if (
                not isinstance(index_digest, Mapping)
                or index_digest.get("algorithm") != "SHA-256"
                or index_digest.get("scope") != "RAW_FILE_BYTES"
                or index_digest.get("value") != actual_digest
            ):
                errors.append(f"{label}: index raw-byte digest does not match target")
            if target.get("artifact_type") != entry.get("artifact_type"):
                errors.append(f"{label}: index artifact type does not match target")
            target_id_field = (
                "study_record_id"
                if expected_artifact_type == "foundational_study_manifest"
                else "record_id"
            )
            if target.get(target_id_field) != record_id:
                errors.append(f"{label}: index record ID does not match target")
            if target.get("record_version") != entry.get("record_version"):
                errors.append(f"{label}: index record version does not match target")

            active = entry.get("registry_status") == "ACTIVE"
            required_status = {
                "foundational_study_manifest": "FROZEN",
                "research_finding_record": "PUBLISHED",
                "foundational_study_closeout": "PUBLISHED",
            }[expected_artifact_type]
            if active and target.get("record_status") != required_status:
                errors.append(
                    f"{label}: ACTIVE {expected_artifact_type} must be {required_status}"
                )

        for record_id, count in active_by_record.items():
            if count != 1:
                errors.append(
                    f"{index_path}: more than one ACTIVE version for record {record_id!r}"
                )

    for artifact_type in (
        "foundational_study_manifest",
        "research_finding_record",
        "foundational_study_closeout",
    ):
        for path, _record in bundle.records(artifact_type):
            if path not in indexed_paths:
                errors.append(f"{bundle.name}: core record is not indexed: {path}")
    return errors


def _binding_errors(bundle: BundleSnapshot) -> list[str]:
    errors: list[str] = []
    study_item = _core(bundle, "foundational_study_manifest")
    subject_item = _core(bundle, "foundational_subject_registry")
    closeout_item = _core(bundle, "foundational_study_closeout")
    if study_item is None or subject_item is None or closeout_item is None:
        return errors
    study_path, study = study_item
    subject_path, subject_registry = subject_item
    closeout_path, closeout = closeout_item
    findings = bundle.records("research_finding_record")
    indexes = bundle.indexes()

    profile = study.get("primary_method_profile")
    subject = study.get("subject")
    if not isinstance(profile, Mapping) or not isinstance(subject, Mapping):
        return errors
    if profile.get("profile_kind") != EXPECTED_PROFILE[bundle.name]:
        errors.append(f"{study_path}: mismatched profile kind for dry-run bundle")
    if subject.get("subject_kind") != EXPECTED_SUBJECT_KIND[bundle.name]:
        errors.append(f"{study_path}: mismatched subject kind for dry-run bundle")
    if study.get("record_status") != "FROZEN":
        errors.append(f"{study_path}: study manifest is not FROZEN")
    preregistration = study.get("preregistration")
    if not isinstance(preregistration, Mapping) or preregistration.get("status") != "FROZEN":
        errors.append(f"{study_path}: preregistration is not FROZEN")

    subject_entries = subject_registry.get("entries")
    if isinstance(subject_entries, list):
        active_subjects = [
            entry
            for entry in subject_entries
            if isinstance(entry, Mapping) and entry.get("entry_status") == "ACTIVE"
        ]
        active_by_subject: dict[Any, int] = {}
        for entry in active_subjects:
            key = entry.get("subject_id")
            active_by_subject[key] = active_by_subject.get(key, 0) + 1
        if len(active_subjects) != 1:
            errors.append(f"{subject_path}: expected exactly one ACTIVE synthetic subject")
        for subject_id, count in active_by_subject.items():
            if count != 1:
                errors.append(
                    f"{subject_path}: more than one ACTIVE subject version for {subject_id!r}"
                )
        if active_subjects:
            registered = active_subjects[0]
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
                if registered.get(field) != subject.get(field):
                    errors.append(f"{study_path}: registered subject mismatch for {field}")
            for field in _artifact_differences(
                registered.get("definition_artifact"),
                subject.get("definition_artifact"),
            ):
                errors.append(
                    f"{study_path}: registered subject definition mismatch for {field}"
                )

    analyses = study.get("analyses")
    expected_analyses = {
        analysis.get("analysis_id"): analysis
        for analysis in analyses
        if isinstance(analyses, list) and isinstance(analysis, Mapping)
    }
    if len(expected_analyses) != len(analyses or []):
        errors.append(f"{study_path}: planned analysis IDs must be unique")

    active_study_entry = None
    active_finding_entries: dict[tuple[Any, Any], Mapping[str, Any]] = {}
    active_closeout_entry = None
    if "foundational_study_registry" in indexes:
        active = [
            entry
            for entry in indexes["foundational_study_registry"][1].get("entries", [])
            if isinstance(entry, Mapping) and entry.get("registry_status") == "ACTIVE"
        ]
        if len(active) == 1:
            active_study_entry = active[0]
    if "research_finding_registry" in indexes:
        for entry in indexes["research_finding_registry"][1].get("entries", []):
            if isinstance(entry, Mapping) and entry.get("registry_status") == "ACTIVE":
                active_finding_entries[(entry.get("record_id"), entry.get("record_version"))] = entry
    if "foundational_study_closeout_registry" in indexes:
        active = [
            entry
            for entry in indexes["foundational_study_closeout_registry"][1].get("entries", [])
            if isinstance(entry, Mapping) and entry.get("registry_status") == "ACTIVE"
        ]
        if len(active) == 1:
            active_closeout_entry = active[0]

    findings_by_analysis: dict[Any, list[tuple[str, Mapping[str, Any]]]] = {}
    manifest_reference: Mapping[str, Any] | None = None
    for finding_path, finding in findings:
        analysis_reference = finding.get("analysis_reference")
        analysis_id = (
            analysis_reference.get("analysis_id")
            if isinstance(analysis_reference, Mapping)
            else None
        )
        findings_by_analysis.setdefault(analysis_id, []).append((finding_path, finding))
        if finding.get("record_status") != "PUBLISHED":
            errors.append(f"{finding_path}: atomic finding is not PUBLISHED")
        study_reference = finding.get("study_reference")
        if not isinstance(study_reference, Mapping):
            continue
        candidate_reference = study_reference.get("manifest_artifact")
        if isinstance(candidate_reference, Mapping):
            manifest_reference = candidate_reference
        for field, expected in (
            ("study_id", study.get("study_id")),
            ("study_record_id", study.get("study_record_id")),
            ("study_record_version", study.get("record_version")),
        ):
            if study_reference.get(field) != expected:
                errors.append(f"{finding_path}: exact study binding mismatch for {field}")
        if active_study_entry is not None:
            for field in _index_reference_differences(
                study_reference.get("manifest_artifact"), active_study_entry, bundle
            ):
                errors.append(f"{finding_path}: study index binding mismatch for {field}")

        subject_reference = finding.get("subject_reference")
        if isinstance(subject_reference, Mapping):
            for field in (
                "target_type",
                "subject_kind",
                "subject_id",
                "subject_series",
                "subject_version",
            ):
                if subject_reference.get(field) != subject.get(field):
                    errors.append(f"{finding_path}: exact subject binding mismatch for {field}")
            for field in _artifact_differences(
                subject_reference.get("definition_artifact"),
                subject.get("definition_artifact"),
            ):
                errors.append(
                    f"{finding_path}: exact subject definition binding mismatch for {field}"
                )

        profile_reference = finding.get("primary_method_profile_reference")
        if isinstance(profile_reference, Mapping):
            for field in ("profile_kind", "profile_id", "profile_series", "profile_version"):
                if profile_reference.get(field) != profile.get(field):
                    errors.append(f"{finding_path}: exact profile binding mismatch for {field}")
            for field in _artifact_differences(
                profile_reference.get("profile_artifact"),
                profile.get("profile_definition_artifact"),
            ):
                errors.append(
                    f"{finding_path}: exact profile artifact binding mismatch for {field}"
                )

        planned = expected_analyses.get(analysis_id)
        if planned is None:
            errors.append(f"{finding_path}: finding targets an unplanned analysis")
        elif isinstance(analysis_reference, Mapping) and (
            analysis_reference.get("analysis_mode") != planned.get("analysis_mode")
        ):
            errors.append(f"{finding_path}: exact analysis mode binding mismatch")

        active_entry = active_finding_entries.get(
            (finding.get("record_id"), finding.get("record_version"))
        )
        if active_entry is None:
            errors.append(f"{finding_path}: finding is not an ACTIVE indexed version")

    for analysis_id in expected_analyses:
        count = len(findings_by_analysis.get(analysis_id, []))
        if count != 1:
            errors.append(
                f"{bundle.name}: planned analysis {analysis_id!r} has {count} terminal findings; expected one"
            )
    extras = set(findings_by_analysis) - set(expected_analyses)
    if extras:
        errors.append(f"{bundle.name}: findings exist for extra analyses: {sorted(extras, key=str)}")

    study_reference = closeout.get("study_reference")
    if isinstance(study_reference, Mapping):
        for field, expected in (
            ("study_id", study.get("study_id")),
            ("study_record_id", study.get("study_record_id")),
            ("study_record_version", study.get("record_version")),
        ):
            if study_reference.get(field) != expected:
                errors.append(f"{closeout_path}: exact closeout study binding mismatch for {field}")
        if active_study_entry is not None:
            for field in _index_reference_differences(
                study_reference.get("manifest_artifact"), active_study_entry, bundle
            ):
                errors.append(f"{closeout_path}: closeout study index mismatch for {field}")
        if manifest_reference is not None:
            for field in _artifact_differences(
                study_reference.get("manifest_artifact"), manifest_reference
            ):
                errors.append(f"{closeout_path}: finding/closeout study reference mismatch for {field}")
    if closeout.get("record_status") != "PUBLISHED":
        errors.append(f"{closeout_path}: closeout is not PUBLISHED")
    if closeout.get("completeness_assertion") != (
        "EXACTLY_ONE_PUBLISHED_FINDING_PER_PLANNED_ANALYSIS"
    ):
        errors.append(f"{closeout_path}: closeout does not assert exact terminal completeness")
    if active_closeout_entry is None:
        errors.append(f"{closeout_path}: closeout is not an ACTIVE indexed version")

    dispositions = closeout.get("analysis_dispositions")
    disposition_list = dispositions if isinstance(dispositions, list) else []
    disposition_ids = [
        row.get("analysis_id") for row in disposition_list if isinstance(row, Mapping)
    ]
    if len(disposition_ids) != len(set(disposition_ids)):
        errors.append(f"{closeout_path}: duplicate analysis disposition")
    if set(disposition_ids) != set(expected_analyses):
        errors.append(f"{closeout_path}: closeout disposition set does not equal planned analyses")

    used_finding_keys: set[tuple[Any, Any]] = set()
    finding_lookup = {
        (finding.get("record_id"), finding.get("record_version")): (path, finding)
        for path, finding in findings
    }
    for position, disposition in enumerate(disposition_list):
        if not isinstance(disposition, Mapping):
            continue
        label = f"{closeout_path}:analysis_dispositions/{position}"
        finding_key = (
            disposition.get("finding_record_id"),
            disposition.get("finding_record_version"),
        )
        if finding_key in used_finding_keys:
            errors.append(f"{label}: duplicate terminal finding reuse")
        used_finding_keys.add(finding_key)
        target = finding_lookup.get(finding_key)
        if target is None:
            errors.append(f"{label}: disposition does not resolve to an atomic finding")
            continue
        _finding_path, finding = target
        finding_analysis = finding.get("analysis_reference")
        comparisons = (
            (disposition.get("finding_id"), finding.get("finding_id"), "finding_id"),
            (
                disposition.get("terminal_disposition"),
                finding.get("terminal_disposition"),
                "terminal_disposition",
            ),
            (
                disposition.get("analysis_id"),
                finding_analysis.get("analysis_id") if isinstance(finding_analysis, Mapping) else None,
                "analysis_id",
            ),
            (
                disposition.get("analysis_mode"),
                finding_analysis.get("analysis_mode") if isinstance(finding_analysis, Mapping) else None,
                "analysis_mode",
            ),
        )
        for actual, expected, field in comparisons:
            if actual != expected:
                errors.append(f"{label}: exact finding disposition mismatch for {field}")
        finding_entry = active_finding_entries.get(finding_key)
        if finding_entry is None:
            errors.append(f"{label}: disposition target is not ACTIVE in finding index")
        else:
            for field in _index_reference_differences(
                disposition.get("finding_artifact"), finding_entry, bundle
            ):
                errors.append(f"{label}: finding index binding mismatch for {field}")

    return errors


def _boundary_errors(bundle: BundleSnapshot) -> list[str]:
    errors: list[str] = []
    combined = b"\n".join(bundle.raw_files.values()).decode("utf-8", errors="replace")
    if CORPUSSTUDIO.search(combined):
        errors.append(f"{bundle.name}: CorpusStudio content is prohibited in the dry run")
    if SPECIFIC_TECHNOLOGY.search(combined):
        errors.append(f"{bundle.name}: vendor or implementation-specific technology appears")
    if POSITIVE_COUPLING.search(combined):
        errors.append(f"{bundle.name}: positive vendor/product/implementation coupling appears")

    for document_path, document in bundle.documents.items():
        if FALSE_COMPLETION.search("\n".join(_iter_strings(document))):
            errors.append(f"{document_path}: false completed-study claim")
        for mapping in _iter_mappings(document):
            for field, value in mapping.items():
                if field in HIGH_LEVEL_ID_FIELDS and isinstance(value, str):
                    if value.startswith("LCMRP-") and not SYNTHETIC_ID.search(value):
                        errors.append(f"{document_path}: real-looking ID is not marked synthetic: {value}")
                lowered = field.lower()
                if (
                    ("human_subject" in lowered or "human_participant" in lowered)
                    and value is not False
                ):
                    errors.append(f"{document_path}: human data/subjects flag is not false")
            if "mechanism_versions" in mapping or "evidence_decision" in mapping:
                errors.append(f"{document_path}: mechanism evidence decision leaked into dry run")

    for path, study in bundle.records("foundational_study_manifest"):
        ethics = study.get("ethics_scope")
        if not isinstance(ethics, Mapping) or any(
            ethics.get(field) is not False
            for field in ("human_subjects_involved", "human_participant_data_involved")
        ):
            errors.append(f"{path}: human-subject ethics boundary is not false")
        sources = study.get("sources")
        if isinstance(sources, list):
            for source in sources:
                if isinstance(source, Mapping) and source.get("human_subjects_involved") is not False:
                    errors.append(f"{path}: source is not explicitly non-human")
        boundary = study.get("mechanism_maturity_boundary")
        if not isinstance(boundary, Mapping) or (
            boundary.get("applicability") != "NOT_APPLICABLE"
            or boundary.get("mechanism_under_evaluation") is not False
            or boundary.get("may_award_mechanism_evidence_labels") is not False
            or boundary.get("may_change_mechanism_evidence_profile") is not False
        ):
            errors.append(f"{path}: mechanism maturity boundary is unsafe")
        if not NON_EVIDENCE.search("\n".join(_iter_strings(study))):
            errors.append(f"{path}: no strong synthetic/non-evidence marker")

    for artifact_type in ("research_finding_record", "foundational_study_closeout"):
        for path, record in bundle.records(artifact_type):
            maturity = record.get("mechanism_maturity_effect")
            if not isinstance(maturity, Mapping) or (
                maturity.get("applicability") != "NOT_APPLICABLE"
                or maturity.get("mechanism_under_evaluation") is not False
                or maturity.get("may_award_mechanism_evidence_labels") is not False
                or maturity.get("may_change_mechanism_evidence_profile") is not False
                or maturity.get("awarded_mechanism_evidence_labels") != []
            ):
                errors.append(f"{path}: record awards or changes mechanism maturity")
            if not NON_EVIDENCE.search("\n".join(_iter_strings(record))):
                errors.append(f"{path}: no strong synthetic/non-evidence marker")

    for path, finding in bundle.records("research_finding_record"):
        claim = finding.get("claim")
        if not isinstance(claim, Mapping) or not SYNTHETIC_ID.search(str(claim.get("claim_id", ""))):
            errors.append(f"{path}: claim ID is not explicitly synthetic")
        claim_text = "\n".join(_iter_strings(claim)) if isinstance(claim, Mapping) else ""
        if not re.search(r"(?i)(?:synthetic|dry[- ]run)", claim_text):
            errors.append(f"{path}: claim is not bounded to synthetic inputs")

    subject_item = _core(bundle, "foundational_subject_registry")
    if subject_item is not None:
        path, registry = subject_item
        for entry in registry.get("entries", []):
            if isinstance(entry, Mapping) and entry.get("mechanism_maturity_applicability") != "NOT_APPLICABLE":
                errors.append(f"{path}: subject entry implies mechanism maturity")
    return errors


def bundle_errors(bundle: BundleSnapshot) -> list[str]:
    return (
        _topology_errors(bundle)
        + _schema_errors(bundle)
        + _digest_errors(bundle)
        + _index_errors(bundle)
        + _binding_errors(bundle)
        + _boundary_errors(bundle)
    )


def production_registry_errors(documents: Mapping[str, Any]) -> list[str]:
    errors: list[str] = []
    for relative in PRODUCTION_REGISTRIES:
        registry = documents.get(relative)
        if not isinstance(registry, Mapping):
            errors.append(f"{relative}: production registry is missing or malformed")
            continue
        entries = registry.get("entries")
        if not isinstance(entries, list):
            errors.append(f"{relative}: production registry entries are malformed")
            continue
        if relative == "registry/foundational-subjects.yaml":
            subject_ids = {
                entry.get("subject_id")
                for entry in entries
                if isinstance(entry, Mapping)
            }
            if len(entries) != len(ADMITTED_REAL_SUBJECT_IDS) or subject_ids != ADMITTED_REAL_SUBJECT_IDS:
                errors.append(
                    f"{relative}: contains an unauthorized subject or dry-run contamination"
                )
            if any(
                SYNTHETIC_ID.search(value)
                for entry in entries
                for value in _iter_strings(entry)
            ):
                errors.append(f"{relative}: contains a synthetic dry-run subject")
        elif entries:
            errors.append(f"{relative}: production registry was populated by a dry run")
    return errors


class M1DryRunAdversarialTests(unittest.TestCase):
    """Fail closed on absent, mutable, cross-bound, or evidentiary dry runs."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.bundles = {
            name: BundleSnapshot.load(name, path) for name, path in BUNDLE_PATHS.items()
        }
        cls.production_registries = {
            relative: _load_serialized(ROOT / relative) for relative in PRODUCTION_REGISTRIES
        }

    def assert_rejected(self, bundle: BundleSnapshot, marker: str) -> None:
        errors = bundle_errors(bundle)
        self.assertTrue(errors, "adversarial mutation unexpectedly passed")
        self.assertTrue(
            any(marker.lower() in error.lower() for error in errors),
            f"mutation was rejected, but not by the expected {marker!r} gate: {errors}",
        )

    def test_01_bundles_have_complete_governed_topology(self) -> None:
        for name, bundle in self.bundles.items():
            with self.subTest(bundle=name):
                self.assertEqual([], _topology_errors(bundle))

    def test_02_every_schema_backed_record_validates_under_draft_2020_12(self) -> None:
        for name, bundle in self.bundles.items():
            with self.subTest(bundle=name):
                self.assertEqual([], _schema_errors(bundle))

    def test_03_raw_byte_digests_and_active_indexes_are_exact(self) -> None:
        for name, bundle in self.bundles.items():
            with self.subTest(bundle=name):
                self.assertEqual([], _digest_errors(bundle))
                self.assertEqual([], _index_errors(bundle))

    def test_04_study_subject_profile_analysis_and_closeout_bind_exactly(self) -> None:
        for name, bundle in self.bundles.items():
            with self.subTest(bundle=name):
                self.assertEqual([], _binding_errors(bundle))

    def test_05_dry_runs_remain_synthetic_non_evidentiary_and_product_independent(self) -> None:
        for name, bundle in self.bundles.items():
            with self.subTest(bundle=name):
                self.assertEqual([], _boundary_errors(bundle))
        self.assertEqual([], production_registry_errors(self.production_registries))

    def test_06_bundle_identities_do_not_overlap(self) -> None:
        identity_sets: dict[str, set[tuple[str, str]]] = {}
        for name, bundle in self.bundles.items():
            identities: set[tuple[str, str]] = set()
            for document in bundle.documents.values():
                for mapping in _iter_mappings(document):
                    for field, value in mapping.items():
                        if field in HIGH_LEVEL_ID_FIELDS and isinstance(value, str):
                            identities.add((field, value))
            identity_sets[name] = identities
        overlap = identity_sets["taxonomy"] & identity_sets["formal-analysis"]
        self.assertEqual(set(), overlap, f"dry-run record identities overlap: {sorted(overlap)}")

    def test_07_digest_substitution_is_rejected(self) -> None:
        for name, original in self.bundles.items():
            mutated = original.clone()
            finding_path, finding = mutated.records("research_finding_record")[0]
            finding["study_reference"]["manifest_artifact"]["digest"]["value"] = "0" * 64
            with self.subTest(bundle=name, record=finding_path):
                self.assert_rejected(mutated, "raw-byte SHA-256 mismatch")

    def test_08_cross_bundle_identity_substitution_is_rejected(self) -> None:
        taxonomy = self.bundles["taxonomy"].clone()
        formal = self.bundles["formal-analysis"]
        _taxonomy_path, taxonomy_finding = taxonomy.records("research_finding_record")[0]
        _formal_path, formal_finding = formal.records("research_finding_record")[0]
        taxonomy_finding["subject_reference"] = copy.deepcopy(
            formal_finding["subject_reference"]
        )
        self.assert_rejected(taxonomy, "exact subject binding mismatch")

    def test_09_missing_duplicate_and_extra_closeout_dispositions_are_rejected(self) -> None:
        for name, original in self.bundles.items():
            closeout_path, _original_closeout = original.records(
                "foundational_study_closeout"
            )[0]

            missing = original.clone()
            missing_closeout = missing.documents[closeout_path]
            missing_closeout["analysis_dispositions"] = missing_closeout[
                "analysis_dispositions"
            ][1:]
            with self.subTest(bundle=name, mutation="missing"):
                self.assert_rejected(missing, "disposition set")

            duplicate = original.clone()
            duplicate_closeout = duplicate.documents[closeout_path]
            duplicate_closeout["analysis_dispositions"].append(
                copy.deepcopy(duplicate_closeout["analysis_dispositions"][0])
            )
            with self.subTest(bundle=name, mutation="duplicate"):
                self.assert_rejected(duplicate, "duplicate analysis disposition")

            extra = original.clone()
            extra_closeout = extra.documents[closeout_path]
            extra_row = copy.deepcopy(extra_closeout["analysis_dispositions"][0])
            extra_row["analysis_id"] = "ANALYSIS-SYNTHETIC-EXTRA"
            extra_closeout["analysis_dispositions"].append(extra_row)
            with self.subTest(bundle=name, mutation="extra"):
                self.assert_rejected(extra, "disposition set")

    def test_10_mismatched_profile_kind_is_rejected(self) -> None:
        for name, original in self.bundles.items():
            mutated = original.clone()
            _path, finding = mutated.records("research_finding_record")[0]
            finding["primary_method_profile_reference"]["profile_kind"] = (
                "FORMAL_ANALYSIS"
                if name == "taxonomy"
                else "STRUCTURAL_OR_TAXONOMY_EVALUATION"
            )
            with self.subTest(bundle=name):
                self.assert_rejected(mutated, "exact profile binding mismatch")

    def test_11_false_completed_study_claim_is_rejected(self) -> None:
        for name, original in self.bundles.items():
            mutated = original.clone()
            _path, finding = mutated.records("research_finding_record")[0]
            finding["finding_statement"] = (
                "This research study was successfully completed and establishes a real finding."
            )
            with self.subTest(bundle=name):
                self.assert_rejected(mutated, "false completed-study claim")

    def test_12_accidental_production_registry_population_is_rejected(self) -> None:
        mutated = copy.deepcopy(self.production_registries)
        mutated["registry/foundational-studies.yaml"]["entries"].append(
            {"synthetic_dry_run_must_not_be_registered": True}
        )
        errors = production_registry_errors(mutated)
        self.assertTrue(
            any("populated by a dry run" in error for error in errors),
            f"production registry mutation unexpectedly passed: {errors}",
        )

    def test_13_more_than_one_active_record_version_is_rejected(self) -> None:
        for name, original in self.bundles.items():
            mutated = original.clone()
            index_path, index = mutated.indexes()["foundational_study_registry"]
            duplicate = copy.deepcopy(index["entries"][0])
            duplicate["record_version"] = duplicate["record_version"] + 1
            index["entries"].append(duplicate)
            with self.subTest(bundle=name, index=index_path):
                self.assert_rejected(mutated, "more than one ACTIVE version")


if __name__ == "__main__":
    unittest.main()
