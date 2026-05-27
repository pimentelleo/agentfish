"""Auto-discover known AI agent configuration files in a directory."""

from pathlib import Path

AGENT_CONFIG_PATTERNS: list[str] = [
    ".claude/CLAUDE.md",
    ".claude/settings.json",
    ".claude/commands/**/*",
    ".cursor/rules",
    ".cursor/rules/**/*.mdc",
    ".continue/instructions.md",
    ".continue/config.json",
    ".codeium/instructions.md",
    ".github/copilot-instructions.md",
    ".github/copilot-setup-steps.yml",
    ".github/agents/*.md",
    ".github/agents/*.mmd",
    "AGENTS.md",
    ".windsurfrules",
    ".clinerules",
    ".clinerules/**/*",
    ".roo/**/*",
    ".aider.conf.yml",
    ".aiderignore",
    ".junie/**/*",
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
