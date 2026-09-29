---
id: arxiv-2005.13166-safeml-safety-monitoring-machine-learning
fiche: done
date: 2026-09-29
benchmarks: none
---

# SafeML: Safety Monitoring of Machine Learning Classifiers through Statistical Difference Measure

Koorosh Aslansefat, Ioannis Sorokos, Declan Whiting, Ramin Tavakoli Kolagari, Yiannis Papadopoulos, 2020, arXiv preprint. https://arxiv.org/abs/2005.13166
Type : preprint non relu par les pairs

## Problème

Les classifieurs ML entrent dans des domaines critiques où le test seul d'une boîte noire ne suffit pas. Les auteurs traitent le décalage de distribution (*distributional shift*) entre données d'entraînement et données observées en opération, sans étiquettes, pour estimer en ligne si la précision du classifieur reste valide (§1, §1.1, §3). Ils visent à la fois safety et security (un décalage peut venir d'une manipulation malveillante des données) (Abstract).

## Méthode

- Hors ligne : entraînement sur données de confiance ; la PDF et les paramètres statistiques de chaque classe sont stockés (§3, Fig. 2).
- En ligne : on accumule un tampon d'échantillons non étiquetés, on estime les distributions par classe, puis on compare aux distributions d'entraînement. Distance faible : résultats jugés fiables ; distance élevée : bascule vers une autre méthode ou alerte d'un opérateur humain (§3).
- Base théorique : borne d'erreur de Chernoff (dérivée en §2, éq. 2-12, avec la distance de Bhattacharyya pour lambda = 0,5), puis lien entre erreur et différence de fonctions de répartition empiriques (ECDF) (éq. 13-14). Mesures ECDF testées : Kolmogorov-Smirnov (KSD), Kuiper, Anderson-Darling (ADD), Wasserstein (WD), Wasserstein-Anderson-Darling (WAD) (§4.1).
- Indépendant de l'algorithme de classification (§1.1). Pas d'architecture matérielle, ni de quantification.

## Plateforme et implémentation

Sans objet : aucune cible matérielle. Implémentation en R, Python et MATLAB (§4) ; dépôt « SafeML Github Repository » cité sans lien dans le texte extrait (§4, §4.2). Puissance : n/r.

## Résultats

- Jeux synthétiques XOR, Spiral, Circle (2 features, 2 classes) : 80 % entraînement/test avec validation croisée 10 plis, 20 % validation ; classifieurs LDA, CART, RF, KNN, SVM (§4.1). Jeu de sécurité CICIDS2017 (intrusion réseau, attaques du mercredi et du jeudi), classifieurs Naive Bayes, analyse discriminante, arbre, plus proches voisins, 100 itérations (§4.2).
- XOR : pour LDA, l'exactitude minimale vraie (MTA) est 0,508 et KSD estime 0,772, ADD 0,903, WAD 0,986 : la mesure surestime, surtout ADD et WAD ; pour CART/KNN/SVM/RF, MTA entre 0,975 et 0,996 et KSD entre 0,928 et 0,931 (Table 1). Le texte commente cela en disant que KSD « reporte une faible précision » pour LDA (§4.1), formulation ambiguë au regard de la Table 1.
- Spiral et Circle : écarts absolus entre mesure et MTA, le plus grand étant celui de LDA (jusqu'à 0,33 pour KSD sur Circle, Table 4) ; KSD et Kuiper meilleurs sur Spiral (texte sous Table 2/3).
- CICIDS2017 : KSD, Kuiper et Wasserstein donnent les meilleures estimations mais avec une variance élevée (Fig. 8, lecture du texte §4.2). Corrélation de Pearson entre classes et distances, WD et WAD les plus corrélées (Fig. 9, §4.3). Valeurs numériques de ces figures : n/r dans le texte.
- Conclusion des auteurs : KS est la mesure la plus efficace (§7).
→ reportés dans `benchmarks.csv` : aucune ligne. Article sans mesure matérielle (aucun FPS, GOPS, W, ressource) ; les tableaux portent sur des précisions estimées de classifieurs jouets, hors du schéma de `benchmarks.csv`. `benchmarks: none`.

## Limites et critique

- Jeux synthétiques 2D et un seul jeu réel non visuel (trafic réseau tabulaire) ; aucune vision, aucun DNN. Généralisation à des images en haute dimension non démontrée : les ECDF sont univariées, par feature (déduit de la formulation §2, non discuté par les auteurs).
- Les auteurs affirment ne trouver aucun travail comparable (§1.3) et ne se comparent à aucune méthode de détection OOD ou d'incertitude ; pas de baseline.
- Pour LDA, les estimations surestiment fortement l'exactitude minimale vraie (Table 1), ce qui est le cas dangereux pour la sûreté ; l'argument « surestimer l'erreur est sûr » (§2) ne couvre pas ce sens d'erreur.
- Nécessite un tampon d'échantillons, donc une latence de détection ; taille de fenêtre non étudiée systématiquement (une fenêtre de 1500 en §4.3).
- Pas de seuil d'alerte opérationnel défini, ni de garantie formelle ; « preliminary findings » (Abstract). Preprint, résultats préliminaires.
- Le texte extrait est partiel côté §5 (XAI) et référence des sous-sections mal détectées.

## Pertinence pour la thèse

Axe `safety-certification`, surveillance à l'exécution (*runtime monitoring*) : un moniteur de décalage de distribution sans étiquettes, indépendant du modèle, qui pourrait surveiller les entrées ou les caractéristiques d'un détecteur YOLO déployé (changement d'éclairage, de caméra, d'environnement industriel) et déclencher une dégradation contrôlée. Le calcul d'ECDF et de distances est léger et pourrait se mapper sur FPGA (déduit, non discuté par les auteurs). Il faut le transposer aux images et à la détection, ce que le papier ne fait pas, et il ne fournit pas d'argument de certification en tant que tel, seulement un indicateur pouvant alimenter un argumentaire (§6.2).

## Gaps identifiés

- Moniteurs de décalage de distribution évalués sur des détecteurs d'images (YOLO) et non sur des classifieurs tabulaires.
- Implémentation matérielle (FPGA) d'un moniteur statistique en ligne : coût en ressources et latence inconnus.
- Calibration d'un seuil d'alerte lié à un niveau d'intégrité (SIL / PL) : absente.

## Statut de lecture

Papier complet (`fulltext.md` lu en entier ; extraction GROBID, section 5 non détectée, texte rattaché à la section précédente). Figures 1-10 non consultées (légendes seules), donc les résultats CICIDS2017 reposent sur le texte. Tableaux 1-4 lus avec corps.
Ce qui suit est déduit et non affirmé par les auteurs : transposabilité aux images et à YOLO, mappage FPGA, limites d'univariance des ECDF, jugement sur le sens dangereux de la surestimation.
