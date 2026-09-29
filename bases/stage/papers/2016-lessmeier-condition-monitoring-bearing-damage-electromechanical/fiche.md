---
id: 2016-lessmeier-condition-monitoring-bearing-damage-electromechanical
fiche: done
date: 2026-09-29
benchmarks: none
---

# Condition Monitoring of Bearing Damage in Electromechanical Drive Systems by Using Motor Current Signals of Electric Motors: A Benchmark Data Set for Data-Driven Classification

Christian Lessmeier, James Kuria Kimotho, Detmar Zimmer, Walter Sextro, 2016, Proceedings of the European Conference of the PHM Society. https://doi.org/10.36001/phme.2016.v3i1.1577
Type : conférence (PHM Europe 2016) — article de jeu de données (dit « Paderborn »)

## Problème

Surveiller les roulements par le **courant moteur** (déjà mesuré par le variateur) éviterait
d'ajouter des accéléromètres sur les petits entraînements (≈ 1 kW). Mais les roulements
**externes** au moteur laissent une signature faible, noyée dans le bruit du procédé, et les
données publiques existantes (CWRU, FEMTO, MFPT, IMS) sont vibratoires et souvent à défauts
artificiels (§1).

## Méthode

Ce que l'article **définit** :

- **Grille de description des dommages** (Table 1) : informations générales, données constructeur
  (géométrie), informations d'application (conditions, durée de vie) et dommage (mode selon
  ISO 15243, localisation, combinaison simple / répétée / multiple, géométrie, **niveau d'étendue 1 à
  5** selon la longueur rapportée à la circonférence primitive, Table 2 ; ponctuel vs distribué)
  (§2).
- **Génération des dommages** sur des roulements à billes 6203 (FAG, MTK, IBU/IBB) (§3) :
  - **artificiels** : électroérosion, perçage (0,9 à 3 mm), gravure électrique manuelle (1 à 4 mm)
    (Tables 3-4) ;
  - **réels** par essais de vie accélérés : 108 roulements testés, 33 dommages sur 18 roulements
    (≈ 70 % de piqûres de fatigue, le reste des indentations par particules) (§3.2, Table 5).
- **Banc modulaire** (Université de Paderborn) : moteur PMSM de 425 W sur variateur industriel (16 kHz
  de découpage), arbre de mesure de couple, module de roulement, volant d'inertie, moteur de charge
  (§4.1). **Courants de phase à 64 kHz** (filtre 25 kHz) et **vibration du palier à 64 kHz**,
  synchronisés ; force radiale, couple, vitesse et température d'huile à cadence plus faible.
- **Quatre conditions opératoires** : 1500 tr/min, 0,7 N·m, 1000 N (référence) puis une variable
  réduite à la fois (900 tr/min ; 0,1 N·m ; 400 N) ; 20 mesures de 4 s par condition (Table 6).
- **Jeu publié** : 32 roulements = 6 sains, 12 à dommages artificiels, 14 à dommages réels ; fichiers
  Matlab nommés par condition et code roulement (N15_M07_F10_KA01_1.mat) ; licence CC BY-NC 4.0 ;
  portail KAt-DataCenter (§5).
- Validation des données par analyse d'enveloppe des vibrations (fréquences de passage des billes
  visibles) (§6) ; puis classification 3 classes (sain, bague extérieure, bague intérieure) avec
  CART, RF, arbres boostés, réseau de neurones, SVM-PSO, ELM, kNN et un ensemble (§7).

## Plateforme et implémentation

Banc physique ; features (23 par signal : ondelettes, FFT, PSD) et classifieurs hors ligne (§7.1).

## Résultats

Classification, pour situer la difficulté du jeu (pas de ligne dans `benchmarks.csv`, conformément
au profil pour les papiers de jeux de données, `benchmarks: none`) :
- **Apprentissage sur défauts artificiels, test sur défauts réels** : 26,8 à 60,9 % avec le courant
  (meilleur : SVM-PSO), 62,3 à 75,0 % avec les vibrations (Table 9) → les défauts artificiels ne
  suffisent pas à reconnaître les défauts réels.
- **Apprentissage et test sur défauts réels** (validation croisée par roulement) : ensemble 93,3 %
  (courant) et 98,3 % (vibrations) (Table 11).
- Avec les roulements à **dommages multiples** : 86,3 % (courant) et 91,3 % (vibrations) pour
  l'ensemble (Table 13).
- Les vibrations restent meilleures que le courant dans tous les cas (§7.5).

## Limites et critique

- Pas de run-to-failure : ce sont des états figés (roulements sains ou endommagés), donc un jeu de
  **diagnostic**, pas de pronostic RUL.
- Mesures de 4 s en conditions constantes ; les conditions variables sont laissées en perspective
  (§8).
- Petit nombre de roulements par classe (5 roulements réels par classe dans la validation croisée) :
  risque de résultats dépendants du découpage.
- Incohérences texte/tableaux : le texte donne 93,3 % pour RF et l'ensemble (courant) alors que la
  Table 11 donne RF 83,3 %, et 98,5 % au lieu de 98,3 % pour les vibrations.
- Seuls deux modes de dommage sur les six de l'ISO 15243 sont couverts (§8).

## Pertinence pour la thèse

Article de référence du jeu **Paderborn (KAt)**, cité dans la bibliographie du stage pour le
diagnostic de roulements. Il apporte deux éléments utiles au CL : (1) l'écart artificiel → réel
(≈ 30 points de précision) est une **dérive de domaine** mesurée, qui motive l'adaptation sur le
terrain ; (2) les quatre conditions opératoires forment un découpage naturel en tâches pour un
scénario domain-incremental (déduit). Le courant moteur à 64 kHz est aussi un signal réaliste pour
un diagnostic embarqué sans capteur ajouté (déduit).

## Gaps identifiés

- Adaptation du diagnostic de défauts artificiels vers réels (dérive de domaine) : non traitée.
- CL entre conditions opératoires sur le jeu Paderborn : pas de protocole standard.
- Conditions variables en cours de mesure : non couvertes (§8).

## Statut de lecture

Papier complet (`fulltext.md` lu en entier). Tables 1, 3 et 10 reconstruites par PyMuPDF (et en
double) ; Table 7 désalignée ; §7.3 fusionnée avec la légende de la Table 11 ; figures non
disponibles (matrices de confusion lues en texte).
Déduit et non affirmé par les auteurs : lecture de l'écart artificiel/réel comme dérive de domaine,
découpage en tâches, usage embarqué du courant.
