"""Tests for agentfish manifest module."""

import json
import tempfile
from pathlib import Path

from agentfish.manifest import (
    Manifest,
    Thing,
    add_thing,
    find_thing,
    load_manifest,
    remove_thing,
    save_manifest,
)


def test_load_empty_manifest():
    with tempfile.TemporaryDirectory() as tmp:
        m = load_manifest(Path(tmp))
        assert m.version == "1.0"
        assert m.things == []


def test_save_and_load_manifest():
    with tempfile.TemporaryDirectory() as tmp:
        d = Path(tmp)
        m = Manifest(things=[Thing(name="test", source="owner/repo", files=["AGENTS.md"])])
        save_manifest(d, m)
        loaded = load_manifest(d)
        assert len(loaded.things) == 1
        assert loaded.things[0].name == "test"
        assert loaded.things[0].files == ["AGENTS.md"]


def test_add_thing():
    m = Manifest()
    t = Thing(name="foo", source="a/b", files=["x.md"])
    m = add_thing(m, t)
    assert len(m.things) == 1
    assert m.things[0].name == "foo"


def test_add_thing_replaces_existing():
    m = Manifest(things=[Thing(name="foo", source="a/b", files=["old.md"])])
    t = Thing(name="foo", source="a/b", files=["new.md"])
    m = add_thing(m, t)
    assert len(m.things) == 1
    assert m.things[0].files == ["new.md"]


def test_remove_thing():
    m = Manifest(things=[Thing(name="a", source="x"), Thing(name="b", source="y")])
    m, removed = remove_thing(m, "a")
    assert removed is not None
    assert removed.name == "a"
    assert len(m.things) == 1
    assert m.things[0].name == "b"


def test_remove_nonexistent():
    m = Manifest(things=[Thing(name="a", source="x")])
    m, removed = remove_thing(m, "z")
    assert removed is None
    assert len(m.things) == 1


def test_find_thing():
    m = Manifest(things=[Thing(name="a", source="x"), Thing(name="b", source="y")])
    assert find_thing(m, "a") is not None
    assert find_thing(m, "b") is not None
    assert find_thing(m, "c") is None


def test_manifest_json_format():
    with tempfile.TemporaryDirectory() as tmp:
        d = Path(tmp)
        m = Manifest(things=[Thing(name="test", source="x", branch="main", files=["a.md"])])
        save_manifest(d, m)
        raw = json.loads((d / ".agentfish.json").read_text())
        assert raw["version"] == "1.0"
        assert raw["things"][0]["branch"] == "main"
