---
id: arxiv-2604.21280-imagehd-energy-efficient-device-continual
fiche: done
date: 2026-09-24
---

# ImageHD: Energy-Efficient On-Device Continual Learning of Visual Representations via Hyperdimensional Computing

Jebacyril Arockiaraj, Dhruv Parikh, Viktor Prasanna, 2026, 2026 IEEE 34th Annual International Symposium on Field-Programmable Custom Computing Machines (FCCM). https://doi.org/10.1109/FCCM68464.2026.00041 (texte lu : version arXiv 2604.21280)
Type : conférence (acceptation déclarée dans le commentaire arXiv, DOI éditeur trouvé via Crossref)

## Problème

L'apprentissage continu sur l'appareil exige des mises à jour rapides sous contraintes de
mémoire et d'énergie ; la rétropropagation et les classifieurs à exemplaires sont trop
coûteux (Abstract, §I). Les systèmes HDC antérieurs ([11]) reposent sur une mémoire à deux
niveaux (STM/LTM) et un clustering spectral en O(N³), peu compatibles avec un FPGA (§I, §IV-C).

## Méthode

- Pipeline hybride CNN–HDC non supervisé : MobileNetV2 pré-entraîné, gelé, quantifié INT8
  (PTQ statique, calibration sur les batchs de warm-up du flux) → encodage HDC ID-level en
  hypervecteurs binaires → recherche de similarité (Hamming) → admission (nouveau cluster
  si s < µ − βσ) (§IV-A, §IV-B, Algorithm 1).
- Mémoire d'exemplaires unifiée et bornée (Cmax clusters) à la place de STM/LTM ; fusion
  périodique par kMeans++ simplifié (Top-M + échantillonnage uniforme, LFSR) et quelques
  itérations de raffinement dans l'espace HV (§IV-C, Algorithm 2).
- Accélérateur en dataflow streaming, Vitis HLS : PCU (pointwise, p = 2, m = 4), DCU
  (depthwise 3×3, n = 4, row buffers BRAM + fenêtre glissante en registres), HEU
  (p_c = 16), HLU (p_k = 16), CMU ; tuiles 32×32 ; hypervecteurs par mots de 64 bits,
  p_w = 4 (§VI, §VII-A). Poids du CNN lus en DRAM, tables HDC et clusters sur puce (§V).
- Dimension D des hypervecteurs, Cmax, β, α : n/r dans le texte extrait.

## Plateforme et implémentation

- AMD Zynq UltraScale+ ZCU104, 300 MHz (§VII-A, Table IV). Puce XCZU7EV : déduit des
  ressources disponibles de la Table II, non écrit.
- Ressources (Table II) : 143 927 LUT (62 %), 116 019 FF, 322 BRAM18K (52 %), 57 URAM
  (59 %), 126 DSP (7 %).
- Outils : Vitis HLS, Vitis Unified IDE 2024.2 (§VII-A).
- **Mesures FPGA** : latence et puissance issues de « l'analyseur intégré » de Vitis Unified
  IDE (§VII-D) — donc estimations d'outil, pas une mesure sur carte ; GPU via nvidia-smi,
  CPU via powertop. Puissance « device », statique + dynamique, batch 1.
- Code et bitstream : non publiés (aucune mention).

## Résultats

| Jeu | Latence FPGA | Débit | Puissance | Énergie | vs CPU / GPU / Jetson (énergie) | ACC INT8 | Source |
|---|---|---|---|---|---|---|---|
| CIFAR-10 | 0,27 ms | 3703,70 img/s | 3,6 W | 0,97 mJ/img | 258× / 77× / 73× | 0,2689 | Table VII, Table VI |
| CIFAR-100 | 0,34 ms | 2965,77 img/s | 3,6 W | 1,21 mJ/img | 263× / 65× / 74× | 0,1940 | Table VII, Table VI |
| CORe50 | 0,48 ms | 2097,05 img/s | 3,7 W | 1,76 mJ/img | 383× / 105× / 44× | 0,1944 | Table VII, Table VI |

