---
id: 2022-khanam-effective-intrusion-detection-model-focal
fiche: done
date:
---

# Towards an Effective Intrusion Detection Model Using Focal Loss Variational Autoencoder for Internet of Things (IoT)

Salma Khanam, Ismail Ahmedy, Mohd Yamani Idna Idris, Mohamed Hisham Jaward, 2022, Sensors. https://doi.org/10.3390/s22155822
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

These passages contain no FPGA or other hardware measurements. The only compute platform mentioned is a GPU-enabled Google Colaboratory instance with 12 GB RAM, used for the software implementation in TensorFlow/Keras. Throughput, latency, power and resource figures are therefore all n/r. The 'autoencoder-fpga' axis looks like an automatic mis-tag and should be removed or confirmed.

Method: a VAE with a class-wise focal loss (CFLVAE, 87-40-20-10-20-40-87) generates extra samples for the rare attack classes. A lightweight DNN (87-40-20-10-5) is then trained on the balanced NSL-KDD data, using the 20% training subset of 25,192 samples.

Results:
- **KDDTest+:** accuracy 88.08, recall 88.02, precision 88.25, F1 87.69, FPR 3.77.
- **KDDTest-21:** accuracy 76.22, F1 76.66, FPR 6.51.

Critical issues:
1. **R2L and U2R rates are swapped in the abstract.** It gives U2R 79.25 and R2L 67.5, but the body and Table 2 give R2L 79.26 and U2R 67.5.
2. **Hyperparameters were tuned on the test set.** Gamma and alpha were chosen by trial and error on KDDTest-21, which is also a reported test set, so the Test-21 results are optimistically biased.
3. **The SOTA comparison uses other papers' published numbers** under different protocols. The claims of best F1 and best minority-class rates rest on that table. SCDNN has higher accuracy (91.97) and ICVAE-DNN has lower FPR (2.74).
4. **The 'lightweight, suitable for IoT' claim is not measured.** No inference cost, model size, or on-device deployment is reported.
5. **Naming and metadata are inconsistent.** The text uses both CFVAE and CFLVAE and has an 'NSK-KDD' typo. The metadata gives the first author's given name as 'Salma', but the preamble says 'Shapla'.
