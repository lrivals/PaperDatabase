---
id: arxiv-2005.04757-simple-semi-supervised-learning-framework
fiche: done
date: 2026-10-18
---

# A Simple Semi-Supervised Learning Framework for Object Detection

Kihyuk Sohn, Zizhao Zhang, Chun-Liang Li, Han Zhang, Chen-Yu Lee, Tomas Pfister, 2020, arXiv preprint. https://arxiv.org/abs/2005.04757 (pas de DOI)
Type : preprint non relu par les pairs

## Problème

Le coût d'annotation des boîtes est bien plus élevé que celui des étiquettes de classification, alors que le semi-supervisé (SSL) était surtout démontré en classification (§1). Les rares travaux de SSL en détection s'appuient sur un contexte supplémentaire (similarités de catégories) ou sur une régularisation par consistance plus complexe (flip, schedule de poids ; §1, §2). Question : peut-on transposer à la détection la recette « pseudo-labels + augmentations fortes » de FixMatch / Noisy-Student, avec peu d'hyperparamètres ?

## Méthode

STAC (Self-Training and Augmentation driven Consistency), en deux étapes hors ligne façon Noisy-Student (§3.2) :

1. Entraîner un détecteur « professeur » (Faster R-CNN, ResNet-50 FPN, Tensorpack ; §4.1) sur les seules images annotées.
2. Générer les pseudo-labels des images non annotées par inférence normale du professeur, **NMS incluse** : le score retenu est celui de chaque boîte après NMS (retire les doublons, mais pas les boîtes mal placées ; §3.2). Filtrage par seuil de confiance τ (FixMatch). Les boîtes retenues deviennent des cibles, le reste de l'image est traité comme fond.
3. Appliquer des augmentations fortes aux images non annotées ; les pseudo-boîtes subissent la même transformation quand elle est géométrique globale (Fig. 2, §3.2).
4. Entraîner avec perte supervisée + λu × perte non supervisée (équation 4), λu constant (pas de rampe, contrairement à [23]).

Hyperparamètres : τ = 0,9 et λu = 2 partout, sauf COCO 100 % où τ = 0,5 pour augmenter le rappel des pseudo-labels (§4.1). Le professeur est fixe, d'où une génération hors ligne passant à l'échelle (§3.1).

**Augmentations fortes** (§3.2, « Data Augmentation Strategy », Fig. 3), RandAugment étendu à la détection à partir de l'espace de recherche de [70] :

- C : transformation couleur globale (opérations de RandAugment) ;
- G : géométrique globale (translation x-y, rotation, cisaillement x-y), qui impose de transformer aussi les boîtes ;
- B : géométrique au niveau des boîtes (3 opérations de G, magnitudes plus petites) ;
- Cutout à plusieurs positions aléatoires de l'image entière (pas seulement dans les boîtes, pour éviter une solution triviale).

Ordre : une opération de C, puis une de G ou B (tirée uniformément), puis Cutout.

## Plateforme et implémentation

Pas d'aspect FPGA. Détecteur Faster R-CNN + FPN, backbone ResNet-50 préentraîné ImageNet, bibliothèque Tensorpack (§4.1) ; matériel d'entraînement n/r dans le texte lu. Schedule « quick » (images de plus basse résolution, batch plus petit, mêmes mises à jour de poids) pour les protocoles 1/2/5/10 %, schedule standard ×3 pour 100 % (§4.2, note 6). Code publié : https://github.com/google-research/ssl_detection/ (résumé).

## Résultats

Protocoles COCO : 1, 2, 5, 10 % d'images annotées, le reste de train comme non annoté, 5 folds (≈1,2k images pour 1 %) ; 100 % + images non annotées de COCO ; VOC07 trainval annoté (5 011 images) + VOC12 trainval (11 540) avec ou sans COCO non annoté (§4).

