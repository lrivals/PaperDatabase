---
id: 2024-huang-anti-uav410-thermal-infrared-benchmark
fiche: done
date: 2026-09-28
---

# Anti-UAV410: A Thermal Infrared Benchmark and Customized Scheme for Tracking Drones in the Wild

Bo Huang, Jianan Li, Junjie Chen, Gang Wang, Jian Zhao, Tingfa Xu, 2024, IEEE Transactions on Pattern Analysis and Machine Intelligence 46(5), 2852-2865. https://doi.org/10.1109/TPAMI.2023.3335338
Type : article de journal

## Problème

Les jeux de suivi en infrarouge thermique (TIR) visent de grandes cibles ; le jeu Anti-UAV
[2] présente des drones assez gros (diagonale moyenne 40 px) sur fond de ciel ou de
bâtiments, loin des conditions réelles de suivi longue portée (§I, §III-D). Les trackers
TIR existants compensent l'absence de couleur mais ne traitent ni les cibles minuscules ni
le fouillis de fond dynamique (§II-C, §V-B). Les auteurs séparent explicitement le suivi
**vu du drone** (air → sol, UAV123, UAVDT) du suivi **anti-UAV** (la cible est le drone)
(§II-A).

## Méthode

Deux contributions :
- **Jeu Anti-UAV410** : 410 séquences TIR (moyen infrarouge, 25 FPS, 640×512), plus de
  438 k boîtes annotées à la main ; 100 min de vidéo propre (plus de 150 000 images) plus
  des vidéos reprises du 1st Anti-UAV Challenge et du jeu Anti-UAV [2], recadrées et
  « nettoyées » (§III-A). Découpage 200 / 90 / 120 séquences (train / val / test),
  équilibré à la main par attributs ; test indépendant, train et val tirés de clips
  disjoints des mêmes séquences (§III-C). Tailles (diagonale) : tiny [2,10), small
  [10,30), medium [30,50), normal ≥ 50 px ; 6 attributs (OV, OC, TC, FM, SV, DBC) ;
  77 séquences DBC et plus de 100 séquences à drone tiny (§I, §III-C). Longueur moyenne
  1069 images (§III-A).
- **Tracker SiamDT** : Siamese à backbone **Swin-Tiny** (pré-entraîné COCO, 12 époques),
  recherche **globale** sur toute l'image (RPN + RoI align à la GlobalTrack / Siam R-CNN),
  **DS-RPN** qui concatène sémantique de correspondance (corrélation depth-wise
  gabarit / recherche) et sémantique « présence d'un objet », **VR-CNN** à deux scores à
  poids partagés, et branche de **suppression des distracteurs** (mémoire d'au plus 50
  distracteurs du fond, mise à jour si IoU > 0,8 et S1 + S2 > 1,9) ; les trois scores sont
  combinés linéairement (§IV, §V-A).
- Évaluation OPE : précision (seuil 20 px), succès (AUC), **state accuracy (SA)** du jeu
  Anti-UAV, qui pénalise aussi les erreurs de présence / absence de la cible (§V-A).

## Plateforme et implémentation

GPU d'entraînement et d'inférence : n/r. Vitesse (FPS), latence, puissance, mémoire :
n/r. Aucun chiffre de coût de calcul (FLOPs, paramètres) dans le texte extrait. Code et
jeu de données : aucun lien dans le texte extrait (n/r).

Position du capteur : non décrite. La mention de l'azimut et du site de la caméra comme
information à ajouter (§VI) laisse penser à une caméra sur tourelle au sol (déduit).

## Résultats

- Sans entraînement sur Anti-UAV410, les trackers à recherche globale (Siam R-CNN,
  GlobalTrack) dominent ; les backbones plus profonds (Stark-ST101, SwinTrack-Base) ne
  battent pas leurs versions légères ; les trackers TIR dédiés (MMNet, MLSSNet, CMD-DiMP)
  sont faibles (§V-B, Table III — corps non extrait).
- Réentraîner sur Anti-UAV410 améliore tous les trackers testés ; six gagnent plus de 10 %
  sur val et test (§V-B, Table IV — corps non extrait).
- **SiamDT : SA 68,19 (test) et 71,65 (validation)**, premier, « légèrement » devant
  GlobalTrack et Siam R-CNN, jusqu'à ~30 % devant TCTrack et plus de 10 % devant Stark,
  TransT, ToMP et SwinTrack réentraînés (§V-B, texte).
- Par taille : écart croissant quand la cible rétrécit ; catégorie tiny : +23,3 % en
  précision et +18,4 % en succès face à SwinTrack (§V-B, Fig. 5).
