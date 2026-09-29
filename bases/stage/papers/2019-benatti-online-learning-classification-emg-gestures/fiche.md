---
id: 2019-benatti-online-learning-classification-emg-gestures
fiche: done
date: 2026-09-29
---

# Online Learning and Classification of EMG-Based Gestures on a Parallel Ultra-Low Power Platform Using Hyperdimensional Computing

Simone Benatti, Fabio Montagna, Victor Kartsch, Abbas Rahimi, Davide Rossi, Luca Benini, 2019, IEEE Transactions on Biomedical Circuits and Systems. https://doi.org/10.1109/TBCAS.2019.2914476
Type : article de journal

## Problème

La reconnaissance de gestes par EMG dépend fortement du sujet et de la session (sueur,
déplacement des électrodes, pose et retrait), donc le modèle doit être réentraîné souvent. Les
méthodes classiques (SVM, LDA, ANN) ont un entraînement itératif, coûteux, fait sur PC ; il
manque un apprentissage en ligne « one-shot », entièrement embarqué, sur un budget de quelques
mW (§I, §II).

## Méthode

- **Hyperdimensional computing (HDC)** avec hypervecteurs binaires de dimension 10 000
  (313 mots de 32 bits) (§III-B, §IV) :
  - item memory (IM) : un hypervecteur aléatoire par canal ; continuous item memory (CIM) :
    22 niveaux de quantification de l'amplitude, interpolés entre deux extrémités orthogonales ;
  - encodeur spatial : XOR canal ⊕ niveau puis majorité sur les canaux (Eq. 1) ; encodeur
    temporel en N-grammes par permutation (Eq. 2), avec N = 1 ici (gestes statiques) ;
  - **apprentissage** : le prototype d'une classe est la majorité des hypervecteurs de ses
    échantillons, calculée en une passe (non itératif) ; **inférence** : distance de Hamming au
    prototype le plus proche (§III-B).
- Features : enveloppe RMS sur 60 échantillons, calculée toutes les 100 ms (EMG à 1 kHz) (§IV-B,
  §V-C).
- Protocole : 10 sujets, 11 gestes (dont repos), 8 canaux ; 25 % des échantillons de chaque geste
  pour l'entraînement, **tout le jeu pour le test** (§V). Comparaison à un SVM linéaire.

## Plateforme et implémentation

- **Mr. Wolf** (PULP, CMOS 40 nm) : un cœur RISC-V de contrôle + cluster de 8 cœurs RISC-V ri5cy
  avec extensions DSP (builtins p.extractu, p.insert, p.cnt), 64 Ko L1, 512 Ko L2 ; à 100 MHz et
  0,8 V ; deep sleep 72-108 µW (§III-A, §V-C). Référence : **STM32F407** (Cortex-M4 à 168 MHz,
  1,85 V, 90 nm) (§V).
- Mémoire : IM 5 Ko, CIM 27 Ko, prototype ≈ 2 Ko par classe (linéaire en nombre de gestes)
  (§IV-B).
- Accélérations par rapport au Cortex-M4 : jusqu'à ×19,2 sur l'encodeur et ×17,3 sur
  l'inférence complète avec 8 cœurs + builtins (§V-B).
- Énergie : sans l'ADC dans la comparaison d'architectures (§V-C) ; la mesure du « 10,4 mW »
  n'est pas décrite (portée non précisée). Code : non publié.

## Résultats

- Précision moyenne : **85 % sur 11 gestes** (Abstract, §VII) — mais 90,40 % dans l'introduction
  (§I) ; au plus 4 points sous le SVM (§V-A, Fig. 6).
- Temps d'entraînement HDC déterministe, linéaire en nombre de classes, **2 à 3 ordres de
  grandeur sous le SVM** (§V-A, Fig. 5).
- Énergie d'entraînement (11 gestes) : 29,02 mJ sur Cortex-M4, 5,35 mJ sur Mr. Wolf 1 cœur,
  ×49,1 de gain avec 8 cœurs + builtins (§V-C) ; 10,04 mJ annoncés pour le système complet
  (Abstract).
- Énergie par classification : 7,2 µJ sur Mr. Wolf 8 cœurs, gain ×44 sur le Cortex-M4 (§V-C) ;
  83,2 µJ pour le système (Abstract) ; latence de classification 8 ms (§II).
- Puissance moyenne en classification : 10,4 mW, soit ≈ 29 h sur 100 mAh (Abstract) ; 0,82 mW
  pour Mr. Wolf 8 cœurs seul (§V-C) ; ≈ 300 h d'autonomie sans l'ADC (§V-C).
- Passage à 256 canaux : temps et mémoire linéaires ; 12 h d'autonomie avec l'ADC (§VI).

→ reportés dans `benchmarks.csv` : 3 lignes (Mr. Wolf 8 cœurs : inférence et apprentissage ;
STM32F407 : apprentissage), `medium` (Table II absente de l'extraction, valeurs du texte).

## Limites et critique

- **Test sur tout le jeu, entraînement compris** (25 % des échantillons servent aux deux) :
  précision optimiste ; les auteurs disent l'écart avec un découpage par essais < 1 % (§V).
- Chiffres incohérents entre sections : 85 % vs 90,40 % ; 10,4 mW vs 10,04 mW ; 83,2 µJ vs 7,2 µJ
  par classification (système avec ADC vs cœur seul, déduit).
- La comparaison d'énergie Cortex-M4 / Mr. Wolf mêle technologie (90 vs 40 nm), fréquence et
  tension : l'architecture n'explique qu'une partie du gain (reconnu §V-C).
- « Online learning » = recalcul d'un prototype par classe sur une session ; pas de scénario de
  dérive inter-sessions mesuré, pas de mise à jour incrémentale des prototypes évaluée.
- Pas de code publié ; Table I (état de l'art) et Table II (cycles, énergie) absentes de
  l'extraction.

## Pertinence pour la thèse

Référence d'apprentissage réellement embarqué et ultra-basse consommation : l'HDC apprend en une
passe, sans rétropropagation, avec des opérations binaires et une mémoire de quelques dizaines de
Ko, et ajoute une classe sans toucher aux autres (un prototype de plus, pas d'oubli structurel).
Il situe la gamme PULP (mW, µJ par inférence) face au Cortex-M4 et montre l'intérêt des
extensions DSP et du parallélisme. Pour la PdM, le paradigme prototype + distance est une
alternative légère à un réseau régularisé par EWC, pour la classification de défauts (déduit).

## Gaps identifiés

- HDC pour séries temporelles de vibrations / PdM et pour la régression (RUL) : non traité.
- Mise à jour incrémentale des prototypes HDC sous dérive inter-sessions : non évaluée.
- Comparaison HDC vs réseau quantifié + EWC à budget énergétique égal sur MCU.

## Statut de lecture

Papier complet (`fulltext.md` lu en entier). Tables I et II sans corps à l'extraction (cycles et
énergie par kernel manquants) ; figures non disponibles.
Déduit et non affirmé par les auteurs : explication de l'écart 83,2 / 7,2 µJ, transposition à la
PdM.