(Rapports GPU et Jetson calculés à partir de la Table VII : déduits.)

- Baselines : AMD EPYC 7763 (128 cœurs), RTX A4000, Jetson AGX Orin, en PyTorch 2.0.1,
  mêmes algorithmes et INT8 (§VII-C, §VII-H).
- Quantification INT8 vs FP32 : ACC +0,0120 et NMI +0,0093 en moyenne, pureté −0,0535 ;
  modèle 8,5 → 2,3 Mo (§VII-E, Table VI).
- Mémoire unifiée : 189,3 → 126,6 Ko dans le pire cas (−33 %, mesuré en PyTorch) (§VII-F).
- kMeans++ vs spectral : ×8-9 en moyenne sur GPU, pertes d'ACC −0,0035 et de pureté
  −0,0468 (§VII-G, Fig. 6).
- vs accélérateurs antérieurs : 19,7× moins de latence et 53,27× d'efficacité vs [11]
  (Jetson TX2) ; 6,3× et 37× vs ILOC (§VII-I, Table IV).

→ reportés dans `benchmarks.csv` : 3 lignes (une par jeu de données, Table VII + VI + II,
`high`).

## Limites et critique

- **Précision très faible, présentée comme « strong accuracy » (§IX).** ACC de clustering
  0,19 sur CORe50 (50 classes) et CIFAR-100, 0,27 sur CIFAR-10 (Table VI). C'est au-dessus du
  hasard mais loin d'un système utilisable ; aucune comparaison de précision avec [11] ni
  avec un CL supervisé (§VII-I l'écarte explicitement).
- **Mesures FPGA non comparables aux baselines.** Latence et puissance FPGA viennent de
  l'analyseur Vitis (estimation), celles du GPU de nvidia-smi et du CPU de powertop : les
  gains ×258-383 en énergie mélangent estimation et mesure. Aucune mesure au wattmètre sur
  la carte.
- **Baselines défavorisées.** CPU/GPU/Jetson exécutés en PyTorch à batch 1, sans TensorRT
  sur Jetson ; la Jetson est plus lente que le CPU serveur sur CIFAR (0,6×), signe d'une
  implémentation peu optimisée.
- **Comparaison Table IV hétérogène** : jeux (CIFAR-10, CIFAR-100, CORe50), tâches
  (supervisé vs non supervisé) et périmètres (ILOC sans extraction de features) différents.
- Résolution d'entrée par jeu (Table III non extraite), dimension D, Cmax : n/r.
- Incohérences mineures : « speedup of 8.6× » (§I) contre « 8-9× » (§VII-G).

## Pertinence pour la thèse

Travail central pour l'axe apprentissage continu : seul accélérateur FPGA de bout en bout
(extraction de features + apprentissage) pour du CL sur images, avec des budgets (3,7 W,
< 0,5 ms/img) compatibles avec l'embarqué. Montre qu'on peut faire tenir la mise à jour en
ligne sur puce via HDC ; laisse ouverte la question de la précision (non supervisé, ACC
< 0,3) et d'une mesure énergétique réelle.

## Gaps identifiés

- CL non supervisé sur FPGA : précision très basse, aucune étude de la frontière
  précision/énergie face à un CL supervisé (SLDA, replay latent) sur la même carte.
- Mesures d'énergie FPGA estimées par outil, pas mesurées : manque un protocole de mesure
  sur carte commun aux accélérateurs de CL.
- Pas de backbone de détection (YOLO) : CL limité à la classification/clustering d'images.

## Statut de lecture

Papier complet (`fulltext.md` lu en entier). Extraction : l'Algorithm 1, la fin de §VII-E
et de §VII-G sont tronquées ou déplacées dans « Figures et tableaux » ; la Table III
(jeux de données, résolutions) et la Table V n'ont pas été extraites.
Déduit et non affirmé par les auteurs : puce XCZU7EV ; rapports GPU/Jetson de la table
Résultats ; lecture « estimation d'outil » de la mesure Vitis ; faiblesse des baselines.
