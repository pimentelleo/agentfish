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
    # --- Claude Code (Anthropic) ---
    # Docs: https://docs.anthropic.com/en/docs/claude-code/settings
    # Docs: https://docs.anthropic.com/en/docs/claude-code/memory
    AgentConfig(
        name="Claude Code",
        config_dir=".claude",
        home_paths=(".claude",),
        cwd_paths=(".claude", "CLAUDE.md"),
        file_patterns=(
            "CLAUDE.md",
            "CLAUDE.local.md",
            ".claude/",
        ),
        init_files={
            "CLAUDE.md": (
                "# Project Guidelines\n"
                "\n"
                "## Build & Test Commands\n"
                "\n"
                "- Install: `npm install`\n"
                "- Test: `npm test`\n"
                "- Lint: `npm run lint`\n"
                "- Build: `npm run build`\n"
                "\n"
                "## Architecture\n"
                "\n"
                "Describe your project structure here.\n"
                "\n"
                "## Coding Standards\n"
                "\n"
                "Add your coding conventions here.\n"
            ),
            ".claude/settings.json": (
                "{\n"
                '  "$schema": "https://json.schemastore.org/claude-code-settings.json",\n'
                '  "permissions": {\n'
                '    "allow": [],\n'
                '    "deny": []\n'
                "  }\n"
                "}\n"
            ),
        },
    ),
    # --- Cursor ---
    # Docs: https://cursor.com/docs/rules
    # Format: .mdc (Markdown with YAML frontmatter) in .cursor/rules/
    AgentConfig(
        name="Cursor",
        config_dir=".cursor",
        home_paths=(".cursor/extensions", ".cursor/argv.json"),
        cwd_paths=(".cursor", ".cursorrules"),
        file_patterns=(
            ".cursor/rules/",
            ".cursorrules",
        ),
        init_files={
            ".cursor/rules/project.mdc": (
                "---\n"
                "description: Project-wide coding standards\n"
                "globs: \n"
                "alwaysApply: true\n"
                "---\n"
                "\n"
                "# Project Guidelines\n"
                "\n"
                "Add your project-wide rules here.\n"
            ),
        },
    ),
    # --- GitHub Copilot ---
    # Docs: https://docs.github.com/en/copilot/customizing-copilot
    AgentConfig(
        name="GitHub Copilot",
        config_dir=".github",
        home_paths=(".copilot", ".copilot/agents"),
        cwd_paths=(
            ".github/copilot-instructions.md",
            ".github/agents",
            ".github/instructions",
        ),
        file_patterns=(
            ".github/copilot-instructions.md",
            ".github/copilot-setup-steps.yml",
            ".github/agents/",
            ".github/instructions/",
            ".github/prompts/",
        ),
        init_files={
            ".github/copilot-instructions.md": (
                "# Copilot Instructions\n"
                "\n"
                "## Project Overview\n"
                "\n"
                "Describe what this project does.\n"
                "\n"
                "## Coding Standards\n"
                "\n"
                "Add your coding conventions here.\n"
                "\n"
                "## Build & Validation Commands\n"
                "\n"
                "- Install: `npm install`\n"
                "- Test: `npm test`\n"
                "- Lint: `npm run lint`\n"
            ),
        },
    ),
    # --- Windsurf (Codeium) ---
    # Docs: https://docs.windsurf.com/plugins/cascade/memories
    # Rules: .windsurf/rules/*.md (workspace), .windsurf/workflows/*.md
    AgentConfig(
        name="Windsurf",
        config_dir=".windsurf",
        home_paths=(
            ".codeium/windsurf",
            ".codeium/windsurf/config.json",
        ),
        cwd_paths=(".windsurf", ".windsurfrules"),
        file_patterns=(
            ".windsurf/rules/",
            ".windsurf/workflows/",
            ".windsurfrules",
        ),
        init_files={
            ".windsurf/rules/project.md": (
                "# Project Guidelines\n"
                "\n"
                "Add your Windsurf Cascade rules here.\n"
                "\n"
                "## Code Style\n"
                "\n"
                "- Describe your coding conventions\n"
                "\n"
                "## Architecture\n"
                "\n"
                "- Describe your project structure\n"
            ),
        },
    ),
    # --- Continue.dev ---
    # Docs: https://docs.continue.dev/customize/deep-dives/rules
    # Config: .continue/config.yaml (v1 schema), rules in .continue/rules/*.md
    AgentConfig(
        name="Continue.dev",
        config_dir=".continue",
        home_paths=(".continue",),
        cwd_paths=(".continue",),
        file_patterns=(
            ".continue/config.yaml",
            ".continue/config.json",
            ".continue/rules/",
        ),
        init_files={
            ".continue/rules/project.md": (
                "---\n"
                "name: Project Guidelines\n"
                "globs: []\n"
                "alwaysApply: true\n"
                "---\n"
                "\n"
                "Add your Continue.dev rules here.\n"
            ),
        },
    ),
    # --- Codex (OpenAI CLI) ---
    # Docs: https://developers.openai.com/codex
    # Config: .codex/config.toml (TOML), instructions via AGENTS.md
    AgentConfig(
        name="Codex",
        config_dir=".codex",
        home_paths=(".codex", ".codex/config.toml"),
        cwd_paths=(".codex",),
        file_patterns=(
            ".codex/config.toml",
        ),
        init_files={
            ".codex/config.toml": (
                "# Codex CLI Configuration\n"
                "# See https://developers.openai.com/codex/config-basic\n"
                "\n"
                '# model = "codex-1"\n'
                '# approval_policy = "on-request"\n'
            ),
        },
    ),
    # --- Gemini CLI (Google) ---
    # Docs: https://github.com/google-gemini/gemini-cli
    # Context: GEMINI.md (project + global), settings: .gemini/settings.json
    AgentConfig(
        name="Gemini CLI",
        config_dir=".gemini",
        home_paths=(".gemini", ".gemini/settings.json"),
        cwd_paths=(".gemini", "GEMINI.md"),
        file_patterns=(
            "GEMINI.md",
            ".gemini/settings.json",
            ".geminiignore",
        ),
        init_files={
            "GEMINI.md": (
                "# Project Guidelines\n"
                "\n"
                "## General Instructions\n"
                "\n"
                "Add your Gemini CLI instructions here.\n"
                "\n"
                "## Coding Style\n"
                "\n"
                "Describe your conventions.\n"
            ),
        },
    ),
    # --- OpenCode ---
    # Docs: https://opencode.ai/docs/config
    # Config: opencode.json (project root), .opencode/ directory
    AgentConfig(
        name="OpenCode",
        config_dir=".opencode",
        home_paths=(".config/opencode", ".config/opencode/opencode.json"),
        cwd_paths=(".opencode", "opencode.json"),
        file_patterns=(
            "opencode.json",
            ".opencode/agents/",
            ".opencode/commands/",
        ),
        init_files={
            "opencode.json": (
                "{\n"
                '  "$schema": "https://opencode.ai/config.json"\n'
                "}\n"
            ),
        },
    ),
    # --- Goose (AAIF / Linux Foundation) ---
    # Docs: https://goose-docs.ai/docs/guides/context-engineering/using-goosehints
    # Context: .goosehints (supports @file imports), global: ~/.config/goose/
    AgentConfig(
        name="Goose",
        config_dir=".",
        home_paths=(".config/goose", ".config/goose/config.yaml"),
        cwd_paths=(".goosehints",),
        file_patterns=(
            ".goosehints",
        ),
        init_files={
            ".goosehints": (
                "# Project context for Goose\n"
                "\n"
                "Describe your project and conventions here.\n"
                "\n"
                "# Reference other files with @:\n"
                "# @README.md\n"
                "# @docs/contributing.md\n"
            ),
        },
    ),
    # --- Cline ---
    # Docs: https://github.com/cline/cline (docs/customization/cline-rules.mdx)
    # Rules: .clinerules/ directory (.md/.txt, optional YAML frontmatter with paths:)
    # Global: ~/Documents/Cline/Rules/ (Windows/macOS/Linux)
    AgentConfig(
        name="Cline",
        config_dir=".clinerules",
        home_paths=("Documents/Cline/Rules",),
        cwd_paths=(".clinerules",),
        file_patterns=(
            ".clinerules/",
        ),
        init_files={
            ".clinerules/project.md": (
                "# Project Guidelines\n"
                "\n"
                "## Code Style\n"
                "\n"
                "Add your coding conventions here.\n"
                "\n"
                "## Testing\n"
                "\n"
                "Describe your testing requirements.\n"
            ),
        },
    ),
    # --- Roo Code ---
    # Docs: https://docs.roocode.com/features/custom-instructions
    # Rules: .roo/rules/ (all modes), .roo/rules-{mode}/ (mode-specific)
    # Global: ~/.roo/rules/
    AgentConfig(
        name="Roo Code",
        config_dir=".roo",
        home_paths=(".roo", ".roo/rules"),
        cwd_paths=(".roo", ".roorules"),
        file_patterns=(
            ".roo/rules/",
            ".roo/rules-code/",
            ".roo/rules-architect/",
            ".roo/rules-debug/",
            ".roorules",
        ),
        init_files={
            ".roo/rules/project.md": (
                "# Project Guidelines\n"
                "\n"
                "Add your Roo Code rules here.\n"
                "These apply to all modes (code, architect, debug).\n"
            ),
        },
    ),
    # --- Kilo Code ---
    # Docs: https://kilocode.dev (fork of Roo Code)
    # Config: kilo.jsonc (project manifest), .kilo/rules/*.md
    # Global: ~/.config/kilo/kilo.jsonc
    AgentConfig(
        name="Kilo Code",
        config_dir=".kilo",
        home_paths=(".config/kilo", ".kilocode"),
        cwd_paths=(".kilo", "kilo.jsonc", ".kilocode"),
        file_patterns=(
            "kilo.jsonc",
            ".kilo/rules/",
            ".kilo/agents/",
        ),
        init_files={
            ".kilo/rules/project.md": (
                "# Project Guidelines\n"
                "\n"
                "Add your Kilo Code rules here.\n"
            ),
        },
    ),
    # --- Kiro (AWS) ---
    # Docs: https://kiro.dev
    # Steering: .kiro/steering/*.md, specs: .kiro/specs/, hooks: .kiro/hooks/
    AgentConfig(
        name="Kiro",
        config_dir=".kiro",
        home_paths=(".kiro",),
        cwd_paths=(".kiro",),
        file_patterns=(
            ".kiro/steering/",
            ".kiro/specs/",
            ".kiro/hooks/",
        ),
        init_files={
            ".kiro/steering/product.md": (
                "# Product Guidelines\n"
                "\n"
                "Describe your product context and coding standards.\n"
            ),
        },
    ),
    # --- Aider ---
    # Docs: https://aider.chat/docs/config/aider_conf.html
    # Config: .aider.conf.yml (YAML, every CLI option is a key)
    # Ignore: .aiderignore (gitignore syntax)
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
            ".aider.conf.yml": (
                "# Aider Configuration\n"
                "# See https://aider.chat/docs/config/aider_conf.html\n"
                "\n"
                "# model: claude-sonnet-4-5\n"
                "# auto-commits: true\n"
                "# auto-lint: true\n"
                "# gitignore: true\n"
                "\n"
                "# Read-only context files:\n"
                "# read:\n"
                "#   - CONVENTIONS.md\n"
            ),
        },
    ),
    # --- Junie (JetBrains) ---
    # Docs: https://www.jetbrains.com/help/junie/
    # Guidelines: .junie/guidelines.md
    AgentConfig(
        name="Junie",
        config_dir=".junie",
        home_paths=(),
        cwd_paths=(".junie",),
        file_patterns=(
            ".junie/guidelines.md",
            ".junie/",
        ),
        init_files={
            ".junie/guidelines.md": (
                "# Project Guidelines for Junie\n"
                "\n"
                "## Tech Stack\n"
                "\n"
                "Describe your technologies here.\n"
                "\n"
                "## Code Style\n"
                "\n"
                "Add your coding conventions.\n"
                "\n"
                "## Testing\n"
                "\n"
                "Describe testing requirements.\n"
            ),
        },
    ),
    # --- Amp (Sourcegraph) ---
    # Docs: https://ampcode.com/manual
    # Context: AGENTS.md (hierarchical, cwd + parents + subtrees)
    # Global: ~/.config/amp/AGENTS.md
    AgentConfig(
        name="Amp",
        config_dir=".",
        home_paths=(".config/amp", ".config/amp/AGENTS.md"),
        cwd_paths=("AGENTS.md",),
        file_patterns=(),
        init_files={
            "AGENTS.md": (
                "# Project Guidelines\n"
                "\n"
                "## Build & Test\n"
                "\n"
                "- Build: `npm run build`\n"
                "- Test: `npm test`\n"
                "- Lint: `npm run lint`\n"
                "\n"
                "## Architecture\n"
                "\n"
                "Describe your project structure.\n"
                "\n"
                "## Coding Standards\n"
                "\n"
                "Add your conventions here.\n"
            ),
        },
    ),
    # --- Trae (ByteDance) ---
    # Docs: https://docs.trae.ai/ide/rules-for-ai
    # Rules: .trae/rules/*.md (project), global via IDE settings
    AgentConfig(
        name="Trae",
        config_dir=".trae",
        home_paths=(".trae",),
        cwd_paths=(".trae",),
        file_patterns=(
            ".trae/rules/",
        ),
        init_files={
            ".trae/rules/project.md": (
                "# Project Rules\n"
                "\n"
                "## Code Style\n"
                "\n"
                "Add your coding conventions here.\n"
                "\n"
                "## Architecture\n"
                "\n"
                "Describe your project structure.\n"
            ),
        },
    ),
    # --- Augment (Augment Code) ---
    # Docs: https://docs.augmentcode.com/cli/rules
    # Rules: .augment/rules/*.md (YAML frontmatter: type, description)
    # Global: ~/.augment/rules/*.md
    # Also reads: CLAUDE.md, AGENTS.md from project root
    AgentConfig(
        name="Augment",
        config_dir=".augment",
        home_paths=(".augment", ".augment/rules"),
        cwd_paths=(".augment",),
        file_patterns=(
            ".augment/rules/",
        ),
        init_files={
            ".augment/rules/project.md": (
                "---\n"
                "type: always_apply\n"
                "---\n"
                "\n"
                "# Project Guidelines\n"
                "\n"
                "Add your Augment rules here.\n"
            ),
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
