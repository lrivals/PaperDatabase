---
id: arxiv-2511.17135-multi-stage-optimization-framework-deploying
fiche: done
date: 2026-09-29
benchmarks: none
---

# A Multi-Stage Optimization Framework for Deploying Learned Image Compression on FPGAs

Jiaxun Fang, Li Chen, 2025, arXiv preprint. https://arxiv.org/abs/2511.17135
Type : preprint non relu par les pairs

## Problème

Les modèles de compression d'image apprise (LIC, architectures de type autoencodeur variationnel avec hyperprior) sont trop lourds en FP32 pour des FPGA à ressources limitées. La quantification INT8 classique (QAT) fait chuter les performances débit-distorsion, à cause de poids avec outliers extrêmes et d'activations à dynamique très variable selon les canaux, et échoue à converger avec les couches GDN (Generalized Divisive Normalization) (§III).

## Méthode

Pipeline en deux étapes (Fig. 1).
- Étape I, DRAQ (Dynamic Range-Aware Quantization) : clipping des activations calibré statistiquement (seuil mu + k·sigma, avec k = 625·lambda + 2, Eq. 3-4) ; régularisation des poids qui pénalise ceux hors des percentiles alpha / 1-alpha (Eq. 5) ; GDN décomposée en convolution depthwise sur |x| suivie d'une division, avec clipping bilatéral avant la GDN (§IV).
- Étape II, optimisations « pour FPGA » : recherche progressive de précision mixte par couche (tolérance epsilon, fine-tuning à chaque pas, Fig. 7) ; élagage de canaux « GDN-slimming » (facteur d'échelle appris par canal après la GDN, régularisation L1) (§V).
- Backbones : Ballé2018 (hyperprior) et He2021 (contexte checkerboard). Entraînement sur un sous-ensemble de 72 000 images de PASS, test sur Kodak24 (§VI-A).

## Plateforme et implémentation

n/r : aucune implémentation FPGA n'apparaît dans le texte disponible (pas de puce, de fréquence, de ressources, de latence ni de puissance). Les modèles sont entraînés sur une RTX 3090 (§VI-A). Le « FPGA » sert de motivation (largeurs de bits arbitraires) ; les optimisations sont évaluées en simulation de quantification (PSNR, BD-rate, GFLOPs). Code ou bitstream : non publiés (aucun lien dans le texte).

## Résultats

- BD-rate vs FP32 en INT8 : Ballé2018-ReLU 12,8 % (baseline) contre 4,93 % (DRAQ) ; Ballé2018-GDN 30,0 % contre 6,30 % ; He2021-GDN 24,0 % contre 9,48 % ; He2021-ReLU 15,3 % contre 6,82 % (Table I). Concurrents sur Ballé2018-ReLU : Hong2020 26,5 % (INT10), Sun2021 9,01 % (INT8) (Table I).
- Avec DRAQ, les modèles GDN quantifiés dépassent les ReLU quantifiés, ex. Ballé2018 lambda 0,0130 : 32,94 dB contre 32,55 dB (Table II).
- Ablation Ballé2018-ReLU : régularisation seule 10,8 %, clipping seul 6,16 %, les deux 4,93 % ; clipping en FP32 : -1,02 % seulement (Table III).
- MSQE d'activation de la couche B réduit de 6,46e-6 à 2,48e-6 (Table IV, reconstruit par Docling, à vérifier).
- Précision mixte (Table V) : FP32 34,71 dB ; mixte quasi sans perte, 8,7 bits équivalents, 34,62 dB ; mixte budgétée 7,9 bits, 34,35 dB ; uniforme 8 bits 34,13 dB (bpp comparables ~0,725).
- GDN-slimming : -20 % de complexité (138,5 à 109,9 GFLOPs/pixel), économie de débit vs BPG 11,29 % à 10,66 % (Table VII).
- Le résumé annonce « BD-rate de 30 % à 6,3 % » et un modèle « supérieur aux implémentations LIC sur FPGA existantes » ; la comparaison correspondante (Tables VIII-IX, section VI-E) est absente du texte extrait.
→ reportés dans `benchmarks.csv` : aucune ligne, pas de mesure matérielle (FPS, puissance, ressources) ni de plateforme FPGA.

## Limites et critique

- Aucune mesure sur FPGA dans la partie lue : le titre et le résumé promettent un déploiement, mais l'efficacité matérielle est jugée par GFLOPs et « bit-width équivalent » (Eq. 9), pas par LUT/DSP/latence/énergie. Une précision mixte ou un élagage ne se traduit pas mécaniquement en gain sur FPGA (déduit).
- Entraînement sur seulement 72 000 images et test sur Kodak24 : généralisation non discutée.
- Comparaison aux concurrents (Hong, Sun) sur backbone ReLU seulement ; la baseline est le QAT de [17] réimplémenté.
- Heuristique k = 625·lambda + 2 empirique, sans justification théorique ; « Time (ms) » de la Table VII sans plateforme indiquée.
- Pas de code publié, preprint non relu ; texte extrait tronqué en fin (voir Statut).
- Tâche (compression d'image) éloignée de la détection d'objets.

## Pertinence pour la thèse

Faible en direct : ni détection, ni sûreté. Intérêt indirect par l'axe autoencodeurs sur FPGA (architecture VAE appliquée à l'image, ce que la base identifie comme peu étudié) et par les techniques transférables à YOLO : clipping calibré d'activations et régularisation des outliers de poids pour INT8, recherche de précision mixte par couche, élagage de canaux. Reste ouvert : le déploiement effectif sur FPGA, et toute considération de déterminisme ou de certification d'une chaîne quantifiée (l'écart FP32/INT8 est mesuré en BD-rate, pas comme garantie).

## Gaps identifiés

- Autoencodeurs / VAE sur images sur FPGA : ici seulement de la quantification simulée, pas d'implémentation mesurée.
- Recherche de précision mixte évaluée sur des critères matériels réels (LUT/DSP, latence) : à traiter.

## Statut de lecture

Papier lu jusqu'à la fin du texte extrait, mais celui-ci s'arrête dans la section VI-E (« Final Integrated System Performance ») ; les Tables VIII et IX, la conclusion et les références n'y figurent pas. Table IV reconstruite par Docling, chiffres à vérifier. Déduit et non affirmé par les auteurs : l'absence d'implémentation FPGA (déduite de ce qui est présent dans le texte extrait), les limites de transférabilité vers le matériel, la pertinence pour YOLO.
