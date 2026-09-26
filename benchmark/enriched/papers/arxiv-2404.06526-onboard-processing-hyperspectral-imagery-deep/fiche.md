---
id: arxiv-2404.06526-onboard-processing-hyperspectral-imagery-deep
fiche: done
date:
---

# Onboard Processing of Hyperspectral Imagery: Deep Learning Advancements, Methodologies, Challenges, and Emerging Trends

Nafiseh Ghasemi, Jon Alvarez Justo, Marco Celesti, Laurent Despoisse, Jens Nieke, 2024, arXiv preprint. https://arxiv.org/abs/2404.06526
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

Review paper from ESA-ESTEC (arXiv 2404.06526, 2024). It surveys deep learning for onboard hyperspectral (HS) processing: CNNs (1D, 2D and 3D), autoencoders, DBNs, GANs, RNNs and CapsNets. It also covers training-data scarcity, noise handling and hardware accelerators (FPGA/GPU).

Critical reading:
(1) The paper is a literature survey. It reports no FPGA or accelerator experiments of its own, and gives no numbers for throughput, latency, power or resources. It says itself that 'there have been limited studies exploring the implementation of DL on FPGAs' and lists DL-on-FPGA as a research gap.
(2) The 'autoencoder-fpga' axis tag seems overstated. Autoencoders appear only as a way to reduce dimensions and extract features from noisy or limited data (refs 72–80). None of the supplied passages links them to an FPGA implementation.
(3) The only hardware-related quantitative claim is second-hand. The Phi-Sat-1 onboard cloud detection on a 'dedicated chip' reached accuracy 'more than 90%' with a 1D CNN. The chip, dataset, quantization and metric definition are not named, and the value is a lower bound. I recorded it as a single row with low confidence. It should be traced to ref [70] before anyone relies on it.
(4) The claim that 1D CNNs 'consistently outperformed' 2D CNNs for onboard use comes without numbers or citations in the passages.
(5) Extraction warnings say the metadata needs manual checking. The DOI is missing, and some passages are truncated (e.g., the end of the FPGA section).
