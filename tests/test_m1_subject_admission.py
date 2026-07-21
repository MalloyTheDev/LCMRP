"""Adversarial gates for the first two real M1 foundational subjects.

These tests review identity registration and provenance only.  They do not
evaluate the taxonomy, prove the formal model, establish independent
validation, or create a mechanism evidence state.
"""

from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
from typing import Any, Iterable, Mapping
import unittest

from jsonschema import Draft202012Validator, FormatChecker
import yaml

from tools.validate_repository import (
    load_json,
    load_yaml,
    validate_registry_entry_semantics,
)


ROOT = Path(__file__).resolve().parents[1]
SUBJECT_REGISTRY = ROOT / "registry" / "foundational-subjects.yaml"
SUBJECT_SCHEMA = ROOT / "schemas" / "foundational-subject-registry.schema.json"

EXPECTED_SUBJECTS = {
    "LCMRP-FSUBJ-0001-MEMORY-TAXONOMY": {
        "subject_series": "LCMRP-MEMORY-TAXONOMY",
        "subject_kind": "MEMORY_TAXONOMY",
        "artifact_id": "LCMRP-MEMORY-TAXONOMY",
        "locator": "docs/taxonomy/MEMORY_TAXONOMY_v0.1.md",
        "digest": "dbdc96095ae90549132e50cbb8759bc45f228cae7d8fcb9a107b95d33647ba70",
        "dossier": "reviews/M1_TAXONOMY_SUBJECT_ADMISSION_2026-07-21.md",
        "independence_marker": "product-independent",
    },
    "LCMRP-FSUBJ-0002-FORMAL-MEMORY-OBJECT-MODEL": {
        "subject_series": "LCMRP-FORMAL-MEMORY-OBJECT-MODEL",
        "subject_kind": "FORMAL_MEMORY_MODEL",
        "artifact_id": "LCMRP-FORMAL-MEMORY-OBJECT-MODEL",
        "locator": "docs/taxonomy/FORMAL_MEMORY_OBJECT_MODEL_v0.1.md",
        "digest": "82052e424c01d3204828472ef569f74f7c0aad418f827cffda92400562bbfaf3",
        "dossier": "reviews/M1_FORMAL_MODEL_SUBJECT_ADMISSION_2026-07-21.md",
        "independence_marker": "avoiding implementation assumptions",
    },
}

NON_SUBJECT_REGISTRIES = (
    "registry/mechanisms.yaml",
    "registry/experiments.yaml",
    "registry/evidence.yaml",
    "registry/foundational-studies.yaml",
    "registry/research-findings.yaml",
    "registry/foundational-study-closeouts.yaml",
)

CANONICAL_RECORD_DIRECTORIES = (
    "records/experiments",
    "records/evidence",
    "records/foundational/studies",
    "records/foundational/findings",
    "records/foundational/closeouts",
)

EXPECTED_SCHEMA_ID = "urn:lcmrp:artifact-schema:markdown:1"
FALSE_AWARD = re.compile(
    r"(?i)\b(?:is|are|was|were|has been|have been)\s+"
    r"(?!(?:not|never)\b)(?:scientifically\s+)?"
    r"(?:validated|adopted|proved|proven|completed|production[- ]ready)\b"
)
FALSE_MILESTONE_COMPLETION = re.compile(
    r"(?i)\bM1\s+(?:is|was|has been)\s+(?!not\b)(?:now\s+)?complete(?:d)?\b"
)
SPECIFIC_PRODUCT = re.compile(
    r"(?i)\b(?:pinecone|weaviate|qdrant|milvus|pgvector|chroma|faiss|"
    r"openai|anthropic|gemini|postgresql|dynamodb|redis|mongodb|"
    r"elasticsearch|sqlite|mysql|mariadb|cassandra|neo4j|"
    r"firebase|ollama|aws|azure|gcp)\b"
)
def _iter_strings(value: Any) -> Iterable[str]:
    if isinstance(value, str):
        yield value
    elif isinstance(value, Mapping):
        for child in value.values():
            yield from _iter_strings(child)
    elif isinstance(value, list):
        for child in value:
            yield from _iter_strings(child)


def _entries_by_id(registry: Mapping[str, Any]) -> dict[str, Mapping[str, Any]]:
    entries = registry.get("entries", [])
    return {
        entry.get("subject_id"): entry
        for entry in entries
        if isinstance(entry, Mapping) and isinstance(entry.get("subject_id"), str)
    }


