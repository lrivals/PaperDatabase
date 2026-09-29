---
id: 2024-zhang-end-end-acceleration-yolo-object
fiche: done
date: 2026-09-29
---

# End-to-end acceleration of the YOLO object detection framework on FPGA-only devices

Dezheng Zhang, Aibin Wang, Ruchan Mo, Dong Wang, 2024, Neural Computing and Applications 36(3), 1067-1089. https://doi.org/10.1007/s00521-023-09078-8
Type : article de journal

## Problème

Les accélérateurs YOLO existants soit mappent un réseau complet en pipeline (YOLOv2-Tiny, contraint par les ressources, non reprogrammable pour des réseaux plus profonds), soit utilisent des données 16/18 bits coûteuses en DSP et en bande passante, et laissent le pré/post-traitement (sigmoïde, exponentielle, softmax, IoU, NMS) à un CPU. Sur les FPGA « seuls » (sans cœur ARM, seulement un soft-core MicroBlaze), ce post-traitement doit être matériel pour tenir une latence de bout en bout faible (§1, §3.5).

## Méthode

Accélérateur à couches séquentielles (donc YOLOv2, YOLOv3 et variantes Tiny) : réseau de PE (N_r unités de calcul x N_p PE, chaque PE avec N_n DSP48 effectuant deux multiplications 8 bits par DSP par empaquetage via le pré-additionneur, §3.1), tampons de lignes en ping-pong, unités d'accès mémoire à rafales (feature load, weight load, feature store), ordonnanceur de tâches qui ne synchronise que quand un groupe de calcul est terminé (§3.2-3.4). Parallélisme sur canaux de sortie, lignes de sortie, MAC internes et batch. Ordonnancement A (réutilisation des features) retenu contre B (poids) via le modèle Roofline (§4.4). Quantification INT8 dynamic fixed-point avec BRECQ après fusion de la batch-norm ; la couche de sortie est scindée en deux convolutions (position et classes) pour quantifier séparément deux distributions différentes (§2.2-2.3). Post-traitement matériel : décodage des coordonnées par LUT à 256 entrées, softmax, unité NMS économe (sans tri, inspirée de [10]) (§3.5). Exploration de l'espace de conception par modèles de performance et de ressources, contrainte de 70 % de ressources (§4). HLS paramétré, Vitis HLS / Vivado 2021.2 (§5.1) ; un MicroBlaze envoie des instructions grossières.

## Plateforme et implémentation

Deux cartes : KC705 (Kintex-7 XC7K325T : 203 k LUT, 840 DSP, 16 Mbit BRAM, DDR3 1 Go) et VC709 (Virtex-7 XC7VX690T : 433 k LUT, 3600 DSP, 52,9 Mbit BRAM, deux DDR3 de 4 Go) (§5.1). Paramètres retenus : XC7K325T N_n=8, N_m=12, N_r=13, N_b=1, 200 MHz ; XC7VX690T N_m=16, N_b=1 ou 2, 180 puis 160 MHz (§4.3, §5.1, Table 3). Puissance : puce estimée par l'analyseur de puissance de Vivado (donc `estimated`), carte entière mesurée par un wattmètre externe (§5.1) ; la colonne `power_w` de `benchmarks.csv` prend la mesure carte, `power_scope: board`. Latence par couche mesurée avec le timer logiciel du MicroBlaze. Code ou bitstream : non publiés (aucun lien dans le texte).

## Résultats

