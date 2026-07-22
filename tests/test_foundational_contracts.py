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


def errors_for(schema_name: str, instance):
    schema = load_json(f"schemas/{schema_name}.schema.json")
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    return list(validator.iter_errors(instance))


def make_digest(status: str = "RECORDED", value: str | None = None):
    if value is None and status in {"RECORDED", "VERIFIED"}:
        value = "a" * 64
    return {
        "algorithm": "SHA-256",
        "status": status,
        "value": value,
        "scope": "RAW_FILE_BYTES",
    }


class FoundationalStudyContractTests(unittest.TestCase):
    def setUp(self) -> None:
        self.study = load_json("examples/foundational-study-manifest.example.json")

    def assert_invalid(self, instance, message: str = "") -> None:
        errors = errors_for("foundational-study-manifest", instance)
        self.assertTrue(errors, message or "expected foundational study to be invalid")

    def make_immutable(self, artifact, fill: str = "a") -> None:
        artifact["digest"] = make_digest("RECORDED", fill * 64)

    def freeze(self, study):
        frozen = copy.deepcopy(study)
        frozen["record_status"] = "FROZEN"
        frozen["preregistration"] = {
            "status": "FROZEN",
            "results_accessed_before_freeze": False,
            "frozen_at": "2026-07-21T01:00:00Z",
            "registration_authority": "SYNTHETIC-TEST-AUTHORITY",
            "freeze_artifact": copy.deepcopy(frozen["protocol_artifact"]),
        }
        for fill, artifact in (
            ("b", frozen["preregistration"]["freeze_artifact"]),
            ("c", frozen["subject"]["definition_artifact"]),
            ("d", frozen["primary_method_profile"]["profile_definition_artifact"]),
            ("e", frozen["primary_method_profile"]["category_definition_artifact"]),
            ("f", frozen["reproducibility"]["environment_artifact"]),
            ("e", frozen["protocol_artifact"]),
        ):
            self.make_immutable(artifact, fill)
        for index, source in enumerate(frozen["sources"]):
            self.make_immutable(source["provenance_artifact"], str(index + 1))
        for index, artifact in enumerate(
            frozen["reproducibility"]["configuration_artifacts"]
        ):
            self.make_immutable(artifact, str(index + 7))
        return frozen

    def formal_profile(self):
        taxonomy = self.study["primary_method_profile"]
        formal_system = copy.deepcopy(taxonomy["category_definition_artifact"])
        tool = copy.deepcopy(taxonomy["profile_definition_artifact"])
        self.make_immutable(tool, "f")
        return {
            "profile_kind": "FORMAL_ANALYSIS",
            "profile_id": "LCMRP-MPROF-9999-FORMAL-ANALYSIS",
            "profile_series": "LCMRP-METHOD-PROFILE-FORMAL-ANALYSIS",
            "profile_version": 1,
            "profile_definition_artifact": copy.deepcopy(
                taxonomy["profile_definition_artifact"]
            ),
            "formal_system_artifact": formal_system,
            "assumptions": ["The synthetic axiom set is the complete system under test."],
            "propositions": ["PROPOSITION-SYNTHETIC-CONSISTENCY"],
            "consistency_or_satisfiability_checks": [
                "Check that the complete axiom set has at least one model."
            ],
            "intended_entailments": ["The declared example proposition is entailed."],
            "non_entailments_or_countermodels": [
                "Retain a countermodel for the declared non-entailment."
            ],
            "tool_provenance": tool,
            "proof_or_verification_method": "Synthetic proof replay.",
            "semantic_validity_check": "Evaluate model-level entailment, not syntax alone.",
            "counterexample_search": "Search the bounded synthetic model space.",
        }

    def test_mechanism_free_study_example_is_valid_and_awards_nothing(self) -> None:
        self.assertEqual([], errors_for("foundational-study-manifest", self.study))
        self.assertNotIn("mechanism_versions", self.study)
        self.assertNotIn("evidence_decision", self.study)
        self.assertEqual(
            {
                "applicability": "NOT_APPLICABLE",
                "mechanism_under_evaluation": False,
                "may_award_mechanism_evidence_labels": False,
                "may_change_mechanism_evidence_profile": False,
                "rationale": self.study["mechanism_maturity_boundary"]["rationale"],
            },
            self.study["mechanism_maturity_boundary"],
        )

    def test_existing_mechanism_oriented_examples_remain_valid(self) -> None:
        for schema_name in (
            "experiment-manifest",
            "evidence-record",
            "mechanism-registry",
        ):
            with self.subTest(schema_name=schema_name):
                example = load_json(f"examples/{schema_name}.example.json")
                self.assertEqual([], errors_for(schema_name, example))

    def test_primary_profile_is_required_and_cannot_be_ambiguous(self) -> None:
        missing = copy.deepcopy(self.study)
        missing.pop("primary_method_profile")
        self.assert_invalid(missing)

        unknown = copy.deepcopy(self.study)
        unknown["primary_method_profile"]["profile_kind"] = (
            "STRUCTURAL_AND_FORMAL_ANALYSIS"
        )
        self.assert_invalid(unknown)

        hybrid = copy.deepcopy(self.study)
        hybrid["primary_method_profile"].update(
            {
                "formal_system_artifact": copy.deepcopy(
                    hybrid["primary_method_profile"]["category_definition_artifact"]
                ),
                "assumptions": ["Synthetic assumption"],
            }
        )
        self.assert_invalid(hybrid)

    def test_taxonomy_profile_requires_structural_obligations(self) -> None:
        required = (
            "competency_questions",
            "integrity_constraints",
            "positive_case_source_ids",
            "negative_case_source_ids",
            "adjudication_method",
            "coverage_rule",
        )
        for field in required:
            with self.subTest(field=field):
                mutated = copy.deepcopy(self.study)
                mutated["primary_method_profile"].pop(field)
                self.assert_invalid(mutated)

        for field in (
            "competency_questions",
            "integrity_constraints",
            "positive_case_source_ids",
            "negative_case_source_ids",
        ):
            with self.subTest(empty_field=field):
                mutated = copy.deepcopy(self.study)
                mutated["primary_method_profile"][field] = []
                self.assert_invalid(mutated)

    def test_formal_profile_requires_semantic_not_merely_syntactic_obligations(self) -> None:
        formal = copy.deepcopy(self.study)
        formal["subject"]["subject_kind"] = "FORMAL_MEMORY_MODEL"
        formal["primary_method_profile"] = self.formal_profile()
        self.assertEqual([], errors_for("foundational-study-manifest", formal))

        required = (
            "consistency_or_satisfiability_checks",
            "intended_entailments",
            "non_entailments_or_countermodels",
            "tool_provenance",
            "semantic_validity_check",
            "counterexample_search",
        )
        for field in required:
            with self.subTest(field=field):
                mutated = copy.deepcopy(formal)
                mutated["primary_method_profile"].pop(field)
                self.assert_invalid(mutated)

        pending_tool = copy.deepcopy(formal)
        pending_tool["primary_method_profile"]["tool_provenance"]["digest"] = (
            make_digest("PENDING", None)
        )
        self.assert_invalid(pending_tool)

    def test_frozen_study_requires_exact_subject_profile_protocol_and_freeze_digests(self) -> None:
        frozen = self.freeze(self.study)
        self.assertEqual([], errors_for("foundational-study-manifest", frozen))

        for path in (
            ("subject", "definition_artifact"),
            ("primary_method_profile", "profile_definition_artifact"),
        ):
            with self.subTest(path=path):
                mutated = copy.deepcopy(frozen)
                mutated[path[0]][path[1]]["digest"] = make_digest("PENDING", None)
                self.assert_invalid(mutated)

        for field in ("subject_id", "subject_series", "subject_version"):
            with self.subTest(field=field):
                mutated = copy.deepcopy(frozen)
                mutated["subject"].pop(field)
                self.assert_invalid(mutated)

        for field in ("profile_id", "profile_series", "profile_version"):
            with self.subTest(field=field):
                mutated = copy.deepcopy(frozen)
                mutated["primary_method_profile"].pop(field)
                self.assert_invalid(mutated)

        pending_protocol = copy.deepcopy(frozen)
        pending_protocol["protocol_artifact"]["digest"] = make_digest("PENDING", None)
        self.assert_invalid(pending_protocol)

        pending_freeze = copy.deepcopy(frozen)
        pending_freeze["preregistration"]["freeze_artifact"]["digest"] = make_digest(
            "PENDING", None
        )
        self.assert_invalid(pending_freeze)

        profile_inputs = copy.deepcopy(frozen)
        profile_inputs["primary_method_profile"]["category_definition_artifact"][
            "digest"
        ] = make_digest("PENDING", None)
        self.assert_invalid(profile_inputs)

        source = copy.deepcopy(frozen)
        source["sources"][0]["provenance_artifact"]["digest"] = make_digest(
            "PENDING", None
        )
        self.assert_invalid(source)

        environment = copy.deepcopy(frozen)
        environment["reproducibility"]["environment_artifact"]["digest"] = (
            make_digest("PENDING", None)
        )
        self.assert_invalid(environment)

        configuration = copy.deepcopy(frozen)
        configuration["reproducibility"]["configuration_artifacts"][0][
            "digest"
        ] = make_digest("PENDING", None)
        self.assert_invalid(configuration)

    def test_draft_cannot_claim_frozen_or_preaccessed_preregistration(self) -> None:
        mutated = copy.deepcopy(self.study)
        mutated["preregistration"]["results_accessed_before_freeze"] = True
        self.assert_invalid(mutated)

        mutated = copy.deepcopy(self.study)
        mutated["preregistration"]["status"] = "FROZEN"
        mutated["preregistration"]["frozen_at"] = "2026-07-21T01:00:00Z"
        self.assert_invalid(mutated)

    def test_post_result_supersession_requires_disclosure_and_exploratory_analyses(self) -> None:
        amended = self.freeze(self.study)
        amended["record_version"] = 2
        amended["amendment"] = {
            "kind": "SUPERSEDING_RECORD",
            "supersedes_record_version": 1,
            "supersedes_artifact_digest": make_digest("RECORDED", "1" * 64),
            "rationale": "Synthetic post-result profile change test.",
            "changed_fields": ["primary_method_profile", "analyses"],
            "result_accessed_before_amendment": True,
            "post_result_change_disclosure": (
                "Results were accessed before the change; every amended analysis is exploratory."
            ),
        }
        amended["analyses"][0]["analysis_mode"] = "EXPLORATORY"
        self.assertEqual([], errors_for("foundational-study-manifest", amended))

        undisclosed = copy.deepcopy(amended)
        undisclosed["amendment"]["post_result_change_disclosure"] = None
        self.assert_invalid(undisclosed)

        concealed = copy.deepcopy(amended)
        concealed["analyses"][0]["analysis_mode"] = "CONFIRMATORY"
        self.assert_invalid(concealed)

    def test_per_analysis_modes_allow_transparent_mixed_plans(self) -> None:
        mixed = copy.deepcopy(self.study)
        exploratory = copy.deepcopy(mixed["analyses"][0])
        exploratory["analysis_id"] = "ANALYSIS-EXPLORATORY-BOUNDARY"
        exploratory["analysis_mode"] = "EXPLORATORY"
        mixed["analyses"].append(exploratory)
        self.assertEqual([], errors_for("foundational-study-manifest", mixed))

    def test_human_study_and_other_source_bypasses_are_rejected(self) -> None:
        literal = copy.deepcopy(self.study)
        literal["sources"][0]["source_kind"] = "USER_STUDY"
        self.assert_invalid(literal)

        disguised = copy.deepcopy(self.study)
        disguised["sources"][0]["source_kind"] = "OTHER_NON_HUMAN_SOURCE"
        disguised["sources"][0]["human_subjects_involved"] = True
        self.assert_invalid(disguised)

        for field in ("human_subjects_involved", "human_participant_data_involved"):
            with self.subTest(ethics_field=field):
                mutated = copy.deepcopy(self.study)
                mutated["ethics_scope"][field] = True
                self.assert_invalid(mutated)

    def test_layer_three_and_corpusstudio_smuggling_are_rejected(self) -> None:
        layer_three = copy.deepcopy(self.study)
        layer_three["research_layer"] = "LAYER_3_FUTURE_CORPUSSTUDIO_INTEGRATION"
        self.assert_invalid(layer_three)

        implication = copy.deepcopy(self.study)
        implication["future_corpusstudio_integration_implications"] = {
            "status_label": "RESEARCH-TO-PRODUCT HYPOTHESIS"
        }
        self.assert_invalid(implication)

        product_subject = copy.deepcopy(self.study)
        product_subject["subject"]["target_type"] = "CORPUSSTUDIO_INTEGRATION"
        self.assert_invalid(product_subject)

    def test_mechanism_maturity_applicability_is_not_ambiguous_or_mutable(self) -> None:
        mutations = (
            ("applicability", "APPLICABLE"),
            ("mechanism_under_evaluation", True),
            ("may_award_mechanism_evidence_labels", True),
            ("may_change_mechanism_evidence_profile", True),
        )
        for field, value in mutations:
            with self.subTest(field=field):
                mutated = copy.deepcopy(self.study)
                mutated["mechanism_maturity_boundary"][field] = value
                self.assert_invalid(mutated)


