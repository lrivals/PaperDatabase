---
id: arxiv-2602.15751-enabling-low-latency-machine-learning
fiche: done
date:
---

# Enabling Low-Latency Machine learning on Radiation-Hard FPGAs with hls4ml

Katya Govorkova, Julian Garcia Pardinas, Vladimir Loncar, Victoria Nguyen, Sebastian Schmitt, Marco Pizzichemi, Loris Martinazzoli, Eluned Anne Smith, 2026, Machine Learning: Science and Technology. https://doi.org/10.1088/2632-2153/ae8218
Type : article de journal

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

Critical reading: The paper adds a new hls4ml backend (released in hls4ml v1.3.0) that targets Microchip SmartHLS, so hls4ml can now generate designs for flash-based, radiation-hard PolarFire FPGAs. It demonstrates the backend with a 32→2 dense autoencoder encoder (ReLU) that compresses PicoCal calorimeter pulses into two 10-bit latent values. Quantization-aware training (QKeras) uses <16,9> inputs, <10,4> weights and biases, and <10,7> activations. The quantization scan shows reconstruction MSE levelling off at about 10 bits. The 10-bit multiplications map to 4-input LUTs, so no 18x18 math blocks are used. Timing: post-synthesis fmax is 200 MHz for the full model and 300 MHz for the nano model, against a 160 MHz target. II is 3–4 cycles, so a new input can be accepted every 25 ns, which meets the 40 MHz bunch-crossing rate. Latency is 25 ns (4 cycles) for the nano-FPGA model and 150 ns for the full model. These latencies are reported only in ns, so latency_ms is n/r to avoid converting units. Resources: about 1% of LUTs/FFs per channel. The nano model on the MPF100T uses 3.10% of 4-input LUTs, which scales to about 25% for 8 channels. That figure is a percentage, not a count, so the luts column is n/r. Physics results: CFD timestamp residual σ is 0.15 for the autoencoder versus 0.13 for direct regression. The CFD timestamp resolution is slightly better on the reconstructed pulses than on the original 32-sample pulses. Caveats: (1) Table 1's actual numbers are not in the supplied passages, so absolute LUT/FF/BRAM counts are unknown. (2) Most results are post-synthesis or co-simulation. Only the MPF300TS was run on hardware, and the paper says only that it 'agrees' with co-simulation, without giving separate numbers in these passages. (3) No power is reported. (4) The model is tiny (a single dense layer), so it shows the toolflow works rather than stress-testing it. (5) The data are Geant4 simulations with a hand-picked downsampling from 1024 to 32 samples, and timing validation covers front-pulse seed cells only. (6) The 'nano' model's lower internal precision is not fully specified in these passages. (7) There is no radiation testing; radiation tolerance is argued from the flash configuration memory alone.
