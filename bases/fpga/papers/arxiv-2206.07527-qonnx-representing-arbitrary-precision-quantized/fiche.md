---
id: arxiv-2206.07527-qonnx-representing-arbitrary-precision-quantized
fiche: done
date: 2026-09-29
benchmarks: none
---

# QONNX: Representing Arbitrary-Precision Quantized Neural Networks

Alessandro Pappalardo, Yaman Umuroglu, Michaela Blott, Jovan Mitrevski, Ben Hawks, Nhan Tran, Vladimir Loncar, Sioni Summers, Hendrik Borras, Jules Muhizi, Matthew Trahms, Shih-Chieh Hsu, Scott Hauck, Javier Duarte, 2022, arXiv preprint. https://arxiv.org/abs/2206.07527
Type : preprint non relu par les pairs (les métadonnées d'extraction portaient l'avertissement « à vérifier à la main » : la venue n'est pas précisée).

## Problème

Il n'y a pas de consensus sur la façon de représenter un réseau quantifié (QNN) à haut niveau, ce qui nuit à l'interopérabilité entre outils d'entraînement (QAT) et compilateurs FPGA (§I). Les formats ONNX existants (quantized operator, integer operator, QDQ) sont limités à 8 bits, ne représentent pas les précisions inférieures à 8 bits, dupliquent les opérateurs ou n'exposent pas les sorties en haute précision (§III).

## Méthode

- Extension rétrocompatible avec des Clip : format « quantized operator avec clipping » et QCDQ (quantize-clip-dequantize), qui modélisent des précisions au plus égales à 8 bits sur les outils existants, au prix de limites (précision au plus 8 bits, bornes scalaires, donc pas de largeur de bit par canal) (§IV).
- Nouveau format QONNX, de plus haut niveau, avec trois opérateurs (Table II) : Quant (quantification uniforme affine avec dé-quantification fusionnée, entrée et sortie float32, attributs signed, narrow, rounding_mode, entrées scale, zero_point, bit_width), BipolarQuant (binaire) et Trunc (troncature des bits de poids faible, p. ex. pour un average pooling quantifié) (§V). La représentation entière est laissée à l'implémentation ; tensor-wise ou channel-wise est décidé par le broadcast ; bit_width peut être un float32 (intervalles non alignés sur une puissance de deux, utiles pour borner les débordements) (§V).
- Utilitaires Python (pip) : exécution d'un modèle QONNX (moteur d'exécution nœud par nœud de FINN, conçu pour vérifier la correction, pas la performance), inférence de formes, repliement de constantes, conversion channels-first vers channels-last, documentation (§V).
- Intégrations : export depuis Brevitas (QONNX, QCDQ, quantized operator avec clipping) et conversion de QKeras via tf2onnx (§VI-A, §VI-B) ; ingestion par hls4ml (les nœuds Quant deviennent des types de quantification ; la dé-quantification est propagée à travers les opérateurs linéaires pour être synthétisable, §VI-C) et par FINN depuis la version 0.7b de novembre 2021 (conversion vers le dialecte FINN-ONNX, activations remplacées par des MultiThreshold, seules ReLU, hardtanh et identité gérées, erreur si l'architecture est incompatible, §VI-D). QONNX model zoo (§VI-E, Fig. 5).

## Plateforme et implémentation

Sans objet côté matériel : c'est une spécification de représentation intermédiaire et une bibliothèque logicielle. Pas de mesure de latence, de puissance ou de ressources. Code : bibliothèque et model zoo publics (références [26] et [31] du texte, liens non repris dans l'extraction) ; bitstream : sans objet.

## Résultats

Il n'y a pas de résultats expérimentaux chiffrés dans le texte lu : le papier est une spécification et un rapport d'outil. Éléments qualitatifs : Table I (comparaison des formats : précision arbitraire, variantes d'arrondi, sous 8 bits, quantification poids seuls, évitement de duplication d'opérateurs, sortie haute précision ; les croix du corps ne sont pas restituées par l'extraction, et le texte ne donne que QONNX comme couvrant l'ensemble) ; Fig. 5 du model zoo (précision en fonction du nombre d'opérations binaires BOPs sur MNIST, CIFAR-10 et ImageNet, sans valeurs dans le texte).
→ reportés dans `benchmarks.csv` : aucune ligne (aucune mesure de performance ; la liste des modèles du zoo est coupée dans le texte extrait). `benchmarks: none`.

## Limites et critique

- Papier de spécification : pas de benchmark de bout en bout (ressources FPGA, latence, précision après compilation) comparant QONNX à un flot sans QONNX ; l'intérêt est l'interopérabilité, non mesurée.
- Les ingestions sont partielles : FINN ne gère que ReLU, hardtanh et l'identité (§VI-D) ; hls4ml doit propager les dé-quantifications pour être synthétisable, avec un cas des échelles en puissance de deux « envisagé » mais non implémenté (§VI-C) ; QKeras : seuls quantized_bits et quantized_relu sont gérés (§VI-A).
- Sémantique : la représentation entière est laissée à l'implémentation ; aucune garantie formelle que deux outils implémentent l'arrondi ou la saturation de manière identique (déduit ; le papier mentionne seulement que l'exécution sert à vérifier la correction).
- Le format « QCDQ » est limité à 8 bits et moins, sans bit-width par canal (§IV).
- Aucune vérification formelle ni traçabilité de la conversion n'est discutée.
- Texte extrait tronqué à la fin (voir Statut de lecture) : liste du model zoo et conclusion manquantes ; Table II sans corps extrait (les opérateurs sont décrits dans le texte).

## Pertinence pour la thèse

Axe toolflows. QONNX est le format d'échange entre l'entraînement quantifié (Brevitas, QKeras) et les toolflows FPGA FINN et hls4ml : il fixe la sémantique de la quantification d'un modèle de la base et sert de point d'entrée à la chaîne de déploiement. Pour la thèse « IA sécuritaire certifiable » : une représentation explicite, exécutable et vérifiable de la quantification est un maillon de la traçabilité entre le modèle entraîné et le modèle implémenté (déduit, non affirmé par les auteurs). Il faut un modèle YOLO exportable en QONNX pour l'utiliser ; les limites d'ingestion (activations prises en charge par FINN) sont à tester sur les couches de YOLO (SiLU, LeakyReLU non listées par le papier). Ouvert : équivalence formelle entre le QONNX et le matériel généré, et couverture des opérateurs d'un détecteur.

## Gaps identifiés

- Preuve d'équivalence ou de conformité entre un modèle QONNX et l'implémentation générée par FINN/hls4ml (traçabilité pour la certification).
- Couverture des opérateurs de détecteurs d'objets (YOLO) par les ingestions FINN et hls4ml de QONNX : non documentée dans ce papier.

## Statut de lecture

Texte lu en entier tel que fourni par `fulltext.md`, mais il s'arrête en §VI-E (« It currently includes: » sans la liste des modèles du zoo) : la fin de l'article, dont la liste du model zoo, l'éventuelle conclusion et les références, est absente de l'extraction ; les figures 1 à 5 et le corps des Tables I et II ne sont lisibles qu'en légendes. Déduit et non affirmé par les auteurs : l'intérêt pour la traçabilité et la certification, la compatibilité avec les activations de YOLO, l'absence de garantie sur l'identité des arrondis entre outils.
