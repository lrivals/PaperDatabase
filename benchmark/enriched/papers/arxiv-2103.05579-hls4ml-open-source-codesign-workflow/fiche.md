---
id: arxiv-2103.05579-hls4ml-open-source-codesign-workflow
fiche: done
date:
---

# hls4ml: An Open-Source Codesign Workflow to Empower Scientific Low-Power Machine Learning Devices

Farah Fahim, Benjamin Hawks, Christian Herwig, James Hirschauer, Sergo Jindariani, Nhan Tran, Luca P Carloni, Giuseppe Di Guglielmo, Philip Harris, Jeffrey Krupa, Dylan Rankin, Manuel Blanco Valentin, Josiah Hester, Yingyi Luo, John Mamish, Seda Orgrenci-Memik, Thea Aarrestad, Hamza Javed, Vladimir Loncar, Maurizio Pierini, Adrian Alan Pol, Sioni Summers, Javier Duarte, Scott Hauck, Shih-Chieh Hsu, Jennifer Ngadiuba, Mia Liu, Duc Hoang, Edward Kreinar, Zhenbin Wu, 2021, TinyML Research Symposium 2021. https://arxiv.org/abs/2103.05579
Type : conférence

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

hls4ml (TinyML 2021) is mainly a workflow and tooling paper. It covers Python package internals, (Q)Keras/TF/PyTorch/ONNX converters, graph optimizers such as BN fusion, numerical profiling, QKeras QAT propagation, and the new quantization-aware pruning (QAP) method using Brevitas with lottery-ticket rewinding. It also covers reuse-factor parallelization, and Vitis Accel and Catapult ASIC backends. The supplied passages give few hard numbers. (1) For the jet tagging MLP (16-64-32-32-5), PTQ accuracy starts to drop below 14 bits, while QAT matches 32-bit float down to 6 bits. This comes from Fig. 4, borrowed from Ref. [11]. (2) After QAP, a 6-bit, 80%-pruned model uses 50 times fewer BOPs than the 32-bit unpruned model, with no loss in performance (Fig. 5). (3) The MNIST 784-16-10 MLP needs 12,704 multiplications and was swept over reuse factors from 14 to 12,544 (Fig. 6), but no resource figures appear in the text. (4) The FPGA results for 16-bit and 14-bit PTQ and 6-bit QAT are in Table 1, which is not included in the passages. The paper only says that DSP use is drastically reduced. (5) The only measured hardware figure is the SVHN CNN from Ref. [12]: pruning plus QAT, 5 μs latency, under 10% of FPGA resources, and 'low estimated power'. The FPGA part, exact resource counts and power value are not given. latency_ms is n/r because the value is reported in μs and unit conversion was not allowed. Critical points: most quantitative claims are cited from companion papers ([11], [12], [14]), not measured here. There is no power number, even though the paper frames itself around low power. The claim that the ASIC flow's PPA is comparable to handwritten RTL is supported only by a citation.
