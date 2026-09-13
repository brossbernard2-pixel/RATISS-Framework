"""Tests du rendu de rapport — aucun réseau, vérifie le contrat R7."""

import pytest

from ratiss import report

DATE = "2026-09-13T12:00:00+00:00"


def test_verdict_conforme():
    v, sym = report.render_verdict("a" * 64, "A" * 64)
    assert v == "conforme"
    assert sym == "OK"


def test_verdict_divergence():
    expected = "a" * 64
    obtained = "b" * 64
    assert report.render_verdict(expected, obtained) == ("divergence", "KO")


def test_verdict_non_calcule():
    assert report.render_verdict("a" * 64, None) == ("non calculé", "??")
    assert report.render_verdict(None, "a" * 64) == ("non calculé", "??")
    assert report.render_verdict(None, None) == ("non calculé", "??")


def test_render_report_commence_par_len_tete_exacte():
    checks = [
        report.Check("GHZ ideal", "ratiss audit --url … --sha256 …", "a" * 64, "a" * 64)
    ]
    out = report.render_report("exemple", checks, "Rouge", DATE)
    assert out.startswith(report.REPORT_HEADER)


def test_render_report_produit_les_champs_de_chaque_check():
    expected = "a" * 64
    obtained = "a" * 64
    checks = [report.Check("GHZ ideal", "ratiss audit …", expected, obtained)]
    out = report.render_report("exemple", checks, "Rouge", DATE)
    assert "GHZ ideal" in out
    assert "ratiss audit …" in out
    assert expected in out
    assert "OK (conforme)" in out


def test_render_report_refuse_un_verdict_non_calcule():
    checks = [report.Check("GHZ ideal", "ratiss audit …", "a" * 64)]
    with pytest.raises(ValueError):
        report.render_report("exemple", checks, "Rouge", DATE)


def test_render_report_refuse_un_check_malforme():
    with pytest.raises(ValueError):
        report.Check("", "commande", "a" * 64)
    with pytest.raises(ValueError):
        report.Check("nom", "", "a" * 64)
    with pytest.raises(ValueError):
        report.Check("nom", "commande", "")