class ResearchFindingContractTests(unittest.TestCase):
    def setUp(self) -> None:
        self.finding = load_json("examples/research-finding-record.example.json")

    def assert_invalid(self, instance, message: str = "") -> None:
        errors = errors_for("research-finding-record", instance)
        self.assertTrue(errors, message or "expected research finding to be invalid")

    def completed(self, result_classification: str, claim_assessment: str):
        finding = copy.deepcopy(self.finding)
        finding["terminal_disposition"] = "COMPLETED"
        finding["result_classification"] = result_classification
        finding["claim_assessment"] = claim_assessment
        finding["raw_output_artifacts"] = [
            copy.deepcopy(finding["study_reference"]["manifest_artifact"])
        ]
        finding["failures"] = []
        finding["finding_statement"] = (
            "Synthetic completed outcome used only to test contract orthogonality."
        )
        return finding

    def test_mechanism_independent_not_run_finding_is_valid(self) -> None:
        self.assertEqual([], errors_for("research-finding-record", self.finding))
        self.assertNotIn("mechanism_versions", self.finding)
        self.assertNotIn("evidence_decision", self.finding)
        self.assertEqual("NOT_RUN", self.finding["terminal_disposition"])
        self.assertEqual([], self.finding["mechanism_maturity_effect"]["awarded_mechanism_evidence_labels"])

    def test_generic_finding_cannot_award_or_imply_mechanism_evidence(self) -> None:
        mutations = (
            ("applicability", "APPLICABLE"),
            ("mechanism_under_evaluation", True),
            ("may_award_mechanism_evidence_labels", True),
            ("may_change_mechanism_evidence_profile", True),
            ("awarded_mechanism_evidence_labels", ["BENCHMARKED"]),
        )
        for field, value in mutations:
            with self.subTest(field=field):
                mutated = copy.deepcopy(self.finding)
                mutated["mechanism_maturity_effect"][field] = value
                self.assert_invalid(mutated)

        decision_smuggling = copy.deepcopy(self.finding)
        decision_smuggling["evidence_decision"] = {
            "decision_action": "AWARD",
            "state": "BENCHMARKED",
        }
        self.assert_invalid(decision_smuggling)

    def test_study_subject_and_profile_bindings_require_exact_versioned_digests(self) -> None:
        references = (
            ("study_reference", "manifest_artifact"),
            ("subject_reference", "definition_artifact"),
            ("primary_method_profile_reference", "profile_artifact"),
        )
        for parent, artifact_field in references:
            with self.subTest(reference=parent):
                mutated = copy.deepcopy(self.finding)
                mutated[parent][artifact_field]["digest"] = make_digest("PENDING", None)
                self.assert_invalid(mutated)

        identity_fields = {
            "study_reference": ("study_id", "study_record_id", "study_record_version"),
            "subject_reference": ("subject_id", "subject_series", "subject_version"),
            "primary_method_profile_reference": (
                "profile_id",
                "profile_series",
                "profile_version",
            ),
        }
        for parent, fields in identity_fields.items():
            for field in fields:
                with self.subTest(reference=parent, field=field):
                    mutated = copy.deepcopy(self.finding)
                    mutated[parent].pop(field)
                    self.assert_invalid(mutated)

    def test_result_class_and_claim_assessment_are_orthogonal(self) -> None:
        combinations = (
            ("NULL", "SUPPORTS_CLAIM"),
            ("NEGATIVE", "SUPPORTS_CLAIM"),
            ("POSITIVE", "DOES_NOT_SUPPORT_CLAIM"),
            ("MIXED", "PARTIALLY_SUPPORTS_CLAIM"),
        )
        for result_class, assessment in combinations:
            with self.subTest(result_class=result_class, assessment=assessment):
                finding = self.completed(result_class, assessment)
                self.assertEqual([], errors_for("research-finding-record", finding))

    def test_all_terminal_dispositions_have_retainable_valid_shapes(self) -> None:
        self.assertEqual([], errors_for("research-finding-record", self.finding))

        halted = copy.deepcopy(self.finding)
        halted["terminal_disposition"] = "HALTED"
        halted["finding_statement"] = "Synthetic halted disposition."
        self.assertEqual([], errors_for("research-finding-record", halted))

        invalid = copy.deepcopy(self.finding)
        invalid["terminal_disposition"] = "INVALID"
        invalid["result_classification"] = "INVALID"
        invalid["finding_statement"] = "Synthetic invalid disposition."
        self.assertEqual([], errors_for("research-finding-record", invalid))

        completed = self.completed("INCONCLUSIVE", "INCONCLUSIVE")
        self.assertEqual([], errors_for("research-finding-record", completed))

    def test_disposition_result_and_output_mismatches_are_rejected(self) -> None:
        not_run_observation = copy.deepcopy(self.finding)
        not_run_observation["result_classification"] = "POSITIVE"
        self.assert_invalid(not_run_observation)

        halted_output = copy.deepcopy(self.finding)
        halted_output["terminal_disposition"] = "HALTED"
        halted_output["raw_output_artifacts"] = [
            copy.deepcopy(halted_output["study_reference"]["manifest_artifact"])
        ]
        self.assert_invalid(halted_output)

        invalid_as_null = copy.deepcopy(self.finding)
        invalid_as_null["terminal_disposition"] = "INVALID"
        invalid_as_null["result_classification"] = "NULL"
        self.assert_invalid(invalid_as_null)

        completed_without_output = self.completed("NULL", "SUPPORTS_CLAIM")
        completed_without_output["raw_output_artifacts"] = []
        self.assert_invalid(completed_without_output)

    def test_completed_output_digest_must_be_immutable(self) -> None:
        completed = self.completed("NULL", "SUPPORTS_CLAIM")
        completed["raw_output_artifacts"][0]["digest"] = make_digest("PENDING", None)
        self.assert_invalid(completed)

    def test_analysis_reference_is_required_and_mode_is_explicit(self) -> None:
        missing = copy.deepcopy(self.finding)
        missing.pop("analysis_reference")
        self.assert_invalid(missing)

        ambiguous = copy.deepcopy(self.finding)
        ambiguous["analysis_reference"]["analysis_mode"] = "MIXED"
        self.assert_invalid(ambiguous)

    def test_layer_three_and_corpusstudio_fields_cannot_enter_finding(self) -> None:
        layer_three = copy.deepcopy(self.finding)
        layer_three["research_layer"] = "LAYER_3_FUTURE_CORPUSSTUDIO_INTEGRATION"
        self.assert_invalid(layer_three)

        implication = copy.deepcopy(self.finding)
        implication["future_corpusstudio_integration_implications"] = {
            "status_label": "RESEARCH-TO-PRODUCT HYPOTHESIS"
        }
        self.assert_invalid(implication)

        product_subject = copy.deepcopy(self.finding)
        product_subject["subject_reference"]["target_type"] = "CORPUSSTUDIO_INTEGRATION"
        self.assert_invalid(product_subject)

    def test_superseding_finding_requires_prior_raw_digest_and_change_record(self) -> None:
        superseding = copy.deepcopy(self.finding)
        superseding["record_version"] = 2
        superseding["amendment"] = {
            "kind": "SUPERSEDING_RECORD",
            "supersedes_record_version": 1,
            "supersedes_artifact_digest": make_digest("RECORDED", "2" * 64),
            "rationale": "Synthetic correction fixture.",
            "changed_fields": ["terminal_disposition"],
        }
        self.assertEqual([], errors_for("research-finding-record", superseding))

        pending = copy.deepcopy(superseding)
        pending["amendment"]["supersedes_artifact_digest"] = make_digest(
            "PENDING", None
        )
        self.assert_invalid(pending)


