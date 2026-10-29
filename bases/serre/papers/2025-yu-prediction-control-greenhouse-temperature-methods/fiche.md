---
id: 2025-yu-prediction-control-greenhouse-temperature-methods
fiche: done
date: 2026-10-29
benchmarks: none
---

# Prediction and control of greenhouse temperature: Methods, applications, and future directions

Jingxin Yu, Congcong Sun, Jinpeng Zhao, Lushun Ma, Wengang Zheng, Qiuju Xie, Xiaoming Wei, 2025, Computers and Electronics in Agriculture 237, 110603. https://doi.org/10.1016/j.compag.2025.110603
Type : article de journal (survey, relu par les pairs)

## Problème

Revue de la prédiction et de la commande de la température de serre par IA : les méthodes
traditionnelles (manuelles, mécaniques, hybrides) laissent des fluctuations allant jusqu'à
20 °C (2025-yu#027.0) ; les auteurs comparent modèles physiques, data-driven et hybrides, puis
lois de commande (flou, MPC, RL, systèmes intelligents) et dégagent des pistes
(2025-yu#000.0, 2025-yu#034.0).

## Méthode

Survey (Section 3 : méthodes traditionnelles et ML classique ; Section 4 : ANN, RNN/CNN/Transformer,
hybrides série / parallèle / hiérarchique ; Section 5 : commande). Pas de protocole expérimental
propre. Les tableaux 6 à 15 résument les travaux cités (entrées, horizon, performance).

## Plateforme et implémentation

n/r (revue). Aucun code ni bitstream publié. Un seul point de calcul embarqué : l'ELM est dit
« efficace en calcul et adapté aux appareils à ressources limitées » (2025-yu#012.0), sans mesure.

## Résultats

Chiffres de synthèse rapportés par les auteurs (non mesurés par eux) :
- Deep learning : RMSE typique 0,3 à 1,3 °C, R² 0,96 à 0,99 ; hybrides : RMSE 0,2 à 0,8 °C,
  R² 0,97 à 0,99 (§4.4, 2025-yu#025.0).
- ML classique : RMSE 1,32 °C (RBF, Bolandnazar 2023) et 0,82 °C (RBF, Hosseini Monjezi 2023)
  (2025-yu#012.0).
- Entrées et horizons typiques (Table 6, 2025-yu#053.0) : GRU, 25 min, RMSE 0,5857 °C, R² 0,9848
  (Oh 2022) ; BiLSTM, 24 h à partir de 24 h, R² 0,78 à 0,81 ; LSTM, meilleur aux pas courts de 1 à 15 min.
- MPC : 30 % d'énergie économisée face à une commande par relais, température maintenue
  (Bersani 2021, 2025-yu#029.0).
- Hybrides : réduisent les besoins en données et améliorent l'interprétabilité, mais pondération
  parallèle délicate (instabilités en transition) et coût de calcul des architectures
  hiérarchiques (2025-yu#024.0).
- RL : espaces continus de grande dimension, exploration sûre difficile (2025-yu#031.2) ;
  pistes : RL basé modèle, comparaison RL / méthodes classiques, MPC+RL (2025-yu#033.0).
- Table 15 : flou = non-linéarités, MPC = précision et énergie, RL = adaptation (2025-yu#060.0).
→ reportés dans `benchmarks.csv` : aucune ligne (survey, chiffres des travaux cités).

## Limites et critique

Les RMSE agrégés mélangent serres, saisons, variables (T seule ou T/HR/CO2), pas de temps (1 min
à 24 h) et splits : non comparables entre eux. Pas de baseline simple (persistance, régression
linéaire) rapportée à côté des chiffres 0,3 à 1,3 °C ; or la persistance à 5 à 30 min est
difficile à battre (remarque déduite, non affirmée). Pas d'évaluation sur micro-contrôleur
ni sur petite serre : biais vers les serres commerciales et simulateurs. Les gains MPC
(30 %) viennent d'une seule étude, en comparaison à une commande par relais.

## Pour SerreIA

- Fichiers concernés : `edge/controller/rules.py` (hystérésis, `serre.yaml` : température 1,0),
  `forecast.py` (GRU prévue), `sim/`, docs/06 §4.
- Reprise concrète : (1) garder l'hystérésis comme niveau de sécurité et comme baseline ;
  la revue ne donne aucune valeur de réglage d'hystérésis ou de PID (n/r). (2) GRU : viser une
  prévision de T à 5 à 30 min à partir de T/HR/rayonnement extérieur, comme Oh 2022
  (GRU, 25 min, RMSE 0,5857 °C, 2025-yu#053.0) ; plage de référence 0,3 à 1,3 °C (2025-yu#025.0).
  (3) Un hybride bilan thermique simple + correcteur appris convient à une petite serre :
  moins de données, extrapolation plus fiable (2025-yu#024.0) ; à tester dans `sim/`.
  (4) MPC, puis RL, seulement après la GRU et en simulation ; le MPC n'est justifié que s'il bat
  l'hystérésis en énergie (30 % cité en 2025-yu#029.0, à ne pas supposer). RL : exploration non
  sûre sur système réel (2025-yu#031.2) ; l'agent LLM validé par un humain est déjà le garde-fou.
- Métrique de validation : RMSE/MAE de la GRU contre persistance et contre un modèle linéaire,
  par horizon ; énergie et temps hors plage contre hystérésis, sur `sim/` puis en serre.
- Pièges : ne pas comparer à ces RMSE sans même pas de temps ni même variables ; split
  temporel (pas aléatoire) ; saison d'entraînement différente du test.

## Gaps identifiés

- Aucune étude de commande de T sur micro-serre ou nœud embarqué (RPi/ESP32) : coût de calcul
  du MPC et de la GRU non mesuré.
- Pas de comparaison hystérésis / PID / MPC sur la même serre avec métriques énergie et
  dépassement.

## Statut de lecture

Sections lues par recherche ciblée (pdb search / show) : résumé, 1, 3.1.2, 4.1.2, 4.3.3, 4.4,
5.1, 5.3, 5.4, 5.6, 7, tables 6, 15 ; fulltext non lu en entier. Les sections 3.1.1, 4.2,
4.3.1, 5.2, 5.5, 6 et les tables 8 à 14 ne sont connues que par extraits.
Déduit et non affirmé par les auteurs : la remarque sur la persistance, la recommandation
pour SerreIA, l'ordre GRU puis MPC puis RL. Tableaux listés « sans corps extrait » (figure
sans légende) : chiffres éventuels manquants.
