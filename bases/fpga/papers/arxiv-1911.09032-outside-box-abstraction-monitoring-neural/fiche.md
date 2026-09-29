---
id: arxiv-1911.09032-outside-box-abstraction-monitoring-neural
fiche: done
date: 2026-09-29
benchmarks: none
---

# Outside the Box: Abstraction-Based Monitoring of Neural Networks

Thomas A. Henzinger, Anna Lukina, Christian Schilling, 2019 (arXiv 1911.09032), ECAI 2020, DOI 10.3233/FAIA200375. https://arxiv.org/abs/1911.09032
Type : conférence (ECAI 2020, d'après `journal_ref` arXiv) ; la version lue est l'arXiv.

## Problème

Un classifieur neuronal doit toujours répondre par une des classes apprises ; il ne sait pas dire « je ne sais pas » face à une entrée inédite (novelty detection), ce qui est crucial pour les applications critiques (§1). Les approches de référence traitent le réseau en boîte noire et se fient à la confiance de la sortie (softmax), alors que le réseau n'est pas entraîné à baisser sa confiance sur des entrées nouvelles (abstract).

## Méthode

- Moniteur d'exécution en parallèle du réseau, avec la même interface ; sortie : la classe prédite ou un avertissement « do not know » (Fig. 1, §1).
- Le moniteur observe des couches cachées proches de la sortie (hypothèse 1, §2.1). À l'entraînement, il collecte les vecteurs des entrées correctement classées, les regroupe par classe puis par cluster (k-means, nombre de clusters augmenté jusqu'à un seuil tau sur l'amélioration de la somme des carrés), et construit pour chaque couple classe/cluster la boîte (intervalle par neurone) la plus serrée (Algorithm 1, §3.1).
- À l'exécution, l'entrée est acceptée si le vecteur observé est dans une des boîtes de la classe prédite, rejetée sinon (Algorithm 2, §3.2). Plusieurs couches : un moniteur par couche, acceptation si tous acceptent (§4.2).
- Garanties : une entrée d'entraînement n'est jamais rejetée (Prop. 1) ; si l'abstraction a convergé, un rejet est toujours justifié (Prop. 2) ; les faux avertissements ne viennent que d'une abstraction non convergée (§4.1).
- Coût : opérations linéaires, mémoire indépendante de la taille du jeu d'entraînement, linéaire en neurones × clusters (§4.3). Agrandissement des boîtes d'un facteur pour régler le compromis fausses alarmes / détections (§6.2).

## Plateforme et implémentation

Sans objet côté FPGA : évaluation logicielle sur un portable (CPU 2,20 GHz, 4 cœurs, 8 Go RAM, Linux) (Table 3, légende). Puissance : n/r. Code et réseaux entraînés « disponibles en ligne » (note de bas de page 3 ; lien non repris dans le texte extrait).

## Résultats

- Protocole : réseau entraîné sur k classes parmi n (k de 2 à n-1), puis test sur les n classes ; les classes non apprises jouent les nouveautés. Jeux : MNIST, Fashion-MNIST, CIFAR-10, GTSRB ; réseaux NN1 et NN2 repris de Cheng et al. (Table 1, §5). Précision des réseaux : MNIST 99/99 %, F-MNIST 98-99/91-99 %, CIFAR-10 99/71-95 %, GTSRB 98-99/88-97 % (train/test, Table 1).
- Comparaison à l'approche par seuil sur softmax (alpha = 0,9 et 0,99) et à l'abstraction booléenne de Cheng et al. : le seuil « performe mal » quand il y a peu de classes connues (§5) ; les chiffres de détection figurent seulement dans les barres de la Fig. 5, non reproduites dans le texte.
- Abstraction booléenne : 48 s d'entraînement et 17 s d'exécution sur MNIST (une couche) contre 8 s et 2 s pour les boîtes (quatre couches) ; mémoire épuisée (8 Go) sur la dernière couche cachée de NN2 (84 neurones) (§5). Le moniteur prend moins d'une milliseconde par entrée (§5) ; le corps de la Table 3 est absent de l'extraction.
- Boîtes vs octogones sur MNIST : boîtes sur quatre couches meilleures en détection et en fausses alarmes, 2 s contre 121 s (§6.3). Les boules sont trop grossières (§6.3).
- Sur GTSRB (moins de 1 000 images par classe), tau = 0,3 et boîtes agrandies de 10 % (§5).
→ reportés dans `benchmarks.csv` : aucune ligne (pas de mesure sur FPGA ni sur cible embarquée ; temps sur portable, taux de détection uniquement en figures). `benchmarks: none`.

## Limites et critique

- Évalué uniquement en classification d'images de petite taille (MNIST, F-MNIST, CIFAR-10, GTSRB) avec de petits réseaux ; rien sur la détection d'objets. Une adaptation à YOLO (plusieurs objets, sorties de régression) n'est pas discutée.
- La « nouveauté » est simulée par des classes retirées de l'entraînement ; pas de décalage de distribution réaliste (éclairage, météo, capteur) ni d'évaluation sur des données hors domaine réelles.
- Résultats donnés en barres de figures sans tableau chiffré ; pas d'AUROC/FPR@TPR, ni de comparaison à des méthodes plus récentes (ODIN mentionné en related work mais non comparé, §1.1).
- Réglage de tau et du facteur de boîte propre à chaque jeu (tau = 0,07 puis 0,3 pour GTSRB) : sensibilité au réglage, pas de procédure générale.
- Le moniteur exige l'accès aux couches cachées : à intégrer dans le flot de données du FPGA (non traité).
- Les auteurs le disent : une nouveauté qui tombe dans une boîte n'est pas détectée (§4.1).

## Pertinence pour la thèse

Axe sûreté / certification, sous-thème runtime monitoring et OOD. Le moniteur par boîtes est très léger (comparaisons d'intervalles, mémoire indépendante du jeu de données), donc en principe bon candidat à une implémentation matérielle en parallèle du réseau sur FPGA : c'est une inférence, le papier ne parle pas de matériel. Il fournit un mécanisme simple et analysable (Prop. 1 et 2) pour produire un « do not know », utile pour un dossier de sûreté d'un YOLO de vidéosurveillance de personnes (entrée hors domaine, zone inhabituelle). Reste ouvert : le passage à la détection d'objets, l'implémentation matérielle et sa surcharge, la quantification des activations surveillées, et la validité des garanties sur données réelles.

## Gaps identifiés

- Moniteur OOD/runtime en matériel (FPGA) avec surcoût mesuré en ressources et latence : non traité ici.
- Moniteurs de couches cachées pour détecteurs d'objets (YOLO) plutôt que classifieurs.
- Évaluation sur nouveautés réalistes (décalage de distribution, personnes en environnement industriel) au lieu de classes retirées.

## Statut de lecture

Papier complet (fulltext.md lu en entier ; extraction GROBID). Tableau manquant : le corps de la Table 3 (temps de clustering, création, exécution) est absent ; les résultats de détection de la Fig. 5, 6, 7, 8 sont dans des figures non lisibles en texte, donc non chiffrés ici. Déduit et non affirmé par les auteurs : la faisabilité et l'intérêt d'une implémentation FPGA ; l'extension à YOLO.
