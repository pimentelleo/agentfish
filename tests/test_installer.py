"""Tests for agentfish installer module."""

import tempfile
from pathlib import Path
from unittest.mock import patch

from agentfish.installer import install_files


def test_install_files_basic():
    with tempfile.TemporaryDirectory() as src_tmp, tempfile.TemporaryDirectory() as dst_tmp:
        src = Path(src_tmp)
        dst = Path(dst_tmp)
        (src / ".claude").mkdir()
        (src / ".claude" / "CLAUDE.md").write_text("# Claude")
        (src / "AGENTS.md").write_text("# Agents")

        installed = install_files(
            [".claude/CLAUDE.md", "AGENTS.md"], src, dst, interactive=False
        )
        assert ".claude/CLAUDE.md" in installed
        assert "AGENTS.md" in installed
        assert (dst / ".claude" / "CLAUDE.md").read_text() == "# Claude"
        assert (dst / "AGENTS.md").read_text() == "# Agents"


def test_install_creates_parent_dirs():
    with tempfile.TemporaryDirectory() as src_tmp, tempfile.TemporaryDirectory() as dst_tmp:
        src = Path(src_tmp)
        dst = Path(dst_tmp)
        (src / ".github" / "agents").mkdir(parents=True)
        (src / ".github" / "agents" / "Review.md").write_text("# Review")

        installed = install_files(
            [".github/agents/Review.md"], src, dst, interactive=False
        )
        assert ".github/agents/Review.md" in installed
        assert (dst / ".github" / "agents" / "Review.md").exists()


def test_install_skips_traversal():
    with tempfile.TemporaryDirectory() as src_tmp, tempfile.TemporaryDirectory() as dst_tmp:
        src = Path(src_tmp)
        dst = Path(dst_tmp)

        installed = install_files(
            ["../etc/passwd"], src, dst, interactive=False
        )
        assert installed == []


def test_install_overwrites_non_interactive():
    with tempfile.TemporaryDirectory() as src_tmp, tempfile.TemporaryDirectory() as dst_tmp:
        src = Path(src_tmp)
        dst = Path(dst_tmp)
        (src / "AGENTS.md").write_text("new content")
        (dst / "AGENTS.md").write_text("old content")

        installed = install_files(["AGENTS.md"], src, dst, interactive=False)
        assert "AGENTS.md" in installed
        assert (dst / "AGENTS.md").read_text() == "new content"
