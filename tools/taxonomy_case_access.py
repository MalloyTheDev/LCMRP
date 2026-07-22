#!/usr/bin/env python3
"""Build a fail-closed, metadata-only access catalog for taxonomy studies.

The catalog is constructed from the foundational-study registry and its indexed
canonical manifests before any repository-wide JSON scan occurs.  It identifies
case sources and planned outputs that generic validation must treat as opaque.
This module never reads a protected case or output body and grants no execution
or case-access authority. Research layer: program infrastructure supporting
Layer 1 — Foundational Research. Evidence effect: none.
"""

from __future__ import annotations

from collections import defaultdict
from collections.abc import Mapping
from dataclasses import dataclass
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import stat
from typing import Any, Literal
import unicodedata

import yaml


STUDY_REGISTRY = "registry/foundational-studies.yaml"
TAXONOMY_PROFILE_KIND = "STRUCTURAL_OR_TAXONOMY_EVALUATION"
TAXONOMY_SUBJECT_KIND = "MEMORY_TAXONOMY"
CASE_SOURCE_KIND = "SYNTHETIC_CASE_SET"
CASE_SCHEMA_ID = "urn:lcmrp:taxonomy-synthetic-case-set:0.1.0"
CASE_ROLES = frozenset(
    {"POSITIVE_CASES", "NEGATIVE_CASES", "HELD_OUT_EVALUATION"}
)
SHA256 = re.compile(r"^[a-f0-9]{64}$")
SAFE_LOCATOR = re.compile(r"^[A-Za-z0-9._/-]+$")
STUDY_ARTIFACT_PREFIX = ("studies", "foundational")
CANONICAL_MANIFEST_PREFIX = ("records", "foundational", "studies")


class CatalogLoadError(ValueError):
    """Raised when authoritative catalog metadata cannot be loaded safely."""


@dataclass(frozen=True)
class GovernedCaseBinding:
    """Exact metadata binding retained for an immutable governed case source."""

    source_id: str
    source_kind: str
    role: str
    artifact_id: str
    artifact_version: int
    schema_id: str
    locator: str
    media_type: str
    digest_status: str
    digest_value: str

    @property
    def binding_key(self) -> tuple[Any, ...]:
        return (
            self.artifact_id,
            self.artifact_version,
            self.schema_id,
            self.locator,
            self.media_type,
            "SHA-256",
            self.digest_status,
            self.digest_value,
            "RAW_FILE_BYTES",
        )


GOVERNED_V1_TAXONOMY_KEY = (
    "LCMRP-FSTUDY-0001-M1-TAXONOMY",
    "LCMRP-FSTUDYREC-0001-M1-TAXONOMY",
    1,
)
GOVERNED_V1_TAXONOMY_LINEAGE_KEY = GOVERNED_V1_TAXONOMY_KEY[:2]
GOVERNED_V1_STUDY_NAMESPACE = "studies/foundational/m1-taxonomy-v1"
GOVERNED_V1_MANIFEST_LOCATOR = (
    "records/foundational/studies/LCMRP-FSTUDYREC-0001-M1-TAXONOMY-v1.json"
)
GOVERNED_V1_MANIFEST_DIGEST = (
    "01640e8dae3836874b2b39fe3ea2a8f9c090374508aa69b31adf06fea9272139"
)
GOVERNED_V1_CASE_BINDINGS = (
    GovernedCaseBinding(
        source_id="SOURCE-M1-TAXONOMY-POSITIVE",
        source_kind=CASE_SOURCE_KIND,
        role="POSITIVE_CASES",
        artifact_id="ARTIFACT-M1-TAXONOMY-POSITIVE-CASES",
        artifact_version=1,
        schema_id=CASE_SCHEMA_ID,
        locator="studies/foundational/m1-taxonomy-v1/cases/positive-cases.json",
        media_type="application/json",
        digest_status="VERIFIED",
        digest_value="61412fb42208441f78927ac0ad3f579758a34591b6cb20bd8163648edcea424b",
    ),
    GovernedCaseBinding(
        source_id="SOURCE-M1-TAXONOMY-NEGATIVE",
        source_kind=CASE_SOURCE_KIND,
        role="NEGATIVE_CASES",
        artifact_id="ARTIFACT-M1-TAXONOMY-NEGATIVE-CASES",
        artifact_version=1,
        schema_id=CASE_SCHEMA_ID,
        locator="studies/foundational/m1-taxonomy-v1/cases/negative-cases.json",
        media_type="application/json",
        digest_status="VERIFIED",
        digest_value="6a546d401f8c412a6a15f3ae7e8f733924b46a145e7339d5d1d441e887d1ab4a",
    ),
    GovernedCaseBinding(
        source_id="SOURCE-M1-TAXONOMY-HELD-OUT",
        source_kind=CASE_SOURCE_KIND,
        role="HELD_OUT_EVALUATION",
        artifact_id="ARTIFACT-M1-TAXONOMY-HELD-OUT-CASES",
        artifact_version=1,
        schema_id=CASE_SCHEMA_ID,
        locator="studies/foundational/m1-taxonomy-v1/cases/held-out-cases.json",
        media_type="application/json",
        digest_status="VERIFIED",
        digest_value="e0f08002a9252ff1f1f4da119958c9d6a86f50cf3b3922672c9bffbf73c68c79",
    ),
)
GOVERNED_V1_FOOTPRINT_LOCATORS = (
    GOVERNED_V1_STUDY_NAMESPACE,
    GOVERNED_V1_MANIFEST_LOCATOR,
    *(binding.locator for binding in GOVERNED_V1_CASE_BINDINGS),
)


@dataclass(frozen=True)
class ProtectedArtifact:
    """One case source or planned output that generic readers must not open."""

    kind: Literal["CASE_SOURCE", "PLANNED_OUTPUT"]
    locator: str
    resolved_path: Path
    owner_manifest: str
    study_id: str
    study_record_id: str
    record_version: int
    artifact_id: str
    source_role_or_analysis_id: str
    binding_key: tuple[Any, ...]
    expected_sha256: str | None


@dataclass(frozen=True)
class IndexedTaxonomyStudy:
    """Metadata needed to validate version lineage without reading case bytes."""

    registry_index: int
    registry_status: str
    registry_digest: str | None
    manifest_path: str
    manifest: Mapping[str, Any]

    @property
    def study_id(self) -> Any:
        return self.manifest.get("study_id")

    @property
    def record_id(self) -> Any:
        return self.manifest.get("study_record_id")

    @property
    def record_version(self) -> Any:
        return self.manifest.get("record_version")


