"""Tests for agent detection and identification."""

from pathlib import Path

from agentfish.agents import (
    AGENT_CONFIGS,
    UNIVERSAL_PATTERNS,
    AgentConfig,
    detect_agent_globally,
    detect_agent_in_project,
    get_agent_by_name,
    get_detected_agents,
    identify_agent_for_file,
    initialize_agent,
    is_universal_file,
)


def test_agent_configs_not_empty():
    """Agent configs registry should have entries."""
    assert len(AGENT_CONFIGS) >= 18


def test_all_agents_have_names():
    """Every agent config must have a name."""
    for config in AGENT_CONFIGS:
        assert config.name, f"Agent config missing name: {config}"


def test_identify_claude_files():
    """Claude Code files should map to Claude Code agent."""
    agent = identify_agent_for_file("CLAUDE.md")
    assert agent is not None
    assert agent.name == "Claude Code"

    agent = identify_agent_for_file(".claude/settings.json")
    assert agent is not None
    assert agent.name == "Claude Code"

    agent = identify_agent_for_file(".claude/commands/test.md")
    assert agent is not None
    assert agent.name == "Claude Code"

    agent = identify_agent_for_file(".claude/rules/my-rule.md")
    assert agent is not None
    assert agent.name == "Claude Code"


def test_identify_cursor_files():
    """Cursor files should map to Cursor agent."""
    agent = identify_agent_for_file(".cursorrules")
    assert agent is not None
    assert agent.name == "Cursor"

    agent = identify_agent_for_file(".cursor/rules/python.mdc")
    assert agent is not None
    assert agent.name == "Cursor"


def test_identify_copilot_files():
    """GitHub Copilot files should map to GitHub Copilot agent."""
    agent = identify_agent_for_file(".github/copilot-instructions.md")
    assert agent is not None
    assert agent.name == "GitHub Copilot"

    agent = identify_agent_for_file(".github/agents/Review.md")
    assert agent is not None
    assert agent.name == "GitHub Copilot"


def test_identify_cline_files():
    """Cline files should map to Cline agent."""
    agent = identify_agent_for_file(".clinerules/project.md")
    assert agent is not None
    assert agent.name == "Cline"


def test_identify_aider_files():
    """Aider files should map to Aider agent."""
    agent = identify_agent_for_file(".aider.conf.yml")
    assert agent is not None
    assert agent.name == "Aider"

    agent = identify_agent_for_file(".aiderignore")
    assert agent is not None
    assert agent.name == "Aider"


def test_universal_file():
    """AGENTS.md is agent-agnostic."""
    assert is_universal_file("AGENTS.md") is True
    assert is_universal_file(".claude/CLAUDE.md") is False


def test_identify_unknown_file_returns_none():
    """Unknown files should return None."""
    agent = identify_agent_for_file("random/file.txt")
    assert agent is None


def test_detect_agent_globally_missing(tmp_path, monkeypatch):
    """Agent not installed globally should not be detected."""
    monkeypatch.setattr(Path, "home", lambda: tmp_path)
    config = AgentConfig(
        name="Test Agent",
        config_dir=".test",
        home_paths=(".test/config.json",),
        cwd_paths=(),
    )
    assert detect_agent_globally(config) is False


def test_detect_agent_globally_found(tmp_path, monkeypatch):
    """Agent installed globally should be detected."""
    monkeypatch.setattr(Path, "home", lambda: tmp_path)
    (tmp_path / ".test").mkdir()
    (tmp_path / ".test" / "config.json").write_text("{}")
    config = AgentConfig(
        name="Test Agent",
        config_dir=".test",
        home_paths=(".test/config.json",),
        cwd_paths=(),
    )
    assert detect_agent_globally(config) is True


def test_detect_agent_in_project(tmp_path):
    """Agent configured in project should be detected."""
    (tmp_path / ".claude").mkdir()
    config = AgentConfig(
        name="Claude Code",
        config_dir=".claude",
        home_paths=(),
        cwd_paths=(".claude",),
    )
    assert detect_agent_in_project(config, tmp_path) is True


def test_detect_agent_in_project_missing(tmp_path):
    """Agent not configured in project should not be detected."""
    config = AgentConfig(
        name="Claude Code",
        config_dir=".claude",
        home_paths=(),
        cwd_paths=(".claude",),
    )
    assert detect_agent_in_project(config, tmp_path) is False


