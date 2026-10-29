---
id: arxiv-1703.09844-multi-scale-dense-networks-resource
fiche: done
date: 2026-10-26
benchmarks: none
---

# Multi-Scale Dense Networks for Resource Efficient Image Classification

Gao Huang, Danlu Chen, Tianhong Li, Felix Wu, Laurens Van Der Maaten, Kilian Q. Weinberger, 2017, arXiv preprint. https://arxiv.org/abs/1703.09844
Type : preprint non relu par les pairs (version arXiv ; la version publiée à ICLR 2018 n'est pas celle lue ici : à ne pas affirmer d'après ce texte)

## Problème

Classification d'images sous contrainte de calcul au test (§1, §3) : (1) *anytime prediction*, où le budget par exemple est aléatoire et la sortie doit pouvoir être produite à tout instant ; (2) *budgeted batch classification*, où un budget global fixe est dépensé inégalement entre exemples « faciles » et « difficiles ». Ajouter naïvement des classifieurs intermédiaires à un CNN dégrade la précision : les couches précoces manquent de features à grosse échelle, et les classifieurs intermédiaires perturbent la formation des features des couches tardives (§4, Fig. 3).

## Méthode

MSDNet : réseau à features multi-échelles maintenues sur toute la profondeur (connexions horizontales et diagonales par convolution à pas, Fig. 2), connectivité dense à la DenseNet pour que les classifieurs précoces n'interfèrent pas avec le classifieur final (§4.1), classifieurs de sortie sur l'échelle la plus grossière uniquement (2 conv + average pooling + linéaire). Perte : somme pondérée des entropies croisées des classifieurs (poids égaux en pratique). Réduction du réseau (suppression progressive des échelles fines) et *lazy evaluation* (§4.1).
Mode batch : un exemple sort au classifieur k si le maximum du softmax dépasse un seuil θ_k. Les seuils sont calés sur un jeu de validation pour respecter le budget moyen B, sous l'hypothèse d'une probabilité de sortie q constante par étage (§4.1). Mode anytime : on propage jusqu'à épuisement du budget et on renvoie la dernière prédiction.
Pas de quantification, pas de toolflow, pas de mapping FPGA.

## Plateforme et implémentation

Aucune plateforme matérielle. Le coût est exprimé en FLOPs (« computational budget »), jamais en latence, FPS ou énergie mesurés : n/r. Entraînement avec le framework de Gross & Wilber (2016) (§5). Code : annoncé à une URL anonyme (« https://anonymous-url », §5), donc non publié dans cette version ; bitstream sans objet.

## Résultats

- ImageNet, anytime : pour des budgets de 0,1 à 0,3 x 10^10 FLOPs, MSDNet gagne ~4 à 8 % de précision top-1 sur un ensemble ResNets/DenseNets (§5.1, Fig. 5).
- ImageNet, batch (lots de M = 128) : à 1,7 x 10^9 FLOPs en moyenne, ~75 % top-1, ~6 % de plus qu'un ResNet à FLOPs égaux ; 2 à 3 fois moins de FLOPs que DenseNet à précision égale (§5.2, Fig. 7).
- CIFAR-100 (lots de 256) : précision d'un ResNet-110 avec ~1/10 du budget, jusqu'à ~5 fois plus efficace que DenseNets, Stochastic Depth, WideResNets, FractalNets (§5.2). Résultats CIFAR-10 similaires (App. B.2).
- Ablation (CIFAR-100, ~3,0 x 10^8 FLOPs) : la connectivité dense est cruciale ; retirer le multi-échelle ne nuit qu'aux faibles budgets (App. B.1, Fig. 10).
- Sorties précoces : les premiers classifieurs reconnaissent les exemples prototypiques, le dernier les atypiques (Fig. 6, qualitatif).
Valeurs lues dans le texte ; les courbes des figures ne sont pas chiffrées.
→ reportés dans `benchmarks.csv` : aucune ligne. La base ne garde que les mesures sur plateforme matérielle ; ce papier ne rapporte que des FLOPs et des précisions sur GPU/CPU non précisés.

## Limites et critique

- Coût en FLOPs seulement : non comparable à des mesures de latence, FPS ou énergie. Les FLOPs ne prédisent pas la latence sur FPGA ou MCU (déduit).
- Seuil de confiance = max softmax : la qualité du critère de sortie n'est pas analysée. Pas de calibration, pas d'analyse de l'erreur commise parmi les exemples sortis tôt, pas de taux de faux négatifs (le papier ne mesure que la précision globale top-1).
- Les seuils supposent une probabilité de sortie q constante et un jeu de validation représentatif ; aucune étude de robustesse à un décalage de distribution.
- Classification d'images 32x32 et ImageNet uniquement : ni détection, ni segmentation (cité comme travail futur, §6).
- Latence d'exécution non déterministe par construction (chemin dépendant de l'entrée) : aucune discussion du pire cas ; en anytime, le budget est une variable aléatoire, pas une borne (§3).
- Comparaisons : baselines entraînées par les auteurs avec le même schéma ; les FractalNets sont repris de leur papier d'origine (§5.1). Pas de baseline matérielle.
- Code non publié dans cette version (URL anonyme).

## Pertinence pour la thèse

Papier fondateur des sorties anticipées par seuil de confiance (axe `failure-prediction`). Pour la thèse ARCYS (prédiction d'échec ciblée sur les faux négatifs d'un détecteur de personnes, sorties anticipées conservatrices) :
- Fournit le mécanisme de base : classifieurs intermédiaires, seuil sur max softmax, calage des seuils sur validation pour un budget donné. Une sortie « conservative » reviendrait à relever θ_k pour ne sortir que lorsque l'erreur (en particulier le faux négatif « personne ») est improbable, ce que le papier ne traite pas (déduit).
- Montre que le max softmax sépare exemples faciles et difficiles (Fig. 6), mais sans garantie de fiabilité : à comparer aux travaux de calibration et de confiance du corpus.
- Pour le moniteur sur FPGA et le WCET : la variabilité du chemin d'exécution est le problème ; le pire cas reste le réseau complet, donc un WCET certifiable doit le borner (déduit). Rien sur la quantification ni sur l'implémentation matérielle.
- Reste ouvert : détection (pas de classification), faux négatifs, garanties de sécurité, implémentation FPGA, coût réel du moniteur.

## Gaps identifiés

- Sorties anticipées conservatrices contrôlant le taux de faux négatifs (aucune analyse ici).
- Early exit pour la détection d'objets, pas seulement la classification.
- Mesure de latence / énergie réelle d'un réseau à sorties anticipées sur FPGA ; borne WCET d'un réseau à chemin dynamique.
- Effet de la quantification sur les seuils de confiance.

## Statut de lecture

papier complet (fulltext.md lu en entier, extraction grobid ok ; figures non lisibles en texte : courbes de Fig. 3, 5, 7, 8, 10, 11 non exploitables chiffre à chiffre, seuls les chiffres du texte sont repris).
Déduit et non affirmé par les auteurs : lien entre FLOPs et latence FPGA/MCU ; variante conservatrice par relèvement des seuils ; remarque sur le WCET ; absence de publication du code dans la version finale.
