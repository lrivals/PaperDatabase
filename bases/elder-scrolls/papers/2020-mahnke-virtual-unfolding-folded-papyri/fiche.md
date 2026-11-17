---
id: 2020-mahnke-virtual-unfolding-folded-papyri
fiche: done
date: 2026-11-17
benchmarks: none
---

# Virtual unfolding of folded papyri

Heinz-Eberhard Mahnke, Tobias Arlt, Daniel Baum, Hans-Christian Hege, Felix Herter, Norbert Lindow, Ingo Manke, Tzulia Siopi, Eve Menei, Marc Etienne, Verena Lepper, 2020, Journal of Cultural Heritage 41, 264-269. https://doi.org/10.1016/j.culher.2019.07.007
Type : short communication de journal (revue par les pairs, open access CC BY-NC-ND)

## Problème

Des papyrus égyptiens (collection du Louvre, fouilles de Clermont-Ganneau, île d'Éléphantine selon le contexte) sont conservés pliés en paquets, trop fragiles pour être dépliés à la main (Abstract, Introduction). Le texte caché doit être lu sans les détruire. Le cas diffère des rouleaux : le dépliage est plus compliqué que le déroulage (Introduction). Le papier pose aussi la question de la visibilité de l'encre : les encres à ions métalliques (fer, plomb) contrastent avec le papyrus en absorption X, pas les encres carbonées (Introduction, Conclusions).

## Méthode

Dépliage virtuel en deux étapes majeures, détaillé dans une publication antérieure des auteurs (Baum et al., réf. [10]) (§3.3) :
- **Dépliage** : coupe par coupe (orientation d'axe choisie), contours interne et externe par coupe, dessinés à la main sur quelques coupes seulement et interpolés linéairement entre elles. Le contour interne est redressé en conservant l'espacement des points ; transformation « moving least squares » as-rigid-as-possible (Schaefer et al., réf. [13]). Plusieurs passes avec des axes différents.
- **Déroulage** : maillage de la surface médiane de la feuille, construit à partir de contours sur peu de coupes (nombre de points identique), puis aplatissement dans le plan par une approche de type masse-ressort (réf. [14,15]) avec la contrainte que les cellules restent convexes. Un volume mince déroulé est rééchantillonné à la taille de voxel d'origine, épaisseur fixée par l'utilisateur, le long de la normale.
- Visualisation par rendu volumique avec fonction de transfert (réf. [16]).
- Préalable : fluorescence X portable (pXRF, XGLab Elio, spot 1 mm) pour détecter du Fe, indice d'une encre à ions métalliques ; trois objets montrent des variations de Fe selon la position (§3.2). Fe seul n'est pas une preuve (sable, ocre).

## Plateforme et implémentation

Pas de FPGA : papier de méthode et de cas d'étude. Micro-CT du Helmholtz-Zentrum Berlin, tube Hamamatsu à anode W ; tension, taille de spot et résolution en µm : n/r dans le texte extrait (valeurs perdues, §3.2). Logiciel : Amira (réf. [12]) ; algorithmes de dépliage développés par le Zuse-Institut Berlin. Matériel de calcul et temps : n/r. Code et données : non publiés.

## Résultats

- Objet L/El227b/1-pC : dépliage réussi ; premier mot identifié sur un paquet réel : le mot copte « Seigneur » (« pjoe[is] »), éventuellement « ô Seigneur » (vocatif, peut-être une courte prière) (Abstract, §Results).
- Objet L/El227b/4-pG : très fragile, plusieurs dépliages successifs nécessaires par couche ; feuille très abîmée (trous, fibres manquantes), seules quelques fibres identifiées, pas de texte (§Results).
- Objet L/El227b/2-pU, paquet compact « de type magic fold » : coupes du volume, distorsions trop fortes pour une extraction simple ; indications de lettres seulement partielles (§Results). Les auteurs supposent une encre carbonée, sans absorption suffisante.
- Les auteurs revendiquent, à leur connaissance, un dépliage de papyrus pliés le long de lignes et la structure à deux plis de fibres qui complique l'identification des couches (§Conclusions).
- Aucune métrique quantitative : pas de précision, de distorsion ni de temps rapportés.

Aucune ligne de `benchmarks.csv` : papier qualitatif, sans chiffre de performance ni d'évaluation (d'où `benchmarks: none`).

## Limites et critique

- Évaluation purement qualitative : un seul mot lu sur trois objets, pas de vérité terrain ni de mesure de distorsion du dépliage.
- Contours dessinés à la main sur certaines coupes : méthode semi-manuelle, temps de travail n/r.
- Le contraste dépend de l'encre : les auteurs concluent que l'imagerie par absorption atteint sa limite pour les encres carbonées et qu'une technique d'imagerie adaptée est nécessaire (§Conclusions).
- Le texte extrait est fortement dégradé : paramètres d'acquisition (tension, résolution) non récupérables ; fidélité des chiffres non vérifiable.
- Pas de code publié ; reproductibilité limitée.

## Pertinence pour la thèse

Axe `papyrology` surtout, avec écho sur `mesh-flattening` et `ct-imaging`. C'est le pendant « plié » des travaux de déroulage : mêmes briques (maillage de surface médiane, aplatissement masse-ressort, contrainte de distorsion minimale) que celles employées pour les rouleaux d'Herculanum, mais sans le suivi de feuillet par apprentissage. Il rappelle que l'encre carbonée n'offre pas de contraste d'absorption, ce qui motive la détection d'encre par apprentissage et la super-résolution du Vesuvius Challenge (déduit, non dit par les auteurs ainsi). Le papier cite explicitement l'encre à base de plomb des papyrus d'Herculanum (Brun et al. ; Mocella et al.).

## Gaps identifiés

- Aucune métrique de qualité du dépliage ou de l'aplatissement pour comparer les méthodes.
- Encre carbonée sans contraste en absorption : non résolu ici (les auteurs cherchent une autre modalité d'imagerie).
- Segmentation de feuillets très distordus ou compacts (paquet « magic fold ») : échec partiel, pas d'automatisation.

## Statut de lecture

Papier complet (fulltext.md lu en entier). Extraction `pymupdf`, `extraction.ok` à `false`, aucune section détectée : le texte est très dégradé (mots et nombres manquants, en particulier les paramètres du micro-CT, les numéros de figures et de tableaux, les références) ; les résultats sont reconstitués à partir de phrases partielles.
Déduit et non affirmé par les auteurs : la filiation avec les méthodes de déroulage d'Herculanum ; « première » dans l'Abstract lue comme première identification d'un mot sur un paquet réel plié ; le lieu d'origine (Éléphantine) issu d'un fragment illisible.
