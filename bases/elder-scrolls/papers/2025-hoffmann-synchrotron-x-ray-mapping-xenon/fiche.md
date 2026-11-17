---
id: 2025-hoffmann-synchrotron-x-ray-mapping-xenon
fiche: done
date: 2026-11-17
benchmarks: none
---

# Synchrotron X-ray Mapping of Xenon Sorption in Carbon Ink on Papyrus

Hannes Hoffmann, Tobias Arlt, André Hilger, Dirk Wallacher, Ingo Manke, 2025, ChemRxiv (posté le 17 juillet 2025). https://doi.org/10.26434/chemrxiv-2025-x4zvc
Type : preprint non relu par les pairs (mention « Data may be preliminary » dans le texte).

## Problème

L'imagerie X d'encres carbonées cachées sur support organique est présentée comme un problème non résolu (Abstract) : l'atténuation X ne distingue pas l'encre carbonée du papyrus (§1), les traces de métaux lourds dans les encres anciennes sont sporadiques (§1), et la reconnaissance d'encre par texture exige de très hautes résolutions et n'a donné que du texte fragmentaire (§1, citant Nicolardi et al. 2024 et Parsons 2023). Les rouleaux d'Herculanum, le cartonnage de momies et les rouleaux fermés sont concernés. Les auteurs cherchent un agent de contraste non destructif.

## Méthode

