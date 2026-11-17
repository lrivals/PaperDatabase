# Carte des gaps — Vesuvius Challenge : lecture virtuelle des rouleaux d'Herculanum

Zones non couvertes et verrous repérés dans le corpus. Mis à jour par `/paper-gaps` à partir
des fiches `done` et de `benchmarks.csv`. Chaque gap cite les `paper_id` qui l'étayent, avec
la section de fiche d'où vient le constat, et distingue ce qui est lu de ce qui est déduit.

Format d'une entrée :

```
### <intitulé du gap>
- Constat : ce que montre le corpus (paper_id, section source).
- Ce qui manque : la question laissée ouverte.
- Statut : hypothèse (déduite de la bibliographie de départ) | étayé (fiches done).
- Piste : expérience ou lecture pour le confirmer.
```

Abréviations des sections de fiche : **L** = « Limites et critique », **G** = « Gaps
identifiés », **P** = « Pertinence ».

---

Mise à jour du 17/11/2026 (1er passage) : **45 fiches `done` sur 45**, **141 lignes** dans
`benchmarks.csv` (20 papiers). `bin/pdb bench --comparable` : **aucun groupe ne réunit deux
papiers** (109 groupes d'un seul papier) ; aucune comparaison chiffrée entre papiers n'est
donc valable en l'état.

**Hors de ce passage** : 8 papiers fichés le même jour par une autre session et fusionnés ensuite (2004-seales, 2005-lin, 2012-mills, 2015-allegra, 2017-baum, 2020-mahnke, 2022-wang THz, 2025-hoffmann xénon) ; la base compte 53 fiches. Ils concernent surtout l'historique du déroulage et les modalités (gaps A4, D4, D5) : à intégrer au 2e passage.

Précautions de lecture :
- **11 papiers sont des dépôts communautaires récents** (10 de type `repo`, plus Rectina,
  `2026-pellerano-rectina-m3-m4-dense-ink`, `preprint` hébergé sur GitHub ; voir
  [veille_communaute.md](veille_communaute.md)) : non relus, chiffres auto-déclarés,
  extraction PyMuPDF aux tableaux aplatis (lignes surtout tirées de la prose, `confidence:
  medium`). Ils fournissent 69 des 141 lignes et presque toutes les mesures sur rouleaux
  entiers. Un gap qui ne repose que sur eux le dit (mention **[dépôts]**).
- **Colonnes de `benchmarks.csv`** : l'en-tête vient d'un schéma FPGA. `fps`, `gops`,
  `power_w`, `power_scope`, `luts`, `dsps`, `bram` sont `n/r` sur 141/141 lignes,
  `latency_ms` sur 135, `batch` sur 131 : ce sont des `n/r` **structurels**, pas des gaps de
  la littérature (suggestion d'en-tête adapté déjà en attente dans `profile.md`). Les
  manques du domaine sont listés à part, en fin de fichier.
- Le corpus (45 papiers) est petit et biaisé par la bibliographie de départ (travaux
  EduceLab / Seales, groupe Mocella–Bukreeva, papyrologie italienne) et par la veille
  Discord. Les axes `self-supervised-3d` (0 papier) et `super-resolution` (1 papier, hors
  papyrus) sont quasi vides : tout gap qui s'appuie sur ce vide est une `hypothèse`.
- Hors dépôts, 9 preprints et 2 rapports (Zenodo) ne sont pas relus par les pairs, dont
  arxiv-2606.29085 (lecture complète d'un rouleau) et arxiv-2304.02084 (EduceLab-Scrolls).

## Couverture croisée (tâche × résolution / scan × rouleau)

Lu dans `benchmarks.csv` (colonnes `dataset`, `dataset_split`) et dans les fiches ; « VT » =
vérité terrain indépendante du modèle évalué.

| Tâche | Fragments ≤ 4 µm | Rouleau 2,4 µm | Rouleau 7,9–9,6 µm | Autre modalité | VT indépendante ? |
|---|---|---|---|---|---|
| Encre | arxiv-2308.05070 (3,2 µm), 2023-mou (4 µm), arxiv-2304.02084, 2019-parker | nexusai (1 ROI, Paris 4) ; arxiv-2606.29085 (Paris 4, qualitatif) | pellerano (~9 µm, 14 unités), ruiconte (0841, 1447), snyder (0841), de-vore (9,6 µm, Paris 4), korotetskyi (Scroll 5), gilman ×2, de-meij (0306B), betka | arxiv-2603.27698 (profilométrie), 2025-ceccarelli (thermographie), 2019-tournie (SWIR), 2026-hoffmann (xénon, modèle) | IR sur fragments seulement ; sur rouleaux : masques d'organisateurs ou labels d'équipe |
| Surface / enroulement | — | de-vore (scan 2,4 µm lu à 9,6 µm) | arxiv-2512.04927 (Paris 4, 7,91 µm), winding-field (Paris 4), betka (8 rouleaux), gilman (4 + 13 rouleaux), snyder (cubes, 0139) | — | maillage manuel partiel de Paris 4 ; contrôles de développement de HerculeX ; rien ailleurs |
| Aplatissement / distorsion | — | — | betka (« isométrique » 81–86 %) | arxiv-2007.15551 (En-Gedi), 2021-stabile (12 / 47 µm), 2021-dambrogio (lettres pliées) | aucune |
| Super-résolution | — | — | — | arxiv-1907.07131 (roches, 2D, LR synthétique) | aucune sur papyrus |
| Auto-supervisé 3D | — | — | — | — | — |

Lecture (déduit) : (1) les mesures d'encre sur rouleaux viennent presque toutes des dépôts ;
(2) la géométrie quantitative se concentre sur **PHerc. Paris 4** (arxiv-2512.04927,
de-vore, winding-field, nexusai, arxiv-2606.29085) ; (3) aucune case « même rouleau, deux
résolutions, même métrique » n'est remplie.

---

## A. Signal d'encre et résolution

### Part du signal d'encre carbonée qui survit à 8–9 µm : jamais mesurée sur paires de scans
- Constat : le seuil de résolution est soit non quantifié (2019-parker-invisibility-readability-recovering-ink-herculaneum,
  G : « seuil 3-12 µm non quantifié, pas de test à 8-9 µm »), soit mesuré hors CT
  (arxiv-2603.27698-ink-detection-surface-topography-herculaneum, L : seuil ≈ 1 µm par
  dégradation par blocs de profils de surface, sans PSF ni bruit de scanner), soit affirmé
  qualitativement (arxiv-2304.02084-educelab-scrolls-verifiable-recovery-text, G : effet de
  2,2 à 24 µm « non mesuré »). La seule comparaison 7,91 / 2,4 µm confond gain de modèle et
  gain de scan (arxiv-2606.29085-complete-virtual-unwrapping-reading-rolled, L, Fig. 3).
  Côté dépôts : traits ~2 fois trop larges à 9,6 µm (2026-de-vore-vesuvius-ply-layers-separating-pressed,
  L) ; Argus V1 entraîné sur rendus 2,4 µm poolés perd contre Reader V3 en natif 9 µm
  (2026-ruiconte-ink-swarm-argus-v1-v2, L) ; perte de 4 % de corrélation à 8,64 µm citée sans
  mesure publiée (2026-limegs-ink-sdk-standalone-inference-sdk, G).
- Ce qui manque : une courbe « métrique d'encre en fonction de la résolution » sur un même
  rouleau scanné à 2,4 et 7,9–9 µm, mêmes labels, même modèle réentraîné à chaque résolution.
- Statut : étayé (6 fiches le listent en G ou L ; volet dépôts : 3 fiches **[dépôts]**).
- Piste : sur PHerc. Paris 4 (scanné à 2,4 et 7,91 µm d'après de-vore et
  arxiv-2606.29085 ; PHerc0841 existe aussi en rendu poolé depuis 2,4 µm et en scan natif
  113 keV, 2026-ruiconte-ink-swarm-argus-v1-v2 #001.2), entraîner le même lecteur à 2,4 µm, à 2,4 µm poolé ×4 et à
  7,91 µm natif ; mesurer AUC et lisibilité des lettres sur les mêmes masques.

### Super-résolution volumétrique sur paires réelles recalées et mesure d'hallucination
- Constat : un seul papier de super-résolution, sur roches, en 2D, avec basse résolution
  synthétique (bicubique) ; les auteurs admettent que le PSNR ne mesure pas la texture
  générée et que la texture extrapolée appelle un « scepticisme légitime »
  (arxiv-1907.07131-boosting-resolution-recovering-texture-micro, L et G). Les modèles
  d'encre sont décrits comme « amplificateurs de visibilité » sans mesure du risque
  d'hallucination (arxiv-2606.29085, L, G).
- Ce qui manque : SR 3D 9 → 2,4 µm sur paires réelles recalées ; métrique qui teste la
  préservation du signal d'encre (lecteur aval, contrôle placebo) plutôt que PSNR / SSIM ;
  comparaison à la distillation enseignant 2,4 µm → élève 9 µm et au réentraînement natif.
- Statut : **hypothèse** pour l'absence de littérature (axe `super-resolution` quasi vide,
  biais de la bibliographie de départ) ; étayé pour l'insuffisance du PSNR (1 fiche).
- Piste : `/paper-discover super-resolution` (SR volumétrique micro-CT sur paires réelles,
  géosciences et matériaux ; distillation entre résolutions) ; protocole : SR entraînée sur
  Paris 4, lecteur 2,4 µm appliqué à la sortie, contrôle sur zones sans encre et sur ordre de
  profondeur inversé.

### Lien composition de l'encre (Pb, liant) ↔ contraste ou texture en micro-CT
- Constat : le Pb est mesuré sur 2 fragments seulement, sans lien chiffré au contraste CT
  (2016-brun-revealing-metallic-ink-herculaneum-papyri, L et G ; 2016-tack-tracking-ink-composition-herculaneum-papyrus,
  G : « lien quantitatif entre concentration de Pb, épaisseur d'encre et contraste … à
  8-9 µm : non traité ») ; fréquence de l'encre plombifère inconnue (2021-damiani-ink-herculaneum-survey-recent-perspectives,
  G) ; rouleau modèle lisible grâce au dopage Pb, cas carbone pur non démontré
  (2026-seiler-model-carbonized-papyrus-scroll-opens, L, G) ; réglure au plomb non cherchée
  en CT (2023-romano-layout-ancient-greek-papyri-through, G).
- Ce qui manque : savoir si la variabilité de l'encre entre rouleaux explique les échecs de
  transfert des lecteurs (voir E).
- Statut : étayé (5 fiches).
- Piste : croiser la liste des rouleaux où les lecteurs réussissent / échouent avec les
  données XRF publiées ; chercher Tack et al. / Brun et al. suivants (spéciation sur d'autres
  fragments).

### Modalités alternatives jamais confrontées au CT sur le même fragment
- Constat : xénon par sorption sur échantillon modèle seulement, sans paires avec / sans
  xénon (2026-hoffmann-xenon-contrast-carbon-ink-tomography, L, G) ; thermographie
  (2025-ceccarelli-pulsed-thermographic-analysis-herculaneum-papyri, G : aucun lien avec le
  signal CT), SWIR (2019-tournie-ancient-greek-text-concealed-back, G : pas de transfert vers
  les prédictions CT), topographie (arxiv-2603.27698, G : « aucune mesure en volume CT
  réel »), radar sub-THz (2025-verde-sub-terahertz-radar-imaging-ancient, G).
- Ce qui manque : un fragment imagé en CT (8–9 et 2,4 µm), IR/SWIR, profilométrie et XRF,
  pour décider quel mécanisme (relief, densité, Pb) porte le signal appris.
- Statut : étayé (5 fiches).
- Piste : rechercher les jeux de fragments multimodaux d'EduceLab (arxiv-2304.02084 en
  donne le principe pour IR + CT).

## B. Comparabilité des métriques d'encre

### Métriques d'encre non comparables entre papiers (unité, résolution, labels, code de lecture)
- Constat : `--comparable` ne trouve aucun groupe de deux papiers. Les lecteurs rapportent
  AUC par unité à fenêtre choisie, fond différent entre unités tenues à l'écart et contrôles
  (2026-pellerano-rectina-m3-m4-dense-ink, L : « ces deux AUC ne sont pas comparables ») ;
  AUC moyenne de 3 fenêtres, seuils « 80 % recall » propres à chaque modèle, rendus 2,4 µm
  poolés vs natifs (2026-ruiconte-ink-swarm-argus-v1-v2, L) ; ROC-AUC / F0.5 sur une ROI
  (2026-nexusai-kevin-vesuvius-ink-bench-volumetric-ink, L) ; MCC dépendant d'une bande δ
  choisie a priori (2026-korotetskyi-volumetric-texture-analysis-unsupervised-ink, L) ;
  Dice à split, seuil et post-traitement inconnus (2023-mou-ink-detection-carbonized-herculaneum-papyri,
  L) ; Fβ d'un modèle vs Fβ d'un ensemble Kaggle (arxiv-2308.05070-volumetric-fast-fourier-convolution-detecting,
  L). Le même checkpoint donne r = 0,079 avec un runner générique contre 0,885 avec le sien :
  le prétraitement n'est pas interchangeable (2026-limegs-ink-sdk-standalone-inference-sdk,
  L, et veille_communaute.md).
