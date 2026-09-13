# PROVENANCE — ratiss-framework (banc d'essai)

Chaque module consolidé doit porter une ligne dans ce tableau **avant** d'être
poussé. Une ligne sans commit source et sans auditeur est une ligne morte :
le module ne part pas.

| Module | Dépôt source | Commit source | Date consolidation | Réécrit ou copié | Auditeur |
|---|---|---|---|---|---|
| `ratiss/verify.py` | aucun (règles R4–R7 + connaissances de domaine corrigées le 2026-09-12) | — | 2026-09-12 | réécrit from scratch | Équipe Rouge (assistant), tests verts localement + CI |
| `ratiss/verify.py` (extension) | passage multi-algorithme, doc Zenodo (md5) + GitHub (sha256) | — | 2026-09-13 | réécrit from scratch | Équipe Rouge (assistant), tests verts localement + CI |
| `ratiss/seal.py` | spec du prompt (§2.2 scellé de manifeste R5) | — | 2026-09-13 | réécrit from scratch | Équipe Rouge (assistant), tests verts localement + CI |
| `ratiss/journal.py` | spec du prompt (§2.3 journal des déviations chaîné R5) | — | 2026-09-13 | réécrit from scratch | Équipe Rouge (assistant), tests verts localement + CI |
| `ratiss/bounds.py` | spec du prompt (§2.4 plausibilité physique R4, borne de Tsirelson) | — | 2026-09-13 | réécrit from scratch | Équipe Rouge (assistant), tests verts localement + CI |
| `ratiss/ids.py` | spec du prompt (§2.5 identifiants réels Hérité 2 + docs.quantum.ibm.com/guides/save-jobs) | — | 2026-09-13 | réécrit from scratch | Équipe Rouge (assistant), tests verts localement + CI |
| `ratiss/report.py` | spec du prompt (§2.6 rapport d'audit + annexe R7) | — | 2026-09-13 | réécrit from scratch | Équipe Rouge (assistant), tests verts localement + CI |
| `ratiss/__main__.py` | spec du prompt (§2.7 commande unique, stdlib uniquement) | — | 2026-09-13 | réécrit from scratch | Équipe Rouge (assistant), tests verts localement + CI |

## Règles de ce tableau

1. **Copié ≠ consolidé.** Un module copié-collé d'un dépôt tiers sans
   réécriture vérifiée ne porte pas la mention « copié » : il est refusé.
   M1–M2 prévoit de *retirer* les copies tierces des 42 dépôts, pas de les
   recoller ici.
2. Le commit source est le SHA complet du dépôt d'origine, pas une date
   approximative.
3. L'auditeur nomme qui a relu le module ligne par ligne et rejoué ses tests.
   « L'agent IA » n'est pas un nom d'auditeur.
4. Tout module dont la provenance est impossible à établir (historique
   perdu, téléphone mort) est marqué `ORPHELIN` et isolé dans `orphelins/`,
   jamais mélangé au corps du framework.

## Inventaire à faire (prochain commit)

Liste anonyme des 42 dépôts publics de `jonathansearch`, avec pour chacun :
nombre de fichiers Python, dépendances tierces, présence ou absence de tests,
présence ou absence de secrets accidentels (scan de formes `ghp_`, clés PEM,
`.env`). Cet inventaire se fait **sans clé**, en lecture publique.
| `ratiss/ids.py` (ext. `is_doi_form`) | spec campagne PoC 2026-09-13 (garde-fou hors-ligne forme DOI) | — | 2026-09-13 | réécrit from scratch | EN ATTENTE (visa Rouge post-push) |
| `ratiss/__main__.py` (ext. `doi`) | spec campagne PoC 2026-09-13 (commande unique R7 pour identifiants) | — | 2026-09-13 | réécrit from scratch | EN ATTENTE (visa Rouge post-push) |
| `proofs/` (campagne 10 runs) | cibles externes publiques : Zenodo 6164620/7347926/884117/1427076, PyPI openai+requests, Crossref 3 DOIs | — | 2026-09-13 | exécuté, pas copié | EN ATTENTE (relecture chef) |
