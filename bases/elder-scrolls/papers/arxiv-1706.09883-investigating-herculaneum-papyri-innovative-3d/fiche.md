---
id: arxiv-1706.09883-investigating-herculaneum-papyri-innovative-3d
fiche: done
date: 2026-11-15
benchmarks: none
---

# Investigating Herculaneum papyri: An innovative 3D approach for the virtual unfolding of the rolls

Inna Bukreeva, Michele Alessandrelli, Vincenzo Formoso, Graziano Ranocchia, Alessia Cedola, 2017, arXiv preprint (arXiv:1706.09883). https://arxiv.org/abs/1706.09883
Type : preprint non relu par les pairs (DOI : n/r)

## Problème

Ouvrir et lire virtuellement les rouleaux d'Herculanum (carbonisés, écrasés, tordus par l'éruption de 79 ap. J.-C.) dont la géométrie interne est très irrégulière ; les méthodes de déroulage pour feuillets lâches ne conviennent pas aux feuillets étroitement compressés et enchevêtrés, notamment dans les zones intermédiaire et externe où se trouvent auteur et titre (Results, « Herculaneum papyri after 79 AD eruption »).

## Méthode

- Procédure semi-automatique de « scorzatura virtuelle » : rendu 3D, choix d'une région d'intérêt, isolement de la région, retrait virtuel des couches externes (« scorze ») puis pelage des paquets de feuillets un par un (Fig. 4-6).
- Aplatissement préliminaire d'un paquet épais de feuillets (« volume flattening ») qui simplifie la segmentation d'un feuillet isolé ; puis aplatissement supplémentaire sur le feuillet pour restituer le texte (Fig. 6, 9). Hypothèse de départ : zones proches de surfaces développables (cylindre généralisé, cône, plan), extension à une géométrie plus complexe annoncée comme future.
- Les fibres croisées du papyrus (périodicité d'environ 1-1,5 mm) servent de grille naturelle pour contrôler la distorsion de l'aplatissement (Fig. 7, 10).
- Entrées : volumes XPCT reconstruits. Labels : aucun, procédure non apprise ; algorithmes détaillés dans le matériel supplémentaire de la réf. [2] (non repris ici). Pas d'entraînement, pas de détection d'encre automatique : le texte est repéré visuellement.
- Un fantôme carbonisé (feuilles de papier avec chiffres et lettres grecques à l'encre maison) sert à développer et tester les algorithmes (Fig. 9-10).

## Plateforme et implémentation

- Scan : synchrotron ESRF, ligne ID17 (Grenoble), propagation libre, détecteur FReLoN 3k CCD, pixel effectif 47 x 47 µm, monochromateur double cristal Si(111), échantillon à environ 10 m du détecteur (Methods).
- Énergie : 73 keV pour les papyrus, 54 et 80 keV pour le fantôme (Methods). Résolution spatiale limitée par la taille du pixel (47 µm) (Methods).
- Objets : rouleaux PHerc. 375 et PHerc. 495 (Bibliothèque nationale de Naples), plus un fantôme carbonisé.
- Matériel de calcul et temps : n/r. Code et données : non publiés (aucun lien ; algorithmes renvoyés à la réf. [2]).

## Résultats

Résultats qualitatifs uniquement, aucune métrique chiffrée de qualité d'encre ou de segmentation :
- Segments de texte grec jusqu'à 14 lignes (PHerc. 375, Fig. 12) et 10 lignes (PHerc. 495, Fig. 13), annoncés comme les plus étendus jamais détectés dans des rouleaux non ouverts ; 3 lignes parallèles lisibles (Fig. 11), 7 lignes assez régulières (Fig. 14), 3 lignes les plus lisibles (Fig. 15) (§ Textual discoveries).
- Lectures proposées : ἀ̣πω[ (ἀπωθέω ou ἀπώλεια, ligne 2, Fig. 14), ἀντιποιέομαι (ligne 6), ἀ]κο̣ήν̣ (Fig. 15) ; déchiffrement jugé « difficile », conjectural dans plusieurs cas.
- Texte toujours trouvé sur le recto (§ Textual discoveries).
→ reportés dans `benchmarks.csv` : aucune ligne (aucun résultat chiffré ; `benchmarks: none`).

## Limites et critique

- Aucune évaluation quantitative, aucune vérité terrain pour les lettres ; pas de région ou rouleau tenu à l'écart, pas de validation à l'aveugle : l'identification du texte est visuelle et subjective.
- Les auteurs reconnaissent que plis, trous, fissures, contamination et artefacts de reconstruction ou d'aplatissement peuvent « imiter » le texte, d'où un risque de faux positifs ; l'aplatissement n'est qu'approximatif (§ Problems related to text detection).
- Lignes pas parfaitement parallèles : « every textual reconstruction would be haphazard » pour certaines figures (§ Textual discoveries).
- Résolution d'environ 47 µm de pixel, très en dessous du 8-9 µm du Vesuvius Challenge (comparaison déduite, non faite par les auteurs) ; contraste de phase à 73 keV, pas du CT d'absorption.
- Procédure semi-automatique, méthode décrite de façon qualitative, non reproductible depuis ce papier ; pas de code ; preprint.

## Pertinence pour la thèse

Travail fondateur (équipe CNR, ESRF) sur le déroulage virtuel de rouleaux d'Herculanum : pelage par paquets de feuillets, aplatissement en deux temps, fibres du papyrus comme contrôle de distorsion (lien avec le suivi de fibres et l'aplatissement SLIM/flatboi du projet), et inventaire des fausses structures imitant l'encre (matière pour l'axe validation et faux positifs). Utile comme contexte papyrologique (Philodème, De Rhetorica) et pour la zone « écrasée » compressée. Reste ouvert : automatisation, mesure quantitative de la distorsion, détection d'encre sans contraste, validation indépendante.

## Gaps identifiés

- Absence de métrique de distorsion d'aplatissement et de validation des lettres (placebo, aveugle) pour cette méthode.
- Algorithme non spécifié ici (renvoi à la réf. [2]) : à retrouver dans le papier d'origine (Nature Communications 2016, à vérifier avant citation).

## Statut de lecture

Papier complet (fulltext.md lu en entier ; extraction PyMuPDF, `extraction.ok` false : texte et figures non vérifiés, légendes seulement).
Ce qui suit est déduit et non affirmé par les auteurs : comparaison de résolution avec le Vesuvius Challenge ; pertinence pour SLIM/flatboi et pour la zone écrasée ; référence de [2].
