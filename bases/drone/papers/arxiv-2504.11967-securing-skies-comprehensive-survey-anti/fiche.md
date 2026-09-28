---
id: arxiv-2504.11967-securing-skies-comprehensive-survey-anti
fiche: done
date: 2026-09-28
---

# Securing the Skies: A Comprehensive Survey on Anti-UAV Methods, Benchmarking, and Future Directions

Yifei Dong, Fengyi Wu, Sanjian Zhang, Guangyu Chen, Yuzhi Hu, Masumi Yano, Jingdong Sun, Siyu Huang, Feng Liu, Qi Dai, Zhi-Qi Cheng, 2025, arXiv preprint. https://arxiv.org/abs/2504.11967
Type : preprint non relu par les pairs (survey). Une version d'atelier (workshop
Anti-UAV, CVPR 2025) existe peut-être : non confirmé par le texte extrait, à vérifier.

## Problème

Donner une vue d'ensemble du contre-drone autour de trois tâches : classification (§3),
détection (§4) et suivi (§5). Le survey couvre toutes les modalités (RGB, IR, audio, radar,
RF, LiDAR) et les paradigmes émergents : diffusion, vision-langage, auto-supervision,
fusion multimodale, apprentissage par renforcement (§1, §6, Fig. 2).

## Méthode

Survey court, format atelier, sans expérience propre :
- jeux de données (§2, Table 1 non extraite) : DUT Anti-UAV, Anti-UAV (RGB-T),
  Anti-UAV410/600 (IR), Drone-vs-Bird, Det-Fly, AOT, MMAUD (radar + LiDAR), Halmstad
  (RGB+IR+audio), UAVSwarm (jusqu'à 23 drones), DroneRF, DroneAudio ;
- tableaux de méthodes par modalité pour la classification (Table 2), la détection
  (Table 3) et le suivi (Table 4), avec la mention explicite que les chiffres ne sont pas
  comparables entre eux (légendes des Tables 3-4) ;
- taxonomie des techniques émergentes (Fig. 2, §6).

## Plateforme et implémentation

Pas d'implémentation. Aucune plateforme matérielle n'est discutée de façon chiffrée :
l'embarqué n'apparaît que comme défi générique (« on-board or edge-based processing »,
§3 ; « specialized hardware optimizations for on-board or edge devices », §5).

## Résultats

Chiffres repris des travaux cités (non vérifiés à la source) :

| Travail cité | Modalité | Jeu | Chiffre repris | Source |
|---|---|---|---|---|
| Huang et al. 2024 [56] (YOLOv8 + ghost + EMA + DCNv2) | RGB | DUT Anti-UAV | 0,971 mAP@0.5 | Table 2 |
| Bo et al. 2024 [16] (YOLOv7-tiny) | RGB | DUT Anti-UAV | 0,932 mAP@0.5 à 104 FPS | Table 2 |
| Cheng et al. 2024 [26] (YOLOv5s + LGFFM) | RGB | DUT Anti-UAV | 0,943 mAP@0.5 ; 4,4 ms/image | Table 2 |
| [49] (YOLOv8, 1,13 M param.) | RGB | MOT-Fly / Det-Fly | 0,949 / 0,964 mAP@0.5 | Table 2 |
| Sun et al. 2024 [122] | IR | jeu Hui | 0,943 mAP@0.5 à 72 FPS | Table 2 |
| Seidaliyeva et al. 2020 [114] | RGB | Drone-vs-Bird | 0,56 F1 (IoU 0,5), 9 FPS | Table 2 |
| Cheng et al. [25] SiamAD | IR | Anti-UAV | 88,4 % de précision à 37,1 FPS | §5 |
| Wu et al. 2024 [148] EECF | RGB | Anti-UAV / USC-Drone | 66,42 / 70,45 % à 86 FPS | Table 4, §5 |
| Xie et al. 2023 [153] STFTrack | IR | Anti-UAV | 91,2 % de précision, 66,6 % de succès, 12,4 FPS | Table 4 |
| Zhao et al. [169] mDrone | radar | propre | ≈ 9 cm de localisation à 10 Hz | Table 2 |

Aucun de ces FPS n'est accompagné de sa plateforme dans le texte extrait.

→ reportés dans `benchmarks.csv` : aucune ligne. C'est un survey : les travaux cités sont à
ficher à la source.

## Limites et critique

- **Pas de distinction sol → air / air → air**, qui est pourtant le critère central de la
  base. La quasi-totalité des méthodes et des capteurs (radar, RF, audio, caméras
  d'Anti-UAV) relève de la surveillance au sol. Det-Fly et MOT-Fly, jeux pris depuis un
  drone, sont mêlés aux autres sans être signalés comme tels (déduit de la connaissance de
  ces jeux, non dit par les auteurs).
- **Aucune dimension matérielle** : ni plateforme, ni puissance, ni latence mesurée sur
  cible embarquée. Les FPS repris n'ont pas de plateforme associée.
- **Reprise de chiffres à vérifier** : pour Seidaliyeva et al. [114], le survey donne
  0,56 de F1, alors que la fiche du papier dans cette base rapporte un F1 global de 0,742
  (2020-seidaliyeva-real-time-accurate-drone-detection, Table 1). Écart non expliqué :
  autre configuration ou erreur de reprise.
- La Table 1 (comparaison des jeux) n'est pas extraite ; les Tables 2 à 4 sont partielles.
- Format court : la section §6 (tendances) reste programmatique, avec des références
  générales (diffusion, CLIP), sans lien quantifié au contre-drone.

## Pertinence pour la thèse

- **Axes `surveys` et `counter-uav`** : bonne carte des jeux de contre-drone et des
  challenges (Anti-UAV Workshops 1 à 4). Utile pour situer un jeu **air → air** (Det-Fly,
  MOT-Fly, AOT) face aux jeux sol → air, à condition de faire le tri soi-même.
- La section §2 signale que les flux haute résolution (Det-Fly, AOT) « challenge onboard
  systems in terms of storage and processing », ce qui appelle compression et accélération
  matérielle : c'est l'ouverture vers la thèse, laissée sans contenu par le survey.
- Pointeurs à ficher à la source : Huang et al. [56] et [49] (YOLOv8 légers sur Det-Fly),
  AOT [10] (Airborne Object Tracking).

## Gaps identifiés

- **Contre-drone air → air embarqué absent des surveys** : aucun survey du corpus
  n'isole à ce stade le cas « détecteur sur drone intercepteur » avec des contraintes
  matérielles chiffrées (à confirmer avec les autres surveys de la base).
- **Essaims** : UAVSwarm plafonne à 23 drones ; au-delà de 50, rien (§2).
- **Furtivité et brouillage** peu représentés dans les jeux ouverts (§2).
- **Temps réel en extérieur encombré** « largely underexplored » (§4).

## Statut de lecture

Papier complet (`fulltext.md` lu en entier, extraction GROBID `ok`). L'extraction est
désordonnée : les Tables 2 et 3 sont éclatées dans le texte des §3-4, la Table 1 n'a pas de
corps, la Table 4 est partielle (plusieurs lignes sans observations), et une partie du §6
est dans le bloc de la Fig. 2. Certaines attributions entre ligne de tableau et méthode
peuvent donc être imprécises.

Ce qui suit est déduit et non affirmé par les auteurs :
- le caractère sol → air de la majorité des méthodes, et air → air de Det-Fly, MOT-Fly
  et AOT ;
- l'écart avec la fiche Seidaliyeva (comparaison entre fiches de la base) ;
- la venue CVPR 2025 Workshops.
