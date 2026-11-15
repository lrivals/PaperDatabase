---
id: 2019-tournie-ancient-greek-text-concealed-back
fiche: done
date: 2026-11-15
benchmarks: none
---

# Ancient Greek text concealed on the back of unrolled papyrus revealed through shortwave-infrared hyperspectral imaging

Aurélie Tournié, Kilian Josef Fleischer, Inna Bukreeva, Francesca Palermo, Michela Perino, Alessia Cedola, Christine Andraud, Graziano Ranocchia, 2019, Science Advances 5(10), eaav8936. https://doi.org/10.1126/sciadv.aav8936
Type : article de journal (relu par les pairs ; reçu le 11/01/2019, accepté le 13/08/2019, publié le 04/10/2019)

## Problème

Parmi les 1840 papyrus d'Herculanum catalogués, seuls huit portent aussi du texte au verso (Introduction). Pour PHerc. 1691/1021 (Philodème, *History of the Academy*), douze colonnes de verso ne sont connues que par des dessins du XVIIIe siècle (Bodleian Library), car les fragments déroulés mécaniquement en 1795 (machine de Piaggio) ont été collés sur carton. Il faut lire ce verso sans décoller les fragments, et améliorer la lisibilité du recto par rapport à l'imagerie à 950 nm des années 1999-2002 (BYU), qui ne pénètre pas assez pour le verso (Introduction).

## Méthode

Imagerie hyperspectrale SWIR (970-2500 nm), reflectance imaging spectroscopy, en push-broom ; cube normalisé par blanc (Spectralon 99 %) et noir, travail sur 1000-2500 nm (Materials and Methods). Analyse en composantes principales (PCA) du cube, sous ENVI ; seules PC1 à PC10 (99,99 % de la variance) sont visualisées ; étirement manuel (ENVI) puis netteté (ImageJ). PC3 révèle l'encre du verso ; PC1 donne le meilleur contraste encre/papyrus pour le recto (Results). D'autres traitements essayés au préalable (soustraction de bandes, continuum removal, rapports de bandes, dérivée spectrale) ne sont pas détaillés (Statistical analysis). Validation du verso par comparaison avec les dessins d'Oxford, retournés horizontalement (Fig. 3).

## Plateforme et implémentation

Caméra IMSPECTOR N25E (Specim, Finlande), détecteur MCT refroidi 320 × 256 pixels, plateforme MOLAB (IPERION CH). Temps d'intégration 3,5 ms, vitesse de balayage 41,7 mm/s. Objectif OLES56 : 200 µm d'échantillonnage spatial, distance de travail 380 mm, champ 60 mm ; 4 ou 5 balayages par fragment, assemblés manuellement. Objectif macro : 30 µm, distance 100 mm, champ 10 mm, réservé aux annotations marginales. Éclairage : deux rampes de trois lampes halogènes de 35 W ; exposition cumulée 14 lux·h par fragment (Materials and Methods). Neuf fragments, trois jours d'acquisition (Samples characteristics). Papyrus d'environ 0,15 mm d'épaisseur sur carton d'environ 0,30 mm. Code : aucun (logiciels commerciaux ENVI, ImageJ). Données : sélection d'images promise en accès ouvert par la Biblioteca Nazionale de Naples ; autres données sur demande aux auteurs (Discussion, Data availability). Pas de puissance ni de FPS : sans objet.

## Résultats

