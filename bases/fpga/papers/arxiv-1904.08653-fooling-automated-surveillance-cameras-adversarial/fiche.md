---
id: arxiv-1904.08653-fooling-automated-surveillance-cameras-adversarial
fiche: done
date: 2026-09-29
benchmarks: none
---

# Fooling automated surveillance cameras: adversarial patches to attack person detection

Simen Thys, Wiebe Van Ranst, Toon Goedemé, 2019, arXiv preprint. https://arxiv.org/abs/1904.08653
Type : preprint non relu par les pairs

## Problème

Les attaques adverses physiques existantes ciblent des objets à apparence fixe (panneaux stop) ; aucune n'a été proposée pour des personnes, classe à forte variabilité intra-classe (vêtements, pose, contexte) (Abstract, §3.2). Les auteurs veulent montrer qu'un simple carton imprimé (~40 cm x 40 cm) tenu devant le corps peut cacher une personne à un détecteur de vidéosurveillance (§1).

## Méthode

Optimisation directe des pixels d'un patch (poids du réseau gelés, initialisation aléatoire, optimiseur Adam) avec la perte L = alpha*L_nps + beta*L_tv + L_obj : non-printability score, variation totale, et score maximal d'objectness/classe du détecteur (§3). Trois variantes de L_obj : score de classe (CLS), objectness (OBJ), produit des deux (OBJ-CLS) (§3.1). Données d'entraînement : images réelles d'Inria (pas de transformation d'un seul modèle) ; le détecteur lui-même fournit les boîtes de personnes ; le patch est posé à position fixe relative à la boîte (§3.2). Robustesse physique : rotation jusqu'à ±20°, changement d'échelle, bruit, luminosité/contraste aléatoires (§3.3). Cible : YOLOv2 entraîné sur MS COCO, en boîte blanche (§2, §3.1).

## Plateforme et implémentation

Sans objet côté matériel : pas de FPGA, ni latence, ni puissance (n/r). Code publié : https://gitlab.com/EAVISE/adversarial-yolo (§1). Vidéo de démonstration : https://youtu.be/MIbFvK2S9g8.

## Résultats

- Sur le jeu de test Inria, recall à un point de fonctionnement fixé (seuil 0,4 choisi sur la courbe CLEAN) : CLEAN 100 %, NOISE (patch aléatoire) 87,14 %, OBJ-CLS 39,31 %, OBJ 26,46 %, CLS 77,58 % (Table 1). Minimiser l'objectness (OBJ) est le plus efficace (§4, Fig. 5).
- Minimiser la classe fait converger le patch vers une autre classe COCO (ours en peluche) : moins transférable (§3.1).
- Test réel qualitatif avec le patch imprimé : « fonctionne plutôt bien » ; échec quand le patch est mal placé au centre de la personne (§4, Fig. 7).
→ reportés dans `benchmarks.csv` : aucune ligne (attaque logicielle, pas de mesure matérielle) ; `benchmarks: none`.

## Limites et critique

- Cible unique (YOLOv2, boîte blanche) ; transférabilité à d'autres détecteurs faible d'après les auteurs (section 6 tronquée dans l'extraction) et non quantifiée.
- Évaluation quantitative uniquement sur Inria, avec les « vérités terrain » produites par le même détecteur (CLEAN = 100 % par construction, §4) : les chiffres mesurent une réduction d'alarmes du détecteur, pas de la vérité terrain. Le test réel est qualitatif, sans statistique (Fig. 7).
- Patch tenu devant le corps à position précise ; sensible à l'alignement (§4). Pas de test sur vêtements, ni de défense proposée.
- Aucune analyse sur cibles embarquées ou quantifiées ; l'effet de la quantification (INT8, binaire) sur la vulnérabilité n'est pas étudié (déduit).

## Pertinence pour la thèse

Volet secondaire *security* du profil : le cas d'application (YOLO de détection de personnes en vidéosurveillance) est exactement le scénario de l'attaque ; un patch peut rendre une personne invisible dans une zone dangereuse. Motive un moniteur d'exécution (redondance, détection d'anomalie d'entrée) et une évaluation adverse dans un dossier d'assurance, mais ne traite pas de safety ni de FPGA. Reste ouvert : robustesse des détecteurs quantifiés/embarqués et défenses compatibles FPGA.

## Gaps identifiés

- Effet de la quantification et de la compilation FPGA sur la vulnérabilité aux patchs adverses.
- Défenses à l'exécution (moniteurs) compatibles avec les contraintes temps réel embarquées.

## Statut de lecture

papier complet (fulltext.md lu en entier ; la section « Future work » est tronquée en fin d'extraction ; Table 1 lue ; les figures ne sont que des légendes). Déduit et non affirmé par les auteurs : la portée pour des détecteurs quantifiés ou FPGA, et l'utilité pour un moniteur d'exécution.
