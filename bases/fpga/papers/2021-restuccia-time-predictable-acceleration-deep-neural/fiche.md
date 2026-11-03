---
id: 2021-restuccia-time-predictable-acceleration-deep-neural
fiche: done
date: 2026-11-03
---

# Time-Predictable Acceleration of Deep Neural Networks on FPGA SoC Platforms

Francesco Restuccia, Alessandro Biondi, 2021, 2021 IEEE Real-Time Systems Symposium (RTSS) 441-454. https://doi.org/10.1109/RTSS52674.2021.00047
Type : conférence (RTSS 2021, relu par les pairs)

## Problème

Les DNN de perception (ADAS, robots, automatisation d'usine) exigent une accélération matérielle sous contraintes temporelles. Les GPU commerciaux sont peu prédictibles et peu documentés (§I) ; les SoC FPGA le sont davantage, mais le DPU de Xilinx (Vitis AI), accélérateur DNN le plus mûr selon les auteurs, est une IP fermée dont le comportement interne n'est pas public (§II-D). Aucune borne de temps de réponse n'existait pour un DNN exécuté par le DPU : les outils Xilinx (profileur Vitis AI, System ILA) visent la performance moyenne (§IX). Les auteurs se disent les premiers à traiter la prédictibilité temporelle des DNN sur FPGA (§VIII).

## Méthode

- Campagne de profilage du DPU avec un profileur matériel multicanal, branché en parallèle sur les ports AXI et l'interruption du DPU, sans perturber l'exécution (§III). Six DNN d'ADAS (détection de voie VpgNet, détection et reconnaissance de plaque, détection d'objets YOLOv3 et SSD, détection de piétons SSD), 1000 exécutions chacun, images tirées de Cityscapes (§III).
- Observations (§III-C) : le DPU ne communique avec le logiciel qu'à la configuration ; son trafic bus est constant d'un job à l'autre (variation < 0,1 %) et indépendant de l'image ; les phases lecture d'instructions et écriture sont recouvertes à au moins 97-98 % par la lecture de données (Fig. 2) ; fluctuations de temps de réponse limitées (Table II). Parallélisme des ports : M_DATA 14 lectures et 7 écritures en attente, M_INS 2 lectures ; rafales de 1 à 256 mots sur M_DATA, 4 mots sur M_INS (§III-A).
- Modèle série-parallèle du DPU : la lecture de données s'exécute en parallèle des phases instructions + écriture, suivie d'une phase de calcul pur « elaboration » (§IV-A, Fig. 4). Modèle d'interconnexion AXI et de contrôleur DRAM grossier : un retard cumulé maximal par transaction (d_read_DRAM, d_write_DRAM, d_read_OCM) qui englobe aussi, de façon pessimiste, l'interférence des processeurs du PS (§IV-C).
- Analyse de temps de réponse : lemmes 1 à 3 puis théorème 1, T = max(D_R_data, D_R_ins + D_W_data) + D_elab (éq. 7, §V). L'interférence entre les deux ports de lecture du DPU lui-même (auto-interférence) est bornée par min(N_INS · N_DATA_outs, N_DATA · d_read_DRAM) (éq. 3).
- DICTAT (DPU Instruction Dump - Address Translator) : IP en HDL entre M_INS et l'interface FPGA-PS, qui capture les instructions du DPU puis redirige leur lecture vers la mémoire sur puce (OCM, 256 Ko) ; découple M_INS de M_DATA et supprime l'auto-interférence ; sans latence ajoutée, transparent pour le DPU (§VI). Borne affinée par l'éq. 9.

## Plateforme et implémentation

ZCU102, Zynq UltraScale+ ; DPU d'architecture par défaut (version 3.3) de Vitis AI 1.3.2, horloge DPU 330 MHz (DRAM à 1067 MHz) ; quantification INT8 du flux Vitis AI (§II-C, §III). Ressources (Table IV) : DPU 108134 LUT, 1394 DSP, 518 BRAM ; DICTAT 374 LUT, 0 BRAM, 0 DSP ; profileur 256 LUT ; System ILA 21877 LUT. Puissance : n/r (non mesurée). Code, profileur et DICTAT : non publiés (aucun lien dans le texte). Charge PS : image Petalinux stock avec une seule application qui accélère des DNN (§VII-B) ; pas de charge concurrente sur les cœurs ARM.

