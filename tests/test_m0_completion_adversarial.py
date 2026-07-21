from __future__ import annotations

import copy
import hashlib
import json
import tempfile
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker

from tools.validate_repository import (
    validate_local_artifact_references,
    validate_registries,
    validate_registry_entry_semantics,
)


ROOT = Path(__file__).resolve().parents[1]


def load_json(relative: str):
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))


def write_json(path: Path, value) -> bytes:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(value, indent=2).encode("utf-8") + b"\n"
    path.write_bytes(payload)
    return payload


def raw_digest(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def immutable_digest(value: str, status: str = "RECORDED"):
    return {
        "algorithm": "SHA-256",
        "status": status,
        "value": value,
        "scope": "RAW_FILE_BYTES",
    }


class SyntheticFoundationalRepository:
    """A complete non-evidentiary subject/study/finding/closeout graph."""

    def __init__(
        self,
        root: Path,
        *,
        analysis_count: int = 2,
        include_closeout: bool = True,
        finding_reference_status: str = "RECORDED",
    ) -> None:
        self.root = root
        self.analysis_count = analysis_count
        self.include_closeout = include_closeout
        self.finding_reference_status = finding_reference_status

        (root / "schemas").mkdir(parents=True)
        (root / "registry").mkdir(parents=True)
        for name in (
            "foundational-record-index.schema.json",
            "foundational-study-manifest.schema.json",
            "research-finding-record.schema.json",
            "foundational-study-closeout.schema.json",
            "foundational-subject-registry.schema.json",
        ):
            (root / "schemas" / name).write_bytes((ROOT / "schemas" / name).read_bytes())

        self.support_payload = write_json(
            root / "records/foundational/support/immutable-input.json",
            {"fixture_notice": "Synthetic M0 contract input; not research evidence."},
        )
        self.subject_payload = write_json(
            root / "records/foundational/subjects/subject-v1.json",
            {
                "fixture_notice": "Synthetic foundational subject; not research evidence.",
                "subject_version": 1,
            },
        )
        self.profile_payload = write_json(
            root / "records/foundational/profiles/profile-v1.json",
            {
                "fixture_notice": "Synthetic method profile; not research evidence.",
                "profile_version": 1,
            },
        )
        (root / "records/foundational/reports").mkdir(parents=True, exist_ok=True)
        self.report_path = "records/foundational/reports/closeout.md"
        (root / self.report_path).write_text(
            "# Synthetic closeout fixture\n\nNot research evidence.\n",
            encoding="utf-8",
        )

        self.subject_entry = self._subject_entry()
        self.subject_registry = {
            "schema_version": "0.1.0",
            "artifact_type": "foundational_subject_registry",
            "registry_type": "foundational_subject_registry",
            "entries": [self.subject_entry],
        }

        self.study = self._frozen_study()
        self.study_path = "records/foundational/studies/study-v1.json"
        study_payload = write_json(root / self.study_path, self.study)
        self.study_entry = self._record_entry(
            record_id=self.study["study_record_id"],
            record_version=1,
            artifact_type="foundational_study_manifest",
            schema_id="urn:lcmrp:schema:foundational-study-manifest:0.1.0",
            artifact_path=self.study_path,
            payload=study_payload,
        )
        self.study_registry = self._index("foundational_study_registry", [self.study_entry])

        self.findings: list[dict] = []
        self.finding_paths: list[str] = []
        self.finding_entries: list[dict] = []
        for index, analysis in enumerate(self.study["analyses"], 1):
            finding = self._published_finding(index, analysis)
            path = f"records/foundational/findings/finding-{index}.json"
            payload = write_json(root / path, finding)
            entry = self._record_entry(
                record_id=finding["record_id"],
                record_version=finding["record_version"],
                artifact_type="research_finding_record",
                schema_id="urn:lcmrp:schema:research-finding-record:0.1.0",
                artifact_path=path,
                payload=payload,
            )
            self.findings.append(finding)
            self.finding_paths.append(path)
            self.finding_entries.append(entry)
        self.finding_registry = self._index(
            "research_finding_registry",
            self.finding_entries,
        )

        self.closeout = None
        self.closeout_path = "records/foundational/closeouts/closeout-v1.json"
        self.closeout_entries: list[dict] = []
        if include_closeout:
            self.closeout = self._published_closeout()
            payload = write_json(root / self.closeout_path, self.closeout)
            self.closeout_entries.append(
                self._record_entry(
                    record_id=self.closeout["record_id"],
                    record_version=1,
                    artifact_type="foundational_study_closeout",
                    schema_id="urn:lcmrp:schema:foundational-study-closeout:0.1.0",
                    artifact_path=self.closeout_path,
                    payload=payload,
                )
            )
        self.closeout_registry = self._index(
            "foundational_study_closeout_registry",
            self.closeout_entries,
        )
        self.write_registries()

    def _artifact(
        self,
        artifact_id: str,
        artifact_version: int,
        schema_id: str,
        locator: str,
        *,
        media_type: str = "application/json",
        status: str = "RECORDED",
    ):
        payload = (self.root / locator).read_bytes()
        return {
            "artifact_id": artifact_id,
            "artifact_version": artifact_version,
            "schema_id": schema_id,
            "locator": locator,
            "digest": immutable_digest(raw_digest(payload), status),
            "media_type": media_type,
        }

    def _subject_entry(self):
        return {
            "target_type": "FOUNDATIONAL_SUBJECT",
            "subject_kind": "MEMORY_TAXONOMY",
            "subject_id": "LCMRP-FSUBJ-9999-ADVERSARIAL",
            "subject_series": "LCMRP-ADVERSARIAL-SUBJECT",
            "subject_version": 1,
            "supersedes_subject_version": None,
            "supersedes_definition_digest": None,
            "entry_status": "ACTIVE",
            "name": "Synthetic adversarial subject",
            "definition": "A synthetic subject used only for M0 contract tests.",
            "boundary": "No mechanism, product, or scientific claim is evaluated.",
            "definition_artifact": self._artifact(
                "ARTIFACT-ADVERSARIAL-SUBJECT",
                1,
                "urn:lcmrp:test:foundational-subject",
                "records/foundational/subjects/subject-v1.json",
            ),
            "research_layer": "LAYER_1_FOUNDATIONAL_RESEARCH",
            "mechanism_maturity_applicability": "NOT_APPLICABLE",
            "registered_at": "2026-07-21T00:00:00Z",
        }

    def _frozen_study(self):
        study = load_json("examples/foundational-study-manifest.example.json")
        study["study_record_id"] = "LCMRP-FSTUDYREC-9999-ADVERSARIAL"
        study["study_id"] = "LCMRP-FSTUDY-9999-ADVERSARIAL"
        study["record_status"] = "FROZEN"
        study["subject"] = {
            key: copy.deepcopy(self.subject_entry[key])
            for key in (
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
        }
        support_artifact = lambda artifact_id: self._artifact(
            artifact_id,
            1,
            "urn:lcmrp:test:immutable-input",
            "records/foundational/support/immutable-input.json",
        )
        profile = study["primary_method_profile"]
        profile["profile_definition_artifact"] = self._artifact(
            "ARTIFACT-ADVERSARIAL-PROFILE",
            1,
            "urn:lcmrp:test:method-profile",
            "records/foundational/profiles/profile-v1.json",
        )
        profile["category_definition_artifact"] = support_artifact(
            "ARTIFACT-ADVERSARIAL-CATEGORIES"
        )
        study["preregistration"] = {
            "status": "FROZEN",
            "results_accessed_before_freeze": False,
            "frozen_at": "2026-07-21T01:00:00Z",
            "registration_authority": "SYNTHETIC-M0-TEST",
            "freeze_artifact": support_artifact("ARTIFACT-ADVERSARIAL-FREEZE"),
        }
        for index, source in enumerate(study["sources"], 1):
            source["provenance_artifact"] = support_artifact(
                f"ARTIFACT-ADVERSARIAL-SOURCE-{index}"
            )
        study["reproducibility"]["environment_artifact"] = support_artifact(
            "ARTIFACT-ADVERSARIAL-ENVIRONMENT"
        )
        study["reproducibility"]["configuration_artifacts"] = [
            support_artifact("ARTIFACT-ADVERSARIAL-CONFIG")
        ]
        study["protocol_artifact"] = support_artifact("ARTIFACT-ADVERSARIAL-PROTOCOL")

        first = study["analyses"][0]
        first["analysis_id"] = "ANALYSIS-ADVERSARIAL-1"
        first["planned_output_artifact"]["artifact_id"] = "ARTIFACT-PLANNED-1"
        first["planned_output_artifact"]["locator"] = (
            "records/foundational/planned/output-1.json"
        )
        analyses = [first]
        for index in range(2, self.analysis_count + 1):
            analysis = copy.deepcopy(first)
            analysis["analysis_id"] = f"ANALYSIS-ADVERSARIAL-{index}"
            analysis["analysis_mode"] = "EXPLORATORY" if index % 2 == 0 else "CONFIRMATORY"
            analysis["planned_output_artifact"]["artifact_id"] = f"ARTIFACT-PLANNED-{index}"
            analysis["planned_output_artifact"]["locator"] = (
                f"records/foundational/planned/output-{index}.json"
            )
            analyses.append(analysis)
        study["analyses"] = analyses
        return study

    def _study_reference(self):
        return {
            "study_id": self.study["study_id"],
            "study_record_id": self.study["study_record_id"],
            "study_record_version": self.study["record_version"],
            "manifest_artifact": self._artifact(
                "ARTIFACT-ADVERSARIAL-STUDY",
                self.study["record_version"],
                "urn:lcmrp:schema:foundational-study-manifest:0.1.0",
                self.study_path,
                status=self.finding_reference_status,
            ),
        }

    def _published_finding(self, index: int, analysis: dict):
        finding = load_json("examples/research-finding-record.example.json")
        suffix = f"ADVERSARIAL-{index}"
        finding["record_id"] = f"LCMRP-FINDREC-9999-{suffix}"
        finding["finding_id"] = f"LCMRP-FIND-9999-{suffix}"
        finding["record_status"] = "PUBLISHED"
        finding["study_reference"] = self._study_reference()
        finding["subject_reference"] = {
            key: copy.deepcopy(self.study["subject"][key])
            for key in (
                "target_type",
                "subject_kind",
                "subject_id",
                "subject_series",
                "subject_version",
            )
        }
        finding["subject_reference"]["definition_artifact"] = copy.deepcopy(
            self.study["subject"]["definition_artifact"]
        )
        finding["subject_reference"]["definition_artifact"]["digest"]["status"] = (
            self.finding_reference_status
        )
        profile = self.study["primary_method_profile"]
        finding["primary_method_profile_reference"] = {
            "profile_kind": profile["profile_kind"],
            "profile_id": profile["profile_id"],
            "profile_series": profile["profile_series"],
            "profile_version": profile["profile_version"],
            "profile_artifact": copy.deepcopy(profile["profile_definition_artifact"]),
        }
        finding["primary_method_profile_reference"]["profile_artifact"]["digest"][
            "status"
        ] = self.finding_reference_status
        finding["analysis_reference"] = {
            "analysis_id": analysis["analysis_id"],
            "analysis_mode": analysis["analysis_mode"],
        }
        finding["claim"]["claim_id"] = f"CLAIM-ADVERSARIAL-{index}"
        finding["created_at"] = f"2026-07-21T02:00:0{index}Z"
        return finding

    def _published_closeout(self):
        closeout = load_json("examples/foundational-study-closeout.example.json")
        closeout["record_id"] = "LCMRP-FCLOSEREC-9999-ADVERSARIAL"
        closeout["closeout_id"] = "LCMRP-FCLOSE-9999-ADVERSARIAL"
        closeout["record_status"] = "PUBLISHED"
        closeout["study_reference"] = self._study_reference()
        closeout["completeness_assertion"] = (
            "EXACTLY_ONE_PUBLISHED_FINDING_PER_PLANNED_ANALYSIS"
        )
        closeout["analysis_dispositions"] = []
        for analysis, finding, path in zip(
            self.study["analyses"],
            self.findings,
            self.finding_paths,
        ):
            closeout["analysis_dispositions"].append(
                {
                    "analysis_id": analysis["analysis_id"],
                    "analysis_mode": analysis["analysis_mode"],
                    "finding_id": finding["finding_id"],
                    "finding_record_id": finding["record_id"],
                    "finding_record_version": finding["record_version"],
                    "terminal_disposition": finding["terminal_disposition"],
                    "finding_artifact": self._artifact(
                        f"ARTIFACT-{finding['record_id']}",
                        finding["record_version"],
                        "urn:lcmrp:schema:research-finding-record:0.1.0",
                        path,
                    ),
                }
            )
        closeout["closeout_report_artifact"] = self._artifact(
            "ARTIFACT-ADVERSARIAL-CLOSEOUT-REPORT",
            1,
            "urn:lcmrp:test:foundational-closeout-report",
            self.report_path,
            media_type="text/markdown",
        )
        closeout["closeout_authority"] = "SYNTHETIC-M0-TEST"
        closeout["closed_at"] = "2026-07-21T03:00:00Z"
        return closeout

    @staticmethod
    def _index(registry_type: str, entries: list[dict]):
        return {
            "schema_version": "0.1.0",
            "artifact_type": "foundational_record_index",
            "registry_type": registry_type,
            "entries": entries,
        }

    @staticmethod
    def _record_entry(
        *,
        record_id: str,
        record_version: int,
        artifact_type: str,
        schema_id: str,
        artifact_path: str,
        payload: bytes,
    ):
        return {
            "record_id": record_id,
            "record_version": record_version,
            "artifact_type": artifact_type,
            "schema_id": schema_id,
            "artifact_path": artifact_path,
            "artifact_digest": {
                "algorithm": "SHA-256",
                "value": raw_digest(payload),
                "scope": "RAW_FILE_BYTES",
            },
            "registry_status": "ACTIVE",
            "registered_at": "2026-07-21T04:00:00Z",
        }

    def write_registries(self) -> None:
        write_json(self.root / "registry/foundational-subjects.yaml", self.subject_registry)
        write_json(self.root / "registry/foundational-studies.yaml", self.study_registry)
        write_json(self.root / "registry/research-findings.yaml", self.finding_registry)
        write_json(
            self.root / "registry/foundational-study-closeouts.yaml",
            self.closeout_registry,
        )

    def rewrite_finding(self, index: int) -> None:
        payload = write_json(self.root / self.finding_paths[index], self.findings[index])
        self.finding_entries[index]["artifact_digest"]["value"] = raw_digest(payload)
        if self.closeout is not None:
            disposition = self.closeout["analysis_dispositions"][index]
            disposition["finding_artifact"] = self._artifact(
                f"ARTIFACT-{self.findings[index]['record_id']}",
                self.findings[index]["record_version"],
                "urn:lcmrp:schema:research-finding-record:0.1.0",
                self.finding_paths[index],
            )
            self.rewrite_closeout()
        self.write_registries()

    def rewrite_closeout(self) -> None:
        assert self.closeout is not None
        payload = write_json(self.root / self.closeout_path, self.closeout)
        self.closeout_entries[0]["artifact_digest"]["value"] = raw_digest(payload)
        self.write_registries()

    def errors(self) -> list[str]:
        return validate_local_artifact_references(self.root) + validate_registries(self.root)


class FullLifecycleAdversarialTests(unittest.TestCase):
    def fixture(self, **kwargs):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        return SyntheticFoundationalRepository(Path(temporary.name), **kwargs)

    def test_complete_indexed_lifecycle_is_valid(self) -> None:
        fixture = self.fixture()
        self.assertEqual([], fixture.errors())

    def test_digest_verification_status_is_not_artifact_identity(self) -> None:
        fixture = self.fixture(finding_reference_status="VERIFIED")
        self.assertEqual([], fixture.errors())

    def test_active_finding_must_bind_the_exact_indexed_study_artifact(self) -> None:
        fixture = self.fixture(include_closeout=False)
        substituted = copy.deepcopy(fixture.study)
        substituted["research_question"] = (
            "A substituted manifest with the same IDs must not satisfy the study index binding."
        )
        # Keep the substituted copy outside the canonical record directory so the
        # finding-to-index binding, rather than orphan-record discovery, must reject it.
        alternate_path = "artifacts/substituted-study-v1.json"
        write_json(fixture.root / alternate_path, substituted)
        fixture.findings[0]["study_reference"]["manifest_artifact"] = fixture._artifact(
            "ARTIFACT-ADVERSARIAL-STUDY",
            1,
            "urn:lcmrp:schema:foundational-study-manifest:0.1.0",
            alternate_path,
        )
        fixture.rewrite_finding(0)

        errors = fixture.errors()
        self.assertTrue(
            any("finding study index binding mismatch" in error for error in errors),
            errors,
        )

    def test_published_finding_rejects_an_unavailable_manifest(self) -> None:
        fixture = self.fixture(include_closeout=False)
        fixture.findings[0]["study_reference"]["manifest_artifact"]["locator"] = (
            "artifacts/missing-study-manifest.json"
        )
        fixture.rewrite_finding(0)

        errors = fixture.errors()
        self.assertTrue(
            any(
                "recorded artifact is missing" in error
                or "finding binding cannot resolve" in error
                for error in errors
            ),
            errors,
        )

    def test_published_closeout_requires_analysis_set_equality(self) -> None:
        fixture = self.fixture()
        fixture.closeout["analysis_dispositions"].pop()
        fixture.rewrite_closeout()

        errors = fixture.errors()
        self.assertTrue(any("analysis IDs must exactly equal" in error for error in errors), errors)

    def test_published_closeout_rejects_duplicate_analysis_and_finding_reuse(self) -> None:
        fixture = self.fixture()
        fixture.closeout["analysis_dispositions"].append(
            copy.deepcopy(fixture.closeout["analysis_dispositions"][0])
        )
        fixture.rewrite_closeout()

        errors = fixture.errors()
        self.assertTrue(any("disposition IDs must be unique" in error for error in errors), errors)
        self.assertTrue(any("cannot reuse one finding record" in error for error in errors), errors)

    def test_closeout_finding_must_be_active_in_the_index(self) -> None:
        fixture = self.fixture()
        fixture.finding_entries[0]["registry_status"] = "SUPERSEDED"
        fixture.write_registries()

        errors = fixture.errors()
        self.assertTrue(any("must resolve to an ACTIVE published finding" in error for error in errors), errors)

    def test_closeout_finding_reference_must_match_index_path_and_digest(self) -> None:
        fixture = self.fixture()
        alternate_path = "records/foundational/findings/copied-finding.json"
        (fixture.root / alternate_path).write_bytes(
            (fixture.root / fixture.finding_paths[0]).read_bytes()
        )
        fixture.closeout["analysis_dispositions"][0]["finding_artifact"] = fixture._artifact(
            f"ARTIFACT-{fixture.findings[0]['record_id']}",
            1,
            "urn:lcmrp:schema:research-finding-record:0.1.0",
            alternate_path,
        )
        fixture.rewrite_closeout()

        errors = fixture.errors()
        self.assertTrue(any("finding index binding mismatch for locator" in error for error in errors), errors)

    def test_closeout_report_raw_bytes_are_bound_by_digest(self) -> None:
        fixture = self.fixture()
        (fixture.root / fixture.report_path).write_text(
            "# Mutated after closeout publication\n",
            encoding="utf-8",
        )

        errors = fixture.errors()
        self.assertTrue(
            any("recorded SHA-256 does not match" in error for error in errors),
            errors,
        )

    def test_canonical_foundational_record_cannot_bypass_its_index(self) -> None:
        fixture = self.fixture(include_closeout=False)
        write_json(
            fixture.root / "records/foundational/findings/unindexed.json",
            {"artifact_type": "research_finding_record", "record_status": "PUBLISHED"},
        )

        errors = fixture.errors()
        self.assertTrue(any("canonical record is not indexed" in error for error in errors), errors)

    def test_superseded_subject_version_remains_resolvable(self) -> None:
        fixture = self.fixture(include_closeout=False)
        old = fixture.subject_entry
        old["entry_status"] = "SUPERSEDED"
        version_two_path = "records/foundational/subjects/subject-v2.json"
        write_json(
            fixture.root / version_two_path,
            {"fixture_notice": "Synthetic successor subject.", "subject_version": 2},
        )
        successor = copy.deepcopy(old)
        successor["subject_version"] = 2
        successor["entry_status"] = "ACTIVE"
        successor["supersedes_subject_version"] = 1
        successor["supersedes_definition_digest"] = copy.deepcopy(
            old["definition_artifact"]["digest"]
        )
        successor["definition_artifact"] = fixture._artifact(
            "ARTIFACT-ADVERSARIAL-SUBJECT",
            2,
            "urn:lcmrp:test:foundational-subject",
            version_two_path,
        )
        successor["registered_at"] = "2026-07-21T05:00:00Z"
        fixture.subject_registry["entries"].append(successor)
        fixture.write_registries()

        self.assertEqual([], fixture.errors())

    def test_active_study_rejects_missing_or_divergent_subject_registration(self) -> None:
        fixture = self.fixture(include_closeout=False)
        fixture.subject_registry["entries"] = []
        fixture.write_registries()
        missing_errors = fixture.errors()
        self.assertTrue(any("absent from foundational-subjects" in error for error in missing_errors), missing_errors)

        fixture = self.fixture(include_closeout=False)
        fixture.subject_entry["definition"] = "Divergent registry definition."
        fixture.write_registries()
        divergent_errors = fixture.errors()
        self.assertTrue(any("registered subject mismatch for definition" in error for error in divergent_errors), divergent_errors)

    def test_same_profile_identity_cannot_resolve_to_two_definitions(self) -> None:
        fixture = self.fixture(include_closeout=False)
        alternate_profile_path = "records/foundational/profiles/divergent-profile.json"
        write_json(
            fixture.root / alternate_profile_path,
            {"fixture_notice": "Divergent profile under the same exact identity."},
        )
        other = copy.deepcopy(fixture.study)
        other["study_record_id"] = "LCMRP-FSTUDYREC-9999-ADVERSARIAL-OTHER"
        other["study_id"] = "LCMRP-FSTUDY-9999-ADVERSARIAL-OTHER"
        other["primary_method_profile"]["profile_definition_artifact"] = fixture._artifact(
            "ARTIFACT-ADVERSARIAL-PROFILE",
            1,
            "urn:lcmrp:test:method-profile",
            alternate_profile_path,
        )
        path = "records/foundational/studies/other-study-v1.json"
        payload = write_json(fixture.root / path, other)
        fixture.study_registry["entries"].append(
            fixture._record_entry(
                record_id=other["study_record_id"],
                record_version=1,
                artifact_type="foundational_study_manifest",
                schema_id="urn:lcmrp:schema:foundational-study-manifest:0.1.0",
                artifact_path=path,
                payload=payload,
            )
        )
        fixture.write_registries()

        errors = fixture.errors()
        self.assertTrue(any("divergent definition artifacts" in error for error in errors), errors)

    def test_superseded_frozen_studies_remain_subject_and_profile_auditable(self) -> None:
        fixture = self.fixture(include_closeout=False)
        fixture.study_entry["registry_status"] = "SUPERSEDED"
        for entry in fixture.finding_entries:
            entry["registry_status"] = "SUPERSEDED"
        fixture.subject_entry["definition"] = "Divergent historical subject definition."
        fixture.write_registries()

        subject_errors = fixture.errors()
        self.assertTrue(
            any("registered subject mismatch for definition" in error for error in subject_errors),
            subject_errors,
        )

        fixture = self.fixture(include_closeout=False)
        alternate_profile_path = "records/foundational/profiles/historical-divergence.json"
        write_json(
            fixture.root / alternate_profile_path,
            {"fixture_notice": "Historical profile identity divergence."},
        )
        historical = copy.deepcopy(fixture.study)
        historical["study_record_id"] = "LCMRP-FSTUDYREC-9999-HISTORICAL"
        historical["study_id"] = "LCMRP-FSTUDY-9999-HISTORICAL"
        historical["primary_method_profile"]["profile_definition_artifact"] = fixture._artifact(
            "ARTIFACT-ADVERSARIAL-PROFILE",
            1,
            "urn:lcmrp:test:method-profile",
            alternate_profile_path,
        )
        path = "records/foundational/studies/historical.json"
        payload = write_json(fixture.root / path, historical)
        historical_entry = fixture._record_entry(
            record_id=historical["study_record_id"],
            record_version=1,
            artifact_type="foundational_study_manifest",
            schema_id="urn:lcmrp:schema:foundational-study-manifest:0.1.0",
            artifact_path=path,
            payload=payload,
        )
        historical_entry["registry_status"] = "SUPERSEDED"
        fixture.study_registry["entries"].append(historical_entry)
        fixture.write_registries()

        profile_errors = fixture.errors()
        self.assertTrue(
            any("divergent definition artifacts" in error for error in profile_errors),
            profile_errors,
        )

    def test_superseding_study_must_retain_logical_study_identity(self) -> None:
        fixture = self.fixture(include_closeout=False)
        fixture.study_entry["registry_status"] = "SUPERSEDED"
        for entry in fixture.finding_entries:
            entry["registry_status"] = "SUPERSEDED"

        successor = copy.deepcopy(fixture.study)
        successor["record_version"] = 2
        successor["study_id"] = "LCMRP-FSTUDY-9999-UNRELATED-STUDY"
        successor["amendment"] = {
            "kind": "SUPERSEDING_RECORD",
            "supersedes_record_version": 1,
            "supersedes_artifact_digest": immutable_digest(
                fixture.study_entry["artifact_digest"]["value"]
            ),
            "rationale": "Synthetic identity-drift adversarial case.",
            "changed_fields": ["study_id"],
            "result_accessed_before_amendment": False,
            "post_result_change_disclosure": None,
        }
        successor_path = "records/foundational/studies/study-v2.json"
        payload = write_json(fixture.root / successor_path, successor)
        fixture.study_registry["entries"].append(
            fixture._record_entry(
                record_id=successor["study_record_id"],
                record_version=2,
                artifact_type="foundational_study_manifest",
                schema_id="urn:lcmrp:schema:foundational-study-manifest:0.1.0",
                artifact_path=successor_path,
                payload=payload,
            )
        )
        fixture.write_registries()

        errors = fixture.errors()
        self.assertTrue(
            any("superseding study must retain study_id" in error for error in errors),
            errors,
        )

    def test_superseding_finding_must_retain_logical_finding_identity(self) -> None:
        fixture = self.fixture(include_closeout=False)
        prior = fixture.findings[0]
        prior_entry = fixture.finding_entries[0]
        prior_entry["registry_status"] = "SUPERSEDED"

        successor = copy.deepcopy(prior)
        successor["record_version"] = 2
        successor["finding_id"] = "LCMRP-FIND-9999-UNRELATED-FINDING"
        successor["amendment"] = {
            "kind": "SUPERSEDING_RECORD",
            "supersedes_record_version": 1,
            "supersedes_artifact_digest": immutable_digest(
                prior_entry["artifact_digest"]["value"]
            ),
            "rationale": "Synthetic identity-drift adversarial case.",
            "changed_fields": ["finding_id"],
        }
        successor_path = "records/foundational/findings/finding-1-v2.json"
        payload = write_json(fixture.root / successor_path, successor)
        fixture.finding_registry["entries"].append(
            fixture._record_entry(
                record_id=successor["record_id"],
                record_version=2,
                artifact_type="research_finding_record",
                schema_id="urn:lcmrp:schema:research-finding-record:0.1.0",
                artifact_path=successor_path,
                payload=payload,
            )
        )
        fixture.write_registries()

        errors = fixture.errors()
        self.assertTrue(
            any("superseding finding must retain finding_id" in error for error in errors),
            errors,
        )


class RegistryAndScopeAdversarialTests(unittest.TestCase):
    def subject_entry(self, version: int, *, status: str = "ACTIVE"):
        return {
            "subject_id": "LCMRP-FSUBJ-9999-LINEAGE",
            "subject_version": version,
            "subject_series": "LCMRP-LINEAGE",
            "subject_kind": "MEMORY_TAXONOMY",
            "entry_status": status,
            "definition_artifact": {
                "artifact_version": version,
                "digest": immutable_digest(str(version) * 64),
            },
            "supersedes_subject_version": None if version == 1 else version - 1,
            "supersedes_definition_digest": (
                None if version == 1 else immutable_digest(str(version - 1) * 64)
            ),
        }

    def test_subject_lineage_rejects_wrong_digest_and_identity_drift(self) -> None:
        first = self.subject_entry(1, status="SUPERSEDED")
        second = self.subject_entry(2)
        registry = {
            "registry_type": "foundational_subject_registry",
            "entries": [first, second],
        }
        self.assertEqual([], validate_registry_entry_semantics(registry, "subjects"))

        wrong_digest = copy.deepcopy(registry)
        wrong_digest["entries"][1]["supersedes_definition_digest"]["value"] = "f" * 64
        self.assertTrue(validate_registry_entry_semantics(wrong_digest, "subjects"))

        series_drift = copy.deepcopy(registry)
        series_drift["entries"][1]["subject_series"] = "LCMRP-DIFFERENT-SERIES"
        self.assertTrue(validate_registry_entry_semantics(series_drift, "subjects"))

        kind_drift = copy.deepcopy(registry)
        kind_drift["entries"][1]["subject_kind"] = "FORMAL_MEMORY_MODEL"
        self.assertTrue(validate_registry_entry_semantics(kind_drift, "subjects"))

    def test_subject_lineage_rejects_absent_or_nonlower_predecessor_and_two_active_versions(self) -> None:
        absent = self.subject_entry(2)
        registry = {
            "registry_type": "foundational_subject_registry",
            "entries": [absent],
        }
        self.assertTrue(validate_registry_entry_semantics(registry, "subjects"))

        nonlower = {
            "registry_type": "foundational_subject_registry",
            "entries": [self.subject_entry(1, status="SUPERSEDED"), self.subject_entry(2)],
        }
        nonlower["entries"][1]["supersedes_subject_version"] = 2
        self.assertTrue(validate_registry_entry_semantics(nonlower, "subjects"))

        two_active = {
            "registry_type": "foundational_subject_registry",
            "entries": [self.subject_entry(1), self.subject_entry(2)],
        }
        self.assertTrue(validate_registry_entry_semantics(two_active, "subjects"))

    def test_foundational_index_rejects_dot_segment_family_escape(self) -> None:
        schema = load_json("schemas/foundational-record-index.schema.json")
        index = load_json("examples/foundational-record-index.example.json")
        index["registry_type"] = "foundational_study_registry"
        index["entries"] = [
            {
                "record_id": "LCMRP-FSTUDYREC-9999-PATH",
                "record_version": 1,
                "artifact_type": "foundational_study_manifest",
                "schema_id": "urn:lcmrp:schema:foundational-study-manifest:0.1.0",
                "artifact_path": "records/foundational/studies/../../../rogue.json",
                "artifact_digest": {
                    "algorithm": "SHA-256",
                    "value": "a" * 64,
                    "scope": "RAW_FILE_BYTES",
                },
                "registry_status": "ACTIVE",
                "registered_at": "2026-07-21T00:00:00Z",
            }
        ]
        errors = list(
            Draft202012Validator(schema, format_checker=FormatChecker()).iter_errors(index)
        )
        self.assertTrue(errors)

    def test_mechanism_record_index_rejects_dot_segment_family_escape(self) -> None:
        schema = load_json("schemas/record-index.schema.json")
        index = {
            "schema_version": "0.1.0",
            "registry_type": "experiment_registry",
            "entries": [
                {
                    "record_id": "LCMRP-EXPREC-9999-PATH",
                    "record_version": 1,
                    "artifact_type": "experiment_manifest",
                    "schema_id": "urn:lcmrp:schema:experiment-manifest:0.1.0",
                    "artifact_path": "records/experiments/../../../rogue.json",
                    "artifact_digest": {
                        "algorithm": "SHA-256",
                        "value": "a" * 64,
                        "scope": "RAW_FILE_BYTES",
                    },
                    "registry_status": "ACTIVE",
                    "registered_at": "2026-07-21T00:00:00Z",
                }
            ],
        }
        errors = list(
            Draft202012Validator(schema, format_checker=FormatChecker()).iter_errors(index)
        )
        self.assertTrue(errors)

    def test_all_canonical_mechanism_record_families_require_index_entries(self) -> None:
        cases = (
            ("experiment_registry", "experiments.yaml", "records/experiments/orphan.json"),
            ("evidence_registry", "evidence.yaml", "records/evidence/orphan.json"),
        )
        for registry_type, registry_name, artifact_path in cases:
            with self.subTest(registry_type=registry_type):
                with tempfile.TemporaryDirectory() as directory:
                    root = Path(directory)
                    write_json(
                        root / "registry" / registry_name,
                        {
                            "schema_version": "0.1.0",
                            "registry_type": registry_type,
                            "entries": [],
                        },
                    )
                    write_json(
                        root / artifact_path,
                        {"fixture_notice": "An unindexed canonical record must be rejected."},
                    )
                    errors = validate_registries(root)
                self.assertTrue(
                    any("canonical record is not indexed" in error for error in errors),
                    errors,
                )

    def test_record_indexes_reject_multiple_active_versions_of_one_record(self) -> None:
        for registry_type in (
            "experiment_registry",
            "evidence_registry",
            "foundational_study_registry",
            "research_finding_registry",
            "foundational_study_closeout_registry",
        ):
            with self.subTest(registry_type=registry_type):
                registry = {
                    "registry_type": registry_type,
                    "entries": [
                        {
                            "record_id": "SAME-RECORD",
                            "record_version": 1,
                            "registry_status": "ACTIVE",
                        },
                        {
                            "record_id": "SAME-RECORD",
                            "record_version": 2,
                            "registry_status": "ACTIVE",
                        },
                    ],
                }
                errors = validate_registry_entry_semantics(registry, "records")
                self.assertTrue(
                    any("more than one ACTIVE version" in error for error in errors),
                    errors,
                )

    def test_unsupported_foundational_method_profiles_remain_rejected(self) -> None:
        schema = load_json("schemas/foundational-study-manifest.schema.json")
        study = load_json("examples/foundational-study-manifest.example.json")
        for unsupported in ("CONTROLLED_EMPIRICAL_EVALUATION", "EVIDENCE_SYNTHESIS"):
            with self.subTest(profile=unsupported):
                mutated = copy.deepcopy(study)
                mutated["primary_method_profile"]["profile_kind"] = unsupported
                errors = list(
                    Draft202012Validator(
                        schema,
                        format_checker=FormatChecker(),
                    ).iter_errors(mutated)
                )
                self.assertTrue(errors)

    def test_human_facing_foundational_templates_expose_completion_obligations(self) -> None:
        protocol = (ROOT / "templates/foundational-study-protocol.md").read_text(
            encoding="utf-8"
        )
        finding = (ROOT / "templates/foundational-finding-report.md").read_text(
            encoding="utf-8"
        )
        closeout = (ROOT / "templates/foundational-study-closeout.md").read_text(
            encoding="utf-8"
        )
        for required in (
            "Layer 1 — Foundational Research",
            "Mechanism under evaluation: `None`",
            "Rejection and stop criteria",
            "Security and privacy considerations",
            "Reproducibility information",
        ):
            self.assertIn(required, protocol)
        for required in (
            "Terminal disposition",
            "Failure analysis",
            "Mechanism maturity effect: `Not applicable`",
        ):
            self.assertIn(required, finding)
        for required in (
            "EXACTLY_ONE_PUBLISHED_FINDING_PER_PLANNED_ANALYSIS",
            "All-analysis disposition ledger",
            "Closeout completeness does not establish",
        ):
            self.assertIn(required, closeout)


if __name__ == "__main__":
    unittest.main()
