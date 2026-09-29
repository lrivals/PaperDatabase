---
id: arxiv-2206.15472-device-training-256kb-memory
fiche: done
date: 2026-09-29
---

# On-Device Training Under 256KB Memory

Ji Lin, Ligeng Zhu, Wei-Ming Chen, Wei-Chen Wang, Chuang Gan, Song Han, 2022, 36th Conference on Neural Information Processing Systems (NeurIPS 2022) (la version arXiv est la camera-ready, changelog v3). https://arxiv.org/abs/2206.15472
Type : conférence (relue par les pairs) ; le champ `venue` de metadata.json (« arXiv preprint ») a été corrigé d'après le texte.

## Problème

Adapter un modèle après déploiement (fine-tuning sur données capteur) est impossible sur microcontrôleur : les frameworks (PyTorch, TensorFlow) demandent plus de 300 Mo pour MobileNetV2-w0.35 en batch 1, contre 256 KB de SRAM (>1000x d'écart, §1). Deux difficultés : les graphes réellement quantifiés (INT8, sans BatchNorm) sont difficiles à optimiser ; la rétropropagation complète dépasse la mémoire.

## Méthode

Co-design algorithme/système (§2) : (1) Quantization-Aware Scaling (QAS), règle de mise à l'échelle des gradients sans hyperparamètre qui corrige le déséquilibre poids/gradient (facteur s^-2, Eq. 3-4) et permet un entraînement INT8 complet ; (2) Sparse Update : mise à jour des biais des dernières couches et de sous-ensembles de couches ou de canaux, schéma choisi par analyse de contribution et recherche évolutive sous budget mémoire (Eq. 5, ~10^30 combinaisons pour MCUNet) ; (3) Tiny Training Engine (TTE) : différentiation automatique au moment de la compilation, élagage du graphe backward, réordonnancement des opérateurs avec mise à jour en place, génération de code sans runtime Python. Classifieur conservé en FP32 (annexe C, +2,3 % de précision moyenne).

## Plateforme et implémentation

STM32F746 (Cortex-M7, 320 KB SRAM, 1 MB Flash), backend TinyEngineV2, batch 1 (§3.1). Les précisions sur plusieurs jeux sont simulées sur GPU RTX 3090, avec, selon les auteurs, un niveau de précision équivalent à l'entraînement sur MCU (§3.1, annexe C ; écart de 2,5 % sur VWW sans gradient accumulation). Aucun FPGA. Puissance et énergie : n/r (seule l'économie d'énergie est évoquée qualitativement). Code : lien projet dans la version arXiv, non vérifié ici (changelog v4 « update project and demo links »).

## Résultats

- QAS (Table 1, MCUNet, deux derniers blocs) : accuracy moyenne INT8 SGD-M 64,9 %, Adam 71,8 %, INT8+QAS 73,5 % vs FP32 73,3 %.
- Mémoire : 303 MB (PyTorch) vers 141 KB pour MobileNetV2-w0.35 (Fig. 1) ; sparse update réduit le pic de mémoire mesurée de 7-9x, le réordonnancement porte à 20-21x au total ; les 3 modèles tiennent dans 256 KB (§3.2, Fig. 10a).
- Vitesse : 23-25x plus rapide que la mise à jour complète avec noyaux TF-Lite Micro ; latence de la référence complète projetée (OOM) (§3.2, Fig. 10c).
- VWW : 89,1 % top-1 avec 206 KB de SRAM mesurée, avec gradient accumulation (§3.2), contre 88,7 % pour MCUNet entraîné dans le cloud et 86,2 % pour TF-Lite Micro+MobileNetV2 (inférence seule).
- Sparse update donne une meilleure précision moyenne que la mise à jour des k dernières couches avec 4,5-7,5x moins de mémoire (Fig. 9, analytique).
→ reportés dans `benchmarks.csv` (via bench_rows.csv) : 1 ligne (MCUNet-5FPS sur STM32F746, VWW, §3.2, confidence medium car chiffre lu dans le texte).

## Limites et critique

- Cible MCU, pas FPGA ; CNN de classification uniquement (limite reconnue par les auteurs : pas de RNN, Transformers, audio) ; pas de détection d'objets.
- Il s'agit de transfert d'apprentissage (fine-tuning) sur jeu fixe, non d'apprentissage continu : pas de mesure de l'oubli catastrophique ni de flux de classes.
- Précisions multi-jeux obtenues par simulation GPU et non sur cible ; hyperparamètres (taux d'apprentissage) réglés jeu par jeu pour rapporter le meilleur résultat (annexe C). La comparaison à MCUNet sur VWW (89,1 vs 88,7) est faite avec gradient accumulation.
- Latence absolue et énergie non rapportées dans le texte ; comparaison de vitesse avec TF-Lite Micro utilise ses noyaux d'inférence (pas d'entraînement natif) et une extrapolation pour le cas OOM.
- Le schéma de mise à jour est choisi hors ligne, propre à chaque modèle.

## Pertinence pour la thèse

Axe `continual-learning` (référence MCU, comparable à la famille FPGA). Idées transposables à un accélérateur FPGA : entraînement INT8 réel, mise à jour sparse par couche/canal, graphe backward compilé statiquement (compatible avec l'allocation mémoire statique nécessaire à la certification, déduit). Pour la thèse sur la sûreté, l'adaptation en ligne pose une difficulté (modèle qui change après déploiement, non compatible telle quelle avec une certification figée, déduit) ; l'article ne l'aborde pas.

## Gaps identifiés

- Apprentissage/fine-tuning embarqué sur FPGA de détecteurs (YOLO), pas seulement de classifieurs, sous budget mémoire on-chip.
- Assurance et surveillance d'un modèle qui s'adapte après déploiement.

## Statut de lecture

papier complet (corps et annexes A-H de fulltext.md). Table 5 reconstruite par Docling (à vérifier) : ses chiffres ne sont pas utilisés ; le texte principal donne les 89,1 % et 206 KB. Le texte de Table 5 apparaît mélangé avec le tableau de sélection de canaux. Déduit et non affirmé par les auteurs : la transposabilité au FPGA, l'incompatibilité avec la certification, l'absence de mesures énergétiques (le texte n'en donne pas).
