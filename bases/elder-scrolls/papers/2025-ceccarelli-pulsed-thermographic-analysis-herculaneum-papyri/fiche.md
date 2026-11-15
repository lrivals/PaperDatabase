---
id: 2025-ceccarelli-pulsed-thermographic-analysis-herculaneum-papyri
fiche: done
date: 2026-11-15
benchmarks: none
---

# Pulsed thermographic analysis of Herculaneum papyri

Sofia Ceccarelli, Massimo Rippa, Giovanni Caruso, Loredana Luvidi, Simona Boccuti, Melania Paturzo, Vito Pagliarulo, Kilian Josef Fleischer, Costanza Miliani, Graziano Ranocchia, 2025, Scientific Reports. https://doi.org/10.1038/s41598-025-19911-w
Type : article de journal (relu par les pairs ; reçu 19/05/2025, accepté 11/09/2025). Accès libre (CC BY 4.0).

## Problème

Les papyrus d'Herculanum sont carbonisés, et leur encre (carbonée) est presque indiscernable du substrat sombre (Introduction, Discussion). Les auteurs veulent un moyen non invasif d'obtenir à la fois la lecture du texte et des informations structurales (texture, points d'adhésion au carton) utiles aux restaurateurs, ce qui n'avait « jamais été fait » avec une seule méthode (Discussion). Ils étudient des fragments **déroulés mécaniquement** (machine de Piaggio) et collés sur carton, pas des rouleaux fermés : il n'y a ni CT ni déroulage virtuel ici.

## Méthode

- Thermographie pulsée (PT) en réflexion : deux flashs (3 kW max, Hensel EH Mini + Tria 24, à 45° de la surface, filtres verre+eau contre UV et IR de la lampe) chauffent le papyrus de ~2–3 °C ; une caméra FLIR X6800sc (MWIR 3,5–5 µm, InSb refroidi, pas 25 µm, 640 × 512 px, 520 Hz à pleine résolution, NETD < 20 mK) enregistre l'émission IR (Matériaux et méthodes). La transmission n'est pas utilisée car les fragments ne peuvent être décollés de leur support.
- Texte : acquisition à 520 Hz, quelques thermogrammes seulement ; les premières images après le flash donnent le meilleur contraste. Traitement : rehaussement de contraste (Matlab), masques de netteté GIMP, mosaïque (PTgui, ICE). Zones d'inspection d'environ 15 × 12 cm avec recouvrement (Résultats).
- Structure : acquisition à 128 Hz, plus longue ; cartes de temps de recouvrement thermique (TR, temps pour retrouver 50 % du ΔT induit ; seuil 45–55 % sans effet notable) et thermographie de phase pulsée (PPT, FFT 1D par pixel ; phase à 0,2 Hz retenue, 0,1 Hz saturé, > 0,3 Hz moins contrasté ; les amplitudes sont écartées car l'éclairage est inhomogène). Scripts Matlab R2019b maison.
- Mécanisme proposé (hypothèse, pas mesuré) : l'encre en surface absorbe plus dans le visible et émet plus en IR que le papyrus carbonisé, d'où une encre plus chaude juste après le flash (Textual enhancement).
- Échantillons : quatre papyrus déroulés, PHerc. 1018 (cornices 1 et 2), 1691/1021 (cornice 2), 1780 (cornice 7), 1025 (cornice 1) ; épaisseur ~0,15 mm, lettres de 3–4 mm.

## Plateforme et implémentation

- Matériel : caméra FLIR X6800sc, flashs Hensel (voir Méthode). Mesures en mars et novembre 2024, dans le cadre du projet ERC GreekSchools (Remerciements).
- Pas de calcul lourd (traitement Matlab/GIMP) ; temps de calcul `n/r`.
- Code : non publié (« scripts Matlab maison ») ; données : dans l'article et le matériel supplémentaire, le reste « sur demande » (Data availability).
- Pas de résolution en µm/voxel (imagerie 2D) : résolution spatiale de la caméra en µm/pixel au sol `n/r` ; seul le pas du détecteur (25 µm) est donné.

## Résultats

Résultats **qualitatifs uniquement**, aucune métrique rapportée :
- PHerc. 1018 cornice 1 : la mosaïque thermique est comparée à l'image NIR à 1000 nm ; meilleure lecture du haut de quatre colonnes et de plusieurs lettres dans la partie basse, multicouche (Fig. 1). Colonne 3, lignes 4–5 : la thermographie confirme la lecture récente προεµνήϲ|˹θ͙η͙˺µ̣ε̣ν̣ au lieu de προεµνήϲ|α̣µ̣ε̣ν̣ (Résultats).
- PHerc. 1021 cornice 2 (substrat très sombre, à peine lisible en NIR) : restes de cinq colonnes mieux révélés (Fig. 2) ; la reconstruction de la col. 9, l. 34–37, est « validée » par la continuité physique du papyrus.
- PHerc. 1780 cornice 7 (non plan, multicouche) : « meilleur contraste et lisibilité jamais atteints » pour ce papyrus selon les auteurs (Fig. 3).
- Structure : les cartes TR distinguent zones en contact avec le carton (temps courts) et zones surélevées (temps longs, l'air isole) ; elles peuvent aussi refléter les kolleseis ou des couches superposées restées collées (Fig. 4b, Fig. 5). La phase PPT à 0,2 Hz montre la trame des fibres et la corrugation, masquées par endroits par des « nuages » blanchâtres qui coïncident avec l'adhésion au carton (Fig. 4c, Fig. 5, Fig. S2 pour PHerc. 1025).
- Les auteurs reconnaissent que des travaux en SWIR hyperspectral (réf. 18) obtiennent un contraste comparable ou supérieur (Discussion).
- Les lettres peuvent apparaître déformées selon la morphologie de surface (Résultats).
→ reportés dans `benchmarks.csv` : aucune ligne (aucune valeur chiffrée de performance ; comparaison seulement visuelle à la NIR 1000 nm).

## Limites et critique

- Aucune évaluation quantitative : pas de métrique de contraste, de rapport signal/bruit, de lecture à l'aveugle ni de vérité terrain ; les « confirmations » de lecture (col. 3 de PHerc. 1018, col. 9 de PHerc. 1021) s'appuient sur l'avis des papyrologues coauteurs (Ranocchia, Fleischer), qui sont aussi les éditeurs des textes concernés (réfs. 49, 50), donc non indépendants. Déduit.
- Comparaison avec la NIR seulement, sans pas de multispectral ni SWIR présentés ; la comparaison est visuelle, les palettes de couleurs changent d'une figure à l'autre (Fig. 2, 3).
- Mécanisme de contraste donné comme « probable » ; la méthode dépend des fragments (paramètres à réoptimiser pour chaque papyrus, Discussion).
- Les chiffres de dégradation thermique (ΔT 2–3 °C, « sans risque ») sont un argument, pas une mesure de non-dommage.
- Limité à des fragments plats déroulés ; non applicable aux rouleaux fermés. Le signal exploité est en surface (encre en face avant) : aucun lien démontré avec le signal d'encre en CT.
- Pas de code publié.

## Pertinence pour le thème

Pertinence indirecte et faible pour la chaîne CT d'Elder-scrolls (prédiction de surface, aplatissement, Reader V3). Le papier apporte (i) une **modalité de vérité terrain indépendante** potentielle sur des fragments déroulés, où l'encre réagit au flash en MWIR, utile pour la validation et la lecture inversée ; (ii) un exemple de lecture papyrologique confirmée par une image non CT (axe papyrologie, validation) ; (iii) l'idée, en l'état non testée, d'un indice morphologique (hauteur, adhésion, fibres via PPT) qui rappelle les champs de fibres et la structure de surface exploités en CT. Il laisse ouvert : toute mesure quantitative, la comparaison avec les cartes d'encre CT, et l'appui par apprentissage (les auteurs suggèrent la reconnaissance de motifs/IA comme piste, Discussion).

## Gaps identifiés

- Aucune base de comparaison quantitative entre thermographie, NIR/SWIR et cartes d'encre CT sur un même fragment.
- Pas de lien établi entre le signal thermique d'encre (absorption/émission en surface) et le signal d'encre carbonée en CT à 8–9 µm.
- Pas de segmentation automatique de l'encre sur images thermiques.

## Statut de lecture

papier complet (texte principal ; matériel supplémentaire Fig. S1–S3 non lu, figures non vues). Attention : `extraction.backend` = `pymupdf` et `extraction.ok` = `false` (aucune section détectée) : le texte peut être mal découpé (légendes déplacées, deux colonnes entremêlées), mais aucun tableau n'est concerné. `chunks.jsonl` n'existe pas : pas de `chunk_id`.
Déduit et non affirmé par les auteurs : l'indépendance limitée des confirmations de lecture, la faible pertinence pour la chaîne CT, la possibilité d'une vérité terrain indépendante, l'absence de lien avec le signal d'encre CT.
