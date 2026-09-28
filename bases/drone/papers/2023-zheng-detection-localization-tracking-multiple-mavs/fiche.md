---
id: 2023-zheng-detection-localization-tracking-multiple-mavs
fiche: done
date: 2026-09-28
---

# Detection, Localization, and Tracking of Multiple MAVs With Panoramic Stereo Camera Networks

Ye Zheng, Canlun Zheng, Xiaoyu Zhang, Fei Chen, Zhang Chen, Shiyu Zhao, 2023, IEEE Transactions on Automation Science and Engineering 20(2), 1226-1243. https://doi.org/10.1109/TASE.2022.3176294
Type : article de journal

## Problème

Surveiller l'intrusion de MAV malveillants sur une grande zone. Selon les auteurs (§I) :
- les détecteurs par apparence (deep learning) généralisent mal aux MAV **inconnus**, leur
  apparence variant beaucoup ; leur propre évaluation de huit détecteurs [7] le montre ;
- la vision monoculaire ne donne pas la distance d'un MAV de taille inconnue ;
- les caméras stéréo du commerce ont une base courte (< 0,2 m) et une portée utile d'environ
  15 m.

C'est un système de contre-drone **sol → air** : les nœuds de capteurs sont fixes au sol (Fig. 1).

## Méthode

Réseau de nœuds de capteurs et un nœud central (§III) :
- **Nœud** : 4 caméras HIKVISION DS-2CD6984F-IHS/NFC de 4 objectifs chacune, soit 16
  objectifs formant une vision panoramique 360° et 8 paires stéréo de **base 1 m**. Chaque
  nœud porte aussi une IMU, un RTK-GPS, deux PC et un routeur. Objectifs à 1280 × 720 et
  25 FPS (§III).
- **Détection (§IV)** : par le mouvement plutôt que par l'apparence. Soustraction de fond
  KNN pour extraire les objets mobiles, puis YOLOv5 pour **exclure** les objets courants
  (piétons, voitures) par IoU > 0,5 (Éq. 1-2). Les candidats restants sont suivis par SORT,
  puis classés par une métrique spatiale P_S (vitesse apparente, distance type CIoU, Éq. 4-8)
  et une métrique temporelle P_T (durée du mouvement continu, sigmoïde, Éq. 9-10), combinées
  par un poids β (Éq. 3, 11). La taille minimale détectable est de 3 × 3 pixels (élément
  structurant morphologique) ; le fond est remodélisé toutes les 75 images (§IV-A).
- **Localisation (§V)** : stéréo **éparse** et non carte de profondeur dense. Appariement des
  boîtes par points ORB communs, élimination des faux appariements par contrainte
  épipolaire, triangulation, filtrage des points de fond, puis moyenne des points 3D.
- **Suivi et fusion (§VI)** : un filtre de Kalman à vitesse constante par MAV, association
  GNN, et un module de raffinement de trajectoire (Éq. 14, t_s = 6 s). Au nœud central, les
  segments de trajectoire de 6 s sont fusionnés par score de similarité position + vitesse
  (Éq. 15-17) et algorithme de Kuhn-Munkres.

## Plateforme et implémentation

- **Nœud de capteurs** : chaque PC traite 8 objectifs, avec un Intel i7-11700K à 3,6 GHz et
  une Nvidia **RTX 3070** (§VII-B.3). YOLOv5 tourne sur le GPU, tout le reste sur le CPU.
- **Nœud central** : Intel i7-10750H à 2,6 GHz (§VII-B.3).
- Puissance : n/r. Gamme de puissance : **GPU de bureau au sol** (déduit : plusieurs centaines
  de W par nœud, non mesurés), hors de toute contrainte embarquée.
- Résolution traitée par PC : 1280 × 2880 selon le §III, mais 5760 × 1280 selon le §VII-B.3.
  Les deux valeurs sont incohérentes dans le texte extrait.
