---
id: 2019-parker-invisibility-readability-recovering-ink-herculaneum
fiche: done
date: 2026-11-15
benchmarks: none
---

# From invisibility to readability: Recovering the ink of Herculaneum

C. Seth Parker, Stephen Parsons, Jack Bandy, Christy Chapman, Frederik Coppens, William Brent Seales, 2019, PLoS ONE 14(5): e0215775. https://doi.org/10.1371/journal.pone.0215775
Type : article de journal (relu par les pairs, accès libre).

## Problème

Les auteurs contestent l'idée reçue que l'encre carbonée (lamp black) serait « invisible » en micro-CT, faute de différence de densité avec le papyrus carbonisé. Ils posent que l'encre atténue bien les rayons X et laisse un signal subtil (morphologique et d'intensité) détectable par apprentissage, et visent la lecture des rouleaux d'Herculanum fermés (Abstract, « Rethinking visibility »).

## Méthode

- Observations préalables : un fantôme (fiche cartonnée, encre lamp black + huile de lin) scanné à 42 kV/190 uA et 130 kV/61 uA montre l'encre comme une « bosse » (Fig. 1) ; des images MEB d'un fantôme de papyrus montrent une surface encrée plus lisse, avec fissures propres (Fig. 2). Couche d'encre mesurée à 3-5 µm, plus 4-12 µm d'absorption, soit 3-17 µm au total (§ Scan resolution). Voxel idéal déduit : ≤ 3 µm ; plage retenue 3-17 µm.
- Modèle : CNN 3D qui classe des sous-volumes situés sur la surface d'écriture, déjà isolée et aplatie par le pipeline de déroulage virtuel (§ Methods). Architecture détaillée, taille de patch et hyperparamètres : n/r dans le corps du texte (renvoyés à l'Annexe S1, non disponible dans `fulltext.md`).
- Deux variantes, même architecture : (1) « ink prediction » avec labels binaires ink / no ink ; (2) « photorealistic rendering » entraîné sur les valeurs RGB de la photographie de référence (§ Photorealistic rendering).
- Labels : issus de photographies de manuscrits ouverts, recalées sur le volume par le pipeline de déroulage ; ce ne sont ni des labels manuels sur le CT ni des pseudo-labels, mais des labels par imagerie de référence (photo, microscope confocal pour le fragment), car l'encre n'est pas visible dans le CT (§ Features and training labels).
- Évaluation : une colonne à la fois isolée comme colonne de prédiction/évaluation (6 entraînements, Fig. 7) ; pour le fragment, variante de validation croisée k-fold sur 10 régions disjointes (§ Lunate sigma fragment).

## Plateforme et implémentation

- Fantôme de rouleau de papyrus moderne (grille 6x5, 5 symboles, 1 à 6 couches d'encre carbone par colonne, repères en encre ferro-gallique), scan à 12 µm/voxel, source lab (n/r : énergie, scanner) (§ Experimental data, § Carbon phantom scroll).
- Fragment authentique PHerc. Paris 2, Fragment 96 (sigma lunaire), scan tomographique : résolution, source (lab / synchrotron) et énergie n/r dans le texte. Les remerciements citent Diamond Light Source, sans lien explicite avec ce scan.
- Calcul : cluster Lipscomb de l'Université du Kentucky (remerciements) ; GPU et temps n/r. TensorFlow cité en contexte (réf. 13), sans confirmation de son usage.
- Code : https://github.com/viscenter/ink-id ; données : OSF, DOI 10.17605/OSF.IO/ZDKN4 (Data Availability Statement). Publiés.
- Discussion : scanners lab (Bruker SkyScan 1272, pixel 6,92 µm pour un rouleau de 10 cm de diamètre avec triple décalage du détecteur, ~5 µm avec quadruple) ou synchrotron pour une bibliothèque de référence (§ Discussion).

## Résultats

Résultats uniquement qualitatifs (images), aucune métrique chiffrée (F0.5, IoU, AUC…) dans le texte.
- Fantôme : l'encre est détectée là où le filtre de texture « intégral » (ancien état de l'art) ne la montre presque pas (visible seulement en colonnes 5 et 6) ; meilleure détection là où la morphologie est la plus marquée ; colonne 1 (une couche) à la limite de détectabilité à 12 µm (§ Carbon phantom scroll, Fig. 6).
- Faux positifs en colonnes 2 et 3, souvent alignés sur les fibres du papyrus, interprétés comme usage de l'épaisseur combinée ; le rendu photoréaliste réexprime beaucoup de ces fausses encres en fibres (§ Carbon phantom scroll).
- Fragment Herculanum : lettre discernible sur l'image composite, courbe visible en bas, qui ne peut venir des fibres (linéaires et orthogonales) (§ Lunate sigma fragment, Fig. 5).
- Voxel minimal estimé pour détecter l'encre carbonée : entre 3 et 12 µm, probablement près de 3 (§ Discussion).
→ reportés dans `benchmarks.csv` : aucune ligne (pas de valeur chiffrée rapportée ; `benchmarks: none`).

