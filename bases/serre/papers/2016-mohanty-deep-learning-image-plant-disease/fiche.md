---
id: 2016-mohanty-deep-learning-image-plant-disease
fiche: done
date: 2026-10-29
---

# Using Deep Learning for Image-Based Plant Disease Detection

Sharada P. Mohanty, David P. Hughes, Marcel Salathé, 2016, Frontiers in Plant Science 7. https://doi.org/10.3389/fpls.2016.01419
Type : article de journal (relu par les pairs)

## Problème

Identifier la paire culture-maladie (38 classes, 14 cultures, 26 maladies) à partir d'une photo de feuille, sans ingénierie de caractéristiques, pour un diagnostic assisté par smartphone (`2016-mohanty#010.3`). Les auteurs se demandent aussi si le réseau apprend la « notion » de maladie ou seulement les biais de collecte de PlantVillage (`2016-mohanty#003.1`).

## Méthode

AlexNet et GoogLeNet de Caffe, entraînés de zéro ou par transfert depuis ImageNet (seules les couches finales sont réinitialisées, tout reste entraînable) (`2016-mohanty#005.3`). 54 306 images PlantVillage redimensionnées en 256 × 256 (`2016-mohanty#003.0`), en trois versions : couleur, niveaux de gris, feuille segmentée (fond retiré, par script tuné pour ce jeu ; correction des dominantes de couleur) (`2016-mohanty#003.1`). Cinq découpages train-test, de 80-20 à 20-80, en gardant toutes les vues d'une même feuille du même côté (mapping connu pour 41 112 images sur 54 306) (`2016-mohanty#004.0`). 60 configurations, 30 époques, SGD, lr 0,005 (`2016-mohanty#008.1`). Test hors domaine : deux petits jeux de 121 et 119 images vérifiées à la main, tirées de Bing Images et d'IPM Images (`2016-mohanty#009.3`).

## Plateforme et implémentation

Entraînement : « plusieurs heures sur un cluster GPU », puce non précisée (`2016-mohanty#010.3`). Inférence : « moins d'une seconde sur CPU » (`2016-mohanty#010.3`), sans matériel ni protocole : puissance, FPS, quantification `n/r`. Fork Caffe maison ; les résultats de base sont dits reproductibles avec Caffe standard (`2016-mohanty#008.1`). Code et poids : non publiés d'après le texte lu (pas de lien trouvé).

## Résultats

