# Expérience : mAP mesurée sur la cible (Kria KV260)

Protocole rédigé le 24/09/2026 pour étayer le gap « Précision non vérifiée sur la cible
après compilation et quantification » ([gaps.md](../../gaps.md), section « Mesure et
comparaison »). Il complète la tâche 3 de [SETUP.md §9](../../SETUP.md#9-état-actuel-et-tâches-à-faire)
(expérience de référence YOLOv5 INT8 sur KV260).

Statut : **protocole, non exécuté**. Les noms d'outils et d'options suivis de « (à
vérifier) » viennent de ma connaissance de l'écosystème AMD-Xilinx, pas d'un papier du
corpus : ils sont à confirmer dans la documentation de la version de Vitis AI utilisée.

---

## 1. Question

La mAP d'un détecteur déployé sur le DPU du KV260 est-elle celle que rapportent les
outils (modèle flottant, ou modèle quantifié simulé sur GPU) ? Et à quelle étape de la
chaîne se perd-elle, si elle se perd ?

Constats du corpus qui motivent la question :
- conversion OpenVINO → 0 % de confiance (2022-feng-benchmark-analysis-yolo-performance-edge,
  Table 3) ;
- TPU dégradé par la quantification post-entraînement, et modification d'architecture pour
  le DPU (arxiv-2211.11647, §2.3, §3) ;
- AP identique en FP32 et en INT16, sans lieu de mesure indiqué
  (2023-zhai-fpga-vehicle-detection-tracking-accelerator, Table 8).

## 2. Hypothèses

- **H1.** La mAP mesurée sur la carte, NMS compris, est inférieure à la mAP du modèle
  quantifié simulé. L'écart vient de différences d'implémentation entre simulation et
  DPU : arrondis, activations non supportées repliées sur CPU, post-traitement réécrit.
- **H2.** L'essentiel de la perte vient de la quantification post-entraînement (PTQ), pas
  de la compilation. Le QAT la réduit.
- **H3.** Un post-traitement réimplémenté sur l'ARM (décodage des sorties, NMS) introduit
  à lui seul un écart mesurable si ses seuils ou son ordre d'opérations diffèrent de la
  référence.

Hypothèse nulle : les trois mAP (flottant, simulé, cible) sont égales à ±0,3 point, valeur
à fixer après une mesure de répétabilité (§5).

## 3. Conditions

| Élément | Choix | Pourquoi |
|---|---|---|
| Carte | Kria KV260, image officielle, DPU B4096 (à vérifier selon l'app) | cible du corpus (arxiv-2507.18174) |
| Modèle | YOLOv5s (variante déclarée), entrée 640×640, puis 416×416 | le corpus manque de variante et de résolution déclarées (gap protocole) |
| Données | COCO val2017 complet (5000 images) | split officiel, jamais un sous-ensemble ad hoc |
| Métrique | mAP@[.5:.95] et mAP@.5 par pycocotools, sur les **mêmes** fichiers de prédictions JSON | une seule implémentation de la métrique pour les trois points |
| Seuils | confiance 0,001 et IoU NMS 0,6 (réglage d'évaluation COCO usuel de YOLOv5, à vérifier) ; identiques partout | un seuil de confiance élevé fausse la mAP |
| Batch | 1 | comparable à la latence |
| Chaîne | Vitis AI : quantizer (PTQ, puis QAT en variante), compilateur `vai_c_*` pour le DPU cible, exécution par VART (à vérifier) | toolflow du corpus |

## 4. Les trois mesures

| Point | Où | Ce qui est mesuré |
|---|---|---|
| **A. Flottant** | GPU hôte, PyTorch | mAP de référence du modèle entraîné |
| **B. Quantifié simulé** | GPU hôte, sortie du quantizer Vitis AI en mode test (à vérifier) | mAP INT8 annoncée par l'outil |
| **C. Sur cible** | KV260 : DPU + post-traitement sur l'ARM | mAP de ce qui tourne réellement, NMS compris |

Pour localiser une perte (H1-H3), deux points intermédiaires :
- **C0 :** sorties brutes du DPU copiées sur l'hôte, puis décodées et soumises au NMS par
  le **même** code Python que A et B. L'écart C0 − B isole le DPU.
- **C1 :** post-traitement embarqué (celui de l'application sur l'ARM) appliqué aux mêmes
  sorties brutes. L'écart C − C0 isole le post-traitement.

Contrôle d'équivalence : pour une centaine d'images, comparer tenseur par tenseur les
sorties du DPU (C0) et celles du modèle simulé (B). Relever l'écart maximal et moyen en
unités de quantification.

## 5. Mesures annexes (même session)

- **Latence et débit :** à batch 1, en séparant pré-traitement, DPU et post-traitement
  (horodatage sur l'ARM). Cela répond aussi au gap « post-traitement sur le PS »
  (arxiv-2509.04153 ; arxiv-2211.11647, §2.5 ; 2023-zhai, §3.3).
- **Puissance :** au wattmètre à l'entrée de la carte (`board`) et par la télémétrie de la
  puce (`chip` ; outil `xmutil platformstats` sur Kria, à vérifier). Plus la puissance au
  repos, pour pouvoir calculer `board-dynamic`. Modèle : P_chip et P_wall de FINN
  (arxiv-1612.07119, §5.1).
- **Répétabilité :** trois exécutions complètes de C. L'écart entre elles fixe le seuil de
  l'hypothèse nulle.
- **Traces :** versions (Vitis AI, image Kria, PyTorch), empreinte SHA-256 du modèle
  compilé, fichiers JSON de prédictions de A, B, C0 et C. Tout est archivé pour que la
  mesure soit refaisable.

## 6. Résultat attendu et lecture

Un tableau unique :

| Point | mAP@[.5:.95] | mAP@.5 | Écart / A | Latence (ms) | P board / chip (W) |
|---|---|---|---|---|---|
| A flottant | | | 0 | n/a | n/a |
| B simulé | | | | n/a | n/a |
| C0 DPU + NMS hôte | | | | | |
| C cible complète | | | | | |

Lecture :
- **C ≈ B :** l'outil dit vrai, et le gap porte seulement sur la **publication** (les
  papiers ne mesurent pas sur la cible). Le résultat reste utile comme exemple de
  protocole.
- **C < B :** le gap devient technique. L'écart C0 − B (DPU) et l'écart C − C0
  (post-traitement) disent où agir.
- En variante, **QAT contre PTQ** : si le QAT supprime l'écart, H2 est confirmée.

## 7. Coût et risques

- **Matériel :** KV260, wattmètre USB-C ou de laboratoire, GPU hôte pour A et B.
- **Temps estimé (déduit, à réviser) :** 1 à 2 semaines. Le plus long est la mise en place
  de la chaîne Vitis AI et du post-traitement embarqué ; les mesures elles-mêmes prennent
  quelques heures (5000 images à batch 1).
- **Risques :**
  - couches YOLOv5 non supportées par le DPU (activation SiLU selon la version du DPU, à
    vérifier), donc repli sur CPU : c'est à documenter, puisque c'est précisément ce que
    l'expérience doit révéler ;
  - télémétrie de la puce indisponible ou peu précise : la portée `board` seule reste
    exploitable.

## 8. Suites

- Refaire C sur une Jetson Orin Nano avec TensorRT INT8 (même modèle, même JSON COCO,
  même protocole de puissance) : c'est le gap « baseline Jetson ».
- Refaire la chaîne avec FINN ou hls4ml sur un modèle plus petit (TinyissimoYOLO) : c'est
  le gap « passerelle MCU ↔ FPGA ».
- Après exécution : ajouter les lignes dans `benchmarks.csv` sous le `paper_id`
  `own-2026-kv260-map-sur-cible` (mesure propre, DATA_MODEL §1 ; `source_section` renvoie
  à une section de ce fichier), puis mettre à jour `gaps.md`.
