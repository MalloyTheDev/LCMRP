#!/usr/bin/env python3
"""Run a direct Python command with a tripwire around opaque taxonomy artifacts.

The runner resolves the metadata-only study access catalog and filesystem
metadata needed to configure the child. It does not parse, hash, render, or
otherwise open any protected case body. Research layer: program infrastructure
supporting Layer 1 — Foundational Research. Evidence effect: none.
"""

from __future__ import annotations

import argparse
import os
from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]
SUPPORT_DIRECTORY = ROOT / "tests" / "support" / "no_case_access"
DEFAULT_PROTECTED_ROOT = (
    ROOT / "studies" / "foundational" / "m1-taxonomy-v1" / "cases"
)
ENVIRONMENT_VARIABLE = "LCMRP_PROTECTED_CASE_ROOTS"
BLOCKED_EXIT_STATUS = 97
BLOCKED_MARKER = "LCMRP_CASE_ACCESS_BLOCKED:"


class GateConfigurationError(RuntimeError):
    """The metadata-only protection policy could not be established."""


_BOOTSTRAP_AUDIT_INSTALLED = False


def _canonical_path(path: str | os.PathLike[str], *, base: Path) -> Path:
    candidate = Path(path)
    if not candidate.is_absolute():
        candidate = base / candidate
    return Path(os.path.realpath(candidate))


def _install_bootstrap_access_audit() -> None:
    """Deny all study-artifact body opens while protected paths are discovered."""

    global _BOOTSTRAP_AUDIT_INSTALLED
    if _BOOTSTRAP_AUDIT_INSTALLED:
        return
    study_tree = _canonical_path(
        ROOT / "studies" / "foundational",
        base=ROOT,
    )

    def audit(event: str, arguments: tuple[object, ...]) -> None:
        if event != "open" or not arguments:
            return
        candidate = arguments[0]
        if isinstance(candidate, int) or not isinstance(
            candidate,
            (str, bytes, os.PathLike),
        ):
            return
        try:
            path = _canonical_path(os.fsdecode(os.fspath(candidate)), base=Path.cwd())
        except (OSError, TypeError, ValueError):
            return
        if path == study_tree or study_tree in path.parents:
            raise GateConfigurationError(
                "catalog bootstrap attempted to open a foundational study "
                f"artifact body: {path}"
            )

    sys.addaudithook(audit)
    _BOOTSTRAP_AUDIT_INSTALLED = True


def _inherited_protected_roots() -> list[Path]:
    raw = os.environ.get(ENVIRONMENT_VARIABLE, "")
    return [
        _canonical_path(value, base=Path.cwd())
        for value in raw.split(os.pathsep)
        if value
    ]


def _catalog_protected_paths() -> list[Path]:
    """Return every indexed opaque artifact and namespace without body reads."""

    inserted_root = False
    if str(ROOT) not in sys.path:
        sys.path.insert(0, str(ROOT))
        inserted_root = True
    try:
        from tools.taxonomy_case_access import build_study_access_catalog

        catalog = build_study_access_catalog(ROOT)
    except Exception as exc:
        raise GateConfigurationError(
            f"taxonomy case-access catalog bootstrap failed: {exc}"
        ) from exc
    finally:
        if inserted_root:
            sys.path.remove(str(ROOT))

    if catalog.errors:
        raise GateConfigurationError(
            "taxonomy case-access catalog is unavailable: "
            + "; ".join(catalog.errors)
        )

    root_real = Path(os.path.realpath(ROOT))
    result: list[Path] = []
    protected_paths = [
        *(artifact.resolved_path for artifact in catalog.protected_artifacts),
        *catalog.protected_roots,
    ]
    for protected_path in protected_paths:
        candidate = _canonical_path(protected_path, base=ROOT)
        try:
            candidate.relative_to(root_real)
        except ValueError as exc:
            raise GateConfigurationError(
                "taxonomy case-access catalog path escapes the repository: "
                f"{protected_path}"
            ) from exc
        result.append(candidate)
    return result


