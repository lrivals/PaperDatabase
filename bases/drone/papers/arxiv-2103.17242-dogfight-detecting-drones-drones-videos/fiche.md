---
id: arxiv-2103.17242-dogfight-detecting-drones-drones-videos
fiche: done
date: 2026-09-28
---

# Dogfight: Detecting Drones from Drones Videos

Muhammad Waseem Ashraf, Waqas Sultani, Mubarak Shah, 2021, arXiv preprint. https://arxiv.org/abs/2103.17242
Type : preprint non relu par les pairs selon `metadata.json`. Une version publiée en
conférence (CVPR 2021) est probable, mais elle n'est pas vérifiée dans la base.

## Problème

Détecter des drones dans des vidéos filmées **depuis un autre drone en vol (air → air)**,
pour l'anti-collision, le vol multi-drones sûr et la défense contre les attaques de drones
(§1). Les difficultés sont les suivantes :
- des cibles minuscules, qui occupent en moyenne 0,05 % (NPS) et 0,07 % (FL) de l'image,
  contre environ 20 % sur VOC et ImageNet (§1) ;
- les mouvements brusques de la caméra et de la cible, des formes changeantes, des
  occlusions par les nuages et des variations d'illumination.

Selon les auteurs, les détecteurs à propositions de régions capturent mal le contraste
entre la cible et le fond. L'agrégation temporelle de features (MEGA, SLSA) fonctionne pour
les gros objets, pas pour les drones, où il vaut mieux un **mouvement explicite** (§1, §2).

## Méthode

Approche en **deux étages, fondée sur la segmentation** (Fig. 2).
- **Étage 1, apparence** : l'image est découpée en tuiles qui se chevauchent (9 pour NPS,
  4 pour FL). Chaque tuile passe dans un **ResNet50\***, qui concatène les features des
  4 blocs pour garder le détail local, puis dans un pyramid pooling (PSP) et des attentions
  par canal et par pixel. Pertes : focal loss, DIoU et smooth-L1 sur l'attention (§3.1-3.3).
- **Étage 2, spatio-temporel** : de nouveaux candidats sont trouvés grâce aux **frontières
  de mouvement** (gradients de flot optique après stabilisation par points-clés sur
  3 images, dilatation, puis CRF). Chaque candidat, y compris ceux de l'étage 1, est suivi
  par un tracker à corrélation sur **8 images** (3 en avant, 4 en arrière). On en extrait
  des cuboïdes N×N×8, redimensionnés en 224×224×8. Ils passent dans un **I3D** figé
  (pré-entraîné sur Kinetics), puis dans un PSP et les attentions (§3.4).
- Post-traitement : les détections présentes sur une seule image sont supprimées, et les
  candidats hors de la plage de tailles vue à l'entraînement sont filtrés (§4.1).
- **Ré-annotation** complète de NPS-Drones et FL-Drones, dont les boîtes d'origine sont
  jugées trop grandes (§4.2, Fig. 8). Les auteurs annoncent leur publication.

## Plateforme et implémentation

- Entraînement de toutes les méthodes sur **une seule GTX 1080Ti** (§4.3).
- **Aucune mesure de temps d'inférence, de FPS ni de puissance.** Le pipeline cumule flot
  optique, stabilisation, CRF, tracking et I3D pour chaque candidat, ce qui le rend lourd
  (déduit). Rien n'est embarqué.
- Code : non mentionné dans le texte extrait. Les annotations améliorées sont annoncées
  « will be released » (§4.2).

## Résultats

Évaluation sur une image sur quatre du test, chaque image étant traitée indépendamment ;
seuil IoU de l'AP non précisé (§4.1).

| Jeu | Précision | Rappel | F1 | AP | Meilleur baseline (AP) | Source |
|---|---|---|---|---|---|---|
| NPS-Drones (50 vidéos HD, 10 en test) | 0,92 | 0,91 | 0,92 | 0,89 | Mask-RCNN 0,89 ; FCOS 0,83 | Table 1 |
| FL-Drones (14 vidéos, 640×480 et 752×480) | 0,84 | 0,76 | 0,80 | 0,72 | Mask-RCNN 0,68 | Table 2 |