- Ce qui manque : un protocole commun (segments, résolution, labels, normalisation, fenêtre
  de profondeur, métrique à seuil fixé a priori) pour classer les lecteurs.
- Statut : étayé (7 fiches ; la partie « lecteurs sur rouleaux » repose sur 4 **[dépôts]**).
- Piste : utiliser ink-sdk comme banc, Reader V3, Argus V2, Rectina m4 sur les mêmes 6
  contrôles de Rectina, avec un seul code de lecture.

### Gains annoncés sous le bruit : pas d'intervalle de confiance, pas de graines
- Constat : bruit mesuré 0,013 (exactitude équilibrée) contre un gain de m4 sur Reader v3 de
  +0,0056 AUC en moyenne, une graine, aucune ablation (2026-pellerano-rectina-m3-m4-dense-ink,
  L, G) ; 0,928 contre 0,922 sans IC (2026-ruiconte-ink-swarm-argus-v1-v2, L) ; un seul run
  (2026-nexusai-kevin-vesuvius-ink-bench-volumetric-ink, L) ; +0,01 Fβ sur un fragment de
  test (arxiv-2308.05070, L) ; écarts de quelques points de Dice sans test (2023-mou, L).
- Ce qui manque : variance entre graines et IC par bootstrap sur segments, avant tout
  classement de lecteurs.
