"""Tests de la commande `doi` et de la forme DOI — offline par défaut."""

import pytest

from ratiss import ids, __main__ as cli


def test_forme_doi():
    assert ids.is_doi_form("10.5281/zenodo.6164620") is True
    assert ids.is_doi_form("10.1038/s41586-019-1666-5") is True
    assert ids.is_doi_form("9.1234/x") is False        # préfixe 10. requis
    assert ids.is_doi_form("10.1234") is False         # suffixe requis
    assert ids.is_doi_form("") is False


def test_cli_doi_forme_invalide_sans_reseau():
    # garde-fou offline : forme invalide → exit 1, aucun appel réseau
    assert cli.main(["doi", "pas-un-doi"]) == 1


@pytest.mark.network
def test_cli_doi_resout_un_doi_reel():
    assert cli.main(["doi", "10.5281/zenodo.6164620"]) == 0


@pytest.mark.network
def test_cli_doi_un_doi_mort_ne_resout_pas():
    # forme valide mais DOI inexistant → divergence, exit 1
    assert cli.main(["doi", "10.99999/zzz.nexiste.pas"]) == 1