def _safe_repository_locator(locator: Any) -> bool:
    if not isinstance(locator, str) or not locator or "\\" in locator:
        return False
    path = PurePosixPath(locator)
    return not path.is_absolute() and ".." not in path.parts and "." not in path.parts


def _dossier_registry_specimen(text: str, subject_id: str) -> Mapping[str, Any] | None:
    candidates: list[Mapping[str, Any]] = []
    for match in re.finditer(r"```(?:json|yaml)\s*\n(.*?)\n```", text, re.DOTALL):
        try:
            value = yaml.safe_load(match.group(1))
        except yaml.YAMLError:
            continue
        if isinstance(value, Mapping) and value.get("subject_id") == subject_id:
            candidates.append(value)
    return candidates[0] if len(candidates) == 1 else None


def _admission_errors(
    registry: Mapping[str, Any],
    *,
    non_subject_registries: Mapping[str, Mapping[str, Any]] | None = None,
) -> list[str]:
    """Apply M1 admission semantics that are stricter than schema shape."""

    errors: list[str] = []
    entries = registry.get("entries")
    if not isinstance(entries, list):
        return ["subject entries are not a list"]

    if len(entries) != 2:
        errors.append("exactly two foundational subjects are required")

    by_id = _entries_by_id(registry)
    if set(by_id) != set(EXPECTED_SUBJECTS):
        errors.append("subject ID set differs from the reviewed pair")

    seen_series: set[Any] = set()
    seen_identity_versions: set[tuple[Any, Any]] = set()
    for entry in entries:
        if not isinstance(entry, Mapping):
            errors.append("subject entry is not a mapping")
            continue
        subject_id = entry.get("subject_id")
        expected = EXPECTED_SUBJECTS.get(subject_id)
        identity_version = (subject_id, entry.get("subject_version"))
        if identity_version in seen_identity_versions:
            errors.append("duplicate subject ID/version")
        seen_identity_versions.add(identity_version)

        series = entry.get("subject_series")
        if series in seen_series:
            errors.append("duplicate subject series")
        seen_series.add(series)

        if entry.get("entry_status") != "ACTIVE":
            errors.append(f"{subject_id}: subject is not ACTIVE")
        if entry.get("subject_version") != 1:
            errors.append(f"{subject_id}: initial subject version is not 1")
        if entry.get("supersedes_subject_version") is not None:
            errors.append(f"{subject_id}: v1 has a superseded version")
        if entry.get("supersedes_definition_digest") is not None:
            errors.append(f"{subject_id}: v1 has a superseded definition digest")
        if entry.get("target_type") != "FOUNDATIONAL_SUBJECT":
            errors.append(f"{subject_id}: wrong target type")
        if entry.get("research_layer") != "LAYER_1_FOUNDATIONAL_RESEARCH":
            errors.append(f"{subject_id}: wrong research layer")
        if entry.get("mechanism_maturity_applicability") != "NOT_APPLICABLE":
            errors.append(f"{subject_id}: mechanism maturity leaked into subject admission")

        if expected is None:
            continue
        for field in ("subject_series", "subject_kind"):
            if entry.get(field) != expected[field]:
                errors.append(f"{subject_id}: {field} does not match reviewed identity")

        artifact = entry.get("definition_artifact")
        if not isinstance(artifact, Mapping):
            errors.append(f"{subject_id}: missing definition artifact")
            continue
        if artifact.get("artifact_id") != expected["artifact_id"]:
            errors.append(f"{subject_id}: artifact ID mismatch")
        if artifact.get("artifact_version") != 1:
            errors.append(f"{subject_id}: artifact version mismatch")
        if artifact.get("schema_id") != EXPECTED_SCHEMA_ID:
            errors.append(f"{subject_id}: Markdown artifact schema coordinate mismatch")
        if artifact.get("media_type") != "text/markdown":
            errors.append(f"{subject_id}: media type mismatch")
        locator = artifact.get("locator")
        if locator != expected["locator"]:
            errors.append(f"{subject_id}: definition locator mismatch")
        if not _safe_repository_locator(locator):
            errors.append(f"{subject_id}: unsafe definition locator")

        digest = artifact.get("digest")
        if not isinstance(digest, Mapping):
            errors.append(f"{subject_id}: missing definition digest")
        else:
            if digest.get("algorithm") != "SHA-256":
                errors.append(f"{subject_id}: wrong digest algorithm")
            if digest.get("status") != "VERIFIED":
                errors.append(f"{subject_id}: digest is not VERIFIED")
            if digest.get("scope") != "RAW_FILE_BYTES":
                errors.append(f"{subject_id}: digest scope is not raw file bytes")
            if digest.get("value") != expected["digest"]:
                errors.append(f"{subject_id}: reviewed digest mismatch")

        structured_claim_text = "\n".join(
            str(entry.get(field, "")) for field in ("name", "definition", "boundary")
        )
        if FALSE_AWARD.search(structured_claim_text) or FALSE_MILESTONE_COMPLETION.search(
            structured_claim_text
        ):
            errors.append(f"{subject_id}: false validation, adoption, or completion claim")

    errors.extend(validate_registry_entry_semantics(registry, "foundational-subjects"))

    if non_subject_registries is not None:
        for relative, other in non_subject_registries.items():
            if other.get("entries") != []:
                errors.append(f"{relative}: subject admission contaminated another registry")
    return errors


