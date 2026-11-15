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
- Super-résolution : métriques de fidélité au-delà du PSNR/SSIM, détection d'hallucination
  (texture plausible sans gain d'information, risque pour l'encre).
- Physique et chimie de l'encre (Pb, XRF, XANES), agents de contraste, et modalités hors CT
  appliquées aux papyrus : thermographie, profilométrie de surface, NIR/SWIR, macro-XRF.
- Rouleaux modèles et fantômes carbonisés à vérité terrain connue (validation à l'aveugle).

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
- *Fantôme / rouleau modèle* : papyrus moderne écrit puis carbonisé, scanné pour disposer
  d'une vérité terrain.
- *Scorza* : couches externes, très dégradées, d'un rouleau d'Herculanum.

## Suggestions en attente

<!-- Une ligne par suggestion : - AAAA-MM-JJ (source : paper_id ou /base-profile) — proposition — raison -->

## Historique

- 2026-11-15 — base créée (`pdb base new`) ; profil, 12 axes et règles rédigés à partir des docs du dépôt Elder-scrolls (PRIZES, COMMUNITY_BRIEF, research/).
- 2026-11-15 — axe `ink-physics` ajouté (règle, requête, tags xrf/thermography/phantom) ; attribué à Tack 2016, Romano 2023, Ceccarelli 2025, Hoffmann 2026, Seiler 2026, 2603.27698 ; `ink-detection` retiré de Ceccarelli — suggestions Tack, Ceccarelli, profilométrie : chimie de l'encre et modalités hors CT sans axe.
- 2026-11-15 — Inclus : fidélité/hallucination en super-résolution, physique de l'encre et modalités hors CT, rouleaux modèles ; vocabulaire : fantôme, scorza — suggestions Boosting Resolution et Seiler.
- 2026-11-15 — bloc `plot` : 5 classes de tâches, 2 familles (scanner CT, XRF), figures FPGA écartées — 74 % des tâches et 24 % des plateformes classées « autre ».
- 2026-11-15 — `benchmarks.csv` : colonnes optionnelles input_res, dataset_split, metric_def, chunk_id — suggestion « colonnes adaptées au thème » (résolution, région tenue à l'écart) sans changer le schéma partagé.
