---
id: 2021-guo-fpga-uav-heterogeneous-computing-platform
fiche: done
date: 2026-09-28
benchmarks: none
---

# FPGA-based UAV Heterogeneous Computing Platform Architecture

Junpeng Guo, Bo Jiang, Hong Xu, 2021, 2021 6th International Conference on Computational Intelligence and Applications (ICCIA) 252-256. https://doi.org/10.1109/ICCIA52886.2021.00056
Type : conférence

## Problème

Les petits UAV (30-40 cm entre pales, ~2 kg au total, ~400 g disponibles pour le cœur de
calcul) ne peuvent pas embarquer l'architecture courante Jetson + Pixhawk 4 (~300 g
selon les auteurs, câbles en sus), jugée trop lourde, trop gourmande et mal intégrée
(deux ARM séparés, Cortex-M4 pour le vol, Cortex-A9 pour l'image) (Abstract, §I). Les
auteurs proposent une architecture hétérogène **FPGA-ARM-GPU** où le FPGA fait le
transfert et l'accélération des données.

## Méthode

Proposition d'architecture, sans évaluation (§III) :
- **Zynq XC7Z020** (PL) + Cortex-A9 (PS) + carte GPU NVIDIA externe ; Pixhawk 4 démonté,
  seul son Cortex-M4 garde les capteurs et la caméra (§III, Fig. 1-2).
- Bus : AXI entre FPGA et ARM ; I2C capteurs → ARM, SPI vers le FPGA ; FPGA ↔ GPU par
  PCIe **sans passer par l'ARM**, mémoire FPGA mappée sur le bus et lue par le GPU via
  CUDA (FPGA esclave, GPU maître), faute de GPUDirect RDMA sur GPU grand public (§III,
  Fig. 5).
- IP FPGA (Fig. 3-4) : *Sensor core* (IMU en entiers 16 bits, caméras MIPI), *Identify
  core* (aiguillage IMU / image), *Accelerate core* (filtrage de l'IMU, fusion et
  compression multi-caméras), *Control core* (PID roulis/tangage, sortie 6 rapports
  cycliques). HLS ou Verilog.
- GPU : inférence d'un modèle de **pose humaine** (OpenPose envisagé, à compresser) —
  **pas de détection d'objets** (§III, « Model selection »).
- Prototype physique : Zynq-7020, Jetson AGX Xavier, 8 caméras + Structure Core, châssis
  DJI S450, moteurs 3508, charge max 2 kg (§IV, Fig. 6-7).

## Plateforme et implémentation

- Xilinx Zynq-7000 **XC7Z020** et **Jetson AGX Xavier** dont les auteurs disent n'utiliser
  « only the GPU core », en retirant la partie CPU ARMv8 (§IV-B) — affirmation
  techniquement douteuse, le GPU étant intégré au SoC Xavier (déduit).
- Fréquence, ressources FPGA (LUT/DSP/BRAM), latence, débit, poids réel, puissance :
  **tous n/r**. La Fig. 4 est une simulation RTL après synthèse, sans chiffres dans le
  texte.
- Code / bitstream : non publiés.

## Résultats

Aucun résultat quantitatif sur la plateforme proposée. Les seuls chiffres sont des
arguments d'introduction repris d'autres travaux : efficacité énergétique FPGA > 2× GPU
pour le filtrage et les transformations d'image ([3]) ; Cortex-A9 à 24,2 Mpixels/s contre
5,68 Mpixels/s pour le Cortex-M4 ([4]) (§I).

→ reportés dans `benchmarks.csv` : aucune ligne. Le papier ne rapporte ni débit, ni
latence, ni ressources, ni puissance pour son propre système (`benchmarks: none`).

## Limites et critique

- **Papier de position sans évaluation** : aucune mesure de latence, de puissance, de masse
  ou de ressources, alors que les motivations sont précisément la masse, l'énergie et la
  réactivité (§I).
- **Incohérence du bilan de masse** : le problème posé est la lourdeur de Jetson +
  Pixhawk, et le prototype ajoute un Zynq-7020 à une **Jetson AGX Xavier** (module plus
  lourd et plus gourmand que les Jetson de la série Nano/NX, déduit) et 8 caméras.
- **« GPU seul de la Xavier, sans CPU »** : non réalisable sur un SoC tel que décrit
  (déduit) ; la liaison PCIe FPGA → GPU n'est pas démontrée.
- **Pas de vision par DNN sur FPGA** : le FPGA ne fait que capteurs, filtrage, PID et
  assemblage d'images ; l'IA (pose humaine) reste sur GPU, et le modèle n'est pas choisi
  définitivement.
- Rédaction peu rigoureuse (références génériques, affirmations non sourcées) ;
  conférence de faible visibilité (ICCIA).

## Pertinence pour la thèse

- Faible sur le plan quantitatif, mais le papier illustre l'axe `system-codesign` / 
  `drone-fpga` : **intégrer le contrôle de vol (PID) et la perception sur le même SoC
  FPGA** pour réduire masse et câblage — idée utile pour une architecture de thèse
  (co-localisation contrôleur + détecteur sur Zynq / Kria).
- Montre que la communication FPGA ↔ GPU sans ARM et la répartition des tâches entre
  accélérateurs sont des questions de conception ouvertes, jamais chiffrées ici.
- À citer avec prudence, comme exemple de proposition non évaluée.

## Gaps identifiés

- **Plateformes hétérogènes FPGA + GPU sur drone non évaluées** : masse, puissance et
  latence de bout en bout absentes — confirme le gap « aucune métrique système ».
- **Contrôle de vol et détection sur le même FPGA** : proposé ici sans DNN sur la PL ;
  aucune mesure de l'interférence entre boucle de contrôle et accélérateur de vision.

## Statut de lecture

Papier complet (`fulltext.md` lu en entier, extraction GROBID `ok`). La section I n'a pas
été détectée comme titre (sans perte apparente). Papier court (5 pages), sans tableau.

Ce qui suit est déduit et non affirmé par les auteurs :
- l'impossibilité d'utiliser le GPU de la Jetson AGX Xavier sans son CPU ;
- la masse et la consommation supérieures de la Xavier par rapport aux Jetson Nano/NX ;
- l'intérêt de la co-localisation contrôle + vision sur Zynq pour la thèse.
