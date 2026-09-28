---
id: arxiv-2301.01755-autonomous-drone-racing-survey
fiche: done
date: 2026-09-28
---

# Autonomous Drone Racing: A Survey

Drew Hanover, Antonio Loquercio, Leonard Bauersfeld, Angel Romero, Robert Penicka, Yunlong Song, Giovanni Cioffi, Elia Kaufmann, Davide Scaramuzza, 2023, IEEE Transactions on Robotics (T-RO), Vol. 40, 2024. https://doi.org/10.1109/TRO.2024.3400838
Type : article de journal (survey) ; v1 arXiv en 2023, publiée dans T-RO en 2024.

## Problème

Premier survey dédié à la course de drones autonome, selon les auteurs (§I-A). La course
sert de proxy à la navigation rapide : franchir une suite de portes en temps minimal, avec
capteurs et calcul **embarqués**, à plus de 80 km/h et 4 g (Abstract). Le verrou est
système : perception, estimation d'état, planification et contrôle doivent tous tenir des
échéances de quelques dizaines de ms sur une plateforme de calcul limitée (§I-A).

## Méthode

Survey, sans expérience propre. Organisation :
- modélisation du drone : cinématique, aérodynamique (BEM, modèles hybrides appris),
  moteurs et batterie (modèles OTC, décharges > 100 A), caméra et IMU (§II) ;
- pipeline classique perception / planification / contrôle (§III, Fig. 3) : VIO
  (filtrage MSCKF contre lissage à fenêtre glissante), VIO + détection de portes + PnP pour
  corriger la dérive, planification (polynomiale, optimisation, recherche, échantillonnage),
  contrôle (platitude différentielle, INDI, NMPC, MPCC, perception-aware) ;
- approches apprises, classées en cinq architectures (Fig. 5 à 9) : perception apprise,
  perception + planification, contrôle appris (RL), planification + contrôle
  (optimiseurs différentiables), bout-en-bout (§IV) ;
- simulateurs (RotorS, AirSim, FlightGoggles, Flightmare, Aerial Gym ; §V), compétitions
  (IROS ADR 2016-2019, AlphaPilot 2019, Game of Drones 2019, Swiss Drone Days 2022 ; §VI),
  jeux de données, code ouvert et matériel (§VII), défis ouverts (§VIII).

## Plateforme et implémentation

Pas d'implémentation propre. Sur le matériel (§VII-C), les auteurs affirment que la famille
NVIDIA Jetson est « the smallest off-the-shelf hardware with sufficient compute to run
complex neural networks », ce qui fixe des châssis de 6 pouces. Moteurs > 500 W pour 50 g,
> 2 kW à plein gaz pour l'ensemble, batteries LiPo 120 C (§VII-C1). Contrôleur bas niveau
Betaflight plutôt que PX4 (§VII-C1). Aucune mention de FPGA, de MCU ou d'ASIC comme calculateur
de bord. Puissance du calculateur : n/r. La Table I (dépôts de code ouvert) n'est pas dans
le texte extrait.

## Résultats

Repères historiques repris des travaux cités (non mesurés par les auteurs) :

| Événement / travail | Résultat | Source |
|---|---|---|
| IROS ADR 2016 (KAIST, 1er) | 10 portes sur 26 en 1 min 26 s ; ≈ 0,6 m/s | §VI, Abstract/Fig. 2 |
| IROS ADR 2017 (INAOE, 1er) | 9 portes sur 13 en plus de 3 min ; 0,7 m/s | §VI, Fig. 2 |
| AlphaPilot 2019 | MAVLab (TU Delft) 11 s, UZH-RPG 15 s, pilote humain 6 s | §VI |
| Swiss Drone Days 2022 (UZH) | > 100 km/h, victoire possible sans motion capture | §VI |
| INDI + platitude [127] | ≈ 13 m/s, > 2 g | §III-C1 |
| INDI-NMPC [125], NMPC adaptatif [124] | ≈ 20 m/s, > 4 g | §III-C1 |
| NMPC + GP [40] | tourne à bord d'une Jetson TX2 (latence n/r) | §III-C1 |

