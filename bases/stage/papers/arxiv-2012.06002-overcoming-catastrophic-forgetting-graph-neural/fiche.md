---
id: arxiv-2012.06002-overcoming-catastrophic-forgetting-graph-neural
fiche: done
date: 2026-09-29
---

# Overcoming Catastrophic Forgetting in Graph Neural Networks

Huihui Liu, Yiding Yang, Xinchao Wang, 2020, arXiv preprint. https://arxiv.org/abs/2012.06002
Type : preprint non relu par les pairs (version arXiv)

> Ne pas confondre avec Kirkpatrick et al. 2017, « Overcoming catastrophic forgetting in neural
> networks » (EWC, `arxiv-1612.00796`) : les deux titres ne diffèrent que d'un mot, et cet article
> avait d'abord reçu par erreur les métadonnées d'EWC à l'ingestion.

## Problème

Les méthodes de CL ont été conçues pour des CNN sur données en grille. Les GNN oublient aussi,
et appliquer EWC nœud par nœud ignore la topologie : sur Corafull avec un GAT, EWC perd 7,48 %
de précision sur la tâche 1 après la tâche 3 (§Introduction, Fig. 1).

## Méthode

**TWP (Topology-aware Weight Preserving)**, régularisation par importance des poids, en module
adaptable à tout GNN (§Method) :

- **Importance « perte »** : |∂L/∂w|, comme SI (Eq. 3).
- **Importance « topologie »** : |∂‖e‖²/∂w|, où e sont les coefficients d'attention de la
  couche intermédiaire, pour préserver la façon dont le GNN agrège ses voisins (Eq. 4-6).
- Importance finale I = λ_l·I_loss + λ_t·I_ts (Eq. 7) ; pénalité quadratique de type EWC
  cumulée sur les tâches passées, Σ I_n ⊗ (W − W*_n)² (Eq. 8).
- **Parcimonie** : pénalité L1 β‖I‖₁ sur les importances de la tâche courante, pour garder de
  la capacité aux tâches futures (Eq. 9).
- Pour les GNN sans attention (GCN, GIN), attention non paramétrique ajoutée pour le seul calcul
  des importances (Eq. 10, Fig. 3).
- Protocole : tâches disjointes par classes ; Corafull (9 tâches de 5 classes), Amazon
  Computers (5 × 2), PPI (12 × 10), Reddit (8 × 5), Tox21 (12 tâches binaires) ; métriques AP
  (précision moyenne) et AF (oubli moyen) ; 5 graines (§Experiments).

## Plateforme et implémentation

Matériel n/r. Aucune implémentation embarquée. Précision numérique : n/r.
Code publié : https://github.com/hhliu79/TWP (Abstract).

## Résultats

Backbone GAT, AP / AF (Table 1) :

| Jeu | Fine-tune | EWC | MAS | GEM | TWP | Joint |
|---|---|---|---|---|---|---|
| Corafull (précision) | 51,6 / 46,1 | 86,9 / 6,4 | 84,1 / 8,6 | 84,4 / 4,2 | **89,0 / 3,3** | 91,9 / 0,1 |
| Amazon Computers (précision) | 86,5 / 12,3 | 94,5 / 4,6 | 94,0 / 5,0 | 97,1 / 0,7 | **97,3 / 0,6** | 98,2 / 0,02 |
| PPI (micro-F1) | 0,365 / 0,178 | 0,826 / 0,142 | 0,749 / 0,092 | 0,741 / 0,112 | **0,853 / 0,086** | 0,931 / 0,035 |

- Backbone GCN, Corafull : TWP 87,8 / 2,9 contre EWC 84,5 / 7,1 et MAS 86,1 / 4,8 (Table 1).
- Tox21 (AUC), GAT : TWP 0,801 / 0,022 contre EWC 0,774 / 0,038 (Table 2).
- Ablation Corafull, GAT : importance « perte » seule (= EWC) 86,9 ; + topologie 88,6 ; + L1
  89,0 (Table 3).
- LwF est proche du fine-tuning sur les graphes ; EWC et MAS « work well » (§Node
  Classification Task).

→ reportés dans `benchmarks.csv` : 3 lignes (TWP : GAT sur Corafull, GCN sur Corafull, GAT sur
Tox21), `high`.

## Limites et critique

- Scénario task-incremental avec tâches disjointes par classes : le texte ne précise pas si
  l'identité de tâche est donnée au test (supplément absent) (déduit).
- λ_t, β choisis par jeu dans deux valeurs chacun (§Experimental Setup) ; hyperparamètres des
  baselines fixes (10 000 pour EWC et MAS) : réglage plus favorable à la méthode proposée.
- GEM stocke parfois tous les nœuds d'entraînement : comparaison mémoire non homogène.
- Matériel, temps et mémoire des importances non rapportés.

## Pertinence pour la thèse

Pertinence faible pour le domaine (graphes), utile pour la méthode : c'est une variante d'EWC où
l'importance d'un poids combine la sensibilité de la perte et celle d'une structure interne du
réseau (les attentions), plus une pénalité L1 qui garde de la capacité libre. Le premier terme
|∂L/∂w| est calculable sans matrice de Fisher, et la parcimonie des importances pourrait réduire
la mémoire d'un EWC sur MCU (déduit). La base le garde surtout comme référence de la bibliographie
du stage.

## Gaps identifiés

- Importances parcimonieuses (L1) pour réduire le stockage des importances d'EWC sur MCU :
  non évalué.
- Régularisation qui préserve une structure interne du réseau (et pas seulement la perte) pour
  les réseaux temporels (attention, récurrence) en PdM.

## Statut de lecture

Papier complet (`fulltext.md` lu en entier, supplément non inclus). Table 1 partiellement
désalignée (lignes GIN tronquées, en-têtes décalés) ; figure 2 extraite en fragments.
Déduit et non affirmé par les auteurs : scénario au test, intérêt pour EWC sur MCU.