class FoundationalIndexContractTests(unittest.TestCase):
    def setUp(self) -> None:
        self.index = load_json("examples/foundational-record-index.example.json")

    def entry(self, registry_type: str):
        if registry_type == "foundational_study_registry":
            return {
                "record_id": "LCMRP-FSTUDYREC-9999-SYNTHETIC-INDEX",
                "record_version": 1,
                "artifact_type": "foundational_study_manifest",
                "schema_id": "urn:lcmrp:schema:foundational-study-manifest:0.1.0",
                "artifact_path": "records/foundational/studies/synthetic-index.json",
                "artifact_digest": {
                    "algorithm": "SHA-256",
                    "value": "a" * 64,
                    "scope": "RAW_FILE_BYTES",
                },
                "registry_status": "ACTIVE",
                "registered_at": "2026-07-21T00:00:00Z",
            }
        return {
            "record_id": "LCMRP-FINDREC-9999-SYNTHETIC-INDEX",
            "record_version": 1,
            "artifact_type": "research_finding_record",
            "schema_id": "urn:lcmrp:schema:research-finding-record:0.1.0",
            "artifact_path": "records/foundational/findings/synthetic-index.json",
            "artifact_digest": {
                "algorithm": "SHA-256",
                "value": "b" * 64,
                "scope": "RAW_FILE_BYTES",
            },
            "registry_status": "ACTIVE",
            "registered_at": "2026-07-21T00:00:00Z",
        }

    def test_empty_and_nonempty_indexes_validate_for_both_record_families(self) -> None:
        for registry_type in (
            "foundational_study_registry",
            "research_finding_registry",
        ):
            with self.subTest(registry_type=registry_type, empty=True):
                index = copy.deepcopy(self.index)
                index["registry_type"] = registry_type
                self.assertEqual([], errors_for("foundational-record-index", index))

            with self.subTest(registry_type=registry_type, empty=False):
                index = copy.deepcopy(self.index)
                index["registry_type"] = registry_type
                index["entries"] = [self.entry(registry_type)]
                self.assertEqual([], errors_for("foundational-record-index", index))

    def test_index_rejects_cross_family_type_schema_and_path_smuggling(self) -> None:
        index = copy.deepcopy(self.index)
        index["registry_type"] = "foundational_study_registry"
        index["entries"] = [self.entry("research_finding_registry")]
        self.assertTrue(errors_for("foundational-record-index", index))

        index = copy.deepcopy(self.index)
        index["registry_type"] = "research_finding_registry"
        index["entries"] = [self.entry("foundational_study_registry")]
        self.assertTrue(errors_for("foundational-record-index", index))

    def test_index_rejects_unversioned_or_digest_free_entries(self) -> None:
        for field in ("record_version", "schema_id", "artifact_digest"):
            with self.subTest(field=field):
                index = copy.deepcopy(self.index)
                index["entries"] = [self.entry("foundational_study_registry")]
                index["entries"][0].pop(field)
                self.assertTrue(errors_for("foundational-record-index", index))

    def test_foundational_indexes_reject_duplicate_record_versions_semantically(self) -> None:
        for registry_type in (
            "foundational_study_registry",
            "research_finding_registry",
        ):
            entry = self.entry(registry_type)
            index = {
                "artifact_type": "foundational_record_index",
                "registry_type": registry_type,
                "entries": [entry, copy.deepcopy(entry)],
            }
            errors = validate_registry_entry_semantics(index, "synthetic-index")
            self.assertTrue(
                any("duplicate record_id/record_version" in error for error in errors),
                errors,
            )


