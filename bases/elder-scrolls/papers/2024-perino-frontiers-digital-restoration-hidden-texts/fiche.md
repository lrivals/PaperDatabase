---
id: 2024-perino-frontiers-digital-restoration-hidden-texts
fiche: done
date: 2026-11-15
benchmarks: none
---

# New Frontiers in the Digital Restoration of Hidden Texts in Manuscripts: A Review of the Technical Approaches

Michela Perino, Lucilla Pronti, Candida Moffa, Michela Rosellini, Anna Candida Felici, 2024, Heritage 7, 683–696. https://doi.org/10.3390/heritage7020034
Type : article de revue (journal, MDPI, accès ouvert CC BY), relu par les pairs ; article de synthèse (survey), reçu 20/12/2023, accepté 22/01/2024.

## Problème

Rendre lisibles des écritures cachées (effacées, passées, carbonisées, vieillies) sans abîmer le manuscrit.
Les auteurs veulent un guide pratique pour choisir la technique d'imagerie adaptée au support et à l'encre, et esquissent les perspectives d'association avec l'apprentissage automatique (Abstract, §1).

## Méthode

Revue narrative, sans protocole de recherche bibliographique ni critère d'inclusion annoncés (déduit : rien n'est décrit). Un paragraphe d'accessibilité des bibliothèques et de manipulation des codex (§2), puis huit familles de techniques : photographie UV (§3), imagerie multi- et hyperspectrale (§4), MA-XRF (§5), tomographie X (§6), thermographie infrarouge pulsée (§7), térahertz (§8), photoacoustique (§9), sources non conventionnelles : synchrotron, faisceaux d'ions/PIXE, neutrons (§10).

## Plateforme et implémentation

Sans objet : pas d'implémentation propre, pas de puce ni de puissance. Code et données : aucun code publié ; « Data sharing is not applicable » (Data Availability Statement).

## Résultats

Synthèse qualitative, sans chiffre de performance comparé entre techniques. Points utiles à la base :
- La tomographie X (§6) est la seule famille qui lit un rouleau fermé. Premier déroulage virtuel : rouleau d'En-Gedi, encre à base de métal détectable en micro-CT (§6, Fig. 4).
- Encre carbonée sur papyrus carbonisé : la XCT d'absorption standard ne la distingue pas du papyrus ; le contraste vient de la phase (XPCT), Bukreeva et al. 2016, après Mocella et al. 2015 (§6).
- Vesuvius Challenge (2023, Seales et EduceLab) : trois phases, scan, segmentation et aplatissement, détection d'encre ; l'encre se lit après aplatissement sur le scan 3D (§6).
- MA-XRF : insensible aux matériaux de faible numéro atomique, donc à l'encre carbonée ; adaptée aux encres ferro-galliques (§5). Elle a aussi révélé des lignes de réglage au plomb sur des papyrus grecs, preuve expérimentale que les colonnes obliques étaient un choix de scribe (§5, réf. [45]).
- Herculanum : MSI en 1999 (infrarouge) [10,11], HSI [28] (§4) ; projets ERC « GreekSchools » (papyrus d'Herculanum) et « PAGES » (palimpsestes) (§1).
- Apprentissage automatique : GAN et segmentation sémantique pour démêler des écritures superposées, sur jeu synthétique (§4, Fig. 2) ; conclusion : « avancée notable » pour l'encre des palimpsestes et papyrus carbonisés (§11), sans résultat chiffré.
→ reportés dans `benchmarks.csv` : aucune ligne (survey, aucun chiffre propre aux auteurs ; `benchmarks: none`).

## Limites et critique

- Le volet tomographie est très bref (un paragraphe, §6) : aucune méthode de segmentation, d'aplatissement ni de détection d'encre n'est décrite ; Vesuvius Challenge n'est qu'évoqué.
- Aucune comparaison quantitative entre techniques (résolution, contraste, dose, temps d'acquisition) : le « guide de sélection » reste qualitatif.
- Pas de méthode de recherche bibliographique, donc couverture non vérifiable. L'ajout « (accessed on 24 January 2023) » pour scrollprize.org précède la soumission : date probablement erronée (déduit).
- Les affirmations sur l'apprentissage automatique reposent sur des renvois, sans résultat ni limites (hallucination, validation) discutés.

## Pertinence pour la thèse

Faible à moyenne, comme cadrage. Elle situe la lecture virtuelle des rouleaux d'Herculanum parmi les techniques d'imagerie de textes cachés, avec les références fondatrices (En-Gedi, Mocella 2015, Bukreeva 2016, MSI/HSI d'Herculanum) et la formulation en trois phases. Utile pour le contexte et la section papyrologie (lignes de réglage, colonnes obliques). Elle n'apporte rien sur la détection d'encre 3D, la segmentation, la super-résolution ni la validation. Axes : surveys, virtual-unwrapping, papyrology, ct-imaging.

## Gaps identifiés

- Aucune revue de ce corpus qui compare les méthodes de détection d'encre et de segmentation du Vesuvius Challenge ; celle-ci ne les couvre pas.
- Rien sur la validation ni les faux positifs des cartes d'encre.
- Références à suivre (absentes de la base, à vérifier via `bin/pdb base scan`) : Bukreeva 2016, Mocella 2015, déroulage d'En-Gedi (Seales 2016).

## Statut de lecture

papier complet (fulltext.md lu en entier). Extraction par pymupdf avec `extraction.ok: false` : texte possiblement mal découpé (l'en-tête est fragmenté) ; le corps est cependant lisible et complet à la lecture, sans tableau (aucun tableau dans l'article).
Ce qui suit est déduit et non affirmé par les auteurs : absence de protocole de revue, date d'accès erronée, jugements sur la brièveté du volet tomographie et sur la faible pertinence pour la base.
