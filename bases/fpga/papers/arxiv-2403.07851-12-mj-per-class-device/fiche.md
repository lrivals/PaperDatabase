---
id: arxiv-2403.07851-12-mj-per-class-device
fiche: done
date: 2026-09-24
---

# 12 mJ per Class On-Device Online Few-Shot Class-Incremental Learning

Yoga Esa Wibowo, Cristian Cioflan, Thorir Mar Ingolfsson, Michael Hersche, Leo Zhao, Abbas Rahimi, Luca Benini, 2024, 2024 Design, Automation & Test in Europe Conference & Exhibition (DATE). https://doi.org/10.23919/DATE58400.2024.10546598 (texte lu : version arXiv 2403.07851)
Type : conférence (acceptation déclarée dans le commentaire arXiv, DOI éditeur trouvé via Crossref)

## Problème

Apprendre de nouvelles classes à partir de quelques exemples (FSCIL) sans oublier les
anciennes, directement sur un microcontrôleur à batterie : la rétropropagation et les gros
backbones ResNet des méthodes FSCIL existantes sont hors budget mémoire/énergie (Abstract,
§I).

## Méthode

- Architecture : backbone MobileNetV2 (strides réduits pour entrées 32×32, trois variantes
  M, x2, x4 : 25,9 / 45,4 / 149,2 M MAC, 2,5 M paramètres) → Fully Connected Reductor
  (d_a = 1280 → d_p = 256) → mémoire explicite (EM) de prototypes de classe ; inférence par
  similarité cosinus (§IV, Table I).
- Hors ligne (serveur) : pré-entraînement avec Mixup/CutMix et **régularisation
  d'orthogonalité des features** (Eq. 1-2), puis méta-apprentissage avec une **multi-margin
  loss** (m = 0,1) (§IV-B, §IV-C).
- En ligne (appareil) : une nouvelle classe = moyenne des features de ses 5 exemples,
  ajoutée à l'EM, en une seule passe ; fine-tuning optionnel du FCR par descente de
  gradient (§V-B).
- Déploiement : INT8 par TQT (Quantlib) avec époques de QAT, déploiement par DORY (§V-A).
  Prototypes réductibles à 3 bits : 100 classes en 9,6 Ko (§VI-C, Fig. 3).

## Plateforme et implémentation

- MCU GreenWaves GAP9 (fabric controller + cluster de 9 cœurs RISC-V SIMD, L3 externe
  8 Mo), à 650 mV / 240 MHz (§V-A, §VI-C). Pas de FPGA.
- Puissance « mesurée » (§VI-C), ~44-50 mW ; méthode (puce ou carte, instrument) : n/r.
- Jusqu'à 6,5 MAC/cycle sur 8 cœurs pour le plus gros backbone (Fig. 2, §VI-C).
- Code : une note de bas de page « O-FSCIL foot_0 » (§I) laisse supposer un dépôt, mais
  le lien n'est pas dans le texte extrait : n/r.

## Résultats

| Configuration (INT8, GAP9) | Précision moy. CIFAR-100 (session de base + 8 sessions 5-way 5-shot) | Mise à jour EM / classe | Puissance | Énergie / classe | Source |
|---|---|---|---|---|---|
| MobileNetV2 (M) | 62,44 % | 256,65 ms | 44,22 mW | 11,35 mJ | Table II, Table IV |
| MobileNetV2 x2 | 63,19 % | 278,70 ms | 45,75 mW | 12,75 mJ | Table II, Table IV |
| MobileNetV2 x4 | 66,51 % | 513,65 ms | 44,29 mW | 22,75 mJ | Table II, Table IV |
| MobileNetV2 x4 + FT FCR | 66,56 % | 6428,7 ms (fine-tune) | 50,05 mW | 321,75 mJ (fine-tune) | Table II, Table IV |

- Meilleure précision : 68,62 % avec ResNet-12 FP32 + FT, évaluée sur GTX 1080 Ti, non
  déployée (Table II) ; NC-FSCIL : 67,50 %.
- INT8 ≈ FP32 (62,44 vs 62,37 % pour M) (Table II, §VI-C).
- Ablation (ResNet-12) : l'orthogonalité apporte +1,65 à +2,87 points ; le
  méta-apprentissage en cross-entropy dégrade (64,56 %) (Table III, §VI-B).

→ reportés dans `benchmarks.csv` : 3 lignes (M, x2, x4 sans FT ; Table II + Table IV,
`high`).

## Limites et critique

- **Titre et abstract combinent deux configurations.** « 68,62 % » vient de ResNet-12 FP32
  sur GPU avec fine-tuning ; « 12 mJ » vient du plus petit MobileNetV2 INT8 sur GAP9, qui
  plafonne à 62,44 %. La configuration déployée la plus précise (x4, 66,51 %) coûte 22,75 mJ.
- Un seul benchmark (CIFAR-100, images 32×32) : aucune preuve de passage à l'échelle vers
  des résolutions réalistes, ni vers des flux non curés.
- Temps et énergie « par classe, pour 5 exemples » (Table IV) : le coût par image n'est pas
  donné explicitement ; la comparaison aux 167 mJ du neuromorphique ([31], §II-B) porte sur
  des tâches et jeux différents.
- Les comparaisons d'état de l'art (Table II) sont en précision seulement, sur GPU FP32 ;
  aucune autre méthode n'est déployée sur la même cible.
- Protocole de mesure de puissance non décrit.

## Pertinence pour la thèse

Référence MCU pour l'axe apprentissage continu : borne d'énergie (~11-23 mJ par nouvelle
classe à ~45 mW) qu'un accélérateur FPGA de CL devra battre ou justifier. Le schéma
« backbone gelé + mémoire de prototypes » est directement transposable sur FPGA (le
backbone en streaming, l'EM sur puce), comme le fait ImageHD avec HDC. Ne traite pas la
détection d'objets.

## Gaps identifiés

- Aucune comparaison MCU vs FPGA pour le même algorithme de FSCIL : la question du
  meilleur support pour le CL embarqué reste ouverte.
- FSCIL évalué sur petites images de classification seulement ; rien sur la détection ni
  sur l'incrémental de classes en détection.

## Statut de lecture

Papier complet (`fulltext.md` lu en entier). Extraction : la conclusion (VII) est fusionnée
dans §VI-C et dans une légende ; une partie des contributions est dans « Figures et
tableaux ».
Déduit et non affirmé par les auteurs : existence d'un dépôt de code ; lecture de la
tension entre titre et configurations ; transposabilité sur FPGA.
