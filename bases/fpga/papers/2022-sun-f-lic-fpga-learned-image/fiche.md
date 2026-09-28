---
id: 2022-sun-f-lic-fpga-learned-image
fiche: done
date: 2026-09-26
---

# F-LIC: FPGA-based Learned Image Compression with a Fine-grained Pipeline

Heming Sun, Qingyang Yi, Fangzheng Lin, Lu Yu, Jiro Katto, Masahiro Fujita, 2022, 2022 IEEE Asian Solid-State Circuits Conference (A-SSCC) 1-3. https://doi.org/10.1109/A-SSCC56115.2022.9980666
Type : conférence (papier court de 3 pages ; métadonnées issues de l'export IEEE Xplore)

## Problème

La compression d'images apprise (LIC), construite sur un **autoencodeur variationnel avec
hyper-prior**, dépasse l'intra-prédiction de VVC. Mais elle tourne sur GPU en flottant, et
les écarts de calcul flottant d'une plateforme à l'autre provoquent des erreurs de décodage
quand l'encodeur et le décodeur ne tournent pas sur le même matériel. Il faut donc une LIC en
virgule fixe, et rapide (texte principal, sans numérotation de sections).

## Méthode

- **Modèle** : structure hyper-prior de [3]. Côté encodage, trois transformées : analyse (AT)
  x → y, hyper-analyse (HA) y → z, et hyper-synthèse (HS), qui donne µ et σ de y. Côté
  décodage : HS puis synthèse (ST) y → x′ (Fig. 1). **Le codage entropique par range coder de
  z et y se fait sur le PC hôte**, pas sur le FPGA.
- **Quantification** en virgule fixe 8 bits (Fix8).
- **Pipeline à grain fin**, layer-wise : chaque couche a ses propres PE en DSP, avec du
  parallélisme sur la largeur de noyau (k), les canaux d'entrée (c) et les canaux de sortie
  (m), et un budget de cycles par couche inversement proportionnel à la hauteur de sortie
  (Fig. 2). Entre deux couches, un buffer d'activations en ping-pong par lignes, avec
  crossbar, permet de choisir c et m librement, sans les restreindre à des puissances de deux
  comme [6].
- **Cascading DSP (casDSP)** : deux poids de deux canaux de sortie partagent un DSP48, en
  (A+D)×B+C. Les sommes partielles sur la largeur du noyau restent dans la chaîne de DSP, avec
  une chaîne en plus pour gérer le débordement des 17 bits bas (Fig. 3).
- **Déconvolution à saut de zéros** : les zéros insérés par le stride 2 sont évités en
  colonnes (casDSP à 3 et à 2 DSP) et en lignes (ordre de parcours) (Fig. 4).
- Paramètres en DDR, chargés une fois ; image transférée en DDR à l'exécution (Fig. 2).

## Plateforme et implémentation

- Résultats principaux sur **VCU118**. Le tableau de ressources donne 1 182 240 LUT et
  6 840 DSP disponibles, soit la capacité d'un XCVU9P (déduit ; la puce n'est pas nommée
  dans le texte extrait). 200 MHz dans tous les cas.
- Ressources (tableau de la Fig. 6, lu par Docling) :

  | Configuration | LUT | FF | BRAM | DSP |
  |---|---|---|---|---|
  | Encodeur 720p | 339 875 | 532 869 | 672 | 4 146 |
  | Encodeur 1080p | 367 667 | 534 460 | 831 | 4 146 |
  | Décodeur 720p | 436 879 | 569 830 | 578 | 3 706 |
  | Décodeur 1080p | 485 433 | 569 345 | 725 | 3 706 |

- « D'autres cartes d'évaluation » atteignent des vitesses selon leurs ressources (Fig. 5) ;
  une ZCU104 apparaît dans un fragment du tableau, sans chiffres exploitables.
- Démonstrateur (Fig. 7) : caméra et FPGA côté encodeur, FPGA et écran côté décodeur, le flux
  compressé passant par TCP/IP.
- **Puissance** : donnée en énergie par image (J/f), sans méthode de mesure décrite. Code et
  bitstream : non publiés.

## Résultats

| Mesure | Ce travail (VCU118, Fix8) | FPX-NIC [7] (FPGA, Fix8) | Jetson Xavier NX (FP16) | RTX 3090 (FP16) |
|---|---|---|---|---|
| PSNR (dB) / bpp | 29,94 / 0,2542 | 29,89 / 0,2565 | 29,96 / 0,2473 | 29,96 / 0,2473 |
| Encodage 720p / 1080p (fps) | 40,69 / 19,15 | 30,99 / 12,87 | 7,0 / 3,6 | 19,4 / 8,9 |
| Décodage 720p / 1080p (fps) | 35,77 / 16,83 | 7,23 / 3,00 | 7,5 / 3,8 | 25 / 12,7 |
| Énergie encodage 720p / 1080p (J/image) | 1,41 / 2,97 | 1,68 | 1,43 / 3,06 | 6,19 / 13,15 |
| Énergie décodage 720p / 1080p (J/image) | 1,72 / 3,31 | 4,56 | 1,6 / 3,16 | 5,08 / 9,45 |

