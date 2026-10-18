---
id: arxiv-1804.00518-unmanned-aerial-vehicle-benchmark-object
fiche: done
date: 2026-10-18
---

# The Unmanned Aerial Vehicle Benchmark: Object Detection and Tracking

Dawei Du, Yuankai Qi, Hongyang Yu, Yifan Yang, Kaiwen Duan, Guorong Li, Weigang Zhang, Qingming Huang, Qi Tian, 2018, arXiv preprint. https://arxiv.org/abs/1804.00518 (DOI n/r).
Type : preprint non relu par les pairs selon `metadata.json`. Le benchmark UAVDT est
généralement cité dans sa version ECCV 2018 : venue à vérifier, le texte extrait ne la
donne pas.

## Problème

Les jeux de détection et de suivi existants sont pris par des caméras fixes ou embarquées
sur voiture, donc avec des angles de vue limités (§1). Les jeux drone existants (UAV123,
Campus, CARPK) ne couvrent qu'une tâche dans une scène contrainte (§1, §2.2). Les auteurs
listent quatre défis propres au drone : densité élevée, petits objets, mouvement de
caméra et contraintes temps réel sur plateforme embarquée (§1).

## Méthode

Jeu de données **UAVDT** (§2) :
- 100 séquences vidéo extraites de plus de 10 h de vol en milieu urbain (places, artères,
  péages, autoroutes, carrefours, jonctions en T), 30 fps, JPEG 1080 × 540 (§2) ;
- environ 80 000 images annotées, plus de 2 700 véhicules, 0,84 M boîtes (§2.1). Classes :
  car, truck, bus ;
- découpage : 30 séquences d'entraînement et 70 de test (20 pour DET et MOT, 50 pour SOT),
  les séquences d'entraînement étant prises sur des lieux différents de ceux du test, avec
  des scènes et attributs semblables, pour limiter le surapprentissage à une scène (§2.1) ;
- densité moyenne de 10,52 objets par image contre 8,64 (DETRAC), 5,35 (KITTI), 1,00
  (UAV123) (§2.2).

Évaluation des méthodes de l'état de l'art sur trois tâches (§3) :
- DET : Faster-RCNN (VGG-16), R-FCN (ResNet-50), SSD et RON (512 × 512, batch 5). AP selon
  PASCAL VOC, mais au seuil IoU 0,7 comme KITTI-D (§3.1) ;
- MOT : 8 trackers (CMOT, MDP, SORT, DSORT, GOG, CEM, SMOT, IOUT) alimentés par les 4
  détecteurs ; métriques CLEAR et ID (§3.2) ;
- SOT : 18 trackers ; success (AUC) et precision à 20 px (§3.3).

### Protocole d'annotation (§2.1)

- **Qui, quoi, combien** : plus de 10 experts du domaine, outil `vatic`, deux mois, « several
  rounds of double-check » pour réduire les erreurs. Coût en heures-annotateur par boîte :
  n/r ; accord inter-annotateurs et taux d'erreur résiduel : n/r. Le contrôle qualité est
  décrit en une phrase, sans mesure.
- **Zones ignorées** : suivant PASCAL VOC, les régions qui couvrent des véhicules trop petits
  (basse résolution) sont ignorées dans chaque image (§2.1). Le seuil de taille de
  « trop petit » est n/r. Elles apparaissent en rose (Fig. 1). Un objet « hors champ » inclut
  ceux qui sortent de l'image ou tombent dans une zone ignorée.
- **Attributs de prise de vue (3)** : météo/éclairage (daylight, night, fog) ; altitude de vol
  (low 10-30 m, medium 30-70 m, high > 70 m) ; vue (front, side, bird, les deux premières
  pouvant coexister dans une séquence). Annotés pour MOT (§2.1) ; la conclusion dit qu'ils
  couvrent toutes les images (§5).
- **Attributs d'objet pour DET (3)** : catégorie (car, truck, bus) ; occlusion = fraction de la
  boîte occultée : no-occ (0 %), small (1-30 %), medium (30-70 %), large (70-100 %) ;
  out-of-view : no-out (0 %), small-out (1-30 %), medium-out (30-50 %). Les objets dont plus de
  50 % sort du cadre sont écartés (§2.1). « Occlus » vaut aussi pour un obstacle de la scène
  (ex. sous un pont).
- **Attributs SOT (8, par séquence)** : BC, CR, OR, SO, IV, OB, SV, LO ; 74 % des vidéos
  cumulent au moins 4 défis, 51 % en ont 5 (§2.1, Table 2).
