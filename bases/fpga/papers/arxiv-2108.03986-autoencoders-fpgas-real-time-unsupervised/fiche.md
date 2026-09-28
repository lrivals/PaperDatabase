---
id: arxiv-2108.03986-autoencoders-fpgas-real-time-unsupervised
fiche: done
date: 2026-09-24
---

# Autoencoders on FPGAs for real-time, unsupervised new physics detection at 40 MHz at the Large Hadron Collider

Govorkova et al., 2021, Nature Machine Intelligence 4, 154 (2022). arXiv 2108.03986
Type : article de journal. La fiche est rédigée sur la version arXiv, qui peut différer de la
version publiée.

## Problème

Sélectionner en temps réel des collisions « anormales » au premier niveau de déclenchement
(L1T) du LHC, sans hypothèse sur la nouvelle physique cherchée (§I). Contraintes (§I) :
- latence de l'ordre de 1 µs ;
- intervalle d'initiation (II) d'au plus 150 ns (115 ns dans le §VII) ;
- une petite fraction des ressources, car plusieurs algorithmes partagent le FPGA.

## Méthode

- **Données :** 19 objets reconstruits × (p_T, η, φ), soit une entrée 19 × 3. Ce sont des
  **données tabulaires traitées comme une image 2D** pour tester des CNN, pas de vraies
  images (§III).
- **Quatre modèles (§III) :**
  - DNN AE 57-32-16-3 et son VAE ;
  - CNN AE (Conv 16 × 3×3, puis 32 × 3×1, latent de 8) et son VAE.
  Une batch norm en tête de réseau intègre le pré-traitement sur puce.
- **Scores d'anomalie (§IV) :**
  - AE : MSE entre entrée et sortie, calculée sur le FPGA par une couche hls4ml ajoutée
    par les auteurs ;
  - VAE : score D_KL calculé depuis (µ, σ) de l'**encodeur seul**. Cela évite
    l'échantillonnage gaussien sur FPGA (décision non déterministe) et le calcul du décodeur.
- **Compression (§VI) :**
  - pruning à 50 % ;
  - balayage de 2 à 16 bits en QAT (QKeras) et en PTQ ;
  - choix final : QAT pour les AE ; **PTQ pour les VAE**, car le QAT minimise la perte de
    reconstruction et non le score D_KL utilisé en inférence, ce qui le rend instable.
- **Déploiement (§VII) :** hls4ml, puis Vivado HLS 2020.1, pour un VU9P à 200 MHz.
  Intégration du DNN VAE dans le firmware de trigger emp-fwk sur une carte VCU118, à
  240 MHz.

## Plateforme et implémentation

- **Puce :** Xilinx Virtex UltraScale+ VU9P (xcvu9p-flgb2104-2-e), 200 MHz (§VII).
  Estimation supplémentaire pour un Virtex-7 690 (Table IV).
- **Ressources et latence :** **estimations Vivado HLS**, et non résultats d'implémentation
  (Table III). Elles sont exprimées en pourcentage du VU9P, pas en nombre absolu.
- **Validation sur carte :** DNN VAE seul, sur VCU118 à 240 MHz. Les prédictions sont
  « cohérentes » avec la simulation C, sans chiffre d'écart (§VII).
- **Puissance :** non mesurée.
- **Code :** publié. QKeras 0.9.0, et une branche hls4ml `AE_L1_paper` avec les couches
  ajoutées (§IX). Données publiques sur Zenodo (§II, §X).

## Résultats

Table III (VU9P, modèles élagués à 50 %) :

| Modèle | Précision | DSP | LUT | FF | BRAM | Latence | II |
|---|---|---|---|---|---|---|---|
| DNN AE | QAT 8 b | 2 % | 5 % | 1 % | 0,5 % | 130 ns | 5 ns |
| CNN AE | QAT 4 b | 8 % | 47 % | 5 % | 6 % | 1480 ns | 895 ns |
| DNN VAE (encodeur) | PTQ 8 b | 1 % | 3 % | 0,5 % | 0,3 % | **80 ns** | 5 ns |
| CNN VAE (encodeur) | PTQ 8 b | 10 % | 12 % | 4 % | 2 % | 365 ns | 115 ns |

