---
id: arxiv-2106.08816-siamapn-siamese-attentional-aggregation-network
fiche: done
date: 2026-09-28
---

# SiamAPN++: Siamese Attentional Aggregation Network for Real-Time UAV Tracking

Ziang Cao, Changhong Fu, Junjie Ye, Bowen Li, Yiming Li, 2021, arXiv preprint. https://arxiv.org/abs/2106.08816
Type : preprint non relu par les pairs selon `metadata.json`. Une version en conférence
(IROS 2021) est probable, mais elle n'est pas vérifiée dans la base.

## Problème

Suivi mono-objet (single object tracking) **depuis un UAV** : suivre en temps réel,
**à bord**, une cible désignée à la première image. Les trackers à corrélation (CF) sont
rapides mais peu robustes. Les trackers profonds sont précis mais trop coûteux pour une
plateforme embarquée. Les défis propres à l'UAV sont les mouvements rapides, la faible
résolution, les occlusions et les changements d'échelle (§I). Le baseline SiamAPN, à
ancres adaptatives, est sensible aux variations sémantiques et aux changements d'échelle
(§III-A).

## Méthode

- Tracker siamois sur un **backbone AlexNet**, choisi pour le déploiement (§III-B1).
  Gabarit de 127×127, zone de recherche de 287×287 (§IV-A).
- **APN-DF**, un réseau de propositions d'ancres à double feature : il fusionne les cartes
  de similarité des couches 4 et 5 (corrélation en profondeur, GAP + FFN, concaténation)
  pour produire des ancres adaptatives robustes à l'échelle (§III-B2, Éq. 1-3).
- **AAN**, un réseau d'agrégation attentionnelle :
  - *self-AAN* : attention spatiale de type DANet, puis attention par canal (GAP + GMP,
    FFN partagé) ;
  - *cross-AAN* : agrège la carte des ancres R_A avec la carte attentionnelle R_c
    (§III-B3, Éq. 4-7).
- Tête à 3 branches de classification (IoU des ancres, points dans la vérité terrain,
  centrage), régression avec une perte IoU redessinée (Éq. 8). Convergence en 25 epochs
  contre 37 pour le baseline (§III-B4).
- Entraînement sur COCO, ImageNet VID, GOT-10K et YouTube-BB, SGD, batch de 220 paires,
  sur 2× TITAN RTX (§IV-A).

## Plateforme et implémentation

- **Tests réels à bord d'une NVIDIA Jetson AGX Xavier** : **34,9 FPS** en moyenne (§V),
  soit « around 35 FPS without TensorRT acceleration » (légende d'une figure non
  identifiée). Mode de puissance, précision numérique et puissance consommée : `n/r`. Gamme
  **Jetson** (puissance non rapportée).
- Vitesse sur le PC d'évaluation des benchmarks : `n/r`.
- Code : https://github.com/vision4robotics/SiamAPN (§IV-A). Vidéos :
  https://youtu.be/okS289p3pCQ (Fig. 6).

## Résultats

Protocole OPE : précision à 20 px de CLE et AUC du success plot (§IV-B).

| Benchmark | Précision | AUC | Second (précision / AUC) | Source |
|---|---|---|---|---|
| UAV20L (20 séquences longues, 2934 images en moyenne) | 0,736 | 0,560 | SiamAPN 0,721 / 0,539 | Fig. 4a |
| UAV123@10fps (123 séquences) | 0,764 | 0,580 | SiamAPN 0,752 ; SiamFC++ 0,576 d'AUC | Fig. 4b |

- Selon le texte, les gains sur UAV20L face au second sont de +2,0 % en précision et de
  +4,0 % en AUC (§IV-C1). Ces valeurs sont cohérentes avec 0,736/0,721 et 0,560/0,539 en
  gain relatif (déduit).
