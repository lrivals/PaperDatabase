---
id: 2019-tsukada-neural-network-device-learning-anomaly
fiche: done
date: 2026-09-26
---

# A Neural Network-Based On-device Learning Anomaly Detector for Edge Devices

Mineto Tsukada, Masaaki Kondo, Hiroki Matsutani, 2020, IEEE Transactions on Computers. https://doi.org/10.1109/TC.2020.2973631 (version préliminaire : arXiv 1907.10147, 2019)
Type : article de journal (IEEE TC, relu par les pairs ; le PDF lu est la version IEEE TC)

## Problème

La détection d'anomalies semi-supervisée apprend la distribution des données normales. Avec
des réseaux entraînés par rétropropagation (BP-NN), l'entraînement itératif se fait sur
serveur : (1) il suit mal la **dérive de concept** (la distribution normale change dans le
temps), (2) les transferts edge ↔ serveur coûtent latence, énergie et confidentialité (§1).
Les auteurs proposent un apprentissage **séquentiel sur l'appareil**, et son cœur matériel.

## Méthode

- **ONLAD** : autoencodeur à une couche cachée entraîné par **OS-ELM** (Online Sequential
  Extreme Learning Machine) : poids d'entrée aléatoires figés, seuls les poids de sortie
  sont mis à jour par moindres carrés récursifs (§2.2, §3.3). Score d'anomalie = erreur de
  reconstruction (MSE) (Eq. 17).
- **Batch = 1** : la seule inversion matricielle devient une division scalaire (Eq. 7),
  sans changer la solution (N pas de batch k ≡ Nk pas de batch 1) (§3.1).
- **Mécanisme d'oubli léger** : version de FP-ELM sans régularisation L2, avec facteur
  d'oubli α (Eq. 13-15) ; coût O(Ñ²) au lieu de O(Ñ³) (§3.2, §6.2.2).
- Garde-fou de stabilité : l'apprentissage est sauté si le dénominateur < ε = 1e-4 (§3.4,
  §4.2.3).
- **ONLAD Core** (§4) : IP Vivado HLS 2018.3, **100 MHz** ; modules Parameter Buffer, Input
  Buffer, Train, Predict ; tous les paramètres en BRAM ; arithmétique **virgule fixe 32
  bits** sur DSP ; déroulage d'ordre 2 seulement (§4.2.5) ; jeu de 5 instructions par paquets
  AXI4-Stream depuis le PS via DMA (§4.1, §4.3).

## Plateforme et implémentation

- **PYNQ-Z1**, Zynq-7000 **XC7Z020-1CLG400C** (Cortex-A9 650 MHz, 280 BRAM, 220 DSP, 53 200
  LUT), PYNQ v2.4 (Table 1).
- Ressources pré-synthèse (Table 9) : DSP 40 %, LUT ≈ 30 %, FF ≈ 16 % constants ; BRAM de
  10 % (n = 128, Ñ = 16) à 104,2 % (n = 1 024, Ñ = 64, seule configuration qui ne tient pas).
- Configuration mesurée (n = 512, Ñ = 64), post-implémentation (Table 10, Docling) : BRAM
  55,4 %, DSP 32,7 %, FF 11,6 %, LUT 25,8 %. Les comptes absolus ne sont pas donnés → `n/r`
  dans `benchmarks.csv`.
- Puissance : **3,1 W**, wattmètre sur la carte PYNQ-Z1 entière, ARM inclus (§6.4) →
  `board`. CPU mesuré par s-tui, GPU par nvidia-smi : portées différentes.
- Code / bitstream : non publiés dans le texte extrait.

## Résultats

- Capacité de détection (modèles en TensorFlow, pas sur FPGA) :
  - hors ligne, AUC ONLAD 0,905 à 0,952 selon le jeu, 0,01-0,03 sous NN-AE / DNN-AE
    (Table 4) ;
  - en ligne avec dérive de concept, AUC ONLAD 0,781-0,899 contre 0,548-0,591 sans oubli
    (ONLAD-NF) ; +0,10 à +0,18 sur NN-AE / DNN-AE pour 3 jeux sur 5 (Fashion-MNIST, MNIST,
    Letter), comparable sur les 2 autres (Table 5, §5.3).
