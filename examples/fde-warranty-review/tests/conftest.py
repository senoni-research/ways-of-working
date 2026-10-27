import socket

import pytest

from warranty_review.workflow import Workbench


@pytest.fixture(autouse=True)
def no_network(monkeypatch):
    monkeypatch.setenv("LANGSMITH_TRACING", "false")
    monkeypatch.setenv("LANGCHAIN_TRACING_V2", "false")
    real_connect = socket.socket.connect

    def refuse(sock, address):
        if sock.family in (socket.AF_INET, socket.AF_INET6):
            raise AssertionError(f"a test tried to open a network connection to {address!r}")
        return real_connect(sock, address)

    monkeypatch.setattr(socket.socket, "connect", refuse)


@pytest.fixture
def state_dir(tmp_path):
    return tmp_path / "state"


@pytest.fixture
def bench(state_dir):
    with Workbench(state_dir) as opened:
        yield opened
