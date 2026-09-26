---
id: arxiv-2512.01463-hls4ml-flexible-open-source-platform
fiche: done
date:
---

# hls4ml: A Flexible, Open-Source Platform for Deep Learning Acceleration on Reconfigurable Hardware

Jan-Frederik Schulte, Benjamin Ramhorst, Chang Sun, Jovan Mitrevski, Nicolò Ghielmetti, Enrico Lupi, Dimitrios Danopoulos, Vladimir Loncar, Javier Duarte, David Burnette, Lauri Laatu, Stylianos Tzelepis, Konstantinos Axiotis, Quentin Berthet, Haoyan Wang, Paul White, Suleyman Demirsoy, Marco Colombo, Thea Aarrestad, Sioni Summers, Maurizio Pierini, Giuseppe Di Guglielmo, Jennifer Ngadiuba, Javier Campos, Ben Hawks, Abhijith Gandrakota, Farah Fahim, Nhan Tran, George Constantinides, Zhiqiang Que, Wayne Luk, Alexander Tapper, Duc Hoang, Noah Paladino, Philip Harris, Bo-Cheng Lai, Manuel Valentin, Ryan Forelli, Seda Ogrenci, Lino Gerlach, Rian Flynn, Mia Liu, Daniel Diaz, Elham Khoda, Melissa Quinnan, Russell Solares, Santosh Parajuli, Mark Neubauer, Christian Herwig, Ho Fung Tsoi, Dylan Rankin, Shih-Chieh Hsu, Scott Hauck, 2025, arXiv preprint. https://arxiv.org/abs/2512.01463
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

hls4ml is an open-source compiler-style toolflow. It parses models from front ends (Keras 2/3, QKeras, HGQ/HGQ2, PyTorch, ONNX/QONNX) into an internal representation, runs optimizer passes on it, and generates HLS code through back ends for Vitis/Vivado, oneAPI/Quartus and Catapult. Critical reading: (1) The reported FPGA results are out-of-context place-and-route results on AMD parts (XCVU9P, XCVU13P, XC7A35T). There are no on-board measurements and no power figures. The Evaluation section mentions Agilex7/oneAPI results, but no such numbers appear in the supplied passages. (2) Throughput is implied only by II = 1 at the achieved clock; FPS and GOPS are never reported. (3) The QKeras baselines are cited from earlier work (e.g. [31], [2]) and were not rerun under the same tool versions. The HGQ rows are Pareto points regularized with different beta values, and per-layer bit-widths are not given. (4) The table extraction is noisy. The block labeled Table 4 appears to merge Table 3 (5 ns clock, with II column) with the true Table 4 (1 GHz target, with Fmax column). I therefore took the extracted rows from the cleaner Table 5 and Table 9. (5) The DA strategy (da4ml) removes all DSP usage and often lowers latency. It does not support RF > 1, and its benefit may shrink when high precision is needed. (6) The ASIC results (Catapult, 28 nm: 0.81 mm2 for the 2D variant, 0.39 mm2 for the 1D variant, <1 uW/pixel) are estimates or come from prior work. (7) The authors acknowledge that HLS output can be up to 2x worse than hand-mapped Verilog, that feature support is uneven across back ends, and that HLS compilation of large models can fail. Example: the Latency-strategy model with the highest accuracy failed placement on the XC7A35T.