- L'abstract annonce « up to 14 kinds of attributes » ; le texte en décrit 3 + 3 + 8 = 14.

### Distribution des tailles et difficulté des données

- 27,5 % des objets font moins de 400 pixels, soit environ 0,07 % de l'image (§4).
- Haute altitude : les plus petits objets couvrent 0,005 % de l'image, pour plus d'une
  centaine d'objets par image ; basse altitude : un objet peut occuper jusqu'à 22,6 % de
  l'image dans un cas extrême (§2.1).
- Déséquilibre de classes : truck et bus pèsent moins de 10 % du jeu (§3.1, Fig. 2) ; les
  véhicules de grande taille sont les moins bien détectés.

## Plateforme et implémentation

- DET : entraînement sur i9 7900X + GTX 1080 Ti ; learning rate 0,001 puis 0,0001 (Faster-RCNN,
  R-FCN), 0,005 sur 120k itérations (SSD), momentum 0,9, weight decay 0,0005 (§3.1). La
  plateforme de mesure des vitesses DET n'est pas précisée hors de la légende de la Fig. 3
  (« GPU/CPU speed », non extraite).
- MOT : i7 6700 + Titan X (§3.2). SOT : i7 4790k + Titan X (§3.3).
- Aucune plateforme embarquée évaluée ; puissance n/r.
- Données : mises à disposition (note de bas de page du §2, URL non extraite). Codes des
  méthodes : ceux publiés par leurs auteurs (§3).

## Résultats

- **DET** : R-FCN obtient le meilleur AP, 34,35 %, contre 70,06 % sur le sous-ensemble
  difficile de KITTI-D (§3.1). Les auteurs l'attribuent aux nombreux petits objets dus à la
  perspective et au fond plus chargé en altitude (§3.1). Les AP et vitesses des autres
  détecteurs sont dans la légende de la Fig. 3, **non extraite**. RON (fusion de couches
  profondes) fait moins bien que SSD ici (§3.1). Les méthodes à régions tournent à moins de
  5 fps ; les méthodes sans régions sont « presque temps réel » (§3.1).
