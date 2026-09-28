---
id: arxiv-2108.00202-hift-hierarchical-feature-transformer-aerial
fiche: done
date: 2026-09-28
---

# HiFT: Hierarchical Feature Transformer for Aerial Tracking

Ziang Cao, Changhong Fu, Junjie Ye, Bowen Li, Yiming Li, 2021, arXiv preprint. https://arxiv.org/abs/2108.00202
Type : preprint non relu par les pairs (version arXiv ; la publication à ICCV 2021 n'est pas mentionnée dans le texte extrait, à vérifier)

## Problème

Les trackers Siamese font la classification et la régression sur une carte de similarité
issue de la **dernière couche** (localisation dégradée, petits objets mal traités) ou sur
**plusieurs cartes séparées** (calcul trop lourd pour une plateforme aérienne) (Abstract,
§1). Les backbones légers (AlexNet) manquent de contexte global ; les profonds (ResNet)
sont « loin du temps réel à bord d'un UAV » (§2.1). Les object queries des transformers
de détection ne généralisent pas à une cible arbitraire, et les transformers gèrent mal les
objets basse résolution (§2.2).

## Méthode

- Siamese à backbone **AlexNet** (gabarit 127×127, recherche 287×287) ; cartes de
  corrélation des **trois dernières couches** (M3, M4, M5) (§3.1, §3.2, §4.1).
- **Hierarchical Feature Transformer** : l'encodeur fusionne M3 + M4 (couches haute
  résolution) par attention multi-têtes, avec encodage de position appris et une **couche
  de modulation** (FFN + GAP, pondération apprise) pour les petits objets ; le décodeur
  prend M5 (basse résolution, sémantique) **à la place des object queries**, sans encodage
  de position (§3.2). 1 couche d'encodeur, 2 de décodeur (§4.1).
- Tête anchor-free à deux branches de classification (zone de la boîte ; distance au
  centre, label « circulaire ») + régression IoU loss (§3.3, Éq. 6).
- Entraînement 70 époques sur COCO, ImageNet VID, GOT-10k, Youtube-BB ; PC Intel
  i9-9920X + 2× NVIDIA Titan RTX (§4.1).

## Plateforme et implémentation

- Vitesses de bureau (127 FPS sur UAV20L, ~130 FPS en moyenne) : **GPU de mesure non
  précisé** ; seul le PC d'entraînement (2× Titan RTX) est décrit (§4.1, §4.3.4, Table 6).
- **Embarqué** : NVIDIA **Jetson AGX Xavier** sur un UAV « typique », **31,2 FPS en
  moyenne sans TensorRT** (§5). Mode de puissance du Xavier, précision numérique (FP32 ?),
  consommation : n/r.
- Code publié : https://github.com/vision4robotics/HiFT (Abstract).

## Résultats

| Jeu | Précision @20 px | Succès (AUC) | Source |
|---|---|---|---|
| UAV123 | 0,787 | 0,589 | Table 1 |
| UAV20L | 0,763 | 0,566 | Table 2 |
| DTB70 | 0,802 | 0,594 | §4.3.1, Fig. 4a |
| UAV123@10fps | 0,754 | 0,574 | §4.3.1, Fig. 4b |
| Moyenne 4 jeux | 0,776 | 0,581 | Table 3 |

- Face à SiamRPN++ (AlexNet) : +3,5 % en précision et +3,2 % en succès en moyenne
  (Table 3, Remarque 5). Par attribut, gains de 3,6 % à 10,4 % (fast motion : +10,42 % en
  précision) (Table 4).
- Face aux backbones profonds : sur UAV20L, HiFT 0,763 à 127 FPS contre SiamRPN++
  ResNet-50 0,749, 1,8× plus lent (§4.3.4, Fig. 6) ; Table 6 : HiFT précision moyenne
  0,783 à 129,87 FPS contre SiamRPN++ ResNet-50 0,774 à 71,59 FPS, DiMP / PrDiMP / ATOM
  à 25,94-34,94 FPS (attribution colonne ↔ tracker à confirmer, voir Statut de lecture).
