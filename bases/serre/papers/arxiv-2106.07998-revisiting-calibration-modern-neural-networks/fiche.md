---
id: arxiv-2106.07998-revisiting-calibration-modern-neural-networks
fiche: done
date: 2026-11-03
---

# Revisiting the Calibration of Modern Neural Networks

Matthias Minderer, Josip Djolonga, Rob Romijnders, Frances Hubis, Xiaohua Zhai, Neil Houlsby, Dustin Tran, Mario Lucic, 2021, arXiv preprint. https://arxiv.org/abs/2106.07998
Type : preprint non relu par les pairs

## Problème

Des travaux antérieurs (Guo et al. 2017 notamment) suggèrent que les réseaux plus récents et plus précis sont de plus en plus mal calibrés. Les auteurs vérifient si cela vaut encore pour les modèles de classification d'images de l'état de l'art, en reliant calibration, précision et caractéristiques de conception (Abstract, §1).

## Méthode

- Étude empirique de familles de modèles : MLP-Mixer, ViT, BiT, ResNeXt-WSL, SimCLR, CLIP (zero-shot), AlexNet, plus EfficientNet-NS en annexe (§4.1, Table 1). Tous sont entraînés ou fine-tunés sur ImageNet, sauf CLIP. Le texte annonce 180 modèles de 16 familles, 79 jeux de données et 28 variantes de métriques (Abstract).
- Jeux : ImageNet (val), ImageNetV2, ImageNet-C (15 corruptions x 5 sévérités), ImageNet-R, ImageNet-A (§4.1, App. A.2).
- Métrique : ECE top-label, binning à masses égales, 100 bins (§4.1). Variantes d'ECE, Brier et NLL en annexe (App. E, F).
- Recalibration : temperature scaling, ajusté sur 20 % de la validation ImageNet, métriques calculées sur les 80 % restants (§4.1 ; 10 000 images pour l'ajustement, 40 000 pour l'évaluation, App. A.2).
- Analyses : taille du modèle, quantité et durée de pré-entraînement (BiT), rapport précision/calibration par front de Pareto, coût attendu en prédiction sélective (§4.2, §4.3, App. B).

## Plateforme et implémentation

Aucune plateforme matérielle, aucune latence ni puissance : n/r. Code et jeu de mesures de calibration annoncés (« We provide code and a large dataset of calibration measurements », Abstract) ; le lien exact n'est pas dans le texte extrait (note de bas de page non reprise).

## Résultats

- Les familles récentes (MLP-Mixer, ViT, BiT) sont à la fois précises et bien calibrées, comparées à AlexNet ou aux modèles de Guo et al. ; CLIP est bien calibré compte tenu de sa précision (§4.2, Fig. 1).
- Dans la distribution, les grands modèles d'une famille ont tendance à avoir une ECE plus élevée, mais une erreur de classification plus faible : chaque famille occupe un front de Pareto différent (§4.2, Fig. 2).
- Sous décalage de distribution (ImageNet-C), la calibration se dégrade plus lentement pour MLP-Mixer et ViT ; la tendance en fonction de la taille s'inverse hors distribution, surtout après temperature scaling (§4.3, Fig. 4, 5).
- Le pré-entraînement : plus de données augmente la précision sans effet cohérent sur l'ECE. Après temperature scaling, ECE de BiT-R50x1 pré-entraîné sur ImageNet / ImageNet-21k / JFT-300 : 0,0185 / 0,0182 / 0,0185 ; BiT-R101x3 : 0,0272 / 0,0311 / 0,0236 (§4.2, Fig. 3). Une durée de pré-entraînement plus longue : plus précis, un peu moins bien calibré (App. B.1, Fig. 10).
- Précision et calibration sont corrélées sous décalage ; les modèles Pareto-optimaux sur ImageNet le restent sur les jeux hors distribution (§4.3, Fig. 6, 11).
- Prédiction sélective : pour des taux d'abstention jusqu'à 70 %, le modèle plus précis (BiT R152x4, meilleur de 0,08 en erreur) coûte moins que le mieux calibré (R50x1, meilleur de 0,009 en ECE) (§4.3, Fig. 7).
- Le label smoothing rend le modèle artificiellement sous-confiant ; mieux vaut entraîner sans, puis appliquer le temperature scaling (App. D, Fig. 14).
- Biais de l'estimateur ECE : le classement des modèles dépend du nombre de bins, surtout via un biais positif dépendant de la précision (§5, Fig. 9, App. C).

