---
id: 2026-seiler-model-carbonized-papyrus-scroll-opens
fiche: done
date: 2026-11-15
benchmarks: none
---

# A model carbonized papyrus scroll opens a novel path to identifying readable scrolls of the Herculaneum Library

Douglas Seiler, Jacob Michael LaManna, Michael McOsker, David Kreimer, Michael Cyrus Daugherty, Jens Dopke, 2026, PLoS ONE 21(9): e0353485. https://doi.org/10.1371/journal.pone.0353485
Type : article de journal (reçu 14/03/2026, accepté 24/06/2026, publié 16/09/2026). Données : https://doi.org/10.18434/mds2-4227.

## Problème

En CT synchrotron, l'encre carbonée des rouleaux d'Herculanum est presque indiscernable du papyrus carbonisé (aucune différence d'absorption), d'où un rapport signal/bruit faible (§1). Les auteurs posent deux besoins : (1) choisir en amont les rouleaux les plus lisibles, en faisant l'hypothèse que du plomb dans l'encre augmente le contraste ; (2) disposer de données à vérité terrain connue pour développer et valider des algorithmes de détection de texte sans manipuler les originaux (§1, §4).

## Méthode

- Fabrication d'un rouleau modèle : papyrus égyptien moderne, encre carbonée « Platinum Carbon Ink » (ICP-OES : Pb < 0,4 µg/g dans la phase liquide, §2.2), stylet roseau, encre dopée au nitrate de plomb (§2.3), carbonisation dans un conteneur en acier semi-fermé, quasi sans oxygène (§2.4). Température et durée : `n/r`.
- Calibrage de la dose : environ 2 µL d'encre couvrent 1 cm² de lignes (0,4 à 0,5 g pour 225 cm², §3.2) ; une encre à 100 µg de Pb pour 2 µL (50 g/L) vise la densité surfacique mesurée par Brun et al. sur un fragment d'Herculanum (84 ± 5 µg/cm², valeur citée, §3.2).
- Fragments plats : lettre de 1 cm avec 200, 100, 50, 20 µg/cm² de Pb et un témoin à 0 (§3.3) ; radiographie 2D de lignes de 200 à 25 µg/cm² (§3.4).
- Tomographie du rouleau (40 mm de diamètre, 110 mm de long, Fig 2) sur le système NeXT du NIST : tube à réflexion 225 kV, anode tungstène, utilisé à 30 kV et 1,3 mA ; scintillateur Gd2O2S 20 µm, caméra ZWO ASI6200MM ; pixel effectif 18 µm, champ 172,4 x 114,9 mm ; 1001 projections sur 360°, 5 s chacune ; reconstruction Python/ASTRA (§2.5).
- Déroulage : programme maison, splines posées à la main le long de la spirale, interpolation sur les normales (§2.5, §3.4, Fig 8). Aucun traitement d'amélioration ni algorithme de détection n'est appliqué (§3.4).
- XRF portable : Bruker Tracer (fragments plats) et Olympus Innov-X DS-4000CC réglé pour la peinture au plomb (rouleau) (§2.6).

## Plateforme et implémentation

Sans objet au sens FPGA. Instrumentation : micro-CT de laboratoire NIST NeXT (pas un synchrotron), 18 µm/pixel, 30 kV (§2.5) ; XRF portables Bruker et Olympus (§2.6). Code de reconstruction et de déroulage « custom » : non publié, aucun lien ; seules les données sont déposées (DOI mds2-4227, déclaration de disponibilité des données). Taille du volume reconstruit et résolution isotrope finale : `n/r`.

## Résultats

- Fragments 2D : les deux lignes sans plomb ne sont pas visibles ; les lignes avec plomb sont résolues, la plus contrastée à 200 µg/cm² ; la plus faible testée, 25 µg/cm², reste détectable (§3.4, Fig 6 ; répété en §5). Le seuil de détection n'est donc pas atteint.
- Rouleau modèle : les projections brutes montrent déjà l'encre plombée (Fig 7) ; après reconstruction et déroulage, le texte « the children of » est lisible sans aucun traitement (§3.4, Fig 8c). La concentration de plomb du rouleau scanné : `n/r` dans le texte lu.
- XRF : le Bruker détecte un signal à 200, 100, 50 et 20 µg/cm² et rien sur le témoin, le signal baissant avec la concentration (§3.3, aucune valeur chiffrée) ; l'Olympus détecte le plomb sur le rouleau carbonisé à plusieurs positions (§3.4, Fig 9).
- Encre sans plomb : non testée en tomographie 3D ; les auteurs avancent seulement que la 3D « may allow » une détection par la géométrie (§3.4).
→ reportés dans `benchmarks.csv` : aucune ligne. Le papier ne rapporte aucun modèle ni métrique de performance (pas de précision, F1, etc.), uniquement des observations qualitatives et un seuil « détectable » ; l'en-tête actuel est de plus orienté FPGA. `benchmarks: none` au front-matter.

## Limites et critique

- Preuve de concept qualitative : un seul rouleau, une seule expression partielle lisible, aucune métrique, aucune répétition, aucune lecture à l'aveugle.
- Lecture facilitée par l'encre plombée, fortement contrastée (25 à 200 µg/cm²) ; la difficulté réelle (encre carbone pure, présentée comme le scénario plus difficile, résumé) n'est pas démontrée en 3D.
- Conditions éloignées de la réalité : 18 µm/pixel et 30 kV en laboratoire (§2.5), contre un scan synchrotron du Vesuvius Challenge à environ 8-9 µm (déduit : valeurs hors papier) ; papyrus moderne, carbonisation en four, rouleau de 40 mm de diamètre (Fig 2), plus petit que les rouleaux réels (environ 10 cm, §1). La Fig 4 évoque pourtant un empilement serré et des ondulations.
- Le dopage au plomb en solution coagule l'encre (§2.3) : la distribution du plomb diffère probablement de l'original, dont l'origine reste incertaine (encre ou siccatif, §3.2).
- L'hypothèse « plomb présent dans les rouleaux » repose sur deux fragments d'Herculanum et sur des papyrus égyptiens (réfs. [3], [4], §1, §3.2) ; pas de test sur un vrai rouleau, ni de la détectabilité XRF à travers un rouleau épais.
- XRF : ni sensibilité, ni spécificité, ni seuil chiffrés ; instrument réglé pour la peinture ; le balayage reste manuel (§3.4).
- Reproductibilité limitée : température de carbonisation non donnée, code non publié.

## Pertinence pour la thèse

Pour Elder-scrolls (axes `virtual-unwrapping`, `ct-imaging`, `ink-detection`, `papyrology`) :
- Piste de données synthétiques à vérité terrain (rouleaux modèles à encre carbone seule puis plombée) pour évaluer la détection d'encre en aveugle et par tests placebo (question « comment prouver qu'une lettre est réelle »). Les données sont publiques mais à 18 µm, très au-dessus des 8-9 µm visés : peu utiles pour entraîner Reader V3 / `ink_9um` (déduit) ; envisageables pour des tests de bout en bout ou du transfert entre résolutions.
- Rappelle que l'encre carbonée n'offre pas de contraste d'absorption et que le plomb en fournit un : une lecture sur rouleau plombé est « facile » et ne dit rien du signal de texture/morphologie exploité en First Letters (déduit).
- Le dépistage XRF avant tomographie pourrait aider à prioriser les rouleaux éligibles ; rien ne le démontre sur de vrais rouleaux.

## Gaps identifiés

- Pas de benchmark synthétique public à 8-9 µm avec encre carbone pure et texte connu (perspective évoquée en §4).
- Aucune étude chiffrée du détecteur XRF (sensibilité, profondeur de pénétration dans un rouleau réel).
- Détectabilité de l'encre sans plomb en 3D non validée (hypothèse géométrique, §3.4).
- Lien entre le plomb mesuré dans les fragments et les rouleaux entiers non établi.

## Statut de lecture

papier complet. Avertissement : `extraction.backend` vaut `pymupdf` et `extraction.ok` vaut `false` : le texte peut être incomplet ou mal découpé ; seules les légendes des figures sont lues (Fig 6 à 9 non vues). Aucun tableau. Pas de `chunk_id` (chunks.jsonl absent).
Ce qui suit est déduit et non affirmé par les auteurs : l'écart de résolution avec le scan synchrotron du Vesuvius Challenge (valeurs hors papier), le caractère « facile » de la lecture par rapport au First Letters, l'utilité limitée des données à 18 µm pour `ink_9um`, la différence de géométrie entre rouleau modèle et rouleaux réels.
