---
id: arxiv-2403.18921-smof-streaming-modern-cnns-fpgas
fiche: done
date:
---

# SMOF: Streaming Modern CNNs on FPGAs with Smart Off-Chip Eviction

Petros Toupas, Zhewen Yu, Christos-Savvas Bouganis, Dimitrios Tzovaras, 2024, arXiv preprint. https://arxiv.org/abs/2403.18921
Type : preprint non relu par les pairs

## Problème

Quel verrou le papier attaque-t-il, tel que les auteurs le posent.

## Méthode

Architecture, quantification, stratégie de mapping sur le FPGA, post-traitement (NMS…).
Toolflow employé.

## Plateforme et implémentation

Puce exacte, fréquence, ressources consommées, mémoire. Code ou bitstream publiés ? Où ?

## Résultats

Les chiffres, avec la section ou le tableau source. Baseline de comparaison.
→ reportés dans `benchmarks.csv` : <lignes ajoutées>

## Limites et critique

Comparaisons biaisées, métriques non comparables d'un papier à l'autre, conditions de mesure
non précisées, absence de reproductibilité. Ce que le papier ne mesure pas.

## Pertinence pour la thèse

Ce que ce travail apporte à l'axe visé, et ce qu'il laisse ouvert.

## Gaps identifiés

Points à reporter dans `gaps.md`.

## Statut de lecture

Résumé seul | sections lues : <liste> | papier complet.
Ce qui suit est déduit et non affirmé par les auteurs : <…>

## Lecture automatique

SMOF adds two ways to use off-chip memory to the fpgaConvNet streaming toolflow: activation eviction and weight fragmentation, with optional RLE or Huffman encoding on the DMA ports. It also updates the design-space search and the pipeline-depth model. The authors say the model's estimates deviate from the built hardware by about 12%. The target is modern CNNs with long skip connections (UNet, YOLOv8, UNet3D, X3D-M) on AMD boards (ZCU102, U200, VCU1525, VCU118).

What the passages support:
- Ablation: turning on both mechanisms gives up to 1.3× for UNet and 1.1× for UNet3D at batch size 1. RLE adds up to 2.21× over no encoding on UNet. It does not help UNet3D because that design is LUT-bound, and Huffman encoding slightly lowers UNet3D performance.
- Comparison with prior work: the paper claims 10.65× GOP/s over Basalama's UNet on VCU1525 and 23× fps over Montgomerie on YOLOv8. It reports 1595 GOP/s for UNet3D on U200, with no prior work to compare against.

Caveats:
- The extracted text of Table V is scrambled. Per-design values (fps, DSP, BRAM, frequency) cannot be matched to columns reliably, so none are taken from it.
- The YOLOv8 comparison gives only relative figures (23× fps; 0.16 vs 0.18 GOP/s/DSP) and does not clearly say which variant (YOLOv8s or YOLOv8n) is which.
- Comparisons across devices use different UNet variants and input sizes, and a UNet on an Intel Arria 10.
- Some results use multiple partitions with device reconfiguration and a "favourable batch size", which inflates throughput compared with batch-1 latency.
- No power figures are given.
- Accuracies in Table III are software results (bfp8 weights). They are not measured on hardware.

Row 2 is the design annotated in Figure 4 (47 ms, 21 fps, 6062 DSP). The passage names neither its model nor its device. Its utilisation percentages match U200 capacity, but platform and model are left as n/r, so confidence is low.
