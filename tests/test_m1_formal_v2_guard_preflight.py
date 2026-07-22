"""Gates for formal study-record v2 post-merge guard-only preflight.

Engineering control only: not scientific validation of FMO-0.1.
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PKG = (
    ROOT
    / "studies"
    / "foundational"
    / "m1-formal-model-v1"
    / "superseding"
    / "study-record-v2"
)
PREFLIGHT = PKG / "execution" / "preflight-attestation.json"
ANALYZER = PKG / "analyze_fmo_kernel.py"
MANIFEST = (
    ROOT
    / "records"
    / "foundational"
    / "studies"
    / "LCMRP-FSTUDYREC-0002-M1-FORMAL-MODEL-v2.json"
)
REGISTRY = ROOT / "registry" / "foundational-studies.yaml"
V1_PREFLIGHT = (
    ROOT
    / "studies"
    / "foundational"
    / "m1-formal-model-v1"
    / "execution"
    / "preflight-execution-attestation.json"
)

FORMAL_OUTPUTS = [
    "studies/foundational/m1-formal-model-v1/results/analysis-01-bounded-kernel-raw.json",
    "studies/foundational/m1-formal-model-v1/results/analysis-02-entailment.json",
    "studies/foundational/m1-formal-model-v1/results/analysis-03-nonentailment.json",
    "studies/foundational/m1-formal-model-v1/results/analysis-04-invariant-independence.json",
    "studies/foundational/m1-formal-model-v1/results/analysis-05-authority.json",
    "studies/foundational/m1-formal-model-v1/results/analysis-06-deletion.json",
    "studies/foundational/m1-formal-model-v1/results/analysis-07-semantic-validity.json",
]


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


class FormalV2GuardPreflightTests(unittest.TestCase):
    def test_01_preflight_attestation_exists_and_is_fail_closed(self) -> None:
        self.assertTrue(PREFLIGHT.is_file())
        data = json.loads(PREFLIGHT.read_text(encoding="utf-8"))
        self.assertEqual(data["status"], "PREFLIGHT_PASSED_NO_ANALYSIS_EXECUTED")
        self.assertEqual(data["study_record_version"], 2)
        probe = data["governed_preflight_probe"]
        self.assertFalse(probe["main_called"])
        self.assertFalse(probe["run_kernel_called"])
        self.assertFalse(probe["analyzer_execution_performed"])
        self.assertEqual(probe["result_files_created"], 0)
        self.assertEqual(probe["status"], "PASS")
        self.assertIn("verify_manifest_index", probe["entry_points_called"])

    def test_02_frozen_bindings_match_current_bytes(self) -> None:
        data = json.loads(PREFLIGHT.read_text(encoding="utf-8"))
        bindings = data["frozen_bindings"]
        self.assertEqual(bindings["registry_raw_byte_sha256"], sha(REGISTRY))
        self.assertEqual(bindings["canonical_manifest_raw_byte_sha256"], sha(MANIFEST))
        self.assertEqual(bindings["analyzer_raw_byte_sha256"], sha(ANALYZER))
        self.assertEqual(bindings["active_record_version"], 2)

    def test_03_outputs_absent_and_v1_preflight_preserved(self) -> None:
        for relative in FORMAL_OUTPUTS:
            self.assertFalse((ROOT / relative).exists(), relative)
        self.assertTrue(V1_PREFLIGHT.is_file())
        v1 = json.loads(V1_PREFLIGHT.read_text(encoding="utf-8"))
        self.assertEqual(v1.get("status"), "BLOCKED_NOT_RUN")

    def test_04_guard_probe_reproduces_without_analysis(self) -> None:
        spec = importlib.util.spec_from_file_location(
            "lcmrp_formal_v2_guard_preflight_probe", ANALYZER
        )
        self.assertIsNotNone(spec)
        assert spec is not None and spec.loader is not None
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        module.verify_manifest_index(ROOT, MANIFEST)
        manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
        module.enforce_frozen_manifest(ROOT, MANIFEST, manifest)
        module.verify_analyzer_tool_binding(ROOT, manifest)
        for relative in FORMAL_OUTPUTS:
            self.assertFalse((ROOT / relative).exists(), relative)

    def test_05_claim_boundary_forbids_science_and_completion(self) -> None:
        data = json.loads(PREFLIGHT.read_text(encoding="utf-8"))
        text = " ".join(data["claim_boundary"]).lower()
        self.assertIn("not established", text)
        self.assertIn("main", text)
        self.assertNotIn("proves the formal model", text)


if __name__ == "__main__":
    unittest.main()
