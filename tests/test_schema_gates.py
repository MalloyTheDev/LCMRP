from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker


ROOT = Path(__file__).resolve().parents[1]


def load_json(relative: str):
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))


def errors_for(schema_name: str, instance):
    schema = load_json(f"schemas/{schema_name}.schema.json")
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    return list(validator.iter_errors(instance))


class EvidenceDecisionGateTests(unittest.TestCase):
    GATE_IDS = {
        "HYPOTHESIS": "HYPOTHESIS_GATE",
        "PROTOTYPE": "PROTOTYPE_GATE",
        "REPLICATED": "REPLICATED_GATE",
        "BENCHMARKED": "BENCHMARKED_GATE",
        "ROBUSTNESS_TESTED": "ROBUSTNESS_TESTED_GATE",
        "SECURITY_REVIEWED": "SECURITY_REVIEWED_GATE",
        "INDEPENDENTLY_VALIDATED": "INDEPENDENTLY_VALIDATED_GATE",
        "INTEGRATION_CANDIDATE": "INTEGRATION_CANDIDATE_GATE",
        "PRODUCTION_READY": "PRODUCTION_READY_GATE",
    }

    def setUp(self) -> None:
        self.example = load_json("examples/evidence-record.example.json")

    def artifact(self, record):
        return copy.deepcopy(record["experiment_manifest"])

    def finalize(self, status: str, state: str = "BENCHMARKED"):
        record = copy.deepcopy(self.example)
        record["record_status"] = "PUBLISHED"
        decision = record["evidence_decision"]
        decision["state_under_decision"] = state
        decision["decision_status"] = status
        decision["decision_action"] = "AWARD" if status == "ACCEPTED" else "DENY"
        decision["decision_authority"] = "SYNTHETIC-TEST-AUTHORITY"
        decision["rationale"] = "Synthetic validator test decision."
        decision["effect_summary"] = "Synthetic schema-test effect only; this is not research evidence."
        decision["decision_artifacts"] = [self.artifact(record)]
        decision["decided_at"] = "2026-07-20T01:00:00Z"
        decision["reviewers"] = [
            {
                "reviewer_id": "SYNTHETIC-REVIEWER-1",
                "display_name_or_pseudonym": "Synthetic Reviewer",
                "relationship_to_originators": "SAME_RESEARCH_TEAM",
                "conflict_of_interest": {
                    "status": "NONE_DECLARED",
                    "details": None,
                },
            }
        ]
        decision["gate_assessments"] = [
            {
                "gate_id": self.GATE_IDS[state],
                "outcome": "SATISFIED" if status == "ACCEPTED" else "NOT_SATISFIED",
                "rationale": "Synthetic gate assessment used only to test schema enforcement.",
                "evidence_artifacts": [self.artifact(record)],
            }
        ]
        if status == "ACCEPTED":
            decision["resulting_evidence_profile"] = [
                {
                    "state": state,
                    "claim_id": record["claim"]["claim_id"],
                    "claim_scope": decision["claim_scope"],
                    "qualification": None,
                    "decision_record": self.artifact(record),
                }
            ]
        else:
            decision["resulting_evidence_profile"] = copy.deepcopy(
                decision["existing_awarded_evidence_profile"]
            )
        return record

    def completed_run(self, record):
        artifact = self.artifact(record)
        return {
            "run_id": "RUN-SYNTHETIC-COMPLETE",
            "run_kind": "ORIGINAL",
            "status": "COMPLETED",
            "protocol_artifact": copy.deepcopy(artifact),
            "control_condition_ids": ["BASELINE-STORE-ALL"],
            "randomness": {
                "applicability": "DETERMINISTIC",
                "seed_policy": "No stochastic operations in this synthetic test fixture.",
                "seeds": [],
                "determinism_notes": "Deterministic synthetic schema fixture.",
            },
            "model_provenance": {
                "applicability": "NOT_APPLICABLE",
                "rationale": "The synthetic schema fixture uses no model.",
                "models": [],
            },
            "environment_provenance": {
                "capture_status": "RECORDED",
                "operating_system": "synthetic-os",
                "hardware": ["synthetic-cpu"],
                "software": [{"name": "synthetic-runtime", "version": "1"}],
                "environment_artifact": copy.deepcopy(artifact),
            },
            "configuration_artifacts": [copy.deepcopy(artifact)],
            "output_artifacts": [copy.deepcopy(artifact)],
            "started_at": "2026-07-20T01:00:00Z",
            "finished_at": "2026-07-20T01:01:00Z",
            "notes": "Synthetic completed run used only for schema tests.",
        }

    def complete_benchmark(self, record):
        artifact = self.artifact(record)
        record["claim"]["assessment_status"] = "SUPPORTED"
        record["result_classification"] = "POSITIVE"
        record["assessment"] = "SUPPORTS_CLAIM"
        record["runs"] = [self.completed_run(record)]
        comparison = record["baseline_comparisons"][0]
        comparison.update(
            {
                "status": "EVALUATED",
                "candidate_value": 0.1,
                "baseline_value": 0.2,
                "uncertainty": "Synthetic interval; not an empirical result.",
                "interpretation": "Synthetic values used only to exercise schema gates.",
            }
        )
        coverage = record["dataset_or_scenario_coverage"][0]
        coverage.update(
            {
                "status": "COMPLETE",
                "cases_planned": 1,
                "cases_evaluated": 1,
                "source_artifact": copy.deepcopy(artifact),
            }
        )
        for index, outcome in enumerate(record["metric_outcomes"], start=1):
            outcome.update(
                {
                    "status": "MEASURED",
                    "value": index / 10,
                    "sample_count": 1,
                    "uncertainty": "Synthetic interval.",
                    "justification": "Synthetic measurement used only for schema testing.",
                    "evidence_artifact": copy.deepcopy(artifact),
                }
            )
        for name, measurement in record["resource_measurements"].items():
            if name == "token_cost":
                measurement.update(
                    {
                        "status": "NOT_APPLICABLE",
                        "value": None,
                        "method": "No tokenized model is used by the synthetic fixture.",
                    }
                )
            else:
                measurement.update(
                    {
                        "status": "MEASURED",
                        "value": 1,
                        "method": "Synthetic measured value used only for schema testing.",
                    }
                )
        record["failure_analysis"].update(
            {
                "status": "COMPLETE",
                "analysis": "Synthetic failure analysis completed for schema testing.",
                "retention_decision": "Retain this synthetic fixture only as test data.",
            }
        )
        return record

    def set_independent_reviewer(self, record):
        record["evidence_decision"]["reviewers"][0].update(
            {
                "relationship_to_originators": "EXTERNAL_INDEPENDENT",
                "conflict_of_interest": {
                    "status": "NONE_DECLARED",
                    "details": None,
                },
            }
        )

    def complete_independent_validation(
        self,
        record,
        relationship: str = "EXTERNAL_INDEPENDENT",
        mode: str = "REPLICATION",
    ):
        artifact = self.artifact(record)
        record["independent_validation"] = {
            "status": "COMPLETED",
            "evaluators": [
                {
                    "evaluator_id": "SYNTHETIC-EVALUATOR-1",
                    "display_name_or_pseudonym": "Synthetic Evaluator",
                    "relationship_to_originators": relationship,
                    "conflict_of_interest": {
                        "status": "NONE_DECLARED",
                        "details": None,
                    },
                }
            ],
            "validation_mode": mode,
            "materials": [copy.deepcopy(artifact)],
            "deviations": [],
            "claim_outcomes": [
                {
                    "claim_id": record["claim"]["claim_id"],
                    "outcome": "CONFIRMED",
                    "rationale": "Synthetic claim outcome used only for schema testing.",
                    "evidence_artifacts": [copy.deepcopy(artifact)],
                }
            ],
            "artifacts": [copy.deepcopy(artifact)],
            "summary": "Synthetic independent-validation fixture; not research evidence.",
        }

    def complete_security_review(self, record):
        review = record["security_and_privacy_review"]
        review.update(
            {
                "status": "COMPLETE",
                "findings": ["Synthetic finding used only for schema testing."],
                "controls_evaluated": ["Synthetic control evaluation."],
                "deletion_verification": "VERIFIED",
                "cross_user_isolation": "VERIFIED",
                "review_artifacts": [self.artifact(record)],
            }
        )

    def enable_layer_three(self, record):
        record["research_layer"] = "LAYER_3_FUTURE_CORPUSSTUDIO_INTEGRATION"
        record["future_corpusstudio_integration_implications"] = {
            "section_title": "Future CorpusStudio Integration Implications",
            "status_label": "RESEARCH-TO-PRODUCT HYPOTHESIS",
            "disclaimer": "Content in this section is provisional and does not constitute an architectural decision, implementation commitment, roadmap recommendation, or claim of production readiness.",
            "implications": [
                {
                    "implication": "Synthetic implication used only for schema testing.",
                    "independent_validation_required": [
                        "Independent product-specific validation remains required."
                    ],
                }
            ],
        }

    def fill_prerequisites(self, record, names):
        for name in names:
            record["prerequisite_evidence"][name] = [self.artifact(record)]

    def assert_error_prefix(self, errors, prefix) -> None:
        paths = [tuple(error.absolute_path) for error in errors]
        self.assertTrue(
            any(path[: len(prefix)] == prefix for path in paths),
            f"expected an error beneath {prefix!r}; observed {paths!r}",
        )

    def test_pending_example_awards_nothing_and_validates(self) -> None:
        self.assertEqual([], errors_for("evidence-record", self.example))
        self.assertEqual("PENDING", self.example["evidence_decision"]["decision_status"])
        self.assertIsNone(self.example["evidence_decision"]["decision_action"])
        self.assertEqual(
            [],
            self.example["evidence_decision"]["existing_awarded_evidence_profile"],
        )
        self.assertEqual([], self.example["evidence_decision"]["resulting_evidence_profile"])

    def test_rejected_benchmark_decision_can_preserve_missing_obligations(self) -> None:
        rejected = self.finalize("REJECTED")
        self.assertEqual([], errors_for("evidence-record", rejected))

    def test_accepted_benchmark_requires_runs_and_evaluated_baseline(self) -> None:
        accepted = self.finalize("ACCEPTED")
        errors = errors_for("evidence-record", accepted)
        for prefix in (
            ("runs",),
            ("baseline_comparisons",),
            ("dataset_or_scenario_coverage",),
            ("metric_outcomes",),
            ("resource_measurements",),
            ("failure_analysis",),
        ):
            self.assert_error_prefix(errors, prefix)

    def test_complete_benchmark_fixture_can_satisfy_gate(self) -> None:
        accepted = self.complete_benchmark(self.finalize("ACCEPTED"))
        self.assertEqual([], errors_for("evidence-record", accepted))

    def test_completed_run_claim_fails_without_timestamps_outputs_and_environment(self) -> None:
        accepted = self.complete_benchmark(self.finalize("ACCEPTED"))
        run = accepted["runs"][0]
        run.pop("finished_at")
        run["output_artifacts"] = []
        run["environment_provenance"]["capture_status"] = "PLANNED"
        errors = errors_for("evidence-record", accepted)
        self.assert_error_prefix(errors, ("runs", 0))

    def test_planned_robustness_cases_cannot_satisfy_completed_gate(self) -> None:
        accepted = self.finalize("ACCEPTED", "ROBUSTNESS_TESTED")
        accepted["robustness_assessment"]["status"] = "COMPLETE"
        planned = {
            "case_id": "CASE-SYNTHETIC-PLANNED",
            "status": "PLANNED",
            "outcome": "Planned only; no outcome exists.",
            "artifact": copy.deepcopy(accepted["artifacts"][0]),
        }
        accepted["robustness_assessment"]["boundary_cases"] = [copy.deepcopy(planned)]
        accepted["robustness_assessment"]["adversarial_cases"] = [copy.deepcopy(planned)]
        accepted["robustness_assessment"]["distribution_shifts"] = [copy.deepcopy(planned)]
        errors = errors_for("evidence-record", accepted)
        for name in ("boundary_cases", "adversarial_cases", "distribution_shifts"):
            self.assert_error_prefix(errors, ("robustness_assessment", name))

    def test_originating_author_and_documentation_only_do_not_satisfy_independence(self) -> None:
        accepted = self.finalize("ACCEPTED", "INDEPENDENTLY_VALIDATED")
        self.set_independent_reviewer(accepted)
        self.complete_independent_validation(
            accepted,
            relationship="ORIGINATING_AUTHOR",
            mode="DOCUMENTATION_REVIEW_ONLY",
        )
        self.assert_error_prefix(
            errors_for("evidence-record", accepted),
            ("independent_validation",),
        )

    def test_integration_candidate_requires_cost_and_governance_evidence(self) -> None:
        accepted = self.finalize("ACCEPTED", "INTEGRATION_CANDIDATE")
        self.set_independent_reviewer(accepted)
        self.complete_independent_validation(accepted)
        self.complete_security_review(accepted)
        self.enable_layer_three(accepted)
        self.fill_prerequisites(
            accepted,
            (
                "benchmark_evidence",
                "robustness_evidence",
                "security_review_evidence",
                "independent_validation_evidence",
            ),
        )
        errors = errors_for("evidence-record", accepted)
        self.assert_error_prefix(errors, ("prerequisite_evidence", "operational_cost_evidence"))
        self.assert_error_prefix(errors, ("prerequisite_evidence", "governance_approval_evidence"))

    def test_production_ready_requires_operational_safety_evidence(self) -> None:
        accepted = self.finalize("ACCEPTED", "PRODUCTION_READY")
        self.set_independent_reviewer(accepted)
        self.complete_independent_validation(accepted)
        self.complete_security_review(accepted)
        self.enable_layer_three(accepted)
        self.fill_prerequisites(
            accepted,
            (
                "benchmark_evidence",
                "robustness_evidence",
                "security_review_evidence",
                "independent_validation_evidence",
                "product_validation_evidence",
                "operational_cost_evidence",
                "operational_testing_evidence",
                "governance_approval_evidence",
            ),
        )
        errors = errors_for("evidence-record", accepted)
        for name in (
            "monitoring_evidence",
            "rollback_evidence",
            "incident_response_evidence",
            "deletion_evidence",
        ):
            self.assert_error_prefix(errors, ("prerequisite_evidence", name))

    def test_final_decision_requires_reviewer_identity_and_effect(self) -> None:
        rejected = self.finalize("REJECTED")
        rejected["evidence_decision"]["reviewers"] = []
        rejected["evidence_decision"]["decision_action"] = None
        self.assert_error_prefix(
            errors_for("evidence-record", rejected),
            ("evidence_decision",),
        )

    def test_award_requires_matching_satisfied_gate_assessment(self) -> None:
        accepted = self.complete_benchmark(self.finalize("ACCEPTED"))
        accepted["evidence_decision"]["gate_assessments"][0]["gate_id"] = (
            "PROTOTYPE_GATE"
        )
        self.assert_error_prefix(
            errors_for("evidence-record", accepted),
            ("evidence_decision", "gate_assessments"),
        )

    def test_superseding_record_requires_recorded_non_null_digest(self) -> None:
        for digest in (
            None,
            {"algorithm": "sha256", "status": "PENDING", "value": None},
        ):
            with self.subTest(digest=digest):
                record = copy.deepcopy(self.example)
                record["record_version"] = 2
                record["amendment"] = {
                    "kind": "SUPERSEDING_RECORD",
                    "supersedes_record_version": 1,
                    "supersedes_artifact_digest": digest,
                    "rationale": "Synthetic supersession test.",
                    "changed_fields": ["evidence_decision"],
                }
                self.assert_error_prefix(
                    errors_for("evidence-record", record),
                    ("amendment", "supersedes_artifact_digest"),
                )


class LayerBoundaryGateTests(unittest.TestCase):
    def test_layer_one_manifest_cannot_target_integration_candidate(self) -> None:
        manifest = load_json("examples/experiment-manifest.example.json")
        manifest["target_evidence_state"]["state_under_investigation"] = (
            "INTEGRATION_CANDIDATE"
        )
        self.assertTrue(errors_for("experiment-manifest", manifest))

    def test_layer_three_manifest_requires_isolated_implications(self) -> None:
        manifest = load_json("examples/experiment-manifest.example.json")
        manifest["research_layer"] = "LAYER_3_FUTURE_CORPUSSTUDIO_INTEGRATION"
        manifest.pop("future_corpusstudio_integration_implications", None)
        self.assertTrue(errors_for("experiment-manifest", manifest))

    def test_layer_one_mechanism_cannot_investigate_integration_readiness(self) -> None:
        registry = load_json("examples/mechanism-registry.example.json")
        registry["entries"][0]["states_under_investigation"].append(
            "INTEGRATION_CANDIDATE"
        )
        self.assertTrue(errors_for("mechanism-registry", registry))


if __name__ == "__main__":
    unittest.main()
