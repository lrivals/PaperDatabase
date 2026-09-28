---
id: arxiv-1805.01831-64mw-dnn-visual-navigation-engine
fiche: done
date: 2026-09-28
---

# A 64mW DNN-based Visual Navigation Engine for Autonomous Nano-Drones

Daniele Palossi, Antonio Loquercio, Francesco Conti, Eric Flamand, Davide Scaramuzza, Luca Benini, 2018, arXiv preprint. https://arxiv.org/abs/1805.01831 (DOI 10.1109/JIOT.2019.2917066)
Type : preprint non relu par les pairs selon `metadata.json`. Le DOI renvoie à la version
publiée dans IEEE Internet of Things Journal (2019) : la venue de `metadata.json` est à
corriger après vérification.

## Problème

La navigation visuelle par CNN est courante sur les drones de taille standard (processeurs
de 10 W ou plus, ou calcul déporté), mais jugée hors de portée des nano-drones. Ceux-ci n'ont
que des MCU de quelques centaines de Mop/s, et la part de puissance allouable au calcul est
d'environ 5 % du total (Wood et al. [14], §I). Les auteurs veulent exécuter entièrement à bord,
en boucle fermée, un CNN de navigation de l'état de l'art (DroNet [1]) sur un Crazyflie 2.0
de 27 g (Abstract, §I).

## Méthode

- **Réseau** : DroNet, un CNN résiduel léger à deux sorties (angle de braquage en
  régression, probabilité de collision en classification). Il fait environ 41 MMAC par image
  (convolutions seules) et plus de 1 Mo de poids en FP32 (§III-A, §IV-A).
- **Adaptations** (§IV-A, Table II) :
  - quantification en **Fixed16 Q4.12** (poids et activations), avec réentraînement
    quantization-aware (méthode Hubara et al.) ;
  - max-pooling réduit de 3×3 à 2×2 (2,2 fois plus rapide sur ces couches) ;
  - fine-tuning avec environ 1 300 images de la caméra embarquée HiMax (dataset « HiMax »).
- **Mapping sur GAP8** : outil **AutoTiler**, qui génère le tiling L2 → L1 avec double
  buffering par DMA (§IV-B). Deux schémas de parallélisation sur les 8 cœurs du cluster :
  - spatial, pour la 1re couche ;
  - par canaux de sortie (feature-wise), pour les suivantes (§IV-C).
  Le code utilise les instructions SIMD de GAP8 (dot product 16 bits).
- **Gestion mémoire L3 → L2** : deux piles d'allocation linéaires. Sans elles, il faudrait
  665 kB en L2 ; avec elles, 370 kB suffisent sur les 512 kB, et 142 kB restent libres
  (§IV-D, Fig. 7).
- **PULP-Shield** : PCB de 30 × 28 mm et environ 5 g, enfichable sur le Crazyflie. Il porte
  le GAP8, 64 Mbit de HyperRAM, 128 Mbit de HyperFlash et une caméra HiMax 320 × 240 en
  niveaux de gris (4,5 mW) (§V). Le STM32 du drone délègue l'inférence au shield et reçoit
  les résultats par SPI (Fig. 9).

## Plateforme et implémentation

- **Puce** : GreenWaves GAP8 (RISC-V, 1 FC + 8 cœurs de cluster, 512 kB de L2, 64 kB de L1)
  sur PULP-Shield, monté sur un Crazyflie 2.0 (STM32F405) (§III-B, §V).
- **Points de fonctionnement** : de 50 à 250 MHz, à 1,0 V ou 1,2 V (§VI-A, Fig. 10). Le plus
  efficace est à 1,0 V, FC 50 MHz et CL 100 MHz ; le plus rapide à 1,2 V, FC et CL 250 MHz.
  250 MHz dépasse la configuration officiellement supportée.
- **Mesure de puissance** : analyseur DC de banc, avant le convertisseur DC/DC interne
  (§VI-A).
  - Au point efficace (Fig. 11, Table III) : 39 mW en moyenne pour le SoC, 45 mW avec les
    pertes du DC/DC. 64 mW pour tout le shield, en ajoutant la mémoire L3 et la caméra ;
    le texte ne dit pas clairement si ces deux ajouts sont mesurés ou estimés.
  - Au point rapide : 272 mW pour le SoC, 284 mW pour le shield (§VI-A, §VI-B, Fig. 12).
- **Ressources** : 370 kB de L2 (§IV-D). Cycles par image : 14,61 M, dont 13,47 M de calcul
  (Table V, reconstruite par PyMuPDF, cohérente avec le texte du §VI-B).
- **Code** : le design du PULP-Shield, le code GAP8, les datasets et les réseaux entraînés
  sont annoncés publiés sous licence open source (§I, §VII). Le lien n'est pas dans le texte
  extrait : n/r.

## Résultats

- **Débit et puissance** : 6 FPS à 64 mW au point efficace, jusqu'à 18 FPS à 284 mW au point
  rapide (Abstract, §VII). Cela représente 0,8 % et 3,5 % de la puissance totale du
  drone, estimée à 7,6 W (Fig. 12).
- **Efficacité de calcul** : 2,81 MAC/cycle réels, avec un pic de 0,64 MAC/cycle/cœur
  (§VI-B). Le débit est de 281 MMAC/s à 45 mW au point efficace et 702 MMAC/s à 272 mW au
  point rapide (§VI-B).
- **Comparaison MCU** : un STM32H7 à 400 MHz atteindrait 276 MMAC/s à 346 mW en pic
  théorique (§VI-B). Cela donne 5,4 fois moins de puissance à performance égale pour GAP8, et
  4 fois le pic de CMSIS-NN. Les chiffres du STM32H7 sont théoriques et non mesurés.