class FoundationalBindingValidatorTests(unittest.TestCase):
    def validation_errors(self, mutate=None):
        study = load_json("examples/foundational-study-manifest.example.json")
        finding = load_json("examples/research-finding-record.example.json")

        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            subject_bytes = (
                ROOT / "examples/fixtures/synthetic-foundational-subject-definition.json"
            ).read_bytes()
            profile_bytes = (
                ROOT / "examples/fixtures/synthetic-structural-taxonomy-profile.json"
            ).read_bytes()
            (root / "subject.json").write_bytes(subject_bytes)
            (root / "profile.json").write_bytes(profile_bytes)
            study["subject"]["definition_artifact"]["locator"] = "subject.json"
            study["subject"]["definition_artifact"]["digest"] = make_digest(
                "RECORDED",
                hashlib.sha256(subject_bytes).hexdigest(),
            )
            study["primary_method_profile"]["profile_definition_artifact"][
                "locator"
            ] = "profile.json"
            study["primary_method_profile"]["profile_definition_artifact"][
                "digest"
            ] = make_digest(
                "RECORDED",
                hashlib.sha256(profile_bytes).hexdigest(),
            )
            study_path = root / "study.json"
            study_bytes = json.dumps(study, indent=2).encode("utf-8") + b"\n"
            study_path.write_bytes(study_bytes)
            digest = hashlib.sha256(study_bytes).hexdigest()
            finding["study_reference"]["manifest_artifact"]["locator"] = "study.json"
            finding["study_reference"]["manifest_artifact"]["digest"] = make_digest(
                "RECORDED",
                digest,
            )
            finding["subject_reference"]["definition_artifact"] = copy.deepcopy(
                study["subject"]["definition_artifact"]
            )
            finding["primary_method_profile_reference"]["profile_artifact"] = (
                copy.deepcopy(
                    study["primary_method_profile"]["profile_definition_artifact"]
                )
            )
            if mutate is not None:
                mutate(finding)
            (root / "finding.json").write_text(
                json.dumps(finding, indent=2) + "\n",
                encoding="utf-8",
            )
            return validate_local_artifact_references(root)

    def test_exact_finding_bindings_resolve_to_referenced_study(self) -> None:
        self.assertEqual([], self.validation_errors())

    def test_mismatched_study_subject_profile_and_analysis_bindings_are_rejected(self) -> None:
        mutations = {
            "study_id": lambda finding: finding["study_reference"].__setitem__(
                "study_id", "LCMRP-FSTUDY-9999-DIFFERENT-STUDY"
            ),
            "study_record_id": lambda finding: finding["study_reference"].__setitem__(
                "study_record_id", "LCMRP-FSTUDYREC-9999-DIFFERENT-STUDY"
            ),
            "study_record_version": lambda finding: finding["study_reference"].__setitem__(
                "study_record_version", 2
            ),
            "study_schema_id": lambda finding: finding["study_reference"][
                "manifest_artifact"
            ].__setitem__("schema_id", "urn:lcmrp:schema:wrong:0.1.0"),
            "subject_kind": lambda finding: finding["subject_reference"].__setitem__(
                "subject_kind", "FORMAL_MEMORY_MODEL"
            ),
            "subject_id": lambda finding: finding["subject_reference"].__setitem__(
                "subject_id", "LCMRP-FSUBJ-9999-DIFFERENT-SUBJECT"
            ),
            "subject_series": lambda finding: finding["subject_reference"].__setitem__(
                "subject_series", "LCMRP-DIFFERENT-SUBJECT-SERIES"
            ),
            "subject_version": lambda finding: finding["subject_reference"].__setitem__(
                "subject_version", 2
            ),
            "profile_kind": lambda finding: finding[
                "primary_method_profile_reference"
            ].__setitem__("profile_kind", "FORMAL_ANALYSIS"),
            "profile_id": lambda finding: finding[
                "primary_method_profile_reference"
            ].__setitem__("profile_id", "LCMRP-MPROF-9999-DIFFERENT-PROFILE"),
            "profile_series": lambda finding: finding[
                "primary_method_profile_reference"
            ].__setitem__("profile_series", "LCMRP-DIFFERENT-PROFILE-SERIES"),
            "profile_version": lambda finding: finding[
                "primary_method_profile_reference"
            ].__setitem__("profile_version", 2),
            "analysis_id": lambda finding: finding["analysis_reference"].__setitem__(
                "analysis_id", "ANALYSIS-NOT-IN-STUDY"
            ),
            "analysis_mode": lambda finding: finding["analysis_reference"].__setitem__(
                "analysis_mode", "EXPLORATORY"
            ),
        }
        for name, mutation in mutations.items():
            with self.subTest(binding=name):
                errors = self.validation_errors(mutation)
                self.assertTrue(
                    any("binding" in error.lower() for error in errors),
                    errors,
                )

    def test_published_or_completed_finding_requires_frozen_study(self) -> None:
        def publish(finding):
            finding["record_status"] = "PUBLISHED"

        def complete(finding):
            finding["terminal_disposition"] = "COMPLETED"
            finding["result_classification"] = "NULL"
            finding["claim_assessment"] = "SUPPORTS_CLAIM"
            finding["raw_output_artifacts"] = [
                copy.deepcopy(finding["study_reference"]["manifest_artifact"])
            ]
            finding["failures"] = []

        for name, mutation in (("published", publish), ("completed", complete)):
            with self.subTest(state=name):
                errors = self.validation_errors(mutation)
                self.assertTrue(
                    any("requires a FROZEN study" in error for error in errors),
                    errors,
                )


