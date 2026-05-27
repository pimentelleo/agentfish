"""Tests for agentfish discovery module."""

import tempfile
from pathlib import Path

from agentfish.discovery import discover_agent_files


def test_discover_claude_md():
    with tempfile.TemporaryDirectory() as tmp:
        d = Path(tmp)
        (d / ".claude").mkdir()
        (d / ".claude" / "CLAUDE.md").write_text("# Claude instructions")
        result = discover_agent_files(d)
        assert ".claude/CLAUDE.md" in result


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
        (d / ".cursor").mkdir()
        (d / ".cursor" / "rules").write_text("cursor rules")
        (d / ".continue").mkdir()
        (d / ".continue" / "instructions.md").write_text("# Continue")
        (d / ".codeium").mkdir()
        (d / ".codeium" / "instructions.md").write_text("# Codeium")
        (d / "AGENTS.md").write_text("# Agents")
        result = discover_agent_files(d)
        assert ".cursor/rules" in result
        assert ".continue/instructions.md" in result
        assert ".codeium/instructions.md" in result
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
