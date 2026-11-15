---
id: 2026-korotetskyi-volumetric-texture-analysis-unsupervised-ink
fiche: done
date: 2026-11-15
---

# Volumetric Texture Analysis for Unsupervised Ink Detection in Herculaneum Papyri

Oleksandr Korotetskyi, Michal Haindl, 2026, Zenodo (CERN European Organization for Nuclear Research). https://doi.org/10.5281/zenodo.20766168
Type : rapport déposé sur Zenodo (`type: report`) ; aucune relecture par les pairs n'est indiquée dans le texte.

## Problème

L'encre carbonée des papyrus d'Herculanum a presque la même atténuation X que le substrat carbonisé : elle laisse peu de contraste dans le volume micro-CT (Abstract, §1). Les lecteurs d'encre de pointe sont des réseaux supervisés, opaques, dépendants de labels coûteux (IR), à lisibilité inégale selon les lettres et pas encore étendus des régions rognées aux rouleaux entiers (§1). Les auteurs demandent si des descripteurs de texture classiques, étendus en 3-D, restent utiles comme signal d'encre déterministe, explicable et sans entraînement (§1).

## Méthode

Entrée : pile aplatie de 65 couches de profondeur (8 bits, 4771×7414 px) du segment 20241108120732 de Scroll 5 (PHerc. 172), produite par Thaumato Anakalyptor ; l'axe de profondeur est une coordonnée normale à la feuille, pas un z physique (§3). Chaîne sans paramètre appris (§4, Fig. 8) :
- trois descripteurs volumiques : autocorrélation par blocs ACF3D (b = 2), énergie du premier ordre FOS3D (fenêtre w = 5), énergie de Laws LTE3D-LL (k = 7) (§4.4) ;
- fusion par moyenne par voxel après normalisation min-max (§4.6) ;
- a priori de profondeur ancré sur le pic (gaussienne σ = 15 tronquée aux minima locaux de la courbe de moyenne par couche) (§4.3), puis projection 2-D par maximum par colonne ;
- lissage MRF gaussien doux (10 itérations ICM, β = 2,5), seuil adaptatif par spécimen Ts = µ + 0,5 σ après retrait des 1 % d'anomalies par un filtre RX (§4.5, §4.6).

## Plateforme et implémentation

Matériel, temps de calcul et mémoire : n/r. Données : EduceLab-Scrolls / Vesuvius Challenge, Scroll 5 (PHerc. 172), licence CC BY-NC 4.0 ; résolution µm/voxel et énergie du scan : n/r dans le texte (§3). Code et archives par spécimen publiés : https://github.com/korotole/vtfid et https://doi.org/10.5281/zenodo.20766169 (§15). Les auteurs déclarent avoir utilisé des LLM (Claude) pour la traduction, le LaTeX et la revue de code (§14).

## Résultats

