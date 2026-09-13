"""Bornes de plausibilité physique — R4.

Un chiffre publié doit être calculé ET plausible. Ce module fournit des
prédicats purs qui rejettent un nombre hors des bornes physiques sans essayer
de le « corriger ». Chaque prédicat renvoie ``(ok, reason)`` : ``reason`` est
vide quand ``ok`` est vrai, sinon une chaîne explicite justifiant le refus.
"""

from __future__ import annotations

import math

__all__ = [
    "TSIRELSON",
    "chsh_bound",
    "fidelity_bound",
    "probability_bound",
    "counts_nonnegatives",
]

TSIRELSON = 2.0 * math.sqrt(2.0)


def chsh_bound(value: float) -> tuple[bool, str]:
    """Borne de Tsirelson : |S| ≤ 2·√2 ≈ 2.8284271247461903.

    « 3.1 » est physiquement impossible pour un paramètre CHSH ; « 2.5 » est
    en deçà de la borne (donc plausible). Aucune tolérance d'arrondi : c'est
    une affirmation mathématique, pas une approximation.
    """
    if not math.isfinite(value):
        return False, f"valeur non finie : {value!r}"
    if abs(value) <= TSIRELSON:
        return True, ""
    return False, (
        f"|S| = {abs(value):.10f} dépasse la borne de Tsirelson "
        f"2·√2 = {TSIRELSON:.16f}"
    )


def fidelity_bound(value: float) -> tuple[bool, str]:
    """Fidélité : 0 ≤ F ≤ 1."""
    if not math.isfinite(value):
        return False, f"valeur non finie : {value!r}"
    if 0.0 <= value <= 1.0:
        return True, ""
    if value < 0.0:
        return False, f"fidélité négative : {value!r}"
    return False, f"fidélité > 1 : {value!r}"


def probability_bound(value: float) -> tuple[bool, str]:
    """Probabilité : 0 ≤ p ≤ 1."""
    if not math.isfinite(value):
        return False, f"valeur non finie : {value!r}"
    if 0.0 <= value <= 1.0:
        return True, ""
    if value < 0.0:
        return False, f"probabilité négative : {value!r}"
    return False, f"probabilité > 1 : {value!r}"


def counts_nonnegatives(counts: dict) -> tuple[bool, str]:
    """Tous les comptages sont des entiers ≥ 0.

    ``counts`` est un mapping {état : nombre}. Une valeur négative, non
    entière ou non numérique est refusée.
    """
    for etat, nb in counts.items():
        if isinstance(nb, bool) or not isinstance(nb, int):
            return False, f"comptage non entier pour {etat!r} : {nb!r}"
        if nb < 0:
            return False, f"comptage négatif pour {etat!r} : {nb!r}"
    return True, ""