Proposition : le xénon (Z = 54, gaz inerte) s'adsorbe/absorbe davantage dans le carbone concentré (suie, charbon, grande surface interne, forces de van der Waals) que dans la matière végétale ; il crée donc un contraste d'atténuation encre/support (§1). L'hypothèse d'un carbone plus concentré dans l'encre ancienne que dans le papyrus est posée, non mesurée (§1).
Échantillon modèle : papyrus du commerce, poudre de charbon « médicinal » de haute pureté, gomme arabique en solution aqueuse ; trois couches de papyrus (cadre intermédiaire ménageant un espace où l'encre forme une lettre), chauffées entre deux plaques d'aluminium jusqu'à la teinte rougeâtre de pyrolyse incomplète (§2). Cuve sous pression en aluminium, livraison et régulation de gaz (Fig. 1).
Protocole : tomographies d'absorption à 33,3 keV (sous le seuil K du Xe) et 34,9 keV (au-dessus), à vide, 1, 5 et 10 bar puis retour (Fig. 2, §3). Analyse par images de différence (10 bar vs vide, 34,9 vs 33,3 keV), profils le long de lignes, séries temporelles par région (Fig. 6, 7).

## Plateforme et implémentation

Ligne BAMline, synchrotron BESSY II (HZB, Berlin), mesures du 11 avril 2024 (§3). Caméra pco edge 5,5 + scintillateur CdWO4 de 100 µm, pixel de 3,6 µm, 2000 projections, 150 ms d'exposition (§3). Hauteur de faisceau limitant l'échantillon à environ 3 mm (§3). Pas de méthode d'apprentissage ni de calcul. Dose, flux, taille de voxel reconstruit, logiciel de reconstruction : n/r. Code et données : non publiés.

## Résultats

Résultats qualitatifs, aucune métrique chiffrée de contraste (CNR, taux d'absorption) ; tout est montré sur images et profils (Fig. 3-7).
- Le marquage au Xe rend visibles des particules de l'encre (couche < 370 µm, particules de 10 à 150 µm), mais ces particules seraient aussi discernables sans Xe, leur géométrie suffisant ; le Xe « renforce » le contraste (§3).
- Distribution différentielle du Xe dans les particules selon la pression ; à 10 bar, l'accumulation débute dans certaines parties des particules et progresse vers le centre (§3, Fig. 6-7). Lecture des auteurs : adsorption initiale sur surfaces élevées, puis absorption dans le volume de carbone (§4, interprétation).
- Signal Xe faible dans les fibres, qui les rend visibles, plus fort dans les particules (§3).
- Désorption : une part importante partie après 1 h sous vide (§3, Fig. 4-5) ; le résumé et la Conclusion disent qu'aucun Xe résiduel n'a été détecté ; aucun changement ou dommage observé (§4-5).
- Affirmation non sourcée par une mesure : à moins de 100 keV, l'atténuation du Xe serait environ 18 fois celle des ions fer (§4, sans référence ni calcul).
→ reportés dans `benchmarks.csv` : aucune ligne. Papier qualitatif sur un échantillon modèle, sans métrique de détection ni configuration chiffrée comparable (`benchmarks: none`).

## Limites et critique

- Limites des auteurs (§3) : mouvements de l'échantillon dus aux vibrations et aux variations de pression, corrigés seulement localement (grosses particules comme repères), pas de correction globale ; hauteur d'échantillon limitée à 3 mm.
- La démonstration est très faible comme preuve de contraste : les particules d'encre étaient visibles sans xénon (§3), et la lettre n'est pas montrée lisible. Pas de comparaison quantitative avec/sans Xe. « Valuable tool » (§3) est une conclusion forte pour des images qualitatives (jugement déduit).
- Échantillon modèle : charbon de haute pureté, particules de 10 à 150 µm, couche jusqu'à 370 µm ; l'encre carbonée d'Herculanum est selon la base d'échelle et de nature différentes (déduit, non mesuré ici). L'hypothèse centrale (carbone et surface interne de l'encre antique plus élevés que ceux d'un papyrus lui-même partiellement carbonisé, §1) n'est pas testée ; la prévision de sélectivité encre/papyrus carbonisé est ouverte.
- Incohérence interne : « une part importante désorbée après 1 h » (§3) contre « aucun Xe résiduel détecté » (Conclusion).
- Sécurité de conservation non démontrée : 10 bar sur un rouleau carbonisé fragile, dose X, un seul échantillon sans réplicat. Le « first time » (§4) n'est pas vérifié ici.
- Pas de comparaison avec les méthodes d'encre par apprentissage (Reader, texture) ; l'amélioration de ces méthodes est suggérée sans test (§1, §4).
- Auteur principal indépendant ; non relu par les pairs.

## Pertinence pour la thèse

Rattaché à `ink-detection` (créer un contraste physique pour une encre carbonée sans contraste d'absorption), à `ct-imaging` (seuil K, 33-35 keV, 3,6 µm) et à `papyrology` (Herculanum, cartonnage, appariement de fragments par « code-barres » des fibres, §4, spéculatif). Il propose, face à l'apprentissage sur le signal résiduel, un chemin chimique/physique ; il n'aide pas les scans déjà acquis (8-9 µm, sans Xe) et ne concerne que de futurs scans, avec un risque de conservation non évalué (déduit).
Situation par rapport à `2026-hoffmann-xenon-contrast-carbon-ink-tomography` (même auteur) : ce preprint est l'étude source, détaillée, avec ses protocoles et ses figures ; le poster Zenodo 2026 (Eighth Papyrus Curatorial and Conservation Meeting) en est une version condensée qui reprend les images de cette étude (réf. [1] du poster). Le poster ajoute des perspectives sans mesure (déplacement compétitif Kr-Xe, comptage de photons, neutrons ¹³¹Xe, IRM ¹²⁹Xe, chargement par refroidissement) ; le preprint évoque seulement dual-energy, comptage de photons et IRM (§4) et ajoute l'idée de fibres comme code-barres et les fossiles. Les deux ne sont donc pas deux preuves indépendantes : un seul jeu de mesures (11 avril 2024, BAMline), publié deux fois ; ne pas compter deux sources. Pour les détails mesurés, citer le preprint ; pour l'état des idées de l'auteur en 2026, le poster. Écart à noter : le poster dit « plus de xénon détectable » après 1 h sous vide, ce qui lève l'incohérence du preprint (part importante désorbée vs aucun résidu) au profit de la lecture forte (déduit).

## Gaps identifiés

- Aucune mesure de contraste (CNR) avec/sans xénon ; pas d'échantillon antique ou de papyrus réellement carbonisé.
- Sélectivité encre vs papyrus carbonisé d'Herculanum non testée.
- Sécurité de conservation (pression, dose, rétention) non documentée ; pas de lien avec les cartes d'encre apprises.

## Statut de lecture

Papier complet (fulltext.md lu en entier). Extraction `pymupdf`, `extraction.ok: false` : texte dupliqué (page de garde puis texte), sections numérotées non détectées, figures non lisibles (seules les légendes), numéros de figures cités dans le texte (« Fig. 6 et 7 », « Fig. 4 et 5 ») pas toujours cohérents avec les légendes. Références non incluses dans la base.
Ce qui suit est déduit et non affirmé par les auteurs : non-représentativité de l'échantillon modèle par rapport à l'encre d'Herculanum, faiblesse de la preuve de contraste, incohérence désorption/aucun résidu, relation avec le poster 2026 (même jeu de mesures), inapplicabilité aux scans existants.
