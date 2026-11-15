---
id: 2018-stromer-browsing-through-sealed-historical-manuscripts
fiche: done
date: 2026-11-15
---

# Browsing through sealed historical manuscripts by using 3-D computed tomography with low-brilliance X-ray sources

Daniel Stromer, Vincent Christlein, Christine F. Martindale, Patrick Zippert, Eric Haltenberger, Tino Hausotte, Andreas Maier, 2018, Scientific Reports. https://doi.org/10.1038/s41598-018-33685-4
Type : article de journal (Open Access, relu par les pairs)

## Problème

Lire un livre fermé (non ouvrable) sans synchrotron, avec un micro-CT de laboratoire mobile : quelles encres sont visibles, avec quels paramètres de scan, et comment extraire et aplatir automatiquement les pages d'un volume où elles sont minces (1 à 3 voxels), ondulées et collées (Résumé, §Page extraction).

## Méthode

- Pas d'apprentissage : algorithme classique en trois étapes (§Page extraction) : (1) binarisation du volume par filtre guidé puis vesselness de Frangi sur chaque tranche yz (seuil 0,1), séparation des pages plus épaisses que 1,5 fois l'épaisseur moyenne ; (2) segmentation itérative des pages (comptage des pages par ligne, remplacement des lignes corrompues par la plus proche valide, médian sur xy) ; (3) texturation : valeur maximale le long de la normale à la ligne centrale de la page, projetée en image 2-D.
- Entrées : volume FDK reconstruit (CONRAD). Labels : aucun ; la vérité terrain est visuelle (photographies des pages), les zones d'encre sont segmentées à la main pour mesurer le contraste.
- Estimation théorique du contraste CR_est (Eq. 2-4) à partir des coefficients d'atténuation NIST XCOM et d'une épaisseur d'encre supposée de 2 µm. Mesure CR_msr = |m1 - m2| / sigma0 (CNR).
- Objet : livre fait maison (17 x 13 x 3 cm, 56 pages de papier artisanal d'environ 150 µm, couverture en cuir de buffle), 6 encres : malachite, 3 encres ferrogalliques (IG3 = IG avec FeSO4 en plus), pourpre de Tyr, nerprun (§Material).
- Placement horizontal (couverture orthogonale à l'axe de rotation) pour réduire artefacts métalliques et de cône (angle de cône max d'environ 1,43 degré) (§3-D reconstruction, Fig. 5).

## Plateforme et implémentation

- Source : micro-CT de laboratoire à géométrie cône (tube à faible brillance, marque n/r), pas de synchrotron. 3 scans de 360 degrés, 1800 projections : 30, 40, 50 kV (50 kV avec pré-filtre Cu 0,25 mm) ; 3 mA, 2 s d'exposition ; SOD 710 mm, SID 1377 mm, pixel détecteur 0,2 mm (§Volumetric scan).
- Résolution : voxel de 103 µm isotrope (scan principal) ; 59 µm pour un scan vertical à grand volume ; 30 µm pour un petit livre 4 x 4 x 0,5 cm testé auparavant (§Discussion). Énergie en kV (spectre polychromatique), pas de keV monochromatique.
- Rouleau/objet : livre fermé artificiel, pas de papyrus ni de rouleau carbonisé.
- Calcul : scan et reconstruction en ligne environ 2 h 10 min ; extraction de pages environ 15 min par volume ; matériel de calcul n/r (§Results). Couverture retirée manuellement du volume avant extraction.
- Code et données : annoncés publics (https://www5.cs.fau.de/~stromer/) ; base de 30 scans de livres (3 scanners, 6 livres) mentionnée (§Discussion, §Summary). Lien non vérifié.

## Résultats

- Évaluation : sur les scans du même livre, aucune région ni objet tenu à l'écart (pas d'apprentissage). Vérité terrain : photographies des pages et segmentation manuelle des symboles.
- Toutes les encres à particules métalliques sont visibles ; le nerprun (cellulose seule) est indiscernable du papier ; le pourpre de Tyr est à peine visible (§Qualitative analysis, Fig. 6).
- Plus l'énergie est basse, meilleur est le contraste : le scan à 30 kV est le meilleur pour toutes les encres ; CR_msr IG3 : 4,23 (50 kV), 4,33 (40 kV), 4,68 (30 kV) (Table 1). Valeurs CR_msr de malachite 0,90 / 1,55 / 1,76 ; Tyrian 0,07 / 0,22 / 0,45 (50 / 40 / 30 kV) (Table 1). CR_msr généralement cohérent avec CR_est.
- Plus de fer (IG3) donne une meilleure visibilité (§Qualitative analysis, Table 1).
- Effet chromatographique : dans le papier, les particules métalliques s'accumulent aux bords des lettres ; intensité 2 à 3 fois le fond aux bords, environ 1,5 fois au centre (§Chromatographic effect, Fig. 7).
- Placement horizontal : pas d'artefacts métalliques, contre artefacts en placement vertical (Fig. 5). Recommandation : au moins 3 mA et 2 s (6 mAs), énergie 20-40 kV (§Discussion).
- Une page de 150 µm couverte par 1-3 voxels à 103 µm ; l'auteur note 1-3 voxels comme minimum pour séparer les pages (le texte dit « 13 », probablement un artefact d'extraction pour « 1-3 ») (§Discussion).
→ reportés dans `benchmarks.csv` : 15 lignes (CR_msr par encre et par tension, Table 1 ; CR_est non repris car estimé).

