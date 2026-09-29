---
id: arxiv-2011.10671-review-comparative-probabilistic-object-detection
fiche: done
date: 2026-09-29
benchmarks: none
---

# A Review and Comparative Study on Probabilistic Object Detection in Autonomous Driving

Di Feng, Ali Harakeh, Steven Waslander, Klaus Dietmayer, 2020, arXiv preprint (DOI de la version publiée : IEEE Trans. Intelligent Transportation Systems, 10.1109/TITS.2021.3096854, d'après `metadata.json`). https://doi.org/10.1109/TITS.2021.3096854
Type : preprint non relu par les pairs (version arXiv v1, 2020)

## Problème

Les détecteurs d'objets profonds sont déterministes : ils prédisent des classes (softmax) et des boîtes sans incertitude fiable, alors que la conduite autonome exige des détecteurs qui « savent ce qu'ils ne savent pas » (Abstract, §I). Les méthodes probabilistes existantes utilisent des réseaux, des capteurs, des jeux de données et des métriques différents, ce qui rend toute comparaison et tout choix de méthode difficiles (Abstract, §I). Les auteurs proposent (i) un état de l'art de l'estimation d'incertitude en détection d'objets, (ii) une comparaison contrôlée sur une base commune.

## Méthode

- Survey (§II-§III) : incertitude épistémique (du modèle, `p(W|D)`) vs aléatoire (du capteur, `p(y|x,W)`) ; quatre méthodes pratiques : MC-Dropout, Deep Ensembles, Direct Modeling (le réseau prédit variance/paramètres de la distribution, entraînement par NLL « loss attenuation »), Error Propagation (§II-D). Métriques : calibration (ECE, MCE), règles de scoring propres (NLL, Brier), PDQ, MUE, JIoU, mAP (§II-E, §III-C). Tableau I : synthèse des détecteurs probabilistes (capteur, dataset, type d'incertitude, post-traitement, métrique).
- Étude comparative (§IV) : RetinaNet (ResNet-50 + FPN, Detectron2) entraîné sur BDD100K (70k images d'entraînement), évalué sur BDD val, KITTI et 5 000 images Lyft (décalage de distribution) ; 7 classes en entraînement, Car et Person seulement en évaluation décalée. Huit variantes (Tableau II) : Output Redundancy, Loss Attenuation, BayesOD (fusion bayésienne au lieu de NMS), + MC-Dropout (10 passes, taux 0,1), Pre-NMS et Post-NMS Ensembles (5 modèles), Black Box (dropout dans la tête, clustering après NMS) (§IV-A, §IV-C).
- §IV-E : comparaison de l'incertitude aléatoire entre détection image (RetinaNet) et LiDAR (ProbPIXOR) sur KITTI.

## Plateforme et implémentation

Sans objet côté FPGA : pas d'implémentation matérielle. Temps d'exécution mesurés sur GPU Nvidia Titan V + CPU Intel i3770k (§IV-D), valeurs de FPS non extraites du texte (corps du Tableau III absent). Puissance : n/r. Code publié : https://github.com/asharakeh/pod_compare (Abstract, §I).

## Résultats

Chiffres rapportés dans le texte extrait (les valeurs de NLL, PDQ, calibration et runtime du Tableau III/Fig. 4-6 ne sont pas disponibles) :

- Baseline RetinaNet déterministe : 28,62 % mAP sur BDD, 7 classes (§IV-D) ; toutes les extensions probabilistes restent à moins de 2 % de mAP de ce baseline (§IV-D).
- mAP sur Car+Person, sous décalage de distribution (tableau de mAP, légendé Tableau IV, corps peut-être décalé par l'extraction) : baseline 40,63 / 37,11 / 5,33 (BDD / KITTI / Lyft) ; BayesOD 41,33 / 39,32 / 6,01 ; Post-NMS Ensembles 41,95 / 39,52 / 5,949 ; Output Redundancy 38,75 / 34,99 / 5,21. Le décalage vers Lyft (surexposition ~60 % des pixels > 250, boîtes 2D projetées depuis la 3D, App. F / Fig. 10) effondre le mAP.
- Constats (§IV-D) : (1) le mAP seul ne mesure pas la qualité de l'incertitude (deux détecteurs de même moyenne mais covariances différentes ont le même mAP ; NLL de régression de Black Box et Output Redundancy deux ordres de grandeur plus grand à mAP comparable) ; (2) le Direct Modeling de l'incertitude spatiale est essentiel ; (3) modéliser la variance des logits n'apporte rien par rapport au softmax + entropie croisée ; (4) BayesOD gagne 3 % de PDQ et réduit la NLL de régression de 2,24 points vs Loss Attenuation (remplacement du NMS par la fusion bayésienne) ; (5) MC-Dropout et ensembles n'améliorent pas assez la qualité d'incertitude pour justifier leur coût (MC-Dropout à 10 passes : 2-3 FPS, §V-A) ; les ensembles apportent un léger gain de mAP, le dropout une baisse.
- Aucune ligne dans `benchmarks.csv` : c'est un survey + étude comparative sur GPU sans mesure matérielle FPGA ni FPS/W exploitable (FPS non extraits), donc `benchmarks: none`.

## Limites et critique

- Un seul détecteur (RetinaNet, 1 étage, 2D image) et trois jeux de données de conduite ; les auteurs précisent que les conclusions valent pour ce cadre (§IV-D). LiDAR/3D laissés à des travaux futurs.
- Dropout à 0,1 seulement (des taux plus élevés faisaient perdre jusqu'à 10 % de mAP, §IV-C) et 10 passes : la conclusion « MC-Dropout ne vaut pas son coût » est peut-être sensible à ce réglage ; 5 modèles pour les ensembles. Les auteurs expliquent l'absence de gain des ensembles par la grande taille du jeu d'entraînement (70 k images, §IV-D) : hypothèse, pas testée.
- Évaluation uniquement sur les détections bien localisées (IoU > 0,7), ce qui masque les erreurs de localisation grossières (reconnu §IV-D pour l'insensibilité de la régression au décalage).
- Détecteur lourd (ResNet-50 RetinaNet, GPU Titan V) : aucune considération de quantification, de latence déterministe ni de coût matériel ; le survey ne cite pas d'implémentation embarquée (déduit). YOLO n'est cité que comme exemple (YOLOv3 avec dropout, Kraus et al. [81], §III-B3).
- Extraction : corps des Tableaux III et V absents, Fig. 4-6 non chiffrées ; le tableau de mAP semble correspondre au Tableau IV mais figure sous la légende du Tableau III.
- Preprint ; aucune vérification de sûreté formelle : l'incertitude est un indicateur statistique, pas une garantie.

## Pertinence pour la thèse

Apporte à l'axe « sûreté » un cadre conceptuel utile pour le moniteur d'exécution d'un YOLO de vidéosurveillance de personnes : distinguer incertitude épistémique (personne hors distribution, EPI inhabituels) et aléatoire (occlusion, faible éclairage), et les métriques à exiger (NLL, calibration, pas seulement mAP). Le résultat que l'incertitude par « loss attenuation » (une passe, coût quasi nul) donne l'essentiel du gain, alors que MC-Dropout/ensembles multiplient le coût, est directement exploitable pour un accélérateur FPGA à budget temps réel fixe (inférence déduite : ce papier ne parle pas de FPGA). Les sept sources d'incertitude de Czarnecki et al. (App. A) sont un canevas pour l'argumentaire de sûreté. Reste ouvert : mise en œuvre matérielle, incertitude sur des personnes en zone industrielle (domaine routier ici), liaison avec un dossier d'assurance/certification.

## Gaps identifiés

- Estimation d'incertitude de détecteurs YOLO sur FPGA (coût matériel de Direct Modeling, dropout, ensembles, Error Propagation) : non traitée.
- Détection probabiliste sur personnes en milieu industriel (jeux de données, décalage de domaine) : absente.
- Métriques d'incertitude (NLL, ECE, PDQ) sous quantification INT8 / faible précision : non étudiées.
- Lien entre calibration de l'incertitude et exigences de sûreté (niveau SIL/PL) : ouvert.

## Statut de lecture

Papier complet (fulltext.md lu en entier, y compris annexes et tableaux extraits). Backend d'extraction : grobid, ok. Corps des Tableaux III et V absents (avertissement d'extraction) ; Fig. 4-6 non chiffrées ; le tableau de mAP sous la légende du Tableau III semble être celui du Tableau IV (à vérifier dans le PDF, non ouvert).
Ce qui est déduit et non affirmé par les auteurs : la portée pour le FPGA et la vidéosurveillance ; l'absence d'implémentation embarquée dans la littérature qu'ils citent ; l'utilité du canevas Czarnecki pour un dossier de sûreté.
