"""Adversarial gates for the taxonomy pre-result metadata/intake v2 package.

These tests establish package structure, v1 immutability, intake non-self-
reference, result absence, and lane isolation only. They are not scientific
evidence about the candidate taxonomy and do not authorize execution.
"""

from __future__ import annotations

import hashlib
import json
import unittest
from pathlib import Path
from typing import Any, Mapping

from jsonschema import Draft202012Validator, FormatChecker
from jsonschema.exceptions import ValidationError

ROOT = Path(__file__).resolve().parents[1]
PKG = (
    ROOT
    / "studies"
    / "foundational"
    / "m1-taxonomy-v1"
    / "superseding"
    / "pre-result-metadata-intake-v2"
)
TAXONOMY_V1_RECORD = (
    ROOT / "records" / "foundational" / "studies" / "LCMRP-FSTUDYREC-0001-M1-TAXONOMY-v1.json"
)
FORMAL_V1_RECORD = (
    ROOT / "records" / "foundational" / "studies" / "LCMRP-FSTUDYREC-0002-M1-FORMAL-MODEL-v1.json"
)
TAXONOMY_PROTOCOL = ROOT / "studies" / "foundational" / "m1-taxonomy-v1" / "protocol-v1.md"
TAXONOMY_FREEZE = ROOT / "studies" / "foundational" / "m1-taxonomy-v1" / "freeze-attestation.json"
FORMAL_ANALYZER = ROOT / "studies" / "foundational" / "m1-formal-model-v1" / "analyze_fmo_kernel.py"
FORMAL_GUARD_V2 = (
    ROOT
    / "studies"
    / "foundational"
    / "m1-formal-model-v1"
    / "superseding"
    / "pre-result-guard-v2"
    / "analyze_fmo_kernel.py"
)
INTAKE_SCHEMA = ROOT / "schemas" / "foundational-execution-intake.schema.json"
RECEIPT_SCHEMA = ROOT / "schemas" / "foundational-execution-intake-receipt.schema.json"
LIVE_INTAKE = (
    ROOT
    / "studies"
    / "foundational"
    / "m1-taxonomy-v1"
    / "execution"
    / "execution-intake.json"
)

# Digests at package baseline a4d0279 / protected immutability targets.
V1_TAXONOMY_RECORD_DIGEST = "01640e8dae3836874b2b39fe3ea2a8f9c090374508aa69b31adf06fea9272139"
V1_FORMAL_RECORD_DIGEST = "b99da2d9cfa34d659416fe30cc1d3fa731425d1fcfb8b6c9422cd9b5add2707e"
V1_PROTOCOL_DIGEST = "667f01d88287f04418b04ca7e549b8e13a48725f7b30262f21ce47f53e4dcb1c"
V1_FREEZE_DIGEST = "fbfa5b94cc940af1ccf5e38ddf763ef93982463ca0bd8f5fb0325d4bf6e843a9"
V1_FORMAL_ANALYZER_DIGEST = "957573ab5abd2f2b73d4272a4549145d28e99e3ceaa52f2d26d99939a10e5a72"
FORMAL_GUARD_V2_DIGEST = "95356a2ed130cc815899fe0562757041b89b8ae39e1d774cd75ca50f286c50a5"

TAXONOMY_OUTPUTS = [
    "studies/foundational/m1-taxonomy-v1/outputs/term-contract-ledger.json",
    "studies/foundational/m1-taxonomy-v1/outputs/organization-competition-ledger.json",
    "studies/foundational/m1-taxonomy-v1/outputs/distinction-integrity-ledger.json",
    "studies/foundational/m1-taxonomy-v1/outputs/governance-adversarial-ledger.json",
    "studies/foundational/m1-taxonomy-v1/outputs/ambiguity-catalog.json",
]

FORMAL_OUTPUTS = [
    "studies/foundational/m1-formal-model-v1/results/analysis-01-bounded-kernel-raw.json",
    "studies/foundational/m1-formal-model-v1/results/analysis-02-entailment.json",
    "studies/foundational/m1-formal-model-v1/results/analysis-03-nonentailment.json",
    "studies/foundational/m1-formal-model-v1/results/analysis-04-invariant-independence.json",
    "studies/foundational/m1-formal-model-v1/results/analysis-05-authority.json",
    "studies/foundational/m1-formal-model-v1/results/analysis-06-deletion.json",
    "studies/foundational/m1-formal-model-v1/results/analysis-07-semantic-validity.json",
]


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def validator_for(schema_path: Path) -> Draft202012Validator:
    schema = load_json(schema_path)
    Draft202012Validator.check_schema(schema)
    return Draft202012Validator(schema, format_checker=FormatChecker())