- Statut : étayé (5 fiches ; 3 **[dépôts]**).
- Piste : réentraîner un lecteur 3 graines × 3 découpages et publier l'écart-type de l'AUC ;
  bootstrap par segment sur les 14 unités de Rectina.

### Labels non indépendants du modèle, décalés ou circulaires
- Constat : labels posés sur les cartes du modèle (2026-de-meij-pherc-0306b-winding-w040-row,
  L) ; « vérité » = prédictions d'un réseau supervisé (2026-korotetskyi, L) ; labels dessinés
  sur la surface officielle qui avantagent celle-ci, modèle d'encre ayant peut-être vu la
  région (2026-de-vore, L) ; décalage de 7 px mesuré, 11 segments sur 87 contrôlés
  (2026-pellerano, L) ; accord inter-relecteurs kappa 0,12 (2026-snyder-scroll-label-snap-snapping-approximate,
  L) ; désalignement IR / CT non discuté (arxiv-2308.05070, L) ; labels de provenance non
  dite (2026-nexusai, L).
- Ce qui manque : labels indépendants de la surface et du modèle (IR de fragments recalé,
  traces manuelles en double aveugle) et mesure de l'effet du bruit de labels sur l'AUC.
- Statut : étayé (7 fiches ; 5 **[dépôts]**).
- Piste : sur un segment, comparer AUC avec labels organisateurs, labels décalés de ±7 px et
  labels tirés des cartes du modèle : l'écart borne le biais de circularité.

