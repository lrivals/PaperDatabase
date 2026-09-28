---
id: 2023-kaufmann-champion-level-drone-racing-deep
fiche: done
date: 2026-09-28
---

# Champion-level drone racing using deep reinforcement learning

Elia Kaufmann, Leonard Bauersfeld, Antonio Loquercio, Matthias Müller, Vladlen Koltun, Davide Scaramuzza, 2023, Nature 620(7976), 982-987. https://doi.org/10.1038/s41586-023-06419-4
Type : article de journal (Nature, open access CC BY 4.0)

## Problème

Atteindre le niveau des champions humains de course FPV avec un drone autonome qui n'utilise
**que ses capteurs et son calcul embarqués** (Abstract). Les systèmes antérieurs proches du
niveau expert s'appuyaient sur une capture de mouvement externe, ce que les auteurs jugent
injuste face à des pilotes qui ne voient que la caméra embarquée (introduction). Le verrou
est double : perception bruitée à très haute vitesse (flou, dérive de la VIO) et dynamique
mal modélisée (Methods, « Simulation results »).

## Méthode

Système **Swift**, en deux modules (Fig. 2) :
- **Politique d'observation** :
  - VIO de la caméra Intel RealSense T265 (100 Hz) ;
  - un **détecteur de coins de portes**, un U-Net à 6 niveaux avec (8, 16, 16, 16, 16, 16)
    filtres et des noyaux de 3 à 7 (Methods, « Gate detection ») ;
  - une estimation de pose par IPPE sur la carte connue de la piste ;
  - un filtre de Kalman qui corrige la dérive de translation de la VIO (Methods,
    « VIO drift estimation »).
- **Politique de contrôle** : un MLP à deux couches cachées de 128 neurones, qui produit la
  poussée collective et les vitesses angulaires. Il est entraîné par PPO en simulation, avec
  une récompense qui combine la progression vers la porte suivante et le maintien de cette
  porte dans le champ de la caméra (perception-aware) (Methods, « Policy training »).
- **Transfert simulation → réel** : des résidus empiriques identifiés sur environ 50 s de vol
  réel (trois tours). Les résidus d'observation sont modélisés par des processus gaussiens,
  ceux de dynamique par des k-NN (k = 5), puis la politique est affinée en simulation
  augmentée (Methods, « Residual model identification »).
- Coût d'entraînement : 10⁸ interactions en 50 min sur une station i9-12900K + RTX 3090
  (Methods).

## Plateforme et implémentation

- **Drone** : 870 g, poussée statique d'environ 35 N (rapport poussée/poids 4,1), châssis
  6″, cadre Agilicious. Même masse et même propulsion que les drones humains, qui portent un
  lest à la place du Jetson et de la caméra (Methods, « Drone hardware configuration »).
- **Calcul** : NVIDIA Jetson TX2 sur carte Connect Tech Quasar. Contrôleur de vol STM32 à
  216 MHz sous Betaflight (Methods).
- **Détecteur de portes** : porté en TensorRT, FP16, entrée 384 × 384 en niveaux de gris,
  **40 ms par inférence** sur le GPU du TX2 (Methods, « Gate detection »).
- **Politique** : 8 ms par inférence sur le CPU du TX2 (Methods).
- **Latence sensorimotrice** : 40 ms pour Swift, contre 220 ms en moyenne pour un pilote
  expert. Caméra à 30 Hz, contre 120 Hz pour les humains (Discussion).
- Puissance du calcul embarqué : n/r. Consommation de la plateforme : les puissances moyennes
  tirées sont dans l'Extended Data Table 1d, absente du texte extrait.
- Code : « statements of data and code availability » renvoyés au site de l'éditeur (Online
  content). Lien non présent dans le texte extrait : n/r.

## Résultats

- **Courses face à face** (Fig. 3b) : Swift gagne 5 courses sur 9 contre A. Vanover, 4 sur 7
  contre T. Bitmatta et 6 sur 9 contre M. Schaepper (Results).
- **Causes des 10 défaites** : 40 % de collisions avec l'adversaire, 40 % de collisions avec
  une porte, 20 % de vitesse inférieure (Results).
- **Meilleur temps de course enregistré** : avance d'une demi-seconde sur le meilleur humain
  (Results). Écart d'environ 0,16 s sur un tour (Methods, « Fine-tuning for several
  iterations »).
- **Réaction au départ** : 120 ms plus tôt que les humains en moyenne (Results).
- **Statistiques** : plus de 300 tours par concurrent (Results). Moyenne et variance des
  temps plus faibles pour Swift (Fig. 3a).
- **Temps au tour absolus** : n/r dans le texte extrait (Fig. 3a et Extended Data Table 1
  non extraites).
