---
id: arxiv-1804.06913-fast-inference-deep-neural-networks
fiche: done
date: 2026-10-26
---

# Fast inference of deep neural networks in FPGAs for particle physics

Javier Duarte, Song Han, Philip Harris, Sergo Jindariani, Edward Kreinar, Benjamin Kreis, Jennifer Ngadiuba, Maurizio Pierini, Ryan Rivera, Nhan Tran, Zhenbin Wu, 2018, JINST 13 P07027 (2018). https://doi.org/10.1088/1748-0221/13/07/P07027 (arXiv 1804.06913)
Type : article de revue (JINST, venue donnée par arXiv `journal_ref`) ; version lue : preprint arXiv, non vérifiée contre la version publiée.

## Problème

Le déclenchement de niveau 1 (L1) du LHC exige une inférence de réseau de neurones en moins d'une microseconde, à 40 MHz, ce que CPU et GPU ne permettent pas (§1). Les auteurs veulent savoir quels réseaux entrent dans un FPGA sous ces contraintes de latence et de ressources, et rendre ce portage accessible aux physiciens sans VHDL/Verilog.

## Méthode

- Outil `hls4ml` : traduit un modèle Keras ou PyTorch (architecture, poids, biais) en projet Vivado HLS 2017.2 (§1, §2.1). Réseaux entièrement connectés seulement ; chaque couche est calculée de façon indépendante et séquentielle, l'ensemble étant pipeliné (§2.1).
- Cas d'étude : classifieur de jets à 5 classes (q, g, W, Z, t) sur 16 observables expertes, MLP à trois couches cachées, 4389 paramètres, ReLU, softmax (§2.2). Données simulées (MadGraph, Pythia8), 200 000 événements par classe.
- Trois leviers (§2.3) : compression (élagage itératif avec régularisation L1, 70 % des poids retirés : 3051 sur 4389), quantification (virgule fixe `<X,Y>`, X bits au total dont Y entiers, sans réentraînement quantifié), parallélisation (« reuse factor » R : un multiplicateur réutilisé R fois, latence par couche L_m = L_mult + (R-1)·II_mult + L_activ, Eq. 2.4).
- Activations non triviales précalculées en BRAM ; ReLU en logique (§2.1). Les poids restent en logique, donc les multiplications par zéro sont éliminées à la synthèse (§3.2).

## Plateforme et implémentation

- Cible de synthèse : Xilinx Kintex UltraScale `xcku115-flvb2104-2-i`, horloge fixée à 200 MHz (§3.2).
- Ressources de la section 3.2 : estimations de la synthèse HLS (Vivado HLS), pas de place-and-route ; les auteurs les jugent conservatrices (§3.2).
- Implémentation réelle (§3.3) : seulement avec un réseau plus petit (une couche cachée, 10 entrées, 1 sortie, Fig. 4 droite), dans un habillage VHDL « bare » relié aux broches ; l'horloge d'implémentation a dû être relâchée à 8 ns (5 ns visés en HLS, pour le réseau 3 couches 32 bits).
- Puissance : tracée en Fig. 15 pour le modèle 3 couches, mais méthode de mesure ou d'estimation non décrite et valeurs non tabulées : `n/r`, portée `unspecified`.
- Code : `hls4ml` est publié (note de bas de page 1 du papier, URL non reprise dans le texte extrait) ; bitstream non publié (déduit : non mentionné).

## Résultats

