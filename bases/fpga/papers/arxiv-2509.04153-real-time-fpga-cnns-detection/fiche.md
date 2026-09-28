---
id: arxiv-2509.04153-real-time-fpga-cnns-detection
fiche: done
date: 2026-09-24
---

# Real Time FPGA Based CNNs for Detection, Classification, and Tracking in Autonomous Systems: State of the Art Designs and Optimizations

Safa Mohammed Sali, Mahmoud Meribout, Ashiyana Abdul Majeed, 2025, arXiv preprint. https://arxiv.org/abs/2509.04153
Type : preprint non relu par les pairs

## Problème

Survey des implémentations FPGA de CNN pour la détection, la classification et le suivi
d'objets en temps réel (autonome, robotique, surveillance), avec l'ambition de couvrir la
littérature 2025, les Versal (ACAP), la parcimonie, les toolchains et les systèmes hybrides
GPU/FPGA, présentés comme peu traités par les surveys antérieurs (Abstract, §I, Table 1).

## Méthode

Revue narrative, non systématique : littérature IEEE, Springer, arXiv et brevets US
trouvée sur Google Scholar avec les mots-clés « 2025 », « real-time », « FPGA », « CNN
detection/classification/tracking » (§I). Aucun protocole de sélection (PRISMA ou autre),
aucun critère d'inclusion.

Plan : fondamentaux (couches, jeux de données, métriques) (§II) ; trois familles de FPGA —
LUT-DSP, SoC, SoC avec AI Engines (Versal) (§III, Tables IV-V) ; techniques
d'implémentation — dataflow/pipelining, quantification, DSP packing, élagage (§IV) ;
toolchains — Vitis/Vitis AI, OpenVINO + FPGA AI Suite, FINN, hls4ml, AutoHLS (§V) ;
détection, classification, suivi, systèmes hétérogènes (§VI, Tables VII-IX) ; compromis
(§VII).

## Plateforme et implémentation

Sans objet (survey). Plateformes récapitulées (Table V) : ZCU104 (230 400 LUT, 1728 DSP,
~1678 $), Versal VC1902 (400 AI Engines, ~13 195 $), Kria KV260 (70 560 LUT, ~249 $),
Agilex 7, Arria 10 GX.

## Résultats

Chiffres repris des travaux cités (non vérifiés ici) :

| Travail cité | Plateforme | Chiffres | Source dans le survey |
|---|---|---|---|
| LCAM-YOLOX, DPU [98] | ZCU102 (texte) / Kria KV260 (Table VII) | 195 FPS, 84,73 mAP, 640×640, 9,72 W | §VI-A, Table VII |
| YOLOv5, DPUCVDX8G [99] | Versal VCK190 | 244,49 FPS, F1 0,852 (RarePlanes) | §VI-A |
| YOLOv11-S [95] | PYNQ-Z1 | 18 FPS, ~70 % LUT, 80 % DSP | §VI-A |
| YOLOv3-tiny [103] | ZCU106 | 60 FPS, 1,57 W, 292,18 GOPS | Table VII |
| YOLOv8n 4 bits (FINN) + SORT [125] | ZCU102 | 195,3 FPS détection seule, 24 FPS de bout en bout, MOTA 0,389 (MOT15) | §VI-C |
| SiamRPN++ [128] | Kria KV260 | 6,37 FPS, 1,11 W | Table IX |
| Tiny DarkNet 16 bits [100] | XCVU19P / XCVP1902 | 120,48 FPS, 8,3 ms | §VI-A, Table VII |

Messages du survey : les YOLO tiny/nano se prêtent mieux au streaming FPGA que SSD
(SSD-VGG16 > 80 W, ~49× YOLOv3-tiny) (§VI-A) ; le suivi sur FPGA est quasi exclusivement
en tracking-by-detection sur SoC (détection en PL, association sur PS) (§VI-C) ; Vitis AI
n'accepte que l'INT8 à partir de FP32 (§V-A).

→ reportés dans `benchmarks.csv` : aucune ligne (survey : chiffres de travaux cités).

## Limites et critique

- **Incohérences internes** : LCAM-YOLOX sur ZCU102 (§VI-A) mais sur Kria KV260 dans la
  Table VII ; Tiny DarkNet [100] à 4,756 W sur XCVU19P dans le texte, mais 6,014 W sur
  XCVU19P et 4,756 W sur XCVP1902 dans la Table VII ; renvois de références incohérents
  entre texte et tableaux pour le suivi (SiamRPN++ [93] vs [128], YOLOv3-tiny + DeepSORT
  [168] vs [129], YOLOv8n + SORT [56] vs [125]) ; deux sections numérotées VII.
- **Tableaux comparatifs non comparables** : mAP sur des jeux et résolutions différents,
  puissance puce vs carte non distinguée, fréquences et précisions hétérogènes (Tables
  VII-IX). Le survey conclut pourtant sur « quel FPGA choisir » à partir de ces lignes
  (§VI-A).
- **Chiffres de plateforme discutables** : « ~1-143 TOPS » pour les FPGA LUT-DSP
  (Table IV) ; comparaison Zynq 16,7 GOPS/W vs RTX 3090 6,32 GOPS/W sur un seul travail
  ([132], §II-C) alors que le survey met lui-même en garde contre les TOPS crête.
- Méthode de sélection non reproductible ; avis non étayés (« Xilinx a un léger avantage »,
  §III).
- Aucune analyse de reproductibilité (code, bitstream publiés) des travaux cités.

## Pertinence pour la thèse

Bonne carte d'orientation 2025 pour l'axe YOLO sur FPGA : familles de plateformes,
toolchains (Vitis AI, FINN, hls4ml, FPGA AI Suite), et pointeurs vers des travaux à ficher
([98] LCAM-YOLOX, [95] YOLOv11 sur PYNQ, [125] YOLOv8n FINN + SORT, [74] YOLOv7-tiny
INT8 Gemmini). À utiliser comme index de références, jamais comme source de chiffres :
toujours remonter au papier cité.

## Gaps identifiés

- Gestion temps réel de l'interaction PS-PL (RTOS, priorités, WCET) pour plusieurs modèles
  d'IA vidéo sur SoC FPGA : non traitée dans la littérature selon les auteurs (§III-B).
- Pas d'équivalent d'AutoHLS (exploration assistée par ML) pour les flots Intel (§V-C).
- Suivi multi-objets sur FPGA : uniquement sur SoC, post-traitement (NMS, association)
  souvent en Python sur le PS, qui fait chuter le débit (195 → 24 FPS pour [125]) (§VI-C).
- Absence de protocole commun de mesure (puissance, mAP, résolution) dans les comparaisons
  YOLO-FPGA (déduit des Tables VII-IX).

## Statut de lecture

Papier complet (`fulltext.md` lu en entier). Extraction : le titre « I. INTRODUCTION » et
le début de l'introduction manquent (le texte reprend en cours de phrase) ; plusieurs
paragraphes sont déplacés dans « Figures et tableaux » (§III-B sur la DPU, §IV-B-2 sur la
quantification, outils Vitis) ; les Tables II-III sont illisibles, la Table VI absente.
Déduit et non affirmé par les auteurs : caractère non systématique de la revue comme
limite ; non-comparabilité des lignes des Tables VII-IX ; dernier gap.
