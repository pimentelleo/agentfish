# agentfish 🐠

Install complete AI agent configuration bundles from any git repository.

Like [skillfish](https://github.com/knoxgraeme/skillfish) but for **full agent configs** — not just skills.

## What it does

`agentfish` discovers and installs AI coding agent configuration files from any git repository into your project. It auto-detects files for Claude Code, Cursor, GitHub Copilot, Continue, Codeium, Windsurf, Cline, and more.

While **skillfish** manages individual skills (`SKILL.md` files), **agentfish** manages **complete agent configuration bundles** — the full set of instruction files, rules, and agent definitions that make AI coding assistants work well in a project.

## Quick Start

```bash
# Install with uvx (no install needed)
uvx agentfish add owner/repo

# Or install globally
pip install agentfish
agentfish add owner/repo
```

One command discovers all agent config files in the source repo and installs them into your project.

---

## Creating an Agent Config Bundle

Any git repository can be an agentfish-compatible bundle. There's no special marker file needed — agentfish auto-discovers standard agent configuration files.

### Step 1: Create your repo

Create a new git repository (GitHub, Azure DevOps, GitLab, or any git host):

```bash
mkdir my-agent-configs
cd my-agent-configs
git init
```

### Step 2: Add agent config files

Add any combination of the supported files. You don't need all of them — add only what you need:

```
my-agent-configs/
├── .claude/
│   └── CLAUDE.md              # Claude Code instructions
├── .cursor/
│   └── rules                  # Cursor rules
├── .github/
│   ├── copilot-instructions.md  # GitHub Copilot instructions
│   └── agents/                  # Copilot agent definitions
│       ├── CodeReview.md
│       └── Security.md
├── .continue/
│   └── instructions.md        # Continue.dev instructions
├── .codeium/
│   └── instructions.md        # Codeium / Windsurf instructions
└── AGENTS.md                  # Generic agent instructions
```

### Step 3: Write your instructions

Each file contains instructions specific to its agent. A common pattern is to write the main instructions in one file (e.g. `.claude/CLAUDE.md`) and have other agent files reference it:

**.claude/CLAUDE.md** — your main, detailed instructions:
```markdown
# Project Guidelines

## Code Style
- Use TypeScript strict mode
- Follow ESLint rules
- Write tests for all new code

## Architecture
- Use repository pattern for data access
- Keep controllers thin
- Business logic goes in services

## Testing
- Jest for unit tests
- Cypress for E2E tests
- Minimum 80% coverage for new code
```

**.github/copilot-instructions.md** — reference the main file:
```markdown
# Copilot Instructions

For comprehensive guidelines, refer to [CLAUDE.md](../.claude/CLAUDE.md).

## Quick Reference
- TypeScript strict mode
- ESLint compliance required
- Jest for unit tests, Cypress for E2E
```

**.cursor/rules** — same pattern:
```markdown
# Cursor Rules

Refer to [CLAUDE.md](../.claude/CLAUDE.md) for full guidelines.

## Key Points
- TypeScript strict mode
- Repository pattern for data access
- Tests required for all new code
```

### Step 4: Add Copilot Agents (optional)

If you use GitHub Copilot coding agent, you can include reusable agent definitions in `.github/agents/`:

**.github/agents/CodeReview.md**:
```markdown
## Code Review Agent

You review pull requests for quality, security, and adherence to project standards.

### Checklist
- [ ] Code follows project style guide
- [ ] Tests are included
- [ ] No security vulnerabilities introduced
- [ ] Documentation updated if needed
```

### Step 5: Push and share

```bash
git add -A
git commit -m "Add agent config bundle"
git remote add origin https://github.com/yourname/my-agent-configs.git
git push -u origin main
```

Now anyone can install your configs:

```bash
uvx agentfish add yourname/my-agent-configs
```

### Using a branch

You can keep agent configs on a specific branch. This is useful for maintaining different configs for different purposes in the same repo:

```bash
uvx agentfish add yourname/my-repo#my-branch
```

---

## Supported Agent Config Files

agentfish auto-discovers these files in source repositories:

| Path | Agent |
|---|---|
| `.claude/CLAUDE.md` | Claude Code |
| `.claude/settings.json` | Claude Code settings |
| `.claude/commands/**/*` | Claude Code custom commands |
| `.cursor/rules` | Cursor |
| `.cursor/rules/**/*.mdc` | Cursor rule files |
| `.github/copilot-instructions.md` | GitHub Copilot |
| `.github/copilot-setup-steps.yml` | GitHub Copilot setup |
| `.github/agents/*.md` | GitHub Copilot Agents |
| `.github/agents/*.mmd` | Agent interaction diagrams |
| `.continue/instructions.md` | Continue.dev |
| `.continue/config.json` | Continue.dev config |
| `.codeium/instructions.md` | Codeium / Windsurf |
| `AGENTS.md` | Generic (any agent) |
| `.windsurfrules` | Windsurf |
| `.clinerules` | Cline |
| `.clinerules/**/*` | Cline rule files |
| `.roo/**/*` | Roo Code |
| `.aider.conf.yml` | Aider |
| `.aiderignore` | Aider |
| `.junie/**/*` | Junie |

---

## Commands

### add

Install agent configs from a git repository.

```bash
agentfish add owner/repo                    # GitHub shorthand
agentfish add owner/repo#branch             # Specific branch
agentfish add https://github.com/owner/repo # Full URL
agentfish add https://dev.azure.com/org/project/_git/repo  # Azure DevOps
agentfish add https://gitlab.com/owner/repo # GitLab
agentfish add owner/repo --name my-configs  # Custom name
agentfish add owner/repo --yes              # Skip prompts
```

When a file already exists in your project, agentfish asks whether to overwrite it.

### list

View installed agent config bundles.

```bash
agentfish list
```

### remove

Remove an installed bundle.

```bash
agentfish remove my-configs                 # Remove from manifest only
agentfish remove my-configs --delete-files   # Also delete the files
agentfish remove my-configs --yes            # Skip confirmation
```

### update

Update installed configs from their source repos.

```bash
agentfish update                             # Update all
agentfish update my-configs                  # Update specific bundle
agentfish update --yes                       # Skip prompts
```

### init

Create an empty `.agentfish.json` manifest.

```bash
agentfish init
```

### bundle

Scan current project for agent config files and create a manifest.

```bash
agentfish bundle
```

### install

Install all things listed in `.agentfish.json` manifest.

```bash
agentfish install                            # Install from manifest
agentfish install --yes                      # Skip prompts
```

---

## Team Sync

Share agent configs across your team using the manifest:

1. Add configs to your project:
   ```bash
   agentfish add yourorg/shared-agent-configs
   ```

2. Commit the `.agentfish.json` manifest to your project repo.

3. Team members run:
   ```bash
   agentfish install
   ```

This keeps everyone's agent configs in sync, similar to how `package.json` + `npm install` works.

---

## Repo Reference Formats

agentfish works with any git-cloneable repository:

```bash
# GitHub (shorthand)
agentfish add owner/repo
agentfish add owner/repo#branch

# GitHub (full URL)
agentfish add https://github.com/owner/repo

# Azure DevOps
agentfish add https://dev.azure.com/org/project/_git/repo
agentfish add https://user@dev.azure.com/org/project/_git/repo#branch

# GitLab
agentfish add https://gitlab.com/owner/repo

# Any git host
agentfish add https://git.example.com/owner/repo.git
```

## Manifest Format

`.agentfish.json` tracks what's installed:

```json
{
  "version": "1.0",
  "things": [
    {
      "name": "my-agent-configs",
      "source": "https://github.com/owner/repo.git",
      "branch": "main",
      "sha": "abc123def456",
      "installed_at": "2025-06-01T10:30:00+00:00",
      "files": [
        ".claude/CLAUDE.md",
        ".cursor/rules",
        ".github/copilot-instructions.md",
        ".github/agents/CodeReview.md"
      ]
    }
  ]
}
```

## Security

- **Path validation**: agentfish rejects paths containing `..` or symlinks that escape the project directory
- **Shallow clones**: source repos are cloned with `--depth=1` and deleted after installation
- **Conflict prompts**: existing files are never silently overwritten (unless `--yes` is used)

## License

MIT
