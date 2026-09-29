---
id: arxiv-2402.09780-tinycl-efficient-hardware-architecture-continual
fiche: done
date: 2026-09-29
benchmarks: none
---

# TinyCL: An Efficient Hardware Architecture for Continual Learning on Autonomous Systems

Eugenio Ressa, Alberto Marchisio, Maurizio Martina, Guido Masera, Muhammad Shafique, 2024, arXiv preprint. https://arxiv.org/abs/2402.09780
Type : preprint non relu par les pairs

## Problème

Les accélérateurs DNN existants n'exécutent que l'inférence ; les rares accélérateurs d'entraînement n'ont pas de gestion du workload d'apprentissage continu (CL) et donc de l'oubli catastrophique (Abstract, §I-A). Il faut un matériel exécutant propagation avant, rétropropagation et mise à jour des poids avec une politique CL, sous contraintes de ressources.

## Méthode

Architecture TinyCL en RTL (SystemVerilog) : une unité de traitement de 9 blocs MAC (chacun 8 multiplieurs + 8 additionneurs, reconfigurables en mode multi-opérande ou multi-additionneur) réutilisée pour les six calculs (conv avant, gradient de propagation, gradient du noyau, dense avant, gradient, dérivée des poids) ; une unité de contrôle qui gère la mémoire de replay (politique GDumb) ; parcours de la fenêtre glissante « en serpentin » pour réutiliser 6 des 9 entrées à chaque cycle (§III-C à III-F). Quantification : virgule fixe 16 bits (4 entiers + 12 fractionnaires), produits gardés en pleine précision et additions sur 32 bits (§III-A, §III-D). Seule la famille CL à mémoire (replay) est supportée (§II-B).

## Plateforme et implémentation

ASIC, pas FPGA : synthèse Synopsys Design Compiler en CMOS 65 nm, puis simulation au niveau porte comparée à TensorFlow sur Tesla P100 (§IV-A). Période d'horloge 3,87 ns, 86 mW (méthode de mesure/estimation : n/r, résultat de synthèse ; non mesuré sur silicium), surface 4,74 mm2 ; mémoire = 80 % de la surface et 76 % de la puissance (§IV-B, Fig. 7). Mémoire de replay de 6,144 Mo (1000 images 32x32 RGB) (§IV-A). Code ou netlist publiés : non indiqués (non publiés d'après le texte).

## Résultats

- Modèle test : 2 couches conv + ReLU puis une couche dense, CIFAR-10, 5 tâches de 2 classes, 10 époques, batch 1 (§IV-A). Une époque : 1,76 s sur TinyCL contre 103 s sur P100, soit 58x (§IV-C).
- Cycles : 8 192 cycles pour conv avant / gradient / dérivée des poids sur 32x32x8 avec 8 filtres ; couche dense : 1 280 (avant), 1 821 (gradient des poids), 1 280 (propagation) (§IV-B).
- Table I : TinyCL 3,87 ns, 86 mW, 4,74 mm2, 0,037 TOPS contre HNPU 1 162 mW / 12,96 mm2 / 3,07 TOPS, LNPU 367 mW / 16 mm2 / 0,6 TOPS, ISSCC19 196 mW / 16 mm2 / 0,204 TOPS (Table I).
→ aucune ligne dans `benchmarks.csv` : la seule mesure est un temps d'entraînement par époque sur ASIC 65 nm (1,76 s, puissance de synthèse), sans colonne adaptée ; `latency_ms` aurait été trompeur.
→ reportés dans `benchmarks.csv` (via `bench_rows.csv`) : 1 ligne (TinyCL, ASIC 65 nm, entraînement CL sur CIFAR-10).

## Limites et critique

- Incohérence interne : l'introduction annonce 35x d'accélération (§I-B) alors que l'Abstract et §IV-C donnent 58x (103 s / 1,76 s).
- Comparaison biaisée : baseline GPU avec batch size 1 sous TensorFlow (P100, ancien), donc sous-utilisée ; l'ASIC est en virgule fixe 16 bits contre virgule flottante GPU (déduit). La Table I compare des accélérateurs d'autres nœuds technologiques et précisions (déduit) ; la « latence » de la Table I est la période d'horloge, pas un temps de traitement.
- Puissance issue de la synthèse, pas de mesure ; périmètre (avec ou sans mémoire replay de 6 Mo) non précisé.
- Modèle jouet (2 conv + dense) ; aucun résultat de précision continue rapporté dans le texte extrait ; le texte parle de « Conv + ReLU + Dense » dans l'Abstract et de deux conv en §IV-A.
- Pas d'implémentation FPGA ; la portée pour un SoC FPGA est une transposition à faire (déduit). Aucune considération de sûreté.
- Texte de la conclusion tronqué en fin d'extraction (§V).

## Pertinence pour la thèse

Axe apprentissage continu embarqué : montre une architecture de calcul unifiée avant/arrière avec replay (GDumb) et l'ordre de grandeur de ce que coûte l'entraînement embarqué (86 mW, mémoire dominante). Pour la thèse « sécuritaire certifiable », l'apprentissage en ligne est plutôt un facteur de risque de certification (modèle non figé) ; ce papier illustre la contrainte mais n'apporte rien sur l'assurance. Reste ouvert : cible FPGA, modèles de détection, garantie sur l'oubli.

## Gaps identifiés

- Apprentissage continu sur FPGA pour de la détection (pas seulement classification CIFAR-10).
- Compatibilité de l'apprentissage en ligne avec la certification (modèle non figé, re-validation).

## Statut de lecture

papier complet (fulltext.md lu en entier ; conclusion tronquée dans l'extraction ; Table I lue ; les figures ne sont que des légendes). Déduit et non affirmé par les auteurs : transposabilité FPGA, biais des comparaisons (précision, batch, nœud technologique), absence de mesure silicium.
