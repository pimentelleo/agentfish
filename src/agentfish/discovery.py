"""Auto-discover known AI agent configuration files in a directory."""

from pathlib import Path

AGENT_CONFIG_PATTERNS: list[str] = [
    # Universal
    "AGENTS.md",
    # Claude Code
    "CLAUDE.md",
    "CLAUDE.local.md",
    ".claude/**/*",
    # Cursor
    ".cursorrules",
    ".cursor/rules/**/*.mdc",
    # GitHub Copilot
    ".github/copilot-instructions.md",
    ".github/copilot-setup-steps.yml",
    ".github/agents/*.md",
    ".github/agents/*.agent.md",
    ".github/instructions/*.instructions.md",
    ".github/prompts/*.prompt.md",
    # Windsurf
    ".windsurfrules",
    ".windsurf/rules/**/*",
    ".windsurf/workflows/**/*",
    # Continue.dev
    ".continue/config.yaml",
    ".continue/config.json",
    ".continue/rules/**/*",
    # Codex
    ".codex/config.toml",
    # Gemini CLI
    "GEMINI.md",
    ".gemini/settings.json",
    ".geminiignore",
    # OpenCode
    "opencode.json",
    ".opencode/**/*",
    # Goose
    ".goosehints",
    # Cline
    ".clinerules/**/*",
    # Roo Code
    ".roo/**/*",
    ".roorules",
    # Kilo Code
    "kilo.jsonc",
    ".kilo/**/*",
    # Kiro
    ".kiro/**/*",
    # Aider
    ".aider.conf.yml",
    ".aiderignore",
    # Junie
    ".junie/**/*",
    # Amp (uses AGENTS.md — already covered)
    ".amprules",
    # Trae
    ".trae/rules/**/*",
    # Augment
    ".augment/rules/**/*",
    "augment-guidelines.md",
]


def discover_agent_files(repo_dir: Path) -> list[str]:
    """Discover all known agent config files in a directory.

    Returns relative paths (posix-style) of discovered files.
    """
    found: list[str] = []
    for pattern in AGENT_CONFIG_PATTERNS:
        for match in sorted(repo_dir.glob(pattern)):
            if match.is_file():
                rel = match.relative_to(repo_dir).as_posix()
                if rel not in found:
                    found.append(rel)
    return sorted(found)
