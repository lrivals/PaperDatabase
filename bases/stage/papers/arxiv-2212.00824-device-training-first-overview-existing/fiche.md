---
id: arxiv-2212.00824-device-training-first-overview-existing
fiche: done
date: 2026-09-29
---

# On-Device Training: A First Overview on Existing Systems

Shuai Zhu, Thiemo Voigt, Fatemeh Rahimian, JeongGil Ko, 2024, ACM Transactions on Sensor Networks. https://doi.org/10.1145/3696003
Type : article de journal (survey ; version arXiv initiale 2022)

## Problème

L'entraînement sur l'appareil permet la confidentialité, la personnalisation, l'adaptation à
l'environnement et le déploiement hors connexion, mais la rétropropagation consomme 4 à 103 fois
plus de mémoire que l'inférence et les appareils sont très hétérogènes (Abstract, §1, §4.1). Le
papier fait un état des lieux **du point de vue systèmes** (§1.2).

## Méthode

Survey de **onze systèmes** publiés de 2019 à 2023 (MobiCom, SenSys, IPSN, MobiSys, EWSN, AAAI, ICLR,
ICML, NeurIPS, IJCAI), plus Miro en marge ; hors apprentissage fédéré et hors plateformes Jetson
seules (§1.2, §2).

- **Classes d'appareils** : fortement contraints (centaines de Ko), moyennement (centaines de Mo),
  faiblement (quelques Go) (§2.3, Table 2).
- **Quatre paradigmes** (§2) : *one-stage* (TinyTL, MiniLearn), *two-stage* avec plan
  d'exécution préparé (POET, Mandheling, Melon, Sage, TTE, ElasticTrainer), **continual learning**
  (MDLdroidLite par croissance continue, LifeLearner par méta-CL + rejeu compressé), apprentissage
  par renforcement (zTT, DVFS).
- **Techniques** (§4) : recalcul (gradient checkpointing), micro-batch, pagination (mémoire) ;
  quantification, déquantification, précision mixte, élagage, mise à jour parcimonieuse,
  croissance continue, ajout de couches (modèle) ; délestage sur DSP (matériel).
- Synthèse des gains rapportés (précision, mémoire, énergie, vitesse) par système (§5, Table 4).

## Plateforme et implémentation

Sans objet (survey). Les MCU couverts : nRF52840 (MiniLearn), STM32F746 à 320 Ko de SRAM (TTE),
Arduino MKR1000 (POET) (Table 2, §2.5).

## Résultats

Pas de ligne dans `benchmarks.csv` (survey ; chiffres des systèmes cités non repris). Chiffres
rapportés, utiles comme ordres de grandeur (à vérifier dans les papiers sources) :
- **MiniLearn** (nRF52840) : réentraînement avec 100 échantillons en 6-10 s et 138-254 mJ ; avec
  600 échantillons en 30-56 s et 786-1016 mJ ; RAM 92-196 Ko pour réentraîner tout le réseau,
  6-12 Ko pour les seules couches denses (§5.3-5.5).
- **TTE** (STM32F746) : mises à jour parcimonieuses → mémoire de pointe ÷ 7-9 ; avec
  réordonnancement du graphe ÷ 20-21 ; vitesse ×23-25 par rapport aux noyaux TFLite Micro ;
  « quantization-aware scaling » pour entraîner un modèle quantifié (§2.5, §5.3, §5.5).
- **LifeLearner** : −0,2 point (CIFAR-100) et −2,7 (MiniImageNet) par rapport à l'oracle ; énergie
  −80,9 à −96 % par rapport au méta-CL de référence (§5.2, §5.4).
- **TinyTL** : mémoire d'entraînement ÷ 6 en ne réglant que les biais + « lite residual » (§5.3).

## Limites et critique

- Échantillon réduit (11 systèmes), biaisé vers smartphones et Jetson/Raspberry ; seuls 3 systèmes
  visent des MCU (reconnu en conclusion, §7).
- Pas de comparaison homogène : les gains sont repris des papiers avec leurs propres baselines
  (Table 4) ; aucune ré-expérimentation.
- La partie CL est brève (deux systèmes) et ne traite pas la régularisation (EWC, SI) sur appareil.
- Texte extrait par morceaux dans le désordre (fragments de §2.4-2.5 et de §5 intercalés), ce qui
  n'affecte pas les chiffres cités mais rend certaines attributions à vérifier.

## Pertinence pour la thèse

Carte utile des techniques d'entraînement embarqué, avec les ordres de grandeur MCU les plus
directement comparables au stage : MiniLearn (réentraînement sur nRF52840 en quelques secondes et
centaines de mJ) et TTE (entraînement de modèles quantifiés sur STM32F746, 320 Ko). Il confirme que
la mémoire des activations est le goulot, et que la mise à jour partielle (couches denses, biais)
est la voie pratique sur MCU — cadre dans lequel un EWC limité aux couches entraînées reste peu
coûteux (déduit). Il note l'absence de systèmes CL sur MCU, ce qui situe l'originalité d'un EWC INT8
sur Cortex-M (déduit).

## Gaps identifiés

- Systèmes d'apprentissage continu sur MCU (fortement contraints) : quasi inexistants (§2.6, §7).
- Régularisation anti-oubli (EWC, SI) dans les systèmes d'entraînement embarqué : absente.
- Pas de cadre commun d'évaluation (mémoire, énergie, précision) des systèmes d'entraînement
  embarqué.

## Statut de lecture

Papier complet (`fulltext.md` lu en entier). Extraction désordonnée (paragraphes intercalés, Table 2
et Table 4 reconstituées en vrac) ; Table 1 partielle.
Déduit et non affirmé par les auteurs : coût d'un EWC limité aux couches entraînées, originalité
d'un CL sur MCU.
