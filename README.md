# agentfish 🐠

Install complete AI agent configuration bundles from any git repository.

Like [skillfish](https://github.com/knoxgraeme/skillfish) but for **full agent configs** — not just skills.

## What it does

`agentfish` discovers and installs AI coding agent configuration files from any git repository into your project. It **automatically detects which AI coding agents you have installed** (globally and per-project) and **only installs config files for those agents**.

While **skillfish** manages individual skills (`SKILL.md` files), **agentfish** manages **complete agent configuration bundles** — the full set of instruction files, rules, and agent definitions that make AI coding assistants work well in a project.

## Quick Start

```bash
# Install with uvx (no install needed)
uvx agentfish add owner/repo

# Or install globally
pip install agentfish
agentfish add owner/repo
```

One command discovers all agent config files in the source repo, detects which agents you use, and installs only the relevant files.

## Agent Detection

agentfish automatically detects 20+ AI coding agents by checking for their configuration directories and files — both globally (`~/`) and in the current project:

```bash
# See which agents are detected
agentfish detect
```

```
       Detected AI coding agents
┏━━━━━━━━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━━┓
┃ Agent          ┃  Global  ┃ Project  ┃
┡━━━━━━━━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━━┩
│ Claude Code    │    ✓     │    ✓     │
│ GitHub Copilot │    ✓     │    –     │
│ Cursor         │    –     │    ✓     │
└────────────────┴──────────┴──────────┘
```

When you run `add`, `update`, or `install`, agentfish:

1. **Detects** your installed agents automatically
2. **Shows** all discovered files with their agent ownership
3. **Installs** only files for detected agents + universal files (like `AGENTS.md`)
4. **Skips** files for agents you don't use

Use `--all-agents` / `-a` to bypass detection and install everything:

```bash
agentfish add owner/repo --all-agents
```

### No Agents? Initialize One

When no agents are detected, agentfish offers to initialize one for you:

```
No AI coding agents detected.
Would you like to initialize an agent for this project? [Y/n]: y

       Available agents
┏━━━━━┳━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━┓
┃ #   ┃ Agent          ┃ Config Dir   ┃
┡━━━━━╇━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━┩
│ 1   │ Claude Code    │ .claude      │
│ 2   │ Cursor         │ .cursor      │
│ 3   │ GitHub Copilot │ .github      │
│ ... │ ...            │ ...          │
└─────┴────────────────┴──────────────┘

Enter agent numbers to initialize (comma-separated, e.g. 1,3,5): 1,3
  ✓ Created .claude/CLAUDE.md
  ✓ Created .github/copilot-instructions.md
```

This creates starter config files for the selected agents, making them detectable for future installs.

### Detected Agents

| Agent | Config Files | Global Detection | Project Detection |
|---|---|---|---|
| Claude Code | `CLAUDE.md`, `.claude/settings.json`, `.claude/rules/`, `.claude/agents/` | `~/.claude/` | `.claude/`, `CLAUDE.md` |
| Cursor | `.cursor/rules/*.mdc` (MDC format with YAML frontmatter) | `~/.cursor/` | `.cursor/`, `.cursorrules` |
| GitHub Copilot | `.github/copilot-instructions.md`, `.github/agents/*.agent.md`, `.github/instructions/*.instructions.md` | `~/.copilot/` | `.github/copilot-instructions.md`, `.github/agents/` |
| Windsurf | `.windsurf/rules/*.md`, `.windsurf/workflows/*.md`, `.windsurfrules` | `~/.codeium/windsurf/` | `.windsurf/`, `.windsurfrules` |
| Continue.dev | `.continue/config.yaml`, `.continue/rules/*.md` | `~/.continue/` | `.continue/` |
| Codex | `.codex/config.toml` (TOML), `AGENTS.md` (instructions) | `~/.codex/` | `.codex/` |
| Gemini CLI | `GEMINI.md`, `.gemini/settings.json`, `.geminiignore` | `~/.gemini/` | `.gemini/`, `GEMINI.md` |
| OpenCode | `opencode.json`, `.opencode/agents/`, `.opencode/commands/` | `~/.config/opencode/` | `.opencode/`, `opencode.json` |
| Goose | `.goosehints` (supports `@file` imports) | `~/.config/goose/` | `.goosehints` |
| Cline | `.clinerules/*.md` (optional YAML frontmatter with `paths:`) | `~/Documents/Cline/Rules/` | `.clinerules/` |
| Roo Code | `.roo/rules/`, `.roo/rules-{mode}/` (code, architect, debug) | `~/.roo/` | `.roo/`, `.roorules` |
| Kilo Code | `kilo.jsonc`, `.kilo/rules/*.md`, `.kilo/agents/` | `~/.config/kilo/` | `.kilo/`, `kilo.jsonc` |
| Kiro | `.kiro/steering/*.md`, `.kiro/specs/`, `.kiro/hooks/` | `~/.kiro/` | `.kiro/` |
| Aider | `.aider.conf.yml` (YAML), `.aiderignore` | `~/.aider.conf.yml` | `.aider.conf.yml` |
| Junie | `.junie/guidelines.md` | — | `.junie/` |
| Amp | `AGENTS.md` (hierarchical, cwd + parents) | `~/.config/amp/` | `AGENTS.md` |
| Trae | `.trae/rules/*.md` | `~/.trae/` | `.trae/` |
| Augment | `.augment/rules/*.md` (YAML frontmatter: `type`, `description`) | `~/.augment/` | `.augment/` |

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
├── CLAUDE.md                        # Claude Code instructions (project root)
├── GEMINI.md                        # Gemini CLI instructions (project root)
├── AGENTS.md                        # Universal instructions (any agent)
├── .claude/
│   ├── settings.json                # Claude Code settings
│   └── rules/                       # Claude Code scoped rules
│       └── security.md
├── .cursor/
│   └── rules/                       # Cursor rules (MDC format)
│       └── project.mdc
├── .github/
│   ├── copilot-instructions.md      # GitHub Copilot instructions
│   ├── agents/                      # Copilot agent definitions
│   │   └── CodeReview.agent.md
│   └── instructions/                # Copilot scoped instructions
│       └── python.instructions.md
├── .windsurf/
│   └── rules/                       # Windsurf Cascade rules
│       └── project.md
├── .continue/
│   └── rules/                       # Continue.dev rules
│       └── project.md
├── .clinerules/                     # Cline rules
│   └── project.md
├── .roo/
│   └── rules/                       # Roo Code rules (all modes)
│       └── project.md
├── .aider.conf.yml                  # Aider configuration
├── .goosehints                      # Goose context hints
└── .junie/
    └── guidelines.md                # Junie guidelines
```

### Step 3: Write your instructions

Each file contains instructions specific to its agent. A common pattern is to write the main instructions in one file (e.g. `.claude/CLAUDE.md`) and have other agent files reference it:

**CLAUDE.md** (project root) — your main, detailed instructions:
```markdown
# Project Guidelines

## Build & Test Commands

- Install: `npm install`
- Test: `npm test`
- Lint: `npm run lint`
- Build: `npm run build`

## Architecture

- Use repository pattern for data access
- Keep controllers thin
- Business logic goes in services

## Coding Standards

- TypeScript strict mode
- Follow ESLint rules
- Write tests for all new code
```

**.github/copilot-instructions.md** — always loaded by Copilot:
```markdown
# Copilot Instructions

For comprehensive guidelines, refer to [CLAUDE.md](../CLAUDE.md).

## Quick Reference
- TypeScript strict mode
- ESLint compliance required
- Jest for unit tests, Cypress for E2E
```

**.cursor/rules/project.mdc** — MDC format with YAML frontmatter:
```markdown
---
description: Project-wide coding standards
globs:
alwaysApply: true
---

# Project Rules

Refer to CLAUDE.md for full guidelines.
- TypeScript strict mode
- Repository pattern for data access
- Tests required for all new code
```

### Step 4: Add Copilot Agents (optional)

If you use GitHub Copilot coding agent, you can include reusable agent definitions in `.github/agents/`:

**.github/agents/CodeReview.agent.md** (requires `.agent.md` suffix):
```markdown
---
description: Reviews pull requests for quality and security
tools:
  - github
---

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
| `CLAUDE.md`, `CLAUDE.local.md` | Claude Code |
| `.claude/**/*` | Claude Code (settings, rules, agents, commands, skills) |
| `.cursorrules` | Cursor (legacy) |
| `.cursor/rules/**/*.mdc` | Cursor rules (MDC format) |
| `.github/copilot-instructions.md` | GitHub Copilot |
| `.github/copilot-setup-steps.yml` | GitHub Copilot setup |
| `.github/agents/*.md`, `*.agent.md` | GitHub Copilot Agents |
| `.github/instructions/*.instructions.md` | GitHub Copilot scoped instructions |
| `.github/prompts/*.prompt.md` | GitHub Copilot prompts |
| `.windsurf/rules/**/*` | Windsurf rules |
| `.windsurf/workflows/**/*` | Windsurf workflows |
| `.windsurfrules` | Windsurf (legacy flat file) |
| `.continue/config.yaml`, `.continue/config.json` | Continue.dev config |
| `.continue/rules/**/*` | Continue.dev rules |
| `.codex/config.toml` | Codex configuration |
| `GEMINI.md` | Gemini CLI |
| `.gemini/settings.json` | Gemini CLI settings |
| `.geminiignore` | Gemini CLI ignore file |
| `opencode.json` | OpenCode config |
| `.opencode/**/*` | OpenCode (agents, commands) |
| `.goosehints` | Goose |
| `.clinerules/**/*` | Cline rules |
| `.roo/**/*` | Roo Code rules |
| `.roorules` | Roo Code (legacy flat file) |
| `kilo.jsonc` | Kilo Code manifest |
| `.kilo/**/*` | Kilo Code (rules, agents) |
| `.kiro/**/*` | Kiro (steering, specs, hooks) |
| `.aider.conf.yml` | Aider config |
| `.aiderignore` | Aider ignore file |
| `.junie/**/*` | Junie guidelines |
| `.trae/rules/**/*` | Trae rules |
| `.augment/rules/**/*` | Augment rules |
| `augment-guidelines.md` | Augment (legacy) |
| `.amprules` | Amp rules |
| `AGENTS.md` | Universal (any agent) |

---

## Commands

### add

Install agent configs from a git repository. Auto-detects agents first and only installs relevant files.

```bash
agentfish add owner/repo                    # GitHub shorthand
agentfish add owner/repo#branch             # Specific branch
agentfish add https://github.com/owner/repo # Full URL
agentfish add https://dev.azure.com/org/project/_git/repo  # Azure DevOps
agentfish add https://gitlab.com/owner/repo # GitLab
agentfish add owner/repo --name my-configs  # Custom name
agentfish add owner/repo --yes              # Skip prompts
agentfish add owner/repo --all-agents       # Install for all agents
```

### detect

Show which AI coding agents are detected on your system and in the current project. If none are found, offers to initialize one.

```bash
agentfish detect
```

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
agentfish update --all-agents                # Update for all agents
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
agentfish install --all-agents               # Install for all agents
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

## Usage with Git Providers

agentfish works with **any git-cloneable repository**. It uses `git clone` under the hood, so any URL that `git clone` accepts will work. Below are examples for every major provider.

### GitHub

```bash
# Shorthand (auto-expands to https://github.com/owner/repo.git)
uvx agentfish add owner/repo
uvx agentfish add owner/repo#main

# Full HTTPS URL
uvx agentfish add https://github.com/owner/repo
uvx agentfish add https://github.com/owner/repo#my-branch

# SSH (requires SSH key configured)
uvx agentfish add git@github.com:owner/repo.git
```

**Private repos**: GitHub HTTPS works automatically if you have `gh` CLI authenticated or a git credential manager configured. For SSH, ensure your key is in `~/.ssh/`.

### Azure DevOps

```bash
# HTTPS (standard format)
uvx agentfish add https://dev.azure.com/org/project/_git/repo
uvx agentfish add https://dev.azure.com/org/project/_git/repo#my-branch

# HTTPS with username (common when copied from Azure DevOps UI)
uvx agentfish add https://user@dev.azure.com/org/project/_git/repo

# SSH
uvx agentfish add git@ssh.dev.azure.com:v3/org/project/repo
```

**Authentication**: Azure DevOps HTTPS requires a [Personal Access Token (PAT)](https://learn.microsoft.com/en-us/azure/devops/organizations/accounts/use-personal-access-tokens-to-authenticate) or a configured git credential manager. When prompted for a password, use your PAT. You can also configure it globally:

```bash
# Cache credentials for Azure DevOps
git config --global credential.https://dev.azure.com.provider generic
# Or use Azure CLI credential helper
az devops login
```

### GitLab

```bash
# HTTPS
uvx agentfish add https://gitlab.com/owner/repo
uvx agentfish add https://gitlab.com/owner/repo#my-branch

# Self-hosted GitLab
uvx agentfish add https://gitlab.mycompany.com/group/repo

# SSH
uvx agentfish add git@gitlab.com:owner/repo.git
```

**Private repos**: Use a [Personal Access Token](https://docs.gitlab.com/user/profile/personal_access_tokens/) or SSH key.

### Bitbucket

```bash
# HTTPS
uvx agentfish add https://bitbucket.org/owner/repo
uvx agentfish add https://bitbucket.org/owner/repo#my-branch

# SSH
uvx agentfish add git@bitbucket.org:owner/repo.git
```

**Authentication**: Use an [App Password](https://support.atlassian.com/bitbucket-cloud/docs/create-an-app-password/) for HTTPS.

### Self-Hosted / Other Git Servers

```bash
# Any HTTPS git URL
uvx agentfish add https://git.mycompany.com/team/repo.git
uvx agentfish add https://git.mycompany.com/team/repo.git#develop

# Any SSH git URL
uvx agentfish add git@git.mycompany.com:team/repo.git

# Gitea, Forgejo, etc.
uvx agentfish add https://gitea.example.com/owner/repo
```

### Branch Selection

Append `#branch-name` to any URL or shorthand to use a specific branch:

```bash
uvx agentfish add owner/repo#develop
uvx agentfish add https://dev.azure.com/org/project/_git/repo#feature/security-configs
uvx agentfish add https://gitlab.com/team/configs#v2
```

This is useful when you maintain different config bundles on different branches (e.g., `#dotnet`, `#python`, `#security`).

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

## Adding a New Agent

To add support for a new AI coding agent, append an `AgentConfig` to `AGENT_CONFIGS` in `src/agentfish/agents.py`:

```python
AgentConfig(
    name="My New Agent",
    config_dir=".mynewagent",
    home_paths=(".mynewagent",),           # paths under ~/ for global detection
    cwd_paths=(".mynewagent",),            # paths under ./ for project detection
    file_patterns=(".mynewagent/",),       # patterns this agent owns (for filtering)
    init_files={                           # files created by `agentfish detect` init
        ".mynewagent/instructions.md": "# My New Agent\n\nInstructions here.\n",
    },
)
```

That's it — the new agent will automatically work with detection, filtering, and initialization.

## License

MIT
