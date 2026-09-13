"""Tests des identifiants réels — la résolution DOI est marquée network."""

import pytest

from ratiss import ids, verify


def test_reexporte_les_formes_depuis_verify():
    assert ids.is_osf_guid is verify.is_osf_guid
    assert ids.is_ibm_job_id is verify.is_ibm_job_id


def test_forme_job_id_ibm_reference_officielle():
    # docs.quantum.ibm.com/guides/save-jobs — format réel, pas du hex 24
    assert ids.is_ibm_job_id("d762omnq1anc738d2cj0") is True
    assert ids.is_ibm_job_id("d9u47t0u5hac73agnhj0") is True
    assert ids.is_ibm_job_id("a" * 24) is False
    assert ids.is_ibm_job_id("bell_run_2026") is False


def test_formes_guid_osf():
    assert ids.is_osf_guid("6jzmb") is True
    assert ids.is_osf_guid("WF7QM") is False


@pytest.mark.network
def test_doi_resout_un_doi_reel():
    # DOI publié par le labo (la résolution ne prouve pas le contenu,
    # seulement que l'identifiant pointe encore quelque part)
    assert ids.doi_resolves("10.17605/OSF.IO/6JZMB") is True


@pytest.mark.network
def test_doi_invalide_ne_resout_pas():
    assert ids.doi_resolves("10.9999/DOI-INEXISTANT-2026-xyz") is False