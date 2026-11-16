# Carte des gaps — Vesuvius Challenge : lecture virtuelle des rouleaux d'Herculanum

Zones non couvertes et verrous repérés dans le corpus. Mis à jour par `/paper-gaps` à partir
des fiches `done` et de `benchmarks.csv`. Chaque gap cite les `paper_id` qui l'étayent et
distingue ce qui est lu de ce qui est déduit.

Format d'une entrée :

```
### <intitulé du gap>
- Constat : ce que montre le corpus (paper_id, section source).
- Ce qui manque : la question laissée ouverte.
- Statut : hypothèse (déduite de la bibliographie de départ) | étayé (fiches done).
- Piste : expérience ou lecture pour le confirmer.
```

Sections sources des fiches : **[L]** « Limites et critique », **[G]** « Gaps identifiés »,
**[P]** « Pertinence ». Entre parenthèses après le crochet : la section du papier citée par la
fiche, quand elle existe.

---

Carte du 16/11/2026, **1ᵉʳ passage** : **34 fiches `done` sur 34**, **72 lignes** dans
`benchmarks.csv` (10 papiers ; 24 papiers sans ligne, presque tous à évaluation qualitative).

**Portée des statuts.** « Étayé » signifie que plusieurs fiches constatent le manque dans les
papiers lus (mesure absente, limite reconnue par les auteurs, case vide de `benchmarks.csv`
recoupée par [L] et [G]). Cela ne prouve pas que le travail n'existe nulle part. Le corpus
compte 34 papiers. Il est biaisé vers les travaux fondateurs du déroulage (22 papiers dans
`virtual-unwrapping`), l'imagerie (19) et la papyrologie (17). Il est très mince sur les axes
ML du projet : `super-resolution` 1, `domain-transfer` 1, `label-efficiency` 2,
`validation-fp` 2, et aucun papier d'auto-supervisé 3D. Il ne contient aucun rapport des
gagnants du Vesuvius Challenge (Progress Prizes, Grand Prize 2023). Un gap qui ne repose que
sur l'absence d'un type de papier dans la base reste une **hypothèse**.

### Chiffres de couverture (`benchmarks.csv`, 72 lignes)

| Constat | Valeur |
|---|---|
| Lignes par papier | 21 topographie de surface (arxiv-2603.27698), 15 livre fermé en CT de laboratoire (2018-stromer), 8 Korotetskyi, 7 Quattrini, 6 Henderson, 6 Mou, 9 pour 4 autres papiers |
| Lignes de détection d'encre mesurées en CT sur un rouleau entier à 8–9 µm | **0** (fragments à 3,2–4 µm, profilométrie à 0,34 µm, Scroll 5 à résolution n/r) |
| Métriques d'encre | Dice médian (21), CR_msr (15), MCC (8), F0.5 (6), Dice (6), rappel de caractères (2) : aucune métrique commune à deux papiers d'encre |
| `dataset_split` à `n/r` | 64 / 72 |
| `measure_protocol` à `n/r` | 55 / 72 |
| `input_res` à `n/r` | 41 / 72 |
| `confidence` | 29 `high`, 40 `medium`, 3 `low` |
| Lignes de qualité de surface ou d'aplatissement | 6, toutes de Henderson (ChD, WJF, AD, Str) sur une région de PHerc. Paris 4 |

Les colonnes héritées du gabarit FPGA (`fps`, `luts`, `power_w`…) sont vides par construction ;
le temps de calcul (`latency_ms`) est `n/r` sur 68 lignes.

---

## A. Signal d'encre et résolution

### A1. Part du signal d'encre qui survit à 8–9 µm : non mesurée en CT
- Constat : le signal exploité est décrit comme morphologique ou de texture, avec une
  résolution utile de 3–12 µm (2019-parker-invisibility-readability-recovering-ink-herculaneum,
  [P], [G]) ou de 5–10 µm (arxiv-2304.02084-educelab-scrolls-verifiable-recovery-text, [P]
  (§4.1.1)), affirmée qualitativement (même fiche, [G]). La seule courbe chiffrée
  résolution → score vient de la profilométrie de surface, sans CT : Dice < 0,70 au-delà
  d'environ 1 µm effectif (arxiv-2603.27698-ink-detection-surface-topography-herculaneum,
  [P] (Table 1), [L]). Sur Paris 4, la comparaison 7,91 µm / 2,4 µm confond gain de scan et gain
  de modèle (arxiv-2606.29085-complete-virtual-unwrapping-reading-rolled, [L], [G]).
  2026-korotetskyi-volumetric-texture-analysis-unsupervised-ink ne donne pas la résolution
  ([L]) et laisse la question ouverte ([P]). En contraste de phase, 2015-mocella et
  arxiv-1706.09883 lisent à 47–100 µm, mais par un autre mécanisme ([L]).