class M1SubjectAdmissionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.registry = load_yaml(SUBJECT_REGISTRY)
        cls.schema = load_json(SUBJECT_SCHEMA)
        cls.non_subject_registries = {
            relative: load_yaml(ROOT / relative) for relative in NON_SUBJECT_REGISTRIES
        }

    def test_registry_is_schema_valid_and_contains_exactly_reviewed_pair(self) -> None:
        validator = Draft202012Validator(
            self.schema,
            format_checker=FormatChecker(),
        )
        schema_errors = sorted(
            validator.iter_errors(self.registry),
            key=lambda error: tuple(str(part) for part in error.absolute_path),
        )
        self.assertEqual([], schema_errors)
        self.assertEqual(
            [],
            _admission_errors(
                self.registry,
                non_subject_registries=self.non_subject_registries,
            ),
        )

    def test_definition_artifacts_are_exact_raw_bytes(self) -> None:
        for subject_id, expected in EXPECTED_SUBJECTS.items():
            with self.subTest(subject_id=subject_id):
                artifact_path = ROOT / expected["locator"]
                self.assertTrue(artifact_path.is_file())
                actual = hashlib.sha256(artifact_path.read_bytes()).hexdigest()
                self.assertEqual(expected["digest"], actual)
                entry = _entries_by_id(self.registry)[subject_id]
                digest = entry["definition_artifact"]["digest"]
                self.assertEqual(actual, digest["value"])
                self.assertEqual("RAW_FILE_BYTES", digest["scope"])
                self.assertEqual("VERIFIED", digest["status"])

    def test_admission_dossiers_bind_final_coordinates_and_keep_claim_boundary(self) -> None:
        entries = _entries_by_id(self.registry)
        for subject_id, expected in EXPECTED_SUBJECTS.items():
            with self.subTest(subject_id=subject_id):
                dossier = (ROOT / expected["dossier"]).read_text(encoding="utf-8")
                for token in (
                    subject_id,
                    expected["subject_series"],
                    expected["subject_kind"],
                    expected["artifact_id"],
                    expected["locator"],
                    expected["digest"],
                    EXPECTED_SCHEMA_ID,
                    "LAYER_1_FOUNDATIONAL_RESEARCH",
                    "NOT_APPLICABLE",
                ):
                    self.assertIn(token, dossier)
                self.assertIsNone(FALSE_MILESTONE_COMPLETION.search(dossier))
                self.assertRegex(dossier.lower(), r"not independent scientific validation")
                self.assertRegex(
                    dossier.lower(),
                    r"(?:scientific finding(?:s)? asserted[^\n]*none|"
                    r"scientific findings asserted[^\n]*none)",
                )
                self.assertEqual(
                    entries[subject_id],
                    _dossier_registry_specimen(dossier, subject_id),
                    "the dossier's one final registry specimen must exactly match production",
                )

    def test_non_subject_registries_and_real_record_areas_remain_empty(self) -> None:
        for relative, registry in self.non_subject_registries.items():
            with self.subTest(registry=relative):
                self.assertEqual([], registry.get("entries"))
        for relative in CANONICAL_RECORD_DIRECTORIES:
            directory = ROOT / relative
            if directory.is_dir():
                self.assertEqual([], sorted(directory.rglob("*.json")), relative)

    def test_admission_material_remains_product_independent(self) -> None:
        common_paths = [SUBJECT_REGISTRY]
        for expected in EXPECTED_SUBJECTS.values():
            common_paths.append(ROOT / expected["dossier"])
        for path in common_paths:
            with self.subTest(path=path.relative_to(ROOT).as_posix()):
                text = path.read_text(encoding="utf-8")
                self.assertIsNone(SPECIFIC_PRODUCT.search(text))
                self.assertIn("product-independent", text.lower())
        for expected in EXPECTED_SUBJECTS.values():
            path = ROOT / expected["locator"]
            with self.subTest(path=path.relative_to(ROOT).as_posix()):
                text = path.read_text(encoding="utf-8")
                self.assertIsNone(SPECIFIC_PRODUCT.search(text))
                self.assertIn(expected["independence_marker"], text.lower())

    def test_digest_substitution_is_rejected(self) -> None:
        mutated = copy.deepcopy(self.registry)
        mutated["entries"][0]["definition_artifact"]["digest"]["value"] = "0" * 64
        errors = _admission_errors(mutated)
        self.assertTrue(any("digest" in error for error in errors), errors)

    def test_subject_kind_swap_is_rejected(self) -> None:
        mutated = copy.deepcopy(self.registry)
        first_kind = mutated["entries"][0]["subject_kind"]
        mutated["entries"][0]["subject_kind"] = mutated["entries"][1]["subject_kind"]
        mutated["entries"][1]["subject_kind"] = first_kind
        errors = _admission_errors(mutated)
        self.assertTrue(any("subject_kind" in error for error in errors), errors)

    def test_locator_substitution_and_path_escape_are_rejected(self) -> None:
        substitution = copy.deepcopy(self.registry)
        substitution["entries"][0]["definition_artifact"]["locator"] = (
            EXPECTED_SUBJECTS["LCMRP-FSUBJ-0002-FORMAL-MEMORY-OBJECT-MODEL"]["locator"]
        )
        substitution_errors = _admission_errors(substitution)
        self.assertTrue(any("locator" in error for error in substitution_errors))

        escape = copy.deepcopy(self.registry)
        escape["entries"][0]["definition_artifact"]["locator"] = "../outside.md"
        escape_errors = _admission_errors(escape)
        self.assertTrue(any("locator" in error for error in escape_errors))
        validator = Draft202012Validator(self.schema, format_checker=FormatChecker())
        self.assertTrue(list(validator.iter_errors(escape)))

    def test_duplicate_active_identity_series_and_version_are_rejected(self) -> None:
        duplicate_version = copy.deepcopy(self.registry)
        duplicate_version["entries"].append(copy.deepcopy(duplicate_version["entries"][0]))
        version_errors = _admission_errors(duplicate_version)
        self.assertTrue(
            any("duplicate subject ID/version" in error for error in version_errors),
            version_errors,
        )

        duplicate_series = copy.deepcopy(self.registry)
        duplicate_series["entries"][1]["subject_series"] = duplicate_series["entries"][0][
            "subject_series"
        ]
        series_errors = _admission_errors(duplicate_series)
        self.assertTrue(any("duplicate subject series" in error for error in series_errors))

    def test_false_validation_adoption_and_completion_claims_are_rejected(self) -> None:
        for claim in (
            "This subject is scientifically validated.",
            "This taxonomy has been adopted.",
            "M1 is now complete.",
        ):
            with self.subTest(claim=claim):
                mutated = copy.deepcopy(self.registry)
                mutated["entries"][0]["boundary"] = claim
                errors = _admission_errors(mutated)
                self.assertTrue(any("false validation" in error for error in errors), errors)

    def test_accidental_study_finding_closeout_or_evidence_effect_is_rejected(self) -> None:
        for relative in NON_SUBJECT_REGISTRIES:
            with self.subTest(registry=relative):
                contaminated = copy.deepcopy(self.non_subject_registries)
                contaminated[relative]["entries"] = [{"unexpected": "admission side effect"}]
                errors = _admission_errors(
                    self.registry,
                    non_subject_registries=contaminated,
                )
                self.assertTrue(any(relative in error for error in errors), errors)

    def test_registry_contains_no_mechanism_label_or_evidence_decision_fields(self) -> None:
        forbidden_keys = {
            "awarded_labels",
            "evidence_decision",
            "evidence_state",
            "mechanism_id",
            "mechanism_version",
            "maturity_label",
        }
        serialized = json.loads(json.dumps(self.registry))

        def walk(value: Any) -> Iterable[str]:
            if isinstance(value, Mapping):
                for key, child in value.items():
                    yield key
                    yield from walk(child)
            elif isinstance(value, list):
                for child in value:
                    yield from walk(child)

        present = forbidden_keys.intersection(walk(serialized))
        self.assertEqual(set(), present)
        self.assertEqual(
            {"NOT_APPLICABLE"},
            {
                text
                for text in _iter_strings(serialized)
                if text == "NOT_APPLICABLE"
            },
        )


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
