---
id: arxiv-2505.23355-grower-loop-interactive-reinforcement-learning
fiche: done
date: 2026-11-03
---

# Grower-in-the-Loop Interactive Reinforcement Learning for Greenhouse Climate Control

Maxiu Xiao, Jianglin Lan, Jingxin Yu, Weihong Ma, Qiuju Xie, Congcong Sun, 2025, arXiv preprint. https://arxiv.org/abs/2505.23355 (DOI : n/r)
Type : preprint non relu par les pairs

## Problème

Le RL appliqué au contrôle climatique de serre souffre d'une faible efficacité d'apprentissage et d'une forte dépendance aux conditions initiales ; il exclut aussi le producteur de la boucle, ce qui freine son adoption (§1). Le RL interactif (entrée humaine pendant l'apprentissage) n'a jamais été appliqué à ce domaine, et les entrées d'un producteur sont imparfaites : disponibilité, biais cognitif, latence et niveau de connaissance se contredisent (§3.2).

## Méthode

- Environnement simulé de serre de laitue en conditions hivernales (modèle dynamique de van Henten, réf. [21] du papier), pas de 15 min, pas de contrôle 1 h ; 27 actions discrètes : consigne de température (-2/0/+2 °C), consigne de CO2 (-200/0/+200 ppm), ventilation (-0,5/0/+0,5 mm/s) ; chauffage et injection de CO2 convertis en consignes par PI (§2.1, Table 1). Récompense = profit (laitue - CO2 - chauffage) moins une pénalité de contraintes (éq. 1, Table 2).
- Baseline : PPO (Stable-Baselines3) (§2.2).
- Trois algorithmes de RL interactif : reward shaping (éq. 4) et control sharing (éq. 6) avec un retour binaire (bon/mauvais), policy shaping (éq. 5) avec un conseil d'action (précis ou par contraintes) (§4.1). Un réseau auxiliaire (fonction F ou π_grower) estime l'entrée, ce qui ramène l'apport humain à de l'apprentissage actif « pool-based » ; sélection aléatoire ou « sélective » (réseau π_error, inspiré de SafeDAgger) des pas où demander l'entrée (§4.2, Algorithme 1).
- Producteur simulé à partir de connaissances pré-extraites (donc biaisées) : retour et conseil précis (valeurs optimales de croissance, haute connaissance), conseil par contraintes (plages, basse connaissance) (§3.3, Tables 5-6). Poids β décroissant linéairement jusqu'à 0 sur les 400 000 premiers pas.

## Plateforme et implémentation

Simulation seule, pas de matériel : puissance, FPS, latence, ressources FPGA et quantification : n/r. Entraînement : épisodes de 14 jours (336 pas), 500 000 pas au total, 15 graines, réseaux 512×4 (Tables 7-8). Test : cycle complet de 56 jours, météo horaire de La Haye (Den Haag) 2021-2024, 7 trajectoires ; entraînement sur 2011-2020 (nov.-févr.) (§5.1). CO2 extérieur supposé constant à 400 ppm. Code : non mentionné dans le texte lu (non publié, à notre lecture).

## Résultats

Récompense cumulée moyenne en test (Hfl/m², Table 9) : PPO de base 1,91 ; PPO avec le seul retour simulé comme récompense 0,71 (-62,8 %) ; policy shaping précis (β=0,2) 2,07 (+8,4 %) ; policy shaping par contraintes (β=0,1) 1,97 (+3,1 %) ; control sharing (β=0,05) 2,04 (+6,8 %) ; reward shaping (β=0,2) 1,73 (-9,4 %). Les valeurs de β sont les meilleures sur le test (§5.3), donc choisies sur le jeu d'évaluation.
- Policy shaping précis et control sharing : environ -10 % d'énergie et de CO2 pour un poids récolté similaire (§5.3, Fig. 4) ; reward shaping réduit aussi énergie et CO2 mais baisse le poids récolté.
- β trop élevé n'accélère pas l'apprentissage ; plage utile β = 0,05-0,2 (§5.4, Fig. 6-7).
- Disponibilité limitée : le conseil d'action est moins sensible que le retour ; la sélection discrépance (π_error) bat l'aléatoire pour π_grower mais pas pour F (§5.5, Fig. 8-9). Pas de chiffre dans le texte pour ces courbes (figures seulement).
→ reportés dans `benchmarks.csv` : 6 lignes proposées (Table 9, toutes `confidence: high`, `chunk_id` 2505.23355#047.0), à intégrer par l'agent principal. Plateforme matérielle `n/r (simulation)`.

## Limites et critique

- Simulation uniquement, producteur simulé (règles pré-calculées) : aucun producteur réel, donc la question centrale (entrées humaines réelles) n'est pas testée ; le « biais cognitif » est modélisé, non mesuré.
- Gains modestes (+3 à +8 %) sans intervalle de confiance ni test statistique rapportés pour Table 9 malgré 15 graines ; β réglé sur le test, ce qui gonfle les résultats (déduit).
- Un seul algorithme (PPO) ; l'explication par le GAE est une hypothèse des auteurs (« probablement »), non vérifiée. Espace d'actions discret, 27 actions seulement ; la discrétisation limite le réalisme.
- Une seule culture (laitue), un seul climat (hiver néerlandais), un seul modèle de serre ; pas d'actuateur de refroidissement, d'où températures nocturnes élevées (§5.3). Pas de comparaison avec MPC ni avec un contrôleur à règles (déduit : absence), alors que le MPC est cité comme référence (§1).
- Les prix (Hfl, florins néerlandais) sont anciens, repris de [16] ; le profit n'est pas comparable à d'autres études sans conversion.
- Le texte extrait de §5.5 est désordonné (phrases coupées entre colonnes) ; les courbes de perte ne sont pas chiffrées.
- Code non publié (à notre lecture) : reproductibilité faible.

## Pertinence pour la thèse

Axe `climate-control` (RL pour le climat de serre, laitue). Pour SerreIA : la baseline de pratiques est un contrôleur à règles avec agent LLM validé par un humain ; ce papier fournit un cadre pour intégrer des conseils d'opérateur (action advice, contraintes de plages comme Table 6) dans une boucle apprenante, et l'observation que le conseil d'action tolère mieux le manque de disponibilité que le retour. Les plages de Table 6 (T° jour 10-25 °C, nuit 6-10 °C ; CO2 400-1500 / 300-600 ppm) sont des contraintes de simulation, pas des consignes de culture sourcées : à ne pas utiliser pour `recettes.yaml`. Laisse ouvert : validation sur matériel réel, producteurs réels, MPC comme point de comparaison.

## Gaps identifiés

- Aucun test avec des opérateurs humains réels dans une serre de contrôle climatique.
- Pas de comparaison RL interactif vs MPC vs règles sur le même simulateur.
- Pas de variante avec un agent LLM comme source d'entrée (conseil en langage naturel) ni de garde-fous pour l'application à un système physique.

## Statut de lecture

Papier complet (fulltext.md lu en entier ; extraction grobid, `ok: true`). Réserves : le résumé est tronqué dans le texte extrait (fin de la phrase sur la robustesse) ; §5.5 est mal ordonné ; les tableaux 2, 3, 6, 10 étaient listés « sans corps extrait » dans les avertissements mais leur corps figure en partie dans le texte (Tables 2 et 6 lues ; Table 3 lue en texte courant), Table 9 a un corps complet. Déduit et non affirmé par les auteurs : β choisi sur le test donc optimiste ; absence de code publié ; absence de comparaison MPC/règles ; absence d'intervalles de confiance.
