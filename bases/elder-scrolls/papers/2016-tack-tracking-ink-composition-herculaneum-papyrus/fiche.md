---
id: 2016-tack-tracking-ink-composition-herculaneum-papyrus
fiche: done
date: 2026-11-15
benchmarks: none
---

# Tracking ink composition on Herculaneum papyrus scrolls: quantification and speciation of lead by X-ray based techniques and Monte Carlo simulations

Pieter Tack, Marine Cotte, Stephen Bauters, Emmanuel Brun, Dipanjan Banerjee, Wim Bras, Claudio Ferrero, Daniel Delattre, Vito Mocella, Laszlo Vincze, 2016, Scientific Reports. https://doi.org/10.1038/srep20763
Type : article de journal (relu par les pairs)

## Problème

Le texte des rouleaux d'Herculanum, lu par tomographie à contraste de phase (Mocella et al.), est parfois difficile à lire à cause des fibres du papyrus ; Brun et al. (soumis, non lu ici) ont montré que le plomb (Pb) fait partie de l'encre et rend le texte plus lisible en fluorescence X (Introduction). Les auteurs cherchent l'origine et l'état chimique de ce Pb à partir de plusieurs hypothèses : contamination de l'eau ou d'un récipient en bronze, pigment (galène PbS, céruse, minium), ou siccatif (litharge PbO dans une encre à base lipidique) (Introduction).

## Méthode

Pas de modèle d'apprentissage : analyse physico-chimique non destructive. Entrées : deux fragments plats de rouleaux déroulés (« grand » 0,9 × 1,2 cm, « petit » 0,5 × 0,8 cm, épaisseur environ 0,3 mm), mesurés entre deux feuilles d'ultralene (Methods). Trois volets :
- cartographie XRF multi-échelle (macro : pas de 50 et 100 µm ; micro : 10, 5 et 1 µm, faisceau focalisé environ 0,3 × 0,6 µm²) ; pixels « encre » isolés par clustering K-means (Results, Methods) ;
- quantification par simulation Monte Carlo (XMI-MSIM) : ajustement itératif de la composition simulée sur le spectre expérimental, faisceau monochromatique 3,5 keV (Methods) ;
- spectroscopie XANES aux seuils Pb-L3, S-K et Cl-K, avec ajustement par combinaison linéaire de composés de référence (Results).
Labels / vérité terrain : aucun au sens apprentissage ; la comparaison porte sur des spectres de référence (acétate de plomb(II), PbS, minium de la littérature).

## Plateforme et implémentation

- Source : synchrotron ESRF (Grenoble) ; XRF sur la ligne ID21 (3,5 keV, Si(111), SDD Bruker XFlash 5100, sous vide), XAFS Pb-L3 sur DUBBLE BM26A (Methods). Énergie des seuils : Pb-L3 environ 13,035 keV, S-K environ 2,48 keV, Cl-K environ 2,83 keV (Methods).
- Résolution spatiale : 100 µm (petit fragment), 50 µm (grand) en macro ; jusqu'à 1 µm en micro-XRF. Pas de tomographie ici : pas de taille de voxel.
- Objets : fragments déroulés, pas de rouleau intact ; densité supposée 0,36 g/cm³, déduite d'un rouleau cylindrique de 5 cm de diamètre, 20 cm de long, 141 g (Methods).
- Calcul : simulation XMI-MSIM ; temps de calcul n/r.
- Code et données : logiciels tiers (XMI-MSIM, PyMCA, AXIL, Microxrf2) ; données brutes non publiées avec lien (figures supplémentaires S1 à S4 seulement) ; n/r pour le reste.

## Résultats

