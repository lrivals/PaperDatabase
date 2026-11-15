---
id: 2026-korotetskyi-volumetric-texture-analysis-unsupervised-ink
fiche: done
date: 2026-11-15
---

# Volumetric Texture Analysis for Unsupervised Ink Detection in Herculaneum Papyri

Oleksandr Korotetskyi, Michal Haindl, 2026, Zenodo (CERN European Organization for Nuclear Research). https://doi.org/10.5281/zenodo.20766168
Type : **rapport Zenodo non relu par les pairs** (pas de venue à comité de lecture ; à traiter comme un preprint).

## Problème

Les encres carbonées d'Herculanum sont quasi iso-atténuantes avec le papyrus carbonisé en micro-CT. Les lecteurs d'encre de l'état de l'art sont des réseaux supervisés, opaques, dépendants de labels coûteux et réglés sur des régions rognées (Abstract, §1). Les auteurs cherchent une alternative déterministe, sans entraînement, explicable, qui traite la dalle de profondeur dépliée comme un vrai signal 3D et puisse fournir une carte d'évidence ou des pseudo-labels aux détecteurs supervisés (§1, §7).

## Méthode

- Entrée : pile de 65 couches de profondeur 8 bits (4771×7414 px) du segment 20241108120732 de Scroll 5 (PHerc. 172), produite par Thaumato Anakalyptor ; l'axe de profondeur est une coordonnée normale à la feuille, pas un z physique (§3).
- Trois descripteurs de texture classiques portés en 3D : statistiques d'ordre 1 (FOS3D, fenêtre w=5), énergie de Laws L⊗L⊗L (LTE3D LL, k=7), autocorrélation par blocs (ACF3D, b=2) (§4.4). Fusion par moyenne par voxel après normalisation min-max (§4.6).
- A priori de profondeur ancré sur un pic : centre = argmax de (moyenne de couche × cohérence spatiale), support borné par les minima locaux de la courbe de moyenne, enveloppe gaussienne σ=15 (§4.3, Algorithme 1).
- Projection 2D par maximum de la réponse pondérée en profondeur, lissage MRF gaussien (10 itérations ICM, β=2,5), seuil adaptatif Ts = µ + 0,5σ après retrait des 1 % de valeurs RX extrêmes (§4.5, §4.6).
- Aucun paramètre entraîné : pas de découpage train/val/test, tout le jeu sert à l'évaluation (§3). Les hyperparamètres (k=0,5 du seuil, σ, δ) sont choisis a priori ou calibrés sur ces mêmes 25 vignettes (§4.5, §6).
- Labels d'évaluation : prédiction d'encre communautaire d'un réseau supervisé (pas des traces manuelles) rééchantillonnée sur la grille des couches ; 25 vignettes 512×512 d'une lettre grecque chacune, localisées à la main, lettre « approximative » (§3, §7).

## Plateforme et implémentation

- Source du scan : EduceLab-Scrolls / Vesuvius Challenge, Scroll 5 (PHerc. 172), segment 20241108120732 (CC BY-NC 4.0) (§3). Énergie (keV) et résolution µm/voxel : n/r dans le papier. Tuilage Thaumato en cellules de 500³ voxels (§3).
- Objet : rouleau complet Scroll 5 ; le segment voisin 20241108111522 sert à la comparaison qualitative (§6, Fig. 12). Scroll 1 (PHerc. Paris 4) testé aussi, résultat négatif, sans chiffres (§7, §8).
- Matériel et temps de calcul : n/r.
- Code et données : scripts, configurations et archives par spécimen publiés, https://github.com/korotole/vtfid et https://doi.org/10.5281/zenodo.20766169 (§15). Données de scan publiques (https://scrollprize.org/data).

## Résultats

Données d'évaluation : 25 vignettes de lettres de Scroll 5, **non tenues à l'écart** (aucun entraînement, mais calibrage sur ces vignettes) ; vérité terrain = prédiction d'un réseau supervisé, bande d'exclusion de δ=4 px autour du contour (§5.1).

| Variante | MCC moyen | MCC médian | Source |
|---|---|---|---|
| FOS3D (w=5) | +0,351 | +0,377 | Table 2 |
| LTE3D LL (k=7) | +0,361 | +0,383 | Table 2 |
| ACF3D (b=2) | +0,374 | +0,392 | Table 2, §5.2 |
| Fusion des trois | +0,364 | +0,386 | Table 2, §5.2 |