@dataclass(frozen=True)
class StudyAccessCatalog:
    """Authoritative metadata-only policy plus any fail-closed bootstrap errors."""

    root: Path
    case_artifacts: tuple[ProtectedArtifact, ...]
    output_artifacts: tuple[ProtectedArtifact, ...]
    taxonomy_studies: tuple[IndexedTaxonomyStudy, ...]
    errors: tuple[str, ...]

    @property
    def protected_artifacts(self) -> tuple[ProtectedArtifact, ...]:
        return self.case_artifacts + self.output_artifacts

    @property
    def case_roots(self) -> tuple[Path, ...]:
        return tuple(
            sorted({artifact.resolved_path.parent for artifact in self.case_artifacts})
        )

    @property
    def output_roots(self) -> tuple[Path, ...]:
        return tuple(
            sorted({artifact.resolved_path.parent for artifact in self.output_artifacts})
        )

    @property
    def protected_roots(self) -> tuple[Path, ...]:
        return tuple(sorted(set(self.case_roots) | set(self.output_roots)))

    def require_usable(self) -> None:
        """Reject incomplete catalogs before any repository body reader runs."""

        if self.errors:
            first = self.errors[0]
            remainder = len(self.errors) - 1
            suffix = f" (+{remainder} more error(s))" if remainder else ""
            raise CatalogLoadError(
                f"taxonomy case-access policy is unavailable: {first}{suffix}"
            )

    def artifacts_for_locator(self, locator: str) -> tuple[ProtectedArtifact, ...]:
        return tuple(
            artifact
            for artifact in self.protected_artifacts
            if artifact.locator == locator
        )

    def artifact_for_locator(self, locator: str) -> ProtectedArtifact | None:
        matches = self.artifacts_for_locator(locator)
        return matches[0] if matches else None

    def artifact_for_path(self, path: Path) -> ProtectedArtifact | None:
        resolved = path.resolve(strict=False)
        matches = [
            artifact
            for artifact in self.protected_artifacts
            if artifact.resolved_path == resolved
        ]
        return matches[0] if matches else None

    def protects_path(self, path: Path) -> bool:
        """Return whether generic validation must treat ``path`` as opaque."""

        resolved = path.resolve(strict=False)
        if any(artifact.resolved_path == resolved for artifact in self.protected_artifacts):
            return True
        return any(
            resolved == protected_root or protected_root in resolved.parents
            for protected_root in self.protected_roots
        )

    def read_metadata_bytes(self, path: Path) -> bytes:
        """Read one non-protected metadata file through the fail-closed policy."""

        self.require_usable()
        if self.protects_path(path):
            try:
                relative = path.resolve(strict=False).relative_to(self.root).as_posix()
            except ValueError:
                relative = str(path)
            raise CatalogLoadError(
                f"metadata reader cannot access protected taxonomy bytes: {relative}"
            )
        return _read_repository_file_bytes(self.root, path)


def _reject_duplicate_json_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise CatalogLoadError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def _read_repository_file_bytes(root: Path, path: Path) -> bytes:
    """Read one regular repository file without following any path component.

    The descriptor walk closes the check/open race present in a separate
    ``lstat`` followed by ``Path.open``.  Fail closed on platforms that cannot
    provide ``O_NOFOLLOW`` rather than silently weakening the access boundary.
    """

    root = root.resolve()
    candidate = path if path.is_absolute() else root / path
    try:
        relative = candidate.relative_to(root)
    except ValueError as exc:
        raise CatalogLoadError(f"repository metadata path escapes root: {path}") from exc
    if not relative.parts or any(part in {"", ".", ".."} for part in relative.parts):
        raise CatalogLoadError(f"repository metadata path is not canonical: {path}")
    if not hasattr(os, "O_NOFOLLOW"):
        raise CatalogLoadError("O_NOFOLLOW is required for repository metadata reads")

    directory_flags = os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW
    file_flags = os.O_RDONLY | os.O_NOFOLLOW
    directory_flags |= getattr(os, "O_CLOEXEC", 0)
    file_flags |= getattr(os, "O_CLOEXEC", 0)

    directory_fd: int | None = None
    file_fd: int | None = None
    try:
        directory_fd = os.open(root, directory_flags)
        for part in relative.parts[:-1]:
            next_fd = os.open(part, directory_flags, dir_fd=directory_fd)
            metadata = os.fstat(next_fd)
            if not stat.S_ISDIR(metadata.st_mode):
                os.close(next_fd)
                raise CatalogLoadError(
                    f"repository metadata path has a non-directory ancestor: {path}"
                )
            os.close(directory_fd)
            directory_fd = next_fd

        file_fd = os.open(relative.parts[-1], file_flags, dir_fd=directory_fd)
        metadata = os.fstat(file_fd)
        if not stat.S_ISREG(metadata.st_mode):
            raise CatalogLoadError(f"repository metadata is not a regular file: {path}")
        if metadata.st_nlink != 1:
            raise CatalogLoadError(
                f"repository metadata has {metadata.st_nlink} hard links: {path}"
            )
        with os.fdopen(file_fd, "rb", closefd=True) as handle:
            file_fd = None
            return handle.read()
    except CatalogLoadError:
        raise
    except OSError as exc:
        raise CatalogLoadError(f"cannot safely read repository metadata {path}: {exc}") from exc
    finally:
        if file_fd is not None:
            os.close(file_fd)
        if directory_fd is not None:
            os.close(directory_fd)


def _load_json_bytes(root: Path, path: Path) -> tuple[Any, str]:
    try:
        raw = _read_repository_file_bytes(root, path)
        document = json.loads(
            raw.decode("utf-8"),
            object_pairs_hook=_reject_duplicate_json_pairs,
        )
    except (OSError, UnicodeDecodeError, json.JSONDecodeError, CatalogLoadError) as exc:
        raise CatalogLoadError(f"{path}: {exc}") from exc
    return document, hashlib.sha256(raw).hexdigest()