| Config. (mAP COCO, ResNet-50 FPN) | Sup. (aug. défaut) | Sup.† (C+{G,B}+Cutout) | STAC | Source |
|---|---|---|---|---|
| 1 % | 9,05±0,16 | 9,83±0,23 | 13,97±0,35 | Table 1 |
| 2 % | 12,70±0,15 | 14,28±0,22 | 18,25±0,25 | Table 1 |
| 5 % | 18,47±0,22 | 21,18±0,20 | 24,38±0,12 | Table 1 |
| 10 % | 23,86±0,81 | 26,18±0,12 | 28,64±0,21 | Table 1 |
| 100 % | 37,63 | 39,48 | 39,21 | Table 1 |

- RandAugment seul améliore le supervisé de 2,71 mAP (5 %), 2,32 (10 %), 1,85 (100 %) (§4.2). Gain de STAC sur le supervisé fort : 5,91 mAP à 5 %, 4,78 à 10 % (§4.2).
- Efficacité en données : STAC à 5 % (24,36 dans le texte §4.2, 24,38 dans Table 1) dépasse le supervisé à 10 % (23,86) ; STAC à 10 % (28,56 §4.2) égale le supervisé à 20 % (28,63).
- 100 % annotés : STAC (39,21) bat le baseline (37,63) mais pas le supervisé fortement augmenté (39,48) (§4.2) ; explication des auteurs (hypothèse) : trop peu de non annoté relativement à l'annoté.
- VOC07 : supervisé 42,6 mAP / 76,30 AP50 ; supervisé fort 43,4 / 78,21 ; STAC avec VOC12 seul 77,45 AP50 (inférieur au supervisé fort) ; STAC avec VOC12 + COCO 46,01 mAP / 79,08 AP50 (§4.2, §5.2, légende Table 4/5 ; corps de Table 2 non extrait, chiffres lus dans le texte).
- **Ablation des augmentations, supervisé seul** (Table 3, un seul fold, schedule quick) : 5 % : 18,67 (défaut) → 20,13 (C) → 20,78 (C+{G,B}) → 21,16 (+Cutout) ; 10 % : 24,05 → 25,26 → 25,92 → 26,34. Chaque brique ajoute un gain. À 100 % annotés (standard) les augmentations fortes sous-apprennent : 37,42 (défaut) contre 36,12 (C+{G,B}+Cutout) ; avec 3× plus de schedule : 37,63 contre 39,48.
- **STAC sans augmentation forte** (§5.1) : 10 % un fold : 24,05 → 26,27 (self-training seul avec flip) contre 29,00 avec STAC complet ; 100 % : 37,63 → 37,57.
- **Taille du non annoté** (Table 4, un fold) : 5 % : STAC 19,81 (1×), 20,79 (2×), 22,09 (4×), 23,14 (8×), 24,49 (complet) ; 10 % : 25,38, 26,52, 27,33, 27,95, 29,00. À 1× STAC reste sous le supervisé fort (21,16 ; 26,34).
- **Seuil τ et poids λu** (Fig. 4, un fold à 10 %, valeurs lues dans le texte §5.3) : optimum τ = 0,9, λu = 2 ; sans filtrage par confiance (τ = 0) gain marginal sur le baseline fort ; dégradation si λu > 2 ou < 0,5. Précision préférée au rappel à 10 %. Valeurs numériques de la Fig. 4 : n/r.
- **Qualité des pseudo-labels** (§5.4, 10 %) : professeur à 18,67 mAP (5 % annoté) → STAC 24,25 ; professeur à 37,63 (100 %) → STAC 30,30 ; professeur 10 % → 29,00. Mais un professeur mieux augmenté (Table 5) ne donne pas de gain net : 5 % : STAC 24,49 / 25,01 / 24,70 / 25,12 selon l'augmentation du professeur ; 10 % : 29,00 / 28,97 / 28,41 / 28,81.

→ reportés dans `benchmarks.csv` : 14 lignes proposées dans `.cache/bench/arxiv-2005.04757-simple-semi-supervised-learning-framework.csv` (Table 1 : STAC 1/2/5/10/100 % et supervisé fort 5/10 % ; VOC07 ; Table 4 ; §5.4), à intégrer par l'agent principal.

## Limites et critique