- Ablation (UAV20L, Table 5) : object queries classiques −2,29 % en précision ; carte de
  caractéristiques à la place des queries +10,47 % ; HFT complet +24,88 % ; encodage de
  position sur M5 ou label rectangulaire font chuter le gain à +12,77 % et +2,95 %.
- Tests réels à bord (jour et nuit, occlusion, petit objet) : 31,2 FPS sur AGX Xavier
  (§5, Fig. 7), sans métrique de précision chiffrée.

→ reportés dans `benchmarks.csv` : 5 lignes : précision @20 px sur UAV123 (78,7, Table 1),
UAV20L (76,3 à 127 FPS, plateforme n/r), DTB70 (80,2), UAV123@10fps (75,4) ; et AGX Xavier
à 31,2 FPS (§5, précision n/r).

## Limites et critique

- **127-130 FPS sur GPU de bureau non précisé** : c'est ce chiffre qui porte le message
  « efficace ». À bord, le débit tombe à **31,2 FPS** (×4 plus lent) sur AGX Xavier, de
  la gamme Jetson ~10-30 W (déduit, puissance n/r), sans TensorRT. Aucune mesure de
  puissance ni d'énergie par image.
- **Comparaison « même backbone »** : tous les Siamese sont ramenés à AlexNet (§4.3.1),
  ce qui avantage HiFT face à des méthodes conçues pour des backbones profonds ; la
  comparaison §4.3.5 aux backbones profonds est plus honnête mais la vitesse est mesurée
  sur un GPU non dit.
- **Baselines** majoritairement anciennes (DCF à la main : KCF, fDSST, BACF…) ; pas de
  comparaison aux trackers transformer contemporains (TransT, Stark).
- **Tests réels qualitatifs** : pas de métrique de suivi rapportée à bord, séquences non
  publiées.
- Le « transformer » est léger (1 encodeur, 2 décodeurs) ; son coût (FLOPs, paramètres)
  n'est pas donné.

## Pertinence pour la thèse

- **Axe `tracking-navigation`** : jalon du groupe vision4robotics (Tongji, C. Fu) sur le
  suivi aérien mono-objet « à bord » ; point de comparaison pour TCTrack
  (arxiv-2203.01885) et SiamAPN (arxiv-2106.08816), présents dans la base.
- Donne un **ordre de grandeur Jetson** : un tracker Siamese AlexNet + petit transformer
  tient ~31 FPS sur AGX Xavier sans optimisation. Aucun portage FPGA ni MCU : la question
  du transformer de suivi sur FPGA (hypothèse « Transformer rarement porté sur FPGA » de
  gaps.md) reste entière.
- La **couche de modulation multi-échelle pour petits objets** est une idée proche de la
  tête P2 des YOLO drone, ici côté suivi.

## Gaps identifiés

- **Puissance non mesurée** pour un tracker « temps réel à bord » : aucune donnée W ni
  J/image, ni mode de puissance du Xavier.
- **Transformer de suivi aérien sur FPGA / MCU** : non traité ; l'attention à 1-2 couches
  sur cartes de corrélation de petite taille paraît un candidat raisonnable (déduit).
- **Effet de la quantification (INT8, TensorRT)** sur la précision de suivi des petits
  objets : non mesuré (pas de TensorRT ici).

## Statut de lecture

Papier complet (`fulltext.md` lu en entier, extraction GROBID `ok`). Les corps des Tables
2, 5 et 6 sont signalés « sans corps extrait » mais des fragments sont présents : la Table
2 est partielle (noms des trackers perdus, seuls les chiffres de HiFT et des deux suivants
sont confirmés par le texte) ; la Table 6 est éclatée en fragments (FPS et précisions
moyennes dans un bloc séparé, l'ordre des colonnes n'est pas garanti). Début de §4.3.3
(définition des symboles) et une partie de §4.3.4-4.3.5 mélangés. Le matériel
supplémentaire (autres ablations, détails de classification) n'est pas dans la base.

Ce qui suit est déduit et non affirmé par les auteurs :
- la gamme de puissance Jetson du test embarqué ;
- le rapport ×4 entre vitesse bureau et vitesse Xavier ;
- l'avantage donné à HiFT par l'alignement des baselines sur AlexNet ;
- l'intérêt d'un portage FPGA de l'attention légère.
