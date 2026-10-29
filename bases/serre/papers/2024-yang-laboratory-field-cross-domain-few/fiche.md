---
id: 2024-yang-laboratory-field-cross-domain-few
fiche: done
date: 2026-10-29
---

# From laboratory to field: cross-domain few-shot learning for crop disease identification in the field

Sen Yang, Quan Feng, Jianhua Zhang, Wanxia Yang, Wenwei Zhou, Wenbo Yan, 2024, Frontiers in Plant Science 15. https://doi.org/10.3389/fpls.2024.1434222
Type : article de journal (relu par les pairs)

## Problème

Les méthodes few-shot (FSL) pour les maladies des plantes utilisent des classes de base et des classes nouvelles du même jeu (souvent PlantVillage) ; leur performance chute sur des images de terrain (fond complexe, éclairage variable) (§1, `2024-yang#001.1`). Les auteurs étudient le few-shot inter-domaines (CD-FSL) : quel domaine source choisir, quelle diversité, pour reconnaître de nouvelles classes dans un domaine cible de terrain avec 1 ou 5 images par classe.

## Méthode

- Cible : jeu maison FCDD (Field Crop Disease Dataset), 9 cultures, 43 classes, images de terrain collectées (auto-constitué, internet, jeux publics) (§2.1, Table 1) ; non publié d'après le texte (aucun lien).
- Sources testées une à une : Cars, Leaves, CUB200, PlantVillage, Flower, Pest ; pré-entraînement sur MiniImageNet (§3.1, `2024-yang#012.0`).
- Trois modèles, backbone ResNet-18 + CBAM : CDFSL-BDC (ProtoNet + module Brownian distance covariance), CDFSL-MAML (ResNet-12+CBAM), CDFSL-NML (entraînement non épisodique).
- Similarité de domaine : cosinus et distance euclidienne entre moyennes de features source/cible (§2.4, Table 2).
- Évaluation : 600 tâches N-way K-shot tirées dans FCDD, 15 images de requête par classe, exactitude moyenne ; K = 1 et 5 seulement (§2.5, §3.1). Le support de chaque tâche, tiré de FCDD, sert à ré-ajuster le modèle (§2.2). Aucun point intermédiaire (K = 2, 10, 20) n'est testé.

## Plateforme et implémentation

Matériel GPU d'entraînement : n/r (aucune latence, aucun FPS, aucun déploiement edge ; vérifié par lecture complète). Hyperparamètres : batch 64, 400 époques de pré-entraînement, lr 5e-2 ; meta-train 60 époques, lr 1e-3 (§3.1). Code et données : non publiés (aucun lien dans le texte).

## Résultats

Exactitude moyenne sur tâches 5-way, test sur FCDD (terrain) ; source = domaine d'entraînement (§3.2).

| Source → FCDD | cos. | BDC 5-shot | NML 5-shot | MAML 5-shot | BDC 1-shot | NML 1-shot |
|---|---|---|---|---|---|---|
| Cars | 0,65 | 73,61 | 63,17 | 38,93 | 52,45 | 47,11 |
| PlantVillage | 0,85 | 77,42 | 75,81 | 54,16 | 62,46 | 58,27 |
| Pest | 0,93 | 80,13 | 83,61 | 59,94 | 63,95 | 66,82 |

(Tables 2, 3, 4 ; `2024-yang#033.0`, `#034.0`, `#035.0`.)

- Passer de 5 à 1 image par classe fait perdre 16 à 17 points sur Pest (§3.2, `2024-yang#013.1`).
- PlantVillage comme source est moins bon que Flower et Pest malgré une sémantique proche ; les auteurs l'attribuent au fond fixe de PlantVillage (hypothèse, non testée) (§3.2, `2024-yang#013.2`).
- Multi-domaine : source A = {Cars, Leaves, CUB200} gagne 8,95 / 5,58 / 2,38 points (NML, 5-shot) sur chaque source seule (§3.5, `2024-yang#017.1`).
- Taille de la source : l'exactitude plafonne au-delà de 64 classes sources ; de 16 à 64 classes : +8,33 (NML) et +13,12 points (BDC) en 5-shot (§4.1, `2024-yang#019.0`, `#019.1`).
- Par culture (Pest → culture, Table 6, `2024-yang#037.0`) : pomme de terre BDC 76,48 / NML 81,02 en 5-shot, tomate 56,54 / 59,38, pomme 53,63 / 57,47. Fond complexe et lésions petites = échec (§3.6).
- CBAM : +3,57 (Cars) et +1,79 (Pest) points pour BDC en 5-shot (Table 5).
→ reportés dans `benchmarks.csv` : lignes prêtes à coller renvoyées à l'agent principal (non écrites ici, périmètre).

## Limites et critique

- Le jeu cible FCDD est maison et non publié ; les classes de test diffèrent d'une tâche à l'autre (tâches 5-way tirées de 43 classes) : l'exactitude n'est pas celle d'un classifieur 43 classes, et n'est pas comparable à un rappel, une précision ou un F1 par classe.
- Pas de classe « sain vs malade » traitée comme détection, pas de faux positifs sur images saines, pas de calibration (ECE) : métrique unique, l'exactitude.
- Seulement K = 1 et K = 5 : pas de courbe « images de terrain par classe → gain » ; pas de comparaison avec un fine-tuning supervisé classique sur le même nombre d'images de terrain (la comparaison se fait contre ProtoNet, MAML, GNN+LFT, DeepEMD, Fig. 9, valeurs non tabulées).
- Le classement des sources (Pest > PlantVillage) est une corrélation à 6 points avec la similarité cosinus ; la cause « fond fixe » est une explication des auteurs (§3.2), non isolée par expérience. Aucune ablation « avec / sans fond remplacé ».
- Pas d'écart-type ni d'intervalle de confiance sur les 600 tâches rapportés dans les tableaux ; pas de graines multiples.
- Les auteurs notent eux-mêmes que le fond complexe reste le facteur dominant (§4.3, `2024-yang#021.0`) et proposent une détection de la zone malade, sans l'essayer.