- PlantVillage (test en domaine, split par feuille) : exactitude de 85,53 % (AlexNet, de zéro, gris, 80-20) à 99,34 % (GoogLeNet, transfert, couleur, 80-20) (`2016-mohanty#009.0`) ; la discussion écrit 99,35 % (`2016-mohanty#010.3`). Avec seulement 20 % d'entraînement : 98,21 %, F1 0,9820 (`2016-mohanty#009.0`). GoogLeNet > AlexNet, transfert > de zéro ; couleur > segmenté > gris (`2016-mohanty#009.1`, `2016-mohanty#009.2`).
- **Chute vers des images de terrain** : avec le meilleur modèle, 31,40 % (jeu 1, 121 images) et 31,69 % (jeu 2, 119 images) sur 38 classes ; hasard 2,63 % (`2016-mohanty#009.3`). Top-5 : 52,89 % et 65,61 % (`2016-mohanty#009.3`, `2016-mohanty#009.4`). Soit environ 68 points perdus (99,34 % → 31,4 %, calcul de la fiche, non des auteurs). Les auteurs la décrivent comme « réduite substantiellement, à un peu plus de 31 % » quand les conditions de prise de vue diffèrent de l'entraînement (`2016-mohanty#010.4`) et l'attribuent au manque de diversité des données : « plus de données variables suffira » (affirmation d'auteurs, non testée ici).
- Culture connue (tâche plus réaliste) : jeu 1, 33 classes / 9 cultures : 0,478 (hasard 0,225) ; 25 classes / 5 cultures : 0,411 ; jeu 2, 13 classes : 0,545 ; 11 classes : 0,485 (`2016-mohanty#009.5`).
- Le fond n'explique pas seul la chute : la version segmentée est à peine inférieure à la couleur en domaine (`2016-mohanty#009.2`), et le meilleur modèle du jeu 1 est celui entraîné sur images segmentées (`2016-mohanty#009.4`), sans que cela rende l'écart de domaine petit. Aucun test de segmentation appliqué aux images de terrain n'est rapporté (déduit).
- Le corps de TABLE 1 n'est pas extrait (légende seule) : les valeurs par configuration viennent du texte (confidence `medium`).
→ reportés dans `benchmarks.csv` : 6 lignes (renvoyées à l'agent principal, non écrites ici).

## Limites et critique

- Jeux de terrain minuscules (121 et 119 images), un seul modèle évalué, sans intervalle de confiance : ±4 points environ à 31 % sur 120 images (déduit, calcul binomial).
- Le test PlantVillage est en domaine ; fond homogène, feuille unique face visible, ce que les auteurs reconnaissent (`2016-mohanty#010.4`). Aucune parade testée : le papier constate la chute et propose de collecter plus de données.
- Pas de calibration, pas de mesure de faux positifs sur images saines, pas de rappel/précision par classe sur le jeu de terrain : seulement l'exactitude 38 classes et le top-5.
- Architectures de 2016 (AlexNet, GoogLeNet) ; matériel et vitesse d'inférence non mesurés. Le jeu de terrain est issu de recherches web avec vérification visuelle, donc biaisé vers des images illustratives de vulgarisation (déduit).

## Pour SerreIA

**Ce que le papier établit.** C'est la première mesure publiée de l'écart PlantVillage → images de terrain : 99,3 % en domaine, 31,4 % hors domaine (`2016-mohanty#009.3`), plus un test de fond (couleur / gris / segmenté) qui montre que le fond ne suffit pas à tout expliquer. Il justifie de ne jamais présenter les chiffres PlantVillage de SerreIA (F1 en domaine) comme une performance de serre.

**Ce que le projet reprend.**
- Méthode de protocole : découper train/test par feuille et non par image (`2016-mohanty#004.0`). À contrôler dans `vision/datasets/near_duplicates.py` et `vision/datasets/build_index.py` que PlantVillage et CCMT sont bien découpés ainsi (sinon le test en domaine est gonflé).
- Expérience à faire : mesurer l'effet du remplacement/retrait de fond sur PlantDoc. Mohanty n'a testé la segmentation qu'en domaine ; SerreIA peut la tester sur le test hors domaine (`vision/eval/cross_domain_eval.py`, `vision/datasets/augment.py` / `batch_augment.py`, `data/backgrounds/` à créer). Comparer trois bras identiques à ceux de l'article : couleur, fond retiré, gris, tous évalués sur PlantDoc.
- Expérience : rapporter l'exactitude top-1 et top-5 et la variante « culture connue » (`2016-mohanty#009.5`) sur PlantDoc. Dans SerreIA la culture est connue de la serre : la tâche à mesurer est la maladie à culture donnée, ce que les têtes multiples de `vision/models/multihead.py` permettent.
- Métrique : en plus de l'exactitude, ajouter faux positifs sur images saines et ECE (`vision/eval/metrics.py`, `vision/eval/temperature.py`), absents du papier ; ils sont le vrai problème de SerreIA (spécificité 0,50, 42 % de faux positifs en deux étages).
- Barre de comparaison : un gain annoncé par une parade (fond, augmentation) doit dépasser l'incertitude d'un test d'environ 120 images (±4 points) ; PlantDoc est plus grand mais cette règle reste la bonne.

**Comparabilité des chiffres.** Non, pas directement.
- 99,34 % (Mohanty) est un test en domaine (même distribution PlantVillage, split par feuille) ; il est comparable seulement à une F1 en domaine de SerreIA sur PlantVillage, pas aux métriques PlantDoc de SerreIA (rappel 0,986, précision 0,679, spécificité 0,50, ECE 0,13/0,30).
- 31,4 % est hors domaine mais sur un autre test (121/119 images web, 38 classes culture-maladie, exactitude top-1 multi-classes), alors que SerreIA mesure un rappel/une précision binaire « anormal » sur PlantDoc avec classe saine : métriques et classes différentes. Le seul rapprochement valable est qualitatif : une chute de dizaines de points hors domaine, avec un entraînement PlantVillage seul. SerreIA entraîne aussi sur CCMT (plus varié), ce qui est une différence de protocole.
- Le papier n'a pas de point saine/malade pour la spécificité : impossible de comparer les 42 % de faux positifs.

## Gaps identifiés

- Effet de la segmentation/suppression de fond sur un test hors domaine (jamais mesuré par ce papier ni, à ce jour, par SerreIA).
- Faux positifs sur images saines et calibration hors domaine : absents.
- Jeux de terrain à grande échelle avec splits fixes (Mohanty en a 240 images au total).

## Statut de lecture

Papier complet (sections lues par passages `pdb search` / `pdb show` : jeux de données, méthode, résultats, discussion ; légendes des figures ; supplément absent). Extraction GROBID ; TABLE 1 sans corps extrait, ses valeurs ne sont donc pas lues.
Déduit et non affirmé par les auteurs : la perte de 68 points, les ±4 points d'incertitude, le biais « images illustratives » du jeu de terrain, l'absence de test de segmentation sur images de terrain (absence dans le texte lu), les correspondances avec les fichiers de SerreIA (non relus ici hors listage des noms de fichiers).
