---
id: 2023-mou-ink-detection-carbonized-herculaneum-papyri
fiche: done
date: 2026-11-15
---

# Ink Detection from Carbonized Herculaneum Papyri using Deep Learning

Farzana Sharmin Mou, Tanvir Ahmed, 2023, International Conference on Computer and Information Technology (ICCIT), Cox's Bazar. DOI 10.1109/iccit60459.2023.10441240 (https://doi.org/10.1109/iccit60459.2023.10441240)
Type : conférence (actes ICCIT 2023 ; relu par les pairs selon la venue, mais sans code ni protocole détaillé)

## Problème

Détecter l'encre carbonée, sans contraste d'absorption aux rayons X sur le papyrus carbonisé, à partir des « surface volumes » (65 tranches) des fragments détachés du Kaggle « Vesuvius Challenge - Ink Detection », avec comme vérité terrain une image binaire d'encre tirée d'une photo infrarouge recalée (§I, §III-A1, Fig. 3).

## Méthode

- Entrée : sous-volumes de forme (64, 64, 20) centrés sur des positions aléatoires, avec les labels correspondants ; images redimensionnées à une hauteur de 4000 ; augmentation limitée à des ajustements de contraste aléatoires ; validation sur des zones non utilisées à l'entraînement (§III-A1, Fig. 4).
- Trois modèles : U-Net (convolutions séparables, connexions résiduelles, sortie sigmoïde, Adam, entropie croisée binaire), Attention U-Net (portes d'attention encodeur/décodeur), Attention U-Net avec autoencodeur pré-entraîné sur AL-PUB (lettres grecques de papyrus, 24 classes, 1000 images par classe, 64x64 étendues à 20 canaux par des canaux nuls) (§III-A2, §III-B).
- Trois ensembles de ces modèles : moyenne, vote, moyenne pondérée. Les poids de la moyenne pondérée et le seuil de binarisation ne sont pas donnés (n/r).
- Post-traitement : composantes connexes (filtre de taille), érosion/dilatation 3x3 (§III-C, Fig. 6).
- Métriques : précision, rappel, exactitude, Dice, IoU, au niveau du pixel (§III-D).

## Plateforme et implémentation

Matériel d'entraînement, GPU, temps d'entraînement ou d'inférence : n/r. Cadre logiciel : n/r (l'architecture est décrite en termes Keras-like : « UpSampling2D », « SeparableConv », sans que le papier nomme le cadre). Hyperparamètres (taux d'apprentissage, époques, batch, taille du filtre de composantes) : n/r. Code et poids : non publiés (aucun lien dans le papier).

## Résultats

Table I (une seule valeur par méthode, sans écart-type ni répétitions ; split non précisé : validation ou fragments tenus à l'écart, voir critique) :

| Méthode | Précision | Rappel | Exactitude | Dice | IoU |
|---|---|---|---|---|---|
| U-Net | 0.763 | 0.537 | 0.927 | 0.630 | 0.460 |
| Attention U-Net | 0.723 | 0.640 | 0.930 | 0.679 | 0.514 |
| Attention U-Net pré-entraîné | 0.751 | 0.595 | 0.931 | 0.664 | 0.497 |
| Ensemble (moyenne) | 0.831 | 0.710 | 0.950 | 0.766 | 0.620 |
| Ensemble (vote) | 0.889 | 0.568 | 0.942 | 0.693 | 0.531 |
| Ensemble (moyenne pondérée) | 0.877 | 0.654 | 0.950 | 0.749 | 0.599 |

Meilleur Dice : 0.766, ensemble par moyenne (Table I, §IV-C). Le pré-entraînement AL-PUB ne bat pas l'Attention U-Net seul (Dice 0.664 contre 0.679). Évaluation visuelle qualitative : Fig. 7. Baseline externe : aucune ; le score de 48,44 de Dice cité en §II vient d'un autre travail [6], sans lien de protocole.
→ reportés dans `benchmarks.csv` : 6 lignes (une par méthode, métrique Dice ; les autres métriques de Table I sont dans le tableau ci-dessus, `chunk_id` 2023-mou#027.0).

## Limites et critique

- Protocole d'évaluation flou : Table I ne dit pas si elle porte sur la zone de validation (prise dans le même fragment que l'entraînement, Fig. 4) ou sur des fragments tenus à l'écart ; le jeu de test caché du Kaggle n'est pas utilisé (n/r). Si c'est la validation intra-fragment, les scores sont probablement optimistes (inférence, non affirmée par les auteurs).
- Pas de répétitions, pas d'intervalle de confiance, pas de test de significativité : les écarts entre U-Net, Attention U-Net et variantes sont de quelques points de Dice.
- Pas d'ablation du post-traitement : on ne sait pas si Table I est avant ou après composantes connexes et morphologie.
- Le pré-entraînement sur des lettres grecques en 2D (étendues par des canaux nuls) est discutable : pas de justification de l'écart de domaine avec des volumes CT ; il n'apporte pas de gain.
- Pas de comparaison avec les solutions publiques du concours Kaggle ni avec les travaux fondateurs (Seales et al.) ; la revue de littérature est descriptive. Dice 0.766 non comparable en l'état à d'autres Dice (split, seuil, post-traitement inconnus).
- Les auteurs ne traitent pas de faux positifs ni d'hallucination (le Dice pixel ne prouve pas la lisibilité) ; leur propre texte reconnaît que la lisibilité visuelle ne suit pas toujours les métriques (§IV-A).
- Résolution : le texte cite 4 µm (§III-A1) et 4-8 µm (§I) pour les scans de fragments ; la valeur de 4 µm vient du papier mais reste à recouper avec EduceLab. Aucun code publié.

## Pertinence pour la thèse

Pour le projet Elder-scrolls (axe `ink-detection`), c'est une référence mineure : un exemple de ligne de base sur les fragments Kaggle (Dice 0.63 à 0.77) avec U-Net, Attention U-Net et ensembles, qui confirme que l'ensemble est le gain le plus net (+0.087 de Dice sur le meilleur modèle seul, Dice 0.679 → 0.766, Table I). Rien sur les rouleaux entiers, le 8-9 µm, la super-résolution ni la validation à l'aveugle : le papier laisse ouverte la question de la généralisation d'un fragment à un rouleau.

## Gaps identifiés

- Évaluation hors fragment d'entraînement (rouleaux scannés à 8-9 µm) : absente de ce papier.
- Quantification de l'incertitude et des faux positifs sur les cartes d'encre : non traitée.
- Apport réel d'un pré-entraînement 2D sur lettres grecques pour la détection d'encre : non démontré (Dice 0.664 contre 0.679).

## Statut de lecture

papier complet (fulltext.md lu en entier). Avertissement : `extraction.backend` vaut `pymupdf` et `extraction.ok` vaut `false` : le texte est complet en apparence mais les figures sont absentes et Table I a été aplatie en texte (valeurs recoupées avec le commentaire de §IV-C, concordantes).
Ce qui suit est déduit et non affirmé par les auteurs : l'optimisme possible de la validation intra-fragment ; l'absence de gain du pré-entraînement comme effet du décalage de domaine ; le caractère mineur de l'apport pour la base. Les lignes `benchmarks.csv` ont `confidence: high` (valeurs de Table I recoupées avec le texte de §IV-C).
