"""Terminate a child before it opens a protected taxonomy case/output body.

This module is loaded automatically when its directory leads ``PYTHONPATH``.
The gate is deliberately independent of repository validator code so a
regression in that validator cannot silently weaken the CI access boundary.
It guards standard Python startup and file APIs; it is not an operating-system
sandbox. Native syscalls, inherited file descriptors, and hostile code that
executes before this module remain outside what a Python audit hook can enforce.
Research layer: program infrastructure supporting Layer 1 — Foundational
Research. Evidence effect: none.
"""

from __future__ import annotations

import os
from pathlib import Path
import sys
import _thread
from typing import Any


ENVIRONMENT_VARIABLE = "LCMRP_PROTECTED_CASE_ROOTS"
PYTHON_PATH_VARIABLE = "PYTHONPATH"
PYTHON_HOME_VARIABLE = "PYTHONHOME"
PYTHON_NO_USER_SITE_VARIABLE = "PYTHONNOUSERSITE"
BLOCKED_EXIT_STATUS = 97
BLOCKED_MARKER = "LCMRP_CASE_ACCESS_BLOCKED:"
SUPPORT_DIRECTORY = Path(__file__).resolve().parent


def _terminate(
    message: str,
    path: Path | None = None,
    *,
    _write: Any = os.write,
    _exit: Any = os._exit,
) -> None:
    suffix = f" at {path}" if path is not None else ""
    marker = f"{BLOCKED_MARKER} {message}{suffix}\n".encode(
        "utf-8", errors="replace"
    )
    try:
        _write(2, marker)
    finally:
        _exit(BLOCKED_EXIT_STATUS)


def _absolute_path(
    value: str | bytes | os.PathLike[str] | os.PathLike[bytes],
    *,
    base: Path | None = None,
) -> Path:
    path = Path(os.fsdecode(os.fspath(value)))
    if not path.is_absolute():
        path = (base if base is not None else Path.cwd()) / path
    return Path(os.path.abspath(path))


def _canonical_path(value: str | bytes | os.PathLike[str] | os.PathLike[bytes]) -> Path:
    return Path(os.path.realpath(_absolute_path(value)))


def _configured_roots() -> tuple[Path, ...]:
    raw = os.environ.get(ENVIRONMENT_VARIABLE, "")
    return tuple(
        _canonical_path(value)
        for value in raw.split(os.pathsep)
        if value
    )


PROTECTED_ROOTS = _configured_roots()


def _normalize_propagation_environment() -> None:
    os.environ.pop(PYTHON_HOME_VARIABLE, None)
    os.environ[PYTHON_NO_USER_SITE_VARIABLE] = "1"
    os.environ[ENVIRONMENT_VARIABLE] = os.pathsep.join(
        str(path) for path in PROTECTED_ROOTS
    )
    existing = os.environ.get(PYTHON_PATH_VARIABLE, "")
    support_real = _canonical_path(SUPPORT_DIRECTORY)
    parts = [str(support_real)]
    for value in existing.split(os.pathsep):
        if not value or _canonical_path(value) == support_real:
            continue
        parts.append(value)
    os.environ[PYTHON_PATH_VARIABLE] = os.pathsep.join(parts)


def _path_identity(
    path: Path,
    *,
    follow_symlinks: bool = True,
    _stat: Any = os.stat,
    _terminate_guard: Any = _terminate,
) -> tuple[int, int] | None:
    try:
        metadata = _stat(path, follow_symlinks=follow_symlinks)
    except (FileNotFoundError, NotADirectoryError):
        return None
    except OSError as exc:
        _terminate_guard(
            f"cannot inspect protected filesystem metadata: {exc}",
            path,
        )
    return (metadata.st_dev, metadata.st_ino)


CURRENT_PYTHON_IDENTITY = _path_identity(Path(sys.executable))
if CURRENT_PYTHON_IDENTITY is None:
    _terminate("cannot establish the current Python interpreter identity")