- Le Pb cartographié suit exactement l'écriture (Fig. 1B) ; Al, P et (moins) Cl sont plus abondants dans l'encre (Table 1).
- Quantification de l'encre, grand fragment, en w% : Pb 0,78 contre 0,05 pour le papyrus nu ; Al 1,00 contre 0,50 ; P 0,60 contre 0,40 ; petit fragment : Pb 0,15 contre 0,05 (Table 1). Ces valeurs sont un mélange encre plus papyrus sous-jacent (Results).
- Pb dans l'encre : environ 16 ± 5 µg/cm² (petit) et 84 ± 5 µg/cm² (grand) (Results).
- Pas de co-distribution Cu-Pb : une contamination par un récipient en bronze est écartée ; la teneur est trop élevée pour une contamination de l'eau (Results, Conclusion).
- Co-distribution Pb-P et Pb-Cl ; Al corrélé à Pb en macro mais pas en micro : encre de composition complexe et hétérogène à l'échelle micro (Fig. 2, Results).
- XANES Pb-L3 : Pb proche de l'acétate de plomb(II), avec une part éventuelle de PbS jusqu'à 45 % (Fig. 3) ; pas de contribution du minium. S-K : pas de pic de sulfure à 2,4725 keV, donc galène non indiquée (Fig. 4). Cl-K : ressemble à un organochloré, sans liaison directe avec Pb (Fig. 4).
- Interprétation : Pb ajouté volontairement, comme pigment ou siccatif (carboxylates de plomb), origine non tranchée ; un siccatif litharge-huile à 1:16 et 50 µm d'épaisseur donnerait 290 µg/cm², contre environ 80 µg/cm² mesurés (Results). Possible transformation par les éruptions puis par l'acide acétique des armoires en bois après 1754 (Results).
- Implication pour le contraste CT (affirmée par les auteurs seulement en une phrase) : les concentrations trouvées « fournissent des informations importantes pour optimiser les futures expériences de tomographie » (Conclusion).
→ reportés dans `benchmarks.csv` : aucune ligne. Les résultats sont des teneurs élémentaires et des spéciations, pas des performances de méthode ou de modèle comparables ; `benchmarks: none`.

## Limites et critique

- Deux petits fragments seulement, issus de rouleaux déroulés : représentativité pour les rouleaux intacts non établie.
- Les compositions mélangent encre et papyrus sous-jacent (pénétration des rayons X) ; hypothèses fortes dans la simulation (densité 0,36 g/cm³ déduite d'un rouleau entier, épaisseur 300 µm, fonction de transfert de la fenêtre du détecteur approchée par une baisse de flux de 30 %) (Methods).
- Origine du Pb non tranchée : altération probable pendant l'éruption et le stockage ; pas de FTIR ni de caractérisation de la partie organique (destructive) (Results, Conclusion).
- Le résultat de Brun et al. sur lequel tout repose est cité « soumis » : non vérifiable ici.
- Aucun calcul de contraste CT ni comparaison avec une tomographie n'est fait : le lien avec la détection d'encre est indirect.

## Pertinence pour la thèse

Thème de la base : lecture virtuelle en micro-CT. Ce papier apporte la chimie de l'encre : plomb, quantité de l'ordre de 16 à 84 µg/cm² d'encre, sous forme de carboxylates (type acétate) plutôt que de PbS, avec Al, P, Cl associés. C'est la raison physique plausible d'un signal d'encre dans les scans à haute énergie (déduit : Pb, numéro atomique élevé, absorbe nettement plus que le carbone du papyrus carbonisé, mais les auteurs ne le calculent pas), et il invite à la prudence : la composition est hétérogène à l'échelle micro, donc le contraste CT peut varier localement, ce qui touche la validation et l'écart de domaine entre rouleaux. Il laisse ouvert le lien quantitatif entre teneur en Pb et contraste en absorption ou en phase aux énergies et résolutions des scans (voxel de 2,4 à 9 µm), et la présence d'encre non plombée (encre carbonée) dans d'autres rouleaux.

## Gaps identifiés

- Lien quantitatif Pb (µg/cm²) vers atténuation CT à l'énergie du scan, modèle direct du contraste d'encre.
- Variabilité de la composition de l'encre entre rouleaux et entre scans (seulement deux fragments ici).
- Caractérisation de la fraction organique de l'encre (non faite).

## Statut de lecture

papier complet. Attention : extraction pymupdf avec `extraction.ok` à `false`, aucune section détectée ; le texte lu est continu mais le découpage en sections (Introduction, Results, Methods) est reconstitué de mémoire de lecture, et les corps de figures ne sont pas extraits (Fig. 2 à 4 lues par leurs légendes seulement). Supplementary Figures S1 à S4 non disponibles.
Ce qui suit est déduit et non affirmé par les auteurs : le lien avec le contraste CT (absorption du Pb par rapport au carbone), la pertinence pour la validation et l'écart de domaine.
