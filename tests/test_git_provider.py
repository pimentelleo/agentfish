"""Tests for agentfish git_provider module."""

from agentfish.git_provider import parse_repo_ref


def test_parse_github_shorthand():
    ref = parse_repo_ref("owner/repo")
    assert ref.url == "https://github.com/owner/repo.git"
    assert ref.branch is None
    assert ref.name == "repo"


def test_parse_github_shorthand_with_branch():
    ref = parse_repo_ref("owner/repo#main")
    assert ref.url == "https://github.com/owner/repo.git"
    assert ref.branch == "main"
    assert ref.name == "repo"


def test_parse_github_url():
    ref = parse_repo_ref("https://github.com/owner/repo")
    assert ref.url == "https://github.com/owner/repo"
    assert ref.branch is None
    assert ref.name == "repo"


def test_parse_github_url_with_branch():
    ref = parse_repo_ref("https://github.com/owner/repo#develop")
    assert ref.url == "https://github.com/owner/repo"
    assert ref.branch == "develop"


def test_parse_ado_url():
    ref = parse_repo_ref("https://dev.azure.com/org/project/_git/myrepo")
    assert ref.url == "https://dev.azure.com/org/project/_git/myrepo"
    assert ref.name == "myrepo"


def test_parse_ado_url_with_branch():
    ref = parse_repo_ref("https://dev.azure.com/org/project/_git/myrepo#feature")
    assert ref.url == "https://dev.azure.com/org/project/_git/myrepo"
    assert ref.branch == "feature"
    assert ref.name == "myrepo"


def test_parse_gitlab_url():
    ref = parse_repo_ref("https://gitlab.com/group/repo")
    assert ref.url == "https://gitlab.com/group/repo"
    assert ref.name == "repo"


def test_parse_git_suffix():
    ref = parse_repo_ref("https://github.com/owner/repo.git")
    assert ref.name == "repo"
