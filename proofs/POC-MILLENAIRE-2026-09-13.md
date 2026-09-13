# AUDIT EXTERNE SPÉCIAL — « OpenAI a résolu un problème du millénaire » · 2026-09-13

**Revendication auditée :** le 8 septembre 2026, OpenAI annonce qu'un système
interne non publié a résolu le problème de l'existence et de la régularité de
Navier–Stokes (l'un des sept problèmes du prix du millénaire du Clay
Mathematics Institute), via ~10 000 agents, ~88 heures, ~130 milliards de
tokens ; preuve analytique de 165 pages + formalisation Lean.
**Sources de la revendication :** page officielle OpenAI
(openai.com/index/navier-stokes-solution/, 2026-09-08), presse internationale
du 8 au 11 septembre 2026, article Wikipédia « Navier–Stokes priority
controversy » (état au 2026-09-12).

**Ce que la méthode PEUT auditer ici :** existence, publicité, intégrité et
reproductibilité des artefacts ; statut de la revendication auprès du registre
officiel ; cohérence d'ordre de grandeur des chiffres annoncés.
**Ce qu'elle NE PEUT PAS auditer :** la validité mathématique de la preuve
(hors de sa compétence ; la vérification Lean est celle d'OpenAI, l'examen
communautaire indépendant est en cours, et le règlement Clay impose
publication + deux ans de recul).

## Les runs

| # | Artefact | Commande rejouable | Verdict |
|---|---|---|---|
| M1 | Papier OpenAI (PDF, cdn.openai.com) | `python -m ratiss audit --url https://cdn.openai.com/pdf/32d9f210-8b73-45e0-91bc-82a30aef8a9a/navier-stokes.pdf --sha256 0e779481c4da40bd28d1e642e1d8ca57447d129610df28dfa5a11e9af8ae228f` | CONFORME au scellé du 2026-09-13 (le PDF servi aujourd'hui = le PDF audité) |
| M2 | Dépôt Lean `openai/NavierStokesAndEuler` | public ✔ créé 2026-09-08 ; tarball scellé au commit `f9e8bc5b38b6e212696e8a30e3e91517af887bbd` : `python -m ratiss audit --url https://codeload.github.com/openai/NavierStokesAndEuler/tar.gz/f9e8bc5b38b6e212696e8a30e3e91517af887bbd --sha256 9832374e0926a8a9dfb19699e50bf8ddb957fb9e961e7cc85b8fb689eda2b1b7` | CONFORME au scellé ; dépôt public, preuve formelle accessible |
| M3 | Papier-programme sous-jacent (Córdoba–Martínez-Zoroa, cité par T. Tao, v3) | `python -m ratiss doi 10.48550/arXiv.2410.22920` + `python -m ratiss audit --url https://arxiv.org/pdf/2410.22920v3 --sha256 14c3a2423cbcec2d6ca5c54258ae4bd978f66631165fdb6217248bda280d45e8` | DOI RESOUT + PDF v3 CONFORME au scellé |
| M4 | Registre officiel Clay (page Navier–Stokes, consultée le 2026-09-13) | consultation humaine datée : aucun marqueur de résolution sur la page ; règlement du prix = publication + 2 ans | **REVENDICATION, PAS RÉSOLUTION CERTIFIÉE** — le registre ne décerne rien à ce jour |
| M5 | Chiffres annoncés (130·10⁹ tokens, 2,7·10⁶ messages, 88 h, 10 000 agents) | calcul : 130·10⁹/(88·3600)/10⁴ = **41,0 tokens/s/agent** ; 2,7·10⁶/(88·60)/10⁴ = **0,05 message/min/agent** | COHÉRENT en ordre de grandeur (un message par agent toutes les ~20 min) ; cohérence ≠ vérité |
| M6 | Préprints concurrents Buckmaster–Alpöge (8 sept. 2026) | recherche anonyme : API arXiv muette depuis la sandbox d'audit, page auteur sans identifiant 2026, Wikipédia sans identifiant | **NON AUDITÉS, FAUTE D'IDENTIFIANT STABLE ATTEIGNABLE** — lacune documentée, pas un verdict |

## Verdict global, en une phrase

Les artefacts de la revendication OpenAI **existent, sont publics, et leur
intégrité est maintenant scellée et rejouable** (M1–M3) ; mais au 2026-09-13
le registre officiel **ne reconnaît aucune résolution** (M4), la cohérence des
chiffres annoncés est calculée sans être prouvée vraie (M5), et le travail
concurrent n'a pas d'identifiant stable atteignable par un auditeur externe
(M6) — donc : **revendication machine-vérifiée par son auteur, pas encore
résolution certifiée par son juge.**

## Portée et limites (Hérité 2, R4)

- Un scellé RATISS n'est pas une approbation : M1–M3 disent « ces octets-là,
  à cette date-là », rien de plus.
- « Vérifié par Lean » est une affirmation d'OpenAI ; la méthode ne rejoue pas
  Lean (hors périmètre couche 1 ; candidat couche 2 si le chef le décide).
- La controverse de priorité (Buckmaster–Alpöge vs OpenAI) est documentée par
  des sources tierces ; la méthode ne juge pas les intentions, seulement les
  artefacts et les registres.

*Le labo journalise ses propres retards. C'est précisément ce qui le rend crédible.*