### La lisibilité (lettres, CER) n'est jamais la métrique
- Constat : la lisibilité visuelle ne suit pas toujours le Dice (2023-mou, L, §IV-A) ; 15
  caractères de vérité terrain au total (arxiv-2304.02084, L) ; lecture par inspection
  experte sans métrique (arxiv-2606.29085, L ; 2015-mocella-revealing-letters-rolled-herculaneum-papyri,
  L) ; préférence subjective, pas d'erreur de transcription
  (arxiv-2104.01106-personalizing-image-enhancement-critical-visual, G).
- Ce qui manque : une métrique de lecture (lettres identifiées à l'aveugle, CER contre une
  transcription connue) reliée aux métriques pixel.
- Statut : étayé (5 fiches).
- Piste : sur les fragments à texte connu, mesurer la corrélation AUC pixel ↔ lettres lues à
  l'aveugle par 2 lecteurs.

## C. Faux positifs et contrôles

### Contrôles de faux positifs non standardisés (ordre de profondeur inversé, face aveugle, placebo)
- Constat : les seuls contrôles rapportés viennent des dépôts. Ordre de profondeur inversé :
  AUC 0,53 (attendu ~0,5), mais sur un jeu non précisé et sans labels humains dans les zones
  marquées en plus (2026-ruiconte, L, ligne `benchmarks.csv`) ; face aveugle jugée à l'œil,
  sans seuil (2026-de-meij, L, G) ; la « liveness gate » accepte une carte lue dans le
  mauvais sens (2026-limegs-ink-sdk, L, G). Côté articles : aucun placebo, aucune lecture
  inversée (2019-parker, L ; arxiv-2304.02084, G ; arxiv-2603.27698, G ; arxiv-2606.29085, L ;
  arxiv-1706.09883-investigating-herculaneum-papyri-innovative-3d, G) ; cartes d'encre de
  8 rouleaux entiers sans contrôle (2026-betka-herculex-virtual-unwrapping-whole-herculaneum, G).