def _load_yaml_unique(root: Path, path: Path) -> Any:
    class UniqueKeyLoader(yaml.SafeLoader):
        pass

    def construct_mapping(
        loader: UniqueKeyLoader,
        node: Any,
        deep: bool = False,
    ) -> Any:
        mapping: dict[Any, Any] = {}
        for key_node, value_node in node.value:
            key = loader.construct_object(key_node, deep=deep)
            if key in mapping:
                raise CatalogLoadError(f"{path}: duplicate YAML key: {key}")
            mapping[key] = loader.construct_object(value_node, deep=deep)
        return mapping

    UniqueKeyLoader.add_constructor(
        yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
        construct_mapping,
    )
    try:
        raw = _read_repository_file_bytes(root, path)
        return yaml.load(raw.decode("utf-8"), Loader=UniqueKeyLoader)
    except (
        OSError,
        TypeError,
        UnicodeDecodeError,
        yaml.YAMLError,
        CatalogLoadError,
    ) as exc:
        raise CatalogLoadError(f"{path}: {exc}") from exc


def _parse_repository_locator(
    locator: Any,
    *,
    required_prefix: tuple[str, ...] | None = None,
) -> tuple[PurePosixPath | None, list[str]]:
    """Parse one canonical ASCII repository locator without touching its target."""

    if not isinstance(locator, str) or not locator:
        return None, ["locator must be a non-empty string"]
    if unicodedata.normalize("NFC", locator) != locator:
        return None, [f"repository locator is not NFC-normalized: {locator!r}"]
    if (
        "\x00" in locator
        or "\\" in locator
        or any(ord(character) < 32 or ord(character) == 127 for character in locator)
        or not SAFE_LOCATOR.fullmatch(locator)
    ):
        return None, [f"unsafe repository locator: {locator!r}"]

    pure = PurePosixPath(locator)
    if (
        pure.is_absolute()
        or locator != pure.as_posix()
        or any(part in {"", ".", ".."} for part in pure.parts)
    ):
        return None, [f"non-canonical repository locator: {locator!r}"]
    if required_prefix is not None and pure.parts[: len(required_prefix)] != required_prefix:
        return None, [
            f"repository locator is outside {'/'.join(required_prefix)}/: {locator}"
        ]
    return pure, []


def _repository_path_presence(
    root: Path,
    locator: str,
) -> tuple[bool, list[str]]:
    """Inspect whether an exact repository path exists without following aliases."""

    pure, errors = _parse_repository_locator(locator)
    if pure is None:
        return True, errors

    current = root
    for index, part in enumerate(pure.parts):
        current = current / part
        try:
            metadata = os.lstat(current)
        except FileNotFoundError:
            return False, errors
        except OSError as exc:
            errors.append(f"cannot inspect repository locator {locator}: {exc}")
            return True, errors

        if stat.S_ISLNK(metadata.st_mode):
            errors.append(f"repository locator traverses a symlink: {locator}")
            return True, errors
        if index < len(pure.parts) - 1 and not stat.S_ISDIR(metadata.st_mode):
            errors.append(
                f"repository locator has a non-directory ancestor: {locator}"
            )
            return True, errors
    return True, errors


def _governed_v1_footprint(root: Path) -> tuple[bool, list[str]]:
    """Detect immutable v1 path signals without reading any artifact body."""

    present = False
    errors: list[str] = []
    for locator in GOVERNED_V1_FOOTPRINT_LOCATORS:
        observed, locator_errors = _repository_path_presence(root, locator)
        present = present or observed
        errors.extend(
            f"governed v1 taxonomy footprint {locator}: {error}"
            for error in locator_errors
        )
    return present, errors


def _safe_repository_path(
    root: Path,
    locator: Any,
    *,
    must_exist: bool,
    required_prefix: tuple[str, ...] | None = None,
) -> tuple[Path | None, list[str]]:
    """Resolve a canonical repository-relative path using metadata-only checks."""

    pure, errors = _parse_repository_locator(
        locator,
        required_prefix=required_prefix,
    )
    if pure is None:
        return None, errors

    candidate = root.joinpath(*pure.parts)
    current = root
    leaf_stat: os.stat_result | None = None
    for index, part in enumerate(pure.parts):
        current = current / part
        try:
            metadata = os.lstat(current)
        except FileNotFoundError:
            if must_exist:
                errors.append(f"repository artifact is missing: {locator}")
            break
        except OSError as exc:
            errors.append(f"cannot inspect repository locator {locator}: {exc}")
            break

        is_leaf = index == len(pure.parts) - 1
        if stat.S_ISLNK(metadata.st_mode):
            errors.append(f"repository locator traverses a symlink: {locator}")
            break
        if is_leaf:
            leaf_stat = metadata
        elif not stat.S_ISDIR(metadata.st_mode):
            errors.append(f"repository locator has a non-directory ancestor: {locator}")
            break

    if leaf_stat is not None:
        if not stat.S_ISREG(leaf_stat.st_mode):
            errors.append(f"repository artifact is not a regular file: {locator}")
        elif leaf_stat.st_nlink != 1:
            errors.append(
                f"repository artifact has {leaf_stat.st_nlink} hard links: {locator}"
            )
    return candidate, errors


def _digest_value(reference: Any) -> tuple[str | None, list[str]]:
    errors: list[str] = []
    if not isinstance(reference, Mapping):
        return None, ["artifact reference is missing"]
    digest = reference.get("digest")
    if not isinstance(digest, Mapping):
        return None, ["artifact digest is missing"]
    if digest.get("algorithm") != "SHA-256":
        errors.append("artifact digest algorithm must be SHA-256")
    if digest.get("scope") != "RAW_FILE_BYTES":
        errors.append("artifact digest scope must be RAW_FILE_BYTES")
    value = digest.get("value")
    if not isinstance(value, str) or not SHA256.fullmatch(value):
        errors.append("artifact digest value must be a lowercase SHA-256")
        return None, errors
    if digest.get("status") not in {"RECORDED", "VERIFIED"}:
        errors.append("protected case digest must be RECORDED or VERIFIED")
    return value, errors


def _artifact_binding_key(reference: Mapping[str, Any]) -> tuple[Any, ...]:
    digest = reference.get("digest")
    digest_mapping = digest if isinstance(digest, Mapping) else {}
    return (
        reference.get("artifact_id"),
        reference.get("artifact_version"),
        reference.get("schema_id"),
        reference.get("locator"),
        reference.get("media_type"),
        digest_mapping.get("algorithm"),
        digest_mapping.get("status"),
        digest_mapping.get("value"),
        digest_mapping.get("scope"),
    )


