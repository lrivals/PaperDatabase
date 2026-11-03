---
id: arxiv-1906.02530-can-you-trust-your-model
fiche: done
date: 2026-11-03
---

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
→ reportés dans `benchmarks.csv` (proposition, 6 lignes, Table G.2, `confidence: medium`) : ECE médian sur les 80 variantes ImageNet-C, ResNet-50, par méthode : Vanilla 0.102, Temp. Scaling 0.072, Ensembles (M=10) 0.032, MC-Dropout 0.043, LL-Dropout 0.071, LL-SVI 0.106. Pas de lignes pour MNIST, CIFAR-10, Criteo (valeurs seulement en figures ou tableaux sans libellé fiable).

## Limites et critique

- Classification uniquement ; aucune image de plante ni détection.
- Méthodes les plus fiables (ensembles, dropout, SVI) coûtent k passes avant ou k modèles : coût que le papier reconnaît (§5) sans le mesurer ; pour un RPi 5 / Hailo, impact déduit, non mesuré.
- Pas de quantification ni de précision réduite ; l'effet sur la calibration n'est pas étudié.
- Ordre des méthodes non stable (SVI meilleur sur MNIST, pas ailleurs, §4.2) ; SVI difficile à entraîner à grande échelle (§5).
- Décalages synthétiques (corruptions, rotations) : leur représentativité de dérives réelles (éclairage de serre, capteur, fond de terrain) est non établie.
- Preprint (la fiche d'origine, écrite pour la base `fpga`, a été revérifiée contre le texte et sa pertinence réécrite pour `serre`) ; hyperparamètres tunés par méthode, ImageNet non tuné (§4).

## Pertinence pour la thèse

Pour SerreIA (base `serre`, axe `calibration-decision`) : réponse directe à la question « comment calibrer un classifieur (temperature scaling, ECE) et choisir les seuils ». Apports : (1) la temperature scaling ajustée sur validation i.i.d. (cas d'un classifieur PlantVillage/CCMT) se dégrade quand le décalage croît (§4.2, §5), donc elle ne protège pas sur PlantDoc ou en serre réelle ; sur Criteo elle aggrave même le Brier (§4.4) ; (2) protocole transposable : ECE, Brier et accuracy-vs-confiance sous corruptions graduées, utile pour évaluer le rejet des crops hors distribution et les seuils de fausses alertes « anormal » ; (3) l'entropie prédictive permet de s'abstenir (§4.3), ce qui alimente le garde-fou « validation humaine » ; (4) coût : ensembles M=5 (≈5 passes avant) à comparer au budget d'inférence RPi 5 / Hailo-8L (Table S1, formules seulement). Non traité : images de plantes, détection, quantification INT8 et son effet sur la calibration, agrégation multi-feuilles. Déduit (non affirmé par les auteurs) : les liens avec PlantDoc, Hailo et l'agrégation par capture. Les corruptions ImageNet-C (flou, bruit, luminosité) ne remplacent pas un vrai écart de domaine feuille/terrain.

## Gaps identifiés

- Calibration sous écart de domaine réel PlantVillage vers PlantDoc (et non corruptions synthétiques), avec temperature scaling vs ensembles.
- Effet de la quantification INT8 (Hailo) sur l'ECE et le seuil de rejet.
- Coût en latence d'un ensemble M=5 ou d'un MC-Dropout sur Raspberry Pi 5 / Hailo-8L.

## Statut de lecture

papier complet (fulltext.md lu en entier, backend grobid, extraction ok). Les figures ne sont pas lisibles en texte : résultats tirés du texte et des Tables G. Les tableaux G sont extraits sans légende fiable (l'étiquette « G.1 CIFAR-10 » est perdue, le tableau d'en-tête sans titre après G.3 est non identifié) ; les chiffres de G.2 (ImageNet) sont recoupés avec le texte seulement qualitativement, d'où `medium`. Déduit et non affirmé par les auteurs : toute la section « Pertinence » (liens SerreIA) et le jugement sur le coût des ensembles pour un budget embarqué.
