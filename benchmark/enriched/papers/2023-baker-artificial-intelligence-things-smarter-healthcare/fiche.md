---
id: 2023-baker-artificial-intelligence-things-smarter-healthcare
fiche: done
date:
---

# Artificial Intelligence of Things for Smarter Healthcare: A Survey of Advancements, Challenges, and Opportunities

Stephanie Baker, Wei Xiang, 2023, IEEE Communications Surveys & Tutorials. https://doi.org/10.1109/comst.2023.3256323
Type : n/r

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

Baker & Xiang (2023, IEEE COMST) is a survey of the Artificial Intelligence of Things for healthcare (AIoMT), not an experimental paper. What it contributes: (1) a three-layer computing hierarchy (device/embedded, edge, cloud) plus an application layer; (2) a proposed cross-layer AI approach, where lightweight models on the device or edge handle data quality checks, preprocessing and offloading decisions, and heavier models run in the cloud; (3) overviews of sensors (PPG, ECG, EEG, rPPG, sweat and interstitial-fluid sensors), communications (LoRaWAN, Sigfox, NFC, NB-IoT, 5G, RedCap, 6G, LEO satellite) and ML model families (CNN, RNN/LSTM, RF, autoencoders, transformers/BERT/ViT); (4) a review across monitoring, diagnosis, prognosis and explainability, plus use cases (dementia, stroke, breast cancer, COVID-19). Critical points: FPGA and CMOS embedded AI get only a one-line mention with citations [24], [25]. No accelerator design, resource use, latency, throughput or power is reported, so the paper adds nothing to hardware benchmarking. The accuracy figures it quotes come from other papers, with datasets and protocols that aren't comparable: 96.7% of heat-stroke cases detected with kNN [180]; 80% for RF on 12 patients [181]; 83.33% kNN and about 79% RF/SVM for Wi-Fi CSI respiratory rate [145]; 95.30% CNN for CSI activity recognition [185]; 65.3% RF for depression/anxiety [144]. Some quoted numbers use very small cohorts (for example 12 patients). The comparison with other surveys (Table I) is a simple checkmark matrix defined by the authors themselves. Some claims, such as vision transformers 'routinely outperform' CNNs, are stated without quantitative support in these passages. Metadata extraction was flagged as needing manual checking. No benchmark rows were produced: none of the supplied passages reports a measured hardware result, and the accuracy numbers belong to the cited primary works, not to this paper.
