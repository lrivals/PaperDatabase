---
id: arxiv-1901.09192-selectivenet-deep-neural-network-integrated
fiche: done
date: 2026-10-29
benchmarks: none
---

# SelectiveNet: A Deep Neural Network with an Integrated Reject Option

Yonatan Geifman, Ran El-Yaniv, 2019, arXiv preprint (la version ICML 2019 n'est pas vérifiée ici). https://arxiv.org/abs/1901.09192
Type : preprint non relu par les pairs

## Problème

Les mécanismes de rejet existants appliquent un seuil sur la confiance d'un réseau pré-entraîné sur tous les points (Softmax Response, SR ; MC-dropout), sans optimiser le réseau pour la zone de couverture visée (§1, §3). Les auteurs veulent un modèle qui apprend prédiction et rejet ensemble, pour une couverture cible c donnée (§2, Éq. 1 : minimiser le risque sélectif sous contrainte φ(g) ≥ c). MC-dropout coûte jusqu'à des centaines de passes avant par prédiction (§3).

## Méthode

Réseau à trois têtes sur un corps commun (§4.1) : prédiction f, sélection g (sigmoïde, prédit si g(x) ≥ 0,5) et tête auxiliaire h (entraînement seul, expose le corps à tous les exemples). Perte : risque sélectif empirique + pénalité quadratique λ·max(0, c − couverture)² (variante de point intérieur, Éq. 2), combinée à la perte auxiliaire : L = αL(f,g) + (1−α)L_h, α = 0,5, λ = 32 (§4.2, §6.3). Calibration post-entraînement de la couverture par un seuil τ (percentile 100(1−c) de g sur un jeu de validation non étiqueté), avec borne de Hoeffding (§5). Corps : VGG-16 adapté (CIFAR-10, SVHN, Cats vs Dogs) ; MLP pour la régression (§6.3). Pas de quantification ni de cible matérielle.

## Plateforme et implémentation

Aucune plateforme matérielle : entraînement et évaluation logiciels, plateforme n/r. Code publié : https://github.com/geifmany/SelectiveNet (§6).

## Résultats

- CIFAR-10, erreur 0/1 (risque sélectif) : à couverture 0,80, SelectiveNet 0,86±0,06 contre SR 1,05±0,07 et MC-dropout 1,08±0,05 ; à 1,00, 6,79 pour tous (Table 2).
- SVHN : 0,53±0,01 contre 0,61 (SR et MC-dropout) à 0,80 ; indistinguable à 0,95 (Table 3).
- Cats vs Dogs : 0,35±0,09 contre SR 0,68±0,05 à 0,80 (Table 4, corps de tableau non extrait proprement : valeurs à vérifier ; lues dans le texte extrait).
- Régression (Concrete, UCI) : gain de 26,8 à 30,5 % relatif sous 0,9 de couverture annoncé dans le texte (§7.2), tandis que la Table 5 montre 4,4 à 17,1 % : incohérence interne à signaler.
- Écart de couverture moyen par rapport à la cible : 3,63 % (SelectiveNet) contre 11,98 % (SR) (Table 1) ; la calibration τ le corrige (§5, §8.1).
Pas de métrique de faux négatifs par classe : le risque est l'erreur globale.
→ reportés dans `benchmarks.csv` : aucune ligne. Article ML sans mesure sur plateforme matérielle (FPS, puissance, ressources absents) ; la base ne garde que les mesures de plateforme.

## Limites et critique

- Petits jeux d'images 32×32 / 64×64 et un seul jeu tabulaire ; pas de détection d'objets, pas de faux négatifs d'une classe critique (§7).
- Risque symétrique (erreur 0/1) : aucune pondération du coût d'un rejet ou d'un faux négatif, contrairement à ce que voudrait une surveillance de sécurité.
- Un modèle par couverture cible (re-entraînement) ; la cible c est fixée à l'entraînement, la calibration τ ne compense que partiellement.
- Surcoût d'inférence : tête de sélection FC 512 + batch norm + ReLU puis une sortie sigmoïde (§6.3, 1901.09192#013.1), non chiffré ; aucun coût mémoire, latence ni quantification mesurés.
- Hypothèse i.i.d. : aucune évaluation sous décalage de distribution ou OOD. Les résultats de l'écart relatif sont des moyennes sur 3 runs (§8.1) seulement.
- Preprint ; les baselines (SR, MC-dropout) sont celles de 2017.

## Pertinence pour SerreIA

Axe `calibration-decision` : rejet des prédictions peu fiables d'un classifieur de maladies. SelectiveNet apprend prédiction et rejet ensemble pour une couverture cible, et sert de borne haute à la simple option de rejet par seuil sur la softmax (SR), que SerreIA peut appliquer sans réentraîner. Gain mesuré sur CIFAR-10 : 8,5 % (0,95 de couverture) à 26,8 % (0,75, face à MC-dropout) de risque sélectif en moins (1901.09192#015.0) ; à 0,80, 0,86 contre 1,05 pour SR (Table 2). SR et MC-dropout sont équivalents entre eux (même passage), donc MC-dropout n'apporte rien de plus que SR ici.

Attention au vocabulaire : « calibration » dans l'article désigne le réglage du seuil τ pour atteindre une couverture cible (§5, 1901.09192#008.0, #018.0), pas la calibration probabiliste (ECE, temperature scaling). Les deux sont complémentaires et ne se substituent pas.

## Pour SerreIA

Contexte (fourni par le projet, non vérifié dans l'article) : classifieur `vision/` EfficientNet-B0 multi-têtes ; hors domaine (PlantDoc) ECE `sante` 0,13, ECE `classe` 0,30, spécificité 0,50, 42 % de faux positifs sur images saines ; ni temperature scaling ni seuil réglé (`docs/14-resultats-phase1.md`, `docs/17-analyse-systeme.md` §10) ; règle `edge/controller/regles.yaml` : `classe_conf_min: 0.6` non calibré ; simulateur `sim/`.

Méthode recommandée, par ordre de coût :
1. **Sans réentraîner (à faire d'abord)** : temperature scaling sur la tête `sante` et sur la tête `classe`, puis rejet par seuil SR (max softmax) sur les probabilités recalibrées, seuil choisi par courbe risque-couverture sur un jeu de validation (c'est la procédure de calibration de couverture de §5 appliquée à SR : percentile 100(1−c) du score sur validation). Remplacer `classe_conf_min: 0.6` par ce seuil. Fichiers : `vision/eval/` (courbe risque-couverture, ECE), `edge/controller/regles.yaml`.
2. **Décision asymétrique** : le risque de l'article est l'erreur 0/1 (limite). Pour SerreIA, fixer le seuil sur la sortie `sante` pour borner les faux positifs sur plantes saines (cible : spécificité, pas erreur globale) et mesurer la couverture résultante ; ajouter un état « incertain » dans le contrôleur au lieu de traiter le rejet comme une maladie.
3. **SelectiveNet seulement si le seuil SR ne suffit pas** : ajouter à EfficientNet-B0 une tête de sélection g (FC 512 + BN + ReLU + sigmoïde, 1901.09192#013.1) et une tête auxiliaire h, perte avec λ = 32, α = 0,5 (§4.2, §6.3) ; un modèle par couverture cible, donc un réentraînement par valeur de c. À essayer seulement après l'étape 1, car sans gain démontré hors domaine.

Métrique de validation : courbe risque-couverture (selective risk à couverture donnée, AURC) en domaine et hors domaine séparément, plus ECE avant/après et spécificité sur images saines à la couverture retenue. Critère d'acceptation : couverture réellement atteinte sur PlantDoc proche de la cible (l'article trouve 3,63 % d'écart moyen pour SelectiveNet contre 11,98 % pour SR en domaine, Table 1 ; hors domaine n/r).

Pièges :
- Les résultats de l'article sont en domaine (i.i.d., CIFAR-10, SVHN, Cats vs Dogs) ; aucune évaluation sous décalage de distribution. Un seuil ou une couverture calibrés sur une validation de laboratoire ne se transfèrent pas à PlantDoc : calibrer sur un jeu de validation représentatif du terrain (images de serre), et re-mesurer en hors domaine. Une tête g apprise peut se surajuster au domaine d'entraînement.
- Les baselines de l'article (SR, MC-dropout) sont des modèles non recalibrés ; un SR après temperature scaling peut réduire l'écart (déduit, non testé par les auteurs).
- Contrainte Hailo : la tête g est un petit FC + sigmoïde (une seule passe, coût fixe), donc compilable a priori ; en revanche MC-dropout (plusieurs passes) est coûteux sur NPU. Le seuil SR et le temperature scaling se font hors réseau (division des logits, comparaison), donc sans impact sur le HEF quantifié ; mais la quantification INT8 modifie les logits : recalibrer T et le seuil sur les sorties quantifiées. Effet de la quantification sur g : non étudié (déduit).
- Le rejet par seuil dépend de la couverture voulue : sur la serre, un rejet trop fréquent déclenche une alerte inutile, un rejet trop rare laisse passer un faux positif ; à simuler dans `sim/` (`faults.py`, `scenario.py`) en injectant des images hors domaine avec le taux de rejet mesuré.

## Gaps identifiés

- Prédiction sélective hors domaine (plantes de terrain) : absente de l'article.
- Interaction temperature scaling + SR contre SelectiveNet : non comparée.
- Perte sélective à coût asymétrique (faux positif sur plante saine) : absente.
- Effet de la quantification (INT8, NPU Hailo) sur la tête de sélection et sur le seuil.

## Statut de lecture

Papier complet (fulltext.md lu en entier ; extraction grobid, ok ; Table 4 et Table 6 sans corps extrait, Table 5 mélangée avec la Table 6 : valeurs de ces tableaux à vérifier ou lues dans le texte).
Ce qui suit est déduit et non affirmé par les auteurs : la compatibilité avec Hailo et la quantification INT8 ; l'adaptation au classifieur de SerreIA ; l'effet du temperature scaling sur SR ; le contexte SerreIA (fourni par la demande, non relu dans le dépôt SerreIA).