def _collect_protected_identities(
    protected_roots: tuple[Path, ...],
    *,
    _identity_guard: Any = _path_identity,
    _scandir: Any = os.scandir,
    _terminate_guard: Any = _terminate,
) -> frozenset[tuple[int, int]]:
    identities: set[tuple[int, int]] = set()
    for root in protected_roots:
        for follow_symlinks in (False, True):
            identity = _identity_guard(
                root,
                follow_symlinks=follow_symlinks,
            )
            if identity is not None:
                identities.add(identity)
        if not root.is_dir():
            continue
        pending = [root]
        while pending:
            directory = pending.pop()
            try:
                with _scandir(directory) as entries:
                    for entry in entries:
                        entry_path = Path(entry.path)
                        for follow_symlinks in (False, True):
                            identity = _identity_guard(
                                entry_path,
                                follow_symlinks=follow_symlinks,
                            )
                            if identity is not None:
                                identities.add(identity)
                        try:
                            if entry.is_dir(follow_symlinks=False):
                                pending.append(entry_path)
                        except OSError as exc:
                            _terminate_guard(
                                f"cannot inspect protected directory metadata: {exc}",
                                entry_path,
                            )
            except (FileNotFoundError, NotADirectoryError):
                continue
            except OSError as exc:
                _terminate_guard(
                    f"cannot enumerate protected directory metadata: {exc}",
                    directory,
                )
    return frozenset(identities)


_normalize_propagation_environment()
PROTECTED_IDENTITIES = _collect_protected_identities(PROTECTED_ROOTS)


def _is_protected_path(
    path: Path,
    protected_roots: tuple[Path, ...] = PROTECTED_ROOTS,
) -> bool:
    return any(path == root or root in path.parents for root in protected_roots)


def _block_if_protected(
    value: str | bytes | os.PathLike[str] | os.PathLike[bytes] | Path,
    *,
    _protected_roots: tuple[Path, ...] = PROTECTED_ROOTS,
    _protected_identities: frozenset[tuple[int, int]] = PROTECTED_IDENTITIES,
    _terminate_guard: Any = _terminate,
    _collect_guard: Any = _collect_protected_identities,
) -> None:
    try:
        lexical = _absolute_path(value)
        canonical = Path(os.path.realpath(lexical))
    except (OSError, TypeError, ValueError):
        return
    if _is_protected_path(lexical, _protected_roots) or _is_protected_path(
        canonical,
        _protected_roots,
    ):
        _terminate_guard(
            "attempted to open protected taxonomy case/output bytes",
            canonical,
        )

    try:
        metadata = os.stat(lexical)
    except (FileNotFoundError, NotADirectoryError):
        return
    except OSError:
        return
    identity = (metadata.st_dev, metadata.st_ino)
    if identity in _protected_identities:
        _terminate_guard(
            "attempted to open a protected taxonomy case/output alias",
            lexical,
        )

    # A protected path can be atomically replaced after startup. Refresh only
    # for multiply linked candidates, which are the hard-link alias risk.
    if metadata.st_nlink > 1:
        refreshed = _collect_guard(_protected_roots)
        if identity in refreshed:
            _terminate_guard(
                "attempted to open a protected taxonomy case/output alias",
                lexical,
            )


def _text(value: object) -> str | None:
    if isinstance(value, (str, bytes, os.PathLike)):
        try:
            return os.fsdecode(os.fspath(value))
        except (OSError, TypeError, ValueError):
            return None
    return None


def _environment_value(environment: object, name: str) -> str | None:
    if not hasattr(environment, "get"):
        return None
    value = environment.get(name)  # type: ignore[union-attr]
    if value is None:
        value = environment.get(os.fsencode(name))  # type: ignore[union-attr]
    return _text(value)


