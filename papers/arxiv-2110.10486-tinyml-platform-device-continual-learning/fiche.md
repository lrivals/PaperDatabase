---
id: arxiv-2110.10486-tinyml-platform-device-continual-learning
fiche: done
date: 2026-09-26
---

# A TinyML Platform for On-Device Continual Learning with Quantized Latent Replays

Leonardo Ravaglia, Manuele Rusci, Davide Nadalini, Alessandro Capotondi, Francesco Conti, Luca Benini, 2021, IEEE Journal on Emerging and Selected Topics in Circuits and Systems 11.4 (2021), 789-802. https://doi.org/10.1109/JETCAS.2021.3121554 — texte lu : version arXiv 2110.10486
Type : article de journal (IEEE JETCAS, relu par les pairs, d'après le journal_ref arXiv ;
la version lue est le preprint arXiv)

## Problème

Le TinyML suit un schéma « entraîner puis déployer » : les modèles figés ne s'adaptent pas
à la dérive des données sans collecte et réentraînement dans le cloud (§I). L'apprentissage
continu par **Latent Replays** (LR, Pellegrini et al.) évite l'oubli catastrophique en
rejouant des activations intermédiaires stockées plutôt que des images. Il n'avait été
démontré que sur smartphone (Snapdragon 845, quelques watts), trop gourmand en calcul et en
mémoire pour un MCU (§I, §II-C).

## Méthode

- **QLR-CL** (§III-C) : le réseau (MobileNet-V1 128 × 128, pré-entraîné ImageNet) est
  coupé à une couche l ; l'**étage figé** (couches < l) est quantifié en **INT8** par
  quantification post-entraînement (NEMO) ; les **Latent Replays sont stockés quantifiés**
  (UINT-8, 7 ou 6 bits) ; l'**étage adaptatif** (couches > l) est réentraîné en **FP32** par
  rétropropagation, avec mini-batchs de 128 = 21 nouvelles images + 107 LR, 4 époques
  (§III-A, §V-A, §V-D).
- **Plateforme VEGA** (§IV-A) : SoC PULP 22 nm GlobalFoundries ; cluster de 9 cœurs RISC-V
  (8 de calcul + 1 contrôleur), **4 FPU FP32/FP16 partagées**, 128 Ko L1 TCDM, 1,5 Mo L2,
  4 Mo MRAM, DRAM/Flash externe jusqu'à 64 Mo.
- **Bibliothèque de primitives** d'entraînement (forward, backward erreur, backward gradient)
  pour conv. pointwise, depthwise et linéaire ; im2col (possiblement fait par le DMA) ;
  parallélisation sur 8 cœurs ; tuilage L2 → L1 en double tampon (§IV-B).
- Protocole **Core50 NICv2-391** : 3 000 images initiales sur 10 classes, puis 40 classes
  en 390 événements d'apprentissage (§V-A).

## Plateforme et implémentation

- Pas de FPGA. **VEGA** (ASIC 22 nm) à **375 MHz**, puissance moyenne **62 mW**, mesurée par
  le courant absorbé par la puce sous 1,8 V (§V-D, §V-E) → portée `chip`.
- Comparaison sur **STM32L476RG** (Cortex-M4, 80 MHz, NUCLEO-64), portage direct du même code
  (§V-E) ; ses latences n'incluent pas le tuilage vers la mémoire externe (§V-E).
- Code : les auteurs partent du code public de [1] ; leur propre bibliothèque n'a pas de
  lien dans le texte extrait.

## Résultats

- Précision Core50 avec 1 500 LR (Table II, moyenne sur 5 runs) :

  | Couche LR | FP32 | UINT-8 + UINT-8 | UINT-8 + UINT-7 |
  |---|---|---|---|
  | 27 (linéaire) | 72,7 % | 69,2 % | 67,8 % |
  | 23 | 75,0 % | 73,4 % | 69,9 % |
  | 21 | 76,5 % | 73,9 % | 72,6 % |
  | 19 | 77,7 % | 76,0 % | 75,2 % |

  UINT-8 avec 3 000 LR à l = 19 : −0,26 % seulement face au FP32 (§V-B). Sous 6 bits, la CL
  ne converge pas (§V-B). La quantification des LR coûte plus que celle de l'étage figé
  (Table II).