- Ce qui manque : un jeu de contrôles chiffrés et reproductibles (inversion de profondeur,
  face opposée, zone sans papyrus, volume permuté) avec taux de faux positifs attendu.
- Statut : étayé (8 fiches) ; les contrôles existants reposent sur 3 **[dépôts]**.
- Piste : reproduire le test d'inversion de ruiconte avec Reader V3, Argus V2 et Rectina m4
  sur les 6 contrôles de Rectina, et chiffrer la face aveugle de de Meij (part de pixels >
  seuil, comparée à la face lue).

### Probabilités d'encre non calibrées, seuils choisis sur les labels d'évaluation
- Constat : 5–10 % de pixels > 0,5 sur des surfaces sans lettres identifiées
  (2026-gilman-first-letters-clean-sheets-173, G) ; F0.5 « optimal » à seuil choisi sur les
  labels d'évaluation (2026-nexusai, L) ; seuil réglé sur la couverture d'encre de la
  référence (2026-korotetskyi, L) ; aucune calibration (2026-pellerano, G ;
  arxiv-2308.05070, G ; 2023-mou, G).
- Ce qui manque : calibration (ECE, courbes de fiabilité) et incertitude des cartes, seuil
  fixé hors du jeu d'évaluation.
- Statut : étayé (6 fiches ; 3 **[dépôts]**).
- Piste : calibration par température sur segments tenus à l'écart, puis taux de pixels
  > seuil sur des enroulements sans encre attendue.

### Faux positifs structurels (fibres, trous, plis, artefacts) jamais quantifiés
- Constat : fibres confondues avec l'encre (2019-parker, L ; 2026-korotetskyi, L : séparation
  encre / fibre en travail futur) ; trous, fissures et plis affichés comme encre
  (2019-tournie, L ; arxiv-1706.09883, L) ; apophénie reconnue (2015-mocella, L).
- Ce qui manque : taux de faux positifs par type de structure, sur des zones annotées
  « fibre / pli / trou sans encre ».
- Statut : étayé (5 fiches).
- Piste : annoter 50 régions sans encre par type de structure et mesurer la réponse des
  lecteurs.

### Pas de témoin d'encre connue ni de banc synthétique à texte connu pour les rouleaux 8–9 µm
- Constat : « absence de témoin d'encre connue sur les rouleaux 8-9 µm » (2026-gilman-first-letters-clean-sheets-173,
  G) ; banc synthétique carbone pur à 8–9 µm évoqué comme perspective
  (2026-seiler, G) ; banc physique non quantitatif (arxiv-2504.11485-deciphering-scrolls-tomography-training-experiment,
  G) ; rouleau modèle au xénon sans scan original (2026-hoffmann, L).
- Ce qui manque : un rouleau modèle carbonisé, encre carbone pure, texte connu, scanné aux
  résolutions du Challenge : la seule vérité terrain où les faux positifs se comptent.
- Statut : étayé (4 fiches) ; l'absence d'un tel banc publié est une hypothèse (corpus petit).
- Piste : chercher les suites de Seiler et al. (rouleaux modèles d'EduceLab ou de l'ESRF).

## D. Géométrie : surfaces, enroulements, aplatissement