- Meilleure lettre : 17-η (fusion +0,523) ; ACF3D +0,533 sur 7-η ; pire : 6-β (≈ +0,16) (Table 2). MCC strictement positif sur toutes les lettres (Abstract).
- ACF3D bat la fusion sur 16/25 spécimens (§5.2).
- Sensibilité à δ (fusion, moyenne) : 0 px +0,342 ; 2 px +0,354 ; 4 px +0,364 ; 8 px +0,381 ; 12 px +0,393 (Table 3 ; association valeurs-δ lue dans l'ordre de la table extraite).
- Séparabilité ink/papyrus par couche : d′ max 0,42 (couche 31), recouvrement OL1 = 0,79 ; au bord de la dalle d′ s'effondre et OL1 > 0,96 (§4.1, Table 1).
- Qualitatif : sur le segment entier (trois bandes de profondeur, ACF3D), apparition d'un texte partiellement reconnaissable correspondant à la prédiction communautaire du segment voisin 20241108111522 qui se recouvre en volume (§6, Fig. 12). Pas de métrique associée.
- Scroll 1 : résultat négatif déclaré, sans chiffres (§7).
→ reportés dans `benchmarks.csv` : 6 lignes (4 variantes à δ=4, plus fusion à δ=0 et δ=12), proposées dans le fichier bench ; l'agent principal les intègre.

## Limites et critique

- Rapport non relu par les pairs, un seul rouleau pour le chiffrage (Scroll 5, un seul segment), négatif sur Scroll 1 (§7, §8).
- Évaluation circulaire : la « vérité terrain » est la sortie d'un réseau supervisé, pas des labels humains ; les auteurs notent que ce réseau ajuste des formes canoniques de lettres, et qu'il recouvre parfois du vide (16-ρ) (§7). Le MCC mesure donc l'accord avec un autre détecteur, pas avec l'encre réelle.
- Pas de séparation calibrage/test : les 25 vignettes servent aussi à fixer k, δ, σ ; la bande δ gonfle le score (+0,03 entre δ=4 et 12 ; Table 3). Pas d'intervalle de confiance ni de test de significance.
- Pas de baseline comparative (ni supervisé, ni z-moyenne brute en MCC, ni texture 2D) : on ne sait pas ce que la 3D apporte. Le papier ne compare pas à un lecteur supervisé (déduit : MCC ≈ 0,37 est modeste).
- Vignettes recadrées autour de lettres déjà connues par la prédiction communautaire : la détection n'est pas évaluée à l'aveugle ni sur des zones sans encre ; aucune mesure de faux positifs sur le segment entier. La projection par max mélange fibres, anomalies et encre (§7 ; les descripteurs répondent aussi aux fibres, §8).
- Le texte « révélé » dans le segment voisin est qualitatif et peut venir d'un recouvrement de feuilles, non d'un gain de détection ; nombre de segments testés pour Scroll 5/1 non précisé (§8).
- Reproductibilité : code et archives publiés (§15), points positifs.

## Pertinence pour la thèse

Thème : détection d'encre sans contraste d'absorption. Apporte (1) un signal d'encre sans labels : candidat de pseudo-label ou d'entrée supplémentaire pour un lecteur supervisé (label-efficiency) ; (2) une quantification utile de la concentration du signal sur quelques couches centrales (d′ max 0,42, §4.1), qui informe le choix de la fenêtre de profondeur ; (3) un exemple de faux positif/vrai positif ambigu : une réponse détectée sur un segment qui appartient à une feuille voisine (§6), pertinent pour la validation et les artefacts de recouvrement entre segments. Laisse ouvert : résolution et énergie non données, performance absolue faible, aucune évaluation sur zone hors rouleau, échec sur Paris 4 (Scroll 1).

## Gaps identifiés

- Descripteurs 3D de texture comparés à un lecteur supervisé sur les mêmes lettres, avec labels humains plutôt que la prédiction d'un réseau.
- Transfert entre rouleaux : échec sur Scroll 1, non analysé.
- Utilisation de la carte texture comme pseudo-label ou canal d'entrée d'un réseau supervisé : proposée, non testée (§8).
- Séparation encre/fibres et détection des recouvrements entre segments comme source de faux positifs.

## Statut de lecture

Papier complet (`fulltext.md` lu en entier). Extraction PyMuPDF (`extraction.ok: false`) : texte correct pour l'essentiel, quelques ligatures non réparées (« classi cation ») ; tableaux reconstruits sans mise en forme fiable, la Table 3 a perdu les en-têtes de δ (association déduite de l'ordre {0, 2, 4, 8, 12} annoncé en §5.3, et cohérente avec δ=4 → +0,3643).
Déduit et non affirmé par les auteurs : jugement « MCC modeste », absence de baseline comparative, calibrage sur les mêmes vignettes pour les hyperparamètres (seule la valeur de k est explicitement « choisie », §4.5), circularité de la vérité terrain.
