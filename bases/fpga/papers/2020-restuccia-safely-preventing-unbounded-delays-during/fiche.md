---
id: 2020-restuccia-safely-preventing-unbounded-delays-during
fiche: done
date: 2026-11-03
---

# Safely Preventing Unbounded Delays During Bus Transactions in FPGA-based SoC

Francesco Restuccia, Alessandro Biondi, Mauro Marinoni, Giorgio Buttazzo, 2020, 2020 IEEE 28th Annual International Symposium on Field-Programmable Custom Computing Machines (FCCM) 129-137. https://doi.org/10.1109/FCCM48280.2020.00026
Type : conférence (FCCM 2020, relu par les pairs)

## Problème

Les SoC FPGA du commerce échangent leurs données par AXI, dont le standard n'impose aucun mécanisme pour détecter un maître défaillant (§IV). Un seul accélérateur matériel (HW-task) peut donc retarder le bus sans limite et bloquer tout le système, jusqu'au reset (§I, §IV). Cela interdit toute garantie temporelle a priori, exigée pour la certification, surtout avec des IP tierces non validées, la reconfiguration partielle dynamique (DPR) ou des fautes silicium (§I).

## Méthode

- Démonstration du blocage (§IV) : deux traffic generators HW0 et HW1 derrière l'AXI SmartConnect ; HW0 émet une adresse d'écriture (AW) sans fournir les données (W). AXI interdisant l'entrelacement des écritures, W1 reste bloqué derrière W0, indéfiniment (Fig. 1). Même blocage possible en lecture (non détaillé).
- Analyse de pire temps de réponse (§V-VI) pour des HW-tasks périodiques (N^R, N^W transactions, burst B, calcul C cycles, période T, échéance = période) derrière un interconnect à arbitrage round-robin de granularité φ_I. Temps d'accès d'une transaction (Éq. 1-2), deux bornes incomparables du nombre de transactions interférentes (Éq. 3 et 4, combinées par min en Éq. 5), puis RT = Δ^R + C + Δ^W (Éq. 6-8). Lecture, écriture et calcul sont supposés sérialisés (pire cas). La latence du contrôleur DDR est modélisée grossièrement par d^read_PS et d^write_PS, obtenues par profilage.
- AXI Stall Monitor (ASM, §VII), IP HDL placée entre chaque HW-task et l'interconnect. Un « cycle bloqué » est détecté sur RVALID/RREADY, WREADY/WVALID, BVALID/BREADY. Un compteur à budget est réapprovisionné périodiquement (période commune, budget par ASM, registres mappés par le PS). Mode monitor : transparent, sans latence. Budget épuisé : mode decouple, qui lève une interruption, découple la HW-task, vide les lectures en attente et termine les écritures en attente avec des données factices. Le PS décide de la réadmission.
- Configuration des budgets (§VII-A) : période ASM = max des périodes ; sûr si Σβ_i ≤ S_min/2 (S_min = plus petite marge T_i - RT_i). Implémenté dans un driver (PS) qui peut reconfigurer les ASM à l'exécution.

## Plateforme et implémentation

- Zynq-7000 Z-7020 et Zynq UltraScale+ ZU9EG ; seuls les résultats du Z-7020 sont montrés, ceux des deux SoC étant dits « comparables » (§VIII). Fréquence d'horloge : n/r.
- HW-tasks : IP Xilinx AXI FFT, AXI DMA, AXI FIR ; SW-tasks périodiques sous FreeRTOS sur le PS ; ILA pour profiler la latence de l'interconnect, d_PS, φ et C (§VIII-A).
- Ressources d'un ASM (Table III, reconstruite par PyMuPDF) : Z-7020 185 LUT (0,35 %), 203 FF (0,19 %), 0 BRAM/DSP ; ZU9EG 183 LUT (0,07 %), 203 FF (0,04 %), 0 BRAM/DSP.
- Code, bitstream, driver : non publiés (aucun lien dans le texte). Puissance : n/r.

## Résultats

