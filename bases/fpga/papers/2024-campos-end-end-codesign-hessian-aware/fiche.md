---
id: 2024-campos-end-end-codesign-hessian-aware
fiche: done
date: 2026-09-26
---

# End-to-end codesign of Hessian-aware quantized neural networks for FPGAs

Javier Campos, Jovan Mitrevski, Nhan Tran, Zhen Dong, Amir Gholaminejad, Michael W. Mahoney, Javier Duarte, 2024, ACM Trans. Reconfigurable Technol. Syst. 17(3), 36. https://doi.org/10.1145/3662000
Type : article de journal (ACM TRETS, relu par les pairs)

## Problème

La quantification mixte guidée par la Hessienne (HAWQ) quantifie finement chaque couche
selon sa sensibilité, ce qui convient bien aux FPGA, mais aucun chemin automatisé ne menait
d'un modèle HAWQ (PyTorch) à un firmware FPGA (§1). Les auteurs veulent un flot open source
de bout en bout, accessible aux non-experts, pour des applications à contraintes extrêmes
de latence, comme le trigger de niveau 1 du LHC (40 MHz de collisions, latence < 1 µs,
§1, §3.1).

## Méthode

- **HAWQ(v3)** : quantification entière uniforme avec facteurs d'échelle dyadiques
  (multiplications entières + décalages, sans division ni flottant) (§2.1).
- **Choix automatique des largeurs** : sensibilité par couche = trace moyenne de la
  Hessienne (algorithme de Hutchinson, Eq. 9) ; perturbation Ω (Eq. 10) minimisée par
  **programmation linéaire en nombres entiers (ILP)** sous contrainte de BOPs (bit
  operations, Eq. 8) (§4.2.2).
- **Export HAWQ → QONNX** (opérateurs Quant, Bipolar, Trunc) ou ONNX QCDQ (INT8) par tracing
  PyTorch et fonctions symboliques personnalisées ; nettoyage QONNX (inférence de formes,
  constant folding, fusion des échelles à travers ReLU) (§5).
- **hls4ml** ingère le QONNX et génère le HLS ; implémentations entièrement parallèles (reuse
  factor 1), 200 MHz, Vivado 2020.1 (§6.1).
- Cas d'étude 1 : **jet tagging** (MLP 16 → 64 → 32 → 32 → 5, 5 classes, 870 000 jets
  simulés), entrées INT16 (§3, §4.1). Recherche exhaustive (poids 4-8 bits, activations =
  poids + 3) comparée aux solutions ILP (§4.2.3, Fig. 4).
- Cas d'étude 2 : **ECON-T autoencoder** (compression de données du calorimètre HGCAL de
  CMS), encodeur seul (Conv + FC), métrique EMD (§7).

## Plateforme et implémentation

- Cible de synthèse : « Xilinx Kintex Ultrascale FPGA with part number
  xcu250-figd2104-2L-e » (§6.1). Incohérence : la référence xcu250 est celle de l'Alveo U250
  (Virtex UltraScale+ VU13P, déduit) ; la puce exacte est à vérifier. 200 MHz.
- Ressources : après synthèse RTL pour le jet tagging (§6.1), après placement-routage pour
  ECON-AE (§7) ; design « nu » (réseau seul, sans I/O ni système). BRAM non rapportée
  (utilisée seulement par le softmax).
- Latences **estimées par Vivado HLS** (§6.2) ; aucune exécution sur carte ; aucune mesure
  de puissance.
- Code : extension HAWQ → QONNX annoncée open source ; lien non visible dans le texte extrait.

## Résultats

Jet tagging (Table 2) :

| Modèle | Précision | Latence | LUT | FF | DSP | BOPs |
|---|---|---|---|---|---|---|
| Baseline hls4ml ap_fixed<16,6> | 76,85 % | 65 ns | 60 272 | 15 116 | 3 602 | 4 652 832 |
| INT8 homogène | 76,45 % | 95 ns | 54 888 | 14 210 | 671 | 281 277 |
| Hessien (4, 4, 5, 4 bits) | 75,78 % | 90 ns | 34 842 | 9 622 | 154 | 182 260 |

