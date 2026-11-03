---
id: 2026-juniar-edge-seismic-denoising-benchmarking-hailo
fiche: done
date: 2026-11-03
---

# Edge Seismic Denoising: Benchmarking the Hailo-8L on Raspberry Pi 5

Antonia Indriyani Juniar, Naura Anbiyya Faka Mursaid, Ahmad Kadarisman, Martarizal, 2026, Spektra: Jurnal Fisika dan Aplikasinya 11(2), 135–150. https://doi.org/10.21009/spektra.112.04
Type : article de journal (revue à comité de lecture d'après `metadata.json`, `type: journal`)

## Problème

Débruiter en continu des signaux sismiques sur une station de terrain à faibles ressources (Raspberry Pi 5) : les méthodes d'apprentissage profond existent mais leur déploiement sur un accélérateur edge bas coût, en flux continu, est peu étudié (Introduction). Les auteurs veulent caractériser le compromis qualité de débruitage / charge CPU / latence d'un Hailo-8L, et la perte due à la quantification INT8.

## Méthode

- Modèle AE-v4 : autoencodeur débruiteur convolutionnel de 17 185 paramètres (ONNX 70,1 Ko, HEF 868 Ko ; le texte donne aussi 0,839 Mo pour le HEF), encodeur 3 blocs Conv2D(1,k)+ReLU+MaxPool, décodeur 3 blocs Upsample(nearest)+Conv2D, sortie Tanh ; entrée 1×1×1×400 (§Model Architecture). Conv1D converti en Conv2D avec dimension fictive de hauteur 1 ; ConvTranspose remplacé par Upsample+Conv2D car incompatible avec la quantification INT8 du DFC (§Model Architecture).
- Données : station BMKG CIKJI (IA.CIKJI.00.SHZ), 23 fichiers MiniSEED de janvier 2025, 21 598 fenêtres de 400 échantillons (8 s à 50 Hz), normalisation P95 (3 819,60 counts), 55 992 paires d'entraînement par ajout de bruit gaussien synthétique (noisy = clean + 0,3 × bruit). Station TSJM utilisée uniquement pour le test inter-stations (§Data).
- Chaîne : PyTorch, ONNX (opset 18), parsing HAR, quantification INT8 avec 256 échantillons de calibration, compilation HEF (Hailo DFC 3.33.1, HailoRT 4.23.0) (§Conversion to HEF). Baseline CPU : ONNX Runtime CPUExecutionProvider (§Experimental Setup).
- Évaluation : latence (200 itérations après 200 de chauffe), tailles de lot 1 à 32, charge parallèle, flux simulé de 24 h (10 800 fenêtres), détection d'événements STA/LTA (ObsPy), test inter-stations, ablation du nombre d'échantillons de calibration.

## Plateforme et implémentation

- Raspberry Pi 5 (Cortex-A76 4 cœurs 2,4 GHz, 8 Go LPDDR4X, Debian Bookworm) + Hailo-8L AI Kit (13 TOPS, M.2 B+M, PCIe Gen3) (§Data, §Methods).
- Puissance : **estimée**, puissance système totale ; repos 0,31 W (§Methods) ; Table 2 : 3,29 W (Hailo) vs 3,49 W (CPU FP32). La méthode d'estimation n'est pas décrite ; les auteurs reconnaissent « estimated rather than directly measured power consumption » (Conclusion/limites). `power_scope` = `estimated`.
- Fréquence, ressources de la puce Hailo : n/r. Code, modèle, HEF : non mentionnés comme publiés (aucun lien dans le texte lu).

## Résultats

Tous sur CIKJI (in-distribution) sauf mention, RPi5, lot 1 sauf mention.

| Config | SNR (dB) | Pearson r | Latence moy. (ms) | Source |
|---|---|---|---|---|
| CPU FP32 | 17,08 | 0,9727 | 0,159 (Table 5) / 0,17 (Table 2) | Tables 2, 5 |
| CPU INT8 (ONNX Runtime) | 15,44 | 0,9599 | 0,353 | Table 5 |
| Hailo INT8 | 14,95 | 0,9645 | 0,267 (Table 5) / 0,27 (Table 2) | Tables 2, 5 |

- Lot 32 : Hailo 8,23 ms contre 5,04 ms CPU (accélération 0,61x), mais CPU 14,1 % contre 100 % (Table 3). Le Hailo est plus lent que le CPU à tous les lots (0,78x à 0,60x, Table 3) : surcoût PCIe, modèle trop petit (§CPU vs. Hailo-8L).
- Flux 24 h (10 800 fenêtres) : CPU moyen 14,5 % (Hailo) contre 61,4 % (FP32), latence 0,2698 contre 0,1674 ms, 748 événements STA/LTA identiques (Table 6).
- Charge parallèle (500 fenêtres) : CPU 9,0 % (Hailo) contre 42,0 % (Table 4).
- Inter-stations CIKJI → TSJM : SNR -11,14 dB (Hailo) et -11,08 dB (CPU), chute d'environ 4,3 dB ; Pearson 0,2893 / 0,2917 (Table 7).
- Calibration 128 à 1 024 échantillons : effet marginal (ΔPearson 0,003) (Table 8).
→ reportés dans `benchmarks.csv` : 9 lignes proposées (AE-v4 Hailo INT8 / CPU FP32 / CPU INT8 sur CIKJI lot 1 ; Hailo et CPU sur TSJM ; Hailo et CPU lot 32 ; Hailo et CPU flux 24 h), puissance `estimated`. Lignes écrites dans le scratchpad, pas dans `benchmarks.csv`.

## Limites et critique

- Le gain est uniquement la charge CPU ; la latence et le débit sont pires sur le Hailo (Tables 2, 3, 6), ce que le résumé et la conclusion (« increasing the inference speed ») formulent de façon contradictoire.
- Puissance estimée, système entier, méthode non décrite ; 3,29 W (Table 2) et 3,41 W (Table 3, lot 1) pour la même config Hailo ; 4,2x d'efficacité CPU présenté mais aucune mesure d'énergie directe.
- Chiffres incohérents entre tableaux : CPU Hailo 2,7 % (Table 2), 5,8 % (Table 3), 9,0 % (Table 4), 14,5 % (Table 6) ; latence CPU lot 1 0,17 / 0,21 / 0,159 ms ; SNR CIKJI 14,95 dB (Table 5) contre -6,83 dB (Table 7, même station et même Hailo) et 0,35 dB (Table 8, sous-ensemble de 500 fenêtres). Les protocoles diffèrent ou sont mal décrits ; ne pas comparer les valeurs d'un tableau à l'autre.
- Bruit synthétique gaussien ajouté à des fenêtres réelles supposées propres (proxy), donc SNR mesuré contre une référence elle-même bruitée ; pas de données de bruit réel ; l'amélioration de détection (34 contre 33 événements, un seul jour) est anecdotique.
- Un seul petit modèle (17 185 paramètres), un seul accélérateur, pas de baseline GPU/Jetson/MCU ; pas de comparaison à un débruiteur de référence (DeepDenoiser, U-Net) faute de compatibilité Hailo.
- Généralisation faible : Pearson 0,29 sur TSJM, réentraînement par station nécessaire.
- Reproductibilité : pas de dépôt de code mentionné ; texte extrait partiellement désordonné.

## Pertinence pour la thèse

Pertinence pour SerreIA (axe `edge-inference`) : donnée de référence sur le même matériel cible (Raspberry Pi 5 + Hailo-8L, HailoRT/DFC INT8), pas sur des plantes. Enseignements transférables : (1) contraintes du DFC (pas de Conv1D, ConvTranspose incompatible avec INT8 ; Upsample+Conv2D et dimension fictive) ; (2) pour un petit modèle, le Hailo n'accélère pas mais décharge le CPU (14,5 % contre 61,4 % en flux continu), utile quand le Pi 5 doit aussi faire MQTT, acquisition et agent ; (3) la quantification INT8 coûte ~2 dB de SNR ici, calibration peu sensible entre 128 et 1 024 échantillons ; (4) piège de mesure : surcoût PCIe à petite taille de lot. Ne répond pas à la latence de classifieurs de vision (EfficientNet-B0) ni à la quantification sur images ; à ne pas comparer à des FPS d'images.

## Gaps identifiés

- Pas de mesure de puissance directe du Hailo-8L sur Pi 5 (ici estimée) : à mesurer au wattmètre pour SerreIA.
- Latence/CPU du Hailo-8L pour un classifieur de feuilles (EfficientNet-B0 INT8) toujours à mesurer ; ce papier ne couvre qu'un modèle de 17 k paramètres.
- Effet de la charge concurrente (MQTT, agent LLM) sur un pipeline vision + Hailo : seul le cas acquisition + débruitage est testé.

## Statut de lecture

Papier complet (`fulltext.md` lu en entier ; backend `grobid`, `ok: true`). Le texte extrait est partiellement désordonné (phrases coupées dans §Experimental Setup et Results, tableaux 1 et 8 listés « sans corps extrait » dans `extraction.warnings` mais leur contenu apparaît dans le texte) ; les chiffres des Tables 2 à 8 sont lus dans leur corps de tableau extrait et recoupés avec le texte quand il les répète. Table 3 : colonnes lues telles quelles (en-tête mal formé).
Ce qui suit est déduit et non affirmé par les auteurs : l'attribution `power_scope` = `estimated` (le texte dit « estimated » sans détailler la méthode) ; la formulation « SNR mesuré contre une référence elle-même bruitée » ; les pistes de transfert vers SerreIA ; l'absence de code publié (aucun lien lu).
