---
id: arxiv-2507.10006-vision-anti-unmanned-aerial-technology
fiche: done
date: 2026-09-28
---

# Vision-Based Anti Unmanned Aerial Technology: Opportunities and Challenges

Guanghai Ding, Yihua Ren, Yuting Liu, Qijun Zhao, Shuiwang Li, 2025, arXiv preprint. https://arxiv.org/abs/2507.10006
Type : preprint non relu par les pairs (survey)

## Problème

Les auteurs veulent faire le point sur la détection et le suivi de drones (« Anti-UAV ») par
vision, seule ou fusionnée avec d'autres capteurs (§I). Ils décrivent les difficultés
propres à la cible : drones petits, à basse altitude, peu texturés, confondus avec les
oiseaux ; mouvements rapides qui changent l'échelle et la forme ; fonds extérieurs
bruités, en particulier en infrarouge thermique (§II-A, Fig. 2). Radar, RF et acoustique
sont présentés en introduction avec leurs limites (§I), mais le survey se concentre sur la
vision.

## Méthode

Survey, sans expérience propre. Il comprend :
- un inventaire de **19 jeux de données** publics, RGB et IR, décrits un par un (§III) et
  résumés dans la Table I (scène, taille, modalité, complexité, type de drone) ; la
  Table II (liens d'accès) est presque vide dans l'extraction ;
- une taxonomie des méthodes (§IV, Fig. 4) : **détection** (surtout des variantes YOLO
  v8 à v11, un RT-DETR) et **suivi** en trois familles : Siamese, self-attention et fusion
  vision + autre modalité (RF, radar, RGB-TIR) ;
- une revue des métriques (§IV-C) : SA (State Accuracy) de Anti-UAV410, *acc* du challenge
  Anti-UAV avec pénalité de faux négatifs, MOTA, P/R/F1, FPS, AP/mAP, TCR ;
- les limites des jeux de données et des méthodes, et sept pistes (§V).

## Plateforme et implémentation

Pas d'implémentation propre. **Aucune plateforme embarquée n'est discutée** : pas de
Jetson, de FPGA ni de MCU dans le texte. Les FPS cités ne donnent pas le matériel, sauf
TransIST [126], « 30 FPS on a GPU platform » (§IV-B2). La Table III, censée donner
l'« Experimental Environment » de chaque méthode, est vide dans l'extraction.

## Résultats

Chiffres repris des travaux cités (§IV), non vérifiés à la source :

| Travail | Tâche | Jeu | Résultat cité |
|---|---|---|---|
| DotD-YOLOv9-C, Gao et al. [56] | détection | Anti2 (4 classes) | 92,6 % mAP |
| Awan et al. [98], YOLOv6-L6 | détection | images 4K | 92,7 % mAP |
| Liu et al. [100], YOLOv8 modifié (tête 160×160) | détection | City-UAV | AP 93,4 % (+2,6 pts vs YOLOv8) |
| Gao et al. [92], YOLOv11 + HWD + CCFM | détection | DUT Anti-UAV | +4,1 pts mAP50, −38,4 % de paramètres, vitesse « slight decline » |
| ISTD-DETR, Yuan et al. [96] | détection IR | Anti-UAV / SIRST | 96,2 % / 96,4 % mAP50, 133 FPS (matériel n/r) |
| RTM-UAVDet, Wang et al. [134] | détection RGB-TIR | n/r | AP 66,1 %, 72,4 FPS (matériel n/r) |
| StrongSiamTracker, Cui et al. [113] | suivi IR | Anti-UAV410 | acc 0,6673 |
| DLST, Zhang et al. [114] | suivi IR | Anti-UAV410 | SA 68,81 % |
| PPTracker, Qin et al. [115] | suivi multi-drones | 4th Anti-UAV (MOT) | MOTA 67,9 % |
| SiamUF, Qian et al. [111] | suivi IR | jeux publics | 83,1 % (CLE ≤ 10 px), 30 FPS |
| UTTracker, Yu et al. [127] | suivi IR | Anti-UAV Challenge | AUC 77,9 % |

La Table III, qui devait regrouper jeux, résultats et environnements, n'a **pas de corps
extrait** : seul l'en-tête et une cellule (DotD-YOLOv9-C) subsistent.

→ reportés dans `benchmarks.csv` : aucune ligne. C'est un survey : les chiffres viennent
des travaux cités, à ficher à la source.

## Limites et critique

- **Aucune dimension embarquée.** Les FPS (133, 72,4, 30) sont donnés sans plateforme ni
  puissance. La piste « real-time vs accuracy » (§V-C) se limite à citer quantification,
  pruning et distillation, sans aucun chiffre sur carte.
- **Pas de distinction sol → air / air → air.** Le point de vue du capteur n'est jamais
  discuté : TIB-Net est explicitement une caméra fixe au sol (§III), alors que Det-Fly
  (« air-to-air », capté depuis un DJI M210), ARD-MAV (capté depuis un Mavic 2 Pro / M300)
  et MMFW-UAV (capté depuis un M30T) sont aéroportés. Ces jeux sont pourtant mélangés
  dans la Table I (déduit de §III).
- **Métriques hétérogènes :** mAP sur Anti2 (4 classes), AP sur City-UAV, SA et acc sur
  Anti-UAV410, MOTA. Les chiffres du tableau ci-dessus ne sont pas comparables entre eux,
  et le survey ne les harmonise pas.
- **Revue surtout descriptive.** Les méthodes sont résumées une par une, sans analyse
  critique ni tableau comparatif exploitable ; la section « Discussion » (§IV-D) reste
  qualitative.
- Incohérences de rédaction : 19 jeux dans la Table I, mais DUT Anti-UAV y a
  « Image 1,000 » alors que le texte dit 10 000 images (§III) ; ARD-MAV y est noté
  « Multimodal : Yes », sans justification dans le texte.

## Pertinence pour la thèse

- **Utile comme annuaire de jeux de données contre-drone**, notamment les trois jeux
  aéroportés, pertinents pour l'**air → air** : Det-Fly [69], ARD-MAV [62] (cible
  moyenne à 0,02 % de l'image, jusqu'à 6×3 px) et MMFW-UAV [57]. Anti-UAV410 [17] est déjà
  dans la base (`2024-huang-anti-uav410-thermal-infrared-benchmark`), comme Anti-UAV [48]
  (`arxiv-2101.08466-anti-uav-large-multi-modal`).
