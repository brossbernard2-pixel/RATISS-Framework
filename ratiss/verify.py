"""Primitives de vérification — le cœur méthodologique de RATISS.

Chaque fonction ici est un *test* qu'un étranger peut rejouer (R7).
Aucune ne produit de chiffre non calculé (R4).

Connaissances de domaine corrigées, journalisées le 2026-09-12 :
- un job ID IBM Quantum réel ressemble à ``d762omnq1anc738d2cj0``
  (20 caractères alphanumériques minuscules, cf. docs.quantum.ibm.com) ;
  ce N'EST PAS une chaîne hexadécimale de 24 caractères ;
- un hash SHA-256 est exactement 64 caractères hexadécimaux ;
- un GUID OSF est exactement 5 caractères alphanumériques minuscules
  (ex. ``wf7qm``, ``4867h``, ``u4aek``, ``6jzmb``).
"""

from __future__ import annotations

import hashlib
import re
import urllib.request

__all__ = [
    "sha256_hex",
    "sha256_file",
    "sha256_url",
    "is_sha256_hex",
    "is_osf_guid",
    "is_ibm_job_id",
    "check_hash_url",
]

_SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
_OSF_GUID_RE = re.compile(r"^[a-z0-9]{5}$")
_IBM_JOB_RE = re.compile(r"^[a-z0-9]{20}$")


def sha256_hex(data: bytes) -> str:
    """SHA-256 d'un octet-string, en hexadécimal minuscule."""
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: str) -> str:
    """SHA-256 d'un fichier local, lu par blocs (tient en mémoire faible)."""
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for bloc in iter(lambda: fh.read(1 << 16), b""):
            h.update(bloc)
    return h.hexdigest()


def sha256_url(url: str, timeout: int = 30) -> str:
    """SHA-256 du contenu servi à ``url`` (http, https ou file://).

    C'est la primitive R7 : « ce que le serveur sert » et non « ce que
    je crois avoir poussé ».
    """
    with urllib.request.urlopen(url, timeout=timeout) as resp:  # nosec: audit tool
        h = hashlib.sha256()
        while True:
            bloc = resp.read(1 << 16)
            if not bloc:
                break
            h.update(bloc)
    return h.hexdigest()


def is_sha256_hex(value: str) -> bool:
    """Vrai ssi ``value`` a la forme d'un SHA-256 hexadécimal complet."""
    return bool(_SHA256_RE.match(value or ""))


def is_osf_guid(value: str) -> bool:
    """Vrai ssi ``value`` a la forme d'un GUID OSF (5 alnum minuscules)."""
    return bool(_OSF_GUID_RE.match(value or ""))


def is_ibm_job_id(value: str) -> bool:
    """Vrai ssi ``value`` a la forme d'un job ID IBM Quantum (20 alnum minuscules).

    Historique : une précédente génération d'artefacts du labo affichait des
    « job IDs » sémantiques ou hexadécimaux de 24 caractères. Les deux formes
    sont fausses. Cette fonction est le garde-fou.
    """
    return bool(_IBM_JOB_RE.match(value or ""))


def check_hash_url(url: str, expected: str, timeout: int = 30) -> bool:
    """R7 en une fonction : le contenu servi à ``url`` a-t-il le hash attendu ?

    Renvoie un booléen calculé — jamais une assertion décorative.
    """
    if not is_sha256_hex(expected):
        raise ValueError(f"hash attendu malformé : {expected!r}")
    return sha256_url(url, timeout=timeout) == expected.lower()