- **Virtex-7 690, DNN VAE (Table IV) :** 205 ns, II de 5 ns, 9 % des LUT.
- **Détection (Table II), AUC pour les quatre signaux** (LQ → bτ, A → 4ℓ, h± → τν,
  h0 → ττ) :
  - DNN AE : 95, 96, 96 et 88 % ;
  - DNN VAE : 92, 94, 94 et 81 % ;
  - TPR à un FPR de 10⁻⁵ : de 0,05 % à 5,96 %, selon le modèle et le signal.
- **Rejet :** seul le CNN AE est exclu, car il dépasse le budget de ressources et d'II
  (§VII).

→ reportés dans `benchmarks.csv` : 5 lignes (4 pour le VU9P, 1 pour le Virtex-7 690). La
métrique retenue est l'AUC sur le signal A → 4ℓ ; les autres signaux sont dans la fiche.
`luts`, `dsps` et `bram` valent `n/r` : seuls des pourcentages sont rapportés, et les
convertir en nombres absolus serait un calcul de ma part.

## Limites et critique

- **Incohérence entre texte et tableaux :** le §VI dit « QAT CNN … 8 bits » et « PTQ CNN
  VAE … 4 bits », alors que les Tables II et III indiquent CNN AE en QAT 4 bits et CNN VAE
  en PTQ 8 bits. Les lignes de `benchmarks.csv` suivent les tables, et le signalent.
- **Latence et ressources estimées (HLS C Simulation, Vivado HLS), pas mesurées.** Une
  seule validation sur carte (DNN VAE), et qualitative.
- **Pas de puissance :** normal pour l'application (FPGA de trigger sous-utilisé), mais
  cela empêche toute comparaison avec l'embarqué.
- **Données tabulaires de très petite dimension** (57 valeurs) : les conclusions (80 ns,
  3 % des LUT) ne se transposent pas à des images réelles. C'est exactement le gap
  « autoencodeurs sur images ».
- **Cible :** un FPGA de centre de calcul (VU9P), pas un SoC embarqué.

## Pertinence pour la thèse

- **Référence méthodologique pour la détection d'anomalies par autoencodeur sur FPGA :**
  - score calculé sur la puce (couche de perte ajoutée à hls4ml) ;
  - VAE réduit à l'encodeur, avec score D_KL, ce qui divise la latence par deux environ
    (§VIII) et supprime le décodeur ;
  - choix PTQ ou QAT selon la stabilité du score d'anomalie, pas selon la perte
    d'entraînement.
  Ces trois idées sont transposables à un CAE ou VAE d'images.
- **Montre une limite concrète :** le seul modèle convolutionnel « type image » (CNN AE)
  est aussi celui qui ne tient pas (47 % des LUT, II de 895 ns), sur une entrée de
  seulement 20 × 3. Pour des images réelles, le passage à l'échelle est le verrou.

## Gaps identifiés

- **Autoencodeurs sur images (anomalie visuelle) :** étaye le gap. Même le CNN du papier
  traite des données tabulaires, et il est le seul modèle à dépasser le budget.
- **Quantification et score d'anomalie :** le QAT optimise la reconstruction, pas le score
  d'anomalie (§VI). Une quantification guidée par le score (distillation, classification
  du seuil, citées en §I comme pistes non explorées) reste ouverte.
- **Précision après compilation :** le papier compare simulation C et carte pour un modèle,
  sans chiffrer l'écart (§VII). C'est le même motif que le gap « précision non vérifiée sur
  la cible », en version favorable (le contrôle est au moins fait).

## Statut de lecture

Papier complet (`fulltext.md` lu en entier, version arXiv, extraction GROBID `ok`). Le
Tableau I (performances en flottant) est vide dans l'extraction.

Ce qui suit est déduit et non affirmé par les auteurs :
- la non-transposabilité aux images ;
- l'intérêt des trois idées pour un CAE d'images ;
- la lecture de l'échec du CNN AE comme verrou de passage à l'échelle.
