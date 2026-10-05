---
id: arxiv-2201.07425-webuav-3m-benchmark-unveiling-power
fiche: todo
date: 2026-09-28
benchmarks: none
---

> **Importée de la base `drone` le 2026-10-05.** Cette fiche a été écrite pour une autre base (autre thème) : pertinence à réévaluer ici, puis `fiche: done` via `/paper-fiche`. Statut d'origine : done.

# WebUAV-3M: A Benchmark for Unveiling the Power of Million-Scale Deep UAV Tracking

Chunhui Zhang, Guanjie Huang, Li Liu, Shan Huang, Yinan Yang, Xiang Wan, Shiming Ge, Dacheng Tao, 2022, arXiv preprint. https://arxiv.org/abs/2201.07425
Type : preprint non relu par les pairs (version lue : arXiv v4, 31 déc. 2022)

## Problème

Selon les auteurs, les benchmarks de suivi mono-objet (SOT) depuis UAV sont trop petits pour
entraîner des trackers profonds (rarement plus de 500 vidéos, Fig. 1), ne portent pas de
descriptions en langage naturel ni audio, couvrent peu de classes (VisDrone : 10) et
n'évaluent que par attributs globaux binaires, ce qui masque les forces et faiblesses des
trackers (§1, points i à iv).

## Méthode

Contribution de type **jeu de données + protocole**, sans modèle nouveau :
- **WebUAV-3M** : 4 500 vidéos, plus de 3,3 M d'images, 223 classes de cibles, 63 classes
  de mouvement, 12 super-classes (§3.2, Table 1). 3 617 vidéos YouTube (sur plus de 28 k
  téléchargées, mots-clés « aerial photography », « drone », « UAV »), plus 616 vidéos de
  Stanford Drone et 267 d'Okutama-Action réannotées (§3.2). Longueur moyenne 710 images
  (23,7 s à 30 FPS) ; taille moyenne de cible ≈ 50 pixels (§3.7, Fig. 8b).
- **SATA** (semi-automatic target annotation) : boucle interactive tracker (SiamRPN++) +
  correction humaine ; 2,99 s par boîte en moyenne contre 15,81 s (Labelme) et 3,86 s
  (CVAT) (§3.3, Table 3, Annexe B).
- **17 attributs**, dont 3 au niveau vidéo (complexité, taille, longueur) (§3.4, Table A).
- **Langage et audio** : une phrase anglaise par vidéo (4 500), convertie en 9 000
  descriptions audio par synthèse vocale (voix féminine et masculine) (§3.5, A.5).
- **Découpage** : 3 520 vidéos d'entraînement, 200 de validation, 780 de test ; taille du
  test choisie par stabilité du classement de 10 trackers (§3.6, A.6, Fig. C). Le texte
  donne aussi « 520 videos as the training set » à l'étape 4 de A.6, incohérent avec les
  3 520 de §3.6 (probable coquille).
- **Protocole UTUSC** : 7 indicateurs continus calculés image par image (faible lumière,
  occlusion longue, petites cibles, vitesse, distorsion via MetaIQA, perturbations
  « dual-dynamic » cible + caméra, exemples adverses) et 7 sous-ensembles de test de
  100 vidéos (§4, Table 4).
- **Métrique cAUC** (complete success plot) : recouvrement pénalisé par la distance des
  centres et la cohérence du rapport d'aspect, sur le modèle de CIoU (§5.3).

## Plateforme et implémentation

Pas d'implémentation embarquée. Évaluation sur serveur : Intel Xeon Gold 6230R, 3 ×
NVIDIA RTX A5000, 64 Go, Ubuntu 18.04 ; Python/PyTorch ou MATLAB (§5.2). Les FPS de la
Table 5 sont mesurés sur ce GPU de bureau ou sur CPU (« @GPU », « @CPU »).
Puissance : n/r. Données, toolkit et résultats publiés :
https://github.com/983632847/WebUAV-3M (résumé, §6).

## Résultats

Évaluation de 43 trackers (paramètres et poids d'origine, sans réglage : « lower bound »,
§5.2) sur le test (Table 5) :

| Tracker | Pre | nPre | AUC | cAUC | mAcc | FPS (plateforme) |
|---|---|---|---|---|---|---|
| AlphaRefine | 0,753 | 0,643 | 0,593 | 0,562 | 0,602 | 42,3 (GPU) |
| KeepTrack | 0,710 | 0,603 | 0,543 | 0,512 | 0,550 | 33,9 (GPU) |
| PrDiMP | 0,674 | 0,575 | 0,514 | 0,484 | 0,521 | 32,4 (GPU) |
| TransT | 0,618 | 0,509 | 0,448 | 0,422 | 0,453 | 53,5 (GPU) |
| HiFT | 0,515 | 0,413 | 0,360 | 0,314 | 0,358 | 122,6 (GPU) |
| LightTrack | 0,602 | 0,494 | 0,458 | 0,415 | 0,459 | 64,9 (GPU) |
| SiamRPN | 0,519 | 0,367 | 0,345 | 0,317 | 0,346 | 142,8 (GPU) |
| KCF | 0,457 | 0,294 | 0,272 | 0,245 | 0,271 | 132,9 (CPU) |

- AlphaRefine devance le 2ᵉ de 4,3 / 4,0 / 5,0 / 5,0 / 5,2 points (§5.4). Des trackers à
  features manuelles (MCCT, AutoTrack) égalent ou battent certains trackers profonds (§5.4).