def _root_value_preserves_protection(
    value: object,
    protected_roots: tuple[Path, ...] = PROTECTED_ROOTS,
) -> bool:
    raw = _text(value)
    if raw is None:
        return False
    try:
        configured = {
            _canonical_path(item)
            for item in raw.split(os.pathsep)
            if item
        }
    except (OSError, TypeError, ValueError):
        return False
    return set(protected_roots).issubset(configured)


def _python_path_preserves_hook(
    value: object,
    support_directory: Path = SUPPORT_DIRECTORY,
) -> bool:
    raw = _text(value)
    if raw is None:
        return False
    first = raw.split(os.pathsep, maxsplit=1)[0]
    if not first:
        return False
    try:
        return _canonical_path(first) == _canonical_path(support_directory)
    except (OSError, TypeError, ValueError):
        return False


def _environment_preserves_gate(
    environment: object,
    *,
    _environment_value_guard: Any = _environment_value,
    _root_guard: Any = _root_value_preserves_protection,
    _python_path_guard: Any = _python_path_preserves_hook,
) -> bool:
    if environment is None:
        return True
    if type(environment) is not dict:
        return False
    roots = _environment_value_guard(
        environment,
        ENVIRONMENT_VARIABLE,
    )
    python_path = _environment_value_guard(
        environment,
        PYTHON_PATH_VARIABLE,
    )
    python_home = _environment_value_guard(environment, PYTHON_HOME_VARIABLE)
    no_user_site = _environment_value_guard(
        environment,
        PYTHON_NO_USER_SITE_VARIABLE,
    )
    return (
        python_home in {None, ""}
        and no_user_site == "1"
        and _root_guard(roots)
        and _python_path_guard(python_path)
    )


def _argument_list(arguments: object) -> list[object]:
    if isinstance(arguments, (str, bytes, os.PathLike)):
        return [arguments]
    try:
        return list(arguments)  # type: ignore[arg-type]
    except TypeError:
        return []


def _executable_candidates(
    token: str,
    environment: object,
    cwd: object,
    *,
    _text_guard: Any = _text,
    _environment_value_guard: Any = _environment_value,
) -> list[Path]:
    cwd_text = _text_guard(cwd)
    base = _absolute_path(cwd_text) if cwd_text is not None else Path.cwd()
    has_directory = os.sep in token or (
        os.altsep is not None and os.altsep in token
    )
    if has_directory:
        return [_absolute_path(token, base=base)]

    if environment is None:
        path_value = os.environ.get("PATH", os.defpath)
    else:
        configured_path = _environment_value_guard(
            environment,
            "PATH",
        )
        path_value = os.defpath if configured_path is None else configured_path
    return [
        _absolute_path(Path(directory or base) / token, base=base)
        for directory in path_value.split(os.pathsep)
    ]


def _is_current_python_executable(
    arguments: object,
    executable: object,
    environment: object,
    cwd: object,
    *,
    _current_python_identity: tuple[int, int] = CURRENT_PYTHON_IDENTITY,
    _argument_guard: Any = _argument_list,
    _text_guard: Any = _text,
    _candidate_guard: Any = _executable_candidates,
) -> bool:
    values = _argument_guard(arguments)
    token = _text_guard(executable)
    if token is None and values:
        token = _text_guard(values[0])
    if token is None:
        return False
    for candidate in _candidate_guard(
        token,
        environment,
        cwd,
    ):
        try:
            metadata = os.stat(candidate)
        except (FileNotFoundError, NotADirectoryError):
            continue
        except OSError:
            return False
        return (metadata.st_dev, metadata.st_ino) == _current_python_identity
    return False


def _unsafe_python_option(
    arguments: object,
    *,
    _argument_guard: Any = _argument_list,
    _text_guard: Any = _text,
) -> str | None:
    values = _argument_guard(arguments)
    if not values:
        return None
    skip_value = False
    for value in values[1:]:
        token = _text_guard(value)
        if token is None:
            continue
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


