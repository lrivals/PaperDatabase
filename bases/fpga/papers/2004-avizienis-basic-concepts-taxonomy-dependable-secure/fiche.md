---
id: 2004-avizienis-basic-concepts-taxonomy-dependable-secure
fiche: done
date: 2026-11-03
benchmarks: none
---

# Basic concepts and taxonomy of dependable and secure computing

A. Avizienis, J.-C. Laprie, B. Randell, C. Landwehr, 2004, IEEE Transactions on Dependable and Secure Computing 1(1), 11–33. https://doi.org/10.1109/tdsc.2004.2
Type : article de journal (IEEE TDSC). Attention : le PDF ingéré est la version rapport technique de l'ISR (University of Maryland), pas la version publiée ; les métadonnées (venue, pagination, DOI) sont celles de l'article IEEE. Le texte peut différer de la version éditée (non vérifié).

## Problème

Les communautés de la sûreté de fonctionnement (*dependability*) et de la sécurité (*security*) emploient des termes proches avec des sens divergents (« systems in which there are uncertainties about system boundaries », §1). Les auteurs veulent documenter un « minimum consensus » de concepts, utilisable par les organismes de normalisation et pour l'enseignement (§1). Il ne s'agit pas d'un état de l'art ni d'implémentation : les normes (IEC 61508 pour la sûreté, ISO/IEC 15408 pour la sécurité) sont citées mais explicitement hors sujet (§1). Les mesures quantitatives de sûreté de fonctionnement sont signalées comme non consensuelles (§1).

## Méthode

Article conceptuel : définitions et classifications, sans expérience.

