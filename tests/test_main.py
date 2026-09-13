"""Tests de la commande unique — audit/chsh/audit-zenodo.

``audit`` et ``chsh`` sont testés avec des URL file:// et des valeurs
déterministes. ``audit-zenodo`` est testé hors-ligne en remplaçant
``urllib.request.urlopen`` (aucun réseau réel pendant la suite) — c'est le
seul point où un faux réseau est nécessaire.
"""

import hashlib
import io
import json
import os
import urllib.request

from ratiss import __main__ as m


def _file_url(tmp_path, content: bytes) -> str:
    p = os.path.join(tmp_path, "artefact.bin")
    with open(p, "wb") as fh:
        fh.write(content)
    return "file://" + p


def test_audit_ok(tmp_path):
    content = b"contenu conforme"
    url = _file_url(tmp_path, content)

    h = hashlib.sha256(content).hexdigest()
    assert m.main(["audit", "--url", url, "--sha256", h]) == 0


def test_audit_divergence(tmp_path):
    content = b"contenu conforme"
    url = _file_url(tmp_path, content)
    assert m.main(["audit", "--url", url, "--sha256", "b" * 64]) == 1


def test_chsh_ok():
    assert m.main(["chsh", "2.5"]) == 0


def test_chsh_impossible():
    assert m.main(["chsh", "3.1"]) == 1


def test_chsh_valeur_invalide(tmp_path):
    assert m.main(["chsh", "abc"]) == 1


def test_audit_zenodo_hors_ligne(tmp_path, monkeypatch):
    """Simule l'API Zenodo (checksum publié) puis le fichier servi."""

    md5_publie = "f55640062b3346801576aee6f624a20f"  # md5("contenu du fichier zenodo")
    contenu_fichier = b"contenu du fichier zenodo"

    class FakeResponse:
        """Reproduit urlopen : un flux qui se vide, puis renvoie b'' (EOF)."""

        def __init__(self, payload: bytes):
            self._buf = payload

        def read(self, *a, **k):
            out, self._buf = self._buf, b""
            return out

        def __enter__(self):
            return self

        def __exit__(self, *a, **k):
            return False

    records = {
        "https://zenodo.org/api/records/6164620": json.dumps(
            {"files": [{"key": "README.md", "checksum": "md5:" + md5_publie}]}
        ).encode("utf-8"),
        "https://zenodo.org/records/6164620/files/README.md": contenu_fichier,
    }

    def fake_urlopen(url, timeout=None):
        for key, payload in records.items():
            if key in url:
                return FakeResponse(payload)
        raise urllib.error.URLError(f"pas de réponse simulée pour {url}")

    monkeypatch.setattr(urllib.request, "urlopen", fake_urlopen)
    assert m.main(["audit-zenodo", "--record", "6164620", "--file", "README.md"]) == 0


def test_aucune_commande_affiche_aide():
    assert m.main([]) == 2