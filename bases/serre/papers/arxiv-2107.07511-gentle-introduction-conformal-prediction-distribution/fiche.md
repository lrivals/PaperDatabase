---
id: arxiv-2107.07511-gentle-introduction-conformal-prediction-distribution
fiche: done
date: 2026-11-03
benchmarks: none
---

# A Gentle Introduction to Conformal Prediction and Distribution-Free Uncertainty Quantification

Anastasios N. Angelopoulos, Stephen Bates, 2021, arXiv preprint. https://arxiv.org/abs/2107.07511 (arXiv 2107.07511, pas de DOI)
Type : preprint non relu par les pairs. Tutoriel / survey pédagogique avec code Python et notebooks.

## Problème

Les modèles « boîte noire » déployés en contexte à risque ont besoin d'une quantification d'incertitude
rigoureuse, alors que leurs scores heuristiques (softmax, écart-type prédit) n'ont aucune garantie
(Abstract, §1). Les auteurs veulent donner un mode d'emploi autonome de la prédiction conforme et des
techniques « distribution-free » : garanties non asymptotiques, valables pour tout modèle et toute
distribution des données (Abstract, §1).

## Méthode

Pas de méthode nouvelle : exposé didactique de méthodes existantes.
- **Split conformal** (§1) : score de non-conformité s(x,y) (ex. 1 moins le softmax de la vraie classe), quantile
  ⌈(n+1)(1-α)⌉/n des scores sur n points de calibration, ensemble C(x) = {y : s(x,y) ≤ q}. Garantie de couverture
  marginale 1-α ≤ P(Y∈C(X)) ≤ 1-α+1/(n+1) (Eq. 1, Théorème 1), sous échangeabilité/i.i.d. calibration-test.
- **Scores** (§2) : APS pour la classification (§2.1), conformalized quantile regression (§2.2), écart-type ou autre
  scalaire d'incertitude (§2.3), conformalized Bayes (§2.4). L'utilité des ensembles dépend du score, pas la validité (§1).
- **Évaluation** (§3) : adaptativité (histogramme des tailles, couverture conditionnelle, FSC, SSC), taille du jeu de
  calibration (loi Beta de la couverture ; n≈1000 « suffisant pour la plupart des usages », §3.2), vérification de la couverture par splits répétés (§3.3).
- **Extensions** (§4) : couverture par groupe (§4.1) et par classe (§4.2), conformal risk control (§4.3, Théorème 2),
  **détection d'outliers** avec contrôle des faux positifs ≤ α (§4.4), covariate shift pondéré (§4.5, Théorème 3),
  dérive temporelle par poids sur les scores récents (§4.6, Théorème 4).
- **Exemples travaillés** (§5) : multilabel (MS COCO, contrôle du FNR), segmentation de tumeurs, prévision de
  température avec dérive (Yandex Weather, Shifts), toxicité de commentaires (Jigsaw/WILDS), **classification sélective**
  avec garantie de précision sur les prédictions retenues (§5.5, ImageNet, via Learn then Test).
- §6 : full conformal, CV+/jackknife+ ; §7 : historique ; Annexes A-B : Learn then Test (contrôle de risques généraux,
  p-values, FWER) et exemple OOD + couverture simultanés.
Toolflow : n/r (Python, PyTorch/NumPy).

## Plateforme et implémentation

Aucune plateforme matérielle, aucune puissance, aucune latence : n/r. Code Python en figures (Fig. 2, 3, 5, 7, 12, 20) ;
les auteurs indiquent un notebook Jupyter par exemple de code (Abstract), sans lien dans le texte extrait (les liens/icônes sont
perdus dans `fulltext.md`) : lien exact n/r. Bibliothèque MAPIE citée (§7).

## Résultats

Pas de résultats expérimentaux comparatifs : exemples illustratifs, surtout en figures dont `fulltext.md` ne donne que
les légendes (Fig. 13 à 17).
- Seuil de calibration : n=1000 donne une couverture typiquement entre 0,88 et 0,92 pour α=0,1 (§3.2, Fig. 11).
- Taille de calibration n(ε) pour δ=0,1 et α=0,1 : 22, 102, 2491, 9812, 244390 pour ε=0,1 ; 0,05 ; 0,01 ; 0,005 ; 0,001
  (Table 1 ; le tableau est mal reconstruit par l'extraction, valeurs lisibles mais l'alignement avec ε est une lecture à confirmer).
