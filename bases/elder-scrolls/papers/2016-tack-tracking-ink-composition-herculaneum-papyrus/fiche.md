---
id: 2016-tack-tracking-ink-composition-herculaneum-papyrus
fiche: done
date: 2026-11-15
benchmarks: none
---

# Tracking ink composition on Herculaneum papyrus scrolls: quantification and speciation of lead by X-ray based techniques and Monte Carlo simulations

Pieter Tack, Marine Cotte, Stephen Bauters, Emmanuel Brun, Dipanjan Banerjee, Wim Bras, Claudio Ferrero, Daniel Delattre, Vito Mocella, László Vincze, 2016, Scientific Reports. https://doi.org/10.1038/srep20763
Type : article de journal (relu par les pairs ; reçu 26/08/2015, accepté 07/01/2016).

## Problème

Le texte des rouleaux d'Herculanum, révélé par tomographie de phase X (Mocella et al.), reste difficile à lire à cause des fibres du papyrus qui croisent l'écriture. Brun et al. (« submitted », non publié au moment de l'article) ont montré que l'encre contient du plomb (Pb), qui rend le texte plus lisible en fluorescence X (XRF). Les auteurs cherchent l'origine et l'état chimique de ce Pb (Introduction) en testant quatre hypothèses : Pb contaminant de l'eau du solvant ; contaminant d'un récipient en bronze ; pigment au plomb (galène PbS, céruse, minium) ; siccatif au plomb (litharge PbO) d'une encre à base lipidique.

## Méthode

Analyse non destructive multi-échelle sur deux fragments plats de rouleaux déroulés (« grand » ≈ 0,9 × 1,2 cm², « petit » ≈ 0,5 × 0,8 cm², épaisseur ≈ 0,3 mm ; lettres E, Π, Ι, N, Ι, Α et O, Λ) (Methods).
- Cartes XRF 2D sur toute la surface, faisceau sous-millimétrique (pas 50 µm pour le grand, 100 µm pour le petit), ligne ID21 de l'ESRF, énergie 3,5 keV (Methods).
- Pixels « encre » isolés par clustering K-means, comparés visuellement à la carte XRF ; spectres moyens encre vs papyrus nu (Results).
- Quantification par simulation Monte Carlo (XMI-MSIM), en ajustant itérativement la composition simulée au spectre expérimental (Results, Methods).
- Micro-XRF jusqu'à 1 µm de pas (faisceau ≈ 0,3 × 0,6 µm²) pour tester la co-localisation Pb/P/Al/S/Cl (Methods, Fig. 2).
- XANES aux seuils Pb-L3 (ligne BM26A DUBBLE), S-K et Cl-K (ID21), comparés à des composés de référence, avec ajustement par combinaison linéaire (Fig. 3, 4).

## Plateforme et implémentation

Synchrotron ESRF (Grenoble) : ID21 (microscopie X, détecteur Bruker XFlash 5100 SDD, fenêtre Moxtek AP3.3) et BM26A (DUBBLE, détecteur Vortex-EM). Logiciels : XMI-MSIM, PyMCA, AXIL, Microxrf2 (Methods). Échantillons pris entre deux films ultralène de 4 µm. Code et données : non publiés (rien d'annoncé dans le texte ; les figures supplémentaires S1-S4 ne sont pas dans `fulltext.md`). Matériel et temps de calcul : n/r (sans objet : pas de modèle d'apprentissage).

## Résultats

- Les cartes de Pb reproduisent la distribution de l'encre (Fig. 1B) ; Al, P et Pb sont plus élevés dans l'écriture (Results).
- Composition de l'encre vs papyrus, en % massique (Table 1) : grand fragment, Pb 0,78 (encre) vs 0,05 (papyrus), Al 1,00 vs 0,50, P 0,60 vs 0,40 ; petit fragment, Pb 0,15 vs 0,05, Al 0,75 vs 0,60, P 0,35 vs 0,25. Le C (≈ 75-77 %) est déterminé par différence (note de Table 1).
- Concentration de Pb dans l'encre ≈ 16 ± 5 µg/cm² (petit) et 84 ± 5 µg/cm² (grand) (Results). Ces valeurs représentent un mélange encre + papyrus sous-jacent, non l'encre pure (Results).
- Cu sans co-distribution avec l'écriture, ce qui écarte un récipient de bronze (Results, Fig. S2).
- Micro-XRF : Pb co-distribué avec P et Cl ; pas d'association chimique Pb-Al à l'échelle micro ; S seulement partiellement co-localisé, donc PbS improbable comme constituant principal (Fig. 2).
- XANES Pb-L3 : état proche de l'acétate de plomb(II) ; combinaison linéaire avec PbS jusqu'à 45 % possible, mais le post-seuil de PbS est peu structuré (Fig. 3). Pas de raie blanche de minium (≈ 13,055 keV).
- S-K : spectre dominé par le papyrus, pas de pic de sulfure à 2,4725 keV ; Cl-K : ressemble à un organochloré, sans lien direct avec Pb (Fig. 4).
- Estimation théorique pour un siccatif (ratio litharge/huile 1:16, épaisseur 50 µm, huile 0,93 g/mL) : 290 µg/cm², supérieure au ≈ 80 µg/cm² mesuré (Results).
- Conclusion des auteurs : Pb n'est ni un contaminant du solvant ni du récipient ; il a plus probablement été ajouté volontairement (pigment ou siccatif), sans réponse définitive (Conclusion).

→ reportés dans `benchmarks.csv` : aucune ligne. Papier de chimie analytique, sans modèle, tâche ni métrique de performance comparable aux colonnes du fichier (fps, luts, accuracy_metric…). Les concentrations en Pb sont des résultats d'analyse, non des benchmarks.

## Limites et critique

- Deux fragments seulement, déroulés mécaniquement puis conservés depuis 1754 : histoire d'altération (pyroclastique, armoires en bois émettant de l'acide acétique) qui peut avoir transformé le Pb ; les auteurs le reconnaissent et ne concluent pas sur l'origine (Conclusion).
- Les concentrations sont celles d'un mélange encre + papyrus (rayons X pénétrants) ; épaisseur 300 µm et densité 0,36 g/cm³ du modèle sont estimées à partir d'un rouleau cylindrique (5 cm × 20 cm, 141 g) et non mesurées sur les fragments (Methods).
- Les incertitudes de la quantification Monte Carlo ne sont données que pour le Pb (± 5 µg/cm²) ; Table 1 est sans incertitude. Écart spectral attribué à l'absence de simulation < 1 keV et à l'empilement d'impulsions (Fig. 1C).
- Pas de FTIR ni d'analyse organique (destructif) : la nature du liant reste hypothétique.
- Les résultats XRF ne se transposent pas directement à la tomographie de phase des rouleaux fermés : seul lien évoqué, les concentrations utiles à « l'optimisation des futures expériences de tomographie » (Conclusion). Le papier de Brun et al. cité est « submitted ».
- Reproductibilité : pas de données ni code publiés dans le texte lu.

