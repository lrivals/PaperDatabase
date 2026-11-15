---
id: 2026-hoffmann-xenon-contrast-carbon-ink-tomography
fiche: done
date: 2026-11-15
benchmarks: none
---

# XENON CONTRAST FOR CARBON-INK TOMOGRAPHY

Hannes Hoffmann (Independent Researcher), 2026, Zenodo (poster pour le Eighth Papyrus Curatorial and Conservation Meeting, 17-18 septembre 2026, Berlin). https://doi.org/10.5281/zenodo.23164128
Type : rapport (poster de conférence déposé sur Zenodo ; non relu par les pairs, ni preprint au sens strict). Le poster reprend les images de Hoffmann, Arlt, Hilger, Wallacher & Manke, « Synchrotron X-ray Mapping of Xenon Sorption in Carbon Ink on Papyrus », ChemRxiv 2025, doi:10.26434/chemrxiv-2025-x4zvc (réf. [1], elle aussi preprint) ; les co-auteurs figurent dans le bandeau « Experimental study » (Helmholtz-Zentrum Berlin).

## Problème

L'encre carbonée des papyrus d'Herculanum et le papyrus carbonisé sont deux matériaux légers, de coefficient d'atténuation aux rayons X très proches : l'écriture reste invisible en tomographie X conventionnelle (« Why the ink remains invisible »). Résoudre les couches internes ne sert à rien pour la lecture si l'encre n'est pas distinguable du support (« The contrast problem »). Les auteurs cherchent un agent de contraste non destructif pour objets fermés ou enroulés.

## Méthode

Idée : utiliser le xénon comme marqueur à Z élevé. Gaz noble, il s'adsorbe par forces de van der Waals sans réaction chimique ; les différences de composition, de structure poreuse et de chimie de surface entre encre et papyrus deviennent des différences d'atténuation (« Xenon adds a high-Z label »).

Démonstration sur un échantillon modèle (« Model sample ») : trois couches de papyrus avec charbon médicinal et gomme arabique, chauffées jusqu'à pyrolyse partielle ; particules de 10 à 150 µm, épaisseur d'encre de 20 à 370 µm. Protocole : vide, puis Xe à 1 / 5 / 10 bar, puis évacuation. Deux énergies de scan, 33,3 keV (sous le seuil K du Xe) et 34,9 keV (au-dessus) ; le seuil K du Xe est donné à 34,56 keV (§ perspectives) ; 3,6 µm, 2000 projections × 150 ms (« Demonstration conditions »). Lecture cinétique et spectrale : la sorption/désorption produit une signature temporelle, et les bins autour du seuil K isolent le xénon du substrat léger.

Perspectives avancées sans mesure (hypothèses des auteurs) : déplacement compétitif Kr-Xe, micro-CT à comptage de photons avec seuils de part et d'autre du seuil K (source de laboratoire), tomographie neutronique résonante ¹³¹Xe, IRM ¹²⁹Xe, chargement assisté par refroidissement, signal d'encre isotrope comme étiquette de surface pour la segmentation.

## Plateforme et implémentation

