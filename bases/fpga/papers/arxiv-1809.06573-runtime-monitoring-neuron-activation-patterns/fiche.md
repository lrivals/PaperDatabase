---
id: arxiv-1809.06573-runtime-monitoring-neuron-activation-patterns
fiche: done
date: 2026-09-29
benchmarks: none
---

# Runtime Monitoring Neuron Activation Patterns

Chih-Hong Cheng, Georg Nührenberg, Hirotoshi Yasuoka, 2018, arXiv preprint. https://arxiv.org/abs/1809.06573
Type : preprint non relu par les pairs

## Problème

Pour utiliser un réseau de neurones en domaine critique, il faut savoir à l'exécution si une décision est étayée par des similarités avec l'entraînement ou si le réseau opère « hors de sa zone de confort » (§I). Les méthodes de vérification formelle à la compilation (Reluplex, Planet) sont limitées à des réseaux linéaires par morceaux de petite taille (§IV).

## Méthode

Après l'entraînement, les patrons d'activation « on/off » (ReLU > 0) d'une couche proche de la sortie sont enregistrés pour toutes les images d'entraînement correctement classées, par classe, dans un BDD (binary decision diagram) : le « comfort zone » (Définition 2) (§II). Cette zone est élargie par distance de Hamming <= gamma via quantification existentielle (Algorithme 1). En opération, le moniteur signale « décision non étayée » si le patron de la nouvelle entrée est hors de la zone de sa classe prédite ; la requête est linéaire en nombre de neurones (§I). Pour les couches larges (limite pratique des BDD ~200 variables), sélection des neurones importants par analyse de sensibilité par gradient (§II). Le gamma est choisi sur un jeu de validation pour que « patron inconnu » corresponde souvent à une erreur (§I, §III). Implémentation PyTorch et package Python `dd` (§III).

## Plateforme et implémentation

Logiciel sur CPU/GPU (n/r), sans FPGA. Aucune mesure de ressources, latence ou puissance (n/r). Code : non indiqué comme publié.

## Résultats

Table I (§III) : réseau 1 (MNIST, taux d'erreur 1,19 %) et réseau 2 (GTSRB, taux d'erreur 3,27 %, seule la classe stop c = 14 surveillée, 25 % des 84 neurones de la couche choisis par gradient). Part d'images hors patron / part de mal classées parmi elles :

| gamma | MNIST | GTSRB |
|---|---|---|
| 0 | 7,66 % / 10,70 % | 32,92 % / 10,13 % |
| 1 | 2,01 % / 21,89 % | 15,0 % / 19,44 % |
| 2 | 0,6 % / 31,66 % | 7,08 % / 41,17 % |
| 3 | n/r | 4,58 % / 54,54 % |

Ainsi, avec gamma = 3 sur GTSRB, le moniteur reste silencieux 95,42 % du temps et, quand il alerte, l'image est mal classée dans 54,54 % des cas (§III). Une étude de cas sur un système de détection du véhicule de tête pour un pilotage autoroutier est mentionnée (Fig. 3) mais sans résultats chiffrés dans le texte extrait (n/r).
→ reportés dans `benchmarks.csv` : aucune ligne (méthode logicielle, pas de mesure matérielle) ; `benchmarks: none`.

## Limites et critique

- Résultats sur MNIST et GTSRB (classification), pas sur des détecteurs d'objets ; l'extension à YOLO est annoncée comme « directement applicable » (§V) mais non testée.
- La part de vrais positifs est modeste : même à gamma = 3, 45 % des alertes ne sont pas des erreurs ; le moniteur ne détecte qu'une fraction des erreurs de classification (le rappel des erreurs n'est pas donné explicitement dans le texte extrait ; n/r).
- L'affirmation d'une garantie « sûre » (surapproximation des patrons visités, §IV) ne concerne que la notion d'« hors patron » ; elle ne garantit rien sur la correction de la sortie. Le taux d'alertes en opération suppose l'absence de dérive de distribution (note 3, §III).
- La zone est construite sur le jeu d'entraînement ; le choix de gamma se fait sur un jeu de validation supposé de même distribution que l'opération. Le passage à l'échelle des BDD (~200 variables) impose une sélection de neurones.
- Aucun coût d'implémentation embarquée évalué : la portabilité d'un BDD sur FPGA (mémoire, latence) est une question ouverte (déduit).

## Pertinence pour la thèse

Référence fondatrice pour l'axe surveillance à l'exécution : moniteur d'OOD léger, à structure binaire, dont l'abstraction (patrons on/off d'une couche) est très proche du calcul de seuillage des accélérateurs quantifiés (FINN, BNN) et donc plausiblement implantable sur FPGA en parallèle du réseau (déduit). Utile pour un YOLO de détection de personnes : signaler les entrées inhabituelles (éclairage, occultation, patchs adverses) sans changer le réseau. Ce qui reste ouvert : détecteurs d'objets, implémentation matérielle, taux d'alerte requis par une exigence de sûreté.

## Gaps identifiés

- Moniteurs d'activation implémentés sur FPGA (coût en LUT/BRAM et latence) pour un détecteur d'objets quantifié.
- Évaluation d'un moniteur d'activation sur des données de personnes en zone industrielle (dérive de distribution, patchs adverses).

## Statut de lecture

papier complet (fulltext.md lu en entier ; extraction GROBID ok ; la section III est rattachée à la précédente ; le Table I a été lue dans « Figures et tableaux » ; l'étude de cas du véhicule de tête est tronquée). Déduit et non affirmé par les auteurs : la portabilité FPGA, le lien avec les seuils FINN, l'utilité contre les patchs adverses.
