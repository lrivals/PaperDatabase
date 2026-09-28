---
id: arxiv-1907.11093-slimyolov3-narrower-faster-better-real
fiche: done
date: 2026-09-28
benchmarks: none
---

# SlimYOLOv3: Narrower, Faster and Better for Real-Time UAV Applications

Pengyi Zhang, Yunxin Zhong, Xiaoqiong Li, 2019, arXiv preprint. https://doi.org/10.1109/ICCVW.2019.00011
Type : preprint non relu par les pairs selon `metadata.json` (version arXiv lue) ; le DOI
renvoie à ICCV Workshops 2019 (ICCVW), donc une version publiée en atelier existe (à
vérifier).

## Problème

La détection temps réel à bord d'un UAV bute sur la mémoire et le calcul limités de
l'embarqué ; les vitesses « temps réel » des YOLO sont mesurées sur GPU puissant (§1,
§2). Les auteurs cherchent à réduire FLOPs et paramètres de YOLOv3 sans perte notable de
précision sur images de drone (VisDrone) (§1).

## Méthode

- **Network slimming** (Liu et al. [24]) appliqué à YOLOv3 : régularisation L1 sur les
  facteurs d'échelle γ des BatchNorm (sparsity training, 100 époques, pénalité α ∈ {0,01 ;
  0,001 ; 0,0001}, retenu 0,0001 car 0,01 sous-apprend), puis élagage des canaux sous un
  **seuil global** (percentile n de tous les γ) et un **seuil local de sécurité**
  (percentile 90 par couche, au moins 10 % des canaux gardés), puis fine-tuning (§3,
  §4.2, §4.3, §5).
- Traitement des connexions Darknet : masques concaténés pour les couches `route`, OU
  logique des masques pour les couches reliées par `shortcut` (§3).
- Modèle de départ **YOLOv3-SPP3** : trois modules SPP (maxpool 1, 5, 9, 13) devant les
  trois têtes (§4.2, Fig. 4). Trois modèles élagués : **SlimYOLOv3-SPP3-50 / -90 / -95**
  (50 % élagué itérativement deux fois ; 90 % et 95 % en une passe « agressive ») (§4.2).
- Baselines : YOLOv3-tiny (416) et YOLOv3-SPP1 (608) ; entrées testées 416, 608 et 832
  (§4.2-4.4). Darknet pour l'entraînement normal et le fine-tuning, PyTorch pour la
  sparsity training (§4.3).
- Métriques : précision, rappel, mAP@0.5, F1, volume, paramètres, FLOPs, FPS ; seuils
  conf 0,1, NMS 0,5 (§4.4).

## Plateforme et implémentation

- Mesures sur **une NVIDIA GTX 1080 Ti, Darknet, sans batch** (batch 1) (§4.4) ; serveur
  Xeon E5-2683 v3 + 4× GTX 1080 Ti pour l'entraînement (§4).
- **Aucune plateforme embarquée** (ni Jetson, ni FPGA, ni MCU), malgré le titre ;
  puissance : n/r.
- Code publié : https://github.com/PengyiZhang/SlimYOLOv3 (Abstract).

## Résultats

Chiffres lus dans le texte (entrée 832×832, par rapport à YOLOv3-SPP3) (§5) :

| Modèle | FLOPs | Paramètres | Volume | Temps d'inférence (GTX 1080 Ti) |
|---|---|---|---|---|
| SlimYOLOv3-SPP3-50 | −57,1 % | −67,4 % | −67,5 % | −38,8 % |
| SlimYOLOv3-SPP3-90 | −85,9 % | −87,5 % | −87,4 % | −42,6 % |
| SlimYOLOv3-SPP3-95 | −90,8 % | −92,0 % | −92,0 % | −49,5 % |

- SPP3 contre SPP1 : comparable en 416 et 608 ; ~+1 % de mAP et de F1 en 832 (§5, Fig. 5),
  pour +21 BFLOPs (§5, fragment).
- SlimYOLOv3-SPP3-90 et -95 ont une précision « comparable à YOLOv3 » avec moins de
  paramètres que YOLOv3-tiny ; l'élagage itératif à 50 % préserve mieux la précision que
  l'élagage agressif (§5, Fig. 1, Table 1).
