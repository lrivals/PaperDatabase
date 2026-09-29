---
id: arxiv-1702.01135-reluplex-efficient-smt-solver-verifying
fiche: done
date: 2026-09-29
benchmarks: none
---

# Reluplex: An Efficient SMT Solver for Verifying Deep Neural Networks

Guy Katz, Clark Barrett, David Dill, Kyle Julian, Mykel Kochenderfer, 2017, arXiv preprint. https://arxiv.org/abs/1702.01135
Type : preprint non relu par les pairs (dans cette base ; la version publiée à CAV 2017 n'est pas celle lue ici)

## Problème

Fournir des garanties formelles sur le comportement de réseaux de neurones ReLU utilisés dans des systèmes critiques (contrôleur ACAS Xu de collision aérienne pour drones). Vérifier une propriété d'un DNN ReLU est NP-complet (Annexe I, réduction depuis 3-SAT) ; les solveurs généraux (SMT, LP/MIP) échouent et les outils dédiés se limitent à ~10-20 neurones cachés (§1).

## Méthode

Reluplex étend l'algorithme du simplexe à la théorie des réels avec contraintes ReLU (§3) : chaque ReLU est codé par une paire de variables (arrière v_b / avant v_f) ; l'algorithme laisse temporairement les bornes et la sémantique ReLU être violées, les corrige par pivots et mises à jour (règles Update_b, Update_f, PivotForRelu), et ne « découpe » (ReluSplit : actif/inactif) qu'après un seuil de corrections (5 dans l'implémentation, §6). Trois techniques d'implémentation (§4) : dérivation de bornes plus serrées (élimine des ReLU sans découpage), analyse de conflits avec retour arrière, arithmétique flottante (double) avec contrôle de l'erreur d'arrondi et restauration du tableau (seuil 1e-6, contrôle tous les 5000 pivots). Calcul prouvé correct et complet (Annexe II) ; la version flottante ne garantit pas la correction (§4). Propriétés vérifiées : contraintes linéaires sur entrées et sorties, robustesse locale (delta-locally-robust) et globale (§6).

## Plateforme et implémentation

Sans objet côté FPGA : solveur logiciel (prototype construit sur le solveur LP GLPK modifié, §6), exécuté sur CPU ; matériel de test n/r dans le texte extrait. Cible vérifiée : 45 réseaux ACAS Xu, complètement connectés, 6 couches cachées, 300 ReLU chacun, 5 entrées / 5 sorties, moins de 3 Mo au total contre plus de 2 Go pour la table de référence (§5). Code et expériences annoncés en ligne (réf. [14] du papier), lien non repris dans le texte extrait.

## Résultats

- Table 1 (corps non extrait, cf. `extraction.warnings`) : 8 propriétés simples satisfiables, timeout de 4 h, sur 2 réseaux : Reluplex les résout toutes ; Yices et MathSat en résolvent 2 chacun, Gurobi 3 (rapidement quand aucun découpage n'est nécessaire), CVC4 et Z3 : aucun succès mentionné (déduit : le texte dit que seuls Yices et MathSat ont résolu des instances) (§6). Temps individuels : n/r ici.
- Table 2 : φ1 prouvée sur 41 réseaux sur 45 (4 timeouts), 394 517 s au total et 1 522 384 découpages ; φ3 et φ4 prouvées sur 42 réseaux ; φ2 fausse sur 35 réseaux (comportement jugé acceptable par les auteurs, §6). φ5, φ6, φ9, φ10 prouvées (temps 19 355 s, 180 288 s, 99 634 s, 19 944 s) ; φ7 en timeout ; φ8 : contre-exemple (SAT, 40 102 s) révélant une incohérence avec la table de référence, confirmée en simulation (§6).
- La profondeur maximale de découpage reste très inférieure à 300 ReLU et environ 10 % des ReLU suffisent souvent à éliminer tous les autres via les bornes (§6).
- Robustesse locale (Table 3) : 5 points x 5 valeurs de delta (temps totaux de 1 064 s à 20 462 s, le point 5 étant le plus coûteux), recherche binaire de delta (ex. point 4 : delta optimal entre 0,025 et 0,05) (§6). La robustesse globale n'est prouvée que sur de petits réseaux.
→ reportés dans `benchmarks.csv` : aucune ligne. Justification : mesures de temps de vérification logicielle, sans plateforme matérielle ni FPS/GOPS/puissance ; les temps sont donnés dans la fiche (Table 1 sans corps extrait).

## Limites et critique

- Passage à l'échelle : réseaux de ~300 ReLU seulement ; propriété φ7 et 4 réseaux de φ1 en timeout ; les auteurs le disent (§6, §8).
- Correction : arithmétique flottante, restauration du tableau mais « ne garantit pas la correction » (§4) ; les auteurs proposent de rejouer en arithmétique exacte ou de produire des preuves vérifiables (§8). Or un argument de certification exige la correction.
- Ne traite que des ReLU, réseaux complètement connectés (max-pooling évoqué comme piste, §8) ; pas de convolutions, pas de YOLO ni de détecteur, pas de quantification entière ni de virgule fixe. Pas de lien avec l'implémentation matérielle : ce que l'on vérifie est le modèle réel en flottant, pas le réseau quantifié tel que déployé sur FPGA (inférence des auteurs, non discutée dans le papier).
- Preprint ; évalué sur un seul cas d'étude aéronautique ; comparaison avec solveurs généraux sur 2 réseaux, 8 propriétés triviales de la forme x >= c (biais possible en faveur de Reluplex qui est spécialisé).

## Pertinence pour la thèse

Référence fondatrice de la vérification formelle de DNN, donc de l'axe `safety-certification` (« vérification formelle de réseaux quantifiés ou binarisés » du profil). Fournit le vocabulaire (propriétés entrée/sortie, robustesse locale/globale) et illustre le cas ACAS Xu, où la certification a été un moteur du remplacement d'une table de 2 Go par des DNN de moins de 3 Mo. Pour la thèse : les techniques ne s'appliquent pas telles quelles à un YOLO convolutif de dizaines de millions de paramètres ; elles montrent la nécessité de petits réseaux ou de vérification sur sous-composants (déduit).

## Gaps identifiés

- Vérification formelle de réseaux de détection convolutifs quantifiés (INT8/binaires) tels que déployés sur FPGA : non couverte par ce papier.
- Écart entre le modèle vérifié (flottant) et le circuit FPGA (virgule fixe, HLS) : pas de chaîne de preuve de bout en bout.

## Statut de lecture

Papier complet (corps principal et annexes I-VI lus jusqu'aux définitions de propriétés). Seul le corps de la Table 1 (comparaison aux autres solveurs, temps par solveur) manque à l'extraction : ces temps ne sont donnés que qualitativement par le texte ; les Tables 2 et 3 sont extraites. Déduit et non affirmé par les auteurs : pertinence pour YOLO/FPGA, écart flottant/quantifié, matériel de test (n/r).
