---
id: arxiv-1804.06516-training-deep-networks-synthetic-data
fiche: done
date: 2026-10-18
---

# Training Deep Networks with Synthetic Data: Bridging the Reality Gap by Domain Randomization

Jonathan Tremblay, Aayush Prakash, David Acuna, Mark Brophy, Varun Jampani, Cem Anil, Thang To, Eric Cameracci, Shaad Boochoon, Stan Birchfield, 2018, arXiv preprint. https://arxiv.org/abs/1804.06516
Type : preprint non relu par les pairs

## Problème

Entraîner un détecteur demande beaucoup d'images annotées à la main ; les jeux synthétiques photo-réalistes (Virtual KITTI, VKITTI) coûtent cher à modéliser, ce qui annule l'intérêt du synthétique « gratuit » (§1). Les auteurs étendent le domain randomization (DR, Tobin et al.) à la détection d'objets réels (voitures, boîtes englobantes) et posent quatre questions : le DR seul donne-t-il de bons résultats sur des images réelles ? Quel gain apporte un complément de données réelles ? Quel est le poids de chaque paramètre ? Comment se compare-t-il à du synthétique plus coûteux ? (§1)

## Méthode

Génération sous Unreal Engine 4 (plug-in interne, images 1200 × 400 avec boîtes à 30 Hz, §3). Chaque image tire au hasard (§3) :
- nombre et type de voitures parmi 36 modèles 3D de berlines/hatchbacks ;
- distracteurs volants (cônes, pyramides, sphères, cylindres, piétons, arbres…) : nombre, type, couleur, échelle (nouveauté du papier) ;
- texture des voitures et photo de fond, toutes deux tirées de Flickr 8K ;
- position de la caméra (azimut 0-360°, élévation 5-30°) et angle (pan/tilt/roll ±30°) ;
- 1 à 12 lumières ponctuelles + une lumière ambiante plane ; visibilité du plan du sol.

Jeu DR principal : 100K images, au plus 14 voitures par image (§4.1). Comparaison à VKITTI : 2.5K images rendues sous Unity pour imiter KITTI (§4.1). Test : 500 images KITTI tirées au hasard, voitures de hauteur > 40 px et troncature < 0.15 (« easy »), AP@IoU 0.5 (§4.1). Trois détecteurs (implémentations open source, extracteurs recommandés) : Faster R-CNN, R-FCN (Inception-ResNet V2), SSD (ResNet101), pré-entraînés ImageNet (§4.1). Augmentations classiques en plus pendant l'entraînement : luminosité, contraste, bruit gaussien, flips, redimensionnement, box jitter, crop (§4.1). Fine-tuning : learning rate divisé par 10, gradient complet, jusqu'à convergence (§4.1). Ablation : Faster R-CNN ResNet V1, 50K images, un paramètre retiré à la fois (§4.2).

## Plateforme et implémentation

Détecteurs entraînés sur NVIDIA DGX Station, batch 4 (essais sur Titan X « avec résultats similaires », non chiffrés) (§4.1). Pas de mesure de vitesse ni de puissance d'inférence : n/r. Code et jeu de données : non publiés dans le texte lu (lien n/r) ; le plug-in UE4 est « interne » (§3).

## Résultats

AP@0.5 sur KITTI, voitures (entraînement synthétique seul sauf mention) :

| Détecteur | VKITTI 2.5K | DR 100K | Source |
|---|---|---|---|
| Faster R-CNN | 79.7 | 78.1 | Table 1 |
| R-FCN | 64.6 | 71.5 | Table 1 |
| SSD | 36.1 | 46.3 | Table 1 |

