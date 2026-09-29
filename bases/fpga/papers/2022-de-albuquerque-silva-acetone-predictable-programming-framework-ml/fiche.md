---
id: 2022-de-albuquerque-silva-acetone-predictable-programming-framework-ml
fiche: done
date: 2026-09-29
benchmarks: none
---

# ACETONE: Predictable Programming Framework for ML Applications in Safety-Critical Systems

Iryna De Albuquerque Silva, Thomas Carle, Adrien Gauffriau, Claire Pagetti, 2022, 34th Euromicro Conference on Real-Time Systems (ECRTS 2022), LIPIcs 231. https://doi.org/10.4230/LIPIcs.ECRTS.2022.3
Type : conférence (relue par les pairs)

## Problème

Il n'existe pas de processus de développement accepté pour embarquer du ML avec les niveaux de confiance de la sûreté classique (aéronautique, DO-178C). Les exigences visées : traçabilité exigences-code, calcul du WCET, tests exhaustifs (couverture des branches) (§1). Les runtimes ML usuels (TensorFlow, graph executors) interprètent un graphe avec allocation dynamique, non analysable.

## Méthode

ACETONE (Avionics C code generator for Neural NEtworks) : un prototype Python génère du code C séquentiel à partir de la description JSON (version dégradée de NNEF) d'un réseau feed-forward entraîné hors ligne (MLP et CNN : dense, convolution, pooling, batch norm, flatten, activations ReLU/tanh/sigmoid/linéaire) (§2.3, §3.1). Allocation statique, ordonnancement statique, compilation en -O0. Sémantique des couches formalisée (§2.1) et transformations préservant la sémantique (fusion batch norm/convolution, ReLU après max pooling ; §2.2). Trois variantes de code (§3.2-3.4) : V1 fonction d'inférence générique par pointeurs de fonctions ; V2 inlinée (bornes de boucle codées en dur) ; V3 entièrement déroulée. Évaluation : benchmarks ACAS-Xu (5 MLP FP32), LeNet-5, CifarNet, AlexNet (et VGG-16 pour la préservation sémantique seulement), comparaison à Keras2c et uTVM avec runtime C statique (§4-5). Critères : préservation sémantique (erreur max sur 1000 tests, x86), temps mesuré (Cortex-A15 du Keystone TI, moyenne de 50 exécutions, -O0) et WCET par OTAWA (cible lpc2138), layout mémoire.

## Plateforme et implémentation

Pas de FPGA : cibles CPU (ARM Cortex-A15 du TI Keystone pour la mesure ; lpc2138 pour OTAWA, non représentative du A15, §4.2). Un seul cœur, FP32. Puissance : sans objet. Code : prototype Python annoncé ; lien de publication n/r dans le texte extrait (les auteurs disent seulement qu'OTAWA est open source).

## Résultats

- Préservation sémantique : erreurs de l'ordre de 1e-6 pour tous les frameworks en FP32 (§5, Table 1 dont le corps est absent du texte).
- WCET : la forme du code C détermine la précision de la borne ; V1 et Keras2c (pointeurs de fonctions) sont pessimistes (OTAWA suppose que chaque appel est la couche la plus coûteuse), V2 et uTVM statique donnent des bornes plus serrées ; OTAWA échoue par manque de mémoire sur V3, AlexNet et VGG-16 (§5).
- Mémoire (Table 5, ACAS-Xu reg50) : stack 240 o / .text 17 004 o (V1), 158 / 18 556 (V2), V3 .text 1 603 980 o ; Keras2c : stack 129 280 o, .text 12 744 060 o ; uTVM statique .text 12 688 208 o.
- Performances « comparables et parfois légèrement meilleures » que les deux autres cadres (§1) ; les Tables 1 à 4 (erreurs, MET, WCET) n'ont pas de corps dans `fulltext.md`, donc aucun chiffre de temps n'est reporté ici.
→ reportés dans `benchmarks.csv` : aucune ligne. Pas de plateforme FPGA, et les chiffres de temps sont absents du texte extrait ; `benchmarks: none`.

## Limites et critique

- Restreint au feed-forward FP32, monocœur, sans parallélisme ni accélérateur ; pas de quantification, pas de détection d'objets (YOLO) : les benchmarks (ACAS-Xu, LeNet-5, CifarNet, AlexNet) sont loin d'un détecteur moderne.
- La préservation sémantique est validée par tests et revue de code, non prouvée formellement (assumé par les auteurs, §4.2, en citant DO-178C).
- WCET calculé sur lpc2138 (non représentatif du A15 mesuré) : les bornes ne sont pas des WCET de la cible réelle ; -O0 impose un coût de performance.
- V3 non analysable pour les grands réseaux (taille du .text de 1,6 Mo dès un MLP de 50 neurones par couche).
- Pas de couverture de code structurelle (MC/DC) ni de qualification de l'outil de génération ; traçabilité affirmée qualitativement.
- Le lien avec le FPGA est indirect : les cibles certifiables visées sont des multicœurs COTS.

## Pertinence pour la thèse

Axe `safety-certification`. Fournit un exemple concret de chaîne « modèle entraîné vers code C » alignée sur DO-178C : sémantique formalisée, allocation statique, traçabilité, WCET par analyse statique, et compare des générateurs. Pour la thèse FPGA, elle documente les exigences à transposer à un flux HLS/RTL : équivalence sémantique modèle/implémentation, prédictibilité temporelle, code lisible et traçable (déduit : le flux HLS de type SMOF/hls4ml ne fournit rien de tel). Reste ouvert : l'équivalent sur FPGA (WCET remplacé par latence déterministe du dataflow), CNN de détection, quantification.

## Gaps identifiés

- Génération de code prédictible et traçable pour accélérateurs FPGA (équivalent d'ACETONE pour HLS/RTL).
- Préservation sémantique quantifiée (INT8) d'un détecteur type YOLO, et sa vérification formelle.
- Analyse de WCET/déterminisme sur cibles GPU/FPGA (ACETONE se limite au CPU).

## Statut de lecture

papier complet (fulltext.md lu en entier). Les Tables 1 à 4 (préservation sémantique, temps mesurés, WCET) ne sont pas présentes dans le texte extrait ; seule la Table 5 l'est. Déduit et non affirmé par les auteurs : la portée de la comparaison avec le FPGA, l'absence de qualification de l'outil (le texte ne l'évoque pas), le statut de publication du code.