- Code non publié. Seule une vidéo est donnée (https://youtu.be/PNtRgkqgHw4, Fig. 1). Jeu de
  données propre (DJI Phantom 4, M300, Mavic 2), non publié selon le texte.

## Résultats

Lus dans le texte (les tableaux II à VIII n'ont pas de corps extrait) :
- **Détection** : précision > 99 % sur images panoramiques (§IV-C.3, Table III) ; rappel
  > 94 % selon le type de MAV (§IV-C.3, Table IV). La précision baisse en OD_IS3 (voitures
  partiellement occultées non reconnues par YOLOv5) et quand l'éclairage se dégrade (Table II).
  Contre Cascade R-CNN, Grid R-CNN, RetinaNet et YOLOv5-x, entraînés sur Phantom 4 et Mavic 2
  et testés sur M300 : « the highest AP with a relatively low runtime » (§IV-C.3, Table V).
  Valeurs d'AP : n/r dans le texte extrait.
- **Localisation** : portée utile d'environ 50 m pour Mavic 2 et Phantom 4, et d'environ
  **80 m** pour le M300. L'erreur relative reste ≤ 10 % dans le pire cas (§V-C, Table VI).
  Au-delà d'environ 65 m, aucun point ORB n'est apparié ; le centre de la boîte sert alors de
  point (§V-C).
- **Suivi (simulation, 7 MAV et 4 nœuds)** : RMSE de position moyen d'environ 1,4 m (§VI-C.3,
  Table VIII). CV+GNN+Refinement retenu : précision proche d'IMM+GNN+Refinement pour un temps
  de calcul moindre (§VI-C.2, Table VII, valeurs n/r).
- **Système réel** : erreur absolue de 3,34 m et erreur relative moyenne de 4,57 %
  (§VII, fragment attribué à l'expérience « un nœud, un MAV » par déduction).
- **Temps de calcul** : détection 97,82 ms, localisation 9,99 ms, suivi 1,03 ms ; soit
  « at least 9 FPS » (§VII-B.3, Fig. 17). Portée de détection seule jusqu'à 150 m pour le
  M300, ramenée à 80 m pour le système complet (§VII-B.3).

→ reportés dans `benchmarks.csv` : 1 ligne (pipeline KNN + YOLOv5 + classification par le
mouvement, sur i7-11700K + RTX 3070, 9 FPS, 97,82 ms pour le module de détection, précision
n/r ; §VII-B.3, Fig. 17, confidence medium).

## Limites et critique

- **Sol → air, sur GPU de bureau** : hors du périmètre IA embarquée de la base. Aucun chiffre
  de puissance, de masse ou d'encombrement.
- **Comparaison biaisée en faveur de la méthode (déduit)** : les détecteurs deep learning
  sont testés sur un MAV absent de l'entraînement (M300), alors que la méthode proposée n'est
  pas apprise. Le protocole favorise l'approche par le mouvement, sans fine-tuning ni
  augmentation pour les baselines.
- **Hypothèse forte** : un MAV en vol stationnaire n'est pas détecté (§IV-C.3) ; le suivi
  prend le relais « based on the information obtained in the last few steps ». Les oiseaux
  en mouvement continu ne sont pas discutés comme source de faux positifs persistants,
  alors qu'ils figurent dans le jeu de données (Fig. 7).
- **Jeu de données petit et propre** : 3 modèles DJI, séquences en nombre non précisé dans le
  texte extrait, non publié.
- **Robustesse aux paramètres** : nombreux seuils fixés à la main (k = 2/3, ω = 1/2, λ = 20,
  θ = 1, ζ = 20 images, p = 3, q = 7), sans étude de sensibilité.
- **Simulation du suivi simpliste** : bruit gaussien σ = 10 sans autre modèle d'erreur
  (§VI-C.1).
- 9 FPS avec une RTX 3070 par groupe de 8 objectifs : coût matériel élevé pour un débit
  modeste.

## Pertinence pour la thèse

- **Faible sur le cœur embarqué** : contre-drone sol → air, donc explicitement exclu par
  `profile.md`. Utile seulement comme référence de contraste.
- **Idée transposable (déduit)** : la détection par le mouvement (fond KNN + exclusion par un
  détecteur générique + indices spatio-temporels) est une alternative légère aux détecteurs
  par apparence. Pour l'**air → air**, elle se heurte au mouvement propre de la caméra, qui
  rend la soustraction de fond inopérante sans compensation d'ego-motion.
- La stéréo éparse limitée à la boîte détectée est un bon principe pour réduire le coût de
  la profondeur sur une cible embarquée.
- Même groupe que le dataset Det-Fly [7] (Zheng et al., Westlake University), cité comme
  évaluation de huit détecteurs sur MAV : référence à vérifier et à ajouter si elle est
  absente de la base.

## Gaps identifiés

- **Détection de MAV inconnus** : la généralisation des détecteurs par apparence à un modèle
  de drone non vu reste ouverte selon les auteurs (§I, §II-A). Aucune étude de ce type en
  embarqué air → air dans ce papier.
- **Détection par le mouvement sur plateforme mobile** : non traitée (caméras fixes). Gap
  pour l'air → air : compensation d'ego-motion + indices temporels, sur calculateur
  embarqué.
- **Aucune métrique énergétique** pour un système de surveillance multi-nœuds.

## Statut de lecture

Papier complet (`fulltext.md` lu en entier, extraction GROBID `ok`). Les tableaux I, II,
III, V, VI et VIII sont signalés « sans corps extrait » ; IV et VII n'apparaissent qu'en
légende ou en fragment. Les valeurs de précision, rappel, AP, erreurs de localisation par
distance et RMSE par méthode ne sont donc connues que par les phrases du texte. Plusieurs
passages sont fragmentés (algorithmes 1-2, §VII-A/B mélangés) ; l'attribution des 3,34 m /
4,57 % à l'expérience « un nœud, un MAV » est déduite de l'ordre du texte.

Ce qui suit est déduit et non affirmé par les auteurs :
- la gamme de puissance (GPU de bureau, centaines de W) ;
- le biais du protocole de comparaison avec les détecteurs deep learning ;
- la difficulté de transposer la méthode en air → air (ego-motion) ;
- l'identification de [7] au dataset Det-Fly.
