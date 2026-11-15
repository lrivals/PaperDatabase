---
id: arxiv-2504.11485-deciphering-scrolls-tomography-training-experiment
fiche: done
date: 2026-11-15
benchmarks: none
---

# Deciphering scrolls with tomography: A training experiment

Sonia Foschiatti, Axel Kittenberger, Otmar Scherzer, 2025, arXiv preprint. https://arxiv.org/abs/2504.11485 (DOI : n/r)
Type : preprint non relu par les pairs

## Problème

Les auteurs veulent un laboratoire pédagogique qui simule toute la chaîne d'acquisition et de déroulage virtuel d'un document ancien enroulé, sans X-rays : acquisition de projections, reconstruction tomographique, segmentation, lecture du texte (Abstract, §1). Public visé : cours de licence en mathématiques appliquées, physique ou archéologie, Maker Fairs, ateliers de vulgarisation (§1). Ce n'est pas une méthode de recherche : aucun verrou scientifique de la lecture des rouleaux d'Herculanum n'est attaqué.

## Méthode

- **Fantômes** : feuilles d'acétate de cellulose transparentes de 21 x 15 cm, imprimées d'un texte grec (Hymni Homerici XV, v. 1-3) ou latin (Lucrèce, De Rerum Natura, v. 72-74), enroulées avec du ruban velcro pour éviter les couches fusionnées (§3).
- **Acquisition** : lumière visible (projecteur) à la place des X-rays ; lentille de Fresnel PMMA 30 x 30 cm (focale 60 cm) pour limiter la parallaxe ; papier blanc comme écran ; appareil photo numérique comme détecteur piloté par CHDK ; moteur pas à pas NEMA 17 via Arduino + A4988 ; 800 projections sur 360° à 0,44 fps, soit 30 min (§3).
- **Reconstruction** : détermination de l'axe de rotation (GUI `guiAxisFinder`, différence entre l'image 0 et son homologue à 180°) ; Filtered Back-Projection (`iradon`, interpolation linéaire, filtre Ram-Lak) ; masque pour supprimer les artefacts central et externe (§4, annexe A).
- **Segmentation** : `guiSegment`, points de contrôle manuels sur une coupe en spirale, optimisés par algorithme génétique, puis spline cubique lissante (§4).
- **Texturation** : Maximum Intensity Projection (MIP, éq. 4.1) sur la surface segmentée ; pas de post-traitement (§4).
- Annexe A : rappel du modèle mathématique (Beer-Lambert, transformée de Radon, sinogramme, rétroprojection, théorème de coupe de Fourier, FBP).

## Plateforme et implémentation

Matériel de bricolage listé en §3 (Arduino, breadboard, PC, appareil photo avec CHDK, projecteur, lentille de Fresnel, moteur NEMA 17, structures carton et bois). Pas de GPU ni de temps de calcul reportés (n/r). Code Matlab et Jupyter Notebook publiés : https://gitlab.com/csc1/archeolab/ ; documentation : https://csc1.gitlab.io/archeolab/ (§1, §3, §6). Une base d'images « tuned » de reconstruction de référence est annoncée (§6). Résolution spatiale, taille de voxel et pas du système : n/r.

## Résultats

Résultat qualitatif seulement : « most of the Greek and Latin letters are legible without the application of any post-processing » malgré des artefacts (§4, Fig. 6 et 7) ; les grands caractères sont moins flous que les petits, attribué par les auteurs à la position des mots dans la couche interne, perturbée par l'écriture des couches externes (§4) ; les caractères des couches internes sont attendus plus flous (flexion de la lumière) (§6). Aucune métrique (PSNR, taux de lettres lisibles, CER), aucun baseline, aucune étude de paramètres. Les seuls chiffres sont des paramètres d'acquisition (800 projections, 0,44 fps, 30 min, §3), pas des performances.
→ reportés dans `benchmarks.csv` : aucune ligne (pas de métrique comparable ; papier pédagogique, résultats qualitatifs). `benchmarks: none` au front-matter.

## Limites et critique

- Aucune évaluation quantitative : la « réussite » est définie comme « la majorité des lettres lisibles » (§6), sans protocole ni lecteurs indépendants.
- Analogie lumière visible / X-rays posée par principe (« premise », §1) : le fantôme transparent imprimé n'a ni le contraste d'absorption, ni le bruit, ni l'encre carbonée, ni les feuilles écrasées d'un vrai rouleau ; le problème dur (encre sans contraste, segmentation de feuillets compressés) n'est pas simulé. Segmentation manuelle d'une spirale 2D, loin des chaînes 3D automatiques du Vesuvius Challenge.
- Texte imprimé sur la face de la feuille, sans modèle d'encre : n'informe pas sur la détection d'encre.
- Contexte historique du §2 : assertions non sourcées sur place ; deux points à vérifier avant citation (déduit, non affirmé par la lecture) : le papier date la découverte de Luke Farritor de 2024 alors que le First Letters du Vesuvius Challenge date de 2023 ; l'extraction de texte du mot « πoρφνραζ » est probablement mal orthographiée (pymupdf).
- Texte extrait par pymupdf (`extraction.ok` false) : formules et caractères grecs dégradés ; les figures ne sont pas lisibles dans le texte.
- Reproductibilité : code publié, mais pas de seuils ni de paramètres de l'algorithme génétique.

## Pertinence pour la thèse

Faible pour les objectifs de compétition d'Elder-scrolls (gains d'encre, segmentation 3D, aplatissement, 8-9 µm). Intérêt limité : (1) exemple pédagogique de la chaîne segmentation → texturation (MIP) → lecture, avec la FBP et le théorème de coupe de Fourier de l'annexe A comme rappel de base de la reconstruction CT (axe `ct-imaging`) ; (2) un banc d'essai physique à bas coût (fantôme transparent) pour tester des idées de pipeline sans scan synchrotron, avec vérité terrain connue (texte imprimé). Ne répond à aucune question de recherche du profil (encre, super-résolution, transfert, validation). Axes retenus : `virtual-unwrapping`, `ct-imaging`.

## Gaps identifiés

- Pas de banc de test physique à vérité terrain pour valider des détecteurs d'encre ou des chaînes de déroulage (ce papier est une piste, mais non quantitative).
- Valeur pédagogique et communication : rien dans la base sur la formation de nouveaux contributeurs.

## Statut de lecture

papier complet (`fulltext.md` lu en entier, extraction pymupdf, `extraction.ok` false : texte potentiellement dégradé, figures non vues, aucun tableau).
Ce qui suit est déduit et non affirmé par les auteurs : l'absence de pertinence directe pour les questions du profil ; l'écart des phénomènes physiques entre fantôme transparent et rouleau carbonisé ; l'incohérence de date sur la découverte de Farritor.
