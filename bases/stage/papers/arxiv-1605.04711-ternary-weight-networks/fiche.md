---
id: arxiv-1605.04711-ternary-weight-networks
fiche: done
date: 2026-09-29
---

# Ternary Weight Networks

Fengfu Li, Bo Zhang, Bin Liu, 2016, arXiv preprint. https://arxiv.org/abs/1605.04711
Type : preprint non relu par les pairs

## Problème

Réduire la mémoire et le calcul des réseaux profonds pour les appareils embarqués ; les poids
binaires (BinaryConnect, BWN, XNOR-Net) compriment 32× mais perdent en capacité
d'expression (§1).

## Méthode

- **Ternary Weight Networks (TWN)** : poids contraints à {−1, 0, +1} × un facteur d'échelle
  α ≥ 0 par filtre, en minimisant ‖W − α Ŵ‖² (§2.2, éq. 1).
- Fonction de ternarisation à seuil Δ ; pour Δ donné, α* = moyenne des |W_i| au-dessus du seuil
  (éq. 5) ; règle empirique **Δ* ≈ 0,75 · E(|W|)** (hypothèse de poids uniformes ou gaussiens)
  (§2.3).
- Entraînement comme BinaryConnect / XNOR-Net : ternarisation en passes avant et arrière,
  **copie flottante des poids pour la mise à jour** (SGD momentum, BN, décroissance par
  paliers) (§2.4, Fig. 1).
- Déploiement : seuls les poids ternaires (2 bits) et les α sont stockés → compression jusqu'à
  16× ; multiplications remplacées par des additions (§2.5).
- Arguments : un filtre 3×3 ternaire a 3⁹ = 19 683 motifs contre 512 en binaire (§2.1).

## Plateforme et implémentation

Aucune plateforme matérielle évaluée (n/r). Code PyTorch publié :
https://github.com/Thinklab-SJTU/twns (Abstract).

## Résultats

Table 2 (top-1 %, ResNet18 / ResNet18B entre parenthèses) :

| | MNIST (LeNet-5) | CIFAR-10 (VGG-7) | ImageNet top-1 | ImageNet top-5 |
|---|---|---|---|---|
| TWN | 99,35 | 92,56 | 61,8 (65,3) | 84,2 (86,2) |
| Binaire (BPWN) | 99,05 | 90,18 | 57,5 (61,6) | 81,2 (83,9) |
| Flottant | 99,41 | 92,88 | 65,4 (67,6) | 86,76 (88,0) |

- Détection YOLOv5s sur PASCAL VOC (fine-tuning 150 époques depuis COCO) : mAP@0,5 76,8 %
  (TWN) contre 62,9 % (binaire) et 86,7 % (flottant) ; mAP@0,5:0,95 51,5 / 39,4 / 63,7 %
  (Table 3).
- Les TWN convergent presque aussi vite et stablement que le flottant, le binaire non (Fig. 2).

→ reportés dans `benchmarks.csv` : 3 lignes (ImageNet ResNet18, CIFAR-10 VGG-7, VOC YOLOv5s ;
Tables 2-3, `high`).

## Limites et critique

- Version lue : révision arXiv récente (expériences YOLOv5 ajoutées), pas la version 2016
  d'origine citée dans le manuscrit (déduit de la présence de YOLOv5, sorti en 2020).
- Activations en pleine précision : le gain de calcul réel dépend d'un matériel qui exploite
  les poids ternaires ; aucune mesure de latence ou d'énergie.
- Écart au flottant important sur ImageNet (−3,6 points) et en détection (−10 points de mAP).
- Preprint : type arXiv, pas de venue relue indiquée dans les métadonnées.

## Pertinence pour la thèse

Référence du stage pour la compression extrême des poids (2 bits). Sa technique d'entraînement
(poids réduits en avant, **copie flottante mise à jour**) illustre la contrainte centrale d'un
apprentissage en ligne quantifié : sans copie haute précision, les petites mises à jour se
perdent. Utile surtout comme borne basse de précision face à l'INT8 retenu sur MCU (déduit).

## Gaps identifiés

- Apprentissage continu avec poids ternaires (ancres EWC ternaires ?) : non étudié.
- Aucune mesure matérielle du gain de calcul.

## Statut de lecture

Papier complet (`fulltext.md` lu en entier ; papier court). Table 1 partiellement extraite
(paliers de learning rate déplacés dans §3).
Déduit et non affirmé par les auteurs : version révisée ; intérêt pour l'apprentissage en ligne.
