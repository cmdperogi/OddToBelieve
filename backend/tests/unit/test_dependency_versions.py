"""Unit tests verifying STORY-18 (coordinated dependency bump clears starlette/python-multipart CVEs)."""

from importlib.metadata import version

from packaging.version import Version


def test_fastapi_meets_minimum_secure_version() -> None:
    assert Version(version("fastapi")) >= Version("0.137.1")


def test_starlette_meets_minimum_secure_version() -> None:
    """fastapi>=0.137.1 must resolve a starlette free of CVE-2026-54283/54282/48817/48818."""
    assert Version(version("starlette")) >= Version("1.3.1")


def test_python_multipart_meets_minimum_secure_version() -> None:
    """Must clear CVE-2026-53538/53539/53540 disclosed against 0.0.27-0.0.30."""
    assert Version(version("python-multipart")) >= Version("0.0.31")


def test_pydantic_meets_minimum_required_by_fastapi() -> None:
    assert Version(version("pydantic")) >= Version("2.9.0")
