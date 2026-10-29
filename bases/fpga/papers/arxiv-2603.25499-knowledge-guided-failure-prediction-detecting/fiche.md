---
id: arxiv-2603.25499-knowledge-guided-failure-prediction-detecting
fiche: done
date: 2026-10-26
benchmarks: none
---

# Knowledge-Guided Failure Prediction: Detecting When Object Detectors Miss Safety-Critical Objects

Jakob Paul Zimmermann, Gerrit Holzbach, David Lerch, 2026, arXiv preprint (2603.25499). https://arxiv.org/abs/2603.25499
Type : preprint non relu par les pairs. Le texte porte la note « Accepted at the SAIAD Workshop, CVPR 2026 » (note de bas de page de l'introduction) ; `metadata.json` garde la venue « arXiv preprint ».

## Problème

Un détecteur d'objets déployé en environnement critique peut échouer en silence (personnes ou ouvriers non détectés, sans alerte) (Abstract, §1). Les méthodes OOD classiques repèrent la nouveauté d'une entrée, pas l'échec fonctionnel du détecteur (Abstract). Les auteurs posent la prédiction d'échec comme une classification binaire supervisée : l'image contient-elle au moins un objet critique (ici une personne) que le détecteur manque (IoU < 0,5) ? (§1, §3.1, Éq. 1). Ils visent aussi la fatigue d'alarmes : ne pas signaler une nouveauté bénigne (§1).

## Méthode

- Détecteur : YOLOv8l gelé, entraîné sur COCO train ; features de la FPN P3/P4/P5 (256/512/512 canaux, 80×80, 40×40, 20×20 pour une entrée 640×640) (§3.2).
- Modèle auxiliaire (« world knowledge ») : embedding [CLS] de DINO ViT-B (768 d, image 518×518), gelé, pré-calculé en cache HDF5 (§3.2, §4.2).
- Moniteur (KGFP) : attention inter-échelles avant fusion, patchification 4×4, 2 blocs de self-attention puis 2 de cross-attention (requêtes = YOLO, clés/valeurs = DINO), 8 têtes ; deux encodeurs vers un espace partagé de 64 d (DINO : MLP à 5 couches 768→1024→768→640→512→64) ; score = cosinus entre les deux embeddings, converti en p = (1-s)/2 (§3.2, §3.3). Plus l'angle est grand, plus l'image est jugée dangereuse.
- Entraînement : perte BCE sur l'étiquette sûr/non sûr, LARS, 60 époques, batch 6, lr 0,00095 (§3.3, §4.2). Seul le moniteur est entraîné ; le détecteur reste figé (§4). Étiquette calculée avec un seuil de certitude 0,5 et IoU 0,5 (§4.1).
- Utilisation : porte de prédiction sélective au niveau de l'image. Elle rejette les images jugées dangereuses et ne modifie pas les détections (§5.1). Seuil fixé sur validation ID à 5 % de FPR (0,843 pour le modèle complet) (§3.3).
- Baselines : GRAM, KNN, ViM adaptées aux features YOLOv8, entraînées sur images sûres seulement ; DINO-MLP, DINO-ViM ; têtes MLP (§4.4).

## Plateforme et implémentation

Aucune plateforme matérielle : GPU non précisé, pas de FPGA, Jetson ni MCU. Rien sur la précision numérique (quantification) ni sur la puissance (n/r). Code, modèles et features publiés : https://gitlab.ccasp.fraunhofer.de/iosb_public/KGFP (Abstract). Poids du détecteur (YOLOv8l) et de DINO : modèles publics ; ce que le dépôt contient précisément n'a pas été vérifié ici.
Coût du moniteur : 2,6 M de paramètres pour la configuration 64 d (§5.2, hors YOLOv8l et DINO ViT-B de 86 M). Il exige les deux passes avant (YOLOv8 et DINO) ; les auteurs disent que la latence vient surtout des backbones et que la tête est négligeable, sans chiffre de latence ni de FLOPs (§6, « Limitations »). Pistes évoquées : saut d'images (vérification toutes les N images), compression, distillation.

## Résultats

Données : classe « person » de COCO 2017, 64 115 images d'entraînement (split 90/10 entraînement/validation pour le seuil), 2 693 images de test (COCO val), 10 777 personnes annotées en val ; hors distribution : six domaines de COCO-O (cartoon, sketch, painting, handmake, tattoo, weather) (§3.3, §4.1). Pas de données de vidéosurveillance ni de site industriel.

- Rappel des personnes parmi les images acceptées à 5 % de FPR : 64,3 % (YOLOv8 sans porte) → 84,5 % (KGFP) sur COCO val ; 66,1 % → 71,4 % sur COCO-O weather (§5.1). Réduction relative des personnes manquées : 56,6 % (COCO val) et 15,6 % (COCO-O weather) (§5.1). Le Tableau 1 n'est pas dans `fulltext.md` : ces valeurs viennent du texte.
- Baselines sur COCO val : GRAM, KNN, ViM 65,1 à 65,5 % ; DINO-MLP 69,1 % ; DINO-ViM 65,2 % ; KGFP +15,4 points sur la meilleure (§5.1).
- COCO-O, moyenne des six domaines : KGFP 34,2 % de rappel ; peintures 36,2 %, handmake 37,0 % ; KNN meilleur sur handmake (38,5 %) et ViM sur sketch (34,1 % contre 29,5 %) (§5.1, §5.3).
- Tableau 2 : AUROC sûr/non sûr 92,9 % (KGFP) contre 52,5 à 54,3 % (GRAM, ViM, KNN) sur COCO val ; AUC du rappel 90,4 % ; moyenne COCO-O : AUROC 80,3 %, AUC du rappel 55,8 % (KGFP) contre 52,4 à 68,9 % d'AUROC pour les baselines (Table 2).
- Ablations (Table 3, §5.2) : sans attention 82,3 % ; tête MLP à la place du cosinus 83,7 % ; DINO ViT-B 85,1 % contre CLIP 84,5 %, DINOv2 84,4 %, SigLIP 84,8 % ; 64 d meilleur que 128, 256, 512 d ; LARS meilleur qu'Adam.
→ reportés dans `benchmarks.csv` : aucune ligne. Le papier ne mesure rien sur plateforme matérielle (GPU de bureau seulement, non précisé) ; les résultats sont des métriques de précision de détection de panne.

## Limites et critique

Limites déclarées (§6) : dépendance à un encodeur de fondation gelé ; étiquette tout-ou-rien (au moins une personne manquée) ; une seule classe ; surcoût de latence non mesuré ; attaques adverses non traitées ; adaptation continue de l'encodeur laissée en travaux futurs.
Critique (déduit, sauf mention) :
- Le moniteur est conçu pour un détecteur donné et reste séparé : le détecteur est gelé et entraîné à part, il n'y a ni entraînement conjoint, ni sortie anticipée, ni intégration dans le réseau. Le signal tombe après les deux passes complètes, donc pas d'alerte précoce.
- Le niveau de décision est l'image entière, pas la personne ni la région ; pas de localisation de l'échec.
- Comparaison déséquilibrée, reconnue en §5.3 : KGFP est supervisé avec des étiquettes d'échec, les baselines OOD sont non supervisées (images sûres seulement) ; seuls DINO-MLP et la tête MLP sont comparables en supervision.
- Les performances hors distribution sont faibles en absolu : 34,2 % de rappel moyen sur COCO-O, alors que la conclusion écrit « 85 % de rappel à 5 % de FPR sur les données ID et les domaines nouveaux » ; ce chiffre est contredit par les résultats de §5.1 (84,5 % ID, 34,2 % COCO-O en moyenne). Seul « weather » reste proche de l'ID (71,4 %).
- Le « rappel parmi les images acceptées » est un rappel conditionné au filtrage : la métrique ne dit pas combien de personnes manquées passent sans alarme en valeur absolue, ni le taux d'images rejetées utiles. Le FPR est défini comme taux de fausses alarmes sur les images sûres de validation ID (inférence d'après §4.3, Tableau 1 absent).
- Pas de seuil ni de taux d'alarme sur flux vidéo (corrélation temporelle entre images, alarmes successives) ; un seul run apparent, pas d'intervalle de confiance ni d'écart-type rapporté (n/r).
- Les personnes de COCO (photographies diverses) ne représentent pas une scène industrielle fixe ; pas de test sur site ni sur EPI.
- Le texte invoque le SIL 4 comme motivation (§1) sans aucun argument d'assurance (couverture, taux de défaillance dangereuse) : revendication de sûreté non étayée.
- Ni quantification, ni virgule fixe, ni WCET, ni analyse de fautes matérielles.

