---
id: arxiv-2304.11580-framework-benchmarking-real-time-embedded
fiche: done
date: 2026-09-29
---

# A Framework for Benchmarking Real-Time Embedded Object Detection

Michael Schlosser, Daniel König, Michael Teutsch, 2023, DAGM GCPR 2022, Lecture Notes in Computer Science vol. 13485, Springer. DOI 10.1007/978-3-031-16788-1_33 ; https://arxiv.org/abs/2304.11580
Type : conférence (GCPR 2022) ; version arXiv lue.

## Problème

Comparer équitablement des accélérateurs d'inférence propriétaires et leurs chaînes d'optimisation (Vitis AI, TensorRT) pour la détection d'objets sur flux vidéo est difficile : les travaux existants ne mesurent pas tout (précision, temps, puissance), ne couvrent qu'un matériel ou un fournisseur, ou mesurent l'accuracy sur la cible sans cadre uniforme (§1, §2).

## Méthode

Cadre générique hôte/cible : une application hôte (PC) publie les images via un broker MQTT (OpenCV + sérialisation Msgpack) ; l'application cible fait pré-traitement, inférence, post-traitement (NMS) et renvoie boîtes et temps mesurés ; l'hôte calcule mAP, temps, FPS, FPS/W (§3). Architecture publish-subscribe : plusieurs cibles évaluées en parallèle, greffons « evaluator » (hôte) et « object detector » (cible). Expériences : YOLOv4 (Darknet converti en TensorFlow), résolutions 416/512/608 (512 en baseline), COCO val (5000 images, 6 passes moyennées) et test (accuracy, un seul passage, seuil de confiance 0,05 ; sinon 0,25 ; NMS 0,45) (§4.1, §4.2). Chaîne Vitis AI (Quantizer INT8, Compiler ; pruning via modèles du Model Zoo) contre TensorRT (via ONNX, FP32/FP16/INT8) (§4.1). Énergie : multimètre en série, puissance absolue et relative (idle soustrait) (§4.1).

## Plateforme et implémentation

- FPGA : Zynq UltraScale+ MPSoC ZCU104 avec DPU (Vitis AI) ; GPU : Jetson AGX Xavier (modes MAXN, 30, 15, 10 W) (§4). Version exacte de puce/DPU (B-size, fréquence) : n/r.
- Puissance : multimètre en série avec la carte (tension fixe x courant) : carte entière (`board`) ; puissance relative = absolue moins idle (`board-dynamic`) (§4.1).
- Code/bitstream : non publiés d'après le texte (aucun lien).

## Résultats

Table 1 (YOLOv4-512 sauf mention ; mAP 0,5:0,95 en %, portée du jeu (val/test) non précisée dans la table) :

| Config | Inférence | P abs | P relative | FPS/W | mAP |
|---|---|---|---|---|---|
| TensorFlow CPU FP32 | 767,16 ms | n/r | n/r | n/r | 40,7 |
| Jetson TensorRT FP32 | 69,75 ms | 28 W | 18,5 W | 0,45 | 39,8 |
| Jetson TensorRT FP16 | 35,32 ms | 20 W | 10,5 W | 1,17 | 39,8 |
| Jetson TensorRT INT8 | 22,0 ms | 16,5 W | 7,0 W | 2,05 | 38,6 |
| ZCU104 Vitis AI INT8 | 54,42 ms | 23 W | 7,0 W | 1,31 | 37,5 |
| ZCU104 Vitis AI Zoo INT8 (416) | 67,84 ms | 22,5 W | 6,5 W | 1,40 | 38,3 |
| ZCU104 Zoo pruné INT8 (416, -36 % d'opérations) | 48,42 ms | 21,6 W | 5,6 W | 1,97 | 36,5 |

- Le Vitis AI Quantizer fait perdre 2,2 % de mAP, la compilation DPU en retire encore ; tous les modèles TensorRT dépassent en mAP les modèles Vitis AI (§4.3, §4.4).
- Modes de puissance Jetson INT8 (Table 2, Docling à vérifier) : total pré + inférence + post de 70,23 ms (MAXN), 85,75 (30 W), 118,3 (15 W), 150,58 (10 W) ; les auteurs recommandent 15 W pour l'efficacité (§4.4). Le post-traitement (Python numpy sur Jetson) pèse plus que l'inférence.
→ reportés dans `benchmarks.csv` : 6 lignes (Jetson FP32/FP16/INT8, ZCU104 Vitis AI, Zoo, Zoo pruné), fournies dans `bench_rows.csv`. `power_w` = puissance absolue (`board`) ; puissances relatives dans la fiche ci-dessus. FPS n/r : la Table 1 ne donne que le temps d'inférence (le FPS/W n'est pas recalculable à partir de celui-ci : par exemple 1000/22 ms / 16,5 W ≠ 2,05, il inclut probablement pré/post-traitement, non expliqué).

## Limites et critique

- Contribution principalement méthodologique ; les résultats portent sur un seul modèle (YOLOv4) et deux cartes.
- Comparaison pas tout à fait équitable : pré/post-traitement optimisé (Vitis AI Library) pour le DPU contre Python numpy pour TensorRT (§4.2) ; le post-traitement domine le temps Jetson (Table 2) ; le Zoo utilise 416x416 contre 512 pour les autres lignes.
- Les puissances absolues mesurées carte entière (23 W ZCU104 pour un DPU) incluent le carrier board ; la relative dépend de la définition de l'idle.
- Pruning non intégré à la chaîne (outil payant), évalué sur des modèles Zoo (autre entraînement) : pas de comparaison à iso-modèle.
- mAP val/test ambigus dans la Table 1 (§4.2) ; efficacité FPS/W non recalculable.
- Gestion de la latence MQTT : les temps sont mesurés côté cible, donc le transport n'est pas compté, mais la charge réseau/CPU sur cible n'est pas discutée. Baseline GPU non embarqué absent (CPU TensorFlow seulement).

## Pertinence pour la thèse

Méthode d'évaluation reproductible (hôte séparé, accuracy mesurée sur la cible déployée) : utile pour vérifier qu'une conversion vers le DPU garde les performances (traçabilité de la chaîne, point d'assurance) et pour comparer FPGA et Jetson avec puissance absolue et relative séparées (gap de comparabilité `power_scope`). Directement lié au cas YOLO : les chiffres YOLOv4 ZCU104/Jetson servent de baseline. Ne traite pas la sûreté, le déterminisme de latence, la fiabilité ni les personnes.

## Gaps identifiés

- Pas de mesure de gigue/déterminisme de latence (pire cas) : seulement des moyennes sur 6 passes.
- Pas d'évaluation de la robustesse (OOD, fautes) dans les cadres de benchmark.
- Comparaison FPGA/GPU à iso-pré/post-traitement peu fréquente.

## Statut de lecture

Papier complet (fulltext.md lu en entier). Table 2 reconstruit par Docling ; Table 1 partiellement mal découpée (colonnes) mais lisible et cohérente avec le texte (54,4 ms Vitis AI). Fig. 5 et 6 (barres) non disponibles. Déduit : portées de puissance (board / board-dynamic, d'après la description du multimètre) ; recommandation sur l'efficacité FPS/W non recalculable ; absence de code publié.