class TaxonomyPreResultRepairV2Tests(unittest.TestCase):
    def test_01_package_tree_and_manifest_identity(self) -> None:
        self.assertTrue(PKG.is_dir())
        manifest_path = PKG / "package-manifest.json"
        self.assertTrue(manifest_path.is_file())
        manifest = load_json(manifest_path)
        self.assertEqual(manifest["package_id"], "M1-TAX-PRE-RESULT-METADATA-INTAKE-V2")
        self.assertEqual(manifest["slice_id"], "M1-TAX-PRE-RESULT-METADATA-INTAKE-V2-001")
        self.assertEqual(manifest["package_status"], "PRE_RESULT_REPAIR_PACKAGE_NOT_FROZEN")
        self.assertEqual(
            manifest["supersedes"]["study_record_raw_byte_sha256"],
            V1_TAXONOMY_RECORD_DIGEST,
        )
        for blocker in ("B2", "B3", "B4", "B5", "B6"):
            self.assertIn(blocker, manifest["supersedes"]["blocker_ids"])
        self.assertEqual(manifest["supersedes"]["residual_blocker_ids"], ["B1"])
        boundary = manifest["execution_boundary"]
        self.assertTrue(boundary["pre_result_only"])
        self.assertFalse(boundary["frozen"])
        self.assertFalse(boundary["registered"])
        self.assertFalse(boundary["live_intake_created"])
        self.assertFalse(boundary["adjudicators_appointed"])
        self.assertFalse(boundary["case_contents_accessed"])
        self.assertEqual(boundary["planned_outputs_created"], 0)
        self.assertFalse(boundary["execution_authorized"])

    def test_02_package_artifact_digests_match_raw_bytes(self) -> None:
        manifest = load_json(PKG / "package-manifest.json")
        for entry in manifest["artifacts"]:
            path = ROOT / entry["locator"]
            self.assertTrue(path.is_file(), entry["locator"])
            self.assertEqual(sha256_file(path), entry["raw_byte_sha256"], entry["locator"])
        for entry in manifest["shared_contract_artifacts"]:
            path = ROOT / entry["locator"]
            self.assertTrue(path.is_file(), entry["locator"])
            self.assertEqual(sha256_file(path), entry["raw_byte_sha256"], entry["locator"])

    def test_03_protected_v1_and_formal_lane_digests_unchanged(self) -> None:
        self.assertEqual(sha256_file(TAXONOMY_V1_RECORD), V1_TAXONOMY_RECORD_DIGEST)
        self.assertEqual(sha256_file(FORMAL_V1_RECORD), V1_FORMAL_RECORD_DIGEST)
        self.assertEqual(sha256_file(TAXONOMY_PROTOCOL), V1_PROTOCOL_DIGEST)
        self.assertEqual(sha256_file(TAXONOMY_FREEZE), V1_FREEZE_DIGEST)
        self.assertEqual(sha256_file(FORMAL_ANALYZER), V1_FORMAL_ANALYZER_DIGEST)
        self.assertEqual(sha256_file(FORMAL_GUARD_V2), FORMAL_GUARD_V2_DIGEST)

    def test_04_planned_outputs_and_multi_human_live_intake_absent(self) -> None:
        """Pre-result v2 package did not open multi-human execution.

        After taxonomy study-record v3 (solo+AI), ``execution/`` may hold solo
        intake and provisional work. Multi-human ``execution-intake.json`` and
        locked planned outputs under ``outputs/`` must still be absent.
        """
        for relative in TAXONOMY_OUTPUTS + FORMAL_OUTPUTS:
            self.assertFalse((ROOT / relative).exists(), relative)
        self.assertFalse(LIVE_INTAKE.exists())
        execution_dir = ROOT / "studies/foundational/m1-taxonomy-v1/execution"
        if execution_dir.is_dir():
            self.assertFalse((execution_dir / "execution-intake.json").exists())
            # Locked planned-output names must not appear under outputs/.
            outputs_dir = ROOT / "studies/foundational/m1-taxonomy-v1/outputs"
            self.assertFalse(outputs_dir.exists())

    def test_05_source_reconciliation_covers_b2_b3(self) -> None:
        recon = load_json(PKG / "source-binding-reconciliation.json")
        self.assertEqual(set(recon["blocker_ids"]), {"B2", "B3"})
        proposed = set(recon["proposed_version_2_source_set"]["source_ids"])
        self.assertIn("SOURCE-M1-FOUNDATIONAL-CONTRACT", proposed)
        self.assertIn("SOURCE-M1-MILESTONE", proposed)
        self.assertEqual(len(proposed), 7)
        policy = recon["milestone_binding_policy"]
        self.assertEqual(
            policy["selected_version_2_policy"],
            "TRANSPARENT_REBIND_CURRENT_WITH_DISCLOSURE",
        )
        self.assertTrue(policy["proposed_version_2_binding"]["must_recompute_at_freeze"])
        self.assertTrue(
            policy["proposed_version_2_binding"]["disclosure_required_in_superseding_amendment"]
        )
        self.assertIn("case contents were not accessed", " ".join(recon["claim_boundary"]).lower())

    def test_06_environment_obligations_cover_b4_b5(self) -> None:
        env = load_json(PKG / "environment-freeze-obligations.json")
        self.assertEqual(set(env["blocker_ids"]), {"B4", "B5"})
        fields = {
            item["field"]
            for item in env["b4_environment_freeze_location_requirements"][
                "required_version_2_fields_in_manifest_or_attestation"
            ]
        }
        self.assertIn("dependency_lockfile", fields)
        self.assertIn("platform_details", fields)
        self.assertIn("repository_revision", fields)
        lifecycle = env["b5_attestation_inventory_and_lifecycle"]["lifecycle_label_resolution"]
        self.assertIn("forbidden", lifecycle)
        self.assertIn("Editing version-1", lifecycle["forbidden"])

    def test_07_intake_schemas_valid_and_examples_conform(self) -> None:
        intake_v = validator_for(INTAKE_SCHEMA)
        receipt_v = validator_for(RECEIPT_SCHEMA)
        intake_example = load_json(
            ROOT / "examples" / "foundational-execution-intake.example.json"
        )
        receipt_example = load_json(
            ROOT / "examples" / "foundational-execution-intake-receipt.example.json"
        )
        intake_v.validate(intake_example)
        receipt_v.validate(receipt_example)
        self.assertEqual(
            intake_example["digest_binding"]["mode"], "EXTERNAL_DIGEST_RECEIPT"
        )
        self.assertTrue(
            intake_example["digest_binding"]["forbidden_self_digest_of_entire_payload_file"]
        )
        roles = {row["role"] for row in intake_example["roles"]}
        self.assertEqual(roles, {"PRIMARY_1", "PRIMARY_2", "TIE"})
        for row in intake_example["roles"]:
            self.assertEqual(row["contributor_kind"], "HUMAN_RESEARCH_CONTRIBUTOR")
            self.assertFalse(row["contributor_id"].startswith("AGENT"))
            self.assertFalse(row["contributor_id"].startswith("LCMRP-AGENT"))

    def test_08_rejects_self_digest_field_on_intake_payload(self) -> None:
        intake_v = validator_for(INTAKE_SCHEMA)
        payload = load_json(ROOT / "examples" / "foundational-execution-intake.example.json")
        poisoned = dict(payload)
        poisoned["raw_byte_sha256_of_this_file"] = "0" * 64
        with self.assertRaises(ValidationError):
            intake_v.validate(poisoned)

    def test_09_rejects_agent_contributor_id_pattern(self) -> None:
        intake_v = validator_for(INTAKE_SCHEMA)
        payload = load_json(ROOT / "examples" / "foundational-execution-intake.example.json")
        payload = json.loads(json.dumps(payload))
        payload["roles"][0]["contributor_id"] = "AGENT-ROOT-ORCHESTRATOR"
        with self.assertRaises(ValidationError):
            intake_v.validate(payload)

    def test_10_residual_b1_gate_and_contracts_present(self) -> None:
        residual = (PKG / "residual-human-contributor-gate.md").read_text(encoding="utf-8")
        self.assertIn("B1", residual)
        self.assertIn("remains **open**", residual)
        self.assertIn("language-model", residual.lower())
        contract = (PKG / "intake-binding-contract.md").read_text(encoding="utf-8")
        self.assertIn("External digest receipt", contract)
        self.assertIn("Self-referential", contract)

    def test_11_registries_remain_empty_for_results(self) -> None:
        for relative in (
            "registry/research-findings.yaml",
            "registry/foundational-study-closeouts.yaml",
            "registry/evidence.yaml",
            "registry/experiments.yaml",
            "registry/mechanisms.yaml",
        ):
            text = (ROOT / relative).read_text(encoding="utf-8")
            self.assertIn("entries: []", text)

    def test_12_case_paths_exist_but_package_does_not_require_body_reads(self) -> None:
        cases = ROOT / "studies" / "foundational" / "m1-taxonomy-v1" / "cases"
        for name in ("positive-cases.json", "negative-cases.json", "held-out-cases.json"):
            self.assertTrue((cases / name).is_file())
        # Package JSON must not embed case file bodies or quote long case payloads.
        for path in PKG.glob("*.json"):
            text = path.read_text(encoding="utf-8")
            self.assertNotIn('"cases":', text)
            self.assertNotIn("case_body", text)
            # Locators may mention case source IDs; must not include raw case JSON arrays.
            self.assertNotIn('"case_id"', text)

    def test_13_claim_boundary_forbids_execution_and_completion(self) -> None:
        manifest = load_json(PKG / "package-manifest.json")
        not_made = " ".join(manifest["claims_explicitly_not_made"]).lower()
        self.assertIn("execution", not_made)
        self.assertIn("m1 completion", not_made)
        self.assertIn("b1", not_made)
        readme = (PKG / "README.md").read_text(encoding="utf-8")
        self.assertIn("CLAIMS_EXPLICITLY_NOT_MADE", readme)
        self.assertIn("NOT_EXECUTABLE", readme)


if __name__ == "__main__":
    unittest.main()
