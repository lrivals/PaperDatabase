---
id: arxiv-2409.07114-continual-incremental-learning-tinyml-device
fiche: done
date: 2026-09-29
benchmarks: none
---

# A Continual and Incremental Learning Approach for TinyML On-device Training Using Dataset Distillation and Model Size Adaption

Marcus Rüb, Philipp Tuchel, Axel Sikora, Daniel Mueller-Gritschneder, 2024, 2024 IEEE 7th International Conference on Industrial Cyber-Physical Systems (ICPS). DOI 10.1109/ICPS59941.2024.10639989 ; https://arxiv.org/abs/2409.07114
Type : conférence (la version lue est l'arXiv, non vérifiée contre la version publiée).

## Problème

L'entraînement sur l'appareil (MCU, TinyML) est limité en mémoire et en calcul ; on ne peut pas stocker de gros jeux de données, d'où l'apprentissage incrémental/continu, qui souffre d'oubli catastrophique. Beaucoup de méthodes actuelles demandent beaucoup de mémoire (§I).

## Méthode

Cycle en cinq étapes répété à chaque pas de temps t (Fig. 1, §III-B) :
1. distillation du jeu de données courant (distribution matching, avec Differentiable Siamese Augmentation, DSA) ;
2. entraînement du réseau sur les images distillées de tous les pas vus jusque-là ;
3. validation sur l'ensemble des jeux de test vus ;
4. si la précision est sous un seuil A_standard, agrandissement du modèle (couches/neurones supplémentaires) et réentraînement ;
5. enregistrement des données suivantes.
Réseaux : ConvNetD2, D3, D4 (2 à 4 blocs convolutifs, group norm, ReLU, average pooling) ; la distillation est toujours faite sur le plus grand (D4) pour permettre la transition vers un modèle plus grand (§IV-A). Le modèle adaptatif commence à D2 et grandit si besoin. Comparaison à quatre scénarios : cumulatif (« baseline », toutes les données), modèle fixe le plus grand, modèle adaptatif, oubli catastrophique (données courantes seules) (§IV-A, §V-A). Les FLOPs sont comptés par époque.

## Plateforme et implémentation

Aucun déploiement sur MCU ou FPGA décrit : les réseaux « petits » simulent un scénario TinyML (§IV-A) ; matériel d'expérimentation n/r ; puissance, latence : n/r. Code : non publié d'après le texte (aucun lien).

## Résultats

Cinq jeux (§IV) : MNIST (10 pas, rotations, 10 images/classe, ~1,7 % des données), CORe50 (NIC, 79 pas, 64x64, 400 images distillées, ~0,3 %), Speech Commands (35 pas, 20 images/classe, ~0,8 %), HAR (8 pas, 10 IPC, ~4,68 %), CIFAR10 (10 pas, 50 IPC, 1 %).
Précision finale / moyenne et FLOPs (§V) :
- CIFAR10 : cumulatif 85,4 % / 47,8 % ; plus grand modèle 57,7 % / 35,6 % ; adaptatif 58,2 % / 35,9 % avec 43 % des FLOPs ; oubli 10 % / 10 % (§V-B).
- CORe50 : cumulatif 55,3 % / 36,5 % ; adaptatif à 49 % des FLOPs ; oubli 3,7 % / 3,6 % (§V-C ; valeurs adaptatif/plus grand n/r dans le texte, Table II sans corps extrait).
- Speech Commands : cumulatif 95 % / 45,6 % ; plus grand et adaptatif vers 70 % en final, adaptatif à 36 % des FLOPs ; oubli 3,8 % / 2,9 % (§V-D).
- MNIST : cumulatif 98,8 % / 78,8 % ; plus grand et adaptatif autour de 92 % en final, adaptatif à 36 % des FLOPs ; oubli 60,1 % / 66,2 % (§V-E ; Table IV sans corps extrait).
- HAR : cumulatif 83,1 % / 43,1 % ; plus grand et adaptatif « milieu de la gamme des 60 % », réduction des FLOPs de près des deux tiers ; oubli 15 % / 12,5 % (§V-F).
- Mémoire : ~1 % du jeu de données original (§V-G) ; CORe50 : plus de 78 % de la précision du réseau cumulatif, contre ~50 % pour CWR d'un autre travail (§IV-B, avec un modèle plus grand et du 128x128 dans ce dernier, §II).
→ reportés dans `benchmarks.csv` : aucune ligne (pas de plateforme matérielle ; le tableau est en précision et FLOPs relatifs sur simulation). `benchmarks: none`.

## Limites et critique

- Incohérence entre l'abstract/conclusion et les chiffres : « perte de précision négligeable de 1 % » et « 0,4 % de perte moyenne » (abstract, §VI) sont des écarts entre modèle adaptatif et plus grand modèle sous distillation, pas par rapport à l'entraînement cumulatif. Par rapport au cumulatif, les pertes sont fortes : CIFAR10 85,4 % contre 58,2 % en final ; Speech Commands 95 % contre ~70 % ; MNIST 98,8 % contre ~92 % ; HAR 83,1 % contre ~65 % (§V).
- Dans la §V-A, la « baseline » est décrite comme un entraînement sur tout le jeu de données, alors qu'en §IV-A elle est l'oubli catastrophique et le scénario « cumulatif » l'idéal : la terminologie est confuse, à recouper avec les tableaux (dont II et IV n'ont pas de corps extrait).
- Aucune mesure sur cible embarquée : FLOPs relatifs uniquement ; ni mémoire réelle, ni énergie, ni temps de distillation. La distillation elle-même (optimisation sur les images) est coûteuse et rien ne dit qu'elle tienne sur un MCU ; la méthode dit « on device » mais n'évalue pas le coût de l'étape 1.
- Le critère d'agrandissement dépend d'un seuil A_standard fixé à la main ; pas d'analyse de sensibilité. Le modèle agrandi est réentraîné à chaque fois, sans réutilisation des poids précisée.
- Comparaison à CWR/EWC/LwF reprise d'un autre travail (modèle plus grand, résolution 128x128), non comparable directement (§II).
- Le papier reconnaît que la performance peut varier avec la complexité du jeu de données (§VI).
- Preprint arXiv ; Tables II et IV sans corps extrait, les chiffres CORe50 et MNIST viennent du texte.

## Pertinence pour la thèse

Axe apprentissage continu embarqué. Intérêt : un schéma de replay compact (distilled replay à ~1 % des données) avec croissance du modèle, dans l'esprit TinyML/MCU. Applicabilité à un YOLO sur FPGA limitée : classification d'images de petite taille, petits CNN, pas de détection. L'agrandissement dynamique du modèle est difficilement compatible avec un FPGA à architecture fixe et avec la certification (un modèle qui change en ligne complique la vérification et la traçabilité) : point à discuter dans la problématique « apprentissage continu certifiable ». Ce que le travail laisse ouvert : coût matériel réel, déploiement FPGA, détection.

## Gaps identifiés

- Apprentissage continu embarqué évalué sur cible réelle (énergie, mémoire, temps de distillation) : ici uniquement FLOPs.
- Apprentissage continu avec architecture évolutive et garanties de sûreté/certification : non abordé.
- Continual learning pour la détection d'objets sur cible contrainte (ce papier est en classification).

## Statut de lecture

Papier complet (fulltext.md lu en entier ; extraction GROBID). Corps des Tables II et IV absent ; Tables I, III, V non extraites non plus (leurs chiffres sont pris du texte §V). Déduit et non affirmé par les auteurs : l'incompatibilité avec FPGA/certification ; la remarque sur le coût de la distillation ; l'écart avec le cumulatif (calculé à partir des valeurs du texte).
