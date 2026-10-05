---
id: arxiv-1405.0312-microsoft-coco-common-objects-context
fiche: done
date: 2026-10-05
---

# Microsoft COCO: Common Objects in Context

Tsung-Yi Lin, Michael Maire, Serge Belongie, Lubomir Bourdev, Ross Girshick, James Hays, Pietro Perona, Deva Ramanan, C. Lawrence Zitnick, Piotr Dollár, 2014, arXiv preprint. https://arxiv.org/abs/1405.0312
Type : preprint non relu par les pairs (version arXiv ; la version abrégée est citée comme [19], ECCV 2014 — déduit de la mention « An abridged version of this work appeared in [19] », §1, venue non vérifiée ici)

## Problème

Les datasets de détection d'alors (PASCAL VOC, ImageNet) sont dominés par des vues « iconiques » (un objet centré, vue canonique), avec peu d'instances par image. Les auteurs veulent un dataset pour trois verrous : objets en vue non iconique (occultés, en arrière-plan, dans le désordre), raisonnement contextuel entre objets, et localisation 2D précise (masques par instance). Il faut pour cela que **chaque instance de chaque catégorie soit étiquetée et segmentée** (§1).

## Méthode

**Choix des catégories (§3.1).** 91 catégories « thing » d'entrée de gamme (pas de « stuff », pas de parties d'objet). Candidats : catégories PASCAL VOC + 1200 mots visuels fréquents + objets nommés par des enfants de 4 à 8 ans → 272 candidats ; vote des co-auteurs (1 à 5) ; équilibre entre super-catégories ; catégories à moins de 5 000 instances écartées ; toutes les classes VOC conservées.

**Collecte d'images (§3.2).** Images Flickr ; requêtes par **paires de catégories** (« dog + car ») et par paires scène/objet (40 scènes SUN) plutôt que par catégorie seule, ce qui donne des images non iconiques. Au plus 5 photos par photographe et fenêtre temporelle courte. Repli : requête mono-catégorie puis filtrage explicite des images iconiques. Résultat : 328 000 images.

**Protocole d'annotation (§4, annexe I), sur Amazon Mechanical Turk.** Quatre étapes :

| Étape | Consigne | Redondance | Coût (heures de travail) |
|---|---|---|---|
| 1. Category labeling (§4.1) | 11 super-catégories présentées tour à tour (hiérarchie, évite 91 questions binaires) ; pour chaque catégorie présente, glisser l'icône sur UNE instance | 8 workers par image ; catégorie présente si un seul l'a cochée (rappel d'abord, faux positifs rattrapés plus loin) | ~20k h |
| 2. Instance spotting (§4.2) | placer une croix sur chaque instance de la catégorie ; au plus 10 instances par catégorie et par image ; position de l'étape 1 montrée (priming) ; loupe (x2 de résolution, annexe) pour les petits objets | 8 workers par image | ~10k h |
| 3. Instance segmentation (§4.3) | polygone par instance (interface OpenSurfaces de Bell et al.) ; zoom ; les segmentations déjà faites sont affichées ; on peut déclarer « aucune instance » (faux positif) ou « tout est segmenté » | 1 seul worker par instance ; test d'entraînement par catégorie obligatoire (~1 worker sur 3 le réussit) | > 22 h par 1 000 segmentations (§4.3) |
| 4. Vérification (§4.3, annexe) | grille de 64 segmentations, dont 4 mauvaises connues ; le worker doit repérer 3 des 4 pour valider sa tâche | 3 juges ; si l'un juge mauvais, 2 de plus ; rejet sans 4 votes favorables sur 5 → instance remise dans le pool | n/r séparément |

Total annoncé : « over 70,000 worker hours » (§8). Incohérence apparente : 20k + 10k + (2,5 M x 22 h / 1 000 = 55k, déduit) = 85k > 70k ; le papier ne la explique pas et ne chiffre pas la vérification.

**Cas des foules (§4.3, annexe).** Jusqu'à 10 instances d'une catégorie par image sont segmentées individuellement (jusqu'à 15 dans certaines images) ; au-delà, le reste est marqué « crowd » par un seul segment (éventuellement multi-parties, peint par le worker). Les zones « crowd » sont **ignorées à l'évaluation** (ne pénalisent pas le détecteur).

**Contrôle qualité.** (a) test d'entraînement qualifiant ; (b) vérification des masques par vote ; (c) rejet de tout le travail des workers jugés constamment mauvais ; (d) étape 1 : workers sous un seuil de précision rejetés (Fig. 4b). Analyse (§4.4, Fig. 4a) : l'union de 8 workers AMT a un rappel supérieur à chacun des 7 experts (co-auteurs) ; le rappel sature vers 9-10 workers ; estimation des auteurs : plus de 99 % des catégories présentes (non rejetées ensuite comme faux positifs) détectées avec 8 annotateurs ; borne théorique 0,5^8 ≈ 0,004 pour un cas non ambigu. Les experts eux-mêmes divergent souvent sur la présence d'une catégorie (ambiguïté de définition). Pas d'accord inter-annotateurs sur les masques (un seul worker par instance).

**Tailles small/medium/large.** **Non définies dans ce papier** : aucun seuil en pixels n'apparaît (les seuils 32²/96² des métriques COCO viennent du serveur d'évaluation, absent de cette version : « A full discussion of evaluation metrics will be added once the evaluation server is complete », §6). Seule la distribution des tailles d'instance est montrée (Fig. 5e, non extraite) avec la conclusion que les objets sont en moyenne plus petits dans COCO et SUN que dans ImageNet et PASCAL (§5).

## Plateforme et implémentation

Sans objet (dataset). Détecteur de base : DPM release 5, entraînement CPU, plateforme n/r. Dataset, API et site annoncés (« project website », §8, URL non reproduite dans le texte extrait) ; code de l'annotation : n/r (interface dérivée d'OpenSurfaces).

