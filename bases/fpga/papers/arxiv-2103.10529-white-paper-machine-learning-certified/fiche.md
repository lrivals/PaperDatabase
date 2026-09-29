---
id: arxiv-2103.10529-white-paper-machine-learning-certified
fiche: done
date: 2026-09-29
benchmarks: none
---

# White Paper Machine Learning in Certified Systems

Hervé Delseny, Christophe Gabreau, Adrien Gauffriau, Bernard Beaudouin, Ludovic Ponsolle, Lucian Alecu, Hugues Bonnin, Brice Beltran, Didier Duchel, Jean-Brice Ginestet, Alexandre Hervieu, Ghilaine Martinez, Sylvain Pasquet, Kevin Delmas, Claire Pagetti, Jean-Marc Gabriel, Camille Chapdelaine, Sylvaine Picard, Mathieu Damour, Cyril Cappi, Laurent Gardès, Florence De Grancey, Eric Jenn, Baptiste Lefevre, Gregory Flandin, Sébastien Gerchinovitz, Franck Mamalet, Alexandre Albore, 2021, arXiv preprint. https://arxiv.org/abs/2103.10529
Type : preprint non relu par les pairs (livre blanc du groupe de travail « ML Certification » du projet DEEL, IRT Saint Exupéry / ANITI ; les auteurs le présentent comme un instantané de travaux en cours, Abstract)

## Problème

Les normes de certification (DO-178C/ED-12C, DO-254, ARP4754A, ISO 26262, EN 50128) ont été écrites avant la maturité du ML et couvrent mal ses spécificités (§2.3.3.1). Deux différences de fond sont posées d'emblée : les algorithmes de ML sont fondamentalement stochastiques alors que les solutions classiques sont (essentiellement) déterministes, et leur comportement est déterminé par les données plutôt que par des instructions (§1.2.2). Le livre blanc cherche à identifier les verrous de certification de systèmes embarquant du ML, dans l'aéronautique, le ferroviaire et l'automobile, pour l'apprentissage supervisé hors ligne uniquement (§1.3).

## Méthode

Document de position, sans expérience ni implémentation. Les auteurs définissent 8 « High-Level Properties » (auditability, data quality, explainability, maintainability, resilience, robustness, specifiability, verifiability ; §3.2) et les analysent par trois approches (§3.4) : analyse du processus de développement ML, analyse de similarité avec des techniques non-ML déjà certifiées (filtres de Kalman, WCET, processeurs COTS) et analyse « à rebours » (arbres de décision pour l'explicabilité, Reluplex/ACAS-Xu pour la preuvabilité). Ils en tirent 7 « main challenges » (§3.5, §4) : 1 évaluation probabiliste, 2 résilience, 3 spécifiabilité, 4 qualité et représentativité des données, 5 explicabilité, 6 robustesse, 7 vérifiabilité, chacun décliné en sous-défis numérotés (#1.1 à #7.7, §5). Un processus de développement simplifié en 10 étapes (Figure 9, §4.1) situe où chaque défi apparaît.

Idées techniques notables :
- Trois cas selon l'ordre de grandeur de l'incertitude du modèle par rapport au risque acceptable ; si elle est très supérieure, un moyen de mitigation indépendant du modèle est requis au niveau système (Table 4, §4.2.1).
- Fonction de perte asymétrique tenant compte de la gravité de l'erreur, avec l'exemple de la détection de piétons : non-détection catastrophique, fausse détection seulement « major » (§4.2.4.2).
- Résilience par surveillance à l'exécution (runtime assurance, architecture simplex, détection OOD, motifs d'activation de neurones, prédiction conforme pour calibrer les probabilités), redondance duplex/triplex et dissimilarité, difficile à obtenir pour le ML (§4.3.2, §4.3.3, §4.2.3.9).
- Représentativité des données définie par rapport à l'Operational Design Domain (ODD), méthodes d'échantillonnage, impossibilité de garantir a priori la représentativité pour des données non structurées comme les images (§4.5.3).
- Vérifiabilité : preuvabilité a priori (réseaux Lipschitz, monotones) et a posteriori (interprétation abstraite, Reluplex/SMT), test (neuron coverage, fuzzing, VERIFAI/SCENIC), validation multi-plateforme, carte sur un V-model (Figure 21, §4.8).

## Plateforme et implémentation

Sans objet : aucune implémentation, aucune plateforme, aucun code ni bitstream. Le document déclare explicitement hors périmètre l'implémentation (logicielle ou matérielle) des modèles, en citant seulement les effets du calcul flottant et le déterminisme des temps de réponse (§1.3). La partie implémentation du processus renvoie aux normes existantes et liste seulement les erreurs à surveiller : représentation incorrecte des poids sur la cible, ressources insuffisantes, dégradation de précision, réduction de la précision arithmétique (§4.1.8). La cybersécurité est hors périmètre (§1.3).

## Résultats

Pas de résultat expérimental ni de mesure matérielle. Les seuls chiffres sont des illustrations :
- Borne VC : pour δ ≈ 10^-5 avec VC = 10^5, il faudrait au moins environ 10^15 échantillons ; approche jugée théoriquement correcte mais impraticable (§4.2.4.3, Limitation 3).
- Conversion taux d'erreur du modèle vers taux de défaillance horaire : un obstacle par minute en ville et une erreur de 10^-3 donnent 6·10^-2 défaillances par heure (§4.2.4.4). Exemple pédagogique des auteurs, pas une mesure.
- Objectif de sûreté de référence : 10^-9 par heure de vol pour une fonction catastrophique (§4.2.1).
- Reluplex appliqué à un réseau de 8 couches de 300 neurones ; ACAS-Xu en 3 Mo contre 2 Go pour les tables (§3.4.3.2).
- Chute de précision de 3 à 15 % (CIFAR-10) et 11 à 14 % (ImageNet) sur de nouveaux jeux de test, rapportée d'après [120] (§4.7.3.3).