def _process_event(
    event: str,
    arguments: tuple[object, ...],
    *,
    _python_guard: Any = _is_current_python_executable,
    _environment_guard: Any = _environment_preserves_gate,
    _option_guard: Any = _unsafe_python_option,
    _terminate_guard: Any = _terminate,
) -> None:
    if (
        event == "os.system"
        or event.startswith("os.startfile")
        or event.startswith("os.spawn")
    ):
        _terminate_guard(
            "non-Python or shell descendants are forbidden by this gate"
        )
    if event == "subprocess.Popen" and len(arguments) >= 4:
        executable, argv, cwd, environment = arguments[:4]
    elif event in {"os.exec", "os.posix_spawn"} and len(arguments) >= 3:
        executable, argv, environment = arguments[:3]
        cwd = None
    else:
        return
    if not _python_guard(
        argv,
        executable,
        environment,
        cwd,
    ):
        _terminate_guard(
            "non-Python or indirect descendants are forbidden by this gate"
        )
    if not _environment_guard(environment):
        _terminate_guard(
            "descendant environment removed taxonomy case protection"
        )
    option = _option_guard(argv)
    if option is not None:
        _terminate_guard(
            f"descendant Python option {option!r} disables gate startup"
        )


def _environment_event(
    event: str,
    arguments: tuple[object, ...],
    *,
    _text_guard: Any = _text,
    _root_guard: Any = _root_value_preserves_protection,
    _python_path_guard: Any = _python_path_preserves_hook,
    _terminate_guard: Any = _terminate,
) -> None:
    if event == "os.unsetenv" and arguments:
        name = _text_guard(arguments[0])
        if name in {
            ENVIRONMENT_VARIABLE,
            PYTHON_PATH_VARIABLE,
            PYTHON_NO_USER_SITE_VARIABLE,
        }:
            _terminate_guard(
                f"refusing to remove required environment variable {name}"
            )
    if event != "os.putenv" or len(arguments) < 2:
        return
    name = _text_guard(arguments[0])
    value = arguments[1]
    if name == PYTHON_HOME_VARIABLE and _text_guard(value) not in {None, ""}:
        _terminate_guard("refusing to set PYTHONHOME inside the guarded process")
    if (
        name == PYTHON_NO_USER_SITE_VARIABLE
        and _text_guard(value) != "1"
    ):
        _terminate_guard("refusing to enable the Python user site")
    if name == ENVIRONMENT_VARIABLE and not _root_guard(value):
        _terminate_guard("refusing to shrink protected taxonomy case roots")
    if name == PYTHON_PATH_VARIABLE and not _python_path_guard(value):
        _terminate_guard(
            "refusing to remove the taxonomy case startup hook"
        )


_ORIGINAL_OS_OPEN = os.open
_OPEN_MODULE = sys.modules.get(_ORIGINAL_OS_OPEN.__module__)
_APPROVED_RELATIVE_OPENS: dict[int, list[tuple[str, Path]]] = {}


def _directory_path_from_fd(directory_fd: int) -> Path:
    for namespace in ("/proc/self/fd", "/dev/fd"):
        try:
            target = os.readlink(f"{namespace}/{directory_fd}")
        except OSError:
            continue
        if target.endswith(" (deleted)"):
            break
        path = Path(target)
        if not path.is_absolute():
            path = Path(namespace) / path
        return Path(os.path.realpath(path))
    _terminate(
        "cannot resolve dir_fd metadata safely; refusing relative os.open"
    )
    raise AssertionError("unreachable")


def _open_target(
    path: str | bytes | os.PathLike[str] | os.PathLike[bytes],
    directory_fd: int | None,
) -> tuple[Path, bool, str]:
    raw = Path(os.fsdecode(os.fspath(path)))
    relative = not raw.is_absolute()
    if relative and directory_fd is not None:
        target = _absolute_path(raw, base=_directory_path_from_fd(directory_fd))
    else:
        target = _absolute_path(raw)
    return target, relative, os.fsdecode(os.fspath(path))