- Ce qui manque : une mesure, sur les mêmes régions, d'un même détecteur à 2,4 µm,
  dégradé vers 8–9 µm, et à 8–9 µm natif, avec une PSF réelle et non une moyenne de blocs.
- Statut : **étayé** (5 fiches le constatent).
- Piste : paires recalées 2,4 / 7,91 µm de Paris 4 (arxiv-2606.29085) ; entraîner le même
  lecteur aux deux résolutions et tracer F0.5 en fonction de la résolution simulée par la vraie
  PSF du scanner.

### A2. Super-résolution volumétrique 9 → 2,4 µm : un seul papier, hors domaine
- Constat : seul arxiv-1907.07131-boosting-resolution-recovering-texture-micro traite de SR :
  2D, roches, LR synthétique bicubique, PSNR comme seule métrique, texture GAN non vérifiable
  et « scepticisme légitime » reconnu par les auteurs ([L] (§4.2, Conclusion), [G]). La
  topographie montre qu'un modèle entraîné fin se dégrade mieux qu'un modèle entraîné grossier
  jusqu'à environ 1 µm (arxiv-2603.27698, [P]) : argument indirect pour la distillation.
- Ce qui manque : SR 3D sur paires CT réelles recalées ; métrique de préservation du signal
  d'encre (texture) au-delà du PSNR ; comparaison SR contre distillation enseignant 2,4 µm →
  élève 9 µm.
- Statut : **hypothèse** pour l'absence de travaux (un seul papier dans l'axe) ; **étayé**
  pour le risque d'hallucination de la SR GAN (arxiv-1907.07131, [L]).
- Piste : `/paper-discover super-resolution` (SR volumétrique micro-CT sur paires réelles,
  SR de roches et de matériaux 3D, distillation entre résolutions).

### A3. Composition de l'encre (plomb ou carbone) et effet sur le signal CT
- Constat : du Pb est mesuré dans deux fragments seulement
  (2016-brun-revealing-metallic-ink-herculaneum-papyri, [L] ;
  2016-tack-tracking-ink-composition-herculaneum-papyrus, [L], [G]). La part de la
  collection concernée est `n/r` (2021-damiani-ink-herculaneum-survey-recent-perspectives,
  [G]). Une encre plombée facilite la lecture sur rouleau modèle
  (2026-seiler-model-carbonized-papyrus-scroll-opens, [L]) ; du Pb de réglure ou de
  contamination peut brouiller ce signal (2023-romano-layout-ancient-greek-papyri-through,
  [P], [G]). Le lien concentration de Pb → contraste à 8–9 µm n'est mesuré nulle part
  (2016-brun, [G] ; 2016-tack, [G]). L'échec de Korotetskyi sur Scroll 1 n'est pas expliqué
  ; le type d'encre fait partie des causes évoquées (2026-korotetskyi, [G]).
- Ce qui manque : un lien entre composition d'encre et performance des lecteurs, rouleau par
  rouleau.
- Statut : **étayé**.
- Piste : croiser les scores des lecteurs par rouleau avec tout dépistage XRF disponible ;
  lire Brun et al. sur le contraste de phase si un papier de suivi existe.

### A4. Créer un contraste physique (xénon, sorption) : non évalué sur papyrus réel
- Constat : 2026-hoffmann-xenon-contrast-carbon-ink-tomography montre un contraste sur un
  échantillon modèle seulement, sans mesure de contraste-bruit ni protocole de conservation
  ([L], [G]). Poster, non relu.
- Ce qui manque : un essai sur papyrus carbonisé et des paires de scans avec et sans
  marqueur, qui donneraient un label dense.
- Statut : **hypothèse** (un seul document, préliminaire).
- Piste : suivre la réf. [1] de Hoffmann (non lue).

---

## B. Validation des lettres, faux positifs, hallucination

