---
id: arxiv-2501.14377-dream-fly-model-reinforcement-learning
fiche: done
date: 2026-10-01
benchmarks: none
---

# Dream to Fly: Model-Based Reinforcement Learning for Vision-Based Drone Flight

Angel Romero, Ashwin Shenai, Ismail Geles, Elie Aljalbout, Davide Scaramuzza, 2025, arXiv preprint. https://arxiv.org/abs/2501.14377
Type : preprint non relu par les pairs (le texte dit « accepted for publication at the… », venue tronquée dans l'extraction : n/r)

## Problème

Apprendre une politique visuomotrice de course de drones (pixels RGB d'une seule caméra vers poussée collective et vitesses angulaires, format CTBR), sans représentation intermédiaire simplifiée (masque binaire des portes, [10]) ni amorçage par imitation d'un expert à état privilégié ([12]) (§I). Les méthodes sans modèle (PPO, SAC) sont peu efficaces en échantillons dans ce cadre.

## Méthode

DreamerV3 (RL avec modèle du monde) : RSSM (encodeur CNN, modèle récurrent, prédicteurs de dynamique, de récompense et de continuation, décodeur) + acteur-critique entraînés sur des trajectoires imaginées, horizon T = 16 (§III-D). Observation : image RGB redimensionnée en 64×64 (§IV). Récompense : progression vers le centre de la porte, pénalité sur les vitesses angulaires (b1 = 1,0 ; b2 = 0,01), r_collision = -4, r_passed = +10 (§III-C) ; curriculum sur b2, nul au départ (§IV-A). Configuration « Large » de DreamerV3 (MLP 4 couches de 768 unités, 2048 unités récurrentes) (§IV). Baselines : PPO et SAC, CNN + MLP 4×768 (§IV). Pas de quantification ni de compression ; aucune optimisation pour l'embarqué.

## Plateforme et implémentation

Entraînement : un GPU Quadro RTX 8000 ; PyTorch (dreamerv3-torch, stable-baselines3), simulation Flightmare + Agilicious avec rendu Habitat dans la boucle (plusieurs milliers d'images/s) (§IV). Quadrirotor simulé : m = 0,6 kg, poussée maximale par rotor 4,0 N, rapport poussée/poids 2,7 (§IV). Déploiement réel : variante d'Agilicious, calculateur de bord remplacé par un récepteur RF relié à un contrôleur de vol Betaflight ; les commandes viennent d'un ordinateur déporté, les images sont rendues par Habitat (hardware-in-the-loop, HIL) (§V-A). Puissance, latence d'inférence, FPS, mémoire du réseau : n/r. Code : non publié d'après le texte lu (lien vidéo seulement, https://www.youtube.com/watch?v=nctQ2rxZnIc) ; à vérifier hors fulltext.

## Résultats

- Sur trois pistes (Circle, Kidney, Figure 8), 5 graines chacune, DreamerV3 converge en 20 M d'interactions ; PPO et SAC n'atteignent aucun vol utile (Fig. 3, §IV-A). Aucune valeur numérique de récompense dans le texte.
- Temps d'entraînement DreamerV3 : environ 240 h, nettement plus que les baselines (§IV-A, §VI).
- Comportement « perception-aware » émergent : la caméra se tourne vers les portes sans terme de récompense dédié ; avec deux portes décoratives supplémentaires, le regard se répartit sur toutes (Fig. 5, §IV-B).
- HIL sur la piste Figure 8 : trajectoires et profils de vitesse simulés et réels proches (Fig. 6, §V-B) ; vitesses jusqu'à 9 m/s (résumé, non rapportées numériquement ailleurs).
→ reportés dans `benchmarks.csv` : aucune ligne. Aucun FPS, GOPS, latence, puissance ou précision n'est rapporté, seulement des courbes de récompense et des figures ; le papier n'est pas un survey, mais rien n'est justifiable (`benchmarks: none`).

## Limites et critique

- Le « réel » est un HIL : les pixels sont rendus (Habitat), pas capturés par une caméra de bord ; l'écart sim-to-real de perception reste entier (reconnu en §VI). La conclusion sur la « petite différence sim-to-real » ne porte que sur la dynamique.
- Entraînement très coûteux (240 h sur un GPU de bureau) ; inférence sur ordinateur déporté, pas à bord : aucune évaluation de l'embarquabilité (taille du modèle Large, latence, énergie). Le réseau Large DreamerV3 (2048 unités récurrentes) est probablement hors de portée d'un Jetson/MCU sans compression (déduit).
- Comparaison aux baselines PPO/SAC uniquement sur courbes de récompense, sans temps de tour ni taux de réussite chiffrés ; pas de comparaison à l'état de l'art de la course (états estimés, [4], [5]) ni à [10], [12] en performance.
- Résolution 64×64 : les détails de fond sont perdus (reconnu en §IV-B).
- Preprint, une seule piste testée en réel, nombre d'essais n/r.

## Pertinence pour la thèse

Axe `tracking-navigation`, sous-thème vol agile (tag `drone-racing`) : référence de la chaîne perception → contrôle de bout en bout, en gamme GPU de bureau pour l'entraînement (aucune mesure à bord). Intéressant comme point de contraste : le goulot de calcul se déplace de l'inférence vers l'entraînement, et la boucle perception-action empêche de découpler un détecteur compressé. Aucun lien direct avec FPGA, MCU ou quantification.

## Gaps identifiés

- Aucune politique visuomotrice par MBRL évaluée avec latence, énergie ou taille de modèle à bord (Jetson, FPGA, MCU).
- Effet de la quantification ou de la compression d'un modèle du monde sur la qualité du vol : non étudié.
- Passage du HIL à de vraies images de caméra : non traité.

## Statut de lecture

Papier complet (fulltext.md lu en entier). Extraction PyMuPDF (`extraction.ok: false`) : légendes de figures mélangées au texte, équations disloquées, aucune table extraite (le papier n'en contient pas, d'après le texte). Venue finale et publication des sources non établies.
Ce qui suit est déduit et non affirmé par les auteurs : l'inadéquation du modèle Large à l'embarqué ; l'absence de code publié (non mentionné dans le texte lu).
