from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from tools.validate_repository import validate_schemas_and_examples


class M1DryRunDiscoveryTests(unittest.TestCase):
    """Ensure nested M1 dry-run records cannot bypass schema validation."""

    def test_nested_schema_backed_dry_run_record_is_validated(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            schemas = root / "schemas"
            bundle = root / "examples/m1-dry-runs/synthetic"
            schemas.mkdir()
            bundle.mkdir(parents=True)

            (schemas / "foundational-study-manifest.schema.json").write_text(
                json.dumps(
                    {
                        "$schema": "https://json-schema.org/draft/2020-12/schema",
                        "$id": "urn:lcmrp:test:nested-foundational-study",
                        "type": "object",
                        "additionalProperties": False,
                        "required": ["artifact_type", "record_status"],
                        "properties": {
                            "artifact_type": {
                                "const": "foundational_study_manifest"
                            },
                            "record_status": {"const": "FROZEN"},
                        },
                    }
                ),
                encoding="utf-8",
            )
            (bundle / "study-manifest.json").write_text(
                json.dumps(
                    {
                        "artifact_type": "foundational_study_manifest",
                        "record_status": "DRAFT",
                    }
                ),
                encoding="utf-8",
            )

            errors = validate_schemas_and_examples(root)

        self.assertTrue(
            any(
                "examples/m1-dry-runs/synthetic/study-manifest.json" in error
                and "FROZEN" in error
                for error in errors
            ),
            errors,
        )

    def test_untyped_support_fixture_is_parsed_but_not_forced_into_a_schema(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "schemas").mkdir()
            bundle = root / "examples/m1-dry-runs/synthetic"
            bundle.mkdir(parents=True)
            (bundle / "case-set.json").write_text(
                json.dumps({"fixture_status": "SYNTHETIC-DRY-RUN"}),
                encoding="utf-8",
            )

            errors = validate_schemas_and_examples(root)

        self.assertEqual([], errors)


if __name__ == "__main__":
    unittest.main()
