# Gabarit de prompt de sous-agent

Préambule identique d'un appel à l'autre, pour profiter du cache ; seule la partie « Tâche »
change. `description` de l'appel Agent : `[classe] objet court` (classes : CLAUDE.md racine,
« Mesurer la délégation »). Lot I de docs/AMELIORATIONS.md, piste 2.

---

Base : `<chemin>/bases/<nom>/`. Lis d'abord son `CLAUDE.md` (règles de travail, format).
Commandes : `bin/pdb …` lancées depuis ce dossier.

Règles :
- Ne lis jamais `papers/*/fulltext.md` en entier : `bin/pdb search "<q>" --paper <id>`, puis
  `bin/pdb show <chunk_id>` ou `Read` avec `offset`/`limit`.
- N'écris que dans les fichiers listés au périmètre. `benchmarks.csv`, `INDEX.md` et la
  réindexation restent à l'agent principal (sauf consigne contraire, avec `PDB_NO_PLOT=1`).
- Pas de compte rendu : le retour entre dans le contexte de l'agent principal.

Tâche : <ce qu'il faut faire>

Périmètre (fichiers que tu peux écrire) : <liste>

Retour attendu, 15 lignes au plus :
- fichiers écrits ;
- décisions prises et doutes (avec chunk_id quand c'est une donnée chiffrée) ;
- ce qui n'a pas pu être fait.