def _seed_governed_v1_case_protections(
    root: Path,
    artifacts: list[ProtectedArtifact],
    errors: list[str],
    *,
    label: str,
) -> None:
    """Protect each reviewed case locator even when its manifest binding is damaged."""

    for binding in GOVERNED_V1_CASE_BINDINGS:
        if any(
            artifact.owner_manifest == GOVERNED_V1_MANIFEST_LOCATOR
            and artifact.locator == binding.locator
            and artifact.binding_key == binding.binding_key
            for artifact in artifacts
        ):
            continue
        resolved, path_errors = _safe_repository_path(
            root,
            binding.locator,
            must_exist=True,
            required_prefix=STUDY_ARTIFACT_PREFIX,
        )
        errors.extend(f"{label}: {error}" for error in path_errors)
        if resolved is None:
            continue
        artifacts.append(
            ProtectedArtifact(
                kind="CASE_SOURCE",
                locator=binding.locator,
                resolved_path=resolved,
                owner_manifest=GOVERNED_V1_MANIFEST_LOCATOR,
                study_id=str(GOVERNED_V1_TAXONOMY_KEY[0]),
                study_record_id=str(GOVERNED_V1_TAXONOMY_KEY[1]),
                record_version=int(GOVERNED_V1_TAXONOMY_KEY[2]),
                artifact_id=binding.artifact_id,
                source_role_or_analysis_id=binding.role,
                binding_key=binding.binding_key,
                expected_sha256=binding.digest_value,
            )
        )


def _binding_key(value: Any) -> Any:
    if isinstance(value, Mapping):
        return tuple(sorted((key, _binding_key(item)) for key, item in value.items()))
    if isinstance(value, list):
        return tuple(_binding_key(item) for item in value)
    return value


def _inventory_case_namespaces(
    root: Path,
    artifacts: list[ProtectedArtifact],
) -> list[str]:
    """Reject undeclared or aliased entries without opening any case body."""

    errors: list[str] = []
    declared_by_parent: dict[Path, set[Path]] = defaultdict(set)
    for artifact in artifacts:
        declared_by_parent[artifact.resolved_path.parent].add(artifact.resolved_path)

    observed_inodes: dict[tuple[int, int], Path] = {}
    for parent, declared in sorted(declared_by_parent.items()):
        try:
            parent_relative = parent.relative_to(root).as_posix()
        except ValueError:
            errors.append(f"protected case namespace escapes repository: {parent}")
            continue
        try:
            with os.scandir(parent) as entries:
                for entry in entries:
                    child = parent / entry.name
                    child_relative = child.relative_to(root).as_posix()
                    if child not in declared:
                        errors.append(
                            "protected case namespace contains an undeclared entry: "
                            f"{child_relative}"
                        )
                        continue
                    try:
                        metadata = entry.stat(follow_symlinks=False)
                    except OSError as exc:
                        errors.append(
                            f"cannot inspect protected case artifact {child_relative}: {exc}"
                        )
                        continue
                    if entry.is_symlink():
                        errors.append(
                            f"protected case artifact is a symlink: {child_relative}"
                        )
                        continue
                    if not stat.S_ISREG(metadata.st_mode):
                        errors.append(
                            f"protected case artifact is not a regular file: {child_relative}"
                        )
                        continue
                    if metadata.st_nlink != 1:
                        errors.append(
                            "protected case artifact has an aliasing hard-link count "
                            f"of {metadata.st_nlink}: {child_relative}"
                        )
                    inode_key = (metadata.st_dev, metadata.st_ino)
                    previous = observed_inodes.get(inode_key)
                    if previous is not None and previous != child:
                        errors.append(
                            "protected case artifacts alias one inode: "
                            f"{previous.relative_to(root).as_posix()}, {child_relative}"
                        )
                    observed_inodes[inode_key] = child
        except FileNotFoundError:
            errors.append(f"protected case namespace is missing: {parent_relative}")
        except NotADirectoryError:
            errors.append(
                f"protected case namespace is not a directory: {parent_relative}"
            )
        except OSError as exc:
            errors.append(f"cannot inventory protected case namespace {parent_relative}: {exc}")
    return errors


def _inventory_output_namespaces(
    root: Path,
    artifacts: list[ProtectedArtifact],
) -> list[str]:
    """Reject undeclared entries in any materialized planned-output parent."""

    errors: list[str] = []
    declared_by_parent: dict[Path, set[Path]] = defaultdict(set)
    for artifact in artifacts:
        declared_by_parent[artifact.resolved_path.parent].add(artifact.resolved_path)

    for parent, declared in sorted(declared_by_parent.items()):
        try:
            metadata = os.lstat(parent)
        except FileNotFoundError:
            continue
        except OSError as exc:
            errors.append(f"cannot inspect planned-output namespace {parent}: {exc}")
            continue
        parent_relative = parent.relative_to(root).as_posix()
        if stat.S_ISLNK(metadata.st_mode) or not stat.S_ISDIR(metadata.st_mode):
            errors.append(
                f"planned-output namespace is not a plain directory: {parent_relative}"
            )
            continue
        try:
            with os.scandir(parent) as entries:
                for entry in entries:
                    child = parent / entry.name
                    if child not in declared:
                        errors.append(
                            "planned-output namespace contains an undeclared entry: "
                            f"{child.relative_to(root).as_posix()}"
                        )
        except OSError as exc:
            errors.append(
                f"cannot inventory planned-output namespace {parent_relative}: {exc}"
            )
    return errors


def _inventory_repository_symlinks(root: Path) -> list[str]:
    """Reject repository symlinks structurally without opening their targets."""

    errors: list[str] = []
    ignored = {".git", ".venv", "__pycache__"}
    for current_value, directory_names, file_names in os.walk(
        root,
        topdown=True,
        followlinks=False,
    ):
        current = Path(current_value)
        retained_directories: list[str] = []
        for name in directory_names:
            candidate = current / name
            if name in ignored:
                continue
            try:
                metadata = os.lstat(candidate)
            except OSError as exc:
                errors.append(f"cannot inspect repository entry {candidate}: {exc}")
                continue
            if stat.S_ISLNK(metadata.st_mode):
                errors.append(
                    "repository symlink is forbidden during case-access containment: "
                    f"{candidate.relative_to(root).as_posix()}"
                )
                continue
            retained_directories.append(name)
        directory_names[:] = retained_directories

        for name in file_names:
            candidate = current / name
            try:
                metadata = os.lstat(candidate)
            except OSError as exc:
                errors.append(f"cannot inspect repository entry {candidate}: {exc}")
                continue
            if stat.S_ISLNK(metadata.st_mode):
                errors.append(
                    "repository symlink is forbidden during case-access containment: "
                    f"{candidate.relative_to(root).as_posix()}"
                )
    return errors


