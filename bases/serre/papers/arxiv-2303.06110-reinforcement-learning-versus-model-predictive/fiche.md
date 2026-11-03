---
id: arxiv-2303.06110-reinforcement-learning-versus-model-predictive
fiche: done
date: 2026-11-03
---

# Reinforcement Learning Versus Model Predictive Control on Greenhouse Climate Control

Bernardo Morcego, Wenjie Yin, Sjoerd Boersma, Eldert van Henten, Vicenç Puig, Congcong Sun, 2023, arXiv preprint. https://arxiv.org/abs/2303.06110
Type : preprint non relu par les pairs

## Problème

Peu de travaux comparent MPC et RL pour le climat de serre, ni mathématiquement ni en performance (Abstract, §1). Les auteurs veulent formuler les deux dans un cadre unifié (principe de prédiction, coût/récompense, contraintes), puis les comparer sur un même cas : une serre de laitue simulée (§1, §3).

## Méthode

- Modèle de serre de laitue à 4 états (matière sèche, CO2, température, humidité), 3 commandes (apport de CO2, ventilation, chauffage) et 4 perturbations météo, repris de la réf. [7], discrétisé en Runge-Kutta 4, pas h = 15 min (§2, Table 4).
- MPC non linéaire à horizon glissant, Np = 6 h, coût = maximiser la matière sèche finale moins énergie des commandes, contraintes de bornes, de pente et de température jour/nuit (10-15 °C / 15-20 °C selon le rayonnement) (§3.1, Eq. 2-5, Table 4). Résolu avec CasADi + IPOPT sous Matlab, single shooting (§4.2).
- RL : DDPG (acteur-critique, hors politique, sans modèle), état à 10 termes, récompense à 6 termes qui recode coût et contraintes (accroissement de matière sèche, récompense/pénalité CO2 et température, pénalité des commandes) ; gamma = 0,9 réglé par essais pour approcher le comportement du MPC (§3.2, Eq. 11-13, Table 1-2). Critique : 3 couches de 10 ReLU ; acteur : 3 couches de 20 ReLU + tanh (§3.2.2). Entraînement : 500 épisodes d'un jour (96 pas), perturbations multipliées par κ ~ U(0,7 ; 1,3) (§3.2.2).
- Indicateur économique EPI = revenu à la récolte (1,8 + 16 × poids Hfl/m2) moins coûts d'énergie et de CO2 (Eq. 14, Table 3). Météo réelle de la serre Venlow Energy, Bleiswijk, pas de 5 min rééchantillonné (§4).

## Plateforme et implémentation

