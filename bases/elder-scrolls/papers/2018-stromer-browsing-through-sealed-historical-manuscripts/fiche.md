---
id: 2018-stromer-browsing-through-sealed-historical-manuscripts
fiche: done
date: 2026-11-15
---

# Browsing through sealed historical manuscripts by using 3-D computed tomography with low-brilliance X-ray sources

Daniel Stromer, Vincent Christlein, Christine F. Martindale, Patrick Zippert, Eric Haltenberger, Tino Hausotte, Andreas Maier, 2018, Scientific Reports. https://doi.org/10.1038/s41598-018-33685-4
Type : article de journal (relu par les pairs ; reçu 31/05/2018, accepté 03/10/2018)

## Problème

Des manuscrits fragiles ou scellés (pages collées, livres brûlés ou inondés ; les papyrus d'Herculanum sont cités en exemple) ne peuvent plus être ouverts. Les auteurs veulent savoir quels manuscrits et quelles encres se prêtent à une lecture par micro-CT de laboratoire (source à faible brillance, sans synchrotron) et comment choisir les paramètres d'acquisition ; le contraste est suivi sur toute la chaîne : scan, extraction des pages, mise à plat (Résumé, Introduction).

## Méthode

- Livre fabriqué pour l'étude : 17 × 13 × 3 cm, couverture en cuir de buffle, 56 pages de papier artisanal d'environ 150 µm (Material). Six encres : trois encres ferro-galliques (IG1, IG2, IG3 = une encre enrichie en FeSO4), malachite (Cu), pourpre de Tyr (Al, S, Cl, Sn), nerprun (cellulose seule, donc de même atténuation que le papier) (Material, Fig. 1c, Fig. 2 : EDS).
- Contraste attendu : coefficients d'atténuation massique NIST XCOM, `CR_est` = rapport de contraste encre + papier / papier seul, avec papier 200 µm et encre 2 µm (Eq. 2-4, Results).
- Acquisition : micro-CT à géométrie conique, 3 scans à 360° avec 1800 projections, 30, 40 et 50 kV (50 kV avec préfiltre Cu 0,25 mm), 3 mA, 2 s, SOD 710 mm, SID 1377 mm, détecteur 0,2 mm, voxel 103 µm (Methods). Livre posé à plat (couverture orthogonale à l'axe de rotation) pour réduire les artefacts métalliques et coniques. Reconstruction FDK avec CONRAD (Methods).
- Extraction automatique des pages (méthode publiée antérieurement, réf. 40) : filtre guidé, filtre de vesselness de Frangi sur les coupes yz, binarisation par seuil 0,1, séparation des pages épaisses (> 1,5 p), correction itérative des lignes où le nombre de pages diffère de N, filtre médian, puis texturage par maximum le long de la normale à la page pour obtenir l'image 2D (Methods, Fig. 4). Couverture retirée à la main avant extraction (Results).
- Mesure : `CR_msr` = |m1 − m2| / σ0, m1 = moyenne sur les symboles segmentés à la main, m2 = papier seul, σ0 = écart type du bruit (Results ; la formule est mal extraite, forme lue par déduction du texte).

## Plateforme et implémentation

Micro-CT de laboratoire à cône (modèle exact n/r), cadre CONRAD. Durée : environ 2 h par scan, 2 h 10 avec reconstruction en ligne ; extraction environ 15 min par volume (Results). Matériel de calcul n/r. Données, code et calculs : « publiquement disponibles » sur www5.cs.fau.de/~stromer/ (Summary) ; lien non vérifié. Base de 30 scans de livres (3 scanners, 6 livres) annoncée mais non distribuée explicitement (Discussion).

## Résultats

- Placement horizontal : pas d'artefacts métalliques, contre artefacts en vertical ; la comparaison est confondue avec la taille de voxel (voxel d'environ 59 µm pour le scan vertical, « large volume scan ») (Results, Fig. 5).
- Encres métalliques visibles ; nerprun invisible, pourpre de Tyr à peine visible, malachite et ferro-galliques lisibles ; l'encre IG3 la plus contrastée (Results, Fig. 6).
- Plus la tension est basse, meilleur est le contraste, au prix de plus de bruit (Table 1). CR_msr à 30 / 40 / 50 kV : malachite 1,76 / 1,55 / 0,90 ; IG1 1,12 / 0,92 / 0,32 ; IG2 1,55 / 1,25 / 1,24 ; IG3 4,68 / 4,33 / 4,23 ; pourpre de Tyr 0,45 / 0,22 / 0,07 (Table 1). CR_est à 30 / 40 / 50 kV : malachite 2,98 / 2,19 / 1,74 ; ferro-gallique 2,32 / 1,78 / 1,49 (une valeur pour IG1-3) ; pourpre de Tyr 1,06 / 1,04 / 1,03 (Table 1).
- Effet chromatographique : l'encre migre avec le liquide dans le papier artisanal et s'accumule aux bords des lettres ; intensité 2 à 3 fois le fond aux bords, environ 1,5 fois au centre (Fig. 7, « Chromatographic effect »). Ce signal est propre au papier absorbant, pas au papyrus ni au parchemin (le papier le dit).
- Recommandations : courant ≥ 3 mA, exposition ≥ 2 s (6 mAs), énergie de 20 à 40 kV (Discussion). Pages sur environ 1-3 voxels à 103 µm, jugé minimum pour séparer les pages (Methods ; la Discussion écrit « only 13 », chiffre ambigu, probablement 1-3).
→ reportés dans `benchmarks.csv` : 15 lignes (5 encres × 3 tensions, `CR_msr`, Table 1), `confidence: medium` (corps du tableau extrait par PyMuPDF, colonnes à vérifier). Les `CR_est` restent dans cette fiche seulement.

## Limites et critique

- Livre d'expérience, papier artisanal neuf, encre à environ 2 µm d'épaisseur supposée : très éloigné d'un papyrus carbonisé, où l'encre au carbone est invisible en absorption (déduit, non dit par les auteurs ; ils reconnaissent que les matériaux ne sont pas historiques et pourraient se comporter autrement). Résultat utile surtout comme borne : une encre sans élément métallique (nerprun, cellulose) est indiscernable du support, ce qui éclaire le problème de l'encre carbonée (déduit).
- Voxel de 103 µm, 12 fois plus grossier que les 8-9 µm du Vesuvius Challenge : l'extraction de pages par vesselness ne se transpose pas telle quelle (déduit).
- Pas de répétition ni d'incertitude sur CR_msr ; une seule page par encre, segmentation manuelle des symboles. Table 1 : à 50 kV, IG2 (1,24) dépasse la malachite (0,90), alors que le texte dit la malachite plus contrastée que IG1 et IG2 ; incohérence possible du corps de tableau extrait, ou énoncé valable seulement à 30 kV.
- CR_est n'a qu'une valeur pour les trois encres ferro-galliques alors que leurs CR_msr diffèrent beaucoup (IG3 enrichie) : le modèle ne rend pas compte de la concentration.
- Comparaison « verticale vs horizontale » confondue avec la résolution (59 vs 103 µm). Aucun baseline de segmentation, aucune métrique de qualité de l'extraction de pages ; pas de pages recto-verso testées (Discussion).
- Ne pas comparer ces CR_msr à d'autres CNR : définition propre, scanner et préfiltrage non standard.

## Pertinence pour la thèse

Pour Elder-scrolls, papier de contexte (axes `ct-imaging`, `ink-detection`, `virtual-unwrapping`) : il fixe la physique du contraste d'encre en CT (atténuation de l'élément métallique et concentration), explique pourquoi l'encre de carbone d'Herculanum n'est pas visible en absorption, et montre un déroulage de livre fermé en laboratoire. Il ne traite ni papyrus, ni encre carbonée, ni apprentissage ; l'accumulation de l'encre aux bords est une hypothèse morphologique, relative au papier. Importance : faible à moyenne.

## Gaps identifiés

- Pas de mesure du contraste d'une encre carbonée en CT de laboratoire à haute résolution (rouleaux ou papyrus modèles).
- Page extraction par filtres classiques non évaluée contre une vérité terrain ; les auteurs annoncent une base de 30 scans pour de l'apprentissage, sans résultat.

## Statut de lecture

Papier complet (`fulltext.md` lu en entier). Extraction `pymupdf`, `extraction.ok` faux, aucune section détectée : formules (Eq. 1-4, CR_msr) mal rendues, corps de Table 1 reconstruit par PyMuPDF (à vérifier ; lecture colonnes : malachite CR_est, CR_msr ; ferro-gallique CR_est, IG1, IG2, IG3 ; pourpre de Tyr CR_est, CR_msr). `chunks.jsonl` absent : `chunk_id` à `n/r`.
Déduit et non affirmé par les auteurs : lecture des colonnes de Table 1 ; formule de CR_msr ; transposition à l'encre carbonée et à la résolution de 8-9 µm ; « only 13 » lu comme 1-3 voxels ; l'importance pour le projet.
