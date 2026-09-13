"""Rapport d'audit et annexe de reproduction — R7.

Un rapport RATISS ne contient que des verdicts *calculés*. Chaque check doit
pouvoir être rejoué par un étranger avec la commande exacte donnée dans le
rapport. Un verdict non calculé est une exception, pas une chaîne vide.
"""

from __future__ import annotations

__all__ = [
    "REPORT_HEADER",
    "Check",
    "render_report",
    "render_verdict",
]

REPORT_HEADER = "RATISS audit report — every verdict below is a computed value."


def render_verdict(expected_hash: str | None, obtained_hash: str | None) -> tuple[str, str]:
    """Calcule ``(verdict, sym)`` à partir des hash attendu et obtenu.

    - expected==obtained → ``("conforme", "OK")``
    - hash fournis mais différents → ``("divergence", "KO")``
    - un hash attendu sans obtenu, ou inversement → ``("non calculé", "??")``
    - aucun des deux → ``("non calculé", "??")``

    ``sym`` sert au tableau ; ``verdict`` est le mot lisible.
    """
    if expected_hash is not None and obtained_hash is not None:
        if expected_hash.lower() == obtained_hash.lower():
            return "conforme", "OK"
        return "divergence", "KO"
    return "non calculé", "??"


class Check:
    """Un check d'audit : nom, commande rejouable (R7), hash attendu et obtenu.

    Tous les champs sont obligatoires. Un check sans résultat **calculé** ne
    doit pas être affiché ; ``render_report`` lève une ``ValueError`` si un
    ``obtained_hash`` manque, parce qu'un rapport n'affiche pas de « vide ».
    """

    def __init__(
        self,
        name: str,
        command: str,
        expected_hash: str,
        obtained_hash: str | None = None,
    ) -> None:
        if not name or not command or not expected_hash:
            raise ValueError("nom, commande et hash attendu sont obligatoires")
        self.name = name
        self.command = command
        self.expected_hash = expected_hash
        self.obtained_hash = obtained_hash

    def verdict(self) -> tuple[str, str]:
        return render_verdict(self.expected_hash, self.obtained_hash)


def render_report(
    target: str,
    checks: list[Check],
    auditor: str,
    date_utc: str,
) -> str:
    """Rendu Markdown du rapport d'audit.

    Commence par ``REPORT_HEADER`` ; chaque check affiche sa commande exacte,
    le hash attendu, le hash obtenu et son verdict. Lève si un check n'a pas
    de hash obtenu (verdict non calculé = exception).
    """
    lines = [REPORT_HEADER, "", f"- Target: {target}", f"- Auditor: {auditor}", f"- Date (UTC): {date_utc}", ""]
    rows = []
    for check in checks:
        if check.obtained_hash is None:
            raise ValueError(
                f"verdict non calculé pour {check.name!r} : obtained_hash manquant"
            )
        verdict, sym = check.verdict()
        rows.append((check.name, check.command, check.expected_hash, check.obtained_hash, verdict, sym))

    lines.append("| # | Check | Command | Expected | Obtained | Verdict |")
    lines.append("|---:|---|---|---|---|---|")
    for i, (name, command, expected, obtained, verdict, sym) in enumerate(rows, 1):
        lines.append(f"| {i} | {name} | `{command}` | {expected} | {obtained} | {sym} ({verdict}) |")

    non_computed = [r for r in rows if r[4] == "non calculé"]
    lines.append("")
    lines.append(f"Checks: {len(rows)} — conformes: {sum(1 for r in rows if r[4] == 'conforme')}, divergences: {sum(1 for r in rows if r[4] == 'divergence')}, non calculés: {len(non_computed)}")
    lines.append("")
    lines.append("Reproduction (R7) : chaque commande ci-dessus peut être rejouée par un étranger.")
    return "\n".join(lines) + "\n"