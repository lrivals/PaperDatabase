---
id: arxiv-2409.12789-reinforcement-learning-model-predictive-control
fiche: done
date: 2026-11-03
---

# Reinforcement Learning-based Model Predictive Control for Greenhouse Climate Control

Samuel Mallick, Filippo Airaldi, Azita Dabiri, Congcong Sun, Bart De Schutter, 2024, arXiv preprint (DOI indiqué dans metadata : 10.1016/j.atech.2024.100751, à vérifier). https://arxiv.org/abs/2409.12789
Type : preprint non relu par les pairs

## Problème

Le MPC de serre dépend d'un modèle de prédiction inexact (erreurs de modèle, prévisions météo), ce qui dégrade la performance et provoque des violations de contraintes climatiques (CO₂, T°, humidité) (§1). Les MPC robustes/stochastiques existants sont conservateurs (baisse de rendement) ou coûteux en calcul ; le RL profond (DDPG) n'offre ni garantie de contraintes ni interprétabilité (§1).

## Méthode

- Cadre « MPC comme approximateur de politique et de fonction de valeur » en RL (§2.2, d'après [9]) : le MPC paramétré par θ fournit π_θ et Q_θ (éq. 22, 28-30).
- Paramètres appris : coûts (offset, poids du gain de masse sèche, pénalité d'entrée, pénalité de violation, coût terminal) et les 28 paramètres du modèle de prédiction θ_p (Table 3, Table 4).
- Apprentissage en ligne par Q-learning LSTD du second ordre avec tampon de rejeu et QP borné (§4.3, éq. 31-33) ; exploration induite seulement par les perturbations météo (Remark 2).
- Cas d'étude : serre de laitue (modèle de [28], 4 états, 3 entrées : injection CO₂, ventilation, chauffage), pas de 15 min, cycle de 40 jours = 3840 pas (§2.1, §3). Contraintes de sortie : CO₂ ≤ 1,6 ‰, T° 10-15 °C (nuit) / 15-20 °C (jour, seuil de rayonnement 10 W m⁻²), HR ≤ 70 % (éq. 11-12) ; entrées max (1,2 ; 7,5 ; 150) (éq. 13).
- Solveurs : CasADi + IPOPT (§5). Horizon N = 24 (§5.2). Apprentissage : γ = 0,99, α = 0,1, mise à jour par cycle, 5 % max (§5.3).

## Plateforme et implémentation

Simulation uniquement (pas de matériel ni de serre réelle). CPU, fréquence, OS : n/r. Puissance : n/r. Code publié : non mentionné dans le texte lu. Météo : données réelles de la serre Venlow Energy, Bleiswijk (Pays-Bas), 40 jours, rééchantillonnées à 15 min, perturbées par du bruit brownien pour chaque épisode (§5.1).

## Résultats

Comparaison sur 100 cycles d'évaluation (Fig. 6, barres moyenne ± écart type, valeurs numériques non données dans le texte, donc non reprises ici) contre I-MPC (modèle exact), N-MPC (modèle faux, paramètres tirés à ±20 %), R-MPC-n (MPC robuste par échantillons, [4]) et DDPG (§5.2-5.3) :
- Violations Ψ : MPC-RL les réduit le plus, proche de I-MPC ; R-MPC reste insatisfaisant ; DDPG améliore N/R-MPC mais moins que MPC-RL (§5.3, Fig. 6). Pendant l'entraînement les violations tendent vers zéro en 100 cycles ; CO₂ jamais violé et HR dépassée rarement au dernier cycle (§5.3, Fig. 3-4).
- Rendement : N-MPC et R-MPC-5 donnent un rendement très élevé mais irréaliste (croissance modélisée irréaliste quand CO₂ et humidité sont trop hauts) ; R-MPC avec plus d'échantillons perd du rendement par conservatisme ; MPC-RL limite cette perte ; DDPG dépasse même I-MPC en rendement (§5.3).
- Profit P : DDPG sous-performe I-MPC et MPC-RL (rendement obtenu de façon peu efficace en intrants) (§5.3).
- Coût d'étape L_ep : MPC-RL meilleur que DDPG (§5.3).
- Temps de calcul moyen par pas (Table 7) : I-MPC 0,0378 s ; N-MPC 0,0390 s ; R-MPC-5/10/20 0,229 / 0,570 / 1,234 s ; MPC-RL entraînement 0,0793 s, évaluation 0,0430 s ; DDPG 0,000155 s. Matériel non précisé.
→ reportés dans `benchmarks.csv` : 8 lignes proposées (temps de calcul, Table 7, chunk 2409.12789#029.0, confidence medium car corps de tableau extrait en vrac). Aucune ligne de précision/rendement : valeurs seulement en figure.

## Limites et critique

- Simulation seule ; l'environnement « réel » est le même modèle que celui du MPC (structure exacte, seuls les paramètres sont incertains, ±20 %) ; pas de validation en serre réelle (cité en travaux futurs, §6). Estimation d'état supposée parfaite (§2.1).
- Le rendement de N-MPC / R-MPC-5 est gonflé par une dynamique non réaliste hors contraintes : la comparaison de rendement n'a de sens qu'avec Ψ (le papier le dit, §5.3).
- Pas de valeurs numériques en texte ; résultats en barres d'erreur (Fig. 6), donc non reproductibles par tableau. Trois graines seulement pour les approches RL (§5.3).
- Temps de calcul sans matériel : non comparable à d'autres papiers. Entraînement coûte deux optimisations par pas (§4.3).
- Horizon, coefficients de coût et hyper-paramètres du DDPG repris de [22] : équité de la comparaison non discutée (déduit).
- Code non mentionné ; preprint.

## Pertinence pour la thèse

Pertinence pour SerreIA, axe climate-control (MPC/RL) : montre une voie intermédiaire entre contrôleur à règles et RL boîte noire, avec contraintes explicites, interprétabilité et calcul léger, utile pour envisager une évolution du contrôleur à règles. Cultures : laitue, ce qui recoupe la cible hydroponique, mais seulement CO₂/T°/HR/chauffage/ventilation, sans pH/EC, éclairage ni VPD. Les plages de contraintes (T° 10-15 / 15-20 °C, HR ≤ 70 %, CO₂ ≤ 1,6 ‰) viennent de la littérature néerlandaise de simulation, pas de consignes de culture validées (déduit). Non applicable tel quel à un RPi/ESP32 : coûts de calcul mesurés sur un matériel inconnu. Laisse ouvert : validation réelle, modèle de serre alternatif, humain dans la boucle.

## Gaps identifiés

- Aucune validation de MPC appris par RL sur une serre réelle ni sur matériel embarqué (RPi).
- Pas de lien entre contraintes de contrôle apprises et consignes de culture sourcées par espèce/stade.
- Modèle sans irradiance artificielle, pH/EC, ni risque maladie (humectation foliaire).

## Statut de lecture

papier complet (`fulltext.md` lu en entier ; extraction grobid ok). Tableau 5 listé « sans corps extrait » dans les warnings (le texte en donne tout de même les valeurs en fragments) ; Table 7 extrait en vrac (valeurs lues dans l'ordre des colonnes, à vérifier) ; annexe du modèle (Table 8, équations) illisible, non exploitée. Figures 3-8 non lisibles en texte : valeurs de Fig. 6 non relevées.
Déduit et non affirmé par les auteurs : l'équité de la comparaison avec DDPG, l'origine des plages de contraintes, l'inadaptation à l'embarqué, l'absence de code (simplement non mentionné).
