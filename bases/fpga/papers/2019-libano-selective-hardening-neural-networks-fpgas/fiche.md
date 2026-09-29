---
id: 2019-libano-selective-hardening-neural-networks-fpgas
fiche: done
date: 2026-09-29
benchmarks: none
---

# Selective Hardening for Neural Networks in FPGAs

F. Libano, B. Wilson, J. Anderson, M. J. Wirthlin, C. Cazzaniga, C. Frost, P. Rech, 2019, IEEE Transactions on Nuclear Science 66(1), 216-222. https://doi.org/10.1109/TNS.2018.2884460
Type : article de journal

## Problème

Les FPGA SRAM sont sensibles aux SEU dans la mémoire de configuration, qui peuvent modifier routage, LUT ou BRAM. Les réseaux de neurones sur FPGA sont proposés pour des usages critiques (véhicules, militaire, spatial), mais la sensibilité par couche n'a pas été étudiée sur FPGA (§II-A) et le TMR complet est coûteux, voire irréalisable en LUT (§I, §V-C).

## Méthode

- Deux cas d'étude : Iris Flower ANN (2 couches complètement connectées, 19 poids) et MNIST CNN (7 couches : 2 conv, 2 pooling, 2 inner product, ReLU ; 1848 poids ; précision ~94 %), entraînés avec Caffe hors de tout environnement fautif (§II, §II-C, §III).
- Chaque couche est isolée dans un Pblock pour relier une faute à une couche (§III-A). Injection de fautes : ICAP pour l'ANN (campagne exhaustive de tous les bits de configuration de la zone : LUT, DSP, FF, routage ; BRAM exclue) ; pour le CNN, ~13 millions de fautes aléatoires via le processor configuration access port (§III-A).
- Classification des erreurs : « tolerable » (sortie différente mais classification correcte) vs « critical » (classification fausse) (§III-C).
- Durcissement sélectif : TMR seulement sur la couche la plus vulnérable (hidden layer pour l'ANN ; IP2 pour le CNN) (§IV, §V-B). Quatre configurations pour l'ANN : non protégé, TMR sélectif, TMR complet avec voteur PL, TMR complet avec voteur PS (ARM) (§V-B).
- Validation par faisceau de neutrons : LANSCE (Los Alamos) pour le Zynq-7000 et ChipIR (ISIS, R.-U.) pour l'UltraScale+ (§III-B).

## Plateforme et implémentation

Zynq-7000 XC7Z020 (CLG484, 28 nm) pour l'Iris ANN ; Zynq UltraScale+ MPSoC ZU9EG (16 nm FinFET) pour le MNIST CNN (§III). Fréquence : n/r. Ressources : dans la Table I, dont le corps n'est pas extrait (LUT, DSP, FF : n/r ici). Puissance : n/r. Irradiation : ~40 h à LANSCE (fluence 1,6x10^11 n/cm2, ~1,5 million d'années d'exposition naturelle), ~20 h à ChipIR (fluence 3,0x10^11 n/cm2) ; flux terrestre de référence 13 n/(cm2.h) (§III-B, §V-C). Code ou bitstream publiés : non indiqués.

## Résultats

- Les erreurs tolérables dominent les erreurs critiques ; ~4 fois plus fréquentes dans l'ANN (§V-A, Fig. 5). Pour le CNN, la couche IP2 (fully connected finale) est la plus vulnérable (Fig. 6).
- ANN : le TMR sélectif réduit la probabilité d'erreur de 64,2 % par rapport à l'ANN non durci ; TMR complet : 85,1 % (voteur FPGA) et 85,6 % (voteur ARM) (§V-C, Fig. 7). L'introduction annonce 68 % de fautes masquées pour ~45 % de surcoût en ressources, contre ~94 % de masquage et ~200 % de surcoût en TMR complet (§I, §V-C). Écart entre 64,2 % et 68 % non expliqué dans le texte (probablement métriques différentes ; déduit).
- CNN : TMR sélectif sur IP2 : ~40 % de fautes masquées pour 8 % de surcoût ; réduction de 14 % des erreurs critiques (§V-C, Fig. 10-11, Abstract). Le TMR complet n'a pas pu être testé faute de LUT dans le ZU9EG (Table I).
- Efficacité (masquage/ressources) : 25 % supérieure pour le TMR sélectif sur l'ANN (Fig. 9) ; supérieur aussi sur le CNN (Fig. 12, TMR complet théorique).
→ reportés dans `benchmarks.csv` : aucune ligne (résultats de fiabilité sous radiation, sans FPS, précision hardware, ni puissance ; ressources en Table I sans corps extrait) ; `benchmarks: none`.

## Limites et critique

- Réseaux minuscules (19 et 1848 poids) et non critiques : l'extrapolation à un YOLO (des millions de poids) n'est qu'affirmée (« same topology and computational flow », §I).
- Deux cartes, deux installations de faisceau différentes : pas de comparaison croisée ; fautes uniquement dans la configuration CLB/DSP/FF/routage, BRAM exclue de l'injection (§III-A), alors que les poids peuvent résider en BRAM.
- Pour le CNN, pas de baseline TMR complet : l'efficacité comparée est théorique (« calculated theoretical efficiency », §V-C). Le masquage de 40 % reste faible pour une exigence de sûreté ; aucune traduction en SIL, taux de danger ou taux de défaillance par heure.
- Un seul niveau de durcissement (une couche) ; pas de couverture des fautes de données (SEU dans les activations), ni de multi-faute. Pas d'incertitude statistique pour le CNN citée (95 % confiance < 15 % donné pour l'ANN seulement).
- Précision de classification et quantification du CNN : n/r pour la quantification ; le critère « critical » repose sur la classe prédite seulement, pas sur la confiance.

## Pertinence pour la thèse

Papier central pour l'axe fiabilité matérielle : fournit la méthode complète (injection de fautes par couche via ICAP/Pblocks, classification tolérable/critique, validation en neutrons, TMR sélectif) transposable à un YOLO sur SoC FPGA. Il montre aussi que la criticité varie par couche, ce qui motive un durcissement ciblé (poids de la tête de détection, voteur). Ce qu'il laisse ouvert : réseaux de détection (métrique mAP et non simple classe), BRAM, exigences chiffrées de sûreté.

## Gaps identifiés

- Analyse de criticité par couche et TMR sélectif sur un détecteur d'objets (YOLO) sur FPGA, avec une métrique adaptée (mAP, non-détections de personnes).
- Traduction des taux FIT mesurés en objectifs de sûreté (SIL / PL).
- Fautes dans les BRAM (poids) et multi-fautes.

## Statut de lecture

papier complet (fulltext.md lu en entier ; extraction GROBID ok mais les sections I et IV sont rattachées à la section précédente, la Table I n'a pas de corps et les valeurs des figures 5 à 12 ne sont pas dans le texte). Déduit et non affirmé par les auteurs : l'écart 64,2 % / 68 %, la portée limitée pour un YOLO, la traduction en niveaux de sûreté.