### B1. Aucun protocole de validation à l'aveugle, placebo ou calibré
- Constat : aucun papier de la base ne décrit de lecture à l'aveugle, de test placebo, de
  lecture inversée ni de calibration des cartes d'encre. Le manque est relevé dans 2015-mocella
  ([L], [G]), arxiv-1602.08071 ([L]), arxiv-1706.09883 ([L], [G]), 2019-parker ([L], [G]),
  arxiv-2304.02084 ([L], [G]), arxiv-2308.05070 ([L], [G]), 2023-mou ([L], [G]),
  arxiv-2603.27698 ([L], [G]), arxiv-2606.29085 ([L], [G]), 2026-seiler ([L]). Les lectures
  dites « confirmées » viennent souvent des éditeurs des textes eux-mêmes
  (2025-ceccarelli-pulsed-thermographic-analysis-herculaneum-papyri, [L]) ou d'un seul
  papyrologue (arxiv-2304.02084, [L]).
- Ce qui manque : un protocole de preuve d'une lettre (aveugle, k-fold par rouleau, placebo
  sur zones sans papyrus, incertitude).
- Statut : **étayé** (10 fiches ou plus).
- Piste : `/paper-discover validation-fp` hors du domaine (hallucination en imagerie
  scientifique, calibration en segmentation médicale, tests placebo en astronomie).

### B2. Risque d'hallucination des lecteurs et des « amplificateurs de visibilité » non quantifié
- Constat : rendu « photoréaliste » appris sans discussion du risque (2019-parker, [L]) ;
  modèles présentés comme « amplificateurs de visibilité » sans mesure
  (arxiv-2606.29085, [L], [G]) ; affirmation d'« absence d'hallucination » non vérifiée
  (arxiv-2304.02084, [L]) ; SR GAN (arxiv-1907.07131, [L]) ; mise en garde de papyrologues
  sur les réseaux qui « hallucinent » des formes de lettres
  (arxiv-2104.01106-personalizing-image-enhancement-critical-visual, [P] (§6.1)).
- Ce qui manque : mesure du taux de lettres produites sur zones sans encre connue.
- Statut : **étayé**.
- Piste : test placebo sur un rouleau modèle à texte connu (2026-seiler) ou sur des
  zones vierges, à combiner avec A1.

### B3. Faux positifs dus aux fibres, plis et fissures : reconnus, jamais chiffrés
- Constat : fibres confondues avec l'encre (2019-parker, [L] ; 2026-korotetskyi, [L] (§8) ;
  arxiv-2603.27698, [L]) ; plis, trous et fissures qui « imitent » le texte
  (arxiv-1706.09883, [L] ; 2019-tournie-ancient-greek-text-concealed-back, [L]) ;
  apophénie fibres/traits (2015-mocella, [L]) ; aucune métrique de faux positifs hors lettre
  (2026-korotetskyi, [L] ; 2023-mou, [G]).
- Ce qui manque : un taux de faux positifs par type de structure.
- Statut : **étayé**.
- Piste : annoter des fausses structures (fibres, fissures) sur un segment et mesurer le taux
  de détection des lecteurs.

### B4. Modalités indépendantes (IR, SWIR, thermographie, XRF, THz) jamais confrontées quantitativement au CT
- Constat : SWIR sur papyrus déroulés (2019-tournie, [G]), thermographie (2025-ceccarelli,
  [G]), THz (2025-verde-sub-terahertz-radar-imaging-ancient, [G]), cartes XRF comme labels
  possibles (2016-brun, [G]) : aucune comparaison chiffrée avec une carte d'encre CT. La
  validation croisée volume / surface d'arxiv-2606.29085 est qualitative ([P], [L]).
- Ce qui manque : un fragment imagé dans plusieurs modalités et en CT, avec une métrique
  d'accord.
- Statut : **étayé**.
- Piste : chercher si les fragments EduceLab (IR recalé) ont aussi des images SWIR ou
  thermiques publiées.

### B5. Priors papyrologiques (mise en page, fibres) pour valider une lecture : proposés, non testés
- Constat : mise en page (inclinaison de Maas, intercolonnes) comme prior possible
  (2023-romano, [G]) ; motif de fibres croisées comme contrôle d'aplatissement
  (2021-stabile-computational-platform-virtual-unfolding-herculaneum, [P] ;
  arxiv-1706.09883, [P]) ; rendus négatifs et alternatifs pour juger une trace
  (arxiv-2104.01106, [P], [G]).