Source : tableau de la Fig. 6, dont l'ordre 720p / 1080p a été rétabli par recoupement avec le
texte. Tous les rapports cités par les auteurs se retrouvent : 1,31-1,49× à l'encodage et
4,95-5,61× au décodage face à [7] ; 4,43-5,81× face au Jetson ; jusqu'à 2,15× face à la
RTX 3090.

- Efficacité DSP au-dessus de 90 % pour presque toutes les couches, en 720p à 41 fps à
  l'encodage et 36 fps au décodage sur VCU118 (Fig. 5).
- **Efficacité énergétique comparable à celle du Jetson Xavier NX** (1,41 contre 1,43 J/image
  à l'encodage 720p), mais **pas meilleure**. Les auteurs l'attribuent à la finesse de gravure
  (16 nm contre 12 nm côté Jetson, selon la ligne « Technology »). Meilleure que la RTX 3090,
  parce que le GPU est peu utilisé.

→ reportés dans `benchmarks.csv` : 4 lignes (encodeur et décodeur, en 720p et 1080p, sur
VCU118). `confidence: medium` : tableau reconstruit, dont l'ordre des colonnes est rétabli
par recoupement. `power_w` vaut n/r, puisque seule l'énergie par image est donnée ; elle est
reportée dans le champ `model`.

## Limites et critique

- **Le codage entropique n'est pas sur le FPGA.** Les range coders de z et de y tournent sur le
  PC hôte. Les fps FPGA portent donc sur les transformées neuronales, sans qu'on sache si le
  temps du range coding est compté (n/r). Un système embarqué autonome demanderait aussi ce
  bloc.
- **Grosse FPGA** : l'encodeur 720p prend 4 146 DSP sur un VU9P. Rien de chiffré sur une carte
  embarquée ; la ZCU104 n'est qu'évoquée.
- **Énergie sans protocole** : sans méthode de mesure (carte, puce ou outil), la comparaison au
  Jetson et à la RTX 3090 n'est pas vérifiable.
- **Baselines GPU en FP16** : le texte ne dit pas si TensorRT est utilisé ni quel batch. Le jeu
  de test du PSNR et du bpp n'est pas précisé dans le texte extrait (n/r).
- Papier de 3 pages : pas d'ablation chiffrée, notamment sur le casDSP et le saut de zéros.

## Pertinence pour la thèse

C'est **le premier papier de la base où un autoencodeur (un VAE) traite des images sur
FPGA**, en temps réel en 720p et 1080p, et démontré sur caméra. Cela nuance le gap « AE sur
FPGA, peu sur images » : la compression apprise d'images est un débouché réel. L'architecture
layer-wise avec saut de zéros dans les déconvolutions est réutilisable pour le décodeur d'un
autoencodeur convolutif de détection d'anomalies. Deux points restent ouverts : la
compression ou l'anomalie sur une FPGA embarquée (Zynq, KV260), et le codage entropique
intégré.

## Gaps identifiés

- Gap « autoencodeurs sur FPGA appliqués aux images » : ce papier **nuance** le gap du côté de
  la compression apprise, mais sur une grosse FPGA et sans codage entropique on-chip. La
  **détection d'anomalies visuelles par AE sur FPGA** reste absente de la base.
- LIC sur FPGA embarquée à faible consommation : non chiffré.
- L'énergie par image des FPGA face à un Jetson récent (Orin) reste non mesurée.

## Statut de lecture

Papier complet (`fulltext.md` en entier, 3 pages, extraction GROBID).
- **Tableau de comparaison (Fig. 6)** : GROBID l'a mélangé, et il a été reconstruit à la main.
  L'ordre 720p / 1080p des fps de décodage et de l'énergie d'encodage de ce travail a été
  rétabli par recoupement avec les rapports que donne le texte. Pour l'énergie, j'ai supposé
  720p < 1080p, ce qui concorde avec l'efficacité « comparable » au Jetson dite par les
  auteurs.
- **Tableau de ressources** : lu par Docling, sur le PDF, dans le scratchpad (pas enregistré
  dans le dossier du papier).

Ce qui suit est déduit et non affirmé par les auteurs : la puce XCVU9P ; l'attribution des
valeurs 720p et 1080p dans le tableau de comparaison ; la question du temps de range coding
dans les fps.