def _guarded_os_open(
    path: str | bytes | os.PathLike[str] | os.PathLike[bytes],
    flags: int,
    mode: int = 0o777,
    *,
    dir_fd: int | None = None,
) -> int:
    target, relative, token = _open_target(path, dir_fd)
    _block_if_protected(target)
    if not relative:
        return _ORIGINAL_OS_OPEN(path, flags, mode, dir_fd=dir_fd)

    thread_id = _thread.get_ident()
    approvals = _APPROVED_RELATIVE_OPENS.setdefault(thread_id, [])
    approval = (token, target)
    approvals.append(approval)
    try:
        return _ORIGINAL_OS_OPEN(path, flags, mode, dir_fd=dir_fd)
    finally:
        current = _APPROVED_RELATIVE_OPENS.get(thread_id)
        if current and current[-1] == approval:
            current.pop()
        if current == []:
            _APPROVED_RELATIVE_OPENS.pop(thread_id, None)


def _approved_relative_open(candidate: object) -> Path | None:
    token = _text(candidate)
    if token is None:
        return None
    approvals = _APPROVED_RELATIVE_OPENS.get(_thread.get_ident())
    if not approvals or approvals[-1][0] != token:
        return None
    _token, target = approvals.pop()
    if not approvals:
        _APPROVED_RELATIVE_OPENS.pop(_thread.get_ident(), None)
    return target


def _forbidden_process_primitive(*_args: object, **_kwargs: object) -> int:
    _terminate(
        "direct fork/spawn primitives are forbidden; use a guarded Python subprocess"
    )
    raise AssertionError("unreachable")


def _audit(
    event: str,
    arguments: tuple[object, ...],
    *,
    _enabled: bool = bool(PROTECTED_ROOTS),
    _environment_guard: Any = _environment_event,
    _process_guard: Any = _process_event,
    _approval_guard: Any = _approved_relative_open,
    _terminate_guard: Any = _terminate,
    _block_guard: Any = _block_if_protected,
) -> None:
    if not _enabled:
        return
    _environment_guard(event, arguments)
    _process_guard(event, arguments)
    if event != "open" or not arguments:
        return
    candidate = arguments[0]
    if isinstance(candidate, int) or not isinstance(
        candidate,
        (str, bytes, os.PathLike),
    ):
        return
    mode = arguments[1] if len(arguments) > 1 else ""
    try:
        relative = not Path(os.fsdecode(os.fspath(candidate))).is_absolute()
    except (OSError, TypeError, ValueError):
        relative = False
    if mode is None and relative:
        approved_target = _approval_guard(candidate)
        if approved_target is None:
            _terminate_guard(
                "unmediated relative os.open could bypass dir_fd protection"
            )
        _block_guard(approved_target)
        return
    _block_guard(candidate)


if PROTECTED_ROOTS:
    sys.addaudithook(_audit)
    os.open = _guarded_os_open
    if (
        _OPEN_MODULE is not None
        and getattr(_OPEN_MODULE, "open", None) is _ORIGINAL_OS_OPEN
    ):
        setattr(_OPEN_MODULE, "open", _guarded_os_open)
    for _process_name in (
        "fork",
        "forkpty",
        "spawnl",
        "spawnle",
        "spawnlp",
        "spawnlpe",
        "spawnv",
        "spawnve",
        "spawnvp",
        "spawnvpe",
    ):
        _original_process_primitive = getattr(os, _process_name, None)
        if _original_process_primitive is None:
            continue
        setattr(os, _process_name, _forbidden_process_primitive)
        _owner = sys.modules.get(
            getattr(_original_process_primitive, "__module__", "")
        )
        if (
            _owner is not None
            and getattr(_owner, _process_name, None) is _original_process_primitive
        ):
            setattr(_owner, _process_name, _forbidden_process_primitive)
