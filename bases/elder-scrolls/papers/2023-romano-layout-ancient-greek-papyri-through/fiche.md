---
id: 2023-romano-layout-ancient-greek-papyri-through
fiche: done
date: 2026-11-15
benchmarks: none
---

# Layout of ancient Greek papyri through lead-drawn ruling lines revealed by Macro X-Ray Fluorescence Imaging

Francesco P. Romano, Enzo Puglia, Claudia Caliri, Danilo P. Pavone, Michele Alessandrelli, Andrea Busacca, Claudia G. Fatuzzo, Kilian J. Fleischer, Carlo Pernigotti, Zdenek Preisler, Christian Vassallo, Gertjan Verhasselt, Costanza Miliani, Graziano Ranocchia, 2023, Scientific Reports 13:6582. https://doi.org/10.1038/s41598-023-33242-8
Type : article de journal (open access, CC BY 4.0)

## Problème

Les scribes grecs traçaient-ils des lignes de réglure au plomb pour mettre en page les rouleaux ? Seules les sources classiques (Catulle, Pline, Anthologie Palatine) l'affirmaient ; aucune preuve directe n'existait. Question connexe : l'inclinaison vers la gauche des colonnes (« loi de Maas », jusqu'à 5°) est-elle voulue ou une imprécision du scribe (Introduction).

## Méthode

Pas d'algorithme d'apprentissage : imagerie physique. MA-XRF (macro X-ray fluorescence) mobile, déconvolution à la volée des spectres par pixel, cartes de distribution élémentaire du Pb (raies M et L ; Pb-M utilisé pour les figures car Pb-L est pollué par l'agrégation de plomb au bord des lacunes, Methods). Entrées : fragments de papyrus déroulés mécaniquement aux XVIIIe-XIXe s. (pas de CT). Vérité terrain : aucune annotation ; comparaison visuelle des cartes Pb avec des images NIR (950-1000 nm) des mêmes fragments (Figs. 1-4). Quantification semi-quantitative du Pb via des cibles minces de référence : ~8 ng/pixel sur les lignes (borne haute), ~1 ng/pixel hors lignes (Methods, Fig. 5, Tab. S1) ; pixels des lignes choisis à la main (biais de sélection, déduit).

## Plateforme et implémentation

- Source de l'imagerie : scanner MA-XRF mobile de laboratoire (XRAYLab CNR-ISPC Catania), mesure in situ à l'Officina dei Papiri Ercolanesi (Naples), sept. 2021 et janv. 2022 ; tube à anode Rh avec polycapillaire (spot 50 µm à 15 mm, mesuré à 10 keV), 6 détecteurs SDD (240 mm2 au total), géométrie 90°-45° (Methods). Ni synchrotron ni micro-CT.
- Résolution : pixel typique 250 µm, 10 ms ; zones d'intérêt à 100 µm, 50 ms ; minimum 1 mm / 7 ms (Methods).
- Objets : six rouleaux déroulés (PHerc. 1691/1021, 1018, 1420, 1390/908, 558, 164), un fragment par rouleau (de 6,4 x 37,1 à 20,8 x 30,5 cm), ~0,15 mm d'épaisseur, collés sur carton ; IIe s. av. J.-C. au Ier s. ap. J.-C. (Methods).
- Calcul : unité temps réel multi-nœuds (FPGA, serveur Xeon, deux CPU Intel 9e génération) ; temps de calcul n/r (traitement à la volée).
- Évaluation : pas de jeu de test ni de région tenue à l'écart ; confirmation visuelle sur les fragments mesurés (certains seulement en zones partielles, faute de temps).
- Code et données : pas de code publié ; données « dans le papier et le matériel supplémentaire, le reste sur demande » (Data availability).

## Résultats

Trois systèmes de mise en page identifiés d'après le Pb (Results, Figs. 1-4, S3, S4) :
1. Ligne horizontale en haut + lignes quasi verticales marquant le bord gauche de chaque colonne (intercolonne non distinguée) : PHerc. 1021, rouleau de qualité inférieure (version provisoire du Index Academicorum) (Fig. 1).
2. Lignes verticales délimitant colonnes et intercolonnes (une horizontale + sept verticales) : PHerc. 1018 et 1420 ; aussi PHerc. 1390/908 et 558 (Figs. 2, 3, S3, S4).
3. Grille complète avec lignes horizontales servant de lignes de base du texte : PHerc. 164, version calligraphique finale (Fig. 4).
Lignes verticales inclinées à gauche, cohérent avec la loi de Maas, tracées avant le texte : preuve que l'inclinaison est délibérée (Discussion). Lignes horizontales ondulées par la déformation thermique de l'éruption de 79 (Results). Corrélation système de réglure / qualité du rouleau : interprétation des auteurs sur 3 rouleaux (déduit, échantillon faible). Plomb aussi concentré aux bords des lacunes (cause non tranchée).
→ reportés dans `benchmarks.csv` : aucune ligne (pas de métrique de performance comparable ; chiffres uniquement physiques, Methods).

## Limites et critique

- Échantillon de 6 rouleaux, un fragment chacun, parfois zones partielles ; la partie basse des colonnes n'est pas imagée (limite de temps) : la ligne inférieure est supposée, non observée.
- Validation purement qualitative (superposition NIR / Pb), sans métrique de détection ni mesure d'erreur de position des lignes.
- Quantité de Pb : bornes hautes, sélection manuelle de pixels ; le signal de surface est difficile à séparer du plomb de contamination ou migré (Pb-L vs Pb-M).
- Pas de lecture des lettres ni d'encre : le Pb de réglure n'est pas l'encre (les travaux sur l'encre au plomb sont cités, refs 29-30). Non applicable aux rouleaux non ouverts.
- Pas de code ; instrument de laboratoire non commercial.
- Aucune ligne de réglure n'a été trouvée sur des papyrus gréco-égyptiens ; les auteurs notent que MA-XRF n'y a pas été appliqué systématiquement (Discussion).

## Pertinence pour la thèse

Axe papyrologie. Intérêt indirect pour Elder-scrolls : (1) prior géométrique de mise en page (colonnes inclinées jusqu'à ~5°, intercolonnes régulières, marges haute/basse, lignes de base) utilisable pour valider ou régulariser les cartes d'encre aplaties et l'assemblage des colonnes ; (2) validation papyrologique : une mise en page régulière retrouvée dans une lecture virtuelle appuie son authenticité ; (3) le Pb comme signal élémentaire sur papyrus d'Herculanum, distinct du contraste d'absorption CT. Reste ouvert : détectabilité de ces lignes en micro-CT (une trace de ~8 ng/pixel à 250 µm paraît hors de portée à 8-9 µm, déduit, non testé) ; fusion MA-XRF/CT n/r.

## Gaps identifiés

- Détection de la réglure ou de la mise en page dans les volumes CT : non couverte.
- Utilisation de contraintes de mise en page (loi de Maas, grille de lignes) pour la validation des lettres virtuelles.
- Extension MA-XRF aux papyrus littéraires gréco-égyptiens.

## Statut de lecture

papier complet (fulltext.md lu en entier ; extraction `pymupdf`, `ok: false`, aucune section détectée : texte lisible mais légendes de Figs. 1-3 tronquées ; supplément Figs. S1-S9 et Tab. S1 non disponible).
Ce qui suit est déduit et non affirmé par les auteurs : biais de sélection des pixels, détectabilité en CT, lien avec les contraintes de validation d'Elder-scrolls, faiblesse de l'échantillon pour la corrélation qualité/système.
