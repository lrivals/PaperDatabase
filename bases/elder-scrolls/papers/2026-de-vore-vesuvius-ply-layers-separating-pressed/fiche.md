---
id: 2026-de-vore-vesuvius-ply-layers-separating-pressed
fiche: done
date: 2026-11-17
---

# vesuvius-ply-layers: separating pressed papyrus layers by recto/verso fibre plies in Herculaneum scroll CT

Victoria De Vore, 2026, GitHub (commit 92675735c2, 2026-11-16). https://github.com/Victoria-TechNexus/vesuvius-ply-layers/tree/92675735c2f98fbf295a13dc9c85a11bc2e79c7f
Type : dépôt GitHub communautaire du Vesuvius Challenge (README, WRITEUP, MATH, TUNING), **non relu par les pairs, chiffres auto-déclarés**, un seul auteur, MIT. « Research code ».

## Problème

Dans les scans micro-CT de rouleaux, le suivi de fibres donne beaucoup de courtes traces ; le verrou est de décider lesquelles appartiennent à la même couche (un tour de papyrus). Là où deux feuillets sont séparés par un vide sombre c'est facile, mais dans environ un quart à un tiers des endroits échantillonnés ils sont pressés sans vide (WRITEUP §1, chunk 2026-de-vore#004.0). Les auteurs rapportent qu'une règle de vide sombre n'y donne que 40-61 % de réponses justes, « pas mieux qu'une pièce » (WRITEUP §1). But : séparer les couches pressées sans traçage manuel, mailler sans lisser les plis, aplatir, lire l'encre.

## Méthode

