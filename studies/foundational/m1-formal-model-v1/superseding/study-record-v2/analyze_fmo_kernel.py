#!/usr/bin/env python3
"""Run the frozen, bounded FMO-0.1 propositional-kernel analyses.

This study-local analyzer intentionally implements only the finite Boolean kernel
declared in artifacts/formal-system.json. It is not a parser, type checker, model
checker, or proof assistant for the full natural-language FMO-0.1 artifact.

The execution guard refuses DRAFT manifests. Importing or compiling this module
does not run an analysis or create a result artifact.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import re
from pathlib import Path
from typing import Any, Iterable, Mapping


EXPECTED_STUDY_ID = "LCMRP-FSTUDY-0002-M1-FORMAL-MODEL"
EXPECTED_RECORD_ID = "LCMRP-FSTUDYREC-0002-M1-FORMAL-MODEL"
EXPECTED_PROFILE_ID = "LCMRP-MPROF-0002-M1-FORMAL-ANALYSIS"
EXPECTED_SUBJECT_ID = "LCMRP-FSUBJ-0002-FORMAL-MEMORY-OBJECT-MODEL"
EXPECTED_SUBJECT_DIGEST = (
    "82052e424c01d3204828472ef569f74f7c0aad418f827cffda92400562bbfaf3"
)
ACKNOWLEDGEMENT = "RUN-FROZEN-LCMRP-FSTUDY-0002-M1-FORMAL-MODEL"
CANONICAL_MANIFEST = Path(
    "records/foundational/studies/"
    "LCMRP-FSTUDYREC-0002-M1-FORMAL-MODEL-v2.json"
)
CANONICAL_INDEX = Path("registry/foundational-studies.yaml")
EXPECTED_INPUTS = {
    "formal_system": Path(
        "studies/foundational/m1-formal-model-v1/artifacts/formal-system.json"
    ),
    "assumptions": Path(
        "studies/foundational/m1-formal-model-v1/artifacts/assumptions.json"
    ),
    "propositions": Path(
        "studies/foundational/m1-formal-model-v1/artifacts/propositions.json"
    ),
    "configuration": Path(
        "studies/foundational/m1-formal-model-v1/artifacts/configuration.json"
    ),
}


class StudyGuardError(RuntimeError):
    """Raised when execution is attempted without exact frozen bindings."""


def raw_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as stream:
        return json.load(stream)


def contained_path(root: Path, candidate: Path, *, must_exist: bool = True) -> Path:
    path = candidate if candidate.is_absolute() else root / candidate
    resolved = path.resolve(strict=must_exist)
    if not resolved.is_relative_to(root):
        raise StudyGuardError(f"path escapes repository root: {candidate}")
    return resolved


def require_exact_path(root: Path, supplied: Path, expected_relative: Path) -> Path:
    supplied_resolved = contained_path(root, supplied)
    expected_resolved = contained_path(root, expected_relative)
    if supplied_resolved != expected_resolved:
        raise StudyGuardError(
            f"unexpected input path {supplied}; expected {expected_relative}"
        )
    return supplied_resolved


def evaluate(expression: Any, valuation: Mapping[str, bool]) -> bool:
    """Evaluate the deliberately small Boolean expression language."""
    if isinstance(expression, bool):
        return expression
    if isinstance(expression, str):
        try:
            return valuation[expression]
        except KeyError as exc:
            raise ValueError(f"undeclared Boolean variable: {expression}") from exc
    if not isinstance(expression, dict) or len(expression) != 1:
        raise ValueError(f"invalid expression node: {expression!r}")

    operator, operands = next(iter(expression.items()))
    if operator == "not":
        return not evaluate(operands, valuation)
    if operator in {"and", "or"}:
        if not isinstance(operands, list) or not operands:
            raise ValueError(f"{operator} requires a nonempty operand list")
        values = [evaluate(item, valuation) for item in operands]
        return all(values) if operator == "and" else any(values)
    if operator in {"implies", "iff"}:
        if not isinstance(operands, list) or len(operands) != 2:
            raise ValueError(f"{operator} requires exactly two operands")
        left, right = (evaluate(item, valuation) for item in operands)
        return ((not left) or right) if operator == "implies" else left == right
    raise ValueError(f"unsupported expression operator: {operator}")


def valuations(variables: Iterable[str]) -> Iterable[dict[str, bool]]:
    names = tuple(variables)
    for values in itertools.product((False, True), repeat=len(names)):
        yield dict(zip(names, values, strict=True))


def expression_variables(expression: Any) -> set[str]:
    if isinstance(expression, bool):
        return set()
    if isinstance(expression, str):
        return {expression}
    if not isinstance(expression, dict) or len(expression) != 1:
        raise ValueError(f"invalid expression node: {expression!r}")
    _, operands = next(iter(expression.items()))
    if isinstance(operands, list):
        variables_used: set[str] = set()
        for item in operands:
            variables_used.update(expression_variables(item))
        return variables_used
    return expression_variables(operands)


def constraints_hold(
    module: Mapping[str, Any],
    valuation: Mapping[str, bool],
    omitted_invariant: str | None = None,
) -> bool:
    for constraint in module["constraints"]:
        if constraint["invariant_id"] == omitted_invariant:
            continue
        if not evaluate(constraint["formula"], valuation):
            return False
    return True


def canonical_model(valuation: Mapping[str, bool]) -> dict[str, bool]:
    return {key: valuation[key] for key in sorted(valuation)}


def module_models(module: Mapping[str, Any]) -> list[dict[str, bool]]:
    return [
        canonical_model(valuation)
        for valuation in valuations(module["variables"])
        if constraints_hold(module, valuation)
    ]


def find_query_witness(
    module: Mapping[str, Any],
    premise: Any,
    conclusion: Any,
    relation: str,
) -> dict[str, bool] | None:
    declared = set(module["variables"])
    relevant = expression_variables(premise) | expression_variables(conclusion)
    for constraint in module["constraints"]:
        relevant.update(expression_variables(constraint["formula"]))
    if not relevant <= declared:
        raise ValueError(
            f"query uses undeclared variables: {sorted(relevant - declared)}"
        )
    for valuation in valuations(sorted(relevant)):
        if not constraints_hold(module, valuation):
            continue
        premise_holds = evaluate(premise, valuation)
        conclusion_holds = evaluate(conclusion, valuation)
        if relation == "ENTAILMENT" and premise_holds and not conclusion_holds:
            return canonical_model(valuation)
        if relation == "NON_ENTAILMENT" and premise_holds and not conclusion_holds:
            return canonical_model(valuation)
    return None


def verify_artifact_reference(root: Path, reference: Mapping[str, Any]) -> None:
    digest = reference["digest"]
    if digest["status"] not in {"RECORDED", "VERIFIED"}:
        raise StudyGuardError(
            f"artifact is not immutable: {reference['artifact_id']}"
        )
    path = contained_path(root, Path(reference["locator"]))
    if not path.is_file():
        raise StudyGuardError(f"artifact is not a file: {reference['locator']}")
    actual = raw_sha256(path)
    if actual != digest["value"]:
        raise StudyGuardError(
            f"digest mismatch for {reference['locator']}: {actual}"
        )


def find_reference(
    manifest: Mapping[str, Any], artifact_id: str
) -> Mapping[str, Any]:
    references: list[Mapping[str, Any]] = []
    profile = manifest["primary_method_profile"]
    references.extend(
        [
            manifest["subject"]["definition_artifact"],
            profile["profile_definition_artifact"],
            profile["formal_system_artifact"],
            profile["tool_provenance"],
            manifest["protocol_artifact"],
            manifest["reproducibility"]["environment_artifact"],
        ]
    )
    references.extend(
        source["provenance_artifact"] for source in manifest["sources"]
    )
    references.extend(manifest["reproducibility"]["configuration_artifacts"])
    matches = [ref for ref in references if ref["artifact_id"] == artifact_id]
    if not matches:
        raise StudyGuardError(
            f"manifest has no reference for {artifact_id}"
        )
    if any(reference != matches[0] for reference in matches[1:]):
        raise StudyGuardError(
            f"manifest has conflicting references for {artifact_id}"
        )
    return matches[0]


def require_bound_input(
    root: Path,
    manifest: Mapping[str, Any],
    supplied: Path,
    expected_relative: Path,
    artifact_id: str,
) -> Path:
    resolved = require_exact_path(root, supplied, expected_relative)
    reference = find_reference(manifest, artifact_id)
    if reference["locator"] != expected_relative.as_posix():
        raise StudyGuardError(
            f"manifest locator mismatch for {artifact_id}: {reference['locator']}"
        )
    verify_artifact_reference(root, reference)
    if raw_sha256(resolved) != reference["digest"]["value"]:
        raise StudyGuardError(f"loaded input is not frozen artifact {artifact_id}")
    return resolved


def verify_manifest_index(root: Path, manifest_path: Path) -> None:
    """Fail closed unless the canonical index binds this exact manifest digest.

    This superseding pre-result guard intentionally avoids indentation-sensitive
    matching for nested ``artifact_digest.value``. It locates the accepted active
    registry entry by record identity, then reads required key/value pairs within
    that entry regardless of their YAML indentation depth.
    """
    index_path = contained_path(root, CANONICAL_INDEX)
    text = index_path.read_text(encoding="utf-8")
    entries: list[list[str]] = []
    current: list[str] | None = None
    for line in text.splitlines():
        if re.match(r"^\s*-\s+record_id:\s*", line):
            if current is not None:
                entries.append(current)
            current = [line]
        elif current is not None:
            current.append(line)
    if current is not None:
        entries.append(current)

    def scalar(line: str) -> str:
        return line.split(":", 1)[1].strip().strip('"\'')

    def field_from(entry_lines: list[str], label: str, pattern: str) -> str:
        found = [line for line in entry_lines if re.match(pattern, line)]
        if len(found) != 1:
            raise StudyGuardError(f"canonical index entry lacks {label}")
        return scalar(found[0])

    active_matches: list[list[str]] = []
    for entry_lines in entries:
        record_lines = [
            line for line in entry_lines
            if re.match(r"^\s*-\s+record_id:\s*", line)
        ]
        if len(record_lines) != 1 or scalar(record_lines[0]) != EXPECTED_RECORD_ID:
            continue
        try:
            status = field_from(
                entry_lines, "registry_status", r"^\s+registry_status:\s*"
            )
        except StudyGuardError:
            continue
        if status == "ACTIVE":
            active_matches.append(entry_lines)
    if len(active_matches) != 1:
        raise StudyGuardError(
            "canonical study index must contain exactly one ACTIVE matching record entry"
        )
    entry_lines = active_matches[0]

    version = field_from(entry_lines, "record_version", r"^\s+record_version:\s*")
    artifact_path = field_from(entry_lines, "artifact_path", r"^\s+artifact_path:\s*")
    indexed_digest = field_from(
        entry_lines,
        "artifact_digest.value",
        r"^\s+value:\s*[\"']?[a-f0-9]{64}[\"']?\s*$",
    )
    status = field_from(entry_lines, "registry_status", r"^\s+registry_status:\s*")
    if version != "2":
        raise StudyGuardError("canonical index points to an unexpected record version")
    if artifact_path != CANONICAL_MANIFEST.as_posix():
        raise StudyGuardError("canonical index points to an unexpected artifact path")
    if status != "ACTIVE":
        raise StudyGuardError("canonical frozen study record is not ACTIVE")
    if indexed_digest != raw_sha256(manifest_path):
        raise StudyGuardError("canonical index digest does not match the manifest")

def verify_analyzer_tool_binding(
    root: Path, manifest: Mapping[str, Any]
) -> None:
    reference = find_reference(
        manifest, "LCMRP-ARTIFACT-0002-M1-FMO-TOOL-PROVENANCE"
    )
    verify_artifact_reference(root, reference)
    tool_document = load_json(contained_path(root, Path(reference["locator"])))
    expected_script = Path(tool_document["analyzer"]["locator"])
    actual_script = contained_path(root, Path(__file__))
    if actual_script != contained_path(root, expected_script):
        raise StudyGuardError("executed analyzer path differs from frozen tool provenance")
    if raw_sha256(actual_script) != tool_document["analyzer"]["raw_byte_sha256"]:
        raise StudyGuardError("executed analyzer digest differs from tool provenance")


def enforce_frozen_manifest(
    root: Path, manifest_path: Path, manifest: Mapping[str, Any]
) -> None:
    if manifest.get("study_id") != EXPECTED_STUDY_ID:
        raise StudyGuardError("unexpected study identity")
    if manifest.get("study_record_id") != EXPECTED_RECORD_ID:
        raise StudyGuardError("unexpected study-record identity")
    if manifest.get("record_status") != "FROZEN":
        raise StudyGuardError("analysis is forbidden until record_status is FROZEN")
    preregistration = manifest.get("preregistration", {})
    if preregistration.get("status") != "FROZEN":
        raise StudyGuardError("analysis is forbidden until preregistration is FROZEN")
    if preregistration.get("results_accessed_before_freeze") is not False:
        raise StudyGuardError("no-prior-result-access assertion is absent")
    for required in ("frozen_at", "registration_authority", "freeze_artifact"):
        if not preregistration.get(required):
            raise StudyGuardError(f"missing frozen preregistration field: {required}")

    subject = manifest.get("subject", {})
    if subject.get("subject_id") != EXPECTED_SUBJECT_ID:
        raise StudyGuardError("unexpected subject identity")
    subject_digest = subject.get("definition_artifact", {}).get("digest", {})
    if subject_digest.get("value") != EXPECTED_SUBJECT_DIGEST:
        raise StudyGuardError("unexpected subject raw-byte digest")

    profile = manifest.get("primary_method_profile", {})
    if profile.get("profile_id") != EXPECTED_PROFILE_ID:
        raise StudyGuardError("unexpected method-profile identity")
    if profile.get("profile_kind") != "FORMAL_ANALYSIS":
        raise StudyGuardError("unexpected method-profile kind")

    verify_artifact_reference(root, subject["definition_artifact"])
    verify_artifact_reference(root, profile["profile_definition_artifact"])
    verify_artifact_reference(root, profile["formal_system_artifact"])
    verify_artifact_reference(root, profile["tool_provenance"])
    verify_artifact_reference(root, preregistration["freeze_artifact"])
    verify_artifact_reference(root, manifest["protocol_artifact"])
    for source in manifest["sources"]:
        verify_artifact_reference(root, source["provenance_artifact"])
    verify_artifact_reference(root, manifest["reproducibility"]["environment_artifact"])
    for reference in manifest["reproducibility"]["configuration_artifacts"]:
        verify_artifact_reference(root, reference)
    verify_manifest_index(root, manifest_path)
    verify_analyzer_tool_binding(root, manifest)


def check_identity(document: Mapping[str, Any], key: str, expected: str) -> None:
    if document.get(key) != expected:
        raise StudyGuardError(f"unexpected {key}: {document.get(key)!r}")


def enforce_unique_absent_output_plan(
    root: Path,
    manifest: Mapping[str, Any],
    configuration: Mapping[str, Any],
) -> dict[str, str]:
    manifest_outputs = {
        analysis["analysis_id"]: analysis["planned_output_artifact"]["locator"]
        for analysis in manifest["analyses"]
    }
    configured_outputs = configuration.get("analysis_output_artifacts")
    if configured_outputs != manifest_outputs:
        raise StudyGuardError(
            "configuration output map differs from frozen manifest analyses"
        )
    if len(manifest_outputs) != 7:
        raise StudyGuardError("frozen study must contain exactly seven analyses")
    if len(set(manifest_outputs.values())) != len(manifest_outputs):
        raise StudyGuardError("each analysis must have one unique output locator")
    for locator in manifest_outputs.values():
        planned_path = contained_path(root, Path(locator), must_exist=False)
        if planned_path.exists():
            raise StudyGuardError(
                f"planned analysis output already exists before execution: {locator}"
            )
    return manifest_outputs


def run_kernel(
    formal_system: Mapping[str, Any],
    propositions: Mapping[str, Any],
) -> dict[str, Any]:
    modules = {module["module_id"]: module for module in formal_system["modules"]}
    model_summary: list[dict[str, Any]] = []
    for module in modules.values():
        if module.get("include_in_satisfiability", True) is not True:
            continue
        models = module_models(module)
        model_summary.append(
            {
                "module_id": module["module_id"],
                "valuation_count": 2 ** len(module["variables"]),
                "satisfying_model_count": len(models),
                "first_satisfying_model": models[0] if models else None,
            }
        )

    entailments: list[dict[str, Any]] = []
    non_entailments: list[dict[str, Any]] = []
    for proposition in propositions["semantic_queries"]:
        module = modules[proposition["module_id"]]
        witness = find_query_witness(
            module,
            proposition["premise"],
            proposition["conclusion"],
            proposition["relation"],
        )
        row = {
            "proposition_id": proposition["proposition_id"],
            "module_id": proposition["module_id"],
            "relation": proposition["relation"],
            "counterexample_or_witness": witness,
        }
        if proposition["relation"] == "ENTAILMENT":
            row["holds_within_kernel"] = witness is None
            entailments.append(row)
        else:
            row["witness_retained"] = witness is not None
            non_entailments.append(row)

    invariant_independence: list[dict[str, Any]] = []
    for module in modules.values():
        for constraint in module["constraints"]:
            invariant_id = constraint["invariant_id"]
            witness = None
            for valuation in valuations(module["variables"]):
                if not constraints_hold(module, valuation, invariant_id):
                    continue
                if not evaluate(constraint["formula"], valuation):
                    witness = canonical_model(valuation)
                    break
            invariant_independence.append(
                {
                    "invariant_id": invariant_id,
                    "module_id": module["module_id"],
                    "independence_witness": witness,
                    "independent_within_kernel": witness is not None,
                }
            )

    named_witnesses: list[dict[str, Any]] = []
    for witness_definition in propositions["named_countermodels"]:
        module = modules[witness_definition["module_id"]]
        supplied_assignment = witness_definition["assignment"]
        if not set(supplied_assignment) <= set(module["variables"]):
            raise ValueError(
                f"{witness_definition['countermodel_id']} assigns undeclared variables"
            )
        assignment = {name: False for name in module["variables"]}
        assignment.update(supplied_assignment)
        constraints_satisfied = constraints_hold(module, assignment)
        witness_condition_holds = evaluate(
            witness_definition["witness_condition"], assignment
        )
        named_witnesses.append(
            {
                "countermodel_id": witness_definition["countermodel_id"],
                "module_id": witness_definition["module_id"],
                "constraints_satisfied": constraints_satisfied,
                "witness_condition_holds": witness_condition_holds,
                "assignment": canonical_model(assignment),
            }
        )

    return {
        "study_id": EXPECTED_STUDY_ID,
        "study_record_id": EXPECTED_RECORD_ID,
        "profile_id": EXPECTED_PROFILE_ID,
        "kernel_id": formal_system["formal_system_id"],
        "kernel_version": formal_system["formal_system_version"],
        "scope_notice": formal_system["scope_notice"],
        "satisfiability": model_summary,
        "intended_entailments": entailments,
        "non_entailments": non_entailments,
        "invariant_independence": invariant_independence,
        "named_countermodels": named_witnesses,
        "semantic_validity_status": "REQUIRES-SEPARATE-HUMAN-ADJUDICATION",
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repository-root", type=Path, required=True)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--formal-system", type=Path, required=True)
    parser.add_argument("--assumptions", type=Path, required=True)
    parser.add_argument("--propositions", type=Path, required=True)
    parser.add_argument("--configuration", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--acknowledge", required=True)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.acknowledge != ACKNOWLEDGEMENT:
        raise StudyGuardError("explicit frozen-study acknowledgement is required")

    root = args.repository_root.resolve(strict=True)
    if not root.is_dir():
        raise StudyGuardError("repository root is not a directory")
    manifest_path = require_exact_path(root, args.manifest, CANONICAL_MANIFEST)
    manifest = load_json(manifest_path)
    enforce_frozen_manifest(root, manifest_path, manifest)

    formal_system_path = require_bound_input(
        root,
        manifest,
        args.formal_system,
        EXPECTED_INPUTS["formal_system"],
        "LCMRP-ARTIFACT-0002-M1-FMO-BOUNDED-FORMAL-SYSTEM",
    )
    assumptions_path = require_bound_input(
        root,
        manifest,
        args.assumptions,
        EXPECTED_INPUTS["assumptions"],
        "LCMRP-ARTIFACT-0002-M1-FMO-ASSUMPTIONS",
    )
    propositions_path = require_bound_input(
        root,
        manifest,
        args.propositions,
        EXPECTED_INPUTS["propositions"],
        "LCMRP-ARTIFACT-0002-M1-FMO-PROPOSITIONS",
    )
    configuration_path = require_bound_input(
        root,
        manifest,
        args.configuration,
        EXPECTED_INPUTS["configuration"],
        "LCMRP-ARTIFACT-0002-M1-FMO-CONFIGURATION",
    )

    formal_system = load_json(formal_system_path)
    assumptions = load_json(assumptions_path)
    propositions = load_json(propositions_path)
    configuration = load_json(configuration_path)
    check_identity(
        formal_system,
        "formal_system_id",
        "LCMRP-FSYS-0002-M1-FMO-BOUNDED-KERNEL",
    )
    check_identity(assumptions, "study_id", EXPECTED_STUDY_ID)
    check_identity(propositions, "study_id", EXPECTED_STUDY_ID)
    check_identity(configuration, "study_id", EXPECTED_STUDY_ID)

    if configuration.get("execution_requires_frozen_manifest") is not True:
        raise StudyGuardError("configuration does not preserve the freeze guard")
    if configuration.get("network_allowed") is not False:
        raise StudyGuardError("network must remain disabled")
    if configuration.get("randomness") != "NONE-DETERMINISTIC-EXHAUSTIVE":
        raise StudyGuardError("unexpected randomness policy")
    output_plan = enforce_unique_absent_output_plan(root, manifest, configuration)

    output_path = contained_path(root, args.output, must_exist=False)
    expected_output = contained_path(
        root, Path(configuration["machine_output_artifact"]), must_exist=False
    )
    if output_path != expected_output:
        raise StudyGuardError("output path differs from frozen configuration")
    if output_plan["ANALYSIS-FMO-01-SATISFIABILITY"] != Path(
        configuration["machine_output_artifact"]
    ).as_posix():
        raise StudyGuardError(
            "machine output must be Analysis 01's unique planned artifact"
        )

    result = run_kernel(formal_system, propositions)
    result["input_digests"] = {
        "manifest": raw_sha256(manifest_path),
        "formal_system": raw_sha256(formal_system_path),
        "assumptions": raw_sha256(assumptions_path),
        "propositions": raw_sha256(propositions_path),
        "configuration": raw_sha256(configuration_path),
        "analyzer": raw_sha256(Path(__file__)),
    }
    result["execution_boundary"] = (
        "A bounded kernel result is not proof, validation, or evidence for all of "
        "FMO-0.1. Human semantic-validity adjudication remains mandatory."
    )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("x", encoding="utf-8", newline="\n") as stream:
        json.dump(result, stream, indent=2, sort_keys=True)
        stream.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
