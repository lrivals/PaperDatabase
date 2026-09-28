---
id: arxiv-2101.08466-anti-uav-large-multi-modal
fiche: done
date: 2026-09-28
benchmarks: none
---

# Anti-UAV: A Large Multi-Modal Benchmark for UAV Tracking

Nan Jiang, Kuiran Wang, Xiaoke Peng, Xuehui Yu, Qiang Wang, Junliang Xing, Guorong Li, Jian Zhao, Guodong Guo, Zhenjun Han, 2021, arXiv preprint. https://arxiv.org/abs/2101.08466
Type : preprint non relu par les pairs (version arXiv ; une publication ultérieure dans une revue n'est pas indiquée dans `metadata.json`)

## Problème

Suivre un drone (position, trajectoire, présence dans le champ) à longue distance. Selon
les auteurs, il n'existait pas de benchmark de suivi multi-modal dédié aux UAV : les jeux
de suivi portent sur des objets génériques (voitures, personnes) (§I, Table I). L'image
infrarouge seule est jugée trop basse résolution, d'où l'intérêt d'une fusion RGB + IR
(§I).

## Méthode

- **Jeu de données Anti-UAV** : 318 paires de vidéos RGB + infrarouge thermique (RGB-T),
  **non alignées** entre modalités, drones surtout DJI et Parrot, jour et nuit, fonds
  variés (bâtiments, nuages, arbres), vidéos à 25 FPS (§III-A, Fig. 2). 585,9 k boîtes au
  total ; 160 séquences d'entraînement (294,4 k boîtes), 91 de test (168,4 k) (Table I).
  Le reste (67 séquences) forme sans doute la validation (déduit : 318 − 160 − 91).
- Annotation progressive grossière → fine → correction, avec un drapeau « exist » par
  image (§III-B). Taille moyenne des cibles < 40 pixels dans les trois sous-ensembles
  (§III-B, Fig. 3b).
- 7 attributs : OV (hors champ), OC (occultation), FM (mouvement rapide), SV (échelle), LI
  (faible illumination), TC (cible thermique croisée, en trois niveaux), LR (basse
  résolution) (§III-D, Tables III-IV).
- **Métrique mSA** (state accuracy) : IoU sur les images où le drone est visible, et
  score de prédiction d'absence sinon, moyennés par séquence puis sur les séquences
  (§III-E, Éq. 1). Trois protocoles : I (sans données UAV à l'entraînement), II
  (entraînement sur Anti-UAV), III (multi-modal non aligné) (§III-E).
- **DFSC** (dual-flow semantic consistency) : stratégie d'entraînement sur la base de
  GlobalTrack. Une modulation au niveau classe entre séquences (CSM, RPN guidé par
  requête) précède une modulation au niveau instance dans la séquence (ISM, QG-RCNN)
  (§IV). Elle ne sert qu'à l'entraînement : pas de coût à l'inférence selon les auteurs
  (§I, §VI).

## Plateforme et implémentation

- Entraînement sur GPU, batch 2 par GPU ; modèle GPU et nombre de GPU : n/r (§V-B).
- **Position et nature des caméras** (au sol ou embarquées, fixes ou orientables) : n/r
  dans le texte extrait. Les images décrites (drone sur fond de ciel, bâtiments, nuages)
  laissent penser à des caméras **au sol**, donc à un scénario **sol → air** (déduit, non
  affirmé).
- Vitesse (FPS) des trackers : n/r pour tous, DFSC compris. Les auteurs notent seulement
  que les trackers long-terme « peinent à tenir le temps réel » (§V-C).
- Puissance : n/r. Aucune plateforme embarquée.
- Données et code annoncés sur https://github.com/ucas-vg/Anti-UAV (Abstract) ; données
  « publiées » selon les contributions (§I). Challenge : CVPR 2020 Workshop, 1st Anti-UAV
  Challenge (§I).

## Résultats

Protocole I (plus de 40 trackers sans réentraînement, Tables III et IV) :

| Tracker | mSA IR val. | mSA IR test | mSA visible test |
|---|---|---|---|
| SiamRCNN [99] | 74,33 | 65,41 | 70,83 |
| GlobalTrack [76] | 72,00 | 63,86 | 66,24 |
| LTDSE [22] | 61,27 | 56,51 | 64,29 |
| SiamRPN++LT [11] | 65,84 | 54,34 | 61,17 |
| KCF [50] | 36,82 | 32,88 | 39,40 |

- Précision / success OPE : SiamRCNN 95,70 % / 71,52 % sur IR validation ; sur IR test,
  63,60 % de success pour SiamRCNN et 87,13 % de précision pour GlobalTrack (bloc de
  texte fondu dans la Table III, §V-C).
- Attribut le plus dur : TC_hard (cible sur fond de bâtiments chauds) ; SiamRCNN
  42,48 mSA sur le test (Table IV). Les trackers long-terme dominent (§V-C).

Protocole II (DFSC, §V-D) : +1,07 point de mSA sur TC_all au test (62,75 %) face au
fine-tuning normal ; gains de 0,78 à 1,28 point sur OC, SV, LR. Ablation : α = 0,25
optimal (§V-E, Table VI). Les **Tables V et VI ne sont pas dans l'extraction** : le score
mSA global de DFSC n'est pas connu.

→ reportés dans `benchmarks.csv` : aucune ligne. Aucun FPS, aucune plateforme, aucune
puissance pour DFSC ni pour les baselines ; le score global de DFSC (Table V) manque, et
les baselines du protocole I sont des travaux tiers.

## Limites et critique

- **Pas de coût de calcul** : aucune vitesse d'inférence ni plateforme, alors que le
  contexte applicatif (anti-UAV) est temps réel. Les trackers en tête (SiamRCNN,
  GlobalTrack) sont des modèles lourds à deux étages (déduit).
- **Gain DFSC marginal** (≈ 1 point de mSA) et non accompagné d'écart-type ni de
  répétitions (§V-D).
- **Incohérences de décompte** : « plus de 300 paires » et « plus de 580 k boîtes »
  (Abstract) contre 318 et 585,9 k (Table I) ; « 30 paires » retenues après annotation
  fine (§III-B), sans lien clair avec le total.
- **Données non alignées** entre RGB et IR : présentées comme un défi, mais le protocole
  III n'a aucun résultat dans le texte extrait.
- **Scénario sol → air probable** (déduit) : le benchmark ne dit rien du capteur ni de sa
  position. Il ne relève pas de l'IA embarquée au sens du profil ; il sert de source de
  données et de métrique.

## Pertinence pour la thèse

- Référence de base pour l'axe **`counter-uav`** : premier grand benchmark RGB-T de suivi
  de drones, avec une métrique qui intègre la **présence/absence** de la cible (mSA),
  réutilisable pour un détecteur-tracker embarqué.
- Jeu de **petits objets** (< 40 px en moyenne) : utile pour tester un détecteur
  quantifié sur des cibles minuscules, sous réserve de l'écart de point de vue sol → air
  vs air → air.
- Aucun apport côté plateforme embarquée ; les trackers évalués ne sont pas portés sur
  FPGA, Jetson ou MCU.

## Gaps identifiés

- **Coût de calcul absent** des benchmarks anti-UAV de suivi : aucun tracker évalué en
  FPS ni en W sur plateforme embarquée.
- **Air → air** : Anti-UAV est (probablement) filmé du sol ; un benchmark équivalent vu
  depuis un drone intercepteur manque ici (à croiser avec arxiv-2103.17242, Dogfight).
- **Fusion RGB-IR non alignée** embarquée : protocole III proposé, non traité.

## Statut de lecture

Papier complet (`fulltext.md` lu en entier, extraction GROBID `ok`). Manques
d'extraction : le début de l'introduction (§I) est perdu (le texte reprend en milieu de
phrase) ; la Table II (attributs) n'a pas de corps ; les **Tables V et VI (résultats DFSC,
ablation) sont absentes** ; la fin de §III-B et §III-C (répartition train/val/test,
distribution des positions) est tronquée ; une partie de §V-C est fondue dans les
Tables III et IV. `metadata.json` donne « arXiv preprint » : une version publiée en revue
existe peut-être, non vérifiée ici.

Ce qui suit est déduit et non affirmé par les auteurs :
- le scénario sol → air (position des caméras non décrite) ;
- la taille de la validation (67 séquences) ;
- le caractère lourd, non temps réel, des trackers en tête.
