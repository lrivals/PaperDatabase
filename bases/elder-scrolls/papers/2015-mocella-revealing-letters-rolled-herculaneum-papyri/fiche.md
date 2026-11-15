---
id: 2015-mocella-revealing-letters-rolled-herculaneum-papyri
fiche: done
date: 2026-11-15
benchmarks: none
---

# Revealing letters in rolled Herculaneum papyri by X-ray phase-contrast imaging

Vito Mocella, Emmanuel Brun, Claudio Ferrero, Daniel Delattre, 2015, Nature Communications 6:5895. https://doi.org/10.1038/ncomms6895
Type : article de journal (relu par les pairs ; reçu 17 mai 2014, publié 20 janv. 2015).

## Problème

L'encre carbonée des papyrus d'Herculanum a presque la même densité que le papyrus carbonisé : la tomographie X par absorption ne la distingue pas, et les rouleaux ne peuvent plus être déroulés mécaniquement sans destruction (Introduction). Les auteurs veulent montrer qu'on peut lire des lettres à l'intérieur d'un rouleau fermé, sans l'ouvrir.

## Méthode

- Principe : tomographie X en contraste de phase par propagation (PBI/XPCT). Les lettres, en léger relief (« au moins une centaine de microns » au-dessus des fibres), produisent un contraste de phase ; la différence de composition encre/papyrus ne suffit pas en absorption (Results, Sample characteristics).
- Reconstruction : rétroprojection filtrée (Fourier), code PyHST2 sur GPU (Methods). Pas d'apprentissage automatique : aucune architecture, entrée, label ni entraînement.
- Segmentation des spires : les algorithmes disponibles échouent sur la surface complexe, de petites portions continues de la même surface ont été identifiées **manuellement** dans presque tous les cas (Discussion). Lecture des lettres par inspection visuelle de coupes planes, interprétation papyrologique par un des auteurs (D. Delattre).
- Alphabet de PHerc.Paris. 4 reconstitué à partir de plusieurs régions et comparé à des images infrarouges de PHerc. 1471 (Fig. 4) ; rapprochement avec le groupe M de Cavallo, datation probable 2e quart du Ier s. av. J.-C. et attribution possible à Philodème (Discussion ; hypothèse, non démontrée).

## Plateforme et implémentation

- Source : synchrotron ESRF, ligne biomédicale ID17, décembre 2013 ; faisceau monochromatique 70 keV (double cristal Si(111)) ; énergie choisie : diffusion forte en dessous, lisibilité moindre au-delà de 75-80 keV (Methods).
- Détecteur : caméra CCD FReLoN 2k, champ 90 x 90 mm², pixel effectif 46 µm, scintillateur Gd2O2S 60 µm ; **résolution spatiale mesurée 100 µm** dans les 3 dimensions ; distance échantillon-détecteur environ 11 m ; faisceau 5 mm x 15 cm, échantillon déplacé par pas de 5 mm ; 2 000 projections sur 360 degrés, 4 min par pas, environ 4 h pour l'échantillon entier (16 cm) (Methods).
- Échantillons : PHerc.Paris. 1 fr. 101 (fragment du rouleau déroulé par la méthode d'Oslo en 1986/87) et PHerc.Paris. 4 (rouleau presque entier, environ 16 cm, fortement déformé) (Results).
- Matériel de calcul : GPU pour la reconstruction (PyHST2), modèle et temps de reconstruction n/r.
- Code et données : PyHST2 est open source (réf. 32) ; données du scan et segmentations manuelles non publiées dans le papier (n/r).

## Résultats

- PHerc.Paris. 1 fr. 101 : deux mots lus sur une couche cachée, PIPTOIE et EIPOI ; lettres de 2-3 mm, donc bien au-dessus des 100 µm de résolution (Fig. 1, Results).
- PHerc.Paris. 4 : séquences APN, HEY, KI (Fig. 3) ; la plupart des lettres de l'alphabet grec retrouvées, sauf X et Psi (Fig. 4, Discussion). Plusieurs lettres difficiles à distinguer des fibres horizontales/verticales ; certaines apparaissent inversées haut-bas ou gauche-droite (Discussion).
- Estimation des auteurs : un rouleau entier demanderait quelques heures de faisceau une fois la technique réglée (Discussion, projection non mesurée).
- Aucune métrique quantitative (pas de F-score, IoU, SNR, taux de lecture) : les résultats sont des figures illustratives.
→ reportés dans `benchmarks.csv` : aucune ligne (preuve de concept sans mesure de performance exploitable) ; `benchmarks: none`.

## Limites et critique

- Évaluation : aucune ; pas de régions tenues à l'écart, pas d'aveugle, pas de contrôle placebo. Labels : aucun (lecture visuelle experte, pas d'IR ni de pseudo-labels pour valider les lettres). Risque d'apophénie reconnu par les auteurs (traits horizontaux/verticaux confondus avec les fibres).
- Lecture et segmentation manuelles, non reproductibles ; pas d'estimation de la fraction de texte récupérée (« petit nombre de caractères »).
- Le signal exploité est morphologique (relief de l'encre), pas chimique ; sensible aux artefacts de texture du papyrus (Discussion).
- Résolution 100 µm, bien plus grossière que les scans actuels du Vesuvius Challenge (8-9 µm) : comparaison déduite, pas faite par le papier. L'identification de la main et de l'auteur (Philodème) reste une hypothèse.
- Les travaux ultérieurs (Parker et al. 2019 sur l'encre en absorption) ont mis en doute le rôle du seul relief : à vérifier, absent de ce papier.

## Pertinence pour la thèse

Référence fondatrice pour la base : première lecture non destructive de lettres dans un rouleau fermé, sur PHerc.Paris. 4, le rouleau visé par le projet (titre de PHerc. Paris. 4). Elle établit l'hypothèse « l'encre est en relief, donc un signal topographique/de phase » et décrit la difficulté de segmentation des spires, que la chaîne visée (surface, aplatissement, encre) cherche à automatiser. Laisse ouverts : segmentation automatique, validation quantitative, effet de la résolution.

## Gaps identifiés

- Aucune méthode de validation (faux positifs, lecture à l'aveugle) pour les lettres lues en XPCT.
- Comparaison encre en phase (100 µm, 70 keV) vs absorption à 8-9 µm sur PHerc.Paris. 4 : non faite.
- Segmentation automatique des spires de PHerc.Paris. 4 : citée comme échec des algorithmes de 2014.

## Statut de lecture

Papier complet (fulltext.md lu en entier). Extraction pymupdf, `extraction.ok` false, aucune section détectée, ligatures cassées dans le texte (« classi cation ») : numéros de page et sections par noms de titre uniquement. Figures non vues (légendes seules).
Déduit et non affirmé par les auteurs : comparaison avec la résolution des scans actuels, absence de validation, mise en regard avec Parker et al.
