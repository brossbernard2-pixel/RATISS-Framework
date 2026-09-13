"""Journal des déviations chaîné — R5.

Toute modification d'un manifeste scellé après mesure est une déviation :
elle est consignée ici, jamais silencieuse. Chaque entrée porte le hash de la
précédente (`prev_hash`), ce qui rend une altération au milieu de la chaîne
détectable. Le stockage est en JSON Lines : une entrée par ligne.
"""

from __future__ import annotations

import hashlib
import json
import os
from datetime import datetime, timezone

__all__ = ["entry_hash", "append_entry", "verify_chain", "read_chain"]

_STORAGE_SEPARATORS = (",", ":")


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def entry_hash(entry: dict) -> str:
    """SHA-256 de l'entrée en JSON canonique (clés triées, séparateurs stricts).

    Le champ ``hash`` de l'entrée est volontairement exclu, sinon le hash de
    l'entrée dépendrait de lui-même. ``prev_hash`` y est inclus, ce qui lie
    chaque entrée à la précédente.
    """
    body = {k: v for k, v in entry.items() if k != "hash"}
    payload = json.dumps(
        body, sort_keys=True, separators=_STORAGE_SEPARATORS
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def append_entry(path: str, author: str, text: str, date_utc: str | None = None) -> dict:
    """Ajoute une entrée au journal ``path`` et renvoie l'entrée complète.

    L'index est auto-incrémenté ; ``prev_hash`` est le hash de la dernière
    entrée existante, ou ``"0"*64`` pour la première. La date par défaut est
    l'instant UTC courant ; la passer explicitement rend le test déterministe.
    """
    entries = read_chain(path)
    prev_hash = entries[-1]["hash"] if entries else "0" * 64
    entry = {
        "index": len(entries) + 1,
        "date_utc": date_utc or _utc_now(),
        "author": author,
        "text": text,
        "prev_hash": prev_hash,
    }
    h = entry_hash(entry)
    record = dict(entry)
    record["hash"] = h
    payload = json.dumps(record, sort_keys=True, separators=_STORAGE_SEPARATORS)
    with open(path, "a", encoding="utf-8") as fh:
        fh.write(payload + "\n")
    return record


def read_chain(path: str) -> list[dict]:
    """Lit toutes les entrées du journal ``path``, dans l'ordre."""
    if not os.path.exists(path):
        return []
    out = []
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            out.append(json.loads(line))
    return out


def verify_chain(path: str) -> bool:
    """Vrai ssi la chaîne est intacte : liens ``prev_hash`` et hashs valides.

    Vérifie chaque entrée dans l'ordre : le hash de l'entrée *i* (champ créé
    par ``entry_hash``, sans le champ ``hash``) doit égaler son champ
    ``hash``, et son ``prev_hash`` doit égaler (ou ``"0"*64`` pour la
    première) le hash de l'entrée précédente. Toute insertion, suppression
    ou altération casse l'un de ces liens.
    """
    entries = read_chain(path)
    if not entries:
        return True
    if entries[0].get("prev_hash") != "0" * 64:
        return False
    for i, entry in enumerate(entries):
        if entry.get("hash") != entry_hash(entry):
            return False
        if i > 0 and entry.get("prev_hash") != entries[i - 1]["hash"]:
            return False
    return True