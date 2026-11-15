---
id: 2021-damiani-ink-herculaneum-survey-recent-perspectives
fiche: done
date: 2026-11-15
benchmarks: none
---

# Ink in Herculaneum: A Survey of Recent Perspectives

Vincenzo Damiani, 2021, BRILL eBooks (chapitre 3 d'un ouvrage collectif, accès libre CC BY-NC 4.0). DOI : https://doi.org/10.1163/9789004444805_005
Type : chapitre d'ouvrage (survey court), publié et relu selon l'éditeur ; `metadata.json` porte `type: journal` faute de valeur « chapitre » dans le vocabulaire fermé.

## Problème

Faire le point sur la nature et la chimie de l'encre des papyrus gréco-latins d'Herculanum. L'opinion commune la tient pour une encre au noir de carbone, comme ailleurs dans l'Antiquité (§ Ink in Greek and Latin Papyri ; § The Herculaneum Collection). Des études récentes en XPCT (tomographie de contraste de phase) et en fluorescence X y trouvent du plomb, ce qui rouvre la question et offre un agent de contraste pour lire les rouleaux fermés (Abstract).

## Méthode

Revue narrative, sans expérience propre. Le chapitre :
- rappelle les recettes antiques d'encre (suie + gomme arabique, ratio 1 pour 3 en onces chez Dioscoride ; encres métallogalliques attestées dès le IIIe s.) ;
- retrace l'histoire de la collection : découverte 1752-1754, déroulage mécanique de Piaggio, éditions ;
- rapporte les analyses de composition de l'encre : Störmer et al. 1990 (carbone), Seales 2009 (trois critères de contraste), Mocella et al. 2015 et Bukreeva et al. 2016 (XPCT à l'ESRF), Tack et al. 2016 et Brun et al. 2016 (plomb), Leal et al. 2018 (fac-similé avec plomb).

## Plateforme et implémentation

Sans objet (pas de matériel ni de code propres). Instruments rapportés d'après les travaux cités : ligne ID17 de l'ESRF (Grenoble) pour l'XPCT de PHerc.Paris. 4 et 1, décembre 2013 (§ Herculaneum, 5e paragraphe après « Ink composition ») ; EDX, PIXE, IRM, CT pour les analyses antérieures. Code et données : n/r.

## Résultats

Résultats rapportés, pas obtenus par l'auteur :
- Encre majoritairement carbonée selon les expériences de la fin des années 1980 et du début des années 1990 (Fig. 3.1, spectre EDX).
- Trois critères de contraste encre/papyrus : différence de densité, morphologie de l'écriture, composition chimique (§ après la Fig. 3.1).
- Le calcium est un marqueur possible ; le plomb et le strontium sont détectés (même section).
- La radiographie conventionnelle ne distingue pas l'encre des fibres carbonisées.
- L'XPCT a révélé de courtes séquences de lettres sur PHerc.Paris. 1 (ΠΙΠΤΟΙΕ, ΕΙΠΟΙ, Fig. 3.2) et des groupes de lettres sur PHerc.Paris. 4 (ΑΡΝ, ΗΕΥ, ΚΙ, Fig. 3.3). Une équipe indépendante a aussi lu des portions de PHerc. 375 et 495, encore enroulés.
- Plomb de type acétate de plomb(II) dans l'encre de certains fragments. Concentrations selon Tack et al. : 11-21 µg/cm² dans un cas, 79-89 µg/cm² dans l'autre. Trop élevées pour une contamination de l'eau (moins de 1,5 mg/L en moyenne) ou des encriers en bronze (pas de co-distribution du cuivre). Ajout intentionnel jugé plus probable, d'où une encre « de type mixte ».
- Le plomb est le meilleur élément discriminant sur les cartes de répartition ; Fig. 3.4 le compare à la lumière naturelle et à l'infrarouge à 940 nm.
- Expérience de Leal et al. : un fragment écrit à l'acétate de plomb(II), placé dans un rouleau fac-similé et scanné en XPCT, laisse lire quelques lettres en 3D.
- Précaution de l'auteur : toutes les encres ne contiennent pas de plomb (absent chez Mocella et al. 2015). La composition a pu varier avec la chronologie (IIIe s. av. J.-C. à fin du Ier s. apr. J.-C.) et avec les scribes.

→ reportés dans `benchmarks.csv` : aucune ligne. Survey sans résultat propre : règle « ne rien ajouter » de /paper-fiche (`benchmarks: none`).

## Limites et critique

- Chapitre bref et narratif, sans protocole de recherche bibliographique. Les concentrations de plomb et les lettres lues viennent de 2-3 groupes (Mocella, Tack/Cotte/Brun, Leal) et de peu d'échantillons : généralité non établie, ce que l'auteur reconnaît lui-même.
- Antérieur à la lecture d'encre par apprentissage (Vesuvius Challenge 2023) : rien sur les modèles ML, le scan en lumière synchrotron des rouleaux entiers ni la résolution en µm. Il fixe donc le contexte physique, pas l'état de l'art actuel (déduit de la date).
- L'extension de l'encre au plomb à toute la collection est écartée, mais seulement par l'absence de plomb dans une étude (déduction de l'auteur).
- Hypothèse plomb comme agent de contraste : valable seulement pour les encres qui en contiennent. Pour une encre purement carbonée, le contraste dépend de la densité et du relief (morphologie), un point que le chapitre mentionne sans le quantifier.
- Aucun chiffre de performance ni de résolution : métriques non comparables à celles de la base.

## Pertinence pour la thèse

Pertinence pour le thème de la base (profile.md) : contexte physique de la détection d'encre. L'encre est supposée carbonée, donc peu contrastée en absorption, ce qui motive la détection par modèles (axe ink-detection) et l'imagerie en contraste de phase (ct-imaging). Un rouleau dont l'encre contient du plomb se prête à une détection plus facile qu'un rouleau carboné : source de variabilité entre rouleaux, utile pour l'écart de domaine (domain-transfer) et la validation des faux positifs (validation-fp). Il laisse ouvert la fréquence réelle de l'encre plombifère dans la collection et son lien avec la chronologie ou le scribe.

## Gaps identifiés

- Proportion des papyrus d'Herculanum à encre plombifère : n/r, à chiffrer (piste : Brun et al. 2016, Tack et al. 2016, absents de la base ?).
- Lien entre composition de l'encre (plomb ou carbone) et signal détecté par les modèles d'encre : non traité ici.

## Statut de lecture

Papier complet (`fulltext.md` lu en entier, 128 lignes). Extraction `pymupdf`, `extraction.ok` à `false`, aucune section détectée : les notes de bas de page sont mélangées au texte et les légendes de figures sont isolées (« (préambule) ») ; les images des Fig. 3.1 à 3.4 ne sont pas lisibles, seules leurs légendes l'étant. Aucun tableau.
Déduit et non affirmé par l'auteur : la portée limitée du chapitre par rapport au Vesuvius Challenge, la pertinence pour le domain-transfer et la validation-fp, et le statut « relu » (supposé de l'éditeur).
