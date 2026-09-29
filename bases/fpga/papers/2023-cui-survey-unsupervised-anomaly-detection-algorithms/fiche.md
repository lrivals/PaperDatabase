---
id: 2023-cui-survey-unsupervised-anomaly-detection-algorithms
fiche: done
date: 2026-09-29
benchmarks: none
---

# A Survey on Unsupervised Anomaly Detection Algorithms for Industrial Images

Yajie Cui, Zhaoxiang Liu, Shiguo Lian, 2023, IEEE Access. https://doi.org/10.1109/ACCESS.2023.3282993
Type : article de journal (survey)

## Problème

Les approches supervisées de détection de défauts sur images industrielles exigent beaucoup
d'images annotées, alors que les échantillons défectueux sont rares et les types de défauts
variés (§I, §III). Les auteurs passent en revue les algorithmes non supervisés récents
(entraînés sur images normales seulement) pour l'inspection visuelle industrielle, les jeux de
données publics, et dégagent les problèmes ouverts (Abstract, §I).

## Méthode

Survey, pas de contribution expérimentale propre. Taxonomie en cinq familles (§III, Table 2) :
- reconstruction (AE, VAE, GAN, CAVGA, UTAD, DFR, STPM/RSTPM, reverse distillation, AST, MOCCA,
  OCR-GAN, VT-ADL, SOMAD) : le score d'anomalie est l'erreur de reconstruction ;
- normalizing flows (DifferNet, CFlow, CS-Flow, FastFlow) : densité des features des images normales ;
- représentation (SPADE, PaDiM, PatchCore, Gaussian-AD, Patch SVDD, CFA…) : distance à des
  features de référence issues d'un backbone pré-entraîné ;
- augmentation / anomalies synthétiques (DRAEM, NSA, CutPaste, SSPCAB, AnoSeg) ;
- améliorations d'algorithmes (IGD, FCDD, mean-shifted contrastive loss, attention).
Sections comparatives : avantages/inconvénients par famille (§IV, Tables 2-3), complexité
temps/mémoire, jeux de données (BTAD, ELPV, AITEX, MTD, KolektorSDD, DAGM, MVTec AD, §V).
Défis (§VI) : manque de jeux de données ouverts représentatifs, conflit entre taux de fausses
alarmes (FAR) et d'alarmes manquées (MAR), combinaison apprentissage de distribution +
augmentation, foundation models, apprentissage multimodal.

## Plateforme et implémentation

Sans objet (aucune implémentation FPGA). Seule mesure de vitesse : Xeon E5-2680 V4 + GTX 1080Ti
(§IV) ; le corps de la Table 4 (FPS, temps additionnel, paramètres additionnels par méthode)
n'a pas été extrait : `n/r`. Code : sans objet.

## Résultats

Chiffres repris de la littérature, sans mesure propre sauf un test « edible oil » :
- MVTec AD (Table 10, reconstruit Docling, à vérifier) : moyenne (AUROC image, AUROC pixel)
  PatchCore (99.1, 98.1), FastFlow (99.4, 98.5), CFA (99.2, 98.2), CFlow (98.3, 98.6), SPADE
  (96.2, 96.5), Patch SVDD (92.1, 95.7).
- Sur données réelles d'huile alimentaire (Table 12, à vérifier), AUROC détection : PatchCore
  single 92.2, PatchCore 3 modèles 94.4, AST 91.8, « loin » des résultats MVTec (§V).
- Tables 5-9 (BTAD, AITEX/ELPV, MTD, KolektorSDD, DAGM) : AUROC de méthodes hétérogènes.
- Qualitatif (§IV) : PatchCore/SPADE sans entraînement mais forte mémoire pour les banques de
  patchs ; SPADE a une inférence lente (kNN) ; reconstruction rapide en inférence ; NF plus
  coûteux à entraîner.
→ reportés dans `benchmarks.csv` : aucune ligne (survey, chiffres de tiers, aucune plateforme
FPGA). `benchmarks: none`.

## Limites et critique

- Aucune cible embarquée : aucun coût matériel (mémoire, latence, virgule fixe) n'est
  quantifié ; la Table 4 sur GTX 1080Ti n'est pas exploitable ici (corps manquant).
- Tables 5-10 comparent des méthodes issues de papiers différents, protocoles non harmonisés
  (déduit) ; tableaux reconstruits par Docling, chiffres à vérifier ; Table 10 contient au moins
  une coquille (« 100.0.98.7 »).
- Ne traite que des images statiques d'objets/surfaces manufacturés, pas de vidéo, pas de scènes
  avec personnes (exclu explicitement, §II-A).
- Les seuils de décision, l'étalonnage de l'incertitude et les garanties de couverture ne sont
  pas discutés ; le conflit FAR/MAR est posé mais sans méthode (§VI-B). Aspects reproductibilité
  (code, jeux de hyperparamètres) non abordés. Le résultat « huile » repose sur un jeu privé
  non décrit en détail.

## Pertinence pour la thèse

Pertinence indirecte. Sert de cartographie du domaine « détection d'anomalies / OOD non
supervisée » pour un moniteur d'exécution d'un YOLO de surveillance (détecter une entrée hors
domaine) et pour l'axe autoencodeurs (famille reconstruction : AE/VAE/CAE, DFR). Les familles
à faible coût de calcul en inférence (reconstruction légère, distillation élève-enseignant
compacte) sont les candidates plausibles pour un FPGA ; les méthodes à banque de patchs
(PatchCore, SPADE) ont un coût mémoire élevé (§IV) — inférence de ma part pour le FPGA. Ne
répond à aucune question de certification ni de personnes.

## Gaps identifiés

- Aucune méthode d'anomalie visuelle non supervisée évaluée sur FPGA dans ce survey ; les
  autoencodeurs sur images côté FPGA restent à combler (gap déjà connu).
- Coût matériel (mémoire, latence, énergie) des méthodes d'anomalie visuelle non comparé.
- Compromis FAR/MAR et seuils de décision non traités de façon calibrée (lien avec
  prédiction conforme / moniteur d'exécution).

## Statut de lecture

Papier complet (fulltext.md lu en entier). Table 4 : corps non extrait (légende seule).
Tables 1-3, 5-10, 12 reconstruites par Docling, chiffres à vérifier.
Déduit et non affirmé par les auteurs : la pertinence pour FPGA et pour un moniteur d'exécution
(coût mémoire, adéquation), et l'hétérogénéité des protocoles entre tables.
