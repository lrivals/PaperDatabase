---
id: 2023-romano-layout-ancient-greek-papyri-through
fiche: done
date: 2026-11-15
benchmarks: none
---

# Layout of ancient Greek papyri through lead-drawn ruling lines revealed by Macro X-Ray Fluorescence Imaging

Francesco Paolo Romano, Enzo Puglia, Claudia Caliri, Danilo Paolo Pavone, Michele Alessandrelli, Andrea Busacca, C. G. Fatuzzo, Kilian Josef Fleischer, Carlo Pernigotti, Zdeněk Preisler, Christian Vassallo, Gertjan Verhasselt, Costanza Miliani, Graziano Ranocchia, 2023, Scientific Reports 13:6582. https://doi.org/10.1038/s41598-023-33242-8
Type : article de journal (relu par les pairs ; accès libre CC BY 4.0)

## Problème

Les auteurs cherchent une preuve expérimentale directe de l'usage de lignes de réglure tracées au plomb par les scribes grecs pour la mise en page des rouleaux de papyrus, jusque-là connu seulement par des auteurs classiques (Catulle, Pline, Anthologie Palatine) et postulé par quelques savants (Gardthausen, Turner) (Introduction). Ils veulent aussi trancher la controverse sur la « loi de Maas » : l'inclinaison des colonnes vers la gauche (jusqu'à 5°) est-elle voulue ou accidentelle ? (Introduction).

## Méthode

- Imagerie par fluorescence X macroscopique (MA-XRF) in situ, non invasive, de fragments de papyrus d'Herculanum déroulés mécaniquement (pas de CT) (Results, Methods).
- Scanner mobile du XRAYLab CNR-ISPC Catania : tube à anode Rh, polycapillaire (spot 50 µm à 15 mm), tête à 6 détecteurs SDD en « hodoscope » (240 mm² actifs au total), géométrie 90°–45° ; acquisition temps réel (Methods, MA-XRF imaging set-up).
- Réglages : pas de 250 µm et 10 ms par pixel ; zones d'intérêt remesurées à 100 µm et 50 ms (Methods, Analysis of Herculaneum Papyri).
- Cartes de Pb (raies M, préférées aux raies L pour la surface car le Pb des lacunes traverse toute l'épaisseur) comparées à des images NIR (950 / 1000 nm) du même fragment (Results ; NIR prises par les auteurs ou par l'équipe BYU, réf. 33).
- Semi-quantification du Pb (limites hautes) à partir de cibles minces de référence : pixels de réglure choisis à la main, comparés à des pixels de fond tirés au hasard (Methods, Fig. 5, Tab. S1).

## Plateforme et implémentation

Pas de calcul ML : instrument de laboratoire mobile décrit ci-dessus. Données : « all data needed … in the paper and/or the Supplementary Information ; additional data on request » (Data availability) ; ni code ni jeu de données publics. Fragments : six rouleaux (PHerc. 1691/1021, 1018, 1420, 1390/908, 558, 164), mesurés en septembre 2021 et janvier 2022 à l'Officina dei Papiri Ercolanesi, Naples ; épaisseur du papyrus environ 0,15 mm (Methods, Samples description). Résolution : pas XRF de 250 µm ou 100 µm (pas de µm/voxel CT : sans objet). Labels / supervision : sans objet (analyse visuelle).

## Résultats

- Trois systèmes de mise en page identifiés (Results) :
  1. lignes verticales marquant seulement le bord gauche de chaque colonne (espace « colonne + entrecolonne ») et lignes horizontales haut et bas : PHerc. 1021 (Fig. 1) ; brouillon de l'Index Academicorum, qualité faible ;
  2. lignes verticales gauche et droite de chaque colonne et entrecolonne : PHerc. 1018 (Fig. 2), 1420 (Fig. 3), et 1390/908, 558 (Figs. S3, S4) ; qualité intermédiaire ou haute ;
  3. en plus, lignes horizontales servant de lignes de base du texte : PHerc. 164 (Fig. 4) ; copie calligraphique finale de l'Index Academicorum.
- Lignes verticales légèrement inclinées vers la gauche, tracées avant le texte : preuve que la loi de Maas est un choix délibéré (Discussion).
- Quantité de Pb : environ 8 ng par pixel le long des réglures (limite haute) contre environ 1 ng par pixel hors réglure, pixel de 250 µm, spot de 50 µm (Methods, Fig. 5). Les valeurs par ROI sont dans Tab. S1 (supplément, non lu).
- Pb aussi concentré aux bords des lacunes, attribué hypothétiquement à une migration de composés solubles ou à une contamination, non étudié (Results, Methods).
→ reportés dans `benchmarks.csv` : aucune ligne (pas de benchmark de modèle ; mesures d'instrument et résultats qualitatifs de papyrologie, sans configuration comparable aux colonnes de l'en-tête).

## Limites et critique

- Échantillon réduit : six rouleaux, un seul fragment par rouleau, souvent seulement une zone (« only a few selected samples were fully investigated », Results) ; la généralisation à « la pratique commune de la Méditerranée » (Discussion) est une inférence des auteurs.
- Association qualité du rouleau / système de réglure fondée sur très peu de cas (un seul rouleau pour les systèmes 1 et 3, Discussion) : corrélation non testée.
- Les lignes de réglure inférieures sont supposées (« should be assumed »), non imagées faute de temps (Results).
- Corrélation lignes de plomb / bord du texte établie par comparaison visuelle avec le NIR, sans mesure quantitative d'alignement ni test statistique ; sélection manuelle des pixels pour la quantification (Methods).
- Aucune comparaison avec des papyrus égyptiens (non étudiés) : l'absence de réglure au plomb ailleurs est une absence de test, pas une preuve (Discussion).
- Les papyrus ont subi un choc thermique : les lignes horizontales sont ondulées (Results), caveat pour toute géométrie dérivée.
- Non reproductible en l'état (instrument sur mesure, données sur demande).

## Pertinence pour la thèse

Papier de papyrologie / imagerie de matériaux sur papyrus déroulés, pas sur rouleaux fermés. Apports possibles pour Elder-scrolls (déduit, non affirmé par les auteurs) : (1) priors géométriques de mise en page (colonnes inclinées à gauche, marges, lignes de base régulières) pour valider ou régulariser la lecture d'une prédiction d'encre et des colonnes reconstituées ; (2) du Pb non lié à l'encre (réglure, contamination aux bords des lacunes) est un facteur de confusion potentiel pour des signaux liés au plomb ; (3) les textes (Philodème, Épicure) sont ceux visés par le Challenge. Reste ouvert : lien avec le signal CT de rouleaux fermés, aucune donnée CT ici.

## Gaps identifiés

- Détectabilité éventuelle d'une réglure au plomb (environ 8 ng par pixel de 250 µm, traces) dans des scans micro-CT 8–9 µm de rouleaux fermés : non traitée.
- Exploiter la mise en page (inclinaison de Maas, intercolonnes) comme prior de validation des lettres prédites : aucune méthode dans le papier.
- Chimie du Pb (contamination, migration) et interférence avec les signaux d'encre : explicitement hors périmètre (Results).

## Statut de lecture

papier complet (`fulltext.md` lu en entier ; extraction `pymupdf`, `extraction.ok` à false, « aucune section détectée » : pas de découpage en sections, légendes de figures mêlées au texte, figures non vérifiées visuellement). Supplément (Figs. S1–S9, Tab. S1) indisponible : valeurs de Tab. S1 non lues.
Ce qui suit est déduit et non affirmé par les auteurs : toute la section « Pertinence » (priors de mise en page, facteur de confusion Pb en CT) et le jugement qu'un échantillon de six rouleaux est trop limité pour corréler qualité du rouleau et système de réglure.
