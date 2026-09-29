# Profil — Vision embarquée sur FPGA

Thème et périmètre de la base. La partie machine (axes, règles de classement, requêtes de
découverte) est dans `base.json` ; ce fichier en donne la justification. Le LLM propose des
changements (`/base-profile`, suggestions de `/paper-fiche`) ; rien n'est appliqué sans accord.

## Thème (utilisateur)

Base de connaissance d'articles scientifiques sur la vision embarquée sur FPGA (YOLO,
autoencodeurs, apprentissage continu), destinée à préparer une thèse.

Intitulé temporaire de la thèse : « IA embarquée sécuritaire certifiable sur base de
technologie FPGA ». Cas d'application potentiel : modèle YOLO embarqué sur flux de caméra de
vidéosurveillance, pour la surveillance et l'identification de personnes dans un secteur
industriel dangereux.

## Précisions

- Finalité : préparer une thèse (pré-projet, carte des gaps, labos et encadrants en France).
- Objet : l'inférence et l'apprentissage de réseaux de vision sur FPGA et SoC FPGA, avec comme
  points de comparaison les autres cibles embarquées (Jetson, VPU, Edge TPU, MCU / TinyML).
- Questions de recherche de départ (voir `gaps.md`) : autoencodeurs sur FPGA appliqués à
  l'image (surtout étudiés sur séries temporelles et physique des particules) ; apprentissage
  continu sur la cible ; comparabilité des mesures de puissance (puce vs carte).
- Questions ajoutées avec le thème de thèse (2026-09-29) : assurance et certification d'un
  réseau de vision sur FPGA (déterminisme, traçabilité, normes IEC 61508 / ISO 13849 /
  ISO/IEC TR 5469) ; fiabilité matérielle (SEU, TMR, injection de fautes) ; surveillance à
  l'exécution (OOD, incertitude, prédiction conforme) ; détection et identification de
  personnes en zone industrielle dangereuse. « Sécuritaire » s'entend d'abord *safety*
  (sûreté de fonctionnement) ; la *security* (attaques adverses) est un volet secondaire.

## Inclus

- Accélérateurs YOLO et détection d'objets sur FPGA / SoC (Zynq, Kria, Versal…).
- Autoencodeurs sur FPGA, quel que soit le domaine d'application.
- Apprentissage continu / incrémental embarqué (FPGA, MCU).
- Toolflows (hls4ml, FINN, Vitis AI, fpgaConvNet, SATAY…) et surveys du domaine.
- Baselines embarquées non FPGA (Jetson, VPU, Edge TPU, Hailo, MCU) pour comparer.
- Sûreté, assurance et certification du ML, même sans contexte FPGA (cœur du sujet de thèse).
- Fiabilité des accélérateurs DNN (SEU, radiations, tolérance aux fautes) et vérification
  formelle de réseaux quantifiés ou binarisés.
- Détection, suivi et ré-identification de personnes en milieu industriel (EPI, zones
  dangereuses, collaboration humain-machine).

## Exclus

- Architectures et entraînements génériques sans contexte embarqué (ResNet, AlexNet,
  Batch Norm…), même très cités.
- Résultats uniquement sur GPU de bureau ou serveur.

## Vocabulaire

YOLO (versions, `-tiny`), autoencodeur / VAE / CAE, apprentissage continu, class-incremental,
replay, SLDA, HDC, quantification (INT8, binaire, ternaire), pruning, HLS, dataflow,
streaming, DPU, GOPS, FPS/W, `power_scope`. Sûreté : IEC 61508, ISO 13849, IEC 62061,
ISO/PAS 8800, ISO/IEC TR 5469, DO-178C / DO-254, EASA, SIL / PL, SEU, TMR, injection de
fautes, OOD, moniteur d'exécution, prédiction conforme, EPI (PPE), ré-identification (re-ID).

## Suggestions en attente

<!-- Une ligne par suggestion : - AAAA-MM-JJ (source : paper_id ou /base-profile) — proposition — raison -->

## Historique

- 2026-09-24 — axes de veille repris de `basicStart.txt` ; `in_topic` exige un contexte matériel.
- 2026-09-28 — profil rédigé par Claude à partir de `CLAUDE.md`, `base.json` et `gaps.md`, à relire (`/base-profile`).
- 2026-09-29 — thème de thèse précisé (IA embarquée sécuritaire certifiable sur FPGA ; cas YOLO vidéosurveillance de personnes en secteur industriel dangereux) ; axes `safety-certification` et `person-detection` ajoutés — demande utilisateur.
