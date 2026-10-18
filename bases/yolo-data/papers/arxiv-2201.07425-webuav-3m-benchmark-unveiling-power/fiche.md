---
id: arxiv-2201.07425-webuav-3m-benchmark-unveiling-power
fiche: done
date: 2026-10-18
benchmarks: none
---

# WebUAV-3M: A Benchmark for Unveiling the Power of Million-Scale Deep UAV Tracking

Chunhui Zhang, Guanjie Huang, Li Liu, Shan Huang, Yinan Yang, Xiang Wan, Shiming Ge, Dacheng Tao, 2022, arXiv preprint. https://arxiv.org/abs/2201.07425
Type : preprint non relu par les pairs (version lue : arXiv v4, 31 déc. 2022)

## Problème

Les benchmarks de suivi mono-objet (SOT) depuis drone sont, selon les auteurs, trop petits pour
entraîner des trackers profonds (rarement plus de 500 vidéos), sans langage ni audio, avec peu
de classes et un protocole d'évaluation pauvre (§1, points i à iv). Pour cette base, la partie
utile est le **problème d'annotation** : étiqueter 3,3 M d'images à la boîte est impossible à la
main ; les auteurs proposent le pipeline SATA et un contrôle qualité en plusieurs passes (§1,
§3.3, Table 2).

## Méthode

Contribution de type **jeu de données + outil d'annotation + protocole**, sans modèle nouveau.

- **WebUAV-3M** : 4 500 vidéos, plus de 3,3 M d'images et environ 3,3 M de boîtes, 223 classes
  de cibles, 63 classes de mouvement, 12 super-classes (§1, §3.2). 3 617 vidéos YouTube, plus
  616 vidéos de Stanford Drone et 267 d'Okutama-Action réannotées par SATA (§3.2).
- **SATA** (semi-automatic target annotation), 5 étapes en boucle (§3.3, Fig. 4) :
  1. l'humain dessine la boîte de la cible sur la première image ;
  2. étiquette manuelle de l'image courante (première image, ou image corrigée) ;
  3. initialisation, puis réentraînement facultatif du tracker (SiamRPN++ préentraîné, §3.3,
     Annexe B) sur les boîtes corrigées ; l'étape peut être sautée à la main ;
  4. le tracker prédit la boîte de l'image suivante à partir de la boîte validée précédente ;
  5. l'annotateur vérifie en temps réel, garde ou ajuste la boîte, et la boucle repart jusqu'à
     la fin de la vidéo.
  L'annotateur découpe la vidéo en segments courts et peut choisir un nouveau point de départ
  quand le suivi se dégrade (Annexe B). Le tracker est donc un « dessinateur de boîtes » ; l'humain
  ne fait que valider ou corriger.
- **Règles d'annotation** (A.1) : boîte aussi serrée que possible sur toutes les parties
  visibles (autorisée à être légèrement trop petite plutôt que trop grande) ; pas de boîte
  quand la cible est entièrement masquée (étiquette « absent ») ; occlusion et réapparition
  annotées sur tout leur déroulé.
- **Contrôle qualité en 10 étapes** (Table 2) : vérification de toutes les vidéos par les
  auteurs, annotation par une équipe professionnelle d'environ 10 personnes, vérification des
  boîtes par une équipe de vérification sur 75 % des données, puis par les auteurs sur 100 %
  et 3 fois (« ×3 »), idem pour attributs, langage et audio, puis acceptation.
- Tracking en quelques lignes : 17 attributs, une phrase anglaise par vidéo et 9 000
  descriptions audio synthétiques (§3.4-3.5) ; découpage 3 520 / 200 / 780 vidéos (§3.6, avec
  une coquille probable « 520 » en A.6) ; protocole UTUSC (7 sous-ensembles de test, §4) ;
  métrique cAUC (§5.3) ; 43 trackers évalués sur le test (§5.4, Table 5).

## Plateforme et implémentation

Pas d'implémentation embarquée. Évaluation sur serveur : Intel Xeon Gold 6230R, 3 × NVIDIA RTX
A5000 (§5.2). Puissance : n/r. Données, toolkit et résultats annoncés publiés :
https://github.com/983632847/WebUAV-3M. Le code de l'outil SATA lui-même : non mentionné comme
publié dans les passages lus (n/r).

