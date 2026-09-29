---
id: arxiv-2006.08357-codenet-efficient-deployment-input-adaptive
fiche: done
date: 2026-09-29
---

# CoDeNet: Efficient Deployment of Input-Adaptive Object Detection on Embedded FPGAs

Zhen Dong, Dequan Wang, Qijing Huang, Yizhao Gao, Yaohui Cai, Tian Li, Bichen Wu, Kurt Keutzer, John Wawrzynek, 2020, FPGA 2021 (ACM/SIGDA, venue donnée par arXiv journal_ref). https://arxiv.org/abs/2006.08357 ; le DOI de `metadata.json` (10.5281/zenodo.4341394) est un DOI Zenodo, probablement celui de l'artefact et non de l'article (déduit).
Type : conférence (version arXiv lue, non la version publiée)

## Problème

La détection d'objets sur FPGA embarqué est peu traitée (l'essentiel des travaux vise la classification). Les convolutions déformables, à l'état de l'art en précision, sont mal supportées par les accélérateurs : accès mémoire irréguliers dépendant des offsets, peu de réutilisation des entrées, bande passante d'offsets, interpolation bilinéaire coûteuse (§1, §3).

## Méthode

- Modifications de la convolution déformable adaptées au matériel (Fig. 3, §3.1) : remplacement par une convolution depthwise 3x3 + 1x1 ; offsets bornés à [0, N] (N = 7) pour mettre les entrées en buffer ; forme carrée (un seul paramètre de distance) ; offsets arrondis à des entiers (pas d'interpolation bilinéaire).
- Optimisations matérielles par modification : cache LLC via ACP, line buffer de 2N lignes, ports parallèles vers trois line buffers (§3.2).
- Réseau CoDeNet : ShuffleNetV2 comme extracteur, blocs de suréchantillonnage à convolution déformable, tête CenterNet sans NMS (top-100 pics), concaténation au lieu de connexions résiduelles (§4.1).
- Quantification 4 bits poids (par canal) / 8 bits activations (par couche), quantificateur uniforme symétrique, fine-tuning consciente de la quantification avec STE (§4.1).
- Accélérateur dataflow en Vivado HLS : moteur 1x1 16x16 MAC, moteur depthwise 3x3 (16 canaux), unité de quantification ; première couche, split/shuffle/concat sur le processeur ARM (§4.2).

## Plateforme et implémentation

Ultra96, Zynq UltraScale+ MPSoC XCZU3EG, 250 MHz après place and route (§5). Ressources : 34 144 LUT (48,4 %), 41 827 FF (29,6 %), 216 BRAM (100 %), 360 DSP (100 %) (Table 6, reconstruit par PyMuPDF, à vérifier). Puissance : 4,3 W sur la ligne d'alimentation de l'Ultra96 sans charge sur la PL, 5,6 W avec le réseau, lue par un moniteur de puissance, donc portée carte (§5) ; 5,75 fps/W pour la config a. Latence à batch 1 (§5). Code : DOI Zenodo cité dans les métadonnées (à vérifier), rien d'autre dans le texte.

## Résultats

- Ablation de l'opération (Table 1) : 3x3 déformable 42,9 AP VOC contre 42,3 pour un 9x9 régulier ; version finale (depthwise, bornée, carrée, offsets entiers) 41,1 AP VOC, 21,5 AP COCO.
- Accélération matérielle : 1,36x pour la convolution déformable complète, 9,76x pour la depthwise (§3.2, Table 2) ; latences par variante dans la Table 2.
- VOC07, w4a8 (Tables 3 et 5) : config a 256x256, 51,1 AP50, 32,2 fps (latence 31 ms, §5) ; config b 55,1 AP50, 26,9 fps (37 ms) ; config c 512x512, 61,7 AP50, 9,3 fps ; config d 67,1 AP50, 5,2 fps ; config e 69,7 AP50, 4,6 fps. Taille de modèle 0,76 MB (config a-c), 2,90 MB (d-e) ; Tiny-YOLO 416x416 FP32 : 57,1 AP50, 60,5 MB, 3,49 GMACs (Table 3).
- COCO : CoDeNet1x 22,2 AP en FP32 et 18,8 AP en 4/8 bits ; CoDeNet2x 26,1 et 21,0 (Table 4). Aucune mesure matérielle sur COCO.
- Comparaison (Table 5, Table reconstruite en partie) : FINN-R (Zynq XC7Z045, w1a3, 224x224) 16 fps, 50,1 AP50 ; Tiny-Yolo-v2 [11] (Ultra96, w16a16) 43,1 fps, 48,5 AP50. Le résumé annonce « 26,9 fps, 0,76 MB, 61,7 AP50 » : cela mélange la config b (26,9 fps, 55,1 AP50) et la config c (61,7 AP50, 9,3 fps) d'après les Tables 3 et 5.
→ reportés dans `benchmarks.csv` : 5 lignes (configs a à e, VOC07), dans `bench_rows.csv`.

## Limites et critique

- Incohérence entre le résumé et les Tables 3 et 5 : 26,9 fps et 61,7 AP50 n'appartiennent pas à la même configuration ; à retenir, les tableaux.
- Tiny-YOLO est une référence FP32 (accuracy 57,1) et Tiny-Yolo-v2 [11] a 48,5 AP50 en 16 bits : comparaisons entre précisions, résolutions et FPGA différents (Zynq-706 pour FINN-R). Le « 10 % plus précis que Tiny-YOLO » compare un modèle quantifié à un baseline FP32 ancien.
- Débit à 512x512 modeste (4,6 à 9,3 fps) ; le temps réel n'est atteint qu'en 256x256 avec AP50 51-55 %. La première couche et les couches non accélérées tournent sur le processeur ARM.
- Puissance : carte entière avec 4,3 W de repos, pas de puissance par configuration hors config a.
- Aucun résultat COCO sur matériel ; GOPS effectifs non rapportés (les 128 et 72 GOPS du §4.2 sont des pics théoriques).
- Aucune considération de robustesse, de déterminisme ou de sûreté ; l'accès mémoire dépendant des données (offsets) est un facteur d'incertitude temporelle, atténué par le bornage (déduit).

## Pertinence pour la thèse

Bonne référence de co-conception réseau/accélérateur pour la détection sur SoC FPGA, avec ressources, puissance carte et latence batch 1, et ancre de comparaison à Tiny-YOLO et FINN-R. Détecteur sans NMS (CenterNet) : intéressant pour la simplicité et le déterminisme d'un pipeline (déduit). Ne traite ni YOLO récents, ni personnes/vidéosurveillance, ni sûreté ou certification ; reste ouvert : passage aux classes personnes en zone industrielle, analyse WCET/déterminisme, robustesse de la quantification 4 bits.

## Gaps identifiés

- Détecteurs anchor-free / sans NMS sur FPGA avec analyse du déterminisme temporel.
- Évaluation de robustesse (OOD, fautes) d'un détecteur quantifié 4/8 bits.
- Comparabilité des mesures de puissance (ici carte, avec repos de 4,3 W).

## Statut de lecture

Papier complet (texte extrait lu en entier). Table 6 reconstruite par PyMuPDF, chiffres à vérifier ; Table 5 en partie mal alignée (FINN-R et Tiny-Yolo-v2 sur la même ligne, attributions recoupées par le texte du §5 et de l'ordre des colonnes). Déduit et non affirmé par les auteurs : incohérence du résumé (constat comparatif), lien du DOI Zenodo avec un artefact, remarques sur le déterminisme et la pertinence pour la thèse.
