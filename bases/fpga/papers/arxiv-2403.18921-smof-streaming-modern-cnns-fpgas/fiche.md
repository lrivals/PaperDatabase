---
id: arxiv-2403.18921-smof-streaming-modern-cnns-fpgas
fiche: done
date: 2026-09-29
---

# SMOF: Streaming Modern CNNs on FPGAs with Smart Off-Chip Eviction

Petros Toupas, Zhewen Yu, Christos-Savvas Bouganis, Dimitrios Tzovaras, 2024, arXiv preprint. https://arxiv.org/abs/2403.18921
Type : preprint non relu par les pairs

## Problème

Les toolflows d'architectures streaming (fpgaConvNet, FINN, hls4ml, HPIPE) gardent poids et activations sur puce ; les réseaux modernes à longues skip connections (UNet, YOLO, X3D) exigent alors des FIFO très profondes et dépassent la mémoire on-chip, alors que la mémoire externe reste inutilisée (§I).

## Méthode

Trois leviers intégrés à fpgaConvNet (§III, §IV-A) : (1) *activation eviction* : le buffer profond d'une skip connection est remplacé par deux petites FIFO et un aller-retour DMA vers la DDR ; (2) *weight fragmentation* : une fraction m des poids d'une couche est chargée dynamiquement depuis l'off-chip dans une mémoire partagée ; (3) partitionnement en sous-graphes avec reconfiguration du FPGA (compromis latence/débit, Eq. 5-6). Compression sans perte optionnelle (RLE ou Huffman) sur les flux DMA. DSE gloutonne itérative en 5 passes, avec heuristique L·Δd/ΔBW pour choisir où évincer (§IV-B). Modèle de profondeur de pipeline révisé (écart annoncé ~12 %, §IV-C). Quantification : poids block floating-point 8 bits par canal, activations 8 bits fixes, sans fine-tuning (§V-A).

## Plateforme et implémentation

ZCU102, Alveo U200, VCU1525, VCU118 (§V). Générateur RTL depuis PyTorch via fpgaConvNet. Fréquences et ressources dans Table V (les colonnes fréquence et URAM sont mal alignées à l'extraction). Puissance : n/r (aucune mesure). Code publié : https://github.com/ICIdsl/smof.git (Abstract) ; bitstreams : n/r.

## Résultats

- Ablation (Fig. 6) : eviction seule ~+5 % sur UNet ; les deux techniques jusqu'à 1,3x (UNet) et 1,1x (UNet3D, batch 1). Les gains diminuent avec un grand batch (64), la DSE préférant plus de partitions (§V-B).
- Compression (Fig. 7) : RLE jusqu'à 2,21x MACs/s vs sans encodage sur UNet ; aucun gain sur UNet3D, limité par les LUT (§V-C).
- Table V (reconstruite par Docling, à vérifier) : UNet 21,21 fps / 2758 GOP/s sur U200 ; YOLOv8n 184,27 fps / 808 GOP/s sur VCU118 (0,16 GOP/s/DSP) ; X3D-M 27,08 clips/s / 171 GOP/s sur ZCU102 ; UNet3D 1,75 clips/s / 1595 GOP/s sur U200.
- Comparaisons (§V-D) : « 10,65x » en GOP/s vs [43] à fps similaire (UNet plus lourd : 130 GMACs) ; 23x en fps vs SATAY [23] sur YOLO mais GOP/s/DSP légèrement inférieur (0,16 vs 0,18) ; 1,98x en GOP/s vs [30] sur X3D. Précision YOLOv8n : 35,10 en bfp8 vs 37,10 en f32 (Table III).
→ reportés dans `benchmarks.csv` (via bench_rows.csv) : 6 lignes SMOF (UNet x3 : VCU1525, U200, ZCU102 ; YOLOv8n VCU118 ; X3D-M ZCU102 ; UNet3D U200), confidence medium car Table V est reconstruite.

## Limites et critique

- Aucune mesure de puissance ni d'énergie : impossible de comparer en FPS/W ; pas de baseline GPU/Jetson.
- Comparaisons hétérogènes : UNet de tailles différentes (0,6 à 130 GMACs), précisions différentes (W8A8 vs W16A16 ou float32), FPGA différents ; le « 10,65x » est en GOP/s alors que le fps est similaire, donc une partie du gain vient de la charge de travail.
- YOLOv8n (184 fps) est comparé à YOLOv8s de SATAY (autre taille de modèle) sur une même puce ; la précision est mesurée sans fine-tuning, avec une chute notable en fp8 (29,6 mAP).
- Débits multi-partitions rapportés « avec le batch favorable » (note Table V) ; la reconfiguration coûte 31 % de la latence en batch 1 sur UNet3D (Table IV) : peu compatible avec du temps réel à image unique.
- Performance dépendante du taux de compression des activations, variable selon l'image : dégradation si la bande passante est sous-estimée (Fig. 8) ; le comportement temporel varie donc avec les données, mauvais point pour le déterminisme.
- Preprint, pas de comparaison ni d'analyse de sûreté.

## Pertinence pour la thèse

Axe `toolflows` / `yolo-fpga` : montre comment mapper un YOLOv8 sur FPGA en streaming avec offload DDR, et fournit un toolflow open source (fpgaConvNet + SMOF) potentiellement exploitable pour le cas vidéosurveillance. Pour la thèse « sécuritaire certifiable », les points ouverts sont importants : latence non déterministe (DMA, compression à taux variable, reconfiguration), toolflow à DSE heuristique difficile à qualifier, aucune traçabilité ni tolérance aux fautes (déduit).

## Gaps identifiés

- Déterminisme/WCET des accélérateurs streaming avec eviction off-chip et compression.
- Puissance et énergie de ces designs non mesurées ; YOLOv8 sur FPGA embarqué modeste (ZCU102, Kria) : non évalué en détail.

## Statut de lecture

papier complet. Table V reconstruite par Docling (chiffres à vérifier, colonnes fréquence/URAM/reconfigurations mal alignées : non reportées) ; le tableau « Pipeline Depth Initiation Rate » est une figure sans corps. Déduit et non affirmé par les auteurs : attribution des colonnes de Table V aux appareils (recoupée par GOP/s/DSP et capacité des puces), remarques sur le déterminisme et la certification.