class FoundationalStudySemanticValidatorTests(unittest.TestCase):
    def validation_errors(self, mutate):
        study = load_json("examples/foundational-study-manifest.example.json")
        mutate(study)
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "study.json").write_text(
                json.dumps(study, indent=2) + "\n",
                encoding="utf-8",
            )
            return validate_local_artifact_references(root)

    def test_taxonomy_case_ids_must_resolve_to_unique_matching_role_sources(self) -> None:
        mutations = {
            "missing_positive": lambda study: study["primary_method_profile"].__setitem__(
                "positive_case_source_ids", ["SOURCE-DOES-NOT-EXIST"]
            ),
            "wrong_positive_role": lambda study: study[
                "primary_method_profile"
            ].__setitem__(
                "positive_case_source_ids", ["SOURCE-NEGATIVE-SYNTHETIC"]
            ),
            "wrong_negative_role": lambda study: study[
                "primary_method_profile"
            ].__setitem__(
                "negative_case_source_ids", ["SOURCE-POSITIVE-SYNTHETIC"]
            ),
            "duplicate_source_id": lambda study: study["sources"].append(
                copy.deepcopy(study["sources"][0])
            ),
        }
        for name, mutation in mutations.items():
            with self.subTest(mutation=name):
                errors = self.validation_errors(mutation)
                self.assertTrue(
                    any("foundational study" in error for error in errors),
                    errors,
                )

    def test_analysis_ids_must_be_unique_for_unambiguous_finding_binding(self) -> None:
        def duplicate_analysis(study):
            study["analyses"].append(copy.deepcopy(study["analyses"][0]))

        errors = self.validation_errors(duplicate_analysis)
        self.assertTrue(any("analysis IDs must be unique" in error for error in errors), errors)


