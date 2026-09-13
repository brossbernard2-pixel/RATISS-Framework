"""Tests des bornes de plausibilité physique — aucun réseau."""

from ratiss import bounds


def test_chsh_3_1_impossible():
    ok, reason = bounds.chsh_bound(3.1)
    assert ok is False
    assert "Tsirelson" in reason


def test_chsh_2_5_ok():
    ok, reason = bounds.chsh_bound(2.5)
    assert ok is True
    assert reason == ""


def test_chsh_borne_exacte_est_ok():
    ok, reason = bounds.chsh_bound(bounds.TSIRELSON)
    assert ok is True
    assert reason == ""


def test_chsh_negatif_ok():
    ok, reason = bounds.chsh_bound(-2.0)
    assert ok is True
    assert reason == ""


def test_chsh_non_fini_refuse():
    ok, reason = bounds.chsh_bound(float("nan"))
    assert ok is False
    assert "non finie" in reason
    ok, reason = bounds.chsh_bound(float("inf"))
    assert ok is False


def test_fidelity_borne():
    assert bounds.fidelity_bound(0.0)[0] is True
    assert bounds.fidelity_bound(1.0)[0] is True
    assert bounds.fidelity_bound(0.5)[0] is True
    assert bounds.fidelity_bound(1.0001)[0] is False
    assert bounds.fidelity_bound(-0.1)[0] is False


def test_probability_borne():
    assert bounds.probability_bound(0.0)[0] is True
    assert bounds.probability_bound(1.0)[0] is True
    assert bounds.probability_bound(0.75)[0] is True
    assert bounds.probability_bound(1.01)[0] is False
    assert bounds.probability_bound(-0.01)[0] is False


def test_counts_nonnegatifs():
    assert bounds.counts_nonnegatives({})[0] is True
    assert bounds.counts_nonnegatives({"00": 256, "11": 243})[0] is True
    assert bounds.counts_nonnegatives({"00": 256, "11": -1})[0] is False
    assert bounds.counts_nonnegatives({"00": 2.5})[0] is False
    assert bounds.counts_nonnegatives({"00": "256"})[0] is False