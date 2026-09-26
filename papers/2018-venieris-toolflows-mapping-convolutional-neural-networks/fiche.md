---
id: 2018-venieris-toolflows-mapping-convolutional-neural-networks
fiche: done
date: 2026-09-26
---

# Toolflows for Mapping Convolutional Neural Networks on FPGAs: A Survey and Future Directions

Stylianos I. Venieris, Alexandros Kouris, Christos-Savvas Bouganis, 2018, ACM Comput. Surv. 51(3), 56. https://doi.org/10.1145/3186332
Type : article de journal (ACM Computing Surveys, relu par les pairs). Survey.

## Problème

Les frameworks de deep learning ciblent CPU et GPU ; les FPGA pourraient offrir un meilleur
compromis performance / puissance / programmabilité, mais les outils HLS génériques ne
tiennent pas compte de la structure des CNN. Les auteurs recensent les **toolflows
CNN→FPGA** (logiciel qui mappe directement une description haut niveau de CNN vers une
architecture d'inférence, sous contraintes de ressources d'un FPGA cible, §1), les comparent,
et proposent une méthodologie d'évaluation uniforme (§3.1).

## Méthode

Survey de 13 toolflows (Table 6) : fpgaConvNet, DeepBurning, Angel-Eye, ALAMO, Haddoc2,
DnnWeaver, Caffeine, AutoCodeGen, FINN, FP-DNN, Snowflake, SysArrayAccel, FFTCodeGen.
Axes de comparaison :

- **Interface** (§2.2.1) : Caffe dominant (7 outils) ; Torch (fpgaConvNet, Snowflake),
  TensorFlow (FP-DNN), Theano (FINN) ; front-ends propriétaires pour 3 outils.
- **Portabilité** (§2.2.2) : DnnWeaver la plus large (Xilinx + Intel, SoC et serveur).
- **Architecture** (§2.3) :
  - *streaming* (un bloc matériel par couche, pipeline) : fpgaConvNet, DeepBurning, Haddoc2,
    AutoCodeGen, FINN ; efficace mais un bitstream par CNN ;
  - *moteur de calcul unique* (réseau systolique ou multiplication matricielle piloté par
    logiciel) : Angel-Eye, ALAMO, DnnWeaver, Caffeine, FP-DNN, Snowflake, SysArrayAccel,
    FFTCodeGen ; flexible, un seul bitstream pour plusieurs CNN.
- **Exploration de l'espace de conception** (§2.4) : optimisation contrainte avec recuit
  simulé (fpgaConvNet), roofline exhaustif (Caffeine), modèles analytiques + élagage
  (SysArrayAccel), heuristiques d'équilibrage de débits (FINN, DeepBurning, AutoCodeGen),
  mapping déterministe (Haddoc2).
- **Précision** (§2.5) : quantification dynamique par couche (Angel-Eye automatisée,
  ALAMO, AutoCodeGen, DnnWeaver, DeepBurning) vs uniforme (Caffeine, fpgaConvNet, FP-DNN,
  SysArrayAccel, FFTCodeGen, Haddoc2 ; Snowflake 16 bits fixe) ; FINN binaire.
- **Performance** (§2.6, Tables 2-5) : chiffres rassemblés depuis les publications et par
  échange avec les auteurs, comparés seulement à paire CNN-FPGA identique (AlexNet, VGG16
  principalement) et avec des designs faits main.

## Plateforme et implémentation

Sans objet (survey). Plateformes couvertes : Zynq XC7Z020 / XC7Z045, UltraScale KU060 /
KU115, Virtex-7 VX690T, Stratix V, Arria 10, Intel HARP (§2.2.2). Disponibilité du code à
l'écriture (§2.6) : DnnWeaver (open source, support limité XC7Z020), Haddoc2 (open source),
FINN (version légère pour PYNQ-Z1), fpgaConvNet (page de résultats seulement), Angel-Eye
(usage interne DeePhi) ; les autres non publiés.

## Résultats

Survey : **aucune ligne ajoutée à `benchmarks.csv`** (les chiffres sont ceux des travaux
cités). Principaux constats, à citer comme rapportés par le survey :

- Zynq XC7Z020, AlexNet (conv.) : fpgaConvNet 38,30 GOp/s, 2,06× DeepBurning et 1,9×
  DnnWeaver (§2.6, Fig. 4a).
- Zynq XC7Z045, VGG16 : Angel-Eye 187,80 GOp/s (conv.) et 136,97 GOp/s (réseau complet),
  1,20× fpgaConvNet en débit conv. et 1,52× moins de latence ; à fréquence normalisée, débit
  équivalent (§2.6, Table 3).
