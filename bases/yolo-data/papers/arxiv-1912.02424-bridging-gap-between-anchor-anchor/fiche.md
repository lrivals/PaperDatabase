---
id: arxiv-1912.02424-bridging-gap-between-anchor-anchor
fiche: done
date: 2026-10-05
---

# Bridging the Gap Between Anchor-based and Anchor-free Detection via Adaptive Training Sample Selection

Shifeng Zhang, Cheng Chi, Yongqiang Yao, Zhen Lei, Stan Z Li, 2019, arXiv preprint (version CVPR 2020 connue, non vérifiée ici). https://arxiv.org/abs/1912.02424 ; code : https://github.com/sfzhang15/ATSS (§Abstract)
Type : preprint non relu par les pairs

## Problème

Les détecteurs anchor-free (FCOS) surpassent RetinaNet à architecture quasi identique (37.1 % vs 32.5 % AP, §3.2). Les auteurs cherchent lequel des trois écarts (nombre d'ancres par position, définition des positifs/négatifs, point de départ de la régression) explique cet écart (§1). Le papier part de la question « comment une boîte annotée devient des exemples positifs et négatifs ».

## Méthode

**Démonstration (§3).** RetinaNet à une ancre carrée 8S par position (#A=1) est comparé à FCOS. Après avoir greffé sur RetinaNet les astuces universelles de FCOS (GroupNorm, GIoU, positifs limités à l'intérieur de la boîte, centerness, scalaire par niveau), l'écart tombe de 5,3 à 0,8 point : 37.0 vs 37.8 (Table 1, §3.2). Ensuite, en croisant définition des positifs et point de départ de la régression (Table 2, §3.3) :

| Positifs définis par | régression depuis boîte | depuis point |
|---|---|---|
| IoU (RetinaNet) | 37.0 | 36.9 |
| contrainte spatiale + d'échelle (FCOS) | 37.8 | 37.8 |

Donc la régression (boîte ou point) est indifférente ; la définition des positifs fait la différence. Le nombre d'ancres est traité à part (§4.5).

**Règle ATSS (§4.1, Algorithme 1).** Pour chaque boîte annotée g :
1. sur chaque niveau de pyramide, prendre les k ancres dont le centre est le plus proche (distance L2) du centre de g ; k par défaut = 9, soit k x L candidats (L = 5 niveaux) ;
2. calculer l'IoU entre candidats et g, puis sa moyenne m_g et son écart-type v_g ;
3. seuil propre à g : t_g = m_g + v_g ;
4. positifs = candidats avec IoU >= t_g et centre à l'intérieur de g ; si une ancre est assignée à plusieurs boîtes, on garde la boîte d'IoU maximale ; tout le reste est négatif.

Motivations données (§4.1) : m_g mesure l'adéquation des ancres à l'objet (seuil haut si les ancres sont bonnes, bas sinon) ; v_g mesure si un niveau est nettement plus adapté (v_g élevé : positifs pris surtout sur ce niveau ; v_g faible : plusieurs niveaux se partagent les positifs). Environ 0.2 x kL positifs par objet quelle que soit son échelle, son ratio ou sa position, contre beaucoup plus de positifs pour les grands objets avec RetinaNet ou FCOS : le gain est présenté comme un meilleur équilibre entre objets (§4.1, affirmation statistique de l'auteur, mesure détaillée non fournie).

Pas de surcoût d'inférence : seule l'assignation à l'entraînement change.

## Plateforme et implémentation

Pas de matériel embarqué. ResNet-50 (ImageNet) + FPN 5 niveaux, SGD 90K itérations, batch 16, lr 0.01 (§3.1) ; entrée courte 800 / longue <= 1333. Pour le test-dev : entraînement multi-échelle 640-800, 180K itérations (§4.4). Puissance, FPS, latence : n/r. Code publié (lien ci-dessus) ; la version « lite » est intégrée au code FCOS officiel sous le nom center sampling (§4.2).

## Résultats

Tous sur MS COCO, minival sauf mention.
- RetinaNet (#A=1) 37.0 -> 39.3 AP avec ATSS (+2.3 ; AP_S 21.4 -> 24.3) (Table 3). FCOS 37.8 -> 39.2 avec ATSS complet (AP_S 22.1 -> 22.7), 38.6 avec center sampling seul (Table 3).
- Sensibilité à k (Table 4) : 38.0 (k=3), 38.8 (5), 39.1 (7), 39.3 (9), 39.1 (11), 39.0 (13), 39.1 (15), 39.2 (17), 38.9 (19). Insensible de 7 à 17 ; k trop petit = instabilité statistique, k trop grand = candidats de faible qualité (§4.3).
- Échelle de l'ancre carrée (ratio 1:1) (Table 5) : AP 39.0 / 39.2 / 39.3 / 39.3 / 38.9 pour 5S / 6S / 7S / 8S / 9S ; AP_S 23.2 / 23.5 / 22.9 / 24.3 / 22.9 (plus bruité que l'AP global).
- Ratio d'aspect à 8S (Table 6) : AP 39.1 (1:4), 39.0 (1:2), 39.3 (1:1), 39.3 (2:1), 39.1 (4:1).
- Nombre d'ancres (Table 7, §4.5) : RetinaNet #A=9 d'origine 36.3 ; avec astuces universelles 38.4 (donc, avec l'assignation IoU, plus d'ancres aide : 38.4 contre 37.0 pour #A=1) ; avec ATSS 39.2 (3x3), 39.3 (3 éch. x 1 ratio), 39.2 (1 x 3), 39.3 (1 x 1) : plus aucun gain à multiplier les ancres.
- test-dev (Table 8) : ATSS ResNet-101 43.6 AP (RetinaNet R-101 : 39.1) ; ResNeXt-64x4d-101 45.6 ; avec DCN 47.7 ; test multi-échelle 50.7 (AP_S 33.2). YOLOv2 listé à 21.6 AP (valeur citée, pas de leur travail).

→ reportés dans `benchmarks.csv` : 12 lignes proposées (3 Table 3, 4 Table 7, 5 Table 8), colonnes matériel `n/r`. Les chiffres de Table 4, 5, 6 ne sont pas reportés (analyse de sensibilité, tous dans cette fiche).

## Limites et critique

- Tous les chiffres viennent d'un seul jeu (COCO, 80 classes, objets de taille variée) et d'un seul schéma d'entraînement (800x1333, 90K itérations). Aucune évaluation sur un domaine à petits objets dominants (aérien, VisDrone) ni sur peu de données : la robustesse à k et aux ancres n'est pas démontrée hors COCO.
- Les petits objets : le gain AP_S est net pour RetinaNet (+2.9) mais faible pour FCOS (+0.6 ATSS complet vs FCOS d'origine, Table 3 ; texte §4.2) ; la variation d'AP_S selon l'échelle d'ancre (22.9 à 24.3, Table 5) n'est pas commentée par les auteurs et pourrait être du bruit d'un seul run (pas d'écart-type rapporté).
- Pas de mesure de variance entre runs : les écarts de 0.1-0.3 AP de Tables 4-7 sont à lire comme « stable », pas comme un classement.
- Le « plus d'ancres est inutile » (§4.5) est démontré avec ATSS sur RetinaNet à 5 niveaux ; les auteurs disent eux-mêmes que le rôle d'ancres multiples reste à étudier. Les ancres issues de k-means de YOLOv2/v3 ne sont pas testées.
- Comparaison Table 8 : les détecteurs comparés ont des backbones, durées d'entraînement et astuces différents ; DCN et test multi-échelle sont ajoutés seulement à ATSS. Aucune vitesse rapportée ni comparaison à YOLOv3+ (seul YOLOv2 est listé).
- Le terme « sans hyperparamètre » est exagéré : k, l'échelle d'ancre (8S) et le centre-dans-la-boîte restent des choix ; les auteurs disent « presque » (§4.1).

## Pertinence pour la thèse

Pertinence pour cette base (axe imbalance-small : assignation des labels) :
- **ANNOTER / CONSTRUIRE** : l'assignation dépend directement de la boîte annotée : centre de g (candidats), IoU avec g (seuil), centre dans g (filtre). Une boîte imprécise ou mal centrée décale les positifs et, via m_g et v_g, le seuil lui-même. Déduit : le bruit de boîtes pèse aussi sur l'assignation, pas seulement sur la cible de régression (le papier ne teste pas ce point).
- **AUGMENTER / PRÉTRAITER** : déduit : toute transformation qui modifie la taille effective ou le centre d'une boîte (mosaic, échelle aléatoire, recadrage, tiling) change les candidats par niveau ; l'assignation ATSS étant relative à l'objet, elle suit sans réglage, mais le papier ne le teste pas.
- **Petits objets et conception des ancres d'un YOLO** : sous ATSS, le choix de l'échelle et du ratio des ancres et leur nombre influent peu (Tables 5-7) : s'il est possible de changer l'assignation (top-k par niveau + seuil adaptatif au lieu d'un IoU fixe), le clustering k-means des ancres devient secondaire. Avec l'assignation IoU classique, au contraire, le nombre et la forme des ancres comptent (36.3 -> 38.4 avec plus d'ancres, Table 7), et il faut donc les adapter au dataset. Tout petit objet est pénalisé par un seuil IoU fixe parce que ses ancres ont de faibles IoU ; ATSS abaisse le seuil quand m_g est bas (§4.1).
- **Quand l'appliquer** : (1) détecteur à ancres sur dataset aux tailles d'objet très dispersées ou petits objets : préférer une assignation adaptative à des seuils IoU/échelle fixes ; (2) comparer deux détecteurs « anchor-based vs anchor-free » : vérifier d'abord que l'assignation est la même ; (3) YOLO moderne : les assignateurs dynamiques (déduit : famille ATSS/TAL) reprennent cette idée, hors périmètre de ce papier.
- Reste ouvert : effet sur dataset à petits objets (VisDrone, aérien), avec labels bruités, et avec des ancres k-means style YOLO.

## Gaps identifiés

- Assignation adaptative sur petits objets (VisDrone, aérien) : aucune mesure ici ; à croiser avec SAHI / tiling.
- Sensibilité de l'assignation au bruit de boîtes annotées (décalage de centre, taille), non testée.
- Équivalence ATSS vs ancres k-means de YOLOv2/v3/v5 : non comparée.

## Statut de lecture

papier complet (`fulltext.md` lu en entier, extraction grobid ok). Table 3 et Table 4 listées « sans corps extrait » ; les valeurs de Table 3 ont été retrouvées en texte (§4.2 : +2.3 AP etc., Table 3 inline) donc `confidence: medium` ; Table 4 recoupée avec le texte (k 7-17 stable, 19 en baisse, 3 net recul).
Ce qui suit est déduit et non affirmé par les auteurs : l'effet du bruit de boîtes sur m_g/v_g ; le comportement d'ATSS sous mosaic, tiling ou sur petits objets ; l'implication pour les ancres k-means d'un YOLO ; le rapprochement avec les assignateurs dynamiques récents ; l'interprétation d'AP_S dans Table 5 comme du bruit.