### Pas de vérité terrain géométrique hors rouleaux de référence : la « bonne spire » ne se mesure pas
- Constat : 69 290 cm² produits sur 8 rouleaux sans maillage publié, sans mesure
  d'enroulement correct ; scores sur contrôles de développement, pas de holdout
  (2026-betka, L, G) ; dérive intrafibre de 1,34 feuillet à 30–45 mm, couverture 36,8 %,
  séparation entre feuillets voisins montrée en synthétique seulement
  (2026-limegs-winding-field-continuous-winding-coordinate, L, G) ; « snap » = cohérence avec
  m7, pas exactitude (2026-gilman-spiral-fit-inputs-first-windings, L, G) ; mono-couche non
  prouvée (2026-gilman-first-letters-clean-sheets-173, G) ; critère « plis » circulaire
  (2026-de-vore, L, G). Seul article relu avec VT : maillage manuel partiel de Paris 4, nnU-Net
  d'entrée entraînés sur le même rouleau, ChD unidirectionnel
  (arxiv-2512.04927-virtually-unrolling-herculaneum-papyri-diffeomorphic, L, G).
- Ce qui manque : une métrique de « bonne spire » utilisable sans maillage d'expert (par
  exemple cohérence de fibres traversantes, continuité du texte, comptage d'enroulements
  depuis l'ombilic) et un holdout géométrique.
- Statut : étayé (6 fiches) ; 5 **[dépôts]**, un seul article relu.
- Piste : tester une métrique de « wrong-wrap » sur Paris 4 en masquant le maillage d'expert,
  puis l'appliquer à un rouleau First Letters ; lire les métriques officielles TopoScore / VOI
  citées par snyder.

### Pas de comparaison de pipelines de surface sur les mêmes crops et métriques
- Constat : HerculeX non comparé à villa / Lasagna / ThaumatoAnakalyptor (2026-betka, G) ;
  winding-field comparé seulement à sa version antérieure (2026-limegs-winding-field, L) ;
  diffeomorphic spiral fitting contre ThaumatoAnakalyptor seul, 3 métriques communes
  (arxiv-2512.04927, L, G) ; de-vore sans comparaison chiffrée (L, G) ; méthodes classiques
  sans baseline (2018-dahl-layered-surface-detection-virtual-unrolling, L ;
  2018-rosin-virtual-recovery-content-x-ray, G ; arxiv-2308.07070-local-iterative-extraction-2d-manifolds,
  L).
- Ce qui manque : un banc de surface commun (crops, VT, ChD bidirectionnel, WJF, TopoScore).
- Statut : étayé (7 fiches).
- Piste : rejouer HerculeX (version CUDA à faire) et la spirale de Henderson sur le crop
  Paris 4 d'arxiv-2512.04927, mêmes métriques.

### Qualité de surface → qualité d'encre : un seul résultat, négatif
- Constat : meilleure géométrie après snapping, mais carte d'encre préférée sans snapping
  (75 contre 31, test pré-enregistré) (2026-snyder, L) ; lien ChD / WJF ↔ encre non mesuré
  (arxiv-2512.04927, G) ; lien distorsion ↔ lecture non étudié
  (arxiv-2007.15551-quantitative-distortion-analysis-flattening-applied, G) ; effet du
  protocole de surface sur le score d'encre (2026-de-vore, G) ; « 89 % du signal d'encre
  conservé » de définition vague (2026-betka, L).
