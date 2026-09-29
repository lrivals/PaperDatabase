---
id: 2020-easa-concepts-design-assurance-neural-networks
fiche: done
date: 2026-09-29
benchmarks: none
---

# Concepts of Design Assurance for Neural Networks (CoDANN)

EASA, Daedalean, 2020, EASA AI Task Force and Daedalean AG, public report extract, version 1.0 (contrat IPC P-EASA.IPC.004, mai 2019 - février 2020). DOI/URL : n/r.
Type : rapport public de projet (extrait d'un rapport d'Innovation Partnership Contract), sans valeur normative (avertissement en tête : « no binding advice »), non relu par les pairs. `type` laissé à `null` dans `metadata.json` (pas de valeur du vocabulaire fermé adaptée).

## Problème

Les cadres classiques de Development Assurance (ARP4754A/ED-79A, DO-178C/ED-12C) ne conviennent pas au ML : difficulté à décrire la fonction voulue, manque de prédictibilité et d'explicabilité, pas de garantie de robustesse ni d'absence de « fonction non voulue », pas de méthode standard d'évaluation, biais/variance, complexité, apprentissage adaptatif (liste reprise de l'EASA AI Roadmap, §2.1). Le rapport cherche à poser un premier jeu de lignes directrices de « Learning Assurance » compatibles avec le cadre réglementaire EASA, et à dériver des garanties quantitatives pour un composant ML dans une analyse de sûreté réaliste (§2.4).

## Méthode

Rapport conceptuel, sans expérience propre. Cas fil rouge : Visual Landing Guidance (détection de piste/vertiport sur image 512x512 par un CNN, plus pré/post-traitement classique ; §4.2). Apports :

