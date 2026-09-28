---
id: 2024-zhang-comprehensive-analysis-dac-sdc-fpga
fiche: done
date: 2026-09-28
---

# A comprehensive analysis of DAC-SDC FPGA low power object detection challenge

Jingwei Zhang, Guoqing Li, Meng Zhang, Xinye Cao, Yu Zhang, Xiang Li, Ziyang Chen, Jun Yang, 2024, Science China Information Sciences 67(8), 182401. https://doi.org/10.1007/s11432-023-3958-4
Type : article de journal

## Problème

Le Low Power Object Detection Challenge (LPODC) de DAC-SDC évalue sur la même plateforme
embarquée la précision, le débit et l'énergie d'un détecteur sur images de drone (§1). Les
auteurs (équipe SEUer, Southeast University, championne 2022) constatent que les analyses
existantes se limitent à l'édition 2018 (Xu et al. [15]) ou tiennent en deux pages
(Jia et al. [16]) (§1). Ils proposent une analyse de toutes les solutions du Top-3 FPGA de
2018 à 2022 et en tirent des règles de co-design algorithme ↔ matériel.

## Méthode

Analyse de concours, sans nouvelle méthode, sauf la description de leur propre design 2022.
- **Cadre du concours** (§2) : jeu DJI-UAV, 12 catégories, 95 sous-catégories, un seul
  objet par image, 100 000 images d'entraînement, 1 000 de validation, 52 500 de test cachées ;
  la plupart des objets occupent 1 à 2 % de l'image 640×360 (§2.1). Métrique : IoU moyen,
  sans classe (§2.3). FPS mesuré par le code officiel, énergie = puissance mesurée au
  wattmètre sur la carte (100 Hz avant 2020, 20 Hz ensuite) × durée (§2.3). Deux formules de
  score, avec des seuils IoU 0,7 et FPS 30 à partir de 2021 (Éq. 3-4). En 2022, le temps ne
  compte plus que l'exécution sur la PL, pas le chargement des images (§2.3).
- **Designs Top-3 par année** (§3) : réseau, quantification, architecture (moteur de calcul
  unique contre streaming), ressources (Tables 2 à 6).
- **Analyse transversale** (§4) : score total recalculé avec la formule 2022, après
  compensation de la puissance (×0,8 pour le 28 nm) et du nombre de DSP pour 2018 (§4.1,
  Fig. 10) ; tendances IoU, poids et multiplications (Fig. 11), quantification (Fig. 12),
  FPS/DSP et GOPS/W (Fig. 13).
- **Leur design 2022 (SEUer)** (§3.5) : UltraNet entraîné par iSmart en 2021, W4/A4,
  architecture streaming, **DSP packing non signé (uint-packing) DSP6**, qui demande moins de
  LUT que l'int-packing, domaines d'horloge multiples (IP rapide, reste lent) et prétraitement
  d'image accéléré (−0,005 d'IoU). Toolflow : n/r pour SEUer (HLS pour la plupart des autres
  équipes).

## Plateforme et implémentation

- 2018 : PYNQ-Z1 (Zynq-7000 XC7Z020, 28 nm, 53k LUT, 220 DSP, 4,9 Mo de BRAM, DDR3 512 Mo) ;
  2019 : Ultra96 V1 ; 2020-2022 : Ultra96 V2 (Zynq UltraScale+ ZU3EG, 16 nm, 71k LUT,
  360 DSP, 7,6 Mo de BRAM, DDR4 2 Go) (Table 1, §2.2). Alimentation 4 A à partir de 2020
  (§2.2).
- Catégorie GPU (Jetson TX2) seulement en 2018-2019, exclue de l'analyse (§1).
- **Puissance** : mesurée par l'organisateur au wattmètre sur la carte FPGA (§2.3), donc
  portée `board`. Le V2 a d'autres régulateurs que le V1, ce qui rend les mesures 2019 et
  2020+ non strictement comparables (§2.2).
- SEUer 2022 : 50,0k LUT, 345 DSP, 4,8 Mo de BRAM, 45,0k FF (Table 6). Fréquences : n/r.
- Code : les designs des équipes sont publiés par les organisateurs (dépôts
  `jgoeders/dac_sdc_20xx_designs` cités en notes 2 à 4) ; celui de SEUer n'est pas lié
  explicitement.

## Résultats

