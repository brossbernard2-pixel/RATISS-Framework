"""Scellé de manifeste — R5.

Un manifeste scellé fige les paramètres d'un run (prompt, paramètres,
cible, règle) avant la mesure. Toute modification après scellé doit être
journalisée comme déviation (R5). Le scellé ne prouve pas une valeur : il
prouve qu'un paramètre a changé après figeage.
"""

from __future__ import annotations

import hashlib
import json

__all__ = ["canonical_json", "seal_manifest", "verify_manifest"]


def canonical_json(params: dict) -> bytes:
    """Représentation JSON canonique UTF-8 : clés triées, séparateurs stricts.

    ``json.dumps`` (non utilisé ici) insère des espaces et préserve l'ordre
    d'insertion des clés : deux dictionnaires équivalents produiraient des
    octets différents. La forme canonique assure qu'un même manifeste scellé
    par deux machines produit le même hash.
    """
    return json.dumps(
        params,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
    ).encode("utf-8")


def seal_manifest(params: dict) -> str:
    """SHA-256 du manifeste ``params`` encodé en JSON canonique."""
    return hashlib.sha256(canonical_json(params)).hexdigest()


def verify_manifest(params: dict, seal: str) -> bool:
    """Vrai ssi le scellé re-calculé de ``params`` vaut ``seal``.

    Usage (R5) : on scelle avant mesure, on re-vérifie au moment de publier.
    Un ``False`` est une déviation à journaliser — jamais une valeur à
    contourner.
    """
    return seal_manifest(params) == seal.lower()