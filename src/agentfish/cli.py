"""CLI commands for agentfish."""

import shutil
from pathlib import Path

import click
from rich.prompt import Confirm, Prompt
from rich.table import Table

from agentfish import __version__
from agentfish.agents import (
    AGENT_CONFIGS,
    detect_agent,
    get_detected_agents,
    identify_agent_for_file,
    initialize_agent,
    is_universal_file,
)
from agentfish.discovery import discover_agent_files
from agentfish.git_provider import RepoRef, cleanup_clone, clone_repo, parse_repo_ref
from agentfish.installer import (
    filter_files_by_agents,
    get_repo_sha,
    install_files,
    show_detected_agents,
    show_discovered_files,
)
from agentfish.manifest import (
    MANIFEST_FILE,
    Manifest,
    Thing,
    add_thing,
    find_thing,
    load_manifest,
    now_iso,
    remove_thing,
    save_manifest,
)
from agentfish.utils import console, derive_thing_name, err_console


def _prompt_initialize_agents(target: Path) -> list:
    """When no agents are detected, offer to initialize one.

    Returns the list of newly detected agents (may still be empty if user declines).
    """
    console.print("\n[yellow]No AI coding agents detected.[/yellow]")

    create = Confirm.ask("Would you like to initialize an agent for this project?", default=True)
    if not create:
        return []

    # Build numbered list
    names = [c.name for c in AGENT_CONFIGS]
    console.print()
    table = Table(title="Available agents", show_lines=False)
    table.add_column("#", style="dim", width=4)
    table.add_column("Agent", style="bold cyan")
    table.add_column("Config Dir", style="dim")

    for i, config in enumerate(AGENT_CONFIGS, 1):
        table.add_row(str(i), config.name, config.config_dir)
    console.print(table)

    choices = Prompt.ask(
        "\nEnter agent numbers to initialize (comma-separated, e.g. 1,3,5)",
    )

    selected: list = []
    for part in choices.split(","):
        part = part.strip()
        if not part.isdigit():
            continue
        idx = int(part) - 1
        if 0 <= idx < len(AGENT_CONFIGS):
            selected.append(AGENT_CONFIGS[idx])

    if not selected:
        console.print("[dim]No agents selected.[/dim]")
        return []

    console.print()
    for config in selected:
        created = initialize_agent(config, target)
        if created:
            for f in created:
                console.print(f"  [green]✓[/green] Created {f}")
        else:
            console.print(f"  [dim]{config.name} already initialized.[/dim]")

    # Re-detect now that files exist
    return get_detected_agents(project_dir=target)


def _detect_or_init(target: Path, all_agents: bool) -> list | None:
    """Detect agents. If none found and not --all-agents, offer to create.

    Returns detected agents list, or None if the command should abort.
    """
    detected = get_detected_agents(project_dir=target)
    console.print()

    if detected:
        show_detected_agents(detected)
        return detected

    if all_agents:
        show_detected_agents(detected)
        return detected

    detected = _prompt_initialize_agents(target)
    if detected:
        console.print()
        show_detected_agents(detected)
        return detected

    err_console.print("[dim]Use --all-agents to skip agent detection.[/dim]")
    return None


@click.group()
@click.version_option(version=__version__, prog_name="agentfish")
def main() -> None:
    """agentfish - Install AI agent config bundles from any git repo."""


@main.command()
@click.argument("repo")
@click.option("--branch", "-b", default=None, help="Branch to clone.")
@click.option("--name", "-n", default=None, help="Custom name for this thing.")
@click.option("--yes", "-y", is_flag=True, help="Skip confirmation prompts.")
@click.option("--all-agents", "-a", is_flag=True, help="Install for all agents, not just detected ones.")
def add(repo: str, branch: str | None, name: str | None, yes: bool, all_agents: bool) -> None:
    """Add agent configs from a git repository."""
    ref = parse_repo_ref(repo)
    if branch:
        ref.branch = branch
    thing_name = name or ref.name or derive_thing_name(repo)

    target = Path.cwd()

    # Always detect agents — offer to create if none found
    detected = _detect_or_init(target, all_agents)
    if detected is None:
        return

    console.print(f"\nFetching [bold]{ref.display}[/bold]...")

    clone_dir = None
    try:
        clone_dir = clone_repo(ref)
        files = discover_agent_files(clone_dir)

        if not files:
            err_console.print("[yellow]No agent config files found in this repository.[/yellow]")
            return

        # Always filter by detected agents (unless --all-agents)
        if not all_agents:
            to_install, to_skip = filter_files_by_agents(files, detected)
            show_discovered_files(files, ref.display, detected)

            if to_skip:
                console.print(
                    f"\n[dim]{len(to_skip)} file(s) skipped (agents not detected). "
                    f"Use --all-agents to install everything.[/dim]"
                )

            files = to_install
            if not files:
                err_console.print("[yellow]No files match detected agents.[/yellow]")
                return
        else:
            show_discovered_files(files, ref.display)

        if not yes:
            proceed = Confirm.ask("\nInstall these files?", default=True)
            if not proceed:
                console.print("[dim]Cancelled.[/dim]")
                return

        console.print()
        installed = install_files(files, clone_dir, target, interactive=not yes)

        if installed:
            sha = get_repo_sha(clone_dir)
            manifest = load_manifest(target)
            thing = Thing(
                name=thing_name,
                source=ref.url,
                branch=ref.branch,
                sha=sha,
                installed_at=now_iso(),
                files=installed,
            )
            manifest = add_thing(manifest, thing)
            save_manifest(target, manifest)
            console.print(f"\n[green]✓ Installed {len(installed)} file(s) as [bold]{thing_name}[/bold][/green]")
        else:
            console.print("\n[yellow]No files were installed.[/yellow]")
    except RuntimeError as e:
        err_console.print(f"[red]Error:[/red] {e}")
    finally:
        if clone_dir:
            cleanup_clone(clone_dir)


