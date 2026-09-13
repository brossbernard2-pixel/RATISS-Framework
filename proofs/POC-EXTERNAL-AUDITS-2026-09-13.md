# PREUVE DE CONCEPT — audits externes réels, 2026-09-13

**Exécuté par :** Équipe Rouge, sous ordre direct du chef (jonathan Evina).
**Méthode :** couche 1 de ce dépôt (`ratiss/`), commandes CLI uniquement.
**Cibles :** 9 artefacts publics externes sur 3 plateformes indépendantes
(Zenodo, PyPI, Crossref/DOI) + 1 contrôle négatif délibéré.

## Portée du verdict (lire avant tout)

Chaque verdict ci-dessous est un verdict d'**intégrité** ou de **résolution**,
pas un verdict scientifique :

- Zenodo / PyPI : « les octets servis aujourd'hui ont le checksum que
  l'éditeur publie aujourd'hui ». Rien de plus.
- DOI : « l'identifiant résout aujourd'hui » (Hérité 2 : un identifiant
  enregistré n'est pas une revalidation en temps réel).
- Aucun verdict ne porte sur la validité scientifique des articles concernés.
  La méthode ne sait pas encore faire ça ; elle le dira quand elle saura.

## Les 10 runs

| # | Plateforme | Cible | Verdict | Exit |
|---|---|---|---|---|
| Z1 | Zenodo | record 6164620, `README.md` (829 o) | CONFORME (md5 publié = md5 servi) | 0 |
| Z2 | Zenodo | record 7347926, `ultralytics/yolov5-v7.0.zip` (1 048 193 o) | CONFORME | 0 |
| Z3 | Zenodo | record 884117, `Data_for_Policy_2017_paper_43.pdf` (106 510 o) | CONFORME | 0 |
| Z4 | Zenodo | record 1427076, `article.pdf` (article de chimie, 1856) | CONFORME | 0 |
| P1 | PyPI | wheel `openai-3.13.0` (2 009 683 o), digest sha256 publié par PyPI | CONFORME | 0 |
| P2 | PyPI | wheel `requests-2.34.2` (73 075 o), digest sha256 publié par PyPI | CONFORME | 0 |
| D1 | DOI/Crossref | `10.31235/osf.io/8jwhk` | RESOUT | 0 |
| D2 | DOI/Crossref | `10.1207/s15327906mbr0404_6` | RESOUT | 0 |
| D3 | DOI/Crossref | `10.1201/9781003267218-8` | RESOUT | 0 |
| N1 | PyPI | **contrôle négatif** : digest sha256 de la wheel openai appliqué à la wheel requests | **DIVERGENCE détectée** (KO) | 1 |

**Lecture :** 9 conformes + 1 divergence *attendue et détectée*. Une méthode
qui ne sait pas dire non ne prouve rien : le run N1 est là pour ça.

## Rejouer (R7)

```bash
bash proofs/replay_poc.sh
```

Le script exécute les 10 commandes exactes, affiche chaque code de sortie,
et conclut. Un étranger, une machine, une commande : c'est la loi du labo.

## Ce que cette preuve démontre — et ce qu'elle ne démontre pas

- **Démontre :** la couche 1 produit des verdicts calculés, rejouables, sur
  des artefacts réels hors du labo ; elle détecte une divergence réelle
  d'intégrité ; elle tient sur trois écosystèmes de publication différents.
- **Ne démontre pas :** que la méthode juge la science. Bornes physiques,
  ablation R6 et audit de raisonnement restent à éprouver sur mandat réel
  (pilote scellé promis dans la candidature EV).

*Le labo journalise ses propres retards. C'est précisément ce qui le rend crédible.*
