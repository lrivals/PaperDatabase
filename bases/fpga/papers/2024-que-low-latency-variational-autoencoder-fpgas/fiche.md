---
id: 2024-que-low-latency-variational-autoencoder-fpgas
fiche: done
date: 2026-09-26
---

# Low Latency Variational Autoencoder on FPGAs

Zhiqiang Que, Minghao Zhang, Hongxiang Fan, He Li, Ce Guo, Wayne Luk, 2024, IEEE Journal on Emerging and Selected Topics in Circuits and Systems 14(2), 323-333. https://doi.org/10.1109/JETCAS.2024.3389660
Type : article de journal (métadonnées issues de l'export IEEE Xplore, `citation.bib`)

## Problème

Les rares VAE sur FPGA évitent l'échantillonnage gaussien en matériel (§I, §II-B). L'un
n'implémente que l'encodeur, avec un score D_KL, pour le trigger du LHC [9] (c'est
`arxiv-2108.03986` dans la base). L'autre génère les nombres aléatoires en lots sur CPU et les
transfère au FPGA, pour une latence de plusieurs centaines de µs [5]. Les auteurs veulent une
**inférence VAE entièrement stochastique en matériel**, à très faible latence, pour de la
détection d'anomalies en flux.

## Méthode

- **Couche d'échantillonnage gaussien en matériel** : Z = µ + σ ⊙ ε (§III-B). Un PRNG Mersenne
  Twister MT19937 génère l'aléa, avec un vecteur d'état coupé en deux tableaux pair et impair
  de 512 pour doubler les lectures (§III-C). La transformée de Box-Muller le rend gaussien, avec
  les fonctions log, sqrt, sin et cos de la bibliothèque HLS (§III-D).
- **Quantification du GRNG** (§III-E) : trois versions, float32, fixe 16 bits unifié
  (6 bits entiers) et précision mixte. La version mixte met 48 bits en entrée de log et 16 bits
  pour sin et cos. Encodeur et décodeur sont en virgule fixe 16 bits, à précision égale au
  float32 selon les auteurs (§IV-B).
- **Architecture layer-wise en pipeline** (dataflow) : un moteur dédié par couche,
  entièrement déroulé, données on-chip, entrée et sortie en flux AXI (§III-F). Les auteurs
  s'inspirent explicitement de FINN et hls4ml.
- **Transformation de code HLS** : l'inférence est réécrite en « perfect loop » pilotée par une
  FSM (Algorithm 2), pour pipeliner aussi l'encodeur et fixer le nombre N_D d'instances
  décodeur + GRNG selon le budget (§III-G).
- **Modèle évalué, très petit** : encodeur FC 64 → (µ, log σ²) de dimension 1, décodeur FC 64
  (§IV-B). Les variantes LSTM et CNN ne servent qu'à l'étude de précision (Fig. 8), pas au
  matériel.
- **Application** : détection d'anomalies sur **séries temporelles** d'ondes
  gravitationnelles simulées (PyCBC, bruit de détecteur, SEOBNRv4). 240k événements
  d'entraînement, 60k de validation, 50k de test (§IV-A).

## Plateforme et implémentation

- Zynq-7000 **Z7045** à 142 MHz et **Alveo U250** à 200 MHz ; Vivado HLS 2020.1
  (bloc « Algorithm 2 » de `fulltext.md`, §IV-A). Puces exactes au-delà de « ZYNQ 7045 » et
  « U250 » : n/r.
- Ressources (Table I) :
  - Z7045 N_vae = 2 : 12 708 LUT, 175 DSP, 9 BRAM ;
  - Z7045 N_vae = 10 : 62 590 LUT, 860 DSP (95,6 %), 53 BRAM ;
  - U250 N_vae = 12 : 188 350 LUT, 1032 DSP, 62 BRAM.
- Unité VAE seule, selon le GRNG (Table III, sur U250 selon la légende lue par Docling) :
  float32 24 cycles, 147 DSP ; 16 bits unifié 16 cycles, 109 DSP ; mixte 17 cycles, 113 DSP,
  15 570 LUT, 12 BRAM. II = 1 dans les trois cas.
- **Puissance** : 5,755 W dont 2,997 W statiques, pour N_vae = 12 sur U250. C'est
  l'**estimation de Vivado après placement-routage**, restreinte au noyau de la région
  dynamique (§IV-E) → `power_scope: estimated`.
- Code et bitstream : non publiés (aucun lien).

## Résultats

| Mesure | Valeur | Source |
|---|---|---|
| Latence, 1 unité, 1 inférence | 17 cycles = 85 ns (200 MHz) | §IV-E |
| « Latence moyenne », 1 unité, 10 000 inférences | 5,6 ns par inférence (11 267 cycles au total) | §IV-E, Fig. 12, Table IV |
| Latence totale minimale, 10 000 inférences | 2 448 cycles, atteinte à 8 unités | §IV-E, Fig. 12 |
| AUC | 0,76 (égale à celle de [13], LSTM-AE sur U250) | Table IV |
| TPR à FPR 0,1 / 0,01 / 0,001 | 0,531 / 0,381 / 0,261 | Table II |
| Accélération | 82× face au CPU E5-2620, 208× face à la RTX 2080Ti, 61× face à [13] | Table IV |
| Qualité du GRNG | 3,7 σ en 16 bits unifié, 5,5 σ en précision mixte ([43] atteint 8,2 σ) | §IV-D, Fig. 10 |
| Puissance, N_vae = 12, U250 | 5,755 W estimés par Vivado | §IV-E |

→ reportés dans `benchmarks.csv` : 4 lignes. Deux lignes U250 : 1 unité (Table III, Table IV,
§IV-E) et N_vae = 12 (Table I, §IV-E, puissance estimée). Deux lignes Z7045 : N_vae = 2 et
N_vae = 10 (Table I ; latence, précision et puissance n/r). `confidence: medium` pour toutes
(tableaux reconstruits par Docling avec OCR).

## Limites et critique

- **« Latence » amortie.** Les 5,6 ns et le « 61× » viennent du temps total de 10 000
  inférences divisé par 10 000 : c'est un débit inverse, pas une latence. La vraie latence d'une
  inférence est de 85 ns, soit 17 cycles (§IV-E). La Table IV compare cette valeur amortie à la
  latence moyenne de [13] ; que les deux se mesurent pareil n'est pas établi.
- **Baselines CPU et GPU peu informatives.** Le modèle est minuscule (quelques centaines de
  MAC) avec un batch de 10k : le GPU (1162,5 ns) y est plus lent que le CPU (461,7 ns), signe
  qu'il est dominé par le surcoût de lancement (déduit). Le 208× mesure surtout ce surcoût.
- **Comparaison FPGA.** [13] est un LSTM-AE de l'équipe (Que et al.) ; ici c'est un VAE dense,
  plus simple. À AUC égale (0,76), la comparaison est honnête sur la précision, mais les
  modèles et leur coût intrinsèque diffèrent.
- **Puissance estimée par outil**, sur la seule région dynamique : aucune mesure carte ou puce,
  rien sur le Z7045, aucun énergie par inférence.
- **Incohérence.** 1026 DSP en §IV-B contre 1032 en Table I et §IV-E pour N_vae = 12. Table II :
  la légende annonce 10 % et 1 %, le corps donne aussi 0,001.
- L'initialisation du PRNG représente 67 % de la latence totale à 12 unités (§IV-E) ; les
  auteurs laissent ce point pour plus tard.
- **Aucune image.** Le traitement d'image et de vidéo n'est cité qu'en travaux futurs (§V), et
  le F-LIC (compression d'images apprise par VAE sur FPGA) [18] qu'en travaux liés (§II-B).

## Pertinence pour la thèse

C'est la brique matérielle la plus complète de la base pour un VAE : échantillonnage gaussien
on-chip, GRNG quantifié et pipeline layer-wise. Elle serait réutilisable pour un VAE d'images
en vision embarquée (détection d'anomalies industrielles, par exemple). Mais le papier
**confirme le gap** plutôt qu'il ne le comble : l'application est une série temporelle et le
modèle compte 64 neurones. Passer à un VAE convolutif sur images (encodeur CNN, espace latent
de grande dimension, GRNG en parallèle) sur une FPGA embarquée reste à faire, avec une mesure
de puissance réelle.

## Gaps identifiés

- Gap « autoencodeurs sur FPGA appliqués aux images » : un troisième papier du corpus porte
  sur un AE ou VAE FPGA hors images (ondes gravitationnelles, après la physique des particules
  du LHC). La piste F-LIC [18] (compression d'images apprise par VAE sur FPGA) est à vérifier
  et à ajouter.
- Échantillonnage gaussien en matériel pour un espace latent de grande dimension (image) :
  coût en ressources non étudié.
- VAE sur FPGA sans puissance mesurée (seulement estimée par Vivado).

## Statut de lecture

Papier complet (`fulltext.md` en entier, extraction GROBID). **Les tableaux I à IV viennent de
Docling avec OCR** (sans corps après GROBID et PyMuPDF). Dans la Table II, l'OCR laisse des
fragments parasites (« 二 », « II »), et la ligne FPR 0,001 n'a de valeur que pour « This
work ». Les chiffres de la Table I sont cohérents avec leurs pourcentages d'utilisation, et
ceux de la Table IV avec le texte de §IV-E.
Ce qui suit est déduit et non affirmé par les auteurs : le GPU dominé par le surcoût de
lancement ; le caractère amorti des 5,6 ns comme débit (les auteurs parlent de « latence
moyenne ») ; l'attribution de la Table III au U250, qui vient de la légende lue par Docling.