## Limites et critique

- Aucune évaluation quantitative : pas de métrique, pas de seuil, pas de comparaison chiffrée aux baselines (filtre intégral) ; tout repose sur l'inspection visuelle.
- Évaluation sur le fantôme : colonne tenue à l'écart de l'entraînement, mais les colonnes partagent le même papyrus, le même scan et les mêmes symboles, donc fuite de domaine probable (déduit). Sur le fragment, 10 régions d'un même petit fragment : la validation croisée ne teste pas la généralisation à un autre fragment ou rouleau.
- Une seule lettre authentique ; les auteurs notent le faible nombre d'exemples. Généralisation aux rouleaux fermés non démontrée (affirmé comme espoir).
- Faux positifs importants, la morphologie des fibres étant confondue avec l'encre ; pas de test placebo ni de calibration.
- Sensibilité aux paramètres de scan et normalisation des intensités non explorées (§ Discussion).
- Le caractère « photoréaliste » des rendus est une estimation apprise : risque d'hallucination (déduit, non discuté par les auteurs).
- Conflit d'intérêts déclaré : un auteur salarié de Bruker Micro-CT, financement Google.

## Pertinence pour la thèse

Papier fondateur de la détection d'encre carbonée en micro-CT par CNN 3D, directement lié à la question de recherche du profil : le signal exploité est morphologique (surface, épaisseur 3-17 µm) plus qu'une différence de densité, ce qui fixe un ordre de grandeur de résolution (3-12 µm) à comparer avec les scans de 8-9 µm du Challenge, et questionne la part de signal restante à 9 µm et l'intérêt de la super-résolution. Il pose aussi le schéma de labels par imagerie de référence (IR/photo) et la question des faux positifs. Laisse ouvert : métriques, généralisation entre rouleaux et scanners, validation à l'aveugle.

## Gaps identifiés

- Perte de signal d'encre selon la résolution (seuil 3-12 µm non quantifié, pas de test à 8-9 µm).
- Absence de métriques et de protocole d'évaluation standard pour l'encre carbonée.
- Faux positifs dus aux fibres, absence de test placebo et de calibration.
- Transfert entre scans, énergies et rouleaux (normalisation non explorée).

## Statut de lecture

Papier complet (`fulltext.md` lu en entier). Extraction `pymupdf`, `extraction.ok` à `false`, aucune section détectée : le texte semble complet mais le découpage en sections est absent ; figures sans légende de corps de tableau, aucun tableau chiffré. L'Annexe S1 (architecture, patch, hyperparamètres, texture intégral) n'est pas dans le texte.
Ce qui suit est déduit et non affirmé par les auteurs : fuite de domaine entre colonnes du fantôme ; risque d'hallucination du rendu photoréaliste ; absence de lien explicite entre Diamond Light Source et les scans présentés.
