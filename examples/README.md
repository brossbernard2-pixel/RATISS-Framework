# Exemples — trois runs réels de la couche 1

Trois rapports d'audit *réels*, générés via `ratiss/report.py`
(`examples/generate_example_reports.py`), chacun au format exigé
`EXAMPLE_AUDIT_REPORT_<n>.md`. Chaque rapport contient la commande exacte
permettant à un étranger de rejouer le run (R7) : un verdict n'existe que
s'il a été calculé.

Génération (rejouable) :

    PYTHONPATH=. python3 examples/generate_example_reports.py

## `EXAMPLE_AUDIT_REPORT_1.md` — RUN 1, auto-rejeu du dépôt public

Les 4 fichiers de `jonathansearch/ratiss-audit-public`, rejoués par
`python -m ratiss audit` contre les hash SHA-256 publiés. Verdict : 4/4
conformes.

## `EXAMPLE_AUDIT_REPORT_2.md` — RUN 2, cible externe réelle (Zenodo)

Le fichier `README.md` du record Zenodo 6164620
(DOI 10.5281/zenodo.6164620), comparé au checksum MD5 publié par l'API
Zenodo. Verdict : conforme.

## `EXAMPLE_AUDIT_REPORT_3.md` — RUN 3, plausibilité (fixture locale)

Bornes de Tsirelson via `python -m ratiss chsh` : `3.1` → IMPOSSIBLE
(exit 1), `2.5` → OK (exit 0). Aucun réseau.

## Portée d'un verdict

Un verdict conforme signifie : le hash recalculé localement coïncide avec le
hash déclaré. Cela ne prouve ni le contenu scientifique ni la fraîcheur d'un
lien (Hérité 2). La reproduction reste anonyme et offline — les tests réseau
du banc sont marqués `@pytest.mark.network` et exclus de la suite par défaut.