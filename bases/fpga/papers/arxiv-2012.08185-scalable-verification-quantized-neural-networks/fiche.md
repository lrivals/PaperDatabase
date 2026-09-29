---
id: arxiv-2012.08185-scalable-verification-quantized-neural-networks
fiche: done
date: 2026-09-29
benchmarks: none
---

# Scalable Verification of Quantized Neural Networks (Technical Report)

Thomas A. Henzinger, Mathias Lechner, Đorđe Žikelić, 2020, arXiv preprint (rapport technique (« Technical Report » dans le titre) ; venue de publication n/r dans les métadonnées). https://arxiv.org/abs/2012.08185
Type : preprint non relu par les pairs

## Problème

La vérification formelle de réseaux de neurones travaille presque toujours sur un modèle idéalisé en arithmétique réelle (`f_R`) ou suppose `f_float32 ≈ f_R`, en ignorant les erreurs d'arrondi. Or la quantification (arithmétique à point fixe de k bits, 4 à 8 bits) est largement utilisée pour déployer des réseaux, et une propriété vraie sur `f_R` ou `f_float32` peut être fausse après quantification (Introduction, « Verification of quantized neural networks »). Les outils existants pour réseaux quantifiés (encodage SMT bit-vector de Giacobbe et al. 2020, théorie point fixe de Baranowski et al. 2020, SAT pour réseaux binaires) ne passent pas à l'échelle. Deux questions : ce problème est-il intrinsèquement plus dur, et peut-on l'accélérer ?

## Méthode

- Résultat théorique : la vérification de réseaux quantifiés avec spécification bit-vector (fragment QF_BV2_bw) est PSPACE-hard, par réduction depuis TQBF (Théorème 1, §« Hardness… » et preuve en annexe), alors que la vérification idéalisée est NP-complète (Katz et al. 2017) et la satisfiabilité de la spécification seule est dans NP. Borne supérieure : NEXP (les auteurs), écart non refermé.
- Trois techniques pour l'encodage SMT monolithique bit-exact (§« Improvements ») : (I) suppression des branches mortes de l'activation ReLU-N grâce à une analyse d'intervalles (interprétation abstraite) ; (II) largeur minimale de bit-vector par variable, `b_min = 1 + log2(max(|lb|,|ub|)+1)` au lieu de `2k + log2(n) + 1` ; (III) élimination de multiplications redondantes (multiplications par le même poids, ou réductibles à des décalages).
- Évaluation : robustesse adversariale `l∞` (spécification éq. 13) sur MNIST et Fashion-MNIST avec un réseau dense (784-64-32-10, 52 650 paramètres) entraîné par quantization-aware training sur 6 bits ; solveur Boolector avec CaDiCaL (baseline = Giacobbe et al. 2020, avec Lingeling ou CaDiCaL) ; ablation sur MNIST (§« Experimental Evaluation »).

## Plateforme et implémentation

Sans objet côté FPGA : aucune implémentation matérielle, aucune mesure de puissance. Expériences sur CPU Intel W-2175 14 cœurs, 64 Go de RAM (§« Experimental Evaluation »). Code : n/r dans le texte lu (pas de lien trouvé).

## Résultats

Chiffres tirés de tableaux dont le corps est reconstruit de façon désordonnée par l'extraction (Tables 1 à 4) ; à recouper avec le PDF avant toute citation. Lecture proposée :
- MNIST, instances résolues (Table 1, ε = 1..4 ; Baseline+Lingeling / Baseline+CaDiCaL / Ours) : 63 (63,6 %), 0, 0, 0 / 92 (92,9 %), 20 (20,2 %), 2 (2,1 %), 1 (1,0 %) / 99 (100 %), 94 (94,9 %), 71 (74,0 %), 54 (55,7 %). Les dénominateurs varient d'un ε à l'autre : 100 échantillons pour ε = 1, 100 pour ε = 2, 200 pour ε = 3 et ε = 4 (§ Experimental Evaluation).
- Fashion-MNIST (Table 3, fragment extrait) : à ε = 1, 2, 3, 4 : 2 (2,3 %) / 44 (50,6 %) / 76 (87,4 %), 0 / 7 (7,8 %) / 73 (81,1 %), 0 / 1 (2,3 %) / 27 (62,8 %), 0 / 0 / 18 (40,9 %) (baseline Lingeling / baseline CaDiCaL / ours). Affectation des colonnes déduite de la forme du tableau.
- Temps (Table 2, médiane|moyenne par échantillon résolu, unité non extraite, probablement secondes, déduit) : MNIST 8803|8789 (Lingeling), 2798|3931 (CaDiCaL), 5|90 (ours) ; Fashion-MNIST 6927|6927, 3105|3474, 4|49. Les auteurs annoncent un gain jusqu'à trois ordres de grandeur sur les outils existants (Abstract).
- Ablation MNIST (Table 4) : tout activé 318 résolus (81,3 %) en 7,9 h cumulées ; sans simplification ReLU 88 (22,5 %) ; sans interprétation abstraite 107 (27,4 %) ; sans redondance de multiplications 316 (80,8 %) ; sans largeur minimale 315 (80,6 %). L'essentiel du gain vient de la simplification ReLU ; les deux autres techniques comptent peu, ce que les auteurs attribuent à la recherche locale de Boolector (hypothèse non testée).
- Pas de ligne dans `benchmarks.csv` : aucune mesure de type FPS, puissance ou ressources FPGA (`benchmarks: none`).

