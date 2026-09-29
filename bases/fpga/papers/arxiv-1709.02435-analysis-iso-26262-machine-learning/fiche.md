---
id: arxiv-1709.02435-analysis-iso-26262-machine-learning
fiche: done
date: 2026-09-29
benchmarks: none
---

# An Analysis of ISO 26262: Using Machine Learning Safely in Automotive Software

Rick Salay, Rodrigo Queiroz, Krzysztof Czarnecki, 2017, arXiv preprint. https://arxiv.org/abs/1709.02435
Type : preprint non relu par les pairs

## Problème

ISO 26262 (sûreté fonctionnelle des véhicules routiers) n'a pas été conçue pour le machine learning ; les auteurs analysent où l'usage de ML comme technique d'implémentation logicielle perturbe le cycle de vie de sûreté (§I) et proposent des recommandations d'adaptation de la norme.

## Méthode

Analyse qualitative de la norme (surtout Part 3, analyse de risque, et Part 6, développement logiciel) : un domaine est dit « impacté » si le traitement d'un composant ML devrait différer de celui d'un composant logiciel programmé (§III). Quatre caractéristiques du ML sont retenues : non-transparence, taux d'erreur, dépendance à l'entraînement, instabilité (§II-B). Cinq domaines d'impact : identification des dangers (§III-A), fautes et modes de défaillance (§III-B), usage de jeux d'entraînement à la place d'une spécification (§III-C), niveau d'usage du ML (§III-D), techniques logicielles requises (§III-E). Pour ce dernier, évaluation des 75 techniques de la Part 6 (34 au niveau unité) en trois catégories : Ok / Adapt / N/A (Fig. 3). Pas de FPGA ni de matériel.

## Plateforme et implémentation

Sans objet (analyse normative). Code : sans objet. Plateforme, puissance : n/r.

## Résultats

- ML apporte de nouveaux dangers non dus à une défaillance (complaisance de l'opérateur, réward hacking en RL) : recommandation d'élargir la définition de « hazard » (§III-A).
- Les fautes peuvent être spécifiques au ML (topologie, algorithme d'apprentissage, jeu de données), mais les modes de défaillance ne diffèrent pas : sortie incorrecte pour une entrée (§III-B).
- Un jeu d'entraînement viole l'hypothèse de spécification complète du modèle en V ; certaines fonctions de perception (« reconnaître un piéton ») sont possiblement inspécifiables. Recommandation : exigences différenciées selon que la fonction est spécifiable, spécifications partielles, couverture du jeu de données, et pour les ASIL élevés des stratégies de tolérance aux fautes (reconnaisseurs redondants sur modèles et jeux différents, « safety envelope ») (§III-C).
- Approche end-to-end déconseillée : incompatible avec l'architecture hiérarchique stable ; ML limité au niveau composant (§III-D).
- Environ 40 % des techniques du niveau unité sont N/A pour le ML quel que soit le degré de recommandation ; les techniques « highly recommended » applicables le sont surtout aux ASIL bas (§III-E, Fig. 3 ; valeurs exactes lues dans un graphique non extrait, non reprises ici). Recommandation : exprimer les exigences par intention et maturité des techniques.
→ reportés dans `benchmarks.csv` : aucune ligne (papier normatif/conceptuel sans mesure) ; `benchmarks: none`.

## Limites et critique

Analyse d'auteurs, sans validation empirique ni retour d'assesseurs ; preprint 2017, antérieur à ISO/PAS 8800 et à SOTIF (ISO 21448), donc en partie daté (déduit, non dit par le papier). La Fig. 3 (proportions Ok/Adapt/N/A) est un jugement des auteurs, sans critères détaillés dans le texte. Cadre automobile : la transposition à IEC 61508 / ISO 13849 est un travail à faire. Ne traite pas du matériel d'exécution (FPGA, SEU) : les fautes matérielles sont évoquées seulement comme fautes « apparentes » du logiciel sous-jacent (§III-B).

## Pertinence pour la thèse

Cœur du sujet « certifiable » : donne un vocabulaire et une grille d'analyse (non-spécifiabilité, exigences de données, tolérance aux fautes par redondance diversifiée, ML limité au niveau composant) transposables à un YOLO de détection de personnes en zone dangereuse, dont l'exigence « détecter une personne » est précisément inspécifiable au sens du §III-C. La recommandation de redondance de reconnaisseurs et de safety envelope motive des architectures FPGA à moniteurs. Ce que le papier laisse ouvert : la norme visée (IEC 61508 / ISO 13849) et la couche matérielle.

## Gaps identifiés

- Transposition de cette analyse ISO 26262 aux normes industrielles (IEC 61508, ISO 13849, IEC 62061).
- Lien entre exigences de données/couverture et architecture d'exécution sur FPGA (déterminisme, moniteurs).

## Statut de lecture

papier complet (fulltext.md lu en entier ; extraction GROBID ok). Les figures 1 à 3 ne sont pas dans le texte extrait. Déduit et non affirmé par les auteurs : l'obsolescence relative face à ISO/PAS 8800 / SOTIF, et la pertinence pour YOLO en vidéosurveillance.