Champions et design des auteurs (valeurs mesurées par l'organisateur) :

| Année | Équipe | Réseau, précision | IoU | FPS | GOPS | P (W) | Énergie (J) | Source |
|---|---|---|---|---|---|---|---|---|
| 2018 | TGIIF | SSD, W8/A8 | 0,624 | 12,0 | 56,5 | 4,2 | 18 444,2 | Table 2 |
| 2019 | iSmart3 | SkyNet, W11/A9 | 0,716 | 25,1 | 23,2 | 7,26 | 15 215,6 | Table 3 |
| 2020 | BJUT Runner | UltraNet, W4/A4 | 0,656 | 212,7 | 85,1 | 6,65 | 1 641,2 | Table 4 |
| 2021 | Skrskr | SkyNet, W5/A8 | 0,716 | 299,3 | 277,1 | 3,77 | 661,1 | Table 5 |
| 2022 | **SEUer (auteurs)** | UltraNet, W4/A4 | 0,703 | 2 020,6 | 808,2 | 1,41 | 36,7 | Table 6 |

- Le streaming apparaît en 2020 (BJUT Runner) et domine le Top-3 en 2021-2022 (§3.3, §3.5).
- Le DSP packing (DSP2, DSP4, DSP6) domine en 2021-2022 (§3.4).
- Depuis 2020, tous les Top-3 utilisent UltraNet ou SkyNet ; en 2022 il n'y a plus de gain
  d'IoU, seulement d'efficacité matérielle (§4.2).
- Recommandation (§4.5) : W8/A8 + DSP2 pour la haute précision, W4/A4 + DSP6 pour la basse
  consommation, W3/A5 à envisager ; les poids ne doivent pas descendre sous 3 bits (constat
  des auteurs, sans tableau à l'appui).

→ reportés dans `benchmarks.csv` : **15 lignes**, les Top-3 FPGA de 2018 à 2022 (Tables 2 à
6), dont la ligne SEUer 2022 des auteurs. Ce sont des mesures officielles du concours
compilées par les auteurs, comme pour `2021-xu-dac-sdc-low-power-object`.
`power_scope = board`. BRAM en Mo dans le papier, donc `bram = n/r` (la colonne attend des
blocs). Latence : n/r.

## Limites et critique

- **IoU mono-objet, pas mAP multi-classe.** L'IoU DAC-SDC ignore la classe et suppose un
  seul objet par image (§2.3). Il n'est pas comparable au mAP de VisDrone ou UAVDT.
- **Le FPS 2022 exclut le chargement des images** (§2.3). Les 2 020 FPS de SEUer ne sont pas
  un débit système de bout en bout ; le saut de 2021 à 2022 (×6,8 en FPS, énergie ÷18) vient
  en partie de ce changement de règle, ce que les auteurs admettent (§4.1).
- **Ultrateam : 2 266,2 FPS** présenté dans le texte comme un débit « théorique » alors que
  la Table 6 le range avec les mesures, et le texte dit aussi que le gain réel est d'environ
  10 % sur SEUer (§3.5). Ambiguïté non levée.
- **Normalisations maison** (§4.1, §4.4) : compensation 0,8 de la puissance 28 nm → 16 nm
  (fiche technique Xilinx) et des FPS au prorata des DSP. Elles ne sont que des
  approximations, et le score total recalculé (Fig. 10) n'est pas donné en chiffres dans le
  texte extrait.
- **Une seule plateforme, un seul modèle en 2022** : UltraNet (8 couches conv 3×3 + PWC,
  210k poids) est très loin des YOLO drone actuels ; les conclusions sur la quantification
  (W4/A4, W3/A5) ne sont pas démontrées sur des modèles multi-échelles avec tête P2 (déduit).
- **Pas de comparaison avec un GPU embarqué** : la catégorie Jetson TX2 est exclue (§1).
- **Juge et partie** : les auteurs sont champions 2022 ; leur propre contribution (uint-
  packing, multi-horloges) est décrite sans ablation chiffrée (§3.5).
- Petites incohérences de rédaction : « 6th place in 2020 » répété pour 2021 (§3.4) ;
  « system peak power of 268 GOPS » pour HiPU (§3.2).

## Pertinence pour la thèse

- **Axe `drone-fpga` et `datasets-benchmarks`** : la table de référence la plus complète du
  corpus pour la gamme FPGA (1,4 à 9,2 W carte) sur images de drone, avec une mesure de
  puissance homogène à la carte, ce qui est rare.
- **Montre l'effet de la règle de mesure sur le résultat** : exclure le chargement des images
  multiplie le FPS, argument pour mesurer de bout en bout dans la thèse.
- **Enseignements réutilisables** : streaming + poids sur puce + W4/A4 + DSP packing est la
  recette gagnante sur un petit ZU3EG. Mais elle suppose un réseau minuscule, sans rapport
  avec les détecteurs multi-classes de petits objets.
- Ce qu'il laisse ouvert : pas de mAP_small, pas de multi-objet, pas de lien avec le vol.

## Gaps identifiés

- **Écart DAC-SDC ↔ VisDrone** : les recettes gagnantes (UltraNet W4/A4 streaming) n'ont
  pas été évaluées en multi-objet multi-classe ; le coût de passer à une tête YOLO
  multi-échelle sur ZU3EG n'est pas mesuré (appuie l'hypothèse « YOLO drone SOTA rarement
  portés sur FPGA »).
- **Quantification ↔ petits objets** : les objets font 1 à 2 % de l'image (§2.1), mais
  l'effet de W4/A4 n'est rapporté qu'en IoU moyen, jamais par taille d'objet.
- **Aucune métrique système** (latence de bout en bout, autonomie) ; le FPS 2022 exclut même
  les E/S.

## Statut de lecture

Papier complet (`fulltext.md` lu en entier, extraction GROBID `ok`). `extraction.warnings`
signale la Table 2 comme « sans corps extrait » : son corps figure pourtant dans la section
« Figures et tableaux », avec un décalage de colonne pour iSmart2 ; ses valeurs d'IoU, FPS,
énergie et ressources sont recoupées par le texte (§3.1), mais pas GOPS ni puissance
(ligne iSmart2 en `confidence: medium`). Les Figures 10 à 13 (score total recalculé, FPS/DSP,
GOPS/W) n'ont pas de valeurs dans le texte extrait. Les sections 3 et 4 ne sont pas détectées
comme titres.

Ce qui suit est déduit et non affirmé par les auteurs :
- la part du changement de règle 2022 dans le saut de FPS (les auteurs le reconnaissent pour
  le score, pas chiffré) ;
- la non-transférabilité des recettes W4/A4 aux YOLO multi-échelles ;
- la portée `board` : déduite de « a power meter is used on the FPGA board » (§2.3).
