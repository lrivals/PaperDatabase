# Profil — Vesuvius Challenge : lecture virtuelle des rouleaux d'Herculanum

Thème et périmètre de la base. La partie machine (axes, règles de classement, requêtes de
découverte) est dans `base.json` ; ce fichier en donne la justification. Le LLM propose des
changements (`/base-profile`, suggestions de `/paper-fiche`) ; rien n'est appliqué sans accord.

## Thème (utilisateur)

Vesuvius Challenge : lecture virtuelle des papyrus carbonisés d'Herculanum par micro-tomographie X — détection d'encre, segmentation et déroulage des surfaces, super-résolution et transfert entre résolutions, apprentissage auto-supervisé 3D, validation et faux positifs, papyrologie

## Précisions

- Finalité : appuyer le projet Elder-scrolls (dépôt `l1t-w1n/elder-scrolls`), une équipe qui
  concourt au [Vesuvius Challenge](https://scrollprize.org/prizes) : dérouler virtuellement et
  lire les rouleaux de papyrus carbonisés d'Herculanum à partir de scans micro-CT. Objectifs :
  Progress Prizes mensuels, First Letters (19 rouleaux éligibles, scan 8–9 µm), titre de
  PHerc. Paris. 4, Grand Prize 2027 (échéance 25/06/2027). Machine : un GPU de 32 Go
  (RTX 5090), 31 Go de RAM, ~200 Go de disque ; pile ML villa `vesuvius` (sous WSL).
- Chaîne visée : prédiction de surface (nnU-Net m7, U-Net 3D recto, champs Lasagna) →
  contraintes (patchs, fibres, ombilic) → ajustement de spirale → aplatissement (SLIM,
  flatboi) → rendu tifxyz → détection d'encre (Reader V3, `ink_9um`, Hecate…).
- Questions de recherche :
  - comment détecter une encre carbonée sans contraste d'absorption en CT, et que montrent les
    travaux publiés (Parker et al., Seales et al.) sur le signal exploité (texture, morphologie,
    topographie de surface) ?
  - quelle part du signal d'encre survit à 8–9 µm ? La super-résolution 9 → 2,4 µm sur paires
    recalées peut-elle aider, ou l'information est-elle perdue (risque d'hallucination) ?
    Comparer à la distillation enseignant 2,4 µm → élève 9 µm et au `scan_transfer`.
  - quelles méthodes de segmentation de feuillets minces, compressés et enroulés tiennent dans
    les zones « écrasées », les courbures serrées et les jonctions (kolleseis) ? Champs de
    nombre d'enroulement, level sets, suivi de fibres, optimisation sur graphe, instances 3D.
  - comment aplatir un maillage de grande taille avec une distorsion bornée (paramétrisation
    conforme, ARAP/SLIM) ?
  - quels pré-entraînements auto-supervisés 3D (DINO volumique, MAE) transfèrent aux scans de
    rouleaux ? Quels gains avec peu de labels (pseudo-labels denses, auto-entraînement) ?
  - comment transférer un modèle d'un rouleau, d'un scanner ou d'un protocole à l'autre
    (adaptation de domaine, harmonisation des histogrammes, augmentation) ?
  - comment prouver qu'une lettre est réelle : validation à l'aveugle, k-fold, tests placebo,
    lecture inversée, ensembles, calibration, incertitude ?
  - quelles connaissances papyrologiques (paléographie grecque, mise en page des colonnes,
    textes de Philodème) aident à valider ou lire une prédiction ?
- Toujours noter la résolution (µm/voxel), la source du scan (synchrotron, énergie keV,
  laboratoire), le rouleau ou le fragment, la nature des labels (IR, manuels, pseudo-labels)
  et si l'évaluation est sur une région ou un rouleau tenu à l'écart. Noter le matériel et le
  temps de calcul pour les méthodes lourdes.

## Inclus

- Déroulage virtuel de documents enroulés ou fermés (papyrus, parchemin, livres), dont les
  travaux EduceLab / Seales et le Vesuvius Challenge.
- Détection d'encre en tomographie X, en imagerie multispectrale ou IR des fragments, en
  topographie de surface.
- Segmentation de structures minces en 3D (feuillets, membranes, couches) et méthodes
  transférables d'autres domaines (géologie sismique, biologie, matériaux).
- Reconstruction et aplatissement de maillages, suivi de fibres et d'orientation (tenseur de
  structure), optimisation globale (flots, graphes, level sets).
