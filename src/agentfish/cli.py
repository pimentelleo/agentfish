"""CLI commands for agentfish."""

import shutil
from pathlib import Path

import click
from rich.prompt import Confirm
from rich.table import Table

from agentfish import __version__
from agentfish.discovery import discover_agent_files
from agentfish.git_provider import RepoRef, cleanup_clone, clone_repo, parse_repo_ref
from agentfish.installer import get_repo_sha, install_files, show_discovered_files
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


@click.group()
@click.version_option(version=__version__, prog_name="agentfish")
def main() -> None:
    """🐠 agentfish — Install AI agent config bundles from any git repo."""


@main.command()
@click.argument("repo")
@click.option("--branch", "-b", default=None, help="Branch to clone.")
@click.option("--name", "-n", default=None, help="Custom name for this thing.")
@click.option("--yes", "-y", is_flag=True, help="Skip confirmation prompts.")
def add(repo: str, branch: str | None, name: str | None, yes: bool) -> None:
    """Add agent configs from a git repository."""
    ref = parse_repo_ref(repo)
    if branch:
        ref.branch = branch
    thing_name = name or ref.name or derive_thing_name(repo)

    console.print(f"\n🐠 Fetching [bold]{ref.display}[/bold]...")

    clone_dir = None
    try:
        clone_dir = clone_repo(ref)
        files = discover_agent_files(clone_dir)

        if not files:
            err_console.print("[yellow]No agent config files found in this repository.[/yellow]")
            return

        show_discovered_files(files, ref.display)

        if not yes:
            proceed = Confirm.ask("\nInstall these files?", default=True)
            if not proceed:
                console.print("[dim]Cancelled.[/dim]")
                return

        target = Path.cwd()
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
def update(name: str | None, yes: bool) -> None:
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

    for thing in things_to_update:
        console.print(f"\n🐠 Updating [bold]{thing.name}[/bold] from {thing.source}...")
        ref = RepoRef(url=thing.source, branch=thing.branch, name=thing.name)
        clone_dir = None
        try:
            clone_dir = clone_repo(ref)
            files = discover_agent_files(clone_dir)

            if not files:
                console.print(f"  [yellow]No agent config files found.[/yellow]")
                continue

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
    console.print(f"\n[green]✓ Bundled {len(files)} file(s) into {MANIFEST_FILE}[/green]")


@main.command("install")
@click.option("--yes", "-y", is_flag=True, help="Skip confirmation prompts.")
def install_cmd(yes: bool) -> None:
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

    for thing in remote_things:
        console.print(f"\n🐠 Installing [bold]{thing.name}[/bold] from {thing.source}...")
        ref = RepoRef(url=thing.source, branch=thing.branch, name=thing.name)
        clone_dir = None
        try:
            clone_dir = clone_repo(ref)
            files = discover_agent_files(clone_dir)

            if not files:
                console.print(f"  [yellow]No agent config files found.[/yellow]")
                continue

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
