---
id: arxiv-2606.29085-complete-virtual-unwrapping-reading-rolled
fiche: done
date: 2026-11-15
benchmarks: none
---

# Complete virtual unwrapping and reading of a rolled Herculaneum papyrus

Giorgio Angelotti, Stephen Parsons, Federica Nicolardi, Youssef Nader, Sean Johnson, David Josey, Paul Henderson, Hendrik Schilling, Johannes Rudolph, Forrest McDonald, Elian Rafael Dal Prá, Paul Tafforeau, Alessandro Mirone, Clifford Seth Parker, Jan Paul Posma, Benjamin Kyles, Claudio Vergara, Alessia Lavorante, Rossella Villa, Maria Chiara Robustelli, Marzia D'Angelo, Gianluca Del Mastro, Michael McOsker, Kilian Fleischer, Christy Chapman, Nat Friedman, William Brent Seales, 2026, arXiv preprint. https://arxiv.org/abs/2606.29085 (DOI : n/r)
Type : preprint non relu par les pairs

## Problème

Les rouleaux d'Herculanum scellés ne peuvent être ouverts sans dommage irréversible ; les travaux antérieurs sur rouleaux scellés n'avaient obtenu que des lectures locales ou des surfaces limitées (Abstract). Le contraste CT entre papyrus carbonisé et encre carbonée est faible, et le signal d'encre varie (contraste métallique faible, relief de surface, texture ; Introduction). Il manquait une chaîne de bout en bout, de l'échantillon entier à une surface lisible : scan optimisé, reconstruction géométrique, récupération d'encre, revue papyrologique (Introduction).

## Méthode

Chaîne couplée en quatre étages (« Technical strategy ») :
- Scan µCT synchrotron à contraste de phase modéré, ligne BM18 de l'ESRF ; voxel isotrope 2,4 µm (Fig. 1b, Fig. 2a) ; reconstruction tomographique grand volume (réf. [22]). Énergie, géométrie, temps de scan : dans Methods / Extended Data Table 1, **absents du texte extrait** (n/r).
- Déroulage semi-automatisé : un modèle appris de segmentation du recto donne des indices volumétriques ; la surface finale est un maillage quadrilatéral explicite, corrigé manuellement, ré-optimisé localement, paramétré dans un domaine 2D quasi isométrique à faible distorsion. Chaque point aplati a ses coordonnées 3D dans le volume (« Technical strategy »).
- Encre, deux régimes : (1) la plupart des zones scellées : modèles entraînés sur supervision issue de fragments et pseudo-labels conservateurs de rouleaux scellés, utilisés comme amplificateurs de visibilité pour l'inspection experte, sans labels de caractères/OCR ; (2) PHerc. Paris 4 : l'encre est directement visible dans le volume, segmentée en 3D puis projetée sur la surface aplatie (« Technical strategy »).
- Revue papyrologique pour la transcription (crochets pour la restitution, point souscrit pour les lettres incertaines ; Results).

## Plateforme et implémentation

Pas de FPGA. Source du scan : synchrotron ESRF BM18, voxel 2,4 µm isotrope (Fig. 1b). Rouleaux : PHerc. 1667, PHerc. Paris 4, PHerc. 139. Comparaison avec le volume EduceLab-Scrolls de PHerc. Paris 4 à 7,91 µm (Fig. 3). Matériel et temps de calcul : n/r (texte lu). Code, modèles, données : non mentionnés dans le texte lu (renvois possibles vers Methods / Supplementary, non extraits) : n/r.

## Résultats

- PHerc. 1667 : déroulage complet de la surface d'écriture préservée, 22 colonnes ou équivalents sur environ 860 cm² (Results, Fig. 1d) ; lecture complète de tout le texte supporté par les images, sauf 33 cm² dans les trois premières colonnes (fragmentaires, Results). « Complet » est défini au sens borné (surface approuvée du maillage, inspectable dans le CT) ; la transcription est donnée en Methods (non extraite).
- PHerc. Paris 4 : encre vue comme dépôts brillants associés à la surface, épaisseur apparente d'environ 10 à 20 µm, après rétrieval de phase (Results, Fig. 2, Extended Data Fig. 3) ; segmentation 3D projetée sur la surface, coïncidant avec la région Grand Prize Banner de 2023 (Fig. 3). Validation physique indépendante, « sous au moins un régime de scan et un état de conservation de l'encre » (Results). Aucune métrique de recouvrement (Dice, etc.) rapportée dans le texte lu.
- PHerc. 139 : titre lu « Φιλοδήμου περὶ θεῶν Η̅ », soit Philodème, *On Gods*, livre 8 (Fig. 4) ; premier indice que ce traité comptait au moins 8 livres ; titre et numéro de livre sur la même ligne, mise en page rare (Results).
- Aucune ligne dans `benchmarks.csv` (voir Limites) : `benchmarks: none`.

