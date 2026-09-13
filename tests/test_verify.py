"""Tests des primitives — vecteurs connus, aucun réseau requis."""

import os
import tempfile

import pytest

from ratiss import verify


def test_sha256_vecteur_connue():
    # vecteur FIPS : sha256("abc")
    assert verify.sha256_hex(b"abc") == (
        "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad"
    )


def test_sha256_vide():
    assert verify.sha256_hex(b"") == (
        "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    )


def test_sha256_file_et_url_file_sont_egaux():
    with tempfile.TemporaryDirectory() as d:
        p = os.path.join(d, "artefact.bin")
        with open(p, "wb") as fh:
            fh.write(b"ratiss banc d'essai 2026-09-12")
        local = verify.sha256_file(p)
        servi = verify.sha256_url("file://" + p)
        assert local == servi
        assert verify.check_hash_url("file://" + p, local) is True
        assert verify.check_hash_url("file://" + p, "0" * 64) is False


def test_formes_sha256():
    assert verify.is_sha256_hex("a" * 64) is True
    assert verify.is_sha256_hex("A" * 64) is False          # majuscules : non
    assert verify.is_sha256_hex("a" * 63) is False          # trop court : non
    assert verify.is_sha256_hex("9f8a...3e41") is False     # tronqué : non
    assert verify.is_sha256_hex("") is False


def test_formes_guid_osf():
    for bon in ("wf7qm", "4867h", "u4aek", "6jzmb"):
        assert verify.is_osf_guid(bon) is True
    for mauvais in ("WF7QM", "wf7", "wf7qmq", "", "wf-qm"):
        assert verify.is_osf_guid(mauvais) is False


def test_formes_job_id_ibm():
    # exemples de format réel, docs.quantum.ibm.com + artefact public du labo
    assert verify.is_ibm_job_id("d762omnq1anc738d2cj0") is True
    assert verify.is_ibm_job_id("d9u47t0u5hac73agnhj0") is True
    # les deux formes fausses historiquement produites par le labo :
    assert verify.is_ibm_job_id("a" * 24) is False          # 24 hex : non
    assert verify.is_ibm_job_id("bell_run_2026") is False   # sémantique : non
    assert verify.is_ibm_job_id("") is False


def test_check_hash_refuse_un_hash_malforme():
    with pytest.raises(ValueError):
        verify.check_hash_url("file:///dev/null", "pas-un-hash")
