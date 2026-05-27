"""Agent detection and configuration registry.

Detects which AI coding agents are installed globally (home directory)
or locally (project directory), and provides metadata for smart installation.

To add a new agent, append an AgentConfig to AGENT_CONFIGS with:
  - name: display name
  - config_dir: project-level config directory
  - home_paths: paths under ~/ that indicate global installation
  - cwd_paths: paths under ./ that indicate project-level presence
  - file_patterns: file patterns this agent owns (for discovery filtering)
  - init_files: dict of {relative_path: content} to create when initializing
"""

from dataclasses import dataclass, field
from pathlib import Path


@dataclass(frozen=True)
class AgentConfig:
    """Configuration for a known AI coding agent.

    To register a new agent, create an AgentConfig and add it to AGENT_CONFIGS.
    """

    name: str
    config_dir: str
    home_paths: tuple[str, ...] = ()
    cwd_paths: tuple[str, ...] = ()
    file_patterns: tuple[str, ...] = ()
    # Files to create when initializing this agent in a project.
    # Keys are relative paths, values are default file contents.
    init_files: dict[str, str] = field(default_factory=dict)


AGENT_CONFIGS: list[AgentConfig] = [
    AgentConfig(
        name="Claude Code",
        config_dir=".claude",
        home_paths=(".claude",),
        cwd_paths=(".claude",),
        file_patterns=(
            ".claude/CLAUDE.md",
            ".claude/settings.json",
            ".claude/commands/",
        ),
        init_files={
            ".claude/CLAUDE.md": "# Project Guidelines\n\nAdd your Claude Code instructions here.\n",
        },
    ),
    AgentConfig(
        name="Cursor",
        config_dir=".cursor",
        home_paths=(".cursor/extensions", ".cursor/argv.json"),
        cwd_paths=(".cursor",),
        file_patterns=(
            ".cursor/rules",
            ".cursor/rules/",
        ),
        init_files={
            ".cursor/rules": "# Cursor Rules\n\nAdd your Cursor rules here.\n",
        },
    ),
    AgentConfig(
        name="GitHub Copilot",
        config_dir=".github",
        home_paths=(".copilot/config.json", ".copilot"),
        cwd_paths=(".github/copilot-instructions.md", ".github/agents"),
        file_patterns=(
            ".github/copilot-instructions.md",
            ".github/copilot-setup-steps.yml",
            ".github/agents/",
        ),
        init_files={
            ".github/copilot-instructions.md": "# Copilot Instructions\n\nAdd your GitHub Copilot instructions here.\n",
        },
    ),
    AgentConfig(
        name="Windsurf",
        config_dir=".windsurf",
        home_paths=(
            ".codeium/windsurf/config.json",
            ".codeium/windsurf/argv.json",
            ".codeium/windsurf",
        ),
        cwd_paths=(".windsurf",),
        file_patterns=(".windsurfrules",),
        init_files={
            ".windsurfrules": "# Windsurf Rules\n\nAdd your Windsurf rules here.\n",
        },
    ),
    AgentConfig(
        name="Codeium",
        config_dir=".codeium",
        home_paths=(".codeium",),
        cwd_paths=(".codeium",),
        file_patterns=(".codeium/instructions.md",),
        init_files={
            ".codeium/instructions.md": "# Codeium Instructions\n\nAdd your Codeium instructions here.\n",
        },
    ),
    AgentConfig(
        name="Continue.dev",
        config_dir=".continue",
        home_paths=(".continue",),
        cwd_paths=(".continue",),
        file_patterns=(
            ".continue/instructions.md",
            ".continue/config.json",
        ),
        init_files={
            ".continue/instructions.md": "# Continue.dev Instructions\n\nAdd your Continue.dev instructions here.\n",
        },
    ),
    AgentConfig(
        name="Codex",
        config_dir=".codex",
        home_paths=(".codex/config.json", ".codex/settings.json", ".codex"),
        cwd_paths=(".codex",),
        file_patterns=(),
        init_files={
            ".codex/instructions.md": "# Codex Instructions\n\nAdd your Codex instructions here.\n",
        },
    ),
    AgentConfig(
        name="Gemini CLI",
        config_dir=".gemini",
        home_paths=(".gemini",),
        cwd_paths=(".gemini",),
        file_patterns=(),
        init_files={
            ".gemini/instructions.md": "# Gemini CLI Instructions\n\nAdd your Gemini CLI instructions here.\n",
        },
    ),
    AgentConfig(
        name="OpenCode",
        config_dir=".opencode",
        home_paths=(".config/opencode", ".opencode"),
        cwd_paths=(".opencode",),
        file_patterns=(),
        init_files={
            ".opencode/instructions.md": "# OpenCode Instructions\n\nAdd your OpenCode instructions here.\n",
        },
    ),
    AgentConfig(
        name="Goose",
        config_dir=".goose",
        home_paths=(".config/goose",),
        cwd_paths=(".goose",),
        file_patterns=(),
        init_files={
            ".goosehints": "# Goose Hints\n\nAdd your Goose hints here.\n",
        },
    ),
    AgentConfig(
        name="Cline",
        config_dir=".cline",
        home_paths=(".cline/settings.json", ".cline"),
        cwd_paths=(".cline",),
        file_patterns=(
            ".clinerules",
            ".clinerules/",
        ),
        init_files={
            ".clinerules": "# Cline Rules\n\nAdd your Cline rules here.\n",
        },
    ),
    AgentConfig(
        name="Roo Code",
        config_dir=".roo",
        home_paths=(".roo",),
        cwd_paths=(".roo",),
        file_patterns=(".roo/",),
        init_files={
            ".roo/instructions.md": "# Roo Code Instructions\n\nAdd your Roo Code instructions here.\n",
        },
    ),
    AgentConfig(
        name="Kilo Code",
        config_dir=".kilocode",
        home_paths=(".kilocode",),
        cwd_paths=(".kilocode",),
        file_patterns=(),
        init_files={
            ".kilocode/instructions.md": "# Kilo Code Instructions\n\nAdd your Kilo Code instructions here.\n",
        },
    ),
    AgentConfig(
        name="Kiro CLI",
        config_dir=".kiro",
        home_paths=(".kiro",),
        cwd_paths=(".kiro",),
        file_patterns=(),
        init_files={
            ".kiro/instructions.md": "# Kiro Instructions\n\nAdd your Kiro instructions here.\n",
        },
    ),
    AgentConfig(
        name="Aider",
        config_dir=".",
        home_paths=(".aider.conf.yml",),
        cwd_paths=(".aider.conf.yml",),
        file_patterns=(
            ".aider.conf.yml",
            ".aiderignore",
        ),
        init_files={
            ".aider.conf.yml": "# Aider Configuration\n# See https://aider.chat/docs/config.html\n",
        },
    ),
    AgentConfig(
        name="Junie",
        config_dir=".junie",
        home_paths=(".junie",),
        cwd_paths=(".junie",),
        file_patterns=(".junie/",),
        init_files={
            ".junie/guidelines.md": "# Junie Guidelines\n\nAdd your Junie guidelines here.\n",
        },
    ),
    AgentConfig(
        name="Amp",
        config_dir=".amp",
        home_paths=(".config/amp",),
        cwd_paths=(".amp",),
        file_patterns=(),
        init_files={
            ".amp/instructions.md": "# Amp Instructions\n\nAdd your Amp instructions here.\n",
        },
    ),
    AgentConfig(
        name="Trae",
        config_dir=".trae",
        home_paths=(".trae",),
        cwd_paths=(".trae",),
        file_patterns=(),
        init_files={
            ".trae/instructions.md": "# Trae Instructions\n\nAdd your Trae instructions here.\n",
        },
    ),
    AgentConfig(
        name="Augment",
        config_dir=".augment",
        home_paths=(".augment",),
        cwd_paths=(".augment",),
        file_patterns=(),
        init_files={
            ".augment/instructions.md": "# Augment Instructions\n\nAdd your Augment instructions here.\n",
        },
    ),
    AgentConfig(
        name="Kimi CLI",
        config_dir=".kimi",
        home_paths=(".kimi/kimi.json", ".kimi/config.toml", ".kimi"),
        cwd_paths=(".kimi",),
        file_patterns=(),
        init_files={
            ".kimi/instructions.md": "# Kimi Instructions\n\nAdd your Kimi instructions here.\n",
        },
    ),
]

