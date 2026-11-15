---
id: arxiv-2606.29085-complete-virtual-unwrapping-reading-rolled
fiche: done
date: 2026-11-15
---

# Complete virtual unwrapping and reading of a rolled Herculaneum papyrus

Giorgio Angelotti, Stephen Parsons, Federica Nicolardi, Youssef Nader, Sean Johnson, David Josey, Paul Henderson, Hendrik Schilling, Johannes Rudolph, Forrest McDonald, Elian Rafael Dal Prá, Paul Tafforeau, Alessandro Mirone, Clifford Seth Parker, Jan Paul Posma, Benjamin Kyles, Claudio Vergara, Alessia Lavorante, Rossella Villa, Maria Chiara Robustelli, Marzia D'Angelo, Gianluca Del Mastro, Michael McOsker, Kilian Fleischer, Christy Chapman, Nat Friedman, William Brent Seales, 2026, arXiv preprint. https://arxiv.org/abs/2606.29085 (arXiv 2606.29085, pas de DOI)
Type : preprint non relu par les pairs

## Problème

Les rouleaux carbonisés d'Herculanum sont illisibles sans ouverture destructrice ; les travaux antérieurs sur rouleaux fermés n'avaient donné que des lectures locales ou des régions de surface limitées (Abstract). Verrou posé par les auteurs : l'encre carbonée a un contraste d'absorption quasi nul face au papyrus carbonisé, et son signal varie (recette, contaminants, relief, préservation) ; il manquait une chaîne de bout en bout « échantillon entier → surface lisible » couplant imagerie synchrotron optimisée, reconstruction géométrique, récupération d'encre et revue papyrologique (Introduction).

## Méthode

Chaîne en quatre étages (« Technical strategy ») :
- **Tomographie** : scan synchrotron à contraste de phase modéré, régime choisi après une série de tests (énergie, résolution, géométrie, niveau de contraste de phase) ; reconstruction de grands volumes par la méthode citée [22]. Paramètres dans les Methods / Extended Data Table 1 : **non présents dans le texte extrait** (n/r ici).
- **Segmentation et déroulage** : un modèle appris de segmentation de la surface recto donne des indices volumétriques ; la surface finale est un **maillage quadrilatéral explicite**, extrait, corrigé manuellement si besoin, ré-optimisé localement, puis paramétré dans un domaine 2D quasi isométrique à faible distorsion. Chaque point du plan aplati garde ses coordonnées 3D dans le CT, ce qui permet de distinguer erreur de placement de surface et erreur d'interprétation de l'encre. Algorithmes précis (flatboi, SLIM…) : n/r dans le texte lu.
- **Détection d'encre, régime 1 (rouleaux fermés)** : l'encre est trop subtile pour une segmentation volumique ; des réseaux entraînés sur des supervisions dérivées de fragments (labels IR) et des pseudo-labels « conservateurs » de rouleaux scellés renforcent la visibilité sur des rendus conditionnés par la surface. Ces modèles sont des « amplificateurs de visibilité » pour l'inspection d'experts, pas des systèmes de lecture : pas d'entraînement sur identités de caractères, mots, transcriptions ou OCR. Architecture, perte, entraînement : n/r.
- **Régime 2 (PHerc. Paris 4)** : l'encre est directement visible dans le volume après phase retrieval ; segmentation 3D de l'encre puis projection sur la surface aplatie.
- **Revue papyrologique** : transcription restreinte au texte préservé visible ; crochets pour lettres perdues, point souscrit pour lettres incertaines.

## Plateforme et implémentation