- **Précision** : configuration déployée (Fixed16, pool 2×2, dataset Original + HiMax),
  Table II :
  - collision sur le dataset HiMax : accuracy 0,891, F1 0,821 ;
  - collision sur le dataset Original : accuracy 0,977, F1 0,946 ;
  - braquage : EVA 0,732, RMSE 0,110.
  En référence, la version FP32 3×3 entraînée sur le seul dataset Original fait 0,859 en
  accuracy sur HiMax.
- **Autonomie** (Table IV, vol stationnaire à 0,5 m) : environ 440 s pour le Crazyflie seul,
  350 s avec le shield éteint, 340 s avec le shield qui exécute DroNet. Le coût total est
  d'environ 22 %, surtout dû à la masse (§VI-A).
- **Contrôle** : à 4 m/s, un arrêt demande 400 ms et 0,7 m (modèle analytique). L'inférence
  à 10 Hz suffit à éviter l'obstacle, pas celle à 5 Hz. Ce test est fait **hors ligne**, sur
  des images d'un vol manuel (§VI-C, Fig. 13). La boucle fermée n'est montrée qu'en vidéo.

→ reportés dans `benchmarks.csv` : 2 lignes (DroNet Fixed16 sur GAP8, points de
fonctionnement efficace 6 FPS / 64 mW et rapide 18 FPS / 284 mW ; précision = accuracy de
collision sur le dataset HiMax, Table II ; `power_scope` = board, c'est-à-dire le shield
entier, confidence medium).

## Limites et critique

- **Tâche non comparable à la détection** : DroNet est une régression plus une
  classification binaire (résolution d'entrée du réseau : n/r dans le texte). Il n'y a ni
  boîtes, ni mAP, ni petits objets. Les 41 MMAC sont environ deux ordres de
  grandeur sous un YOLO-tiny (déduit).
- **Portée de la puissance** : la chaîne 39, 45 puis 64 mW mêle mesure (SoC) et ajouts
  (L3, caméra) dont la méthode n'est pas précisée. La puissance du STM32 hôte et de
  l'électronique du drone (277 mW) n'est pas incluse dans les 64 mW.
- **Baseline MCU théorique** : pic du STM32H7 sans mouvement de données, contre des mesures
  réelles sur GAP8. La comparaison favorise GAP8 sur la forme, même si l'écart est réel.
- **Évaluation du contrôle hors ligne** : l'évitement d'obstacle est rejoué sur des images
  enregistrées. Pas de taux de réussite en vol réel, ni de nombre d'essais.
- **Surfréquence** : le point 18 FPS est hors de la spécification officielle de GAP8 (§VI-A).
- **Gamme de puissance** : nano (dizaines à centaines de mW), l'échelle GAP8 du profil. Pour
  un ordre de grandeur (déduit), c'est environ 100 fois moins qu'une Jetson TX2 à environ
  10 W, et au moins 10 fois moins qu'un FPGA à quelques W.

## Pertinence pour la thèse

- **Papier fondateur de l'axe `nano-drone`** : premier CNN de navigation en boucle fermée
  entièrement à bord d'un nano-drone. La méthodologie (Fixed16, tiling L3/L2/L1, double
  buffering, parallélisation) est réutilisable pour porter un détecteur sur GAP8 ou GAP9.
- **Métriques système rares et précieuses pour l'axe `system-codesign`** :
  - bilan de puissance du drone entier (Fig. 12) ;
  - coût en autonomie décomposé en masse et en calcul (Table IV : masse 90 s, calcul 10 s) ;
  - lien entre fréquence d'inférence et distance d'arrêt (§VI-C).
  C'est exactement le type de métrique « autonomie, vitesse de vol sûre » que les papiers
  YOLO/FPGA n'ont pas (hypothèse de `gaps.md`).
- **Enseignement quantitatif** (lu) : la masse du module coûte plus d'autonomie que le
  calcul. Cela plaide pour un co-design masse × puissance, pas seulement W.
- **Laisse ouvert** : la détection d'objets à cette échelle (voir TinyissimoYOLO dans la
  base), et la fiabilité en vol réel.

## Gaps identifiés

- **Coût d'autonomie décomposé (masse contre calcul)** : mesuré ici pour un nano-drone
  (Table IV). Aucun équivalent n'est connu pour un module FPGA ou Jetson sur un drone de
  taille moyenne. À chercher ou à mesurer.
- **Relation fréquence d'inférence, distance d'arrêt et vitesse sûre** : esquissée (§VI-C),
  mais hors ligne et pour une tâche binaire. Rien d'équivalent pour un détecteur dont la
  latence dépend de la résolution.
- **Détection multi-classe à l'échelle nano** : non traitée ici. DroNet reste un réseau de
  régression et classification.

## Statut de lecture

Papier complet (`fulltext.md` lu en entier, extraction GROBID `ok`). La section I n'est pas
détectée comme titre : l'introduction est rattachée à l'Abstract. La Table V est reconstruite
par PyMuPDF (chiffres recoupés avec le §VI-B). La Table I (comparaison des plateformes) est
absente de l'extraction. La Fig. 10 (balayage fréquence et tension) n'est connue que par le
texte.

Ce qui suit est déduit et non affirmé par les auteurs :
- la publication dans IEEE IoT Journal, d'après le DOI ;
- l'écart de complexité avec un YOLO-tiny ;
- les comparaisons d'ordre de grandeur avec Jetson et FPGA ;
- le caractère possiblement estimé des parts L3 et caméra dans les 64 mW ;
- la décomposition 90 s / 10 s de la perte d'autonomie, calculée à partir de la Table IV.
