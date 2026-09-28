---
id: arxiv-2607.13106-no-attention-no-problem-dpu
fiche: todo
date: 2026-09-28
---

> **Importée de la base `drone` le 2026-09-28.** Cette fiche a été écrite pour une autre base (autre thème) : pertinence à réévaluer ici, puis `fiche: done` via `/paper-fiche`. Statut d'origine : done.

# No Attention, No Problem: DPU-Aware Attention Approximation in Modern YOLO on FPGA

Suraj Karki, Qazi Arbab Ahmed, Thorsten Jungeblut, 2026, arXiv preprint. https://arxiv.org/abs/2607.13106
Type : preprint non relu par les pairs.

## Problème

Les travaux YOLO sur FPGA portent surtout sur d'anciennes versions ; les YOLO récents **à
attention** (YOLOv11 : module C2PSA ; YOLOv26) et la **détection orientée (OBB)** ne sont
presque pas déployés sur FPGA SoC (§II-B). Le DPU Vitis AI ne supporte ni SiLU, ni split,
ni reshape / transpose / matmul / softmax : ces opérations retombent sur le CPU (§III-B).

## Méthode

- Modèles nano : YOLOv8n, YOLOv11n, YOLOv26n et leurs variantes OBB (Ultralytics),
  entrée 416 px (grand côté), entraînement FP16 mixte, PTQ INT8 Vitis AI (§III-B, §III-C).
- **Adaptations DPU-aware** (§III-B) :
  - SiLU → ReLU ;
  - split du bloc C2f → deux convolutions 1×1 initialisées en matrice de sélection binaire
    (Fig. 2) ;
  - **attention C2PSA approximée** : q, k, v par conv 1×1, poids d'attention = produit
    élément par élément q ⊙ k mis à l'échelle, softmax → hard-sigmoid, projection 1×1 puis
    fusion (Fig. 3). Ce n'est plus une attention au sens matriciel (déduit : pas de mélange
    spatial global).
  - YOLOv26 : sans DFL, tête NMS-free, mais **le NMS est conservé** pour l'évaluation
    (§III-B3).
- Compilation Vitis AI (XIR, VART) pour **DPUCZDX8G**, 8 architectures B512 à B4096
  reconstruites à partir du TRD AMD (Vivado / Vitis 2022.2), URAM, channel augmentation,
  low-power mode (§III-D, §III-E).
- Pré- et post-traitement (dont NMS) en Python sur l'ARM (Vitis AI Library) (§III-F).

## Plateforme et implémentation

- **ZCU104** (Zynq UltraScale+ MPSoC EV, 4× Cortex-A53) (§IV-A) ; fréquence du DPU n/r.
- Un seul cœur DPU pour les mesures de débit (§IV-C, §V).
- Ressources et puissance par architecture (Table III) — **puissance « on-chip » rapportée
  par Vivado**, donc estimée, pas mesurée :

| DPU | Puissance (Vivado) | LUT | BRAM | URAM | DSP |
|---|---|---|---|---|---|
| B512 | 4,792 W | 28,2 k | 28 | 15 | 118 |
| B1024 | 5,654 W | 36,5 k | 76 | 15 | 230 |
| B2304 | 7,165 W | 45,1 k | 104 | 38 | 438 |
| B4096 | 8,760 W | 55,8 k | 142 | 46 | 710 |

- Code / bitstream : non publiés (aucun lien dans le texte).

## Résultats

- **Coût des modifications** (FP, avant quantification) : −3 points de mAP@0.5:0.95 en
  moyenne (Table I, §IV-B). Ex. COCO : YOLOv11n 0,35 → 0,31 ; YOLOv26n 0,36 → 0,31 ;
  DOTA-OBB : YOLOv11n 0,44 → 0,34, YOLOv26n 0,42 → 0,32 (Table I).
- **Après INT8 sur FPGA** (Table II), mAP@0.5:0.95 CPU → FPGA :

| Modèle | VOC | KITTI | COCO | DIOR-R (OBB) | DOTA (OBB) |
|---|---|---|---|---|---|
| YOLOv8n(-OBB) | 0,60 → 0,45 | 0,64 → 0,34 | 0,27 → 0,26 | 0,66 → 0,56 | 0,43 → 0,31 |
| YOLOv11n(-OBB) | 0,59 → 0,57 | 0,60 → 0,59 | 0,31 → 0,29 | 0,61 → 0,53 | 0,34 → 0,30 |
| YOLOv26n(-OBB) | 0,57 → 0,48 | 0,58 → 0,51 | 0,31 → 0,29 | 0,60 → 0,52 | 0,32 → 0,29 |

