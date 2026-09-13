"""Tests du scellé de manifeste — aucun réseau, vecteurs déterministes."""

import pytest

from ratiss import seal


def test_scelle_puis_verifie_ok():
    params = {"rule_version": "R4", "params": {"shots": 1}, "target": "banc"}
    assert seal.verify_manifest(params, seal.seal_manifest(params)) is True


def test_un_parametre_modifie_apres_scelle_echeoue():
    params = {"rule_version": "R4", "params": {"shots": 1}, "target": "banc"}
    s = seal.seal_manifest(params)
    change = dict(params)
    change["params"] = {"shots": 2}
    assert seal.verify_manifest(change, s) is False


def test_ordre_des_cles_n_importe_pas():
    a = {"alpha": 1, "beta": 2, "gamma": {"x": 1, "y": 2}}
    b = {"gamma": {"y": 2, "x": 1}, "beta": 2, "alpha": 1}
    assert seal.seal_manifest(a) == seal.seal_manifest(b)


def test_separateurs_stricts_et_utf8():
    # le JSON canonique est : {"k":"v"} sans espace, encodé utf-8
    canon = seal.canonical_json({"k": "v"})
    assert canon == b'{"k":"v"}'
    assert isinstance(seal.seal_manifest({"k": "v"}), str)
    assert len(seal.seal_manifest({"k": "v"})) == 64


def test_chaine_vide_premier_jalon_du_journal():
    params = {"target": "journal", "author": "Rouge"}
    s = seal.seal_manifest(params)
    assert s != "0" * 64
    assert seal.verify_manifest({"target": "journal", "author": "Rouge"}, s) is True