Paramètres profilés (§VII-B, chunk 2021-restuccia#028.1) : d_addr = d_bresp = 1 cycle, d_word = 1 (lecture) ou 2 (écriture) ; d_read_DRAM = 40, d_write_DRAM = 30, d_read_OCM = 40 cycles de l'horloge DPU (330 MHz), soit 130, 96 et 130 cycles côté DRAM.

## Résultats

- Les bornes de temps de réponse sont toujours sûres (jamais dépassées par la mesure) et « pas excessivement pessimistes » selon les auteurs, avec le plus de pessimisme sur les phases lecture d'instructions et lecture de données (§VII-C, Fig. 5). Les valeurs numériques de la Fig. 5 ne sont pas dans le texte extrait : écart borne / mesure en pourcentage, n/r.
- Temps d'inférence mesurés, DPU stock, maximum sur 1000 exécutions (Table II) : Lane Detect 7,12 ms, Plate Detect 0,75, Plate Num 3,07, YOLOv3 8,02, SSD objets 8,41, SSD piétons 9,12 ms. Variabilité faible : écart min/max de 0,03 ms pour YOLOv3 (7,99 à 8,02) (Table II, chunk 2021-restuccia#044.1).
- Avec DICTAT (instructions en OCM, Table III, chunk 2021-restuccia#045.0) : YOLOv3 7,99, SSD 8,38, SSD piétons 9,11, Plate Detect 0,71, Plate Num 3,05 ms (maximum). Gain de performance faible (jusqu'à environ 6 % sur Plate Detect), mais la phase de lecture d'instructions gagne au moins 50 %, jusqu'à 62 % (YOLOv3) et 64 % (SSD) sur le maximum (§VII-D). Variabilité réduite.
- Resserrement de la borne grâce à l'OCM : pessimisme réduit d'au moins 12 % sur la borne du temps total, et de 25 % pour YOLOv3 et SSD piétons, par rapport à la borne tout-DRAM (§VII-D, chunk 2021-restuccia#030.2). Il s'agit d'un gain de DICTAT sur la propre borne des auteurs, pas d'une comparaison à un autre papier.
- Le modèle Lane Detect n'a pas pu être testé avec DICTAT : ses instructions dépassent l'OCM de 256 Ko du ZU+ (Table I : 275 Ko), ce que la Versal (OCM de 4 Mo) lèverait (§VII-D).
- Trafic bus par job, Table I : par exemple YOLOv3 84410 transactions de lecture de données (15,44 Mo lus) et 25457 d'écriture (8,24 Mo).
→ reportés dans `.cache/bench/2021-restuccia-time-predictable-acceleration-deep-neural.csv` (12 lignes, `benchmarks.csv` non touché) : 6 latences mesurées en config stock (Table II), 5 latences avec instructions en OCM (Table III), toutes en `latency_ms` = maximum observé sur 1000 exécutions (pas un WCET) ; 1 ligne de ressources du DPU (Table IV). Les bornes analytiques (WCET estimé) et le d_read / d_write ne vont pas dans le tableau : le schéma n'a pas de colonne de borne (cf. suggestion déjà en attente pour Zhang25).

## Limites et critique

- Borne « sûre » sous hypothèses de mesure : les paramètres d_read_DRAM, d_write_DRAM, d_read_OCM sont profilés, pas dérivés d'une documentation (non publique, §IV-C), et le modèle du DPU repose sur de l'observation d'une IP fermée (§IX). Les auteurs proposent de surveiller en ligne que les valeurs restent sous celles du profilage (§V). La borne n'est donc pas prouvée, comme celle de Zhang25.
- Interférence PS vers PL non modélisée : les 40 et 30 cycles ont été estimés avec une seule application Vitis AI active, sans autre charge mémoire sur les ARM ; l'interférence des processeurs est « pessimistement » englobée dans ces constantes, qui ne sont donc pas valables pour un PS chargé (§VII-B, §IX.3). Le modèle de DDR est grossier : toutes les transactions sont servies en série, sans parallélisme de banques (§IV-C, §VII-C).
- Un seul DPU et un seul DNN à la fois (« au plus une instance d'inférence en attente », lemme 3) : pas de multi-DPU, pas de contention entre accélérateurs, ce que traite Zhang25.
- Pas de valeur numérique du pessimisme global (Fig. 5 uniquement) ni de comparaison à une autre analyse : seule baseline, la propre borne DRAM des auteurs. DICTAT demande de capturer les instructions et de les charger dans l'OCM, avec un driver DPU non configurable (§VI) ; non testé sur Versal ni sur une version récente de Vitis AI (1.3.2, 2021).
- Réseaux convolutifs statiques uniquement : le trafic bus constant et indépendant de l'image (§III-C) est mesuré sur des DNN sans branche dépendant de l'entrée. Un réseau à sortie anticipée n'est pas traité (déduit : non mentionné).
- Pas de précision, pas de puissance, pas de baseline GPU ou Jetson ; les latences mesurées sont des maximums observés, pas des FPS de débit.

## Pertinence pour la thèse

Axes `platforms` et `timing-analysis` ; `toolflows` pour le DPU Vitis AI, au cœur de la méthode. Référence fondatrice de la borne de temps de réponse d'un CNN sur SoC FPGA : c'est le travail [8] de Zhang25 (2025-zhang-wcet-estimation-cnn-inference-fpga), « analyse statique pour 1 DPU », que Zhang25 dit resserrer de plus de 27 % en moyenne en DPU seul (§VI-B, Fig. 10 de Zhang25 ; non vérifiable ici : Restuccia ne publie pas ses valeurs de borne dans le texte, et Zhang25 relève lui-même qu'il a dû prendre la configuration par défaut faute de celle de [8]). Modèle commun aux deux : phases lecture d'instructions, lecture de données, écriture, calcul pur ; la différence est que Zhang25 passe en multi-DPU avec contention PL, PS et arbitre DDR, tandis que Restuccia se limite à l'auto-interférence d'un DPU et au levier DICTAT. Points repris : l'OCM comme levier de prédictibilité (borne resserrée de 12 à 25 %) et le constat d'un trafic bus indépendant de l'image.

Avec les deux fiches Restuccia 2020 déjà dans la base : 2020-restuccia-safely-preventing-unbounded-delays-during (ASM, régulation de bande passante et blocage d'une tâche matérielle défaillante) et 2020-restuccia-modeling-analysis-bus-contention-hardware (borne analytique de contention AXI sur interconnect pour des accélérateurs génériques). Ce papier de 2021 applique cette lignée à un accélérateur DNN commercial réel : constantes de retard du PS (d_read_PS=50 et d_write_PS=40 en 2020, 40 et 30 cycles ici, horloges et plateformes différentes : ne pas comparer) et même hypothèse d'un contrôleur DRAM boîte noire. Il n'utilise pas la régulation de bande passante (ASM) de 2020, que Zhang25 évoquait comme piste pour une borne moins pessimiste.

Gap « Interférences PS / PL et DDR non modélisées pour un accélérateur CNN » (`gaps.md`) : ce papier en est l'illustration première, avec un d_DRAM mesuré sans charge ARM et explicitement laissé en « future work » (§IX.3) ; il confirme le gap plus qu'il ne le comble. Gap « Pire cas temporel des sorties anticipées et délai de réaction de bout en bout » : apporte la brique « pire cas du réseau complet sur DPU » (borne d'un chemin nominal), avec la même prémisse de graphe fixe que Zhang25 ; aucune sortie anticipée, aucun moniteur, aucun délai de bout en bout.

## Gaps identifiés

- Valeurs de d_DRAM sous charge du PS (ARM, post-traitement NMS) : papier mesuré sans charge ; aucune borne combinée PS + DPU.
- Pessimisme global de la borne de Restuccia absent du texte (Fig. 5) : le « 27 % » de Zhang25 reste à recouper sur l'image de la figure.
- Borne par chemin d'exécution pour un réseau à sorties anticipées : prémisse de trafic constant indépendant de l'entrée à vérifier pour chaque branche.
- Reproduction sur Versal / KV260 et Vitis AI récent : DICTAT et profileur non publiés.

## Statut de lecture

Papier complet (fulltext.md lu en entier, extraction GROBID `ok`). Fig. 5 (bornes contre mesures) et Fig. 2 non lisibles dans le texte : les écarts de pessimisme par modèle sont n/r, seuls les pourcentages écrits dans le texte (12 %, 25 %) sont repris. Tables II et III recoupées avec le texte (62 % et 64 % de réduction de la phase instructions) ; l'attribution des lignes de la Table II est cohérente. Ce qui suit est déduit et non affirmé par les auteurs : l'absence de traitement des sorties anticipées ; la non-publication du code (pas de lien dans le texte) ; l'identité exacte entre ce papier RTSS 2021 et la référence [8] de Zhang25 (la fiche de Zhang25 la nomme « Restuccia et Biondi, [8] », sans titre) ; la comparaison avec les constantes de 2020.
