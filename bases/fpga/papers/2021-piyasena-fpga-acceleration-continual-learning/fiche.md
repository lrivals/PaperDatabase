---
id: 2021-piyasena-fpga-acceleration-continual-learning
fiche: done
date: 2026-09-29
---

# FPGA Acceleration of Continual Learning at the Edge

Duvindu Piyasena, 2021, PhD thesis, Nanyang Technological University (Singapour). https://hdl.handle.net/10356/153778
Type : thèse de doctorat (les chapitres 3 à 5 ont été publiés à FPL 2020 et FPL 2021, dont un poster FCCM 2021 ; non vérifié ici au-delà de la mention du texte)

## Problème

Les systèmes d'IA embarquée n'exécutent que l'inférence : le modèle est entraîné dans le cloud, et apprendre de nouveaux objets impose de renvoyer les données au cloud (latence, vie privée, dépendance réseau) (§1.1.2). Réentraîner un CNN sur la cible est trop coûteux, et un apprentissage incrémental naïf souffre d'oubli catastrophique. L'objectif est un apprentissage continu de classification d'objets, en ligne (streaming, mono-tête, class-incremental), sur FPGA avec faible latence, faible surcoût énergétique et passage à l'échelle en nombre de classes (§1.2).

## Méthode

Backbone CNN gelé (transfer learning) + classifieur incrémental entraîné sur l'embedding (Fig. 2.4) :
- Ch. 3 : accélérateur d'un réseau auto-organisé croissant (SONN, dérivé de Grow-When-Required) : matrice de PE systolique organisée en colonnes, poids en BRAM, approximations (INT8, taux d'apprentissage en puissance de 2, seuil de distance à la place de l'exponentielle, habituation en ROM), Verilog (§3.2-3.4).
- Ch. 4 : accélérateur de Deep SLDA (Streaming Linear Discriminant Analysis) : cœur GEMM à tuiles + unité vectorielle, ISA à 2 instructions, virgule fixe mixte FxP<16,32> issue d'une analyse de sensibilité, scratchpad L1/L2, variantes PlasticCov / DiagCov / StaticCov (compromis précision/efficacité), Vitis HLS (§4.2-4.4). Le calcul des poids d'inférence (inversion de covariance) reste sur l'ARM.
- Ch. 5 : driver Linux `Zynqmmapdrv` (mapping PS-PL, DMA contigu) pour supprimer la latence hôte (~150 us via OpenCL, §4.4) ; pipeline complet DPU (ResNet18, B4096) + SLDA sur la même puce, flot Vitis AI + Vivado + Petalinux (Fig. 5.4).

## Plateforme et implémentation

