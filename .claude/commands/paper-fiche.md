---
description: Remplit la fiche de lecture d'un article et ses lignes dans benchmarks.csv
argument-hint: <paper_id>
allowed-tools: Read, Edit, Write, Grep, Glob, Bash(.venv/bin/python bin/reindex.py)
---

Rédige la fiche de lecture de `papers/$ARGUMENTS/`. Respecte les règles de `CLAUDE.md` et
le contrat de `DATA_MODEL.md` (§2, §7, §8).

## Sources

- Lis `metadata.json` puis `fulltext.md` **en entier**. N'ouvre jamais `paper.pdf`.
- `sections.jsonl` sert à retrouver la page d'un passage.
- Si `extraction.backend` vaut `pymupdf` ou `extraction.ok` vaut `false`, signale-le en tête
  de la section « Statut de lecture » : le texte peut être incomplet ou mal découpé.

## `fiche.md`

Remplace chaque paragraphe d'instruction du template par le contenu, en gardant les titres.

- Front-matter : `fiche: done`, `date: <date du jour ISO>`.
- Ligne de référence : titre, auteurs, année, venue, DOI ou URL tels que dans
  `metadata.json`. Type : dire explicitement « preprint non relu par les pairs » le cas échéant.
- Chaque chiffre porte sa source entre parenthèses : `(Table 2)`, `(§IV-A)`, `(Fig. 5)`.
- Une valeur non rapportée s'écrit `n/r`. Jamais d'estimation, jamais de valeur reprise d'un
  autre papier.
- **Plateforme** : puce exacte ; puissance mesurée puce ou carte, et comment (sinon `n/r`) —
  c'est ce qui fixe `power_scope` dans `benchmarks.csv` ;
  code/bitstream publiés, avec lien, ou « non publiés ».
- **Limites et critique** : comparaisons biaisées (baselines anciennes, batch sizes ou
  précisions différentes, puissance puce vs carte), métriques non comparables, absence de
  reproductibilité. Compare à un baseline GPU/Jetson/MCU quand c'est pertinent, en le
  signalant comme déduit si le papier ne le fait pas.
- **Statut de lecture** : obligatoire. `papier complet` si tout `fulltext.md` a été lu ;
  liste explicitement ce qui est déduit et non affirmé par les auteurs.

## `benchmarks.csv`

Une ligne **par configuration rapportée** par les auteurs pour leur propre travail (pas les
chiffres des travaux qu'ils citent, sauf pour un survey : dans ce cas, ne rien ajouter et le
dire dans la fiche). Colonnes et vocabulaires : `DATA_MODEL.md` §7.

- Ajoute les lignes en fin de fichier, sans toucher aux lignes existantes. Si des lignes de
  ce `paper_id` existent déjà, montre-les et demande avant de les remplacer.
- Toute cellule sans valeur rapportée vaut `n/r`. Colonnes numériques : un nombre sans unité.
- `source_section` : tableau, figure ou section exacte. `confidence` : `high` (tableau),
  `medium` (texte), `low` (déduit — à éviter, et à signaler).
- Tableau dont la légende porte « [corps du tableau reconstruit par PyMuPDF : à vérifier] » :
  ses chiffres peuvent être décalés d'une colonne. `confidence: medium` au plus, et
  recoupe avec le texte quand il redonne la valeur. Tableau listé « sans corps extrait »
  dans `extraction.warnings` : ses chiffres manquent, dis-le dans « Statut de lecture » et
  n'invente rien.
- `power_scope` : `chip`, `board`, `board-dynamic`, `estimated` ou `unspecified` d'après la
  méthode décrite par les auteurs (DATA_MODEL §7) ; `n/r` si `power_w` vaut `n/r`. Ne jamais
  deviner la portée : une puissance sans méthode décrite est `unspecified`.
- Échappe par des guillemets toute cellule contenant une virgule.
- Reporte dans la section « Résultats » de la fiche la liste des lignes ajoutées.
- Aucune ligne justifiable (hors survey) : dis pourquoi dans « Résultats » et ajoute
  `benchmarks: none` au front-matter de la fiche (DATA_MODEL §8).

## `metadata.json`

- `status.fiche` → `"done"`.
- Confirme ou corrige `axes` (valeurs fermées de `DATA_MODEL.md` §3) et `tags` ; retire alors
  l'avertissement « axes déduits automatiquement… » de `extraction.warnings`.
- Si le `type` vaut `null` et que la venue est connue, fixe-le (`journal` / `conference`).
- Ne modifie jamais `id`.

## Fin

`.venv/bin/python bin/reindex.py` : il doit terminer sans erreur. Puis résume la fiche en
5 lignes (problème, méthode, résultat principal avec source, limite principale, pertinence)
et propose 2-3 pistes : papier à lire, expérience à reproduire, gap pour `gaps.md`.
