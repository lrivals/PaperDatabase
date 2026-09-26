---
id: arxiv-2103.13885-supervised-contrastive-replay-revisiting-nearest
fiche: done
date:
---

# Supervised Contrastive Replay: Revisiting the Nearest Class Mean Classifier in Online Class-Incremental Continual Learning

Zheda Mai, Ruiwen Li, Hyunwoo Kim, Scott Sanner, 2021, arXiv preprint. https://arxiv.org/abs/2103.13885
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

SCR (Mai et al., arXiv 2103.13885) swaps the Softmax classifier for a Nearest-Class-Mean (NCM) classifier in online class-incremental continual learning. It also trains the encoder with a supervised contrastive loss on the incoming batch combined with a replayed memory batch. Setup: reduced ResNet18, SGD with learning rate 0.1, stream batch 10, memory batch 100, temperature 0.1, reservoir update with random retrieval. Table 1 reports average end-of-training accuracy over 10 runs. SCR scores 35.4 on Mini-ImageNet (M=5k), 37.8 on CIFAR-100 (M=5k) and 65.7 on CIFAR-10 (M=1k). These are +13.3, +8.2 and +15.4 over the second-best methods, which are themselves NCM-augmented.

Critical points:
(1) This is not a hardware paper. There is no platform, latency, power or FPGA resource data. Run time appears only as a figure (Fig. 7) with no numbers, so every hardware field is n/r.
(2) The relative-gain claims in the text contradict Table 1. The text says '21.1 (MIR-NCM) -> 35.4' and '16.6 (MIR-NCM) -> 24.1'. In the table, MIR-NCM on Mini-ImageNet is 22.1 at M=5k and 17.8 at M=1k, which matches the stated gains of 13.3 and 6.3. The values 21.1 and 16.6 belong to other methods (ER-NCM/ASERµ-NCM and ASERµ-NCM). So the quoted 60.2% and 35.4% relative gains are miscomputed.
(3) The extracted Table 1 is garbled: the Softmax rows for ER, GSS, MIR and ASERµ have lost their labels, and Mini-ImageNet column alignment depends on position.
(4) The ablations (memory batch size, temperature, projection head) are run only on CIFAR-100 with M=2k and reported only as figures.
(5) Only random/reservoir memory management is tuned. The authors say imbalanced streams may need other memory strategies.
(6) The 'offline' upper bound is trained for 50 epochs, versus a single pass for the continual-learning methods.