- Ce qui manque : savoir quel critère géométrique prédit la lisibilité (position dans
  l'épaisseur, distance à la face recto, lissage).
- Statut : étayé (5 fiches ; le seul résultat chiffré vient d'un **[dépôt]**).
- Piste : sur w052 (snyder), décaler la surface de ±1–3 voxels le long de la normale et
  tracer l'AUC du lecteur.

### Distorsion d'aplatissement : pas de métrique commune ni de comparaison SLIM / ARAP / LSCM sur segments 8–9 µm
- Constat : comparaison ABF / LSCM / masse-ressort sur En-Gedi, SLIM et flatboi non couverts
  (arxiv-2007.15551, L, G) ; LSCM / ABF sans métrique chiffrée, ARAP / SLIM non testés
  (2021-stabile-computational-platform-virtual-unfolding-herculaneum, L, G) ; carte de
  contrainte d'arête sans comparaison (2021-dambrogio-unlocking-history-through-automated-virtual,
  G) ; « isométrique » à ±10 % pour 81–86 %, distorsion non bornée ailleurs (2026-betka, L) ;
  indicateurs aspect / aire / skew non repris (2018-dahl, G).
- Ce qui manque : distorsion (aire, angle, longueur) mesurée par la même métrique pour SLIM,
  ARAP, LSCM, flatboi sur un même segment d'Herculanum, et son effet sur la forme des lettres.
- Statut : étayé (5 fiches).
- Piste : appliquer les métriques d'arxiv-2007.15551 à un segment tifxyz aplati par SLIM et
  flatboi.

### Zones compressées, feuillets en contact, plis et kolleseis
- Constat : feuillets qui se touchent non résolus (2018-rosin, L, G) ; structures
  tangentiellement connectées en échec (arxiv-2308.07070, L, G) ; hypothèse d'une feuille
  unique sans plis (arxiv-2512.04927, L, G) ; fusions, trous, changements de feuillet en zones
  compressées (arxiv-2606.29085, L, G) ; une couche, pire couche doublée à 46–55 %
  (2026-de-vore, L) ; repliements et cassures ouverts (2026-limegs-winding-field, G).
- Ce qui manque : évaluation dédiée aux zones écrasées ; rien sur les kolleseis.
- Statut : étayé pour les zones compressées (6 fiches) ; **hypothèse** pour les kolleseis
  (aucun papier ne les traite : absence dans un corpus petit).
- Piste : `/paper-discover` sur la segmentation d'instances 3D de couches minces en contact
  (géologie sismique, biologie) ; isoler un jeu de crops « compressés » de Paris 4.

## E. Transfert de domaine entre scans et rouleaux

### Transfert entre énergie, résolution, scanner et prétraitement : non mesuré
- Constat : bloc 113 keV de 2 unités d'un seul rouleau, « rien à en conclure »
  (2026-pellerano, L) ; méthode sans entraînement qui marche sur Scroll 5 et échoue sur
  Scroll 1, cause non analysée (2026-korotetskyi, G) ; généralisation inter-papyrus 0,691
  puis 0,475 sur PHerc. 500P2 (arxiv-2603.27698, L, G) ; prétraitement non interchangeable
  (2026-limegs-ink-sdk, L) ; transfert 2,4 → 9 µm sans fine-tuning non résolu
  (2026-ruiconte, G) ; synchrotron ↔ laboratoire non fait (arxiv-2304.02084, G) ;
  normalisation des intensités non explorée (2019-parker, L, G) ; phase ↔ absorption non
  traité (arxiv-1602.08071-enhanced-x-ray-phase-contrast, G).
- Ce qui manque : une matrice rouleau × énergie × résolution × lecteur, et l'effet d'une
  harmonisation d'histogrammes ou d'une augmentation dédiée.
- Statut : étayé (8 fiches ; 4 **[dépôts]**). Littérature générale d'adaptation de domaine
  volumique : absente du corpus (**hypothèse**).
- Piste : comparer Scroll 1 et Scroll 5 (énergie, résolution, histogrammes) pour expliquer
  l'échec de korotetskyi ; `/paper-discover domain-transfer`.

### Évaluation sur rouleau entièrement tenu à l'écart : presque absente
- Constat : unités « tenues à l'écart » = segments de rouleaux d'entraînement
  (2026-pellerano, L, G) ; 2 rouleaux natifs seulement (2026-ruiconte, G) ; checkpoint ayant
  pu voir Paris 4 (2026-nexusai, L, G) ; nnU-Net entraînés sur le rouleau évalué
  (arxiv-2512.04927, L) ; fragments ou moitiés d'un même fragment (arxiv-2304.02084, L ;
  2023-mou, L ; arxiv-2308.05070, G) ; validation par échantillon et non par papyrus
  (arxiv-2603.27698, L).
- Ce qui manque : un découpage par rouleau (leave-one-scroll-out) avec labels
  d'organisateurs.
- Statut : étayé (8 fiches).
- Piste : leave-one-scroll-out sur les rouleaux à labels organisateurs de Rectina (4 unités
  sur 6 contrôles).

## F. Labels rares et pré-entraînement

### Pré-entraînement auto-supervisé 3D sur scans de rouleaux : aucun papier
- Constat : l'axe `self-supervised-3d` est vide dans INDEX.md. Seul indice : un
  pré-entraînement 2D sur lettres grecques n'apporte rien (Dice 0,664 contre 0,679,
  2023-mou, L, G).
- Ce qui manque : DINO / MAE volumiques sur volumes non étiquetés de rouleaux, gains en
  régime peu étiqueté pour l'encre et la surface.
