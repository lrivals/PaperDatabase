---
id: 2026-hoffmann-xenon-contrast-carbon-ink-tomography
fiche: done
date: 2026-11-15
benchmarks: none
---

# XENON CONTRAST FOR CARBON-INK TOMOGRAPHY

Hannes Hoffmann (chercheur indépendant ; expériences avec T. Arlt, A. Hilger, D. Wallacher, I. Manke, Helmholtz-Zentrum Berlin), 2026, Zenodo. https://doi.org/10.5281/zenodo.23164128
Type : `report` — **poster d'un seul auteur déposé sur Zenodo, non relu par les pairs** (préparé pour le 8e Papyrus Curatorial and Conservation Meeting, Berlin, 17-18 sept. 2026). Les expériences reposent sur un article source (réf. [1], preprint ChemRxiv 2025, lui aussi non relu à ce que dit le poster : n/r). Solidité : faible à modérée, voir « Limites ».

## Problème

L'encre carbonée et le papyrus carbonisé sont deux matériaux de numéros atomiques faibles, d'atténuation X très proche : l'écriture reste invisible en tomographie X classique (section « Why the ink remains invisible »). Résoudre les couches ne sert à la lecture que si l'encre se distingue du support.

## Méthode

Idée : introduire du xénon (haut Z, gaz noble, sorption physique par van der Waals) comme marqueur ; la sorption différentielle dans l'encre et le papyrus créerait un contraste d'atténuation, et sa cinétique (charge/décharge) une « signature temporelle » (poster, « Kinetic and spectral readout »).
- Échantillon modèle : trois couches de papyrus, charbon médical et gomme arabique, chauffé jusqu'à pyrolyse partielle ; particules 10-150 µm, épaisseur d'encre 20-370 µm (« Model sample »).
- Protocole : vide, puis Xe à 1 / 5 / 10 bar, puis évacuation ; scans à 33,3 keV (sous le seuil K du Xe) et 34,9 keV (au-dessus) pour isoler le Xe spectralement.
- Pas d'algorithme, de labels ni d'apprentissage : étude de contraste purement physique, par inspection d'images (Figs. 2-4).
- Pistes proposées, non testées : déplacement compétitif Kr-Xe, micro-CT à comptage de photons avec seuils autour de 34,56 keV, tomographie neutronique résonante du ¹³¹Xe, IRM du ¹²⁹Xe, chargement par refroidissement (estimation 2-3x plus de sorption à 0 °C qu'à 25 °C, à partir d'énergies de liaison de 22-27 kJ/mol).

## Plateforme et implémentation

- Source : synchrotron, ligne BAMline, BESSY II, Helmholtz-Zentrum Berlin ; mesures du 11 avril 2024 ; énergies 33,3 / 34,9 keV.
- Résolution : 3,6 µm ; 2000 projections x 150 ms (« Demonstration conditions »).
- Objet : échantillon modèle fabriqué (pas de rouleau ni de fragment authentique). Cuve de pression au xénon sur platine piézo (Fig. 1).
- Matériel de calcul, temps de reconstruction : n/r (aucun calcul). Dose : n/r.
- Code et données : non publiés ; images des Figs. 1-4 reprises de la réf. [1] (CC BY-NC-ND 4.0).
- Données d'évaluation : pas d'évaluation au sens ML ; pas de région ni de rouleau tenus à l'écart. Vérité terrain : la composition connue de l'échantillon modèle (encre déposée par l'auteur), sans mesure de lisibilité.

## Résultats

Qualitatifs, sans valeur numérique de performance (Figs. 2-4, « What the model experiment showed ») :
- le Xe augmente l'atténuation dans les particules d'encre et met en évidence plus faiblement les fibres de papyrus ;
- le contraste suit la pression et le temps ; la comparaison 33,3 / 34,9 keV identifie le Xe au seuil K ;
- la sorption commence dans des sous-régions des particules et progresse vers l'intérieur (Fig. 3) ;
- après 1 h sous vide, le Xe n'est plus détectable (Fig. 4) ; aucun dommage visible sur le modèle.
→ reportés dans `benchmarks.csv` : aucune ligne (aucune métrique chiffrée de détection ou de lisibilité ; les valeurs rapportées sont des conditions expérimentales). `benchmarks: none`.

## Limites et critique

- **Preuve de principe sur un matériau modèle** : les auteurs le reconnaissent (« Limits of the demonstration ») : pas de contraste lisible démontré sur un artefact authentique, pas de fenêtre pression/température/dose pour un objet intact.
- **Aucune quantification** : pas de contraste-sur-bruit, de rapport de contraste ni de courbe de sorption chiffrée ; l'affirmation « contraste » repose sur des images choisies. Pas de réplicats, pas de témoin sans xénon chiffré.
- **Modèle peu représentatif** : charbon médical + gomme arabique, particules de 10-150 µm et encre épaisse (20-370 µm), contre des encres antiques fines et des papyrus d'Herculanum carbonisés, où la structure poreuse et la chimie diffèrent beaucoup. Le contraste observé pourrait refléter la macroporosité des particules, absente d'une encre réelle (déduit).
- **Conflit possible avec la littérature (déduit)** : le poster dit l'encre « invisible » en CT ; or les travaux du Vesuvius Challenge lisent de l'encre carbonée sans marqueur, par détection de texture/morphologie (Parker, Seales et al.), et le poster ne les cite pas ni ne se compare à eux. Il ne cite que deux références (Davy 1821, et un article de l'auteur).
- **Risques non traités** : sorption dans le papyrus (donc faible sélectivité : le papyrus « est plus faiblement mis en évidence »), manipulation sous 10 bar d'objets fragiles carbonisés, conservation, éthique ; « aucun dommage visible » ne vaut pas test de conservation.
- **Titre et affirmation** : l'en-tête parle d'« A solution to the carbon ink tomography problem », ce que le contenu ne démontre pas.
- Pistes finales (Kr-Xe, photon-counting, neutrons, IRM, refroidissement) : spéculatives, aucune testée ; l'estimation 2-3x à 0 °C est un calcul de l'auteur sans donnée.
- Auto-publication unique, sans relecture ; conflit d'intérêts déclaré nul.

## Pertinence pour la thèse

Peu directement exploitable pour la chaîne du projet (détection d'encre par ML sur scans 8-9 µm sans marqueur) : il s'agit d'une voie d'acquisition alternative, non applicable aux rouleaux déjà scannés. Intérêt indirect : (i) rappelle le problème du contraste nul encre/papyrus que le ML contourne via la texture ; (ii) l'idée d'un signal d'encre isotrope servant d'étiquette de surface pour la segmentation (« Isotropic ink signal for segmentation ») est évoquée sans démonstration. Pertinence faible, à citer comme piste de contexte, pas comme résultat établi.

## Gaps identifiés

- Aucun contraste d'encre démontré sur un artefact réel par marqueur gazeux ; pas de quantification contraste/bruit.
- Absence de comparaison entre contraste exogène (Xe) et détection ML sans marqueur sur le même matériau.
- Innocuité pour un papyrus carbonisé fragile non évaluée.

## Statut de lecture

Papier complet (poster de 7 ko ; extraction `pymupdf`, `extraction.ok` faux, aucune section détectée : l'ordre du texte est celui de la mise en page du poster, légendes de figures sans tableaux ; les figures elles-mêmes ne sont pas lues).
Déduit et non affirmé par les auteurs : la non-représentativité du modèle par rapport aux encres antiques, le conflit avec la détection ML sans marqueur, l'absence de réplicats, le fait que le contraste pourrait venir de la macroporosité.
