---
id: arxiv-2304.02643-segment-anything
fiche: done
date: 2026-10-05
---

# Segment Anything

Alexander Kirillov, Eric Mintun, Nikhila Ravi, Hanzi Mao, Chloe Rolland, Laura Gustafson, Tete Xiao, Spencer Whitehead, Alexander C Berg, Wan-Yen Lo, Piotr Dollár, Ross Girshick, 2023, arXiv preprint. https://arxiv.org/abs/2304.02643
Type : preprint non relu par les pairs

## Problème

Il n'existe pas de source web de masques de segmentation à grande échelle (§4). Les auteurs veulent un modèle de fondation pour la segmentation, « promptable » (point, boîte, masque, texte), et le jeu de données qui l'entraîne. Le verrou de données est traité par un « data engine » : le modèle assiste l'annotation, et les masques collectés réentraînent le modèle (§1, §4).

## Méthode

- **Modèle SAM** : encodeur d'image ViT-H pré-entraîné MAE, entrée 1024×1024 obtenue par redimensionnement et padding du côté court (§A) ; encodeur de prompts (points, boîtes, masques, texte via CLIP) ; décodeur de masques léger (~50 ms dans un navigateur sur CPU, embedding précalculé, §3). Sortie à 3 masques par prompt pour lever l'ambiguïté (tout / partie / sous-partie), avec un score d'IoU estimé (§3).
- **Data engine en trois étapes** (§4) :
  - *Assisté-manuel* : annotateurs professionnels, clics avant/arrière-plan dans un outil navigateur propulsé par SAM, pinceau et gomme pour affiner ; pas de contrainte sémantique (« stuff » et « things »), objets par ordre de proéminence, passage à l'image suivante au-delà de 30 s par masque. 6 réentraînements du modèle (ViT-B vers ViT-H). Temps moyen par masque 34 s vers 14 s ; masques par image 20 vers 44 ; 4,3 M masques sur 120 k images. 14 s = 6,5 fois plus vite que l'annotation de masques COCO et seulement 2 fois plus lent qu'une boîte par points extrêmes (§4).
  - *Semi-automatique* : un détecteur de boîtes (classe générique « object ») entraîné sur les masques de l'étape 1 pré-remplit les masques confiants ; les annotateurs ajoutent les objets restants (moins saillants, plus difficiles). 5,9 M masques sur 180 k images (total 10,2 M) ; temps par masque remonté à 34 s (hors masques automatiques) ; 44 vers 72 masques par image (§4).
  - *Entièrement automatique* : grille régulière 32×32 de points, 3 masques par point ; filtres : IoU prédit ≥ 88,0, stabilité (IoU entre masques seuillés à -1 et +1 des logits ≥ 95,0), rejet des masques couvrant ≥ 95 % de l'image ; NMS à 0,7 (par boîtes) ; 20 recadrages zoomés supplémentaires (fenêtres 2×2 et 4×4, grilles 16×16 et 8×8) sur les images haute résolution d'origine pour améliorer les petits masques ; post-traitement : suppression des composantes < 100 px et bouchage des trous < 100 px (≈ 4 % de masques avec composantes parasites, ≈ 4 % avec trous parasites) (§4, §B). Appliqué aux 11 M d'images : 1,1 B de masques (99,1 % automatiques, §5).
- **Contrôle qualité de SA-1B** (§5) : 500 images (~50 k masques) corrigées par des annotateurs professionnels ; 94 % des paires auto/corrigé ont un IoU > 90 % et 97 % > 75 %, contre 85-91 % d'IoU d'accord inter-annotateurs rapporté dans la littérature [44,60]. Côté annotateurs : formation d'une semaine environ, contrôle par sondage de l'équipe QA du prestataire, retours hebdomadaires, 130 annotateurs (§F.2). Les masques manuels et semi-automatiques ne sont pas publiés ; SA-1B ne contient que les masques automatiques (§F.1, §5).
- **SA-1B** : 11 M d'images sous licence, 3300×4950 px en moyenne, publiées réduites à 1500 px sur le côté court, visages et plaques floutés (§5) ; ~100 masques par image ; sans catégorie ni texte (§F.1) ; plus de petits et moyens masques relatifs que les datasets existants (§5, Fig. 6).
- **SAM comme module de composition** : instance segmentation en promptant SAM avec les boîtes d'un détecteur (ViTDet-H) ; un raffinement supplémentaire réinjecte le masque le plus confiant avec la boîte (§7.4, §D.4). Entraînement : boîte du masque vérité avec bruit gaussien (écart-type 10 % du côté, max 20 px) (§A).