Ligne BAMline, synchrotron BESSY II, Helmholtz-Zentrum Berlin, mesures du 11 avril 2024 (Conclusion) ; cuve sous pression de xénon sur platine piézo (Fig. 1) ; résolution 3,6 µm (voxel/pixel exact : n/r). Détecteur, taille de faisceau, dose : n/r. Code ou données : non publiés dans ce document ; images des Fig. 1-4 reprises de la réf. [1] (CC BY-NC-ND 4.0). Pas de calcul ni de matériel de traitement (pas de méthode d'apprentissage).

## Résultats

Résultats qualitatifs uniquement, aucun chiffre de performance :
- Le xénon augmente l'atténuation dans les particules d'encre et met plus faiblement en évidence les fibres de papyrus ; le contraste suit la pression et le temps ; les mesures sous et au-dessus du seuil K identifient spectralement le xénon (« What the model experiment showed », Fig. 2).
- La sorption commence dans des sous-régions des particules et progresse vers l'intérieur ; cinétiques de sorption/désorption différentes selon les sous-régions (Fig. 3).
- Après 1 h sous vide, plus de xénon détectable (Fig. 4) ; aucun dommage visible sur le modèle.
- Estimation théorique (non mesurée) : avec des énergies de liaison de 22-27 kJ/mol, environ 2-3 fois plus de sorption à 0 °C qu'à 25 °C, ou un chargement comparable à 0,3-0,5 fois la pression (« Cooling-assisted xenon loading », faible couverture de surface).
→ reportés dans `benchmarks.csv` : aucune ligne (poster qualitatif, pas de métrique de détection, pas de configuration chiffrée comparable ; `benchmarks: none`).

## Limites et critique

- Limites reconnues par les auteurs (« Limits of the demonstration ») : l'échantillon modèle isole le mécanisme ; la démonstration n'établit ni un contraste lisible sur un artefact original, ni une fenêtre pression/température/dose praticable pour un objet intact.
- Échantillon modèle (charbon médicinal + gomme arabique, pyrolyse partielle) non représentatif de l'encre antique ni du papyrus d'Herculanum carbonisé par le Vésuve (déduit) ; couches et épaisseurs d'encre (jusqu'à 370 µm) bien supérieures à une encre réelle (déduit, ordre de grandeur non rapporté dans ce document pour l'original).
- Aucune mesure quantitative (contraste-bruit, taux d'adsorption, pression/temps de saturation) dans ce poster : tout est dans les figures et la réf. [1], non lue ici.
- Risques non traités : adsorption par un papyrus fragile, effet de la pression de 10 bar sur un rouleau carbonisé, dose de rayons X, conservation ; « aucun dommage visible » n'est observé qu'à l'échelle du modèle.
- Pas de comparaison avec les méthodes d'encre sans contraste (apprentissage sur texture/topographie) ni avec l'approche contraste de phase.
- Les perspectives (neutrons, IRM, comptage de photons, signal isotrope pour segmentation) sont spéculatives, sans données. Auteur principal indépendant, aucun financement, pas de relecture par les pairs.

## Pertinence pour la thèse

Pertinence pour Elder-scrolls : indirecte mais conceptuelle. Elle répond à la question de recherche « comment détecter une encre carbonée sans contraste d'absorption en CT ? » par un autre chemin que l'apprentissage sur le signal résiduel (texture, morphologie) : créer un contraste physique par un marqueur. Elle ne s'applique pas aux scans existants (8-9 µm, rouleaux déjà scannés sans xénon) ; elle ne servirait qu'à de futurs scans. Résolution de 3,6 µm et énergie 33-35 keV proches de l'échelle des scans synchrotron mais sans lien avec les rouleaux PHerc. Elle apporte aussi l'idée d'un label dense isotrope (xénon) comme vérité terrain pour la segmentation et la validation (axes validation-fp, label-efficiency, à titre d'hypothèse). Reste ouvert : contraste sur original, dose, protocole sûr.

## Gaps identifiés

- Contraste chimique ou par sorption pour l'encre carbonée : aucune évaluation sur un papyrus carbonisé réel dans la base.
- Aucune comparaison quantitative entre signal de sorption et signal appris (Reader V3, `ink_9um`) ; pas de paires scan avec/sans xénon.
- Sécurité de conservation (pression, dose, rétention de gaz) non documentée.

## Statut de lecture

Résumé seul (poster) : `fulltext.md` (~7 ko, extraction `pymupdf`, `extraction.ok: false`, aucune section détectée) contient le texte intégral du poster, mais c'est un poster, pas un article. Il est lu en entier ; les Fig. 1-4 sont des images non lisibles ici (seules les légendes), et la réf. [1] qui porte les mesures détaillées n'est pas dans la base. Ordre du texte extrait mélangé (colonnes de poster).
Ce qui suit est déduit et non affirmé par les auteurs : non-représentativité de l'échantillon modèle, écart d'échelle avec l'encre réelle, inapplicabilité aux scans existants, utilité comme étiquette de validation.
