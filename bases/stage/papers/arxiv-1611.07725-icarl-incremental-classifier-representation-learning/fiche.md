---
id: arxiv-1611.07725-icarl-incremental-classifier-representation-learning
fiche: done
date: 2026-09-29
---

# iCaRL: Incremental Classifier and Representation Learning

Sylvestre-Alvise Rebuffi, Alexander Kolesnikov, Georg Sperl, Christoph H. Lampert, 2017, IEEE Conference on Computer Vision and Pattern Recognition (CVPR). https://arxiv.org/abs/1611.07725
Type : conférence

## Problème

Apprendre de nouvelles classes au fil d'un flux (class-incremental) avec un classifieur
multi-classe unique, compétitif à tout instant, et une mémoire et un calcul bornés (§1).
Les méthodes existantes soit exigent toutes les données, soit reposent sur une
représentation fixe incompatible avec l'apprentissage profond (§1, §3).

## Méthode

Trois composants (§1, §2) :
- **Classification par plus proche moyenne d'exemplaires** : prototype µ_y = moyenne des
  features (L2-normalisées) des exemplaires stockés de la classe ; décision
  argmin ‖φ(x) − µ_y‖ (§2.2). Les prototypes suivent automatiquement les changements de
  représentation, contrairement à des poids de sortie découplés.
- **Sélection des exemplaires par herding** : liste priorisée dont la moyenne approche au
  mieux la moyenne de classe ; budget total K, m = K/t par classe ; réduction en coupant la
  fin de liste (§2.4, Alg. 4-5).
- **Apprentissage de représentation** : entraînement sur nouvelles données + exemplaires,
  perte = classification (sigmoïdes, cross-entropy binaire) + **distillation** des sorties
  des anciennes classes (§2.3, Alg. 3).
- Mémoire totale : paramètres du feature extractor + K images + un vecteur par classe (§2.1).
- Protocole proposé : iCIFAR-100 (lots de 2, 5, 10, 20, 50 classes, 10 ordres), iILSVRC-small
  (100 classes, lots de 10) et -full (1000 classes, lots de 100), métrique « average
  incremental accuracy » (§4).
- ResNet-32, K = 2000 (CIFAR, Theano) ; ResNet-18, K = 20 000 (ImageNet, TensorFlow) (§4).

## Plateforme et implémentation

Aucune plateforme matérielle (n/r). Code publié : http://www.github.com/srebuffi/iCaRL (§4).

## Résultats

- iCaRL domine LwF.MC, représentation figée et fine-tuning, d'autant plus que les lots de
  classes sont petits (Fig. 2) ; LwF.MC est second sauf sur iILSVRC-full (représentation
  figée meilleure) ; même réseau entraîné sur tout : 68,6 % (Fig. 2).
- Average incremental accuracy iCIFAR-100 (Table 1a) : iCaRL 57,0 / 61,2 / 64,1 / 67,2 /
  68,6 pour 2 / 5 / 10 / 20 / 50 classes par lot ; LwF.MC 11,7 / 32,6 / 44,4 / 54,4 / 64,5.
- Ablations : les hybrides se placent entre iCaRL et LwF.MC ; la distillation peut nuire pour
  de très petits lots (hybrid2 57,6 > iCaRL 57,0 à 2 classes) (Table 1a).
- NCM sur toutes les données (non incrémental) : 59,3 / 62,1 / 64,5 / 67,5 / 68,7 — écart
  faible avec les exemplaires (Table 1b).
- Plus de mémoire K → meilleurs résultats ; au-delà d'environ 1000 exemplaires, iCaRL ≈ NCM
  (Fig. 4).
- Matrices de confusion : iCaRL homogène, fine-tuning ne prédit que le dernier lot (Fig. 3).

→ reportés dans `benchmarks.csv` : 3 lignes (lots de 2, 10 et 50 classes, Table 1a, `high`).

## Limites et critique

- Stocke des **images brutes** (K = 2000 ou 20 000) : incompatible avec la vie privée et coûteux
  en mémoire embarquée ; les auteurs l'évoquent comme perspective (§5).
- Résultats ImageNet uniquement en courbes (Fig. 2).
- Le 68,6 % du réseau non incrémental coïncide avec iCaRL à 50 classes par lot (Table 1a) :
  à lots grands, peu de marge à combler.
- Pas de mesure de temps ou de mémoire réelle.

## Pertinence pour la thèse

Référence du scénario **class-incremental** et de la famille rejeu + distillation, citée
dans la bibliographie du stage. Pour la maintenance prédictive, l'analogue serait l'arrivée
de nouveaux modes de défaut ; le classifieur NME est léger (moyennes de features), mais le
stockage d'exemplaires et le réentraînement du feature extractor sont hors de portée d'un
MCU, d'où les variantes à rejeu latent (Ravaglia 2021) (déduit).

## Gaps identifiés

- Budget d'exemplaires en kilo-octets (et non en images) pour signaux capteurs : non étudié.
- Class-incremental sur séries temporelles industrielles (nouveaux défauts) : absent.

## Statut de lecture

Papier complet (`fulltext.md` lu en entier). La définition du critère i) est tronquée dans
l'extraction (§1) ; conclusion coupée puis reprise dans la légende du Table 1.
Déduit et non affirmé par les auteurs : transposition aux nouveaux modes de défaut ;
inadaptation au MCU.