- Ablation sur NPS (F1, Table 3) : 0,85 avec l'entropie croisée seule, 0,86 avec focal et
  DIoU, 0,87 avec l'attention par canal ou par pixel, **0,90 pour l'étage 1** et **0,92
  pour les deux étages**. Le rappel passe de 0,88 à 0,91.
- Un seul étage multi-images a été essayé : F1 inférieur à 40 (§4.4).
- Échecs : drones lents et de forme peu distinctive (Fig. 10, §4.4).

→ reportés dans `benchmarks.csv` : 2 lignes, la méthode proposée sur NPS-Drones (AP 89) et
sur FL-Drones (AP 72), Tables 1-2, `high`. FPS et puissance `n/r` ; plateforme GTX 1080Ti
(entraînement).

## Limites et critique

- **Aucun coût de calcul rapporté**, alors que le cas d'usage visé est l'anti-collision à
  bord. Le pipeline n'est pas embarquable en l'état (déduit) : flot optique, stabilisation,
  CRF, tracker, I3D par cuboïde, et fenêtre temporelle de ±4 images qui impose une
  **latence d'au moins 4 images** (déduit du tracking « 3 frames forward »).
- **Protocole de comparaison discutable** : les baselines sont réglés à partir de poids
  pré-entraînés, avec 80 000 à 100 000 itérations « due to computational power
  limitations » (§4.3), et évalués avec les annotations refaites par les auteurs. Sur NPS,
  Mask-RCNN atteint la même AP (0,89) ; le gain porte sur le F1.
- **Métrique non normalisée** : AP sans seuil IoU explicite, une image sur quatre. Les
  résultats ne sont pas comparables aux mAP multi-classes de type VisDrone.
- Les chiffres NPS et FL reposent sur de **nouvelles annotations**, ce qui empêche une
  comparaison directe avec les travaux antérieurs sur les annotations d'origine ([24], [33]).
- Découpage NPS : les 40 premières vidéos pour l'entraînement et la validation, les 10
  dernières pour le test. FL : moitié-moitié. Il n'y a qu'un seul découpage.

## Pertinence pour la thèse

- **Référence de l'axe contre-drone air → air** : c'est bien le cas embarqué visé par le
  profil (détecteur sur un drone intercepteur). NPS-Drones et FL-Drones, ré-annotés, sont
  les jeux de référence de cette tâche.
- Il montre que le **mouvement explicite** apporte du rappel (Table 3) pour des cibles de
  10 à 20 pixels. Ce résultat est utile pour concevoir un détecteur embarqué, mais son coût
  n'est pas chiffré.
- **Laisse ouvert** toute la question embarquée : un équivalent léger du pipeline
  (flot optique matériel, segmentation légère) sur Jetson, FPGA ou MCU, avec une latence
  mesurée.

## Gaps identifiés

- **Détection air → air de drones à coût mesuré** : Dogfight, qui est la référence de
  précision, ne donne ni FPS ni puissance. C'est un gap direct pour un détecteur embarqué
  sur un intercepteur.
- **Indices temporels et de mouvement sur FPGA** : flot optique et fenêtre multi-images
  pour les petites cibles. Coût et latence à quantifier.
- **Comparabilité des jeux contre-drone** : annotations refaites, métriques propres. Il
  manque un protocole commun.

## Statut de lecture

Papier complet (`fulltext.md` lu en entier, extraction GROBID `ok`). Des passages sont mal
ordonnés : la légende de la Fig. 1 est mêlée à l'introduction, et la description de
l'attention par pixel est tronquée en §3.2. Le warning « tableaux sans corps extrait :
Table » concerne un fragment vide. Les Tables 1-3 ont bien un corps et ont été lues.

Ce qui suit est déduit et non affirmé par les auteurs :
- le caractère non embarquable et le coût du pipeline ;
- la latence minimale liée à la fenêtre temporelle ;
- la publication probable à CVPR 2021, non vérifiée.
