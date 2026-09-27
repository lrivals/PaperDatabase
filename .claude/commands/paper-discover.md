---
description: Cherche des papiers pertinents à ajouter (mes autres bases, puis OpenAlex), propose une liste courte, ajoute après accord
argument-hint: [axe | gap | mots-clés] (vide : citations du corpus)
allowed-tools: Read, Grep, Glob, Bash(bin/pdb discover:*), Bash(bin/pdb add:*), Bash(bin/pdb status), Bash(bin/pdb base scan:*), Bash(bin/pdb base import:*), Bash(bin/pdb base list)
---

Trouve de nouveaux papiers à ajouter à la base courante. Argument : `$ARGUMENTS`.

1. Lis `profile.md` (thème, inclus, exclus), `INDEX.md` (axes couverts, axes maigres) et
   `gaps.md` (verrous à étayer).

**Étape 0 — mes autres bases.** Si `bin/pdb base list` montre d'autres bases, lance
`bin/pdb base scan` et lis `xbase_candidates.csv` (colonnes `kind`, `score`, `source_base`,
`paper_id`, `n_citers_target`, `reasons`) :
- `cited_here` : présent ailleurs et déjà cité par cette base, à proposer en priorité ;
- `in_base` : présent ailleurs, correspond aux règles ; à juger contre `profile.md` ;
- `ref_elsewhere` : cité par une autre base, absent partout ; s'ajoute comme un candidat
  OpenAlex (`bin/pdb add`).
Un papier importé garde son extraction et sa fiche, qui repasse à `todo` : c'est moins cher
qu'un ajout. Avec un argument (axe, gap), ne garde que les candidats qui s'y rattachent.
Continue ensuite avec OpenAlex pour compléter.
2. Choisis la recherche selon l'argument :
   - vide → `bin/pdb discover` (citations entrantes et sortantes du corpus) ;
   - un axe de `base.json` (clé `axes`) → `bin/pdb discover --axis <axe> --since 2019`, plus
     `--forward --backward` ;
   - un gap ou des mots-clés → une à trois requêtes `--query "…"` en anglais, formulées depuis
     l'intitulé du gap, plus `--since 2019` si le sujet est récent.
   Si OpenAlex refuse la recherche (HTTP 503, recherche anonyme suspendue), dis-le, rappelle
   la variable `OPENALEX_API_KEY` (docs/GUIDE.md §4), et fais la recherche par citations
   (`--forward --backward`), qui n'utilise pas la recherche.
3. Lis `candidates.csv` (colonnes : `score`, `in_topic`, `reasons`, `axes_guess`, `arxiv_id`,
   `doi`, `oa_url`). Écarte :
   - les classiques génériques hors du thème de `profile.md` (architectures, frameworks,
     datasets de référence…), même très cités ;
   - tout ce qui relève de la section « Exclus » de `profile.md` ;
   - les papiers dont le titre et le résumé ne concernent ni un axe ni un gap ;
   - les versions en double d'un même travail.
4. Propose une **liste courte de 5 à 10 papiers**, sous forme de tableau : titre, année,
   venue, identifiant (arXiv, sinon DOI), axe ou gap couvert, et raison de le lire (cite
   ou est cité par quels papiers du corpus). Signale ceux qui n'ont pas de version arXiv :
   PDF à récupérer à la main puis à déposer dans `inbox/`. Ne jamais contourner un paywall.
   Ces métadonnées viennent d'OpenAlex et ne sont pas vérifiées : dis-le. Mets à part les
   candidats venus d'une autre base (colonne « source » : `<base>:<paper_id>`).
5. **Attends la validation de l'utilisateur.** N'ajoute rien sans son accord explicite.
   Ensuite, `bin/pdb base import <base>:<paper_id> …` pour ceux d'une autre base, et
   `bin/pdb add <id> <id> …` (qui ingère et réindexe) pour les autres, puis rapporte les
   avertissements d'extraction et propose `/paper-fiche` pour chaque papier ajouté.

Réponds en français, brièvement.