- Détection de commentaires toxiques, α=10 % : 70 % des commentaires toxiques sont signalés (§5.4, Fig. 16 ; modèle Detoxify BERT, Jigsaw/WILDS).
- Prévision de température avec changement de distribution : la version pondérée atteint la couverture visée en régime
  établi et récupère vite après le point de rupture, mieux que le non pondéré (§5.3, Fig. 15) ; pas de chiffre.
→ reportés dans `benchmarks.csv` : aucune ligne. Papier de tutoriel (traitement « survey » de la skill) ; les chiffres
ci-dessus sont des illustrations sur des jeux sans lien avec la serre, sans mesure de plateforme.

## Limites et critique

- Garantie **marginale** seulement : pas de couverture conditionnelle (impossible en général, §3.1), donc des sous-groupes
  (ex. espèces, stades, domaines) peuvent être sous-couverts ; remède partiel : couverture par groupe/classe (§4.1-4.2),
  qui exige assez de calibration par groupe.
- Hypothèse d'échangeabilité calibration/test : rompue par le passage PlantVillage vers terrain (PlantDoc). Seuls un
  covariate shift **connu** (rapport de vraisemblance w(x), §4.5) ou une dérive lente (§4.6) sont traités ; les auteurs
  reconnaissent que le cas général est un domaine de recherche actif (§4.5).
- Inutilité possible si le score est mauvais : ensembles larges mais valides (§1).
- Aucune évaluation quantitative systématique ni comparaison à des baselines (APS vs autres scores, etc.) ; exemples non reproduits ici.
- Aucun coût de calcul ou mémoire sur edge (RPi, Hailo) : le split conformal est « computationnellement trivial » (§2, Discussion), affirmation qualitative, non mesurée.
- Preprint non relu par les pairs (v1 2021 ; la version utilisée peut être plus récente, non vérifié).

## Pertinence pour la thèse

Pertinent pour l'axe `calibration-decision` du projet SerreIA : (1) le rejet / OOD avec taux de fausses alertes
garanti ≤ α (§4.4, Prop. 3) répond à la question « fausses alertes "anormal" à rappel donné » ; (2) la classification sélective avec garantie de
précision sur les prédictions retenues (§5.5, Learn then Test) et le contrôle simultané OOD + couverture (Annexe B) donnent un cadre
pour le seuil de décision par capture ; (3) conformal risk control (§4.3) pour borner le taux de faux négatifs (usage « ne pas rater une maladie ») ;
(4) calibration par classe ou par groupe (§4.1-4.2) pour des classes de maladies rares. Complète temperature scaling/ECE (non traités ici) par une
garantie sans hypothèse de modèle. Reste ouvert : garantie sous écart de domaine non connu (PlantVillage vers PlantDoc), agrégation
multi-feuilles par capture, coût sur Raspberry Pi/Hailo. La prévision de température avec dérive (§5.3) est une analogie pour la GRU de microclimat, pas une validation en serre.

## Gaps identifiés

- Aucune évaluation de la prédiction conforme sur des maladies de plantes ni en conditions de terrain (shift PlantVillage vers PlantDoc) dans ce papier.
- Garantie sous écart de domaine inconnu : non couverte.
- Prédiction conforme pour la décision agrégée par capture (plusieurs feuilles non indépendantes, échangeabilité douteuse).
- Coût et mise en œuvre sur edge (RPi 5, Hailo-8L) : n/r.
- Intervalles conformes pour la prévision GRU du microclimat (§5.3 en donne une version générique, sans serre).

## Statut de lecture

papier complet : `fulltext.md` lu en entier (extraction grobid, `extraction.ok` vrai ; avertissement « métadonnées à vérifier à la main » conservé).
Les figures (Fig. 1-22) ne sont connues que par leurs légendes et le code OCR, les valeurs de Fig. 13-17 sont absentes ; Table 1 est mal reconstruite.
Ce qui suit est déduit et non affirmé par les auteurs : l'inadéquation de l'échangeabilité pour PlantVillage vers PlantDoc ; l'usage
du rejet conforme pour réduire les fausses alertes « anormal » ; l'intérêt pour l'agrégation par capture ; l'absence de coût edge mesuré
(les auteurs ne parlent pas d'edge).