## Limites et critique

- Échelle : un seul réseau, 4 couches denses de 52 k paramètres sur MNIST/Fashion-MNIST ; les auteurs reconnaissent que les réseaux vérifiés en général sont minuscules par rapport aux détecteurs d'objets (§ Limitations). Aucune couche convolutive ni détecteur ; YOLO est hors de portée (déduit).
- Le taux de résolution chute quand ε augmente (ε = 4 : 55,7 % sur MNIST ; 40,9 % sur Fashion-MNIST) : la méthode reste incomplète en pratique (délais d'expiration ; timeout non précisé dans le texte lu).
- La propriété vérifiée est la robustesse `l∞` d'une classification ; pas de spécification sémantiquement liée à un danger (cf. la critique de la robustesse ponctuelle en pixels dans AMLAS, Note 35, rapprochement fait par le rédacteur de la fiche).
- Le modèle vérifié est l'interprétation à point fixe décrite (éq. 3-5) ; l'équivalence avec une implémentation RTL/HLS réelle (débordements, arrondis, ordre de sommation) n'est pas démontrée ici ; c'est à l'utilisateur de faire correspondre la sémantique (déduit).
- Résultat de complexité : la borne PSPACE-hard vaut pour des spécifications bit-vector riches ; pour les spécifications linéaires usuelles la question est ouverte (les auteurs le disent, § Hardness).
- Comparaison à une seule baseline (Giacobbe et al. 2020) et un seul solveur (Boolector) ; les autres solveurs sont écartés d'après leur mauvaise performance dans le travail cité, non re-mesurée.
- Extraction : corps des Tables 2, 4, 5 partiellement reconstruit ; Table 1 mélangée avec Table 3.

## Pertinence pour la thèse

Dans l'axe « sûreté et certification » : c'est l'un des rares travaux qui vérifie formellement la sémantique bit-exacte d'un réseau quantifié, donc celle qui s'exécute sur FPGA (multiplications entières, arrondi par décalage, saturation ReLU-N), et non un modèle flottant. Utile comme brique de preuve de « model verification » (AMLAS, Stage 5, vérification formelle) et pour argumenter que la quantification ne peut pas être ignorée dans un dossier de certification. Ne passe pas à l'échelle d'un détecteur YOLO ; la thèse devra donc soit vérifier des sous-composants (tête de classification, moniteur d'exécution, réseau de surveillance de petite taille), soit viser des garanties statistiques. Le résultat de complexité fournit un argument théorique pour justifier de telles limites. La ressemblance entre son arithmétique (poids entiers, décalage de k_i bits, ReLU-N) et celle des accélérateurs de type FINN/DPU est une inférence, non affirmée par les auteurs.

## Gaps identifiés

- Vérification formelle bit-exacte de réseaux convolutifs quantifiés de taille de détecteur d'objets : hors de portée aujourd'hui.
- Lien formel entre l'interprétation vérifiée (point fixe) et l'implémentation RTL/HLS/bitstream réellement déployée sur FPGA.
- Spécifications formelles pertinentes pour la détection de personnes (au-delà de la robustesse `l∞` sur pixels).
- Vérification de réseaux binaires/ternaires et de tête de réseau (moniteurs OOD) comme sous-problème faisable.

## Statut de lecture

Papier complet (fulltext.md lu en entier, y compris la preuve en annexe). Extraction grobid, ok. Tables 2, 4, 5 et Table 1/3 : corps reconstruits de façon désordonnée (avertissement d'extraction) ; les chiffres ci-dessus sont une lecture recoupée avec les pourcentages, mais l'attribution colonnes/tableaux est déduite, et l'unité des temps est non extraite. Le Table 5 (règles de redondance) est illisible.
Ce qui suit est déduit et non affirmé par les auteurs : l'incapacité à passer à l'échelle d'un YOLO ; l'écart entre sémantique vérifiée et implémentation RTL ; la proximité avec les arithmétiques FINN/DPU ; les unités de temps.
