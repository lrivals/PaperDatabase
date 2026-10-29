---
id: arxiv-1906.02530-can-you-trust-your-model
fiche: todo
date: 2026-10-26
benchmarks: none
---

> **Importée de la base `fpga` le 2026-10-29.** Cette fiche a été écrite pour une autre base (autre thème) : pertinence à réévaluer ici, puis `fiche: done` via `/paper-fiche`. Statut d'origine : done.

# Can You Trust Your Model's Uncertainty? Evaluating Predictive Uncertainty Under Dataset Shift

Yaniv Ovadia, Emily Fertig, Jie Ren, Zachary Nado, D Sculley, Sebastian Nowozin, Joshua V Dillon, Balaji Lakshminarayanan, Jasper Snoek, 2019, arXiv preprint. https://arxiv.org/abs/1906.02530
Type : preprint non relu par les pairs (la version publiée à NeurIPS 2019 n'est pas celle lue ici ; non vérifié)

## Problème

Les décisions fondées sur la sortie d'un DNN exigent une incertitude prédictive fiable, or les données déployées dérivent de la distribution d'entraînement. Les auteurs constatent l'absence de comparaison empirique à grande échelle des méthodes d'incertitude *sous décalage de distribution* (§1) : la calibration i.i.d. ne garantit pas la calibration sous décalage.

## Méthode

Benchmark de classification, sans matériel : méthodes à p(y|x) seul (§3) : Vanilla (softmax max), Temperature Scaling post-hoc, MC-Dropout, Deep Ensembles (M=10), SVI, et variantes dernière couche (LL-SVI, LL-Dropout). Métriques : accuracy, NLL, Brier, ECE, entropie, courbes accuracy-vs-confiance (§3). Décalages : MNIST (rotation/translation), CIFAR-10 et ImageNet avec 80 corruptions ImageNet-C (16 types x 5 intensités), 20 Newsgroups (classes impaires comme décalage, LM1B comme OOD), Criteo (jetons catégoriels remplacés au hasard), séquences génomiques (§4, App. F). OOD complet : Not-MNIST, SVHN. Hyperparamètres par optimisation bayésienne (App. A.8).

## Plateforme et implémentation

Aucune plateforme matérielle (modèles LeNet, ResNet-20, ResNet-50, LSTM, MLP, CNN génomique ; App. A). Puissance : n/r. Code et prédictions des modèles annoncés open source (note de bas de page §1, lien non repris dans le texte lu). Coûts de calcul/mémoire par méthode seulement en formules (Table S1, App. A.9) : ensembles et dropout coûtent mk, SVI 2m de stockage ; aucune mesure de latence.

## Résultats

- La qualité de l'incertitude se dégrade avec le décalage pour toutes les méthodes (§5).
- La temperature scaling est bien calibrée en i.i.d. et à faible décalage mais est dépassée par les méthodes épistémiques quand le décalage croît (§4.2, §5) ; sur Criteo son Brier est pire que Vanilla (§4.4).
- Les Deep Ensembles sont les meilleurs sur la plupart des métriques (CIFAR-10, ImageNet, texte, génomique) ; M=5 suffit à l'essentiel du gain (§5, App. D). Sur ImageNet-C, ECE médian : 0.032 pour les ensembles contre 0.102 Vanilla et 0.072 Temp. Scaling (Table G.2, tableau extrait, chiffres à recouper).
- Les variantes dernière couche (LL-SVI, LL-Dropout) font parfois pire que Vanilla sous décalage et sur OOD (§4.2, §4.3).
- La plupart des méthodes sont « confiantes et fausses » sur OOD complet (MNIST, §4.1).
- Génomique : même la meilleure méthode reste sous 65 % de précision à p(y|x) >= 0.9 (App. F).
→ reportés dans `benchmarks.csv` : aucune ligne. Article ML sans mesure sur plateforme matérielle ; ce n'est pas un survey, mais la base exclut les mesures hors plateforme (benchmarks: none).

## Limites et critique

- Classification uniquement ; pas de détection d'objets, ni de faux négatifs / objets manqués.
- Méthodes les plus fiables (ensembles, dropout, SVI) coûtent k passes avant ou k modèles : incompatible a priori avec un budget FPGA temps réel ; le papier le reconnaît (§5) sans mesurer.
- Pas de quantification, de précision réduite ou de WCET ; l'effet de la quantification sur la calibration n'est pas étudié.
- Ordre des méthodes non stable (SVI meilleur sur MNIST, pas ailleurs, §4.2) ; SVI difficile à entraîner à grande échelle (§5).
- Décalages synthétiques (corruptions, rotations) : leur représentativité de dérives réelles (éclairage, caméra industrielle) est non établie.
- Preprint ; hyperparamètres tunés par méthode, ImageNet non tuné (§4).

## Pertinence pour la thèse

Rattache à l'axe `failure-prediction` du sujet ARCYS (prédiction d'échec ciblée sur les faux négatifs d'un détecteur de personnes, moniteur sur FPGA). Apport : (1) argument empirique que le score de confiance brut et la temperature scaling ne suffisent pas sous décalage, ce qui motive un moniteur dédié et conservateur (abstention / sortie anticipée prudente) ; (2) protocole d'évaluation transposable (ECE, Brier, accuracy-vs-confiance sous corruptions graduées) pour valider ce moniteur ; (3) tableau de coûts (Table S1) base de discussion sur le surcoût d'un ensemble matériel. Laisse ouvert : détection d'objets, faux négatifs, quantification, coût FPGA/WCET d'un estimateur d'incertitude. Déduit (non affirmé par les auteurs) : lien avec les sorties anticipées et la certification.

## Gaps identifiés

- Incertitude sous décalage évaluée sur un détecteur (pas un classifieur), en visant les faux négatifs.
- Effet de la quantification sur la calibration et la prédiction d'échec.
- Coût matériel (latence, WCET, ressources FPGA) des estimateurs d'incertitude, notamment ensembles à M=5.

## Statut de lecture

papier complet (fulltext.md lu en entier, backend grobid, extraction ok). Les figures n'étant pas lisibles en texte, les résultats sont tirés du texte et des Tables G ; Table G.2 recoupée avec le texte seulement qualitativement. Déduit et non affirmé par les auteurs : toute la section « Pertinence » (lien ARCYS) et le jugement d'incompatibilité des ensembles avec un budget FPGA.