- Ce qui manque : un critère automatique fondé sur ces priors, et son effet sur les faux
  positifs.
- Statut : **étayé** pour l'absence de méthode dans les papiers lus ; idée déduite.
- Piste : score de cohérence de ligne de base et d'inclinaison sur les colonnes prédites.

---

## C. Évaluation et comparabilité

### C1. Pas d'évaluation sur fragment, rouleau ou scanner tenu à l'écart
- Constat : colonnes ou régions d'un même fragment (2019-parker, [L]) ; moitiés d'une même
  surface (arxiv-2304.02084, [L]) ; split intra-fragment probable (2023-mou, [L]) ; un seul
  fragment de test (arxiv-2308.05070, [L]) ; nnU-Net entraînés sur le rouleau évalué
  (arxiv-2512.04927-virtually-unrolling-herculaneum-papyri-diffeomorphic, [L]). Quand le
  test tenu à l'écart existe, le score chute : 0,89 en validation croisée par échantillon,
  0,691 tenu à l'écart et 0,475 sur PHerc. 500P2 (arxiv-2603.27698, [L]) ; Scroll 5 réussit,
  Scroll 1 échoue (2026-korotetskyi, [L]). `dataset_split` vaut `n/r` sur 64 lignes sur 72.
- Ce qui manque : des scores à rouleau tenu à l'écart.
- Statut : **étayé**.
- Piste : k-fold par rouleau sur les fragments et rouleaux publics du Challenge.

### C2. Pas de métrique ni de protocole commun pour la détection d'encre
- Constat : cinq métriques pour six papiers d'encre, définitions locales (`benchmarks.csv`) ;
  Dice 0,766 non comparable faute de split et de post-traitement connus (2023-mou, [L]) ;
  PSNR et pFM peu discriminants (arxiv-2308.05070, [L]) ; tableaux illisibles
  (arxiv-2304.02084, [L]) ; aucune métrique d'encre (arxiv-2606.29085, [L]) ; MCC dépendant
  d'une bande δ choisie a priori (2026-korotetskyi, [L]). Pas de revue comparative des
  méthodes du Challenge (2024-perino-frontiers-digital-restoration-hidden-texts, [G]).
- Ce qui manque : un banc d'évaluation commun (split, métrique, seuil, post-traitement).
- Statut : **étayé**.
- Piste : rapports des Progress Prizes et du Kaggle Ink Detection, absents de la base.

### C3. Pas de métrique commune de qualité de segmentation, de déroulage ni de lisibilité
- Constat : évaluation visuelle seulement (2016-seales-damage-discovery-virtual-unwrapping-reading,
  [L], [G] ; 2018-rosin-virtual-recovery-content-x-ray, [L], [G] ;
  2018-liu-robust-virtual-unrolling-historical-parchment, [G] ;
  2018-dahl-layered-surface-detection-virtual-unrolling, [L] ; 2021-dambrogio, [L] ;
  arxiv-2308.07070, [L], [G] ; 2015-barfod-revealing-text-complexly-rolled-silver, [L]).
  Seul arxiv-2512.04927 chiffre (ChD unidirectionnel, qui ne pénalise pas l'excès de
  surface, [L]). Pas de mesure objective de lisibilité (arxiv-2104.01106, [G] ;
  2019-tournie, [G]).
- Ce qui manque : une vérité terrain de surface et une métrique de lisibilité partagées.
- Statut : **étayé**.
- Piste : réutiliser les maillages manuels de Paris 4 d'arxiv-2512.04927 avec un ChD
  bidirectionnel.

### C4. Banc à vérité terrain connue à l'échelle des scans réels : absent
- Constat : rouleau modèle à 18 µm et 30 kV (2026-seiler, [L], [G]) ; fantôme transparent en
  lumière visible (arxiv-2504.11485-deciphering-scrolls-tomography-training-experiment, [G]) ;
  livre d'expérience à 103 µm (2018-stromer, [L], [G]) ; échantillon modèle de xénon
  (2026-hoffmann, [L]).
- Ce qui manque : un rouleau modèle à encre carbonée pure, texte connu, scanné à 8–9 µm et
  2,4 µm.