→ reportés dans `benchmarks.csv` : aucune ligne (document normatif/position, sans mesure matérielle ; `benchmarks: none`).

## Limites et critique

- Position paper : aucune validation empirique, aucun cas d'étude chiffré ; les recommandations ne sont pas testées. Les auteurs reconnaissent que le travail est en cours et que des « détails importants » sont laissés de côté (Abstract).
- Périmètre volontairement restreint : apprentissage supervisé hors ligne, pas d'apprentissage en ligne ni continu, pas de cybersécurité, implémentation matérielle non traitée (§1.3). Le lien avec le FPGA, la quantification et l'arithmétique embarquée n'est qu'effleuré (§4.1.8, §4.7.4, §4.8.2.3).
- Aucune ligne directrice actionnable : le texte formule des questions ouvertes (défis #1.1 à #7.7) plutôt que des moyens de conformité. Les initiatives citées (Overarching Properties de la FAA, Abstraction Layer de l'EASA) sont décrites comme insuffisantes en l'état (§2.3.3.2).
- Publié en 2021 : n'intègre ni les guidances EASA ultérieures ni ISO/PAS 8800 ni ISO/IEC TR 5469 (déduit de la date et de la bibliographie lue ; à vérifier).
- Certaines affirmations reposent sur des références non vérifiées ici (chiffres de Reluplex, [120], effet de la quantification sur la généralisation en note 54).
- Biais de composition : partenaires industriels aéronautique, ferroviaire, automobile ; aucun cas de vidéosurveillance industrielle ou de sécurité des personnes hors transport.

## Pertinence pour la thèse

Très forte pour le volet « certifiable » de l'intitulé de thèse : c'est un cadre de référence pour formuler les objectifs d'assurance d'un réseau de vision embarqué. Apports directs :
- Vocabulaire et structure de l'argumentaire (HLPs, 7 défis, processus en 10 étapes) réutilisables pour un pré-projet de thèse et pour situer les contributions FPGA.
- Piliers directement transposables au cas YOLO de détection de personnes : perte asymétrique (non-détection d'une personne bien plus grave qu'une fausse alerte, §4.2.4.2), ODD et représentativité des données (§4.5.3), surveillance OOD et architecture de sécurité avec moniteur classique autour d'un composant ML (§4.3.2, §4.3.3), prédiction conforme (§4.2.3.9), lien performance sur jeu de données vs taux de défaillance horaire (§4.2.4.4).
- Sur FPGA : arguments favorables non développés par le papier (déduit, non affirmé par les auteurs) : flux de calcul déterministe et temps de réponse bornés, redondance spatiale (TMR) et moniteurs matériels facilitant la dissimilarité ; à instruire dans d'autres sources.
- Le papier laisse ouverts : l'implémentation matérielle (quantification, préservation des propriétés prouvées après réduction de précision, §4.8.3.2), la fiabilité matérielle (SEU cités seulement comme erreur aléatoire, §4.2.2.2), l'apprentissage continu, et tout chiffrage sur un accélérateur réel.
- Contexte normatif utile : ISO 26262/SOTIF pour l'automobile, EN 50126/50128/50129 pour le ferroviaire, DO-178C/DO-254 et ARP4754A pour l'aéronautique ; l'IEC 61508 et l'ISO 13849 (secteur industriel) ne sont pas traitées.

## Gaps identifiés

- Aucune traduction des défis du livre blanc en exigences vérifiables sur cible FPGA (préservation de la robustesse/Lipschitz après quantification INT8 ou binaire ; §4.8.3.2 le pose sans réponse).
- Pas de traitement du cadre industriel générique IEC 61508 / ISO 13849 / IEC 62061 pour un réseau de vision protégeant des personnes.
- Pas de cas d'étude de détection de personnes (fonction « piéton » citée seulement comme exemple de spécification ambiguë, §4.4.2.1).
- Fiabilité matérielle (SEU, TMR, injection de fautes) et surveillance OOD implémentée sur FPGA : cités comme défis, aucune solution matérielle.
- Comment démontrer la dissimilarité et la couverture de test pour un détecteur (YOLO) plutôt qu'un classifieur : défis #2.2.2, #7.4 ouverts.

## Statut de lecture

Papier complet (fulltext.md lu intégralement, lignes 1 à 1633, y compris tables 1 à 3, synthèse des défis et glossaire ; la liste des références n'est pas présente dans le texte extrait). Extraction grobid ok, mais avec des pertes signalées : sections 2 et 3 non détectées (leur texte est rattaché à la section précédente), 3 figures sans légende ni corps, ligatures (« classi cation »), et quelques passages tronqués ou mélangés (début de §4.7.2, §4.8.1 « a priori provability » en partie manquant, paragraphes du §4.7.4 et de la conclusion insérés dans « Figures et tableaux »). Aucun chiffre de tableau de résultats n'est en jeu.
Ce qui suit est déduit et non affirmé par les auteurs : l'ensemble de la section « Pertinence » relative au FPGA, au cas YOLO, à IEC 61508/ISO 13849 et aux normes postérieures à 2021 ; l'absence d'ISO/PAS 8800 et d'ISO/IEC TR 5469 dans le document (constat sur le texte lu).
