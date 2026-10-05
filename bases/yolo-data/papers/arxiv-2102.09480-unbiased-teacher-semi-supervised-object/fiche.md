---
id: arxiv-2102.09480-unbiased-teacher-semi-supervised-object
fiche: done
date: 2026-10-05
---

# Unbiased Teacher for Semi-Supervised Object Detection

Yen-Cheng Liu, Chih-Yao Ma, Zijian He, Chia-Wen Kuo, Kan Chen, Peizhao Zhang, Bichen Wu, Zsolt Kira, Peter Vajda, 2021, arXiv preprint. https://arxiv.org/abs/2102.09480
Type : preprint non relu par les pairs (publié ensuite à ICLR 2021 selon ma connaissance, non vérifié dans le corpus)

## Problème

Entraîner un détecteur avec peu d'images annotées et beaucoup d'images sans label (SS-OD). Les
auteurs identifient un « biais de pseudo-labels » : le déséquilibre fond/objet et entre classes
(le fond pèse ~70 % des instances ; « person » ~30 % des instances d'objets de COCO, §3.3) pousse
le modèle à prédire les classes dominantes, et les pseudo-labels biaisés aggravent le déséquilibre.
Avec peu de labels, les classifieurs RPN et ROI sur-apprennent, pas la régression de boîte (Fig. 2).

## Méthode

Deux étapes (§3, Fig. 3). (1) Burn-In : entraînement supervisé sur les images annotées (§3.1).
(2) Teacher-Student mutual learning (§3.2) : le Teacher génère des pseudo-labels sur des images
faiblement augmentées ; le Student apprend sur les mêmes images fortement augmentées ; le Teacher
est mis à jour par EMA des poids du Student (θt ← αθt + (1-α)θs).
Points pratiques :
- **Filtrage des pseudo-labels** : NMS par classe puis seuil de confiance δ = 0,7 pour tous les
  essais (§4, A.4). Pas de perte de régression de boîte sur les pseudo-labels (seule la
  classification RPN et ROI est supervisée), car la confiance ne mesure pas la qualité de
  localisation (§3.2, Éq. 2).
- **Augmentations** : faible = flip horizontal ; forte = color jitter, niveaux de gris, flou
  gaussien, cutout. Aucune augmentation géométrique (STAC en utilise), hyperparamètres d'augmentation
  non optimisés (§4, A.4, Table 6 citée, non extraite).
- **Déséquilibre** : Focal loss multi-classe sur le classifieur ROI (§3.3) + EMA, qui stabilise
  la frontière de décision (§3.3, Éq. 4).
- Entraînement : Detectron2, Faster R-CNN FPN ResNet-50 init. ImageNet, SGD momentum 0,9, lr 0,01
  constant, batch 32 supervisé + 32 non supervisé, 180k itérations (COCO-standard) dont burn-in de
  1/2/6/12/20k itérations pour 0,5/1/2/5/10 % ; λu = 4 (COCO-standard, VOC), λu = 2 (COCO-additional) ;
  α = 0,9996 (A.4).

## Plateforme et implémentation

Logiciel : Detectron2. Matériel d'entraînement : n/r. Code : une note de bas de page « Unbiased
Teacher 1 » du résumé renvoie à une page de code, mais le lien n'est pas dans le texte extrait :
à vérifier. Pas de FPGA ni d'embarqué.

## Résultats

Métrique : AP50:95 (« mAP »), mesurée sur le Teacher (§4).
COCO-standard, part annotée (Table 1), Unbiased Teacher vs supervisé / STAC :

| Part annotée | 0,5 % | 1 % | 2 % | 5 % | 10 % |
|---|---|---|---|---|---|
| Supervisé | 6,83 | 9,05 | 12,70 | 18,47 | 23,86 |
| STAC | 9,78 | 13,97 | 18,25 | 24,38 | 28,64 |
| CSD* | 7,41 | 10,51 | 13,93 | 18,63 | 22,46 |
| Unbiased Teacher | 16,94 | 20,75 | 24,30 | 28,27 | 31,50 |
| Gain vs supervisé | +10,11 | +11,72 | +11,60 | +9,80 | +7,64 |

Le gain décroît quand la part annotée augmente. 1 % annoté (20,75) dépasse STAC à 2 % (18,25) et le
supervisé à 5 % (18,47) (§4.1). Écart vs STAC à 1 % : 20,75 − 13,97 = 6,78 (résumé : 6,8).
COCO-additional (Table 2) : 41,30 vs supervisé 1x 37,63, supervisé 3x 40,20, STAC 6x 39,21 ; le gain
réel à budget d'itérations égal (3x) n'est que de +1,10 (§4.1).
VOC07 labellisé + VOC12 non labellisé (Table 3, colonnes possiblement décalées) : 48,69 AP50:95
(+6,56 vs supervisé 42,13) ; avec COCO20cls en plus : 50,34 (+8,21).
Ablations (COCO-standard 1 %, §4.2, Fig. 5) : entropie croisée sans EMA 13,42 ; Focal sans EMA 17,85 ;
entropie croisée avec EMA 16,91 ; Focal + EMA 21,19. Divergence KL entre distribution de classes des
pseudo-labels et vérité : 1,7915 → 0,2001 (Focal) / 0,2482 (EMA) / 0,0851 (les deux).
Hyperparamètres (annexe) :
- seuil δ : 0,9 trop peu de boîtes, 0,6 trop de faux positifs, divergence sous 0,5 (A.2.2, valeurs
  de mAP dans la Fig. 8-9, non extraites) ; 0,7 retenu ;
- α EMA : 0,5 instable, meilleur à 0,99 (Fig. 10), 0,9999 trop lent ; 0,9996 utilisé (A.4, écart
  avec « 0,99 meilleur » non expliqué) ;
- λu (10 % annoté, Table 4) : 1,0 → 29,30 ; 2,0 → 30,64 ; 4,0 → 31,82 ; 5,0 → 32,00 ; 6,0 → 31,80 ;
  8,0 diverge ;
- burn-in : accélère la montée en précision des pseudo-boîtes (A.2.1, Fig. 7).
→ reportés dans `benchmarks.csv` : 8 lignes proposées (COCO-standard 0,5/1/2/5/10 %, COCO-additional,
VOC07+VOC12, VOC07+VOC12+COCO20cls), toutes `mAP50-95`, plateforme `n/r`.

## Limites et critique

- Détecteur à deux étages (Faster R-CNN) : aucune expérience sur un détecteur à un étage de type
  YOLO ; Focal loss sur la tête ROI et pertes RPN n'ont pas d'équivalent direct. Le papier note même
  que la Focal loss dégrade YOLOv3 en supervisé (§3.3, affirmé sans mesure ici).
- Pas de régression de boîte sur les pseudo-labels : les pseudo-labels ne corrigent que la classification.
- Le seuil 0,7 et les augmentations sont réglés sur COCO/VOC ; pas d'étude sur un domaine différent,
  des petits objets ou un dataset très déséquilibré (80 classes COCO seulement).
- Gain faible avec toutes les annotations (+1,10 sur COCO-additional à 3x, Table 2).
- Comparaison : CSD réimplémenté par les auteurs (*), STAC 0,5 % issu du code publié (légende Table 1) ;
  STAC 6x vs Ours 3x en Table 2 : budgets d'entraînement différents. Écarts-types fournis seulement
  pour COCO-standard.
- Pas de mesure du coût d'annotation évité ni du nombre d'instances par classe.

## Pertinence pour la base

Pour **AUGMENTER/ANNOTER** un dataset de détection avec peu de labels (annotation semi-automatique) :
- Quand l'appliquer : peu d'images annotées (≤ 10 % de COCO, soit ~12k images pour 10 %) et un grand
  stock d'images brutes du même domaine. C'est là que le gain est le plus fort : ~+10 mAP à 0,5-5 %,
  +7,6 à 10 %, ~+1 avec 100 % annoté (Tables 1-2). Au-delà d'environ 10 %, le bénéfice devient marginal.
- Recette de pseudo-labels pour **CONSTRUIRE** le dataset : (1) entraîner d'abord un modèle sur les
  images annotées ; (2) NMS par classe puis seuil de confiance ~0,7 (pas en dessous de 0,5 : divergence ;
  0,9 : trop peu de boîtes) ; (3) Teacher en EMA lent (α ≈ 0,99-0,9996) plutôt que modèle figé ou partagé ;
  (4) pseudo-labels générés sur vue faible, apprentissage sur vue forte (couleur, flou, cutout) ;
  (5) surveiller la distribution de classes des pseudo-labels (KL vs vérité) : sans EMA ni Focal,
  la plupart des classes disparaissent des pseudo-labels (§4.2).
- **PRÉTRAITER/AUGMENTER** : la paire faible/forte utilisée ici est volontairement non géométrique ;
  la cohérence géométrique des boîtes n'est pas à gérer. Mosaic/MixUp/Copy-Paste ne sont pas testés.
- **Déséquilibre** : l'effet est quantifié ici sur les pseudo-labels, pas sur les labels humains :
  les classes rares sont perdues si l'on réutilise un modèle biaisé.
- Pour un praticien YOLO : idée transférable (seuil de confiance, EMA, vue faible/forte,
  contrôle de la distribution de classes), mais non démontrée sur YOLO ; prévoir de vérifier à la main
  un échantillon des pseudo-labels, car aucun contrôle de qualité de localisation n'est proposé.

## Gaps identifiés

- Semi-supervisé sur détecteurs à un étage (YOLO) : aucun résultat dans ce papier.
- Domaines spécifiques (petits objets, drone, peu de classes) : non couverts.
- Pas de comparaison pseudo-labels vs annotation humaine supplémentaire à coût égal.
- Pas de guide du nombre d'images annotées minimal par classe.

## Statut de lecture

papier complet (fulltext.md entier ; extraction GROBID). Table 4 déclarée « sans corps extrait » dans
`extraction.warnings`, mais ses valeurs figurent dans le texte (A.2.4) et le fragment de tableau ; Table 3
a des colonnes mal alignées (confidence `medium`) ; Tables 5-6 (hyperparamètres, augmentations) et
Fig. 8-10 (courbes) ne sont pas extraites : les valeurs de mAP selon δ et α sont donc inconnues.
Déduit et non affirmé par les auteurs : le bénéfice pour YOLO, la limite « d'environ 10 % » comme point de
bascule (seule la tendance décroissante est montrée), le lien du code, la publication ICLR.
