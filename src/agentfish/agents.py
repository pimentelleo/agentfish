"""Agent detection and configuration registry.

Detects which AI coding agents are installed globally (home directory)
or locally (project directory), and provides metadata for smart installation.
Ported from skillfish's agent detection logic.
"""

from dataclasses import dataclass, field
from pathlib import Path


@dataclass(frozen=True)
class AgentConfig:
    """Configuration for a known AI coding agent."""

    name: str
    # Where agent-specific config files live in a project (e.g. ".claude")
    config_dir: str
    # Paths to check in ~/ for global detection
    home_paths: tuple[str, ...] = ()
    # Paths to check in ./ for project detection
    cwd_paths: tuple[str, ...] = ()
    # File patterns this agent owns (for discovery filtering)
    file_patterns: tuple[str, ...] = ()


AGENT_CONFIGS: list[AgentConfig] = [
    # === Primary Agents ===
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
    ),
    AgentConfig(
        name="Codeium",
        config_dir=".codeium",
        home_paths=(".codeium",),
        cwd_paths=(".codeium",),
        file_patterns=(".codeium/instructions.md",),
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
    ),
    AgentConfig(
        name="Codex",
        config_dir=".codex",
        home_paths=(".codex/config.json", ".codex/settings.json", ".codex"),
        cwd_paths=(".codex",),
        file_patterns=(),
    ),
    AgentConfig(
        name="Gemini CLI",
        config_dir=".gemini",
        home_paths=(".gemini",),
        cwd_paths=(".gemini",),
        file_patterns=(),
    ),
    AgentConfig(
        name="OpenCode",
        config_dir=".opencode",
        home_paths=(".config/opencode", ".opencode"),
        cwd_paths=(".opencode",),
        file_patterns=(),
    ),
    AgentConfig(
        name="Goose",
        config_dir=".goose",
        home_paths=(".config/goose",),
        cwd_paths=(".goose",),
        file_patterns=(),
    ),
    # === Secondary Agents ===
    AgentConfig(
        name="Cline",
        config_dir=".cline",
        home_paths=(".cline/settings.json", ".cline"),
        cwd_paths=(".cline",),
        file_patterns=(
            ".clinerules",
            ".clinerules/",
        ),
    ),
    AgentConfig(
        name="Roo Code",
        config_dir=".roo",
        home_paths=(".roo",),
        cwd_paths=(".roo",),
        file_patterns=(".roo/",),
    ),
    AgentConfig(
        name="Kilo Code",
        config_dir=".kilocode",
        home_paths=(".kilocode",),
        cwd_paths=(".kilocode",),
        file_patterns=(),
    ),
    AgentConfig(
        name="Kiro CLI",
        config_dir=".kiro",
        home_paths=(".kiro",),
        cwd_paths=(".kiro",),
        file_patterns=(),
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
    ),
    AgentConfig(
        name="Junie",
        config_dir=".junie",
        home_paths=(".junie",),
        cwd_paths=(".junie",),
        file_patterns=(".junie/",),
    ),
    AgentConfig(
        name="Amp",
        config_dir=".agents",
        home_paths=(".config/amp",),
        cwd_paths=(".agents",),
        file_patterns=(),
    ),
    AgentConfig(
        name="Trae",
        config_dir=".trae",
        home_paths=(".trae",),
        cwd_paths=(".trae",),
        file_patterns=(),
    ),
    AgentConfig(
        name="Augment",
        config_dir=".augment",
        home_paths=(".augment",),
        cwd_paths=(".augment",),
        file_patterns=(),
    ),
    AgentConfig(
        name="Kimi CLI",
        config_dir=".kimi",
        home_paths=(".kimi/kimi.json", ".kimi/config.toml", ".kimi"),
        cwd_paths=(".kimi",),
        file_patterns=(),
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