- Statut : **étayé**.
- Piste : rouleau modèle de Seiler re-scanné au synchrotron ; à défaut, simulation CT
  (PSF, bruit) d'un volume synthétique.

---

## D. Géométrie : segmentation, déroulage, aplatissement

### D1. Zones écrasées, feuilles en contact, plis et jonctions : non résolus
- Constat : feuilles qui se touchent non séparées (2018-rosin, [L], [G]) ; hypothèses d'une
  seule surface spiralée, sans contact ni plis (2018-dahl, [L] ; arxiv-2512.04927, [L] (§7)) ;
  structures tangentiellement connectées non traitées (arxiv-2308.07070, [L], [G]) ;
  fusions, trous et changements de feuillet en zones compressées (arxiv-2606.29085, [L], [G]) ;
  documents délaminés hors portée (2021-dambrogio, [L], [G]) ; seuillage global inopérant
  (2021-stabile, [P]).
- Ce qui manque : méthode évaluée dans ces zones, comparée aux champs de nombre d'enroulement
  et aux instances 3D.
- Statut : **étayé**.
- Piste : `/paper-discover surface-segmentation` (instances 3D, horizons sismiques, membranes
  en biologie).

### D2. Distorsion d'aplatissement : SLIM, ARAP et flatboi non comparés sur Herculanum
- Constat : comparaison LSCM/ABF/masse-ressort sur En-Gedi sans SLIM ni ARAP
  (arxiv-2007.15551-quantitative-distortion-analysis-flattening-applied, [L], [G]) ;
  LSCM/ABF sur Herculanum sans métrique (2021-stabile, [L], [G]) ; masse-ressort sans mesure
  (2016-seales, [L] ; 2021-dambrogio, [G]) ; AD et Str de arxiv-2512.04927 variables selon
  l'étape SLIM ([L]). Métriques réutilisables : étirement L2/L∞, erreur d'aire
  (arxiv-2007.15551, [P]) ; aspect, aire, skew (2018-dahl, [P]) ; contrainte d'arête
  (2021-dambrogio, [P]).
- Ce qui manque : un tableau de distorsion SLIM / ARAP / LSCM / flatboi sur les mêmes segments
  d'Herculanum à 8–9 µm.
- Statut : **étayé**.
- Piste : mesurer étirement L2/L∞ et erreur d'aire sur les segments du projet avec chaque
  méthode.

### D3. Effet de la qualité de surface et de la distorsion sur l'encre détectée : non mesuré
- Constat : lien distorsion → lecture seulement visuel (arxiv-2007.15551, [L], [G]) ;
  lien ChD/WJF → encre non mesuré (arxiv-2512.04927, [G]) ; lettres déformées par la
  distorsion de surface (arxiv-1602.08071, [L]).
- Ce qui manque : une courbe score d'encre en fonction de l'erreur de surface.
- Statut : **étayé**.
- Piste : perturber un segment de référence (décalage de normale, étirement) et mesurer la
  baisse du lecteur.

### D4. Passage à l'échelle d'un rouleau entier : peu documenté
- Constat : volumes de 10^7 à 10^8 voxels et goulot mémoire (arxiv-2308.07070, [L]) ; environ
  3 semaines par rouleau en Matlab (2018-rosin, [L]) ; fragments d'environ 4 cm
  (2021-stabile, [L]) ; 19 h dont 16 h de post-traitement (arxiv-2512.04927, [L]) ; part de
  correction manuelle non chiffrée (arxiv-2606.29085, [L]). Matériel et temps `n/r` dans la
  plupart des fiches (68 lignes sur 72 sans temps).
- Ce qui manque : coût calcul et part manuelle d'une chaîne complète.
- Statut : **étayé**.
- Piste : relever ces chiffres dans les rapports de prix du Challenge.

### D5. Couplage carte de probabilité apprise + extraction à garantie topologique : non testé
- Constat : proposé comme piste (arxiv-2308.07070, [P], [G]) ; arxiv-2512.04927 dépend des
  prédictions nnU-Net ([L]) ; méthodes de surface en couches non évaluées sur Herculanum
  (2018-dahl, [G]).
- Statut : **hypothèse** (proposition de fiche, aucun résultat).
- Piste : appliquer l'extraction de Klenert et al. à la sortie du nnU-Net de surface.