## Résultats

Annotation (Annexe B, Table 3) : temps moyen par boîte mesuré par les auteurs sur 30 vidéos
(10 faciles, 10 moyennes, 10 difficiles), annotés indépendamment par des annotateurs
expérimentés (nombre n/r) :

| Outil | Type | Facile | Moyen | Difficile | Moyenne |
|---|---|---|---|---|---|
| Labelme | manuel | 13,23 s | 16,08 s | 18,11 s | 15,81 s |
| VoTT | manuel | 6,87 s | 8,61 s | 8,67 s | 8,05 s |
| ViTBAT | semi-auto | 2,50 s | 5,60 s | 5,96 s | 4,68 s |
| CVAT | semi-auto | 1,71 s | 3,76 s | 6,12 s | 3,86 s |
| SATA | semi-auto | 0,11 s | 2,94 s | 5,91 s | 2,99 s |

- SATA : environ 5,3 fois moins de temps que Labelme et 2,7 fois moins que VoTT en moyenne
  (rapports calculés ici à partir de la Table 3, pas donnés par les auteurs). Le gain fond avec
  la difficulté : 0,11 s (facile) contre 5,91 s (difficile), soit près du temps de CVAT (6,12 s).
- Tout le jeu étiqueté « en moins de trois mois » (§1, nombre d'annotateurs et d'heures
  totales : n/r au-delà de l'équipe d'environ 10 personnes, Table 2).
- **Part de boîtes produites automatiquement, part corrigée : n/r.** Le papier ne compte ni le
  taux d'acceptation des prédictions, ni le nombre de corrections par vidéo.
