---
id: 2022-malviya-edge-compatible-convolutional-autoencoder-implemented
fiche: done
date: 2026-09-26
---

# Edge-Compatible Convolutional Autoencoder Implemented on FPGA for Anomaly Detection in Vibration Condition-Based Monitoring

Vaibhav Malviya, Indrani Mukherjee, Siddharth Tallur, 2022, IEEE Sensors Letters 6(4), 1-4. https://doi.org/10.1109/LSENS.2022.3159972
Type : article de journal (IEEE Sensors Letters, lettre de 4 pages, relue par les pairs)

## Problème

La surveillance de l'état des machines (CBM) par vibrations bute sur deux obstacles : les
modèles profonds sont trop lourds pour l'embarqué, et le cloud pose latence, coût de
transmission et confidentialité (§I, résumé). De plus, on dispose surtout de données
saines : il faut une détection d'anomalies **non supervisée** (autoencodeur) et légère,
implantable sur une plateforme bon marché.

## Méthode

- Jeu **Airbus SAS helicopter accelerometer** : séries 1-D d'une minute à 1 024 Hz ; 1 677
  enregistrements sains pour l'entraînement, 594 en test (§II-A).
- **Encodage des séries en images** (§II-B) : spectrogramme (512 × 48), scalogramme
  (ondelette chapeau mexicain, échelle 64, réduit à 64 × 64), MTF et GAF (réduits à
  64 × 64). Chaque série est découpée en 120 sous-séries de 512 échantillons, soit
  201 240 images d'entraînement.
- **CAE** de 3 conv. + max-pool, FC (256 → 10 → 256), 3 conv. + upsampling, soit
  **8 755 paramètres** (Table 1) ; 1,65 MFLOP (encodeur) et 1,82 MFLOP (décodeur) (§III).
  Erreur de reconstruction en entropie croisée ; seuil μ + σ des erreurs d'entraînement
  (§III).
- **Implémentation** : Vivado HLS en C, convolution par line buffer + fenêtre (Fig. 2),
  pragmas unroll / pipeline / dataflow, flux AXI-Stream, DMA, pilotage par overlays PYNQ
  depuis l'ARM (§III, §III-A). **Virgule fixe 23 bits (2 bits entiers)** (§III-A).
  **Deux bitstreams séparés** pour l'encodeur et le décodeur (§III).

## Plateforme et implémentation

- **PYNQ-Z2**, Zynq-7000 **XC7Z020** (résumé, Table 4) ; fréquence d'horloge `n/r`.
- Ressources (Table 4, Docling) :
  - encodeur : 40 403 LUT (75,7 %), 37 094 FF, 6 BRAM, 82 DSP ;
  - décodeur : 38 169 LUT (71,75 %), 39 839 FF, 10 BRAM, 106 DSP.
- Puissance : 1,85 W (encodeur) et 1,79 W (décodeur) (Table 5) ; **méthode non décrite** →
  `unspecified`.
- Code / bitstream : non publiés.

## Résultats

- Précision de détection (CPU, flottant) selon l'encodage (Table 2) : scalogramme 88,8 %,
  spectrogramme 80,4 %, GAF 62 %, MTF 59 %. Pour le scalogramme : précision 88 %, rappel
  91 %, F1 89,07 % (§III).
- Face à la littérature sur ce jeu (Table 3) : CAE de Garcia et al. > 10 M paramètres,
  85 % ; GAN de Ducoffe et al. 88,11 % ; ce travail 88,8 % avec 8 755 paramètres.
- **FPGA** : 85,02 % (perte due à la virgule fixe) ; 2,1 ms (encodeur) + 3,8 ms
  (décodeur) = **5,9 ms** par inférence, contre 109,3 ms sur un Core i7-8700, soit 18,51×
  (§IV-B).

→ reportés dans `benchmarks.csv` : **2 lignes** — encodeur et décodeur (deux bitstreams
distincts, ressources et puissance propres), avec la précision du modèle complet sur FPGA
(85,02 %). Table 4, Table 5, §IV-B.

## Limites et critique

- **Deux bitstreams** : encodeur et décodeur ne tiennent pas ensemble sur la puce ; la
  latence de 5,9 ms ignore le temps de reconfiguration entre les deux (non mentionné) et le
  prétraitement (ondelettes) fait sur CPU, sans doute hors mesure (déduit).
- **Accélération relative à un CPU de bureau** (109,3 ms pour 3,5 MFLOP, ce qui suggère une
  exécution Python / Keras peu optimisée, déduit) ; pas de comparaison MCU, alors que le
  modèle (8 755 paramètres) tiendrait sur un microcontrôleur (déduit).
- Virgule fixe 23 bits choisie sans exploration : −3,8 points de précision.
- **Puissance sans méthode** ; la Table 5 compare à des puissances de travaux hétérogènes
  (Virtex-7 18,61 W, KCU105…) sur des tâches sans rapport.
- Métrique « accuracy » à un seuil fixe μ + σ, sans AUC ; un seul jeu de données.
- Lettre de 4 pages : peu de détails (fréquence, protocole de chronométrage).

## Pertinence pour la thèse

C'est l'illustration même du gap connu : un **autoencodeur sur FPGA appliqué à des séries
temporelles** (vibrations), même si elles sont encodées en petites images 64 × 64. C'est un
point de comparaison utile pour un CAE d'images réelles sur KV260 : ordre de grandeur des
ressources d'un CAE HLS minuscule sur Zynq-7020, et piège des bitstreams séparés à éviter
(déduit). Il n'apporte rien sur l'apprentissage embarqué (entraînement sur CPU).

## Gaps identifiés

- CAE sur **images naturelles** (et non sur séries temporelles encodées) sur FPGA : non traité.
- Encodeur + décodeur dans un seul bitstream sur petite puce : non atteint ici.
- Comparaison FPGA vs MCU pour de très petits autoencodeurs : absente.
- Adaptation en ligne du seuil ou du modèle à la dérive (usure des machines) : non traitée.

## Statut de lecture

Papier complet (`fulltext.md` lu en entier). Toutes les tables sont reconstruites par Docling
(chiffres à vérifier, notamment la Table 1) ; une partie de §II-C et de §IV-A a glissé dans
les légendes ou §III.
Déduit et non affirmé par les auteurs : reconfiguration et prétraitement hors latence ;
baseline CPU non optimisée ; faisabilité sur MCU.