- Par attribut, le gain en AUC est de +5,0 % en mouvement de caméra et atteint +16,2 % en
  occlusion totale face au second (texte fusionné dans la légende de la Fig. 7 ; la
  Table I n'a pas de structure de colonnes lisible).
- Ablation de la précision sur UAV20L (Table II) : 0,721 pour le baseline, 0,727 avec
  APN-DF, 0,730 avec la self-AAN et **0,736 avec l'AAN complète**. Pour les occlusions,
  la précision passe de 0,617 à 0,651.
- Hyperparamètre w1 = 1,2 optimal (Fig. 5).
- Tests réels (bâtiment, voiture, canard, objet occulté) : qualitatifs, en CLE (Fig. 1 et
  7), à 34,9 FPS (§V).

Tous les trackers siamois comparés utilisent le même backbone AlexNet (Remark 4, §IV).

→ reportés dans `benchmarks.csv` : 3 lignes.
- UAV20L, AUC 56,0 (Fig. 4a, `medium`) ;
- UAV123@10fps, AUC 58,0 (Fig. 4b, `medium`) ;
- tests réels sur Jetson AGX Xavier à 34,9 FPS, précision `n/r` (§V, `medium`).

Les valeurs des figures sont lues dans les légendes extraites, d'où la confiance `medium`.

## Limites et critique

- **FPS sans puissance** : 34,9 FPS sur AGX Xavier sans mode de puissance ni mesure en W.
  Aucune vitesse n'est donnée pour les autres trackers sur la même plateforme, alors que le
  temps réel est l'argument principal.
- **Baselines alignés sur AlexNet** (Remark 4) : c'est équitable pour comparer les
  structures, mais SiamRPN++ et SiamFC++ sont ainsi privés de leur backbone d'origine,
  plus fort. Le classement « SOTA » est donc relatif à ce choix.
- Gains modestes : +0,015 de précision et +0,021 d'AUC sur UAV20L face au baseline SiamAPN
  (Fig. 4a). Aucune variance n'est rapportée.
- UAV123@10fps simule une cadence basse. Il n'y a pas d'évaluation sur DTB70 ni VisDrone-SOT.
- Tests réels **uniquement qualitatifs** : pas de métrique quantitative sur des séquences
  annotées embarquées.
- Suivi mono-objet initialisé à la main : ce n'est pas de la détection, et ce n'est pas
  comparable aux mAP.

## Pertinence pour la thèse

- **Axe suivi et navigation** : c'est une référence du groupe Vision4Robotics (Tongji) pour
  le suivi temps réel sur Jetson. Elle illustre la gamme **Jetson** (~10 W) avec un
  backbone léger et sans TensorRT.
- Une piste possible pour un FPGA : la corrélation en profondeur et l'attention d'un
  tracker siamois AlexNet sont des blocs réguliers, a priori portables (déduit). Aucun
  travail FPGA sur ces trackers n'est cité ici.
- **Laisse ouvert** : l'énergie par image, la quantification INT8 et son effet sur la
  précision, et l'intégration à une boucle de contrôle de vol.

## Gaps identifiés

- **Trackers siamois UAV sans mesure de puissance** : FPS sur Jetson sans W ni mode de
  puissance.
- **Pas de portage FPGA ou MCU des trackers siamois UAV** dans ce papier. À vérifier dans
  la base : existe-t-il SiamAPN sur FPGA ?
- **Évaluation embarquée quantitative absente** : les tests réels restent qualitatifs.

## Statut de lecture

Papier complet (`fulltext.md` lu en entier, extraction GROBID `ok`). La section IV n'est
pas détectée comme titre. Le corps de la Table I (attributs) est extrait en une ligne sans
en-têtes de colonnes : ses valeurs ne sont pas exploitables, sauf la ligne SiamAPN++, dont
les colonnes restent ambiguës. Les valeurs de la Fig. 4 sont lues dans les légendes des
courbes, extraites comme texte.

Ce qui suit est déduit et non affirmé par les auteurs :
- la cohérence des gains relatifs ;
- la portabilité sur FPGA ;
- la publication probable à IROS 2021, non vérifiée.
