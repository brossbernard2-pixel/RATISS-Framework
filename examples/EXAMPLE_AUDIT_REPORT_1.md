RATISS audit report — every verdict below is a computed value.

- Target: RUN 1 — auto-rejeu https://raw.githubusercontent.com/jonathansearch/ratiss-audit-public/main
- Auditor: Équipe Rouge
- Date (UTC): 2026-09-13T01:18:00+00:00

| # | Check | Command | Expected | Obtained | Verdict |
|---:|---|---|---|---|---|
| 1 | fetch PUBLIC-AUDIT-REPORT-EN.md | `python -m ratiss audit --url https://raw.githubusercontent.com/jonathansearch/ratiss-audit-public/main/PUBLIC-AUDIT-REPORT-EN.md --sha256 2ef4f16cbbcf030f1a1df63142d0b27bffafdc5020b299bdf5cdfa76fd26229a` | 2ef4f16cbbcf030f1a1df63142d0b27bffafdc5020b299bdf5cdfa76fd26229a | 2ef4f16cbbcf030f1a1df63142d0b27bffafdc5020b299bdf5cdfa76fd26229a | OK (conforme) |
| 2 | fetch NOTICES-OSF-2026-09-12.md | `python -m ratiss audit --url https://raw.githubusercontent.com/jonathansearch/ratiss-audit-public/main/NOTICES-OSF-2026-09-12.md --sha256 f12f0aee1bb4045f93b5fe41801b0396599153ce9331e0565b9b7eebd4c59f7a` | f12f0aee1bb4045f93b5fe41801b0396599153ce9331e0565b9b7eebd4c59f7a | f12f0aee1bb4045f93b5fe41801b0396599153ce9331e0565b9b7eebd4c59f7a | OK (conforme) |
| 3 | fetch JOURNAL-DEVIATIONS.md | `python -m ratiss audit --url https://raw.githubusercontent.com/jonathansearch/ratiss-audit-public/main/JOURNAL-DEVIATIONS.md --sha256 c3b5a67de8da388e51b03eabb323de68f2278e326cd99ee25182669c43b404de` | c3b5a67de8da388e51b03eabb323de68f2278e326cd99ee25182669c43b404de | c3b5a67de8da388e51b03eabb323de68f2278e326cd99ee25182669c43b404de | OK (conforme) |
| 4 | fetch README.md | `python -m ratiss audit --url https://raw.githubusercontent.com/jonathansearch/ratiss-audit-public/main/README.md --sha256 8231043b8e9db09487faa8ab9507be2d3d79d145efa1aa17ab1b5d2f0f93ccba` | 8231043b8e9db09487faa8ab9507be2d3d79d145efa1aa17ab1b5d2f0f93ccba | 8231043b8e9db09487faa8ab9507be2d3d79d145efa1aa17ab1b5d2f0f93ccba | OK (conforme) |

Checks: 4 — conformes: 4, divergences: 0, non calculés: 0

Reproduction (R7) : chaque commande ci-dessus peut être rejouée par un étranger.
