"""Gates for solo intake + provisional term-contract ledger start.

Provisional AI drafts are not locked findings.
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
LEDGER = (
    ROOT
    / "studies/foundational/m1-taxonomy-v1/execution/work/term-contract-ledger.provisional.json"
)
SOLO_SCHEMA = ROOT / "schemas/foundational-execution-intake-solo.schema.json"
RECEIPT_SCHEMA = ROOT / "schemas/foundational-execution-intake-receipt.schema.json"
V3 = ROOT / "records/foundational/studies/LCMRP-FSTUDYREC-0001-M1-TAXONOMY-v3.json"


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

    def test_02_ledger_is_provisional_not_locked(self) -> None:
        self.assertTrue(LEDGER.is_file())
        ledger = json.loads(LEDGER.read_text(encoding="utf-8"))
        self.assertEqual(
            ledger["ledger_status"], "PROVISIONAL_UNLOCKED_AWAITING_HUMAN_ACCEPT"
        )
        self.assertFalse(ledger["lock"]["locked"])
        self.assertEqual(len(ledger["cells"]), 165)
        for cell in ledger["cells"]:
            self.assertEqual(
                cell["status"], "PROVISIONAL_AI_DRAFT_AWAITING_HUMAN_ACCEPT"
            )
            self.assertTrue(cell["ai_drafted"])
        self.assertEqual(
            ledger["reliability"]["inter_rater"], "NOT_ESTIMABLE_SINGLE_CODER"
        )


if __name__ == "__main__":
    unittest.main()
