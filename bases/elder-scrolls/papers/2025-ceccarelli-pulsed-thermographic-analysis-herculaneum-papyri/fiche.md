---
id: 2025-ceccarelli-pulsed-thermographic-analysis-herculaneum-papyri
fiche: done
date: 2026-11-15
benchmarks: none
---

# Pulsed thermographic analysis of Herculaneum papyri

Sofia Ceccarelli, Massimo Rippa, Giovanni Caruso, Loredana Luvidi, Simona Boccuti, Melania Paturzo, Vito Pagliarulo, Kilian Josef Fleischer, Costanza Miliani, Graziano Ranocchia, 2025, Scientific Reports. https://doi.org/10.1038/s41598-025-19911-w
Type : article de journal (relu par les pairs ; reçu le 19 mai 2025, accepté en septembre 2025)

## Problème

Le texte des papyrus d'Herculanum, carbonisés, est difficile à lire : l'encre est à base de carbone, de composition proche du support noirci (Introduction). Les auteurs veulent un moyen non invasif d'obtenir à la fois le texte et des informations structurales (fibres, points d'adhérence au carton) sur des fragments déroulés mais collés sur carton, qu'on ne peut ni détacher ni placer à la verticale (Matériaux et méthodes). Premier usage de la thermographie pulsée (PT) sur ces papyrus (Introduction).

## Méthode

Pas d'apprentissage : imagerie active et traitement de signal classique, sur des fragments déjà déroulés (pas de scan CT, pas de déroulage virtuel).
- Entrée : séquences thermographiques en réflexion après un flash (deux lampes, 3 kW max., à 45°, filtres verre-eau contre UV et IR des lampes) ; échauffement de 2–3 °C (Matériaux et méthodes).
- Texte : première(s) image(s) après le flash, cadence maximale 520 Hz, résolution spatiale maximale ; rehaussement de contraste (Matlab, masques GIMP), mosaïque de zones d'environ 15 × 12 cm recouvrantes (PTgui, ICE) (Matériaux et méthodes ; Résultats).
- Structure : cadence 128 Hz, mesures plus longues ; cartes de temps de récupération (TR, temps pour retrouver 50 % du ΔT induit ; seuil 45–55 % sans effet notable) et thermographie de phase pulsée (PPT, FFT 1D par pixel, phase à 0,2 Hz retenue ; amplitude écartée car sensible à l'inhomogénéité de l'éclairage) (Matériaux et méthodes).
- Labels : aucun. Comparaison qualitative à la photographie NIR à 1000 nm (Pavone et al. 2022) et à la lumière rasante visible.
- Mécanisme proposé (hypothèse, non mesurée) : l'encre en surface absorbe plus dans le visible, s'échauffe davantage et émet plus en IR ; le contraste vient d'une différence d'absorption VIS / émission IR, pas d'une diffusion thermique (Résultats, Textual enhancement).

## Plateforme et implémentation

