from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from tools.validate_repository import (
    validate_registries,
    validate_repository,
    validate_required_paths,
    validate_schemas_and_examples,
    validate_dependency_lock,
    validate_local_artifact_references,
    validate_registry_entry_semantics,
    validate_serialized_documents,
)


class ParsingSafetyTests(unittest.TestCase):
    def test_duplicate_json_keys_are_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            path = root / "duplicate.json"
            path.write_text('{"id": "first", "id": "second"}', encoding="utf-8")

            errors = validate_serialized_documents(root)

        self.assertTrue(any("duplicate JSON key" in error for error in errors), errors)

    def test_duplicate_yaml_keys_are_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            path = root / "duplicate.yaml"
            path.write_text("schema_version: 1\nschema_version: 2\n", encoding="utf-8")

            errors = validate_serialized_documents(root)

        self.assertTrue(any("duplicate YAML key" in error for error in errors), errors)


class RepositoryContractTests(unittest.TestCase):
    def test_missing_required_files_are_reported(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            errors = validate_required_paths(Path(directory))

        self.assertTrue(errors)
        self.assertTrue(any("README.md" in error for error in errors))

    def test_registry_type_mismatch_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            registry_directory = root / "registry"
            registry_directory.mkdir()
            (registry_directory / "mechanisms.yaml").write_text(
                'schema_version: "0.1.0"\n'
                "registry_type: evidence_registry\n"
                "entries: []\n",
                encoding="utf-8",
            )

            errors = validate_registries(root)

        self.assertTrue(any("mechanism_registry" in error for error in errors))

    def test_unlisted_invalid_schema_is_discovered(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            schema_directory = root / "schemas"
            schema_directory.mkdir()
            (schema_directory / "future.schema.json").write_text(
                '{"$schema": "https://json-schema.org/draft/2020-12/schema", '
                '"$id": "urn:lcmrp:test:future", "type": 17}',
                encoding="utf-8",
            )

            errors = validate_schemas_and_examples(root)

        self.assertTrue(any("future.schema.json" in error for error in errors))

    def test_new_schema_and_matching_example_are_discovered_dynamically(self) -> None:
        """A newly added contract must be enforced without a validator allow-list edit."""
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "schemas").mkdir()
            (root / "examples").mkdir()
            (root / "schemas" / "future-artifact.schema.json").write_text(
                json.dumps(
                    {
                        "$schema": "https://json-schema.org/draft/2020-12/schema",
                        "$id": "urn:lcmrp:test:future-artifact",
                        "type": "object",
                        "additionalProperties": False,
                        "required": ["artifact_type"],
                        "properties": {
                            "artifact_type": {"const": "future_artifact"}
                        },
                    }
                ),
                encoding="utf-8",
            )
            (root / "examples" / "future-artifact.example.json").write_text(
                '{"artifact_type": "wrong_artifact_type"}',
                encoding="utf-8",
            )

            errors = validate_schemas_and_examples(root)

        self.assertTrue(
            any(
                "future-artifact.example.json" in error
                and "future_artifact" in error
                for error in errors
            ),
            errors,
        )

    def test_example_without_matching_schema_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "schemas").mkdir()
            (root / "examples").mkdir()
            (root / "examples" / "orphan.example.json").write_text(
                "{}",
                encoding="utf-8",
            )

            errors = validate_schemas_and_examples(root)

        self.assertTrue(any("no matching schema" in error for error in errors))

    def test_dependency_lock_must_match_direct_pins(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "requirements-dev.txt").write_text(
                "jsonschema==4.25.1\n",
                encoding="utf-8",
            )
            (root / "requirements-dev.lock").write_text(
                "jsonschema==4.24.0\n",
                encoding="utf-8",
            )

            errors = validate_dependency_lock(root)

        self.assertTrue(any("expected 4.25.1" in error for error in errors))

    def test_registry_rejects_digest_mismatch(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "registry").mkdir()
            (root / "schemas").mkdir()
            artifact_directory = root / "records" / "evidence"
            artifact_directory.mkdir(parents=True)

            (root / "schemas" / "record-index.schema.json").write_text(
                "{}",
                encoding="utf-8",
            )
            (root / "schemas" / "evidence-record.schema.json").write_text(
                '{"$id": "urn:lcmrp:schema:evidence-record:0.1.0"}',
                encoding="utf-8",
            )
            (artifact_directory / "record.json").write_text(
                '{"artifact_type": "evidence_record", '
                '"record_id": "LCMRP-EVIDREC-2026-TEST", "record_version": 1}',
                encoding="utf-8",
            )
            (root / "registry" / "evidence.yaml").write_text(
                'schema_version: "0.1.0"\n'
                "registry_type: evidence_registry\n"
                "entries:\n"
                "  - record_id: LCMRP-EVIDREC-2026-TEST\n"
                "    record_version: 1\n"
                "    artifact_type: evidence_record\n"
                "    schema_id: urn:lcmrp:schema:evidence-record:0.1.0\n"
                "    artifact_path: records/evidence/record.json\n"
                "    artifact_digest:\n"
                "      algorithm: SHA-256\n"
                f"      value: {'0' * 64}\n"
                "      scope: RAW_FILE_BYTES\n"
                "    registry_status: ACTIVE\n"
                '    registered_at: "2026-07-20T00:00:00Z"\n',
                encoding="utf-8",
            )

            errors = validate_registries(root)

        self.assertTrue(any("digest does not match" in error for error in errors))

    def test_recorded_local_artifact_digest_must_match(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "artifact.txt").write_text("actual bytes", encoding="utf-8")
            (root / "reference.json").write_text(
                json.dumps(
                    {
                        "artifact": {
                            "locator": "artifact.txt",
                            "digest": {
                                "algorithm": "sha256",
                                "status": "RECORDED",
                                "value": "0" * 64,
                            },
                        }
                    }
                ),
                encoding="utf-8",
            )

            errors = validate_local_artifact_references(root)

        self.assertTrue(any("recorded SHA-256 does not match" in error for error in errors))

    def test_registry_rejects_duplicate_record_versions(self) -> None:
        registry = {
            "registry_type": "evidence_registry",
            "entries": [
                {"record_id": "RECORD", "record_version": 1},
                {"record_id": "RECORD", "record_version": 1},
            ],
        }

        errors = validate_registry_entry_semantics(registry, "synthetic-registry")

        self.assertTrue(any("duplicate record_id/record_version" in error for error in errors))

    def test_repository_satisfies_m0_contracts(self) -> None:
        errors = validate_repository()
        self.assertEqual([], errors, "\n".join(errors))


if __name__ == "__main__":
    unittest.main()