## Limites et critique

- Pas de métrique d'encre ni de segmentation (précision, Dice, AUC, faux positifs) dans le texte lu : les affirmations reposent sur l'inspection experte et des figures. Pas de test à l'aveugle, de k-fold, de placebo ni de calibration décrits ici ; ils sont peut-être en Methods, non extraits.
- Les auteurs reconnaissent que la segmentation d'encre reste faible et varie selon la recette d'encre, l'état local et la diffusion des rayons X (Discussion). Les modèles sont décrits comme « amplificateurs de visibilité » : le risque d'hallucination n'est pas quantifié.
- Validation volumétrique (Paris 4) valable pour un seul rouleau et un état d'encre ; la généralisation n'est pas établie (les auteurs le disent). La comparaison de la Fig. 3 oppose deux scans de résolution différente (7,91 µm contre 2,4 µm) : on ne distingue pas gain de modèle et gain de scan.
- Goulots signalés : géométrique (fusions, trous, changements de feuillet en zones compressées) et radiométrique (Discussion). Part de correction manuelle du maillage non chiffrée.
- Reproductibilité : texte extrait sans Methods ni Extended Data ; énergie, temps de scan, code et données non vérifiables ici. Tous les auteurs sont du projet : pas d'évaluation externe. Preprint.

## Pertinence pour la thèse

Pertinence pour Elder-scrolls : référence de l'état de l'art (2026) de la chaîne visée (surface -> maillage quad -> aplatissement quasi isométrique -> rendu -> encre) avec scan synchrotron 2,4 µm. Apport : (i) preuve que le scan 2,4 µm avec rétrieval de phase rend l'encre directement visible sur Paris 4 (10-20 µm), ce qui éclaire la question « quelle part du signal d'encre survit à 8-9 µm » et motive la super-résolution/distillation 9 -> 2,4 µm ; (ii) cadre de validation par modalité indépendante (segmentation volumétrique contre encre de surface), utile contre les faux positifs ; (iii) pseudo-labels conservateurs et supervision fragment-vers-rouleau (label-efficiency) ; (iv) titre de PHerc. 139 : un exemple de validation papyrologique. Reste ouvert : métriques chiffrées, protocole de validation à l'aveugle, résultats à 8-9 µm, détails de segmentation en zones écrasées.

## Gaps identifiés

- Absence de métriques quantitatives d'encre dans ce papier : comparer à des protocoles chiffrés d'autres papiers.
- Visibilité directe de l'encre à 2,4 µm vs 7,91 µm sur Paris 4 : à quantifier à 8-9 µm (lien avec super-résolution).
- Pas de mesure du risque d'hallucination des « amplificateurs de visibilité ».
- Fusions/trous en zones compressées : méthodes de tracé hybrides citées comme piste, non évaluées.

## Statut de lecture

papier complet, mais l'extraction est dégradée : `extraction.backend` = pymupdf, `extraction.ok` = false, « aucune section détectée ». Le texte lu ne contient que le résumé, l'introduction, les résultats et la discussion ; Methods, Extended Data (dont Table 1, Fig. 3 étendue), Supplementary et la transcription sont **absents** : paramètres d'acquisition, énergie keV, matériel et détails des modèles sont donc n/r. Aucune section de benchmark n'existe ; aucun chunks.jsonl (chunk_id : n/r).
Ce qui suit est déduit et non affirmé par les auteurs : la lecture du « 2,4 µm rend l'encre visible » comme réponse à la question 8-9 µm du profil ; l'absence de métriques et de validation à l'aveugle (déduite du texte disponible seulement) ; la confusion gain de scan / gain de modèle sur la Fig. 3.