- Cycle de vie en W (§6.1, Fig. 6.1) : extension du cycle en V avec gestion des données, gestion du processus d'apprentissage, entraînement, vérification du processus d'apprentissage, implémentation du modèle, vérification du modèle d'inférence, vérification des données (avec indépendance).
- Généralisation (§5.3) : écart de généralisation G = E_out - E_in ; décomposition biais/variance ; revue des bornes (VC, Rademacher, PAC-Bayes, compression). Constat : pour les gros réseaux ces bornes sont trop lâches, d'où l'approche par évaluation sur jeu de validation, dont la dépendance en δ est seulement logarithmique (§5.3.5-5.3.7).
- Exigences sur les données (§6.2) : domaine opérationnel, exactitude, traçabilité « back-to-birth », CRC, paramètres d'exploitation explicites, complétude (jeux échantillonnés indépendamment dans X, vérifiée par un « input distribution discriminator » testé sur un jeu OOD), indépendance entre jeux (test élaboré par des personnes distinctes, gelé avant la conception), tailles.
- Vérification du modèle (§6.4) : reproductibilité, dissimilarité multi-versions (ensembles ; exemple 21 classifieurs à 30 % d'erreur indépendante donnant < 0,52 % par vote majoritaire, §6.3.3), tests boîte blanche, falsification, vérification formelle (Reluplex, ReluVal, DeepZ...), limites de passage à l'échelle et de complétude.
- Surveillance à l'exécution (§6.6) : séparation Doer/Checker, taxonomie des entrées (attendues, cas limites, aberrations statiques/dynamiques, attaques adverses), détection OOD par seuils sur le discriminateur, incertitude épistémique/aléatoire, calibration, ensembles, MC dropout, risques (seuils empiriques non valables en opération, modes communs dans les ensembles).
- Concepts avancés : transfert d'apprentissage, données synthétiques (§7), métriques (§8), analyse de sûreté (§9) : FHA, allocation d'objectifs (10^-7/h Hazardous, 10^-9/h Catastrophic, Fig. 9.3), mitigations d'architecture (contrôle/moniteur, tracking, modèles indépendants, manoeuvres), DAL, Common Mode Analysis. La FMEA quantitative du réseau (§9.5) est caviardée dans cet extrait.
- Hypothèses : système non adaptatif (gelé après conception), déterministe, CNN feed-forward supervisé (§2.6, §4.2.1).

## Plateforme et implémentation

Sans objet : pas de plateforme, pas de mesure. Le matériel est explicitement hors périmètre : la conformité du matériel spécialisé (GPU, ASIC, FPGA) à DO-254 « will not be addressed » (§4.2.3), la vérification de l'étape d'implémentation/inférence est laissée à un travail futur (§6.5) et les FPGA/GPU sont cités comme non investigués (Conclusion, Future work). Code ou bitstream : sans objet.

## Résultats

Pas de résultats expérimentaux. Chiffres illustratifs seulement : erreurs 0,20 puis 0,15 en validation, 0,17 en test, 0,18 en opération pour l'exemple pédagogique (§5.2.5) ; répartition 70/15/15 (§5.2.5) ; objectifs quantitatifs 10^-7 et 10^-9 par heure de vol (§9.2.5, Fig. 9.3) ; hypothèse classique de fiabilité de plateforme de 10^-3 à 10^-5 par heure (§9.2.5) ; deux modèles indépendants à 10^-5 donneraient 10^-10 (§9.2.5). Ce sont des exemples ou hypothèses, pas des mesures.
→ reportés dans `benchmarks.csv` : aucune ligne (document normatif/conceptuel sans mesure matérielle ; `benchmarks: none`).

## Limites et critique

- Extrait public : la FMEA quantitative (§9.5) et le chapitre 10 (résumé du cas d'usage) manquent ; le chapitre 10 est absent du texte extrait, sans mention de caviardage explicite dans le texte lu.
- Aucun statut normatif ; en 2020 le rapport précède les guidances EASA ultérieures (concept paper) et ARP6983/ED-324. Le lire comme une source d'idées, non comme exigence (déduit).
- Écrit par un industriel (Daedalean) et l'autorité : l'argumentation sur les bornes de généralisation est heuristique ; les bornes théoriques sont reconnues inutilisables pour les gros réseaux (§5.3.5), donc les garanties quantitatives reposent sur l'hypothèse d'échantillonnage i.i.d. du domaine opérationnel, elle-même difficile à démontrer (§6.2.8, §6.6.5).
- Le discriminateur de distribution est en partie un argument circulaire (lui-même un modèle ML), atténué mais non levé (§6.2.8).
- Hors périmètre : matériel d'inférence, quantification/optimisation (seulement « à valider », §6.1), sécurité informatique (attaques), apprentissage adaptatif, explicabilité, architectures récurrentes.
- Aucune comparaison à un baseline (pas d'expérience).

## Pertinence pour la thèse

Référence fondatrice pour l'axe `safety-certification` : elle fournit le vocabulaire (Learning Assurance, cycle en W, ODD/domaine opérationnel, discriminateur OOD, Doer/Checker, CMA) sur lequel le pré-projet peut s'appuyer, et un canevas pour un dossier d'assurance de YOLO en vidéosurveillance de personnes : exigences de données (complétude, indépendance des jeux, traçabilité), moniteur OOD à l'exécution, architecture redondante/dissimilaire, choix de métriques asymétriques (faux négatifs plus coûteux que faux positifs, §8.1.1, exactement le cas de la détection de personnes en zone dangereuse). Elle laisse ouvert le point central de la thèse : l'étape « implémentation du modèle » sur FPGA (quantification, HLS, préservation des propriétés, WCET, déterminisme, SEU), explicitement renvoyée à un travail futur. Le cadre suppose un modèle gelé, cohérent avec un YOLO figé sur FPGA, mais exclut l'apprentissage continu embarqué (déduit : tension avec l'axe `continual-learning`). Domaine aéronautique : la transposition à IEC 61508 / ISO 13849 est à faire (non traitée par le papier).

## Gaps identifiés

- Vérification de l'inférence quantifiée/compilée sur FPGA (équivalence avec le modèle entraîné, préservation des propriétés) : laissée ouverte (§6.5).
- Certification du matériel d'accélération (DO-254 ou équivalent industriel) pour DNN : hors périmètre (§4.2.3).
- Transposition du Learning Assurance hors aéronautique (IEC 61508, ISO 13849, ISO/PAS 8800) : non traitée.
- Réévaluation/recertification après ré-entraînement (§7.1.3) et apprentissage adaptatif : reportés.
- Détection OOD/monitorage implémentable sur FPGA en parallèle du réseau (moniteur indépendant) : décrit conceptuellement seulement.

## Statut de lecture

Papier complet (fulltext.md lu en entier, 2011 lignes ; extraction Grobid `ok`). Attention : le chapitre 10 et le début de la section 6.3 (6.3.1) sont absents ou fragmentés dans le texte extrait ; Fig. 4.1, 6.1, 9.2 et 9.3 et une partie des tableaux (Table 9.3, sans corps chiffré) ne sont pas lisibles dans le texte ; seules les légendes ou fragments sont disponibles.
Ce qui suit est déduit et non affirmé par les auteurs : la portée du rapport comme « source d'idées et non exigence » ; la tension avec l'apprentissage continu ; la transposition aux normes industrielles hors aéronautique ; l'application au cas YOLO/FPGA/vidéosurveillance de personnes ; l'asymétrie faux négatifs/faux positifs pour la détection de personnes (le rapport ne l'énonce que pour la détection d'aéronefs, §8.1.1).