## Limites et critique

- Livre artificiel, papier artisanal (absorbe l'encre, d'où l'effet chromatographique), pas de vieillissement, pas de pages recto-verso ; le papyrus et le parchemin se comportent autrement, et l'encre de Herculanum est carbonée, sans contraste d'absorption : non traité. Les conclusions sur les métaux ne transfèrent pas directement.
- Pas de comparaison chiffrée à un synchrotron : l'avantage du synchrotron (SNR, résolution) est argumenté, pas mesuré.
- Voxel de 103 µm, bien plus grossier que les 8-9 µm du Vesuvius Challenge ; pages à 1-3 voxels.
- Algorithme d'extraction non évalué quantitativement (pas de métrique de segmentation), seulement visuellement ; dépend du nombre de pages N supposé constant par ligne, et de la suppression manuelle de la couverture.
- CR_msr : zones mesurées manuellement, mesure d'une seule lettre ('C' ou symboles chinois), pas de répétition ni de barre d'erreur ; une seule instance de chaque encre.
- Table 1 extraite par PyMuPDF (extraction.backend pymupdf) : l'assignation des colonnes IG1/IG2/IG3 est déduite de l'ordre et de la cohérence avec le texte ; le texte dit malachite supérieure à IG1 et IG2, ce que les chiffres retenus ne vérifient pas partout (IG2 > malachite à 50 kV). À contrôler contre le PDF rendu.

## Pertinence pour la thèse

Faible à modérée pour le projet Elder-scrolls. Utile comme repère de protocole sur le transfert scanner/protocole : l'énergie du tube, la filtration et la tension modifient le contraste d'encre (CR_est calculable à partir des coefficients XCOM), la même encre donne un signal différent selon la configuration, ce qui motive l'harmonisation et l'adaptation entre scans. Également un cas d'école de déroulage virtuel de pages (vesselness de Frangi, texturation par maximum le long de la normale), proche de l'idée de rendu de surface ; le principe « valeur maximale » diffère du rendu en couches utilisé pour l'encre carbonée. Ne traite pas l'encre carbonée ni le papyrus : n'informe pas la détection d'encre sans contraste d'absorption.

## Gaps identifiés

- Pas de quantification, sur papyrus carbonisé, de l'effet de l'énergie et du protocole du scanner sur le signal d'encre.
- Aucune comparaison directe labo vs synchrotron sur le même objet.
- Extraction de pages classique non comparée à des méthodes apprises (les auteurs annoncent une base de 30 scans pour cela).

## Statut de lecture

Papier complet lu (`fulltext.md`), mais l'introduction est partiellement manquante (extraction PyMuPDF : `extraction.ok` à false, aucune section détectée) ; texte des équations et de Table 1 reconstruit, à vérifier. Déduit et non affirmé par les auteurs : l'assignation exacte des colonnes de Table 1 (IG1/IG2/IG3), la lecture « 1-3 voxels » de « 13 », et la pertinence pour Elder-scrolls.
