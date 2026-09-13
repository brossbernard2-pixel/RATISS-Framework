#!/usr/bin/env python3
"""Générateur des fichiers d'exemple conformes au §4 du prompt.

Produit ``examples/EXAMPLE_AUDIT_REPORT_<n>.md``, chacun contenant la
commande exacte permettant à un étranger de rejouer le run (R7). Les hashs
et verdicts sont recalculés ici — rien n'est affiché qui n'ait été calculé.
"""

from __future__ import annotations

from datetime import datetime, timezone

from ratiss import bounds, report

AUDITOR = "Équipe Rouge"
DATE = datetime.now(timezone.utc).isoformat(timespec="seconds")

BASE = "https://raw.githubusercontent.com/jonathansearch/ratiss-audit-public/main"

RUN1 = [
    (
        "PUBLIC-AUDIT-REPORT-EN.md",
        "2ef4f16cbbcf030f1a1df63142d0b27bffafdc5020b299bdf5cdfa76fd26229a",
    ),
    (
        "NOTICES-OSF-2026-09-12.md",
        "f12f0aee1bb4045f93b5fe41801b0396599153ce9331e0565b9b7eebd4c59f7a",
    ),
    (
        "JOURNAL-DEVIATIONS.md",
        "c3b5a67de8da388e51b03eabb323de68f2278e326cd99ee25182669c43b404de",
    ),
    (
        "README.md",
        "8231043b8e9db09487faa8ab9507be2d3d79d145efa1aa17ab1b5d2f0f93ccba",
    ),
]


def make_run1() -> str:
    from ratiss import verify

    checks = []
    for fname, expected in RUN1:
        url = f"{BASE}/{fname}"
        checks.append(
            report.Check(
                name=f"fetch {fname}",
                command=f"python -m ratiss audit --url {url} --sha256 {expected}",
                expected_hash=expected,
                obtained_hash=verify.sha256_url(url),
            )
        )
    return report.render_report(
        f"RUN 1 — auto-rejeu {BASE}",
        checks,
        AUDITOR,
        DATE,
    )


def make_run2() -> str:
    record, key = "6164620", "README.md"
    from ratiss import verify

    api = f"https://zenodo.org/api/records/{record}"
    import json
    import urllib.request

    with urllib.request.urlopen(api, timeout=30) as resp:  # nosec
        files = json.loads(resp.read().decode("utf-8"))["files"]
    expected = next(f["checksum"].split(":")[-1] for f in files if f["key"] == key)
    file_url = f"https://zenodo.org/records/{record}/files/{key}"
    obtained = verify.hash_url(file_url, algo="md5")
    check = report.Check(
        name=f"zenodo record {record} / {key}",
        command=f"python -m ratiss audit-zenodo --record {record} --file {key}",
        expected_hash=expected,
        obtained_hash=obtained,
    )
    return report.render_report(
        f"RUN 2 — Zenodo record {record} / {key} (DOI 10.5281/zenodo.{record})",
        [check],
        AUDITOR,
        DATE,
    )


def make_run3() -> str:
    tsirelson = f"{bounds.TSIRELSON:.16f}"
    ok3, reason3 = bounds.chsh_bound(3.1)
    ok2, reason2 = bounds.chsh_bound(2.5)
    v3 = "OK" if ok3 else "IMPOSSIBLE"
    v2 = "OK" if ok2 else "IMPOSSIBLE"
    r3 = f"{v3}{(' — ' + reason3) if reason3 else ''}"
    r2 = f"{v2}{(' — ' + reason2) if reason2 else ''}"
    return "\n".join(
        [
            report.REPORT_HEADER,
            "",
            f"- Target: RUN 3 — plausibilité locale (borne de Tsirelson {tsirelson})",
            f"- Auditor: {AUDITOR}",
            f"- Date (UTC): {DATE}",
            "",
            "Commandes exactes rejouables (aucun réseau) :",
            "",
            "    python -m ratiss chsh 3.1",
            "    python -m ratiss chsh 2.5",
            "",
            "- 3.1 → " + r3,
            "- 2.5 → " + r2,
            "",
            "Verdict attendu : 3.1 → IMPOSSIBLE, 2.5 → OK.",
        ]
    )


def main() -> None:
    from pathlib import Path

    out = Path(__file__).resolve().parent
    (out / "EXAMPLE_AUDIT_REPORT_1.md").write_text(make_run1(), encoding="utf-8")
    (out / "EXAMPLE_AUDIT_REPORT_2.md").write_text(make_run2(), encoding="utf-8")
    (out / "EXAMPLE_AUDIT_REPORT_3.md").write_text(make_run3(), encoding="utf-8")
    print("Écrit : EXAMPLE_AUDIT_REPORT_{1,2,3}.md")


if __name__ == "__main__":
    main()