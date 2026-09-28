---
id: 2019-suleiman-navion-2-mw-fully-integrated
fiche: done
date: 2026-09-28
---

# Navion: A 2-mW Fully Integrated Real-Time Visual-Inertial Odometry Accelerator for Autonomous Navigation of Nano Drones

Amr Suleiman, Zhengdong Zhang, Luca Carlone, Sertac Karaman, Vivienne Sze, 2019, IEEE Journal of Solid-State Circuits 54(4), 1106-1119. https://doi.org/10.1109/JSSC.2018.2886342
Type : article de journal

## Problème

Les algorithmes de visual-inertial odometry (VIO) demandent des CPU ou GPU puissants ; un
nano/pico-drone dispose d'environ 100 mW pour tout le vol stable, soit un ordre de grandeur
de moins qu'un CPU embarqué (§I). Le plus petit drone commercial avec VIO cité (Qualcomm,
250 g) utilise un Snapdragon 801 d'environ 3 W (§I). Les accélérateurs existants simplifient
le problème (marqueurs), dépendent de mémoire hors puce ou ne couvrent qu'une partie du
pipeline (§I). Les auteurs visent la **première VIO complète intégrée sur ASIC**, sans DRAM
externe.

## Méthode

- **Algorithme** : VIO à keyframes (KF), préintégration IMU, back-end par optimisation de
  graphe de facteurs (lissage à horizon glissant, Gauss-Newton sur variété, une seule
  itération) (§II, d'après [9], [23]). Front-end vision : suivi Lucas-Kanade pyramidal,
  coins Shi-Tomasi, rectification, appariement stéréo, RANSAC 2 points / 1 point aidé par
  le gyroscope (§II-A). Mono ou stéréo.
- **Paramètres max** : horizon de 20 KF, 200 points suivis par image, âge de piste 10,
  > 4000 facteurs (§II-D). Plus de 250 paramètres programmables (§III).
- **Co-design mémoire** (§IV) : compression d'image (troncature à 5 bits puis quantification
  par blocs 4×4 à 1 bit/pixel : mémoire d'image ÷4,4, puissance ÷4,9, §IV-A) ; mémoire à deux
  étages par pointeurs pour la parcimonie non structurée des pistes (÷5,4, §IV-B) ;
  parcimonie structurée fixe de la hessienne (÷5,2 en mémoire, solveur ×7,2 plus rapide à
  20 KF, back-end ×2,5, §IV-C) ; replanification et parallélisme du front-end (−43 à −55 %
  de temps VFE, §IV-D). Gain mémoire global ×4,1 (§V-A).
- **Arithmétique** : virgule fixe dans le front-end vision, **double précision** dans le
  back-end et l'IMU, la simple précision étant jugée numériquement insuffisante (§III-C).
- Prototype FPGA antérieur [21] ; ce papier en est la version ASIC (§I).

## Plateforme et implémentation

- ASIC **65 nm CMOS**, 2 M portes NAND2 équivalentes, **854 ko de SRAM** sur puce, deux
  domaines d'horloge (§V-A) ; 62,5 MHz (VFE) et 83,3 MHz (BE) en configuration maximale
  (légende Fig. 12). La SRAM occupe 77 % de la surface mais 21 % de la puissance (§V-A).
- Entrées : images 752×480 sur deux bus 8 bits, IMU sur un bus 32 bits (§III-A, §III-B).
- Démonstrateur : carte de test + Xilinx ZC706 qui envoie les données et lit les sorties
  (§V-B). **Pas de vol à bord d'un drone** rapporté.
- **Puissance** : puissance moyenne de la puce à 1 V d'alimentation (§V-A, §V-D) ; le
  dispositif de mesure n'est pas décrit plus avant. Les puissances CPU de comparaison sont
  la puissance moyenne de calcul, sans repos ni DRAM (§V-C).
- Code, RTL : non publiés ; une vidéo de démonstration est sur le site du projet [38].

## Résultats

| Configuration | Débit | Puissance | Précision | Source |
|---|---|---|---|---|
| Paramètres max, 1 V | 28 à 171 fps (suivi), 16 à 90 fps (KF), IMU jusqu'à 52 kHz | 24 mW moyen | erreur de trajectoire normalisée 0,28 % (contre 0,22 % en logiciel) | §V-A, §V-C |
| Adaptée à chaque séquence, débit fixe 20 fps | 20 fps | **2 mW moyen** | cible ≤ 0,35 % par séquence | §V-D, Abstract |

- Énergie **684× inférieure** à un ARM Cortex-A15 et **1582×** à un Intel Xeon E5-2667 (même
  configuration, §V-C). Les chiffres détaillés sont dans la Table III, non extraite.
- L'adaptation des paramètres à l'environnement réduit l'énergie de 2,5× en moyenne, à
  erreur moyenne égale (§V-D, Fig. 16).
- Erreur : +6,27 cm sur un vol moyen de 83 m (EuRoC), due à la compression d'image et à la
  virgule fixe (§V-C).

→ reportés dans `benchmarks.csv` : **2 lignes** (configuration maximale et configuration
adaptée à 20 fps), `task = visual-inertial odometry`, `power_scope = chip`,
`confidence = medium` (chiffres lus dans le texte, Tables III et V non extraites).

## Limites et critique

- **Pas de vol réel** : les 2 mW sont obtenus sur EuRoC rejoué depuis un ZC706 (§V-B,
  §V-D). La puissance des caméras, de l'IMU et des E/S n'est pas comptée.
- **Les 2 mW supposent une configuration optimisée par séquence** a posteriori, pour une
  cible d'erreur fixée (§V-D) : aucun mécanisme n'est décrit pour choisir ces paramètres en
  ligne pendant le vol.
- **Comparaison CPU favorable** : les CPU tournent le logiciel de référence, pas une version
  optimisée ; les chiffres par séquence sont dans la Table III manquante. Pas de comparaison
  avec un GPU embarqué (Jetson) ni avec un MCU (déduit).
- **La plage 28-171 fps** dépend de la séquence ; aucune latence par image n'est donnée.
- Ce n'est pas de la détection d'objets : la VIO est une brique de navigation.

## Pertinence pour la thèse

- **Axe `nano-drone` et `tracking-navigation`, gamme de puissance nano (mW)** : la
  référence ASIC pour la navigation embarquée des nano-drones. Elle montre qu'une tâche de
  vision complète tient dans 2 à 24 mW si l'algorithme et la mémoire sont co-conçus.
- **Méthode de co-design transposable à un détecteur** : tout sur puce, sans DRAM ;
  compression des tampons d'image ; exploitation de la parcimonie ; paramètres
  programmables pour échanger précision, débit et énergie selon la scène (§IV, §V-D).
- **Budget de référence** : ≈ 100 mW pour le vol stable d'un nano-drone (§I, d'après [13]),
  utile pour situer un accélérateur de détection dans le budget énergétique du vol.
