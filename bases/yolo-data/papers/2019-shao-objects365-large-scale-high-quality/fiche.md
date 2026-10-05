---
id: 2019-shao-objects365-large-scale-high-quality
fiche: done
date: 2026-10-05
---

# Objects365: A Large-Scale, High-Quality Dataset for Object Detection

Shuai Shao, Zeming Li, Tianyuan Zhang, Chao Peng, Gang Yu, Xiangyu Zhang, Jing Li, Jian Sun, 2019, IEEE/CVF International Conference on Computer Vision (ICCV) 8430-8439. https://doi.org/10.1109/ICCV.2019.00852
Type : conférence

## Problème

Les jeux de référence (VOC, COCO) sont petits (80 classes, 7,3 boîtes/image pour COCO, Table 1) et le pré-entraînement ImageNet est peu sensible à la localisation : seul le backbone est pré-entraîné, la tête est initialisée au hasard (§1). Les auteurs veulent un jeu de détection pleinement annoté, plus grand (échelle), plus propre (qualité) et utile comme jeu de pré-entraînement (généralisation).

## Méthode

C'est un papier de constitution de dataset, pas de modèle.

**Données et catégories (§3.1).** Images surtout issues de Flickr, licences compatibles recherche. 11 super-catégories (humain et accessoires, salon, vêtements, cuisine, instruments, transport, salle de bain, électronique, nourriture/légumes, fournitures de bureau, animaux), puis 442 catégories candidates « de la vie quotidienne » ; les 442 sont annotées sur les 100K premières images, puis les 365 plus fréquentes sont gardées. Les catégories de VOC et COCO sont incluses (compatibilité). Filtrage des images « iconiques » (un seul objet centré), comme dans COCO.

**Pipeline d'annotation en 3 étapes (§3.2.1, Fig. 2).** (1) classification binaire : image non iconique et contenant au moins un objet d'une des 11 super-catégories, sinon rejetée ; (2) étiquetage image-niveau avec les super-catégories (plusieurs possibles) ; (3) un annotateur par super-catégorie dessine toutes les boîtes de cette super-catégorie avec le nom de l'objet. Raison : aucun annotateur ne peut retenir 365 classes ; chacun ne maîtrise qu'une super-catégorie, ce qui améliore efficacité et qualité.

**Équipe et contrôle qualité (§3.2.2).** Annotateurs (prestataires, formation + examen d'entrée, une seule tâche chacun), inspecteurs (relisent 100 % des images ; une image fautive retourne au même annotateur), examinateurs (géographiquement isolés, relisent des lots d'environ 100 images ; une seule erreur rejette tout le lot). Le taux de rejet des lots entre dans la rémunération des annotateurs et inspecteurs.

**Consignes de cohérence (§3.2.3).** Règle de classification « function-first » pour les cas ambigus (objet = « tap » plutôt que « teapot », « toy » plutôt que « bear », Fig. 3). Règle de boîte : couvrir la plus grande boîte qui ne crée pas d'ambiguïté de catégorie (inclure la décoration de l'horloge, mais pas le décor qui ferait dire « tower », Fig. 4).

**Coût.** Temps, coût monétaire et nombre d'annotateurs : n/r.

## Plateforme et implémentation

Pas de matériel embarqué. Entraînement : 8 GPU GTX 1080 Ti, batch 16, entrée 800×1333, Detectron, SyncBN (§4.1). Dataset et modèles pré-entraînés publiés (www.objects365.org, résumé). Code d'entraînement : n/r.

## Résultats

**Statistiques (Table 1, 2, §3.3).** 638K images (train+val), 10 101K boîtes, 365 classes, 15,8 boîtes/image (COCO : 123K, 896K, 80, 7,3 ; Table 1). Split : 600K train / 38K val / 100K test, 9 623K / 479K / 1 700K boîtes (Table 2, tableau à vérifier). Environ 740K images annotées au total (§3.3). Restreint aux 80 classes COCO : 9,04 boîtes/image contre 7,34, et 3,16 catégories/image contre 2,92 ; surface annotée 63 % contre 57 % (COCO) et 53 % (VOC) (§3.3).