ZCU102 (XCZCU9EG). SONN : Verilog, Vivado 2019.1, 200 MHz (§3.5.2) ; SLDA : Vitis HLS, Vivado 2020.x, 200 MHz ; DPU : Vitis AI 1.3, B4096 (§5.4). Ressources : SONN dans les Tables 4.3/5.1 (115 656 LUT, 1 184 DSP, 415,5 BRAM ; paramètres de conception en Table 3.2 dont les intitulés de colonnes sont illisibles à l'extraction : 2048 neurones max, 8096 connexions max, 200 MHz), Table 5.4 pour le pipeline (DPU seul 58 703 LUT / 704 DSP / 261 BRAM ; +SLDAPlasticCov 142 215 / 1 616 / 553,5). Puissance : outil « ZCU102 Board Interface » sur rails de la carte (statique / totale, ex. 4,42 / 8,16 W pour le DPU seul), portée exacte non précisée (`unspecified`) ; CPU via RAPL, GPU via nvidia-smi (§3.5.2). Code / bitstream : non publiés (aucun lien dans le texte lu).

## Résultats

- Modèle (CoRE50, NC, Table 4.1) : SLDAPlasticCov 80,79 % objet / 91,46 % catégorie, DiagCov 74,34 / 87,41, StaticCov 72,78 / 86,12, SONN 66,12 / 85,01, ExStream 71,49 / 83,76 ; offline 90,08 / 95,24. Mémoire SLDA Diag/Static 0,20 MB, Plastic 1,20 MB. CUB200 : Plastic 62,98 % (offline 60,54 %, valeur telle qu'extraite).
- SONN vs CPU/GPU : latence 231x et 416x, puissance 9x et 6x (§3.5.2). Le SONN grossit avec les classes (mémoire et latence croissantes, §4.1), ce qui motive le SLDA.
- SLDA FxP vs FP32 : au moins 40 % de LUT/DSP/FF en moins (§4.4). Avec Zynqmmapdrv, PlasticCov 47,85 us, 3,97 W ; 24x / 4x plus rapide et 25x / 6x plus économe en énergie que ARM A53 / Jetson Xavier NX ; DiagCov 8,3 us, 3x / 12x (Table 5.2). Cas contraire : StaticCov, ARM A53 (2,80 us) plus rapide que le FPGA (4,76 us).
- Pipeline complet (Table 5.4) : DPU seul 170,20 FPS, 5,875 ms, 8,16 W, 0,048 J/image ; +SLDAPlasticCov 168,67 FPS, 9,00 W, 0,056 J, 78,79 / 89,46 % ; +SLDADiagCov 169,96 FPS, 8,69 W, 0,054 J, 71,81 / 85,37 %. Surcoût latence 0,9 % et 0,1 %, énergie +16,67 % et +12,5 % (§5.4).
→ reportés dans `benchmarks.csv` (via `bench_rows.csv`) : 7 lignes (SONN ; SLDA Plastic/Diag/Static avec driver ; DPU seul ; pipeline DPU+Plastic ; pipeline DPU+Diag), `confidence: medium` (tableaux Docling ou fragments de texte).

## Limites et critique

- Toutes les expériences sont des classifications d'objets isolés (CoRE50, CUB200) sur ResNet18 : pas de détection (YOLO) ni de flux vidéo réel ; l'extracteur de caractéristiques est gelé, donc pas d'adaptation de la représentation (déduit de la conception).
- Les accélérateurs n'entraînent que le classifieur ; les latences (us) portent sur ce classifieur, pas sur le CNN, sauf le pipeline (Table 5.4, ~5,9 ms dominé par le DPU).
- Comparaisons CPU/GPU hétérogènes (Jetson TX1 au Ch. 4, Xavier NX au Ch. 5, PyTorch pour SONN), incluant ou non l'hôte ; puissance de repos incluse ou non (« static / total ») ; la puissance FPGA est sur rails de carte (déduit) alors que RAPL / nvidia-smi mesurent autrement : les facteurs d'énergie sont fragiles.
- Aucune analyse de sûreté, de déterminisme temporel, de robustesse aux fautes ; l'apprentissage en ligne rend la certification bien plus difficile (comportement évolutif) : problème non discuté. Les attaques par injection de fautes ne sont évoquées que comme travail futur en sécurité (§6.2.5).
- Le texte extrait est incomplet (voir Statut de lecture) ; les chiffres de Tables 3.3-3.5 (latences par étape SONN, puissances CPU/GPU) manquent en grande partie.

## Pertinence pour la thèse

Référence de base sur l'apprentissage continu embarqué sur FPGA (SLDA, SONN) et sur l'intégration DPU + accélérateur custom sur une même puce Zynq UltraScale+, plateforme proche de celle d'une thèse Xilinx. Deux pistes en lien avec la sûreté : §6.2.3 propose d'utiliser la distance de Mahalanobis du SLDA pour détecter un échantillon nouveau / OOD (compatible avec un moniteur d'exécution) ; la variante StaticCov (covariance figée) donne un comportement plus prédictible. Le papier laisse ouverte toute la question de la certification d'un système qui apprend en ligne, et l'application à la détection de personnes.

## Gaps identifiés

- Apprentissage continu sur FPGA pour de la détection d'objets (YOLO), pas seulement de la classification.
- Assurance / certification d'un modèle qui apprend en service (gel de la représentation, rollback, contrôle de dérive).
- Détection OOD par Mahalanobis dans SLDA sur FPGA (proposé en §6.2.3, non réalisé).
- Fiabilité (SEU, fautes) d'un accélérateur d'apprentissage continu non étudiée.

## Statut de lecture

Texte lu en entier (fulltext.md, 960 lignes), mais l'extraction est dégradée : « Abstract » = remerciements, sections 1 et 2 non détectées (une partie du §1.1.2 et de la présentation des contributions, chapitre 1, est tronquée), équations et symboles corrompus (Ch. 3-4), Tables 3.3-3.5 et Table 4.2 (sensibilité en virgule fixe) partielles ou absentes, Tables 4 et 5 reconstruites par Docling (chiffres à vérifier, numérotation des tableaux ambiguë : « Table 4.1 » et suivantes recoupées avec le texte des §4.4 et §5.4).
Déduit et non affirmé par les auteurs : portée de la puissance (`unspecified`), lecture de la latence SONN (0,00435 ms = « avec hôte », Table 4.3/5.1), limites sur le gel du backbone, absence de sûreté.