## Résultats

**Statistiques du dataset.**

| Grandeur | Valeur | Source |
|---|---|---|
| Images | 328 000 | Abstract, §3.2 |
| Instances étiquetées | 2 500 000 | Abstract, §1 |
| Catégories | 91 (dont 82 avec > 5 000 instances) ; 80 avec masques dans la release 2014 | §1, §6 |
| Instances par image | 7,7 (ImageNet 3,0 ; PASCAL 2,3 ; SUN > 17 objets+stuff) | §1, §5 |
| Catégories par image | 3,5 ; seulement 10 % des images n'ont qu'une catégorie (> 60 % pour ImageNet et PASCAL) | §5 |
| Release 2014 | 82 783 train / 40 504 val / 40 775 test ; ~270k personnes segmentées, 886k instances segmentées (train+val) | §6 / note de tableau |
| Release cumulée 2015 | 165 482 train / 81 208 val / 81 434 test | note de figure |
| 11 catégories sans masques en 2014 | hat, shoe, eyeglasses (trop d'instances) ; mirror, window, door, street sign (ambigus) ; plate, desk (confusion avec bowl / dining table) ; blender, hair brush (trop peu d'instances) | §6 |

Split : suppression des quasi-doublons entre splits et regroupement par photographe et par date (§6). Annotations train/val publiées, pas test.

**Baseline DPM (§7, Table 1).** Sous-ensemble de 55 000 images, boîtes déduites des masques, split préliminaire. DPMv5-P (entraîné sur VOC 2012) : 29,6 AP moyen sur VOC, 16,9 sur COCO ; DPMv5-C (entraîné sur COCO, 5 000 images positives + 10 000 négatives) : 26,8 sur VOC, 19,1 sur COCO. Écart de généralisation : 12,7 AP (P) contre 7,7 AP (C) (§7). Les performances moyennes sur COCO chutent presque d'un facteur 2 par rapport à VOC pour DPMv5-P (§7) : COCO est plus dur. Baseline de segmentation par projection de masques DPM (Fig. 9, chiffres non extraits).
→ reportés dans `benchmarks.csv` : 3 lignes proposées (DPMv5-C sur VOC, DPMv5-P et DPMv5-C sur COCO), moyenne des 20 catégories, Table 1.

## Limites et critique

