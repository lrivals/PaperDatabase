---
id: arxiv-2602.15751-enabling-low-latency-machine-learning
fiche: done
date: 2026-09-24
---

# Enabling Low-Latency Machine learning on Radiation-Hard FPGAs with hls4ml

Katya Govorkova, Julian Garcia Pardinas, Vladimir Loncar, Victoria Nguyen, Sebastian Schmitt, Marco Pizzichemi, Loris Martinazzoli, Eluned Anne Smith, 2026, Machine Learning: Science and Technology 7 (2026) 045024. https://doi.org/10.1088/2632-2153/ae8218
Type : article de journal

## Problème

Pour l'upgrade II de LHCb, le calorimètre PicoCal devra compresser sur le détecteur chaque
impulsion de 32 échantillons en ~2 nombres, à 40 MHz, dans un environnement radiatif
(§1). Il manquait (i) un algorithme de compression validé et (ii) un chemin hls4ml vers
les FPGA flash durcis Microchip PolarFire (§1, §2.2).

## Méthode

- Autoencodeur dense minimal : encodeur 32 → 2 + ReLU (seule partie en matériel), décodeur
  2 → 32 linéaire hors FPGA ; architecture choisie par keras-tuner parmi 15 variantes
  (§3.1, §3.3).
- Données : 353 513 impulsions simulées Geant4 du prototype PicoCal (signal + pile-up),
  sous-échantillonnées de 1024 à 32 points ; split 70/15/15 (§3.2, §3.3).
- QAT (QKeras) : entrées <16,9>, poids/biais <10,4>, latent <10,7> ; accumulateur <30,17>
  en version « full » (arrondi + saturation) ou « nano » (troncature, sans protection de
  dépassement) (§4.1, Fig. 7).
- Nouveau backend hls4ml pour Microchip SmartHLS (types `ap_fixpt`, génération de code,
  interface FIFO), validé bit à bit en C-simulation, publié dans hls4ml v1.3.0
  (mars 2026) ; couches supportées : dense et ReLU seulement (§5.1, §6.2).

## Plateforme et implémentation

- Microchip PolarFire MPF100T-FCVG484I (cible probable) et MPF300TS-FCG1152I (kit de
  test, mesures réelles), Libero ; cible 160 MHz, fmax 200 MHz (full) / 300 MHz (nano)
  post-synthèse (§5.2).
- Multiplications 10 bits en LUT à 4 entrées, **aucun Math Block** (§5.2).
- Ressources de l'implémentation complète (avec UART) : 5578 / 2995 LUT, 6383 / 2478 DFF,
  8395 / 3725 logic units pour full / nano (§5.2). Nano sur MPF100T : 3,10 % des LUT par
  canal (§6.1).
- Puissance : **estimée** (outil Microchip et Libero SmartPower), statique et dynamique
  « roughly around 0.1 W » chacune (§5.2) ; pas de mesure.
- Code : backend public dans hls4ml v1.3.0 (§6.2) ; modèle et bitstream : n/r.

## Résultats

| Mesure | Full | Nano | Source |
|---|---|---|---|
| Latence | 150 ns | 25 ns (4 cycles à 160 MHz) | §5.2 |
| Intervalle d'initiation | 3-4 cycles | 3-4 cycles | §5.2 |
| Débit | 40 MHz (une donnée / 25 ns) | 40 MHz | §5.2, §7 |
| LUT / DFF (avec UART, MPF300TS) | 5578 / 6383 | 2995 / 2478 | §5.2 |
| Math blocks | 0 | 0 | §5.2 |

- Physique : résolution temporelle CFD ~2× meilleure après reconstruction par
  l'autoencodeur (≈ 30 ps vs 62 ps en supposant 200 ps d'échantillonnage) (§3.6, Fig. 4) ;
  régression directe 32 → 1 : σ = 0,13 contre 0,15 échantillon (§3.7, Fig. 6).
- 10 bits de poids ≈ pleine précision en MSE ; plateau à partir de ~10 bits (§4.1, Fig. 7).
- Corrélation z0 / amplitude : Pearson 0,998 (§3.5).
- Mesures sur MPF300TS cohérentes avec la post-synthèse (§5.2, §6).

→ reportés dans `benchmarks.csv` : 2 lignes (full, nano ; §5.2, `medium` car la Table 1
n'a pas été extraite et les chiffres viennent du texte).

## Limites et critique

- **Données simulées uniquement**, avec un sous-échantillonnage manuel qui ne représente
  pas le numériseur final (SPIDER) : les auteurs préviennent que la résolution temporelle
  finale peut différer (§3.6).
- Le gain « ×2 en timing » est obtenu sur une seule catégorie d'impulsions (front pulses,
  seed cells) (§3.6).
- Puissance seulement estimée par outil, avec une formulation vague (~0,1 W statique et
  ~0,1 W dynamique) ; pas de mesure sur le kit alors que la carte était disponible.
- Tenue aux radiations argumentée (configuration flash immune aux SEU) mais **non testée**
  en faisceau ; la logique utilisateur reste sensible aux SEU (§6.3).
- Modèle trivial (un produit matrice 32×2) : le backend n'est démontré que pour dense +
  ReLU ; rien ne prouve encore son intérêt pour des CNN.
- Pas de comparaison avec un FPGA SRAM + TMR, ni avec l'alternative ASIC évoquée (§1).

## Pertinence pour la thèse

Cas d'école de l'autoencodeur sur FPGA en physique des particules : confirme le constat de
`gaps.md` (autoencodeurs FPGA surtout sur séries temporelles, ici des impulsions de 32
échantillons). Intéressant pour la méthodologie QAT + balayage de précision + hls4ml et pour
le chemin vers des FPGA non AMD/Intel. Très loin de la vision embarquée (pas d'image,
pas de convolution).

## Gaps identifiés

- Autoencodeurs sur FPGA : ici encore sur signal 1D ; pas d'autoencodeur convolutionnel sur
  image (étaye le gap existant).
- hls4ml sur PolarFire limité à dense/ReLU : pas de CNN sur FPGA flash durci.

## Statut de lecture

Papier complet (`fulltext.md` lu en entier). Extraction : le corps de la Table 1 manque
(seule sa légende est extraite) ; la section 4 n'est pas détectée comme titre (son texte
suit §3.7 à partir de « 4.1 ») ; §6.1 est intitulée « FPGA setup » par erreur ; une annexe
de code HLS est mêlée à la fin.
Déduit et non affirmé par les auteurs : absence de comparaison SRAM+TMR/ASIC comme limite ;
portée limitée du backend aux réseaux denses.
