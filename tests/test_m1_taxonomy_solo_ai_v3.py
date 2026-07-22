"""Gates for taxonomy solo+AI method supersession (study-record v3).

Engineering/method-governance only. Not scientific validation of the taxonomy.
"""

from __future__ import annotations

import hashlib
import json
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]
V3 = ROOT / "records/foundational/studies/LCMRP-FSTUDYREC-0001-M1-TAXONOMY-v3.json"
V2 = ROOT / "records/foundational/studies/LCMRP-FSTUDYREC-0001-M1-TAXONOMY-v2.json"
PROFILE = (
    ROOT
    / "studies/foundational/m1-taxonomy-v1/superseding/study-record-v3/definitions/method-profile.json"
)
REGISTRY = ROOT / "registry/foundational-studies.yaml"
SOLO_SCHEMA = ROOT / "schemas/foundational-execution-intake-solo.schema.json"
SOLO_EXAMPLE = ROOT / "examples/foundational-execution-intake-solo.example.json"
LIVE_INTAKE = (
    ROOT
    / "studies/foundational/m1-taxonomy-v1/execution/execution-intake.json"
)


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


class TaxonomySoloAiV3Tests(unittest.TestCase):
    def test_01_active_registry_is_v3_with_lineage(self) -> None:
        text = REGISTRY.read_text(encoding="utf-8")
        self.assertIn("LCMRP-FSTUDYREC-0001-M1-TAXONOMY-v3.json", text)
        self.assertIn(sha(V3), text)
        data = json.loads(V3.read_text(encoding="utf-8"))
        self.assertEqual(data["record_version"], 3)
        self.assertEqual(data["amendment"]["kind"], "SUPERSEDING_RECORD")
        self.assertEqual(data["amendment"]["supersedes_record_version"], 2)
        self.assertEqual(
            data["amendment"]["supersedes_artifact_digest"]["value"], sha(V2)
        )

    def test_02_profile_is_solo_human_ai_not_final_coder(self) -> None:
        profile = json.loads(PROFILE.read_text(encoding="utf-8"))
        self.assertEqual(profile["profile_version"], 2)
        self.assertEqual(
            profile["research_context"]["mode"], "SOLO_RESEARCHER_WITH_AI_TOOLING"
        )
        roles = profile["evaluator_roles"]
        self.assertEqual(roles["research_lead_adjudicators"], 1)
        self.assertEqual(roles["primary_adjudicators"], 0)
        self.assertEqual(roles["tie_adjudicators"], 0)
        ai = roles["ai_tooling_role"]
        self.assertTrue(ai["permitted"])
        self.assertFalse(ai["casts_codes"])
        self.assertEqual(ai["final_code_authority"], "HUMAN_RESEARCH_LEAD_ONLY")
        self.assertEqual(
            profile["reliability"]["inter_rater"], "NOT_ESTIMABLE_SINGLE_CODER"
        )

    def test_03_all_analyses_exploratory_and_versioned_outputs_absent(self) -> None:
        """Planned-output paths stay empty until bootstrap-safe authorization."""
        data = json.loads(V3.read_text(encoding="utf-8"))
        self.assertEqual(data["primary_method_profile"]["profile_version"], 2)
        for analysis in data["analyses"]:
            self.assertEqual(analysis["analysis_mode"], "EXPLORATORY")
            loc = analysis["planned_output_artifact"]["locator"]
            self.assertIn("study-record-v3/outputs/", loc)
            self.assertFalse((ROOT / loc).exists(), loc)
        self.assertFalse(LIVE_INTAKE.exists())

    def test_04_solo_intake_schema_and_example(self) -> None:
        schema = json.loads(SOLO_SCHEMA.read_text(encoding="utf-8"))
        Draft202012Validator.check_schema(schema)
        example = json.loads(SOLO_EXAMPLE.read_text(encoding="utf-8"))
        Draft202012Validator(schema, format_checker=FormatChecker()).validate(example)
        self.assertFalse(example["ai_tooling_disclosure"]["ai_casts_final_codes"])
        self.assertEqual(
            example["research_lead"]["contributor_kind"], "HUMAN_RESEARCH_CONTRIBUTOR"
        )
        # agent-style ids rejected
        bad = json.loads(json.dumps(example))
        bad["research_lead"]["contributor_id"] = "AGENT-ORCHESTRATOR"
        with self.assertRaises(Exception):
            Draft202012Validator(schema, format_checker=FormatChecker()).validate(bad)

    def test_05_claims_forbid_invented_humans_and_ai_adjudication(self) -> None:
        pm = json.loads(
            (
                ROOT
                / "studies/foundational/m1-taxonomy-v1/superseding/study-record-v3/package-manifest.json"
            ).read_text(encoding="utf-8")
        )
        self.assertFalse(pm["execution_boundary"]["invented_human_adjudicators"])
        self.assertFalse(pm["execution_boundary"]["ai_final_coder"])
        not_made = " ".join(pm["claims_explicitly_not_made"]).lower()
        self.assertIn("independent", not_made)
        self.assertIn("ai adjudicated", not_made)


if __name__ == "__main__":
    unittest.main()
