---
id: arxiv-2202.06934-slicing-aided-hyper-inference-fine
fiche: done
date: 2026-09-28
---

# Slicing Aided Hyper Inference and Fine-tuning for Small Object Detection

Fatih Cagatay Akyon, Sinan Onur Altinuc, Alptekin Temizel, 2022, arXiv preprint. https://doi.org/10.1109/ICIP46576.2022.9897990 (arXiv 2202.06934)
Type : `preprint` dans `metadata.json`, mais le DOI enregistré est celui d'**IEEE ICIP
2022**, donc une version publiée en conférence existe (déduit du préfixe du DOI).

## Problème

Les détecteurs pré-entraînés sur COCO ou VOC, dont les images sont en basse résolution et
les objets grands, échouent sur les **petits objets dans des images haute résolution**
issues de drones ou de caméras de surveillance. Entraîner directement en haute résolution
coûte cher en mémoire (§1, §3).

## Méthode

Un cadre **générique et indépendant du détecteur** (§3, Fig. 2) :
- **SF (Slicing aided Fine-tuning)** : le jeu d'entraînement est augmenté de tuiles qui se
  chevauchent, de taille aléatoire (480 à 640 px pour VisDrone, 300 à 500 px pour xView),
  redimensionnées à une largeur de 800 à 1333 px. Les images d'origine sont conservées
  pour les gros objets.
- **SAHI (Slicing Aided Hyper Inference)** : l'image est découpée en tuiles M×N (640×640
  pour VisDrone, 400×400 pour xView), avec un recouvrement optionnel de 25 % (PO). Chaque
  tuile est redimensionnée et inférée séparément, avec une inférence optionnelle sur
  l'image entière (FI) pour les gros objets. Les résultats sont fusionnés par NMS, avec un
  seuil de correspondance Tm = 0,5 (§3, §4).
- Applicable **sans réentraînement** (SAHI seul). Intégré à Detectron2, MMDetection et
  YOLOv5 ; évalué avec FCOS, VFNet et TOOD sous MMDetection (§4).

## Plateforme et implémentation

- Plateforme matérielle : `n/r`. Aucun temps d'inférence, aucune mémoire, aucune
  puissance. Les auteurs écrivent seulement que le temps de calcul **croît linéairement**
  avec le nombre de tuiles, à mémoire constante (§5).
- **Code publié** : https://github.com/obss/sahi (bibliothèque) et
  https://github.com/fcakyon/sahi-benchmark (configs, scripts, résultats) (§4). La
  bibliothèque est très utilisée en pratique (déduit).

## Résultats

Protocole COCO, **AP50** global et par taille (s, m, l), jusqu'à 500 détections. Test sur
VisDrone2019-DET **test-dev** (Table 1) et sur xView avec un découpage aléatoire 75/25
(Table 2).

| Détecteur, VisDrone test-dev | FI (baseline) | + SAHI + FI + PO | + SF + SAHI + FI + PO | AP50s (FI → meilleur) |
|---|---|---|---|---|
| FCOS | 25,8 | 31,0 | 38,5 | 14,2 → 25,9 |
| VFNet | 28,8 | 33,9 | 42,2 | 16,8 → 29,7 |
| TOOD | 29,4 | 34,7 | 43,5 | 18,1 → 31,7 |

(Table 1)