- **Chaîne fondamentale (§2.2, §3.5)** : une *faute* (cause adjugée ou supposée) est dormante ou active ; activée, elle produit une *erreur* (partie de l'état total qui peut conduire à une défaillance) ; l'erreur se propage et, si elle atteint l'interface de service, provoque une *défaillance de service* (écart par rapport au service correct). Beaucoup d'erreurs n'atteignent pas l'état externe (§2.2, §3.4) : la redondance, volontaire ou non, et le comportement du système (état écrasé, jamais utilisé) décident si une erreur devient défaillance (§3.4).
- **Attributs (§2.3)** : disponibilité (*availability*), fiabilité (*reliability*, continuité du service correct), sûreté-innocuité (*safety*, absence de conséquences catastrophiques), intégrité, maintenabilité ; confidentialité en plus pour la sécurité. Deux définitions de la dependability : « capacité à délivrer un service auquel on peut justifiablement faire confiance » et « capacité à éviter des défaillances plus fréquentes ou plus sévères que l'acceptable » (§2.3, §4.1). Une défaillance de dependability est donc relative à une spécification (§3.3.3).
- **Moyens (§2.4, §5)** : prévention, tolérance, élimination (vérification, diagnostic, correction ; injection de fautes pour tester les mécanismes de tolérance, §5.3.1), prévision des fautes. Tolérance = détection d'erreur + recouvrement (reprise arrière/avant, compensation, masquage), §5.2.1.
- **Taxonomie des fautes (§3.2)** : huit points de vue élémentaires (phase, frontière du système, cause phénoménologique, dimension, objectif, intention, capacité, persistance), 31 combinaisons plausibles regroupées en fautes de développement, physiques et d'interaction (§3.2.1). Fautes naturelles (#11-#15) : défauts de production, détérioration interne, interférences externes (rayonnement, transitoires d'alimentation, §3.2.2).
- **Taxonomie des défaillances (§3.3.1)** : quatre points de vue : domaine (contenu / temporel ; arrêt, silence, erratique), détectabilité (signalée / non signalée ; les détecteurs ont deux modes de défaillance : fausse alarme et défaillance non signalée), cohérence (cohérente / byzantine), conséquences (gravité, de mineure à catastrophique). Notion de système *fail-controlled* (défaillances limitées à des modes spécifiés, ex. arrêt plutôt qu'erratique).

## Plateforme et implémentation

Sans objet (article conceptuel, aucun matériel ni code). Le §3.2.2 cite néanmoins les fautes physiques naturelles externes (rayonnement) et le §3.2.3 les errata matériels et composants sur étagère (OTS) comme sources de fautes de développement.

## Résultats

Pas de résultat chiffré : l'apport est la structure conceptuelle (arbre « dependability and security tree », Fig. 2 ; fautes Fig. 3.3 ; modes de défaillance Fig. 3.6-3.7 ; chaîne faute-erreur-défaillance Fig. 3.9). Nouveautés revendiquées en §1 : lien dependability/security clarifié, définition quantitative de la dependability, critère de capacité (incompétence) pour les fautes humaines, distinction défaillance de service / défaillance de dependability, prise en compte du processus de développement, lien avec dependence et trust. Le §4.4 conclut que *high confidence*, *survivability* et *trustworthiness* sont « essentiellement équivalents » à la dependability dans leurs buts.
→ reportés dans `benchmarks.csv` : aucune ligne (`benchmarks: none`) ; article conceptuel, aucune mesure ni plateforme.

## Limites et critique

- Aucune validation empirique ; le cadre n'est pas opérationnalisé en procédure d'analyse (HAZOP, FMEA, arbres de fautes absents).
- Le texte ne traite ni apprentissage automatique, ni fautes de spécification d'un modèle appris, ni dérive de distribution : ce sont des extensions à faire (déduit). L'idée que la spécification elle-même peut être fautive (§2.2, §3.3.3) est la porte d'entrée la plus utile.
- Mesures de dependability explicitement laissées ouvertes (§1) ; sécurité et confidentialité peu traitées (§1).
- Rapport technique et non version éditée : écarts éventuels avec IEEE TDSC non contrôlés.
- Fig. 3.3 (31 classes) est une image : seul le texte l'accompagnant a été lu, non la figure.

## Pertinence pour la thèse

Axe `safety-certification` (cœur du sujet). L'article fournit le vocabulaire commun pour distinguer ce que le sujet ARCYS veut séparer :

- **Défaillance d'un détecteur de personnes** : une personne non détectée est une défaillance de service de type contenu (domaine), éventuellement non signalée (détectabilité), potentiellement catastrophique (conséquences) ; sa gravité fixe l'exigence. Le « faux négatif critique » se classe dans ces modes. L'**erreur** est l'état interne erroné (activations, boîte englobante ratée) ; la **faute** est la cause (donnée d'entraînement manquante, écart de domaine, spécification d'ODD incomplète : faute de développement/spécification, §3.2.1, §3.3.3).
- **Erreur de perception, anomalie d'exécution, défaillance temporelle** : correspondent respectivement à une erreur de contenu, à une erreur latente ou une faute d'exécution, et à une défaillance de type timing (§3.3.1, trop tôt ou trop tard), distinction que la problématique ARCYS réclame.
- **Fautes matérielles SEU sur FPGA** : un SEU est une faute naturelle externe (rayonnement, #14-#15, §3.2.2), transitoire (persistance, §3.2.1) ; elle est dormante tant qu'elle ne change pas un bit utile (activation, §3.5), et le bit de configuration ou de poids touché peut être masqué par la structure (§3.4) : base conceptuelle du taux de SDC et de l'injection de fautes (§5.3.1 : injection de fautes = test avec fautes dans les motifs de test).
- **Moniteurs et tolérance aux fautes** : un moniteur d'exécution est un mécanisme de détection d'erreur (§5.2.1) ; ses deux modes de défaillance, fausse alarme et défaillance non signalée (§3.3.1), correspondent aux faux positifs/négatifs du moniteur et exigent une couverture (*coverage*) chiffrée (§5.2.2). La récursivité de la tolérance (le mécanisme doit être protégé, §5.2.2) s'applique au moniteur lui-même. Sorties anticipées et abstention = service dégradé / arrêt contrôlé (*fail-controlled*, état sûr, §3.3.1).
- **Redondance sélective, TMR** : redondance protectrice versus non intentionnelle (§3.4), masquage par compensation (§5.2.1), mode commun (§3.5).
- **Certification** : la dependability comme « confiance justifiée » (§2.3) et l'évaluation par le processus de développement quand la preuve probabiliste est impossible (§5.4, cite RTCA/EUROCAE, ISO/IEC) rejoignent la logique d'assurance (EASA, ARP6983). Le *safety* au sens thèse = l'attribut safety ici ; la *security* reste secondaire.

Laisse ouvert : transposer fautes/erreurs/défaillances à un réseau appris (qu'est-ce qu'une « faute » de réseau ?), et quantifier la couverture d'un moniteur.

## Gaps identifiés

- Pas de taxonomie fautes/erreurs/défaillances adaptée aux DNN de vision embarqués (faute de données, d'ODD, de quantification) dans la base ; à construire en s'appuyant sur ce vocabulaire.
- Pas de mesure de couverture (*coverage*) d'un moniteur de perception, ni de classement de ses fausses alarmes et défaillances non signalées selon cette grille.

## Statut de lecture

Papier complet (`fulltext.md` lu en entier, extraction GROBID ok). Figures (arbre, Fig. 3.3, 3.6-3.9) non lues : seul leur texte associé l'a été. Version rapport technique ISR, non l'article IEEE publié.
Ce qui suit est déduit et non affirmé par les auteurs : tout le mappage vers le détecteur de personnes, le SEU sur FPGA, les moniteurs d'exécution et le faux négatif critique ; l'assimilation du moniteur à un mécanisme de détection d'erreur ; l'absence de ML dans le texte (relevée par lecture, sans recherche exhaustive).
