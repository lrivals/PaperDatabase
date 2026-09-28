---
id: arxiv-2108.03694-event-driven-vision-control-uavs
fiche: done
date: 2026-09-28
---

# Event-driven Vision and Control for UAVs on a Neuromorphic Chip

Antonio Vitale, Alpha Renner, Celine Nauer, Davide Scaramuzza, Yulia Sandamirskaya, 2021, arXiv preprint. https://arxiv.org/abs/2108.03694
Type : preprint non relu par les pairs (version arXiv lue ; une version publiée n'est pas
indiquée dans `metadata.json`)

## Problème

Les caméras événementielles permettent un contrôle visuel très rapide des UAV (suivi d'un
motif à > 1000 °/s avec un calcul embarqué sur CPU, travail [8] de la même équipe, §I),
mais le traitement des événements reste fait sur CPU. Les auteurs veulent traiter le flux
DVS **directement sur une puce neuromorphique** (SNN sur Intel Loihi) pour gagner en
latence et en fréquence, et exploiter l'**apprentissage sur puce** pour adapter le
contrôleur en ligne (§I).

## Méthode

- **Perception** : transformée de Hough implémentée comme SNN à 5 couches sur Loihi
  (§II-B, Fig. 2) : événements DAVIS sous-échantillonnés par 4 (décalage de 2 bits sur le
  x86 embarqué du Loihi), couche cartésienne → couche (θ, r) par une matrice de poids
  binaire, lecture en θ (90 neurones, 2 °/neurone), nettoyage par inhibition, couche
  mémoire auto-excitatrice. Pas de temps de 50 µs, donc **mise à jour de l'état à 20 kHz**,
  moyenne glissante de 200 éléments pour revenir à 1 kHz. Le DVS est relié au Loihi par
  interface **AER directe**.
- **Contrôle** : PD sur le CPU hôte avec l'angle venant du Loihi ; ou, dans l'expérience
  d'adaptation, **PD en SNN** (populations de 361 neurones, codage par position) avec une
  voie d'adaptation par plasticité synaptique à 3 facteurs sur puce (§II-C, Fig. 3,
  Éq. 1-3). Lecture DMA de la sortie SNN : ≈ 1,5 ms → ≈ 0,05 ms (§II-C1).
- Baseline : même algorithme de Hough événementiel sur CPU (UP board), à 1 kHz, avec
  filtre de Kalman ([8], §II-B).

## Plateforme et implémentation

- **Intel Kapoho Bay** (2 puces Loihi, 256 neuro-cores, 262 144 neurones, jusqu'à 260 M
  synapses, 3 x86 embarqués), monté sur le **dual-copter contraint à 1 DDL** de [8]
  (§II-A1-2, Fig. 1).
- Hôte : UP board Intel Atom x5-Z8350 1,92 GHz, 4 GB, Ubuntu 18.04, ROS Kinetic, NxSDK
  0.9.9 (§II-A6). Caméra DAVIS 240C (240×180) ; contrôleur de vol Lumenier F4 AIO,
  commandes toutes les 1 ms (§II-A3-4).
- **Puissance : n/r.** Le papier invoque la faible consommation du neuromorphique
  (§I, §IV) sans aucune mesure.
- Code : non publié (aucun lien).

## Résultats

- Traitement visuel sur Loihi, des événements à l'angle estimé : **250 µs** (5 couches ×
  50 µs) (Fig. 2) ; fréquence d'estimation **20 kHz contre 1 kHz sur CPU** (§II-B,
  §III-A).
- Suivi d'horizon en rotation : avec l'estimation Loihi, suivi jusqu'à **1200 °/s** avec
  une erreur plus faible que la version CPU aux vitesses élevées (§III-A, Fig. 5 ; valeurs
  RMSE par vitesse n/r dans le texte) ; moins bon aux faibles vitesses (paramètres réglés
  pour la haute vitesse).
