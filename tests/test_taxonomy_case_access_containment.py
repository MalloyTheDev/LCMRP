"""Synthetic adversarial gates for pre-intake taxonomy case containment.

Research layer: program infrastructure supporting Layer 1 — Foundational
Research. These tests create no result, finding, closeout, or evidence effect.
Production taxonomy case bodies are never opened by this module.
"""

from __future__ import annotations

import hashlib
import json
import os
from dataclasses import replace
from pathlib import Path
import subprocess
import sys
import tempfile
from typing import Any, Callable
import unittest

import yaml

from tools.taxonomy_case_access import build_study_access_catalog
from tools.validate_repository import (
    RepositoryValidationError,
    load_json,
    validate_local_artifact_references,
    validate_repository,
    validate_serialized_documents,
)


ROOT = Path(__file__).resolve().parents[1]
RUNNER = ROOT / "tests" / "run_no_case_access_gate.py"
DEFAULT_PROTECTED_ROOT = (
    ROOT / "studies" / "foundational" / "m1-taxonomy-v1" / "cases"
)
BLOCKED_EXIT_STATUS = 97


def _raw_sha256(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def _write_bytes(root: Path, locator: str, payload: bytes) -> Path:
    path = root / locator
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(payload)
    return path


def _write_json(root: Path, locator: str, document: Any) -> tuple[Path, str]:
    payload = json.dumps(document, indent=2, sort_keys=True).encode("utf-8") + b"\n"
    path = _write_bytes(root, locator, payload)
    return path, _raw_sha256(payload)


def _record_open_attempts(*targets: Path) -> list[Path]:
    attempts: list[Path] = []
    target_reals = {Path(os.path.realpath(target)) for target in targets}
    target_inodes: set[tuple[int, int]] = set()
    for target in targets:
        try:
            target_stat = target.stat()
        except OSError:
            continue
        target_inodes.add((target_stat.st_dev, target_stat.st_ino))

    def audit(event: str, arguments: tuple[object, ...]) -> None:
        if event != "open" or not arguments:
            return
        candidate = arguments[0]
        if isinstance(candidate, int) or not isinstance(
            candidate,
            (str, bytes, os.PathLike),
        ):
            return
        try:
            path = Path(os.path.realpath(os.fsdecode(os.fspath(candidate))))
        except (OSError, TypeError, ValueError):
            return
        try:
            candidate_stat = path.stat()
            candidate_inode = (candidate_stat.st_dev, candidate_stat.st_ino)
        except OSError:
            candidate_inode = None
        if path in target_reals or candidate_inode in target_inodes:
            attempts.append(path)

    sys.addaudithook(audit)
    return attempts


class SyntheticCatalogRepository:
    """Minimal metadata authority plus conspicuously synthetic opaque bytes."""

    def __init__(self, root: Path, *, case_directory: str = "opaque-inputs") -> None:
        self.root = root
        self.case_locator = (
            f"studies/foundational/synthetic-taxonomy-v1/{case_directory}/case.json"
        )
        self.negative_case_locator = (
            "studies/foundational/synthetic-taxonomy-v1/"
            f"{case_directory}/negative-case.json"
        )
        self.output_locator = (
            "studies/foundational/synthetic-taxonomy-v1/generated/ledger.json"
        )
        self.case_payload = b'{"synthetic_non_evidence": true}\n'
        self.case_path = _write_bytes(root, self.case_locator, self.case_payload)
        self.negative_case_path = _write_bytes(
            root,
            self.negative_case_locator,
            self.case_payload,
        )
        self.manifests: dict[int, dict[str, Any]] = {}
        self.entries: dict[int, dict[str, Any]] = {}
        self.add_version(1, registry_status="ACTIVE")

    @property
    def case_paths(self) -> tuple[Path, Path]:
        return self.case_path, self.negative_case_path

    def _artifact_reference(
        self,
        locator: str,
        artifact_id: str,
    ) -> dict[str, Any]:
        return {
            "artifact_id": artifact_id,
            "artifact_version": 1,
            "schema_id": "urn:lcmrp:synthetic-case:0.0.0",
            "locator": locator,
            "digest": {
                "algorithm": "SHA-256",
                "status": "VERIFIED",
                "value": _raw_sha256(self.case_payload),
                "scope": "RAW_FILE_BYTES",
            },
            "media_type": "application/json",
        }

    def _output_reference(self, locator: str, version: int) -> dict[str, Any]:
        return {
            "artifact_id": f"ARTIFACT-SYNTHETIC-OUTPUT-V{version}",
            "artifact_version": version,
            "schema_id": "urn:lcmrp:synthetic-output:0.0.0",
            "locator": locator,
            "digest": {
                "algorithm": "SHA-256",
                "status": "PENDING",
                "value": None,
                "scope": "RAW_FILE_BYTES",
            },
            "media_type": "application/json",
        }

    def _manifest(
        self,
        version: int,
        previous_digest: str | None,
        positive_case_locator: str,
        negative_case_locator: str,
    ) -> dict[str, Any]:
        if version == 1:
            amendment = {
                "kind": "INITIAL",
                "supersedes_record_version": None,
                "supersedes_artifact_digest": None,
            }
        else:
            amendment = {
                "kind": "SUPERSEDING_RECORD",
                "supersedes_record_version": version - 1,
                "supersedes_artifact_digest": {
                    "algorithm": "SHA-256",
                    "value": previous_digest,
                    "scope": "RAW_FILE_BYTES",
                },
            }
        output_locator = (
            self.output_locator
            if version == 1
            else f"studies/foundational/synthetic-taxonomy-v{version}/generated/ledger.json"
        )
        return {
            "artifact_type": "foundational_study_manifest",
            "study_record_id": "LCMRP-FSTUDYREC-9999-SYNTHETIC-TAXONOMY",
            "record_version": version,
            "record_status": "FROZEN",
            "study_id": "LCMRP-FSTUDY-9999-SYNTHETIC-TAXONOMY",
            "amendment": amendment,
            "subject": {
                "subject_kind": "MEMORY_TAXONOMY",
                "subject_id": "LCMRP-FSUBJ-9999-SYNTHETIC-TAXONOMY",
                "subject_version": 1,
            },
            "primary_method_profile": {
                "profile_kind": "STRUCTURAL_OR_TAXONOMY_EVALUATION",
                "profile_id": "LCMRP-MPROF-9999-SYNTHETIC-TAXONOMY",
                "profile_series": "LCMRP-MPROF-SERIES-9999-SYNTHETIC",
                "profile_version": 1,
                "positive_case_source_ids": [
                    "SOURCE-9999-SYNTHETIC-POSITIVE"
                ],
                "negative_case_source_ids": [
                    "SOURCE-9999-SYNTHETIC-NEGATIVE"
                ],
            },
            "sources": [
                {
                    "source_id": "SOURCE-9999-SYNTHETIC-POSITIVE",
                    "source_kind": "SYNTHETIC_CASE_SET",
                    "role": "POSITIVE_CASES",
                    "human_subjects_involved": False,
                    "provenance_artifact": self._artifact_reference(
                        positive_case_locator,
                        "ARTIFACT-SYNTHETIC-POSITIVE-CASE",
                    ),
                },
                {
                    "source_id": "SOURCE-9999-SYNTHETIC-NEGATIVE",
                    "source_kind": "SYNTHETIC_CASE_SET",
                    "role": "NEGATIVE_CASES",
                    "human_subjects_involved": False,
                    "provenance_artifact": self._artifact_reference(
                        negative_case_locator,
                        "ARTIFACT-SYNTHETIC-NEGATIVE-CASE",
                    ),
                },
            ],
            "analyses": [
                {
                    "analysis_id": "ANALYSIS-9999-SYNTHETIC",
                    "planned_output_artifact": self._output_reference(
                        output_locator,
                        version,
                    ),
                }
            ],
        }

    def add_version(
        self,
        version: int,
        *,
        registry_status: str,
        supersede_previous: bool = True,
        case_locator: str | None = None,
    ) -> None:
        previous_entry = self.entries.get(version - 1)
        previous_digest = (
            previous_entry["artifact_digest"]["value"]
            if previous_entry is not None
            else None
        )
        if supersede_previous and previous_entry is not None:
            previous_entry["registry_status"] = "SUPERSEDED"
        effective_case_locator = case_locator or self.case_locator
        effective_negative_locator = (
            str(Path(effective_case_locator).with_name("negative-case.json"))
            if case_locator is not None
            else self.negative_case_locator
        )
        if case_locator is not None:
            _write_bytes(self.root, effective_case_locator, self.case_payload)
            _write_bytes(self.root, effective_negative_locator, self.case_payload)
        manifest = self._manifest(
            version,
            previous_digest,
            effective_case_locator,
            effective_negative_locator,
        )
        locator = (
            "records/foundational/studies/"
            f"LCMRP-FSTUDYREC-9999-SYNTHETIC-TAXONOMY-v{version}.json"
        )
        _path, digest = _write_json(self.root, locator, manifest)
        self.manifests[version] = manifest
        self.entries[version] = {
            "record_id": manifest["study_record_id"],
            "record_version": version,
            "artifact_type": "foundational_study_manifest",
            "schema_id": "urn:lcmrp:schema:foundational-study-manifest:0.1.0",
            "artifact_path": locator,
            "artifact_digest": {
                "algorithm": "SHA-256",
                "value": digest,
                "scope": "RAW_FILE_BYTES",
            },
            "registry_status": registry_status,
        }
        self.write_registry()

    def rewrite_manifest(
        self,
        version: int,
        mutation: Callable[[dict[str, Any]], None],
    ) -> None:
        manifest = self.manifests[version]
        mutation(manifest)
        locator = self.entries[version]["artifact_path"]
        _path, digest = _write_json(self.root, locator, manifest)
        self.entries[version]["artifact_digest"]["value"] = digest
        self.write_registry()

    def write_registry(self) -> None:
        registry = {
            "schema_version": "0.1.0",
            "artifact_type": "foundational_record_index",
            "registry_type": "foundational_study_registry",
            "entries": [self.entries[version] for version in sorted(self.entries)],
        }
        path = self.root / "registry" / "foundational-studies.yaml"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(yaml.safe_dump(registry, sort_keys=False), encoding="utf-8")


class TaxonomyCaseCatalogTests(unittest.TestCase):
    def fixture(self, *, case_directory: str = "opaque-inputs") -> SyntheticCatalogRepository:
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        return SyntheticCatalogRepository(
            Path(temporary.name) / "repository",
            case_directory=case_directory,
        )

    def test_case_classification_is_metadata_driven_and_body_is_not_opened(self) -> None:
        fixture = self.fixture(case_directory="not-named-cases")
        attempts = _record_open_attempts(*fixture.case_paths)

        catalog = build_study_access_catalog(fixture.root)

        self.assertEqual((), catalog.errors)
        self.assertEqual([], attempts)
        self.assertEqual(2, len(catalog.case_artifacts))
        self.assertIn("not-named-cases", catalog.case_artifacts[0].locator)

    def test_v1_superseded_v2_active_preserves_the_union(self) -> None:
        fixture = self.fixture()
        second_locator = (
            "studies/foundational/synthetic-taxonomy-v2/distinct-inputs/case.json"
        )
        fixture.add_version(
            2,
            registry_status="ACTIVE",
            case_locator=second_locator,
        )
        attempts = _record_open_attempts(
            *fixture.case_paths,
            fixture.root / second_locator,
            fixture.root / str(Path(second_locator).with_name("negative-case.json")),
        )

        catalog = build_study_access_catalog(fixture.root)

        self.assertEqual((), catalog.errors)
        self.assertEqual({1, 2}, {item.record_version for item in catalog.taxonomy_studies})
        self.assertEqual(4, len(catalog.case_artifacts))
        self.assertEqual(2, len(catalog.case_roots))
        self.assertEqual([], attempts)

    def test_duplicate_active_broken_lineage_and_output_reuse_fail_closed(self) -> None:
        mutations = {
            "duplicate_active": lambda fixture: fixture.entries[1].__setitem__(
                "registry_status", "ACTIVE"
            ),
            "broken_predecessor": lambda fixture: fixture.rewrite_manifest(
                2,
                lambda manifest: manifest["amendment"][
                    "supersedes_artifact_digest"
                ].__setitem__("value", "0" * 64),
            ),
            "output_reuse": lambda fixture: fixture.rewrite_manifest(
                2,
                lambda manifest: manifest["analyses"][0][
                    "planned_output_artifact"
                ].__setitem__("locator", fixture.output_locator),
            ),
            "divergent_study_id": lambda fixture: fixture.rewrite_manifest(
                2,
                lambda manifest: manifest.__setitem__(
                    "study_id",
                    "LCMRP-FSTUDY-9998-DIVERGENT-SYNTHETIC-TAXONOMY",
                ),
            ),
            "skipped_predecessor": lambda fixture: fixture.rewrite_manifest(
                2,
                lambda manifest: manifest.__setitem__("record_version", 3),
            ),
        }
        for name, mutation in mutations.items():
            with self.subTest(name=name):
                fixture = self.fixture()
                fixture.add_version(2, registry_status="ACTIVE")
                mutation(fixture)
                fixture.write_registry()
                catalog = build_study_access_catalog(fixture.root)
                self.assertTrue(catalog.errors, name)

    def test_unsafe_case_locators_are_rejected_without_opening_the_original_case(self) -> None:
        locators = (
            "../escape.json",
            "/absolute.json",
            "studies\\foundational\\case.json",
            "https://example.invalid/case.json",
            "studies/foundational/../case.json",
            "studies/foundational/case\x00.json",
            "studies/foundational/caf\N{LATIN SMALL LETTER E WITH ACUTE}/case.json",
        )
        for locator in locators:
            with self.subTest(locator=repr(locator)):
                fixture = self.fixture()
                attempts = _record_open_attempts(*fixture.case_paths)
                fixture.rewrite_manifest(
                    1,
                    lambda manifest, value=locator: manifest["sources"][0][
                        "provenance_artifact"
                    ].__setitem__("locator", value),
                )
                catalog = build_study_access_catalog(fixture.root)
                self.assertTrue(catalog.errors)
                self.assertEqual([], attempts)

    def test_existing_escape_targets_are_rejected_before_access(self) -> None:
        for name in ("parent-traversal", "absolute-path"):
            with self.subTest(name=name):
                fixture = self.fixture()
                escaped = fixture.root.parent / f"{name}.json"
                escaped.write_bytes(b'{"synthetic_escape_trap": true}\n')
                locator = (
                    f"../{escaped.name}"
                    if name == "parent-traversal"
                    else str(escaped)
                )
                attempts = _record_open_attempts(*fixture.case_paths, escaped)
                fixture.rewrite_manifest(
                    1,
                    lambda manifest, value=locator: manifest["sources"][0][
                        "provenance_artifact"
                    ].__setitem__("locator", value),
                )

                catalog = build_study_access_catalog(fixture.root)

                self.assertTrue(catalog.errors)
                self.assertEqual([], attempts)

    def test_all_case_locators_can_be_corrupt_without_disabling_policy(self) -> None:
        fixture = self.fixture()
        escaped_paths = (
            fixture.root.parent / "escaped-positive.json",
            fixture.root.parent / "escaped-negative.json",
        )
        for escaped in escaped_paths:
            escaped.write_bytes(b'{"synthetic_escape_trap": true}\n')
        attempts = _record_open_attempts(*fixture.case_paths, *escaped_paths)

        def mutate(manifest: dict[str, Any]) -> None:
            for source, escaped in zip(manifest["sources"], escaped_paths):
                source["provenance_artifact"]["locator"] = f"../{escaped.name}"

        fixture.rewrite_manifest(1, mutate)
        catalog = build_study_access_catalog(fixture.root)

        self.assertTrue(catalog.errors)
        self.assertEqual([], attempts)

    def test_classification_tampering_still_protects_the_case_union(self) -> None:
        mutations = {
            "profile_kind": lambda manifest: manifest[
                "primary_method_profile"
            ].__setitem__("profile_kind", "FORMAL_ANALYSIS"),
            "source_kind": lambda manifest: manifest["sources"][0].__setitem__(
                "source_kind", "PRIOR_WORK"
            ),
            "source_role": lambda manifest: manifest["sources"][0].__setitem__(
                "role", "DEVELOPMENT"
            ),
        }
        for name, mutation in mutations.items():
            with self.subTest(name=name):
                fixture = self.fixture()
                attempts = _record_open_attempts(*fixture.case_paths)
                fixture.rewrite_manifest(1, mutation)

                catalog = build_study_access_catalog(fixture.root)

                self.assertTrue(catalog.errors)
                self.assertEqual(2, len(catalog.case_artifacts))
                self.assertEqual([], attempts)

    def test_source_metadata_survives_profile_and_subject_tampering(self) -> None:
        fixture = self.fixture()
        attempts = _record_open_attempts(*fixture.case_paths)

        def mutate(manifest: dict[str, Any]) -> None:
            manifest["subject"]["subject_kind"] = "FORMAL_MEMORY_MODEL"
            profile = manifest["primary_method_profile"]
            profile["profile_kind"] = "FORMAL_ANALYSIS"
            profile.pop("positive_case_source_ids")
            profile.pop("negative_case_source_ids")

        fixture.rewrite_manifest(1, mutate)
        catalog = build_study_access_catalog(fixture.root)

        self.assertTrue(catalog.errors)
        self.assertEqual(2, len(catalog.case_artifacts))
        self.assertEqual([], attempts)

    def test_compound_case_classification_tampering_fails_before_access(self) -> None:
        fixture = self.fixture()
        attempts = _record_open_attempts(*fixture.case_paths)

        def mutate(manifest: dict[str, Any]) -> None:
            source = manifest["sources"][0]
            source["source_kind"] = "OTHER_NON_HUMAN_SOURCE"
            source["role"] = "PRIOR_WORK"

        fixture.rewrite_manifest(1, mutate)
        catalog = build_study_access_catalog(fixture.root)

        self.assertTrue(catalog.errors)
        self.assertEqual(2, len(catalog.case_artifacts))
        self.assertEqual([], attempts)

    def test_output_namespace_descendants_are_opaque(self) -> None:
        fixture = self.fixture()
        catalog = build_study_access_catalog(fixture.root)
        planned = fixture.root / fixture.output_locator
        descendant = planned.parent / "nested" / "undeclared.json"

        self.assertEqual((), catalog.errors)
        self.assertTrue(catalog.protects_path(planned))
        self.assertTrue(catalog.protects_path(descendant))

    def test_forged_clean_catalog_cannot_disable_authoritative_protection(self) -> None:
        fixture = self.fixture()
        authoritative = build_study_access_catalog(fixture.root)
        forged = replace(authoritative, case_artifacts=())
        attempts = _record_open_attempts(*fixture.case_paths)

        errors = validate_serialized_documents(fixture.root, forged)

        self.assertTrue(
            any(
                "policy" in error.lower() or "authoritative" in error.lower()
                for error in errors
            ),
            errors,
        )
        self.assertEqual([], attempts)

    def test_raw_loader_without_policy_denies_before_access(self) -> None:
        fixture = self.fixture()
        attempts = _record_open_attempts(fixture.case_path)

        with self.assertRaisesRegex(
            RepositoryValidationError,
            "policy is unavailable",
        ):
            load_json(fixture.case_path)

        self.assertEqual([], attempts)

    def test_symlink_hard_link_and_undeclared_namespace_entries_are_rejected(self) -> None:
        with self.subTest(kind="symlink"):
            fixture = self.fixture()
            outside = _write_bytes(fixture.root, "outside.json", fixture.case_payload)
            fixture.case_path.unlink()
            fixture.case_path.symlink_to(outside)
            attempts = _record_open_attempts(outside, fixture.negative_case_path)
            self.assertTrue(build_study_access_catalog(fixture.root).errors)
            self.assertEqual([], attempts)

        with self.subTest(kind="symlink-alias"):
            fixture = self.fixture()
            alias = fixture.root / "case-alias.json"
            alias.symlink_to(fixture.case_path)
            attempts = _record_open_attempts(*fixture.case_paths)
            errors = build_study_access_catalog(fixture.root).errors
            self.assertTrue(any("symlink is forbidden" in error for error in errors), errors)
            self.assertEqual([], attempts)

        with self.subTest(kind="ancestor-symlink"):
            fixture = self.fixture()
            case_parent = fixture.case_path.parent
            relocated = fixture.root / "relocated-opaque-inputs"
            case_parent.rename(relocated)
            case_parent.symlink_to(relocated)
            attempts = _record_open_attempts(
                relocated / fixture.case_path.name,
                relocated / fixture.negative_case_path.name,
            )
            self.assertTrue(build_study_access_catalog(fixture.root).errors)
            self.assertEqual([], attempts)

        with self.subTest(kind="hard-link"):
            fixture = self.fixture()
            alias = fixture.root / "hard-link-alias.json"
            os.link(fixture.case_path, alias)
            attempts = _record_open_attempts(*fixture.case_paths, alias)
            self.assertTrue(build_study_access_catalog(fixture.root).errors)
            self.assertEqual([], attempts)

        with self.subTest(kind="undeclared"):
            fixture = self.fixture()
            undeclared = _write_bytes(
                fixture.root,
                str(Path(fixture.case_locator).parent / "undeclared.json"),
                b"{}\n",
            )
            attempts = _record_open_attempts(undeclared)
            errors = build_study_access_catalog(fixture.root).errors
            self.assertTrue(any("undeclared entry" in error for error in errors), errors)
            self.assertEqual([], attempts)

        with self.subTest(kind="undeclared-output"):
            fixture = self.fixture()
            undeclared = _write_bytes(
                fixture.root,
                "studies/foundational/synthetic-taxonomy-v1/generated/unplanned.json",
                b"{}\n",
            )
            attempts = _record_open_attempts(undeclared)
            errors = build_study_access_catalog(fixture.root).errors
            self.assertTrue(
                any("planned-output namespace" in error for error in errors),
                errors,
            )
            self.assertEqual([], attempts)

    def test_non_authoritative_reference_is_rejected_without_case_access(self) -> None:
        fixture = self.fixture()
        attempts = _record_open_attempts(*fixture.case_paths)
        _write_json(
            fixture.root,
            "public-reference.json",
            {
                "artifact": {
                    "locator": fixture.case_locator,
                    "digest": {
                        "algorithm": "SHA-256",
                        "status": "VERIFIED",
                        "value": _raw_sha256(fixture.case_payload),
                    },
                }
            },
        )

        errors = validate_local_artifact_references(fixture.root)

        self.assertTrue(any("non-authoritative" in error for error in errors), errors)
        self.assertEqual([], attempts)

    def test_malformed_bootstrap_aborts_before_broad_json_scans(self) -> None:
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        root = Path(temporary.name)
        trap = _write_bytes(root, "trap.json", b'{"would_be_opened": true}\n')
        registry = root / "registry" / "foundational-studies.yaml"
        registry.parent.mkdir(parents=True)
        registry.write_text("registry_type: [malformed\n", encoding="utf-8")
        attempts = _record_open_attempts(trap)

        errors = validate_repository(root)

        self.assertTrue(any("policy is unavailable" in error for error in errors), errors)
        self.assertEqual([], attempts)


class ProcessCaseAccessGateTests(unittest.TestCase):
    def _run_command(
        self,
        protected_root: Path,
        command: list[str],
        *,
        environment: dict[str, str] | None = None,
    ) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [
                sys.executable,
                str(RUNNER),
                "--protected-root",
                str(protected_root),
                "--",
                *command,
            ],
            cwd=ROOT,
            env=environment,
            text=True,
            capture_output=True,
            check=False,
        )

    def _run(self, protected_root: Path, code: str) -> subprocess.CompletedProcess[str]:
        return self._run_command(
            protected_root,
            [sys.executable, "-c", code],
        )

    def test_gate_blocks_synthetic_protected_open_with_dedicated_status(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            protected_root = Path(directory) / "protected"
            protected = _write_bytes(protected_root, "case.json", b"synthetic\n")
            alias = Path(directory) / "case-alias.json"
            alias.symlink_to(protected)
            hard_link = Path(directory) / "case-hard-link.json"
            os.link(protected, hard_link)
            attempts = {
                "pathlib": (
                    f"from pathlib import Path; Path({str(protected)!r}).read_bytes()"
                ),
                "os-open": (
                    f"import os; descriptor = os.open({str(protected)!r}, os.O_RDONLY); "
                    "os.close(descriptor)"
                ),
                "symlink-alias": (
                    f"from pathlib import Path; Path({str(alias)!r}).read_bytes()"
                ),
                "hard-link-alias": (
                    f"from pathlib import Path; Path({str(hard_link)!r}).read_bytes()"
                ),
                "module-global-tamper": (
                    "import sitecustomize; from pathlib import Path; "
                    "sitecustomize.PROTECTED_ROOTS = (); "
                    "sitecustomize._block_if_protected = lambda *a, **k: None; "
                    f"Path({str(protected)!r}).read_bytes()"
                ),
                "dir-fd-relative-os-open": (
                    f"import os; parent = os.open({str(Path(directory))!r}, "
                    "os.O_RDONLY | os.O_DIRECTORY); "
                    "descriptor = os.open('protected/case.json', os.O_RDONLY, "
                    "dir_fd=parent); os.close(descriptor); os.close(parent)"
                ),
            }
            for name, code in attempts.items():
                with self.subTest(name=name):
                    completed = self._run(protected_root, code)
                    self.assertEqual(
                        BLOCKED_EXIT_STATUS,
                        completed.returncode,
                        completed,
                    )
                    self.assertIn("LCMRP_CASE_ACCESS_BLOCKED", completed.stderr)

    def test_gate_allows_unprotected_body_open(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            protected_root = root / "protected"
            protected_root.mkdir()
            allowed = _write_bytes(root, "allowed.json", b"{}\n")
            completed = self._run(
                protected_root,
                f"from pathlib import Path; Path({str(allowed)!r}).read_bytes()",
            )

        self.assertEqual(0, completed.returncode, completed)

    def test_gate_allows_protected_metadata_operations(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            protected_root = root / "protected"
            protected = _write_bytes(protected_root, "case.json", b"synthetic\n")
            alias = root / "case-link.json"
            alias.symlink_to(protected)
            code = (
                "import os; "
                f"os.stat({str(protected)!r}); "
                f"os.lstat({str(protected)!r}); "
                f"os.readlink({str(alias)!r})"
            )
            completed = self._run(protected_root, code)

        self.assertEqual(0, completed.returncode, completed)

    def test_catalog_discovered_output_namespace_is_write_blocked(self) -> None:
        catalog = build_study_access_catalog(ROOT)
        self.assertEqual((), catalog.errors)
        output_probe = catalog.output_roots[0] / "unauthorized-probe.json"
        self.assertFalse(output_probe.exists())
        with tempfile.TemporaryDirectory() as directory:
            explicit = Path(directory) / "explicit"
            explicit.mkdir()
            completed = self._run(
                explicit,
                f"open({str(output_probe)!r}, 'wb')",
            )

        self.assertEqual(BLOCKED_EXIT_STATUS, completed.returncode, completed)
        self.assertIn("LCMRP_CASE_ACCESS_BLOCKED", completed.stderr)
        self.assertFalse(output_probe.exists())

    def test_explicit_roots_union_with_inherited_production_protection(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            explicit = Path(directory) / "explicit"
            explicit.mkdir()
            catalog = build_study_access_catalog(ROOT)
            self.assertEqual((), catalog.errors)
            production_output_root = catalog.output_roots[0]
            code = (
                "import os; from pathlib import Path; "
                "roots = {Path(os.path.realpath(value)) for value in "
                "os.environ['LCMRP_PROTECTED_CASE_ROOTS'].split(os.pathsep) if value}; "
                f"assert Path({str(explicit.resolve())!r}) in roots; "
                f"assert Path({str(DEFAULT_PROTECTED_ROOT.resolve())!r}) in roots; "
                f"assert Path({str(production_output_root)!r}) in roots"
            )
            completed = self._run(explicit, code)

        self.assertEqual(0, completed.returncode, completed)

    def test_runner_rejects_python_isolation_and_environment_wrappers(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            protected_root = Path(directory) / "protected"
            protected_root.mkdir()
            commands = {
                "no-site": [sys.executable, "-S", "-c", "pass"],
                "isolated": [sys.executable, "-I", "-c", "pass"],
                "ignore-environment": [sys.executable, "-E", "-c", "pass"],
                "environment-wrapper": [
                    "/usr/bin/env",
                    "-i",
                    sys.executable,
                    "-c",
                    "pass",
                ],
            }
            for name, command in commands.items():
                with self.subTest(name=name):
                    completed = self._run_command(protected_root, command)
                    self.assertEqual(BLOCKED_EXIT_STATUS, completed.returncode)
                    self.assertIn("LCMRP_CASE_ACCESS_BLOCKED", completed.stderr)

    def test_runner_rejects_an_earlier_foreign_python_on_path(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            protected_root = root / "protected"
            protected_root.mkdir()
            shadow_directory = root / "shadow-bin"
            shadow_directory.mkdir()
            shadow = shadow_directory / "python"
            shadow.write_text("#!/bin/sh\nexit 0\n", encoding="utf-8")
            shadow.chmod(0o755)
            environment = os.environ.copy()
            environment["PATH"] = os.pathsep.join(
                (
                    str(shadow_directory),
                    str(Path(sys.executable).parent),
                    environment.get("PATH", ""),
                )
            )

            completed = self._run_command(
                protected_root,
                ["python", "-c", "pass"],
                environment=environment,
            )

        self.assertEqual(BLOCKED_EXIT_STATUS, completed.returncode)
        self.assertIn("LCMRP_CASE_ACCESS_BLOCKED", completed.stderr)

    def test_runner_bootstrap_denies_study_tree_body_open(self) -> None:
        trap = ROOT / "studies" / "foundational" / "bootstrap-open-trap.json"
        code = (
            "from tests.run_no_case_access_gate import "
            "_install_bootstrap_access_audit; "
            "_install_bootstrap_access_audit(); "
            f"open({str(trap)!r}, 'rb')"
        )
        completed = subprocess.run(
            [sys.executable, "-c", code],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )

        self.assertNotEqual(0, completed.returncode)
        self.assertIn("catalog bootstrap attempted", completed.stderr)

    def test_gate_rejects_non_python_and_environment_stripping_descendants(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            protected_root = root / "protected"
            protected_root.mkdir()
            shadow_directory = root / "shadow-bin"
            shadow_directory.mkdir()
            shadow = shadow_directory / "python"
            shadow.write_text("#!/bin/sh\nexit 0\n", encoding="utf-8")
            shadow.chmod(0o755)
            attempts = {
                "non-python-subprocess": (
                    "import subprocess; subprocess.run(['/bin/true'], check=True)"
                ),
                "shell": "import os; os.system('true')",
                "stripped-environment": (
                    "import subprocess, sys; "
                    "subprocess.run([sys.executable, '-c', 'pass'], env={}, check=True)"
                ),
                "pythonhome-environment": (
                    "import os, subprocess, sys; env = os.environ.copy(); "
                    "env['PYTHONHOME'] = '/synthetic/unsafe-python-home'; "
                    "subprocess.run([sys.executable, '-c', 'pass'], env=env, check=True)"
                ),
                "deceptive-environment-mapping": (
                    "import os, subprocess, sys\n"
                    "class DeceptiveEnvironment(dict):\n"
                    "    def get(self, key, default=None):\n"
                    "        return os.environ.get(key, default)\n"
                    "env = DeceptiveEnvironment(); "
                    "subprocess.run([sys.executable, '-c', 'pass'], env=env, check=True)"
                ),
                "shadowed-python": (
                    "import os, subprocess; env = os.environ.copy(); "
                    f"env['PATH'] = {str(shadow_directory)!r} + os.pathsep + "
                    "env.get('PATH', ''); "
                    "subprocess.run(['python', '-c', 'pass'], env=env, check=True)"
                ),
                "module-global-process-tamper": (
                    "import sitecustomize, subprocess; "
                    "sitecustomize._process_event = lambda *a, **k: None; "
                    "sitecustomize._is_current_python_executable = "
                    "lambda *a, **k: True; "
                    "subprocess.run(['/bin/true'], check=True)"
                ),
            }
            for name, code in attempts.items():
                with self.subTest(name=name):
                    completed = self._run(protected_root, code)
                    self.assertEqual(BLOCKED_EXIT_STATUS, completed.returncode)
                    self.assertIn("LCMRP_CASE_ACCESS_BLOCKED", completed.stderr)

    def test_repository_validator_completes_under_production_tripwire(self) -> None:
        completed = subprocess.run(
            [
                sys.executable,
                str(RUNNER),
                "--",
                sys.executable,
                str(ROOT / "tools" / "validate_repository.py"),
            ],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )

        self.assertNotEqual(BLOCKED_EXIT_STATUS, completed.returncode, completed.stderr)
        self.assertEqual(0, completed.returncode, completed.stderr)
        self.assertIn("case-byte verification is deferred", completed.stdout)


if __name__ == "__main__":
    unittest.main()