- Sans ASM, une HW-task qui n'envoie jamais ses données bloque tout le système : temps de réponse non borné pour les autres tâches (expérience ii, §VIII-C ; Fig. 1).
- Avec ASM, temps de réponse mesurés identiques avec et sans ASM en nominal (expériences i et iii) : l'ASM n'ajoute pas de latence mesurable (§VIII-C).
- Avec HW_DMA défaillante et ASM actifs (expérience iv), FFT et FIR respectent leurs échéances, quelle que soit la répartition du budget (§VIII-C, Fig. 4). La répartition (b) (90 % du budget à DMA) donne des temps plus grands que (a) (linéaire en période) pour FFT et FIR. Les valeurs numériques de Fig. 4 ne sont pas dans le texte (échelle log, figure sans légende identifiée) : n/r.
- Bornes analytiques (§VIII-B) : RT_FFT = 12,6 ms, RT_DMA = 1,3 ms, RT_FIR = 24,2 ms ; ensemble jugé ordonnançable. Périodes (Table I, extraction dégradée) : FFT 50, DMA 20, FIR 30 ms. Budget global annoncé 8,7 ms = 17,4/2, période de réapprovisionnement 50 ms. Y^R=Y^W : FFT 5120, DMA 512, FIR 8960.
- Paramètres profilés (Table II, PyMuPDF) : φ_I=1, d^addr_I=12, d^data_I=9, d^bresp_I=9, d^read_PS=50, d^write_PS=40 (cycles).
→ reportés dans `benchmarks.csv` : 2 lignes (coût en ressources de l'ASM, Z-7020 et ZU9EG, Table III, confidence medium). Les temps de réponse et paramètres de bus ne tiennent pas dans les colonnes de `benchmarks.csv` (pas de FPS, ni de précision) : restés dans cette fiche. Le `task` « bus monitoring » est hors vocabulaire usuel ; ces lignes n'ont ni FPS ni puissance.

## Limites et critique

- Évaluation faible : un cas d'étude de 3 IP Xilinx, une seule défaillance injectée (DMA qui n'envoie pas ses données en écriture) ; pas de lecture bloquée, ni de ralentissement partiel, ni de fautes réelles. Aucune comparaison avec une autre solution (les travaux voisins sont passifs, §II).
- Incohérence apparente (déduit) : la marge S_FIR = T_FIR - RT_FIR = 30 - 24,2 = 5,8 ms d'après Table I (extraction dégradée) et §VIII-B serait inférieure à 17,4 ms utilisé pour le budget (8,7 ms). Soit T_FIR de Table I est mal extraite, soit le budget est incorrect : à vérifier sur le PDF avec `/table-review`.
- Le modèle d'analyse est coarse-grained pour le DDR (latences pire cas profilées, pas de garantie formelle ; pessimisme non quantifié : la borne n'est pas comparée aux mesures autrement que graphiquement). Les valeurs profilées ne sont pas prouvées pires cas.
- Hypothèses : mémoire privée par HW-task, tâches périodiques à échéance = période, serialisation lecture/écriture/calcul, un seul port FPGA-PS partagé.
- La sortie du mode decouple rend le résultat de la tâche invalide (corrompu) : le papier ne traite pas la reprise applicative au-delà d'une décision laissée au PS.
- Détection fondée sur le comportement du bus seulement : ne détecte pas une erreur de calcul ou de donnée d'un accélérateur.
- Aucun chiffre pour des accélérateurs DNN : les HW-tasks sont FFT, DMA et FIR.

## Pertinence pour la thèse

Axe `timing-analysis` : référence directe pour le délai de réaction de bout en bout d'un accélérateur sur SoC FPGA (WCET, interférences de bus, thème Lauer) et pour la distinction entre défaillance temporelle et erreur de perception (thème ARCYS). Le principe (budget de cycles bloqués, découplage, interruption vers le PS, analyse d'ordonnançabilité) s'applique à un accélérateur YOLO tiers ou reconfiguré (DPR) partageant un port DDR avec d'autres IP. Ouvert : l'analyse ne couvre pas les accélérateurs DNN réels (bursts longs, double buffering, plusieurs ports HP), ni le coût de reprise après découplage pour un flux vidéo de sécurité. Axe `platforms` pour le comportement de l'AXI SmartConnect sur Zynq-7000 et ZU+.

## Gaps identifiés

- Analyse de pire temps de réponse appliquée à un accélérateur DNN (YOLO) sur SoC FPGA, avec le bruit du DDR mesuré, pas seulement profilé.
- Effet d'un découplage ASM sur la sûreté applicative (frame perdue, état dégradé) : non traité.
- Interactions entre monitorage de bus et monitorage de perception (faux négatif critique) : absentes.

## Statut de lecture

Papier complet (fulltext.md lu en entier ; `extraction.backend` = grobid, ok). Réserves d'extraction : Table I déformée (cellules fusionnées) ; Table II et Table III reconstruites par PyMuPDF, chiffres recoupés avec le texte seulement pour RT et Y (§VIII-B), pas pour les ressources ; Fig. 4 sans légende identifiée et sans valeurs numériques extraites ; équations 1 et 2 partiellement tronquées.
Ce qui suit est déduit et non affirmé par les auteurs : incohérence de marge S_FIR ; absence de publication du code (aucun lien trouvé) ; portée limitée de l'évaluation.
