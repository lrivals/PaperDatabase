---
id: 2025-zhang-wcet-estimation-cnn-inference-fpga
fiche: done
date: 2026-11-03
---

# WCET Estimation for CNN Inference on FPGA SoC With Multi-DPU Engines

Wei Zhang, Yunlong Yu, Xiao Jiang, Nan Guan, Naijun Zhan, Lei Ju, 2025, IEEE Trans. Parallel Distrib. Syst. 36(6), 1146–1160. https://doi.org/10.1109/TPDS.2025.3555968
Type : article de journal (relu par les pairs)

## Problème

Le DPU de Xilinx (Vitis AI) est l'accélérateur CNN commercial standard des SoC FPGA, mais la littérature vise la performance moyenne ; la borne de pire cas (WCET) est indispensable pour un système temps réel (§I). Seule une analyse statique existait, pour un DPU seul (Restuccia et Biondi, [8]). Or avec plusieurs DPU sur la même puce, la latence d'un même CNN varie jusqu'à 3x entre meilleur et pire cas observés (Abstract, §III, Fig. 4), à cause de la contention sur la mémoire partagée, ce qui rend une borne par mesure peu sûre.

## Méthode

Analyse statique du temps d'inférence d'un CNN sur un ou plusieurs DPU (§IV-§V) :
- modèle d'exécution du DPU (lectures d'instructions, lectures et écritures de données en parallèle, phase « elaboration » sans accès bus) : T = max{T_R, T_INS + T_W} + T_ELAB (éq. 1, §V-A) ;
- chaque phase = temps de base (transfert maximal mesuré, plus attente entre ports du même DPU) + temps supplémentaire dû aux autres DPU, borné par le nombre de transactions concurrentes (Lemme 1) sur l'interconnexion PL, l'interconnexion PS et l'arbitre de ports DDR, tous à tourniquet (§V-B, §V-C1) ;
- analyse fine : le CNN est découpé en segments de nœuds DPU séquentiels ; une matrice de contention entre deux CNN donne le pire chemin (§V-C2) ; T_extra = min(fin, basique) ;
- WCET = T_base + T_extra + T_ELAB, avec T_ELAB mesuré en DPU seul (§V-A) ;
- paramètres alimentés par mesure : nombre de transactions par phase et par port (AXI Performance Monitor), temps de transfert maximal par interface PL-PS (System ILA), 10 000 à 1 million d'exécutions (§VI-A).

## Plateforme et implémentation

