"""Install agent config files from source to target with conflict handling."""

import shutil
import subprocess
from pathlib import Path

from rich.prompt import Confirm
from rich.table import Table

from agentfish.agents import AgentConfig, identify_agent_for_file, is_universal_file
from agentfish.utils import console, is_safe_path, validate_file_path


def get_repo_sha(repo_dir: Path) -> str | None:
    """Get the HEAD commit SHA from a cloned repo."""
    try:
        result = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=repo_dir,
            capture_output=True,
            text=True,
        )
        if result.returncode == 0:
            return result.stdout.strip()
    except Exception:
        pass
    return None


def show_discovered_files(
    files: list[str],
    source: str,
    detected_agents: list[AgentConfig] | None = None,
) -> None:
    """Display a table of discovered agent config files with agent ownership."""
    detected_names = {a.name for a in detected_agents} if detected_agents is not None else None

    table = Table(title=f"Agent config files found in [bold]{source}[/bold]")
    table.add_column("#", style="dim", width=4)
    table.add_column("File", style="cyan")
    table.add_column("Agent", style="magenta")
    if detected_names is not None:
        table.add_column("Status", width=10)

    for i, f in enumerate(files, 1):
        agent = identify_agent_for_file(f)
        agent_name = agent.name if agent else "Universal"

        if detected_names is not None:
            if is_universal_file(f):
                status = "[green]✓ install[/green]"
            elif agent and agent.name in detected_names:
                status = "[green]✓ install[/green]"
            else:
                status = "[dim]⊘ skip[/dim]"
            table.add_row(str(i), f, agent_name, status)
        else:
            table.add_row(str(i), f, agent_name)

    console.print(table)


def show_detected_agents(detected: list[AgentConfig]) -> None:
    """Display a table of detected agents."""
    table = Table(title="Detected AI coding agents")
    table.add_column("Agent", style="bold cyan")
    table.add_column("Config Dir", style="dim")
    for agent in detected:
        table.add_row(agent.name, agent.config_dir)
    console.print(table)


def filter_files_by_agents(
    files: list[str],
    detected_agents: list[AgentConfig],
) -> tuple[list[str], list[str]]:
    """Split files into installable and skipped based on detected agents.

    Returns (files_to_install, files_to_skip).
    Universal files (e.g. AGENTS.md) are always included.
    """
    detected_names = {a.name for a in detected_agents}
    to_install: list[str] = []
    to_skip: list[str] = []

    for f in files:
        if is_universal_file(f):
            to_install.append(f)
            continue

        agent = identify_agent_for_file(f)
        if agent is None:
            # Unknown agent file — install anyway (conservative)
            to_install.append(f)
        elif agent.name in detected_names:
            to_install.append(f)
        else:
            to_skip.append(f)

    return to_install, to_skip


def install_files(
    files: list[str],
    source_dir: Path,
    target_dir: Path,
    interactive: bool = True,
) -> list[str]:
    """Install discovered files from source to target.

    Returns list of files that were actually installed.
    """
    installed: list[str] = []

    for rel_path in files:
        if not validate_file_path(rel_path):
            console.print(f"  [red]✗[/red] Skipping unsafe path: {rel_path}")
            continue

        src = source_dir / rel_path
        dst = target_dir / rel_path

        if not src.exists():
            continue
        if not is_safe_path(target_dir, dst):
            console.print(f"  [red]Skipping path traversal:[/red] {rel_path}")
            continue

        if dst.exists() and interactive:
            overwrite = Confirm.ask(
                f"  [yellow]File already exists:[/yellow] {rel_path}. Overwrite?"
            )
            if not overwrite:
                console.print(f"  [dim]Skipped:[/dim] {rel_path}")
                continue

        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(str(src), str(dst))
        installed.append(rel_path)
        console.print(f"  [green]Added:[/green] {rel_path}")

    return installed
