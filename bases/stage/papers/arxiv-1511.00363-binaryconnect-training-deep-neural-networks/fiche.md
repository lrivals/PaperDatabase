---
id: arxiv-1511.00363-binaryconnect-training-deep-neural-networks
fiche: done
benchmarks: none
date: 2026-09-29
---

# BinaryConnect: Training Deep Neural Networks with binary weights during propagations

Matthieu Courbariaux, Yoshua Bengio, Jean-Pierre David, 2015, arXiv preprint. https://arxiv.org/abs/1511.00363
Type : preprint non relu par les pairs

## Problème

Les multiplieurs sont les composants les plus coûteux (surface, énergie) du matériel
d'apprentissage profond ; des poids binaires remplaceraient la plupart des multiply-accumulate
par des additions (Abstract, §1). Reste à entraîner un réseau avec de tels poids.

## Méthode

- **BinaryConnect** : les poids sont binarisés (+1/−1) pendant les **propagations avant et
  arrière**, mais les gradients s'accumulent dans des **poids réels** mis à jour par SGD,
  seuls capables de retenir des pas minuscules (§2.3, Alg. 1).
- Binarisation déterministe (signe) ou **stochastique** (+1 avec probabilité σ(w), σ = hard
  sigmoid) qui préserve l'espérance du poids (§2.2).
- Poids réels écrêtés à [−1, 1] après chaque mise à jour (§2.4).
- Astuces : batch-norm partout, ADAM pour les CNN, learning rate mis à l'échelle par les
  coefficients d'initialisation (§2.5, Table 1).
- Inférence : poids binaires (version déterministe) ou poids réels (version stochastique, comme
  au test du dropout) (§2.6).
- Interprétation : la binarisation est un bruit sur les poids, donc un régulariseur proche de
  DropConnect (§1, §2.3).

## Plateforme et implémentation

Aucune plateforme matérielle évaluée (n/r). Code annoncé disponible (note de bas de page non
extraite) (§1).

## Résultats

- Protocoles : MLP 3×1024 sur MNIST invariant par permutation ; CNN type VGG
  (2×128C3-MP2-2×256C3-MP2-2×512C3-MP2-2×1024FC-SVM) sur CIFAR-10 sans augmentation ; même CNN
  réduit de moitié sur SVHN (§3).
- Les erreurs de test de BinaryConnect sont « proches de l'état de l'art » et meilleures que le
  réseau sans régulariseur, surtout en version stochastique (légende de la Table 2) — **les
  valeurs de BinaryConnect ne sont pas présentes dans l'extraction** (seules celles de
  concurrents : Network in Network 10,41 % sur CIFAR-10, DropConnect 1,94 % sur SVHN,
  Deeply-Supervised Nets 9,78 % / 1,92 %).
- Optimiseur (petit CNN, CIFAR-10) : SGD 11,45 % ; Nesterov 15,65 % → 11,30 % et ADAM 12,81 %
  → 10,47 % avec mise à l'échelle du learning rate (Table 1) ; lien exact avec BinaryConnect
  non précisé dans le texte extrait.
- Argument matériel : ≈ 2/3 des multiplications de l'entraînement supprimées, soit un gain
  potentiel de 3× ; mémoire au moins 16× plus petite en inférence déterministe (§5).

→ reportés dans `benchmarks.csv` : aucune ligne (`benchmarks: none`) — le corps de la Table 2
(erreurs de BinaryConnect) n'a pas été extrait ; les autres chiffres concernent des concurrents
ou un réglage d'optimiseur.

## Limites et critique

- Uniquement de petits jeux (MNIST, CIFAR-10, SVHN) ; XNOR-Net montrera plus tard l'échec de
  BinaryConnect sur ImageNet (35,4 % top-1).
- Gains matériels estimés, jamais mesurés.
- La mise à jour garde des poids réels en mémoire : aucun gain mémoire pendant l'entraînement.

## Pertinence pour la thèse

Cité dans les notes du stage (`docs/context/`) : c'est l'origine du principe « **poids
quantifiés en propagation, copie haute précision pour les mises à jour** », repris par XNOR-Net,
TWN et la QAT. Pour un EWC en INT8 sur MCU, il pose la même question : où stocker
l'accumulateur haute précision des mises à jour, et à quel coût mémoire (déduit).

## Gaps identifiés

- Suppression des multiplications de la mise à jour elle-même : explicitement laissée en
  perspective (§5).

## Statut de lecture

Papier complet (`fulltext.md` lu en entier). Table 2 réduite à des fragments de concurrents ;
note de bas de page (lien du code) absente.
Déduit et non affirmé par les auteurs : lien avec l'EWC INT8.