- Imagerie micro-CT et synchrotron : contraste de phase, artefacts, résolution.
- Super-résolution volumétrique, recalage multi-résolution, distillation.
- Pré-entraînement auto-supervisé 3D, labels rares ou bruités, annotation interactive.
- Adaptation de domaine en imagerie volumique.
- Validation, faux positifs et hallucination des modèles en imagerie scientifique.
- Papyrologie d'Herculanum, paléographie grecque, reconnaissance de caractères anciens.

## Exclus

- Imagerie médicale sans méthode transférable (diagnostic clinique, radiologie de routine).
- Restauration physique ou chimique des papyrus sans volet imagerie.
- OCR de documents imprimés modernes.
- Histoire ou philologie sans lien avec la lecture des rouleaux d'Herculanum.

## Vocabulaire

- *Segment* : maillage d'une portion de feuillet ; *tifxyz* : format de quadmesh du projet.
- *Recto* : face écrite ; *winding* : un tour d'enroulement ; *umbilicus* : axe central.
- *Lasagna* : champs de normales, de phase et de fibres ; *spiral fit* : ajustement global.
- *Kollesis* (pl. kolleseis) : jonction collée entre deux feuilles de papyrus.
- *First Letters* : prix pour les premières lettres lisibles d'un rouleau.

## Suggestions en attente

<!-- Une ligne par suggestion : - AAAA-MM-JJ (source : paper_id ou /base-profile) — proposition — raison -->
- 2026-11-15 (arxiv-1907.07131-boosting-resolution-recovering-texture-micro) — ajouter « métriques de fidélité de texture / hallucination en super-résolution GAN » aux Inclus (axe super-resolution ou validation-fp) — le papier admet que le PSNR ne mesure pas la texture générée.
- 2026-11-15 (arxiv-2603.27698-ink-detection-surface-topography-herculaneum) — ajouter la profilométrie optique de surface comme modalité d'étude du signal d'encre (hypothèse morphologique) — papier ink-detection dont la modalité n'est ni CT ni IR/multispectral.
- 2026-11-17 (2025-hoffmann-synchrotron-x-ray-mapping-xenon) — ajouter aux Inclus « agents de contraste et marquage physique/chimique de l'encre carbonée (sorption de gaz, xénon, imagerie au seuil K) » — complément non appris à la détection d'encre, absent du profil.
- 2026-11-17 (2022-wang-virtual-unrolling-technology-terahertz-computed) — ajouter aux Inclus l'imagerie THz CT (hors rayons X) pour le déroulage de documents roulés — modalité non X, `ct-imaging` est centré synchrotron/micro-CT.
- 2026-11-15 (/paper-fiche, agent principal) — adapter les colonnes de benchmarks.csv au thème (résolution µm/voxel, source du scan, région tenue à l'écart, type de labels) — l'en-tête FPGA (fps, luts, power…) laisse 10 colonnes sur 20 à n/r.
- 2026-11-15 (2019-tournie-ancient-greek-text-concealed-back, 2025-verde-sub-terahertz-radar-imaging-ancient) — ajouter aux Inclus l'imagerie non CT des papyrus déjà déroulés (SWIR hyperspectral, radar sub-THz) ou un axe dédié — ces deux papiers ne relèvent que de `papyrology`, tous les axes d'imagerie étant centrés sur la CT.
- 2026-11-15 (2016-brun-revealing-metallic-ink-herculaneum-papyri) — ajouter aux Inclus l'analyse élémentaire de l'encre (XRF/XRD synchrotron sur fragments : Pb, composition), rattachée à `ink-detection` ou `papyrology` — conditionne le contraste attendu de l'encre en micro-CT.
- 2026-11-17 (veille_communaute.md, 11 dépôts ingérés) — ajouter aux Inclus « travaux communautaires du Vesuvius Challenge publiés sur GitHub (dépôts figés à un commit, type `repo`) », avec la règle : chiffres auto-déclarés, jamais comparés sans contrôle commun — ils portent l'essentiel des mesures sur rouleaux entiers.

## Historique

- 2026-11-15 — base créée (`pdb base new`) ; profil, 12 axes et règles rédigés à partir des docs du dépôt Elder-scrolls (PRIZES, COMMUNITY_BRIEF, research/).
- 2026-11-17 — 11 sources communautaires (dépôts GitHub du canal « show and tell » et Rectina) ingérées et fichées ; premier passage de `gaps.md` ; état de l'art v4 (53 papiers).
