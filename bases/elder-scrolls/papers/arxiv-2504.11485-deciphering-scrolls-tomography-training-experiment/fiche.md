---
id: arxiv-2504.11485-deciphering-scrolls-tomography-training-experiment
fiche: done
date: 2026-11-15
benchmarks: none
---

# Deciphering scrolls with tomography: A training experiment

Sonia Foschiatti, Axel Kittenberger, Otmar Scherzer, 2025, arXiv preprint. https://arxiv.org/abs/2504.11485
Type : preprint non relu par les pairs

## Problème

Proposer un laboratoire pédagogique (licence de maths appliquées, physique, archéologie ; ateliers grand public) qui simule toute la chaîne d'acquisition et de déroulage virtuel d'un document enroulé, sans X-rays (Abstract, §1). Ce n'est pas un papier de recherche sur la détection d'encre : le « rouleau » est un fantôme transparent, et le lien avec Herculanum et le Vesuvius Challenge est de contexte (§2).

## Méthode

- Fantôme : feuilles d'acétate de cellulose (CA) de 21 x 15 cm, texte imprimé (grec : Hymni Homerici XV, v. 1-3 ; latin : Lucrèce, De Rerum Natura, v. 72-74), enroulées avec du ruban velcro pour éviter la fusion des couches (§3).
- Acquisition : lumière visible (projecteur + lentille de Fresnel PMMA 30 x 30 cm, focale 60 cm, contre le parallaxe) à la place des X-rays ; géométrie parallèle ; écran de papier blanc, appareil photo comme détecteur ; rotation par moteur pas à pas NEMA 17 piloté par Arduino (§3). 800 projections sur 360° à 0,44 fps, soit 30 min (§3).
- Pipeline (§4) : (1) recherche de l'axe de rotation (`guiAxisFinder`, image à 0° contre image à 180° retournée, minimisation de la différence) ; (2) Filtered Back-Projection (iradon, interpolation linéaire, filtre Ram-Lak) puis masque anti-artefacts ; (3) segmentation de la spirale : points de contrôle posés à la main sur une coupe (`guiSegment`), affinés par algorithme génétique, spline cubique de lissage ; (4) Maximum Intensity Projection (MIP) le long de la surface pour faire apparaître le texte.
- Entrées : projections 2D du fantôme ; labels / vérité terrain : aucun entraînement ; la vérité terrain est le texte imprimé connu. Aucun apprentissage.
- Annexe A : rappel mathématique (transformée de Radon, Beer-Lambert, sinogramme, rétroprojection, théorème de la tranche de Fourier, FBP, filtre Ram-Lak).

## Plateforme et implémentation

- Source de l'imagerie : lumière visible (projecteur), pas de synchrotron ni de micro-CT ; énergie en keV : sans objet ; résolution en µm/voxel : n/r. Objet : fantôme CA transparent (non carbonisé), pas un rouleau ou fragment réel.
- Matériel : Arduino, driver A4988, NEMA 17, appareil photo piloté par CHDK, PC, structures carton/bois (Fig. 2) ; matériel de calcul de la reconstruction et temps de calcul : n/r (seule l'acquisition de 30 min est chiffrée, §3).
- Code publié : scripts Matlab et Jupyter Notebook (Python, skimage) sur https://gitlab.com/csc1/archeolab/ et site https://csc1.gitlab.io/archeolab/ ; une base d'images « tuned » de reconstructions modèles est incluse (§1, §3, §6). Données : projections non vérifiées ici (le texte mentionne seulement la base d'images de référence).

## Résultats

- Évaluation qualitative uniquement : « most of the Greek and Latin letters are legible without any post-processing » malgré des artefacts (§4, Fig. 5-7). Aucune métrique, aucune donnée tenue à l'écart : l'évaluation porte sur les deux fantômes eux-mêmes, avec le texte imprimé comme vérité visuelle.
- Les caractères plus grands sont moins flous que les petits ; les couches internes sont plus floues que les externes (flexion de la lumière, interférence des écritures externes) (§4, §6).
- Aucun chiffre de performance (précision, temps de reconstruction, résolution) : aucune ligne dans `benchmarks.csv` (`benchmarks: none`). Les seuls chiffres (800 projections, 0,44 fps, 30 min, §3) décrivent le protocole d'acquisition, pas un résultat.

## Limites et critique

- Résultat non quantifié, sans comparaison à une baseline ; pas d'évaluation sur des rouleaux réels.
- Les fantômes sont transparents et à fort contraste texte/support : le problème central du Vesuvius Challenge (encre carbonée sans contraste d'absorption sur papyrus carbonisé) est absent ; transférabilité des conclusions : déduit, non affirmé.
- Segmentation manuelle (points de contrôle) sur une seule coupe, sans traitement des déformations, des couches fusionnées ni des compressions ; pas d'aplatissement de maillage 3D à proprement parler (MIP le long de la spirale 2D).
- Description du contexte Vesuvius Challenge sans références chiffrées vérifiables dans ce papier (§2) ; erreurs de transcription visibles (mot grec « πoρφνραζ », « Jupiter Notebook »).
- Reproductibilité : code et instructions publiés, bon point ; mais pas de résultats chiffrés pour comparer.

## Pertinence pour la thèse

Pertinence faible pour la recherche du projet Elder-scrolls : utile comme ressource pédagogique et d'intuition (chaîne segmentation, texturing, flattening, merging ; FBP ; MIP), et comme banc d'essai jouet pour tester une idée de déroulage. Il n'apporte rien sur la détection d'encre carbonée, la segmentation de feuillets écrasés, la super-résolution ou le transfert de domaine. Ne sert pas à valider une méthode du Vesuvius Challenge.

## Gaps identifiés

- Aucun gap de recherche couvert ; la base manque toujours de papiers sur la validation expérimentale sur fantômes à contraste proche de l'encre carbonée (fantôme physique d'encre carbonée sur papyrus avec vérité terrain).

## Statut de lecture

Papier complet (`fulltext.md` lu en entier). Attention : `extraction.backend` vaut `pymupdf` et `extraction.ok` vaut `false` : le texte peut être mal découpé (les équations de l'annexe sont fragmentées, sans impact sur la fiche) ; métadonnées à vérifier à la main (DOI absent, venue : arXiv preprint).
Ce qui suit est déduit et non affirmé par les auteurs : la faible transférabilité au papyrus carbonisé, l'absence d'aplatissement 3D, la qualification de la segmentation comme limitée à une seule coupe.