def _validate_lineage(studies: list[IndexedTaxonomyStudy]) -> list[str]:
    errors: list[str] = []
    study_ids_by_record_id: dict[Any, set[Any]] = defaultdict(set)
    for study in studies:
        study_ids_by_record_id[study.record_id].add(study.study_id)
    for record_id, study_ids in study_ids_by_record_id.items():
        if len(study_ids) > 1:
            errors.append(
                f"taxonomy record {record_id!r} claims multiple study IDs: "
                + ", ".join(sorted(repr(value) for value in study_ids))
            )

    grouped: dict[Any, list[IndexedTaxonomyStudy]] = defaultdict(list)
    for study in studies:
        grouped[study.study_id].append(study)

    for study_id, lineage in grouped.items():
        label = f"taxonomy study lineage {study_id!r}"
        if not isinstance(study_id, str) or not study_id:
            errors.append("indexed taxonomy study is missing a stable study_id")
            continue
        versions = [study.record_version for study in lineage]
        if any(not isinstance(version, int) or version < 1 for version in versions):
            errors.append(f"{label}: every record_version must be a positive integer")
            continue
        if len(versions) != len(set(versions)):
            errors.append(f"{label}: duplicate record_version")
            continue
        by_version = {study.record_version: study for study in lineage}
        active = [study for study in lineage if study.registry_status == "ACTIVE"]
        if len(active) != 1:
            errors.append(f"{label}: exactly one registry version must be ACTIVE")
        elif active[0].record_version != max(versions):
            errors.append(f"{label}: ACTIVE version must be the chain head")
        elif active[0].manifest.get("record_status") != "FROZEN":
            errors.append(f"{label}: ACTIVE taxonomy study must be FROZEN")

        for version in sorted(versions):
            current = by_version[version]
            if version == 1:
                amendment = current.manifest.get("amendment")
                if not isinstance(amendment, Mapping) or any(
                    (
                        amendment.get("kind") != "INITIAL",
                        amendment.get("supersedes_record_version") is not None,
                        amendment.get("supersedes_artifact_digest") is not None,
                    )
                ):
                    errors.append(f"{label}: version 1 lacks an INITIAL amendment")
                continue
            previous = by_version.get(version - 1)
            if previous is None:
                errors.append(f"{label}: version {version} skips its direct predecessor")
                continue
            amendment = current.manifest.get("amendment")
            if not isinstance(amendment, Mapping):
                errors.append(f"{label}: version {version} lacks amendment metadata")
                continue
            if amendment.get("kind") != "SUPERSEDING_RECORD":
                errors.append(f"{label}: version {version} is not a superseding record")
            if amendment.get("supersedes_record_version") != version - 1:
                errors.append(f"{label}: version {version} names the wrong predecessor")
            supersedes_digest = amendment.get("supersedes_artifact_digest")
            prior_value = (
                supersedes_digest.get("value")
                if isinstance(supersedes_digest, Mapping)
                else None
            )
            if prior_value != previous.registry_digest:
                errors.append(f"{label}: version {version} predecessor digest mismatch")
            if previous.registry_status != "SUPERSEDED":
                errors.append(
                    f"{label}: predecessor version {version - 1} must be SUPERSEDED"
                )
            for field in ("study_record_id", "study_id"):
                if current.manifest.get(field) != previous.manifest.get(field):
                    errors.append(f"{label}: version {version} changes {field}")
            if _binding_key(current.manifest.get("subject")) != _binding_key(
                previous.manifest.get("subject")
            ):
                errors.append(f"{label}: version {version} changes exact subject binding")
            current_profile = current.manifest.get("primary_method_profile")
            previous_profile = previous.manifest.get("primary_method_profile")
            if isinstance(current_profile, Mapping) and isinstance(previous_profile, Mapping):
                for field in ("profile_kind", "profile_series"):
                    if current_profile.get(field) != previous_profile.get(field):
                        errors.append(
                            f"{label}: version {version} changes method-profile {field}"
                        )

            def output_locators(manifest: Mapping[str, Any]) -> set[Any]:
                analyses = manifest.get("analyses")
                if not isinstance(analyses, list):
                    return set()
                return {
                    output.get("locator")
                    for analysis in analyses
                    if isinstance(analysis, Mapping)
                    for output in [analysis.get("planned_output_artifact")]
                    if isinstance(output, Mapping)
                }

            reused = output_locators(current.manifest) & output_locators(
                previous.manifest
            )
            if reused:
                errors.append(
                    f"{label}: version {version} reuses predecessor output locators: "
                    + ", ".join(sorted(str(item) for item in reused))
                )
    return errors


