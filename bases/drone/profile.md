# Profil — Vision embarquée sur drone

Thème et périmètre de la base. La partie machine (axes, règles de classement, requêtes de
découverte) est dans `base.json` ; ce fichier en donne la justification. Le LLM propose des
changements (`/base-profile`, suggestions de `/paper-fiche`) ; rien n'est appliqué sans accord.

## Thème (utilisateur)

Base de connaissance d'articles scientifiques sur la vision embarquée sur drone : détection
(YOLO, petits objets), accélérateurs embarqués (FPGA, MCU/nano-drone, ASIC, neuromorphique),
co-design calcul ↔ énergie ↔ vol et fiabilité. Destinée à préparer une thèse.

## Précisions

- Finalité : préparer une thèse, en complément de la base « vision embarquée sur FPGA »
  (`fpga`), dont des papiers peuvent être importés (`bin/pdb base import fpga:<id>`).
- Hypothèses de départ, à étayer (`gaps.md`) : les YOLO drone SOTA (tête P2, Transformer) ne
  sont presque jamais portés sur FPGA ; l'effet de la quantification sur le mAP_small n'est
  pas mesuré ; aucune métrique système (autonomie, vitesse de vol sûre) dans les papiers
  YOLO/FPGA.
- Toujours situer un résultat dans sa gamme de puissance : nano (GAP8, mW), FPGA (W),
  Jetson (~10 W).

## Inclus

- Détection sur images aériennes et de drone, petits objets (VisDrone, UAVDT, DAC-SDC).
- Détection sur FPGA / SoC embarqué à bord.
- Contre-drone **air → air** (détecteur embarqué sur un drone intercepteur).
- Nano-drones, MCU, ASIC, neuromorphique.
- Co-design calcul ↔ énergie ↔ vol ; fiabilité du calcul embarqué ; suivi et navigation.

## Exclus

- Contre-drone **sol → air** (capteur fixe au sol) : ne relève pas de l'IA embarquée.
- Résultats sur GPU de bureau présentés comme « embarqués ».

## Vocabulaire

UAV, MAV, nano-drone, VisDrone, UAVDT, DAC-SDC, mAP_small, IoU mono-objet vs mAP
multi-classe, tête P2, GAP8/GAP9, Crazyflie, roofline, autonomie, soft errors.

## Suggestions en attente

<!-- Une ligne par suggestion : - AAAA-MM-JJ (source : paper_id ou /base-profile) — proposition — raison -->

## Historique

- 2026-09-28 — base créée à la main (liens vers `../PaperDatabase`), 9 axes dans `base.json`.
- 2026-09-28 — déplacée dans le dépôt PaperDatabase (`bases/drone/`), versionnée avec lui.
- 2026-09-28 — profil rédigé par Claude à partir de `CLAUDE.md` et `base.json`, à relire (`/base-profile`).
