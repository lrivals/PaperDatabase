---
id: arxiv-2403.07851-12-mj-per-class-device
fiche: done
date:
---

# 12 mJ per Class On-Device Online Few-Shot Class-Incremental Learning

Yoga Esa Wibowo, Cristian Cioflan, Thorir Mar Ingolfsson, Michael Hersche, Leo Zhao, Abbas Rahimi, Luca Benini, 2024, 2024 Design, Automation & Test in Europe Conference & Exhibition (DATE). https://doi.org/10.23919/DATE58400.2024.10546598
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

O-FSCIL (DATE 2024) uses a frozen, metalearned backbone plus an FCR. It learns each new class in a single pass by averaging features into an explicit-memory prototype, with no backpropagation. It is deployed INT8 on the GAP9 MCU using QuantLib TQT and DORY, at 650 mV and 240 MHz.

Strengths:
- The accuracy claim is clear. ResNet12 FP32 averages 68.52, or 68.62 with FT, on CIFAR100 FSCIL, against 67.50 for NC-FSCIL.
- INT8 MobileNetV2 variants on GAP9 lose little or no accuracy against FP32. For example, x4 scores 66.51 INT8 vs 66.54 FP32.
- Latency, power and energy on GAP9 are measured and reported with standard deviations (Table IV).

Problems and inconsistencies:
1. The headline "12 mJ per class" matches the smallest MobileNetV2 (EM update 11.35 mJ, 256.65 ms). The body text links it to the MobileNetV2 x4 case, which Table IV gives as 22.75 mJ and 513.65 ms. The best-accuracy x4 model therefore needs about 2x the headline energy. The 256 ms "real-time" claim also refers to the smallest backbone.
2. The power envelope is stated as 60 mW in the abstract and 50 mW in the body.
3. The "5.7x reduction in computational effort" vs ResNet12 doesn't match Table I: 525.3/149.2 M MACs is about 3.5x. The 5.2x storage figure (12.9 vs 2.5 M params) does match. The "8.8x" figure is also approximate (6.6G/0.7G is about 9.4).
4. Table IV reports costs per class for 5-shot learning. These are not single-image inference latency or throughput, so fps and GOPS are n/r. The MACs/cycle numbers are only shown in Fig. 2.
5. Power is on-device measured, but the passages don't say whether it covers the chip, cluster or board, so scope is unspecified.
6. FPGA resource columns don't apply (this is an MCU).
7. Units: power_w holds Table IV values copied as reported in mW (44.29, 44.22), not converted to W. latency_ms is the per-class EM-update time.
8. The baselines (NC-FSCIL etc.) are FP32 GPU software results, not hardware comparisons.