- Arria 10, AlexNet : SysArrayAccel 360,4 GOp/s (FP32), 1,95× DnnWeaver ; mais seulement
  26 % du DLA d'Intel (1,382 TFLOp/s, conçu à la main) (§2.6, Table 4).
- FFTCodeGen (convolution par FFT, Stratix V GXA7) : 780,60 GOp/s sur AlexNet (Table 4),
  au prix d'un batch obligatoire (§2.6).
- Haddoc2 bat fpgaConvNet sur LeNet-5 / CIFAR-10 (1,71× / 2,63×), mais en 3 et 6 bits
  contre 16 bits (§2.6).
- Enseignements (§2.7) : RTL optimisé > HLS ; une DSE plus fine donne de meilleurs
  résultats ; les moteurs uniques profitent des réseaux réguliers (VGG16) et souffrent des
  noyaux hétérogènes (AlexNet).
- **Méthodologie d'évaluation proposée** (§3.1) : suite de référence (AlexNet, ZFNet,
  VGG16, GoogLeNet, ResNet-152, Inception-v4, DenseNet-161, Table 7) ; débit en GOp/s avec
  GOp/réseau, poids et batch explicités ; latence en batch 1 ; ressources ; puissance ;
  précision applicative ; spécification mémoire on/off-chip. Les métriques normalisées
  (GOp/s/DSP, /kLUT) ne valent que dans une même famille de FPGA (§3.1).
- Objectifs futurs (§3.2) : nouveaux CNN (blocs résiduels, Inception, dense), RNN/LSTM,
  réseaux compressés et creux, très basse précision (binaire, ternaire), intégration aux
  frameworks (TensorFlow, PyTorch…), entraînement sur FPGA, co-conception réseau-matériel.

## Limites et critique

- **Chiffres non vérifiés** : aucun outil n'est relancé ; les performances viennent des
  publications ou des auteurs (§2.6). Les auteurs de fpgaConvNet sont aussi les auteurs du
  survey : fpgaConvNet est souvent présenté favorablement (« finer exploration »), à lire
  avec recul (déduit).
- Comparaisons mêlant FP32, 16 bits et 3-6 bits, batch 1 et gros batches ; les auteurs le
  reconnaissent partiellement et normalisent par DSP ou kLUT, ce qu'ils critiquent eux-mêmes
  en §3.1.
- **Aucune donnée de puissance ni de précision** dans les tableaux comparatifs : la
  méthodologie proposée les réclame mais le survey ne les fournit pas.
- Aucune comparaison GPU / SoC embarqué.
- Daté (2018) : ni Vitis AI, ni hls4ml, ni FINN-R, ni détection d'objets (YOLO) ; tous les
  benchmarks sont de la classification ImageNet ou plus petite.

## Pertinence pour la thèse

Référence de base pour l'axe `toolflows` : la taxonomie *streaming* vs *moteur unique* et la
critique des métriques normalisées structurent toute la littérature qui suit (FINN-R,
fpgaConvNet TNNLS, SATAY, hls4ml). La méthodologie d'évaluation (§3.1) est une grille
directement réutilisable pour le protocole expérimental de la thèse (déduit) : débit +
latence batch 1 + puissance + précision + mémoire. Ce qu'elle laisse ouvert : détection,
autoencodeurs, apprentissage embarqué.

## Gaps identifiés

- Pas de toolflow ciblant la détection d'objets ou les autoencodeurs en 2018 (seulement
  classification).
- Entraînement sur FPGA « à peine exploré » (§3.2, objectif 5) : rejoint le gap
  apprentissage continu embarqué.
- Protocole d'évaluation uniforme proposé mais, à la lecture du corpus, peu appliqué depuis :
  toujours pas de benchmark commun puissance + précision (déduit).
- Co-conception réseau-matériel automatisée (§3.2, objectif 6) identifiée comme horizon.

## Statut de lecture

`fulltext.md` lu en entier, mais **extraction incomplète** : l'intro de la section 2 et
§2.1 manquent (« sections numérotées non détectées : 2 ») ; le texte s'arrête au milieu de
l'objectif 6 (§3.2) : fin de §3.2 et conclusion absentes. Table 2 (AlexNet sur Zynq) sans
corps ; Tables 3 et 5 aplaties et difficiles à lire colonne par colonne.
Déduit et non affirmé par les auteurs : biais potentiel envers fpgaConvNet ; faible
adoption ultérieure du protocole ; applicabilité de la grille au protocole de la thèse.