class FoundationalRegistryStatusValidatorTests(unittest.TestCase):
    def registry_errors(self, registry_type: str):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "schemas").mkdir()
            (root / "registry").mkdir()
            if registry_type == "foundational_study_registry":
                artifact = load_json("examples/foundational-study-manifest.example.json")
                # This status-only fixture is deliberately outside the managed
                # taxonomy case-access lane; profile-shape errors are immaterial
                # to the ACTIVE-versus-DRAFT assertion below.
                artifact["subject"]["subject_kind"] = "FORMAL_MEMORY_MODEL"
                artifact["primary_method_profile"]["profile_kind"] = (
                    "FORMAL_ANALYSIS"
                )
                artifact["primary_method_profile"].pop("positive_case_source_ids")
                artifact["primary_method_profile"].pop("negative_case_source_ids")
                artifact["sources"] = []
                schema_name = "foundational-study-manifest.schema.json"
                record_id = artifact["study_record_id"]
                artifact_type = "foundational_study_manifest"
                artifact_path = "records/foundational/studies/draft.json"
            else:
                artifact = load_json("examples/research-finding-record.example.json")
                schema_name = "research-finding-record.schema.json"
                record_id = artifact["record_id"]
                artifact_type = "research_finding_record"
                artifact_path = "records/foundational/findings/draft.json"

            for name in (
                "foundational-record-index.schema.json",
                schema_name,
            ):
                (root / "schemas" / name).write_text(
                    (ROOT / "schemas" / name).read_text(encoding="utf-8"),
                    encoding="utf-8",
                )

            artifact_file = root / artifact_path
            artifact_file.parent.mkdir(parents=True)
            artifact_bytes = json.dumps(artifact, indent=2).encode("utf-8") + b"\n"
            artifact_file.write_bytes(artifact_bytes)
            registry = {
                "schema_version": "0.1.0",
                "artifact_type": "foundational_record_index",
                "registry_type": registry_type,
                "entries": [
                    {
                        "record_id": record_id,
                        "record_version": artifact["record_version"],
                        "artifact_type": artifact_type,
                        "schema_id": f"urn:lcmrp:schema:{schema_name.removesuffix('.schema.json')}:0.1.0",
                        "artifact_path": artifact_path,
                        "artifact_digest": {
                            "algorithm": "SHA-256",
                            "value": hashlib.sha256(artifact_bytes).hexdigest(),
                            "scope": "RAW_FILE_BYTES",
                        },
                        "registry_status": "ACTIVE",
                        "registered_at": "2026-07-21T00:00:00Z",
                    }
                ],
            }
            registry_name = (
                "foundational-studies.yaml"
                if registry_type == "foundational_study_registry"
                else "research-findings.yaml"
            )
            (root / "registry" / registry_name).write_text(
                json.dumps(registry, indent=2) + "\n",
                encoding="utf-8",
            )
            return validate_registries(root)

    def test_active_indexes_reject_draft_studies_and_findings(self) -> None:
        expectations = {
            "foundational_study_registry": "ACTIVE foundational study must be FROZEN",
            "research_finding_registry": "ACTIVE research finding must be PUBLISHED",
        }
        for registry_type, expected in expectations.items():
            with self.subTest(registry_type=registry_type):
                errors = self.registry_errors(registry_type)
                self.assertTrue(any(expected in error for error in errors), errors)


if __name__ == "__main__":
    unittest.main()