**Qualité mesurée (§3.4, Table 3).** 3 annotateurs experts relabellisent 200 images (3250 boîtes après raffinement) : rappel d'annotation 92 % (COCO 83, OpenImages 43) ; précision 91,7 % contre 71,9 % pour COCO (faux positif = mauvaise classe ou boîte imprécise). Échantillon de 200 images, un seul passage : indicatif.

**Difficulté (§4.2).** FPN-R50 : 22,5 mmAP sur Objects365 (COCO : 38,3) ; restreint aux 80 classes COCO : 38,5 (FPN), 34,5 (RetinaNet). L'écart vient du rappel (nombreux faux négatifs : petits objets, classes rares) ; certaines classes (radish, saw) n'ont aucun positif (Fig. 8, 9).

**Effet du pré-entraînement sur Objects365 (§4.3), FPN-R50, mmAP COCO.**

| Pré-entraînement | Itérations COCO | mmAP | Source |
|---|---|---|---|
| ImageNet (backbone) | 90K / 180K / 540K | 36,4 / 38,3 / 39,3 | Table 11 |
| Objects365 (backbone seul) | 90K / 180K / 540K | 37,8 / 39,4 / 40,3 | Table 11 |
| Objects365, lr standard 0,02 | 180K | 40,4 | Table 5 |
| Objects365 backbone + tête, lr 0,003 | 90K | 42,0 | Table 5, 11 |
| Objects365 sans les 80 classes COCO | n/r | 39,6 | §4.3.2 (corps Table 6 manquant) |
| Objects365 sans pré-entraînement de la tête | n/r | 39,4 (vs 42,0) | §4.3.5 |

- Gain de +5,6 points sur 90K itérations (42,0 contre 36,4) ; +2,7 contre ImageNet 540K (42,0 contre 39,3) (résumé, §4.3.1).
- Le gain tient à trois facteurs : plus de catégories (meilleure classification), pré-entraînement de la tête (−2,6 points si elle est réinitialisée, §4.3.5), et un lr adapté : les poids Objects365 ont une norme L2 plus faible (0,85 contre 5,67), lr = 0,15 × 0,02 = 3e-3 ; le lr standard ne donne que 40,4 (Table 5).
- Vitesse : 12K itérations COCO depuis Objects365 égalent 540K depuis ImageNet (« 10-20 fois plus rapide », §4.3.3 ; Table de la section, corps non extrait).
- RetinaNet : 39,5 contre 37 à 180K (+2,5) ; un pré-entraînement ImageNet avant Objects365 ajoute +0,3 (FPN) et +1,5 (RetinaNet) (§4.3.2).
- VOC (détection) : 86,2 contre 80,2 (ImageNet) et 85,1 (COCO 540K) (§4.3.2, Table 7 sans corps).
- CityPersons, MR (plus bas = mieux) : 12,12 (Objects365) contre 18,04 (ImageNet), 16,24 (ImageNet→COCO 540K), 16,78 (OpenImages), 39,49 (aucun) (Table 8).
- Segmentation (PSPNet-R50) : VOC 76,7 contre 74,5 (ImageNet) ; ADE 42,9 contre 41,2 (ImageNet) (§4.3.2).

**Gain selon la taille du jeu cible.** Le papier ne varie pas la taille du jeu cible. Le gain le plus grand est sur VOC (11,5K images, +6 points) et CityPersons (−6 points de MR), puis COCO (123K, +5,6 à budget égal), puis ADE (~20K images mais segmentation, +1,7) : les petits jeux détection bénéficient le plus, mais la comparaison mêle tâches et métriques. Déduit, non affirmé.

→ reportés dans `benchmarks.csv` : 10 lignes proposées (fichier `.cache/bench/2019-shao-objects365-large-scale-high-quality.csv`), ajoutées par l'agent principal.

