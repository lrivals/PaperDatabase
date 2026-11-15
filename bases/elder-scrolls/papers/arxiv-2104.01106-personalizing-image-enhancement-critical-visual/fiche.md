---
id: arxiv-2104.01106-personalizing-image-enhancement-critical-visual
fiche: done
date: 2026-11-15
benchmarks: none
---

# Personalizing image enhancement for critical visual tasks: improved legibility of papyri using color processing and visual illusions

Vlad Atanasiu, Isabelle Marthot-Santaniello, 2021, nternational Journal on Document Analysis and Recognition (IJDAR) (2021) (venue tel que dans `metadata.json`, la première lettre est perdue à l'extraction ; il s'agit d'IJDAR). https://doi.org/10.1007/s10032-021-00386-0 (arXiv 2104.01106)
Type : article de journal (accepté par IJDAR le 28/08/2021 d'après la note de bas de page de l'Introduction ; version arXiv lue). Le champ `type` de `metadata.json` reste `null` (hors périmètre d'écriture).

## Problème

Améliorer la lisibilité de papyrus photographiés en lumière visible, pour l'édition savante de textes (§1, §2). Les auteurs posent la tâche comme une « vision critique » : tâche à fort enjeu, observateur sceptique, signal ambigu, où aucune structure d'image n'est du bruit et où l'incertitude doit rester visible (§2.3, §6). Ils notent que la texture du papyrus (fibres) et l'écriture sont proches en fréquence spatiale (§2.2) et que l'apprentissage automatique reste rare sur documents historiques (données rares, vérité terrain coûteuse, risque que des réseaux « hallucinent » des formes de caractères ; §3.2, §6.1).

## Méthode

Méthodes de traitement de la couleur, volontairement simples (§4), toutes dans CIELAB :
- expansion du gamut (sRGB vers Adobe RGB 1998 par profils ICC, sans modifier les valeurs numériques ; §4.2) ;
- étirement de la luminosité `stretchlim` (§4.3) ;
- polarité négative L*' = 100 - L* (§4.4) ;
- `vividness` : L*' = norme l2 de (L*, a*, b*) (§4.5) ;
- `lsv` : différence saturation/valeur HSV fusionnée avec L* (§4.6) ;
- décalage de teinte vers le bleu, ou simple changement de signe de a*, b* (§4.7) ;
- retinex multi-échelle dans CIELAB (MSRCR ; écarts-types gaussiens 15, 80, 250 ; §4.8) ;
- colorisation inter-spectrale : image non visible (IR) insérée dans le canal L*, chrominance de l'image visible conservée (§4.9, Fig. 15) ;
- enchaînement dans l'Algorithme 1 (§4.10).

Évaluation par expérience utilisateur (§5) : 8 participants (7 étudiants et 1 enseignant en papyrologie, formés au grec ancien), 9 images de papyrus couleur du jeu ICDAR 2019 DIBCO, chacune traitée par 10 méthodes (90 images ; §5.1). Quatre méthodes nouvelles (vividness, lsv, negvividness, neglsv) contre cinq méthodes de comparaison (stretchlim, histeq, adapthisteq/CLAHE, locallapfilt, retinex ImageJ). Luminosité normalisée et gamut élargi avant comparaison. Tâches : notation d'utilité (X/A/B/N) et classement, à distance, noms de fichiers non anonymisés (§5.1). Agrégation par Centroids, Majority Judgment et ROD, plus coefficient de concordance W de Kendall et planéité spectrale (§5.3).

## Plateforme et implémentation

Matlab R2020b ; retinex produit avec ImageJ (§5.1). Traitement pixel à pixel, aucun GPU, aucun scanner : images en lumière visible du jeu DIBCO 2019, aucune CT. Logiciel libre Hierax (réf. [16]), qui offre les méthodes nouvelles, adapthisteq et retinex, avec mosaïque, diptyque à zoom/pan synchronisés et bascule rapide (flicker) (§7) ; utilisé pour 70 papyrus de la bibliothèque de l'Université de Bâle (§7). Données d'évaluation : matériel supplémentaire en ligne de l'article (§1). Code des méthodes de classement publié (réf. [15], §5.3.3). Les liens exacts sont dans la bibliographie, non vérifiés ici.

## Résultats

Résultats de préférence d'utilisateurs, pas de métrique de modèle :
- Les méthodes proposées sont surtout d'« usage primaire », les méthodes de comparaison surtout « sans usage » (§5.3.1, Table 2 ; chiffres de la Table 2 absents du texte extrait).
- Classement agrégé : vividness en tête, puis la méthode négative ; locallapfilt et histeq en dernier (§5.3.3, Table 3). Les valeurs de la Table 3 sont mélangées dans l'extraction : non reprises.
- Méthodes jugées « sans usage » dans 42 % des n = 720 cas (§5.3.4, Table 2).
- Accord de Kendall W : entre utilisateurs 0,376, entre documents 0,698 (Table 5A). Les auteurs en tirent qu'il faut investir dans l'interaction plus que dans les algorithmes (§5.3.6).
- L'image originale est classée la plus utile globalement (§5.3.9) ; la négative est top-2 derrière vividness (§5.3.10) ; aucune méthode ne convient à tous (§5.3.5).
- Un participant utilise l'image négative pour juger si une trace d'encre est réelle, et pour distinguer encre et trous (§5.3.10).

→ reportés dans `benchmarks.csv` : aucune ligne.
Aucune ligne justifiable : le papier ne rapporte ni précision, ni IoU, ni F-score, ni temps, ni résolution de scan ; seulement des préférences de 8 utilisateurs, dont les tableaux (Tables 1 à 3) sont illisibles ou incomplets dans l'extraction `pymupdf`. L'en-tête de `benchmarks.csv` ne s'y applique pas. D'où `benchmarks: none`.

## Limites et critique

- Échantillon minuscule (8 participants, 9 documents), hors laboratoire (matériel libre, « devoir à la maison ») et sans anonymisation des méthodes : l'image originale est reconnue et préférée par principe (§5.1, §5.3.9). Les auteurs l'assument comme réalisme écologique.
- Métrique subjective (utilité perçue), sans erreur de transcription ni temps de tâche ni vérité terrain de lecture (§5.1 « Frame »). L'évaluation porte sur une transcription hypothétique pour les 9 images.
- Participation comptée dans les notes du cours (§5.1) : biais possible de complaisance (déduit).
- Décalage de teinte et retinex CIELAB hors expérience (« late-breaking research », §5.1) ; colorisation inter-spectrale illustrée, non évaluée (Fig. 15).
- Lumière visible, papyrus non carbonisés. Les auteurs disent que pour les papyrus carbonisés les images multispectrales sont indispensables (§5.3.4) et que la polarité négative vaut aussi pour les images monochromes, comme celles des papyrus carbonisés (§5.3.10).
- Aucune comparaison à une méthode d'apprentissage (argument de principe seulement, §3.2).
- Lisibilité pour les machines (binarisation, OCR) non testée, laissée aux travaux futurs (§8).

## Pertinence pour la thèse

Pertinence pour Elder-scrolls : indirecte, axe `papyrology` (éventuellement `validation-fp` pour le cadre). Aucune méthode de CT, de segmentation ou de détection d'encre sur rouleaux scannés, aucun chiffre transposable à des scans à 8–9 µm. Apports :
- cadre pour « prouver qu'une lettre est réelle » : vision critique, garder toute structure comme information potentielle, rendre l'incertitude explicite par des alternatives visibles et une bascule entre rendus, avertissement sur les réseaux qui « hallucinent » des formes de caractères (§6.1) ;
- retour de lecteurs papyrologues : l'image négative sert à juger si une trace d'encre est réelle (§5.3.10), besoin de comparer plusieurs rendus côte à côte avec zoom/pan synchronisés (§5.3.11, §7) ; utile pour l'outillage de revue visuelle des cartes d'encre (rendus multiples, flicker) ;
- méthode d'évaluation par experts humains (classement agrégé, accord de Kendall) si l'équipe veut faire valider des lectures par des papyrologues.
Laissé ouvert : aucun lien avec le signal d'encre en CT ni avec la calibration des sorties de modèle ; la colorisation inter-spectrale (détail non visible dans L*, contexte visible dans la chrominance) n'est pas testée sur de la CT.

## Gaps identifiés

- Pas d'évaluation de ces rendus (négatif, flicker, alternatives) sur des cartes d'encre CT ni avec des lecteurs d'Herculanum.
- Pas de mesure objective de lisibilité (erreurs de transcription, temps) ; le papier choisit explicitement des préférences (§5.1).
- Effet de ces traitements sur des modèles automatiques non étudié (travaux futurs, §8).

## Statut de lecture

papier complet (`fulltext.md` lu en entier ; bibliographie non relue en détail).
Attention : `extraction.backend` vaut `pymupdf` et `extraction.ok` vaut `false` ; le texte peut être mal découpé. Les corps des Tables 1 à 5 sont absents ou en désordre (Table 1 : lignes entremêlées ; Table 2 : valeurs absentes ; Table 3 : colonnes mélangées) : seuls les chiffres donnés dans le texte (42 % de 720, W de la Table 5A) sont repris. `chunks.jsonl` n'existe pas encore pour ce papier : aucun `chunk_id`.
Ce qui suit est déduit et non affirmé par les auteurs : le biais de complaisance lié aux notes du cours ; la pertinence pour les cartes d'encre CT et le risque d'hallucination des rendus ; l'absence de lien entre colorisation inter-spectrale et CT.
