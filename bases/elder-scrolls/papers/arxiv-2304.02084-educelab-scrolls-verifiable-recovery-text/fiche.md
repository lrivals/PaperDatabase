---
id: arxiv-2304.02084-educelab-scrolls-verifiable-recovery-text
fiche: done
date: 2026-11-15
---

# EduceLab-Scrolls: Verifiable Recovery of Text from Herculaneum Papyri using X-ray CT

Stephen Parsons, C. Seth Parker, Christy Chapman, Mami Hayashida, W. Brent Seales, 2023, arXiv preprint. https://arxiv.org/abs/2304.02084 (DOI : n/r)
Type : preprint non relu par les pairs

## Problème

Lire sans les dérouler les papyrus carbonisés d'Herculanum. Deux verrous posés par les auteurs (§1) : (1) l'encre (noir de fumée, presque du carbone pur) est quasi invisible en CT sur un support lui aussi carboné, donc pas de contraste d'absorption ; (2) la segmentation 3D de feuillets compressés, froissés, avec des centaines de spires. Contribution double : un jeu de données ouvert (CT volumétrique + labels 2D alignés) et une chaîne logicielle de déroulage virtuel avec détection d'encre par apprentissage supervisé.

## Méthode

- **Pipeline** : segmentation du feuillet, texturation, aplatissement avec Volume Cartographer (§3.1, §4.1.3), puis détection d'encre « ink-ID », raffinement de [37] (§1).
- **Entrées** : petites régions 3D du « surface volume » (volume échantillonné autour de la surface aplatie, vu comme image 2D à canaux de profondeur) ; taille de patch : n/r dans le texte lu (renvoyée à l'Annexe A, absente de `fulltext.md`).
- **Tâche** : classification binaire ink / non-ink du voxel central de chaque patch (§2.1). Aucune connaissance d'alphabet ni d'OCR.
- **Labels** : photographies infrarouge 1000 nm (BYU, depuis 1999) des surfaces exposées, binarisées en masques d'encre puis recalées sur le surface volume (§2.1, §4.1.3, Fig. 4) : labels issus d'une autre modalité, ni manuels sur le CT ni pseudo-labels.
- **Entraînement** : validation croisée à 8 plis (4 surfaces de fragments coupées en moitié haute/basse, 8 modèles, 7 régions d'entraînement chacun, 1 région tenue à l'écart) pour la Fig. 1b ; pour la Fig. 1c (couches cachées), un seul modèle entraîné sur les 4 surfaces (§2.1). Architecture, perte, optimiseur : n/r (Annexe A non disponible dans le texte) ; 620 000 batches d'entraînement (Table 1).

## Plateforme et implémentation

- **Sources de scan** (§4.1.1, Table 3) : synchrotron monochromatique (54 keV et 88 keV pour les fragments Paris 1 et 2 ; Diamond Light Source, remerciements) et source de laboratoire polychromatique (22 à 70 kV pour Objet 59, Cass. 110, rouleaux P.Herc.Paris. 4, 803, 804). Résolution de 2,23 à 23,9 µm, les plus prometteuses entre 3,24 et 7,91 µm (§4.1.1). Les colonnes de voxel par scan de la Table 3 sont perdues à l'extraction.
- **Objets** : 16 scans de 6 fragments issus de 4 rouleaux, et 9 scans de rouleaux intacts (4 rouleaux) ; l'évaluation du papier porte sur 4 fragments : P.Herc.Paris. 1 fr. 34 et fr. 39, P.Herc.Paris. 2 fr. 47 et fr. 143 (§2, §4.1.2).
- **Données** : plus de 11 To (11,5 To) au total, 55,8 Go pour les seuls surface volumes utilisés ici (§4.2). Licence CC BY-NC 4.0 ; un sous-ensemble est déjà diffusé via Vesuvius Challenge (scrollprize.org) (§4.3). Code : « open source » affirmé en conclusion, sans lien donné dans le texte lu ; Volume Cartographer cité.
- **Matériel de calcul et temps** : cluster Lipscomb de l'université du Kentucky (remerciements) ; GPU, temps : n/r. Puissance, FPGA : sans objet.

## Résultats

- **Éval. sur région tenue à l'écart** : oui (CV à 8 plis, moitiés de fragments) pour les surfaces ; pour les couches cachées, pas de vérité terrain (§2.1).
- **Visuel** (§2.2.1) : lignes de texte bien localisées, rappel de caractères d'environ 50 % (estimation visuelle des auteurs), pas de faux positifs notables.
- **Pixel** (Table 1, 4 fragments agrégés, µ et σ calculés sur la seconde moitié des 620 000 batches) : entropie croisée binaire, précision, rappel, FPR, Dice/F1, F0.5. Les valeurs µ sont perdues à l'extraction (corps de tableau absent) ; seul le texte donne que le rappel dépasse le FPR d'un facteur 8 (§2.2.2).
- **Caractères, papyrologue** (§2.2.3) : sur fr. 34, 7 des 15 caractères de la vérité terrain sont récupérés, aucun caractère erroné ou inventé (Fig. 3) ; Table 2 (4 fragments, rappel/FPR en caractères) : valeurs illisibles ; le texte dit que le rappel dépasse le FPR d'au moins un facteur 2 partout sauf pour P.Herc.Paris. 2 fr. 47. Notation « stricte » (caractères incertains comptés).
- **Couches cachées** (Fig. 1c) : texte grec lisible par endroits sur les couches sous-jacentes des fragments (« premier texte caché récupéré de façon non invasive ») ; aucune vérité terrain, cohérence d'échelle et d'interlignes avec la surface comme seul argument.
- Baseline de comparaison : aucune (« nouvelle tâche », §2.2.2).
→ reportés dans `benchmarks.csv` : 2 lignes (rappel de caractères fr. 34, §2.2.3, medium ; rappel visuel ≈50 %, §2.2.1, low). Les Tables 1 et 2 ne sont pas utilisables.

## Limites et critique

- Échantillon minuscule : 4 fragments, 15 caractères de vérité terrain pour fr. 34 ; rappel annoncé comme fort alors qu'au plus la moitié des caractères sont récupérés.
- Auto-évaluation sur des fragments détachés : pas de test sur un rouleau intact ni sur un rouleau/scanner tenu à l'écart ; les moitiés haut/bas d'une même surface sont voisines, avec risque de fuite d'information entre plis (déduit).
- Les moitiés d'un même fragment peuvent partager papyrus, encre et scribe : la généralisation aux rouleaux (autre encre, autre compression) n'est pas démontrée (déduit).
- Texte caché sans vérité terrain : la lisibilité repose sur l'argument d'échelle et sur des transcriptions d'un seul papyrologue pour l'évaluation ; pas d'étude placebo ni de lecture inversée.
- Les Tables 1 et 2 sont illisibles ici : impossible de citer précision, rappel, F0.5. Annexe A (architecture, hyperparamètres) absente du texte. Prétention de « premier » et d'« absence d'hallucination » à relativiser (affirmation des auteurs, non vérifiée).
- Preprint non relu par les pairs ; voxel size par scan inconnu faute de colonnes.

## Pertinence pour le thème

Article fondateur pour le projet : formalise la chaîne segmentation, aplatissement, rendu, détection d'encre ; fixe le protocole de labels (IR recalé sur le surface volume) et le dataset origine des scans du Vesuvius Challenge. Donne l'argument que le signal d'encre est de nature morphologique/texture et que la résolution doit approcher 5-10 µm (§4.1.1) : directement lié à la question « quelle part du signal survit à 8-9 µm ». Introduit F0.5 et le critère « pas d'hallucination » (axe validation-fp) et la validation par papyrologue (axe papyrology). Ne traite ni la super-résolution, ni l'auto-supervisé, ni le transfert entre scans.

## Gaps identifiés

- Comparaison chiffrée ink-ID vs approches 2D/3D ultérieures sur un même protocole ; pas de baseline.
- Évaluation sur rouleau ou scanner tenu à l'écart (transfert synchrotron ↔ labo) non faite.
- Validation de texte caché sans vérité terrain : pas de test placebo ni de calibration.
- Effet de la résolution (2,2 à 24 µm) et de l'énergie sur l'encre : affirmé qualitativement, non mesuré.

## Statut de lecture

papier complet (fulltext.md lu en entier). Avertissement d'extraction : backend `pymupdf` et `extraction.ok: false` : le texte peut être incomplet. Tables 1, 2 et 3 : corps manquants ou en désordre (valeurs µ, σ, rappels, voxels par scan perdus) ; Annexe A absente.
Ce qui suit est déduit et non affirmé par les auteurs : risque de fuite entre plis de CV, généralisation limitée aux rouleaux, nature « texture/morphologie » (les auteurs disent « likely »).
