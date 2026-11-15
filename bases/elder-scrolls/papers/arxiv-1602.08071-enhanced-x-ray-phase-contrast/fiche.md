---
id: arxiv-1602.08071-enhanced-x-ray-phase-contrast
fiche: done
date: 2026-11-15
benchmarks: none
---

# Enhanced X-ray-phase-contrast-tomography brings new clarity to the 2000-year-old 'voice' of Epicurean philosopher Philodemus

I. Bukreeva, A. Mittone, A. Bravin, G. Festa, M. Alessandrelli, P. Coan, V. Formoso, R. G. Agostino, M. Giocondo, F. Ciuchi, M. Fratini, L. Massimi, A. Lamarra, C. Andreani, R. Bartolino, G. Gigli, G. Ranocchia, A. Cedola, 2016, arXiv preprint. https://arxiv.org/abs/1602.08071
Type : preprint non relu par les pairs

**Titre.** Le titre arXiv ci-dessus diffère de celui de la version publiée (« Virtual unrolling and deciphering of Herculaneum papyri by X-ray phase-contrast tomography », Sci. Rep. 2016, DOI 10.1038/srep27227, information fournie par l'agent principal, non vérifiée dans le PDF). Métadonnées gardées telles quelles (`doi: null`). Le PDF porte « LETTER TO NATURE_papyri » : version soumise, non la version publiée.

## Problème

Lire du texte grec caché dans des rouleaux d'Herculanum carbonisés encore fermés (PHerc. 375 et PHerc. 495), sans les détruire. Les logiciels de déroulage virtuel existants (rouleaux réguliers) ne s'appliquent pas à leur structure chaotique, et les logiciels dédiés antérieurs n'avaient permis aucune lecture (préambule). Une expérience antérieure de XPCT n'avait imagé que quelques lettres.

## Méthode

- Acquisition : tomographie par contraste de phase X (XPCT) « optimisée » ; paramètres n/r dans le texte disponible.
- Un fantôme (feuilles de papyrus vierge de qualité, carbonisées) sert à valider la technique et les algorithmes, puis les deux rouleaux sont mesurés de la même façon.
- Déroulage virtuel par un « nouvel ensemble d'algorithmes » développés en interne : le rouleau est partitionné en sous-ensembles de couches courbées et tordues de façon similaire, et un aplatissement propre à chaque distorsion est appliqué à chacun. Détails (segmentation, paramétrisation, interpolation) n/r ; pas de formule ni d'architecture.
- Pas d'apprentissage automatique : lecture et déchiffrement manuels par les papyrologues. Entrées, labels, entraînement : sans objet.
- Le contraste de phase distingue l'encre (carbone amorphe) du substrat (fibres de carbone ordonnées) (préambule).

## Plateforme et implémentation

- Source : synchrotron, ESRF (Grenoble) d'après les affiliations ; énergie (keV), résolution (µm/voxel), taille de volume : n/r dans ce texte.
- Objets : deux rouleaux entiers (PHerc. 375, PHerc. 495, Bibliothèque nationale de Naples) et un fantôme de papyrus carbonisé.
- Matériel de calcul et temps : n/r ; la procédure est dite « très élaborée et longue ».
- Code et données : non publiés, aucun lien.

## Résultats

- Texte lisible de plus de trois lignes sur 11 mm de large dans PHerc. 375 (Fig. 1) ; séquences ]ενερ̣, ]ψιϲ[, ]κωϲ[ et mots τη̣ρῆι, περιε, π]ε̣ιϲθεῖεν̣ (Fig. 3a-b) ; PHerc. 495 : ]επ[, ]ϲτ[, ]εχε[, ]τείπ̣οµ[εν, ]εν̣ γά[ρ, ]τελη βηµ[α (Fig. 3d-f) ; une coronis (Fig. 2, 3g).
- Alphabet grec complet reconstitué pour chaque rouleau ; écriture du recto (sens des fibres), capitales sans espaces ; attribution à Philodème de Gadare sur critères paléographiques ; PHerc. 495 serait vraisemblablement un livre inconnu du De Rhetorica.
- Aucune métrique quantitative (résolution, contraste, taux de lecture) : résultat qualitatif.
- Label : lecture experte, sans vérité terrain indépendante ni région tenue à l'écart (pas d'apprentissage).
→ reportés dans `benchmarks.csv` : aucune ligne (aucune valeur chiffrée rapportée ; `benchmarks: none`).

## Limites et critique

- Texte arXiv sans section méthodes ni chiffres : irreproductible en l'état (énergie, résolution, algorithmes, code absents).
- « Unprecedented resolution and contrast » et « largest portion of text ever » non chiffrés ; pas de comparaison quantitative avec l'étude antérieure.
- Pas de validation à l'aveugle, pas de test placebo ; les lectures sont des propositions d'experts (restitutions entre crochets, ex. ἐδέδ]οκτο) susceptibles de biais de confirmation.
- Les auteurs notent que la distorsion de la surface déforme les lettres.
- Déroulage fait par sous-ensembles manuellement choisis : non automatisable tel que décrit, peu adapté à un rouleau entier.
- Pas de rouleau tenu à l'écart : sans objet (pas d'apprentissage).

## Pertinence pour la thèse

Travail fondateur et historique pour le thème : première lecture de phrases dans des rouleaux d'Herculanum fermés par XPCT synchrotron, preuve que l'encre carbonée est visible en contraste de phase (contrairement au micro-CT d'absorption du Vesuvius Challenge). Intérêt papyrologique : exemples de lettres, d'une coronis, attribution à Philodème (De Rhetorica). Les verrous restent ouverts : déroulage automatique à grande échelle, segmentation de feuillets écrasés, détection d'encre sans contraste de phase, validation quantitative.

## Gaps identifiés

- Paramètres d'acquisition (keV, µm/voxel) et d'algorithmes absents : à chercher dans la version Sci. Rep. 2016.
- Aucune évaluation quantitative de la lisibilité ni protocole de validation de lecture.
- Transfert entre contraste de phase synchrotron et micro-CT d'absorption : non traité.

## Statut de lecture

papier complet (13,5 ko de `fulltext.md`). Extraction `pymupdf`, `extraction.ok` false, aucune section détectée : pas de tableaux ni de figures extraits, légendes des figures absentes ; les références aux figures sont lues dans le texte seul.
Ce qui suit est déduit et non affirmé par les auteurs : ESRF comme source (déduit des affiliations, le texte ne le dit pas) ; absence de reproductibilité ; absence de validation à l'aveugle.
