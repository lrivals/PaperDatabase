---
id: arxiv-2206.11791-open-source-fpga-ml-codesign
fiche: done
date: 2026-09-29
---

# Open-source FPGA-ML codesign for the MLPerf Tiny Benchmark

Hendrik Borras, Giuseppe Di Guglielmo, Javier Duarte, Nicolò Ghielmetti, Ben Hawks, Scott Hauck, Shih-Chieh Hsu, Ryan Kastner, Jason Liang, Andres Meza, Jules Muhizi, Tai Nguyen, Rushil Roy, Nhan Tran, Yaman Umuroglu, Olivia Weng, Aidan Yokuda, Michaela Blott, 2022, arXiv preprint (soumission MLPerf Tiny v0.7, division ouverte). https://arxiv.org/abs/2206.11791
Type : preprint non relu par les pairs

## Problème

Montrer que les flots open source hls4ml et FINN permettent de faire du co-design modèle/FPGA pour le MLPerf Tiny v0.7 (classification d'images IC, détection d'anomalies audio AD, détection de mots-clés KWS) sur un SoC (Pynq-Z2, Zynq-7020) et sur un FPGA seul (Arty A7-100T, Artix-7), avec un flot commun de QAT à l'implémentation (§1).

## Méthode

Modèles quantifiés en architecture dataflow spatiale, sans mémoire off-chip pour le réseau (§3). IC hls4ml : NAS par optimisation bayésienne (KerasTuner) sur un ResNet-8 généralisé, QAT QKeras 8 bits dont 2 entiers, pass hls4ml de dimensionnement des FIFO par simulation RTL, fusion de ReLU (§3.1). IC FINN : CNV-W1A1 (binaire, entrée 8 bits), scan ASHA avec métrique de coût (BOPs et mémoire de poids) (§3.2). AD hls4ml : autoencodeur MLP réduit (9 couches de 128 vers 5 couches de 72, entrée sous-échantillonnée de 640 à 128), couche QDenseBatchnorm (fusion BN/dense), reuse factor 144 (§3.3). KWS FINN : MLP à 3 couches FC quantifié 3 bits par Brevitas (§3.4). Optimisations FINN automatiques (constant folding, streamlining, minimisation des accumulateurs, FIFO) (§3.5). Format d'échange QONNX (§4.1). Intégration Vivado 2019.1 ; MicroBlaze sur l'Arty ; harnais EEMBC EnergyRunner (§4).

## Plateforme et implémentation

Pynq-Z2 (Zynq-7020) et Arty A7-100T (xc7a100t-1csg324) ; fréquence n/r dans le texte extrait. Ressources : Table 5. Latence : médiane sur 5 échantillons, batch 1, au moins 10 s d'exécution continue (§4.4.1). Énergie : Joulescope JS110 sur le DUT alimenté par une alimentation HP/Agilent E3610A, médiane par inférence (§4.4.2) ; il s'agit d'une mesure de l'appareil sous test, portée précise (carte ou puce) non détaillée ; la puissance en W n'est pas rapportée. Code : soumissions publiées dans le dépôt MLPerf Tiny v0.7 (§4.4.1) et flots « publics en ligne » (note de bas de page, lien non extrait) ; bitstreams : n/r.

## Résultats

Table 5 (latence ; énergie par inférence ; ressources) :
- Pynq-Z2 : IC hls4ml 27,3 ms / 44 330 µJ (LUT 28 544, BRAM 42, DSP 4) ; IC FINN 1,5 ms / 2 535 µJ (LUT 24 502, BRAM 100, DSP 0) ; AD 0,019 ms / 30,1 µJ (LUT 40 658, BRAM 14,5, DSP 205) ; KWS 0,017 ms / 30,9 µJ (LUT 33 732, BRAM 37, DSP 1).
- Arty A7-100T : IC hls4ml 33,1 ms / 73 166 µJ ; IC FINN 1,5 ms / 3 419 µJ ; AD 0,045 ms / 98,4 µJ ; KWS 0,033 ms / 53,7 µJ.
- Le résumé annonce des latences jusqu'à 20 µs et 30 µJ par inférence (Abstract), et les auteurs indiquent une plage de 30 ms à 20 µs et de 70 mJ à 30 µJ (§4.4).
- Ablations : Table 3 (IC hls4ml, estimations Vivado HLS, table reconstruite par Docling) : BRAM 477 vers 146 blocs 18 kb avec toutes les optimisations, LUT 66 838 vers 46 969.
- Modèles : IC hls4ml 83,5 % (jeu de test, modèle NAS) contre 87,0 % pour la référence ResNet-8 (§3.1) ; précisions finales mesurées dans la Table 1, absente du texte extrait.
- Comparaison hls4ml/FINN sur IC : hls4ml utilise 58 % de BRAM en moins mais une latence 18,2x plus grande (§4.2.2).
→ reportés dans `benchmarks.csv` (via bench_rows.csv) : 8 lignes (IC hls4ml, IC FINN, AD hls4ml, KWS FINN sur chacune des deux plateformes), confidence high (Table 5) ; précisions à n/r car la Table 1 est absente ; l'énergie par inférence (µJ) n'a pas de colonne et n'est donnée qu'ici.

## Limites et critique

- Aucune tâche de détection d'objets : IC est du CIFAR-10 32x32, AD et KWS sont audio ; pas de YOLO ni de résolution vidéo réelle.
- Pas de comparaison à d'autres plateformes dans l'article (choix assumé, §1) : aucun baseline MCU/GPU ; les latences ne sont pas comparables entre les deux flots sans normaliser modèle et précision (hls4ml : 58 k paramètres à 8-12 bits, FINN : 1,5 M paramètres binaires).
- La latence IC hls4ml (27 ms) reflète une architecture non pipelinée, avec une couche dominante ; les auteurs l'annoncent comme à améliorer.
- Énergie mesurée sur l'appareil sous test dans un montage EEMBC avec MicroBlaze/PS : la portée (carte ou puce) est mal définie (déduit) ; pas de puissance en W.
- Précision d'AD (AUC) et de KWS non reportée dans le texte extrait ; sélection sur un sous-ensemble de 200 images pour IC dans le harnais de référence (§2.1), mais la division ouverte évalue le jeu de test complet (§4.4.1).
- Preprint, outils dans un état de 2022 (Vivado 2019.1, Vivado HLS).

## Pertinence pour la thèse

Axes `toolflows` et `platforms`. Description détaillée et comparaison directe hls4ml vs FINN sur les mêmes cartes, avec un flot de bout en bout (QAT, QONNX, FIFO, intégration SoC) et une méthodologie de mesure normalisée (EEMBC), utile comme référence de méthode pour comparer des flots. Le modèle AD est un autoencodeur sur FPGA (sur audio, non sur image). Pour la thèse « sécuritaire », rien sur la sûreté ni la vérification ; le déterminisme temporel des architectures dataflow (latence fixe) est un atout à exploiter (déduit).

## Gaps identifiés

- Autoencodeurs sur FPGA appliqués à l'image : ici AD est un MLP sur spectrogrammes audio.
- Passage à l'échelle de ces flots (hls4ml, FINN) vers un détecteur de type YOLO sur images réelles.
- Absence de vérification/certification des flots générés (équivalence QAT vers RTL).

## Statut de lecture

papier complet. Table 3 reconstruite par Docling (à vérifier) ; la Table 1 (précisions mesurées) n'est pas dans le texte extrait, et Table 4 n'a que sa légende ; les chiffres de Table 5 semblent cohérents (pourcentages de ressources recoupés). Déduit et non affirmé par les auteurs : portée de la mesure d'énergie, pertinence pour la thèse.
