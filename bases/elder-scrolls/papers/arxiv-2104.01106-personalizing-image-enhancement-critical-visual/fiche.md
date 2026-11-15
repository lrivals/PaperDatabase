---
id: arxiv-2104.01106-personalizing-image-enhancement-critical-visual
fiche: done
date: 2026-11-15
benchmarks: none
---

# Personalizing image enhancement for critical visual tasks: improved legibility of papyri using color processing and visual illusions

Vlad Atanasiu, Isabelle Marthot-Santaniello, 2021, International Journal on Document Analysis and Recognition (IJDAR), 2021 (accepté le 2021.08.28 ; la venue est écrite « nternational… » dans `metadata.json`, à cause de l'extraction). https://doi.org/10.1007/s10032-021-00386-0 ; arXiv 2104.01106.
Type : article de revue (IJDAR) ; version arXiv lue, à comparer à la version publiée avant de citer des chiffres.

## Problème

Améliorer la lisibilité de papyrus photographiés en lumière visible, pour l'édition savante de textes (papyrologie). Les auteurs posent la « vision critique » : tâche à fortes conséquences d'erreur et observateur sceptique, où le signal est ambigu (§2.3). Verrou : peu de travaux sur le rehaussement en lumière visible, pas d'approche systémique, incertitude jamais explicitée (Introduction, §3.2). Aucun volume 3D, aucun scan X.

## Méthode

Entrées : images RGB de papyrus (photographie couleur ou monochrome). Aucun label, aucun entraînement : traitements couleur pixel à pixel dans CIELAB, sans apprentissage (§4). Méthodes proposées :
- expansion de gamut sRGB → Adobe RGB (1998) par changement de profil ICC (§4.2) ;
- étirement de la lightness `stretchlim` (§4.3) ;
- polarité négative L*' = 100 − L* (§4.4) ;
- `vividness` : L*' = norme l2 de (L*, a*, b*), selon le modèle « l'encre réduit lightness et chroma » (§4.5) ;
- `lsv` : fusion de L* avec la différence saturation/valeur HSV pour atténuer le fond (§4.6) ;
- décalage vers le bleu (inversion de a* et b*, §4.7) ;
- retinex multi-échelle (MSRCR) dans CIELAB (§4.8) ;
- colorisation inter-spectrale : image IR ou non-VIS insérée dans L*, chroma du visible conservé (§4.9).
Comparées à `stretchlim`, `histeq`, `adapthisteq`, `locallapfilt`, `retinex` (ImageJ) (§5.1). Le décalage de teinte et le retinex CIELAB ne sont pas dans l'expérience. Les autres chaînes de traitement sont intégrées dans l'Algorithme 1 (§4.10).
Évaluation : expérience utilisateur, huit étudiants et enseignants en papyrologie (« homework », pas de laboratoire), notes X/A/B/N d'utilité et classement, sur 9 papyrus DIBCO 2019 × 10 méthodes = 90 images (§5.1). Agrégation par Centroids, Majority Judgment, ROD ; concordance par W de Kendall (§5.3).

## Plateforme et implémentation

- Source de l'imagerie : photographies en lumière visible de papyrus (bibliothèques de Columbia, Michigan, Yale, Oxford/EES, Istituto Papirologico Vitelli). Ensemble d'entraînement : 8 images de papyrus de la bibliothèque de Fribourg (non publiés). Pas de synchrotron, pas de micro-CT, pas d'énergie keV. Résolution µm/voxel : n/r.
- Objets : papyrus ouverts (non carbonisés), recto/verso. Les images multispectrales (§4.9) servent seulement d'illustration qualitative.
- Matériel de calcul et temps : Matlab R2020b (ImageJ pour retinex) ; temps de calcul n/r (méthodes pixel à pixel).
- Code : logiciel libre Hierax, cité [16] dans le papier ; lien n/r dans le texte lu (renvoi bibliographique seulement). Le code des méthodes de classement est publié en [15]. Le jeu d'images évalué est dans le matériel supplémentaire en ligne.
- Données d'évaluation : les 9 images DIBCO 2019 ne sont pas tenues à l'écart d'un entraînement (aucun apprentissage). Vérité terrain : jugements subjectifs des 8 utilisateurs, pas de transcription de référence ni de masque d'encre (§5.1, « Frame »).

## Résultats

Tous les résultats sont des préférences d'utilisateurs, pas des métriques de lisibilité ou de détection.
- Les méthodes proposées sont en tête : majoritairement d'usage primaire, alors que les méthodes de comparaison sont surtout « sans usage » (Table 2). Top 1 `vividness`, puis `negative` ; derniers `locallapfilt` et `histeq` (§5.3.3, Table 3). Les valeurs numériques de ces tableaux sont illisibles dans le texte extrait (colonnes mélangées) : non reprises ici.
- 42 % des évaluations (n = 720) jugées « sans usage » (§5.3.4, Table 2).
- L'image originale est classée la plus fiable pour la transcription (§5.3.9) ; 3 participants sur 8 préfèrent l'original à une version améliorée (Introduction).
- Accord de Kendall W : 0,376 entre utilisateurs, 0,698 entre documents (Table 5A). Selon les auteurs, l'hétérogénéité des utilisateurs domine, d'où l'intérêt de laisser le choix de la méthode (§5.3.5, §5.3.6). La significativité est testée à α = 0,1 (p = 0,001 et p = 6,1e−9), seuil laxiste (§5.3.5).
- `retinex` révèle le mieux l'écriture mais accentue la texture du papyrus et provoque un vignettage ; `vividness` est le plus équilibré, `lsv` lisse mais abîme parfois les traits (§5.3.2, jugement qualitatif des auteurs).
→ reportés dans `benchmarks.csv` : aucune ligne (`benchmarks: none`). Pas de performance chiffrée sur une tâche : seulement des notes d'utilité subjectives de 8 personnes, non comparables à des métriques d'encre ou de segmentation.

## Limites et critique

- Échantillon minuscule (8 participants, 9 papyrus), noms de méthodes non anonymisés (choix assumé, §5.1), pas de mesure d'erreur de transcription ni de durée : la « meilleure » méthode est celle jugée utile, pas celle qui est démontrée plus exacte.
- Les comparaisons de base sont des filtres classiques (histeq, CLAHE, retinex) ; aucune comparaison à du ML ou à une binarisation. Les auteurs soulignent que l'ML est rare en rehaussement historique (§3.2) sans le tester.
- Tout porte sur la lumière visible, 2D. Le papier lui-même indique que l'imagerie multispectrale donne en général une meilleure lisibilité et que des méthodes supplémentaires sont indispensables pour les papyrus carbonisés (§5.3.4). Aucune expérience sur le contraste de phase ou l'absorption X.
- Les résultats sont ceux de lecteurs humains sur des papyrus lisibles : aucun transfert établi vers la détection d'encre CT, où l'encre carbonée n'a pas de contraste d'absorption.
- Point utile : la polarité négative aide à décider si une trace est de l'encre ou un trou (§5.3.10) ; l'idée de rendre l'incertitude explicite (alternatives plutôt qu'une carte unique, §6.1) est transposable. Les auteurs notent que les réseaux de neurones peuvent halluciner des formes de caractères (§6.1, citation [21]).
- Code : Hierax cité, mais le dépôt n'est pas lisible dans le texte lu. Reproductibilité des images : le matériel supplémentaire est en ligne, non vérifié.