Évaluation sur 25 recadrages de 512×512 px d'une lettre grecque chacun (Scroll 5), contre des masques de référence issus de la prédiction supervisée de la communauté (pas des traces manuelles de lettres, §7). Bande d'exclusion δ = 4 px autour des contours ; métrique : MCC par pixel (§5.1). Aucune séparation train/val/test, pas de paramètre appris (§3).
- Séparabilité par couche : pic en couche 31, d′ = 0,42, OL1 = 0,79, écart de moyenne 11,4 niveaux de gris ; aux bords, écart 1,9 (couche 0) et 0,6 (couche 64), OL1 > 0,96 (§4.1, Table 1).
- MCC moyen / médian (Table 2) : FOS3D +0,351 / +0,377 ; LTE3D-LL +0,361 / +0,383 ; ACF3D (b = 2) +0,374 / +0,392 ; fusion +0,364 / +0,386. Meilleur spécimen : 7-η (ACF3D +0,533) ; fusion +0,523 sur 17-η ; pire : 6-β (+0,155 à +0,159). MCC positif sur chaque spécimen (Abstract). ACF3D seul bat légèrement la fusion (§5.2).
- Sensibilité à δ, MCC moyen de la fusion (Table 3, corps de tableau mal découpé à l'extraction, lecture à vérifier ; recoupée avec le texte §5.3 : « ~0,02 de moins sans bande, ~0,03 de plus à 12 px ») : δ = 0 : 0,3421 ; 2 : 0,3537 ; 4 : 0,3643 ; 8 : 0,3813 ; 12 : 0,3926.
- Plein segment (§6, Fig. 10-12) : avec l'a priori désactivé et trois bandes de profondeur, ACF3D fait apparaître un fragment de texte partiellement lisible dans la bande peu profonde (ℓ ∈ [0, 21], zone 3573×736 px) ; les lettres correspondent à la prédiction communautaire du segment voisin 20241108111522, qui recouvre le segment analysé en (x, y) mais à une autre profondeur. Résultat qualitatif, sans mesure.
- Hors Scroll 5 : sur Scroll 1 (PHerc. Paris 4), la chaîne ne donne rien de comparable (fragments aux bords encre/papyrus), traité comme résultat négatif (§7, §8) ; aucun chiffre.
→ reportés dans `benchmarks.csv` : 8 lignes (MCC moyen : 4 opérateurs à δ = 4 ; fusion à δ = 0, 2, 8, 12).

## Limites et critique

- Cible : les masques de référence sont des prédictions de réseau supervisé, pas des vérités terrain manuelles ; le MCC mesure l'accord avec ce réseau, non la présence réelle d'encre. Les auteurs le reconnaissent (§5.3, §7) ; un contour de lettre peut même recouvrir un vide du papyrus (16-ρ).
- Le MCC monte avec δ (0,342 à 0,393 de δ = 0 à 12) : le choix a priori δ = 4 influe sur le chiffre phare, et les valeurs ne se comparent pas à un MCC sans bande ou à une autre bande (§5.3).
- Évaluation sur 25 petits recadrages monolettre choisis et localisés à la main, étiquetés « approximatifs » (§3) ; le prior de profondeur est calibré sur ces recadrages et perd son ancrage sur un segment entier (§6). Pas d'évaluation de segment entier ni de métrique sur les faux positifs hors lettre ; la projection 2-D sous-estime l'évidence volumique (§7).
- Les descripteurs répondent aussi aux fibres du papyrus ; la séparation encre/fibre est laissée en travail futur (§8). Pires résultats sur substrat déformé.
- Généralité non établie : Scroll 5 fonctionne, Scroll 1 échoue (§7, §8). Le texte dit « plusieurs segments de Scroll 5 » sans chiffres pour les autres segments.
- Aucune comparaison quantitative à un baseline supervisé ou à un seuil d'intensité brute (au-delà de la Table 1 : d′ et OL1 de la prédiction communautaire) ; les auteurs disent ne pas viser la performance absolue (§7). Un MCC de 0,37 est modeste (déduit).
- Seuil Ts : k = 0,5 choisi pour que la part de pixels acceptés (22-28 %) colle à la couverture d'encre observée (0,27 ± 0,07) dans les mêmes recadrages (§4.5) : réglage fait avec une information issue de la référence.
- Matériel, temps de calcul, résolution du scan : n/r.

## Pertinence pour le projet Elder-scrolls

Axe `ink-detection` : apporte une réponse « texture/morphologie » à la question de recherche sur le signal exploité sans contraste d'absorption : l'autocorrélation 3-D à lag z = 1 (continuité inter-couches d'un trait) est le meilleur descripteur, et le contraste d'encre se concentre dans une bande étroite de couches autour de la surface (d′ > 0,3 pour ℓ ∈ [27, 32], §4.1) : utile pour dimensionner la profondeur d'entrée d'un modèle (déduit). Axe `label-efficiency` : carte d'évidence sans entraînement pouvant servir d'entrée auxiliaire ou de faible label pour un lecteur supervisé (proposition des auteurs, non testée). Le résultat sur le segment voisin rappelle le risque de superposition de feuilles dans un segment aplati. Reste ouvert : survie du signal à 8-9 µm vs 2,4 µm, validation indépendante de la lettre, transfert entre rouleaux (échec sur Scroll 1).

## Gaps identifiés

- Détection d'encre sans entraînement : aucune évaluation contre une vérité terrain indépendante d'un réseau (IR, traces manuelles).
- Transfert entre rouleaux d'une méthode déterministe : Scroll 5 réussit, Scroll 1 échoue, cause non analysée (résolution, énergie du scan, type d'encre ?).
- Séparation encre/fibre dans les descripteurs volumiques, et combinaison de ces cartes avec un lecteur supervisé (entrée ou faible label) : proposée, non mesurée.

## Statut de lecture

Papier complet : `fulltext.md` lu en entier. `extraction.backend` = `pymupdf` et `extraction.ok` = false : texte potentiellement mal découpé ; les Tables 1-3 sont aplaties (lignes fusionnées, en-têtes dissociés). Les valeurs de la Table 3 viennent d'un corps sans en-tête de colonne, recoupées avec §5.3 et la valeur de δ = 4 (0,3643, §5.2). Aucun `chunks.jsonl` disponible : `chunk_id` à `n/r`.
Ce qui suit est déduit et non affirmé par les auteurs : le MCC de 0,37 est modeste ; le réglage de k = 0,5 s'appuie sur la référence ; l'intérêt pour la profondeur d'entrée d'un modèle supervisé ; l'attribution des colonnes moyenne/médiane de la Table 3 (paires dans cet ordre).
