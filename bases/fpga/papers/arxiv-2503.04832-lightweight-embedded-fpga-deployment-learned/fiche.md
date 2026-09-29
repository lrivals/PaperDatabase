---
id: arxiv-2503.04832-lightweight-embedded-fpga-deployment-learned
fiche: done
date: 2026-09-29
---

# Lightweight Embedded FPGA Deployment of Learned Image Compression with Knowledge Distillation and Hybrid Quantization

Alaa Mazouz, Sumanta Chaudhuri, Marco Cagnanzzo, Mihai Mitrea, Enzo Tartaglione, Attilio Fiandrotti, 2025, arXiv preprint. https://arxiv.org/abs/2503.04832
Type : preprint non relu par les pairs

## Problème

Les implémentations matérielles de Learned Image Compression (LIC, autoencodeur convolutif + hyperprior + codage entropique) sacrifient l'efficacité débit-distorsion (RD) pour atteindre le temps réel (remplacement de GDN par ReLU, modèle ancien) et exigent une longue exploration de l'espace de conception matériel (§I, §II). Les auteurs déplacent l'effort du réglage matériel vers le dimensionnement du modèle (nombre de canaux).

## Méthode

- Knowledge distillation d'un modèle élève à moins de canaux (160 ou 128 filtres par couche) depuis un teacher (192 filtres) : loss L_KD = alpha L_latent + beta L_perc + gamma (R + lambda D), avec perte perceptuelle sur les couches 3-5 d'un ResNet-50 (§III-A, Eq. 1-2 ; alpha/beta permutés en cours de fine-tuning, Table I).
- Coeur matériel GDN / iGDN personnalisé : carré et division (approximation par réciproque) sur DSP, sommes pondérées en BRAM, racine carrée par interpolation linéaire par morceaux en LUT ; enregistré comme opération XIR personnalisée dans Vitis AI, exécutée sur un cœur DPU dédié (§III-B, Fig. 4).
- Pruning de canaux itératif : 3 x 10 % des filtres de plus faible norme L2, soit 30 % (§III-C) ; quantification mixte : 8 bits partout, GDN en virgule fixe 32 bits (~4 % des FLOPs), PTQ puis QAT 1000 itérations avec STE (§III-D).
- Déploiement : 3 cœurs DPU B4096 (DPUCZDX8L) à 300 MHz en parallèle, image découpée en patchs 256x256 (stride 56) traités en pipeline (§III-E, Fig. 7) ; modèle analytique d'estimation du FPS (Eq. 5-8, η = 0.8).
- Modèle de référence : Ballé et al. hyperprior (réf. [8]), CompressAI, entraîné de zéro sur CLIC, DIV2K, Open Images (§IV-A).

## Plateforme et implémentation

Xilinx ZCU102 (Zynq UltraScale+), DPU B4096 x 3 à 300 MHz, Vitis AI, bande passante mémoire 19.2 GB/s PL + 19.2 GB/s PS (§IV-B), DSP 2148 (Table VII). LUT / BRAM `n/r`. Mesure d'énergie : méthode non décrite, J/frame dans Table VII ; puissance en W `n/r`. Code / bitstream : aucun lien fourni dans le texte lu (« non publiés » à ma lecture).

## Résultats

