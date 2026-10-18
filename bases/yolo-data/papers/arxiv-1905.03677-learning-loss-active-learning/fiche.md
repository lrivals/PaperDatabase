---
id: arxiv-1905.03677-learning-loss-active-learning
fiche: done
date: 2026-10-18
---

# Learning Loss for Active Learning

Donggeun Yoo, In So Kweon, 2019, arXiv preprint. https://arxiv.org/abs/1905.03677
Type : preprint non relu par les pairs (CVPR 2019 selon les auteurs ailleurs ; non indiqué dans `metadata.json`, donc non affirmé ici)

## Problème

Les méthodes d'active learning sont soit propres à une tâche (incertitude à redéfinir pour la détection, la segmentation, la pose), soit trop coûteuses pour les grands réseaux (comité, MC Dropout) ; core-set n'a été validé qu'en classification (§1, §2). Les auteurs veulent une méthode « simple mais indépendante de la tâche » pour choisir quelles images faire annoter (§1).

## Méthode

- Un petit « loss prediction module » est greffé sur le réseau cible : il prend des cartes de caractéristiques de couches intermédiaires, chacune passée par GAP + couche FC (128 dim), concaténées, puis une FC finale donnant une perte prédite scalaire (§3.2, §4). Entraîné conjointement, sans étape séparée (§3.2).
- Perte de rang par paires d'images d'un mini-batch (Eq. 2, marge ξ = 1), car un MSE sur la perte échoue : l'échelle de la perte décroît pendant l'entraînement (§3.3). Gradient du module coupé vers le réseau cible après 120 époques en classification (§4.1) et 75 en pose (§4.3) ; pour SSD, le texte ne précise pas l'arrêt du gradient (`n/r`).
- Boucle (§3.1) : K images tirées au hasard et annotées, entraînement, puis annotation des K images de plus forte perte prédite, répétition jusqu'à épuisement du budget.
- Protocole commun (§4) : K = 1 000 images initiales et 1 000 images ajoutées par cycle, pour les trois tâches.
- Détection (§4.2) : SSD à backbone VGG-16 (code ouvert, 77,43 mAP en plein jeu), module branché sur les 6 cartes de caractéristiques de SSD (conv4_3, 7, 8_2, 9_2, 10_2, 11_2). Hyperparamètres et augmentation de SSD d'origine, sauf le nombre d'itérations ; 300 époques, batch 32, lr 0,001 puis 0,0001 après 240 époques, λ = 1.
- Concurrents (§4.2) : aléatoire ; entropie (moyenne des entropies softmax sur les boîtes de détection de l'image) ; core-set K-Center-Greedy sur les caractéristiques conv7 après average pooling spatial.

## Plateforme et implémentation

Logiciel : PyTorch (§4). Matériel (GPU, temps d'entraînement) : n/r. Code des auteurs : lien non donné dans le texte ; seuls les dépôts open source des modèles cibles sont cités (note de bas de page, non extraite). Mêmes graines pour toutes les méthodes (§4).

## Résultats

Détection, PASCAL VOC (§4.2) : pool = trainval07+12 de 16 551 images, test07, mAP, moyenne de 3 essais avec des jeux initiaux différents.

| Méthode (dernier cycle) | mAP | Écart à aléatoire |
|---|---|---|
| Learn loss | 73,38 | +2,21 |
| Entropie | 72,22 | +1,05 |
| Core-set | 71,71 | +0,54 |
| Aléatoire | 71,17 | — |

(§4.2 ; le texte donne ces valeurs en fraction, converties ×100. Learn loss dépasse l'entropie de 1,15 et core-set de 1,63 : le texte parle de « margins », sans préciser points ou pourcentage ; les écarts de valeurs concordent avec des points de mAP.)

- Référence plein jeu : le SSD cible atteint 77,43 mAP avec tout le pool (§4.2). Le dernier cycle reste à ~4 points de ce plafond.
- Gain de mAP par cycle : la courbe est en Figure 6, dont le corps n'est pas extrait. Les valeurs intermédiaires sont `n/r` ; le nombre de cycles et la taille annotée finale en détection le sont aussi (non dits dans le texte). Seul le dernier point est chiffré.
- Précision du module de prédiction de perte : environ 70 % de « ranking accuracy » en détection (§4.2, Fig. 5), contre 90,74 % en classification (§4.1).
- Classification CIFAR-10 (ResNet-18, 5 essais, §4.1) : learn loss 91,01 ; entropie 90,59 ; core-set 90,10 ; aléatoire 87,64. Pose MPII (Stacked Hourglass à 2 empilements, 3 essais, §4.3) : PCKh@0.5 de 80,46 (learn loss), 79,85 (core-set), 78,99 (entropie), 78,62 (aléatoire).
- Économie d'images à mAP égal : le papier ne la chiffre pas (aucune courbe lue en « images nécessaires pour atteindre X mAP »). Seule lecture directe : à budget égal au dernier cycle, learn loss gagne 2,21 points de mAP sur le tirage aléatoire. Convertir cela en nombre d'images économisées exige la Figure 6 : `n/r`.

→ reportés dans `benchmarks.csv` : lignes proposées à l'agent principal (fichier `.cache/bench/arxiv-1905.03677-learning-loss-active-learning.csv`) : 4 en détection (learn loss, aléatoire, entropie, core-set) et 4 en classification ; pose non reportée (hors thème), valeurs ci-dessus.

## Limites et critique

- Une seule configuration en détection : SSD-VGG16 sur VOC, 3 essais ; écart-type annoncé (§4) mais non lisible (figure). Un écart de +2,21 mAP sur 3 essais peut être sensible au bruit ; aucun test de significativité.
- Aucun détecteur type YOLO, ni dataset avec petits objets, classes déséquilibrées ou images vides. VOC (20 classes, objets souvent grands) est un cas favorable : à vérifier avant de généraliser (déduit).
- Le coût d'annotation est compté en nombre d'images, pas en nombre de boîtes ni en temps ; or une image de VOC contient un nombre variable de boîtes, et la méthode peut favoriser des images à beaucoup d'objets (déduit, non mesuré).
- Le module n'est pas diversifié : les auteurs reconnaissent que ni la diversité ni la densité ne sont prises en compte, et que la précision de prédiction est faible en détection (§5). Les K images les mieux classées peuvent être redondantes (le problème est cité pour CIFAR avec un sous-pool aléatoire de 10 000, §4.1 ; non nécessaire pour VOC, §4.2).
- Core-set et entropie sont des implémentations des auteurs, avec des choix simples (entropie moyennée sur toutes les boîtes, caractéristiques conv7 à pooling spatial) : l'écart est possiblement affecté par ces choix, ce que les auteurs admettent en disant qu'il faudrait un espace de caractéristiques adapté à la détection (§4.2).
- Réentraînement de 300 époques à chaque cycle, modèle réinitialisé ou poursuivi : le texte dit « continue to train the current model » (§4), sans préciser (n/r).
- Pas d'étude du coût de calcul de la sélection, malgré l'argument d'efficacité. Code des auteurs non lié dans le texte.

## Pertinence pour le thème (données de détection)

- **CONSTRUIRE** : donne un protocole concret pour constituer un jeu par vagues plutôt qu'en bloc : 1 000 images tirées au hasard pour amorcer, puis lots de 1 000 par cycle (valeurs du papier sur un pool de 16 551 images, soit environ 6 % de budget initial par cycle ; calcul déduit). Applicable quand on dispose d'un gros pool d'images brutes (flux vidéo, drone) et d'un budget d'annotation limité.
- **ANNOTER** : l'apport est le choix de l'ordre d'annotation : prioriser les images où le modèle courant a la plus forte perte prédite. Sur VOC, à budget égal, +2,21 mAP contre un tirage aléatoire et +1,15 contre l'entropie (§4.2). L'entropie moyenne sur boîtes, simple à implémenter sur un YOLO (confiance de classe), donne déjà +1,05 (§4.2).
- **PRÉTRAITER** : sans objet.
- **AUGMENTER** : sans objet ; l'augmentation d'origine de SSD est conservée telle quelle (§4.2).
- **Quand l'appliquer** : un pool non annoté volumineux, annotation de boîtes chère, modèle réentraînable plusieurs fois. Peu utile si le pool est petit (on annote tout) ou très redondant (images quasi identiques en vidéo : sans critère de diversité, le top-K risque de choisir des doublons, déduit de §5). Pour un YOLO Ultralytics : branchement du module sur les cartes du neck/backbone possible mais non testé ici.
- **Réponse au praticien** : le papier ne dit pas « on économise N images pour un mAP donné » ; il montre un gain à budget fixé (+2,2 mAP) après plusieurs cycles de 1 000 images. L'économie en images doit se lire sur la Figure 6, non extraite : `n/r`.

## Gaps identifiés

- Économie en images à mAP cible (courbes de la Figure 6 non extraites) : à relire sur le PDF/figure ou à reproduire.
- Active learning avec un détecteur de type YOLO, sur un jeu aux petits objets ou aux classes déséquilibrées : non mesuré.
- Coût compté en boîtes ou en temps d'annotation plutôt qu'en images : non mesuré.
- Combinaison incertitude + diversité pour la détection (cité en perspective, §5) : non traité.

## Statut de lecture

Papier complet (fulltext.md lu en entier ; extraction GROBID ok). Les corps des Figures 4 à 7 ne sont pas extraits : les courbes par cycle, le nombre de cycles, les écarts-types et la taille annotée finale sont `n/r`. Le lien du code des auteurs n'est pas dans le texte extrait.
Ce qui suit est déduit et non affirmé par les auteurs : la part de budget par cycle (~6 %), le risque de doublons sans diversité en vidéo, la possible préférence pour les images à nombreuses boîtes, la transposabilité à un YOLO Ultralytics, l'interprétation en points de mAP des écarts « 1,15 % » et « 1,63 % ».