## Limites et critique

- Un seul backbone (ResNet-50), deux détecteurs (FPN, RetinaNet), jamais de détecteur type YOLO ni de petit modèle ; gain non établi pour des modèles compacts (le papier prévoit d'essayer de plus gros).
- Comparaison de pré-entraînement à budget d'itérations très différent (90K contre 540K) et avec un lr réglé pour Objects365 seulement ; l'écart avec lr standard n'est que de +1,1 (40,4 contre 39,3). Le lr d'ImageNet n'est pas réajusté en retour.
- Pré-entraîner la tête (Objects365) contre le backbone seul (ImageNet) mélange deux effets ; la décomposition partielle est en Table 11 et 12.
- Qualité : 200 images, annotateurs experts du même projet, métriques définies par les auteurs ; la précision de COCO (71,9 %) dépend de leur propre critère de boîte « précise ». Le rappel faible (diagnostic Fig. 8) montre qu'il manque tout de même beaucoup de boîtes.
- Coût d'annotation, accord inter-annotateurs chiffré, nombre d'annotateurs : n/r.
- Tailles d'objets et distribution par classe (longue traîne) : non détaillées dans le texte extrait.
- Tables 7, 9, 10, 12 et plusieurs lignes de Table 6 sans corps extrait : certains chiffres viennent du texte seul.

## Pertinence pour le thème (données de détection)

- **CONSTRUIRE** : modèle de pipeline pour un jeu à nombreuses classes : définir 11 super-catégories, annoter un échantillon (100K images) pour mesurer la fréquence de 442 candidates et ne garder que les 365 fréquentes ; inclure les classes des benchmarks standards pour la compatibilité ; filtrer les images iconiques. Applicable quand le nombre de classes dépasse ce qu'un annotateur retient.
- **ANNOTER** : découpage en tâches par super-catégorie (une personne = un domaine de classes), rôles annotateur / inspecteur / examinateur, rejet d'un lot de ~100 images à la première erreur, rémunération liée au taux de rejet ; deux règles écrites (function-first pour la classe, « plus grande boîte non ambiguë » pour le cadre). Applicable dès qu'une équipe, même petite, annote avec plusieurs personnes ; la règle de boîte se transpose directement aux consignes d'un label YOLO. Les chiffres rappel/précision donnent un ordre de grandeur de contrôle qualité (échantillon relabellisé par des experts).
- **PRÉTRAITER** : n/r (entrée 800×1333 en entraînement et test, §4.1).
- **AUGMENTER** : sans objet direct ; le pré-entraînement sur un grand jeu remplace une partie du besoin en données.
- **Transfert** : quand utiliser Objects365 : jeu cible petit ou domaine éloigné d'ImageNet, besoin de converger vite, détecteur de grande taille ; adapter le lr à la norme des poids du pré-entraînement. Pour un YOLO Ultralytics, les poids Objects365 existent mais ne sont pas évalués ici : à vérifier avant de généraliser (déduit).

## Gaps identifiés

- Effet du pré-entraînement Objects365 selon la taille du jeu cible (courbe 1K à 100K images) : non mesuré.
- Transfert vers détecteurs compacts type YOLO / modèles embarqués : non mesuré.
- Coût réel d'annotation (heures, euros par boîte) et accord inter-annotateurs : n/r.
- Qualité de labels en fonction du nombre de passes de contrôle : non étudié.

## Statut de lecture

Papier complet (`fulltext.md`, extraction GROBID ; tables 2, 3, 6 reconstruites par PyMuPDF à vérifier ; tables 7, 9, 10, 12 sans corps, valeurs reprises du texte).
Ce qui suit est déduit et non affirmé par les auteurs : l'effet du gain selon la taille du jeu cible (comparaison croisée VOC / CityPersons / COCO) ; la transposition de la règle de boîte aux labels YOLO ; l'applicabilité aux modèles YOLO.
