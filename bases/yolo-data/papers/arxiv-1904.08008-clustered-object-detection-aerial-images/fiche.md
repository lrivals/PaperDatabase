---
id: arxiv-1904.08008-clustered-object-detection-aerial-images
fiche: todo
date: 2026-09-28
---

> **Importée de la base `drone` le 2026-10-05.** Cette fiche a été écrite pour une autre base (autre thème) : pertinence à réévaluer ici, puis `fiche: done` via `/paper-fiche`. Statut d'origine : done.

# Clustered Object Detection in Aerial Images

Fan Yang, Heng Fan, Peng Chu, Erik Blasch, Haibin Ling, 2019, arXiv preprint. https://arxiv.org/abs/1904.08008
Type : preprint non relu par les pairs (dans `metadata.json`). Le texte extrait ne mentionne
pas de venue ; ClusDet est à notre connaissance paru à ICCV 2019 (non vérifié, à confirmer
avant de citer).

## Problème

Dans les images aériennes haute résolution (~2000×1500 px pour VisDrone), les objets sont
**petits** et **répartis de façon éparse et non uniforme** (§1). Le découpage uniforme en
tuiles (EIP, evenly image partition) améliore les petits objets mais gaspille du calcul :
sur VisDrone, >73 % des tuiles d'une grille sont « sparse », dont 23 % vides (Fig. 1). Les
auteurs observent que les objets sont **groupés** (piétons sur les places, véhicules sur
les routes) et veulent concentrer le détecteur sur ces groupes.

## Méthode

ClusDet, bout en bout, trois sous-réseaux (§3, Fig. 2) :
- **CPNet** (cluster proposal) : type RPN, mais propose des **régions de groupes** ; conv
  5×5 + deux conv 1×1 sur les features haut niveau (§3.2.1, §4.1). Vérité terrain des
  groupes générée par une stratégie décrite en matériel supplémentaire (non inclus).
- **ICM** (iterative cluster merging) : fusion non-max des groupes (seuil 0,7) jusqu'à
  TopN groupes (3 sur VisDrone, 2 sur UAVDT, 5 sur DOTA) (§3.2.2, §4.1).
- **ScaleNet** : régression de l'échelle moyenne des objets de chaque groupe (FC 1024),
  puis **partition ou padding** du crop pour ramener les objets dans [70, 280] px (§3.3).
- **DetecNet** : Faster R-CNN + FPN (Detectron, Caffe2) sur les crops ; fusion
  local/global par NMS 0,5 (§3.4, §4.1). Entrée 600×1000 (VisDrone, UAVDT), 1000×1000 (DOTA).

## Plateforme et implémentation

Aucune cible embarquée : entraînement sur 2 GPU, temps d'inférence mesuré sur une **GTX
1080 Ti** (légende Table 1). Précision numérique n/r (FP32 implicite, non dit). Code
annoncé sur https://github.com/fyangneil (Abstract), dépôt précis n/r.

## Résultats

VisDrone (validation, faute de serveur de test ouvert, §4.2), entrée 600×1000 (Table 1) :

| Méthode | Backbone | #img | AP | AP50 | APs | s/img (1080 Ti) |
|---|---|---|---|---|---|---|
| FRCNN+FPN | R-50 | 548 | 21,4 | 40,7 | 11,7 | 0,055 |
| FRCNN+FPN+EIP | R-50 | 3 288 | 21,1 | 44,0 | 14,4 | 0,330 |
| DetecNet+CPNet | R-50 | 1 945 | 25,6 | 47,9 | 16,2 | 0,195 |
| ClusDet | R-50 | 2 716 | 26,7 | 50,6 | 17,6 | 0,273 |
| ClusDet | X-101 | 2 716 | 28,4 | 53,2 | 19,1 | 0,773 |

- Multi-échelle + box voting : ClusDet X-101 **32,4 AP** / 56,2 AP50 (Table 2).
- UAVDT : ClusDet R-50 13,7 AP contre 11,0 pour FRCNN+FPN et 6,6 avec EIP (Table 3) ;
  l'EIP dégrade car les véhicules sont au centre et se font couper (§4.6).
- DOTA (5 classes mobiles seulement, 920 / 285 images) : 32,2 AP (R-50) avec 1 055 images
  traitées contre 2 838 pour EIP ; AP50 inférieur, AP75 supérieur (Table 4, §4.6).
- TopN : au-delà de 4, l'AP plafonne ~27 alors que le nombre d'images croît (Fig. 7).

→ reportés dans `benchmarks.csv` : 8 lignes (VisDrone R-50 / R-101 / X-101 avec latence
GPU, VisDrone X-101 multi-échelle, UAVDT R-50, DOTA R-50 / R-101 / X-101), `confidence:
high`.

## Limites et critique

- **« Efficacité » mesurée en nombre de crops, pas en coût réel** : ClusDet R-50 prend
  0,273 s/img contre 0,055 s pour FRCNN+FPN sans découpage, soit ~5× plus lent que la
  baseline globale (Table 1) ; il n'est plus rapide que l'EIP. Environ 3,7 FPS sur une GPU
  de bureau (déduit de 0,273 s) : **rien d'embarqué**.
- Évaluation VisDrone sur la **validation** (548 images), pas sur le test ; TopN réglé par
  jeu de données.
- DOTA filtré aux classes « groupables », ce qui favorise la méthode (les auteurs le
  justifient, §4.2).
- Baselines UAVDT reprises de [8] (sauf FRCNN+FPN), donc conditions non homogènes (§4.6).
- Détecteur deux étages (Faster R-CNN) : très loin des contraintes de latence / puissance
  d'un drone ; pas d'étude sur détecteur un étage.
- Pas de puissance, pas de mémoire, pas de FLOPs.

## Pertinence pour la thèse

- Référence fondatrice de la famille **« cluster / region search »** pour les petits objets
  en images de drone (VisDrone, UAVDT), souvent citée par les travaux suivants (DMNet,
  GLSAN…) — à situer dans l'axe `drone-detection`.
- L'idée « ne traiter que les régions denses » est potentiellement intéressante pour
  l'embarqué (moins de pixels à inférer), mais le papier ne l'évalue pas en coût réel ; un
  portage FPGA de ce schéma à deux passes (globale + crops) reste ouvert.
- Donne des APs (petits objets) détaillés, utiles comme point de comparaison pour la
  question « quantification vs mAP_small ».

## Gaps identifiés

- Coût réel (latence, énergie) des schémas de découpage adaptatif (cluster / tiling) sur
  plateforme embarquée : non mesuré.
- Détecteurs un étage (YOLO) + sélection de régions denses sur FPGA : non traité.

## Statut de lecture

Papier complet (`fulltext.md` lu en entier, extraction GROBID `ok`). Matériel
supplémentaire (vérité terrain des groupes, détails NMM) non inclus. Tables 1 à 4 extraites
avec corps ; une coquille d'extraction dans la Table 2 (lignes multi-échelle sans marque
distinctive, identifiées par la légende).

Ce qui suit est déduit et non affirmé par les auteurs :
- la venue ICCV 2019 ;
- le ~3,7 FPS et le « ~5× plus lent » ;
- la précision FP32 ;
- la filiation avec DMNet / GLSAN.
