"""Parse repo references and clone repositories."""

import re
import shutil
import subprocess
import tempfile
from dataclasses import dataclass
from pathlib import Path


@dataclass
class RepoRef:
    """Parsed repository reference."""

    url: str
    branch: str | None = None
    name: str | None = None

    @property
    def display(self) -> str:
        s = self.url
        if self.branch:
            s += f"#{self.branch}"
        return s


def parse_repo_ref(ref: str) -> RepoRef:
    """Parse a repository reference into a RepoRef.

    Supported formats:
        owner/repo              -> https://github.com/owner/repo.git
        owner/repo#branch       -> https://github.com/owner/repo.git (branch)
        https://github.com/...  -> used as-is
        https://dev.azure.com/org/project/_git/repo  -> used as-is
        https://gitlab.com/...  -> used as-is
        git@host:owner/repo.git -> used as-is
    """
    branch: str | None = None

    if "#" in ref and not ref.startswith("http"):
        ref, branch = ref.rsplit("#", 1)
    elif "#" in ref and ref.startswith("http"):
        url_part, branch = ref.rsplit("#", 1)
        ref = url_part

    if ref.startswith(("https://", "http://", "git@", "ssh://")):
        url = ref
    elif re.match(r"^[^/]+/[^/]+$", ref):
        url = f"https://github.com/{ref}.git"
    else:
        url = ref

    name = _derive_name(url)
    return RepoRef(url=url, branch=branch, name=name)


def _derive_name(url: str) -> str:
    """Extract a short name from a git URL."""
    url = url.rstrip("/")
    if "/_git/" in url:
        name = url.split("/_git/")[-1]
    else:
        name = url.split("/")[-1]
    return name.removesuffix(".git")


def clone_repo(ref: RepoRef, target_dir: Path | None = None) -> Path:
    """Shallow clone a repository to a temporary or specified directory.

    Returns the path to the cloned repository.
    """
    if target_dir is None:
        target_dir = Path(tempfile.mkdtemp(prefix="agentfish_"))

    cmd = ["git", "clone", "--depth=1", "--single-branch"]
    if ref.branch:
        cmd += ["--branch", ref.branch]
    cmd += [ref.url, str(target_dir)]

    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        stderr = result.stderr.strip()
        raise RuntimeError(f"git clone failed: {stderr}")
    return target_dir


def cleanup_clone(clone_dir: Path) -> None:
    """Remove a cloned repository directory."""
    shutil.rmtree(clone_dir, ignore_errors=True)