## Pertinence pour la thèse

Axe `ink-detection`, avec `papyrology` en second. Question de recherche « comment détecter une encre carbonée sans contraste d'absorption en CT » : ce papier donne le fait physique de fond. L'encre d'Herculanum contient du Pb (≈ 16-84 µg/cm² selon le fragment), surtout sous forme de carboxylate/acétate, sans pigment au plomb dominant. La quantité de Pb est faible, ce qui est cohérent avec un contraste CT faible à 8-9 µm (déduit, non affirmé par les auteurs). Il laisse ouvert si ce signal chimique se traduit par un signal exploitable en micro-CT, et ne traite d'aucune méthode de détection par apprentissage.

## Gaps identifiés

- Lien quantitatif entre concentration de Pb, épaisseur d'encre et contraste/texture observable en micro-CT à 8-9 µm : non traité.
- Composition organique du liant (lipides, siccatif) non résolue ; absence d'analyse non destructive des composés organiques.
- Échantillon limité à deux fragments : variabilité entre rouleaux (PHerc.) inconnue.

## Statut de lecture

Papier complet (`fulltext.md` lu en entier). Avertissement d'extraction : backend `pymupdf`, `extraction.ok` à `false`, aucune section détectée ; le texte est continu mais le corps de Table 1 est reconstruit sans en-têtes de ligne fiables : la première colonne, étiquetée « Ca », est lue comme C d'après la note a de la table. Les figures supplémentaires S1-S4 ne sont pas disponibles.
Ce qui suit est déduit et non affirmé par les auteurs : le rapprochement avec le contraste CT à 8-9 µm ; la lecture de la première colonne de Table 1 comme C.
