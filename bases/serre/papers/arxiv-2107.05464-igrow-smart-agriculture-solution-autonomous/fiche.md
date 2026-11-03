---
id: arxiv-2107.05464-igrow-smart-agriculture-solution-autonomous
fiche: done
date: 2026-11-03
---

# IGrow: A Smart Agriculture Solution to Autonomous Greenhouse Control

Xiaoyan Cao, Yao Yao, Lanqing Li, Wanpeng Zhang, Zhicheng An, Zhong Zhang, Li Xiao, Shihui Guo, Xiaoyu Cao, Meihong Wu, Dijun Luo, 2021, arXiv preprint. https://arxiv.org/abs/2107.05464 (pas de DOI)
Type : preprint non relu par les pairs

## Problème

Pas de solution IA mûre pour le contrôle de serre autonome (AGC) : décider, sur 3 à 5 mois, des consignes (température, CO₂, éclairage, irrigation) qui maximisent le rendement et minimisent les coûts, à partir de données multimodales coûteuses à collecter et de signaux épars (poids des fruits) (§1). Les simulateurs à règles simplifient trop, les simulateurs neuronaux existants ne couplent pas climat et croissance (§1).

## Méthode

- AGC formulé comme un MDP (§3) : état = météo extérieure, climat intérieur, état de croissance, rendement (14 variables observables) ; action = 4 consignes (température, CO₂, éclairage, irrigation) ; récompense = gain de culture moins coûts (énergie, main-d'œuvre) avec γ = 1 (§3.2).
- Simulateur neuronal en trois modules (climat horaire, croissance horaire, rendement journalier) avec mécanisme incrémental : fine-tuning sur les données réelles qui arrivent (§4.1, Fig. 2).
- Optimisation de stratégie par algorithme génétique élitiste (EGA) ou SAC (§4.2).
- Optimisation à deux niveaux en boucle fermée : stratégie ré-optimisée tous les K1 pas sur le dernier simulateur, simulateur recalibré tous les K2 pas (Algorithme 1, §4.3). Hyperparamètres et détails en annexe technique (non fournie ici : `n/r`).

## Plateforme et implémentation

Pas de matériel d'inférence embarqué décrit. Déploiement : capteurs et actionneurs de serre, plateforme cloud, commandes envoyées à distance par les producteurs ou un ordinateur central (§6.1). Serres de 667 m² à Liaoyang (Liaoning, Chine), tomate (§6.2). Puissance et latence d'inférence : `n/r`. Code et données annoncés « en matériel supplémentaire » (Résumé) ; lien non vérifié, à considérer comme non confirmé.

## Résultats

- Simulateur (Table 1, test sur 200 trajectoires virtuelles WUR) : R² global 0,911±0,009 (base, entraîné sur 1000 trajectoires virtuelles) et 0,906±0,046 (incrémental, 5 trajectoires réelles substituées) (§5.2). Par variable, base/incrémental : AirT 0,915/0,986 ; AirRH 0,707/0,941 ; AirCO₂ 0,930/0,988 ; PAR 1,000/1,000 ; LAI 0,927/0,669 ; PlantLoad 0,935/0,849 ; NetGrowth 0,959/0,939 ; FW 0,917/0,880 (Table 1). Sur la trajectoire réelle de l'équipe Automatoes, le simulateur à règles WUR reste le plus proche de la réalité ; les simulateurs neuronaux sont moins précis, le réel aide à calibrer (Fig. 3, §5.2).
- Optimisation en simulation : profit net +29,39 % (SAC) et +285,82 % (EGA) par rapport à la stratégie Automatoes ; seul EGA dépasse Automatoes en rendement ; EGA retenu pour le réel (Fig. 4, §5.3).
- Pilote réel 2find (mars-juil. 2020, 7 serres iGrow contre 2 serres d'experts) : rendement 12 223,90 ± 45 kg contre 11 097,60 ± 53 kg (+10,15 %, p = 8e-3) ; profit net 2 887,70 ± 183,45 contre 1 498,56 ± 10,03 (+92,70 %, p = 1e-4), par serre, unité monétaire notée « C » (symbole non extrait) ; coût énergie 50,11 contre 13,90 (−260,57 %) ; récolte terminée une semaine plus tôt (Table 2, §6.2). Premier pilote (oct. 2019 - mars 2020) : environ 500 de plus par serre, 2 serres contre 1, sans test statistique (§6.2).
- Baseline : planteurs experts humains (pilote), Automatoes et simulateur WUR (simulation).
→ reportés dans `benchmarks.csv` : 6 lignes proposées (R² base, R² incrémental, gains de profit net EGA et SAC en simulation, gains de profit net et de rendement du pilote réel) ; non écrites dans le CSV à ce stade (fichier du scratchpad, intégration par l'agent principal).

## Limites et critique

- Échantillon du pilote minuscule et déséquilibré (2 serres témoins) ; écarts-types du groupe témoin quasi nuls (±0,00 sur plusieurs lignes) car calculés sur peu de serres, ce qui rend les t-tests fragiles (déduit).
- Gain de profit net (+92,70 %) tiré en partie par une base de comparaison faible (1 498 par serre) et par le prix de vente plus élevé ; le papier attribue le prix à la qualité des fruits sans la mesurer directement (§6.2). Équipements amortis sur six ans, hypothèse propre aux auteurs (§6.1).
- Le simulateur neuronal est moins fidèle que WUR sur la trajectoire réelle (§5.2) et le gain simulé de +285,82 % n'est pas reproduit en réel ; l'écart simulation-réalité de l'optimisation n'est pas mesuré.
- Les auteurs invoquent le théorème central limite pour justifier la convergence du simulateur (§4.1) ; l'argument n'est pas rigoureux (jugement du relecteur).
- R² comparé aux données du simulateur WUR (virtuelles), pas à des mesures réelles pour l'essentiel.
- Pas de garde-fous, pas de validation humaine ni de contrainte de sécurité décrits ; pas de vision. Reproductibilité : annexes techniques et suppléments non disponibles dans le texte lu.

## Pertinence pour la thèse

Axes `iot-greenhouse` et `climate-control` du projet SerreIA. Apporte : une formulation MDP de la serre, un jumeau numérique neuronal incrémental, et la seule preuve réelle d'un gain par contrôle optimisé contre des experts (tomate), utile comme référence de ce qu'on peut espérer d'un contrôleur à règles plus prévision GRU. Laisse ouvert : comparaison à un contrôleur à règles/MPC (pas de baseline de ce type), hydroponie, pH/EC, sécurité des actions et validation humaine, coût de calcul sur un matériel léger (Raspberry Pi). Le cadre est industriel (serres chinoises à grande échelle), pas directement transposable à une serre ESP32 (déduit).

## Gaps identifiés

- Aucune comparaison de l'optimisation par simulateur à un contrôle MPC ou à règles bien réglé.
- Pas de garde-fous ni de validation humaine sur les consignes envoyées.
- Absence de lien entre contrôle et vision (maladies) dans la boucle.
- Pas de coût d'exécution (latence, matériel) pour la ré-optimisation.

## Statut de lecture

papier complet (fulltext.md lu en entier, backend grobid, `extraction.ok` vrai). Annexe technique et matériel supplémentaire (Tables S1/S2, hyperparamètres, Fig. S1-S13) absents du texte : non lus. Table 2 : légende signalée « sans corps extrait » dans les avertissements, mais le corps est présent dans le texte, avec des cellules fusionnées (Gains, Net Profit) ; valeurs recoupées avec le texte (+10,15 %, +92,70 %, +28,07 % cohérents entre eux) ; `confidence: medium`. Passage du §4.1 (module climat) tronqué à l'extraction. Déduit et non affirmé par les auteurs : fragilité des t-tests, base de comparaison faible, non-transposabilité à une serre ESP32, symbole « C » monétaire non résolu.
