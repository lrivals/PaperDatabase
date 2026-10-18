---
id: arxiv-1708.02002-focal-loss-dense-object-detection
fiche: done
date: 2026-10-18
---

# Focal Loss for Dense Object Detection

Tsung-Yi Lin, Priya Goyal, Ross Girshick, Kaiming He, Piotr Dollár, 2017, arXiv preprint. https://arxiv.org/abs/1708.02002
Type : preprint non relu par les pairs (article connu comme ICCV 2017 : information externe au `metadata.json`, à vérifier avant citation)

## Problème

Les détecteurs one-stage (YOLO, SSD) restent 10 à 40 % en deçà des détecteurs two-stage en précision (§1). Les auteurs identifient la cause : le déséquilibre extrême avant-plan / arrière-plan à l'entraînement d'un détecteur dense, « e.g., 1:1000 » (§3), avec ~100k ancres par image (§1) dont quelques-unes seulement contiennent un objet. Deux effets (§2) : entraînement inefficace (la plupart des positions sont des négatifs faciles sans signal) et dégénérescence du modèle quand ces négatifs faciles dominent la perte et le gradient. Les two-stage évitent le problème par la cascade (proposals, 1-2k) et l'échantillonnage (ratio 1:3, OHEM) (§1, §3.4).

## Méthode

**Focal loss** (§3). Partant de CE(p_t) = -log(p_t), ajout d'un facteur modulant : FL(p_t) = -α_t (1-p_t)^γ log(p_t). γ = 0 redonne la CE ; avec γ = 2, un exemple à p_t = 0.9 a une perte 100x plus faible que la CE, 1000x à p_t ≈ 0.968, et un exemple mal classé (p_t ≤ 0.5) est réduit d'au plus 4x (§3.2). α pondère classe rare / fréquente (α-balanced CE, §3.1) mais ne distingue pas faciles et difficiles. Perte appliquée à toutes les ~100k ancres, sans échantillonnage, somme normalisée par le nombre d'ancres **assignées** (pas le total) (§4.1). Sigmoïde fusionnée avec la perte pour la stabilité numérique (§3.2).

**Initialisation du biais (prior π)** (§3.3, §4.1). Biais de la dernière conv de la sous-réseau de classification : b = -log((1-π)/π), avec π = 0.01, pour que chaque ancre soit prédite avant-plan avec confiance ~π au départ. C'est un changement d'initialisation, pas de perte, qui s'applique aussi à la CE.

**RetinaNet** (§4), en bref : backbone ResNet-50/101 + FPN (niveaux P3-P7, 256 canaux) ; deux sous-réseaux conv entièrement convolutionnels par niveau (classification : 4 conv 3x3 + conv KA ; régression de boîte : même structure, 4A sorties, régresseur indépendant de la classe) ; 9 ancres par position (3 échelles {2^0, 2^1/3, 2^2/3} x 3 ratios {1:2, 1:1, 2:1}), aires 32² à 512² de P3 à P7, couvrant 32-813 px ; inférence : seuil 0.05, top 1k par niveau, NMS 0.5 (§4.1). Le FPN est indispensable : un backbone sans pyramide (dernière couche ResNet seule) donne un AP faible (§4).

**Assignation des ancres** (§4). Règle de RPN avec seuils ajustés : IoU ≥ 0.5 avec une vérité terrain => positive ; IoU dans [0, 0.4) => arrière-plan ; IoU dans [0.4, 0.5) => ignorée à l'entraînement. Chaque ancre est assignée à au plus une boîte (cible one-hot de longueur K). Les seuils eux-mêmes ne sont pas ablatés dans le papier.

**Entraînement** (§4.1). SGD, 8 GPU, 16 images par minibatch, 90k itérations, lr 0.01 divisé par 10 à 60k et 80k, weight decay 1e-4, momentum 0.9 ; seule augmentation : flip horizontal (sauf mention contraire) ; perte totale = focal loss + smooth L1.

## Plateforme et implémentation

Détecteur GPU, hors sujet FPGA. Entraînement sur 8 GPU, 10 à 35 h selon les modèles (§4.1). Latence mesurée sur Nvidia M40 (§5.2). Code publié : https://github.com/facebookresearch/Detectron (résumé et §6). Évaluation sur COCO trainval35k (80k train + 35k de val) ; ablations sur minival (5k), résultats finaux sur test-dev (§5).

## Résultats