---

## E. Apprentissage : labels, transfert, pré-entraînement

### E1. Labels bruités ou dérivés d'un réseau ; pseudo-labels non évalués
- Constat : références qui sont des prédictions de réseau, donc MCC = accord avec ce réseau
  (2026-korotetskyi, [L] (§5.3, §7)) ; désalignement IR/CT non discuté (arxiv-2308.05070,
  [L]) ; labels photo aux bords flous (arxiv-2603.27698, [L]) ; une seule lettre authentique
  (2019-parker, [L]) ; 15 caractères de vérité terrain (arxiv-2304.02084, [L]) ;
  pseudo-labels conservateurs et supervision fragment → rouleau sans chiffre
  (arxiv-2606.29085, [P]). Pré-entraînement 2D sur lettres grecques sans gain
  (2023-mou, [G]).
- Ce qui manque : mesure de l'effet du bruit de label et des tours d'auto-entraînement.
- Statut : **étayé** pour le bruit de label ; **hypothèse** pour l'absence de littérature
  sur les pseudo-labels (axe à 2 papiers).
- Piste : `/paper-discover label-efficiency`.

### E2. Transfert entre scans, énergies, scanners et rouleaux : quasi absent
- Constat : normalisation et paramètres de scan non explorés (2019-parker, [L], [G]) ;
  synchrotron ↔ laboratoire non testé (arxiv-2304.02084, [G]) ; phase ↔ absorption non
  traité (arxiv-1602.08071, [G]) ; échec inter-rouleaux inexpliqué (2026-korotetskyi, [G] ;
  arxiv-2603.27698, [G]) ; un seul rouleau et un état d'encre (arxiv-2606.29085, [L]).
- Ce qui manque : méthode d'adaptation de domaine ou d'harmonisation évaluée sur ces scans.
- Statut : **étayé** pour le manque dans les papiers lus ; **hypothèse** pour l'absence de
  méthodes transférables (axe `domain-transfer` à 1 papier).
- Piste : `/paper-discover domain-transfer` (harmonisation d'histogrammes, adaptation de
  domaine en CT volumique).

### E3. Pré-entraînement auto-supervisé 3D : aucun papier
- Constat : question de recherche du profil (`profile.md`, Précisions) ; aucun papier de la
  base ne la traite, aucune fiche n'en parle.
- Statut : **hypothèse** (repose uniquement sur l'absence de papiers).
- Piste : `/paper-discover` « self-supervised 3D pretraining volumetric CT » (MAE, DINO
  volumiques).

---

## F. Reproductibilité

### F1. Code et données rarement publiés
- Constat : code public pour 2019-parker (ink-id, OSF, [Plateforme]), 2021-dambrogio,
  arxiv-2512.04927 ([P] : « baseline publié avec code ») et arxiv-2504.11485 ([L]) ; annoncé
  et non vérifié pour arxiv-2308.05070 ([L]). Absent ou « sur demande » dans la plupart des
  autres fiches : 2016-seales, 2018-dahl, 2018-liu, 2018-rosin, 2021-stabile, 2016-tack,
  2019-tournie, 2023-mou, 2023-romano, 2025-ceccarelli, 2025-verde, 2026-seiler,
  arxiv-1907.07131, arxiv-2308.07070 ([L]). Methods non extraites pour arxiv-2606.29085 ([L]).
- Ce qui manque : implémentations de référence des étapes de déroulage et des lecteurs
  publiés.
- Statut : **étayé**.
- Piste : relever les dépôts GitHub des outils du Challenge (ThaumatoAnakalyptor, villa
  `vesuvius`) comme références logicielles.

---

## Gaps ouverts par une seule fiche (à recouper)

- Conservation des rouleaux (adhérence, décollement) : absente du corpus
  (2025-verde, [G]). Hors cœur du profil.
- Formation de nouveaux contributeurs : rien dans la base (arxiv-2504.11485, [G]). Hors
  profil.
- Paramètres d'acquisition de Bukreeva 2016 et algorithme de Bukreeva 2017 : à chercher
  dans les versions publiées (arxiv-1602.08071, [G] ; arxiv-1706.09883, [G]).
- Version Pattern Recognition 2013 du déroulage virtuel (citée par 5 papiers) : dans
  `A_TELECHARGER.md`, non ingérée.