- UTUSC (Fig. 11-12, courbes seulement) : chute brutale sous une intensité moyenne de 25 ;
  mAcc qui s'effondre sous une taille de cible de 30 pixels ; TransT le moins affecté par
  l'occlusion longue ; PrDiMP 1ᵉʳ en vitesse élevée (§5.6).
- Réentraînement sur WebUAV-3M (Table 6) : gains pour les 5 trackers, par ex. SiamFC cAUC
  0,317 → 0,417, ATOM 0,261 → 0,344.
- Transfert croisé (Table 11, reconstruite par PyMuPDF : à vérifier) : SiamRPN entraîné sur
  WebUAV-3M donne 0,562/0,615 sur VisDrone contre 0,327/0,355 entraîné sur VisDrone.
- Vision-langage (Annexe C.1, Table C non extraite) : le meilleur tracker VL (VLT_TT) reste
  à 11,5 points de Pre derrière AlphaRefine ; le langage n'améliore pas toujours.

→ reportés dans `benchmarks.csv` : aucune ligne. Le papier propose un jeu de données et un
protocole, pas un modèle ni une implémentation propre ; les 43 résultats sont des trackers
tiers, sur GPU de bureau (RTX A5000), sans puissance.

## Limites et critique

- **Aucune donnée embarquée.** FPS sur RTX A5000 ou CPU Xeon, sans puissance ni latence ;
  la gamme de puissance est celle d'un GPU de bureau (hors des gammes nano, FPGA, Jetson).
  Les auteurs ne présentent pas ces FPS comme embarqués, mais les qualifient d'utiles aux
  « real-time applications » (§5.4).
- **Vidéos « UAV » issues de YouTube** : images prises depuis un drone, mais sans
  métadonnées de vol, d'altitude ni de capteur ; la part filmée par des drones grand public
  stabilisés, au montage déjà fait, n'est pas quantifiée (déduit).
- **Test choisi par difficulté** avec 10 trackers (A.6, étape 1) : les vidéos où ces
  trackers échouent sont sur-représentées, ce qui biaise le test en faveur de trackers
  différents de ceux utilisés pour le sélectionner (déduit).
- **Biais d'annotation SATA** : SiamRPN++ génère les boîtes ; les auteurs discutent ce
  biais (Annexe B) mais ne le mesurent pas (pas de comparaison contre une annotation
  entièrement manuelle).
- **Descriptions audio synthétiques** (voix TTS Microsoft), donc sans bruit de rotor ni
  variabilité réelle ; leur intérêt pour le suivi n'est pas démontré dans le papier.
- Incohérences mineures : KCF à 132,0 FPS dans le texte (§5.4), 132,9 dans la Table 5 ;
  520 contre 3 520 vidéos d'entraînement (A.6 contre §3.6).
- Métriques SOT (Pre, AUC, cAUC) non comparables avec le mAP de détection de VisDrone-DET.

## Pertinence pour la thèse

- **Axe suivi et navigation, volet données** : le plus grand jeu SOT vu depuis un drone du
  corpus, avec un sous-ensemble « petites cibles » et une taille moyenne de cible d'environ
  50 pixels, directement en lien avec le thème petits objets.
- Le protocole UTUSC (indicateurs continus par image) est réutilisable pour caractériser la
  **dégradation d'un tracker embarqué** en fonction de la taille de cible ou de la lumière,
  plutôt qu'un seul score global.
- Il laisse ouvert tout le volet embarqué : aucun tracker n'est mesuré sur Jetson, FPGA ou
  MCU. Ce serait un banc naturel pour comparer HiFT, LightTrack ou SiamRPN (les plus rapides
  sur GPU) sur une cible embarquée.
- Pas de contre-drone : les cibles sont au sol ou sur l'eau (personnes, véhicules, navires) ;
  la classe « aircraft » existe mais n'est pas analysée.

## Gaps identifiés

- **Suivi UAV sans métrique embarquée** : les benchmarks SOT depuis drone mesurent les FPS
  sur GPU de bureau ; aucune colonne puissance ni plateforme embarquée (à recouper avec
  TCTrack, arxiv-2203.01885, qui mesure sur Jetson).
- **Petites cibles en suivi** : la chute de mAcc sous 30 pixels (§5.6) est constatée sur
  GPU FP32 ; l'effet de la quantification sur ce régime n'est pas étudié (lien avec
  l'hypothèse mAP_small de la base).
- **Robustesse adverse des trackers** : seuls des exemples adverses numériques sont
  proposés ; rien sur les perturbations matérielles (soft errors) ou physiques.

## Statut de lecture

Papier complet (`fulltext.md` lu en entier, extraction GROBID `ok`, annexes comprises).
Tables 4, 5, 6 et A signalées « sans corps extrait » : la Table 5 a néanmoins été retrouvée
fondue dans le texte de §5.6 (la ligne KCF y est tronquée) ; les Tables 4 et 6 ont un corps
lisible dans la section « Figures et tableaux ». Table 1 (comparaison des benchmarks),
Tables B et C (co-occurrence, trackers vision-langage) absentes. Tables 3 et 11
reconstruites par PyMuPDF. Des passages sont tronqués à l'extraction : fin du scénario
« target distortions » et suivants de §5.6, liste des « Future Directions » (§6) et début
de A.5. Les résultats UTUSC ne sont disponibles qu'en figures (non lues).

Ce qui suit est déduit et non affirmé par les auteurs : le biais de sélection du test ; le
caractère non embarqué des FPS et l'absence de métadonnées de vol ; la probable coquille
520/3 520 ; les gaps « suivi sans métrique embarquée » et « quantification et petites
cibles en suivi ».