- **Ablations en simulation** (Extended Data Table 1b-c, chiffres non extraits) : dans les
  réglages avec décalage de domaine, zero-shot, domain randomization et trajectoire
  time-optimal + MPC ne finissent aucun tour. Seul Swift termine dans tous les réglages.
- **Itérations de fine-tuning** : quasi sans effet. Écart de marge aux portes de
  0,09 ± 0,08 m et de temps au tour de 0,02 ± 0,02 s entre les politiques 1 et 2 (Methods).

→ reportés dans `benchmarks.csv` : 2 lignes.
- Détecteur de portes U-Net sur Jetson TX2, TensorRT FP16, 384 × 384, latence de 40 ms.
- Politique MLP sur le CPU du TX2, latence de 8 ms.
Précision et puissance valent n/r, confidence medium (texte des Methods).

## Limites et critique

- **Pas une contribution de vision embarquée au sens détection** : le seul réseau de vision
  est un petit U-Net de segmentation de coins. Sa précision n'est pas rapportée dans le texte
  extrait.
- **Environnement fixe et connu** : la carte de la piste sert à la localisation, et
  l'apparence doit rester celle de l'entraînement. Les auteurs reconnaissent l'échec possible
  si l'éclairage change, et l'absence de reprise après un crash (Discussion).
- **Données réelles avec capture de mouvement** : les résidus sont identifiés grâce à une
  capture de mouvement pendant la phase de collecte (Methods). Le système est donc
  « onboard » en course, mais pas dans sa préparation.
- **Comparaison avec les humains asymétrique**, dans les deux sens et de l'aveu des auteurs :
  la centrale inertielle et la latence de 40 ms avantagent Swift, la caméra 120 Hz avantage
  les humains (Discussion). S'y ajoute une semaine d'entraînement sur la même piste pour les
  deux.
- **Puissance du Jetson TX2 non mesurée** : gamme Jetson (environ 10 W, ordre de grandeur
  déduit, non rapporté ici) sur une plateforme de 870 g. Le coût énergétique du calcul face à
  la propulsion n'est pas discuté dans le texte extrait.
- **Tableaux étendus absents** de l'extraction : pas de lap times, pas de chiffres
  d'ablation.

## Pertinence pour la thèse

- **Référence de l'axe `tracking-navigation`** et exemple emblématique de la gamme **Jetson
  (environ 10 W)** du profil, avec les travaux de Zurich cités dans `CLAUDE.md`. C'est la
  borne haute « drone agile de moins de 1 kg » face aux nano-drones (GAP8, mW) et aux FPGA
  (W).
- **Métriques système réelles** : latence de bout en bout de 40 ms, bilan des budgets
  d'inférence (40 ms pour la vision, 8 ms pour le contrôle), et fréquence de caméra comme
  facteur limitant. C'est le type de métrique « latence → performance de vol » absente des
  papiers YOLO/FPGA.
- **La vision est le goulot** : 40 ms de détecteur contre 8 ms de politique, sur un réseau de
  seulement 16 filtres au plus. Cela donne un argument (déduit) pour accélérer la perception
  sur FPGA ou ASIC afin de monter en fréquence caméra (30 → 120 Hz).
- Laisse ouvert : détection d'objets génériques ou d'autres drones (contre-drone air → air) à
  cette vitesse, et coût énergétique du calcul.

## Gaps identifiés

- **Perception haute fréquence embarquée** : les auteurs identifient la caméra 30 Hz comme un
  désavantage structurel (Discussion). Aucune étude n'est connue sur le gain de performance de
  vol en passant la perception à 120 Hz avec un accélérateur dédié (FPGA, ASIC, event camera).
- **Coût énergétique et massique du calcul sur un drone agile** : non quantifié ici. À
  confronter au bilan du Crazyflie + GAP8 (arxiv-1805.01831, Table IV).
- **Robustesse de la perception aux changements d'apparence** : limite reconnue, sans
  évaluation.

## Statut de lecture

Papier complet (`fulltext.md` lu en entier, extraction GROBID `ok`). Les équations sont
illisibles dans l'extraction. Plusieurs éléments sont absents ou réduits à leur légende :
Fig. 3 et Fig. 4 (données non extraites), Extended Data Table 1 (temps au tour, puissance,
ablations) et Extended Data Fig. 1-2. Les chiffres de ces éléments manquent et n'ont pas été
reconstitués.

Ce qui suit est déduit et non affirmé par les auteurs :
- l'ordre de grandeur de puissance d'un Jetson TX2 ;
- le rôle de goulot de la vision (déduit du ratio 40 ms / 8 ms) ;
- l'intérêt d'un accélérateur de perception pour monter en fréquence ;
- le caractère non « onboard » de la phase de collecte des résidus (constat, pas une
  critique des auteurs).
