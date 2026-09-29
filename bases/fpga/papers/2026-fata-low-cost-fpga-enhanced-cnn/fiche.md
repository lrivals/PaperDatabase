---
id: 2026-fata-low-cost-fpga-enhanced-cnn
fiche: done
date: 2026-09-29
---

# Low-Cost FPGA-Enhanced CNN Accelerator for Real-Time YOLO Object Detection and Classification

John S. Fata, Wafa M. Elmannai, 2026, IEEE Access 14, 34614-34642. https://doi.org/10.1109/ACCESS.2026.3669451
Type : article de journal

## Problème

Les accélérateurs CNN sur FPGA à bas coût excellent sur une seule métrique (débit, précision ou puissance) : la mémoire on-chip est minuscule et la plupart des designs dépendent de la DDR, ce qui pénalise débit et consommation (§I, §II). Les auteurs veulent un YOLO temps réel équilibré (débit, latence, puissance, précision) sur une Kria KV260 sans accès DDR (hors débordement).

## Méthode

Trois contributions (§I, §III) :
1. Élagage structuré itératif : importance d'un filtre = somme des |poids| (L1), filtres groupés par 8 pour s'aligner sur le DPU, taux d'élagage par couche croissant avec la profondeur (Eq. 1.3), 5 % par itération jusqu'à 70 %, 10 époques de fine-tuning par itération sur 6 000 images (§IV-C).
2. QAT INT8 : facteur d'échelle par couche déduit d'un percentile de clipping (90e, 95e ou 99e), fake-quantization en passe avant, mise à jour de l'échelle par descente de gradient (Eq. 2.1-2.10), 600 images de calibration, lr 1e-4 (§IV-D).
3. Contrôleur mémoire RTL (Verilog) placé entre le DPU et la mémoire : couches 1-10 en BRAM, 11-21 en URAM, repli sur l'autre mémoire puis sur la DDR en cas de débordement, bursts AXI 128 bits (Table 2, Algorithm 3, §IV-E).
Modèle : YOLOv3-Tiny modifié (19 couches cachées au lieu de 21, 75 filtres de sortie, 20 classes), entraîné sous Darknet puis converti en TensorFlow (.h5), exporté en ONNX. Toolflow : Vivado + Vitis AI 2.5 (`vai_c_xir` avec `arch.json` modifié, VART), image Petalinux (§IV-F).

## Plateforme et implémentation

Kria KV260, Zynq UltraScale+ MPSoC XCK26, DPUCZDX8G, 144 blocs BRAM (648 KB) et 64 blocs URAM (~2,25 MB), 4 Go DDR4 (Table 6, §IV-E). Horloge 250 MHz (§IV-E). Utilisation : LUT 82,5 %, FF 44,5 %, DSP 96,4 %, BRAM 100 %, URAM 100 % (Table 9) ; nombres absolus n/r. Puissance : « outil de gestion de plateforme Xilinx » et capteur on-chip, moyenne de 10 vidéos de 1 min à 60 FPS (§V-B) ; portée exacte (puce ou carte) non précisée. Code et bitstream : non publiés (aucun lien dans le texte).

## Résultats

- Modèle : 33,9 MB -> 10,17 MB (élagage) -> 2,54 MB (élagage + INT8), soit 13,3x (Table 5).
- Précision sur le test VOC2012 : accuracy 93,8 %, precision 95,3 %, recall 92,4 %, F1 93,8 % (Table 7). Pas de mAP.
- Matériel (moyenne sur 10 vidéos) : 24,3 FPS, latence 41,59 ms, 60,18 GOPS, 2,13 W, 28,2 GOPS/W (Table 8) ; 11,41 FPS/W (Table 10).
- Comparaison, même modèle compressé (Table 10) : CPU i7-11700K 6,08 FPS / 79 W ; GPU RTX 2070 44,64 FPS / 150 W ; DPU 24,3 FPS / 2,13 W (mesure CPU/GPU : puissance loguée avant/après le test).
- Travaux low-cost (Table 11) : meilleure efficacité FPS/W (11,41), 1,7x le plus proche ; Kim et al. gardent la meilleure GOPS/W (43,9) avec 9,17 FPS.
→ reportés dans `benchmarks.csv` (via `bench_rows.csv`) : 1 ligne (confidence `medium` : tableaux Docling, valeurs recoupées avec le texte et l'abstract).

## Limites et critique

- « Accuracy » définie par (TP+TN)/(TP+TN+FP+FN) (Eq. 4) : notion mal définie pour de la détection (que sont les TN ?) et non comparable aux mAP@0.5 des autres papiers YOLO. Pas de baseline FP32 non compressée : la perte due à l'élagage + INT8 n'est pas quantifiée.
- Incohérences : l'ensemble de test compte 2 308 images (§IV-A) mais §V-A parle de « 3 800 images de test » sur « 20 époques, batch 32 » (test répété ?). Comparaison entre travaux hétérogènes (jeux de données MNIST, CIFAR10, BSTLD, DOTA, Corsican Fire vs VOC2012 ; modèles ResNet-20, U-Net…) : le classement en FPS/W n'est pas iso-tâche.
- Puissance : portée non précisée ; CPU/GPU mesurés autrement (avant/après test, système entier probable, déduit) ; pas de puissance de repos. Le « 70x / 37x » du texte est donc peu robuste. Le GPU fait 44,64 FPS contre 24,3 : la KV260 n'est pas plus rapide.
- Modèle utilisé pour l'évaluation matérielle : 416x416, 24,3 FPS, et la seule évaluation qualitative (Fig. 10-11) ; pas de test hors distribution ni de robustesse.
- Reproductibilité : pas de code, pas de bitstream ; le contournement de l'allocation mémoire du compilateur Vitis AI via `arch.json` n'est décrit que qualitativement.
- Sûreté : aucune analyse de fiabilité (le papier cite la tolérance aux fautes comme travail futur, §VI), pas de déterminisme temporel démontré (latence variable selon vidéo, Fig. 14).

## Pertinence pour la thèse

Cas de référence utile et récent d'un YOLOv3-Tiny INT8 sur KV260 avec DPU, donc sur une cible proche de celle d'un cas vidéosurveillance (classe `person` de VOC, Fig. 11 : 13 personnes détectées). Il apporte une recette de compression (élagage aligné DPU + QAT) et l'idée du contrôle explicite de la mémoire on-chip, qui favorise un temps d'exécution plus prédictible (déduit, non affirmé par les auteurs). Il n'aborde ni certification, ni SEU, ni surveillance à l'exécution : le seul lien sûreté est la piste « fault-tolerant mechanism » en perspective. Un contrôleur RTL custom greffé sur un DPU propriétaire complique la qualification.

## Gaps identifiés

- Aucune évaluation de sûreté (SEU, injection de fautes, déterminisme du WCET) sur un YOLO sur DPU/KV260.
- Métriques de détection standards (mAP) et perte de précision de la compression non mesurées : comparabilité limitée.
- Puissance : portée de mesure non précisée (cf. gap `power_scope`).

## Statut de lecture

Papier complet (fulltext.md lu en entier, y compris Tables 1-11 reconstruites par Docling : chiffres à vérifier, recoupés avec le texte).
Déduit et non affirmé par les auteurs : la portée de puissance (laissée `unspecified`), l'effet sur la prédictibilité temporelle, la méthode de mesure CPU/GPU (système vs composant), l'inadéquation de la métrique accuracy pour la détection.