def build_study_access_catalog(root: Path) -> StudyAccessCatalog:
    """Build the protected-artifact policy without opening protected bodies."""

    root = root.resolve()
    errors: list[str] = []
    case_artifacts: list[ProtectedArtifact] = []
    output_artifacts: list[ProtectedArtifact] = []
    taxonomy_studies: list[IndexedTaxonomyStudy] = []
    registry_path = root / STUDY_REGISTRY
    governed_footprint, footprint_errors = _governed_v1_footprint(root)
    errors.extend(footprint_errors)
    registry_present, registry_presence_errors = _repository_path_presence(
        root,
        STUDY_REGISTRY,
    )
    errors.extend(
        f"{STUDY_REGISTRY}: {error}" for error in registry_presence_errors
    )

    if not registry_present:
        if governed_footprint:
            errors.append(
                f"{STUDY_REGISTRY}: governed v1 taxonomy footprint exists but "
                "the authoritative registry is missing"
            )
            _seed_governed_v1_case_protections(
                root,
                case_artifacts,
                errors,
                label="governed v1 taxonomy fallback protection",
            )
        return StudyAccessCatalog(
            root,
            tuple(case_artifacts),
            (),
            (),
            tuple(errors),
        )
    if registry_presence_errors:
        return StudyAccessCatalog(root, (), (), (), tuple(errors))

    checked_registry_path, registry_path_errors = _safe_repository_path(
        root,
        STUDY_REGISTRY,
        must_exist=True,
    )
    if registry_path_errors or checked_registry_path is None:
        return StudyAccessCatalog(
            root,
            (),
            (),
            (),
            tuple(f"{STUDY_REGISTRY}: {error}" for error in registry_path_errors),
        )

    try:
        registry = _load_yaml_unique(root, registry_path)
    except CatalogLoadError as exc:
        return StudyAccessCatalog(root, (), (), (), (str(exc),))
    if not isinstance(registry, Mapping):
        return StudyAccessCatalog(
            root,
            (),
            (),
            (),
            (f"{STUDY_REGISTRY}: must be an object",),
        )
    if registry.get("registry_type") != "foundational_study_registry":
        errors.append(f"{STUDY_REGISTRY}: wrong registry_type")
    entries = registry.get("entries")
    if not isinstance(entries, list):
        return StudyAccessCatalog(
            root,
            (),
            (),
            (),
            tuple(errors + [f"{STUDY_REGISTRY}: entries must be a list"]),
        )

    governed_registry_signal = False
    governed_v1_seen = False
    for index, entry in enumerate(entries):
        label = f"{STUDY_REGISTRY}:entries/{index}"
        if not isinstance(entry, Mapping):
            errors.append(f"{label}: entry must be an object")
            continue
        if (
            entry.get("record_id") == GOVERNED_V1_TAXONOMY_KEY[1]
            or entry.get("artifact_path") == GOVERNED_V1_MANIFEST_LOCATOR
        ):
            governed_registry_signal = True
        manifest_locator = entry.get("artifact_path")
        manifest_path, path_errors = _safe_repository_path(
            root,
            manifest_locator,
            must_exist=True,
            required_prefix=CANONICAL_MANIFEST_PREFIX,
        )
        errors.extend(f"{label}: {error}" for error in path_errors)
        if manifest_path is None or path_errors:
            continue
        try:
            document, actual_manifest_digest = _load_json_bytes(root, manifest_path)
        except CatalogLoadError as exc:
            errors.append(str(exc))
            continue
        if not isinstance(document, Mapping):
            errors.append(f"{label}: indexed manifest must be an object")
            continue
        expected_digest = entry.get("artifact_digest")
        expected_value = (
            expected_digest.get("value")
            if isinstance(expected_digest, Mapping)
            else None
        )
        if not isinstance(expected_digest, Mapping):
            errors.append(f"{label}: registry artifact digest is missing")
        else:
            if expected_digest.get("algorithm") != "SHA-256":
                errors.append(f"{label}: registry digest algorithm must be SHA-256")
            if expected_digest.get("scope") != "RAW_FILE_BYTES":
                errors.append(f"{label}: registry digest scope must be RAW_FILE_BYTES")
            if not isinstance(expected_value, str) or not SHA256.fullmatch(expected_value):
                errors.append(f"{label}: registry digest must be a lowercase SHA-256")
        if expected_value != actual_manifest_digest:
            errors.append(f"{label}: canonical manifest raw-byte digest mismatch")
        if entry.get("artifact_type") != "foundational_study_manifest":
            errors.append(f"{label}: registry artifact_type is not a study manifest")
        if entry.get("schema_id") != "urn:lcmrp:schema:foundational-study-manifest:0.1.0":
            errors.append(f"{label}: registry schema_id is not the study-manifest schema")
        if entry.get("registry_status") not in {"ACTIVE", "SUPERSEDED"}:
            errors.append(f"{label}: taxonomy lineage status must be ACTIVE or SUPERSEDED")
        if document.get("artifact_type") != "foundational_study_manifest":
            errors.append(f"{label}: indexed artifact is not a study manifest")
        for field, actual in (
            ("study_record_id", entry.get("record_id")),
            ("record_version", entry.get("record_version")),
        ):
            if document.get(field) != actual:
                errors.append(f"{label}: indexed manifest {field} mismatch")

        document_identity = (
            document.get("study_id"),
            document.get("study_record_id"),
            document.get("record_version"),
        )
        is_governed_v1 = document_identity == GOVERNED_V1_TAXONOMY_KEY
        is_governed_taxonomy_lineage = (
            document_identity[:2] == GOVERNED_V1_TAXONOMY_LINEAGE_KEY
        )
        governed_v1_seen = governed_v1_seen or is_governed_v1
        profile = document.get("primary_method_profile")
        subject = document.get("subject")
        sources = document.get("sources")
        profile_case_signal = isinstance(profile, Mapping) and any(
            field in profile
            for field in (
                "positive_case_source_ids",
                "negative_case_source_ids",
            )
        )
        source_case_signal = isinstance(sources, list) and any(
            isinstance(source, Mapping)
            and (
                source.get("role") in CASE_ROLES
                or source.get("source_kind") == CASE_SOURCE_KIND
                or (
                    isinstance(source.get("provenance_artifact"), Mapping)
                    and source["provenance_artifact"].get("schema_id")
                    == CASE_SCHEMA_ID
                )
            )
            for source in sources
        )
        is_taxonomy = is_governed_taxonomy_lineage or (
            (
                isinstance(profile, Mapping)
                and profile.get("profile_kind") == TAXONOMY_PROFILE_KIND
            )
            or (
                isinstance(subject, Mapping)
                and subject.get("subject_kind") == TAXONOMY_SUBJECT_KIND
            )
            or profile_case_signal
            or source_case_signal
        )
        if not is_taxonomy:
            continue

        if not (
            isinstance(profile, Mapping)
            and profile.get("profile_kind") == TAXONOMY_PROFILE_KIND
            and isinstance(subject, Mapping)
            and subject.get("subject_kind") == TAXONOMY_SUBJECT_KIND
        ):
            errors.append(f"{label}: taxonomy subject/profile classification is inconsistent")

        study = IndexedTaxonomyStudy(
            registry_index=index,
            registry_status=str(entry.get("registry_status")),
            registry_digest=expected_value if isinstance(expected_value, str) else None,
            manifest_path=manifest_locator,
            manifest=document,
        )
        taxonomy_studies.append(study)
        study_id = document.get("study_id")
        record_id = document.get("study_record_id")
        version = document.get("record_version")
        identity_valid = (
            isinstance(study_id, str)
            and isinstance(record_id, str)
            and isinstance(version, int)
        )
        if not identity_valid:
            errors.append(f"{label}: taxonomy study identity is incomplete")
            continue
        governed_taxonomy_lineage = (
            study_id,
            record_id,
        ) == GOVERNED_V1_TAXONOMY_LINEAGE_KEY

        if not isinstance(sources, list):
            errors.append(f"{label}: taxonomy sources must be a list")
            sources = []

        profile_source_roles: dict[Any, str] = {}
        if isinstance(profile, Mapping):
            for field, expected_role in (
                ("positive_case_source_ids", "POSITIVE_CASES"),
                ("negative_case_source_ids", "NEGATIVE_CASES"),
            ):
                identifiers = profile.get(field)
                if not isinstance(identifiers, list):
                    errors.append(f"{label}: taxonomy profile {field} must be a list")
                    continue
                valid_identifiers = [
                    source_id
                    for source_id in identifiers
                    if isinstance(source_id, str) and source_id
                ]
                if not valid_identifiers:
                    case_polarity = expected_role.removesuffix("_CASES").lower()
                    errors.append(
                        f"{label}: taxonomy profile must declare a "
                        f"{case_polarity} case source"
                    )
                if len(valid_identifiers) != len(set(valid_identifiers)):
                    errors.append(f"{label}: taxonomy profile {field} contains duplicates")
                for source_id in identifiers:
                    if not isinstance(source_id, str) or not source_id:
                        errors.append(
                            f"{label}: taxonomy profile {field} entries must be strings"
                        )
                        continue
                    previous_role = profile_source_roles.get(source_id)
                    if previous_role is not None and previous_role != expected_role:
                        errors.append(
                            f"{label}: taxonomy profile source {source_id!r} has "
                            "conflicting positive/negative roles"
                        )
                    profile_source_roles[source_id] = expected_role

        seen_source_ids: set[Any] = set()
        seen_case_locators: set[str] = set()
        sources_by_id: dict[Any, Mapping[str, Any]] = {}
        candidate_source_ids: set[Any] = set()
        for source_index, source in enumerate(sources):
            source_label = f"{label}:sources/{source_index}"
            if not isinstance(source, Mapping):
                errors.append(f"{source_label}: source must be an object")
                continue
            source_id = source.get("source_id")
            valid_source_id = isinstance(source_id, str) and bool(source_id)
            if not valid_source_id:
                errors.append(f"{source_label}: source_id must be a non-empty string")
            else:
                if source_id in seen_source_ids:
                    errors.append(f"{source_label}: duplicate source_id")
                seen_source_ids.add(source_id)
                sources_by_id.setdefault(source_id, source)
            role = source.get("role")
            kind = source.get("source_kind")
            reference = source.get("provenance_artifact")
            schema_id = reference.get("schema_id") if isinstance(reference, Mapping) else None
            is_case_candidate = any(
                (
                    valid_source_id and source_id in profile_source_roles,
                    role in CASE_ROLES,
                    kind == CASE_SOURCE_KIND,
                    schema_id == CASE_SCHEMA_ID,
                )
            )
            if not is_case_candidate:
                continue
            if valid_source_id:
                candidate_source_ids.add(source_id)
            if role not in CASE_ROLES or kind != CASE_SOURCE_KIND:
                errors.append(f"{source_label}: case source kind and role disagree")
            expected_profile_role = profile_source_roles.get(source_id)
            if expected_profile_role is not None and role != expected_profile_role:
                errors.append(
                    f"{source_label}: profile expects role {expected_profile_role}"
                )
            if governed_taxonomy_lineage and schema_id != CASE_SCHEMA_ID:
                errors.append(
                    f"{source_label}: case source schema_id must be {CASE_SCHEMA_ID}"
                )
            if source.get("human_subjects_involved") is not False:
                errors.append(f"{source_label}: protected case source must be non-human")
            locator = reference.get("locator") if isinstance(reference, Mapping) else None
            resolved, locator_errors = _safe_repository_path(
                root,
                locator,
                must_exist=True,
                required_prefix=STUDY_ARTIFACT_PREFIX,
            )
            errors.extend(f"{source_label}: {error}" for error in locator_errors)
            digest_value, digest_errors = _digest_value(reference)
            errors.extend(f"{source_label}: {error}" for error in digest_errors)
            if isinstance(locator, str) and locator in seen_case_locators:
                errors.append(f"{source_label}: duplicate case locator in one manifest")
            if isinstance(locator, str):
                seen_case_locators.add(locator)
            if resolved is None or not isinstance(locator, str):
                continue
            case_artifacts.append(
                ProtectedArtifact(
                    kind="CASE_SOURCE",
                    locator=locator,
                    resolved_path=resolved,
                    owner_manifest=manifest_locator,
                    study_id=study_id,
                    study_record_id=record_id,
                    record_version=version,
                    artifact_id=(
                        str(reference.get("artifact_id"))
                        if isinstance(reference, Mapping)
                        else ""
                    ),
                    source_role_or_analysis_id=str(role),
                    binding_key=(
                        _artifact_binding_key(reference)
                        if isinstance(reference, Mapping)
                        else ()
                    ),
                    expected_sha256=digest_value,
                )
            )

        for source_id, expected_role in profile_source_roles.items():
            source = sources_by_id.get(source_id)
            if source is None:
                errors.append(
                    f"{label}: taxonomy profile source {source_id!r} is absent"
                )
                continue
            if source.get("role") != expected_role:
                errors.append(
                    f"{label}: taxonomy profile source {source_id!r} does not "
                    f"resolve to role {expected_role}"
                )
            if source.get("source_kind") != CASE_SOURCE_KIND:
                errors.append(
                    f"{label}: taxonomy profile source {source_id!r} is not a "
                    f"{CASE_SOURCE_KIND}"
                )

        governed_key = (study_id, record_id, version)
        if governed_key == GOVERNED_V1_TAXONOMY_KEY:
            if manifest_locator != GOVERNED_V1_MANIFEST_LOCATOR:
                errors.append(
                    f"{label}: governed v1 taxonomy manifest locator changed"
                )
            if expected_value != GOVERNED_V1_MANIFEST_DIGEST:
                errors.append(
                    f"{label}: governed v1 taxonomy registry digest changed"
                )
            if actual_manifest_digest != GOVERNED_V1_MANIFEST_DIGEST:
                errors.append(
                    f"{label}: governed v1 taxonomy manifest bytes changed"
                )

            expected_by_id = {
                binding.source_id: binding for binding in GOVERNED_V1_CASE_BINDINGS
            }
            if candidate_source_ids != set(expected_by_id):
                errors.append(
                    f"{label}: governed v1 taxonomy case-source identity set changed"
                )
            for governed_binding in GOVERNED_V1_CASE_BINDINGS:
                source = sources_by_id.get(governed_binding.source_id)
                reference = (
                    source.get("provenance_artifact")
                    if isinstance(source, Mapping)
                    else None
                )
                actual_binding_key = (
                    _artifact_binding_key(reference)
                    if isinstance(reference, Mapping)
                    else ()
                )
                if not (
                    isinstance(source, Mapping)
                    and source.get("source_kind") == governed_binding.source_kind
                    and source.get("role") == governed_binding.role
                    and source.get("human_subjects_involved") is False
                    and actual_binding_key == governed_binding.binding_key
                ):
                    errors.append(
                        f"{label}: governed v1 case binding changed for "
                        f"{governed_binding.source_id}"
                    )

                if not any(
                    artifact.owner_manifest == manifest_locator
                    and artifact.locator == governed_binding.locator
                    and artifact.binding_key == governed_binding.binding_key
                    for artifact in case_artifacts
                ):
                    governed_path, governed_path_errors = _safe_repository_path(
                        root,
                        governed_binding.locator,
                        must_exist=True,
                        required_prefix=STUDY_ARTIFACT_PREFIX,
                    )
                    errors.extend(
                        f"{label}: {error}" for error in governed_path_errors
                    )
                    if governed_path is not None:
                        case_artifacts.append(
                            ProtectedArtifact(
                                kind="CASE_SOURCE",
                                locator=governed_binding.locator,
                                resolved_path=governed_path,
                                owner_manifest=manifest_locator,
                                study_id=study_id,
                                study_record_id=record_id,
                                record_version=version,
                                artifact_id=governed_binding.artifact_id,
                                source_role_or_analysis_id=governed_binding.role,
                                binding_key=governed_binding.binding_key,
                                expected_sha256=governed_binding.digest_value,
                            )
                        )

        analyses = document.get("analyses")
        if not isinstance(analyses, list):
            errors.append(f"{label}: taxonomy analyses must be a list")
            analyses = []
        seen_outputs: set[str] = set()
        for analysis_index, analysis in enumerate(analyses):
            output_label = f"{label}:analyses/{analysis_index}/planned_output_artifact"
            reference = (
                analysis.get("planned_output_artifact")
                if isinstance(analysis, Mapping)
                else None
            )
            locator = reference.get("locator") if isinstance(reference, Mapping) else None
            resolved, locator_errors = _safe_repository_path(
                root,
                locator,
                must_exist=False,
                required_prefix=STUDY_ARTIFACT_PREFIX,
            )
            errors.extend(f"{output_label}: {error}" for error in locator_errors)
            digest = reference.get("digest") if isinstance(reference, Mapping) else None
            if not isinstance(digest, Mapping):
                errors.append(f"{output_label}: planned output digest is missing")
            elif digest.get("status") != "PENDING" or digest.get("value") is not None:
                errors.append(
                    f"{output_label}: planned output must remain PENDING "
                    "with a null digest"
                )
            if isinstance(locator, str) and locator in seen_outputs:
                errors.append(f"{output_label}: duplicate planned output locator")
            if isinstance(locator, str):
                seen_outputs.add(locator)
            if resolved is None or not isinstance(locator, str):
                continue
            if resolved.exists():
                errors.append(f"{output_label}: planned output exists before authorization")
            output_artifacts.append(
                ProtectedArtifact(
                    kind="PLANNED_OUTPUT",
                    locator=locator,
                    resolved_path=resolved,
                    owner_manifest=manifest_locator,
                    study_id=study_id,
                    study_record_id=record_id,
                    record_version=version,
                    artifact_id=(
                        str(reference.get("artifact_id"))
                        if isinstance(reference, Mapping)
                        else ""
                    ),
                    source_role_or_analysis_id=str(
                        analysis.get("analysis_id")
                        if isinstance(analysis, Mapping)
                        else ""
                    ),
                    binding_key=(
                        _artifact_binding_key(reference)
                        if isinstance(reference, Mapping)
                        else ()
                    ),
                    expected_sha256=None,
                )
            )

    governed_required = governed_footprint or governed_registry_signal
    if governed_required and not governed_v1_seen:
        errors.append(
            f"{STUDY_REGISTRY}: governed v1 taxonomy footprint or record is present "
            "without its exact reviewed v1 manifest binding"
        )
        _seed_governed_v1_case_protections(
            root,
            case_artifacts,
            errors,
            label="governed v1 taxonomy fallback protection",
        )
    if governed_required and not taxonomy_studies:
        errors.append(f"{STUDY_REGISTRY}: no indexed taxonomy study was found")
    errors.extend(_validate_lineage(taxonomy_studies))
    errors.extend(_inventory_repository_symlinks(root))

    errors.extend(_inventory_case_namespaces(root, case_artifacts))
    errors.extend(_inventory_output_namespaces(root, output_artifacts))
    case_parents = {artifact.resolved_path.parent for artifact in case_artifacts}
    output_parents = {artifact.resolved_path.parent for artifact in output_artifacts}
    for shared_parent in sorted(case_parents & output_parents):
        errors.append(
            "case and planned-output namespaces share a parent: "
            f"{shared_parent.relative_to(root).as_posix()}"
        )

    by_locator: dict[str, ProtectedArtifact] = {}
    by_resolved: dict[Path, ProtectedArtifact] = {}
    for artifact in case_artifacts + output_artifacts:
        previous_locator = by_locator.get(artifact.locator)
        if previous_locator is not None:
            if previous_locator.kind != artifact.kind:
                errors.append(
                    f"protected locator crosses case/output roles: {artifact.locator}"
                )
            elif artifact.kind == "PLANNED_OUTPUT":
                errors.append(
                    f"planned output locator is reused across taxonomy versions: {artifact.locator}"
                )
            elif previous_locator.binding_key != artifact.binding_key:
                errors.append(
                    f"protected case locator has divergent version bindings: {artifact.locator}"
                )
        else:
            by_locator[artifact.locator] = artifact
        previous_resolved = by_resolved.get(artifact.resolved_path)
        if previous_resolved is not None and previous_resolved.locator != artifact.locator:
            errors.append(
                "protected artifact locators alias the same resolved path: "
                f"{previous_resolved.locator}, {artifact.locator}"
            )
        else:
            by_resolved[artifact.resolved_path] = artifact

    return StudyAccessCatalog(
        root,
        tuple(case_artifacts),
        tuple(output_artifacts),
        tuple(taxonomy_studies),
        tuple(errors),
    )
