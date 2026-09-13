"""Configuration pytest du banc d'essai.

- Le marqueur ``network`` est enregistré : les tests qui exigent un accès
  réseau sont exclus par défaut de ``python -m pytest -q``.
- La passer en revue explicite (jamais de garanties "certifiées") reste
  cohérente avec R7 : la reproduction anonyme doit rester offline.
"""

from __future__ import annotations

import pytest


def pytest_configure(config: pytest.Config) -> None:
    config.addinivalue_line("markers", "network: requiert un accès réseau, hors suite offline")


def pytest_addoption(parser: pytest.Parser) -> None:
    parser.addoption(
        "--run-network",
        action="store_true",
        default=False,
        help="exécute aussi les tests marqués @pytest.mark.network",
    )


def pytest_collection_modifyitems(
    config: pytest.Config, items: list[pytest.Item]
) -> None:
    if config.getoption("--run-network"):
        return
    skip_network = pytest.mark.skip(reason="test réseau : lancer avec --run-network")
    for item in items:
        if "network" in item.keywords:
            item.add_marker(skip_network)