Simulation seule, aucune serre réelle ni matériel embarqué. Puce / carte : n/r. Puissance mesurée : n/r (l'énergie est un terme de coût simulé). Code et modèle entraîné : non publiés (aucun lien dans le texte). Temps de calcul rapportés sans machine ni méthode de mesure : n/r (Table 5).

## Résultats

- 3 jours (288 échantillons) : EPI MPC 1,843 Hfl/m2 contre RL 1,788 (§4.3, Table 5). Le RL produit un peu plus de laitue mais consomme plus d'énergie et injecte beaucoup plus de CO2, y compris la nuit ; le MPC ventile plus efficacement (§4.3).
- Cycle complet de 40 jours : EPI MPC 2,504 contre RL 2,195, avec une production du RL nettement plus haute (Fig. 8, texte).
- Temps de calcul : MPC 305,04 s contre RL 2,36 s (Table 5) ; l'unité de référence (par simulation entière ou autre) n'est pas précisée.
- Le RL tolère davantage la contrainte d'humidité, ce qui peut être un risque sanitaire pour la culture (§4.3). Température mieux tenue par le RL, humidité mieux tenue par le MPC (Fig. 6).
- Réglage « raccourci » : ventilation au maximum sans CO2 ni chauffage donne un EPI de 1,894, mais avec température et humidité dangereuses pour les laitues (§5) : l'EPI seul est un mauvais juge.
- Table 6 : liste qualitative des pour/contre (MPC : besoin d'un bon modèle, contraintes faciles, faible adaptabilité ; RL : possible sans modèle, contraintes difficiles, forte adaptabilité).
→ reportés dans `benchmarks.csv` (lignes proposées, 4 : MPC et DDPG sur 3 jours et sur 40 jours, métrique EPI en Hfl/m2). Les temps de calcul n'ont pas de ligne (pas de plateforme ni de protocole). Confiance `medium` : Table 5 est « sans corps extrait » côté tableaux (corps lu depuis le texte extrait par Grobid, colonnes jointes sur une ligne) et les valeurs 40 jours sont en texte.

## Limites et critique

- Un seul scénario météo de 3 jours pour la comparaison principale, une seule graine d'entraînement et une seule valeur de gamma : pas de variance ni de test statistique (§4). Le RL est réglé « par essais pour ressembler au MPC » (§3.2.1) ; le MPC n'est pas non plus comparé à un contrôleur à règles ni à un PID, donc pas de baseline simple.
- Écart de comparaison : le RL reçoit une récompense recodée (accroissement de matière sèche plutôt que cumul, §3.2.1), et ses contraintes sont de simples pénalités ; la comparaison par EPI n'est pas la fonction optimisée par l'agent. Le RL dispose seulement de la météo courante, le MPC de prévisions sur l'horizon (§5, piste 1) : le MPC est donc avantagé sur l'information, c'est écrit à demi par les auteurs.
- Le RL « sous-optimal » par exploration du CO2 (§4.3) : les auteurs ne savent pas si l'agent a convergé (§5). Le MPC est résolu en 305 s mais sans précision sur la machine ni l'unité : le gain de 130x est invérifiable.
- Table 6 est un jugement qualitatif des auteurs, non démontré par les expériences. Le sens de « Difficulty to handle constraints » pour le RL est cohérent avec les violations d'humidité observées.
- La section 3.2.2 et la fin du §3 sont tronquées dans le texte extrait (Table 1 sans corps, phrase d'entraînement interrompue) ; hyperparamètres complets non lus.
- Incohérence mineure : la Table 6 dit que le MPC « optimise un modèle quadratique convexe » alors que le MPC décrit est non linéaire (déduit : coquille ou approximation).
- Simulation uniquement, aucun test sur une serre réelle ni sur du matériel embarqué ; pas de latence d'inférence ni de coût edge.

## Pertinence pour la thèse

Axe `climate-control` du projet SerreIA, qui utilise un contrôleur à règles avec prévision GRU. Ce papier donne des arguments de choix : MPC meilleur en rentabilité et en respect des contraintes dures (humidité), RL beaucoup moins coûteux en calcul en ligne (utile sur un RPi 5) mais difficile à garantir (contraintes non strictes, convergence incertaine). C'est un argument en faveur de garde-fous et d'une validation humaine autour d'un RL ou d'un contrôleur appris, donc du principe de l'agent à actions validées. Les consignes de température jour/nuit (10-15 / 15-20 °C, §3.1.3) sont propres à la laitue de ce modèle, pas une référence de pratique de culture. Le papier ne traite ni pH/EC, ni vision, ni IoT, ni capteurs réels.

## Gaps identifiés

- Aucune comparaison MPC / RL / règles (type SerreIA) sur une serre réelle ou en matériel-dans-la-boucle.
- Pas de RL avec contraintes dures ou « safe RL » ; RL avec prévisions météo en entrée (piste des auteurs) non testé ici.
- Coût d'inférence sur edge (RPi, Hailo) du MPC et du RL : n/r.
- Comparaison avec d'autres algorithmes RL (TD3, PPO, SAC) et MPC+RL hybride : proposée par les auteurs, non faite.

## Statut de lecture

Papier complet (fulltext.md lu en entier ; extraction Grobid, `ok: true`). Réserves d'extraction : Tables 1, 3, 4, 5 listées « sans corps extrait » ; leurs valeurs sont celles lisibles dans le texte extrait, certaines (Table 1, N_s de la Table 4) manquent ; texte coupé en §3.2.2.
Ce qui suit est déduit et non affirmé par les auteurs : l'avantage informationnel du MPC (prévisions) ; l'absence de baseline à règles ; la coquille « quadratic convex » ; l'inférence que le facteur 130 sur le temps de calcul ne se transpose pas à un RPi ; l'absence de code publié (aucun lien trouvé dans le texte extrait).