- La version arXiv est une version préliminaire : serveur d'évaluation, métriques AP (seuils IoU, tailles S/M/L) et baselines sur le vrai split test « seront ajoutés » (§6, §7). Les chiffres DPM viennent d'un split préliminaire de 55k images : non comparables aux résultats COCO ultérieurs.
- Le coût d'annotation est donné en heures de travail, pas en euros, et la vérification n'est pas chiffrée ; la qualité des **masques** n'est mesurée que par vote de vérification, sans accord inter-annotateurs ni comparaison à un expert (seule l'étape 1 est évaluée contre des experts, Fig. 4).
- Les boîtes sont **déduites des masques** (« tight-fitting », §7) : pas d'annotation de boîte directe, donc pas de variabilité de boîte annotée à la main ; pour des boîtes YOLO, le protocole COCO n'est pas transposable tel quel (étape 3 la plus chère).
- Rappel maximisé par union de 8 workers : fait monter le rappel, mais les ambiguïtés de définition de classe restent (désaccord des experts, §4.4). Cela annonce les erreurs de labels relevées plus tard dans COCO (non traitées ici).
- Conclusion « COCO plus dur que VOC » inférée d'une baseline unique (DPM) : l'effet du modèle et celui des données sont confondus.
- Dataset en CC non précisé dans le texte ; licence des images Flickr : n/r.

## Pertinence pour la thèse

Pour CONSTRUIRE : recette de référence d'un dataset de détection « dans le contexte » : collecte par requêtes en paires pour obtenir des images non iconiques, 5 images max par photographe, déduplication et split par photographe/date (évite les fuites train/test), au moins ~5 000 instances par catégorie retenue (critère d'inclusion de classe, §3.1), 7,7 instances/image comme repère de densité. À appliquer pour tout dataset généraliste ou si le dataset cible doit contenir des scènes encombrées.
Pour ANNOTER : pipeline en étapes décomposées (présence par super-catégorie, puis localisation, puis masque, puis vérification) qui réduit le coût ; ordres de grandeur de coût : ~20k h (catégories) + ~10k h (instances) + > 22 h / 1 000 masques pour 2,5 M d'instances, soit environ 0,022 h (~80 s) par masque (déduit du chiffre du §4.3) ; redondance 8x pour le rappel ; test qualifiant, vérification par vote (4/5), crowd après 10-15 instances. Consigne YOLO transférable : annoter toutes les instances, marquer les foules à part (dans le format Ultralytics, `iscrowd` n'existe pas : à ignorer ou à découper), loupe/zoom pour les petits objets. À appliquer pour un budget d'annotation important ou si l'on pilote des annotateurs externes ; pour un petit dataset en interne, la partie « test qualifiant + vérification par échantillon » suffit.
Pour PRÉTRAITER : peu (aucune résolution d'entrée) ; seul enseignement : les objets COCO sont petits (Fig. 5e) : motive tiling/haute résolution. Pour AUGMENTER : rien.
Laisse ouvert : définition des seuils small/medium/large (hors de cette version), bruit réel des labels COCO, annotation de boîtes directes (extreme clicking), pré-annotation automatique.

## Gaps identifiés

- Seuils S/M/L de COCO (32²/96² px) absents de cette version : à retrouver dans la documentation de l'évaluation ou un autre papier avant de les citer.
- Coût d'une boîte directe vs. d'un masque, et qualité/bruit des labels COCO (à croiser avec un papier sur les erreurs de labels).
- Pas de mesure d'accord inter-annotateurs sur les masques ni sur les boîtes.

## Statut de lecture

papier complet (`fulltext.md`, backend grobid, extraction ok). Tableaux 2 et 3 sans corps extrait (listes de 272 catégories et 40 scènes de l'annexe, non nécessaires ici) ; Fig. 4 et 5 sans valeurs extraites (rappel/précision par nombre de workers, distribution des tailles).
Ce qui suit est déduit et non affirmé par les auteurs : coût moyen par masque (~0,022 h, calculé de « 22 h per 1,000 segmentations »), venue de la version abrégée (ECCV 2014, citation [19] non résolue ici), ordre des lignes de Table 1 (haut = VOC, bas = COCO, d'après la légende), le fait que l'AP de Table 1 soit un AP à IoU 0,5 (n/r dans le texte).