- Précision DR > VKITTI sur la plupart des rappels, mais DR plus faible aux rappels élevés ; hypothèse des auteurs : le DR ignore le contexte (voitures garées en rangées) (§4.1, Fig. 5).
- Init COCO (Faster R-CNN Inception-ResNet V2) : COCO seul 56.1 ; COCO+VKITTI 79.7 ; COCO+DR 83.7 (§4.3, texte ; le corps de la Table 2 n'est pas extrait).
- Fine-tuning sur réel : avec les 6000 images réelles, DR+fine-tuning atteint 98.5, soit +1.6 % sur VKITTI+fine-tuning et +2.1 % sur réel seul (§4.1). La courbe AP en fonction du nombre d'images réelles (Fig. 6) n'est pas lisible dans le texte : seul le texte dit que DR dépasse VKITTI quand le nombre d'images réelles augmente. Combien d'images réelles suffisent : n/r (le papier ne donne qu'un seul point chiffré, 6000 images). Il ne précise pas non plus si les « +1.6 % / +2.1 % » sont absolus ou relatifs.
- Ablation (Faster R-CNN ResNet V1, 50K images, §4.2, Fig. 7) :

| Configuration | AP@0.5 |
|---|---|
| Randomisation complète | 73.7 |
| Sans augmentation de lumière (luminosité/contraste off, lumières toujours aléatoires) | 73.6 |
| Lumière fixe | 67.6 |
| Sans texture sur les voitures | 69.0 |
| 4K textures au lieu de 8K | 71.5 |
| Sans augmentation (contraste, luminosité, crop, flip, resize, bruit) | 72.0 |
| Sans distracteurs | −1.1 % (valeur absolue non donnée) |

  Ordre d'importance : éclairage aléatoire (−6.1) > texture (−4.7) > nombre de textures (−2.2) > augmentation classique (−1.7) > distracteurs (−1.1). Les écarts sont déduits des valeurs ci-dessus ; un seul entraînement par ligne, sans barre d'erreur.
- Fond, pose de caméra, nombre d'objets : non ablatés (n/r).
- Gel des couches initiales (Hinterstoisser et al.) nuisible : Faster R-CNN 66.4 vs 78.1 (plein), R-FCN 69.4 vs 71.5 (Table 3) ; jusqu'à −13.5 % (§4.3).
- Quantité : saturation vers 10K images avec poids pré-entraînés, vers 50K sans pré-entraînement ; le pré-entraînement aide jusqu'à 1M images (§4.3, Fig. 8, texte seulement).

→ reportés dans `benchmarks.csv` : 14 lignes proposées (3 de la Table 1, init COCO 83.7 et COCO seul 56.1, DR+fine-tuning 6000 images 98.5, 2 de la Table 3, 6 de l'ablation §4.2), à ajouter par l'agent principal ; pas de ligne pour les valeurs VKITTI (en colonne `baseline`).

## Limites et critique

- Une seule classe (voiture), un seul jeu de test (500 images KITTI, sous-ensemble « easy ») ; pas de transfert à d'autres classes, d'autres domaines, ni à un détecteur YOLO (SSD est le seul détecteur à une étape, et le plus faible : 46.3).
- Entraînements uniques, sans variance ; arrêt « quand la performance sur le test sature » (§4.1) : sélection du meilleur point sur le jeu de test, optimiste.
- Comparaison DR vs VKITTI déséquilibrée : 100K images contre 2.5K, ce que les auteurs reconnaissent (§4.1). Avec Faster R-CNN, VKITTI reste meilleur (79.7 contre 78.1) ; le gain du DR n'est net que pour R-FCN et SSD.
- Ablations à 50K images et autre extracteur que la Table 1 : 73.7 pour la randomisation complète, non comparable à 78.1.
- Fig. 6 (courbe de fine-tuning) et Table 2 illisibles dans l'extraction ; le résultat « peu d'images réelles » ne peut pas être chiffré ici. Le « réel seul » n'est pas donné en valeur absolue.
- Pas de code ni de données publiés ; pas de relecture par les pairs.

## Pertinence pour la thèse

Axe `synthetic-da`. Pour CONSTRUIRE un dataset de détection quand l'annotation est coûteuse : générer des images synthétiques avec boîtes automatiques et randomiser volontairement, sans viser le photo-réalisme, quand on dispose de modèles 3D de l'objet (§3). Ordre de priorité des randomisations mesuré : varier l'éclairage (−6.1 AP si fixe), la texture de l'objet (−4.7 sans), puis le nombre de textures, l'augmentation classique et les distracteurs (§4.2). Pour ANNOTER : les boîtes viennent gratuitement du simulateur, ce qui supprime le coût d'annotation du pré-entraînement. Pour AUGMENTER : le DR est une augmentation « à la source » qui s'ajoute aux augmentations classiques (flip, crop, bruit) ; l'ablation montre que celles-ci apportent encore +1.7 AP. Pour PRÉTRAITER : n/r. À appliquer quand l'objet est rigide, modélisable en 3D, et que les images réelles annotées manquent : pré-entraîner sur 10K-50K images synthétiques, puis fine-tuner sur du réel (LR / 10, toutes les couches dégelées) ; ne pas geler le backbone (§4.3). Ce que le papier laisse ouvert : le nombre minimal d'images réelles, les objets texturés ou de contexte structuré (ses propres pistes, §5), et la transposition à YOLO.

## Gaps identifiés

- Courbe AP en fonction du nombre d'images réelles de fine-tuning (nombre minimal d'images réelles) : non chiffrée ici, à chercher dans d'autres papiers ou à mesurer.
- Randomisation de fond, pose et nombre d'objets non ablatés.
- DR pour détecteurs de type YOLO et pour plusieurs classes : non couvert.
- Comparaison à Copy-Paste de vrais objets (Dwibedi et al., cité §2) absente.

## Statut de lecture

papier complet (`fulltext.md` lu en entier ; extraction GROBID). Tables non extraites : Table 2 (valeurs prises du texte §4.3) ; figures 5-8 non lisibles (valeurs de la Fig. 7 prises du texte §4.2, Fig. 6 non chiffrée).
Ce qui suit est déduit et non affirmé par les auteurs : l'ordre d'importance et les écarts en points d'AP de l'ablation (différences avec 73.7) ; la remarque que le gain du DR sur VKITTI n'est net que pour R-FCN et SSD ; le risque de sélection optimiste sur le jeu de test.
