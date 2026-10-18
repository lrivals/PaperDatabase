# Datasets pour la détection YOLO : annotation, prétraitement, augmentation — mode d'emploi

Base de connaissance d'articles scientifiques. Thème : voir [profile.md](profile.md), qui fait
foi (thème donné par l'utilisateur, périmètre précisé au fil des ajouts).

**Base distincte**, qui partage le code de `../../` : `bin/`, `.venv` et `.claude/commands/`
sont des liens vers ce dépôt, et la base active est détectée par le fichier `base.json` de ce
dossier (axes, règles de classement ; [DATA_MODEL.md §11](../../DATA_MODEL.md)). Ne jamais
écrire dans une autre base depuis ici : pour en reprendre un article, `bin/pdb base import`.

Structure, scripts et installation (code partagé) : [SETUP.md](../../SETUP.md).
Schémas et conventions : [DATA_MODEL.md](../../DATA_MODEL.md).
Guide d'utilisation (pour l'humain) : [docs/GUIDE.md](../../docs/GUIDE.md).

---

## Comment chercher ici

Lis du résumé vers le détail, et arrête-toi dès que tu as la réponse.

1. **[profile.md](profile.md)** — le thème et le périmètre de la base.
2. **[INDEX.md](INDEX.md)** — quels papiers existent, sur quel axe, fichés ou non.
3. **[benchmarks.csv](benchmarks.csv)** — tous les chiffres. Pour toute question quantitative,
   interroge-le avec `bin/pdb bench` (`-h` pour les filtres) plutôt que de le lire en entier.
   Pour l'identité d'un papier : `bin/pdb paper <id court | mot du titre>`.
4. **`papers/<id>/fiche.md`** — la lecture critique : problème, méthode, limites, pertinence.
5. **Passages** — `bin/pdb search "<question en anglais>"`, puis `bin/pdb show <chunk_id>` sur
   2 ou 3 d'entre eux ; vérifie chaque citation textuelle avec
   `bin/pdb verify <chunk_id> "<citation>"`. `search` renvoie toujours des passages, même hors
   sujet : si aucun extrait ne répond, dis que la base ne traite probablement pas le sujet.
   La skill `/paper-ask` enchaîne tout cela ([docs/RAG.md](../../docs/RAG.md)).
   `papers/<id>/fulltext.md` en dernier recours seulement.
6. **`papers/<id>/paper.pdf`** — ne l'ouvre pas : tout ce qu'il contient est dans `fulltext.md`.

**Quoi lire ensuite ?** D'abord mes autres bases : `bin/pdb base scan` (articles déjà présents
ou cités ailleurs). Puis [external_refs.csv](external_refs.csv) (travaux absents cités par le
corpus) et `/paper-discover` (OpenAlex). Métadonnées issues du parsing ou d'OpenAlex : à
vérifier avant de les citer.

---

## Commandes

| Commande | Effet |
|---|---|
| `bin/pdb status` | état de la base et prochaines actions suggérées |
| `bin/pdb base list` / `info` / `check` | bases enregistrées ; profil et axes de celle-ci ; effet des règles de `base.json` |
| `bin/pdb base scan [--from NOM]` / `base import NOM:<paper_id>` | articles utiles présents ou cités dans les autres bases ; copie d'un article |
| `/base-profile [texte]` | le LLM propose d'affiner le profil (axes, règles, périmètre) ; rien n'est écrit sans accord |
| `bin/pdb bench [filtres]` | filtre `benchmarks.csv` sans LLM ; `--check` : valeurs retrouvées dans leur passage (`chunk_id`) ; `--comparable` : groupes de lignes comparables, avant toute comparaison entre papiers |
| `bin/pdb compare --x COL --y COL [filtres]` / `/paper-compare <question>` | comparaison sur deux axes (FPS contre W, précision contre LUT) : groupes comparables avec leur confiance, lignes exclues avec leur motif ; à préférer à une lecture côte à côte de `bench` ([DATA_MODEL.md §7.2](../../DATA_MODEL.md)) |
| `bin/pdb table <id> [<tableau>] --png` / `/table-review <id>` | tableaux d'un papier, signaux de qualité, image de la zone dans le PDF ; relecture et corrections proposées dans `tables_review.md` |
| `bin/pdb search "<q>"`, `show <chunk_id>`, `verify <chunk_id> "<citation>"` | passages sourcés sans LLM |
| `/paper-ask <question>` | réponse sourcée et vérifiée |
| `/paper-research <question>` | route GPU, sur demande seulement (Qwen3, GPU CUDA, `bin/pdb gpu`) : recherche et acquisition open access ; sinon `/paper-ask` |
| `bin/pdb paper <id \| mot>…` | fiche d'identité d'un papier |
| `bin/pdb cites <id>` / `bin/pdb cited-by <id>` | graphe de citations internes |
| `/paper-add <arxiv-id \| url \| doi \| chemin.pdf>` | acquisition + ingestion + réindexation |
| `/paper-fiche <paper_id>` | remplit `fiche.md` et les lignes de `benchmarks.csv` |
| `/paper-extract <paper_id>` | écrit `claims.jsonl` : preuves atomiques liées à leur passage (fiche `done` requise) |
| `/paper-gaps` | met à jour `gaps.md` |
| `/paper-discover [axe \| gap \| mots-clés]` | candidats (autres bases, puis OpenAlex) ; ajoute après accord |
| `bin/pdb viz` | visualisation (graphe 3D, généalogie, onglet Bases) |

Après toute modification du corpus : `bin/pdb reindex`. Pour un article sous paywall, déposer
le PDF dans `inbox/` à la main, puis `bin/pdb ingest`. Aucun contournement de paywall.

---

## Règles de travail

**Langue.** Français par défaut. Termes techniques et titres d'articles en anglais.

**Sources.** Ne jamais inventer de référence. Pour chaque article cité : titre, auteurs,
année, venue, lien ou DOI. En cas de doute, le dire et vérifier.

**Chiffres.** Une valeur non rapportée par les auteurs s'écrit `n/r`, jamais une estimation.
Tout chiffre avancé porte sa section source. Quand `confidence` vaut `low` dans
`benchmarks.csv`, le signaler.

**Lu vs déduit.** Distinguer ce qui vient du papier de ce qui est une inférence. Signaler les
preprints non relus par les pairs (`type: preprint`).

**Esprit critique.** Relever les comparaisons biaisées, les métriques non comparables d'un
papier à l'autre (conditions de mesure), l'absence de code publié.

**Articles importés.** Un papier dont `metadata.json` porte `imported_from` vient d'une autre
base : sa fiche a été écrite pour un autre thème, sa pertinence est à réévaluer ici.

**Gaps.** Les zones non couvertes sont la matière première d'une problématique de recherche :
les signaler plutôt que de les combler par des suppositions.

---

## Format des réponses

- Structurées et concises, tableaux pour toute comparaison.
- Une réponse sur le corpus s'ouvre par son verdict de suffisance (`suffisant | partiel |
  absent`) et la liste de ses exigences avec leur statut (`couvert | partiel | absent`), puis
  **Lu / Déduit / Non trouvé dans la base** (règle de `/paper-ask`). Un verdict `absent`
  dit que la base ne couvre pas le sujet, pas que la littérature l'ignore.
- Une synthèse d'article suit : problème, méthode, résultats, limites, pertinence pour le thème.
- Terminer par 2-3 pistes concrètes : papier à lire, expérience à reproduire, gap à creuser.