## Pertinence pour la thèse

Papier du corpus SerreIA : écart labo → terrain (axes `disease-classif`, `domain-shift`). Il chiffre ce que vaut un tout petit nombre d'images de terrain (1 à 5 par classe) avec des modèles entraînés ailleurs, et montre que la source la plus proche du terrain (Pest, fond naturel) bat PlantVillage. Il laisse ouvert le passage à l'échelle réaliste (dizaines d'images), l'effet d'un remplacement de fond et le déploiement edge.

## Pour SerreIA

**Comparabilité.** Non comparable aux chiffres du projet : (1) test FCDD, jeu maison non publié, pas PlantDoc ; (2) test hors domaine par rapport à des sources variées, mais avec ré-ajustement sur 1 à 5 images de FCDD, alors que le classifieur de SerreIA (entraîné PlantVillage+CCMT) est évalué sans aucune image PlantDoc ; (3) exactitude sur tâches 5-way équilibrées, alors que SerreIA suit rappel 0,986, précision 0,679, spécificité 0,50, F1 0,264 et ECE sur un test binaire sain/anormal déséquilibré. Les 77,42 % (PlantVillage → FCDD, 5-shot BDC) ne se lisent ni comme une exactitude PlantDoc, ni comme une borne. À retenir : l'ordre de grandeur des gains, pas les valeurs.

**Ce que le projet peut reprendre.**
- Expérience « pente few-shot » sur les premières images de la serre : après annotation d'un petit lot, mesurer sur le reste de la serre (test jamais utilisé pour l'ajustement) la métrique du projet (spécificité à rappel fixé, F1 classe, ECE) avec 0, 1, 5, 10, 20 images par classe. Le papier ne donne que K = 1 et 5 : la courbe est à produire. Protocole à imiter : 600 tâches aléatoires, 15 requêtes par classe, moyenne (§2.5) ; ajouter l'écart-type, absent du papier. Branchement : `vision/eval/cross_domain_eval.py` (évaluation hors domaine), `vision/train/train_classifier.py` (ajustement de la tête), `vision/models/multihead.py`.
- Variante peu coûteuse pour la cible Hailo : prototypes de classe (moyennes de features du backbone, comme ProtoNet/BDC) calculés sur les images de la serre ; ne change pas le HEF INT8 si le calcul des prototypes et la distance restent sur le CPU du Pi. À tester d'abord hors ligne : c'est une déduction, pas un résultat du papier.
- Choix des données d'entraînement : la source dont le fond ressemble au terrain (Pest, fond naturel) donne +2,7 points (BDC) et +7,8 points (NML) en 5-shot par rapport à PlantVillage (Table 3) ; piste pour le jeu d'appoint de `vision/datasets/` : compléter PV+CCMT avec des images à fond naturel et de la diversité de classes (plafond autour de 64 classes sources, §4.1). Le papier ne teste pas CCMT.
- Remplacement de fond jamais testé dans SerreIA : le papier avance le fond fixe de PlantVillage pour expliquer son retard sur Pest (hypothèse non testée, §3.2 `2024-yang#013.2`). Argument pour faire l'ablation `data/backgrounds/` (avec/sans, test PlantDoc + images de la serre), à ajouter à `vision/datasets/augment.py`.
- Similarité de domaine (cosinus entre moyennes de features source/cible, §2.4) : indicateur à bas coût à calculer entre PV+CCMT, PlantDoc et les images de la serre, avec le backbone EfficientNet-B0 du projet, pour prévoir le décrochage avant de mesurer.
- Diagnostic par culture : tomate (56,54 % BDC 5-shot) et pomme sont les pires, fond complexe et lésions petites (Table 6, §3.6) ; la tomate est une culture visée par SerreIA, donc attendre un test de serre difficile et suivre la métrique par culture.
- Détecteur de feuilles avant classifieur : les auteurs le proposent (§4.3, `2024-yang#021.0`) mais ne le testent pas ; cela ne tranche pas les 42 % de faux positifs du pipeline en deux étages.

## Gaps identifiés

- Courbe « nombre d'images de terrain par classe → gain » avec K > 5 : absente de ce papier.
- Few-shot avec métriques de décision (spécificité, ECE) et classe « saine » : absent.
- Effet isolé du fond (remplacement, découpe) en cross-domain few-shot : hypothèse non testée.
- Déploiement edge (quantification INT8, Hailo) d'un classifieur à prototypes : non traité.

## Statut de lecture

Papier complet (fulltext.md lu en entier par tranches ; extraction GROBID ; Tables 2 à 6 lues dans le texte, Figures 9, 10, 13 non lisibles en valeurs, non exploitées). Déduit, non affirmé par les auteurs : la comparaison avec les chiffres de SerreIA, les propositions d'expériences (prototypes sur Pi, courbe K, ablation de fond), la lecture « fond fixe » comme cause (c'est une hypothèse des auteurs), la non-publication du code et des données (aucun lien trouvé dans le texte).