- Il laisse ouverte la question de la perception sémantique (détection) dans le même budget.

## Gaps identifiés

- **Détection d'objets + VIO sur un même budget nano** : Navion ne traite que la
  localisation ; aucun papier du lot ne montre les deux dans quelques dizaines de mW (à
  vérifier dans le corpus).
- **Adaptation en ligne de la configuration** selon la scène : les 2,5× d'énergie gagnés
  supposent un choix hors ligne (§V-D).
- **Validation en vol absente** : pas de mesure système (autonomie, vitesse) avec la puce
  embarquée.

## Statut de lecture

Papier complet (`fulltext.md` lu en entier, extraction GROBID `ok`). Les **Tables I à V
n'ont pas de corps extrait** (légendes seules, cf. `extraction.warnings`) : tailles mémoire
avant/après (Table I), paramètres (Table II), comparaison CPU par séquence (Table III),
paramètres adaptés (Table IV), débit, fréquences et puissances par mode (Table V). Les
chiffres ci-dessus viennent uniquement du texte. Quelques passages sont mal ordonnés par
l'extraction (§II-A, §III-B), sans perte apparente.

Ce qui suit est déduit et non affirmé par les auteurs :
- `power_scope = chip` : puissance de la puce à 1 V, méthode de mesure non détaillée ;
- l'absence de comparaison avec Jetson ou MCU comme limite ;
- le gap « détection + VIO dans un budget nano ».