- Ablations : sans recherche globale, −12,5 % (§V-C) ; SiamDS (double sémantique sans BDS)
  +0,9 point face à SiamMS et +1,3 face à SiamFS sur le test (§V-C, Table VI) ; backbone
  plus profond pas forcément meilleur (Table VII) ; fonction de perte presque sans effet
  (Table VIII).
- Généralisation : premier sur Anti-UAV (plus de 10 % devant la plupart des méthodes),
  seulement 7e sur LaSOT / GOT-10k (§V-D, Table V — corps non extrait).

→ reportés dans `benchmarks.csv` : 1 ligne (SiamDT Swin-Tiny, SA 68,19 sur le test
Anti-UAV410, plateforme n/r, `confidence: medium` car lu dans le texte, le corps de la
Table IV n'étant pas extrait).

## Limites et critique

- **Aucune mesure de vitesse ni de coût.** Swin-T + RPN global + R-CNN à deux passes +
  comparaison à 50 distracteurs : un pipeline lourd, dont le temps réel n'est pas établi.
  C'est l'inverse des contraintes d'un détecteur embarqué (déduit).
- **Contre-drone sol → air** (déduit de §VI, la position du capteur n'étant pas dite) :
  hors du périmètre « méthode » de la base. Le jeu reste utile comme **données TIR de
  petits drones**.
- **Pourcentages ambigus** : « 30 % », « plus de 10 % », « 23,3 % » ne précisent pas s'ils
  sont relatifs ou en points ; l'extraction a en outre perdu une valeur (« by a
  significant margin of more than in success plot ») (§V-B).
- **Comparaison hétérogène** : Table III évalue 25+ trackers avec leurs paramètres par
  défaut, sans réentraînement ; seuls quelques-uns sont réentraînés (Table IV). Le gain
  de SiamDT sur les trackers globaux est qualifié de « slight » par les auteurs.
- **Recouvrement potentiel** entre Anti-UAV410 et Anti-UAV [2] (vidéos réutilisées,
  §III-A) : les résultats croisés sur les deux jeux ne sont pas indépendants (déduit).
- **Répartition train/val** : val et train issus des mêmes séquences, donc la SA de
  validation (71,65) est optimiste ; seule la SA test (68,19) est retenue.

## Pertinence pour la thèse

- **Axe `counter-uav`** : référence de données TIR pour cibles drone minuscules (< 10 px),
  avec une métrique (SA) qui intègre la présence / absence — utile pour évaluer un
  détecteur-tracker **air → air** embarqué, même si les vidéos semblent filmées du sol.
- **Axe `tracking-navigation`** : montre que la **recherche globale** (re-détection sur
  toute l'image) domine sur petites cibles rapides (−12,5 % sans elle). Transposé sur
  cible embarquée, c'est un coût de calcul par image élevé : un compromis détecteur léger
  plein cadre + association contre tracker Siamese local reste à mesurer sur plateforme.
- Aucune contribution à `drone-fpga`, `nano-drone` ni `system-codesign`.

## Gaps identifiés

- **Suivi TIR de petits drones sans aucune mesure de coût** : ni FPS, ni FLOPs, ni
  plateforme. Aucun portage embarqué (Jetson, FPGA) d'un tracker anti-UAV TIR n'est
  mesuré ici.
- **Air → air en TIR** : pas de jeu TIR filmé depuis un drone porteur en mouvement dans ce
  papier (les attributs n'incluent pas l'ego-mouvement de la caméra).
- **Quantification / réduction de backbone et petits objets** : les auteurs notent que les
  backbones profonds nuisent aux cibles minuscules (Table VII) ; l'effet d'un backbone
  léger quantifié sur la SA « tiny » n'est pas mesuré.

## Statut de lecture

Papier complet (`fulltext.md` lu en entier, extraction GROBID `ok`). Les corps des Tables
I à V, VII et VIII **ne sont pas extraits** (légendes seules, cf. `extraction.warnings`) :
les chiffres des 25+ trackers comparés, de la Table II (distribution des tailles) et des
résultats LaSOT / GOT-10k manquent ; seuls les chiffres repris dans le texte sont cités.
Le résumé est tronqué à l'extraction. Une partie du §V-B (début du paragraphe sur la
Table IV et un pourcentage du paragraphe par attribut) est déplacée ou perdue.

Ce qui suit est déduit et non affirmé par les auteurs :
- la caméra au sol (sol → air), déduite de la mention azimut / site en §VI ;
- le caractère lourd, non temps réel, du pipeline SiamDT ;
- la non-indépendance entre Anti-UAV410 et Anti-UAV ;
- l'intérêt du jeu pour un détecteur air → air.