- **DET par attribut** (Fig. 4, valeurs non extraites, texte seul, §3.1) : mieux sur low-alt
  et side-view ; moins bien de jour que de nuit (plus d'objets et fond plus chargé) ;
  chute nette pour les grands véhicules, l'occlusion et le hors-champ.
- **MOT** (Table 3) : le meilleur est MDP avec Faster-RCNN (MOTA 43,0 ; IDF 61,5), à
  0,68 fps CPU. SORT avec Faster-RCNN : MOTA 39,0, à 245,79 fps CPU. IOUT avec Faster-RCNN :
  MOTA 36,6, 1438,34 fps CPU. À comparer à SORT sur MOT16 : 59,8 ± 10,3 de MOTA (§3.2). Le
  suivi se dégrade de nuit, en brouillard, en altitude et en vue zénithale (§3.2).
- **SOT** : le meilleur est MDNet (success 46,4, precision 72,5), contre 69,4 / 92,8 pour
  le meilleur résultat sur OTB100. KCF : 29,0 ici contre 33,1 sur UAV-123 (§3.3). Le plus
  rapide des 10 trackers les plus précis tourne à 11,7 fps CPU ; MDNet à 0,28 fps CPU (§3.3).
- Le réglage des tailles d'ancres par les auteurs apporte environ 10 % d'AP aux détecteurs ;
  baisser la résolution des images aggrave le problème des petits objets (§4). Aucune
  ablation par détecteur n'est donnée.

→ lignes de `benchmarks.csv` : 3 lignes existantes (meilleurs résultats DET, MOT et SOT :
R-FCN, MDP+Faster-RCNN, MDNet), `medium`, plus 2 lignes MOT proposées (SORT et IOUT avec
Faster-RCNN, Table 3), à ajouter par l'agent principal.

## Limites et critique

- **AP à IoU 0,7** : non comparable aux AP@0.5 ni aux AP COCO [.5:.95] rapportés
  ensuite sur UAVDT par d'autres papiers (déduit). Vérifier le protocole avant toute
  comparaison chiffrée.
- **Contrôle qualité non mesuré** : « double-check » sans taux d'erreur, sans accord entre
  annotateurs, sans seuil de taille pour les zones ignorées. Des boîtes manquantes ou
  des zones ignorées trop larges biaisent le rappel et l'AP (déduit).
- **Détecteurs de 2016-2017 seulement** (Faster-RCNN, R-FCN, SSD, RON). Les vitesses
  mesurées sur GTX 1080 Ti ou Titan X, et sur CPU de bureau, ne disent rien du temps réel
  embarqué que les auteurs posent pourtant comme défi (§1, §4).
- **Uniquement des véhicules**, en milieu urbain, à 1080 × 540 (résolution modeste pour des
  objets « tiny »), 3 classes très déséquilibrées. Pas de piétons, contrairement à VisDrone
  (déduit).
- Images extraites de vidéos à 30 fps : fortes corrélations temporelles entre images voisines
  (déduit) ; le découpage par séquence et par lieu limite la fuite train/test (§2.1), mais le
  nombre d'images (80 000) surestime la diversité réelle (100 séquences).
- Le gain de 10 % par réglage des ancres n'est pas détaillé (§4).

## Pertinence pour cette base

Ce que le papier apprend, par usage :

- **Construire** : recette d'un dataset de détection aérien. Échantillonner par séquence et
  par lieu (entraînement et test sur sites distincts, §2.1), couvrir explicitement l'altitude,
  la vue et la météo plutôt qu'une seule scène (§2.2). Densité (10,52 objets par image) et
  part de petits objets (27,5 % sous 400 px) sont les deux statistiques à rapporter. Utile
  quand on monte un jeu de domaine (drone, trafic) pour YOLO.
- **Annoter** : protocole concret et réaliste : outil vidéo (`vatic`), experts, passes de
  vérification, labels de catégorie, d'occlusion par fraction de boîte (4 niveaux) et de
  troncature (3 niveaux, rejet au-delà de 50 %), zones ignorées pour les véhicules
  illisibles. À reprendre comme consignes d'annotation : définir à l'avance quoi faire des
  objets trop petits, occultés ou coupés par le bord. Limite : coût et accord non
  mesurés, donc impossible d'en tirer un budget d'annotation.
- **Prétraiter** : la taille compte plus que la classe. Redimensionner à 512 × 512 écrase des
  objets de 0,005 % de l'image ; les auteurs notent que le sous-échantillonnage aggrave les
  petits objets (§4). Appuie l'usage de tiling / haute résolution d'entrée pour les vues
  hautes ; les attributs d'altitude servent à choisir la résolution (déduit).
- **Augmenter / rééquilibrer** : truck et bus < 10 % des instances et pires AP (§3.1) : cas
  d'école pour le rééquilibrage ou le Copy-Paste (déduit, non testé ici). Réglage des
  ancres : +10 % d'AP, sans détail (§4) ; à reproduire avec k-means sur les tailles UAVDT.
- **Quand l'appliquer** : dès que la cible est de la détection de véhicules vue du dessus
  ou en oblique, avec petits objets et forte densité. Les attributs permettent de rapporter
  la robustesse par condition (altitude, éclairage, occlusion) au lieu d'un seul mAP
  (déduit). Ne pas comparer l'AP@0.7 de ce papier aux mAP@0.5 d'autres travaux.

## Gaps identifiés

- **Coût et accord d'annotation absents** : aucun chiffre exploitable pour dimensionner un
  budget d'annotation de bbox aérien.
- **Aucun test d'augmentation ou de rééquilibrage** : l'effet du Copy-Paste, du Mosaic ou du
  tiling sur UAVDT n'est pas mesuré ici.
- **Seuil des zones ignorées non défini** : l'effet sur l'évaluation reste inconnu.
- Protocole AP@0.7 original vs AP@0.5 des travaux ultérieurs : risque de comparaisons
  invalides dans la littérature UAVDT.

## Statut de lecture

Papier complet (`fulltext.md` lu en entier, extraction GROBID `ok`). Manques :
- Table 1 (comparaison des jeux) sans corps ;
- Fig. 2 (distribution des attributs) et Fig. 4 (DET par attribut) : valeurs non extraites,
  seul le texte est utilisé ;
- légende de la Fig. 3 (AP et vitesses des 4 détecteurs) non extraite ;
- Table 3 lisible, mais avec des colonnes fusionnées ;
- Table 4 (SOT par attribut) reconstruite en bloc illisible, sans noms de lignes fiables ;
- la fin du §3.3 (« Run-time Performance… the realtime trackers ») est tronquée.

Ce qui suit est déduit et non affirmé par les auteurs :
- la non-comparabilité avec les AP@0.5 des papiers ultérieurs ;
- les effets probables du contrôle qualité non mesuré et des corrélations temporelles ;
- l'usage des attributs d'altitude pour choisir la résolution, et le lien truck/bus ↔
  rééquilibrage ou Copy-Paste ;
- la venue ECCV 2018 (connaissance externe, à vérifier) ;
- la comparaison avec VisDrone.
