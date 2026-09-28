---
id: arxiv-2203.01885-tctrack-temporal-contexts-aerial-tracking
fiche: done
date: 2026-09-28
---

# TCTrack: Temporal Contexts for Aerial Tracking

Ziang Cao, Ziyuan Huang, Liang Pan, Shiwei Zhang, Ziwei Liu, Changhong Fu, 2022, arXiv preprint. https://arxiv.org/abs/2203.01885
Type : preprint non relu par les pairs (d'après `metadata.json` ; la section « Negative impacts » suggère une soumission en conférence, non confirmée par le texte)

## Problème

Le suivi mono-objet depuis un UAV subit flou de bouger, mouvement de caméra et occlusions,
avec une puissance de calcul embarquée limitée (§1). Les trackers siamois traitent chaque
image indépendamment ; quand ils utilisent l'information temporelle, c'est à un seul
niveau (le template) (§1, §2).

## Méthode

Tracker siamois léger (backbone AlexNet) qui injecte le contexte temporel à deux niveaux
(§3, Fig. 1-2) :
- **Online TAdaConv / TAdaCNN** : les poids des deux dernières couches convolutives sont
  recalibrés à chaque image par des facteurs calculés sur une file de L descripteurs
  globaux (GAP) des images passées, L = 3 (§3.1, §4.1, Table 4).
- **AT-Trans** : transformer encodeur-décodeur (6 têtes) qui met à jour à chaque image un
  « prior » temporel de taille fixe (pas de stockage des images passées, d'où une mémoire
  constante), avec un filtre d'information temporelle (TIF), puis raffine la carte de
  similarité (§3.2, Fig. 4).
- Entraînement sur séquences de 4 images (VID, LaSOT, GOT-10K), 100 époques, 2 × TITAN
  RTX ; template 127², zone de recherche 287² (§4.1).
- Choix du backbone par latence mesurée sur Jetson AGX Xavier : AlexNet 3,4 ms contre
  13,7 ms pour MobileNetV2, ce que les auteurs attribuent au coût d'accès mémoire des
  réseaux mobiles (§4.1, Table 1 ; entrée 287 × 287, CNN seul).

## Plateforme et implémentation

- Tests réels : NVIDIA Jetson AGX Xavier embarqué sur UAV, contrôleur Pixhawk 2 ; RAM
  15,29 %, VRAM GPU 3 %, GPU 46 %, CPU 12,43 % en moyenne ; **sans TensorRT** (§5).
- Comparaisons avec les trackers « profonds » : NVIDIA TITAN RTX (§4.4). Le « PC » des
  125,6 FPS (§1) n'est pas décrit.
- Précision numérique : n/r (FP32 probable faute de TensorRT, non affirmé). Puissance :
  n/r (aucune mesure, ni mode de puissance de la Xavier).
- Code : une note de bas de page (« TCTrack 1 », résumé) renvoie probablement au dépôt,
  mais l'URL est perdue à l'extraction : n/r.

## Résultats

- **UAVTrack112_L** (long terme, > 60 k images) : succès 0,582, précision 0,786, meilleur
  des trackers légers (§4.2, Table 2 ; corps non extrait, valeurs lues dans le texte).
  Suivants : SiamRPN++ 0,559/0,773, HiFT 0,551/0,734, SiamAPN++ 0,537/0,735 (texte de
  §4.2, fragment de la Table 2).
- **UAV123** : +3 points d'AUC sur HiFT et +4,3 sur SiamRPN++ ; **DTB70** : 1ᵉʳ, +5 % d'AUC ;
  UAV123@10fps : 1ᵉʳ en succès et précision (§4.2, Fig. 6, valeurs absolues non extraites).
- **Ablation UAV123** : AT-Trans complet contre transformer simple : +9,8 % d'AUC et +6,7 %
  de précision (relatifs) ; TAdaConv L = 3 : précision 0,776, succès 0,580 contre 0,750 et
  0,550 sans (Tables 3-4).
- **Face aux trackers profonds** (DTB70, TITAN RTX) : performance « compétitive » avec
  TransT en étant 2,49× plus rapide (§4.4, Fig. 8, chiffres non extraits).
- **Vitesse** : 125,6 FPS sur « PC » (§1) ; plus de 27 FPS sur Jetson AGX Xavier en vol,
  sans TensorRT (§5, résumé).

→ reportés dans `benchmarks.csv` : 2 lignes. TCTrack sur UAVTrack112_L (succès 58,2 %,
125,6 FPS sur PC, §1 et §4.2) ; TCTrack sur Jetson AGX Xavier en test réel (27 FPS, §5,
précision n/r).

## Limites et critique

- **Le chiffre embarqué est minimal** : « over 27 FPS » en vol, sans précision mesurée sur un
  benchmark à bord, sans latence par image, sans puissance ni mode énergétique de la
  Xavier. La précision réelle n'est illustrée que qualitativement (CLE sur Fig. 9).
- **Gamme de puissance** : Jetson AGX Xavier (10-30 W selon le mode, non précisé) ; c'est le
  haut de la gamme embarquée drone, hors de portée d'un nano-drone.
- **Écart de 4,6× entre PC et Xavier** (125,6 contre 27 FPS) sans analyse du goulot
  (transformer, pré-traitement, Python) (déduit).
- **Comparaison « même backbone »** pour les siamois (§4.2) : équitable pour l'architecture,
  mais cela dégrade des baselines conçues pour des backbones plus profonds.
- Gains d'ablation donnés en relatif (%) ; la plupart des résultats principaux ne sont
  disponibles qu'en figures.
- Table 1 : paramètres surprenants (EfficientNet à 39,4 K, ShuffleNet à 341,8 K) ;
  probable erreur d'extraction ou d'unité, non vérifiable.
- Limites reconnues par les auteurs : entraînement court (séquences de 4 images), long
  terme et occlusions longues non explorés, versions TensorRT/ONNX à venir (§6).

## Pertinence pour la thèse

- **Axe suivi et navigation** : un des rares trackers aériens avec un test réel **à bord**
  d'un UAV et des taux d'occupation CPU/GPU/mémoire, dans la gamme Jetson.
- Idées d'architecture transposables à l'embarqué contraint : **état temporel de taille
  fixe** (mémoire constante) et recalibrage léger des poids par un descripteur global ; ces
  mécanismes coûtent peu en mémoire, ce qui compte sur FPGA ou MCU (déduit).
- La Table 1 illustre que les réseaux « mobiles » (MobileNetV2, ShuffleNet) peuvent être
  plus lents qu'AlexNet sur GPU embarqué à cause des accès mémoire : argument utile pour
  choisir un backbone sur accélérateur.
- Ne traite ni FPGA, ni quantification, ni puissance.

## Gaps identifiés

- **Trackers aériens temporels sur FPGA ou MCU** : absents ; le transformer AT-Trans et les
  poids dynamiques de TAdaConv sont peu compatibles avec des flots FPGA à poids figés
  (FINN, DPU) (déduit, à vérifier).
- **Mesure énergétique des trackers embarqués** : FPS seul, sans W ni J/image.
- **Précision mesurée à bord** : aucune évaluation quantitative sur un benchmark exécuté sur
  la Xavier (la précision FP32/TensorRT pourrait différer).

## Statut de lecture

Papier complet (`fulltext.md` lu en entier, extraction GROBID `ok`). Tables 1 et 2
signalées « sans corps extrait » : Table 1 retrouvée sous forme de texte (§3.2) ; Table 2
(UAVTrack112_L) seulement par fragments dans §4.2. Fig. 6 et 8 (résultats principaux sur
UAV123, DTB70, UAV123@10fps, et contre trackers profonds) non extraites : valeurs absolues
n/r. Le matériel supplémentaire (critères d'évaluation, pertes) n'est pas dans le texte.
La conclusion (§6) est tronquée.

Ce qui suit est déduit et non affirmé par les auteurs : la précision FP32 sur Xavier ;
l'analyse de l'écart PC/Xavier ; la compatibilité FPGA des mécanismes ; la nature de la
note de bas de page « TCTrack 1 » (lien vers le code).
