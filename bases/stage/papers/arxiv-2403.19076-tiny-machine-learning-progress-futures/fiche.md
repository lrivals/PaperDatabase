---
id: arxiv-2403.19076-tiny-machine-learning-progress-futures
fiche: done
date: 2026-09-29
---

# Tiny Machine Learning: Progress and Futures

Ji Lin, Ligeng Zhu, Wei-Ming Chen, Wei-Chen Wang, Song Han, 2023, IEEE Circuits and Systems Magazine 23(3), 8-34. https://doi.org/10.1109/MCAS.2023.3302182
Type : article de journal (revue, centrée sur les travaux des auteurs : MCUNet, TinyEngine, TTE)

## Problème

Les MCU ont moins de 256 Ko de SRAM, pas de DRAM ni d'OS ; les modèles « mobiles » ne réduisent pas
la **mémoire de pointe des activations**, qui est le vrai goulot : MobileNetV2-1.4 a 4,2× moins de
paramètres que ResNet-50 mais une mémoire de pointe 2,3× plus grande, et l'entraînement demande
6,9× la mémoire de l'inférence (§I-A, Fig. 2). Il faut co-concevoir algorithme et système, pour
l'inférence comme pour l'entraînement (§I-A3).

## Méthode

Revue en deux volets : état de l'art (§II, Tables II-III) puis présentation des travaux du MIT
Han Lab.

- **Inférence (MCUNet)** (§III) : TinyNAS (optimisation de l'espace de recherche par la CDF des
  FLOPs, puis NAS Once-For-All) + TinyEngine (compilation spécifique au modèle, convolution
  depthwise en place, **inférence par patchs** pour les premiers blocs et redistribution du champ
  récepteur), recherche conjointe architecture + ordonnancement.
- **Entraînement (MCUNetV3 / Tiny Training)** (§IV) :
  - **Quantization-Aware Scaling (QAS)** : l'entraînement d'un graphe réellement INT8 déforme le
    rapport ‖W‖/‖G‖ d'un facteur s⁻² ; QAS multiplie les gradients par s⁻² (poids) et s⁻² (biais)
    pour retrouver le comportement flottant, sans hyperparamètre ni mémoire en plus (Eq. 1-4) ;
  - **mise à jour parcimonieuse** : choix des biais, des couches et de la fraction de canaux à
    mettre à jour par analyse de contribution et recherche évolutive sous contrainte mémoire
    (Eq. 5, Fig. 17-18) ;
  - **Tiny Training Engine (TTE)** : différentiation au moment de la compilation, élagage du graphe
    arrière, réordonnancement des opérateurs pour appliquer la mise à jour en place (§IV-C,
    Fig. 19-20).

## Plateforme et implémentation

- MCU : STM32F412 (256 Ko SRAM, 1 Mo Flash), STM32F746 (Cortex-M7, 216 MHz, 320 Ko SRAM), STM32H743
  (480 MHz, 512 Ko SRAM, 2 Mo Flash) (§II-A, Tables III-IV).
- Modèles INT8 (INT4 pour certaines variantes MCUNet) ; entraînement INT8 avec QAS.
- Puissance, énergie : n/r (latence et mémoire seulement).
- Code et modèles : https://github.com/mit-han-lab/mcunet (Table III, note 4).

## Résultats

- **Inférence**, même MCU STM32H743 (Table III) : pour mcunet-vww1 (VWW 88,9 %), TinyEngine 51 ms et
  92 Ko de mémoire de pointe, contre X-Cube-AI 57 ms / 113 Ko, CMSIS-NN 97 ms / 220 Ko, TFLite Micro
  1120 ms / 220 Ko. TinyEngine jusqu'à ×22 plus rapide que TFLite Micro (Fig. 7).
- ImageNet sur MCU (Table IV) : MCUNet-M4 (patchs, INT8) **64,9 % top-1** sous 196 Ko de SRAM sur
  STM32F412 ; MCUNet-H7 **71,8 %** sous 465 Ko sur STM32H743.
- VWW > 90 % sous 32 Ko de SRAM (Fig. 14) ; détection Pascal VOC : 68,3 % mAP sur H743 (Table V).
- **Entraînement** : graphe INT8 avec SGD-M seul → 64,9 % de moyenne sur 8 jeux, contre 73,3 % en
  FP32 ; **avec QAS 73,5 %** ; Adam 71,8 % mais ×3 de mémoire d'optimiseur (Table VII).
- Mémoire d'entraînement ramenée de 303 Mo (PyTorch) à **149 Ko** pour MobileNetV2-w0.35, batch 1,
  128×128 (Fig. 15) ; mises à jour parcimonieuses ÷ 7-9, avec réordonnancement ÷ 20-21 (Fig. 21a) ;
  entraînement ×23-25 plus rapide qu'avec les noyaux TFLite Micro (Fig. 21c) ; les 3 modèles testés
  s'entraînent sous 256 Ko sur STM32F746.

→ reportés dans `benchmarks.csv` : 4 lignes (MCUNet-M4 et MCUNet-H7 sur ImageNet, Table IV ;
mcunet-vww1 + TinyEngine sur STM32H743, Table III ; fine-tuning INT8 + QAS, Table VII).

## Limites et critique

- Revue largement consacrée aux travaux des auteurs (MCUNet, TinyEngine, TTE) : comparaisons
  établies par les mêmes auteurs, sans évaluation indépendante.
- **Vision uniquement** (CNN) ; séries temporelles, capteurs industriels et détection d'anomalies
  ne sont évoqués qu'en perspective (§V).
- Pas de mesure d'énergie ni de puissance ; Table II (état de l'art avec énergie) non extraite, et
  une note signale une erreur d'unité (mJ au lieu de µJ) dans des papiers cités (Table II, note 4).
- L'entraînement présenté est du **transfert / fine-tuning** sur une tâche, pas de l'apprentissage
  continu : pas de mesure d'oubli.
- Table VII : résultats de fine-tuning « simulant » le coût réduit, pas mesurés sur MCU.

## Pertinence pour la thèse

Référence essentielle pour l'**entraînement INT8 sur MCU**, cœur technique d'un « EWC INT8 sur
MCU » : QAS explique pourquoi le gradient d'un graphe quantifié est mal échelonné et donne la
correction (gradients × s⁻²). Cette correction concerne aussi le calcul d'une Fisher à partir de
gradients INT8 (déduit). Les ordres de grandeur (149 Ko pour entraîner MobileNetV2-w0.35, analyse de
contribution pour choisir les couches à mettre à jour) situent le budget d'un EWC restreint aux
couches mises à jour. Table III fournit une comparaison propre des moteurs d'inférence (CMSIS-NN,
X-Cube-AI, TFLite Micro) sur un même MCU.

## Gaps identifiés

- Entraînement INT8 (QAS + mise à jour parcimonieuse) en scénario d'apprentissage continu, avec
  mesure de l'oubli : non traité.
- Calcul de la Fisher / des importances EWC sur gradients INT8 et effet de l'échelle s⁻².
- TinyML pour séries temporelles de capteurs industriels : laissé en perspective (§V).

## Statut de lecture

Papier complet (`fulltext.md` lu en entier). Table II absente, Table V sans corps propre (valeurs
lues dans le bloc fusionné avec la Table VI), Table VII partiellement désalignée (ligne QAS lisible) ;
figures non disponibles (Fig. 15 et 21 citées d'après leurs légendes).
Déduit et non affirmé par les auteurs : application de QAS au calcul d'une Fisher, budget d'un EWC
restreint.