→ reportés dans `benchmarks.csv` : 6 lignes proposées (ECE après temperature scaling de BiT-R50x1 et BiT-R101x3 selon le jeu de pré-entraînement, §4.2). Ce sont les seuls chiffres explicites du texte ; les autres valeurs ne sont que dans des figures (non lisibles sans estimation, donc `n/r`). Ce sont des métriques de calibration sur ImageNet, sans lien matériel : `platform`, `fps`, `power_w` valent `n/r`.

## Limites et critique

- Uniquement ImageNet et ses variantes : aucune donnée de plantes, aucun test de terrain type PlantVillage vers PlantDoc ; le transfert aux feuilles est une inférence, pas une affirmation des auteurs.
- ECE estimée par binning : biais dépendant du nombre de bins et de la précision (§5) ; les auteurs recommandent de lire ECE et erreur de classification conjointement (front de Pareto), et le classement par ECE seule est fragile.
- Le temperature scaling est ajusté sur des données in-distribution ; sous décalage, la recalibration n'est pas refaite (§4.3), ce qui est le cas réaliste pour la serre mais le papier ne l'étudie que par ImageNet-C/R/A.
- Le jugement « choisir le plus précis » repose sur une seule structure de coût (erreur vs abstention, Fig. 7) ; les auteurs concèdent que d'autres coûts peuvent changer la conclusion.
- Hypothèse architecturale (biais inductif spatial) avancée sans test causal (§4.2, §6).
- Modèles très lourds (jusqu'à 936 M paramètres, Table 1) sans lien avec l'edge. Le fait que les familles non convolutionnelles soient mieux calibrées n'est pas transposé à des modèles légers (EfficientNet-B0 du projet) : déduit/non étudié, sauf EfficientNet-NS en annexe.
- Preprint, relecture par les pairs non vérifiée ; métadonnées (venue) à vérifier.

## Pertinence pour la thèse

Axe `calibration-decision` du projet SerreIA. Appui direct à la question « comment calibrer un classifieur (temperature scaling, ECE) » : (1) ECE avec 100 bins à masses égales et temperature scaling sur un split réservé comme protocole de référence ; (2) lire ECE avec l'erreur plutôt qu'ECE seule ; (3) sous décalage (PlantDoc), un modèle calibré en domaine l'est moins : à mesurer ; (4) ne pas utiliser le label smoothing comme substitut de recalibration. Laisse ouvert : transfert à des petits CNN (EfficientNet-B0) et à des données de plantes, choix des seuils de rejet, agrégation multi-feuilles.

## Gaps identifiés

- Aucune mesure de calibration sur PlantVillage/PlantDoc dans ce papier : ECE avant/après temperature scaling du classifieur EfficientNet-B0 en in-domain et hors domaine à mesurer.
- Lien entre calibration et choix de seuil de rejet à rappel donné non traité (seulement coût abstention vs erreur, Fig. 7).
- Effet de la quantification INT8 (Hailo) sur la calibration : non étudié.

## Statut de lecture

papier complet : `fulltext.md` lu en entier (extraction grobid, ok ; sections 2 et 4 non détectées, texte rattaché à la section précédente, d'où des numéros de section approximatifs). Les corps des figures ne sont pas extraits : seules les valeurs écrites dans le texte sont reprises ; aucune valeur lue sur un graphique. Une note de bas de page (lien code) et le début de la section 2 sont tronqués.
Ce qui suit est déduit et non affirmé par les auteurs : la pertinence pour les plantes et pour l'edge, et le protocole de recalibration conseillé pour SerreIA.
