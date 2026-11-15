---
id: arxiv-2007.15551-quantitative-distortion-analysis-flattening-applied
fiche: done
date: 2026-11-15
benchmarks: none
---

# Quantitative Distortion Analysis of Flattening Applied to the Scroll from En-Gedi

Clifford Seth Parker, William Brent Seales, Pnina Shor, 2020, arXiv preprint. https://arxiv.org/abs/2007.15551
Type : preprint non relu par les pairs

## Problème

L'aplatissement (3D vers 2D) d'une surface de manuscrit endommagé, ni isométrique ni conforme au plan, introduit étirements et cisaillements qui déforment le texte lisible et faussent la fusion 2D de patchs voisins (décalage de ligne de base, Fig. 2). Les auteurs veulent mesurer objectivement cette distorsion et la relier aux artefacts visibles (Intro, §2).

## Méthode

- Algorithmes comparés (§2.1) : LSCM (conforme aux moindres carrés, implémentation libigl, deux sommets fixés), ABF (minimise l'erreur sur les angles, implémentation Blender modifiée) et MM, l'algorithme maison de « material modeling » (simulation masses-ressorts sur Bullet Physics, propriétés physiques supposées du matériau) utilisé pour déplier le rouleau d'En-Gedi.
- Métriques (§2.2) : étirement par triangle L2 (moyen) et L∞ (pire cas) de Sander et al. ; erreur angulaire d'ABF F(M) (Éq. 1-2) ; erreur d'aire par triangle de Blender E(t), moyennée en E(M) (Éq. 3). Cartes d'erreur produites avec Blender.
- Entrées : sept maillages de surface (EG0-3, 5, 6, plus EG4) extraits du rouleau d'En-Gedi, avec texture issue du pipeline de dépliage virtuel. Pas de labels ni d'entraînement : méthode géométrique.

## Plateforme et implémentation

- Source du scan, énergie, résolution µm/voxel : n/r dans ce papier (renvoi à Seales et al. [1]). Objet : rouleau d'En-Gedi (synagogue, mer Morte, Lévitique), surfaces EG0-EG6.
- Matériel et temps de calcul : n/r (MM décrit seulement comme « coûteux en calcul », §2.1).
- Code et données : non publiés dans le papier ; seuls libigl et Blender (tiers) sont cités.
- Évaluation : sur les mêmes sept maillages, sans région ni rouleau tenu à l'écart (pas d'apprentissage). Vérité terrain : aucune ; métriques géométriques intrinsèques plus jugement visuel des textures.

## Résultats

- ABF et LSCM n'ont pas produit de paramétrisation pour EG4 ; seul MM est présenté (§3).
- Distorsion angulaire : les trois méthodes sont proches, à quelques exceptions près (Table A.3, corps non extrait) ; MM y est comparable bien qu'il ne cherche pas à minimiser l'erreur conforme (§3).
- MM : L2 et L∞ nettement pires (cisaillement global et élongation du bord droit d'EG0, Fig. A.1, A.8), mais effet global sur l'aire minime (Table A.4) (§3).
- LSCM : L2 proche d'ABF, mais distorsion d'aire bien pire, parfois avec une échelle non linéaire visible dans la texture (Fig. A.3, A.6) (§3).
- MM : un groupe de faces « repliées » sur elles-mêmes a fait disparaître un élément de bord d'EG2 (Fig. 3), faute de garantie sur le contour (§3).
- Conclusion : ABF est le premier choix par défaut (peu de configuration, faible erreur isométrique et conforme) ; ABF++ cité comme suite pour les grands maillages (§4).
→ reportés dans `benchmarks.csv` : aucun. Les valeurs chiffrées sont dans les Tables A.1-A.4 de l'annexe, absentes du texte extrait ; le texte ne donne aucun chiffre.

## Limites et critique

- Chiffres inaccessibles ici (annexe non extraite) : seules les tendances qualitatives sont lisibles.
- Aucune métrique de lisibilité ou de paléographie : le lien entre distorsion et lecture reste visuel et subjectif.
- Sept maillages d'un seul rouleau ; MM n'est pas réglé sur les propriétés physiques réelles du rouleau (les auteurs le reconnaissent, §4) : la comparaison est donc défavorable à MM par construction.
- ABF et LSCM sont des implémentations tierces (Blender modifié, libigl) ; temps de calcul et mémoire non comparés. Déduit : ABF reste coûteux sur de très grands maillages (d'où ABF++).
- Les méthodes ultérieures (SLIM, ARAP, flatboi) ne sont pas couvertes.

## Pertinence pour la thèse

Cadre de mesure utile pour l'étape d'aplatissement de la chaîne Elder-scrolls (SLIM, flatboi) : étirement L2/L∞ et erreur d'aire par triangle sont des métriques directement réutilisables pour comparer des aplatissements de segments Herculanum, en plus de la distorsion de bord qui conditionne la fusion de patchs. Le papier ne traite ni Herculanum, ni grande échelle, ni méthodes isométriques modernes. Preprint de l'équipe EduceLab.

## Gaps identifiés

- Distorsion mesurée sur des segments Herculanum à 8-9 µm avec SLIM/flatboi : non couvert.
- Lien quantitatif entre distorsion et dégradation de la lecture ou de l'encre détectée : non étudié.
- Fusion 3D de patchs plutôt que fusion 2D après aplatissement : non traité.

## Statut de lecture

Papier complet (texte extrait par PyMuPDF, `extraction.ok` faux ; ligatures réparées, 5 fragments non réparés ; tables A.1-A.4 et figures d'annexe sans corps extrait).
Ce qui suit est déduit et non affirmé par les auteurs : le coût d'ABF sur de grands maillages ; la portée pour SLIM/flatboi ; l'absence de comparaison à des méthodes ultérieures.
