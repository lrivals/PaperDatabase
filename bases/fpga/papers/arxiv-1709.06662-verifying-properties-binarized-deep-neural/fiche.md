---
id: arxiv-1709.06662-verifying-properties-binarized-deep-neural
fiche: done
date: 2026-09-29
benchmarks: none
---

# Verifying Properties of Binarized Deep Neural Networks

Nina Narodytska, Shiva Prasad Kasiviswanathan, Leonid Ryzhyk, Mooly Sagiv, Toby Walsh, 2017 (v2 du 31 mai 2018), arXiv preprint. https://arxiv.org/abs/1709.06662
Type : preprint non relu par les pairs (le texte porte la mention « under review »).

## Problème

Vérifier de façon rigoureuse (exacte, complète) des propriétés de réseaux de neurones, en particulier la robustesse aux perturbations adversariales et l'équivalence de deux réseaux. Les méthodes antérieures sont soit approchées (relaxation LP, discrétisation), soit taillées pour ReLU et peu scalables (§1, §7). Les auteurs ciblent les Binarized Neural Networks (BNN), adaptés aux environnements contraints (embarqué, mobile) car poids et activations sont binaires (§1).

## Méthode

- Encodage exact d'un BNN en formule booléenne (« premier encodage booléen exact d'un réseau profond », abstract). Un BNN est une suite de blocs LIN + BatchNorm + sign (BIN), puis un bloc de sortie LIN + ARGMAX (§3, Table 1).
- Trois encodages successifs : MILP (big-M), puis ILP pur (les bornes réelles sont arrondies car les produits scalaires sont entiers), puis SAT/CNF via des compteurs séquentiels (sequential counters) pour les contraintes de cardinalité (§4).
- Propriétés encodées : robustesse adversariale L-infini (et L1), robustesse adversariale universelle, équivalence de réseaux (§5). Cas d'usage cités pour l'équivalence : réduction de modèle pour l'embarqué, ordre des augmentations.
- Recherche guidée par contre-exemples (counterexample-guided, CEG) : le réseau est coupé en un générateur (premier bloc) et un vérificateur (le reste) ; les interpolants de Craig, obtenus à partir du noyau insatisfaisable du vérificateur, bloquent les affectations inutiles (§6).
- Solveurs : SCIP pour l'ILP, Glucose pour le SAT (§8).

## Plateforme et implémentation

Sans objet côté matériel : aucune implémentation FPGA. Entraînement avec Torch sur GPU Titan Pascal X ; vérification par solveurs SAT/ILP (CPU, non précisé) (§8). Code : non publié d'après le texte (aucun lien). Puissance : n/r.

## Résultats

- Réseau : 4 blocs internes (200 neurones puis 3 × 100), plus un bloc de sortie, avec BN + BIN en entrée pour binariser les niveaux de gris ; précision 95,7 % (MNIST), 71 % (MNIST-rot), 70 % (MNIST-back-image) (§8).
- 200 images correctement classées par jeu (20 par classe), epsilon dans {1, 3, 5}, timeout 300 s ; formules moyennes ~1,4 M variables et 5 M clauses, maximum ~3 M variables et 12 M clauses (§8).
- Instances résolues sur 200 (Table 2, epsilon = 1) : MNIST SAT 180, ILP 130, CEG 171 ; MNIST-rot SAT 179, ILP 125, CEG 197 ; MNIST-back-image SAT 191, ILP 143, CEG 191. Sur MNIST-back-image, robustesse certifiée à epsilon = 1 : 138 images (SAT et CEG), 96 (ILP) ; à epsilon = 3 : 20 (SAT), 5 (ILP), 21 (CEG) (Table 2).
- Le SAT et le CEG résolvent jusqu'à 30 % d'instances de plus que l'ILP ; le CEG est plus rapide que le SAT sur les trois jeux mais résout moins d'instances sur MNIST (§8).
- Résumé des auteurs : absence de perturbation prouvée, ou perturbation trouvée, pour jusqu'à 95 % des images considérées avec un réseau à cinq couches entièrement connectées (§1).
→ reportés dans `benchmarks.csv` : aucune ligne. Il n'y a aucune mesure matérielle (FPS, puissance, ressources) ; les temps de solveur et les précisions MNIST ne rentrent pas dans le schéma de `benchmarks.csv`. `benchmarks: none`.

## Limites et critique

- Échelle : réseaux entièrement connectés d'environ 500 neurones, sur MNIST et variantes ; pas de convolutions testées (mentionnées comme encodables, §4), rien sur des détecteurs type YOLO. Les auteurs reconnaissent que l'échelle reste à améliorer (§9).
- Sur MNIST-back-image, dès epsilon = 3 plus de la moitié des instances ne sont pas résolues dans les 300 s (107 à 119 résolues sur 200 pour SAT et CEG, 67 pour ILP, Table 2) : la vérification complète se dégrade vite.
- La robustesse est vérifiée image par image, sur un échantillon de 200 images, et non sur une distribution : ce n'est pas une garantie globale.
- Les entrées sont binarisées par les deux premières couches, ce qui change le modèle de perturbation par rapport à des images en niveaux de gris.
- Comparaison à l'ILP uniquement (SCIP) ; pas de comparaison aux autres vérificateurs (Reluplex, etc.) sur le même réseau. Le travail parallèle de Cheng et al. 2017b est cité sans comparaison chiffrée (§7).
- Aucun temps de vérification rapporté pour un réseau de taille industrielle ; matériel du solveur n/r.

## Pertinence pour la thèse

Axe sûreté / certification. C'est une référence de base sur la vérification formelle d'un réseau binarisé, exactement le type de réseau que FINN/hls4ml déploient sur FPGA : la vérification exacte est possible parce que l'arithmétique est entière et booléenne, ce qui va dans le sens d'une preuve sur le modèle réellement embarqué. Elle donne un vocabulaire (robustesse, équivalence après réduction de modèle) utile à un dossier d'assurance. Elle ne dit rien de la chaîne matérielle (le RTL ou le bitstream généré est-il équivalent au BNN vérifié ?) ni d'un détecteur d'objets : le passage à l'échelle d'un YOLO quantifié reste ouvert. Il s'agit d'une approche de sûreté fonctionnelle et plutôt de *security* pour la robustesse adversariale (volet secondaire du profil) ; l'équivalence après quantification/réduction est le volet le plus directement utile.

## Gaps identifiés

- Vérification formelle de réseaux quantifiés/binarisés de taille réaliste (détection, convolutions) : passage à l'échelle non démontré.
- Équivalence formelle entre le réseau vérifié et l'implémentation FPGA générée (toolflow) : non traitée.
- Propriétés de sûreté au-delà de la robustesse L-infini (comportement en zone dangereuse, absence de faux négatifs sur les personnes) : non abordées.

## Statut de lecture

Papier complet (fulltext.md lu en entier ; extraction GROBID, le corps de la Table 1 est absent mais sa légende et la structure des blocs sont décrites dans le texte ; Table 2 lue). Déduit et non affirmé par les auteurs : le lien avec FINN/hls4ml et les toolflows FPGA ; le jugement sur l'absence de code publié (simple absence de lien dans le texte) ; la mise en perspective avec YOLO.