def test_get_detected_agents_project(tmp_path):
    """Should detect agents present in the project directory."""
    (tmp_path / ".claude").mkdir()
    (tmp_path / ".cursor").mkdir()
    detected = get_detected_agents(location="project", project_dir=tmp_path)
    names = {a.name for a in detected}
    assert "Claude Code" in names
    assert "Cursor" in names


def test_get_agent_by_name():
    """Should find agents by name (case-insensitive)."""
    agent = get_agent_by_name("Claude Code")
    assert agent is not None
    assert agent.name == "Claude Code"

    agent = get_agent_by_name("claude code")
    assert agent is not None
    assert agent.name == "Claude Code"

    assert get_agent_by_name("NonExistent Agent") is None


def test_all_agents_have_init_files():
    """Every agent should have init_files defined for initialization."""
    for config in AGENT_CONFIGS:
        assert config.init_files, f"{config.name} has no init_files"


def test_initialize_agent_creates_files(tmp_path):
    """initialize_agent should create config files in the target directory."""
    agent = get_agent_by_name("Claude Code")
    assert agent is not None
    created = initialize_agent(agent, tmp_path)
    assert len(created) > 0
    assert "CLAUDE.md" in created
    assert (tmp_path / "CLAUDE.md").exists()
    assert ".claude/settings.json" in created
    assert (tmp_path / ".claude" / "settings.json").exists()


def test_initialize_agent_skips_existing(tmp_path):
    """initialize_agent should skip files that already exist."""
    agent = get_agent_by_name("Claude Code")
    assert agent is not None
    # Pre-create both init files
    (tmp_path / "CLAUDE.md").write_text("existing content")
    (tmp_path / ".claude").mkdir()
    (tmp_path / ".claude" / "settings.json").write_text("{}")

    created = initialize_agent(agent, tmp_path)
    assert len(created) == 0
    # Original content should be preserved
    assert (tmp_path / "CLAUDE.md").read_text() == "existing content"


def test_initialize_agent_makes_detectable(tmp_path):
    """After initialization, the agent should be detectable in the project."""
    agent = get_agent_by_name("GitHub Copilot")
    assert agent is not None
    assert detect_agent_in_project(agent, tmp_path) is False

    initialize_agent(agent, tmp_path)
    assert detect_agent_in_project(agent, tmp_path) is True


def test_identify_windsurf_files():
    """Windsurf files should map to Windsurf agent."""
    agent = identify_agent_for_file(".windsurf/rules/project.md")
    assert agent is not None
    assert agent.name == "Windsurf"

    agent = identify_agent_for_file(".windsurfrules")
    assert agent is not None
    assert agent.name == "Windsurf"


def test_identify_gemini_files():
    """Gemini CLI files should map to Gemini CLI agent."""
    agent = identify_agent_for_file("GEMINI.md")
    assert agent is not None
    assert agent.name == "Gemini CLI"

    agent = identify_agent_for_file(".gemini/settings.json")
    assert agent is not None
    assert agent.name == "Gemini CLI"


def test_identify_roo_code_files():
    """Roo Code files should map to Roo Code agent."""
    agent = identify_agent_for_file(".roo/rules/project.md")
    assert agent is not None
    assert agent.name == "Roo Code"

    agent = identify_agent_for_file(".roorules")
    assert agent is not None
    assert agent.name == "Roo Code"


def test_identify_codex_files():
    """Codex files should map to Codex agent."""
    agent = identify_agent_for_file(".codex/config.toml")
    assert agent is not None
    assert agent.name == "Codex"


def test_identify_opencode_files():
    """OpenCode files should map to OpenCode agent."""
    agent = identify_agent_for_file("opencode.json")
    assert agent is not None
    assert agent.name == "OpenCode"


def test_identify_augment_files():
    """Augment files should map to Augment agent."""
    agent = identify_agent_for_file(".augment/rules/coding-style.md")
    assert agent is not None
    assert agent.name == "Augment"


def test_identify_kiro_files():
    """Kiro files should map to Kiro agent."""
    agent = identify_agent_for_file(".kiro/steering/product.md")
    assert agent is not None
    assert agent.name == "Kiro"


def test_kimi_removed():
    """Kimi CLI was removed (no real config system exists)."""
    assert get_agent_by_name("Kimi CLI") is None


def test_all_init_files_make_agent_detectable(tmp_path):
    """Initializing any agent should make it detectable in the project."""
    for config in AGENT_CONFIGS:
        project = tmp_path / config.name.replace(" ", "_")
        project.mkdir()
        initialize_agent(config, project)
        assert detect_agent_in_project(config, project), (
            f"{config.name}: init_files do not create detectable paths "
            f"(cwd_paths={config.cwd_paths})"
        )