- Latence (moyennes sur 50 000 essais, n ∈ {128…1 024}, Ñ ∈ {16, 32, 64}) : entraînement
  1,95× à 6,58× plus rapide que les versions CPU/GPU TensorFlow en batch 1 ; prédiction
  2,29× à 4,73× (§6.2.1, Fig. 11-12) ; « moins d'une milliseconde » par échantillon. Valeurs
  absolues en Fig. 11-12, non extraites.
- Oubli proposé 3,21× plus rapide que FP-ELM (versions CPU) (§6.2.2).
- Puissance en entraînement continu : 3,1 W, 5,0× à 25,4× moins que CPU i7-6700 / GTX 1070
  (§6.4, Fig. 18).

→ reportés dans `benchmarks.csv` : **1 ligne** — ONLAD Core (n = 512, Ñ = 64), XC7Z020,
3,1 W `board`. Précision, latence et ressources absolues `n/r` (AUC mesurées en logiciel sur
d'autres tailles ; latences en figures ; ressources en %).

## Limites et critique

- **Baselines faibles pour la latence** : TensorFlow 1.13 en batch 1 sur CPU/GPU, dominé par
  les surcoûts d'appel (les auteurs le reconnaissent, §6.2.1). Un code C natif ou un MCU
  aurait été un meilleur point de comparaison (déduit). Au-delà de ~1 000 entrées, le cœur
  ne gagne plus (§6.2.1).
- **Puissance non comparable** : carte entière (3,1 W, avec l'ARM) contre CPU seul (s-tui)
  et GPU seul (nvidia-smi). Le rapport 5-25× mélange des portées différentes.
- Pas de mesure d'énergie par échantillon ; ressources de la Table 9 en pré-synthèse.
- **Données tabulaires ou images aplaties** (MNIST 784 pixels) ; pas de convolution. Le
  modèle est une seule couche cachée à poids d'entrée aléatoires : capacité limitée pour des
  images réelles.
- AUC évaluées en logiciel (flottant ?) et non sur le cœur en virgule fixe 32 bits : l'effet
  de la quantification n'est pas mesuré (déduit).
- Dérive simulée par permutation de classes, protocole artificiel.

## Pertinence pour la thèse

Papier clé au croisement des axes `autoencoder-fpga` et `continual-learning` : c'est l'un
des rares **apprentissages embarqués sur FPGA** complets, avec un autoencodeur, une gestion
de la dérive de concept et une mesure de puissance carte sur une petite plateforme
(PYNQ-Z1). L'astuce OS-ELM batch 1 (pas d'inversion matricielle, pas de rétropropagation)
est une piste concrète pour de l'adaptation en ligne sur KV260. Elle pourrait par exemple
tourner sur les caractéristiques d'un extracteur CNN figé (déduit).

## Gaps identifiés

- OS-ELM / ONLAD sur **images réelles**, par exemple en tête d'un encodeur convolutif figé :
  non traité ; les auteurs envisagent seulement un OS-ELM multicouche (§8.2).
- Effet de la virgule fixe sur l'apprentissage séquentiel : non mesuré.
- Aucune comparaison avec un MCU ou un Jetson pour l'apprentissage embarqué.
- Protocole de puissance hétérogène (carte vs CPU seul vs GPU seul).

## Statut de lecture

Papier complet (`fulltext.md` lu en entier). Extraction GROBID bruitée : équations
illisibles (caractères de substitution), §4.3.3-4.3.4 et §7.1, 7.4-7.5 partiellement
perdus ou déplacés dans les légendes, Table 6 absente, Tables 8 et 10 reconstruites par
Docling. Les valeurs absolues de latence (Fig. 11-14) et de puissance des baselines
(Fig. 18) ne sont pas dans le texte.
Déduit et non affirmé par les auteurs : meilleure baseline possible (C natif, MCU) ; AUC
mesurées hors virgule fixe ; usage d'OS-ELM en tête d'un encodeur CNN figé.
