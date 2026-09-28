---
id: arxiv-2303.08778-fully-neuromorphic-vision-control-autonomous
fiche: done
date: 2026-09-28
---

# Fully neuromorphic vision and control for autonomous drone flight

Federico Paredes-Vallés, Jesse Hagenaars, Julien Dupeyroux, Stein Stroobants, Yingfu Xu, Guido de Croon, 2023, arXiv preprint. https://arxiv.org/abs/2303.08778
Type : preprint non relu par les pairs (une version publiée dans Science Robotics, 2024, est
probable mais n'a pas été vérifiée ici ; `metadata.json` reste en preprint)

## Problème

Les réseaux profonds de vision (flot optique, profondeur, détection) demandent un matériel
lourd et gourmand, hors de portée des petits drones (§1). Le couple caméra événementielle +
processeur neuromorphique promet une perception à faible latence et faible énergie. Mais
jusqu'ici, les démonstrations robotiques restaient limitées à des entrées de faible
dimension et à des tâches simples, pour deux raisons selon les auteurs : la taille des
réseaux admise par les puces neuromorphiques embarquées (Kapoho Bay : 262,1k neurones), et
la difficulté d'entraîner des SNN. Le plus petit SNN de flot optique connu compte encore
3,7 M de neurones (LIF-FireFlowNet [43]) (§1). Le précédent sur drone libre [48] n'avait
que 35 neurones de contrôle, la vision restant classique.

## Méthode

Pipeline **vision → contrôle entièrement neuromorphique** (§« A fully neuromorphic
solution », Fig. 1-3) :
- **Capteur** : caméra événementielle DAVIS240C orientée vers le sol, supposé **plan et
  statique**.
- **Vision (SNN)** : seuls les **4 coins** de l'image sont traités, chacun ramené à 16 × 16
  pixels par sous-échantillonnage. Un même petit SNN est appliqué à chaque coin : 5 couches
  (entrée, 3 encodeurs auto-récurrents conv 3 × 3 stride 2, pooling), 7,2k neurones et
  506,4k synapses par coin, soit 28,8k neurones au total (Abstract, Fig. 2). Au plus 90
  événements par coin et par fenêtre de 5 ms. Il sort le flot optique de chaque coin.
- **Neurone** : CUBA-LIF à fuites et seuil appris, partagés par couche (Éq. 1-2).
- **Entraînement auto-supervisé** sur de vraies données événementielles : contrast
  maximization (déflouage des événements), le flot dense étant obtenu par homographie à 4
  points pendant l'entraînement seulement (Éq. 3-12). BPTT sur 25 ms, surrogate gradient
  arctan. **QAT** qui reproduit la quantification de Loihi : poids 6 bits (Δw = 8), états
  entiers, arrondi vers zéro ; correspondance simulation / puce de 100 % (§Materials,
  « spiking, sequential processing »).
- **Contrôle** : une seule couche linéaire (matrice 4 × 9) qui va des observables visuels
  (vitesses mises à l'échelle par la hauteur, lacet) + roulis/tangage absolus + consigne
  vers poussée et attitude. Elle est **évoluée** par algorithme génétique (population 100,
  environ 25k générations) dans Flightmare, **sans simuler d'événements** : les flots de
  coins viennent de l'homographie continue de vérité terrain, avec bruit N(0, 0,025)
  (§« Training control in simulation »). Randomisation de domaine pour le sim-to-real.
- Comme la chaîne est linéaire, le décodage spikes → flot → commande se fusionne en une
  seule matrice (Fig. 7).

## Plateforme et implémentation

- **Drone** : quadrirotor maison de 1,0 kg et 35 cm (Fig. 1A), cadre 225 mm, hélices
  5 pouces, batterie 4S 1800 mAh, Pixhawk 4 Mini sous PX4 (Table 3). Ce n'est **pas un
  nano-drone**.
- **Calcul à bord** : Intel **Kapoho Bay** (2 puces Loihi) pour le SNN, et une carte
  UP Squared (Atom quad-core) pour le prétraitement (sous-échantillonnage, recadrage),
  l'encodage et le décodage des spikes, et le contrôleur (ROS1/ROS2). Tout passe par USB
  (§« Hardware setup »). Boucle complète à **200 Hz**.
- **Énergie** : mesurée non pas sur la Kapoho Bay (pas de sonde) mais sur une carte Nahuku
  (32 Loihi), avec deux puces allouées. Les sondes logicielles donnent la puissance
  statique, dynamique, au repos et totale. Les données sont préchargées en mémoire, donc
  **sans I/O ni prétraitement** (§« Energy benchmark »). La Jetson Nano de comparaison
  exécute le SNN en PyTorch, en modes 5 W et 10 W, puissance mesurée par tegrastats ; on
  compare la différence entre puissance en charge et au repos.
- **27 µJ par inférence** à 200 Hz sur Loihi (Abstract).
- Jeu de données événementiel d'environ 40 min (25 min d'entraînement, 15 de test) publié
  en matériel supplémentaire (§« Robust vision-based state estimation »). Code : n/r dans
  le texte extrait.
- Gamme de puissance (déduit) : le réseau seul est dans le domaine µJ / mW, mais le système
  embarqué (UP Squared + Kapoho Bay + USB) est d'un ordre de grandeur non rapporté,
  vraisemblablement quelques W pour l'UP Squared.

## Résultats

- **Flot optique (Table 1, EPE relatif au meilleur modèle)** : le Conv-GRU ANN avec
  sous-échantillonnage ×2 est la référence (0,056 EPE). Le SNN auto-récurrent final (coins
  + limite d'événements + quantification Loihi) fait **+50,04 %** d'EPE ; le Conv-RNN SNN
  fait +25,32 %. La quantification Loihi fait passer le SNN retenu de +38,74 % à +50,04 %
  (Table 1). Moins de 50 % des neurones de chaque couche sont actifs, même en mouvement
  rapide (Fig. 4C).
- **Vol réel** : sim-to-real réussi (vol stationnaire, atterrissage par divergence,
  translations latérales, y compris en tournant en lacet). Le contrôleur linéaire garde une
  **erreur statique proportionnelle à la consigne** en horizontal et n'atteint pas
  ±1,0 1/s ; un PI réglé à la main fait mieux (§« Control through visual observables »,
  Fig. 5).
- **Robustesse** : atterrissages réussis sous éclairage faible et sous lumière
  stroboscopique ; échec seulement dans l'obscurité quasi totale (Fig. 6B).
- **Énergie / vitesse (Table 2)** : Loihi est plus efficace que la Jetson Nano de **trois à
  quatre ordres de grandeur** en énergie par inférence, et d'un à deux ordres en fréquence
  d'exécution (§« Improved inference speed »). Les valeurs de la Table 2 **ne sont pas
  extraites** (en-tête seul).

→ reportés dans `benchmarks.csv` : 1 ligne (SNN de vision sur Loihi / Kapoho Bay, 200
inférences/s en vol, puissance n/r ; l'énergie de 27 µJ/inférence est donnée ici et non en
colonne ; baseline Jetson Nano ; Abstract et §« Hardware setup », confidence medium).

## Limites et critique

- **Comparaison Jetson biaisée, et reconnue comme telle** par les auteurs : le SNN est
  *simulé* en PyTorch sur la Nano, qui n'est pas faite pour ça ; un ANN à fenêtres
  temporelles y serait bien plus efficace (§« Improved inference speed »). Les trois à
  quatre ordres de grandeur comparent donc une puce dédiée à une émulation logicielle.
- **Portées de puissance différentes** : sondes logicielles de puces Loihi sur carte Nahuku
  (32 puces, les inutilisées éteintes) d'un côté, écart en charge/repos de la carte Jetson
  par tegrastats de l'autre. De plus, **sans I/O**, alors que les auteurs disent que l'I/O
  USB est le vrai goulot (§Discussion).
- **Le reste de la chaîne n'est pas neuromorphique** : prétraitement, décodage et contrôle
  tournent sur l'UP Squared. Sa consommation n'est pas rapportée, et domine sans doute
  l'énergie du système (déduit).
- **Hypothèses de scène fortes** : sol plan, statique, texturé, éclairage intérieur
  constant ; tests en salle avec OptiTrack (failsafe, initialisation du lacet) et avec
  **attache** (Fig. 8).
- **Précision du SNN nettement inférieure à l'ANN** : +50 % d'EPE (Table 1).
- Contrôleur linéaire insuffisant en horizontal ; ce ne sont pas des métriques de vol
  comparables à d'autres travaux (pas d'erreur de position absolue chiffrée dans le texte).
- Aucune tâche de détection.

## Pertinence pour la thèse

- **Axe `nano-drone` (neuromorphique)** : démonstration de référence d'un SNN à entrées
  événementielles de grande dimension, en boucle fermée sur un drone réel, et d'une énergie
  de réseau très faible (27 µJ/inf). C'est la contrepartie neuromorphique des travaux GAP8
  (PULP-Dronet) pour la gamme mW.
- **Co-design** : montre que l'I/O et le nombre de spikes échangés, et non le calcul,
  limitent le système (§Discussion). C'est un argument pour mesurer le système complet et
  non l'accélérateur seul.
- **Laisse ouvert** : la détection d'objets (petits objets, contre-drone) en neuromorphique
  embarqué, et la mesure d'énergie du système entier.

## Gaps identifiés

- **Énergie système vs énergie accélérateur** : la mesure porte sur la puce seule, sans I/O
  ni hôte, alors que l'hôte (UP Squared) reste indispensable. Même gap que pour les FPGA :
  aucune puissance « carte + hôte + capteur ».
- **Détection d'objets sur puce neuromorphique embarquée** : absente ici. Le papier se
  limite à l'ego-motion sur scène plane.
- **Neuromorphique sur nano-drone (< 30 g)** : visé par les auteurs mais hors de portée du
  matériel actuel (§Discussion).

## Statut de lecture

Papier complet (`fulltext.md` lu en entier, extraction GROBID `ok`). **Le corps de la
Table 2** (puissances et énergies Loihi / Jetson Nano) **manque** : seule sa légende et une
ligne d'en-tête sont extraites, bien que `extraction.warnings` ne cite que la Table 5 (dont
le corps manque aussi). Les chiffres absolus d'énergie et de fréquence par séquence sont
donc n/r, sauf les 27 µJ et 200 Hz de l'Abstract. La Table 4 est partiellement tronquée.

Ce qui suit est déduit et non affirmé par les auteurs :
- la gamme de puissance du système embarqué (quelques W pour l'UP Squared) et son poids
  dans l'énergie totale ;
- l'existence d'une version publiée (Science Robotics, 2024), non vérifiée ;
- le parallèle avec les travaux GAP8.
