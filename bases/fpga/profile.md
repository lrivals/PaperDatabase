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
- Tension à instruire (2026-10-01) : apprentissage embarqué contre certification. Les cadres
  actuels (EASA, AMLAS) excluent l'apprentissage en ligne ; question du gel du modèle, du
  versionnage, de la non-régression et du retour arrière d'un modèle mis à jour sur la cible.

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
- Guidance des autorités de certification sur le ML (EASA, concept papers), même hors FPGA ;
  processus de certification ML (ARP6983, ED-324) sur cible non FPGA (Jetson), comme
  références de méthode.
- Génération de code prédictible pour DNN (WCET, traçabilité DO-178C, préservation sémantique
  entre modèle et implémentation).
- Entraînement et fine-tuning embarqués (FPGA, MCU : on-device training, sparse update), rangés
  dans l'axe `continual-learning`.
- Détection d'anomalies et d'OOD visuelles non supervisée (PatchCore, PaDiM, student-teacher),
  comme brique de moniteur d'exécution.
- Compression d'image apprise : seulement si la méthode (quantification, codage) est
  transférable à la détection.

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
Certification ML (aéronautique) : learning assurance / W-shaped, ODD / MLCODD, AMC 20-152A,
AMC 20-193, ED-79B / ARP4754B, ARP6983 / ED-324, EASA AI Roadmap, MLEAP, CoDANN, DAL / IDAL,
tool qualification (TQL), COTS, Doer/Checker, Common Mode Analysis. Robotique collaborative :
ISO 10218, ISO/TS 15066, HRC, speed and separation monitoring, safety-rated monitored stop.
Fiabilité : FIT, SDC (silent data corruption), symptom-based detector, selective latch
hardening. Surveillance : novelty detection, abstraction-based monitor, uncertainty estimation,
localization uncertainty, calibration, incertitude aléatoire / épistémique. Apprentissage
continu : class-IL / task-IL, task-recency bias, exemplars, herding, oubli catastrophique, FACIL,
dataset distillation / distilled replay, on-device training. Mesure : MLPerf Tiny, QONNX, EEMBC
EnergyRunner. Détection : YOLO récents avec attention (v11/v26, OBB, NMS-free), adaptation
d'opérateurs non supportés par le DPU.

## Suggestions en attente

<!-- Une ligne par suggestion : - AAAA-MM-JJ (source : paper_id ou /base-profile) — proposition — raison -->

- 2026-09-29 (arxiv-2001.04193-deep-learning-person-re-identification) — décider si les mesures de précision sans plateforme embarquée (Re-ID, détection de personnes sur GPU) ont leur place dans `benchmarks.csv` — aujourd'hui exclues, alors que le cas d'application les rend utiles comme référence — **reportée 2026-10-01** : change le schéma (SETUP §9)
- 2026-09-29 (2024-easa-concepts-design-assurance-neural-networks) — ajouter au vocabulaire DAL, AMC 20-152A, AMC 20-193, learning assurance, tool qualification (TQL), COTS ; ajouter `learning assurance|design assurance|AMC 20-152|tool qualification` à `axis_rules.safety-certification` ; prévoir un type « rapport » (report) dans le schéma — les rapports EASA n'ont aucun type valide et n'activent l'axe que par des termes absents des règles — **reportée 2026-10-01** : change le schéma (SETUP §9)

## Historique

- 2026-09-24 — axes de veille repris de `basicStart.txt` ; `in_topic` exige un contexte matériel.
- 2026-09-28 — profil rédigé par Claude à partir de `CLAUDE.md`, `base.json` et `gaps.md`, à relire (`/base-profile`).
- 2026-09-29 — thème de thèse précisé (IA embarquée sécuritaire certifiable sur FPGA ; cas YOLO vidéosurveillance de personnes en secteur industriel dangereux) ; axes `safety-certification` et `person-detection` ajoutés — demande utilisateur.
- 2026-10-01 — `safety-certification` : règle élargie (EASA, assurance, ODD, TQL, monitors, conformal, incertitude, vérification de BNN, trustworthiness), `radiation` restreint aux effets radiatifs — rattrape 6 fiches, retire 2 faux positifs HEP (suggestions du 29/09)
- 2026-10-01 — `person-detection` : `+ crowd`, axe ajouté à `hardware_axes` ; `title_topic_re` : `+ tiny (deep learning|ml)` ; tags conformal, easa, uncertainty, hrc — hors sujet 13 → 4 papiers
- 2026-10-01 — Précisions (apprentissage embarqué contre certification), Inclus (EASA, ARP6983, code prédictible, entraînement embarqué, anomalies visuelles, compression) et Vocabulaire complétés — 19 suggestions du 29/09 retenues
- 2026-10-01 — écartée : élargir `yolo-fpga` à la détection d'objets (≈10 faux positifs pour 4 papiers rattrapés ; axes des fiches déjà confirmés) ; reportées : type « report », benchmarks hors plateforme embarquée