Ablations : ResNet-50-FPN (ou -101 si dit), entrée 600 px, COCO minival, flip seul (§5.1). Les corps des Tables 1a-1e ne sont pas extraits de `fulltext.md` (seule la légende de 1d/1e/1c est présente) : les valeurs par (γ, α) de 1a/1b sont `n/r` ici, seuls les chiffres du texte et de la Table 3 sont repris.

| Configuration | AP | Source |
|---|---|---|
| CE sans prior (init standard) | diverge | §5.1 |
| CE avec prior π = 0.01 (R50) | 30.2 | §5.1 |
| α-balanced CE (R50, meilleur α = 0.75) : +0.9 AP | 31.1 | §5.1, Table 3 |
| FL γ = 2, α = 0.25 (R50) : +2.9 AP vs α-CE | 34.0 | §5.1, Table 3 |
| FL* (autre forme, γ = 2 β = 1 ; γ = 4 β = 0) | 33.8 ; 33.9 | Table 3 |
| FL, R101-600 | 36.0 | §5.1 |
| OHEM, meilleur réglage (R101 : batch 128, NMS 0.5, sans 1:3) | 32.8 (écart 3.2 AP) | §5.1 |
| 1 ancre carrée par position (R50) | 30.3 | §5.2 |
| 3 échelles x 3 ratios = 9 ancres (R50) | 34.0 | §5.2 |
| RetinaNet-101-800, scale jitter, 1.5x plus long, test-dev | 39.1 (5 fps) | §1, §5.3 |
| + ResNeXt-32x8d-101-FPN, test-dev | 40.8 | §5.3, Fig. 2 |

Points saillants.
- **Robustesse de γ et α** (§4.1, §5.1) : γ = 2 retenu ; le réseau est « relativement robuste » à γ ∈ [0.5, 5]. α et γ interagissent : plus γ augmente, plus le meilleur α baisse (les négatifs faciles étant atténués, moins besoin de pousser les positifs) ; les meilleurs α sont dans [0.25, 0.75] (testés dans [0.01, 0.999]). α = 0.5 avec γ = 2 est seulement 0.4 AP en dessous de α = 0.25. Le gain de γ pèse bien plus que le réglage de α.
- **Analyse de la perte d'un modèle convergé** (§5.1, Fig. 4) : sur ~10^7 fenêtres négatives et ~10^5 positives, les ~20 % de positifs les plus durs portent environ la moitié de la perte positive, quel que soit γ ; pour les négatifs, γ = 2 concentre la quasi-totalité de la perte sur une petite fraction d'exemples (la CDF des négatifs est proche de celle des positifs à γ = 0).
- **Vs OHEM / échantillonnage** : FL (36.0) > meilleur OHEM (32.8) sur le même réseau ; OHEM jette les exemples faciles, FL les atténue. Variante OHEM 1:3 testée aussi, avec batch et NMS variés ; la Table 1d n'est pas lisible ici, donc ses valeurs sont `n/r`. Le hinge loss sur p_t a été instable, sans résultat exploitable (§5.1).
- **Densité d'ancres** : saturation au-delà de 6-9 ancres (§5.2).
- **Vitesse** : RetinaNet-101-600 égale la précision de FPN Faster R-CNN R101 en 122 ms contre 172 ms par image (M40) (§5.2).

→ reportés dans `benchmarks.csv` : 10 lignes proposées (hors périmètre d'écriture de cet agent, déposées dans `.cache/bench/arxiv-1708.02002-focal-loss-dense-object-detection.csv` pour l'agent principal). Table 3 : confidence `high` ; valeurs du texte : `medium`.

## Limites et critique

- Tout est mesuré sur COCO (80 classes, objets de taille variée) : aucune mesure sur un dataset à classes déséquilibrées, à petits objets ou à données réduites. Le papier traite le déséquilibre avant/arrière-plan, pas la longue traîne entre classes (extension à la multiclasse : la perte est dite « straightforward », mais sans analyse par classe, note 1 de §3).
- Seuils IoU 0.5 / 0.4 posés sans ablation ni justification chiffrée (§4) ; pas de comparaison avec une assignation adaptative.
- Ablations à un seul run apparent, sans barres d'erreur (non indiqué dans le texte) ; des écarts de 0.1 à 0.4 AP (FL vs FL*, α = 0.5 vs 0.25) sont à lire avec prudence.
- Comparaison OHEM : le réglage OHEM est exploré sur batch/NMS, mais les auteurs disent aussi avoir « tried other parameter settings » sans plus de détail ; comparaison faite par les auteurs de la méthode concurrente, donc possible biais d'effort de réglage.
- Latences M40 et AP test-dev à des échelles différentes ; comparaisons à des méthodes citées avec leurs chiffres publics (Fig. 2) : conditions de mesure non harmonisées. Le papier note lui-même qu'une variante de Faster R-CNN publiée après est meilleure (§5.2).
- Preprint non relu par les pairs selon `metadata.json` ; code Detectron publié.
- Le régime « temps réel » (YOLO) n'est pas atteint : 5 fps pour le meilleur modèle (§1) ; les auteurs disent que ce régime demande une conception dédiée (§5.2).