- Un seul détecteur (Faster R-CNN, R50) ; pas de YOLO ni de détecteur one-stage. Les auteurs soulignent eux-mêmes le risque avec un hard negative mining fort, où les pseudo-labels bruités seraient sur-utilisés (§6) : transfert vers YOLO non démontré.
- Écarts internes : l'abstract annonce 24,38 (5 %) et 28,64 (10 %), le texte §4.2 24,36 et 28,56. Les ablations (Tables 3-5, Fig. 4) reposent sur **un seul fold**, sans écart-type, contrairement à Table 1 (5 folds).
- Table 2 (VOC) sans corps extrait : chiffres VOC repris du texte (confidence medium).
- Le gain à 100 % annotés est nul face au supervisé fortement augmenté (39,21 contre 39,48) : l'essentiel du bénéfice vient du faible volume d'annotations plus d'un grand lot non annoté. Le « 2× efficacité » compare à un supervisé aux augmentations par défaut (Sup.), alors que le supervisé fort (Sup.†) réduit l'écart : à 5 %, 21,18 contre 24,38 de STAC.
- Pseudo-labels seulement par seuil sur boîtes post-NMS : aucune correction des boîtes mal localisées ni des classes manquantes (faux négatifs traités comme fond) ; pas d'analyse de rappel/précision quantifiée (illustrations Fig. 5).
- Perte non supervisée détaillée pour la tête RPN seule ; le traitement de la tête CLS reste implicite dans le texte.
- Pas d'appréciation des coûts de calcul (aucun temps ni matériel rapporté).

## Pertinence pour la thèse

- **Construire** : si peu d'images sont annotées mais beaucoup sont disponibles brutes, annoter 5-10 % suffit pour approcher le supervisé à 10-20 % ; le gain croît avec le ratio non annoté/annoté (1× à 8×, Table 4) : ne pas lancer l'approche avec un non annoté du même ordre que l'annoté. Le gain est le plus fort dans les régimes bas (+4,9 mAP à 1 % contre le supervisé simple).
- **Annoter** : recette de pseudo-labellisation hors ligne : entraîner un modèle sur l'annoté, inférer avec NMS normale, ne garder que les boîtes à confiance ≥ 0,9 (précision plutôt que rappel) ; τ = 0,5 seulement quand l'annoté est déjà massif. La qualité du professeur compte (24,25 contre 30,30 selon le professeur), mais l'améliorer par augmentations ne se répercute pas au-delà. À appliquer pour du pré-annotage avant correction humaine ; en YOLO, les boîtes retenues sont à convertir au format normalisé (déduit, non dit par les auteurs).
- **Augmenter** : recette fiable pour l'entraînement supervisé même sans non annoté : couleur, puis géométrique (global ou par boîte avec boîtes transformées), puis Cutout multiple ; chaque brique donne un gain à 5-10 % annotés (Table 3). À 100 % annotés, prévoir un schedule 2-3× plus long, sinon sous-apprentissage. Nécessaire à STAC : sans elle, le self-training perd la moitié de son gain (§5.1).
- **Prétraiter** : rien (résolution du schedule « quick » mentionnée seulement).
- À ouvrir : adaptation à un détecteur YOLO (Mosaic comme augmentation forte ?), seuil par classe, bruit des pseudo-labels, petits objets.

## Gaps identifiés

- Pseudo-labels hors ligne avec un détecteur de type YOLO (one-stage) : aucun chiffre ici.
- Seuil de confiance adapté par classe ou calibré ; effet sur classes rares et petits objets : non étudié.
- Comparaison pseudo-labels vs. Mosaic/MixUp/Copy-Paste comme « augmentation forte » : non traitée.
- Part des faux négatifs dans les pseudo-labels (objets non détectés comptés comme fond) : non quantifiée.

## Statut de lecture

papier complet (fulltext.md lu en entier, backend grobid, extraction ok). Table 2 (VOC) sans corps extrait : chiffres VOC pris dans le texte (§4.2, §5.2) ; valeurs numériques de la Fig. 4 et Appendice (configurations des méthodes SSL, détails d'apprentissage) non disponibles. Appendice non lu.
Ce qui suit est déduit et non affirmé par les auteurs : le transfert vers YOLO et le format normalisé des boîtes ; l'interprétation « le gain vient surtout du faible volume annoté » ; l'usage en pré-annotage avant correction humaine. Le matériel d'entraînement est n/r.
