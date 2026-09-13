# RATISS-Framework — BANC D'ESSAI

> **Statut : banc d'essai temporaire.** Ce dépôt vit sur un compte jetable
> (`brossbernard2-pixel`) créé le 2026-09-12 pour valider la chaîne de
> consolidation avant de toucher au compte principal de Jonathan Evina.
> **Il sera supprimé.** Rien ici n'est un résultat. Tout ici est un échafaudage.

## Ce que c'est

Le squelette de consolidation M1–M2 : rassembler progressivement les outils
Python dispersés dans les dépôts publics de Jonathan Evina en un framework
unique, vérifiable, testé — construit *verification-first*.

## Ce que ce n'est pas

- Ce n'est pas un résultat scientifique.
- Ce n'est pas le dépôt final (le dépôt final vivra sur le compte principal,
  avec son historique véritable restauré).
- Ce n'est pas une preuve de quoi que ce soit, sauf une : la chaîne
  « code → tests → push → vérification anonyme » fonctionne de bout en bout.

## Règles permanentes (clause R4–R7)

- **R4.** Aucun chiffre publié s'il n'a pas été calculé, avec paramètres et hash.
- **R5.** Prompts et paramètres scellés, hashés dans chaque run ; toute
  modification après mesure va au journal des déviations.
- **R6.** Bras expérimentaux séparés du chemin critique ; verdict par ablation.
- **R7.** Aucune affirmation publique sans qu'un étranger puisse la reproduire
  en une commande.
- Aucune clé, aucun jeton, aucun secret dans le code ou dans l'historique git.
  Jamais. La vérification de ce dépôt se fait **anonymement** (API GitHub sans
  authentification) : c'est le rôle de l'Équipe Rouge.

## Structure

```
ratiss/            paquet Python (stdlib uniquement, zéro dépendance)
  verify.py        primitives de vérification : hashes, formats d'identifiants
tests/             pytest, verts localement ET en GitHub Actions
audit/
  PROVENANCE.md    tableau de provenance : chaque module cite son dépôt source,
                   son commit, sa date, son auditeur
.github/workflows/ tests automatisés à chaque push
```

## Reproduire (clause R7)

```bash
git clone https://github.com/brossbernard2-pixel/RATISS-Framework.git
cd RATISS-Framework
python3 -m pytest -q
```

Zéro dépendance externe : stdlib Python seule. Volontairement — ce framework
doit pouvoir tourner sur une connexion à 2 KB/s et une machine de récupération.

## Provenance du squelette

Les primitives de `ratiss/verify.py` sont réécrites from scratch le 2026-09-12
(voir `audit/PROVENANCE.md`). Aucun code tiers copié dans ce commit : c'est la
règle M1–M2, les copies de code tiers seront retirées, pas recopiées.
