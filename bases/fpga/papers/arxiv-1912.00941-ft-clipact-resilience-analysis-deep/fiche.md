---
id: arxiv-1912.00941-ft-clipact-resilience-analysis-deep
fiche: done
date: 2026-09-29
benchmarks: none
---

# FT-ClipAct: Resilience Analysis of Deep Neural Networks and Improving their Fault Tolerance using Clipped Activation

Le-Ha Hoang, Muhammad Abdullah Hanif, Muhammad Shafique, 2019, arXiv preprint. https://arxiv.org/abs/1912.00941
Type : preprint non relu par les pairs

## Problème

Les DNN sont réputés tolérants aux fautes, mais des bit-flips dans la mémoire de poids dégradent fortement la précision, même à des taux de fautes bas (§I, Fig. 1b). Les solutions matérielles (DMR/TMR, ECC) ont un surcoût élevé ; l'entraînement tolérant aux fautes exige le jeu d'entraînement et un réentraînement par puce, et ne couvre pas les fautes à l'exécution (§I). Objectif : améliorer la résilience sans jeu d'entraînement, sans redondance et avec un surcoût minimal.

## Méthode

- Analyse de résilience par injection aléatoire de bit-flips dans les poids, couche par couche (AlexNet), avec observation de la distribution des activations : les fautes produisent des activations de forte intensité (bit MSB passant de 0 à 1 sur des poids proches de zéro) qui dominent la sortie (§III).
- Remplacement de ReLU par une ReLU « clippée » : f(x) = x si 0 ≤ x ≤ T, sinon 0 (les valeurs suspectes sont mises à zéro, pas saturées) (§IV-A).
- Trois étapes : profilage de ACT_max par couche sur un petit sous-ensemble de validation ; remplacement des activations ; réglage des seuils T par une recherche par intervalles (algorithme itératif en quatre points par intervalle), avec pour métrique l'aire sous la courbe précision vs taux de fautes normalisé (AUC) (§IV-B, §IV-C, Algorithme 1).
- Le méthode est indépendante du jeu d'entraînement (seul un sous-ensemble de validation sert au réglage) (§IV).

## Plateforme et implémentation

Pas de FPGA ni d'accélérateur réel : injection de fautes logicielle sous PyTorch, cadre similaire à Ares, sur Intel Core i7 3,2 GHz avec 2 GPU GTX 1080 Ti (§V-A). Puissance, latence, ressources : n/r. Code : non publié d'après le texte.

## Résultats

- Modèles : AlexNet (5 conv, 3 FC ; précision 72,8 %) et VGG-16 (13 conv, 1 FC ; 82,8 %) sur CIFAR-10 (§V-A).
- AlexNet à 5x10^-7 de taux de fautes : 69,36 % avec activations clippées contre 51,16 % sans protection ; +173,32 % d'AUC sur [0 ; 1x10^-5] (§V-B, Fig. 7a). Aux taux 1x10^-8 et 5x10^-8, la précision au pire cas (sur 50 expériences) est proche de la référence contre 41,93 % et 13,66 % pour le réseau non protégé (§V-B, Fig. 7b-c).
- VGG-16 : +654,91 % d'AUC à 5x10^-7 (Fig. 8a) ; +68,92 % en moyenne sur la précision à 1x10^-5 (Abstract, §VI). Les deux figures se rapportent à des métriques différentes (AUC vs précision) et le texte extrait ne donne pas la précision absolue de VGG-16 (n/r).
→ reportés dans `benchmarks.csv` : aucune ligne (simulation logicielle de fautes, sans mesure matérielle) ; `benchmarks: none`.

## Limites et critique

- Évaluation limitée à CIFAR-10 sur des réseaux de classification anciens (AlexNet, VGG-16) : pas de détection d'objets, pas de YOLO ; la précision de base est modeste (72,8 %).
- Fautes dans la mémoire de poids uniquement (bit-flips aléatoires en logiciel) ; pas de fautes dans les activations ou la logique, pas de SEU dans la configuration FPGA, pas de test matériel ni sous radiation. Les taux de fautes sont des valeurs paramétriques, non reliés à un environnement réel (§V-B).
- Le réglage des seuils utilise un sous-ensemble de validation ; le papier annonce ne pas exiger le jeu d'entraînement (§IV), mais l'algorithme d'optimisation est coûteux (évaluations multiples par couche) ; coût en précision fault-free non détaillé dans le texte extrait (n/r).
- Les pourcentages d'amélioration relatifs (+654 %) partent de bases très faibles et sont difficiles à comparer avec d'autres travaux ; l'Abstract cite un « 68,92 % » sans préciser qu'il s'agit d'un écart relatif de précision (déduit).
- Le texte est tronqué à plusieurs endroits (liste des contributions en §I, une phrase du §IV-A) ; l'affirmation « surcoût minimal » n'est pas chiffrée dans le texte extrait.

## Pertinence pour la thèse

Technique légère, sans redondance, adaptable à une implémentation FPGA (un comparateur et un multiplexeur par activation), donc candidate comme couche de protection complémentaire du TMR sélectif pour un YOLO quantifié ; elle attaque le mode de défaillance dominant (activations aberrantes). À évaluer sur un détecteur en INT8 (où le clipping est en partie implicite dans la saturation) et pour la métrique mAP. Ce qu'elle ne prouve pas : la couverture de diagnostic exigée par une norme de sûreté.

## Gaps identifiés

- Transposition du clipping d'activations à des réseaux quantifiés (INT8) et à des détecteurs d'objets, avec mesure sur SEU réels.
- Combinaison clipping + TMR sélectif ou ECC et quantification du surcoût matériel.

## Statut de lecture

papier complet (fulltext.md lu en entier ; extraction GROBID ok ; sections IV et V rattachées à la précédente ; les figures sont seulement des légendes, donc les valeurs des courbes ne sont connues que par le texte). Déduit et non affirmé par les auteurs : l'adaptation FPGA, l'interaction avec la quantification INT8, la pertinence pour YOLO.
