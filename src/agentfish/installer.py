"""Install agent config files from source to target with conflict handling."""

import shutil
import subprocess
from pathlib import Path

from rich.prompt import Confirm
from rich.table import Table

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


def show_discovered_files(files: list[str], source: str) -> None:
    """Display a table of discovered agent config files."""
    table = Table(title=f"Agent config files found in [bold]{source}[/bold]")
    table.add_column("#", style="dim", width=4)
    table.add_column("File", style="cyan")
    for i, f in enumerate(files, 1):
        table.add_row(str(i), f)
    console.print(table)


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
            console.print(f"  [red]✗[/red] Skipping path traversal: {rel_path}")
            continue

        if dst.exists() and interactive:
            overwrite = Confirm.ask(
                f"  [yellow]File already exists:[/yellow] {rel_path}. Overwrite?"
            )
            if not overwrite:
                console.print(f"  [dim]⊘ Skipped:[/dim] {rel_path}")
                continue

        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(str(src), str(dst))
        installed.append(rel_path)
        console.print(f"  [green]✓[/green] {rel_path}")

    return installed
