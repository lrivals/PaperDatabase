---
id: arxiv-2609.24757-npu-accelerator-quantized-real-time
fiche: done
date: 2026-09-29
---

# NPU Accelerator: Quantized Real-Time Vehicle Detection on PYNQ-Z1 Using FINN

Daniel Gutierrez, Antonio Cuesta, Jorge Fe, Bruno Gutierrez, Rashed Al Koutayni, 2026, arXiv preprint. https://arxiv.org/abs/2609.24757
Type : preprint non relu par les pairs.

## Problème

Trouver un point de fonctionnement qui satisfait simultanément quatre exigences sur une petite puce, le Zynq XC7Z020 de la PYNQ-Z1 : > 30 FPS, > 7 FPS/W, latence matérielle PL < 50 ms, mAP@0,5 VOC > 0,55, pour la détection de véhicules (§I, §II-A). Un YOLOv3-tiny complet (8,66 M paramètres, 1,61 GMAC à 320x320) demanderait ≈ 34,7 Mbit de poids à 4 bits pour ≈ 4,9 Mbit de BRAM disponibles, donc irréalisable en streaming sur puce (§III-A).

## Méthode

- Modèles : LP-YOLO (≈ 0,35 M paramètres, 0,091 GMAC, échelle de détection unique) et LP-YOLO Slim (entrée 256x256), plus un YOLOv3-tiny « custom » de référence (§III-A, §IV-C).
- QAT avec Brevitas : w4a4 pour LP-YOLO, w2a4 (sortie 8 bits) pour Slim ; sur la référence YOLOv3-tiny 4 bits, la QAT reste à ≈ 0,006 mAP@0,5 du flottant contre ≈ 0,17 de perte pour la PTQ (§IV-B).
- Compilation FINN à partir de QONNX : folding PE/SIMD, FIFO inter-couches (profondeur 6 manuelle ou dimensionnement automatique), génération HLS/RTL, Vivado, déploiement PYNQ (§IV-D, §IV-E). NMS et décodage sur l'ARM (§II-B).
- Distinction explicite entre estimations analytiques FINN et mesures sur carte : estimation 38 FPS pour un folding LP-YOLO 4/4 contre ≈ 22 FPS mesurés à 100 MHz (§III-B).

## Plateforme et implémentation

- Puce : Zynq XC7Z020 (PYNQ-Z1) ; horloges PL 100 à 200 MHz (§IV-F).
- Puissance : mesurée sur le rail d'entrée 12 V de la carte (§IV-G) : carte entière (`board`) ; méthode d'instrument n/r.
- Débit : lot de 100 images ; latences PL et de bout en bout mesurées (§IV-G).
- Ressources FPGA (LUT/DSP/BRAM) : n/r dans le texte extrait (la Table I de résultats est absente de fulltext.md).
- Code/bitstream : non publiés d'après le texte ; un « project report » interne est cité, non accessible.

## Résultats

Résultats consolidés dans le texte de §V-VI (la Table I n'est pas extraite) :

| Configuration | FPS | P (W) | FPS/W | Latence PL (ms) | Latence E2E (ms) | mAP@0,5 VOC | COCO filtré |
|---|---|---|---|---|---|---|---|
| LP-YOLO 320 w4a4, FIFO manuel, 100 MHz | 22,15 | 2,00 | 11,075 | 62,41 | 66,47 | n/r | n/r |
| LP-YOLO 320 w4a4, FIFO manuel, 200 MHz | 44,29 | 2,18 | 20,32 | 31,73 | n/r | n/r | n/r |
| LP-YOLO 320 w4a4, FIFO auto, 100 MHz | 35 | 2,15 | 16,28 | 40,82 | n/r | 0,39 | 0,27 |
| LP-YOLO Slim 256 w2a4, 125 MHz | 31,22 | 2,80 | 11,15 | 51,49 | 56,13 | 0,594 | n/r |
| LP-YOLO Slim 256 w2a4, 142,86 MHz | 35,66 | 2,91 | 12,25 | 45,11 | 49,77 | 0,594 | 0,492 |
| YOLOv3-tiny custom w4a4, 100 MHz | 12,35 | 2,08 | 5,94 | 94,87 | n/r | 0,761 | 0,559 |

(§V-A à V-E, §VI-A à VI-C, Table II.) Seule la configuration Slim à 142,86 MHz satisfait les quatre exigences (Table II, Conclusion).
→ reportés dans `benchmarks.csv` : 6 lignes fournies dans `bench_rows.csv` (`accuracy_value` : mAP@0,5 VOC en % ; n/r pour les deux lignes sans mAP ; `latency_ms` = latence PL). Confiance `medium` : valeurs lues dans le texte, pas dans un tableau.

## Limites et critique

- Résultats du texte seulement (Table I absente de l'extraction, ressources non chiffrées) ; les auteurs reconnaissent que plusieurs lignes n'ont pas de mAP (§IV-G, §VII-F).
- Tâche « véhicules » restreinte (classes VOC/COCO filtrées) : le mAP de 0,594 (VOC) et 0,492 (COCO filtré) ne se compare pas au mAP COCO 80 classes des autres papiers ; les auteurs montrent que VOC est plus facile (boîtes 2-3 fois plus grandes, §VII-D), et le seuil 0,55 a été choisi par le projet.
- Le mAP de la ligne finale est mesuré avec un protocole « board-test » dont le détail n'est pas donné ; la mention d'une remesure en août 2026 suggère des révisions du protocole.
- Portée de la puissance : rail 12 V, donc carte entière ; comparaison directe avec des puissances de puce impossible. FPS mesuré en lot de 100 : ne reflète pas la latence d'un flux temps réel image par image.
- Le résultat « seule config qui passe » découle de seuils fixés par les auteurs sur six points expérimentaux ; pas de barre d'erreur ni de répétition.
- Baseline GPU/Jetson absente. Différence FIFO manuelle contre automatique (22 contre 35 FPS) : attribuée au buffering, non vérifiée par ailleurs.

## Pertinence pour la thèse

Cas FINN (dataflow, chaîne QAT complète Brevitas, w2a4) sur un petit FPGA, avec une méthodologie explicite d'écart estimation contre mesure et une définition de KPI multiples : modèle de spécification utile pour des exigences de sûreté (latence maximale, débit). Le détecteur est un YOLO allégé sur véhicules, pas sur personnes ; l'écart d'accuracy avec le flottant n'est pas mesuré pour le modèle final. Aucune notion de fiabilité ni de certification, mais le flot FINN (architecture déterministe en streaming, sans DPU) est plus propice à la latence bornée.

## Gaps identifiés

- Détecteurs YOLO en w2a4 sur FPGA pour des personnes ; perte QAT contre flottant du modèle final non rapportée.
- Latence pire cas (gigue) non mesurée, seulement moyennes en lot ; poids du post-traitement ARM (≈ 4,7 ms hors PL).
- Puissance carte seulement ; pas de baseline embarquée équivalente.

## Statut de lecture

Papier complet (fulltext.md lu en entier). La Table I annoncée (« consolidates the measured results ») n'est pas dans l'extraction : les chiffres du tableau ci-dessus viennent du texte, seule la Table II (KPI de la config finale) est présente. Déduit et non affirmé par les auteurs : portée `board` de la puissance (« 12 V input rail ») ; absence de code publié ; comparaison aux baselines.