- **Débit** (vidéo PETS2009-S2L1, 768×576, un cœur DPU) : meilleur E2E **YOLOv26n 34,05 FPS
  / 29,37 ms** et **YOLOv26n-OBB 29,55 FPS / 33,85 ms** en B4096 (§IV-C). Les FPS DPU seuls
  sont nettement plus élevés mais ne sont donnés qu'en figures (Fig. 6-8, n/r en valeur).
- **Goulot = post-traitement sur l'ARM** : agrandir le DPU ne se traduit pas en débit bout
  en bout (§IV-C, §V).
- Puissance « ~3× plus basse que l'état de l'art [27] (SATAY) » (§V).

→ reportés dans `benchmarks.csv` : 23 lignes. 21 lignes de précision FPGA (Table II, 6
modèles × jeux, `high`, FPS n/r car mesurés sur une autre vidéo) et 2 lignes de
performance B4096 (YOLOv26n et YOLOv26n-OBB : FPS / latence E2E, puissance Vivado
`estimated`, ressources ; `medium`).

## Limites et critique

- **Puissance estimée par Vivado** (on-chip), pas mesurée : la comparaison « 3× moins que
  SATAY » compare une estimation puce à des puissances d'une autre méthode (dans
  `benchmarks.csv`, les puissances SATAY ont une portée `unspecified`), et à débit très
  différent. Non comparable.
- **Débit bas en bout en bout** (~30 FPS en B4096) alors que la DPU fait bien mieux :
  post-traitement Python sur A53, un seul cœur, pas de multithreading. Le choix de Python
  pénalise le E2E ; le NMS est conservé même pour YOLOv26 (NMS-free par conception).
- **Chute INT8 importante et irrégulière** : YOLOv8n sur KITTI 0,64 → 0,34 ; la moyenne
  « ~5 % » (Abstract) / « ~7 % » (§IV-B) masque ces cas. PTQ seulement, pas de QAT.
- **L'attention « approximée »** n'est plus une attention (produit élément par élément +
  hard-sigmoid) : le gain de YOLOv11 sur YOLOv8 peut venir du reste de l'architecture ;
  pas d'ablation isolant l'approximation.
- FPS mesurés sur une vidéo de surveillance 768×576 (7 FPS natifs), pas sur les images
  DOTA / DIOR-R 1024×1024 : pas de débit pour la configuration aérienne.
- Pas de comparaison à un GPU embarqué (Jetson) ni à d'autres travaux YOLO/FPGA récents
  en chiffres.
- Rien de spécifique au drone : DOTA / DIOR-R sont des images satellites / aériennes, pas
  des vues de drone basse altitude ; pas de VisDrone, pas d'APs.

## Pertinence pour la thèse

- Directement dans l'hypothèse « les YOLO drone SOTA (Transformer / attention) ne sont
  presque jamais portés sur FPGA » : ce papier montre **comment** on contourne les
  limites du DPU (attention remplacée par des opérations convolutionnelles) et **ce que
  cela coûte** (−3 points FP, puis −2 à −30 points INT8 selon le couple modèle / jeu).
- Donne une table de ressources / puissance Vivado par taille de DPU sur ZCU104,
  réutilisable comme référence (B512 → B4096 : 4,8 → 8,8 W estimés).
- Confirme le goulot du post-traitement sur le PS, déjà noté ailleurs dans la base
  (2025-elhence, §V-F).
- Détection orientée sur FPGA : rare, utile si la thèse vise des vues aériennes obliques.

## Gaps identifiés

- Attention « vraie » (matmul + softmax) sur FPGA pour YOLO drone, hors DPU (HLS / dataflow) :
  non traité.
- Tête NMS-free (YOLOv26) exploitée réellement sur FPGA pour supprimer le goulot PS : annoncé
  en perspective (§V).
- Évaluation sur VisDrone / mAP_small après INT8 : absente.
- Puissance mesurée à la carte pour les 8 tailles de DPU : absente.

## Statut de lecture

Papier complet (`fulltext.md` lu en entier, extraction GROBID `ok`). La section IV n'a pas
été détectée comme titre (texte rattaché à §III-F). Un paragraphe de §IV-C (protocole
PETS2009) a été extrait dans le corps de la Table II. Les valeurs FPS / latence par
architecture DPU ne sont qu'en figures (Fig. 6-8) : n/r.

Ce qui suit est déduit et non affirmé par les auteurs :
- le caractère non matriciel de l'attention approximée ;
- la non-comparabilité de la puissance avec SATAY ;
- l'interprétation de « CPU » (Table II) comme le modèle modifié non quantifié (les valeurs
  coïncident presque avec la colonne « Modified » de la Table I).
