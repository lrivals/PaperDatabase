---
id: 2021-piyasena-accelerating-continual-learning-edge-fpga
fiche: done
date: 2026-09-29
---

# Accelerating Continual Learning on Edge FPGA

Duvindu Piyasena, Siew-Kei Lam, Meiqing Wu, 2021, 2021 31st International Conference on Field-Programmable Logic and Applications (FPL), pp. 294-300. DOI 10.1109/FPL53798.2021.00059 ; https://doi.org/10.1109/FPL53798.2021.00059
Type : conférence (FPL 2021, relue par les pairs).

## Problème

Les accélérateurs CNN sur FPGA ne font que de l'inférence ; l'apprentissage par rétropropagation est trop coûteux en calcul et en mémoire pour l'edge, et les CNN classiques oublient catastrophiquement (§I). Il s'agit de permettre un apprentissage continu class-incremental en flux (streaming) directement sur l'accélérateur edge, sans aller-retour serveur (§I).

## Méthode

- Modèle : Deep SLDA (streaming linear discriminant analysis) : un CNN pré-entraîné sur ImageNet, ici ResNet18 avec les features de l'Avg Pool (D = 512), gelé et jouant le rôle d'extracteur ; SLDA remplace la dernière couche FC et met à jour incrémentalement la moyenne par classe et une covariance partagée (Eq. 1 à 8, §III-A).
- Variante proposée SLDADiagCov : seule la diagonale de la covariance est mise à jour, d'où une économie « au mieux » de D(D-1)/2 paramètres et de 3D(D-1)/2 multiplications (§III-B). Autres variantes de la référence [10] : PlasticCov (covariance mise à jour à chaque échantillon) et StaticCov (covariance figée).
- Accélérateur (Fig. 2, 3) : cœur GEMM (tableau T x T d'éléments de calcul, dataflow output-stationary) + unité vectorielle (VPU) + mémoire scratchpad à deux niveaux (L1/L2) + jeu d'instructions à deux instructions (GEMMOP, VECOP) (§IV). Optimisations : saut de tuiles (seule la moitié triangulaire supérieure de la covariance symétrique est calculée), virgule fixe à précision mixte (analyse de sensibilité par groupes), suppression d'éléments de calcul inutilisés pour DiagCov et StaticCov, réutilisation sur puce (§IV-E).
- Le calcul des poids et du biais (Eq. 4 à 6, incluant l'inversion de matrice) reste sur l'hôte ARM (§IV-D).
- Système complet : SLDA combiné à un ResNet18 sur DPU Xilinx, quantifié et compilé avec Vitis AI 1.3 (§V-E, Fig. 8).

## Plateforme et implémentation

- Puce : Xilinx ZCU102 (ZU9EG), 200 MHz, Vitis HLS C++ sous Vivado 2020.2, tuile T = 16 (grille 16x16) ; pilote Linux et application hôte (§V-E). DPU B4096, un cœur (Table V, note).
- Puissance : lue sur les rails d'alimentation de la carte avec l'outil d'interface de la carte ZCU102, valeurs statique/totale (§V-E, Table III à V) ; pas de précision sur la portée puce ou carte : `power_scope = unspecified`. Le tableau donne le total (p. ex. 8,16 W pour le DPU seul).
- Latence mesurée depuis l'application hôte (§V-E). Comparaisons : CPU ARM A53 de la ZCU102 (C++/Eigen) et GPU Jetson Xavier NX (cuBLAS + noyaux CUDA) (§V-E). Modèles PyTorch mesurés sur GTX1080 pour le temps d'entraînement de la Table I (§V-C).
- Code, bitstream : non publiés d'après le texte (aucun lien).

## Résultats

- Modèles (Table I, top-1, objet/catégorie sur CoRE50) : Offline 90,08 / 95,24 ; ExStream 71,49 / 83,76 ; SONN 66,12 / 85,01 ; SLDAStaticCov 72,78 / 86,12 ; SLDADiagCov 74,34 / 87,41 ; SLDAPlasticCov 80,79 / 91,46 ; Naive 2 / 10,09. Sur CUB200 (Table I) : Offline 60,54 ; SLDAPlasticCov 62,98 ; SLDADiagCov 61,11 ; SLDAStaticCov 58,26 ; SONN 44,85 ; ExStream 52,46. Ajouter une classe coûte 4 Ko de mémoire, sans effet sur la latence d'entraînement (§V-C). Mémoire des paramètres (Table I, CoRE50) : StaticCov et DiagCov 0,20 Mo, PlasticCov 1,20 Mo, ExStream 4,54 Mo (params + données).
- Virgule fixe (Table II ; corps de tableau dégradé, lu avec prudence) : le groupe 1 (activations, moyennes, poids) tient à 16 bits sans perte, le groupe 2 (covariance, biais) nécessite 32 bits pour PlasticCov, d'où une précision mixte 16/32 (§V-D). Effet matériel (Table III) : au moins 40 % de DSP et FF et 30 % de LUT en moins ; PlasticCov latence et puissance réduites d'environ 60 % et 20 % (§V-E).
- Accélérateur seul, virgule fixe (Table III et IV) : PlasticCov 47,85 us par échantillon d'entraînement, 3,97 W total, 73 435 LUT, 914 DSP ; DiagCov 8,30 us, 3,34 W ; StaticCov 4,76 us, 3,34 W. Contre CPU ARM A53 : 1 159,21 us (PlasticCov, facteur 24,23), 25,69 us (DiagCov, 3,09) ; contre GPU Xavier NX : 182,01 us (3,80), 98,25 us (11,84), 76,07 us (15,98) ; énergie par échantillon PlasticCov : FPGA 1,90E-04 J, CPU 4,68E-03 J, GPU 1,18E-03 J (Table IV). Pour StaticCov, le CPU est plus rapide que le FPGA (2,80 us contre 4,76 us, facteur 0,59) (Table IV).
- Système complet DPU + SLDA (Table V ; corps reconstruit par Docling, à vérifier) : DPU seul 170,20 FPS, 5 875,44 us, 8,16 W, 0,048 J/image ; DPU + PlasticCov 168,67 FPS, 5 929,00 us, 9,00 W, 0,056 J/image, précision 78,79 (objet) / 89,46 (catégorie) ; DPU + DiagCov 169,96 FPS, 5 883,70 us, 8,69 W, 0,054 J/image, 71,81 / 85,37. Transfert des features vers le SLDA via l'hôte ARM : environ 600 ns de délai (§V-E). Conclusion des auteurs : apprentissage à presque la même latence que l'inférence.
→ reportés dans `benchmarks.csv` : 9 lignes (6 pour l'accélérateur SLDA seul, FP32 et virgule fixe, 3 pour le système DPU / DPU + SLDA). Les lignes se trouvent dans `bench_rows.csv` de ce dossier, à fusionner (agent principal). Sources : Tables I, III, IV, V. Puissance : total lu dans les tableaux, portée `unspecified`. Les chiffres du CPU et du GPU (Table IV) ne sont pas ajoutés en lignes propres ; ils figurent dans la colonne baseline et ci-dessus.

## Limites et critique

- Le calcul des poids et du biais (inversion de la covariance, Eq. 4 à 6) est laissé à l'hôte ARM et n'apparaît pas dans les latences par échantillon ; le coût de cette étape (et sa fréquence) n'est pas donné.
- Seule la dernière couche est apprise : le CNN reste figé (ResNet18 pré-entraîné sur ImageNet), donc pas d'adaptation des features à un domaine très différent ; évalué en classification (CoRE50, CUB200), pas en détection.
- Comparaisons CPU/GPU : logiciel maison (Eigen, cuBLAS/CUDA), Jetson Xavier NX pour le GPU ; dans le cas de StaticCov, le CPU bat le FPGA (Table IV). L'avantage FPGA n'est pas général : il dépend de la variante.
- Puissance : lue sur les rails de la carte avec statique et total, portée non précisée ; les comparaisons d'énergie avec le CPU et le GPU (autres cartes) mélangent des portées probablement différentes (déduit, non dit).
- Le DPU et son coût dominent le système (5,9 ms de latence, 8 à 9 W) : le coût de l'apprentissage semble faible car il est négligeable devant celui du CNN ; à 170 FPS, le débit n'est pas celui d'un détecteur de type YOLO.
- Nouveauté « premier système d'apprentissage continu complet sur FPGA » : affirmation des auteurs, non vérifiée.
- Table V reconstruite par Docling : chiffres à vérifier (cohérents avec le texte : FPS et latence concordent, 1/5,87544 ms = 170 FPS). Table II en partie illisible.

## Pertinence pour la thèse

Axe apprentissage continu embarqué sur FPGA, avec un vrai matériel (ZCU102), un système complet DPU + apprentissage, et des mesures comparées à CPU et GPU : c'est l'un des rares exemples d'apprentissage continu sur FPGA de la base. Il montre un schéma « backbone figé quantifié (DPU) + tête apprise en virgule fixe » compatible avec un flot Vitis AI. Pour la thèse (YOLO sûr et certifiable) : intéressant pour le principe de figer la partie coûteuse et de n'apprendre qu'un module léger, plus simple à vérifier ; mais il ne traite pas la détection, ni la sûreté ou la fiabilité de l'apprentissage en ligne. Ouvert : passage à un détecteur (têtes YOLO), garanties de non-régression, mise à jour de la partie hôte (inversion).

## Gaps identifiés

- Apprentissage continu sur FPGA pour la détection d'objets (ici, classification uniquement).
- Garanties de sûreté / non-régression d'un apprentissage en ligne sur FPGA (aucune traitée).
- Mesure de puissance de portée non précisée : comparabilité avec les autres accélérateurs de la base à établir (`power_scope`).

## Statut de lecture

Papier complet (fulltext.md lu en entier ; extraction GROBID, tableaux Docling : Table V reconstruit, à vérifier ; Tables I à IV extraits avec une mise en forme partiellement dégradée, recoupés avec le texte et entre eux : p. ex. les latences des Tables III et IV concordent). Déduit et non affirmé par les auteurs : la portée de la puissance (choisie `unspecified`), l'intérêt pour un backbone figé dans une chaîne certifiable, le fait que le coût de l'inversion hôte manque dans les latences, la comparaison des portées de puissance avec le CPU et le GPU.
