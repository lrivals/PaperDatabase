---
id: 2020-schwalbe-survey-methods-safety-assurance-machine
fiche: done
date: 2026-09-29
benchmarks: none
---

# A Survey on Methods for the Safety Assurance of Machine Learning Based Systems

Gesina Schwalbe, Martin Schels, 2020, 10th European Congress on Embedded Real Time Software and Systems (ERTS 2020). DOI et URL : n/r dans `metadata.json`.
Type : article de conférence (survey court)

## Problème

Les méthodes d'assurance de sûreté de la norme automobile ISO 26262 ne suffisent pas pour des systèmes fondés sur l'apprentissage automatique (ML) : inspection et tests unitaires exhaustifs inapplicables à cause de la complexité, argument « proven in use » impossible (§1). Les auteurs veulent un panorama orienté certification des méthodes de soutien à un argumentaire de sûreté, et les défis ouverts.

## Méthode

Survey : les méthodes sont triées selon les phases du cycle de vie en V d'ISO 26262 partie 6 (ingénierie des exigences, développement, vérification, validation), avec pour chaque catégorie la maturité et le domaine d'applicabilité (types de ML) (Table 1, §2). Centré sur les réseaux de neurones (DNN) et la conduite autonome. Aucune méthodologie de sélection de la littérature n'est décrite (déduit : sélection non systématique).

Contenu résumé :
- Exigences (§2.1) : représentativité des données (couverture de scénarios, ontologie de l'espace d'entrée), robustesse (adversariale), tolérance aux fautes (surveillance à l'exécution, redondance et mesure de diversité de modèles), performances liées à la sûreté (ex. objets occultés), plausibilité, expérience de fautes connues.
- Développement (§2.2) : choix de conception justifiés, prise en compte de l'incertitude (réseaux bayésiens, poids probabilistes, Dirichlet, dropout), inclusion de connaissances expertes (fonction de perte, topologie, réparation de modèle pour l'apprentissage par renforcement), renforcement de la robustesse.
- Vérification (§2.3) : solveurs SMT / MILP, estimation de bornes de sortie (ReluVal, DeepGo), algorithmes de recherche ; Reluplex [22] cité comme exemple de vérificateur de règles à logique du premier ordre.
- Validation (§2.4) : couverture des données de test, génération de contre-exemples, analyses qualitatives (cartes d'attention, LIME, RISE, visualisation de features) et quantitatives (extraction de règles, analyse de concepts : Net2Vec, TCAV).

Défis ouverts déduits (résumé) : solveurs plus puissants, inclusion de connaissance experte, validation de la représentativité des données et de la diversité de modèles, introspection du modèle avec garanties prouvables.

## Plateforme et implémentation

Sans objet : survey, aucune implémentation, aucune plateforme matérielle. Aucun code publié.

## Résultats

Pas de résultats chiffrés. Le livrable est la Table 1 (catégories de méthodes par phase, avec exemples, références et portée) et la liste de défis ouverts.
→ reportés dans `benchmarks.csv` : aucune ligne (survey sans mesure matérielle ; `benchmarks: none`).

## Limites et critique

- Très bref (extrait d'environ 17 ko de texte) ; description de chaque catégorie en quelques lignes ; pas de comparaison quantitative, ni de critère explicite de maturité dans le texte extrait (la Table 1 est en partie tronquée à l'extraction).
- Ancré dans ISO 26262 et la conduite autonome ; aucune mention des normes IEC 61508, ISO 13849 ou ISO/IEC TR 5469 dans le texte lu (déduit de l'absence), ni du matériel : rien sur l'implémentation FPGA, la quantification, la tolérance aux SEU ou l'exécution déterministe.
- Vision 2020 : ne couvre pas la prédiction conforme, ISO/PAS 8800 ni les détecteurs OOD récents (déduit de l'année et de l'absence).
- Peu de matériel sur la détection d'objets ; le focus est plus général.

## Pertinence pour la thèse

Forte comme cadrage : structure d'un argumentaire de sûreté ML en phases de cycle de vie, avec le vocabulaire (représentativité des données, robustesse, surveillance à l'exécution, vérification formelle, validation par introspection) utile au volet « certifiable » du sujet. Elle situe Reluplex [22] dans la catégorie « vérification » (recoupe la fiche arxiv-1702.01135). Ce qu'elle laisse ouvert pour la thèse : traduire cet argumentaire vers une cible FPGA (matériel, quantification, HLS), vers IEC 61508 / ISO 13849 plutôt qu'ISO 26262, et vers un détecteur YOLO de personnes en zone industrielle.

## Gaps identifiés

- Correspondance entre méthodes d'assurance ML et normes industrielles (IEC 61508, ISO 13849, ISO/IEC TR 5469) au lieu d'ISO 26262.
- Aucune méthode traitant l'assurance au niveau matériel (FPGA, quantification, tolérance aux fautes matérielles) : les méthodes du survey ne concernent que le modèle logiciel.
- Défis ouverts de validation de la représentativité des données et de la diversité de modèles, à instancier sur la détection de personnes.

## Statut de lecture

Papier complet (fulltext.md lu en entier, environ 17 ko). La Table 1 est partiellement tronquée à l'extraction (lignes de vérification et validation absentes ou fragmentaires) ; le texte du §2 en donne le contenu. Déduit et non affirmé par les auteurs : absence de méthode de sélection, absence de normes non automobiles, pertinence pour le FPGA.
