---
id: 2015-zhang-optimizing-fpga-accelerator-design-deep
fiche: done
date: 2026-09-26
---

# Optimizing FPGA-based Accelerator Design for Deep Convolutional Neural Networks

Chen Zhang, Peng Li, Guangyu Sun, Yijin Guan, Bingjun Xiao, Jason Cong, 2015, Proceedings of the 2015 ACM/SIGDA International Symposium on Field-Programmable Gate Arrays 161–170. https://doi.org/10.1145/2684746.2689060
Type : conférence (FPGA '15, relue par les pairs)

## Problème

L'espace de conception d'un accélérateur CNN sur FPGA est mal exploré : le débit de calcul
ne correspond souvent pas à la bande passante mémoire de la plateforme, si bien que les
ressources logiques ou la bande passante restent sous-utilisées. Les auteurs observent
jusqu'à 90 % d'écart de performance entre deux solutions à ressources égales (§1). Les
travaux antérieurs optimisent soit le moteur de calcul en ignorant la mémoire externe,
soit la réutilisation des données au prix d'une reconfiguration du FPGA entre couches (§1, §6).

## Méthode

- **Modèle roofline** (§2.3, Eq. 1) : performance atteignable = min(toit de calcul,
  ratio calcul/communication (CTC) × bande passante).
- **Transformations de boucles** sur la convolution (Fig. 5) : tuilage des boucles
  `row, col, to, ti` (facteurs Tr, Tc, Tm, Tn) ; les boucles noyau K×K ne sont pas tuilées.
  Analyse polyédrique des dépendances (§3.2, Table 2) : seules `too` et `tii` sont
  déroulées, pour éviter les interconnexions complexes.
- **Toit de calcul** fonction de (Tm, Tn) (Eq. 3) ; **CTC** fonction des tailles de
  tampons et de la promotion mémoire locale de `output_fm` (§3.3, Eq. 4-11).
- **Exploration exhaustive** (§3.4, Fig. 8) : énumération des ordres de boucles et des
  tailles de tuiles ; parmi les points de même performance sous le toit de bande passante,
  choix de celui de plus fort CTC (moins de bande passante). ≤ 98 000 designs légaux,
  explorés en 10 min sur un portable (§3.5).
- **Facteurs de déroulage uniformes** pour toutes les couches : (Tm, Tn) = (64, 7), à
  moins de 5 % du total de cycles des optima par couche (Table 4 : 1 008 246 contre 963 804
  cycles). Pas de reprogrammation du FPGA entre couches.
- **Architecture** (§4) : 64 arbres de 7 multiplieurs-additionneurs (Fig. 11), double
  tampon ping-pong, deux canaux séparés chargement / déchargement, 4 interfaces AXI (besoin
  mesuré ≥ 1,55 GB/s, §4.4). MicroBlaze pour le contrôle.
- Calcul en **virgule flottante 32 bits** ; **couches de convolution seules** (pooling et
  couches FC non accélérées, §2.1). Toolflow : Vivado HLS 2013.4 (C + pragmas, §5.1).

## Plateforme et implémentation

- Carte VC707, Virtex-7 **XC7VX485T**, 100 MHz, DDR3 (§5.1).
- Ressources (Table 6, corps reconstruit par PyMuPDF, à vérifier) : 2 240 DSP (80 %),
  1 024 BRAM (50 %), 186 251 LUT (61,3 %), 205 704 FF (33,87 %).
- Puissance : 18,61 W mesurés par un wattmètre branché sur la carte (§5.2, Fig. 14,
  Table 8) → portée `board`. La puissance CPU (95 W) est le TDP, pas une mesure.
- Code / bitstream : non publiés (aucun lien dans le texte).

## Résultats

- Débit : **61,62 GFLOPS** sur les 5 couches de convolution d'AlexNet (1,33 GFLOP),
  latence totale 21,61 ms (Table 7). Par couche : 27,5 GFLOPS (couche 1) à 83,79 GFLOPS
  (couche 2) (Table 7).
- Contre un Xeon E5-2430 (2,2 GHz, gcc -O3) : 17,42× sur 1 thread, 4,8× sur 16 threads
  (§5.2, Table 7).
- Énergie : 0,40 J par passe contre 9,83 J (16 threads) et 35,77 J (1 thread), soit 24,6×
  à 89,4× (Table 8) — mais la puissance CPU est son TDP.
- Contre les accélérateurs FPGA antérieurs (Table 5) : ≥ 3,62× en GOPS, et densité de
  performance 8,12E-04 GOPS/slice, 1,8× la meilleure précédente.
- Précision : non mesurée (n/r) ; le calcul flottant ne change pas le réseau.

→ reportés dans `benchmarks.csv` : **1 ligne** — AlexNet (conv. uniquement), VC707,
FP32, 61,62 GOPS, 21,61 ms, 18,61 W `board`, Table 6/7/8. FPS non rapporté (n/r) : la
latence ne couvre que les couches de convolution.

## Limites et critique

- **Convolutions seules** : pooling, FC et post-traitement exclus. La latence de 21,61 ms
  n'est pas celle d'une inférence complète ; en déduire un FPS serait une extrapolation.
- **FP32** : choix peu représentatif de l'embarqué actuel (INT8 et moins). Les auteurs le
  reconnaissent eux-mêmes : la virgule fixe coûterait bien moins de ressources (Table 9).
- **Comparaison GOPS biaisée** (Table 5) : GMACS convertis en GOPS, précisions de 16 à
  48 bits en virgule fixe contre FP32, puces de 4 générations (Spartan-3A à Virtex-7). La
  « densité par slice » atténue mais ne corrige pas l'écart technologique.
- **Énergie CPU estimée par le TDP** (95 W), pas mesurée : le rapport 24,6× est une borne
  grossière (les auteurs parlent eux-mêmes de « rough estimation », §5.2).
- Aucune baseline GPU, pourtant pertinente en 2015 (déduit).
- Pas de mesure de précision, pas de batch/protocole de chronométrage détaillé.
- Plateforme haut de gamme (Virtex-7, carte à 18,6 W) : loin des contraintes embarquées.

## Pertinence pour la thèse

Papier fondateur de la méthodologie roofline pour accélérateurs CNN sur FPGA, repris par
quasiment tous les travaux ultérieurs (tuilage Tm/Tn, ping-pong, accélérateur générique
« une unité pour toutes les couches », à opposer au dataflow de FINN). Pour un accélérateur
YOLO ou d'autoencodeur sur KV260, la démarche « CTC vs bande passante DDR » reste
directement applicable pour dimensionner le parallélisme (déduit). Les chiffres, eux, sont
obsolètes (FP32, Virtex-7).

## Gaps identifiés

- Couches non convolutives (pooling, FC, et par extension NMS/post-traitement de YOLO,
  déconvolutions d'un autoencodeur) hors du modèle roofline.
- Pas de précision réduite dans l'exploration : le modèle ne couple pas quantification et
  bande passante.
- Énergie comparée au TDP d'un CPU : illustre à nouveau l'absence de protocole de mesure
  commun.

## Statut de lecture

Papier complet (`fulltext.md` lu en entier). Extraction GROBID correcte ; Table 3 réduite
à sa légende (données partiellement présentes), Table 6 reconstruite par PyMuPDF (valeurs
cohérentes avec le texte « almost fully utilized », à vérifier). Plusieurs équations et
§4.1 tronqués.
Déduit et non affirmé par les auteurs : non-extrapolation de la latence en FPS ;
applicabilité de la démarche au KV260 ; absence de baseline GPU comme faiblesse.
