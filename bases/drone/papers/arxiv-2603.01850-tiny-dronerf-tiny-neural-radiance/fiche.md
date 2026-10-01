---
id: arxiv-2603.01850-tiny-dronerf-tiny-neural-radiance
fiche: done
date: 2026-10-01
---

# Tiny-DroNeRF: Tiny Neural Radiance Fields aboard Federated Learning-enabled Nano-drones

Ilenia Carboni, Elia Cereda, Lorenzo Lamberti, Daniele Malpetti, Francesco Conti, Daniele Palossi, 2026, arXiv preprint (le texte indique « accepted for publication in IEEE ICRA 2026 »). https://arxiv.org/abs/2603.01850
Type : preprint non relu par les pairs (au moment de l'ingestion ; acceptation ICRA 2026 déclarée sur la première page)

## Problème

Faire de la reconstruction 3D dense (NeRF, synthèse de vues nouvelles) à bord d'un nano-drone (< 30 g), dont le MCU fait < 100 mW pour ~100 GOps/s au mieux et dispose de moins de 100 MB de mémoire, alors que les NeRF SoA exigent des GB de mémoire et des GPU de plusieurs centaines de W (Abstract, §I). Objectif secondaire : entraîner de façon collaborative sur un essaim (federated learning, FL) pour dépasser ce qu'une seule image-mémoire de drone permet.

## Méthode

- Tiny-DroNeRF = Instant-NGP (hash-grid multi-résolution MRHE + MLP densité + MLP couleur, occupancy grid) réduit par optimisation d'hyperparamètres : images par pas (100 → 1), résolution (800 → 160 px), taille de batch B, taille de table de hachage T (§IV-A). Configuration retenue : 1 img/pas, 160x160, B = 8k, T = 2^13 (§V-B, Fig. 3).
- Implémentation C embarquée : noyaux écrits à la main pour chaque bloc, parallélisés sur le cluster GAP9, tiling en L1, DMA recouvrant le calcul, batch accumulation (tuiles de 1024 échantillons, 8x, pour B = 8k) ; niveaux du MRHE et occupancy grid déplacés un à un en L2 (§IV-B, §V-C). Arithmétique float16, mise à jour des poids accumulée en float32 (§IV-B).
- FL : un drone coordinateur (pré-entraînement N_pt = 10k pas), N_l = 1k pas locaux par tour, agrégation FedAvg ; deux variantes (avec ou sans échange de l'occupancy grid) ; partition IID et non-IID par secteurs de vue (§IV-C, §V-E).

## Plateforme et implémentation

- Crazyflie 2.1 Brushless (27 g, 10 cm, batterie LiPo 350 mAh) + GAP9Shield (open source) : SoC GreenWaves GAP9, 32 MB HyperRAM / OctaSPI RAM (L3), module Wi-Fi u-blox NINA-W102 (ESP32, jusqu'à 15 Mbit/s), caméra basse consommation (§III-B).
- GAP9 : 9 cœurs de cluster + 1 Fabric Controller, 4 FPU (16/32 bits), accélérateur NE16 (150 GOp/s entiers, non utilisé : conçu pour la passe avant de CNN entiers, alors que la charge exige rétropropagation et virgule flottante) ; 370 MHz, 0,8 V, « 60 mW de puissance moyenne » (§III-B) ; L1 128 kB, L2 1,5 MB (§III-B).
- Mémoire : pics 1,3 MB en L2 et 112 kB en L1 ; 3,6 MB de transferts L3 par pas (§V-C). Modèle 21,4 MB contre 527 MB pour Instant-NGP, soit -96 % (§I) ; 0,284 MB de paramètres (Table I).
- Les latences viennent du simulateur cycle-accurate GVSOC, non du matériel (§V-C).
- Code / modèle publiés : non mentionnés dans le texte lu ; seule une vidéo supplémentaire est donnée (https://youtu.be/-frFPUBGa0c).

## Résultats

- Instant-NGP baseline : 527 MB, 17,52 GOp/pas, PSNR 32,59 dB, SSIM 0,96 (Table II) ; temps d'entraînement > 2 jours sur MCU (§V-B).
- Tiny-DroNeRF : PSNR 26,94 dB, SSIM 0,892, 0,284 MB de paramètres (Table I), -5,7 dB de PSNR vs Instant-NGP (§I). Entraînement : 73 ms par pas amorti, soit 97 min pour 10k pas x 8 tuiles (§V-C) ; passe avant 12,8 ms et arrière 21,7 ms par tuile, Adam 22,4 ms tous les 8 pas, mise à jour de l'occupancy grid 6,4 s tous les 256 pas (§V-C). Rendu d'une image 160x160 : ~4,1 s (13 échantillons/pixel en moyenne ; §V-C). Sur GPU, Table I donne 28 s d'entraînement pour le même modèle.
- En conditions réelles (1954 images niveaux de gris 160x160 prises par le nano-drone, poses par COLMAP, 1709 train / 245 test) : PSNR 21,2 dB, SSIM 0,73 (§V-D).
- FL (Lego, 4 drones, 25 images chacun) : IID, +0,7 dB au-dessus du meilleur drone seul et -0,6 dB sous la borne centralisée ; non-IID, +1,7 dB au-dessus du meilleur drone seul et -3,25 dB sous la borne centralisée (§V-E). Échanger l'occupancy grid est inutile : 0,52 MB et 2,24 s par tour sans elle, contre 4,7 MB et 20,16 s avec (~88 % du volume) (§V-E). Valeurs absolues de PSNR FL : n/r dans le texte (Fig. 6 seulement).
→ reportés dans `benchmarks.csv` (3 lignes, fournies à l'agent principal) : entraînement synthétique (PSNR 26,94 ; 73 ms/pas), rendu 160x160 (4100 ms), entraînement in-field (PSNR 21,2). Les résultats FL n'ont pas de ligne (écarts relatifs, absolus dans les figures seulement) ; la baseline Instant-NGP GPU n'est pas une configuration embarquée.

## Limites et critique

- Puissance : 60 mW « moyenne » à 370 MHz sans méthode de mesure décrite, donc `power_scope: unspecified` ; aucune énergie par pas ni autonomie rapportée, alors que 97 min d'entraînement sur une batterie 350 mAh est précisément la question (déduit : la consommation de vol du Crazyflie dépasse largement celle du SoC, et le papier ne chiffre pas le coût énergétique d'un entraînement ni de la communication).
- Latences issues de GVSOC (simulateur), pas mesurées sur la puce ; l'entraînement complet sur le drone n'est pas démontré de bout en bout (le dataset in-field est transmis par Wi-Fi et post-traité avec COLMAP ; l'entraînement de §V-D n'est pas dit tourner à bord).
- Qualité : -5,7 dB de PSNR (26,94 contre 32,59) à 160x160 vs 800x800 pour Instant-NGP : les images n'ont pas la même résolution, la comparaison de PSNR n'est donc pas iso-conditions. Table I mélange des chiffres de littérature à 800x800 et ceux de Tiny-DroNeRF à 160x160.
- Poses connues supposées (ground truth ou COLMAP hors ligne) : ni SLAM ni estimation de pose embarquée ; scène statique ; scène réelle unique.
- FL : 4 drones, communications Wi-Fi supposées parfaites, pas de pannes ni de perte de paquets ; les coûts de communication (2,24 s par tour) n'incluent pas l'énergie. Deux setups seulement (Lego).
- Table I annonce « 97 min, < 0,10 W, MCU » ; la puissance de classe GPU n'y est pas chiffrée dans le texte extrait. Table II extraite par PyMuPDF est illisible colonne par colonne ; attribution des valeurs aux colonnes déduite.
- Pas de baseline Jetson / autre MCU. Preprint non relu par les pairs au moment de l'ingestion.

## Pertinence pour la thèse

Axe `nano-drone`, gamme de puissance mW (GAP9, 60 mW). Montre que de l'apprentissage embarqué (rétropropagation en virgule flottante) est faisable sur un MCU nano-drone, avec un co-design algorithme-mémoire (tiling, batch accumulation) qui rend la charge compute-bound. Pas de détection ni de FPGA : intérêt indirect (méthodologie de contrainte mémoire L1/L2/L3, apprentissage collaboratif en essaim, borne basse de la charge de calcul). Laisse ouvert : coût énergétique et autonomie, mesure sur matériel réel, perception pour la navigation/planification qui consommerait ce modèle.

## Gaps identifiés

- Aucune mesure d'énergie / d'autonomie pour l'entraînement ou le FL embarqué sur nano-drone (latence seulement, sur simulateur).
- Pas de lien perception 3D ↔ planification de vol ou vitesse de vol sûre : le modèle sert la qualité PSNR, pas une tâche de navigation.
- FL sur essaim réel : pas de test sur plusieurs drones physiques ni de canal sans fil dégradé.
- Quantification entière (INT8) non explorée : le NE16 (150 GOp/s) reste inutilisé.

## Statut de lecture

Papier complet (fulltext.md lu en entier). Extraction par PyMuPDF avec `extraction.ok: false` : le texte peut être mal découpé ; Table I et Table II sont reconstruites par PyMuPDF, leurs colonnes sont mêlées et à vérifier. Seules les valeurs redonnées par le texte (PSNR 26,94 ; mémoire 527 → 21,4 MB ; 73 ms ; 97 min ; PSNR in-field 21,2) sont retenues avec `confidence: medium`.
Ce qui suit est déduit et non affirmé par les auteurs : attribution du couple (T = 2^13, B = 8k) à la deuxième colonne de la ligne B = 8k de Table II ; impact énergétique sur la batterie ; absence de code publié (non mentionné, non vérifié sur le web).