@main.command()
def detect() -> None:
    """Detect AI coding agents installed on this system."""
    project_dir = Path.cwd()

    console.print("\n🔍 Scanning for AI coding agents...\n")

    global_agents = get_detected_agents(location="global")
    project_agents = get_detected_agents(location="project", project_dir=project_dir)
    all_detected = get_detected_agents(location="both", project_dir=project_dir)

    if not all_detected:
        all_detected = _prompt_initialize_agents(project_dir)
        if not all_detected:
            return
        # Refresh after initialization
        global_agents = get_detected_agents(location="global")
        project_agents = get_detected_agents(location="project", project_dir=project_dir)
        console.print()

    table = Table(title="Detected AI coding agents")
    table.add_column("Agent", style="bold cyan")
    table.add_column("Global", width=8, justify="center")
    table.add_column("Project", width=8, justify="center")

    for agent in all_detected:
        is_global = agent in global_agents
        is_project = agent in project_agents
        table.add_row(
            agent.name,
            "[green]✓[/green]" if is_global else "[dim]–[/dim]",
            "[green]✓[/green]" if is_project else "[dim]–[/dim]",
        )

    console.print(table)
    console.print(f"\n[dim]Found {len(all_detected)} agent(s) ({len(global_agents)} global, {len(project_agents)} project)[/dim]")


@main.command("list")
def list_things() -> None:
    """List installed agent config bundles."""
    manifest = load_manifest(Path.cwd())
    if not manifest.things:
        console.print("[dim]No agent configs installed. Use [bold]agentfish add[/bold] to get started.[/dim]")
        return

    table = Table(title="Installed agent configs")
    table.add_column("Name", style="bold cyan")
    table.add_column("Source", style="dim")
    table.add_column("Branch")
    table.add_column("Files", justify="right")
    table.add_column("Installed", style="dim")

    for thing in manifest.things:
        table.add_row(
            thing.name,
            thing.source,
            thing.branch or "-",
            str(len(thing.files)),
            (thing.installed_at or "")[:10],
        )
    console.print(table)


@main.command()
@click.argument("name")
@click.option("--yes", "-y", is_flag=True, help="Skip confirmation.")
@click.option("--delete-files", is_flag=True, help="Also delete the installed files.")
def remove(name: str, yes: bool, delete_files: bool) -> None:
    """Remove an installed agent config bundle."""
    target = Path.cwd()
    manifest = load_manifest(target)
    thing = find_thing(manifest, name)

    if not thing:
        err_console.print(f"[red]Thing '{name}' not found.[/red]")
        return

    if not yes:
        msg = f"Remove [bold]{name}[/bold]"
        if delete_files:
            msg += f" and delete {len(thing.files)} file(s)"
        msg += "?"
        if not Confirm.ask(msg, default=False):
            console.print("[dim]Cancelled.[/dim]")
            return

    if delete_files:
        for f in thing.files:
            p = target / f
            if p.exists():
                p.unlink()
                console.print(f"  [red]✗[/red] Deleted: {f}")
            # Clean up empty parent directories
            parent = p.parent
            while parent != target and parent.exists() and not any(parent.iterdir()):
                parent.rmdir()
                parent = parent.parent

    manifest, _ = remove_thing(manifest, name)
    save_manifest(target, manifest)
    console.print(f"[green]✓ Removed [bold]{name}[/bold][/green]")


