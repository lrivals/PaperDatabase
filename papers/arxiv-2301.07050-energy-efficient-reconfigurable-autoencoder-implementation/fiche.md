---
id: arxiv-2301.07050-energy-efficient-reconfigurable-autoencoder-implementation
fiche: done
date: 2026-09-26
---

# An Energy-Efficient Reconfigurable Autoencoder Implementation on FPGA

Murat Isik, Matthew Oldland, Lifeng Zhou, 2023, arXiv preprint. https://arxiv.org/abs/2301.07050
Type : **preprint non relu par les pairs**

## Problème

Montrer qu'un autoencodeur convolutif de **débruitage** d'images peut être accéléré sur
FPGA de façon plus efficace en énergie que sur GPU, avec une architecture reconfigurable
(résumé, §I). Le verrou n'est pas formulé plus précisément.

## Méthode

- Revue sommaire des types d'autoencodeurs : simple, convolutif, débruiteur, parcimonieux
  (§II).
- CAE de débruitage : encodeur à 3 conv. + 3 max-pool entrelacés, décodeur à 4 conv. +
  3 upsampling, ReLU (§III, Table I non extraite). Entraînement de 20 époques sur MNIST
  bruité par un bruit gaussien (§IV-A, §IV-B).
- Implémentation **VHDL** (§I) : opérations matricielles sur l'entrée 28 × 28 × 1,
  distributeur de canaux (FIFO, 8 canaux), module encodeur / décodeur (conv. + activation +
  max-pool ou upsampling), arbitre round-robin, contrôleur de sortie (§IV-D, Fig. 4-5).
- Baseline GPU : Python sur Google Colab (Tesla K80) (§IV-C).

## Plateforme et implémentation

- Zynq UltraScale+ **XCZU7EV** (504 K LUT annoncées), Vivado 2021.1, **100 MHz** (§IV-C,
  §IV-E).
- Puissance : **5,93 W « on-chip »** (résumé, Table II) ; méthode non décrite. Le terme
  suggère un rapport de puissance Vivado, mais ce n'est pas dit → `unspecified`.
- Ressources, quantification, fréquences des modules : **non rapportées**.
- Code / bitstream : non publiés.

## Résultats

- « Accuracy » du débruitage : 80,83 % au mieux (§IV-B), « 80 % » (résumé) ; métrique non
  définie pour une tâche de reconstruction.
- FPGA : **2,91 ms**, **21,12 GOP/s**, 5,93 W, 3,56 GOP/s/W (Table II, Docling).
- Table II compare avec un K80, un GTX 1080 Ti et trois FPGA de la littérature ([12], [11]
  et [5] = Zhang et al., FPGA'15, présent dans la base sous
  2015-zhang-optimizing-fpga-accelerator-design-deep).

→ reportés dans `benchmarks.csv` : **1 ligne** — CAE de débruitage, XCZU7EV, Table II,
`confidence: low`, car la métrique de précision n'est pas définie, le tableau est
incohérent (voir ci-dessous) et reconstruit par Docling.

## Limites et critique

- **Table II incohérente** : le K80 est classé « ASIC (28 nm) » ; 22 000 GOP/s pour une
  latence de 1 137,62 ms et 733 GOP/s/W ne sont pas compatibles entre eux ni avec un K80.
  Le GTX 1080 Ti affiche la même fréquence que le K80 (1,48 GHz).
- **Comparaisons trompeuses** : Zhang et al. [5] (AlexNet, convolutions seules, FP32, puissance
  carte 18,61 W) est présenté parmi des « CNN autoencoder models » ; aucune des références
  FPGA n'est un autoencodeur, ni sur la même tâche.
- « Accuracy » d'un débruiteur non définie (pas de PSNR, SSIM ni MSE rapporté).
- Pas de ressources, pas de quantification, pas de protocole de mesure : le travail est
  **non reproductible** en l'état.
- Plusieurs passages de l'introduction sont incompréhensibles (§I : « machine vision framework
  developers and respectability… »), ce qui suggère une rédaction non relue.
- 21 GOP/s pour un CAE MNIST 28 × 28 sur un ZU7EV : on ne sait pas si c'est un débit
  soutenu ou crête, ni avec quel batch.

## Pertinence pour la thèse

Faible comme source de chiffres, mais c'est l'un des rares papiers du corpus sur un **CAE
d'images sur Zynq UltraScale+** (famille du KV260, dont la puce est une ZU5EV). Il montre
surtout ce qu'il faut éviter : métrique de qualité indéfinie, comparaisons hors sujet,
absence de ressources. Il confirme le gap : les AE d'images sur FPGA restent peu et mal
documentés (déduit).

## Gaps identifiés

- CAE de **débruitage / reconstruction d'images** sur Zynq UltraScale+ avec métriques
  standard (PSNR, SSIM), ressources et puissance mesurée : encore à faire proprement.
- Passage au RGB et à des résolutions réelles : annoncé en travail futur (§V).
- Débruitage en ligne pour la robotique (§V) : non traité.

## Statut de lecture

Papier complet (`fulltext.md` lu en entier ; papier court). Table I (architecture) absente,
Table II reconstruite par Docling (incohérences probablement présentes dans l'original, à
vérifier sur le PDF), section IV mal découpée (« sections numérotées non détectées »).
Déduit et non affirmé par les auteurs : puissance issue d'un rapport Vivado ; rédaction non
relue ; ZU5EV pour le KV260.
