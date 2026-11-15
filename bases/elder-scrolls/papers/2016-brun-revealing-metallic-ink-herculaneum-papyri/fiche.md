---
id: 2016-brun-revealing-metallic-ink-herculaneum-papyri
fiche: done
date: 2026-11-15
benchmarks: none
---

# Revealing metallic ink in Herculaneum papyri

Emmanuel Brun, Marine Cotte, Jonathan Paul Wright, Marie Ruat, Pieter Tack, László Vincze, Claudio Ferrero, Daniel Delattre, Vito Mocella, 2016, Proceedings of the National Academy of Sciences. https://doi.org/10.1073/pnas.1519958113
Type : article de journal (PNAS, relu par les pairs ; reçu le 8 oct. 2015, accepté le 18 fév. 2016)

## Problème

Le consensus paléographique veut que les encres gréco-romaines soient carbonées (suie + gomme arabique), sans métal avant le IVe-Ve siècle apr. J.-C. (Introduction). Les analyses antérieures de fragments d'Herculanum divergent : aucun métal chez Störmer et al. (1990), plomb et strontium « à concentration relativement élevée » chez Seales et al., mais sur des spots de 0,5 mm sans cartographie (Introduction). Les auteurs cherchent donc la composition élémentaire de l'encre par cartographie, et si des lignes de réglure ont été tracées sur le papyrus. Enjeu aval déclaré : la nature de l'encre conditionne la technique d'imagerie et les énergies à choisir pour les rouleaux encore fermés (Discussion).

## Méthode

Analyse non destructive par rayonnement synchrotron de deux fragments multicouches de l'Institut de France (box « Objet 59 », ~0,9 × 1,2 cm et ~0,5 × 0,8 cm, ~0,3 mm d'épaisseur ; SI, Description of the Samples).
- Photographie visible et microscopie IR (940 nm, caméra CCD Basler 2456 × 2048, pas 3,45 µm ; SI, Infrared Acquisition).
- Micro-XRF à balayage, ligne ID21 de l'ESRF, à 2,48 et 3 keV (de part et d'autre des seuils M4,5 du Pb). Faisceau de 50 µm (grand fragment) ou 100 µm (petit), puis 10 µm et 1 µm sur des zones choisies du grand fragment (SI, XRF Acquisition). Cartes extraites avec PyMCA ; quantification par simulation Monte Carlo itérative (Results).
- Micro-XRD en transmission, ligne ID11, 50 keV, traitée avec pyFAI et factorisation en matrices non négatives, appariée à l'ICSD (SI, XRD Acquisition).
- Témoins : deux papyrus modernes, l'un frais, l'autre carbonisé à 200 °C sous vide (Fig. 5).

## Plateforme et implémentation

Sans objet au sens FPGA/GPU : instruments de laboratoire (ESRF ID21 et ID11, microscope IR), pas de modèle appris ni de calcul embarqué. Pas de code ni de données publiés ; seuls les outils tiers sont cités (PyMCA, pyFAI, scikit-learn). Le SI est en ligne (lien PNAS).

## Résultats

- Le plomb est le meilleur élément discriminant encre / papyrus (Fig. 2). À basse résolution, Pb, P, Cl et Al sont co-localisés ; Mg ne l'est pas ; à 1 µm, Al n'est plus co-localisé avec Pb, alors que Cl, Pb et P restent corrélés (Results).
- Concentration de plomb dans les lettres : 84 ± 5 µg/cm² (grand fragment) et 16 ± 5 µg/cm² (petit) (Results). Le SI donne « 16 et 85 µg/cm² » : écart d'arrondi non commenté.
- Hypothèse d'un apport par l'eau de dilution écartée par un calcul d'ordre de grandeur : eau supposée à 2 000 µg/L, soit 42 mL d'eau par cm² d'encre pour le grand fragment, ~432 L pour un rouleau de 15 × 0,15 m couvert à 40 % d'encre, jugé « définitivement irréaliste » (SI, Demonstration of the Intentional Use of Pb). Contamination par un encrier de cuivre ou de bronze jugée également insuffisante (Results, renvoi au SI).
- Les maxima de Pb marquent le début et la fin des traits de plume (Results).
- Le Pb permet de lire les lettres surtout sur le grand fragment ; sur le petit, le contraste IR est légèrement meilleur (Fig. 1).
- Lignes horizontales : visibles sur les cartes Cl, S, Mg, Si et en IR à 1 µm (Fig. 3, Fig. 4). La cristobalite (SiO2), détectée par XRD sur toute l'épaisseur, coïncide avec les lignes Si XRF ; l'espacement des lignes correspond à la taille des lettres de la rangée inférieure, et les fibres sont plus serrées (Results). Les mêmes lignes Si apparaissent sur les papyrus modernes, frais et carbonisé (Fig. 5). Conclusion : ce sont les fibres naturelles du papyrus, utilisées comme guides, et non une réglure ajoutée.
- Origine du Pb : pigment (sulfure, céruse) ou siccatif (litharge) restent des hypothèses, renvoyées à un travail ultérieur (ref. 20, Tack et al., Sci Rep 2016) (Results).
→ reportés dans `benchmarks.csv` : aucune ligne (voir Limites).