- Verso : texte lisible en PC3, qui ne contient que 0,4 % de la variance du cube (Revealing of the verso). Poids forts du chargement de PC3 vers 1000, 1300, 1680 nm et 2300-2500 nm (Fig. 1B).
- Les passages retrouvés sont dans PHerc. 1021, cornici 1-2, et appartiennent aux cinq premières colonnes de verso (Z, Y, X, V, T) ; seize passages marqués (Fig. 2). Col. V : 15 lignes lisibles (Fig. 3B) ; elle est invisible à 950 nm (Fig. 3A). Congruente avec le dessin d'Oxford, qu'elle corrige sur certaines lettres (col. V, l. 3 et 6, et l. 4).
- Découverte : texte inattendu dans la partie basse de la col. T (fig. S4) et indice d'une seconde main pour les cols. Z, Y, X (Revealing of the verso).
- Recto : PC1 contient 93,8 % de la variance totale ; environ 5 mots lisibles en plus par colonne et plus de 150 mots nouveaux sur le rouleau, par rapport à 950 nm (Enhancement of the recto). Exemple : lecture corrigée en PHerc. 1021, col. 19, l. 38-39 (Fig. 5).
- Annotations marginales : lisibles à 30 µm ; PC1 donne le meilleur contraste mais prend parfois des trous pour de l'encre, PC3 évite cet écueil (Fig. 6).
- Aucun texte détecté derrière les cornici 4-5, où sept colonnes de verso (S à M) sont attendues (Discussion).
- Baseline : imagerie à 950 nm (BYU, caméra Kodak Mega Plus 6.3i 2000 × 3000, 8 bits, environ 8 mois pour toute la collection) ; comparaison qualitative, sans métrique.
→ reportés dans `benchmarks.csv` : aucune ligne (`benchmarks: none`). Les résultats sont des gains de lisibilité qualitatifs ou des comptes de mots, sans métrique de modèle, de FPS ni de dataset ; aucune des colonnes de `benchmarks.csv` ne s'applique.

## Limites et critique

- Évaluation purement qualitative : pas de lecteurs en aveugle, pas de protocole de comparaison, pas de métrique de contraste ; « 5 mots de plus par colonne » est une moyenne sans variance ni méthode de comptage (déduit : non précisé).
- Faux positifs reconnus : à 200 µm, trous, fissures et plis sont parfois affichés comme encre (Discussion). Seule une comparaison avec l'original ou l'image à 950 nm les détecte.
- Validation du verso circulaire en partie : les passages sont identifiés grâce aux dessins du XVIIIe siècle, eux-mêmes imparfaits ; les textes inconnus (col. T basse) n'ont pas de référence. Les sept colonnes des cornici 4-5 ne sont pas retrouvées ; l'explication par l'épaisseur ou l'état de conservation est une hypothèse non testée.
- Le signal de verso ne représente que 0,4 % de variance (PC3) : dépend de la normalisation, des réglages manuels (étirement, netteté) et de l'état du fragment.
- Reproductibilité : pas de code, paramètres PCA non partagés, données sur demande.
- Pas de contrainte de dimension 3D : seule la surface déroulée est imagée, au contraire de la micro-CT.

## Pertinence pour la thèse

Pour le projet Elder-scrolls, article de contexte papyrologique et de validation : (1) c'est l'état de l'art des années 2000-2019 pour lire des papyrus d'Herculanum déroulés, donc la référence « avant CT » ; (2) il fournit une vérité terrain visuelle possible (images SWIR/950 nm de fragments déroulés) pour comparer à une encre détectée en CT, et un cas d'école de faux positifs (trous pris pour de l'encre) ; (3) il documente la mise en page des colonnes, les mains (groupe F de Cavallo) et le verso, utiles à la validation papyrologique des lettres lues ; (4) la détection par spectre (encre carbonée absorbante en SWIR) est un signal de nature différente de celui de la micro-CT. Reste ouvert : le lien avec les rouleaux encore enroulés (aucun, car la méthode demande un papyrus déroulé), et la quantification de la lisibilité.

## Gaps identifiés

- Aucun protocole quantitatif de comparaison de lisibilité entre modalités (SWIR, 950 nm, CT).
- Pas d'étude de transfert entre images spectrales de fragments déroulés et prédictions d'encre CT.
- Colonnes S à M du verso (cornici 4-5) non retrouvées : le signal ne traverse peut-être pas l'épaisseur.

## Statut de lecture

papier complet (`fulltext.md` lu en entier). Extraction : backend `pymupdf`, `extraction.ok` à `false` : texte probablement complet mais figures et légendes séparées du corps, sections numérotées non détectées ; aucun tableau (aucun chiffre de tableau à recouper).
Ce qui suit est déduit et non affirmé par les auteurs : l'absence de protocole d'évaluation quantitatif et de variance sur « 5 mots par colonne » (constat d'absence dans le texte lu) ; la caractérisation « référence avant CT » ; la pertinence pour la validation des faux positifs CT.