# Files that are agent-agnostic and always installed
UNIVERSAL_PATTERNS: tuple[str, ...] = ("AGENTS.md",)


def detect_agent_globally(config: AgentConfig) -> bool:
    """Check if an agent is installed globally (home directory)."""
    home = Path.home()
    return any((home / p).exists() for p in config.home_paths)


def detect_agent_in_project(config: AgentConfig, project_dir: Path | None = None) -> bool:
    """Check if an agent is configured in a project directory."""
    cwd = project_dir or Path.cwd()
    return any((cwd / p).exists() for p in config.cwd_paths)


def detect_agent(config: AgentConfig, project_dir: Path | None = None) -> bool:
    """Check if an agent is detected globally OR in the project."""
    return detect_agent_globally(config) or detect_agent_in_project(config, project_dir)


def get_detected_agents(
    location: str = "both",
    project_dir: Path | None = None,
) -> list[AgentConfig]:
    """Get all detected agents.

    Args:
        location: "global" (home only), "project" (cwd only), or "both"
        project_dir: project directory to check (defaults to cwd)
    """
    results = []
    for config in AGENT_CONFIGS:
        if location == "global":
            detected = detect_agent_globally(config)
        elif location == "project":
            detected = detect_agent_in_project(config, project_dir)
        else:
            detected = detect_agent(config, project_dir)
        if detected:
            results.append(config)
    return results


def identify_agent_for_file(file_path: str) -> AgentConfig | None:
    """Identify which agent owns a given file path.

    Returns the AgentConfig if a match is found, None for universal files.
    """
    normalized = file_path.replace("\\", "/")

    for config in AGENT_CONFIGS:
        for pattern in config.file_patterns:
            if pattern.endswith("/"):
                # Directory prefix match
                if normalized.startswith(pattern) or normalized + "/" == pattern:
                    return config
            else:
                # Exact file match
                if normalized == pattern:
                    return config

    return None


def is_universal_file(file_path: str) -> bool:
    """Check if a file is agent-agnostic (always installed)."""
    normalized = file_path.replace("\\", "/")
    return normalized in UNIVERSAL_PATTERNS


def get_agent_by_name(name: str) -> AgentConfig | None:
    """Find an agent config by name (case-insensitive)."""
    lower = name.lower()
    for config in AGENT_CONFIGS:
        if config.name.lower() == lower:
            return config
    return None


def initialize_agent(config: AgentConfig, project_dir: Path) -> list[str]:
    """Create initial config files for an agent in the project directory.

    Returns list of created file paths (relative).
    Skips files that already exist.
    """
    created: list[str] = []
    for rel_path, content in config.init_files.items():
        target = project_dir / rel_path
        if target.exists():
            continue
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")
        created.append(rel_path)
    return created