## Limites et critique

- Échantillon minuscule : 2 fragments, probablement issus d'un ou deux des six rouleaux de l'Institut de France, non identifiables plus précisément (SI). La généralisation à « l'encre des rouleaux d'Herculanum » est affirmée plus fort que l'échantillon ne le permet ; les auteurs réclament eux-mêmes d'autres fragments (Discussion).
- La preuve d'intentionnalité repose sur un calcul d'ordre de grandeur avec une concentration d'eau « supposée » à 2 000 µg/L (SI) ; la conclusion « radicalement modifie notre connaissance » (Discussion) dépasse la démonstration. Les datations des manuscrits ne sont pas connues précisément (SI).
- Pas de spéciation du Pb ici (renvoi à la ref. 20) ; la nature chimique du composé plombé est donc inconnue.
- Les cartes XRF sont en unités arbitraires normalisées au flux (légendes Fig. 1-3) : pas de contraste chiffré, ni de métrique de lisibilité.
- Le papier lui-même note que le contraste de phase de Mocella et al. 2015 ne montrait pas de signal lié au Pb, et l'explique par une composition d'encre variable d'un scribe à l'autre (Results). Cette explication n'est pas testée.
- Pas de benchmark : mesures physico-chimiques sur fragments, pas de tâche d'apprentissage ni de métrique comparable. Aucune ligne de `benchmarks.csv` n'est justifiable, les colonnes (fps, LUTs, power…) ne s'appliquent pas.
- Déduit (non affirmé) : un encre riche en Pb devrait donner un contraste d'absorption exploitable en CT ; les auteurs disent seulement que cela « aidera à optimiser » les expériences (Discussion). Le papier ne donne ni énergie ni résolution de CT.

## Pertinence pour la thèse

Pertinence pour le thème (profile.md) : article fondateur sur la nature physique de l'encre d'Herculanum, au croisement de la papyrologie et de la détection d'encre. Il porte l'hypothèse d'une encre plombée détectable par absorption X, contraire à l'hypothèse « encre carbonée sans contraste » sur laquelle repose le Vesuvius Challenge (le papier de 2016 ne tranche pas pour les rouleaux entiers). À lire avec les travaux EduceLab sur l'encre carbonée. Il apporte aussi : (1) les fibres naturelles comme guides d'écriture, utile à la validation papyrologique ; (2) un cadre d'imagerie XRF/XRD/IR sur fragments comme vérité terrain possible. Il laisse ouvert l'origine chimique du Pb et sa variabilité entre rouleaux.

## Gaps identifiés

- Variabilité de la teneur en Pb entre rouleaux, scribes et périodes : un seul couple de fragments ici.
- Lien entre concentration de Pb et contraste en micro-CT 8-9 µm et 2,4 µm : non mesuré.
- Spéciation du composé plombé (renvoi à Tack et al. 2016, Sci Rep, absent de la base).
- Les cartes XRF de fragments comme labels d'encre alignés sur CT : non exploité.

## Statut de lecture

papier complet (corps de l'article et Supporting Information, y compris la section « Demonstration of the Intentional Use of Pb »). Extraction : backend `pymupdf`, `extraction.ok` à `false`, aucune section détectée dans `sections.jsonl` ; les légendes de figures sont dans le texte mais les figures et leurs cartes ne sont pas lisibles, donc tout jugement visuel sur Fig. 1-5 vient des légendes et du texte. Aucun tableau dans l'article.
Ce qui suit est déduit et non affirmé par les auteurs : la portée pour le Vesuvius Challenge (absorption X du plomb) ; l'écart 84 / 85 µg/cm² attribué à l'arrondi ; le caractère non testé de l'explication de la divergence avec le contraste de phase de 2015.