- Source d'imagerie : thermographie infrarouge (pas de rayons X, pas de synchrotron, pas de keV). Caméra FLIR X6800sc, MWIR 3,5–5 µm, détecteur InSb refroidi, pas 25 µm, 640 × 512 px, 520 Hz à pleine résolution, NETD < 20 mK à 30 °C (Matériaux et méthodes).
- Résolution : µm/pixel sur le papyrus n/r. Lettres de 3–4 mm ; épaisseur du papyrus ~0,15 mm, carton ~0,30 mm (Matériaux et méthodes).
- Objets : quatre fragments déroulés, collés sur carton : PHerc. 1018 (cornices 1 et 2, Philodème, Histoire du Portique), PHerc. 1691/1021 (cornice 2, Histoire de l'Académie), PHerc. 1780 (cornice 7), PHerc. 1025 (cornice 1) (Matériaux et méthodes). Mesures en mars et novembre 2024, dans le cadre du projet ERC GreekSchools (Remerciements).
- Calcul : scripts Matlab R2019b maison, FLIR Research Studio 3.1.0 ; matériel de calcul et temps de traitement n/r.
- Code et données : code non publié ; « toutes les données nécessaires sont dans l'article et le SI, autres sur demande » (Data availability). Article en accès libre CC BY 4.0.

## Résultats

Résultats qualitatifs uniquement ; aucune métrique, aucun baseline chiffré, aucun test statistique.
- Texte : la PT améliore nettement la lisibilité par rapport à la NIR 1000 nm sur PHerc. 1018 c.1 (haut de quatre colonnes bien lu ; certaines lettres mieux révélées dans la partie basse, multicouche) (Fig. 1) ; PHerc. 1021 c.2, substrat très sombre : cinq colonnes lacunaires mieux révélées (Fig. 2) ; PHerc. 1780 c.7, « meilleur contraste et lisibilité jamais obtenus » pour ce papyrus (Fig. 3).
- Valeur papyrologique : confirme la lecture προεµνήϲθηµεν (col. 3, l. 4–5 de PHerc. 1018) contre l'ancienne προεµνήϲαµεν (Résultats) ; valide une reconstruction de PHerc. 1021 col. 9, l. 34–37 (Résultats).
- Structure : cartes TR (temps courts = contact avec le carton ou faible profondeur ; temps longs = lame d'air) et phase PPT à 0,2 Hz (fibres, ondulations ; « nuages » blanchâtres là où le papyrus adhère au carton) (Fig. 4, Fig. 5 ; Fig. S2 pour PHerc. 1025).
- Les lettres sont déformées là où la surface est non plane (focalisation) ; les auteurs reconnaissent qu'une optimisation des paramètres est nécessaire pour chaque papyrus (Résultats, Discussion).
- Évaluation : pas de vérité terrain, pas de région ni de rouleau tenu à l'écart ; jugement visuel des auteurs/papyrologues.
→ reportés dans `benchmarks.csv` : aucune ligne (pas de configuration chiffrée ; `benchmarks: none`).

## Limites et critique

- Aucune quantification (contraste, SNR, taux de lettres lues), aucun jugement à l'aveugle ni inter-lecteurs : « meilleur que NIR » est qualitatif.
- Ne concerne que des fragments déroulés (Piaggio) en réflexion ; sans rapport direct avec les rouleaux fermés du Vesuvius Challenge, où le CT est la seule voie. Aucun lien avec le CT n'est testé (la PT ne voit que la surface visible).
- Mécanisme du contraste postulé (absorption VIS / émission IR de l'encre), non vérifié ; les auteurs notent que d'autres bandes (SWIR) ont donné un contraste comparable ou supérieur (Discussion, réf. 18).
- Quatre fragments, un seul laboratoire ; paramètres à réajuster par papyrus ; pas de code. L'IA est citée seulement comme perspective (Discussion).
- Comparaison à la NIR 1000 nm sans mesure : biais possible du choix des images et de la palette (palette standard ou inversée selon la figure).

## Pertinence pour la thèse

Peu directe pour la chaîne CT du projet, mais utile comme vérité terrain potentielle et contexte : images de surface (thermographie, NIR, SWIR) de papyrus d'Herculanum déroulés, dont les lectures papyrologiques validées (PHerc. 1018, 1021) pourraient servir de référence indépendante pour valider des lettres ou des cartes d'encre. Rappelle que le signal d'encre carbonée est un contraste faible en absorption, ici exploité en IR de surface ; l'observation (cartes TR) que les « nuages » de PPT et les variations de profondeur recoupent la topographie du papyrus et les kolleseis est à rapprocher des hypothèses morphologiques de détection d'encre. Laisse ouvert : traitement automatique (les auteurs le citent comme piste) et fusion avec le CT.

## Gaps identifiés

- Aucun jeu de données thermographique public ni protocole de validation chiffré pour la lecture de papyrus d'Herculanum en imagerie de surface.
- Pas de comparaison entre modalités de surface (PT, NIR, SWIR, macro-XRF) sur les mêmes fragments, ni avec l'encre prédite en CT.

## Statut de lecture

papier complet (`fulltext.md` lu en entier). Extraction `pymupdf`, `extraction.ok: false`, aucune section détectée : le texte est complet mais mal découpé ; le SI (Fig. S1–S3) n'est pas dans le texte.
Déduit et non affirmé par les auteurs : la non-pertinence directe pour les rouleaux fermés ; l'absence de lien CT ; l'usage possible des lectures comme référence de validation ; le biais de choix des images.
