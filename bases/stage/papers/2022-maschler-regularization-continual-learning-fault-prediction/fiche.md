---
id: 2022-maschler-regularization-continual-learning-fault-prediction
fiche: done
date: 2026-09-29
---

# Regularization-based Continual Learning for Fault Prediction in Lithium-Ion Batteries

Benjamin Maschler, Sophia Tatiyosyan, Michael Weyrich, 2022, Procedia CIRP 112, 513–518. https://doi.org/10.1016/j.procir.2022.09.091
Type : article de journal (actes de conférence CIRP publiés dans Procedia CIRP)

## Problème

Les modèles data-driven de pronostic de batteries Li-ion marchent sur le processus exact
qu'ils ont vu, mais s'adaptent mal quand les conditions d'usage ou d'environnement changent ;
les jeux de données sont petits, hétérogènes et souvent confidentiels (§1, §2.2). Les
auteurs testent si la régularisation (EWC, Online EWC, SI) permet d'apprendre en séquence
sur plusieurs groupes de batteries sans oublier ni partager de données brutes (§2.2).

## Méthode

- **Choix de la régularisation** : le rejeu exige de partager des données et les approches
  architecturales visent des tâches peu liées ; la régularisation convient à des tâches
  proches sans échange de données (§2.2, Fig. 1).
- **Entrées** : 21 features conçues à la main par cycle (10 en charge, 11 en décharge),
  comme dans [10] (§3).
- **Modèle** : LSTM multicouche, hyperparamètres optimisés (Fig. 2, Table 1) ; 1 couche de
  150 nœuds en régression, 2 couches de 100 nœuds et dropout 0,1 en classification (Table 1).
- **RUL → classes** : EWC, Online EWC et SI demandent des vraisemblances de classification,
  donc la RUL est discrétisée en trois classes d'état de santé : safe (RUL > 60), okay
  (30 < RUL ≤ 60), at risk (RUL ≤ 30) (§3, Table 2).
- **Scénario CL** : chaque groupe expérimental = une tâche ; ordre 1, 7, 4, 9 ; 100 époques
  par tâche ; 80/20 aléatoire par groupe ; baseline sans régularisation ; moyennes sur
  5 runs (§4.3). Les auteurs le qualifient d'« incremental task learning scenario » (§4).
  Hyperparamètres des régularisations : trois valeurs (500 000, 2, 200) dont les noms de
  paramètres sont perdus à l'extraction (Table 1).

## Plateforme et implémentation

- Entraînement sur PC : AMD Ryzen Threadripper 2920X + NVIDIA GeForce RTX 2080 8 Go,
  Ubuntu 20.04, PyTorch 1.6 (§4). Aucune exécution embarquée.
- Précision numérique : n/r (FP32 vraisemblable, non dit). Mémoire, latence, énergie : n/r.
- Données : jeu ouvert de dégradation de 34 batteries en groupes de 3-4 ; groupes retenus
  1 (batteries 5, 6, 7, 18), 4 (33, 34, 36), 7 (45-48), 9 (53-56), les autres écartés pour
  fin de vie manquante ou mesures erronées (§4.1). Il s'agit du jeu batteries de la NASA
  (déduit : même source [11] que le FC-AE comparé et numérotation des cellules ; le nom
  n'apparaît pas dans le texte extrait).
- Code : non publié.

## Résultats

**Régression RUL, groupe 1 seul** (Table 3, §4.2) :

| Cas | FC-AE [10] | LSTM proposé |
|---|---|---|
| 1 : batteries 5, 6 → test 7 | 11,8 % RMSE | 4,81 % RMSE (≈ 9,1 cycles) |
| 2 : 5, 6, 7 mélangées, 80/20 | – | 2,15 % RMSE (≈ 2,5 cycles) |

**CL sur 4 tâches**, précision moyenne sur les 20 dernières époques de la tâche 4 (Table 4) :

| Méthode | Meilleure tâche | Moyenne | Pire tâche |
|---|---|---|---|
| Sans régularisation | 0,72 | 0,54 | 0,38 |
| EWC | 0,70 | 0,63 | 0,51 |
| Online EWC | 0,82 | 0,70 | 0,60 |
| SI | 0,70 | 0,52 | 0,41 |

- Online EWC est le meilleur sur la moyenne et la pire tâche ; SI fait moins bien que
  l'absence de régularisation en moyenne (Table 4).
- La précision maximale sur la tâche en cours décroît au fil des tâches (Online EWC : 0,95
  sur la tâche 1 → 0,61 sur la tâche 4), ce qui fait douter du passage à plus de tâches
  (§4.3).
- Forte dépendance aux tâches : les groupes 1 et 4 se renforcent mutuellement ; le groupe 7
  provoque un oubli marqué des tâches 1 et 3, même avec régularisation (§4.3).

→ reportés dans `benchmarks.csv` : 6 lignes — 2 en régression RUL (Table 3, cas 1 et 2) et
4 en CL (Table 4 : sans régularisation, EWC, Online EWC, SI ; métrique = précision moyenne
sur les 4 tâches).

## Limites et critique

- **Pas de BWT ni de FWT** : seules précision moyenne, meilleure et pire tâche sont
  données ; l'oubli n'est lu que sur les courbes (Fig. 5).
- Un seul ordre de tâches ; les auteurs reconnaissent ne pas savoir si l'effet vient de la
  similarité des tâches ou de leur position (§5). Hyperparamètres optimisés sur Online EWC
  seulement, puis appliqués aux autres méthodes (§3) : **comparaison biaisée en faveur
  d'Online EWC**.
- La régression RUL devient une classification à 3 classes pour pouvoir régulariser :
  la tâche CL n'est plus un pronostic RUL continu.
- Pas de baseline « joint training » (borne haute) ni de méthode de rejeu.
- Très petit jeu (quelques centaines de cycles par condition, §4.1) ; 5 runs mais sans
  écart-type publié.
- La comparaison au FC-AE [10] (Table 3) n'utilise pas forcément les mêmes features ni le
  même découpage (déduit).
- Aucune contrainte embarquée évaluée alors que l'argument initial est la décentralisation.

## Pertinence pour la thèse

Référence directe pour le choix de la famille « régularisation » en PdM : premier comparatif
EWC / Online EWC / SI sur un problème industriel de séries temporelles (§2.2), cité à ce titre
par Hurtado 2023 (§6.1). Il fournit un protocole reproductible (tâches = conditions
d'usage) et un résultat utile (Online EWC > EWC > SI), mais sur GPU, en FP32 et sans
métrique d'oubli normalisée : la question de ces régularisations sur MCU en INT8 reste
entière (déduit).

## Gaps identifiés

- Régularisation CL pour la RUL en régression, sans discrétisation en classes.
- Effet de l'ordre des tâches non étudié (un seul ordre).
- Pas de BWT/FWT ni de borne joint training en CL-PdM.
- Aucune évaluation embarquée (mémoire de la matrice de Fisher, INT8).

## Statut de lecture

Papier complet (`fulltext.md` lu en entier). Les équations 1 à 3 et les noms des
hyperparamètres de régularisation (Table 1) sont illisibles à l'extraction ; un passage de
§4.3 sur SI est tronqué. Fig. 5 (courbes) non disponible.
Déduit et non affirmé par les auteurs : identité NASA du jeu de batteries, FP32, biais de
l'optimisation des hyperparamètres, non-comparabilité avec [10].
