---
id: arxiv-2303.14535-efficientad-accurate-visual-anomaly-detection
fiche: done
date:
---

# EfficientAD: Accurate Visual Anomaly Detection at Millisecond-Level Latencies

Kilian Batzner, Lars Heckler, Rebecca König, 2023, arXiv preprint. https://arxiv.org/abs/2303.14535
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

EfficientAD (Batzner, Heckler, König; MVTec Software, arXiv 2303.14535) is a GPU anomaly-detection method, not an FPGA one. The automatic 'autoencoder-fpga' axis should be checked: the only link is that an autoencoder handles logical anomalies. The method uses a 4-layer patch description network (PDN) as both teacher and student. The PDN is distilled from WideResNet-101 features on ImageNet, has a 33×33 receptive field, and uses strided average pooling to downsample early. A hard-feature loss and a pretraining-image penalty create loss-induced asymmetry between student and teacher. An autoencoder catches logical anomalies, and quantile-based map normalization combines the maps. Evaluation covers 32 scenarios from MVTec AD, VisA and MVTec LOCO. Measured results in the supplied passages: (1) the abstract gives about 2 ms latency and about 600 images/s, measured on a 'modern GPU'; Section 4 says Table 1 timings use an NVIDIA RTX A6000, latency at batch size 1 and throughput at batch size 16. (2) PDN feature extraction takes under 800 µs for a 256×256 image on an RTX A6000 (Section 3). This is not a row because the value is in µs, the rule forbids unit conversion, and it is an upper bound for the feature extractor only. Table 1–5 numbers were not extracted (only captions and fragments are available), so no AU-ROC or AU-PRO values can be filled in for the default model. Ablation deltas (Table 4, average AU-ROC): map normalization +0.8, hard feature loss +1.0, pretraining penalty +0.4. Isolated removals (Table 5) cost -0.7, -0.7 and -0.4. With early stopping (tuning on test images, which is disabled by default), the paper reports 99.8 image-level AU-ROC on MVTec AD. Strengths: fair-comparison fixes (SimpleNet test-set tuning disabled, PatchCore center crop disabled, FastFlow early stopping disabled) and timing on several GPUs (A6000, A5000, V100, 3080, 2080 Ti). Caveats: the abstract does not say which variant (S or M) gives 2 ms / 600 fps; no power, FPGA resources or quantization are reported; the GCAD comparison uses only one ensemble member. Metadata extraction was marked ok=false, so title, authors and venue need a manual check.
