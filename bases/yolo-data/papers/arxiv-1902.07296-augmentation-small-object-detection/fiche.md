---
id: arxiv-1902.07296-augmentation-small-object-detection
fiche: done
date: 2026-10-05
---

# Augmentation for small object detection

Mate Kisantal, Zbigniew Wojna, Jakub Murawski, Jacek Naruniec, Kyunghyun Cho, 2019, arXiv preprint. https://arxiv.org/abs/1902.07296
Type : preprint non relu par les pairs

## Problème

Sur MS COCO, l'AP des petits objets est 2 à 3 fois inférieure à celle des grands, y compris pour les meilleurs soumissions (Fig. 1) ; petit = aire < 32×32 px, moyen 32-96, grand > 96 (Table 1). Les auteurs analysent Mask R-CNN (R50-FPN) et identifient deux causes (§3.3) :
- **Peu d'images avec petits objets.** 41,43 % des objets du train sont petits (34,4 % moyens, 24,2 % grands), mais seulement environ la moitié des images en contiennent, contre 70,07 % (moyens) et 82,28 % (grands) (§3.3).
- **Peu de pixels annotés.** Les petits objets ne représentent que 1,23 % de la surface annotée, les moyens 10,18 %, les grands 82,28 % selon le texte (§3.3 ; ce dernier chiffre est le même que le % d'images avec grands objets et ne boucle pas à 100 % : probable coquille, Table 2 sans corps extrait).
- **Appariement aux ancres défavorable.** RPN : ancre positive si IoU > 0,7 avec une vérité terrain, ou meilleure IoU de cette vérité terrain (§3.2). Seules 29,96 % des ancres positives vont aux petits objets contre 44,49 % aux grands ; 2,54 ancres appariées par grand objet contre environ une par petit objet ; IoU max moyen avec les ancres : 0,29 (petits), 0,57 (moyens), 0,66 (grands) (§3.3). Les petits objets contribuent donc peu à la perte RPN.

## Méthode

Deux interventions de prétraitement des données, indépendantes du détecteur selon les auteurs (§4, non testé hors Mask R-CNN) :
1. **Oversampling** des images contenant au moins un petit objet, facteurs 2, 3, 4, par copies hors ligne des images (§5.1).
2. **Copy-paste de petits objets** : un objet est découpé avec son masque d'instance COCO et collé ailleurs dans la même image (contexte plausible, Fig. 3). Transformations avant collage : échelle ±20 %, rotation ±15° ; seuls les objets non occultés sont copiés ; pas de chevauchement avec un objet existant ; au moins 5 px des bords (§4).

Stratégies de collage testées (§5.2-5.4) : (a) un seul petit objet collé k fois ; (b) plusieurs petits objets, chacun collé k fois ; (c) tous les petits objets collés k fois (k = 1..5, 1..3 pour (c)). Réglages de combinaison : image remplacée par sa version augmentée ; version augmentée dupliquée ; originale + augmentée gardées (équivaut à oversampling 2× avec ajout de petits objets sur la copie, utilisé pour (a)-(c)). Variantes de collage : avec ou sans chevauchement, flou gaussien des bords (3 ou 5).

## Plateforme et implémentation

Mask R-CNN + FPN + ResNet-50, implémentation de [16] (Detectron), schedule court : 36k itérations sur 4 GPU, lr 0,01 (règle de mise à l'échelle linéaire), SGD momentum 0,9, weight decay 1e-4, lr ÷10 à 24k et 32k (§3.2). 15 ancres (5 échelles 32² à 512², 3 ratios). Entrée, GPU exacts et temps : n/r. Code publié : aucun lien dans le texte (non publié selon la lecture).

## Résultats

Détection, AP_small (AP_large) sur COCO ; baseline 0,167 (0,393) (Table 3).

| Configuration | AP_small | AP_large | Source |
|---|---|---|---|
| Baseline | 0,167 | 0,393 | Table 3 |
| Oversampling 2× / 3× / 4× | 0,173 / 0,177 / 0,174 | 0,387 / 0,382 / 0,374 | Table 3 |
| Image remplacée par sa copie collée | 0,161 | 0,400 | Table 4 |
| + oversampling 2× | 0,168 | 0,387 | Table 4 |
| Originale + augmentée (meilleur) | 0,179 | 0,386 | Table 4 |
| 1 objet collé 1× / 2× / 3× / 4× / 5× | 0,174 / 0,175 / 0,175 / 0,174 / 0,171 | 0,384 / 0,382 / 0,386 / 0,383 / 0,386 | Table 5 |
| Plusieurs objets 1× / 2× / 3× / 4× / 5× | 0,174 / 0,175 / 0,178 / 0,179 / 0,176 | 0,384 / 0,385 / 0,387 / 0,382 / 0,389 | Table 6 |
| Tous les petits objets 1× / 2× / 3× | 0,179 / 0,179 / 0,167 | 0,386 / 0,388 / 0,383 | Table 7 |
| Chevauchement autorisé | 0,173 | 0,389 | Table 8 |
| Flou gaussien 3 / 5 | 0,170 / 0,173 | 0,389 / 0,383 | Table 8 |

- Gain AP_small : oversampling 3× = +1 point (+8,85 % relatif) pour la segmentation (§6.1, 0,113 vers 0,123) ; en détection 0,167 vers 0,177. Meilleur réglage (originale + augmentée) : 0,113 vers 0,124 en segmentation (+9,7 % relatif) et 0,167 vers 0,179 en détection (+7,1 % relatif) (résumé, §7, Table 4).
- Coût sur les grands objets : AP_large détection 0,393 vers 0,386 (-0,7 point) pour le meilleur réglage ; 0,393 vers 0,374 (-1,9 point) à 4× ; l'AP globale reste stable (0,303 à 0,307, Tables 3-6). Les auteurs parlent d'un compromis petits/grands réglable par le taux d'oversampling (§6.1). Segmentation : AP_large 0,418 vers 0,410.
- Texte (§6.3) : un seul objet, 1 à 2 collages suffisent ; plusieurs objets, jusqu'à 3 collages par objet ; tous les objets : une seule copie est la meilleure, davantage dégrade (Table 7, 3× = 0,167 = baseline). Raisons avancées, non testées : ratio originaux/collés qui chute, décalage train/test.
- Sans chevauchement est préférable ; le flou des bords n'aide pas (§6.4, Table 8).
- Sur un jeu de validation augmenté, l'AP_small du réglage « image remplacée » monte à 0,161 (+38 % annoncé), signe de surapprentissage aux artefacts de collage (§6.2).
→ reportés dans `benchmarks.csv` : 23 lignes proposées (AP_small détection, Tables 3 à 8) ; l'AP_large et la segmentation restent dans cette fiche. Valeurs des Tables 5-7 : étiquetage des tableaux déduit de l'ordre dans le texte (extraction brouillée), `confidence: medium`.

## Limites et critique

- Un seul détecteur (Mask R-CNN R50-FPN), un seul jeu (COCO), un schedule court (36k it.) ; pas de seeds ni d'intervalles : les écarts entre variantes de collage (0,174 à 0,179) sont de l'ordre de 0,5 point, probablement dans le bruit (déduit).
- Gain absolu modeste (+1,2 point AP_small détection) au prix de -0,7 point d'AP_large ; les « 7,1 % / 9,7 % » sont relatifs.
- Pas de test sur détecteurs à ancres de type YOLO ni sans ancres : la généralité affirmée au §4 n'est pas démontrée. L'explication par l'appariement RPN (IoU 0,7) ne se transpose pas telle quelle à l'assignation de YOLO (déduit).
- Le collage exige des masques d'instance (COCO en a) ; sur un dataset à simples bbox, coller le contenu de la bbox embarque le fond (non testé ici).
- Pas de comparaison avec l'augmentation d'échelle ou la montée en résolution d'entrée ; pas de réglage du ratio petits/grands par classe.
- Preprint, code non publié.

## Pertinence pour la thèse

**Pertinence pour la base (préparation de données YOLO).**
- **CONSTRUIRE un dataset.** Mesurer d'abord la part des petits objets (en images et en pixels, pas seulement en instances) : ici 41 % des instances mais 1,2 % de la surface. Si peu d'images contiennent des petits objets, en collecter ou en sur-échantillonner.
- **ANNOTER.** Le copy-paste exige un masque par instance ; avec des bbox seules, la méthode est dégradée. Les petits objets non occultés fournissent les meilleurs candidats au collage.
- **PRÉTRAITER.** Alternative ou complément de la montée en résolution/tiling : l'oversampling et le collage ne coûtent rien à l'inférence (hors-ligne, §4).
- **AUGMENTER.** Recette concrète : oversampling 2-3× des images à petits objets, plus copy-paste de petits objets non occultés, échelle ±20 %, rotation ±15°, sans chevauchement, sans flou, 1 à 3 copies par objet, en gardant l'image originale à côté de l'augmentée. Gain AP_small attendu : +1 à +1,2 point (COCO, Mask R-CNN), coût sur les grands objets.
- **Quand l'appliquer.** Domaine où les petits objets sont rares ou noyés (aérien, drone, inspection) et quand l'AP_small est le critère ; à éviter si les grands objets priment. À vérifier sur YOLO (ancres k-means, assignation TAL/SimOTA ; Copy-Paste d'Ultralytics, hors de ce papier).
- Alerte : ne pas remplacer les images, risque de surapprentissage aux artefacts de collage (§6.2).

## Gaps identifiés

- Effet du copy-paste de petits objets sur un détecteur YOLO moderne (ancres/assignation dynamique) : non mesuré ici.
- Copy-paste à partir de simples bbox (sans masque) et rôle des artefacts de collage : non traité.
- Comparaison à iso-compute avec tiling/SAHI ou entrée à plus haute résolution : absente.

## Statut de lecture

papier complet (fulltext.md, extraction grobid ; Tables 2, 5, 7 sans corps extrait selon `extraction.warnings` : les corps de Tables 5-7 apparaissent en vrac dans le texte, étiquetés par déduction ; Table 2 manque, ses chiffres viennent du texte §3.3).
Ce qui suit est déduit et non affirmé par les auteurs : attribution des blocs de chiffres aux Tables 5, 6, 7 ; bruit statistique des écarts ; non-transposition à l'assignation YOLO ; coquille probable sur 82,28 % de surface des grands objets.
