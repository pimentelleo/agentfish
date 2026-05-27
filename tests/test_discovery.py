"""Tests for agentfish discovery module."""

import tempfile
from pathlib import Path

from agentfish.discovery import discover_agent_files


def test_discover_claude_md():
    with tempfile.TemporaryDirectory() as tmp:
        d = Path(tmp)
        (d / "CLAUDE.md").write_text("# Claude instructions")
        result = discover_agent_files(d)
        assert "CLAUDE.md" in result


def test_discover_github_agents():
    with tempfile.TemporaryDirectory() as tmp:
        d = Path(tmp)
        (d / ".github" / "agents").mkdir(parents=True)
        (d / ".github" / "agents" / "Review.md").write_text("# Review agent")
        (d / ".github" / "copilot-instructions.md").write_text("# Copilot")
        result = discover_agent_files(d)
        assert ".github/agents/Review.md" in result
        assert ".github/copilot-instructions.md" in result


def test_discover_multiple_agents():
    with tempfile.TemporaryDirectory() as tmp:
        d = Path(tmp)
        # Cursor: .cursor/rules/*.mdc format
        (d / ".cursor" / "rules").mkdir(parents=True)
        (d / ".cursor" / "rules" / "project.mdc").write_text("---\nalwaysApply: true\n---\n")
        # Continue: .continue/config.yaml
        (d / ".continue").mkdir()
        (d / ".continue" / "config.yaml").write_text("name: test\n")
        # Goose: .goosehints
        (d / ".goosehints").write_text("# Hints")
        # Universal
        (d / "AGENTS.md").write_text("# Agents")
        result = discover_agent_files(d)
        assert ".cursor/rules/project.mdc" in result
        assert ".continue/config.yaml" in result
        assert ".goosehints" in result
        assert "AGENTS.md" in result


def test_discover_empty_dir():
    with tempfile.TemporaryDirectory() as tmp:
        result = discover_agent_files(Path(tmp))
        assert result == []


def test_discover_ignores_non_agent_files():
    with tempfile.TemporaryDirectory() as tmp:
        d = Path(tmp)
        (d / "README.md").write_text("# Readme")
        (d / "package.json").write_text("{}")
        result = discover_agent_files(d)
        assert result == []
