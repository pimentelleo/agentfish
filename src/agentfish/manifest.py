"""Manage .agentfish.json manifest files."""

import json
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path

MANIFEST_FILE = ".agentfish.json"


@dataclass
class Thing:
    """An installed agent config bundle."""

    name: str
    source: str
    branch: str | None = None
    sha: str | None = None
    installed_at: str | None = None
    files: list[str] = field(default_factory=list)


@dataclass
class Manifest:
    """The .agentfish.json manifest."""

    version: str = "1.0"
    things: list[Thing] = field(default_factory=list)


def load_manifest(project_dir: Path) -> Manifest:
    """Load manifest from project directory, or return empty manifest."""
    manifest_path = project_dir / MANIFEST_FILE
    if not manifest_path.exists():
        return Manifest()
    data = json.loads(manifest_path.read_text(encoding="utf-8"))
    things = [Thing(**t) for t in data.get("things", [])]
    return Manifest(version=data.get("version", "1.0"), things=things)


def save_manifest(project_dir: Path, manifest: Manifest) -> None:
    """Save manifest to project directory."""
    manifest_path = project_dir / MANIFEST_FILE
    data = {"version": manifest.version, "things": [asdict(t) for t in manifest.things]}
    manifest_path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def add_thing(manifest: Manifest, thing: Thing) -> Manifest:
    """Add or replace a thing in the manifest."""
    manifest.things = [t for t in manifest.things if t.name != thing.name]
    manifest.things.append(thing)
    return manifest


def remove_thing(manifest: Manifest, name: str) -> tuple[Manifest, Thing | None]:
    """Remove a thing from the manifest by name. Returns the removed thing."""
    removed = None
    new_things = []
    for t in manifest.things:
        if t.name == name:
            removed = t
        else:
            new_things.append(t)
    manifest.things = new_things
    return manifest, removed


def find_thing(manifest: Manifest, name: str) -> Thing | None:
    """Find a thing in the manifest by name."""
    for t in manifest.things:
        if t.name == name:
            return t
    return None


def now_iso() -> str:
    """Return current UTC time in ISO format."""
    return datetime.now(timezone.utc).isoformat()
