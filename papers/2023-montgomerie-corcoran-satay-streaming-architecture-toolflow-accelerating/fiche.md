---
id: 2023-montgomerie-corcoran-satay-streaming-architecture-toolflow-accelerating
fiche: done
date: 2026-09-26
---

# SATAY: A Streaming Architecture Toolflow for Accelerating YOLO Models on FPGA Devices

Alexander Montgomerie-Corcoran, Petros Toupas, Zhewen Yu, Christos-Savvas Bouganis, 2023, 2023 International Conference on Field Programmable Technology (ICFPT) 179-187. https://doi.org/10.1109/ICFPT59805.2023.00025
Type : conférence (métadonnées issues de l'export IEEE Xplore, `citation.bib`)

## Problème

Les accélérateurs YOLO sur FPGA sont soit des overlays hétérogènes CPU + FPGA (Vitis AI),
limités par les échanges CPU-FPGA, soit des designs faits main pour une seule version de YOLO,
qui ne suivent pas l'évolution des modèles (§I, §II-C). Les auteurs posent trois verrous pour
un toolflow générique (§I) : opérations propres à YOLO (leaky ReLU, SiLU, resize), longues
skip connections qui exigent beaucoup de buffers dans une architecture streaming, et espace
de conception devenu très grand (47 nouvelles couches depuis YOLOv3).

## Méthode

- **Architecture streaming (dataflow)** : une unité matérielle dédiée par nœud du graphe,
  interfaces ready/valid, pipeline profond ; l'image entre depuis la DDR en NHWC et les
  prédictions de boîtes sortent vers la DDR. Tous les poids restent on-chip (§III-A).
- **Blocs** : convolution (générateur de fenêtre glissante à line buffers, moteur
  matrice-vecteur de K × K DSP ; poids en URAM/BRAM), max pooling, resize à la volée, split /
  concat / add, leaky ReLU, et **HardSwish en remplacement de SiLU** (§III-B).
- **Toolflow** : ONNX → représentation interne → DSE → bitstream, sur le squelette open-source
  SAMO [33], dans la lignée de fpgaConvNet et FINN (§IV).
- **Quantification** : post-entraînement, sans fine-tuning, blocs par couche (échelle et zéro
  par couche) ; poids ≥ 8 bits jugés sans effet notable sur la précision, activations fixées à
  16 bits (§IV-A, Fig. 8). Configurations évaluées : W8A16 (Table III).
- **DSE** : modèles analytiques de latence et de DSP, et allocation gloutonne des DSP au nœud
  le plus lent (Algorithm 1, §IV-B).
- **Mémoire** : les poids représentent 50 à 89 % de la mémoire on-chip (Table II), jusqu'à
  26 MB (§IV-C). Les plus gros buffers de skip connections sont déportés en DDR via une
  **FIFO logicielle** (PYNQ, DMA par chunks), en commençant par les plus grands (Algorithm 2).
- Post-traitement (NMS) : n/r ; le texte dit seulement que le pipeline produit les prédictions
  de boîtes (§III-A).

## Plateforme et implémentation

- Cartes AMD : Alveo U250, ZCU104, VCU110, VCU118 (§VI) ; puces exactes n/r (le papier ne
  nomme que les cartes). Vivado 2020.1.
- Ressources, fréquence (200 à 270 MHz), latence, énergie et puissance par design : Table III.
- **Puissance** : aucune méthode de mesure décrite (capteur, outil, carte ou puce : n/r) →
  `power_scope: unspecified`.
- Code et bitstreams : non publiés dans le papier (aucun lien). Le toolflow repose sur SAMO,
  qui est open-source [33].

## Résultats

Le tableau III (comparaison avec l'état de l'art) n'a pas été détecté par GROBID. Il a été lu
par Docling sur `paper.pdf`, aplati en une seule ligne, puis re-découpé à la main (voir
Statut de lecture). Le tableau IV est lu par GROBID et Docling, avec des chiffres identiques.

| Modèle (entrée) | Carte | mAP (%) | Latence (ms) | Puissance (W) | GOP/s | GOP/s/DSP | Source |
|---|---|---|---|---|---|---|---|
| YOLOv3-Tiny (416) | VCU110 | 33,9 | 14,3 | 15,4 | 418,9 | 0,24 | Table III |
| YOLOv3-Tiny (416) | VCU118 | 33,9 | 6,8 | 42,9 | 875,7 | 0,13 | Table III |
| YOLOv5s (640) | VCU110 | 56,2 | 46,4 | 24,8 | 392,0 | 0,22 | Table III |
| YOLOv5s (640) | VCU118 | 56,2 | 14,9 | 67,0 | 1219,8 | 0,24 | Table III |
| YOLOv8s (640) | VCU110 | 61 | 122,8 | 23,5 | 248,2 | 0,14 | Table III |
| YOLOv8s (640) | VCU118 | 61 | 24,5 | 57,4 | 1244 | 0,18 | Table III |
| YOLOv5n (320) | ZCU104 | 21,2 | 9,83 | 14,82 | n/r | n/r | Table IV |
| YOLOv5n (640) | ZCU104 | 26,7 | 21,41 | 14,5 | n/r | n/r | Table IV |
| YOLOv5n (640) | Jetson TX2 (baseline) | 27,7 | 32,28 | 8,58 | n/r | n/r | Table IV |

- Selon les auteurs, c'est la **première implémentation FPGA de YOLOv8** publiée (§VI-A).
  Sur YOLOv3-Tiny, le GOP/s/DSP est 1,1 à 3,4 fois celui de [10], [34], [35], et 7,3 fois
  celui de [26] sur YOLOv5s (§VI-A).
- Face au CPU ARM Cortex-A72 et au Jetson TX2, à consommation d'énergie comparable :
  accélération moyenne de 79× et 3,6× (§VI-B, Fig. 10, COCO-128).
- YOLOv5n : l'énergie par inférence des FPGA (hors U250) est comparable à celle du TX2,
  surtout en 640 × 640 : ZCU104 317 mJ contre TX2 277 mJ (Table IV). En 320 × 320, le TX2
  reste plus sobre (70,7 mJ contre 117,5 à 431 mJ).
- FIFO logicielle, ablation sur YOLOv5n et ZCU104 : déporter les 5 plus gros buffers réduit la
  mémoire des buffers de 56 % et la mémoire on-chip totale de 17 %, pour +35 % de bande
  passante DDR (2,15 Gbps sur 135 Gbps disponibles) (§V, Fig. 9).

→ reportés dans `benchmarks.csv` : 14 lignes. 6 viennent du tableau III (YOLOv3-Tiny, YOLOv5s
et YOLOv8s sur VCU110 et VCU118, W8A16) et 8 du tableau IV (YOLOv5n 320 et 640 sur U250,
ZCU104, VCU110 et VCU118). Toutes sont en `confidence: medium` (tableaux reconstruits par
Docling) et en `power_scope: unspecified`. Le Jetson TX2 figure en baseline. Les designs des
travaux antérieurs repris dans le tableau III ne sont pas reportés.

## Limites et critique

- **Métrique de comparaison choisie.** Le GOP/s/DSP efface les écarts de précision (W1A8,
  W16A16, W32A32 dans la Table III), de carte et de fréquence. Il favorise un design qui
  utilise peu de DSP, sans rien dire de la latence absolue ni de l'énergie. Les chiffres des
  travaux antérieurs sont repris de leurs papiers, sans remesure.
- **Cibles peu embarquées.** Les meilleurs chiffres viennent des cartes Virtex VCU110 et
  VCU118 (23 à 67 W) et de l'Alveo U250 (≈ 110 W). La seule carte SoC embarquée est la ZCU104,
  évaluée seulement sur YOLOv5n. Aucune carte de classe KV260 ou Zynq-7000.
- **Tous les poids on-chip** (jusqu'à 26 MB, §IV-C) : l'approche suppose une grosse FPGA. Sur
  une petite FPGA, le repli (partitionnement, reconfiguration) n'est pas traité.
- **Puissance sans protocole.** Aucune méthode de mesure (carte ou puce, capteur ou outil) :
  les rapports d'énergie face au TX2 ne sont pas vérifiables. La baseline Jetson TX2 date de
  2017 ; son framework et sa précision (TensorRT, FP16 ?) sont n/r.
- **Incohérences internes (à vérifier sur le PDF).** Pour YOLOv3-Tiny et YOLOv5s sur VCU118,
  latence × puissance ne redonne pas l'énergie imprimée : 6,8 ms × 42,9 W ≈ 292 mJ pour
  252 mJ affichés, et 14,9 ms × 67,0 W ≈ 998 mJ pour 910 mJ affichés. Le calcul est de moi ;
  le découpage de Docling est peut-être en cause. Les quatre autres designs sont cohérents.
- **Précision.** mAP « ∗ » dans la Table III (définition de l'astérisque non extraite) et mAP50
  dans la Table IV. En 320 × 320, la valeur 21,2 est une cellule fusionnée qui vaut pour les
  quatre FPGA (lecture de la mise en page, déduite). HardSwish remplace SiLU et la PTQ se fait
  sans fine-tuning : l'impact n'est montré qu'en fonction de la largeur des poids (Fig. 8).
- Batch size, débit en FPS et comptage de la NMS dans la latence : n/r.

## Pertinence pour la thèse

C'est le contre-exemple direct au gap « détection absente des toolflows dataflow quantifiés » :
un toolflow streaming automatisé, de l'ONNX au bitstream, pour YOLOv3 à v8, avec un vrai
traitement des skip connections (FIFO déportée en DDR). Il reste deux ouvertures pour la
thèse. D'abord, rien sur les petites FPGA SoC (KV260, Zynq-7000), où les poids ne tiennent
pas on-chip. Ensuite, aucune mesure de puissance documentée. Une reproduction sur ZCU104 ou
KV260 avec mesure carte et puce serait une contribution nette.

## Gaps identifiés

- Le gap « détection absente des toolflows dataflow quantifiés » est à nuancer : SATAY (2023)
  couvre YOLO en streaming, mais seulement sur grosses FPGA et en W8A16 par PTQ.
- Streaming YOLO sur FPGA embarquée à mémoire on-chip limitée : non traité.
- Puissance des designs streaming YOLO sans protocole de mesure ; alimente le gap
  « Puissance : puce contre carte ».
- Aucune comparaison avec un Jetson récent (Orin) ni avec Vitis AI sur la même carte.

## Statut de lecture

Papier complet (`fulltext.md` en entier, extraction GROBID).
**Le tableau III n'est pas détecté par GROBID**, et donc absent de `fulltext.md` sans
avertissement. Il a été lu par Docling sur `paper.pdf`, sans OCR, en une ligne aplatie, puis
re-découpé à la main. Pour 4 des 6 designs, la cohérence latence × puissance = énergie et
GFLOPs / latence = GOP/s le confirme ; les deux designs VCU118 cités plus haut font exception.
La mAP de YOLOv8s (« 61 ») est ambiguë au découpage : 61 ou 61,3.
Ce qui suit est déduit et non affirmé par les auteurs : l'attribution de 21,2 % aux quatre FPGA
en 320 × 320 ; les incohérences d'énergie calculées ; le fait que les puces exactes ne soient
pas données ; le jugement « cibles peu embarquées ».