- Mémoire : CL faisable en **< 64 Mo** ; les points du cluster A (l = 27) tiendraient dans les
  4 Mo de MRAM (§V-B, Fig. 7).
- Primitives : jusqu'à 1,91 MAC/cycle (pointwise forward, 8 cœurs, L1 512 Ko), accélération
  parallèle 7,2× sur 8 cœurs (§V-C, Fig. 8) ; surcoût de tuilage ≈ 7 % (§V-D).
- Latence par événement d'apprentissage sur VEGA (Table IV) : étage adaptatif 2,07 s
  (l = 27), 877 s (l = 23), 2 490 s (l = 20) ; énergie cumulée 0,13 J, 54,3 J et 154 J.
  Apprendre 300 nouvelles images en ne réentraînant que la dernière couche prend 3,30 s
  (§V-D).
- Contre STM32L4 : en moyenne **65× plus rapide, 37× plus économe** (§V-E, Table IV ; l = 27 :
  139 s et 4,80 J sur STM32). Contre Snapdragon 845 (scénario de [1]) : 9,7× plus efficace en
  énergie, en prenant **4 W « d'enveloppe »** pour le Snapdragon (§V-E).
- Autonomie estimée : ≈ 108 jours avec une batterie de 3 300 mAh, un apprentissage par
  minute et une inférence par seconde (§V-E).

→ reportés dans `benchmarks.csv` : **4 lignes** — VEGA pour l = 27, 23 et 21 (UINT-8 +
UINT-8, 1 500 LR), et STM32L4 pour l = 27. `latency_ms` = latence de l'**étage adaptatif par
événement d'apprentissage** (Table IV), pas une latence d'inférence. Puissance 0,062 W `chip`
pour VEGA ; `n/r` pour STM32 (seule l'énergie est donnée).

## Limites et critique

- **Pas de FPGA** : plateforme ASIC PULP ; utile ici comme référence MCU / ASIC pour l'axe
  apprentissage continu.
- **Comparaison Snapdragon biaisée** : 4 W d'enveloppe supposée (non mesurée) contre 62 mW
  mesurés sur puce. La comparaison STM32 est plus juste (même code), mais le STM32 ne compte
  pas les accès à la mémoire externe, que les auteurs signalent (§V-E).
- Puissance VEGA mesurée sur la puce seule, sans la mémoire externe (DRAM/Flash) qui
  stocke les LR (déduit).
- Latences d'apprentissage de l'ordre de 15 à 40 min dès qu'on remonte dans le réseau :
  seule la dernière couche est réellement rapide.
- Un seul jeu (Core50) et un seul réseau (MobileNet-V1) ; classification uniquement.
- L'autonomie suppose une consommation nulle hors apprentissage et inférence (§V-E).

## Pertinence pour la thèse

Référence centrale de l'axe `continual-learning` embarqué : c'est une recette complète
(étage figé INT8 + replays latents quantifiés + réentraînement FP32 d'une queue de réseau),
évaluée en énergie sur puce et comparée à un MCU. Pour une thèse FPGA, la question ouverte
est directe (déduit) : l'étage figé INT8 est exactement ce que Vitis AI, FINN ou hls4ml
accélèrent bien sur KV260 ; l'étage adaptatif FP32 pourrait tourner sur l'ARM ou dans un
petit moteur de rétropropagation en logique programmable. Aucun papier du corpus ne fait
cette combinaison.

## Gaps identifiés

- **QLR-CL sur FPGA** (étage figé accéléré en PL, rétropropagation de la queue sur PS ou PL) :
  non traité.
- Apprentissage continu pour la **détection** (YOLO) plutôt que la classification : non
  traité.
- Rétropropagation en précision réduite (INT8 / FP16) pour l'étage adaptatif : non
  explorée ici (FP32).
- Coût énergétique de la mémoire externe des LR : non mesuré.

## Statut de lecture

Papier complet (`fulltext.md` lu en entier). Extraction correcte ; un passage de §II-B est
tronqué (fin de la phrase sur Shin et al.) ; Figures 5-10 non extraites (précisions pour
375 / 750 / 3 000 LR lues seulement dans le texte).
Déduit et non affirmé par les auteurs : puissance hors mémoire externe ; transposition sur
KV260 ; absence de ce couplage dans le corpus.
