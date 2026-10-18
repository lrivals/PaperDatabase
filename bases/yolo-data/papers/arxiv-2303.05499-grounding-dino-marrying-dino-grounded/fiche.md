---
id: arxiv-2303.05499-grounding-dino-marrying-dino-grounded
fiche: done
date: 2026-10-18
---

# Grounding DINO: Marrying DINO with Grounded Pre-Training for Open-Set Object Detection

Shilong Liu, Zhaoyang Zeng, Tianhe Ren, Feng Li, Hao Zhang, Jie Yang, Qing Jiang, Chunyuan Li, Jianwei Yang, Hang Su, Jun Zhu, Lei Zhang, 2023, arXiv preprint. https://arxiv.org/abs/2303.05499
Type : preprint non relu par les pairs

## Problème

Détecter des objets arbitraires désignés par du texte (« open-set detection » : noms de catégories ou expressions référentielles), sans liste de classes figée. Les auteurs estiment que les détecteurs open-set antérieurs ne fusionnent langage et vision qu'à une phase (neck pour GLIP, entrée du décodeur pour OV-DETR) (§1).

## Méthode

Architecture résumée (la base ne s'y intéresse que comme outil de pré-annotation) : détecteur DINO (DETR) étendu avec un texte BERT-base ; image (Swin-T ou Swin-L) + texte passent par un « feature enhancer » (attention croisée image-texte), 900 requêtes choisies par similarité avec le texte, décodeur à attention croisée sur les deux modalités (§3, §4.1). Entrée texte = noms de classes concaténés séparés par « . », ex. « cat . person . mouse . » (§3). Les masques d'attention « sub-sentence » évitent que les noms de classes interagissent (§3.4). Perte : L1 + GIoU + contraste région-mot (focal) (§3.5).
Données de pré-entraînement (Annexe B) : détection reformulée en grounding (COCO, Objects365 [O365], OpenImages), grounding (GoldG = Flickr30k Entities + Visual Genome, RefCOCO/+/g), légendes pseudo-annotées (Cap4M, annotées par GLIP-T pour la variante T, GLIP-L pour la variante L). O365v1 (~600K images) pour la variante T, O365v2 (~1,7M) pour la variante L.

## Plateforme et implémentation

Entraînement : T sur 16 V100 (batch 32), L sur 64 A100 (batch 64) (§4.1). Tailles de modèle : T 172M paramètres, L 341M (Table 4). Vitesse d'inférence : Table 20 (efficacité vs GLIP) sans corps extrait, n/r ici. Code et checkpoints publiés : https://github.com/IDEA-Research/GroundingDINO (résumé). Pas de mesure de puissance.

## Résultats

Zero-shot, sans image du jeu cible à l'entraînement ; Table 2 (COCO) sans corps extrait, chiffres repris du texte et de la Table 6.

| Jeu | Modèle (données) | AP | Source |
|---|---|---|---|
| COCO minival zero-shot | T (O365+GoldG) | 48.1 | Table 6, §4.2 |
| COCO zero-shot | L | 52.5 | §4.2, résumé |
| COCO fine-tuné | T / L | 57.1 / 62.6 (63.0 test-dev) | Table 6, §4.2 |
| LVIS minival zero-shot | T (O365+GoldG) | 25.6 (APr 14.4 / APc 19.6 / APf 32.2) | Table 3 |
| LVIS minival zero-shot | T (+Cap4M) | 27.4 (18.1 / 23.3 / 32.7) | Table 3 |
| LVIS minival zero-shot | L | 33.9 (22.2 / 30.7 / 38.8) | Table 3 |
| LVIS fine-tuné | T | 52.1 (35.4 / 51.3 / 55.7) | Table 3 |
| ODinW (35 jeux) zero-shot, AP moyen / médian | T (O365+GoldG) | 20.0 / 9.5 | Table 4 |
| id. | T (+Cap4M) | 22.3 / 11.9 | Table 4 |
| id. | L | 26.1 / 18.4 | Table 4 |
| ODinW few-shot (nombre d'exemples n/r) | T | 46.4 / 51.1 | Table 4 |
| ODinW full-shot | T | 70.7 / 76.2 | Table 4 |

Points utiles pour la pré-annotation :
- **Classes fréquentes vs rares (LVIS).** Pour T (O365+GoldG) : APf 32.2 contre APr 14.4, soit 17.8 points d'écart (Table 3). Les auteurs notent que Grounding DINO fait mieux que GLIP sur les classes communes mais moins bien sur les rares (GLIP-T (C) : APr 17.7), et jugent que c'est peut-être une limite des architectures DETR (§4.2). Le grand modèle L garde l'écart (APr 22.2 contre APf 38.8).
- **Effet des données.** Les légendes pseudo-annotées Cap4M apportent +1.8 AP LVIS (25.6 -> 27.4) contre +1.1 pour GLIP (§4.2) et +2.3 AP moyen ODinW (20.0 -> 22.3) (Table 4). Les données de grounding aident COCO zero-shot (48.1 contre 46.7 sans, §4.2). Ajouter RefCOCO/+/g fait baisser LVIS (25.6 -> 21.9) et ODinW (20.0 -> 17.7) ; ajouter COCO fait passer COCO zero-shot de 48.5 à 56.1 (Table 6, qui n'est plus alors du zero-shot).
- **Fine-tuning.** Sur ODinW, T passe de 20.0 (zero-shot) à 46.4 (few-shot) puis 70.7 (full-shot), au-dessus de DINO-Swin-T (41.2 puis 66.7) (Table 4). Sur LVIS, le fine-tuning fait passer APr de 14.4 à 35.4 (Table 3). Le nombre d'exemples du few-shot n'est pas donné dans le texte lu (n/r).
- **Hétérogénéité par domaine (ODinW).** Écart d'un domaine à l'autre : AP moyen 22.3 mais médian 11.9 pour T avec Cap4M (Table 4). Tables détaillées par jeu (légendes Tables 12-13, associées par ordre de lecture aux données qui les suivent ; à vérifier) : PascalVOC 47.21 puis 66.01 d'AP avec Cap4M, MaskWearing 0.58 puis 1.64, PKLot_640 0.08 puis 0.25, HardHatWorkers 2.39 puis 9.14, plantdoc 0.34 puis 2.02. AerialMaritimeDrone_large 9.48 puis 12.64 (aérien, petits objets, APS souvent faible). Le texte cite PlantDoc à 0.36 contre 1.1 pour GLIP (§C.8) : léger écart avec 0.34.
- **Pseudo-étiquettes comme données.** Un essai avec ImageNet pseudo-annoté par Detic (IN22K-LVIS-1M, ~1M images) donne de bons résultats sur LVIS, mais l'annotateur Detic a vu LVIS, donc pas de vrai zero-shot (§C.7, chiffres de la Table 17 non extraits).
- **Ablations (Table 7, T, O365).** Sans fusion de l'encodeur : COCO zero-shot 45.8 contre 46.7, LVIS 13.1 contre 16.1 ; texte sub-sentence contre word-level : LVIS 16.1 contre 15.6.
- **Plus de requêtes (§C.5, Table 15).** 900 -> 1500 : APr LVIS 9.4 -> 9.2, APf 28.4 -> 29.0 ; l'effet est marginal (O365, T).
- Lignes ajoutées à `benchmarks.csv` (proposées à l'agent principal, 15 lignes) : COCO zero-shot T et L, COCO fine-tune T et L, LVIS zero-shot T, T+Cap4M, L (+ APr et APf de T), LVIS fine-tune T, ODinW zero-shot T, T+Cap4M, L, ODinW few-shot et full-shot T.

## Limites et critique

Dits par les auteurs : pas de segmentation ; moins de données que le plus gros GLIP ; faux positifs (« hallucinations ») dans certains cas (Conclusion, Limitations) ; sur les expressions référentielles, très mauvais sans données RefC (50.41 de précision RefCOCO val pour T sans RefC, Table 5).
Déduit (à signaler comme tel) :
- La sortie est une boîte plus une phrase avec un score, sans garantie d'exhaustivité ni de calibration ; aucune mesure de précision/rappel des boîtes à un seuil de confiance utilisable pour des labels. Le papier rapporte des AP, pas la qualité des boîtes pour l'entraînement d'un autre détecteur.
- Les chiffres de classes fréquentes (LVIS APf 32.2 pour T, 38.8 pour L) restent loin de ce qu'on exige d'un label manuel ; les classes rares (14.4 d'AP pour T) ne sont pas pré-annotables de façon fiable : pré-annotation à relire de façon systématique.
- Le « zero-shot » sur COCO est large : O365 couvre presque toutes les catégories COCO (§4.2) et la variante L est pré-entraînée avec COCO pour le tableau LVIS (Table 3), ce qui rend la comparaison de 52.5 AP à vérifier (Table 2 sans corps extrait). Les chiffres ODinW sur des domaines éloignés (médecine, texture, jeux de cartes, PKLot) sont proches de 0, donc l'outil échoue sur des domaines spécifiques (jeux de domaine, aérien) sans fine-tuning.
- Seuils d'AP sur l'écart petits/grands objets : non traités dans le texte ; les tables détaillées par jeu (APS à 0 sur plusieurs jeux, -1 quand absent) suggèrent des faiblesses sur les petits objets, à confirmer.
- Preprint, jamais relu dans cette version ; code publié, mais les données de pré-entraînement (Cap4M) dépendent d'annotations produites par GLIP (circularité des biais).
- Le texte indique qu'une fuite de données est possible pour RefC/COCO (Table 5, note).

## Pertinence pour la thèse

Axe `auto-labelling`. Ce qu'il apprend pour CONSTRUIRE/ANNOTER un dataset de détection : un invite texte (« person . car . ») suffit à produire des boîtes candidates sans aucune donnée, avec une qualité correcte sur les classes communes d'un domaine proche d'O365/COCO (zero-shot COCO 48.1 pour T, LVIS APf 32.2), faible sur les classes rares (APr 14.4) et variable selon les domaines (ODinW, AP médian 11.9 pour T+Cap4M). À appliquer : pré-annoter des classes communes avant correction humaine, avec relecture ; pour une nouvelle classe rare ou un domaine spécifique, ne pas compter sur le zero-shot, mais fine-tuner : quelques exemples font passer l'AP moyen ODinW de 20.0 à 46.4 (few-shot) puis 70.7 (full-shot). Ne pas utiliser les boîtes brutes comme vérité sans filtrage. Pour PRÉTRAITER/AUGMENTER : rien de direct ; la leçon est l'effet des données de pré-entraînement (grounding et légendes pseudo-annotées) sur le zero-shot. Les sorties servent ensuite à entraîner un YOLO (distillation de pseudo-labels, déduit, non testé dans le papier).

## Gaps identifiés

- Qualité des boîtes Grounding DINO utilisées comme pseudo-labels pour entraîner un détecteur de type YOLO (précision/rappel, seuils de confiance) : non mesurée ici.
- Comportement sur petits objets et images aériennes/haute résolution (VisDrone-like) : non traité, indications indirectes seulement (tables par jeu).
- Combien d'exemples annotés pour passer du zero-shot au few-shot utile : nombre d'exemples du few-shot ODinW non extrait.

## Statut de lecture

papier complet (`fulltext.md`, extraction grobid ok). Tables 2, 8, 9, 10, 15, 20 sans corps extrait (voir `extraction.warnings`) : Table 2 (COCO) lue via le texte et la Table 6 ; Table 20 (efficacité) et Table 17 (Detic) non lues, donc non chiffrées ici ; Tables 8 et 15 : hyperparamètres et requêtes lus dans les blocs de données voisins. Les légendes des Tables 12-14 sont décalées par rapport à leurs données dans l'extraction : les valeurs par jeu ODinW sont à vérifier.
Déduit et non affirmé par les auteurs : la pertinence pour la pré-annotation, l'ordre de grandeur « à relire » pour les classes rares, l'impact sur les petits objets, la distillation vers un YOLO, la circularité des biais Cap4M/GLIP.
