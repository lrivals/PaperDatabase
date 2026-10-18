---
id: arxiv-2309.11069-dynamic-tiling-model-agnostic-adaptive
fiche: done
date: 2026-10-18
---

# Dynamic Tiling: A Model-Agnostic, Adaptive, Scalable, and Inference-Data-Centric Approach for Efficient and Accurate Small Object Detection

Son The Nguyen, Theja Tulabandhula, Duy Nguyen, 2023, arXiv preprint. https://arxiv.org/abs/2309.11069
Type : preprint non relu par les pairs

## Problème

Les détecteurs génériques ratent les objets très petits devant l'image (§1). Le découpage uniforme en tuiles à l'inférence (SAHI, DarkHelp, tuiles à recouvrement fixe) aide, mais les auteurs lui reprochent (§1, §2) : un taux de recouvrement unique pour toutes les tuiles, à recalibrer à chaque nouveau jeu ; des calculs sur des tuiles vides ou redondantes ; des objets grands ou irréguliers fragmentés entre tuiles que la NMS seule fusionne mal (confusions car/van/truck entre classes proches).

## Méthode

Recette d'inférence, sans réentraînement spécifique (§3, Fig. 1) :
1. Grille N x M de tuiles **sans recouvrement** (3 x 2 en expérience, tuiles 640 x 640 sur image 1920 x 1080, §4.2-4.3), traitées en un seul batch.
2. Chaque boîte prédite est classée selon sa distance au bord de sa tuile : seuil x% de W ou H avec x = 2 % ; `near_edge` (un bord), `near_corner` (deux bords), `central`. Les boîtes centrales sont conservées telles quelles.
3. **Tuiles dynamiques** (Dynamic Patch Proposal) : pour chaque frontière E(i,j) portant des boîtes near-edge/near-corner, on crée une tuile centrée sur E(i,j), de taille au plus celle d'une tuile de base (côté commun) ; si la boîte n'apparaît que dans une des deux tuiles, la tuile est étendue à 50 % de la dimension de l'autre. Coin commun : tuile de la taille d'une tuile de base, symétrique autour du coin. Les prédictions near-edge d'origine sont **jetées et remplacées** par celles des tuiles dynamiques (pas de fusion par NMS entre tuiles de base et dynamiques pour ces boîtes).
4. **Tile Minimizer** : les tuiles dynamiques sont regroupées en images composites de la taille d'une tuile de base, pour réduire le nombre de passes avant.
5. **Filtre grand/petit** : l'image entière redimensionnée est aussi inférée (« FI ») ; on n'y garde que les prédictions plus grandes que θ = alpha x (W x H), et dans les tuiles dynamiques que celles plus petites que θ. Valeur d'alpha : « constante entre 0 et 1 », **valeur n/r** (§3).

Entraînement (§4.2) : YOLOv8m préentraîné, affiné 71 époques sans geler de couches ; images mises à 1920 x 1080 ; par image, 6 tuiles 640 x 640 (3 x 2 sans recouvrement) plus l'image entière redimensionnée en 640 x 640 ; Mosaic jusqu'aux 10 dernières époques, MixUp p = 20 %, échelle +/- 20 % ; SGD, lr 0,01, momentum 0,937, weight decay 0,0005. Les tuiles d'entraînement sont donc fixes, non recouvrantes (le « dynamique » n'agit qu'à l'inférence).

## Plateforme et implémentation

2 x NVIDIA TITAN X 12 Go pour l'entraînement, 1 TITAN X pour l'inférence (§4.2-4.3). Détecteur : **YOLOv8m** (Ultralytics, citée « Jocher et al., 2023 »), seul détecteur testé. Quantification, puissance : n/r. Code publié : non mentionné dans le texte lu (n/r).

## Résultats

Jeu unique : VisDrone 2019 (6 471 train / 548 val / 1 610 test public, 10 classes, §4.1) ; test public utilisé (Table 1). Max 1000 détections par image, métriques COCO (§4.3). **Le corps de la Table 1 n'a pas été extrait** (légende seule) : les chiffres ci-dessous viennent uniquement du texte de §4.3, pas du tableau.

| Configuration (§4.3) | mAP@0.5 | mAP@0.5:0.95 | mAP@0.5s | Temps moyen / image |
|---|---|---|---|---|
| YOLOv8m + Dynamic Tiling + FI + Tile Minimizer + TTA (meilleure) | 45,5 | 27 | 31,2 | 0,301 s |
| idem sans Tile Minimizer, avec TTA | 45,6 (« de 43,8 à 45,6 ») | n/r | n/r | 0,333 s |
| Dynamic Tiling sans TTA, sans Tile Minimizer | 43,8 | n/r | n/r | 0,160 s |
| Dynamic Tiling + Tile Minimizer sans TTA | n/r | n/r | n/r | 0,148 s |
| YOLOv8m + SAHI + FI + TTA (baseline) | 41,6 | 24,7 | n/r | n/r |

