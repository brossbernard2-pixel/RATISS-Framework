# Exemples — trois runs réels de la couche 1

Ces rapports sont des traces *réelles* du banc d'essai (RATISS Framework,
couche 1). Chaque commande figure dans le rapport et reste rejouable par un
étranger (R7) : un verdict n'existe que s'il a été calculé.

## RUN 1 — auto-rejeu du dépôt public `jonathansearch/ratiss-audit-public`

Les 4 fichiers de l'espace public, rejoués par `python -m ratiss audit`
contre les hash SHA-256 publiés dans le dossier de travail. Verdict : 4/4
conformes.

- `PUBLIC-AUDIT-REPORT-EN.md`
- `NOTICES-OSF-2026-09-12.md`
- `JOURNAL-DEVIATIONS.md`
- `README.md`

Commande type :

    python -m ratiss audit --url https://raw.githubusercontent.com/jonathansearch/ratiss-audit-public/main/README.md --sha256 8231043b8e9db09487faa8ab9507be2d3d79d145efa1aa17ab1b5d2f0f93ccba

## RUN 2 — Zenodo record 6164620

Rejeu du fichier `README.md` du record Zenodo 6164620 contre le checksum MD5
publié par l'API Zenodo. Verdict : conforme.

    python -m ratiss audit-zenodo --record 6164620 --file README.md

## RUN 3 — borne de Tsirelson (commandes chsh)

Les trois cas du prompt : valeur impossible (3.1, exit 1), valeur plausible
(2.5, exit 0), borne exacte (2·√2, exit 0).

    python -m ratiss chsh 3.1
    python -m ratiss chsh 2.5
    python -m ratiss chsh 2.8284271247461903

## Portée d'un verdict

Un verdict conforme signifie : le hash recalculé localement coïncide avec le
hash déclaré. Cela ne prouve ni le contenu scientifique ni la fraîcheur d'un
lien (Hérité 2). La reproduction reste anonyme et offline — les tests réseau
du banc sont marqués `@pytest.mark.network` et exclus de la suite par défaut.