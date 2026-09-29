---
id: 2024-easa-concepts-design-assurance-neural-networks
fiche: done
date: 2026-09-29
benchmarks: none
---

# Concepts of Design Assurance for Neural Networks (CoDANN) II

EASA (AI Task Force) et Daedalean AG, 2024 (rapport du projet IPC juillet 2020 - mai 2021, achevé mai 2021), « public extract, version 1.1 ». Pas de DOI ni d'URL dans `metadata.json`. Auteurs listés en tête de l'extraction : G. Cima, J.-M. Cluzeau, X. Henriquel, H. Semde, G. Soudain, S. Vaubourg, V. Van Der Brugge (EASA) ; L. Van Dijk, L. Janyst, M. Körner, C. Perret-Gentil, R. Polak, I. Whittington (Daedalean).
Type : rapport technique de projet EASA / industriel (version publique amputée de plusieurs sections confidentielles), ni article relu par les pairs ni norme. Document d'information : il n'engage pas l'agence et ne crée aucune attente de certification (Abstract).

## Problème

Suite du rapport CoDANN (mars 2020), qui avait proposé un cycle de développement en W (gestion des exigences, des données, de l'apprentissage, entraînement, vérification de l'apprentissage, implémentation du modèle, vérification/intégration du modèle d'inférence, vérification indépendante des données et de l'apprentissage) pour le *learning assurance* (Executive summary, §1.1.1, Fig. 1). CoDANN II traite les points restés ouverts : environnements d'apprentissage et d'inférence et passage de l'un à l'autre (Ch. 3), explicabilité (Ch. 4), évaluation de sûreté (détection hors distribution, intégration au filtrage/suivi, incertitude, niveau d'assurance) (Ch. 5), et retour sur un cas d'usage (Ch. 2, 6) (§1.2, §1.4). Question centrale : comment conserver des garanties de performance après les transformations (conversion, quantification, élagage) et malgré un environnement d'entraînement peu maîtrisé (§3.1, §3.6).

## Méthode

Rapport conceptuel : pas d'expérience chiffrée. Cas d'usage fil rouge : détection visuelle de trafic aérien (DAA, *Detect and Avoid*), caméra 12 Mpixels, réseau CNN sur tuiles 512 x 512 RGB produisant des boîtes englobantes, suivi/filtrage en logiciel classique, deux concepts d'opération (conseil au pilote ; vol autonome) (§2.1, §2.2).
- Ch. 3 : distinction entre modèle abstrait (graphe de calcul) et implémentation, conversion de format (ONNX, TVM Relay) et de mode (§3.4), optimisations (réglage/fusion d'opérateurs, quantification uniforme, dynamique, statique, QAT ; élagage) et leurs risques (§3.5), conditions sur les transformations : équivalence ponctuelle, proximité ponctuelle mesurable, équivalence en moyenne (éq. 3.1-3.2, §3.6.1). Stratégie proposée : borne de généralisation évaluée directement sur le modèle transformé dans l'environnement d'inférence (éq. 3.3, §3.7.3), avec quantification/élagage intégrés à l'entraînement, qualification d'outils selon DO-178C §12.2 (§3.7.1) et traçabilité.
- Ch. 4 : taxonomie des explications (objet, destinataire, degré de compréhension), revue de méthodes (visualisation de filtres, méthodes génératives, activations maximales, LIME, cartes de saillance, groupes de recherche). Deux usages retenus : renforcer le lien données-apprentissage, et l'interaction homme-machine (§4.8).
- Ch. 5 : détection OOD par réduction de dimension (paramètres opérationnels explicites, PCA, autoencodeurs), métriques de qualité d'image (luminosité, contraste, entropie) (§5.1) ; critique de l'assurance à l'exécution de type ASTM F3269-17 (moniteur, commutateur, fonction de récupération) (§5.2.1) ; hypothèses de biais et de covariance pour le filtrage de Kalman (§5.3) ; incertitude (calibration, ensembles, régression quantile) (§5.4).

## Plateforme et implémentation

Sans objet pour l'implémentation (aucun résultat mesuré). Éléments matériels discutés :
- Ordre de grandeur : un détecteur DNN à 6 images/s sur des images de 12 Mpixels exige de l'ordre de 10 TOPS et 100 millions de paramètres (§3.2.2, estimation « grossière » des auteurs d'après [GLL19]) ; l'Annexe B parle de 2 à 5 TOPS int8 par caméra pour les produits Daedalean.
- CPU : preuves de conformité AMC 20-152A existantes mais puissance insuffisante pour la vision ; GPU : plateformes propriétaires (pilotes, microcode, ordonnancement), multicœur non partitionné, difficulté d'établir des preuves de certification ; FPGA/ASIC : plus de contrôle et de visibilité avec logique personnalisée ou Soft IP, au prix de la vérification de la logique et d'un jeu d'instructions (ISA) programmable (§3.2.2). Les Firm/Hard IP demandent leurs propres preuves ou une évaluation type COTS (§3.2.2).
- Annexe B : Daedalean argumente pour les FPGA contre les GPU au regard des objectifs COTS-2 à COTS-7 de l'AMC 20-152A et de l'AMC 20-193 (multicœur, CAST-32A) : pas d'errata, microcode secret, températures hors spécification, variabilité de temps d'exécution (DVFS), reconfiguration des zones désactivées.
- Nom exact du FPGA, fréquence, ressources, puissance : n/r. Code et bitstream : non publiés.

## Résultats

Aucun résultat quantitatif sur la performance d'un système (§2 à §6 conceptuels). Points saillants sourcés :
- Une borne de généralisation dépend de la classe de modèles (exemple : borne VC, d_vc = O(W L log W) pour un ReLU à L couches et W poids, Bartlett et al.) et non du procédé d'entraînement ; elle peut donc être évaluée sur le modèle transformé (§3.7.2, §3.7.3).
- Le contrôleur OOD est un moniteur d'exécution qui doit être soumis à la même analyse statistique que la fonction principale ; le réseau, le suivi et le moniteur OOD doivent recevoir un niveau d'assurance élevé, non réduit par une architecture de type RTA (§5.2.2).
- Exemple de défaut de couverture des données : un cône de circulation détecté comme hélicoptère, car le réseau entraîné sur des R66 associe la forme triangulaire (Fig. 4.10, §4.8.1).
- Recommandation : limiter la portée de la fonction ML (images individuelles, pas de bout en bout) et traiter le temps par un suivi classique (§5.2.2).
- Sections 6.1, 6.2, 6.3, 6.4.1, 6.4.3, 6.4.4 et le Chapitre 7 : retirées ou absentes du texte extrait (voir Statut de lecture). Le tableau des conditions de défaillance (Table 6.1) est listé sans corps.
→ reportés dans `benchmarks.csv` : aucune ligne. Rapport réglementaire et conceptuel sans mesure matérielle (aucun FPS, GOPS, W, ressource). `benchmarks: none`.

## Limites et critique

- Version publique expurgée « pour raisons de confidentialité » : la sécurité du système complet, l'allocation fonctionnelle, l'arbre de fautes et l'attribution des DAL (§6.3, §6.4.1, §6.4.3, §6.4.4) sont absents ; Chapitre 6.1-6.2 et 7 manquent dans le texte extrait. L'argumentaire de bout en bout n'est donc pas vérifiable.
- Document d'un partenaire industriel (Daedalean) : l'argumentaire pro-FPGA et anti-GPU (Annexe B) est une position d'entreprise, non étayée par des mesures ; les auteurs le disent eux-mêmes sur plusieurs points (« Daedalean believes »).
- Périmètre : apprentissage hors ligne uniquement (§3.2), réseaux acycliques sans récurrence (§3.4.1), CNN sur images ; l'apprentissage continu est exclu.
- Date : travaux de 2020-2021, antérieurs au concept paper EASA Level 1 finalisé et au règlement européen sur l'IA ; l'année 2024 correspond à la version publique 1.1 (déduit de `metadata.json`, non affirmé par le texte).
- Aucune validation expérimentale des techniques recommandées (borne de généralisation sur modèle quantifié, OOD, calibration) ; les difficultés (calcul de E_in sur la plateforme d'inférence, bornes pour la classe transformée) sont signalées sans solution (§3.7.3).
- Traitement de la saillance et de l'explicabilité : revue plus que prescription ; la conclusion est prudente (risque de faux sentiment de confiance, §4.8).
- Le cas d'usage est un système de sécurité aérien avec DAL ; le transfert vers IEC 61508 / ISO 13849 est une inférence (le rapport ne les cite pas dans le texte lu).

## Pertinence pour la thèse

Cœur du sujet (axe `safety-certification`). Trois apports directs :
1. Vocabulaire et cycle de développement (cycle en W, données et apprentissage comme parties de l'assurance, vérification indépendante) transposables à un YOLO sur FPGA en zone dangereuse ; le cas « détection visuelle + suivi classique » ressemble fortement au cas d'application (caméra fixe, détection de personnes).
2. Arguments FPGA vs GPU/CPU pour la certification (§3.2.2, Annexe B) : contrôle du matériel, Soft IP inspectable, déterminisme et WCET, absence de microcode opaque. Donne un fondement citable pour choisir le FPGA.
3. Traitement du passage entraînement-inférence (quantification, élagage, conversion) : c'est exactement le chemin d'un toolflow FPGA (FINN, hls4ml, Vitis AI) ; le rapport propose de mesurer les garanties sur le modèle quantifié déployé plutôt que de prouver la conservation des propriétés.
Reste ouvert : mise en œuvre concrète sur FPGA (qualification d'un toolflow, TQL), OOD/moniteur sur la cible, norme applicable hors aviation (IEC 61508, ISO 13849), personnes en milieu industriel.

## Gaps identifiés

- Qualification d'outils (DO-178C §12.2 / TQL) appliquée à des toolflows FPGA pour DNN (Vitis AI, FINN, hls4ml) : jamais traitée ici, seulement posée en principe.
- Évaluation de la borne de généralisation sur un modèle quantifié déployé sur FPGA, avec surcoût de calcul du E_in sur cible.
- Moniteur OOD et métriques de qualité d'image implémentés sur FPGA (ressources, latence).
- Correspondance de ce cadre aéronautique (DAL, AMC 20-152A) avec IEC 61508 / ISO 13849 pour un système de vidéosurveillance industrielle.
- Faux négatifs de détection : explication de l'absence de détection, signalée comme plus difficile que celle d'une détection (§6.5.1).

## Statut de lecture

Papier complet : `fulltext.md` lu en entier (2359 lignes). Le texte extrait ne contient pas les sections 6.1, 6.2, ni le Chapitre 7 ; il est incomplet dans certaines zones (fragments de sections 4.1, 5.4.4-6.x mélangés dans la liste des figures) ; la version publique retire aussi les annexes et les sections 6.3, 6.4.1, 6.4.3, 6.4.4. Tableaux sans corps extrait : Table 2, Table 4 (sous-tableaux), Table 6 (conditions de défaillance) ; figures sans légende identifiée. Les chiffres cités proviennent du texte.
Ce qui suit est déduit et non affirmé par les auteurs : transposition au cas de vidéosurveillance industrielle, lien avec IEC 61508 / ISO 13849, mappage sur les toolflows FPGA, datation des travaux (2020-2021), lecture des sections manquantes comme non disponibles plutôt que supprimées par erreur d'extraction.