def _deduplicated_paths(paths: list[Path]) -> tuple[Path, ...]:
    result: list[Path] = []
    seen: set[str] = set()
    for path in paths:
        key = os.path.normcase(str(path))
        if key in seen:
            continue
        seen.add(key)
        result.append(path)
    return tuple(result)


def _executable_candidates(token: str) -> list[Path]:
    has_directory = os.sep in token or (os.altsep is not None and os.altsep in token)
    if has_directory:
        return [_canonical_path(token, base=Path.cwd())]

    path_value = os.environ.get("PATH", os.defpath)
    return [
        _canonical_path(Path(directory or Path.cwd()) / token, base=Path.cwd())
        for directory in path_value.split(os.pathsep)
    ]


def _is_runner_python(token: str) -> bool:
    try:
        current = os.stat(sys.executable)
    except OSError:
        return False
    expected_identity = (current.st_dev, current.st_ino)
    for candidate in _executable_candidates(token):
        try:
            metadata = os.stat(candidate)
        except (FileNotFoundError, NotADirectoryError):
            continue
        except OSError:
            return False
        return (metadata.st_dev, metadata.st_ino) == expected_identity
    return False


def _python_command_index(command: list[str]) -> int | None:
    if command and _is_runner_python(command[0]):
        return 0
    return None


def _python_isolation_option(command: list[str]) -> str | None:
    position = _python_command_index(command)
    if position is None:
        return None
    skip_value = False
    for token in command[position + 1 :]:
        if skip_value:
            skip_value = False
            continue
        if token in {"-c", "-m", "--"} or not token.startswith("-"):
            break
        if token in {"-W", "-X"}:
            skip_value = True
            continue
        if token.startswith("--"):
            continue
        if any(flag in token[1:] for flag in ("S", "I", "E")):
            return token
    return None


def _blocked(message: str) -> int:
    marker = f"{BLOCKED_MARKER} {message}\n".encode("utf-8", errors="replace")
    os.write(2, marker)
    return BLOCKED_EXIT_STATUS


def main(argv: list[str] | None = None) -> int:
    _install_bootstrap_access_audit()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--protected-root",
        action="append",
        type=Path,
        default=[],
        help="file or directory the child must not open (repeatable and additive)",
    )
    parser.add_argument("command", nargs=argparse.REMAINDER)
    args = parser.parse_args(argv)

    command = list(args.command)
    if command[:1] == ["--"]:
        command = command[1:]
    if not command:
        parser.error("a command is required after --")

    python_position = _python_command_index(command)
    if python_position != 0:
        return _blocked(
            "the command must resolve to this runner's Python interpreter"
        )

    isolation_option = _python_isolation_option(command)
    if isolation_option is not None:
        return _blocked(
            f"refusing Python option {isolation_option!r}; it disables gate startup"
        )

    try:
        protected_roots = _deduplicated_paths(
            [
                _canonical_path(DEFAULT_PROTECTED_ROOT, base=ROOT),
                *_catalog_protected_paths(),
                *_inherited_protected_roots(),
                *(
                    _canonical_path(path, base=Path.cwd())
                    for path in args.protected_root
                ),
            ]
        )
    except (GateConfigurationError, OSError, TypeError, ValueError) as exc:
        return _blocked(f"cannot establish taxonomy case protection: {exc}")

    environment = os.environ.copy()
    environment.pop("PYTHONHOME", None)
    environment["PYTHONNOUSERSITE"] = "1"
    existing_python_path = environment.get("PYTHONPATH", "")
    support_real = Path(os.path.realpath(SUPPORT_DIRECTORY))
    python_path_parts = [str(support_real)]
    for value in existing_python_path.split(os.pathsep):
        if not value:
            continue
        if _canonical_path(value, base=Path.cwd()) == support_real:
            continue
        python_path_parts.append(value)
    environment["PYTHONPATH"] = os.pathsep.join(python_path_parts)
    environment[ENVIRONMENT_VARIABLE] = os.pathsep.join(
        str(path) for path in protected_roots
    )

    completed = subprocess.run(command, env=environment, check=False)
    return completed.returncode


if __name__ == "__main__":
    raise SystemExit(main())
