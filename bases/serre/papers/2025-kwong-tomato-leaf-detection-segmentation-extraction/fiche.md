---
id: 2025-kwong-tomato-leaf-detection-segmentation-extraction
fiche: done
date: 2026-10-29
---

# Tomato Leaf Detection, Segmentation, and Extraction in Real-Time Environment for Accurate Disease Detection

Foong Kwong, Sotirios K Goudos, Shahab Ul Islam, Giampaolo Ferraioli, Vito Pascazio, 2025, AgriEngineering 2025, 7(4), 120 (revue ; numéro et volume tirés de l'en-tête de page « AgriEngineering 2025, 7, x » du texte, venue absente de metadata.json avant cette fiche). https://doi.org/10.3390/agriengineering7040120
Type : article de revue (relu par les pairs, MDPI) ; à confirmer sur la page éditeur.

## Problème

Les modèles de maladies sont entraînés et testés sur des images « synthétiques » (feuille isolée) et perdent en précision quand on leur donne l'image de la plante entière ; il faut donc détecter et extraire chaque feuille avant la classification (Abstract).

## Méthode

Pipeline à étapes : YOLOv8 détecte les feuilles (boîtes), SAM ViT-H (checkpoint `sam_vit_h_4b8939.pth`) segmente dans chaque boîte, masque raffiné par érosion/dilatation, feuille découpée et redimensionnée à 640 × 640 (bilinéaire), puis « fournie à un réseau profond » pour la maladie (§3.3, 2025-kwong#017.0). Les étiquettes de boîtes viennent d'**autodistill** : un modèle de base (GroundedSAM) annoté par une ontologie texte (« leaf » = « tomato leaf ») produit le jeu qui entraîne YOLOv8 (§3.2, 2025-kwong#016.0). YOLOv8 initialisé sur COCO, 640 × 640, batch 16, 100 époques, lr 0,001, Adam (§3.2). Jeu : 11 493 images « Tomato Village », découpe 70/20/10 (§3.1, 2025-kwong#013.0), augmentations rotation, flip, luminosité. Le classifieur de maladie n'est ni décrit ni évalué.

## Plateforme et implémentation

2 GPU NVIDIA GeForce GTX 1080 Ti 12 Go, pour SAM (§3.3, 2025-kwong#018.0) ; la variante YOLOv8 (n/s/m…) n'est pas précisée ; aucune quantification, aucun matériel edge. Puissance : n/r. Code et poids : non publiés (aucun lien dans le texte lu).

## Résultats

- Test (1 150 images, 4 086 instances) : précision 100 %, rappel 98 %, mAP@50 90 %, 142 ms par image (Table 1, 2025-kwong#051.0). Texte : mAP 90,7 % à confiance 0,5 (§4, 2025-kwong#029.0), écart non expliqué avec 90 % de la Table 1.
- Segmentation : Dice moyen 88 %, exactitude pixel 80,78 % (§4, 2025-kwong#030.3) ; F1 84 % à seuil 0,612 (Fig. 4d).
- Latence moyenne sur 100 passages : 142 ms, usage GPU 71,19 % (§5, 2025-kwong#032.2).
- Table 2 (2025-kwong#053.0) : YOLOv5-X 608² 88/85/80 %, 415 ms ; YOLOv6-L 89/81/91 %, 400 ms ; YOLOv7 87/83/91 %, 278 ms ; YOLOv8-SAM 960² 92/83/89 %, 198 ms ; ce travail 640² 100/98/90 %, 142 ms (précision/rappel/mAP).
→ reportés dans `benchmarks.csv` : 3 lignes proposées à l'agent principal (test Tomato Village, segmentation, Table 2 YOLOv8-SAM).

## Limites et critique

- Le titre promet la « détection de maladie en temps réel » : aucun résultat de classification de maladie, ni sur feuille extraite ni sur plante entière. L'hypothèse de départ (la découpe améliore la maladie) n'est pas testée.
- Test in-domain : les 10 % de test viennent du même jeu que l'entraînement ; étiquettes **pseudo-annotées** par GroundedSAM, donc la « vérité terrain » est celle d'un autre modèle, et la précision 100 % mesure surtout l'accord avec lui. Les masques « de vérité terrain » pour Dice/IoU ne sont pas décrits.
- « Temps réel » : 142 ms (≈ 7 fps) sur 2 GTX 1080 Ti, SAM ViT-H lourd ; pas d'edge. Table 2 : résolutions différentes (608/640/960), sources des baselines citées d'autres travaux (réf. 30-33), non réentraînées (déduit) ; « 0,90 % » écrit pour mAP dans §5 (coquille).
- Incohérences : mAP 90,7 % (texte) vs 90 % (Table 1) ; Table 1 lignes training/validation décalées entre texte (validation P 99,7 %, mAP 89,4 %) et tableau (ligne training) ; IoU annoncé mais non chiffré ; pas de faux positifs sur images sans feuille ou saines ; pas d'ablation YOLO seul vs YOLO+SAM chiffrée (« augmentation notable » sans valeur).
- Reproductibilité faible : variante YOLOv8, jeu et seuil de confiance non détaillés.

## Pour SerreIA

**Comparabilité : non.** Jeu Tomato Village (feuilles de tomate sur plante, une seule classe « feuille »), test in-domain tiré du même jeu, labels pseudo-générés ; SerreIA mesure mAP@0,5 0,956 sur son test (flatté par PlantVillage) et 42 % de faux positifs sur images saines hors domaine. Les chiffres 100/98/90 % ne se comparent ni à ces mAP ni au test PlantDoc (rappel 0,986, précision 0,679) ; et la latence 142 ms est sur 2 GTX 1080 Ti, pas Hailo-8L INT8. Seul usage : ordre de grandeur de ce qu'un détecteur de feuilles de plante entière atteint en in-domain (~0,90 de mAP@50).

Ce que le projet peut en reprendre :
- **Autodistill / GroundedSAM pour pré-annoter** les feuilles (ontologie « leaf » = « tomato leaf ») : candidat pour `vision/labeling/pseudo_labels.py` et `build_yolo_dataset.py`, avec revue humaine via `label_studio.py` / `active_learning.py` ; mesurer le taux d'accord pseudo-labels vs étiquettes manuelles sur un échantillon avant de s'y fier (le papier ne le fait pas).
- **Masque SAM du crop avant classification** = remplacement de fond par segmentation, la parade prévue mais jamais testée (`data/backgrounds/` absent). Expérience : sur PlantDoc, comparer dans `vision/eval/cross_domain_eval.py` et `two_stage.py` trois entrées (crop boîte, crop masqué fond noir/uni, image entière) avec le même classifieur ; métriques : précision, spécificité, F1 classe « anormal », ECE, taux de faux positifs sur images saines. SAM sert hors ligne (génération de masques d'entraînement), pas sur Pi : il est trop lourd, YOLOv8n + classifieur restent l'inférence edge.
- **Évaluer le détecteur hors domaine** : mesurer le mAP du YOLOv8n de feuilles sur des images de serre réelles/PlantDoc, pas seulement le test Tomato Village/PV ; le papier illustre le risque inverse (test in-domain, pseudo-labels).
- Piste, non démontrée par le papier : la découpe par feuille n'est pas prouvée utile pour la maladie ; l'ablation « classifieur sur image entière vs crops vs crops masqués » reste à faire chez SerreIA (docs/15, docs/17 §10).

## Gaps identifiés

- Aucun chiffre de classification de maladie sur crops extraits vs image entière (question « deux étages vs image entière »).
- Pas de mesure de faux positifs du détecteur de feuilles sur images saines/sans feuille.
- Pas de latence edge (Pi/Hailo) pour détecteur + segmenteur ; SAM seul est GPU.

## Statut de lecture

Sections lues : résumé, §3 (méthodes), §4 (résultats), §5 (discussion), tableaux 1 et 2. Introduction et état de l'art (lignes 12-93) non relus : papier non complet. Extraction `grobid`, texte dupliqué par endroits (paragraphes répétés), Tables 1-2 reconstruites depuis le texte, colonnes à recouper (confidence `medium`).
Déduit, non affirmé par les auteurs : baselines de Table 2 non réentraînées ; pas de code publié (absence de lien dans les parties lues) ; équivalence « ≈ 7 fps » = 1000/142 ; type « revue » d'après AgriEngineering ; coquille « 0,90 % ».
