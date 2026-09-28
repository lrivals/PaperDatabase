# Profil — Vision embarquée sur FPGA

Thème et périmètre de la base. La partie machine (axes, règles de classement, requêtes de
découverte) est dans `base.json` ; ce fichier en donne la justification. Le LLM propose des
changements (`/base-profile`, suggestions de `/paper-fiche`) ; rien n'est appliqué sans accord.

## Thème (utilisateur)

Base de connaissance d'articles scientifiques sur la vision embarquée sur FPGA (YOLO,
autoencodeurs, apprentissage continu), destinée à préparer une thèse.

## Précisions

- Finalité : préparer une thèse (pré-projet, carte des gaps, labos et encadrants en France).
- Objet : l'inférence et l'apprentissage de réseaux de vision sur FPGA et SoC FPGA, avec comme
  points de comparaison les autres cibles embarquées (Jetson, VPU, Edge TPU, MCU / TinyML).
- Questions de recherche de départ (voir `gaps.md`) : autoencodeurs sur FPGA appliqués à
  l'image (surtout étudiés sur séries temporelles et physique des particules) ; apprentissage
  continu sur la cible ; comparabilité des mesures de puissance (puce vs carte).

## Inclus

- Accélérateurs YOLO et détection d'objets sur FPGA / SoC (Zynq, Kria, Versal…).
- Autoencodeurs sur FPGA, quel que soit le domaine d'application.
- Apprentissage continu / incrémental embarqué (FPGA, MCU).
- Toolflows (hls4ml, FINN, Vitis AI, fpgaConvNet, SATAY…) et surveys du domaine.
- Baselines embarquées non FPGA (Jetson, VPU, Edge TPU, Hailo, MCU) pour comparer.

## Exclus

- Architectures et entraînements génériques sans contexte embarqué (ResNet, AlexNet,
  Batch Norm…), même très cités.
- Résultats uniquement sur GPU de bureau ou serveur.

## Vocabulaire

YOLO (versions, `-tiny`), autoencodeur / VAE / CAE, apprentissage continu, class-incremental,
replay, SLDA, HDC, quantification (INT8, binaire, ternaire), pruning, HLS, dataflow,
streaming, DPU, GOPS, FPS/W, `power_scope`.

## Suggestions en attente

<!-- Une ligne par suggestion : - AAAA-MM-JJ (source : paper_id ou /base-profile) — proposition — raison -->

## Historique

- 2026-09-24 — axes de veille repris de `basicStart.txt` ; `in_topic` exige un contexte matériel.
- 2026-09-28 — profil rédigé par Claude à partir de `CLAUDE.md`, `base.json` et `gaps.md`, à relire (`/base-profile`).
