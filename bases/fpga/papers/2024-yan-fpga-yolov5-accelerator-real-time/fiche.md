---
id: 2024-yan-fpga-yolov5-accelerator-real-time
fiche: done
date: 2026-09-29
---

# An FPGA-Based YOLOv5 Accelerator for Real-Time Industrial Vision Applications

Zhihong Yan, Bingqian Zhang, Dong Wang, 2024, Micromachines 15(9), 1164. https://doi.org/10.3390/mi15091164
Type : article de journal (relu par les pairs)

## Problème

Les accélérateurs FPGA de YOLO en 8-16 bits consomment beaucoup de DSP/LUT et plafonnent en débit (§1). Descendre à 4 bits sur tout le réseau fait chuter la mAP, et les schémas asymétriques ou non uniformes exigent des calculs flottants inadaptés au FPGA. Application visée : détection de défauts de PCB en inspection industrielle (§3, §7.3).

## Méthode

Quantification 4 bits de tout le réseau, symétrique et uniforme (§4) : OPReLU (PReLU à décalage entraînable, remplace SiLU), Signed Clipping Quantization (SCQ, écrêtage bilatéral, borne c en puissance de 2) pour les activations, LSQ pour les poids, et Mimic 4-bit Quantization (M4bQ) qui découpe chaque pixel 8 bits de la première couche en deux valeurs 4 bits sans changer le résultat de la convolution (Eq. 5-9). Matériel (§5) : PE Array avec DSP packing de quatre multiplications 4 bits signées par DSP48E1/E2 et correction précalculée (II=1), Parity Adder Trees pour M4bQ, Local Buffer ping-pong, traitement couche par couche ; pré/post-traitement (dont NMS) sur ARM. Stockage DDR concaténé 4 bits sur bus 512 bits (§6). Flot : PyTorch 1.13.1 pour l'entraînement, Xilinx HLS 2022.1 (§7.2).

## Plateforme et implémentation

Carte ZCU102 (Zynq UltraScale+ MPSoC, 2520 DSP, 4 Go DDR4), 200 MHz (Table 2). Ressources (Table 1) : 160 049 LUT, 558 BRAM 36k, 1647 DSP (dont 1600 pour le Conv Engine). Puissance : 12,3 W (§7.4, Table 3), méthode de mesure non décrite donc `power_scope` unspecified. Bande passante DDR moyenne 6,10 GB/s (§6). Code/bitstream : non publiés (aucun lien dans le texte).

## Résultats

- YOLOv5s 512x512 : 79,1 FPS, 808,6 GOPS, 0,49 GOPS/DSP, 12,633 ms, 12,3 W (§7.4, Table 3) ; pic théorique 1638,4 GOP/s à 200 MHz.
- mAP VOC : 73,8 % avec -1,5 pt (Table 2) ; comparé à -3 % pour [12] et -2,9 % pour [29].
- Table 2 : +106 % de GOPS vs [5] (YOLOv5s, 16/8 bits, VCU110, 392 GOPS), et +28,9 % de GOPS/DSP vs le design commercial [30] (YOLOv3, RTL, 816,4 GOPS ; 0,38 GOPS/DSP) ; le résumé annonce « 29 % » face à Vitis AI. Face à [15] (LUT, YOLOv2, 6,70 GOPS/DSP) l'efficacité est inférieure (§7.4).
- Table 3 : 65,7 GOPS/W contre 1,1 (CPU E5-2686 v4, 168,4 GOPS, 160 W) et 10,3 (GPU V100, 2578,1 GOPS, 250 W) : chiffres CPU/GPU repris de [18] (float32) (Table 3).
- Détection de défauts PCB (PKU-Market-PCB) : 79,1 FPS ; la mAP n'est pas donnée dans le texte (§7.3).
→ reportés dans `benchmarks.csv` (via bench_rows.csv) : 2 lignes (VOC, high ; PCB, medium).

## Limites et critique

- Comparaison à des travaux sur des jeux, modèles (YOLOv3/v4-tiny/v5s) et résolutions différents ; la mAP de VOC n'est pas comparable à COCO, donc les comparaisons de précision restent qualitatives.
- Le « +29 % face à Vitis AI » du résumé porte sur GOPS/DSP contre un YOLOv3 de [30] (dont le débit brut est légèrement supérieur : 816,4 vs 808,6 GOPS) ; il ne s'agit pas d'une mesure de Vitis AI sur YOLOv5s sur la même carte dans le texte extrait (déduit).
- Puissance 12,3 W sans méthode : à ne pas comparer à des mesures chip ; baselines CPU/GPU en float32 reprises d'un autre travail, avec un rapport d'efficacité peu équitable (FP32 large vs INT4 dédié).
- Précision seulement sur VOC (mAP -1,5 pt) et sur des défauts de PCB (mAP non rapportée) ; pas de test sur COCO ni sur des personnes.
- Pas de code publié ; 4 bits sur tout le réseau incompatible avec un modèle YOLO pré-entraîné COCO sans ré-entraînement.
- Latence non déterministe non discutée ; pas d'analyse de sûreté ou de robustesse.

## Pertinence pour la thèse

Axe `yolo-fpga` : YOLOv5s sur ZCU102 en INT4, avec 79 FPS à 512x512 et 12,3 W, d'usage industriel (inspection). C'est un point de comparaison direct pour l'axe « détection en secteur industriel » sur SoC FPGA et pour la question précision/ressources. Pour la certification, la quantification 4 bits et le DSP packing avec corrections ajoutent des risques (équivalence bit-exacte modèle/matériel à vérifier, déduit) ; l'article ne fournit ni fiabilité (SEU), ni traçabilité, ni détection de personnes.

## Gaps identifiés

- YOLO INT4 sur FPGA : évaluer l'effet sur des classes « personne » (EPI, zones dangereuses) et sur COCO.
- Mesures de puissance normalisées (chip vs carte) pour ce type d'accélérateur.
- Vérification d'équivalence entre modèle quantifié et implémentation DSP-packée.

## Statut de lecture

papier complet. Table 2 lisible, mais la ligne mAP alignée par déduction sur les colonnes (Ours = 73,8 %) : à vérifier. Déduit et non affirmé par les auteurs : la lecture du « 29 % vs Vitis AI », l'absence de code publié (aucun lien dans le texte), les risques pour la certification.
