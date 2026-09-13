"""Tests du journal des déviations — chaîne intacte, tronquée, altérée."""

import json
import os

from ratiss import journal

DATE = "2026-09-13T00:00:00+00:00"


def _ajoute_trois(tmp_path):
    p = os.path.join(tmp_path, "journal.jsonl")
    journal.append_entry(p, "Rouge", "entrée 1", date_utc=DATE)
    journal.append_entry(p, "Rouge", "entrée 2", date_utc=DATE)
    journal.append_entry(p, "Chef", "entrée 3", date_utc=DATE)
    return p


def test_creer_une_chaene_valide(tmp_path):
    p = os.path.join(tmp_path, "journal.jsonl")
    e = journal.append_entry(p, "Rouge", "première entrée", date_utc=DATE)
    assert e["index"] == 1
    assert e["prev_hash"] == "0" * 64
    assert len(e["hash"]) == 64
    assert journal.verify_chain(p) is True
    ent = journal.read_chain(p)
    assert len(ent) == 1
    assert ent[0]["text"] == "première entrée"


def test_chaene_de_trois_entrees_valide(tmp_path):
    p = _ajoute_trois(tmp_path)
    assert journal.verify_chain(p) is True
    ent = journal.read_chain(p)
    assert [e["index"] for e in ent] == [1, 2, 3]
    assert ent[1]["prev_hash"] == ent[0]["hash"]
    assert ent[2]["prev_hash"] == ent[1]["hash"]


def test_chaene_tronquee_detectee(tmp_path):
    """Couper la chaîne *au milieu* (garder entrées 1 et 3) brise le chaînage.

    La propriété d'une chaîne de journal est : supprimer la dernière entrée
    n'est pas une altération (aucun lien ne la référence) ; supprimer une
    entrée intermédiaire casse le ``prev_hash`` de la suivante.
    """
    p = _ajoute_trois(tmp_path)
    ent = journal.read_chain(p)
    with open(p, "w", encoding="utf-8") as fh:
        for e in (ent[0], ent[2]):  # on supprime l'entrée 2 au milieu
            fh.write(json.dumps(e, sort_keys=True) + "\n")
    assert journal.verify_chain(p) is False


def test_chaene_alteree_au_milieu_detectee(tmp_path):
    p = _ajoute_trois(tmp_path)
    ent = journal.read_chain(p)
    # altérer le texte de l'entrée 2 : son hash ne correspond plus
    ent[1]["text"] = "modifié après mesure"
    with open(p, "w", encoding="utf-8") as fh:
        for e in ent:
            fh.write(json.dumps(e, sort_keys=True) + "\n")
    assert journal.verify_chain(p) is False


def test_journal_inexistant_est_vide(tmp_path):
    p = os.path.join(tmp_path, "absent.jsonl")
    assert journal.verify_chain(p) is True
    assert journal.read_chain(p) == []