→ reportés dans `benchmarks.csv` : aucune ligne. C'est un survey sans chiffre de détection
ni de calcul embarqué propre : ses chiffres sont des vitesses de vol tirées des travaux
cités, à ficher à la source.

## Limites et critique

- **Aucun chiffre de calcul embarqué.** Ni latence, ni puissance, ni fréquence d'inférence
  des détecteurs de portes ne sont compilées ; le coût de calcul est invoqué
  qualitativement (« high computational costs », §III-A3, §IV-A) sans être quantifié.
- **Gamme de puissance unique : Jetson (~10 W).** L'affirmation selon laquelle la Jetson
  serait le plus petit matériel suffisant (§VII-C1) ignore les nano-drones (GAP8), pourtant
  cités via le challenge IMAV 2022 Nanocopter [162] (§IV-B). Pas de discussion FPGA.
- **Survey écrit par le groupe dominant du domaine (UZH-RPG).** Une large part des travaux
  cités et des résultats de pointe (Swift [5], [36], [65], [122]) sont les leurs ; le biais
  de sélection est possible (déduit).
- **Performances « superhumaines » en conditions contrôlées** : les auteurs le disent
  eux-mêmes (§I-A, §VIII-D) ; la sécurité et la généralisation restent ouvertes.
- La Table I (code ouvert) manque dans l'extraction, donc la liste des dépôts n'a pas pu
  être vérifiée.

## Pertinence pour la thèse

- **Axe `tracking-navigation` et `system-codesign`** : ce survey donne le cadre
  vitesse ↔ latence ↔ calcul embarqué qui manque aux papiers YOLO/FPGA. La course illustre
  que la vitesse de vol sûre est bornée par la latence de perception, et que la taille du
  drone est bornée par la taille du calculateur (§VII-C1).
- **La détection (portes, adversaires) y est un sous-problème** : réseaux légers
  GateNet [155], PencilNet [156], détecteur YOLO sur caméra événementielle [158]. Ce sont des
  références pour une détection embarquée à haute fréquence.
- **Défi « Multiplayer racing » (§VIII-C)** : détecter et suivre un adversaire depuis la
  caméra embarquée, c'est un cas **air → air**, proche du contre-drone embarqué.
- Il ne traite ni de quantification, ni de FPGA, ni de consommation du calcul.

## Gaps identifiés

- **Métriques système absentes côté accélérateur, et métriques d'accélérateur absentes côté
  navigation** : le survey relie vitesse et calcul qualitativement mais ne donne aucune
  latence ou puissance mesurée. Cela conforte l'hypothèse « aucune métrique système dans les
  papiers YOLO/FPGA » vue de l'autre côté.
- **Calculateur de bord au-delà de la Jetson** : FPGA et ASIC ne sont pas discutés comme
  moyens de réduire la taille et la masse d'un drone de course (déduit de §VII-C1).
- **Caméras événementielles en course** : « applications of event cameras in drone racing
  tasks are yet to be explored » (§III-A2).
- **Détection d'adversaires air → air à haute vitesse** : identifié comme ouvert (§VIII-C).

## Statut de lecture

Papier complet (`fulltext.md` lu en entier, extraction GROBID `ok`). La Table I (dépôts de
code ouvert) et le contenu des figures (Fig. 2 et 4 : historique des compétitions et vitesses
maximales) ne sont pas dans le texte extrait. La section III n'a pas été détectée comme titre :
son introduction est rattachée à la fin de §II-D.

Ce qui suit est déduit et non affirmé par les auteurs :
- le biais de sélection possible lié au groupe auteur ;
- l'absence de FPGA/ASIC comme lacune pour la miniaturisation ;
- le rapprochement entre « multiplayer racing » et contre-drone air → air.