- **Peu utile pour l'axe matériel** : il ne dit rien du déploiement embarqué. Il complète
  `arxiv-2504.11967-securing-skies-comprehensive-survey-anti`, autre survey contre-drone
  de la base.
- La métrique *SA/acc* (présence + IoU) est à connaître si la thèse évalue un suivi
  air → air avec disparition de cible.

## Gaps identifiés

- **Contre-drone embarqué :** aucun des travaux cités ne rapporte de plateforme embarquée
  ni de puissance. Le gap « détecteur air → air sur FPGA/SoC avec mesure de puissance »
  reste entier (déduit de l'absence dans ce survey).
- **Pas de benchmark de latence** dans les jeux contre-drone : les auteurs le signalent
  eux-mêmes (« Lack of Real-Time Benchmarking », §V-A).
- **Multi-drones :** peu de jeux (Anti-MUAV15, track 3 du 4th Anti-UAV) (§V-A).

## Statut de lecture

Papier complet (`fulltext.md` lu en entier, extraction GROBID `ok`). La Table II (liens)
et la **Table III** (résultats et environnements expérimentaux) n'ont pas de corps extrait
(`extraction.warnings`) : leurs chiffres n'ont pas été lus. La liste des contributions
(§I) est tronquée dans l'extraction.

Ce qui suit est déduit et non affirmé par les auteurs :
- le classement des jeux de données en sol → air et air → air ;
- l'absence de plateforme embarquée comme gap ;
- les incohérences relevées entre la Table I et le texte.
