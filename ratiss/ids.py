"""Identifiants réels vs décoratifs — Hérité 2.

Un identifiant *enregistré* n'est pas une revalidation en temps réel. Un DOI
peut résoudre aujourd'hui et mourir demain ; un job ID IBM peut exister sans
être rejouable. Ce module (1) vérifie les *formes* via les primitives de
``verify``, et (2) résout un DOI contre l'API publique des handles — mais le
test réseau est volontairement hors de la suite offline.

La référence de format de job ID IBM est la doc officielle
(docs.quantum.ibm.com/guides/save-jobs) : 20 caractères alphanumériques
minuscules, ex. ``d762omnq1anc738d2cj0``. Ce n'est PAS de l'hexadécimal sur
24 caractères.
"""

from __future__ import annotations

import urllib.parse
import urllib.request

from ratiss.verify import is_osf_guid, is_ibm_job_id  # noqa: F401 (ré-export)

__all__ = ["doi_resolves", "is_osf_guid", "is_ibm_job_id"]


def doi_resolves(doi: str, timeout: int = 30) -> bool:
    """Vrai ssi l'API des handles DOI répond à ``doi`` avec un état actif.

    L'API officielle ``https://doi.org/api/handles/{doi}`` retourne
    ``responseCode == 1`` lorsque le DOI existe et résout. Résoudre un DOI ne
    prouve pas le contenu : cela prouve seulement que l'identifiant pointe
    encore quelque part aujourd'hui (Hérité 2).
    """
    quoted = urllib.parse.quote(doi, safe="")
    url = f"https://doi.org/api/handles/{quoted}"
    try:
        with urllib.request.urlopen(url, timeout=timeout) as resp:  # nosec
            import json

            data = json.loads(resp.read().decode("utf-8"))
    except Exception:
        return False
    return data.get("responseCode") == 1