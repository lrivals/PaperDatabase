# Veille communauté — dépôts repérés dans « show and tell » (Discord Vesuvius Challenge)

Relevé du 2026-11-17, fait à partir des README GitHub seuls. Ce sont des **dépôts
communautaires** : non relus par les pairs, sans papier ni DOI, et tous les chiffres
sont **auto-déclarés** (aucune reproduction indépendante). Ils ne sont pas ingérés dans
`papers/` et n'ont pas de lignes dans `benchmarks.csv`, faute de PDF et de passage source
vérifiable (`chunk_id`). Section source de chaque chiffre : le README du dépôt.

Non consulté : <https://journal.vesuvius.alive.monster/>, refusé par le réseau de la
session cloud (proxy 403). À relire quand l'hôte sera autorisé.

## Vue d'ensemble

| Dépôt | Étape de la chaîne | Données | Matériel | Résultat principal (auto-déclaré) | Licence | Maturité |
|---|---|---|---|---|---|---|
| [nexusai-kevin/vesuvius-ink-bench](https://github.com/nexusai-kevin/vesuvius-ink-bench) | inférence encre volumique, banc de débit | PHerc0332 (L2) ; PHercParis4 seg. 20230702185753 (2,4 µm) | RTX 5080 | AUC 0,9546 ; F0.5 0,7903 à th = 0,5 ; ~2,5 Gio VRAM | MIT | 4 commits, 0 étoile |
| [Victoria-TechNexus/vesuvius-ply-layers](https://github.com/Victoria-TechNexus/vesuvius-ply-layers) | séparation des couches par plis recto/verso, maillage, aplatissement | PHerc. Paris 4 à 9,6 µm, 6 tuiles 192×416×416 | T4 (Colab) | 99,6 % de surface sur papyrus vs 82,0 % (segment officiel 9971) | MIT | 34 commits, 0 étoile |
| [ruiconte/ink-swarm](https://github.com/ruiconte/ink-swarm) | détection d'encre 2,5D (`ink_9um`), checkpoints Argus V1/V2 | 70 segments natifs (labels `domenicor046/reader-v2-labels`) ; test PHerc0841 w00 | n/r | V2 AUC 0,924 vs Reader V3 0,913 (PHerc0841 natif) | MIT (code et poids) | 4 commits, 0 étoile |
| [adambetka2/HerculeX](https://github.com/adambetka2/HerculeX) | chaîne complète : feuillets → enroulement → aplatissement → encre → visionneuse | 8 rouleaux entiers sans maillage publié | MacBook Pro M1 Pro, 16 Go | 69 290 cm² aplatis ; 1,3–4,7 h CT → feuillet par rouleau | MIT | 6 commits, 2 forks |

## Fiches courtes

### vesuvius-ink-bench (nexusai-kevin)

- **Problème.** Faire tourner le modèle d'encre volumique canonique sur un GPU grand public
  en streaming OME-Zarr, sans artefacts de couture entre tuiles.
- **Méthode.** ResNet3D-152 + décodeur 3D FPN (checkpoint `scrollprize/ink_canonical_2um`,
  `r152_3ddec_v2_l5_epoch13.ckpt`), bf16 ; fusion séparable 3D avec fenêtre de Hann en Z ;
  cache LRU de chunks en RAM. CLI `vesuvius-infer`, `vesuvius-bench`.
- **Chiffres.** 83,2 M voxels/s (79,3 tuiles/s) ; VRAM 2 506 Mio alloués ; PHercParis4 :
  AUC 0,9546, F0.5 / Dice / IoU = 0,7903 / 0,8271 / 0,7052 à th = 0,50 ; meilleur F0.5 0,8724
  à th = 0,70 ; réduction de discontinuité de couture « 99,42 % ».
- **Limites.** Seuil 0,70 choisi sur les données d'évaluation (optimiste) ; le 99,42 % ne
  colle pas avec ses propres valeurs (1 − 0,3466/122,4066 ≈ 99,72 %) et la métrique n'est
  pas définie ; un seul GPU, pas de variance. Le segment 20230702185753 est un segment
  historique très étudié : fuite possible dans l'entraînement du checkpoint, non discutée.
- **Pertinence.** Recette d'inférence basse VRAM réutilisable ; pas de contribution de
  modèle.

### vesuvius-ply-layers (Victoria-TechNexus)

- **Problème.** Séparer des couches de papyrus pressées l'une contre l'autre, là où la
  segmentation saute d'une spire à l'autre.
- **Méthode.** Tenseur de structure → U-Net 3D (feuillet, recto, verso) → ~50 000 pistes de
  crête par tuile, regroupées en feuillets → rayons entre feuillets voisins pour étiqueter
  l'ordre des plis (même couche, couches distinctes, délamination) → numérotation, couture
  des tuiles (recouvrement 40 voxels) → maillage avec 8 auto-contrôles → aplatissement et
  21 tranches pour l'encre (modèle externe).
- **Chiffres** (6 tuiles, vs segment officiel 9971). Sur papyrus 99,6 % vs 82,0 % ; même
  feuillet 99,5 % vs 97,4 % ; franchissements de couche 0,22 vs 0,19 / 100 paires ; score
  d'encre +0,73 vs +0,80 (run antérieur, une couche). Maillage : 6/8 contrôles passés ;
  feuillet aplati 997×615 px (~9,6×5,9 mm). T4 : 13–18 min par tuile, ~9 Go RAM.
- **Limites.** Couverture non égale (91 % officiel vs 87 %) ; métriques conçues par
  l'auteur ; encre moins bonne que l'officiel ; réglé sur Paris 4 seul ; doublons de
  couche résiduels (pire cas 49 %) ; phase 10 dépend de code non fourni.
- **Pertinence.** Seule approche du lot qui exploite explicitement l'orientation des fibres
  recto/verso pour lever l'ambiguïté des couches collées : piste à rapprocher des fibres
  utilisées par le spiral fitting (arxiv-2512.04927).

### ink-swarm / Argus (ruiconte)

- **Problème.** Améliorer Reader V3 (détection d'encre `ink_9um`) sans halluciner de
  texture.
- **Méthode.** `vesuvius_unet_3d_stem_2d` (~34,6 M paramètres, fenêtre 17 couches).
  Argus V1 : soupe de poids de 8 fine-tunings (2 LR × 4 graines) depuis
  `domenicor046/ink9um-dense`, pseudo-labels denses, BCE lissée + Dice. Argus V2 :
  fine-tuning de Reader V3 (12 000 it., tuiles 256 px). Évaluation : TTA ×8, seuil à 80 %
  de rappel propre à chaque modèle ; contrôle « profondeur inversée » (AUC ≈ 0,5 attendue).
- **Chiffres.** PHerc0841 natif : V2 AUC 0,924 vs Reader V3 0,913 ; PHerc1447 w058 : 0,854 vs
  0,856 (Reader V3 devant) ; masques de validation officiels : V1 0,926, Reader V3 0,907,
  V2 0,898 ; profondeur inversée V1 : 0,530.
- **Limites.** Écarts faibles sans intervalles ni variance ; seuils propres à chaque modèle,
  donc précision équilibrée non comparable ; recouvrement possible entre volumes
  d'entraînement (PHerc0139, 0814) et masques de validation, non expliqué.
- **Pertinence.** Le contrôle par profondeur inversée est une idée simple à reprendre contre
  les faux positifs ; la soupe de poids est un gain à bas coût.

### HerculeX (Adam Betka)

- **Problème.** Dérouler des rouleaux entiers sur une seule machine, sans GPU NVIDIA.
- **Méthode.** CT lu à ~19 µm/voxel, cellules de 8 voxels : tenseur de structure et pics
  d'intensité → nœuds de feuillet (kernels Metal) ; graphe de feuillets (normales à 30°,
  rayons vers la spire suivante, coupe min pour orienter) ; numéro d'enroulement par
  optimisation entière L1 (simplexe réseau, 8 solves repondérés, arêtes stables seules) ;
  aplatissement en grilles tifxyz, comblement harmonique ; encre par Reader V3
  (Metal + Neural Engine) ; visionneuse WebGL avec annotation.
- **Chiffres.** 8 rouleaux (PHerc0125, 0175B, 0191, 0358, 0813, 0826, 0846B, 1203) :
  69 290 cm² aplatis, 39 428 cm² en mosaïques ≥ 4 cm² ; 81–86 % des paires voisines à
  ±10 % du pas ; PHerc0343 : 91 % des nœuds des *First Letters* atteints, 89 % du signal
  d'encre conservé vs maillage publié ; 1,3–4,7 h (géométrie) + 1,6–5,0 h (encre) par
  rouleau ; pic 3–8 Go.
- **Limites.** Pas de jeu de test géométrique séparé ; sur les 8 rouleaux, rien ne vérifie
  qu'un morceau est sur la bonne spire (l'auteur le dit) ; mosaïques pouvant joindre deux
  spires ; « isométrique » et « optimalité prouvée » à prendre avec prudence.
- **Pertinence.** Le plus ambitieux du lot ; la formulation de l'enroulement en
  optimisation entière exacte est à comparer à ThaumatoAnakalyptor et au spiral fitting.

## Ce que ça apporte à la base

- **Comparaisons à ne pas faire.** Les AUC d'encre ci-dessus ne sont pas comparables
  entre dépôts (segments, résolution, seuils et labels différents), ni avec
  arxiv-2603.27698 ou arxiv-2308.05070.
- **Gaps confirmés.** Aucune évaluation indépendante commune des modèles d'encre
  communautaires ; aucune métrique de « bonne spire » sur des rouleaux sans vérité
  terrain ; séparation des couches collées encore ouverte.
- **Code cité.** Reader V3 (Domenico Russo), checkpoints Hugging Face
  `scrollprize/ink_canonical_2um`, `domenicor046/*`, `ruiconte/*`, et le dépôt
  [ScrollPrize/villa](https://github.com/ScrollPrize/villa).