- Précision : le rapport AUC/AUC attendue (flottant 32 bits) est de 99,68 % (non compressé) et 99,55 % (compressé) à `<16,6>` (Table 2). Environ 16 bits au total suffisent, avec 6 bits entiers (§3.1, Fig. 9 et 10).
- Table 2, `<16,6>`, R = 1, 200 MHz, **estimation Vivado HLS** : non compressé 4389 paramètres, 3329 DSP48E, 263 234 « logic » (LUT + FF cumulés), 75 ns ; compressé 1338 paramètres (facteur 3,3), 954 DSP48E, 88 797 « logic », 75 ns (Table 2).
- Latence : environ 15 cycles à 200 MHz, soit 75 ns, pour R = 1 (§3.2) ; elle croît de 4 cycles par incrément de R (une par couche, Fig. 14, §3.2). Le résumé donne 75 à 150 ns et environ 10 % des DSP du Kintex (§4).
- HLS contre implémentation (réseau une couche, §3.3, Fig. 16 et 17) : les DSP concordent pour les multiplications à un seul DSP (moins de 24 bits), l'implémentation en utilise moins ailleurs ; les FF estimés en HLS sont 2 à 4 fois trop hauts, les LUT aussi sont surestimées.
- Les courbes des Fig. 11 à 14 (DSP, LUT, FF, latence et II selon la précision et R) ne sont pas tabulées : aucune valeur chiffrée n'en est reprise.
- Baseline : aucune comparaison CPU, GPU ou Jetson ; renvoyée à de futurs travaux (§4).
→ reportés dans `benchmarks.csv` (à écrire par l'agent principal) : 2 lignes, modèle non compressé et compressé, `<16,6>`, R = 1 (Table 2).

## Limites et critique

- Ressources de la Table 2 = estimations HLS, pas des ressources après implémentation ; la même étude montre un surestimé de 2 à 4 fois pour FF et LUT (§3.3). Elles ne sont pas comparables à des chiffres post-implémentation d'autres papiers.
- « Logic » de la Table 2 additionne LUT et FF : pas de colonne LUT séparée ; BRAM non étudiée (§3.2).
- Débit (FPS) et II non donnés dans la Table 2 (texte : II égal au reuse factor, soit 1 ici, déduit) ; puissance non tabulée.
- Réseau MLP de 4389 paramètres sur 16 entrées tabulaires : pas de CNN, pas de vision ; l'extrapolation à un détecteur d'images n'est pas démontrée. Les CNN sont annoncés comme travail futur (§4).
- Quantification post-entraînement uniquement ; le réentraînement quantifié est laissé de côté (§2.3).
- Les auteurs n'avaient pas fait fonctionner l'objectif d'horloge de la synthèse à l'implémentation (5 ns visés, 8 ns obtenus) : la latence de 75 ns suppose l'horloge de la synthèse, non celle de l'implémentation (déduit : 15 cycles à 8 ns donneraient 120 ns).
- Aucune analyse de pire cas ni de sûreté : la latence est un résultat de synthèse déterministe d'un pipeline, sans preuve de borne.

## Pertinence pour la thèse

Papier fondateur de `hls4ml`, un toolflow HLS de référence pour poser un petit réseau en virgule fixe sur FPGA avec une latence déterministe et sans partage de ressources. Pour le sujet ARCYS : (1) un moniteur de prédiction d'échec (petit MLP ou tête de confiance sur les sorties d'un détecteur de personnes) a justement la forme visée, petit, entièrement connecté, à faible latence, donc `hls4ml` est un candidat pour l'implanter à côté du détecteur ; (2) l'étude de la précision `<X,Y>` (6 bits entiers, environ 16 au total sans perte d'AUC) est un modèle pour mesurer l'effet de la quantification sur la décision, même s'elle porte sur l'AUC moyenne et non sur les faux négatifs critiques ; (3) la latence par couche (Eq. 2.4) et le reuse factor donnent une latence calculable, un point de départ pour un argument de délai borné en lien avec la question WCET, sans que le papier ne fasse de WCET. Ce que le papier laisse ouvert : aucune sortie anticipée, aucune prédiction d'échec, aucune certification, aucun CNN, aucun flux vidéo.

## Gaps identifiés

- Pas de borne temporelle formelle ni de WCET pour un pipeline `hls4ml` hors contexte LHC.
- Effet de la quantification sur les décisions critiques (faux négatifs) non étudié : seule l'AUC moyenne l'est.
- Écart entre estimations HLS et implémentation (FF et LUT 2 à 4 fois surestimés) : à prendre en compte avant de comparer des ressources entre papiers.

## Statut de lecture

Papier complet (`fulltext.md` lu en entier ; extraction GROBID correcte). La Table 2 est lue depuis `sections.jsonl` / TEI (extraction GROBID, non reconstruite) ; les valeurs des Fig. 11 à 17 n'étaient pas lisibles en texte.
Ce qui suit est déduit et non affirmé par les auteurs : l'absence de bitstream publié ; II = 1 pour R = 1 pour la Table 2 ; la latence de 120 ns à 8 ns d'horloge ; l'adéquation de `hls4ml` à un moniteur de prédiction d'échec.