## Pertinence pour la thèse

Pertinence faible pour le cœur du projet (CT, segmentation, encre). Aucune méthode du papier ne s'applique directement aux volumes micro-CT. Deux apports indirects : (1) cadre « vision critique » et explicitation de l'incertitude, utile pour la partie validation/faux positifs (lecture inversée, présentation de plusieurs rendus plutôt qu'un seul) ; (2) retour d'expérience sur la visualisation de papyrus par des papyrologues (négatif, comparaison côte à côte, flicker), utile pour rendre les cartes d'encre aux papyrologues. Laisse ouvert : toute application aux cartes d'encre ou à des rendus tifxyz.

## Gaps identifiés

- Pas d'étude utilisateur papyrologues sur des rendus d'encre CT (négatif, couleur, incertitude affichée).
- Aucune mesure d'effet des rehaussements visuels sur le taux d'erreur de lecture des lettres.

## Statut de lecture

papier complet (`fulltext.md` lu en entier ; extraction `pymupdf`, `extraction.ok` à `false` : le texte est lisible mais les Tables 1 à 5 sont désordonnées, leurs valeurs ne sont pas reprises, sauf celles redonnées dans le texte).
Ce qui suit est déduit et non affirmé par les auteurs : jugement de faible pertinence pour le CT ; le lien avec la validation d'encre ; l'absence de lien de dépôt Hierax (seule la citation [16] est dans le texte).