ZCU102, Zynq UltraScale+ XCZU9EG ; DPU B4096 (jusqu'à 3 sur la puce) et B3136, DPU à 300 MHz, Vitis 2021.2 et Vitis AI 2.0, modèles du Vitis AI Model Zoo (§VI-A). Entrées prises dans Cityscapes et ImageNet. Puissance : n/r (non étudiée). Quantification : n/r (non dite dans le texte extrait). Code : le calcul du WCET est publié à https://github.com/212SoleYu/WCET-Multi-DPUs (note de bas de page 1, §VI-B) ; bitstream : n/r.

## Résultats

- DPU seul : latence très stable. MobileNetV2 : min 5,56 ms, max 5,81 ms sur 20 000 images (§III, Fig. 4) ; YOLOv3/Cityscapes : 8,867 et 9,093 (écart 2,49 %, unité non écrite) (§III).
- 3 DPU B4096 (MobileNetV2 sur DPU1, YOLOv4 sur DPU2 et DPU3) : le max dépasse le min d'environ 200 % (§III, Fig. 4) ; l'abstract parle de « 3X » et l'introduction de « up-to 300 % » pour la même variation : formulations non cohérentes entre elles.
- DPU seul : borne estimée plus serrée de plus de 27 % en moyenne que [8] ; meilleur cas à 128 % du WCET mesuré (§VI-B, Fig. 10).
- 2 DPU : meilleur cas à 1,73x du WCET mesuré (§VI-C). 3 DPU : meilleur cas 164 %, moyenne 252 %, pire cas 317 % (§VI-C).
- Temps de transfert maximaux mesurés : HP lecture 35 cycles, écriture 25 ; HPC 38 et 28 ; LPD lecture de données 146, instructions 40, écriture 74 (§VI-A, chunk 2025-zhang#015.2 et #015.3).
- Pessimisme assumé (§VI-D) : transferts maxima, deux ports de données non recouvrants, toute transaction en conflit. Relâcher ces hypothèses (R_ol, R_con) peut sous-estimer le WCET : acceptable en temps réel souple, pas en temps réel dur (§VI-D, Tables X et XI).
- Choix de la configuration des ports mémoire : le défaut Vitis AI n'est pas optimal pour la borne, d'autres configurations donnent des bornes plus serrées (§VI-E, Tables XII et XIII).
→ reportés dans `benchmarks.csv` : 2 lignes : latences mesurées en DPU seul, maximum observé sur 20 000 itérations, colonne `latency_ms` (ce n'est pas un WCET) : MobileNetV2 5,81 (§III, Fig. 4, chunk 2025-zhang#004.0) et YOLOv3 9,093 (§III, chunk 2025-zhang#004.1, `confidence: low`, l'unité ms n'étant pas écrite dans ce passage). Les rapports WCET estimé / WCET mesuré (1, 2 et 3 DPU) et la dispersion en 3 DPU restent dans cette fiche : le schéma n'a pas de colonne pour une borne ni pour un ratio.

## Limites et critique

- Le « WCET » de référence est un maximum mesuré (1 million d'exécutions) ; les auteurs notent eux-mêmes qu'il peut être inférieur au vrai pire cas (§VI-B). La sûreté de la borne repose donc sur des temps de transfert maximaux eux aussi mesurés, et sur l'absence de modèle de la DDR et du matériel DPU (non publics, §V-C1, §VI-D) : borne « sûre » sous hypothèses de mesure, pas prouvée.
- Pessimisme important en multi-DPU : 164 % à 317 % du mesuré à 3 DPU (§VI-C). Un pire cas aussi éloigné est difficilement exploitable pour une certification.
- Interférence entre DPU seulement. Les accès du processeur ARM (PS), du système d'exploitation, du post-traitement (NMS), ou d'un autre maître sur la DDR ne sont pas dans le modèle (déduit : le texte ne les mentionne pas).
- Réseaux statiques uniquement : un chemin d'exécution dépendant de l'entrée (sortie anticipée, branches) n'est pas modélisé ; l'hypothèse « charge de calcul identique quelle que soit l'image » est posée explicitement (§I, §III).
- Comparaison à [8] seulement en DPU seul, avec la configuration par défaut parce que [8] ne publie pas la sienne (§VI-B) ; en multi-DPU, aucune baseline : premier travail du genre.
- Pas de baseline GPU ou Jetson ; pas de puissance ; pas de précision (hors sujet).
- Version Vitis AI 2.0 (2021) ; la transposabilité à Vitis AI récent, à Versal ou à Kria KV260 est annoncée (« se généralise », §IV) mais non testée (déduit).

## Pertinence pour la thèse

Axe `timing-analysis`, vide jusque-là dans le corpus. Montre comment obtenir une borne de pire cas pour un CNN sur SoC FPGA avec le flux Vitis AI/DPU : décomposition en phases, interférence bornée sur la DDR partagée, configuration des ports comme levier de prédictibilité. Complète ACETONE (2022-de-albuquerque-silva-acetone-predictable-programming-framework-ml), qui calcule un WCET par OTAWA sur du code C monocœur d'une cible non représentative : ici la cible est un SoC FPGA réel, mais l'analyse dépend de la mesure, alors qu'ACETONE s'appuie sur une analyse de code statique. Les deux supposent un graphe d'exécution fixe, ce qui est le point de rupture pour les sorties anticipées. Gap « Pire cas temporel des sorties anticipées et délai de réaction de bout en bout » (`gaps.md`) : le papier apporte la brique « pire cas de l'inférence du réseau complet » sur ZCU102 (candidate pour la borne d'un chemin nominal) et le principe des segments, mais n'offre ni sorties anticipées, ni moniteur, ni délai de réaction de bout en bout, ni PS/ARM. Question du draft ARCYS (Zhang25) : réponse partielle, DPU uniquement.

## Gaps identifiés

- Pire cas d'une inférence avec sorties anticipées ou moniteur de confiance sur DPU : borne par chemin d'exécution (segments par sortie), non traité.
- Interférence PS vers PL (ARM, post-traitement) sur la DDR partagée, absente du modèle.
- Borne mesurée à vérifier sur d'autres cibles (KV260, Versal) et versions de Vitis AI.
- Borne moins pessimiste (< 164 %) : modèle de la DDR ou régulation de bande passante (cf. Restuccia sur les délais non bornés), à rapprocher des papiers de contention du corpus.

## Statut de lecture

papier complet (fulltext.md lu en entier). Tableaux sans corps extrait : TABLE I (ressources par architecture DPU), II (temps selon le type d'interface), VIII (2 DPU), XI, XII ; les Tables IV à VII, IX, X et XIII n'ont pas de corps non plus dans le texte (seules les légendes de certaines sont présentes) ; les chiffres par CNN manquent donc, seuls les chiffres du texte (meilleur cas, moyenne, pire cas) sont repris. Sections I, V, VI non détectées par l'extraction (leur texte est rattaché à la section précédente, d'où des libellés de section décalés dans `bin/pdb search`) ; les équations 4, 5, 13 sont partiellement lisibles. Déduits et non affirmés par les auteurs : les limites sur le PS/ARM et sur les chemins dépendants de l'entrée, l'extension à d'autres cartes, le rapprochement avec ACETONE et avec les sorties anticipées, l'unité ms de YOLOv3.