- Source : synchrotron ESRF, ligne **BM18**, µCT à contraste de phase ; énergie (keV) : n/r dans le texte lu (Extended Data Table 1 absente de l'extraction).
- Résolution : voxel isotrope **2,4 µm** (Fig. 1b pour PHerc. 1667 ; Fig. 2a pour Paris 4). Comparaison avec l'ancien volume EduceLab-Scrolls de Paris 4 à **7,91 µm** (Fig. 3).
- Objets : PHerc. 1667 (rouleau scellé, résultat principal), PHerc. Paris 4 (validation volumique), PHerc. 139 (titre).
- Matériel de calcul, temps de déroulage / d'inférence, effort manuel de correction : n/r.
- Code et données : liens n/r dans le texte lu (pas de section Data/Code availability extraite). Données du Vesuvius Challenge et EduceLab-Scrolls citées [3] ; à vérifier.
- Labels : encre des fragments (supervision issue de fragments), pseudo-labels de rouleaux scellés, pas de vérité terrain sur 1667 ; pour Paris 4, la segmentation 3D de l'encre sert de contrôle physique.

## Résultats

- **PHerc. 1667** : surface reconstruite de **22 colonnes ou équivalents sur environ 860 cm²** de surface préservée (Results). Lecture papyrologique complète du texte préservé et visible, sauf **33 cm²** (parties survivantes des trois premières colonnes) où l'état fragmentaire interdit une interprétation sûre (Results). Définitions bornées : « déroulage complet » = surface préservée revendiquée représentée par un maillage approuvé, inspectable dans le CT ; « lecture complète » = texte soutenu par l'image. Transcription complète renvoyée aux Methods (absents de l'extraction).
- **PHerc. Paris 4** : l'encre apparaît comme dépôts brillants proches de la surface, d'épaisseur apparente **~10 à 20 µm** (Fig. 2, Extended Data Fig. 3). Le masque 3D projeté coïncide avec la région « Grand Prize Banner » de 2023 et confirme sa lecture (Fig. 3) : validation indépendante, « sous au moins un régime de scan et un état de préservation de l'encre ». Comparaison qualitative avec le modèle d'encre gagnant 2023 sur le volume 7,91 µm ; aucune métrique chiffrée.
- **PHerc. 139** : titre lu « Φ̣ι[λοδ]ή̣μου περὶ θεῶν Η̅ », soit Philodème, *Sur les dieux*, livre 8 (Fig. 4) ; première attestation d'un livre 8 (le seul livre connu jusqu'ici : livre 1, PHerc. 26). Datation 1er s. av. J.-C. à 1er s. ap. J.-C. (terminus ante quem 79).
- Aucune métrique de détection d'encre (AUC, F-score, IoU), pas de k-fold, pas de test placebo, pas de taux de faux positifs dans le texte lu.

→ reportés dans `benchmarks.csv` : 2 lignes descriptives (surface 860 cm², zone non transcrite 33 cm²), pas des scores de modèle. L'épaisseur d'encre (10-20 µm, plage) n'est pas reportée : une plage n'a pas de valeur unique.

## Limites et critique

- Preprint non relu ; texte extrait **sans Methods, Extended Data, Supplementary** (`extraction.ok: false`, pymupdf) : paramètres de scan, détails des modèles, transcription et protocole de validation papyrologique non vérifiables ici.
- **Faux positifs / validation** : la validation de la lecture repose sur la revue d'experts, avec des définitions volontairement bornées ; aucune quantification de la hallucination ou de la calibration des cartes d'encre. La seule validation physique est Paris 4, un seul rouleau à encre directement visible : les auteurs eux-mêmes limitent la portée. Risque de circularité (pseudo-labels issus de rouleaux scellés, lecture guidée par le rendu) à examiner (déduit).
- Les auteurs relèvent deux goulots : géométrie (zones compressées : fusions, trous, sauts de feuillet) et radiométrie (encre faible, variable selon recette et diffusion X) ; le déroulage reste « semi-automatisé » avec corrections manuelles, effort non chiffré.
- Pas d'ablation (2,4 µm contre 8-9 µm) ni comparaison chiffrée aux méthodes précédentes ; 1667 n'a pas de vérité terrain indépendante.
- Pas de rouleau ni de région tenu à l'écart au sens ML : l'évaluation est qualitative, sur les mêmes rouleaux que ceux traités.
- « Complet » est borné à la surface préservée ; ne généralise pas aux autres rouleaux (Discussion).

## Pertinence pour la thèse

Papier de référence pour le projet : définit la chaîne cible (modèle de surface recto, maillage explicite quad, paramétrisation quasi isométrique, rendu conditionné par la surface, encre comme amplificateur de visibilité, revue papyrologique), établit que l'échelle de rouleau complet est atteignable à 2,4 µm synchrotron, et fournit un cadre de validation (traçabilité 2D→3D, volume de contrôle Paris 4). Il laisse ouverts : l'encre à 8-9 µm, la quantification des faux positifs, le transfert entre scans, l'automatisation des zones compressées (suivi hybride neuronal évoqué, Discussion).

## Gaps identifiés

- Aucune métrique de validation d'encre (calibration, incertitude, placebo) ; contrôle physique limité à Paris 4.
- Effet de la résolution (2,4 contre 7,91 µm, ou 8-9 µm) sur la lisibilité : seulement comparaison visuelle (Fig. 3).
- Déroulage dans les zones compressées encore manuel ; effort et temps non chiffrés.
- Paramètres de scan, code et données à récupérer dans les Methods / la version complète.

## Statut de lecture

Papier complet **tel qu'extrait** : tout `fulltext.md` lu, mais l'extraction est pymupdf avec `ok: false` et ne contient que le texte principal (pas de Methods, Extended Data, Supplementary, ni références numérotées exploitables). Déduit et non affirmé par les auteurs : risque de circularité des pseudo-labels, absence de rouleau tenu à l'écart, jugement sur la portée de la validation, rôle de « papier central » pour le projet.
