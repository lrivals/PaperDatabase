---
id: arxiv-2102.01564-guidance-assurance-machine-learning-autonomous
fiche: done
date: 2026-09-29
benchmarks: none
---

# Guidance on the Assurance of Machine Learning in Autonomous Systems (AMLAS)

Richard Hawkins, Colin Paterson, Chiara Picardi, Yan Jia, Radu Calinescu, Ibrahim Habli, 2021, arXiv preprint (Assuring Autonomy International Programme, University of York). https://arxiv.org/abs/2102.01564
Type : preprint non relu par les pairs (document de guidance ; les auteurs précisent qu'il est « provided as guidance only »)

## Problème

Des systèmes autonomes critiques (santé, automobile, industrie) embarquent du ML dont les performances peuvent dépasser l'humain, mais établir une confiance justifiée dans ce ML est une composante centrale du dossier de sûreté (safety case) du système (Abstract, Introduction). Il manque une méthode qui relie explicitement l'analyse de danger/risque du système aux exigences de sûreté du composant ML, puis à la donnée, à l'apprentissage, à la vérification et au déploiement (Introduction).

## Méthode

AMLAS = un processus en six étapes + des patrons d'arguments de sûreté en GSN (Goal Structuring Notation), à exécuter en parallèle du développement et de façon itérative (Overview, Fig. 1) :

1. Safety Assurance Scoping : exigences de sûreté système allouées au composant ML, description de l'environnement, du système et du composant ; le composant ML inclut le modèle et la plateforme matérielle/logicielle cible (Stage 1).
2. ML Safety Requirements : traduire en exigences de performance et de robustesse mesurables (ex. « boîtes au plus 10 % plus grandes que la boîte minimale » ; « identifier toute personne présente avec une précision d'au moins 0,93 », Ex. 6-7) ; validation par revue et simulation (Stage 2).
3. Data Management : exigences de données (pertinence, complétude, exactitude, équilibre), trois jeux distincts (développement, test interne, vérification), journal de génération, validation (Stage 3, Ex. 22 : 16 856 combinaisons de conditions pour 43 classes de panneaux).
4. Model Learning : choix du modèle, journal de développement, test interne, sélection multi-objectifs (Stage 4).
5. Model Verification : au moins une activité de vérification par exigence, par test sur données de vérification cachées aux développeurs et/ou vérification formelle (SMT, ex. ACAS Xu, Ex. 37), indépendance proportionnée à la criticité (Stage 5).
6. Model Deployment : intégration, surveillance à l'exécution des hypothèses d'environnement, journal des comportements erronés, tests d'intégration en simulation / hardware-in-the-loop / déploiement fantôme (Stage 6, Activities 15-16).

Chaque étape se termine par l'instanciation d'un patron d'argument (claims G*, stratégies S*, justifications J*) et produit des artefacts nommés [A] à [FF]. Périmètre : apprentissage supervisé hors ligne ; à utiliser avec d'autres normes (ARP4754A, ISO/PAS 21448, UL 4000…) (Using this Document).

## Plateforme et implémentation

Sans objet : document méthodologique, aucune plateforme, mesure, code ni bitstream. Le seul point matériel : vérifier à l'intégration que la plateforme cible est adaptée au modèle (puissance de calcul, latence d'accès aux données), sinon redévelopper un modèle plus léger (Stage 6, Ex. 45, Note 39).

## Résultats

Pas de résultats expérimentaux ni de chiffres de performance : les valeurs numériques citées sont des exemples illustratifs (Ex. 6, 7, 22, 28, 46). Aucune étude de cas complète ; les auteurs annoncent des études de cas et expériences futures (Using this Document). Aucune ligne dans `benchmarks.csv` (`benchmarks: none`), document normatif/méthodologique sans mesure.

## Limites et critique

- Aucune validation empirique de la méthode dans ce document (« planned case studies and future experiments »). L'efficacité pour convaincre un certificateur n'est pas démontrée (déduit).
- Portée limitée au composant ML et à l'apprentissage supervisé hors ligne ; l'apprentissage continu/en ligne, pertinent pour la base, n'est pas traité (Using this Document).
- Aucune prise en compte du FPGA : la chaîne de compilation (quantification, HLS, synthèse), la préservation de la sémantique entre modèle entraîné et implémentation matérielle, et les défauts matériels (SEU) ne sont pas abordés ; « model + plateforme » n'est mentionné qu'au titre de l'adéquation (Stage 1, Stage 6). Le guide renvoie à DO-178C seulement pour la qualification d'outils de simulation (Note 18) ; DO-254 et IEC 61508 ne sont pas cités dans le texte lu (déduit de la lecture ; à vérifier par recherche).
- Certaines parties d'arguments (G5.6, G5.8, G6.7) sont laissées « non développées » ; la vérification formelle est traitée en quelques notes (Note 35-36), avec la critique que la robustesse ponctuelle sur pixels n'a pas de sens opérationnel.
- Le texte extrait est ordonné de façon irrégulière (titres de stage décalés, figures sans corps) ; les patrons GSN (Fig. 5, 7, 9, 12, 14, 15) ne sont pas lisibles dans l'extraction.
- Guidance d'un groupe académique, pas une norme : pas de valeur réglementaire propre.

## Pertinence pour la thèse

Très forte pour l'axe « assurance et certification » : c'est un squelette de dossier de sûreté applicable à un YOLO de détection de personnes. Les exemples du guide sont proches du cas d'application (exigence « identifier toute personne présente dans la zone définie », robustesse à l'éclairage et à la pose, Ex. 7 ; boîtes englobantes de piétons, Ex. 6). Utilisable tel quel pour structurer : exigences de performance/robustesse (rappel de personnes), exigences de données pour la vidéosurveillance industrielle, jeu de vérification caché, surveillance à l'exécution des hypothèses (éclairage, distribution des entrées, Ex. 43 et Note 38) et tolérance aux erreurs par vote sur plusieurs images (Ex. 46). Reste ouvert : l'étape « déploiement » n'est pas raffinée pour un accélérateur FPGA (équivalence modèle-bitstream, fautes matérielles, déterminisme temporel), ni articulée avec IEC 61508 / ISO 13849.

## Gaps identifiés

- Extension d'AMLAS à la cible FPGA : preuves d'équivalence flottant/quantifié/bitstream, effet de la quantification sur les exigences de robustesse, déterminisme et WCET.
- Correspondance AMLAS vers IEC 61508 / ISO 13849 / ISO/IEC TR 5469 pour un composant de vision en machinerie.
- Exigences de données et jeux de vérification pour la détection de personnes en zone industrielle dangereuse (EPI, occultation, éclairage).
- Étude de cas complète d'AMLAS sur un détecteur d'objets embarqué.

## Statut de lecture

Papier complet (fulltext.md lu en entier, 942 lignes). Extraction grobid, ok. Les figures (patrons GSN) n'ont pas de contenu extrait ; seules les descriptions textuelles des claims ont été lues.
Ce qui suit est déduit et non affirmé par les auteurs : l'absence de valeur probante démontrée devant un certificateur ; le manque de traitement du FPGA/hardware (absence constatée dans le texte extrait) ; la correspondance avec les normes IEC ; l'application au cas YOLO.