- Kodak tuilé en 720p, comparaison par BD-rate / BD-PSNR par rapport à Sun-2024 [29] (§IV-C) : Teacher -8.95 % BD-rate, +0.48 dB, mais sous 25 FPS (Table VI : 16 FPS en MP) ; Student-160 -5.32 %, +0.25 dB, 43 FPS contre 37 ; Student-128 +7.80 %, -0.10 dB, proche de 60 FPS (59 FPS, Table VI).
- Table VI (BD par rapport au Ballé fp32) : Student 160 MP -0.90 dB / +24.53 % / 44 FPS ; Student 128 MP -1.23 dB / +34.57 % / 59 FPS ; Teacher 192 MP -0.66 dB / +17.62 % / 16 FPS ; variantes single precision plus rapides et moins bonnes (par ex. Student 160 SP 47 FPS, -1.68 dB).
- Table VII : ZCU102 (ce travail) 43.63 FPS encodage, 2148 DSP, efficacité DSP 85 %, 2.88 J/frame ; [28] ZCU102 32.95 FPS, 0.12 J/frame ; [29] VCU118 37.82 FPS, 5864 DSP, 93.7 % ; [26] ZCU104 3.90 FPS.
- Ablations : GDN au lieu de ReLU : -0.5 à -0.7 dB BD-PSNR, +10 à 25 % BD-rate pour ReLU (Fig. 15) ; précision mixte +0.3 dB en moyenne (+0.2 dB, -2 % bpp) ; pruning 30 % : latence -39 % (160), PSNR -0.25 dB (Table III) ; QAT : taille -42.7 %, PSNR +0.108 dB (Table IV) ; pipeline contre séquentiel : encodeur 43.6 contre 17.3 FPS (Table X, ~2.5x) ; sans KD : +22.44 % de bpp, -0.76 dB.
- Modèle analytique FPS (Table V) : écart de -3.4 % à -16.1 % (prédit 44.6 contre 43.1 observé pour 160K).
→ reportés dans `benchmarks.csv` (via `bench_rows.csv`) : 6 lignes (Teacher, Student-160, Student-128 en MP et SP), FPS d'encodage seul.

## Limites et critique

- Incohérences de chiffres : Student-160 donné à 43 FPS (§IV-C), 44 (Table VI), 43.63 (Table VII), 43.1 (Table V) ; la Table VI mélange BD par rapport au Ballé fp32 et le texte par rapport à [29]. Les valeurs de la Table VII ne mentionnent pas de quelle variante (SP / MP) il s'agit.
- 2.88 J/frame à 43.6 FPS impliquerait ~125 W (calcul déduit, non affirmé), incompatible avec une ZCU102 : probable erreur d'unité ou de portée (par ex. énergie par image entière de 720p en mJ ?) ; la méthode de mesure n'est pas décrite. La comparaison à [28] (0.12 J/frame, « sans détail de mesure ») est donc non fiable.
- Les FPS sont pour l'encodage seul (Table V, VII), et le décodage est plus lent (30.5 FPS, Table X) ; images 720p tuilées à partir de Kodak, pas de flux vidéo réel ; la perte RD par rapport au modèle float reste forte (-0.66 à -1.94 dB, Table VI).
- Comparaison avec des travaux sur cartes différentes (VCU118, KU115, ZCU104), sans budget matériel normalisé ; preprint non relu par les pairs ; code non fourni. Tables VI, VII reconstruites (Docling : Table III ; numérotation du texte décalée par rapport à l'extraction).
- Sujet hors détection : compression d'image, pas de tâche de vision aval ; aucune analyse de sûreté ou de déterminisme.

## Pertinence pour la thèse

Cas d'un autoencodeur convolutif sur images déployé sur ZCU102 avec Vitis AI : c'est un des rares travaux « autoencodeur sur image sur FPGA », gap identifié de la base, même si l'application est la compression et non l'anomalie ou la détection. Apporte des recettes transférables : distillation d'un élève dimensionné pour un budget de DPU, pruning de canaux compatible DPU, quantification mixte 8/32 bits pour une couche sensible (leçon de sensibilité à la quantification, utile pour un YOLO sûr), modèle analytique du FPS, opérateur personnalisé dans XIR (relevant pour un flot certifiable : ce qui sort du DPU standard est à qualifier ; inférence de ma part). Ne traite pas de sûreté, de certification ni de personnes.

## Gaps identifiés

- Autoencodeurs sur images sur FPGA appliqués à l'anomalie, non à la compression.
- Opérateurs personnalisés (GDN) intégrés au flot DPU / Vitis AI : impact sur la traçabilité et la qualification.
- Mesure de puissance / énergie non décrite : comparabilité entre travaux (`power_scope`).

## Statut de lecture

Papier complet (fulltext.md lu en entier). Tables reconstruites par Docling (Table III) et corps de plusieurs tableaux du texte extraits de façon désordonnée (Tables VI à X mélangées avec du texte) : chiffres à vérifier, confiance `medium`. Figures (RD curves) non lisibles dans le texte.
Déduit et non affirmé par les auteurs : l'incohérence de 2.88 J/frame (~125 W), l'absence de publication du code, la transposabilité à YOLO et à la certification.
