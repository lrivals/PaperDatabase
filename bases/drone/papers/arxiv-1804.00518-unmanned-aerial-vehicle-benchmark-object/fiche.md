---
id: arxiv-1804.00518-unmanned-aerial-vehicle-benchmark-object
fiche: done
date: 2026-09-28
---

# The Unmanned Aerial Vehicle Benchmark: Object Detection and Tracking

Dawei Du et al., 2018, arXiv preprint (auteurs complets dans `metadata.json`). https://arxiv.org/abs/1804.00518
Type : preprint non relu par les pairs selon `metadata.json`. Le benchmark UAVDT est
généralement cité dans sa version ECCV 2018 : venue à vérifier, le texte extrait ne la
donne pas.

## Problème

Les jeux de détection et de suivi existants sont pris par des caméras fixes ou embarquées
sur voiture, donc avec des angles de vue limités. Les jeux drone existants (UAV123,
Campus, CARPK) ne couvrent qu'une tâche dans une scène contrainte (§1, §2.2). Les auteurs
listent quatre défis propres au drone : densité élevée, petits objets, mouvement de
caméra et contraintes temps réel sur plateforme embarquée (§1).

## Méthode

Jeu de données **UAVDT** (§2) :
- 100 séquences vidéo extraites de plus de 10 h de vol en milieu urbain (places, artères,
  péages, autoroutes, carrefours), 30 fps, JPEG 1080 × 540 ;
- environ 80 000 images annotées, plus de 2 700 véhicules, 0,84 M boîtes (§2.1). Classes :
  car, truck, bus ; les véhicules trop petits sont en zones ignorées ;
- attributs : météo (jour, nuit, brouillard), altitude (basse 10-30 m, moyenne 30-70 m,
  haute > 70 m), vue (frontale, latérale, zénithale), occlusion, hors-champ. Pour le SOT,
  8 attributs (BC, CR, OR, SO, IV, OB, SV, LO) (§2.1, Table 2) ;
- découpage : 30 séquences d'entraînement et 70 de test (20 pour DET et MOT, 50 pour SOT),
  sur des lieux différents (§2.1) ;
- 27,5 % des objets font moins de 400 pixels, soit environ 0,07 % de l'image (§4) ;
  densité moyenne de 10,52 objets par image contre 8,64 pour DETRAC (§2.2).

Évaluation des méthodes de l'état de l'art sur trois tâches (§3) :
- DET : Faster-RCNN (VGG-16), R-FCN (ResNet-50), SSD et RON (512 × 512). AP selon PASCAL
  VOC, mais au seuil IoU 0,7 comme KITTI (§3.1) ;
- MOT : 8 trackers (CMOT, MDP, SORT, DSORT, GOG, CEM, SMOT, IOUT) alimentés par les 4
  détecteurs ; métriques CLEAR et ID (§3.2) ;
- SOT : 18 trackers ; success (AUC) et precision à 20 px (§3.3).

## Plateforme et implémentation

- DET : entraînement sur i9 7900X + GTX 1080 Ti (§3.1) ; la plateforme de mesure des
  vitesses DET n'est pas précisée hors de la légende de la Fig. 3 (« GPU/CPU speed »).
- MOT : i7 6700 + Titan X (§3.2). SOT : i7 4790k + Titan X (§3.3).
- Aucune plateforme embarquée évaluée ; puissance n/r.
- Données : mises à disposition (note de bas de page du §2, URL non extraite). Codes des
  méthodes : ceux publiés par leurs auteurs (§3).

## Résultats

- **DET** : R-FCN obtient le meilleur AP, 34,35 %, contre 70,06 % sur le sous-ensemble
  difficile de KITTI-D (§3.1). Les AP et vitesses des autres détecteurs sont dans la
  légende de la Fig. 3, **non extraite**. Les méthodes à régions tournent à moins de 5 fps
  ; les méthodes sans régions sont « presque temps réel » (§3.1). Performance plus faible
  en haute altitude, en vue zénithale et de jour (fond plus chargé) (§3.1, Fig. 4).