- Hessien vs baseline : −42,2 % LUT, −36,3 % FF, −95,7 % DSP pour −1,07 point de précision
  (§6.2, §8). Latence +25 à 30 ns à cause des opérations de mise à l'échelle (§6.2).
- Quantification homogène : la précision chute sous INT8 (INT6 73,6 %, INT4 62,5 %,
  Table 1) ; la largeur de la 1re couche détermine l'essentiel de la précision (66 des 100
  meilleurs modèles l'ont en INT8, §4.2.3).
- ECON-AE, encodeur (Table 3) : baseline EMD 1,29, 95 ns, 48 107 LUT, 1 696 DSP ; INT8
  EMD 1,15, 100 ns, 73 078 LUT, 408 DSP ; Hessien (Conv 4 bits, FC 8 bits) EMD 1,24, 95 ns,
  43 942 LUT, 208 DSP.
- Le modèle QB d'AutoQKeras (72,79 %, 60 ns, 5 DSP, Table 2) est un travail antérieur
  ([16]) : non reporté.

→ reportés dans `benchmarks.csv` : **6 lignes** — jet tagging baseline / INT8 / Hessien
(Table 2) et encodeur ECON-AE baseline / INT8 / Hessien (Table 3). FPS et puissance `n/r`.

## Limites et critique

- **Aucune mesure matérielle** : latences estimées par HLS, ressources de synthèse, pas de
  puissance, pas de débit mesuré (le papier s'appuie sur [24] pour dire que les estimations
  HLS sont fiables sur cette tâche).
- **Puce cible ambiguë** (« Kintex UltraScale » vs référence xcu250).
- Modèles minuscules (MLP de ~4 000 paramètres, encodeur à 2 couches) entièrement
  déroulés : les conclusions (bascule DSP/LUT à 11 bits, etc.) ne se transposent pas
  directement à des CNN de vision qui exigent du partage de ressources (déduit).
- Gain de précision de l'approche Hessienne sur la recherche exhaustive non quantifié :
  « pas garanti optimal », seulement « stable et fiable » (§4.2.3).
- Les facteurs d'échelle non quantifiés (16+ bits) coûtent en latence ; hls4ml ne les
  reconnaît pas encore comme dyadiques (§8).

## Pertinence pour la thèse

Contribution à l'axe `toolflows` : chaîne **PyTorch (HAWQ) → QONNX → hls4ml** avec
quantification mixte automatique, interopérable avec FINN via QONNX. Pour la thèse, c'est
une méthode de choix des largeurs par couche (Hessienne + ILP sous budget de BOPs) qu'on
pourrait appliquer à un encodeur convolutif ou à une tête YOLO avant génération hls4ml ou
FINN sur KV260 (déduit). Le cas ECON-AE montre aussi un **autoencodeur convolutif quantifié
pour compression de données de détecteur**, confirmant que les AE sur FPGA viennent surtout
de la physique des particules.

## Gaps identifiés

- Quantification Hessienne + hls4ml/FINN sur **CNN de vision** (détection, AE d'images) :
  non traitée, seulement MLP et encodeur à 2 couches.
- Validation sur carte (latence mesurée, puissance) absente.
- AE sur FPGA toujours cantonnés à la physique des particules dans cette lignée (renforce le
  gap connu sur les images).

## Statut de lecture

Papier complet (`fulltext.md` lu en entier). Début de §4.1 absent (texte repris au milieu) ;
figures non extraites (Fig. 2-4, 6-8 : valeurs lues seulement dans le texte) ; Tables 2 et 3
lisibles.
Déduit et non affirmé par les auteurs : xcu250 = Alveo U250 / VU13P ; non-transposabilité
aux CNN de vision ; usage pour la thèse.
