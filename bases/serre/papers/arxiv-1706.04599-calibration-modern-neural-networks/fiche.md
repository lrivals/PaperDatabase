---
id: arxiv-1706.04599-calibration-modern-neural-networks
fiche: done
date: 2026-10-29
benchmarks: none
---

# On Calibration of Modern Neural Networks

Chuan Guo, Geoff Pleiss, Yu Sun, Kilian Q. Weinberger, 2017, arXiv preprint (ICML 2017 d'après la littérature, non indiqué dans metadata.json). https://arxiv.org/abs/1706.04599
Type : preprint non relu par les pairs (version arXiv)

## Problème

Les réseaux profonds modernes sont mal calibrés : leur confiance dépasse leur exactitude (surconfiance), contrairement aux réseaux plus anciens (Abstract, §1). Les auteurs cherchent les facteurs qui causent ce défaut et une correction simple.

## Méthode

- Métriques (§2) : diagrammes de fiabilité, ECE (moyenne pondérée des écarts confiance/exactitude sur M bins, M = 15 dans les tableaux), MCE (écart maximal sur les bins, 1706.04599#003.0), NLL.
- Causes observées (§3) : capacité, Batch Normalization, moindre weight decay dégradent la calibration alors que l'exactitude progresse ; surapprentissage de la NLL en fin d'entraînement (1706.04599#004.1, 1706.04599#013.2).
- Correctifs a posteriori (§4) : histogram binning, isotonic regression, BBQ, et pour le multiclasse matrix scaling, vector scaling, temperature scaling. Tous exigent un jeu de validation hold-out et supposent entraînement, validation et test tirés de la même distribution (1706.04599#005.0).
- Temperature scaling : une seule température T divise les logits avant le softmax, optimisée sur la NLL du jeu de validation ; l'argmax ne change pas, donc l'exactitude est inchangée (1706.04599#007.3).

## Plateforme et implémentation

Sans objet (logiciel, Torch7, §5). Temps de calcul : problème convexe à un paramètre, environ 10 itérations de gradient conjugué, une fraction de seconde (§5, Computation time). Code publié : n/r dans les passages lus.

## Résultats

- Temperature scaling surpasse les autres méthodes sur les tâches vision et se compare aux autres en NLP ; vector scaling retrouve quasiment la même solution (vecteur presque constant), donc la miscalibration est « intrinsèquement de faible dimension » (1706.04599#010.0).
- ECE avant/après temperature scaling (Table 1, M = 15, 1706.04599#022.0) : CIFAR-100 ResNet 110 16,53 % vers 1,26 % ; CIFAR-10 ResNet 110 4,6 % vers 0,83 % ; ImageNet ResNet 152 5,48 % vers 1,86 % ; Birds ResNet 50 9,19 % vers 1,85 %.
- Matrix scaling échoue avec beaucoup de classes (Birds 21,13 %, CIFAR-100 25,49 %, non convergent sur ImageNet) : trop de paramètres pour un petit jeu de validation (1706.04599#010.0, 1706.04599#010.1).
- Exceptions : SVHN et Reuters, déjà sous 1 % d'ECE (Table 1).
→ reportés dans `benchmarks.csv` : aucune ligne (calibration logicielle, aucune métrique FPGA/edge ; le schéma de benchmarks.csv ne porte pas l'ECE).

## Limites et critique

- Hypothèse explicite : validation et test de même distribution (1706.04599#005.0). Le papier ne mesure ni décalage de domaine ni OOD ; la calibration obtenue en domaine ne se transfère pas d'office hors domaine (limite déduite : l'article ne l'évalue pas).
- ECE dépend du nombre de bins (les auteurs le reconnaissent, 1706.04599#010.0) ; taille du jeu de validation utilisée : n/r dans les passages lus.
- Cas binaire ou multi-étiquettes (têtes `sante`, `classe` multi-têtes) : couvert seulement par Platt scaling et binning en §4.1, sans résultats dédiés.
- Pas de seuil de décision ni de rejet traités.

## Pertinence pour SerreIA

Axe `calibration-decision` : référence fondatrice pour le point de la question de recherche « comment calibrer un classifieur (temperature scaling, ECE) ». Elle apporte la recette la plus simple et la mieux validée (une température), mais avec l'hypothèse in-domain qui est précisément ce qui manque à SerreIA.

## Pour SerreIA

> **Mise à jour (29/10/2026)** : SerreIA a déjà `vision/eval/temperature.py` (temperature scaling de la tête `sante`, ajusté sur les crops vérité terrain de PlantDoc val, T copié dans le bundle edge) et `vision/eval/decision_search.py` (recherche de la règle de décision). Restent à faire d'après cette fiche : la tête `classe`, l'ECE avant/après en domaine et hors domaine, et la recalibration après quantification INT8 Hailo.

À reprendre concrètement (fichiers de `/home/leonard/Documents/Perso/SerreIA/`, lecture seule) :

1. **Temperature scaling par tête** sur le classifieur `vision/` (EfficientNet-B0 multi-têtes) : un T pour `sante`, un T pour `classe`, ajustés sur la NLL d'un jeu de validation, logits figés (1706.04599#007.3). L'argmax est inchangé : l'exactitude et les décisions de classe restent identiques, seules les probabilités changent. Coût négligeable (1 paramètre, quelques itérations). Pour une tête binaire `sante` en sigmoïde, appliquer le même T aux logits avant la sigmoïde (ou Platt scaling, §4.1, 1706.04599#006.5).
2. **Mesure** : ECE à 15 bins plus diagramme de fiabilité, avant/après, pour chaque tête, sur `docs/14-resultats-phase1.md` / `docs/17-analyse-systeme.md` §10 comme référence (ECE `sante` 0,13, `classe` 0,30 hors domaine PlantDoc). Ajouter la NLL et le MCE (1706.04599#003.0) ; viser une baisse mesurée, pas l'ordre de grandeur de la Table 1 (CIFAR-100 : 16,5 % vers 1,3 %), qui est en domaine.
3. **Piège principal : jeu de validation** (1706.04599#005.0). Calibrer sur PlantVillage/CCMT in-domain donne un T trop optimiste pour le terrain. Ajuster T sur un jeu de validation hors domaine (une partie de PlantDoc ou images de la serre réelle, disjointe du test) et reporter l'ECE en domaine et hors domaine séparément. Ne jamais régler T sur le jeu de test PlantDoc. Déduit : l'article ne garantit rien sous décalage.
4. **Seuil de décision** : après calibration, remplacer `classe_conf_min: 0.6` dans `edge/controller/regles.yaml` par un seuil choisi sur la courbe confiance/exactitude du jeu de validation hors domaine, à rappel donné sur les cas malades, en visant les 42 % de faux positifs sur images saines (spécificité 0,50). Mesurer faux positifs et rappel au seuil retenu. Le papier fournit la calibration, pas la règle de seuil : la choisir par un balayage (recherche complémentaire dans la base : sélective/rejet).
5. **Simulateur `sim/`** : ré-appliquer T avant de transformer les sorties du classifieur en événements, pour que le contrôleur voie des confiances calibrées ; recalibrer T après tout changement de modèle ou quantification Hailo (la quantification modifie les logits : T à réestimer sur les logits du modèle déployé, déduit).

Étapes : (a) isoler les logits des deux têtes ; (b) découper un jeu de validation hors domaine disjoint du test ; (c) ajuster T (LBFGS ou recherche en ligne) ; (d) ECE/NLL/diagramme avant-après en domaine et hors domaine ; (e) choisir le seuil ; (f) mettre à jour `regles.yaml` et rejouer dans `sim/`. Métrique de validation : ECE hors domaine sur un test jamais utilisé pour T, plus taux de faux positifs sur images saines au rappel cible.

## Gaps identifiés

- Calibration sous décalage de domaine (PlantVillage vers PlantDoc) non traitée par ce papier : à compléter par Ovadia et al. 2019 (Can you trust your model, présent dans la base fpga) ou un papier d'adaptation.
- Choix du seuil et rejet : voir les papiers selective classification.

## Statut de lecture

Lu par recherche ciblée et lecture de passages (définitions, §3, §4, §5, Table 1, Computation time) ; `fulltext.md` non lu en entier, conformément à la consigne de la base. Extraction grobid ok.
Déduit et non affirmé par les auteurs : transfert hors domaine, application aux têtes multi-têtes/sigmoïde, recalibration après quantification, tout le plan SerreIA ci-dessus.
