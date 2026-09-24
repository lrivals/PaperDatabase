---
id: arxiv-2411.01431-efficient-deep-learning-infrastructures-embedded
fiche: done
date: 2026-09-24
---

# Efficient Deep Learning Infrastructures for Embedded Computing Systems: A Comprehensive Survey and Future Envision

Xiangzhong Luo, Di Liu, Hao Kong, Shuo Huai, Hui Chen, Guochu Xiong, Weichen Liu, 2024, ACM Transactions on Embedded Computing Systems. https://doi.org/10.1145/3701728 (texte lu : version arXiv 2411.01431)
Type : article de journal (DOI éditeur trouvé via Crossref)

## Problème

Réduire l'écart entre des DNN toujours plus coûteux et des systèmes embarqués contraints :
survey des « infrastructures » d'apprentissage profond efficaces pour l'embarqué, de
l'entraînement à l'inférence, des CNN aux LLM, du logiciel au matériel (Abstract, §1).

## Méthode

Survey narratif en sept volets, chacun conclu par des « Future Envision » (§1.1, Fig. 1) :

1. Conception manuelle : convolutions efficaces (pointwise, groupwise, depthwise, Ghost,
   partial), familles MobileNet/ShuffleNet/GhostNet/FasterNet, ViT efficaces (LeViT,
   MobileViT, EfficientViT, EdgeViT, FastViT) (§2).
2. NAS matériel-aware : espaces cellule/bloc, RL/évolutionnaire/différentiable,
   prédicteurs de latence (tables, MLP, GNN, HELP), proxies zero-cost, benchmarks NAS (§3).
3. Compression : élagage non structuré/semi-structuré/structuré, quantification (binaire,
   ternaire, INT8, mixte, QAT, HAQ), distillation (§4).
4. Apprentissage sur l'appareil : entraînement économe (checkpointing, élagage de
   gradients, entraînement bas bits, 256 Ko), apprentissage continu, transfer learning
   (TinyTL), fédéré (§5).
5. LLM efficaces (§6) ; 6. frameworks logiciels et matériels (§7) ; 7. applications (§8).

## Plateforme et implémentation

Sans objet (survey). Matériel recensé (Table 4) : Jetson TX2/Nano/AGX Xavier/Xavier NX/AGX
Orin/Orin NX, Intel NCS, Google Edge TPU et Coral Dev Board, HiKey 970, Orange Pi AI Stick
Lite. **Aucun FPGA.**

## Résultats

Chiffres repris des travaux cités (non vérifiés ici) :

| Élément | Valeur | Source |
|---|---|---|
| MobileNetV2 | 300 M FLOPs, 3,4 M param., 72,0 % top-1 ImageNet | §2.1 |
| GhostNetV2 | 167 M FLOPs, 6,1 M param., 75,3 % top-1 | §2.1 |
| MobileNetV2 vs MobileViTv1 | ~2× plus rapide sur Galaxy S21 à FLOPs égaux | §2.3 |
| PiT vs DeiT sur iPhone 12 | 3× moins de FLOPs, latence 10,56 vs 10,99 ms | §2.3 |
| Mémoire d'entraînement ResNet-50 (batch 16) | activations 13,9× les paramètres | §5.1, Fig. 27 |
| TinyTL | mémoire d'entraînement de >250 Mo à 16 Mo | §5.3 |
| Jetson AGX Orin | 15-40 W, 275 TOPS, 1999 $ | Table 4 |
| Google Edge TPU | 2 W, 4 TOPS, 75 $ | Table 4, §7.2 |

Messages clés : les FLOPs ne prédisent pas la latence réelle, il faut optimiser latence et
énergie mesurées (§2.3, §6.5) ; le goulot de l'entraînement embarqué est la mémoire
d'activations, pas les paramètres (§5.1) ; l'élagage non structuré n'accélère que sur
matériel dédié (§4.1).

→ reportés dans `benchmarks.csv` : aucune ligne (survey : chiffres de travaux cités).

## Limites et critique

- **Aucune couverture des FPGA** malgré un titre « embedded computing systems » : ni
  toolflows (hls4ml, FINN, Vitis AI), ni accélérateurs FPGA, ni comparaison FPGA / GPU
  embarqué. Le matériel est réduit aux Jetson, TPU et NPU (§7.2, Table 4).
- **Apprentissage continu embarqué traité en une page** (§5.2) : liste de références, aucun
  chiffre d'énergie, de latence ou de mémoire, aucun accélérateur de CL.
- Comparaisons hétérogènes assumées (« different training recipes », Fig. 3 et 6) ;
  chiffres de plateforme constructeur (TOPS crête, prix de lancement) (Table 4).
- Erreur factuelle probable : Edge TPU « 2 TFLOPS » (§7.2) alors qu'il s'agit d'un
  accélérateur INT8 (déduit).
- Poids important des travaux des auteurs (LightNAS, EdgeNAS, HSCoNAS, SurgeNAS…) —
  affiliation commune supposée, non vérifiée dans le texte extrait.
- Très large, peu profond sur chaque sujet ; section LLM hors périmètre embarqué réel
  (systèmes multi-GPU, §6.4).

## Pertinence pour la thèse

Utile comme carte des techniques algorithmiques (NAS matériel-aware, compression,
apprentissage embarqué) et comme preuve d'un angle mort : les surveys « embarqué » grand
public ignorent les FPGA, et traitent l'apprentissage continu sans matériel. Pour la
thèse, retenir surtout §5 (mémoire d'activations, TinyTL, entraînement 256 Ko) comme
contraintes de conception d'un CL sur FPGA, et §3 (prédicteurs de latence) pour une
co-conception réseau/FPGA.

## Gaps identifiés

- NAS matériel-aware ciblant des FPGA (prédicteurs de latence/ressources FPGA) : absent de
  ce survey ; hls4ml cite des surrogates (rule4ml) mais pour des MLP (arxiv-2512.01463).
- Apprentissage continu embarqué : pas de chiffres système ; aucune comparaison
  FPGA / Jetson / MCU pour le même algorithme de CL.
- ViT efficaces sur FPGA : non traité ici (seulement mobiles et GPU).

## Statut de lecture

Papier complet (`fulltext.md` lu en entier). Extraction : Table 1 (comparaison des NAS)
absente, Table 2 réduite à sa légende, tableau de mémoire (ResNet-50 / MbV2) mélangé à la
Table 3 ; plusieurs figures et fragments intercalés dans le texte (§2.1, §5.1).
Déduit et non affirmé par les auteurs : erreur « TFLOPS » de l'Edge TPU ; part
d'auto-citations ; absence des FPGA comme limite pour la thèse.