- Qualité vérifiée indirectement (§5.7, Table 6, Fig. 13) : cinq trackers réentraînés sur le
  train set annoté par SATA gagnent en cAUC sur le test (SiamFC 0,317 → 0,417 ; SiamRPN
  0,317 → 0,415 ; ATOM 0,261 → 0,344 ; MDNet 0,347 → 0,409 ; GOTURN 0,178 → 0,280). Les
  baselines sont entraînées sur d'autres données (ImageNet VID, etc.), donc l'écart mêle qualité
  des labels et décalage de domaine (les auteurs écrivent « excluding the influence of the
  domain gap », Annexe B, sans l'isoler).
- Effet du volume (Fig. 13, §5.7) : SiamRPN progresse nettement de 1 % (35 vidéos) à 10 %
  (350 vidéos) des données puis converge ; SiamFC sature plus tôt et peut décliner à 100 %
  (surapprentissage). Courbes seulement, pas de valeurs lues.
- Suivi : AlphaRefine premier (Pre 0,753, AUC 0,593, cAUC 0,562, 42,3 FPS sur GPU) (Table 5) ;
  des trackers à features manuelles égalent certains trackers profonds (§5.4). Les autres
  lignes de la Table 5 ont des colonnes décalées à l'extraction : non reprises ici.
  Évaluation de 43 trackers sans réglage (§5.2).

Lignes proposées pour `benchmarks.csv` (7, fichier `.cache/bench/`) : 5 temps d'annotation
(Table 3) et 2 réentraînements (Table 6, cAUC).

## Limites et critique

- **Aucune mesure sur les boîtes erronées.** L'exactitude de SATA n'est pas comparée à une
  annotation manuelle de référence : les auteurs jugent l'expérience impraticable (Annexe B) et
  avancent la qualité par la performance des trackers réentraînés, preuve indirecte.
- **Biais du tracker** : SiamRPN++ propose les boîtes, un annotateur pressé peut valider une
  dérive. Les auteurs le discutent (segments courts, reprise du point de départ, contrôle en
  10 étapes) sans le mesurer (Annexe B).
- **Temps par boîte mesuré sur 30 vidéos** seulement, annotateurs et conditions mal décrits ;
  la Table 3 ne donne pas d'écart-type. Le gain « facile » (0,11 s) vient de vidéos où le tracker
  suit presque sans correction (déduit).
- Le test est choisi par difficulté avec 10 trackers (A.6), ce qui le biaise (déduit). Les FPS
  sont sur RTX A5000 ou CPU Xeon, sans puissance. Vidéos YouTube sans métadonnées de vol.
- Incohérences mineures : KCF 132,0 FPS dans le texte (§5.4) contre 132,9 en Table 5 ; 520 contre
  3 520 vidéos d'entraînement (A.6 contre §3.6). Métriques SOT non comparables au mAP.

## Pertinence pour cette base

Ce que le papier apprend pour **annoter** (et un peu pour construire) un dataset de détection :

- **Boucle humain ↔ modèle prouvée à grande échelle** : un modèle propose la boîte suivante,
  l'humain valide ou corrige, le modèle est réentraîné sur les corrections (§3.3). C'est la
  même boucle que la pré-annotation par détecteur ou SAM pour des images, avec la propagation
  temporelle en plus.
- **Ordre de grandeur du gain** : 2,99 s contre 15,81 s par boîte avec Labelme (Table 3), mais
  ce gain dépend de la difficulté (0,11 à 5,91 s). À budgéter par difficulté, pas en moyenne.
- **Contrôle qualité** : ne pas se fier à la seule passe de l'annotateur : vérification sur
  75 % puis 100 % trois fois par une autre équipe (Table 2). Modèle de gabarit pour un dataset
  maison, au coût d'un jeu à 3,3 M de boîtes.
- **Consignes de boîte** : « serrée, légèrement trop petite plutôt que trop grande », pas de
  boîte pour un objet totalement masqué, occlusion suivie (A.1) : à comparer aux consignes
  d'occultation/troncature de la base.
- **Réutilisable pour un jeu YOLO (déduit, non testé par les auteurs)** : sur des vidéos de
  drone ou de caméra fixe, SATA permet d'obtenir beaucoup de boîtes de la même instance par
  vidéo ; pour des images isolées, seul le principe « proposer, corriger, réentraîner » se
  transpose ; la propagation d'une boîte d'image en image n'existe pas sans continuité
  temporelle. Les images successives étant très corrélées, elles gonflent le nombre de boîtes
  sans augmenter la diversité (déduit) : à sous-échantillonner avant l'entraînement d'un
  détecteur.
- **Volume** : SiamRPN gagne beaucoup entre 35 et 350 vidéos puis converge (§5.7) : indice
  (suivi, pas détection) d'une saturation du gain avec le volume.
- **Dataset** : jeu de suivi, pas de détection ; format boîte `[x, y, w, h]` en pixels, pas de
  format YOLO normalisé. Cibles ≈ 50 pixels en moyenne (§3.7) : petits objets.

Quand l'appliquer : annotation de séquences vidéo (drone, caméra fixe) à grande échelle avec
un budget d'annotation limité ; pas pour des images indépendantes.

## Gaps identifiés

- **Part de boîtes acceptées sans correction, taux d'erreur résiduel** de l'annotation
  assistée par tracker : non rapportés ; aucune comparaison à une vérité terrain manuelle.
- **Biais d'un pré-annotateur** sur le jeu final (le tracker valide ses propres dérives) :
  discuté, non mesuré.
- **Transfert vers images isolées** (pré-annotation SAM ou détecteur) : non traité.

## Statut de lecture

Papier complet (`fulltext.md` lu pour les sections liées à l'annotation : §1, §3, §5.7,
Annexes A.1 et B, Tables 2, 3, 6 ; le reste, notamment §4 et §5.4-5.6, repris de la fiche
d'origine après vérification des chiffres cités). Extraction GROBID `ok`. Tables 3 et 11
reconstruites par PyMuPDF, Tables 4, 5, 6 et A par Docling (à vérifier) : les valeurs de la
Table 3 se recoupent avec le texte de l'Annexe B (15,81 / 8,05 / 4,68 / 3,86 / 2,99 s) ; la
Table 6 est lisible ; la Table 5 a des colonnes décalées sur plusieurs lignes (non reprises).
Résultats UTUSC en figures seulement (non lus). Texte tronqué en fin de §5.6 et dans les
« Future Directions ».

Déduit et non affirmé par les auteurs : les rapports de temps SATA/Labelme et SATA/VoTT ;
l'explication du gain « facile » ; le biais de sélection du test ; la transposition de SATA à des
images isolées et la corrélation entre images successives ; l'absence de données embarquées.
