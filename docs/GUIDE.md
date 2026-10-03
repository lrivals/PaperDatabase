# Guide d'utilisation de PaperDatabase

PaperDatabase transforme des PDF d'articles scientifiques en une base de connaissance en
texte que Claude Code sait parcourir : il y retrouve un chiffre, compare des travaux, repère
les zones non couvertes. Ce guide montre comment s'en servir au quotidien. Le pipeline ne
dépend pas du domaine, et un même code gère plusieurs bases séparées (§8). Le dépôt en contient
trois : `fpga` (vision embarquée sur FPGA), qui sert d'exemple dans ce guide, `drone`
(vision embarquée sur drone, dans `bases/drone/`) et `stage` (apprentissage continu embarqué
pour la maintenance prédictive, références d'un stage, dans `bases/stage/`).

Pour le fonctionnement interne, voir [SETUP.md](../SETUP.md) ; pour les formats de
fichiers, [DATA_MODEL.md](../DATA_MODEL.md).

---

## 1. Le système en un coup d'œil

```
  arXiv id / DOI / PDF
          │  bin/pdb add          (téléchargement arXiv, ou dépôt manuel dans inbox/)
          ▼
  papers/<id>/  metadata.json · fulltext.md · sections.jsonl · refs.jsonl
          │  /paper-fiche         (Claude lit fulltext.md, écrit la fiche et les chiffres)
          ▼
  fiche.md + lignes de benchmarks.csv
          │  bin/pdb reindex      (automatique après add / ingest / fiche)
          ▼
  INDEX.md · external_refs.csv · figures/ périmées refaites     /paper-gaps → gaps.md
          │
          ▼
  vos questions à Claude, et bin/pdb discover / /paper-discover pour trouver la suite
```

Tout ce schéma vaut pour **une** base : celle du dossier courant (`bases/fpga/` pour `fpga`,
`bases/drone/` pour `drone`, `bases/stage/` pour `stage` ; à la racine du dépôt, la base par défaut du registre). Les bases
partagent le code et échangent des articles avec `bin/pdb base scan` et `bin/pdb base import`
(§8).

La répartition des rôles :

| Qui | Fait quoi |
|---|---|
| **Vous** | choisir les articles, récupérer les PDF sous paywall, valider les ajouts proposés, relire une fiche de temps en temps contre le PDF |
| **Les scripts** (`bin/pdb`) | télécharger, extraire le texte (GROBID), indexer, vérifier la cohérence, chercher des candidats |
| **Claude** (`/paper-…`) | lire, ficher, chiffrer, comparer, relever les gaps, trier les candidats |

---

## 2. Installation (10 minutes)

Prérequis : Python 3.12, Docker, Claude Code.

```bash
bash bin/setup.sh          # crée .venv et installe les dépendances
bin/pdb grobid start       # lance GROBID (conteneur Docker, port 8070)
bin/pdb status             # vérifie que tout est vert
```

`bin/pdb` est le point d'entrée unique : `bin/pdb help` liste les commandes. Pour le taper
depuis n'importe quel dossier :

```bash
ln -s "$PWD/bin/pdb" ~/.local/bin/pdb
```

Facultatif :

- `.venv/bin/pip install -r requirements-viz.txt` pour la visualisation ;
- `.venv/bin/pip install -r requirements-plot.txt` pour les figures statiques (`bin/pdb plot`) ;
- `requirements-embed.txt` pour la similarité par embeddings ;
- **route GPU**, seulement si vous voulez utiliser votre carte graphique et qu'elle est CUDA :
  `.venv/bin/pip install -r requirements-rag.txt` puis `bin/pdb gpu on` (§5, encadré
  « Route GPU ») ; sans cela, tout tourne sur CPU ;
- une clé OpenAlex gratuite pour la découverte (§4.3).

---

## 3. Premier article, de bout en bout

**1. Ajouter.**

```bash
bin/pdb add 2507.18174                 # identifiant arXiv
bin/pdb add 10.1088/1748-0221/13/07/P07027   # DOI : sa version arXiv est cherchée via OpenAlex
bin/pdb add ~/Téléchargements/article.pdf    # PDF local
```

La commande télécharge, extrait, range dans `papers/<paper_id>/` et réindexe. Si GROBID est
arrêté, elle propose de le démarrer. Relisez les **avertissements** qu'elle affiche
(métadonnées douteuses, sections non détectées) : ils sont aussi enregistrés dans
`metadata.json`.

**2. Ficher.** Dans Claude Code :

```
/paper-fiche arxiv-2507.18174-real-time-object-detection-classification
```

Claude lit `fulltext.md` en entier et produit deux choses :

- `fiche.md` : problème, méthode, résultats, limites, pertinence, et ce qui a été lu ou déduit ;
- une ligne de `benchmarks.csv` par configuration mesurée, chaque chiffre avec sa section
  source, et `n/r` quand l'article ne donne pas la valeur.

**3. Interroger.** Dans Claude Code, lancez `/paper-ask <question>`. Claude recherche des
passages dans le corpus, lit les sources originales et vérifie les comparaisons chiffrées.
La réponse s'ouvre par un verdict (`suffisant`, `partiel` ou `absent`) et la liste de ce
qu'une réponse complète doit établir, chaque point marqué couvert, partiel ou absent : vous
voyez d'emblée si la base suffit.
Il peut ajouter un article libre d'accès pertinent si la base ne suffit pas. Sans l'index
RAG facultatif, l'ordre manuel reste `INDEX.md`, `benchmarks.csv`, fiches, puis
`fulltext.md`. Il n'ouvre jamais le PDF. Exemples de questions :

- « Quels papiers dépassent 25 FPS sous 5 W, et avec quel toolflow ? »
- « Compare hls4ml et FINN : quantification supportée, ressources, latence. »
- « Qu'est-ce qui a été publié sur l'apprentissage continu sur FPGA, et avec quelles mesures d'énergie ? »
- « Synthèse de 2604.21280 pour ma thèse. »
- « Quels gaps ressortent sur la mesure de puissance ? »

Les réponses citent la section source de chaque chiffre, signalent les preprints et les
valeurs `confidence: low`, et séparent ce qui est lu de ce qui est déduit. Si une réponse
ne le fait pas, demandez-lui de le faire.

---

## 4. Faire grandir le corpus de manière pertinente

Ajouter des papiers ne sert que s'ils répondent à une question : combler un axe maigre,
étayer un gap, compléter une lignée de travaux. Viser 15 à 20 fiches solides vaut mieux que
200 PDF non lus.

### 4.1 Les quatre sources, de la plus sûre à la plus large

| Source | Commande | Ce qu'elle trouve | Piège |
|---|---|---|---|
| **Références du corpus** (en arrière) | `external_refs.csv` (généré), `bin/pdb discover --backward` | les travaux que vos papiers citent tous : fondations, toolflows de référence | beaucoup de classiques génériques (ResNet, Batch Norm) : à ignorer |
| **Citations du corpus** (en avant) | `bin/pdb discover --forward --since 2020` | ce qui a été construit depuis sur vos papiers : l'état de l'art récent | les papiers très cités dominent ; `--since` recentre sur le récent |
| **Recherche par axe ou par gap** | `bin/pdb discover --axis autoencoder-fpga`, `--query "convolutional autoencoder image FPGA"` | les axes maigres, les verrous de `gaps.md` | vocabulaire trop large : formuler en anglais, avec les termes techniques |
| **Veille ciblée** | à la main | les actes des conférences de référence (FPGA, FCCM, FPL, DATE, ACM TRETS, TinyML), les pages des labos (LIRMM, IETR, LAAS, CEA-List) | papiers sous paywall : PDF à déposer dans `inbox/` |

### 4.2 La boucle recommandée

Dans Claude Code :

```
/paper-discover                     # citations du corpus
/paper-discover autoencoder-fpga    # un axe maigre (bin/pdb status les signale par ⚠)
/paper-discover "mesure de puissance YOLO FPGA"   # un gap
```

Claude lance la recherche, lit `candidates.csv`, écarte le hors-sujet et propose 5 à 10
papiers, chacun avec sa justification. **Il n'ajoute rien sans votre accord.**

Sans Claude, la même chose à la main :

```bash
bin/pdb discover --forward --backward --since 2019
# lire candidates.csv (trié : dans le sujet d'abord, puis par score)
# éditer candidates_arxiv.txt : ne garder que les lignes pertinentes
bin/pdb add --from candidates_arxiv.txt
```

Comment lire `candidates.csv` :

- `in_topic` : « oui » si le titre évoque le matériel (FPGA, accélérateur, TinyML, MCU,
  edge computing…), si le résumé le fait au moins deux fois, ou si le papier relève d'un
  toolflow / d'une plateforme ; un autoencodeur purement logiciel, ou un réseau qui cite le
  FPGA une fois en passant (SqueezeNet), reste « non » ;
- `reasons` : le lien avec le corpus (« cite 4 papiers du corpus », « cité par 3 papiers du
  corpus ») ;
- `axes_guess` : l'axe probable ;
- `arxiv_id` vide : pas de version arXiv trouvée. `oa_url` donne alors un éventuel lien
  open access légal ; sinon, passer par l'accès de l'université.

### 4.3 Clé OpenAlex

La découverte interroge [OpenAlex](https://openalex.org), une base bibliographique ouverte.
Sans clé, la recherche par mots-clés (`--query`, `--axis`) est parfois suspendue quand le
service est chargé (erreur HTTP 503). Les modes par citations (`--forward`, `--backward`)
fonctionnent en général. Avec une clé gratuite :

```bash
export OPENALEX_API_KEY=...          # dans ~/.bashrc
export OPENALEX_MAILTO=vous@exemple.fr   # facultatif, quotas plus larges
```

Les réponses sont mises en cache dans `.cache/openalex/`. Pour forcer une nouvelle
interrogation, supprimer ce dossier.

### 4.4 Critères avant d'ajouter un papier

- **Garder** : il relève d'un axe ; il étaye ou contredit un gap ; il est cité par au moins
  2 papiers du corpus ; il donne des mesures sur carte (FPS, W, ressources).
- **Écarter** : les classiques génériques (le corpus n'a pas besoin de ResNet) ; les
  travaux sans rapport avec l'embarqué ; une seconde version d'un papier déjà présent
  (version arXiv et version éditeur).
- **Équilibrer** : `bin/pdb status` affiche le nombre de papiers par axe. Un axe à 1 ou 2
  papiers ne permet aucune comparaison, et c'est souvent là qu'est le gap intéressant.
- **Vérifier** : les métadonnées d'OpenAlex et de `basicStart.txt` peuvent être
  approximatives. Après l'ajout, `/paper-add` compare la note de départ au PDF réel ; un
  écart signale une référence à corriger.

### 4.5 Articles sous paywall

Aucun contournement. Téléchargez le PDF via l'accès de l'université, puis :

```bash
cp ~/Téléchargements/article.pdf ~/Téléchargements/citation.bib inbox/
bin/pdb ingest
```

**Déposez aussi l'export de citation de l'éditeur** (BibTeX `.bib` ou RIS `.ris` : bouton
« Cite » / « Export citation » d'IEEE Xplore, ACM DL, MDPI, Springer). Sur un PDF sans
arXiv, GROBID se trompe souvent de premier auteur ou d'année, ce qui fausse le `paper_id`.
Le nom du fichier importe peu : l'ingestion l'apparie au PDF par DOI, sinon par titre. Ses
champs (titre, auteurs, année, venue, DOI, type) priment alors sur l'en-tête lu par
GROBID, et le fichier est rangé dans `papers/<paper_id>/citation.bib` comme preuve. Un
export groupé (plusieurs entrées) sert à plusieurs PDF.

Sans fichier de citation, GROBID retrouve seul le titre, les auteurs et l'année :
vérifiez-les dans `metadata.json` et précisez `type` et `venue` si l'avertissement le
demande.

---

## 5. Routine de travail

**À chaque session (2 minutes)**

```bash
bin/pdb status
```

La commande dit où en est la base et propose les trois prochaines actions : GROBID à
démarrer, PDF en attente, fiche à rédiger, gaps à mettre à jour, axe à étoffer, commit.

**Chaque semaine**

1. `/paper-discover` sur un axe maigre ou un gap, puis valider 3 à 5 ajouts.
2. `/paper-fiche` sur chaque nouveau papier.
3. Toutes les 3 à 5 fiches : `/paper-gaps`, qui met à jour `gaps.md`, matière première de la
   problématique de thèse.
4. `git add -A && git commit`, car la base est versionnée.

**De temps en temps**

- `bin/pdb viz`, onglet Généalogie : suivre la lignée d'un sujet (`hls4ml`, `finn|binar`,
  `yolo`) et repérer les maillons manquants à ajouter.
- Relire une fiche contre le PDF lu vous-même (§6).
- `bin/pdb plot` : régénérer les figures dans `figures/` (benchmarks, évaluation, statistiques
  du corpus). La carte `corpus_gaps` montre les cases vides famille de plateforme × axe ou
  tâche, à confronter à `gaps.md`.
- `bin/pdb plot --check` : vérifier que les figures sont adaptées à la base. Il dit quelle
  part des lignes tombe en « autre » (plateforme ou tâche non classée) et propose des règles ;
  `/base-profile` les reprend, les éprouve et ne les écrit qu'avec votre accord (bloc `plot`
  de `base.json` : classes de tâches, familles de plateformes, figures à écarter,
  DATA_MODEL §11.2.1). `bin/pdb plot --stale` ne régénère que les figures périmées.
- Les figures suivent la base : une fois `bin/pdb plot` lancé une première fois, chaque
  `reindex` (donc chaque ajout d'article et chaque fiche) refait les figures que le
  changement a rendues périmées ; de même à la fin d'un banc `bin/pdb eval --save` pour
  les figures d'évaluation. Pour un lot de plusieurs articles, `--no-plot` (ou
  `PDB_NO_PLOT=1`) sur les étapes intermédiaires, puis un dernier `bin/pdb reindex` ;
  `"plot": {"auto": false}` dans `base.json` coupe la régénération pour la base.

**Interroger la base sans passer par Claude**

`bin/pdb bench` filtre `benchmarks.csv`, et `bin/pdb paper` affiche l'identité d'un papier.
Les réponses sont instantanées et ne consomment aucun token. Chaque ligne garde sa section
source et sa confiance, ce qui permet de vérifier chaque chiffre.

```bash
bin/pdb bench --platform kv260 --cols model,quantization,fps,power_w
bin/pdb bench --has power_w --sort fps --desc -n 5 --format md
bin/pdb bench --task detection --min fps=30 --max power_w=10
bin/pdb paper finn                  # ambigu : liste FINN et FINN-R
bin/pdb paper 1612.07119 --bench    # métadonnées + lignes de benchmark
bin/pdb paper 1612.07119 2022-feng --fields short,type   # plusieurs papiers, une ligne chacun
bin/pdb cites 2025-hozhabr --external   # ses références : dans la base, puis hors base
bin/pdb cited-by 1612.07119         # papiers de la base qui citent FINN
bin/pdb bench --own                 # vos propres mesures (paper_id own-…, DATA_MODEL §1)
bin/pdb bench --check --paper 2110.10486   # chaque valeur est-elle dans le passage cité (chunk_id) ?
bin/pdb bench --add-columns all     # une fois par base : colonnes optionnelles (chunk_id, split, batch…)
bin/pdb bench --task detection --comparable   # quelles lignes se comparent vraiment ?
```

Dans la sortie, `!` marque une ligne de confiance `low`, et les ids courts sont expliqués en
pied de sortie.

Les colonnes optionnelles de `benchmarks.csv` (DATA_MODEL §7) gardent les conditions d'une
mesure : passage source (`chunk_id`), définition de la métrique, split, résolution, batch,
protocole de mesure, valeur d'origine avant conversion. `/paper-fiche` les remplit pour les
nouvelles lignes. `--check` liste alors les valeurs introuvables dans leur passage
(statuts : [docs/RAG.md](RAG.md) §5.1). `--comparable` regroupe les lignes qui se comparent
(même tâche, jeu, split et métrique, ou portée de puissance avec `--comparable power`) et
signale celles qui en ont l'air sans l'être : à lancer avant de mettre côte à côte les
chiffres de deux papiers.

Pour le texte, `search` trouve les passages par le sens et par les mots, `show` affiche un
passage exact, et `verify` contrôle qu'une citation y figure bien :

```bash
bin/pdb search "power measured at the wall versus the FPGA rails" -k 5
bin/pdb show 1612.07119#019.3
bin/pdb verify 1612.07119#019.3 "P wall using a wall power meter"   # OK
```

`verify` répond `OK` (citation exacte), `APPROX` (ressemblance d'au moins 0,85), `NOMBRES`
(le texte ressemble, mais un nombre diffère du passage : la citation est fausse) ou
`ABSENT`. Il renvoie le code 0 seulement pour `OK` et `APPROX`.

`search` renvoie toujours des passages, même quand la base ne traite pas le sujet. Aucun
score ne permet de le détecter de façon fiable : jugez sur les extraits
([EVAL.md](EVAL.md) §6). Formulez les requêtes en anglais, la langue du corpus : en
français, la recherche perd environ la moitié de ses bonnes réponses. Dans Claude Code, `/paper-ask <question>` enchaîne
ces commandes et rend une réponse sourcée. Détails : [RAG.md](RAG.md) §5.

**Route GPU (optionnelle).** Par défaut, `search` tourne sur CPU (bge-small). Si vous avez
une carte graphique CUDA et voulez vous en servir, `bin/pdb gpu on` fait passer `search` (et
donc `/paper-ask`) sur les modèles Qwen3 : mêmes commandes, mêmes `chunk_id`, meilleure
tenue en français, ~3 s par recherche. `bin/pdb gpu` affiche l'état, `bin/pdb gpu off` revient
au CPU. La route GPU donne aussi accès à `/paper-research`, qui cherche et propose des
articles open access quand la base ne suffit pas (import seulement après votre accord).
Sans GPU, rien ne change et rien n'échoue. Détails : [RAG.md](RAG.md) §13.

---

## 6. Contrôle qualité

L'extraction et la rédaction des fiches sont automatiques, donc faillibles. Cinq réflexes :

1. **Les avertissements d'ingestion** (`bin/pdb status` liste les extractions à vérifier) :
   une section non détectée ou une table absente de `fulltext.md` signifie que ses chiffres
   manquent aussi dans la fiche. Ouvrez alors le PDF vous-même et complétez la fiche.
   La ligne « tableaux à vérifier » donne, par papier, les tableaux réduits à leur légende
   (« sans corps ») et ceux reconstruits automatiquement depuis le PDF (« reconstruits »,
   marqués « à vérifier » dans `fulltext.md` : colonnes décalées ou perdues, fragments d'OCR
   possibles). Pour les tableaux encore sans corps, `bin/pdb ingest --reparse --tables
   docling <id>` essaie Docling, et `--ocr` s'ils sont en image (plusieurs minutes par
   papier).
2. **Recouper une fiche sur cinq** avec le PDF : chaque chiffre de `benchmarks.csv` doit
   exister dans le papier, à la section indiquée.
3. **`bin/pdb reindex`** doit finir sans `erreur`. Une `note` est une remarque, pas un
   blocage.
4. **Après une modification du logiciel** (extraction, recherche, `verify`), lancez
   `bin/pdb eval --compare` : il compare la qualité et les temps au dernier run enregistré,
   et signale les seuils non atteints. `bin/pdb eval --save` enregistre un nouveau run de
   référence. Protocole et résultats : [EVAL.md](EVAL.md).
5. **Pour juger les réponses elles-mêmes**, `/eval-answers` fait répondre `/paper-ask` aux
   questions du banc, à l'aveugle, et note le run : verdict de suffisance (dont les
   questions hors corpus), citations revérifiées, valeurs attendues. Remplissez ensuite
   `grades.csv` (0 à 2 par critère) : seul un humain juge qu'un passage soutient vraiment
   la phrase. À relancer après un changement de `/paper-ask` ou du moteur de recherche
   ([EVAL.md §10](EVAL.md#10-réponses-finales-pdb-eval---answers-02102026)).

Procédure complète : [SETUP.md §8](../SETUP.md#8-vérification).

---

## 7. Dépannage

| Symptôme | Cause probable | Solution |
|---|---|---|
| `Environnement Python absent` | `.venv` non créé | `bash bin/setup.sh` |
| `GROBID ne répond pas`, backend `pymupdf` | conteneur arrêté | `bin/pdb grobid start`, puis `bin/pdb ingest --force papers/<id>/paper.pdf` pour ré-extraire (id et fiche conservés). À faire avant Docling : sans `grobid.tei.xml`, les tableaux ne sont pas repérés et n'apparaissent pas dans « tableaux à vérifier » |
| id `unknown-…` ou `…-untitled`, mauvais premier auteur | en-tête mal lu (PDF d'auteur, thèse) | déposer l'export de citation (`.bib` ou `.ris` ; pas `.nbib`) dans `inbox/` avec le PDF, puis réingérer. Il est apparié par DOI ou par titre : sans titre extrait, corriger `metadata.json` à la main |
| Premier démarrage de GROBID très long | téléchargement de l'image Docker (~1 Go) | patienter, ou `docker logs grobid` |
| `déjà ingéré` | même id arXiv, même DOI ou même PDF | rien à faire ; `--force` pour ré-extraire (la fiche n'est jamais écrasée) |
| `pas de version arXiv pour <DOI>` | article sous paywall | §4.5 |
| `OpenAlex HTTP 503` | recherche anonyme suspendue | réessayer plus tard, ou clé gratuite (§4.3) ; `--forward --backward` fonctionnent sans recherche |
| Mots coupés (« classi cation ») | ligatures perdues à l'extraction | `grep` sur un fragment plus court ; défaut connu (SETUP §9) |
| `reindex` signale `fiche.md dit … metadata.json dit …` | statut modifié d'un seul côté | aligner `fiche:` dans `fiche.md` et `status.fiche` dans `metadata.json` |
| `# route GPU indisponible : … ; moteur CPU` | route GPU demandée, mais pas de torch, pas de CUDA, ou base pas encore encodée par Qwen | `bin/pdb gpu` dit laquelle ; installer `requirements-rag.txt`, ou `bin/pdb reindex` ; sinon `bin/pdb gpu off`. La recherche a quand même répondu (CPU) |
| `rag: route GPU (Qwen3) indisponible` | `pdb rag` / `/paper-research` lancés sans GPU | utiliser `pdb search` et `/paper-ask` |

---

## 8. Plusieurs bases, autres sujets

Le pipeline ne dépend pas du domaine : chaque sujet a sa base, un dossier séparé qui partage
le code (DATA_MODEL §11). Trois bases existent aujourd'hui :

| Base | Intitulé | Dossier |
|---|---|---|
| `fpga` (par défaut) | Vision embarquée sur FPGA (YOLO, autoencodeurs, apprentissage continu) | `bases/fpga/` |
| `drone` | Vision embarquée sur drone (détection, accélérateurs, co-design système) | `bases/drone/` |
| `stage` | Apprentissage continu embarqué pour la maintenance prédictive (stage ISAE) | `bases/stage/` |

Vue d'ensemble et captures de l'interface : [README](../README.md#plusieurs-bases-de-connaissance).

**Créer une base.**

```bash
bin/pdb base new anomalies --theme "Détection d'anomalies visuelles embarquée, par autoencodeurs…"
cd bases/anomalies     # puis, dans Claude Code :  /base-profile
```

`/base-profile` lit le thème et propose des axes, des règles de classement et un périmètre
(inclus / exclus). Il n'écrit rien sans votre accord. Ensuite, `/paper-fiche` note au fil des
lectures des « suggestions en attente » dans `profile.md` (sous-thème émergent, papier hors
axes…), que `/base-profile` vous soumet plus tard.

**Passer d'une base à l'autre, ou travailler sur les deux en parallèle.** Travailler dans le
dossier de la base suffit ; deux sessions Claude Code, une dans `bases/fpga/` et une
dans `bases/drone/`, travaillent chacune sur leur base. Depuis ailleurs :
`bin/pdb --base drone status`. `bin/pdb base list` montre toutes les bases ;
`bin/pdb base use <nom>` fixe la base par défaut.

**Compléter une base depuis les autres.** `bin/pdb base scan` cherche dans vos autres bases
les articles utiles à la base courante : ceux qu'elle cite déjà sans les avoir, ceux qui
correspondent à ses règles, et les références citées des deux côtés. Puis
`bin/pdb base import drone:<paper_id>` copie un article, sans réextraction ; sa fiche repasse
à `todo`, et sa pertinence est à réévaluer avec `/paper-fiche`. `/paper-discover` fait ce
passage en premier. `bin/pdb add` signale un article déjà présent dans une autre base.

**Interface.** `bin/pdb viz`, onglet **Bases** : sélecteur de base (qui s'applique aussi aux
vues 3D et Généalogie), tableau des bases, profil et suggestions en attente, recherche dans les
autres bases avec import de la sélection, création d'une base.

Les bases créées sans `--path` vivent dans `bases/<nom>/` et sont versionnées avec le dépôt
(sans PDF). Dans un clone neuf, le registre est à refaire une fois :
`bin/pdb base register bases/fpga --name fpga`, `bin/pdb base register bases/drone --name drone`,
`bin/pdb base register bases/stage --name stage`.

Les colonnes de benchmark (`lib/schema.py`) sont communes à toutes les bases.

---

## 9. Aide-mémoire

| Terminal | Effet |
|---|---|
| `bin/pdb status` | état et prochaines actions |
| `bin/pdb add <arxiv \| doi \| pdf>…` | ajoute, ingère, réindexe |
| `bin/pdb add --from liste.txt` | ajout par lot (un identifiant par ligne, `#` pour commenter) |
| `bin/pdb ingest [--force] [pdf…]` | ingère `inbox/` et réindexe |
| `bin/pdb discover [--forward] [--backward] [--related] [--axis A] [--query "…"] [--since AAAA]` | candidats → `candidates.csv`, `candidates_arxiv.txt` |
| `bin/pdb reindex [--no-plot]` | régénère `INDEX.md`, `external_refs.csv`, vérifie, refait les figures périmées |
| `bin/pdb bench [filtres]` | filtre `benchmarks.csv` (`-h` pour les filtres) |
| `bin/pdb paper <id \| mot>…` | identité d'un ou plusieurs papiers (`--bench` : ses lignes) |
| `bin/pdb cites <id>` / `cited-by <id>` | références dans la base (`--external` : hors base aussi) / papiers qui le citent |
| `bin/pdb ingest --reparse [id…]` | ré-extrait les papiers déjà ingérés depuis leur TEI, sans GROBID |
| `bin/pdb ingest --reparse --tables docling [--ocr] [id…]` | idem, et Docling pour les tableaux restés sans corps (lent, optionnel : `requirements-docling.txt`) |
| `bin/pdb search "<q>"`, `show <id>`, `verify <id> "<cit.>"` | passages, texte exact, contrôle d'une citation |
| `bin/pdb claims <id>` / `claims [<id>] --check` | preuves atomiques d'un papier / contrôle des excerpts contre leur passage (DATA_MODEL §12) |
| `bin/pdb gpu [on\|off\|status]` | route GPU optionnelle (Qwen3, CUDA) pour `search` ; `search --gpu\|--cpu` pour une seule requête |
| `bin/pdb rag …` | outils de la route GPU : index de preuves, `acquire` / `approve` d'articles open access (RAG.md §13) |
| `bin/pdb eval [--extract\|--rag\|--speed] [--gpu] [--save] [--compare]` | banc d'évaluation du logiciel : extraction, recherche, `verify`, temps ([EVAL.md](EVAL.md)) ; `test --rag` = `eval --rag` |
| `bin/pdb eval --answers <run>…` | note les réponses enregistrées d'un run (EVAL.md §10) |
| `bin/pdb grobid start\|stop\|status` | GROBID |
| `bin/pdb viz` | visualisation (http://127.0.0.1:8050) |
| `bin/pdb plot [bench\|eval\|corpus] [--format pdf]` | figures statiques (PNG par défaut) dans `figures/` (`--list` : noms) |
| `bin/pdb plot --check` / `--stale` | classement des plateformes et tâches pour les figures, règles proposées / régénérer les seules figures périmées |
| `bin/pdb test` | tests |
| `bin/pdb agents [--report] [--scan] [--session <id>]` | journal et coût des sous-agents Claude Code, économie estimée de la délégation et cas défavorables (`--worst N`), bilan d'une session ; `--mark <id> repris\|corrigé\|refait` après vérification |
| `bin/pdb base list \| new \| use \| info \| check` | gérer les bases (§8) |
| `bin/pdb base scan [--from NOM]` / `base import NOM:<id>` | articles utiles dans les autres bases / copie |
| `bin/pdb --base NOM <commande>` | agir sur une autre base que celle du dossier courant |

| Claude Code | Effet |
|---|---|
| `/paper-add <arxiv \| doi \| pdf>` | ajoute et compare à la note de départ |
| `/paper-fiche <paper_id>` | fiche de lecture et lignes de benchmark |
| `/paper-extract <paper_id>` | preuves atomiques `claims.jsonl`, chacune liée à un passage vérifié (après la fiche) |
| `/paper-gaps` | met à jour `gaps.md` |
| `/paper-discover [axe \| gap \| mots-clés]` | propose des papiers à ajouter et attend votre accord |
| `/paper-ask <question>` | réponse sourcée et vérifiée depuis la base (CPU, ou Qwen si la route GPU est active) |
| `/paper-research <question>` | route GPU seulement : réponse avec boucle de lacunes et acquisition open access, après votre accord |
| `/base-profile [consigne]` | propose d'affiner le profil de la base (axes, règles, périmètre) ; applique après accord |
| `/eval-answers [answers\|answers_holdout]` | fait répondre `/paper-ask` aux questions du banc, à l'aveugle, puis note le run (EVAL.md §10) |

| Fichier | Rôle | Qui l'écrit |
|---|---|---|
| `INDEX.md` | liste des papiers par axe | `reindex` (généré) |
| `benchmarks.csv` | tous les chiffres, avec section source | `/paper-fiche` |
| `papers/<id>/fiche.md` | lecture critique | `/paper-fiche` |
| `papers/<id>/claims.jsonl` | preuves atomiques, contrôlées par `reindex` et `pdb claims --check` (DATA_MODEL §12) | `/paper-extract` |
| `gaps.md` | zones non couvertes | `/paper-gaps` |
| `external_refs.csv` | travaux cités mais absents | `reindex` (généré) |
| `candidates.csv`, `candidates_arxiv.txt` | candidats à l'ajout | `discover` (généré, non versionné) |
