---
id: 2020-akintayo-prognostics-combustion-instabilities-hi-speed
fiche: done
date:
---

# Prognostics of Combustion Instabilities from Hi-speed Flame Video using A Deep Convolutional Selective Autoencoder

Adedotun Akintayo, Kin Gwn Lore, Soumalya Sarkar, Soumik Sarkar, 2020, International Journal of Prognostics and Health Management. https://doi.org/10.36001/ijphm.2016.v7i4.2461
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

Scope: this paper is about prognostics, not FPGAs. It trains a convolutional selective autoencoder (CSAE, 416,779 parameters) in Theano/Lasagne/NoLearn. Frames from a lab-combustor flame video are resized from 100×237 to 16×16. The network learns to mask stable-flame frames and pass unstable ones. It is compared with a selective CRF (SCRF, Matlab, 8064 cliques). FPGAs are only proposed as future work ("dedicated FPGAs … can enable on-line real-time instability detection"). The paper reports no FPGA design, resources, power or throughput, so the LUT, DSP, BRAM, power and GOPS fields are n/r. The 'autoencoder-fpga' axis tag is weak and should be checked by hand.

Measured results: Table 2 gives CSAE inference at about 4.7 ms/frame on CPU and about 1 µs/frame on GPU. SCRF takes about 0.24 s/frame on CPU. Model size is O(MB) for CSAE and O(KB) for SCRF. The CPU and GPU models, batch sizes and whether preprocessing is included are not stated. Only the training GPU is named: a Titan Black with "16MB video RAM", which is probably a typo. The GPU figure of about 1 µs/frame is not in ms, so latency_ms is n/r for that row rather than a converted value.

Accuracy: there is no classification accuracy. The quality measure is the ratio Σ(z)/µ(z) of the instability metric, and a transition frame number. For protocol 50040to30 with 10 code units, the ratio is 1.045 for CSAE and 0.2139 for SCRF (Table 3). Thresholds come from the 95% CI of stable validation frames: 0.003901 for CSAE-10 and 0.03636 for SCRF. The column alignment in Table 1 is garbled in the extraction. The DOI (ijphm.2016.v7i4) suggests the paper is from 2016, not 2020 as the metadata says.
