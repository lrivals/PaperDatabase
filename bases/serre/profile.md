# Profil — serre

Thème et périmètre de la base. La partie machine (axes, règles de classement, requêtes de
découverte) est dans `base.json` ; ce fichier en donne la justification. Le LLM propose des
changements (`/base-profile`, suggestions de `/paper-fiche`) ; rien n'est appliqué sans accord.

## Thème (utilisateur)

Serre autonome pilotée par IA : vision des maladies des plantes et écart de domaine, calibration et décision, inférence edge (RPi/Hailo), IoT de serre, contrôle climatique et hydroponique, prévision, agent LLM avec validation humaine

## Précisions

- Finalité : appuyer le projet SerreIA, une serre autonome avec des capteurs et actionneurs
  sur ESP32, un bus MQTT, un Raspberry Pi 5 avec Hailo pour l'inférence, un classifieur de
  maladies multi-têtes (EfficientNet-B0, PlantVillage + CCMT, test hors domaine sur PlantDoc),
  un contrôleur à règles avec prévision GRU et un agent LLM dont les actions sont validées par
  un humain.
- Questions de recherche :
  - pourquoi les modèles entraînés sur PlantVillage s'effondrent-ils sur des images de terrain
    (PlantDoc) ? Quelles parades (remplacement de fond, augmentation, adaptation de domaine,
    pré-entraînement) donnent un gain mesuré ?
  - comment calibrer un classifieur (temperature scaling, ECE) et choisir les seuils pour
    réduire les fausses alertes « anormal » à rappel donné ?
  - comment agréger les prédictions de plusieurs feuilles en une décision par capture (max,
    k feuilles, top-k, moyenne pondérée, multiple instance learning) et rejeter les crops
    inexploitables ou hors distribution ?
  - un pipeline en deux étages (détecteur de feuilles puis classifieur) bat-il un
    classifieur sur l'image entière ? Que coûte-t-il sur l'edge ?
  - la détection d'anomalies non supervisée (PatchCore) fonctionne-t-elle sur des feuilles ?
  - quelles latences et quelle précision après quantification sur Raspberry Pi et NPU Hailo ?
  - quelles architectures IoT et quelles lois de commande (règles, MPC, RL) pour le climat et
    la solution nutritive (pH/EC) en serre ? Quelle précision de prévision pour une GRU ?
  - comment encadrer un agent LLM qui propose des actions sur un système physique (garde-fous,
    preuves, validation humaine) ?
- Toujours noter le dataset d'entraînement et celui de test, et préciser si le test est
  in-domain ou hors domaine. Noter aussi le matériel et la latence mesurée.

## Inclus

- Classification et détection des maladies, nuisibles et carences des plantes.
- Généralisation au terrain, biais de fond, adaptation et généralisation de domaine.
- Calibration, incertitude, OOD et rejet, choix des seuils, agrégation multi-instances.
- Détection et segmentation des feuilles, pipelines en deux étages.
- Détection d'anomalies visuelles non supervisée, appliquée ou transférable aux plantes.
- Phénotypage et suivi de croissance par image, en serre ou en intérieur.
- Annotation semi-automatique et apprentissage actif sur des données agricoles.
- Inférence embarquée : Raspberry Pi, NPU (Hailo, Coral), Jetson, quantification.
- IoT de serre : capteurs, MQTT, ESP32, réseaux de capteurs, jumeau numérique.
- Contrôle climatique et hydroponique : règles, MPC, RL, irrigation, pH/EC, éclairage, énergie.
- Prévision du microclimat de serre (GRU, LSTM, modèles physiques).
- Agents LLM et systèmes d'aide à la décision en agriculture, humain dans la boucle.

## Exclus

- Agriculture de plein champ par satellite ou drone (base `drone`).
- Accélération matérielle sur FPGA (base `fpga`).
- Génomique, sélection variétale et agronomie sans composante logicielle.
- Architectures de vision génériques sans évaluation sur des plantes, sauf pour la
  calibration, l'OOD ou les anomalies quand la méthode est transférable.

## Vocabulaire

PlantVillage, PlantDoc, CCMT, in-domain / hors domaine, domain shift, remplacement de fond,
temperature scaling, ECE, OOD, rejet, spécificité, précision « anormal », multiple instance
learning, agrégation top-k, crop, PatchCore, Grad-CAM, phénotypage, DLI, VPD, EC, pH,
hydroponie, NFT / DWC, MPC, GRU / LSTM, MQTT, ESP32, Raspberry Pi 5, Hailo-8L, HEF, ONNX,
quantification INT8, humain dans la boucle, garde-fous.

## Suggestions en attente

<!-- Une ligne par suggestion : - AAAA-MM-JJ (source : paper_id ou /base-profile) — proposition — raison -->

## Historique

- 2026-10-19 — base créée (`pdb base new`).
- 2026-10-19 — 12 axes plus surveys, règles de classement, requêtes et 35 tag_rules, précisions, inclus, exclus et vocabulaire (/base-profile) — périmètre : tout le projet SerreIA.
