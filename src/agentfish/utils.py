"""Utility functions for agentfish."""

import os
from pathlib import Path

from rich.console import Console

console = Console()
err_console = Console(stderr=True)


def is_safe_path(base: Path, target: Path) -> bool:
    """Ensure target path doesn't escape base via traversal or symlinks."""
    try:
        resolved_base = base.resolve()
        resolved_target = target.resolve()
        return str(resolved_target).startswith(str(resolved_base))
    except (OSError, ValueError):
        return False


def validate_file_path(path: str) -> bool:
    """Validate that a relative path doesn't contain traversal attacks."""
    parts = Path(path).parts
    return ".." not in parts and not any(os.sep == p for p in parts)


def derive_thing_name(source: str) -> str:
    """Derive a short name from a repo source reference.

    Examples:
        owner/repo -> repo
        https://github.com/owner/repo -> repo
        https://dev.azure.com/org/project/_git/repo -> repo
    """
    source = source.rstrip("/")
    if "/_git/" in source:
        return source.split("/_git/")[-1].split("#")[0]
    return source.split("/")[-1].split("#")[0]
