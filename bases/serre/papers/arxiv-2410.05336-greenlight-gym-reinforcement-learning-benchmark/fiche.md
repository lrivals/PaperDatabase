---
id: arxiv-2410.05336-greenlight-gym-reinforcement-learning-benchmark
fiche: done
date: 2026-11-03
---

# GreenLight-Gym: Reinforcement learning benchmark environment for control of greenhouse production systems

Bart Van Laatum, Eldert J Van Henten, Sjoerd Boersma, 2024, IFAC-PapersOnLine 59 (23), (2025), 437-442. https://doi.org/10.1016/j.ifacol.2025.11.827 (arXiv 2410.05336)
Type : article de conférence IFAC (version arXiv v1 2024 ; `venue` d'après le `journal_ref` d'arXiv, non revérifié sur le site de l'éditeur)

## Problème

Il n'existe pas d'environnement de simulation standardisé pour comparer des contrôleurs par apprentissage par renforcement (RL) en production sous serre. Les modèles simplifiés ne reflètent pas les serres high-tech, KASPRO est fidèle mais fermé, et les modèles open source fidèles sont trop lents pour entraîner du RL et peu flexibles pour diversifier les données d'entraînement (§1).

## Méthode

- Réimplémentation du modèle GreenLight (Katzin et al., 2020) en C++ avec CasADi (différentiation automatique, compilation JIT en C), sous forme d'espace d'état discret `x_{k+1}=f(x_k,u_k,d_k,p)` avec 28 états, 8 entrées commandables, 10 perturbations, 208 paramètres (§2.1, éq. 1). Pas de temps 300 s (§4.1).
- Wrapper Python modulaire de type Gym : modules météo, paramètres, modèle d'observation (Table 1), récompense (§2.2).
- Contrôleurs : PPO et SAC via Stable Baselines3 (hyperparamètres : Table 2) et contrôleur à règles de référence dérivé de Katzin et al. 2021 (lampes, CO2 < 800 ppm, consignes chauffage 19,5 °C jour / 16,5 °C nuit, aération si T > consigne + 5 °C ou HR > 85 %, écrans ; §2.3).
- Récompense = EPI (revenu des fruits moins coûts CO2, chaudière, lampes) moins pénalités linéaires de contraintes (T 15-34 °C, CO2 300-1600 ppm, HR 50-85 %), éq. 5-7 et §4.2.
- Expérience : 60 jours de simulation, 28 paramètres de culture randomisés à chaque pas par `p = mu(1+eps)`, `eps ~ U(-delta, delta)`, 7 niveaux de delta de 0 à 30 % (§3.1, §4.2). Chaque contrôleur évalué sur 30 runs.

## Plateforme et implémentation

Pas de cible embarquée : simulation sur un poste de bureau avec CPU Intel Xeon W-2133 à 12 coeurs (jusqu'à 3,6 GHz) (§4.1). Aucune puissance mesurée (`n/r`). Réseaux PPO/SAC : MLP à 3 couches cachées (acteur 256 nœuds, critique 512), activation SiLU, 2 M de pas (Table 2, §4.2). Code : « open source » (résumé), mais la validation contre le Matlab d'origine est « available upon request » (§5.1) ; lien du dépôt non donné dans le texte extrait (note de bas de page non reprise) : `n/r`.

## Résultats

- Vitesse : plus de 1800 pas de simulation par seconde sur un coeur CPU, soit ~24x (GL-Matlab) et ~17x (GL-Python) ; plus d'un million de points en moins de dix minutes (§5.1). Les vitesses absolues des deux autres implémentations ne sont pas données dans le texte (`n/r`).
- RL : PPO et SAC surpassent le contrôleur à règles sur toute la plage d'incertitude (Fig. 2). Le baseline à règles part d'environ -5 EUR/m2 d'EPI et se dégrade ; PPO et SAC restent nettement positifs (§5.2). Les pénalités de contraintes de PPO/SAC varient peu avec l'incertitude, celles du baseline sont nettement plus élevées (§5.2). Une incertitude jusqu'à 10 % améliore les trois contrôleurs (Fig. 2, texte). Les valeurs numériques de Fig. 2 ne sont pas extraites : aucune ligne dans `benchmarks.csv`.
- Les RL apprennent à minimiser l'éclairage d'appoint, trop coûteux en électricité (§5.2).
→ reportés dans `benchmarks.csv` : 1 ligne proposée (vitesse de simulation, §5.1, `2410.05336#011.0`, confidence medium ; `fps` = pas/s, métrique non comparable à des FPS de perception, `platform_class: server`). Les résultats RL ne sont pas chiffrés dans le texte : aucune ligne.

## Limites et critique

- Météo unique et fixe (Schiphol, 1 mars-30 avril 2010) à l'entraînement comme au test : aucune généralisation mesurée (§4.2). Les auteurs eux-mêmes parlent de « limite supérieure » des performances (observations exactes, météo connue, dynamique simplifiée ; §5.2).
- Baseline à règles non réglé (les auteurs reconnaissent qu'un réglage le rendrait plus compétitif, §5.2) et pas de baseline MPC : la supériorité du RL est donc à nuancer.
- Seule l'incertitude paramétrique de culture est testée (pas capteurs, pas météo inconnue). Résultats en simulation uniquement, sans transfert à une serre réelle.
- La récompense peut être exploitée par un écart modèle-réel (ex. humidité extrême) : traité par des pénalités, mais l'EPI dépend des prix choisis (c_frt = 1,6, etc.; §4.2).
- Pas d'écart-type ni d'intervalle donné dans le texte (moyenne de 30 runs, Fig. 2 seule). Code « sur demande » pour la validation. Papier court (6 pages).
- Déduit (non affirmé) : un baseline PI/MPC ou un contrôleur de type Hortimax réel serait un comparatif plus juste.

## Pertinence pour la thèse

Axe `climate-control` (règles, MPC, RL). Pour SerreIA, dont le contrôleur est à règles : apporte un simulateur de serre à tomate rapide et open source pour tester des règles ou un RL avant déploiement, et un exemple de contrôleur à règles chiffré (consignes 19,5/16,5 °C, HR 85 %, CO2 800 ppm ; §2.3) utilisable comme repère de pratiques, mais pour une serre high-tech néerlandaise avec éclairage d'appoint, pas pour une serre à ESP32. Pas d'application à la vision, à l'edge ni à un agent LLM. Laisse ouvert la comparaison RL vs MPC vs règles réglées, et le transfert sim-réel.

## Gaps identifiés

- Comparaison RL / MPC / règles réglées sur le même simulateur (non faite ici).
- Généralisation à d'autres météos et climats, bruit de capteurs.
- Absence de validation sur serre réelle ; aucun lien avec un contrôleur à règles de petite serre à capteurs bas coût.
- Pas de cultures autres que la tomate (laitue hydroponique, basilic, fraise) ni de pH/EC dans ce modèle.

## Statut de lecture

papier complet (`fulltext.md` lu en entier, extraction grobid ok). Les corps des Tables 1 et 2 sont lisibles ; les éq. 8 et le détail des bornes sont partiellement tronqués dans l'extraction (texte de §4.2 morcelé) et Fig. 2 n'a que sa légende : valeurs de RL non lisibles. Déduit et non affirmé par les auteurs : l'appréciation « baseline faible » (les auteurs disent seulement qu'un réglage le rendrait plus compétitif), la pertinence pour SerreIA, la remarque sur MPC/PI.