- Sur xView, la baseline FI est quasi nulle (AP50 d'environ 2). Le meilleur résultat est
  obtenu par **TOOD + SF + SAHI + PO, à 20,6 d'AP50** (14,9 en AP50s) (Table 2).
- Effets par taille : le recouvrement améliore les objets petits et moyens mais dégrade un
  peu les gros. FI rétablit les gros objets : TOOD + SF + FI obtient 66,4 en AP50l (Table 1,
  §4).
- L'analyse d'erreurs (TOOD) montre que la marge principale se trouve dans les faux
  positifs et les faux négatifs, pas dans la localisation (Fig. 3-4).

→ reportés dans `benchmarks.csv` : 4 lignes, en AP50 et sur une plateforme `n/r` :
- VisDrone test-dev (Table 1, `high`) : FCOS, VFNet et TOOD, chacun avec
  SF + SAHI + FI + PO ;
- xView (Table 2, `medium`, corps de tableau fusionné avec celui de la Table 1 à
  l'extraction) : TOOD + SF + SAHI + PO.

## Limites et critique

- **Aucun coût mesuré**, alors que c'est le point faible évident. Avec des tuiles de
  640×640 et 25 % de recouvrement, plus une passe sur l'image entière, SAHI multiplie les
  passes par un facteur proportionnel au nombre de tuiles (§5, « linearly »). Pour de
  l'embarqué, c'est déterminant, et ce n'est ni chiffré ni discuté pour une cible
  contrainte.
- **Chiffres du résumé partiellement incohérents avec la Table 1** (recalcul par nous).
  Le « +6,8 AP » de FCOS avec SAHI ne correspond à aucune ligne : 25,8 → 31,0 donne +5,2.
  Pour TOOD, le cumul vaut 29,4 → 43,5, soit +14,1, contre « 14,5 » annoncé. Les autres
  valeurs concordent (VFNet +5,1 et +13,4, FCOS +12,7).
- **AP50 seulement**, pas d'AP50:95, alors que le chevauchement des tuiles et la NMS de
  fusion peuvent dégrader la localisation fine.
- Les baselines FI sont affinées sans tuiles, sur des images redimensionnées à une largeur
  de 800 à 1333 px. Une partie du gain de SF vient donc simplement de la **résolution
  effective** accrue. Aucune comparaison avec un entraînement direct à plus haute
  résolution à coût égal (déduit).
- Le découpage de xView est aléatoire et non standard : pas de comparaison externe.
- La fusion par NMS entre tuiles (doublons sur les objets coupés) n'est pas évaluée
  séparément.

## Pertinence pour la thèse

- **Référence incontournable pour les petits objets VisDrone** : le découpage en tuiles
  est la manière standard d'obtenir du mAP_small sur de la haute résolution. Il donne des
  valeurs d'AP50s explicites (Table 1), rares dans le corpus.
- **Question centrale pour l'embarqué** : le découpage échange de la mémoire contre du
  temps (linéaire en nombre de tuiles). Sur FPGA, un accélérateur à entrée fixe
  (640×640) traitant des tuiles en flux est naturel (déduit), mais le coût en FPS et en
  énergie d'une image 4K découpée n'est mesuré nulle part ici.
- À relier à BlankSkip (arxiv-2603.28149), qui saute les tuiles vides pour réduire le
  coût, et à DEAL-YOLO (arxiv-2503.04698), avec son inférence en deux passes.

## Gaps identifiés

- **Coût embarqué de l'inférence par tuiles** (FPS, énergie par image 4K, latence de fusion
  NMS) sur FPGA, Jetson ou MCU : non mesuré.
- **Tuiles adaptatives** (sauter les tuiles vides, choisir les régions) contre un
  découpage uniforme, à budget de calcul fixe : piste de co-design.
- **Effet de la quantification INT8 sur l'AP50s obtenu avec SAHI** : non étudié (lien avec
  l'hypothèse sur le mAP_small).

## Statut de lecture

Papier complet (`fulltext.md` lu en entier, extraction GROBID `ok`). La légende de la
Table 2 est tronquée et son corps (xView) est extrait à la suite de la Table 1, sous un
second en-tête « Setup | AP50… ». Il est identifié par ses valeurs, cohérentes avec le
texte (« FI increases large object AP by up to 3.3% », « overlap … up to 1.7% »). Le
warning « Table 2 sans corps » est donc partiellement faux. Les Fig. 3-4 (analyse
d'erreurs) ne sont pas lues en détail.

Ce qui suit est déduit et non affirmé par les auteurs :
- la publication à ICIP 2022, d'après le DOI ;
- les incohérences entre le résumé et la Table 1 (recalculées) ;
- l'effet de la résolution effective dans le gain de SF ;
- la transposition au FPGA ;
- l'usage répandu de la bibliothèque.
