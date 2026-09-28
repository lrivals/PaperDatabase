---
id: 2020-seidaliyeva-real-time-accurate-drone-detection
fiche: done
date: 2026-09-28
---

# Real-Time and Accurate Drone Detection in a Video with a Static Background

Ulzhalgas Seidaliyeva, Daryn Akhmetov, Lyazzat Ilipbayeva, Eric T. Matson, 2020, Sensors 20(14), 3856. https://doi.org/10.3390/s20143856
Type : article de journal

## Problème

Détecter des drones intrus près de sites protégés à partir d'une **caméra fixe**, en temps
réel, sans les confondre avec des oiseaux ou le fond. Le challenge Drone-vs-Bird mesure la
précision mais pas le temps d'exécution ; les auteurs visent une précision compétitive à
vitesse élevée (§1). C'est un scénario de contre-drone **sol → air**.

## Méthode

Pipeline en deux étages (§2, Fig. 1-2) :
1. **détection de mouvement** par soustraction de fond « two-points » [46/47], filtrage du
   bruit, dilatation, puis boîtes englobantes des régions (§2.1) ;
2. **classification** de chaque région en drone / oiseau / fond par un **MobileNetV2**
   modifié pour petites images, entrée 32×32×3 (§2.2).

Jeu de classification construit par les auteurs à partir de Drone-vs-Bird (10 155 drones,
1 921 oiseaux, 9 348 fonds) + 2 651 oiseaux de « Wild Birds in a Wind Farm », soit 24 075
images, découpage 80/20 (§3.1). Entraînement depuis zéro, SGD, batch 88, sur NVIDIA
GeForce GT 1030 2 Go (§3.2). Pas de quantification.

## Plateforme et implémentation

Matériel d'inférence **non précisé** (seul le GPU d'entraînement, GT 1030, est nommé) ;
CPU, précision, implémentation de la soustraction de fond n/r. Puissance n/r. Code : non
mentionné (non publié à notre connaissance). Aucun portage embarqué ; le capteur est fixe
au sol.

## Résultats

- Classifieur : 99,83 % d'exactitude « on the entire dataset » (§3.4, Fig. 5).
- Détection sur les 3 vidéos de test Drone-vs-Bird, IoU = 0,5 (Table 1) :

| Vidéo | Precision | Recall | F1 |
|---|---|---|---|
| gopro_001 | 0,786 | 0,817 | 0,801 |
| gopro_004 | 0,554 | 0,910 | 0,689 |
| gopro_006 | 0,735 | 0,691 | 0,712 |
| Global | 0,701 | 0,788 | 0,742 |

- Comparaison (Table 2, corps lu dans le texte de §4) : F1 0,742 contre 0,734 (Craye et al.
  [14], vainqueur 2019), 0,678 [30], 0,414 [38/39], 0,121 [28]. À IoU = 0,3, les auteurs
  reconnaissent faire « much worse than [14] » (§4).
- Vitesse : **9 images/s en moyenne à 1920×1080** ; un tiers du temps en classification, le
  reste en détection de mouvement ; la vitesse chute quand le fond bouge (§3.4, Fig. 10).
- 85 % des faux positifs viennent de boîtes imprécises (IoU < 0,5), 15 % d'erreurs de
  classification (§3.4).

→ reportés dans `benchmarks.csv` : 1 ligne (pipeline complet, F1 global Drone-vs-Bird,
9 FPS, Table 1 et §3.4). Plateforme n/r.

## Limites et critique

- **Hors du périmètre embarqué** : caméra fixe au sol ; la soustraction de fond suppose un
  fond statique et ne fonctionne pas depuis un drone en mouvement, ce que les auteurs
  reconnaissent (§2.1, §5). Rien n'est transférable tel quel à un intercepteur air → air.
- **« Temps réel » discutable** : 9 FPS en moyenne, sur un matériel non nommé, variable avec
  le mouvement du fond (§3.4). Aucune latence, aucune puissance.
- **Exactitude du classifieur surévaluée** : 99,83 % mesurés « on the entire dataset »,
  entraînement compris semble-t-il, et sur des imagettes extraites des mêmes vidéos que le
  test (fuite probable entre train et test, déduit).
- **Comparaison Table 2 hétérogène** : les chiffres des autres équipes viennent de leurs
  soumissions au challenge (éditions 2017/2019) ; les conditions ne sont pas contrôlées, et
  la comparaison de vitesse ne porte que sur [30] (0,58 FPS pour la seule super-résolution).
- Évaluation sur 3 vidéos seulement.

## Pertinence pour la thèse

Faible pour le thème. Contre-drone **sol → air**, exclu par le profil (l'IA n'est pas à
bord). Intérêt résiduel :
- référence de base « soustraction de fond + petit CNN » pour Drone-vs-Bird, utile comme
  point de comparaison historique pour un détecteur air → air ;
- rappelle que la distinction drone / oiseau à quelques pixels reste le verrou, et qu'un
  détecteur à fond mobile (caméra embarquée) doit s'en passer.

## Gaps identifiés

- Détection de drones depuis une caméra **mobile** (air → air) : la méthode échoue dès que le
  fond bouge ; c'est précisément le cas embarqué.
- Aucune mesure de latence / puissance sur plateforme embarquée pour ce type de pipeline
  léger (MobileNetV2 32×32), qui serait pourtant un bon candidat MCU/FPGA (déduit).

## Statut de lecture

Papier complet (`fulltext.md` lu en entier, extraction GROBID `ok`, nombreux paragraphes
dupliqués). La Table 2 est signalée « sans corps extrait » dans les avertissements, mais
ses valeurs apparaissent en texte brut sous « Methods » (§4) : lues là, alignement des
colonnes non garanti. Les Fig. 6, 7 et 10 (résultats par taille de drone, par IoU, vitesse)
ne sont pas lisibles dans le texte.

Ce qui suit est déduit et non affirmé par les auteurs :
- la fuite probable entre imagettes d'entraînement et vidéos de test ;
- l'intérêt d'un portage MCU/FPGA du classifieur ;
- l'absence de code publié (rien n'est mentionné).
