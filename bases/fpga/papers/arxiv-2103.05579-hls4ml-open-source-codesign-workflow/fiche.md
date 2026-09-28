---
id: arxiv-2103.05579-hls4ml-open-source-codesign-workflow
fiche: done
date: 2026-09-24
benchmarks: none
---

# hls4ml: An Open-Source Codesign Workflow to Empower Scientific Low-Power Machine Learning Devices

Farah Fahim, Benjamin Hawks, Christian Herwig, James Hirschauer, Sergo Jindariani, Nhan Tran, Luca P Carloni, Giuseppe Di Guglielmo, Philip Harris, Jeffrey Krupa, Dylan Rankin, Manuel Blanco Valentin, Josiah Hester, Yingyi Luo, John Mamish, Seda Orgrenci-Memik, Thea Aarrestad, Hamza Javed, Vladimir Loncar, Maurizio Pierini, Adrian Alan Pol, Sioni Summers, Javier Duarte, Scott Hauck, Shih-Chieh Hsu, Jennifer Ngadiuba, Mia Liu, Duc Hoang, Edward Kreinar, Zhenbin Wu, 2021, TinyML Research Symposium 2021. https://arxiv.org/abs/2103.05579 (rapport Fermilab FERMILAB-CONF-21-080-SCD)
Type : conférence (symposium TinyML 2021, d'après le commentaire arXiv ; DOI éditeur n/r)

## Problème

Rendre l'implémentation matérielle (FPGA, ASIC) de réseaux de neurones accessible aux
scientifiques non spécialistes du matériel, et étendre hls4ml, conçu pour la très faible
latence (physique des particules), vers les applications basse consommation (§1).

## Méthode

Papier de présentation d'outil, pas d'un accélérateur :

- Flux : modèle (Q)Keras / TensorFlow / PyTorch / ONNX → représentation interne →
  optimiseurs de graphe (fusion batchnorm, etc.) → projet HLS (Vivado HLS ; Quartus HLS et
  Catapult HLS en développement) → IP core. Émulation bit-exacte en Python, profilage
  numérique des poids pour choisir les précisions (§2, Fig. 2-3).
- Chaque couche est un module matériel dédié ; parallélisme réglé par le « reuse factor »
  R (1 = tout parallèle ; débit ∝ 1/R) (§4.2).
- Nouveautés annoncées : quantization-aware pruning (QAP, Brevitas + élagage lottery
  ticket, ~10 % par itération) (§3.2) ; noyaux creux (directives HLS ou format COO)
  (§4.2) ; intégration Vitis Accel (§4.3.1) ; flux ASIC via Catapult HLS avec
  vérification (§4.3.2).
- Arithmétique en virgule fixe, précision configurable par couche (§3.1).

## Plateforme et implémentation

- Puces FPGA des exemples : n/r dans le texte extrait (la Table 1 manque).
- Exemple MNIST (MLP 784-16-10, 12 704 multiplications) : II de 14 à 12 544 cycles selon
  R, soit 140 ns à 0,125 ms à 100 MHz (§4.2, Fig. 6) — calcul des auteurs, pas une mesure.
- Code : hls4ml est open source (§1 ; dépôt non cité dans le texte extrait).

## Résultats

- QAT (repris de [11]) : en PTQ la précision chute sous 14 bits, en QAT elle reste au
  niveau FP32 jusqu'à 6 bits (§3.1, Fig. 4).
- QAP : le modèle jet 6 bits élagué à 80 % garde la performance (AUC) du modèle 32 bits,
  pour 50× moins de BOPs (§3.2, Fig. 5).
- Table 1 (ressources FPGA PTQ 16 / 14 bits vs QAT 6 bits) : **non extraite**, valeurs n/r
  ici ; le texte dit seulement que QAT réduit « drastiquement » les DSP (§4.1).
- Exemples cités d'autres travaux de la collaboration : CNN SVHN à 5 µs et < 10 % des
  ressources ([12], §4.1) ; autoencodeur ASIC 65 nm, ~4 400 paramètres, 25 ns, 3,6 mm²,
  2,38 nJ/inférence estimés ([83,84], §4.3.2).

→ reportés dans `benchmarks.csv` : aucune ligne. Les seuls chiffres propres au papier sont
dans la Table 1, absente de l'extraction ; les autres viennent de travaux cités.

## Limites et critique

- Papier d'outil sans évaluation expérimentale nouvelle complète : l'essentiel des chiffres
  est repris de travaux antérieurs ([11], [12], [83,84]).
- Les modèles de démonstration sont minuscules (MLP 16 entrées, MNIST 784-16-10) : rien sur
  des CNN de vision de taille réaliste, alors que le titre vise les « low-power devices ».
- Puissance : uniquement « estimée » (SVHN, ASIC) ; aucune mesure sur carte.
- Pas de comparaison avec FINN, Vitis AI ou fpgaConvNet sur un même modèle, alors qu'ils
  sont listés (Related Work).
- Architecture « une couche = un bloc matériel, couches séquentielles » (§4.2) : passe mal
  à l'échelle pour des réseaux profonds sur petits FPGA — limite déduite, non discutée.

## Pertinence pour la thèse

Référence pour l'axe toolflows et pour les autoencodeurs : hls4ml est l'outil de base des
autoencodeurs FPGA/ASIC en physique des particules (profilage de l'autoencodeur d'anomalies,
Fig. 3 ; autoencodeur ASIC, §4.3.2). Utile pour prototyper un petit CAE en QKeras + hls4ml ;
à compléter par la version 2025 (arxiv-2512.01463) pour les capacités actuelles.

## Gaps identifiés

- hls4ml démontré sur MLP et petits CNN : pas d'exemple de CNN de vision (ou d'autoencodeur
  sur images) de taille réaliste sur FPGA embarqué.
- Pas de mesure de puissance réelle dans les démonstrations basse consommation.

## Statut de lecture

Papier complet (`fulltext.md` lu en entier). Extraction : l'abstract est tronqué, la
Table 1 et la Figure 5 (texte illisible) manquent ; les valeurs de la Table 1 restent à
relever à la main.
Déduit et non affirmé par les auteurs : limite de passage à l'échelle de l'architecture
couche par couche ; absence de mesure de puissance réelle.