- **SlimYOLOv3 reste bien plus lent que YOLOv3-tiny à FLOPs comparables** ; les auteurs
  l'attribuent à la profondeur (dépendance séquentielle des couches) et y voient un
  plafond à l'accélération par élagage de canaux (§5).
- Déséquilibre de classes non traité : AP « car » très supérieure à « bicycle » (§5,
  Tables 2-3).

→ reportés dans `benchmarks.csv` : aucune ligne. Le **corps de la Table 1** (mAP, FPS,
BFLOPs, ms, paramètres par modèle et par taille d'entrée) **n'est pas extrait** : seul
l'en-tête de colonnes subsiste. Le texte ne donne que des réductions relatives, sans
aucune valeur absolue de mAP ni de FPS ; une ligne n'aurait que des `n/r`.

## Limites et critique

- **« Real-Time UAV Applications » sans aucune mesure embarquée** : tout est sur GTX 1080
  Ti (gamme GPU de bureau, ~250 W, déduit), à rebours de la règle d'exclusion « GPU de
  bureau présenté comme embarqué » du profil. L'argument énergétique (« power consumption
  is always positively correlated with FLOPs », §6) est affirmé, pas mesuré.
- **Réduction de FLOPs ≠ accélération** : −90,8 % de FLOPs pour seulement −49,5 % de temps
  (×2) ; les auteurs le reconnaissent (§5). Sur FPGA ou MCU, le rapport pourrait être
  différent (déduit) ; rien ne le mesure ici.
- **Évaluation sur le jeu de validation** (548 images) VisDrone2018-Det, pas sur le
  test-dev (§4.1) : chiffres non comparables aux résultats de challenge.
- **mAP@0.5 seulement**, pas de mAP_small ni de mAP@[.5:.95], alors que VisDrone est
  dominé par les petits objets.
- Pas de quantification ; FP32 implicite (déduit).
- Baselines : YOLOv3-tiny et YOLOv3, sans autre méthode de compression.

## Pertinence pour la thèse

- **Axe `drone-detection`** : référence historique très citée pour l'**élagage de canaux
  de YOLO sur VisDrone**. Point de départ naturel d'une chaîne élagage → quantification
  → FPGA (le modèle élagué est « régulier », facile à décrire en configuration, §2.2).
- Son constat principal (FLOPs ÷ 10, vitesse ×2 sur GPU) est une **question ouverte
  pour le FPGA** : sur un accélérateur dataflow (FINN, hls4ml), la réduction de canaux
  se traduit plus directement en ressources et en débit (déduit, à vérifier).
- N'apporte rien sur la puissance, la plateforme embarquée, ni les petits objets en
  particulier.

## Gaps identifiés

- **Élagage de YOLO pour drone mesuré sur plateforme embarquée** (Jetson, FPGA) :
  absent ici ; le gain ×2 sur GPU de bureau ne dit rien de l'embarqué.
- **Effet de l'élagage sur mAP_small** : non mesuré (mAP@0.5 global seulement), dans la
  lignée de l'hypothèse « quantification et mAP_small » de gaps.md.
- **FLOPs vs latence** : la non-proportionnalité observée est un argument pour mesurer la
  latence réelle sur la cible plutôt que les FLOPs.

## Statut de lecture

Papier complet (`fulltext.md` lu en entier, extraction GROBID `ok`). **Table 1 (résultats
principaux) sans corps extrait** — seul l'en-tête de colonnes subsiste — bien que
`extraction.warnings` ne le signale pas ; Tables 2-3 (AP par classe) et Figures 1, 5, 6
absentes : aucune valeur absolue de mAP, FPS ou BFLOPs n'a pu être lue. Formules (1)-(2)
et symboles (γ, λ, seuils) perdus à l'extraction ; section 2.1 rejetée en fin de fichier.

Ce qui suit est déduit et non affirmé par les auteurs :
- la gamme de puissance de la GTX 1080 Ti ;
- la précision FP32 ;
- l'hypothèse d'une meilleure traduction de l'élagage en gains sur FPGA dataflow.
