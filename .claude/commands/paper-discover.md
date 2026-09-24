---
description: Cherche des papiers pertinents à ajouter (OpenAlex), propose une liste courte, ajoute après accord
argument-hint: [axe | gap | mots-clés] (vide : citations du corpus)
allowed-tools: Read, Grep, Glob, Bash(bin/pdb discover:*), Bash(bin/pdb add:*), Bash(bin/pdb status)
---

Trouve de nouveaux papiers à ajouter à PaperDatabase. Argument : `$ARGUMENTS`.

1. Lis `INDEX.md` (axes couverts, axes maigres) et `gaps.md` (verrous à étayer).
2. Choisis la recherche selon l'argument :
   - vide → `bin/pdb discover` (citations entrantes et sortantes du corpus) ;
   - un axe de `lib/schema.py` (`AXES`) → `bin/pdb discover --axis <axe> --since 2019`, plus
     `--forward --backward` ;
   - un gap ou des mots-clés → une à trois requêtes `--query "…"` en anglais, formulées depuis
     l'intitulé du gap, plus `--since 2019` si le sujet est récent.
   Si OpenAlex refuse la recherche (HTTP 503, recherche anonyme suspendue), dis-le, rappelle
   la variable `OPENALEX_API_KEY` (docs/GUIDE.md §4), et fais la recherche par citations
   (`--forward --backward`), qui n'utilise pas la recherche.
3. Lis `candidates.csv` (colonnes : `score`, `in_topic`, `reasons`, `axes_guess`, `arxiv_id`,
   `doi`, `oa_url`). Écarte :
   - les classiques génériques hors sujet (ResNet, AlexNet, Batch Norm, TensorFlow…), même
     très cités ;
   - les papiers dont le titre et le résumé ne concernent ni un axe ni un gap ;
   - les versions en double d'un même travail.
4. Propose une **liste courte de 5 à 10 papiers**, sous forme de tableau : titre, année,
   venue, identifiant (arXiv, sinon DOI), axe ou gap couvert, et raison de le lire (cite
   ou est cité par quels papiers du corpus). Signale ceux qui n'ont pas de version arXiv :
   PDF à récupérer à la main puis à déposer dans `inbox/`. Ne jamais contourner un paywall.
   Ces métadonnées viennent d'OpenAlex et ne sont pas vérifiées : dis-le.
5. **Attends la validation de l'utilisateur.** N'ajoute rien sans son accord explicite.
   Ensuite, `bin/pdb add <id> <id> …` (qui ingère et réindexe), puis rapporte les
   avertissements d'extraction et propose `/paper-fiche` pour chaque papier ajouté.

Réponds en français, brièvement.
