"""Shared pytest fixtures for the hybrid_kem test suite."""

import os
import secrets
from pathlib import Path

import pytest


@pytest.fixture
def random_bytes_32() -> bytes:
    """32 bytes of cryptographic randomness for test inputs."""
    return secrets.token_bytes(32)


@pytest.fixture
def kat_vectors_dir() -> Path:
    """Directory containing NIST KAT test vectors."""
    return Path(__file__).parent / "kat_vectors"


@pytest.fixture
def deterministic_seed() -> bytes:
    """Fixed seed for reproducible test runs.

    Use this when randomness must be deterministic — e.g., comparing
    outputs across implementations.
    """
    return bytes.fromhex(
        "00112233445566778899aabbccddeeff"
        "ffeeddccbbaa99887766554433221100"
    )


def pytest_collection_modifyitems(config, items):
    """Skip integration tests unless --integration is passed."""
    if config.getoption("--integration", default=False):
        return
    skip_integration = pytest.mark.skip(reason="need --integration option")
    for item in items:
        if "integration" in item.keywords:
            item.add_marker(skip_integration)


def pytest_addoption(parser):
    parser.addoption(
        "--integration",
        action="store_true",
        default=False,
        help="run integration tests (requires network for QRNG)",
    )
