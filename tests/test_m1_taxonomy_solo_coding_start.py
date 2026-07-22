"""Gates for solo intake + term-contract ledger (provisional then locked).

Provisional AI drafts are not locked findings. After human accept-all, the
locked workspace ledger and external receipt are the analysis artifact.
Planned-output path materialization remains deferred until a bootstrap-safe
authorization attestation exists.
"""

from __future__ import annotations

import hashlib
import json
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]
INTAKE = ROOT / "studies/foundational/m1-taxonomy-v1/execution/execution-intake-solo.json"
RECEIPT = ROOT / "studies/foundational/m1-taxonomy-v1/execution/execution-intake-solo.receipt.json"
HANDOFF = (
    ROOT
    / "studies/foundational/m1-taxonomy-v1/execution/work/term-contract-ledger.provisional.json"
)
LOCKED = (
    ROOT
    / "studies/foundational/m1-taxonomy-v1/execution/work/term-contract-ledger.locked.json"
)
LOCKED_RECEIPT = (
    ROOT
    / "studies/foundational/m1-taxonomy-v1/execution/term-contract-ledger.receipt.json"
)
FINDING_DRAFT = (
    ROOT
    / "studies/foundational/m1-taxonomy-v1/execution/work/term-contract-finding.draft.json"
)
PLANNED_OUTPUT = (
    ROOT
    / "studies/foundational/m1-taxonomy-v1/superseding/study-record-v3/outputs/term-contract-ledger.json"
)
SOLO_SCHEMA = ROOT / "schemas/foundational-execution-intake-solo.schema.json"
RECEIPT_SCHEMA = ROOT / "schemas/foundational-execution-intake-receipt.schema.json"
FINDING_SCHEMA = ROOT / "schemas/research-finding-record.schema.json"
V3 = ROOT / "records/foundational/studies/LCMRP-FSTUDYREC-0001-M1-TAXONOMY-v3.json"
FINDING_REGISTRY = ROOT / "registry/research-findings.yaml"


class SoloCodingStartTests(unittest.TestCase):
    def test_01_intake_and_receipt_bind(self) -> None:
        self.assertTrue(INTAKE.is_file())
        self.assertTrue(RECEIPT.is_file())
        intake = json.loads(INTAKE.read_text(encoding="utf-8"))
        receipt = json.loads(RECEIPT.read_text(encoding="utf-8"))
        Draft202012Validator(
            json.loads(SOLO_SCHEMA.read_text(encoding="utf-8")),
            format_checker=FormatChecker(),
        ).validate(intake)
        Draft202012Validator(
            json.loads(RECEIPT_SCHEMA.read_text(encoding="utf-8")),
            format_checker=FormatChecker(),
        ).validate(receipt)
        digest = hashlib.sha256(INTAKE.read_bytes()).hexdigest()
        self.assertEqual(receipt["payload_digest"]["value"], digest)
        self.assertEqual(intake["study_record"]["record_version"], 3)
        self.assertEqual(
            intake["study_record"]["manifest_digest"]["value"],
            hashlib.sha256(V3.read_bytes()).hexdigest(),
        )
        self.assertFalse(intake["ai_tooling_disclosure"]["ai_casts_final_codes"])
        self.assertEqual(
            intake["research_lead"]["contributor_kind"], "HUMAN_RESEARCH_CONTRIBUTOR"
        )

    def test_02_locked_term_contract_ledger_after_accept_all(self) -> None:
        self.assertTrue(LOCKED.is_file())
        self.assertTrue(LOCKED_RECEIPT.is_file())
        self.assertFalse(PLANNED_OUTPUT.exists())
        ledger = json.loads(LOCKED.read_text(encoding="utf-8"))
        receipt = json.loads(LOCKED_RECEIPT.read_text(encoding="utf-8"))
        Draft202012Validator(
            json.loads(RECEIPT_SCHEMA.read_text(encoding="utf-8")),
            format_checker=FormatChecker(),
        ).validate(receipt)
        self.assertEqual(ledger["ledger_status"], "LOCKED")
        self.assertTrue(ledger["lock"]["locked"])
        self.assertEqual(len(ledger["cells"]), 165)
        for cell in ledger["cells"]:
            self.assertEqual(cell["status"], "HUMAN_ACCEPTED")
            self.assertTrue(cell["ai_drafted"])
        self.assertEqual(ledger["human_accept_batch"]["mode"], "ACCEPT_ALL")
        self.assertEqual(ledger["code_frequencies"]["SATISFIED"], 149)
        self.assertEqual(ledger["code_frequencies"]["AMBIGUOUS"], 16)
        self.assertFalse(ledger["reliability"]["reliability_thresholds_met"])
        self.assertEqual(
            ledger["reliability"]["inter_rater"], "NOT_ESTIMABLE_SINGLE_CODER"
        )
        digest = hashlib.sha256(LOCKED.read_bytes()).hexdigest()
        self.assertEqual(receipt["payload_digest"]["value"], digest)
        self.assertIsNone(ledger["lock"]["raw_byte_sha256"])

    def test_03_provisional_workspace_is_handoff_only(self) -> None:
        self.assertTrue(HANDOFF.is_file())
        handoff = json.loads(HANDOFF.read_text(encoding="utf-8"))
        self.assertEqual(handoff["handoff_status"], "SUPERSEDED_BY_LOCKED_OUTPUT")
        self.assertEqual(handoff["human_decision"]["mode"], "ACCEPT_ALL")
        self.assertFalse(handoff["lock"]["locked"])
        self.assertEqual(
            handoff["locked_output_locator"],
            "studies/foundational/m1-taxonomy-v1/execution/work/term-contract-ledger.locked.json",
        )

    def test_04_finding_draft_is_inconclusive_and_unregistered(self) -> None:
        self.assertTrue(FINDING_DRAFT.is_file())
        finding = json.loads(FINDING_DRAFT.read_text(encoding="utf-8"))
        Draft202012Validator(
            json.loads(FINDING_SCHEMA.read_text(encoding="utf-8")),
            format_checker=FormatChecker(),
        ).validate(finding)
        self.assertEqual(finding["record_status"], "DRAFT")
        self.assertEqual(finding["terminal_disposition"], "COMPLETED")
        self.assertEqual(finding["result_classification"], "INCONCLUSIVE")
        self.assertEqual(finding["claim_assessment"], "INCONCLUSIVE")
        self.assertEqual(
            finding["analysis_reference"]["analysis_id"],
            "ANALYSIS-M1-TAXONOMY-TERM-CONTRACT",
        )
        self.assertEqual(
            finding["analysis_reference"]["analysis_mode"],
            "EXPLORATORY",
        )
        registry = FINDING_REGISTRY.read_text(encoding="utf-8")
        self.assertIn("entries: []", registry)
        self.assertNotIn(finding["record_id"], registry)


if __name__ == "__main__":
    unittest.main()