## Plateforme et implémentation

Entraînement sur 256 GPU (modèle par défaut, 90 k itérations, batch 256, AdamW, lr 8e-4, aucune augmentation de données ; §A). Inférence : encodeur lourd (non temps réel), décodeur ~50 ms CPU (§3, §8). Code et poids publiés sous licence Apache 2.0 (https://segment-anything.com) ; SA-1B publié pour la recherche sous licence spécifique (Intro, Release). Outil d'annotation propriétaire, non publié (§F.2).

## Résultats

- Annotation : 34 s vers 14 s par masque (étape 1), 34 s (étape 2), masques/image 20 vers 44 vers 72 (§4). Comptes : 4,3 M + 5,9 M = 10,2 M masques manuels/semi-auto ; 1,1 B au total (§4, §5).
- Qualité SA-1B : 94 % des masques à IoU > 90 % avec la correction humaine (§5).
- Ablation data engine : chaque étape améliore le mIoU sur 23 jeux ; entraîner sur les seuls masques automatiques coûte ~0,5 mIoU (Fig. 13 gauche, §7.6) ; ~1 M d'images (10 %, ~100 M masques) donne un résultat comparable au jeu complet, 0,1 M chute nettement (Fig. 13 milieu, §7.6).
- Un point central, 23 jeux : SAM meilleur que RITM sur 16 des 23 (jusqu'à ~47 IoU) ; notes humaines de SAM entre 7 et 9 (§7.1).
- Instance segmentation zero-shot (boîtes ViTDet-H) : mask AP COCO 46,5 (ViTDet-H : 51,0), LVIS 44,7 (46,6) ; par taille COCO AP_S 30,8 vs 32,0, AP_L 61,7 vs 68,9 (Table 5). Notes humaines SAM supérieures à ViTDet (Fig. 11), ce que les auteurs attribuent à des biais d'annotation COCO/LVIS qu'un modèle supervisé apprend et pas SAM (§7.4).
- Propositions d'objets LVIS AR@1000 : SAM 59,3 (petits 45,5) vs ViTDet-H 63,0 (petits 51,7) ; SAM meilleur sur moyens, grands, rares, communs, moins bon sur petits et fréquents (§7.3, Table 4).
→ reportés dans `benchmarks.csv` : 3 lignes proposées (Table 5 COCO et LVIS ; Table 4 AR@1000), à intégrer par l'agent principal.

## Limites et critique

- Les auteurs : SAM peut manquer des structures fines, halluciner de petites composantes déconnectées, et ses frontières sont moins nettes que celles de méthodes « zoom-in » ; il n'est pas conçu pour un IoU très élevé avec beaucoup de points ; des outils spécialisés le surpassent dans leur domaine ; l'encodeur lourd n'est pas temps réel (§8). Il est moins bon que ViTDet sur les petits objets en propositions (§7.3) et sur AP_S/AP_L en instance segmentation (Table 5).
- Pas de classes : SA-1B n'a ni catégorie ni texte (§F.1) ; SAM ne produit que des masques. Pour obtenir des classes il faut un détecteur ou un autre modèle ; le texte vers masque est exploratoire et peu robuste (§7.5, §8).
- Ambiguïté (tout / partie / sous-partie) : en un seul clic, le masque choisi n'est pas forcément l'objet voulu ; l'IoU « oracle » masque cet effet (§7.1). Les consignes d'annotation de « ce qu'est un objet » sont subjectives (deux bottes en un ou deux masques, §F.2).
- Le coût d'annotation 14 s/masque et les temps par étape viennent d'annotateurs professionnels entraînés avec un outil dédié ; non transposable tel quel à un annotateur occasionnel (déduit).
- Qualité SA-1B : mesurée par IoU avec une correction faite à partir du même modèle et du même outil (§5), donc susceptible de sous-estimer l'erreur systématique du modèle ; aucune mesure par classe ni par taille (déduit). Les ~4 % de masques à composantes ou trous parasites sont corrigés par seuil à 100 px, ce qui supprime aussi de vrais très petits objets (déduit).
- Tableaux 4 et 8 « sans corps extrait » (warnings d'extraction) : les valeurs de la Table 4 retenues viennent d'un fragment de texte, `confidence: medium`.
- Preprint ; le jeu de 23 datasets de test est choisi par les auteurs ; pas de mesure de l'usage de SAM pour des boîtes de détection (déduit : voir Pertinence).

## Pertinence pour la thèse

**Pertinence (thème de la base).**
- *Annoter* : SAM est l'outil d'annotation interactive le plus utile pour produire des masques (et, par extension, des boîtes). Un clic ou une boîte grossière donne un masque ; l'annotateur n'a qu'à corriger. Coût de référence mesuré : 14 s par masque (étape 1) contre ~91 s déduit pour COCO via le facteur 6,5 (§4), et seulement 2 fois plus lent que des boîtes par points extrêmes. Pour une base de boîtes pures, un détecteur ou des points extrêmes restent plus économiques par instance (déduit) ; SAM vaut le coup si l'on veut aussi des polygones ou masques (YOLO-seg) ou des boîtes serrées.
- *Boîtes à partir de SAM* (déduit, non évalué par les auteurs) : la boîte englobante d'un masque SAM fournit une boîte serrée à partir d'un clic. Le papier n'évalue pas la précision de ces boîtes pour entraîner un détecteur. Limites héritées de SAM : objets fins (câbles, poteaux, antennes), petits objets (AP_S inférieur, §7.3, Table 5) et composantes parasites qui gonflent la boîte ; SAM ne donne pas la classe (aucune catégorie, §F.1).
- *Auto-labelling* : la grille de points + filtres IoU/stabilité (§B) est une recette de pré-annotation complète ; en la couplant à un détecteur ouvert (Grounding DINO, déduit, hors papier) ou à un classifieur on obtiendrait des labels classés. Le papier montre le schéma boîte vers masque (ViTDet vers SAM, §7.4), pas masque vers classe.
- *Contrôle qualité de labels* : méthode transférable : réviser par un professionnel un échantillon (500 images) et comparer en IoU ; seuils de filtrage IoU prédit/stabilité. Comparaison avec l'accord inter-annotateurs 85-91 % (§5).
- *Prétraitement* : recadrages zoomés à plusieurs échelles sur l'image haute résolution pour améliorer les petits masques (§B) ; même logique que le tiling/SAHI, à l'annotation plutôt qu'à l'inférence. Entrée du modèle 1024×1024 avec padding (§A).
- *Augmentation / volume* : large-scale jitter [0,1 ; 2,0] employé quand les données sont limitées (§A) ; ~1 M d'images suffit, 0,1 M non (§7.6) : repère d'ordre de grandeur, non transposable à la détection.
- *À appliquer quand* : pré-annotation de masques ou de boîtes serrées pour une nouvelle classe sans modèle de détection existant ; nettoyage de labels (comparer boîte vérité et boîte du masque SAM promptée par cette boîte, déduit) ; pas pour des objets filiformes ni à très petite taille sans zoom.

## Gaps identifiés

- Précision des boîtes dérivées des masques SAM et effet sur le mAP d'un détecteur YOLO entraîné dessus : non mesurés ici.
- Comportement de SAM sur objets fins et petits (aérien, drone) : seulement qualitatif/indirect (§8, Table 5).
- Coût d'annotation d'une boîte avec SAM par un annotateur non expert : n/r.
- Association classe-masque (SAM + détecteur ouvert) : hors papier.

## Statut de lecture

papier complet (fulltext.md lu en entier, annexes et cartes F.1/F.2 comprises). Extraction GROBID `ok`, mais Table 4 et Table 8 « sans corps extrait » (légende seule) et une figure sans légende : la Table 4 a été relue à partir d'un fragment de texte (medium).
Ce qui suit est déduit et non affirmé par les auteurs : l'emploi des boîtes de masques SAM comme labels de détection et ses limites (objets fins, petits, parasites) ; le coût d'annotation COCO en secondes (14 s × 6,5) ; la non-transposabilité des temps à un annotateur non entraîné ; la sous-estimation possible de l'erreur par la méthode de contrôle qualité ; les couplages avec Grounding DINO.