Pipeline en 4 étages (README §What it does) :
- **Phases 1-5** (par tuile 192 × 416 × 416 voxels à 9,6 µm, niveau 2 d'un scan 2,4 µm) : tenseur de structure, petit U-Net 3D sans étiquettes humaines (probabilités feuillet / recto / verso, cibles issues du tenseur, MATH §3), suivi de fibres RK4 qui s'arrête quand p_verso > 0,6, environ 50 000 traces par tuile, regroupement en pièces (Louvain) puis en feuillets.
- **Phase 6 : idée centrale**. Chaque couche = 2 plis : recto (fibres autour du rouleau, « H ») et verso (fibres le long de l'axe, « V »). On lit l'ordre des plis entre feuillets voisins (jusqu'à 6 points par paire) et on classe « même couche / couches différentes / délaminée / même pli » (WRITEUP §2, MATH §6c). 6d ordonne la pile de feuillets, lectures de plis prioritaires sur la règle du vide sombre à moins de 80 voxels. Épaisseurs mesurées : 1 pli 8-9 voxels (environ 80 µm), couche 13-15 voxels (environ 135 µm) (WRITEUP §2).
- **Phase 7** : raccord d'une couche entre tuiles (recouvrement 40 voxels), maillage à partir des traces de la couche (plis conservés), aplatissement par MDS + raffinement (distances de marche), 8 auto-contrôles.
- **Phases 8-10** : grille plate, 21 tranches à 5 voxels côté recto, modèle d'encre publié 9 µm (`ink_9um`, hors dépôt), interchangeable.
- Constat d'entraînement : plus de données d'entraînement du U-Net (11 blocs au lieu de 5) dégrade la séparation (sortie verso « écrasée », presque aucun arrêt verso : 0,02 % contre 1,11-1,23 % de papyrus avec verso > 0,6) ; deux checkpoints utilisés, choisis par tuile (WRITEUP §4, chunk 2026-de-vore#007.0).

## Plateforme et implémentation

Matériel : session Google Colab standard, GPU T4, 12 GB de RAM ; par tuile phases 1-5 environ 13-18 min (pic environ 9 GB), phase 6 environ 5-10 min ; maillage d'une couche sur 6 tuiles (5,07 M de points) environ 28-30 min (README §Results ; WRITEUP §9, chunk 2026-de-vore#003.0). Logiciels : Python, `vesuvius` de ScrollPrize/villa (MIT) pour l'inférence d'encre, modèle `scrollprize/ink_9um` (`step-075000.pth`), flux du CT depuis le bucket ouvert `s3://vesuvius-challenge-open-data/PHercParis4/`. Scan : PHerc. Paris 4, ESRF 20260411134726, 2,4 µm, traité à 9,6 µm. Code publié : https://github.com/Victoria-TechNexus/vesuvius-ply-layers (MIT), avec checkpoints U-Net v1 et v1.1 ; le modèle d'encre et le code villa ne sont pas dans le dépôt. Grille plate sauvegardée en TIFF 3 canaux, pas encore en tifxyz VC3D (README §Known limits).

## Résultats

Tous les chiffres sont auto-déclarés, sur **une seule couche** (couche du segment officiel, 6 tuiles = 496 × 416 × 792 voxels, déroulée en 997 × 615 px, environ 9,6 × 5,9 mm).
- Surface jugée par le CT brut (seuil d'Otsu, ±10 %), zone commune avec le segment officiel fait main (WRITEUP §8, chunk 2026-de-vore#011.1) : sur le papyrus 99,6 % contre 82,0 % ; traverse un vide sombre 0,4 % contre 18,0 % ; reste sur le même feuillet 99,5 % contre 97,4 % ; croisements de couches « à peu près égaux » (0,11 contre 0,18 pour 100 paires au run à 4 tuiles ; 0,46 contre 0,23 au seuil le plus strict) ; part comparée 87 % / 91 %.
- Accord d'encre là où les deux surfaces sont sur le même feuillet : 94 % de 100 764 pixels (WRITEUP §8).
- Encre contre étiquettes humaines (run antérieur, U-Net original, non refait sur la surface finale ; WRITEUP §7, chunk 2026-de-vore#010.1) : score +0,73 pour la surface automatique (rappel 78 %, 5 % de blanc marqué encre) contre +0,80 pour le segment officiel (87 %, 6 %), sur 47,1 % de la feuille ; +0,89 sur la seule partie de la tuile 1 (9,9 % de la feuille, rappel 97 %). Hasard environ -0,1, 95e pct +0,3.
- Séparation de couches (WRITEUP §3, §5, chunk 2026-de-vore#008.1) : faits de plis contredits 9,3 % en moyenne (final) contre 10,5 % (U-Net original partout), par tuile 7-12 % ; pire couche doublée 46-55 % (77 % au pire avec l'original) ; sur la tuile 3, faits de feuillets respectés 87,1 % (règle du vide seule) → 90,7 % (6 points par paire à 40 voxels) (§3).
- Raccord de tuiles : 95-99 % des points du recouvrement à moins de 3 voxels, couche suivante au mieux 6 % ou moins (WRITEUP §Summary, §5).
- Maillage : 6 contrôles sur 8 passés, 96,2 % sur papyrus, étirement 0,895-1,113 contre 0,90-1,10 exigé ; 124 246 sommets, 244 736 triangles (WRITEUP §6, chunk 2026-de-vore#009.2).
- Plus de contexte aide : score tuile 1 +0,81 (seule) → +0,88 (2 tuiles) → +0,89 (4 ou 6) (WRITEUP §9).

→ reportés dans `benchmarks.csv` (par l'agent principal, depuis `scratchpad/bench/2026-de-vore-vesuvius-ply-layers-separating-pressed.csv`) : 8 lignes — points sur papyrus (99,6), traversée de vide sombre (0,4), même feuillet (99,5), score d'encre 6 tuiles (+0,73), score d'encre tuile 1 (+0,89), faits de plis contredits moyens (9,3 %), pire couche doublée (55 %), auto-contrôles du maillage (6/8). Toutes `confidence: medium` (texte et tableaux du README/WRITEUP convertis en texte).

## Limites et critique

- **Statut** : dépôt non relu, un auteur, chiffres auto-déclarés, une couche sur un rouleau (PHerc. Paris 4) ; les réglages sont ajustés sur ce même rouleau. Les auteurs l'écrivent eux-mêmes (« tested on one scroll »).
- **Auto-vérification en partie circulaire (déduit)** : les « faits de plis » servent d'entrée au layering (priorité sur la règle du vide à 80 voxels) et de mesure du résultat (« ply facts broken ») ; le choix du checkpoint par tuile utilise ce même contrôle, et les auteurs précisent qu'il a été fixé après avoir vu les résultats par tuile (WRITEUP §4).
- **Métrique « sur le papyrus » favorable par construction (déduit)** : les traces sont semées sur les crêtes de brillance B puis la surface est placée au milieu de la bande brillante (MATH §4, §7b), et le juge est un seuil de brillance du même scan. 99,6 % mesure donc qu'on est sur un feuillet brillant, pas qu'on est sur le bon feuillet ni au bon endroit dans l'épaisseur (les auteurs le disent : « does not score where in the sheet a surface sits »). Autre mesure de la même surface : 96,2 % (auto-contrôle du maillage, tolérance différente), ce qui montre la sensibilité au protocole.
- **Comparaison à la référence humaine** : le segment officiel est un segment unique, semi-manuel ; les étiquettes d'encre ont été dessinées sur la surface officielle, ce qui avantage celle-ci, et le score de la surface automatique n'est mesuré que là où elle est à moins de 6 voxels de l'officielle (47,1 %, ou 9,9 % pour +0,89). La part de l'écart +0,73/+0,80 due à la référence plutôt qu'à la surface n'est pas élucidée (WRITEUP §8). Le modèle d'encre a peut-être vu cette région à l'entraînement : scores absolus possiblement optimistes. Le run d'encre est antérieur et non refait sur la surface finale.
- **Doublage résiduel** : pire couche 46-55 % doublée, aux bords de la pile ; une couche seulement est suivie et validée.
- **Deux U-Net** : le v1.1 sépare moins bien que le v1 sur les tuiles 1 et 4 ; le pourquoi est « inconnu » (WRITEUP §4). Le constat « plus de données = pire » repose sur peu de tuiles.
- **Résolution** : encre à 9,6 µm, traits environ 2 fois trop larges ; lecture à 2,4 µm annoncée comme prochaine étape, non testée.
- **Portée** : 6 tuiles environ 4,8 × 7,6 mm ; zones plissées ou non segmentées : hypothèse non testée ; couverture bien inférieure aux pipelines cités (ThaumatoAnakalyptor, HerculeX, solveur fibres de villa). Pas de comparaison chiffrée à ces méthodes ; pas de baseline hors segment officiel.
- Chiffres non cohérents ou ambigus relevés : tableau « Layer separation per tile » avec 7 valeurs pour 6 tuiles (la dernière semble une moyenne) et ordre des tuiles non lisible dans l'extraction ; « 6 de 8 contrôles » alors que 2 échouent de peu ; croisements de couches « à peu près égaux » mais plus élevés au seuil strict (0,46 contre 0,23) tout en classant « ours better » les autres lignes ; 87 % / 91 % de surface comparée au final contre 83 % / 65 % au run à 4 tuiles (les comparaisons ne portent pas sur la même zone).
- Comparaison à une baseline GPU/FPGA : sans objet (déduit).

## Pertinence pour la thèse

Axe segmentation de feuillets / déroulage : propose un signal complémentaire, l'ordre recto/verso des plis lu par tenseur de structure 2D, pour trancher les contacts pressés, là où la règle du vide sombre échoue ; relie à nos questions sur les zones écrasées et les kolleseis. Les sous-produits (étiquettes « même couche ou non » par point, 11 000-15 000 exemples difficiles par tuile, direction de pli, numéros de couche) sont réutilisables comme données d'entraînement ou de test, au prix de leur origine auto-générée. Le contrôle de surface sans étiquettes (`compare_surfaces.py`) est utilisable pour d'autres surfaces, avec la réserve ci-dessus. L'encre via un modèle externe (`ink_9um`) donne une évaluation indirecte du déroulage. Laisse ouvert : validation sur d'autres couches et rouleaux, lecture à 2,4 µm, comparaison à d'autres segmenteurs sur une même zone, vérification de l'hypothèse sur zones difficiles.

## Gaps identifiés

- Aucune validation indépendante du critère « plis » (pas de vérité terrain de couches pressées hors pipeline) : test sur paires étiquetées à la main.
- Une couche, un rouleau ; pas de comparaison chiffrée aux autres pipelines automatiques (ThaumatoAnakalyptor, HerculeX, solveur fibres de villa) sur une même zone.
- Effet du protocole de surface sur le score d'encre (étiquettes dessinées sur la surface officielle) : à mesurer avec des étiquettes indépendantes de la surface.
- Lecture de l'encre à 2,4 µm sur ces surfaces (relie à l'axe super-résolution / transfert de résolution).
- Lecture des plis à 9,6 µm seulement : quelle part du signal pli survit à plus basse résolution ?

## Statut de lecture

Papier complet (README, WRITEUP, MATH, TUNING ; `fulltext.md` lu en entier). Extraction `pymupdf`, `extraction.ok: false` : tableaux aplatis en texte (colonnes perdues, ex. tableau de raccord des tuiles et tableau « Layer separation per tile », en-têtes de colonnes disparus), images omises : les valeurs de ces tableaux sont lues dans le texte, ordre des tuiles et colonnes à confirmer. Pas de lignes `confidence: high` pour cette raison. Déduit et non affirmé par les auteurs : circularité des faits de plis, caractère favorable de la métrique « sur papyrus », absence de baseline hors segment officiel, mise en regard des deux valeurs 99,6 % / 96,2 %.
