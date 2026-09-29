# Profil — Apprentissage continu embarqué pour la maintenance prédictive

Thème et périmètre de la base. La partie machine (axes, règles de classement, requêtes de
découverte) est dans `base.json` ; ce fichier en donne la justification. Le LLM propose des
changements (`/base-profile`, suggestions de `/paper-fiche`) ; rien n'est appliqué sans accord.

## Thème (utilisateur)

Apprentissage continu embarqué sur microcontrôleur pour la maintenance prédictive : méthodes de CL, TinyML et entraînement sur l'appareil, quantification, RUL, détection d'anomalies et de dérive, jeux de données

## Précisions

- Finalité : base des références du stage ISAE (dépôt `cl-embedded` : manuscrit, soutenance,
  article « EWC INT8 sur MCU »). Elle sert à retrouver et vérifier ce que disent les sources
  citées, pas à élargir la bibliographie sans accord.
- Contenu initial : les articles des quatre `.bib` du stage, les références de `docs/context/`
  absentes des `.bib`, et des articles lus pendant le stage mais non cités.
- Fil conducteur : apprentissage continu (régularisation type EWC/SI/MAS, rejeu) sous les
  contraintes d'un microcontrôleur (mémoire, INT8, énergie), appliqué au pronostic (RUL) et à
  la détection de défauts sur séries temporelles de capteurs, avec détection de dérive pour
  déclencher la mise à jour.
- Toujours situer un résultat embarqué dans sa gamme : MCU Cortex-M / PULP (mW, ko de RAM),
  smartphone, GPU.
- Les articles fondateurs de statistique (Mahalanobis, Page, Massey, Hinkley) et les papiers de
  jeux de données sont des références de méthode ou de données : leur fiche décrit ce qu'ils
  définissent, sans ligne de benchmark.

## Inclus

- Méthodes d'apprentissage continu (régularisation, rejeu, architecture) et surveys.
- TinyML, entraînement et apprentissage continu sur l'appareil (MCU, plateformes basse conso).
- Quantification (INT8, binaire, ternaire) utile à l'inférence ou à l'entraînement embarqué.
- Maintenance prédictive, RUL, détection de défauts ; détection d'anomalies et de dérive.
- Jeux de données de pronostic (PRONOSTIA, C-MAPSS, Paderborn, CWRU) et leurs articles.

## Exclus

- Sources web, livres blancs commerciaux et pages de jeux de données sans article
  (CWRU Data Center, Blue Docker, ebooks « edge AI ») : cités dans le manuscrit, hors base.

## Vocabulaire

## Suggestions en attente

<!-- Une ligne par suggestion : - AAAA-MM-JJ (source : paper_id ou /base-profile) — proposition — raison -->

## Historique

- 2026-09-29 — base créée (`pdb base new`) ; axes et règles écrits d'après les sections de la
  bibliographie du stage.