@main.command()
@click.argument("name", required=False)
@click.option("--yes", "-y", is_flag=True, help="Skip confirmation prompts.")
@click.option("--all-agents", "-a", is_flag=True, help="Install for all agents, not just detected ones.")
def update(name: str | None, yes: bool, all_agents: bool) -> None:
    """Update installed agent configs from their source repos."""
    target = Path.cwd()
    manifest = load_manifest(target)

    if not manifest.things:
        err_console.print("[yellow]No agent configs installed.[/yellow]")
        return

    things_to_update = manifest.things if name is None else [t for t in manifest.things if t.name == name]
    if not things_to_update:
        err_console.print(f"[red]Thing '{name}' not found.[/red]")
        return

    detected = _detect_or_init(target, all_agents)
    if detected is None:
        return

    for thing in things_to_update:
        console.print(f"\nUpdating [bold]{thing.name}[/bold] from {thing.source}...")
        ref = RepoRef(url=thing.source, branch=thing.branch, name=thing.name)
        clone_dir = None
        try:
            clone_dir = clone_repo(ref)
            files = discover_agent_files(clone_dir)

            if not files:
                console.print(f"  [yellow]No agent config files found.[/yellow]")
                continue

            if not all_agents:
                files, _ = filter_files_by_agents(files, detected)

            show_discovered_files(files, thing.name)

            if not yes:
                proceed = Confirm.ask("Update these files?", default=True)
                if not proceed:
                    continue

            installed = install_files(files, clone_dir, target, interactive=not yes)
            sha = get_repo_sha(clone_dir)

            thing.files = installed
            thing.sha = sha
            thing.installed_at = now_iso()
            manifest = add_thing(manifest, thing)
            save_manifest(target, manifest)
            console.print(f"  [green]✓ Updated {len(installed)} file(s)[/green]")
        except RuntimeError as e:
            err_console.print(f"  [red]Error:[/red] {e}")
        finally:
            if clone_dir:
                cleanup_clone(clone_dir)


@main.command()
def init() -> None:
    """Initialize .agentfish.json manifest in the current project."""
    target = Path.cwd()
    manifest_path = target / MANIFEST_FILE

    if manifest_path.exists():
        console.print(f"[yellow]{MANIFEST_FILE} already exists.[/yellow]")
        return

    save_manifest(target, Manifest())
    console.print(f"[green]✓ Created {MANIFEST_FILE}[/green]")


@main.command()
def bundle() -> None:
    """Create manifest from existing agent configs in the current project."""
    target = Path.cwd()
    files = discover_agent_files(target)

    if not files:
        console.print("[yellow]No agent config files found in current directory.[/yellow]")
        return

    show_discovered_files(files, str(target.name))

    manifest = load_manifest(target)
    thing = Thing(
        name=target.name,
        source="local",
        installed_at=now_iso(),
        files=files,
    )
    manifest = add_thing(manifest, thing)
    save_manifest(target, manifest)
    console.print(f"\n[green]Bundled {len(files)} file(s) into {MANIFEST_FILE}[/green]")


@main.command("install")
@click.option("--yes", "-y", is_flag=True, help="Skip confirmation prompts.")
@click.option("--all-agents", "-a", is_flag=True, help="Install for all agents, not just detected ones.")
def install_cmd(yes: bool, all_agents: bool) -> None:
    """Install all things from .agentfish.json manifest."""
    target = Path.cwd()
    manifest = load_manifest(target)

    if not manifest.things:
        err_console.print("[yellow]No things in manifest. Use [bold]agentfish add[/bold] first.[/yellow]")
        return

    remote_things = [t for t in manifest.things if t.source != "local"]
    if not remote_things:
        console.print("[dim]All things are local, nothing to install.[/dim]")
        return

    detected = _detect_or_init(target, all_agents)
    if detected is None:
        return

    for thing in remote_things:
        console.print(f"\nInstalling [bold]{thing.name}[/bold] from {thing.source}...")
        ref = RepoRef(url=thing.source, branch=thing.branch, name=thing.name)
        clone_dir = None
        try:
            clone_dir = clone_repo(ref)
            files = discover_agent_files(clone_dir)

            if not files:
                console.print(f"  [yellow]No agent config files found.[/yellow]")
                continue

            if not all_agents:
                files, _ = filter_files_by_agents(files, detected)

            installed = install_files(files, clone_dir, target, interactive=not yes)
            sha = get_repo_sha(clone_dir)

            thing.files = installed
            thing.sha = sha
            thing.installed_at = now_iso()
            console.print(f"  [green]✓ Installed {len(installed)} file(s)[/green]")
        except RuntimeError as e:
            err_console.print(f"  [red]Error:[/red] {e}")
        finally:
            if clone_dir:
                cleanup_clone(clone_dir)

    save_manifest(target, manifest)
    console.print(f"\n[green]✓ All things installed.[/green]")