## Pertinence pour la thèse

Pour cette base (données pour la détection YOLO) :

- **CONSTRUIRE un dataset** : le ratio positifs/négatifs est un fait structurel du détecteur dense (~100k ancres, quelques positives, jusqu'à 1:1000 selon §3), pas un défaut de dataset. Inutile de « rééquilibrer » en retirant des images vides ou en sous-échantillonnant l'arrière-plan pour ce seul motif ; ce déséquilibre se traite dans la perte. Reste ouvert : le papier ne dit rien sur les déséquilibres entre classes d'un dataset (longue traîne) ni sur la fraction d'images sans objet.
- **ANNOTER** : l'assignation est faite à partir des boîtes annotées avec des seuils IoU 0.5 / 0.4 ; une zone [0.4, 0.5) est ignorée. Une boîte manquante ou décalée transforme des ancres positives en négatives dures, précisément les exemples que FL amplifie : inférence de ma part (non testée dans le papier), à rapprocher des papiers de qualité de labels de la base. FL concentre le gradient sur les exemples durs, donc potentiellement sur les erreurs d'annotation.
- **PRÉTRAITER** : peu d'apport direct (échelle 400-800 px ; résolution et vitesse en Table 1e, non lisible ici). Pas de tiling ni de letterbox discutés. Les petits objets sont couverts seulement par la couverture d'ancres (32-813 px).
- **AUGMENTER** : le papier n'utilise que le flip horizontal (§4.1) ; il n'apporte rien sur Mosaic, MixUp ou Copy-Paste, mais fournit une base de référence « sans augmentation lourde » pour mesurer un gain de perte.
- **Quand l'appliquer** : (1) détecteur dense à ancres entraîné avec la CE standard : essayer FL γ = 2, α = 0.25 (+2.9 AP ici vs α-CE) mais avec l'initialisation π = 0.01, indispensable avant tout ; (2) si le détecteur diverge ou démarre mal sur un fort déséquilibre : régler d'abord le prior, avant la perte ; (3) un détecteur YOLO moderne utilise déjà ses propres objectifs de classification et de quality (Varifocal, TAL, etc.) : ce n'est pas dit dans ce papier, à vérifier dans d'autres fiches de la base avant de recommander FL à un YOLOv8. Pour un dataset à longue traîne, α par classe est une idée à tester (non couverte ici).

## Gaps identifiés

- Effet de FL (γ, α) sur un dataset de domaine à peu de données, ou à petits objets (VisDrone) : non couvert par ce papier.
- Interaction entre bruit d'annotation (boîtes manquantes) et FL : non mesurée.
- Sensibilité aux seuils IoU d'assignation (0.5 / 0.4) : non ablatée ; à croiser avec la littérature sur l'assignation adaptative (ATSS, SimOTA, TAL).
- Déséquilibre entre classes (longue traîne) vs déséquilibre avant/arrière-plan : le papier ne traite que le second.

## Statut de lecture

papier complet (`fulltext.md` lu en entier ; extraction `grobid`, `ok: true`). Les corps des Tables 1a-1e ne sont pas extraits : seules leurs légendes partielles, le texte et la Table 3 sont disponibles ; les valeurs par (γ, α), par nombre d'ancres hors extrêmes, par batch/NMS d'OHEM et par profondeur/échelle sont `n/r`.
Ce qui suit est déduit et non affirmé par les auteurs : l'effet des boîtes manquantes sur FL, l'absence de besoin de rééquilibrer les images vides, la comparaison avec les YOLO récents, le biais d'effort de réglage sur OHEM (impression, pas un fait établi), l'absence de barres d'erreur (non mentionnées dans le texte extrait), la publication ICCV 2017.