- Gain annoncé sur SAHI+FI+TTA : +9,4 % (mAP@0.5) et +9,3 % (mAP@0.5:0.95) en relatif ; mAP@0.5s : +16,4 % vs SAHI, +25,3 % vs PowerTiling (Ünel et al.), +13,5 % vs DarkHelp (§4.3), en valeurs relatives rapportées ; les valeurs absolues de ces baselines pour mAP@0.5s sont n/r dans le texte.
- Coût : TTA fait passer le temps de 0,160 à 0,333 s ; Tile Minimizer le ramène à 0,148 s (-7,5 %) et 0,301 s (-9,6 %) (§4.3). Le texte affirme que la méthode est plus rapide que les méthodes antérieures ; **les temps de SAHI, PowerTiling et DarkHelp ne sont pas dans le texte** (corps de Table 1 manquant), donc ce rapport de vitesse n'est pas vérifié ici.
- Les écarts-types des temps sont annoncés dans Table 1 (colonne STD) : valeurs n/r. Aucune variance sur les mAP.
- Incohérence interne : 45,5 (meilleure config) contre 45,6 (« de 43,8 à 45,6 »), sans précision sur la configuration exacte.
- Pas d'ablation chiffrée lisible de chaque composant (Dynamic Tiling seul, FI, filtre grand/petit) ni de comparaison au plein cadre sans tuiles dans le texte.

→ reportés dans `benchmarks.csv` : 5 lignes proposées (agent principal) : meilleure config (mAP@0.5, mAP@0.5:0.95, mAP@0.5s), config sans Tile Minimizer avec TTA, config sans TTA ni Tile Minimizer ; confidence `medium` (texte, pas tableau).

## Limites et critique

- **Évaluation étroite** : un seul jeu (VisDrone), un seul détecteur (YOLOv8m), un seul run apparent, aucune variance ni intervalle de confiance sur les mAP ; les gains de quelques points (+3,9 mAP@0.5 vs SAHI) ne sont pas testés statistiquement.
- **Tableau principal illisible** dans l'extraction : baselines et temps comparatifs non vérifiables ici ; à relire sur le PDF avant tout usage chiffré.
- **Comparaison non isolée** : la meilleure configuration cumule FI, Tile Minimizer et TTA ; les auteurs comparent à « SAHI + FI + TTA » mais l'effet propre des tuiles dynamiques (vs FI ou TTA) n'est pas montré. L'entraînement (tuiles 640 sans recouvrement + image entière) est propre à leur méthode : le modèle est-il le même pour toutes les baselines ? n/r.
- **Équité vs SAHI** : ils soutiennent que SAHI original utilise du sur-échantillonnage et que leur choix (tuile = taille d'entrée) isole l'effet ; mais « surpasse les chiffres publiés de SAHI » compare des protocoles différents (§2).
- **Rhétorique** (« unparalleled », « paradigme », « normes sans précédent ») sans preuve de généralité ; l'affirmation « pas de recalibration » n'est pas testée (un seul jeu ; x = 2 %, alpha, grille 3 x 2 sont fixés sans étude de sensibilité).
- Le texte attribue une baisse de mAP à des objets non annotés que le modèle détecte : plausible (qualité des labels VisDrone) mais non démontré.
- Temps mesuré sur TITAN X ancien, protocole (échauffement, I/O, post-traitement inclus ?) n/r. Une estimation du surcoût vs découpage fixe n'est pas calculable depuis le texte.
- Grands objets coupés : traités par le filtre de taille et l'inférence plein cadre, pas par fusion de boîtes ; si l'objet est grand et traverse plusieurs tuiles, sa détection repose sur l'image réduite (déduit de §3).
- Code non cité ; preprint, aucune relecture.

## Pertinence pour la thèse

Pertinence pour la base (préparer des données pour la détection YOLO) :
- **PRÉTRAITER** : recette de découpage utilisable telle quelle comme prétraitement : grille non recouvrante 3 x 2 de tuiles 640 sur 1920 x 1080 (tuile = résolution d'entrée du modèle, pas de redimensionnement), plus l'image entière réduite. À appliquer sur images haute résolution (drone, aérien) où les objets font moins de ~32 px à l'échelle d'entrée.
- **CONSTRUIRE / AUGMENTER** : au moment de l'entraînement, ils découpent aussi en tuiles non recouvrantes et ajoutent l'image réduite, avec Mosaic et MixUp (p = 20 %) conservés : indice que l'entraînement doit voir la même distribution de tuiles que l'inférence (§4.2).
- **ANNOTER** : n'apporte pas de règle d'annotation ; seulement le constat que des petits objets non annotés ressortent comme faux positifs (§4.3), donc qualité des labels VisDrone à surveiller.
- Quand l'appliquer : à l'inférence sur grandes images avec de nombreux petits objets, quand SAHI à recouvrement fixe est trop lent ou mal calibré. Éviter d'en tirer des gains généraux : une seule base, un seul détecteur. Axes `preprocessing` + `imbalance-small`.

## Gaps identifiés

- Aucune évaluation sur d'autres jeux (DOTA, UAVDT, jeux industriels) ni d'autres YOLO.
- Pas d'étude de sensibilité (seuil 2 %, grille, alpha) ni de variance multi-graines.
- Pas de comparaison de coût à puissance égale sur GPU embarqué (Jetson) : question ouverte pour le tiling sur cible embarquée.
- Pas de comparaison directe au même modèle entraîné avec tuiles recouvrantes (recette d'entraînement SAHI).

## Statut de lecture

Papier complet (`fulltext.md` lu en entier, extraction GROBID ok). **Corps de la Table 1 non extrait** : tous les chiffres viennent du texte de §4.3 ; les temps et mAP des baselines (SAHI, PowerTiling, DarkHelp) et les écarts-types sont donc `n/r`.
Ce qui est déduit et non affirmé par les auteurs : l'attribution des 43,8 / 45,6 / 0,160 / 0,333 s aux configurations (texte ambigu), le traitement des grands objets traversant plusieurs tuiles, l'absence de code (non mentionné), la non-isolation de l'effet des tuiles dynamiques.
