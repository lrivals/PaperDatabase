---
id: 2021-alonso-elastic-df-scaling-performance-dnn
fiche: done
date: 2026-09-29
---

# Elastic-DF: Scaling Performance of DNN Inference in FPGA Clouds through Automatic Partitioning

Tobias Alonso, Lucian Petrica, Mario Ruiz, Jakoba Petri-Koenig, Yaman Umuroglu, Ioannis Stamelos, Elias Koromilas, Michaela Blott, Kees Vissers, 2021, ACM Trans. Reconfigurable Technol. Syst. 15(2), 15. https://doi.org/10.1145/3470567
Type : article de journal

## Problème

Les accélérateurs dataflow (DFA, type FINN) stockent tous les paramètres en mémoire sur puce : leur taille est bornée par la mémoire du FPGA, la granularité du repliement (folding) limite l'utilisation des ressources, et sur les FPGA multi-die (SSI, SLR) la fermeture de timing est dégradée (signal de reset unique, traversées de SLL) (§3.1-3.3). Les auteurs visent le cloud/datacenter (Alveo), pas l'embarqué.

## Méthode

Elastic-DF combine (§4) : (1) un partitionneur ILP exact (module Python `mip`) qui répartit les couches d'un DFA déjà replié sur SLR et FPGA, sous contraintes de congestion (limites Xilinx 70/50/80 %), de débit inter-puces et d'ancrages (placement absolu/co-location) ; (2) un équilibrage de ressources (LUT/DSP, BRAM/URAM) fait simultanément au partitionnement, et une recherche de « tuile » (nombre de FPGA et d'instances) ; (3) VNx, cœur UDP/IP 100 GbE pour la communication FPGA à FPGA (§4.3). Trois variantes de parallélisme de modèle : SwMP (via l'hôte), HwMP (Ethernet direct), TMP (transparent, même interface logicielle qu'un FPGA unique). Intégré à FINN (frontend Brevitas, ONNX), orchestration InAccel Coral (§5.2).

## Plateforme et implémentation

Cluster ETH Zurich XACC : Alveo U250 / U280 (10 cartes), Ethernet 100 Gb/s pair à pair, Vitis 2020.1, effort d'optimisation maximal, balayage de fréquence cible 180-250 MHz (§5.1, §5.3). Modèles : MobileNetV1 W4A4 (70,39 % top-1) et ResNet-50 W1A2 (67,27 % top-1) (Table 1). Fréquences Fmax de 190 à 241 MHz partitionné (Table 5). Puissance : « board power » moyenne de Table 4 (deux cartes) ; la puissance CPU est estimée par le taux d'utilisation × TDP de 260 W (§6.2) ; VNx dissipe 6 W à plein débit (§4.3), 35 219 LUT (Table 2). Code : le partitionneur, VNx et un exemple d'optimisation de fréquence FINN sont annoncés open source (refs [33,41,45], §1), liens non repris dans le texte extrait.

## Résultats

- Deux U280 : ResNet-50, MP ≈ DP en débit (3 374-3 618 contre 3 513 FPS) mais latence noyau quasi divisée par deux (1,52-1,55 ms contre 2,72 ms) ; MobileNetV1, TMP +41 % de débit (5 923 contre 4 195 FPS) avec 3 instances au lieu de 2 (Table 4, §6.1). Approx. 40 Gb/s de trafic inter-FPGA pour ResNet-50.
- TMP/HwMP/SwMP : SwMP meilleur à petits batchs mais latence applicative plus élevée et plus variable ; en MLPerf multi-stream, SwMP perd ~40 % de FPS à 50 ms (p99) et ~4x à 7 ms (§6.2).
- ILP contre glouton (MobileNetV1) : ILP tient sur 2 SLR sur toutes les cartes, glouton 3 SLR, et échoue sur U50 (§6.3).
- Partitionnement : Fmax +20 % en moyenne face aux builds Vitis monolithiques (Table 5, §1) ; accélération de 1,58 à 1,90 (mesure RSTC en SLR0).
- Speed-up 2 nœuds : 2,06 (ResNet-50), 2,82 (MobileNetV1, 3,73 avec compression) (Table 7). Meilleur FPS multi-nœud 5,9 k (MobileNetV1), latence min 1,7 ms (ResNet-50) selon Table 6 (§6.5).
- VNx : 97 Gb/s au-delà de 1 kB, latence 0,526 µs point à point, aucune perte sur 15 h (~700 milliards de paquets) (§4.3).
→ reportés dans `benchmarks.csv` : 10 lignes (8 de Table 4, 2 configurations monofichier de Table 6), voir `bench_rows.csv`.

## Limites et critique

- Cible datacenter (Alveo, 100 GbE, plusieurs cartes) : les valeurs de débit et de puissance (100-134 W pour deux cartes) ne sont pas comparables à des SoC embarqués (Kria, ZCU104) ; classification ImageNet, pas de détection.
- Puissance : « average power » sans méthode de mesure détaillée dans le texte ; le CPU est estimé et non mesuré (§6.2). Le champ `power_scope` est mis à `board` d'après le vocabulaire « board power » du texte, pas d'une méthode décrite.
- Comparaisons : latences du Table 6 non comparables (kernel contre bout en bout, quantifications différentes, HLS contre RTL) ; les auteurs le reconnaissent (§6.5). Certaines valeurs concurrentes sont estimées.
- Limites propres (§6.5.1) : ILP exact lent sur réseaux très profonds ; seuls MobileNetV1 et ResNet-50 (FINN) évalués ; pas plus de 2 FPGA ; Fmax non explorée par seeds ; UDP non fiable (perte estimée à ~3e-5 de précision, calcul des auteurs sous hypothèse « une erreur = une erreur de classification »).
- Aucun aspect sûreté : UDP sans contrôle de flux, déterminisme non traité (déduit, non discuté par les auteurs).

## Pertinence pour la thèse

Faible à moyenne. Apport : exemple de flot FINN + partitionnement ILP exploitable pour fixer explicitement un floorplan (co-location, contraintes de congestion), donc une implémentation plus prévisible en fréquence, propriété utile à une argumentation de déterminisme/certification (déduit). Ne traite ni YOLO, ni l'embarqué, ni la sûreté ; le multi-FPGA via Ethernet est hors de propos pour un flux vidéosurveillance sur une carte unique. Utile surtout comme référence toolflow (axe `toolflows`).

## Gaps identifiés

- Le partitionnement FINN multi-SLR/FPGA n'est pas évalué sur des détecteurs (YOLO) ni sur SoC embarqués.
- Aucune analyse de déterminisme temporel (latence p99 seulement sur le réseau, pas de WCET) ni de tolérance aux fautes de la liaison entre FPGA.

## Statut de lecture

Papier complet (fulltext.md lu en entier ; l'annexe A ILP est partiellement illisible à l'extraction : équations tronquées). Résumé (abstract) vide dans l'extraction. Table 6 et Table 8 reconstruits par extraction, colonnes de Table 6 alignées par recoupement avec le texte (§6.5). Déduit et non affirmé par les auteurs : la pertinence pour la certification, la portée `board` de la puissance, l'absence d'aspect sûreté.