## Pertinence pour la thèse

Travail le plus proche du sujet ARCYS (prédiction d'échec ciblée sur le faux négatif critique, personnes, YOLO). Détecteur : YOLOv8l ; modèle auxiliaire : DINO ViT-B (86 M de paramètres) ; données : classe « person » de COCO + COCO-O ; métriques : rappel des personnes parmi les images acceptées à 5 % de FPR, AUROC sûr/non sûr, AUC rappel (le taux d'alarme est le FPR fixé à 5 %). Code et modèles publiés, donc une comparaison directe (mêmes étiquettes, mêmes splits COCO person) est faisable comme référence de comparaison pour la thèse.
Axes `safety-certification`, `person-detection`, `failure-prediction`.

Ce qui reste ouvert pour la thèse (différenciation, déduit de la comparaison avec le draft) :
- Entraînement et intégration conjoints du moniteur dans le détecteur, contre un moniteur externe sur détecteur gelé qui coûte une seconde passe avant avec un modèle de 86 M de paramètres.
- Alertes précoces (sorties anticipées comme signal conservateur) contre une alerte émise après les deux passes complètes.
- Implantation FPGA : aucune mesure de latence, de ressources ni de puissance ; un backbone DINO ViT-B est lourd pour un FPGA embarqué, un moniteur léger sur les features du détecteur est un contrepoint naturel.
- Analyse temporelle et matérielle : délai de réaction de bout en bout, WCET, interférences ; la proposition de saut d'images de KGFP pose la question du délai de détection, non traitée.
- Effet de la quantification (virgule fixe) sur le moniteur et sur la décision critique ; distinction erreur de perception / anomalie d'exécution / défaillance temporelle : ici seule l'erreur de perception est traitée.
- Données de scène industrielle ou de vidéosurveillance, évaluation temporelle sur flux, taux d'alarme par heure.

## Gaps identifiés

- Prédiction d'échec de détecteur sans mesure sur cible embarquée (latence, puissance, FPGA) : aucun chiffre de coût du moniteur.
- Moniteur supervisé sur détecteur gelé, jamais entraîné conjointement avec le détecteur.
- Évaluation sur images isolées COCO, pas sur flux vidéo ni en environnement industriel.
- Absence d'argument d'assurance (taux de faux négatifs non détectés résiduel) malgré une motivation par le SIL.

## Statut de lecture

Papier complet : tout `fulltext.md` lu. Le Tableau 1 (résultats principaux par domaine) n'est pas présent dans le texte extrait ; ses valeurs sont reprises du texte de §5.1 et du Tableau 2/3 (partiellement mal extraits). Le détail des domaines COCO-O autres que weather, painting, handmake, sketch n'a pas été lu.
Ce qui suit est déduit et non affirmé par les auteurs : l'absence d'entraînement conjoint comme différence avec la thèse ; le caractère « tardif » de l'alerte ; la définition exacte du FPR ; l'inadéquation de DINO ViT-B pour un FPGA ; la comparabilité avec la thèse ; le contenu exact du dépôt de code (non vérifié).
