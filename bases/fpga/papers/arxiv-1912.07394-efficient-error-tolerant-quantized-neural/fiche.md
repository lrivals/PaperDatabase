---
id: arxiv-1912.07394-efficient-error-tolerant-quantized-neural
fiche: done
date: 2026-09-29
---

# Efficient Error-Tolerant Quantized Neural Network Accelerators

Giulio Gambardella, Johannes Kappauf, Michaela Blott, Christoph Doehring, Martin Kumm, Peter Zipf, Kees Vissers, 2019, 2019 IEEE International Symposium on Defect and Fault Tolerance in VLSI and Nanotechnology Systems (DFT). https://doi.org/10.1109/DFT.2019.8875314 (arXiv : https://arxiv.org/abs/1912.07394)
Type : conférence (version arXiv accessible ; relecture par les pairs de la version DFT non vérifiée ici)

## Problème

Les QNN (binarisés, faible précision) sont supposés robustes aux fautes, mais leur robustesse face aux fautes permanentes dans un accélérateur matériel est mal connue, et la redondance classique (TMR) coûte +200 % (§V-B). Il s'agit de mesurer rapidement l'impact des fautes et de le réduire à moindre coût (Abstract, §I).

## Méthode

- Injection d'erreurs « stuck-at » sur un canal de sortie entier d'une couche, via la modification des seuils du bloc de seuillage MVTU de l'architecture FINN (fixer les seuils à ±th_max), exécutée sur FPGA (§IV). Métrique : précision globale sur le jeu de test complet (10 000 images).
- Réseaux : LFC (MLP, MNIST) et CNV (6 conv, CIFAR-10) de FINN, à précisions W1A1, W1A2, W2A2 (et W4A4 dans la Table III) (§IV).
- Optimisation 1 : réplication sélective de canaux (TMR uniquement sur les canaux critiques) selon un seuil de chute de précision tolérée (§V-B).
- Optimisation 2 : ordonnancement tolérant aux fautes des canaux sur les PE, par programmation linéaire en nombres entiers (ILP), pour maximiser la précision au pire cas avec un PE défaillant (§VI-B). Sans surcoût matériel (réordonnancement des poids).
- Toolflow : FINN, code public d'après les auteurs (§III-A, référence [17]).

## Plateforme et implémentation

Xilinx ZCU104 (XCZU7EV) à 300 MHz pour l'injection accélérée (§VI-B). Ressources (LUT, DSP, BRAM) : n/r. Puissance : n/r. Modèle de coût matériel des MAC : 1,6·w·a (§V-C, d'après [16]). Code d'injection : non publié (le code FINN de base est public ; l'outil d'injection, cité comme travail futur de généralisation, n'est pas indiqué comme publié).

## Résultats

- LFC (MLP) : chute pire cas de seulement 0,09 % (W2A2, s@-1) (Table I, §V-A).
- CNV : précision sans erreur 79,22 % (W1A1), 82,66 % (W1A2), 84,29 % (W2A2) ; pire cas avec un canal bloqué : 73,01 % (W1A1, s@1), 71,85 % (W1A2, s@1), 74,18 % (W2A2, s@1), soit des chutes jusqu'à ~10,8 points (Table II, §V-A). Un canal fixé peut même améliorer la précision (+0,54 % en W1A1), signe de redondance.
- Réplication sélective : surcoût en opérations MAC de 173,47 % / 129,70 % / 49,87 % (CNV-W1A1, pour une chute pire cas tolérée ≤ 0,5 / 1 / 2 %) contre 200 % pour un TMR complet (Table III). Aucun canal des couches FC n'a besoin d'être triplé.
- Ordonnancement (CNV-W1A1, couche 0, folding 2, un PE défaillant) : pire cas 74,82 % (ordonnancement FINN par défaut) -> 76,70 % (ILP), soit +1,88 point (§VI-B, Fig. 5).
- Vitesse : 32 880 FPS d'injection sur ZCU104 en W1A1 ; campagne de ~59 h contre plus de 14 jours sur NVIDIA P40 sous Theano, soit 5,8x plus rapide (§VI-B).
→ reportés dans `benchmarks.csv` (via `bench_rows.csv`) : 1 ligne (CNV-W1A1 sur ZCU104).

## Limites et critique

- Modèle de faute : stuck-at d'un canal entier dans la sortie d'activation, pas des SEU dans la mémoire de configuration ni des fautes de poids ; les SEU sont reportés en travail futur (§VII).
- Seuls des petits réseaux de classification (MNIST, CIFAR-10) ; aucune détection d'objets, aucun YOLO ; extrapolation à des réseaux plus grands non montrée.
- Fautes uniques seulement ; l'ILP suppose une faute par PE et demande une campagne d'injection exhaustive (635 276 expériences par valeur pour f=4, c=64) qui explose avec la taille du réseau (§VI-B).
- Le seuil « ≥ 2 % de chute » du critère de réplication est arbitraire et non relié à un niveau de sûreté (SIL) ; le papier parle de « safety integrity level » sans faire le lien chiffré.
- Le FPS de 32 880 est celui du montage d'injection W1A1, pas un benchmark d'inférence optimisé. Comparaison GPU (P40 / Theano) ancienne (déduit).
- La Table II est celle extraite par GROBID ; la légende ne porte pas d'avertissement de reconstruction.

## Pertinence pour la thèse

Directement dans l'axe fiabilité matérielle : méthodologie d'injection de fautes rapide sur FPGA pour des QNN FINN, TMR sélectif comme alternative moins coûteuse, et démonstration que les couches convolutives sont sensibles (jusqu'à ~10 points) et donc pas « naturellement » tolérantes. Le résultat fonde l'argument qu'un YOLO quantifié sur FPGA en zone dangereuse a besoin d'une analyse de sensibilité par canal et d'un durcissement sélectif. Laisse ouvert : détecteurs d'objets, SEU en mémoire de configuration, lien avec les niveaux SIL/PL.

## Gaps identifiés

- Injection de fautes et durcissement sélectif appliqués à un détecteur d'objets (YOLO) quantifié plutôt qu'à des classifieurs MNIST/CIFAR.
- Passage du modèle stuck-at de canal aux SEU réels (config, BRAM).
- Lien entre chute de précision tolérée et niveau d'intégrité de sûreté requis.

## Statut de lecture

papier complet (fulltext.md lu en entier, tables I à III incluses ; Fig. 1 et 2 seulement en légende ; la Fig. 3 : légende et fragment de texte). Déduit et non affirmé par les auteurs : l'ancienneté de la baseline GPU, l'absence de publication du code d'injection, la pertinence pour un détecteur d'objets.