- **MOT** (Table 3) : le meilleur est MDP avec Faster-RCNN (MOTA 43,0 ; IDF 61,5), à
  0,68 fps CPU. SORT avec Faster-RCNN : MOTA 39,0, à 245,79 fps CPU. IOUT atteint jusqu'à
  1438 fps CPU (MOTA 36,6). À comparer à SORT sur MOT16 : 59,8 ± 10,3 de MOTA (§3.2).
- **SOT** : le meilleur est MDNet (success 46,4, precision 72,5), contre 69,4 / 92,8 pour
  le meilleur résultat sur OTB100. KCF : 29,0 ici contre 33,1 sur UAV-123 (§3.3). Le plus
  rapide des 10 trackers les plus précis tourne à 11,7 fps CPU ; MDNet à 0,28 fps CPU
  (§3.3).
- Le réglage des ancres par les auteurs apporte environ 10 % d'AP aux détecteurs (§4).

→ reportés dans `benchmarks.csv` (fichier du lot) : 3 lignes (meilleurs résultats DET,
MOT et SOT : R-FCN, MDP+Faster-RCNN, MDNet), toutes `medium` (texte, ou Table 3 dont les
colonnes sont partiellement fusionnées à l'extraction).

## Limites et critique

- **AP à IoU 0,7** : non comparable aux AP@0.5 ni aux AP COCO [.5:.95] rapportés
  ensuite sur UAVDT par d'autres papiers (déduit). Vérifier le protocole avant toute
  comparaison chiffrée.
- **Détecteurs de 2016-2017 seulement** (Faster-RCNN, R-FCN, SSD, RON) : baselines
  vite dépassées. Les vitesses mesurées sur GTX 1080 Ti ou Titan X, et sur CPU de bureau,
  ne disent rien du temps réel embarqué que les auteurs posent pourtant comme défi (§1, §4).
- **Uniquement des véhicules**, en milieu urbain chinois, à 1080 × 540 : résolution
  modeste pour des objets « tiny ». Pas de piétons, contrairement à VisDrone (déduit).
- Pas de puissance, pas de plateforme de drone. Le réglage des ancres (+10 %, §4) n'est
  pas détaillé par méthode.

## Pertinence pour la thèse

- **Jeu de référence de l'axe `datasets-benchmarks`**, avec VisDrone : UAVDT est l'un des
  deux jeux standards de la détection petits objets vue de drone. Ses attributs (altitude,
  vue, météo) permettent de mesurer la robustesse par condition, ce que les papiers
  FPGA/YOLO ne font presque jamais (déduit).
- L'attribut **altitude** relie directement la précision à un paramètre de vol : c'est une
  base pour la question co-design (altitude de vol ↔ taille des objets ↔ résolution
  d'entrée ↔ coût de calcul).
- Les vitesses MOT (IOUT, SORT à plusieurs centaines de fps CPU) montrent que
  l'association par position est quasi gratuite : le coût embarqué est dans le détecteur.

## Gaps identifiés

- **Aucune évaluation embarquée** dans le benchmark lui-même : le défi « realtime on
  embedded UAV platforms » (§1) est posé sans mesure.
- **Précision par altitude jamais croisée avec la quantification** ni avec la résolution
  d'entrée d'un accélérateur : lien direct avec le gap mAP_small.
- **Protocole AP@0.7 original** vs AP@0.5 des travaux ultérieurs : risque de
  comparaisons invalides dans la littérature UAVDT.

## Statut de lecture

Papier complet (`fulltext.md` lu en entier, extraction GROBID `ok`). Manques :
- Table 1 (comparaison des jeux) sans corps ;
- légende de la Fig. 3 (AP et vitesses des 4 détecteurs) non extraite ;
- Table 3 lisible, mais avec des colonnes fusionnées ;
- Table 4 (SOT par attribut) reconstruite en bloc illisible, sans noms de lignes fiables ;
- la fin du §3.3 (« Run-time Performance… the realtime trackers ») est tronquée.

Ce qui suit est déduit et non affirmé par les auteurs :
- la non-comparabilité avec les AP@0.5 des papiers ultérieurs ;
- l'intérêt de l'attribut altitude pour le co-design ;
- la venue ECCV 2018 (connaissance externe, à vérifier) ;
- la comparaison avec VisDrone.