- Statut : **hypothèse** (absence de papiers ; corpus biaisé par la bibliographie de départ,
  la littérature générale existe sans doute ailleurs).
- Piste : `/paper-discover self-supervised-3d` (MAE / DINO volumiques en imagerie médicale et
  matériaux) ; premier essai : MAE sur crops 9 µm non étiquetés, sonde linéaire sur l'encre.

## G. Reproductibilité

### Code et poids : les articles relus publient peu, les dépôts publient sans reproduction tierce
- Constat : parmi les articles relus, code publié pour 2021-dambrogio, arxiv-2512.04927 et
  arxiv-2504.11485 (P / L de leurs fiches) ; pas de code pour 2016-seales-damage-discovery-virtual-unwrapping-reading,
  2018-dahl, 2021-stabile, 2026-seiler, arxiv-2308.07070, arxiv-1907.07131 (L), code annoncé
  non vérifié pour arxiv-2308.05070 (L), poids non publiés pour 2023-mou (L), Methods non
  extraits pour arxiv-2606.29085 (L). Les dépôts publient code ou poids (souvent CC BY-NC)
  mais « personne en dehors des auteurs n'a lancé ces fichiers »
  (2026-gilman-spiral-fit, L) ; HerculeX sans version CUDA (2026-betka, G) ; reproductibilité
  des poids dépendante de la version de torch (2026-limegs-ink-sdk, L).
- Ce qui manque : reproduction indépendante d'au moins un lecteur et d'un pipeline de
  surface ; poids des lecteurs des articles relus.
- Statut : étayé (12 fiches) ; plusieurs fiches ne disent rien du code (non mentionné ≠ absent).
- Piste : reproduire Rectina m4 (recette et empreintes publiées) sur la RTX 5090 et comparer
  aux CSV de l'annexe D.

## H. Papyrologie et validation de lecture

### Priors papyrologiques jamais utilisés pour valider une prédiction ; lectures non indépendantes
- Constat : mise en page (inclinaison de Maas, intercolonnes, réglure) proposée comme prior
  sans méthode (2023-romano, G) ; colonnes et mains documentées, sans lien avec la CT
  (2019-tournie, P) ; confirmations de lecture par les éditeurs des textes eux-mêmes
  (2025-ceccarelli, L) ; restitutions d'experts sujettes au biais de confirmation
  (arxiv-1602.08071, L) ; lettres incertaines sans relecture tierce (2026-de-meij, L).
- Ce qui manque : un test qui utilise la géométrie de la mise en page (lignes parallèles,
  hauteur de lettre, intercolonnes) pour accepter ou rejeter une carte d'encre, et une
  lecture à l'aveugle par des papyrologues indépendants.
- Statut : étayé pour le constat (5 fiches) ; l'absence de méthode est une **hypothèse**.
- Piste : sur la rangée w040 de de Meij, vérifier l'alignement des 5 lettres sur une ligne et
  leur hauteur contre les normes paléographiques ; faire lire à l'aveugle les deux faces.

---

## Manques du domaine dans `benchmarks.csv` (hors `n/r` structurels)

À distinguer des colonnes FPGA vides. Métriques ou champs que la littérature du domaine ne
rapporte pas, ou que le schéma ne sait pas porter :

| Manque | Constat | Statut |
|---|---|---|
| IC / variance des AUC d'encre | aucune ligne d'encre avec IC ou graines (pellerano, ruiconte, nexusai, 2308.05070) | étayé |
| Métrique de « bonne spire » | `wrong-wrap share` seulement sur un contrôle de développement (betka) ; WJF sur Paris 4 (arxiv-2512.04927) | étayé |
| Évaluation inter-rouleaux | `dataset_split` vide sur 83/141 lignes ; aucune ligne leave-one-scroll-out | étayé |
| Résolution, énergie, rouleau, nature des labels | portés en texte libre dans `dataset` ; pas de colonne (suggestion en attente dans `profile.md`) | schéma |
| Métrique de lecture (lettres, CER) | une seule ligne (arxiv-2304.02084, caractères sur 15) | étayé |
| Taux de faux positifs sur contrôle | 2 lignes (`encre fausse à rappel 80 %`, pellerano) et 1 ligne d'inversion de profondeur (ruiconte) | étayé **[dépôts]** |
| Distorsion d'aplatissement | Str / AD (arxiv-2512.04927) ; rien d'autre | étayé |
