---
id: arxiv-2106.08295-white-paper-neural-network-quantization
fiche: done
date: 2026-09-29
---

# A White Paper on Neural Network Quantization

Markus Nagel, Marios Fournarakis, Rana Ali Amjad, Yelysei Bondarenko, Mart Van Baalen, Tijmen Blankevoort, 2021, arXiv preprint. https://arxiv.org/abs/2106.08295
Type : preprint non relu par les pairs

## Problème

La quantification réduit la latence et l'énergie de l'inférence, mais le bruit qu'elle
introduit peut dégrader la précision ; ce white paper rassemble l'état de l'art et des
pipelines testés pour la quantification post-entraînement (PTQ) et avec entraînement (QAT)
(Abstract, §1).

## Méthode

- **Fondamentaux matériels** : MAC en virgule fixe, accumulateurs 32 bits, requantification
  en INT8 entre couches ; un facteur d'échelle par tenseur se factorise hors de la somme
  (§2.1, éq. 3).
- Quantification **affine** (échelle s, zero-point z, b bits), **symétrique**, **puissance de
  deux** ; granularité par tenseur, par canal ou par groupe (§2.2).
- **Simulation de la quantification** dans le graphe flottant ; repliement de la batch-norm ;
  fusion des activations ; cas du pooling, de l'addition et de la concaténation (§2.3).
- Recommandation : **poids symétriques, activations asymétriques** (le terme dépendant des
  données coûte autant qu'un canal supplémentaire) ; par canal pour les poids si le matériel le
  permet (§2.4).
- PTQ (§3) : réglage des plages (min-max, MSE, cross-entropy pour les logits, plages déduites
  de la BN) ; **Cross-Layer Equalization** (rééquilibrage des plages entre couches successives
  par équivariance de ReLU, éq. 20-22) et absorption des grands biais ; **correction du biais**
  empirique ou analytique ; **AdaRound** (choix appris de l'arrondi vers le haut ou le bas,
  éq. 29-35) ; pipeline standard (Fig. 8) et procédure de débogage (Fig. 9).
- QAT (§4) : STE (gradient de l'arrondi = 1 dans la plage, 0 hors plage), échelle et
  zero-point **apprenables** (éq. 36-40) ; repliement statique de la BN ; initialisation par PTQ
  ; pipeline standard (Fig. 12).

## Plateforme et implémentation

Aucune mesure sur plateforme : toutes les expériences en quantification simulée (§2.3).
Auteurs Qualcomm AI Research ; outil sous-jacent non nommé dans le texte extrait.

## Résultats

- Plages d'activation (poids FP32) : à 4 bits, MSE + cross-entropy donne 59,07 % (ResNet18) et
  30,94 % (MobileNetV2) contre 18,82 % et 0,53 % en min-max (Table 2).
- CLE sur MobileNetV2 INT8 par tenseur : 0,12 % → 69,91 %, 70,92 % avec absorption des biais,
  contre 70,65 % en par canal (Table 3).
- **Pipeline PTQ** (Table 6) : W8A8 à moins de 0,7 point du FP32 pour tous les modèles ; W4A8 par
  canal : ResNet18 68,91 (FP32 69,68), MobileNetV2 69,79 (71,72), EfficientNet-lite 74,01
  (75,42), EfficientDet-D1 35,08 mAP (40,08) ; BERT-base avec quelques activations en 16 bits.
- **Pipeline QAT** (Table 10, par canal) : W4A4 ResNet18 68,83, ResNet50 75,53, MobileNetV2
  66,89, EfficientDet-D1 28,68 mAP ; W8A8 parfois au-dessus du FP32 (ResNet18 70,43).
- Initialisation de la QAT : l'avantage de l'initialisation MSE disparaît après 20 époques
  (Table 8) ; MobileNetV2 ne s'entraîne pas sans CLE (Table 9, texte).

→ reportés dans `benchmarks.csv` : 3 lignes (MobileNetV2 PTQ W8A8 par canal, Table 6, `high` ;
ResNet18 et MobileNetV2 QAT W4A4 par canal, Table 10 aplatie, `medium`).

## Limites et critique

- Rapport technique (preprint) d'un industriel ; aucune latence ni énergie mesurée.
- Tables 1, 4, 5 et 7 non extraites (seuls les textes qui les commentent).
- Évaluation ciblée sur des accélérateurs à virgule fixe type NPU ; le cas MCU sans unité
  dédiée n'est pas traité.
- Résultats rapportés avec le meilleur learning rate par configuration (§4.5).

## Pertinence pour la thèse

Cité dans les notes du stage (`docs/context/`) : c'est la référence la plus complète pour
justifier les choix INT8 (symétrique pour les poids, asymétrique pour les activations, par
canal, réglage MSE des plages). Deux points s'appliquent directement à un tenseur de Fisher ou
à des ancres EWC quantifiées : l'arbitrage **erreur d'écrêtage ↔ erreur d'arrondi** (§2.2) et
le **biais systématique** de la quantification (§3.3), qui fausserait une pénalité quadratique
(déduit).

## Gaps identifiés

- Quantification de tenseurs non standards (importances, ancres, statistiques de dérive) : hors
  du périmètre.
- Aucune mesure sur MCU.

## Statut de lecture

Papier complet (`fulltext.md` lu en entier). Figures en LaTeX brut non exploitables ;
Tables 1, 4, 5, 7 absentes ; Tables 3 et 10 aplaties.
Déduit et non affirmé par les auteurs : application aux tenseurs d'EWC.
