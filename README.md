# agentfish 🐠

Install complete AI agent configuration bundles from any git repository.

Like [skillfish](https://github.com/knoxgraeme/skillfish) but for **full agent configs** — not just skills.

## What it does

`agentfish` discovers and installs AI coding agent configuration files from any git repository into your project. It auto-detects files for Claude, Cursor, GitHub Copilot, Continue, Codeium, Windsurf, and more.

## Quick Start

```bash
# Install with uvx (no install needed)
uvx agentfish add owner/repo

# Or install globally
pip install agentfish
agentfish add owner/repo
```

## Commands

| Command | Description |
|---|---|
| `agentfish add <repo>` | Install agent configs from a repo |
| `agentfish list` | List installed things |
| `agentfish remove <name>` | Remove installed thing |
| `agentfish update [name]` | Update installed things |
| `agentfish init` | Initialize `.agentfish.json` manifest |
| `agentfish bundle` | Create manifest from existing agent configs |
| `agentfish install` | Install all things from manifest |

## Supported Agent Config Files

agentfish auto-discovers these files in source repositories:

- `.claude/CLAUDE.md` — Claude Code
- `.cursor/rules` — Cursor
- `.github/copilot-instructions.md` — GitHub Copilot
- `.github/agents/*.md` — GitHub Copilot Agents
- `.continue/instructions.md` — Continue.dev
- `.codeium/instructions.md` — Codeium / Windsurf
- `AGENTS.md` — Generic agent instructions
- `.windsurfrules` — Windsurf rules
- `.clinerules` — Cline rules
- And more...

## Repo Reference Formats

```bash
# GitHub shorthand
agentfish add owner/repo
agentfish add owner/repo#branch

# Full URLs (GitHub, Azure DevOps, GitLab, any git host)
agentfish add https://github.com/owner/repo
agentfish add https://dev.azure.com/org/project/_git/repo
agentfish add https://gitlab.com/owner/repo
```

## Manifest

agentfish tracks installed configs in `.agentfish.json`:

```json
{
  "version": "1.0",
  "things": [
    {
      "name": "my-agent-configs",
      "source": "owner/repo",
      "branch": "main",
      "files": [".claude/CLAUDE.md", ".cursor/rules", ".github/agents/Review.md"]
    }
  ]
}
```

## License

MIT
