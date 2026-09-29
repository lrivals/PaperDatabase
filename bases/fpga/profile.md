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

- 2026-09-29 (2024-easa-concept-paper-guidance-level-1) — ajouter au vocabulaire « learning assurance / W-shaped, ODD (operational design domain), AMC 20-152A, ED-79B/ARP4754B, MLEAP, CoDANN » et dans Inclus « guidance d'autorités de certification sur le ML (EASA), même hors FPGA » — cœur du sujet thèse, termes absents du profil
- 2026-09-29 (2024-easa-concept-paper-guidance-level-1) — ajouter `EASA|learning assurance|operational design domain` à `axis_rules.safety-certification` — le document n'est capté que via « certif- »
- 2026-09-29 (arxiv-2001.04193-deep-learning-person-re-identification) — décider si les mesures de précision sans plateforme embarquée (Re-ID, détection de personnes sur GPU) ont leur place dans `benchmarks.csv` — aujourd'hui exclues, alors que le cas d'application les rend utiles comme référence
- 2026-09-29 (2024-easa-concepts-design-assurance-neural-networks) — ajouter au vocabulaire DAL, AMC 20-152A, AMC 20-193, learning assurance, tool qualification (TQL), COTS ; ajouter `learning assurance|design assurance|AMC 20-152|tool qualification` à `axis_rules.safety-certification` ; prévoir un type « rapport » (report) dans le schéma — les rapports EASA n'ont aucun type valide et n'activent l'axe que par des termes absents des règles
- 2026-09-29 (2020-easa-concepts-design-assurance-neural-networks) — ajouter au vocabulaire Learning Assurance, ODD / MLCODD, ARP6983 / ED-324, EASA AI Roadmap, Doer/Checker, Common Mode Analysis, DAL/IDAL — termes centraux de la certification ML aéronautique, absents du profil
- 2026-09-29 (arxiv-2406.12362-certified-ml-object-detection-surveillance) — préciser dans « Inclus » que les papiers de processus de certification ML (ARP6983, ED-324) sur cible non FPGA (Jetson) sont inclus comme références de méthode — YOLO certifié sur GPU embarqué
- 2026-09-29 (arxiv-2010.15277-class-incremental-learning-survey-performance) — ajouter au vocabulaire class-incremental / task-IL, task-recency bias, exemplars, herding, oubli catastrophique, FACIL — vocabulaire central du class-IL, absent du profil
- 2026-09-29 (arxiv-2202.10935-ef-train-enable-efficient-device) — ajouter au périmètre « entraînement / fine-tuning embarqué sur FPGA » et « on-device training » au vocabulaire, avec la question « apprentissage embarqué et certification (gel du modèle, versionnage, non-régression) » — tension entre « certifiable » et apprentissage en ligne (l'EASA exclut l'apprentissage en ligne)
- 2026-09-29 (2023-cui-survey-unsupervised-anomaly-detection-algorithms) — ajouter au profil (et éventuellement à base.json) « détection d'anomalies / OOD visuelle non supervisée (PatchCore, PaDiM, student-teacher) » comme brique de moniteur d'exécution — utile pour un YOLO sûr ; aujourd'hui seulement le tag anomaly-detection
- 2026-09-29 (2017-li-understanding-error-propagation-deep-learning) — ajouter au vocabulaire FIT, SDC (silent data corruption), symptom-based detector, selective latch hardening — termes centraux de la fiabilité des accélérateurs DNN
- 2026-09-29 (arxiv-2304.06052-confident-object-detection-conformal-prediction) — ajouter `conformal (?:prediction|risk control)|uncertainty quantification` à `axis_rules.safety-certification` — le profil cite la prédiction conforme mais aucune règle d'axe ne la capte
- 2026-09-29 (arxiv-2006.08357-codenet-efficient-deployment-input-adaptive) — élargir `yolo-fpga` à « détection d'objets sur FPGA » (CenterNet, anchor-free, convolution déformable) ou créer un axe dédié — CoDeNet n'est classé que par le mot « yolo »
- 2026-09-29 (arxiv-1904.04620-gaussian-yolov3-accurate-fast-object) — ajouter au vocabulaire et à `axis_rules.safety-certification` : uncertainty estimation, localization uncertainty, calibration, incertitude aléatoire / épistémique — moniteur d'exécution pour YOLO non capté par les règles
- 2026-09-29 (arxiv-2511.17135-multi-stage-optimization-framework-deploying) — préciser dans « Inclus » que la quantification issue de la compression d'image apprise n'est admise que si transférable à la détection — papier sans implémentation FPGA
- 2026-09-29 (2022-de-albuquerque-silva-acetone-predictable-programming-framework-ml) — ajouter à « Inclus » et au vocabulaire la génération de code prédictible pour DNN (WCET, OTAWA, traçabilité DO-178C, préservation sémantique modèle/implémentation) — sous-thème assurance logicielle des DNN
- 2026-09-29 (arxiv-2206.15472-device-training-256kb-memory) — préciser que l'entraînement / fine-tuning sur MCU (TinyML, QAS, sparse update) relève de l'axe continual-learning — transfer learning et non apprentissage continu strict
- 2026-09-29 (arxiv-2206.11791-open-source-fpga-ml-codesign) — ajouter au vocabulaire MLPerf Tiny, QONNX, EEMBC EnergyRunner — utiles pour la comparabilité des mesures de puissance (`power_scope`)
- 2026-09-29 (arxiv-2607.13106-no-attention-no-problem-dpu) — ajouter au vocabulaire les YOLO récents avec attention (v11/v26, OBB, NMS-free) et le sous-thème « adaptation d'opérateurs non supportés par le DPU » — YOLO récents absents du profil
- 2026-09-29 (2018-halme-review-vision-safety-systems-human) — ajouter au vocabulaire ISO 10218, ISO/TS 15066, collaboration humain-robot (HRC), speed and separation monitoring, safety-rated monitored stop — cadre normatif du cas d'application industriel
- 2026-09-29 (arxiv-2411.01118-variational-autoencoders-source-data-reduction) — la règle `safety-certification` capte « radiation » en physique des particules : restreindre (ex. `radiation(?:-induced| test| hardness| effects)`) — risque de faux positifs HEP dans l'axe
- 2026-09-29 (arxiv-1911.09032-outside-box-abstraction-monitoring-neural) — ajouter au vocabulaire et à `axis_rules.safety-certification` « novelty detection », « abstraction-based monitor » — surveillance à l'exécution, cœur de la thèse, partiellement captée
- 2026-09-29 (arxiv-2409.07114-continual-incremental-learning-tinyml-device) — ajouter au vocabulaire « dataset distillation », « distilled replay » — technique d'apprentissage continu récurrente

## Historique

- 2026-09-24 — axes de veille repris de `basicStart.txt` ; `in_topic` exige un contexte matériel.
- 2026-09-28 — profil rédigé par Claude à partir de `CLAUDE.md`, `base.json` et `gaps.md`, à relire (`/base-profile`).
- 2026-09-29 — thème de thèse précisé (IA embarquée sécuritaire certifiable sur FPGA ; cas YOLO vidéosurveillance de personnes en secteur industriel dangereux) ; axes `safety-certification` et `person-detection` ajoutés — demande utilisateur.
