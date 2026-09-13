"""Point d'entrée en ligne de commande — R7.

Une seule commande rejouable par un étranger :

- ``python -m ratiss audit --url <url> --sha256 <hash>``
- ``python -m ratiss audit-zenodo --record <id> --file <key>``
- ``python -m ratiss chsh <value>``
- ``python -m ratiss doi <doi>``

Sortie : un rapport minimal + code de sortie 0 (conforme) ou 1 (divergence).
Stdlib uniquement.
"""

from __future__ import annotations

import argparse
import json
import sys
import urllib.parse
import urllib.request
from datetime import datetime, timezone

from ratiss import bounds, ids, report, verify

_ALLOWED_HASHES = {"sha256", "md5"}


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _print_report(title: str, checks: list[report.Check], auditor: str) -> None:
    body = report.render_report(
        title,
        checks,
        auditor=auditor,
        date_utc=utc_now(),
    )
    print(body)


def total_verdict(checks: list[report.Check]) -> str:
    """Verdict global : conforme si tous les checks sont conformes."""
    for check in checks:
        verdict, _ = check.verdict()
        if verdict != "conforme":
            return "divergence"
    return "conforme"


def cmd_audit(args: argparse.Namespace) -> int:
    url: str = args.url
    expected: str = args.sha256
    check = report.Check(
        name=f"fetch {url}",
        command=f"python -m ratiss audit --url {url} --sha256 {expected}",
        expected_hash=expected,
        obtained_hash=verify.sha256_url(url),
    )
    checks = [check]
    _print_report(url, checks, auditor="banc d'essai")
    return 0 if total_verdict(checks) == "conforme" else 1


def cmd_chsh(args: argparse.Namespace) -> int:
    value = args.value[0]
    try:
        flt = float(value)
    except ValueError:
        print(f"chsh : valeur invalide {value!r}")
        return 1
    ok, reason = bounds.chsh_bound(flt)
    verdict = "OK (conforme)" if ok else "IMPOSSIBLE (divergence)"
    print(f"chsh {value} -> |S| ≤ 2·√2 ≈ {bounds.TSIRELSON:.16f} : {verdict}")
    if reason:
        print(f"  raison: {reason}")
    return 0 if ok else 1


def cmd_audit_zenodo(args: argparse.Namespace) -> int:
    record: str = args.record
    key: str = args.file
    checks: list[report.Check] = []

    # 1) le checksum MD5 *publié* par Zenodo, lu depuis l'API records
    api_url = f"https://zenodo.org/api/records/{record}"
    try:
        with urllib.request.urlopen(api_url, timeout=30) as resp:  # nosec
            data = json.loads(resp.read().decode("utf-8"))
    except Exception as exc:  # pragma: no cover - réseau
        print(f"audit-zenodo : impossible de lire l'API Zenodo : {exc}")
        return 1

    expected_md5 = None
    try:
        for f in data["files"]:
            if f["key"] == key:
                expected_md5 = f["checksum"].split(":")[-1]
                break
    except (KeyError, TypeError):
        pass
    if expected_md5 is None:
        print(f"audit-zenodo : fichier {key!r} introuvable sur le record {record}")
        return 1

    # 2) le fichier servi, hashé avec le même algorithme que la valeur publiée
    file_url = f"https://zenodo.org/records/{record}/files/{key}"
    file_url = urllib.parse.quote(file_url, safe=":/")
    obtained_md5 = verify.hash_url(file_url, algo="md5")

    checks.append(
        report.Check(
            name=f"zenodo record {record} / {key}",
            command=(
                f"python -m ratiss audit-zenodo --record {record} --file {key}"
            ),
            expected_hash=expected_md5,
            obtained_hash=obtained_md5,
        )
    )
    _print_report(f"zenodo record {record} / {key}", checks, auditor="banc d'essai")
    return 0 if total_verdict(checks) == "conforme" else 1


def cmd_doi(args: argparse.Namespace) -> int:
    doi: str = args.doi[0]

    if not ids.is_doi_form(doi):
        print(f"doi {doi} -> forme invalide (attendu 10.XXXX/suffixe)")
        return 1
    ok = ids.doi_resolves(doi)
    verdict = "RESOUT (conforme)" if ok else "NE RESOUT PAS (divergence)"
    print(f"doi {doi} -> {verdict}")
    print("  portée : résolution de l'identifiant seulement (Hérité 2 :"
          " un identifiant enregistré n'est pas une revalidation en temps réel)")
    return 0 if ok else 1


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="ratiss",
        description="RATISS audit tool — every verdict below is a computed value (R7).",
    )
    sub = parser.add_subparsers(dest="command")

    audit = sub.add_parser("audit", help="vérifie un URL contre un hash sha256")
    audit.add_argument("--url", required=True)
    audit.add_argument("--sha256", required=True)
    audit.set_defaults(func=cmd_audit)

    az = sub.add_parser("audit-zenodo", help="vérifie un fichier Zenodo contre son checksum publié")
    az.add_argument("--record", required=True)
    az.add_argument("--file", required=True)
    az.set_defaults(func=cmd_audit_zenodo)

    chsh = sub.add_parser("chsh", help="vérifie la borne de Tsirelson d'une valeur")
    chsh.add_argument("value", nargs=1)
    chsh.set_defaults(func=cmd_chsh)

    doi = sub.add_parser("doi", help="vérifie la résolution d'un DOI (Hérité 2)")
    doi.add_argument("doi", nargs=1)
    doi.set_defaults(func=cmd_doi)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if not getattr(args, "command", None):
        parser.print_help()
        return 2
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())