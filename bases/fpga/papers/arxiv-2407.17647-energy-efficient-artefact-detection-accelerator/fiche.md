---
id: arxiv-2407.17647-energy-efficient-artefact-detection-accelerator
fiche: done
date: 2026-09-29
---

# An Energy-Efficient Artefact Detection Accelerator on FPGAs for Hyper-Spectral Satellite Imagery

Cornell Castelino, Shashwat Khandelwal, Shanker Shreejith, Sharatchandra Varma Bogaraju, 2024, 27th Euromicro Conference on Digital System Design (DSD), 2024. https://arxiv.org/abs/2407.17647
Type : conférence (DSD 2024) ; version arXiv lue, `journal_ref` indiqué par arXiv.

## Problème

Les images hyperspectrales (HSI) prises par des CubeSats contiennent souvent des artefacts (nuages, capteur défaillant) ; les transmettre gaspille l'énergie et la fenêtre de liaison descendante. Les détecteurs embarqués existants sont des CNN supervisés ciblés sur les nuages (§I). Les auteurs veulent un détecteur d'artefacts/anomalies non supervisé, généraliste et assez léger pour un CubeSat.

## Méthode

Autoencodeur convolutif 2D (CAE) non supervisé, 2,95 M de paramètres, entrée 144x144 (§III-B, §III-C), entraîné 2000 epochs (Adam, lr 0,001, MSE, BatchNorm). Décision artefact/normal par seuil sur une erreur de reconstruction personnalisée R_err = MSE + k·MSLE ; seuil ≈ 70000 choisi pour maximiser le F1 (§III-D). Quantification INT8 uniforme (poids, biais, activations) par Vitis-AI avec fine-tuning post-quantification de 50 epochs (§IV). Déployé sur un DPU B4096 générique (pas de RTL propre) : les poids se mettent à jour (≈ 2 Mb) sans regénérer le bitstream (≈ 23 Mb) (§IV). Entraînement sur IP et SV, test sur UP et KSC (Conclusion).

## Plateforme et implémentation

- Puce : XCZU7EV (Zynq UltraScale+) sur ZCU104 ; DPU B4096, 300 MHz interface, 600 MHz cœur DSP ; Linux PetaLinux, VART (§IV).
- Ressources (% du XCZU7EV) : LUT 27,17 ; FF 25,03 ; DSP 40,74 ; BRAM 35,42 / URAM 47,92 (Table VI, corps reconstruit par Docling, à vérifier). Valeurs absolues n/r.
- Puissance : 5,38 W actif (idle 4,6 W) mesurés via les rails PMBus par PYNQ-PMBus (§IV-B, Table VI) : portée puce (rails), pas carte entière.
- Baseline : Jetson Xavier NX en mode 10 W, torch2trt FP16 et INT8 ; énergie par jtop (§IV, §IV-B).
- Code/bitstream : non publiés (aucun lien dans le texte).

## Résultats

- Modèle INT8 fine-tuné : accuracy 98,70 %, F1 92,77 %, FNR 13,48 %, FPR 0 % (Table III) ; FP32 : F1 94,05 % ; INT8 PTQ seul : F1 0 % (effondrement, Table III) ; INT8 PyTorch/Jetson : F1 95,29 % (§IV-A).
- Latence 4,0 ms, 250 images/s (moyenne de 1000 runs, §IV-B) ; 21,52 mJ par inférence (§IV-B).
- Jetson Xavier NX : INT8 10,36 ms / 96,52 FPS / 7,6 W ; FP16 19,09 ms / 52,38 FPS / 8,2 W (Table VI). Soit 2,6x et 4,7x de latence, 3,6x et 7,2x d'énergie (§IV-B).
- Vs CloudSatNet (Zynq-7020, INT4) : 1,27x en latence, 7,5x en énergie (§IV-B) ; accuracy 98,70 contre 94,84 (Table V).
→ reportés dans `benchmarks.csv` : 3 lignes (ZCU104 INT8, Xavier NX INT8, Xavier NX FP16), fournies dans `bench_rows.csv`.

## Limites et critique

- Le F1/FPR de 0 % vient d'un seuil choisi sur les mêmes données que celles qui servent à l'évaluation (« threshold found by testing against held-out test dataset », §III-C) : risque d'optimisme ; jeu de test très déséquilibré (837 anomalies pour 79-89 normales, Table IV, reconnu dans la Conclusion).
- Comparaison à CloudScout/CloudSatNet biaisée : jeux de données différents (RGB nuages contre HSI, Table I), tâches différentes, plateformes différentes, précisions différentes (INT4/FP16).
- Comparaison à Jetson : les puissances ne sont pas de même portée (rails PMBus contre jtop, dont la portée exacte n'est pas dite) ; la Jetson est bridée à 10 W, GPU à 510 MHz.
- Fragilité de la quantification : INT8 PTQ pur donne F1 = 0 (Table III) ; le fine-tuning est indispensable. Pas de SEU/radiations testés malgré le contexte spatial.
- « Artefact » n'est pas défini de façon opérationnelle (nuages, distorsions, changements spectraux) ; « FPR 0 % » signifie zéro artefact manqué, au prix de 13,48 % de FNR.
- Table VI (corps Docling) : chiffres cohérents avec le texte (4 ms, 5,38 W, 21,52 mJ).

## Pertinence pour la thèse

Cas d'usage d'un autoencodeur sur image sur FPGA (axe `autoencoder-fpga`, gap identifié dans CLAUDE.md), via le DPU et Vitis-AI, donc chaîne outillée simple. Intéressant pour la surveillance à l'exécution : l'erreur de reconstruction comme score d'anomalie/OOD est le principe d'un moniteur de sûreté. Le choix « zéro faux positif » (ici zéro artefact manqué) illustre un réglage de seuil orienté sûreté. Ne traite ni fiabilité, ni certification, ni personnes ; le DPU est une boîte noire peu adaptée à la traçabilité.

## Gaps identifiés

- Autoencodeur sur image en INT8 sur FPGA : F1 rapporté sans validation croisée ni jeu équilibré.
- Aucune évaluation de la tolérance aux fautes (SEU) d'un CAE sur DPU malgré un contexte spatial.
- Effondrement de l'INT8 PTQ (F1 = 0) : quantification d'autoencodeurs à étudier pour la certification.

## Statut de lecture

Papier complet (fulltext.md lu en entier). Table I, Table VI reconstruits par Docling : chiffres recoupés avec le texte pour latence, puissance, énergie. Texte tronqué par endroits (§III-B, §III-C : détails de l'architecture et du découpage des données absents ; la contribution 1 seule est listée). Déduit et non affirmé par les auteurs : portée `chip` de la puissance (déduite de « PYNQ-PMBus power rails ») ; risque d'optimisme du seuil ; biais de comparaison.