- Contrôle adaptatif (sans vision, entrée encodeur) (Table I) : sans charge, RMSE SNN
  6,9-13,9° contre CPU 6,9-11,5° ; **avec 125 g ajoutés**, SNN adaptatif 6,9-16,0° contre
  CPU non adaptatif 19,6-22,3° (erreur statique ~20° sans adaptation, §III-B).
- Latence de la plante motrice : 100-150 ms, qui sous-exploite la vitesse du SNN (§III-A).

→ reportés dans `benchmarks.csv` : 1 ligne — SNN de Hough sur Loihi (Kapoho Bay),
latence 0,25 ms (Fig. 2, `confidence: medium`). Les RMSE de contrôle (en degrés) n'entrent
pas dans les colonnes de précision en %, et la puissance n'est pas rapportée.

## Limites et critique

- **Aucune mesure de puissance** alors que l'argument central est l'efficacité énergétique
  du neuromorphique ; la Kapoho Bay et l'UP board ne sont pas mesurés.
- **Tâche visuelle minimale** : détection d'une ligne noir/blanc (Hough) sur un banc à
  1 DDL ; très loin de la détection d'objets. Le Loihi ne gère qu'une partie de la boucle :
  le PD « visuel » tourne sur CPU, et le PD en SNN n'est testé qu'avec l'encodeur, sans
  vision (§II-D).
- **Le gain de 20× en fréquence est sous-exploité** : la plante a 100-150 ms de retard
  (§III-A), et la commande reste envoyée à 1 kHz. L'avantage de bout en bout n'est pas
  chiffré (Fig. 4, pipeline de latence, n'a pas de valeurs dans le texte).
- **Comparaison non isolée** : gains de contrôle différents (K_P = 3000 / K_D = 900 sur
  CPU contre 2000 / 600 avec Loihi) et plages d'angle différentes (±180° contre ±90°)
  (§II-D).
- Le SNN adaptatif est **moins précis sans perturbation** (jusqu'à 13,9° contre 11,5°,
  Table I), attribué à la résolution de 360 valeurs.
- Loihi est une puce de recherche non commerciale ; la Kapoho Bay reste attachée à un hôte
  x86 (déduit : pas un système autonome de nano-drone).

## Pertinence pour la thèse

- Axe `nano-drone` (sous-thème neuromorphique) : **premier exemple revendiqué** d'une
  perception visuelle événementielle calculée sur puce neuromorphique dans une boucle de
  contrôle d'UAV (§IV). Donne un ordre de grandeur de latence de perception (250 µs) à
  comparer aux ms des pipelines CNN sur FPGA ou MCU.
- Axe `system-codesign` : illustre qu'une perception plus rapide ne sert que si la boucle
  (plante, bus, commande) suit — exactement le type de métrique système absente des
  papiers YOLO/FPGA.
- Laisse ouvert : la détection d'objets (petits drones, VisDrone) en SNN sur neuromorphique
  embarqué, avec puissance mesurée.

## Gaps identifiés

- **Neuromorphique sans puissance mesurée** : la promesse « low power » n'est pas
  quantifiée à bord. Comparaison Loihi vs FPGA vs MCU à tâche égale : absente.
- **Du Hough à la détection** : aucune tâche de détection d'objets en SNN sur puce dans une
  boucle de vol réelle (les auteurs visent place recognition et obstacle detection, §IV).
- **Latence de bout en bout** perception → actionneur non décomposée chiffrée.

## Statut de lecture

Papier complet (`fulltext.md` lu en entier, extraction GROBID `ok`). La section II n'a pas
été détectée comme titre (texte rattaché à l'introduction, sans perte apparente). **Fig. 4
(latences et fréquences du pipeline) et Fig. 5 (RMSE selon la vitesse) n'ont pas de
valeurs dans le texte** : seuls les chiffres cités dans le corps et la Table I sont connus.
Le papier est court (format workshop / lettre).

Ce qui suit est déduit et non affirmé par les auteurs :
- le fait que la Kapoho Bay ne constitue pas un système autonome embarquable sur nano-drone ;
- l'absence de publication relue (seul l'arXiv est référencé ici) ;
- la comparaison d'ordre de grandeur avec les pipelines CNN sur FPGA / MCU.