- XC7VX690T : 525 GOP/s à batch 1 et 914 GOP/s à batch 2 pour YOLOv2 (résumé, Table 3, §5.2), 859 GOP/s pour YOLOv3 à batch 2 (Table 4, §6), mAP VOC 76,7 % (YOLOv2) et 75,4 % (YOLOv3) en INT8 (Tables 3-4). Puissance à batch 2 : 12,5 W puce (estimée) / 24,1 W carte (Table 3).
- XC7K325T : 418 GOP/s YOLOv2, 401 GOP/s YOLOv3-Tiny, latence bout en bout 14,49 ms (YOLOv2-Tiny, 416x416, §5.3) et 15,2 ms (YOLOv3-Tiny, Table 5) ; puissance 7,8 W puce / 12,3 W carte.
- Post-traitement matériel : 845 boîtes traitées en 0,38 ms, 8 893 LUT, 19 DSP, 20,5 BRAM 18k (Table 2).
- Face aux références des auteurs (Tables 3-5) : jusqu'à 9x de débit (résumé) et 5x de latence en moins (résumé, Tables 3-4) ; 2x plus rapide que le Jetson Nano (40 ms YOLOv3-Tiny FP32) pour ~20 % de puissance en plus (§5.3, Table 5, puissance carte 12,3 W contre 10 W). Le NCS 2 est plus efficace énergétiquement (§5.3).
- Efficacité : 87 % du débit de [6] avec 29,8 % des DSP (§5.3).
→ reportés dans `benchmarks.csv` : 10 lignes (Table 3 et Table 4 : YOLOv2-Tiny/YOLOv2/YOLOv3-Tiny/YOLOv3 sur XC7K325T et XC7VX690T, batch 1 et 2), voir `bench_rows.csv`. Les colonnes des tableaux, aux cellules fusionnées, ont été réalignées par recoupement avec le texte (525, 914, 859, 401, 418 GOP/s) ; les valeurs non recoupées sont marquées `medium`.

## Limites et critique

- Débit rapporté en GOP/s seulement : le FPS n'est pas rapporté (`n/r`) ; latences bout en bout données pour deux configurations Tiny seulement (§5.3, Table 5). GOP/s comptent les MAC en 2 opérations sans que le nombre d'opérations par modèle soit rappelé en dehors de Table 5 (5,7 GOP pour YOLOv3-Tiny).
- Comparaisons hétérogènes : jeux de données différents (KITTI, ILSVRC2015, VOC), résolutions, quantifications (8, 16, 18 bits), technologies (16 nm contre 28 nm), batch 8 pour [28] contre 1 ici, et puissance (puce Vivado contre carte) selon les travaux. Le Jetson Nano est comparé en FP32 (40 ms) et non en INT8 / TensorRT (baseline défavorable, déduit).
- Puissance de puce = estimation Vivado, non mesurée ; la puissance carte inclut celle de la carte de développement (ex. DDR3, périphériques). Portée différente selon les références [4], [7], [9].
- Cartes Kintex-7/Virtex-7 anciennes (28 nm) ; le passage à batch 2 n'apporte de gain qu'en débit, au prix d'une latence supérieure (déduit) ; le batch 1 sur 690T n'est que 1,25x plus rapide que sur 325T, avec 25 % d'utilisation DSP, limité par la fréquence et la bande passante des convolutions 1x1 (§5.3).
- mAP évaluée sur VOC, non sur des scènes industrielles ; seuil IoU du mAP non précisé dans le texte lu. Pas d'analyse de robustesse, de déterminisme, de fautes.
- Code et bitstream non publiés ; reproductibilité limitée.

## Pertinence pour la thèse

Bonne pour l'axe `yolo-fpga` : accélérateur YOLO INT8 complet incluant NMS en matériel, sur FPGA sans processeur dur, ce qui réduit la surface logicielle (déduit : un chemin de traitement entièrement matériel est plus simple à analyser pour une argumentation de sûreté ; les auteurs ne le disent pas). Le modèle Roofline et l'exploration de conception par contrainte de 70 % de ressources sont réutilisables. Rien sur la sûreté, la certification, la tolérance aux fautes ou la détection de personnes ; détecteur de classes VOC uniquement (dont « person »).

## Gaps identifiés

- Aucune évaluation de sûreté ou de fiabilité (SEU, dérive de quantification) d'un accélérateur YOLO complet.
- Pas d'implémentation sur des cartes récentes (Zynq UltraScale+, Kria) ni de YOLO récents (v5+, mentionnés seulement comme travaux futurs) ; pas de puissance dynamique normalisée.
- Latence de bout en bout réellement rapportée pour très peu de configurations, ce qui gêne la comparaison à un critère temps réel de vidéosurveillance.

## Statut de lecture

Papier complet (fulltext.md lu en entier ; deux phrases de §5.3 sont tronquées à l'extraction). Extraction GROBID sans reconstruction de tableaux mais avec cellules fusionnées (Tables 3-5) : colonnes alignées par recoupement avec le texte. Sections 4 et 5 non détectées comme telles par l'extraction (texte rattaché à la précédente), sans perte de contenu constatée. Déduit et non affirmé par les auteurs : la pertinence pour la sûreté, la faiblesse de la baseline Jetson Nano FP32, l'absence de code publié (aucun lien trouvé), la portée `board` retenue pour `power_w`.
