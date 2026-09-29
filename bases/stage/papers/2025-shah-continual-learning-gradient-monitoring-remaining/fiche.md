---
id: 2025-shah-continual-learning-gradient-monitoring-remaining
fiche: done
date: 2026-09-29
---

# Continual learning by gradient monitoring for remaining useful lifetime estimation

Sayed Rafay Bin Shah, Andreas Schwung, 2025, Knowledge-Based Systems 323, 113721. https://doi.org/10.1016/j.knosys.2025.113721
Type : article de journal

## Problème

En RUL industrielle, les sous-jeux successifs (conditions opératoires, modes de défaut)
présentent une dérive de domaine ; réentraîner ou stocker les anciennes données coûte en
calcul et en stockage, et LwF accumule les erreurs quand la dérive est forte (§1, §2). Les
auteurs veulent un CL sans données anciennes, peu coûteux, pour la régression RUL.

## Méthode

- **Base LwF** : encodeur partagé (FC + Transformer encoder) et une tête MLP par tâche ;
  à chaque nouvelle tâche, 25 époques de *warmup* (seule la nouvelle tête apprend, les
  prédictions des anciennes têtes sont enregistrées comme cibles douces), puis entraînement
  joint avec perte de distillation RMSE (§3.2, §5.4, Fig. 1, Fig. 4).
- **Gradient Monitoring (GM)** sur l'encodeur partagé pendant l'entraînement joint (§3.3) :
  - matrice de critère par couche : |G/W| (GoW), |G·W| (GtW) ou |G| (Eq. 3-5) ;
  - masque binaire M = 1 si C ≥ k·mean(C) (seuil par couche, facteur k optimisé) (Eq. 6-7) ;
  - **VGM** : masque binaire recalculé à chaque pas, critère GoW ;
  - **MGM** : moyenne mobile exponentielle du masque, Z = βZ + (1−β)M, β ∈ [0,9 ; 0,99],
    critères GoW ou GtW (Eq. 9).
- **Analyse théorique** : borne de Taylor du 1er ordre sur l'oubli attendu ; masquer les
  gradients réduit la borne (Théorème 1), le momentum la réduit davantage (Théorème 2) (§4).
- **Protocoles** : C-MAPSS, chaque sous-jeu FD001-FD004 = une tâche, 4 ordres (« ablations »,
  Table 2) ; métrique : score asymétrique C-MAPSS (a1 = 13, a2 = 10, plus bas = mieux),
  RUL plafonnée à 120 (§5.2.1). Batteries NASA PCoE : 3 tâches (B5-7 → B18, B45-47 → B48,
  B53-55 → B56), RMSE sur la capacité (§5.2.2, Table 3).
- **Comparaisons** : Vanilla (fine-tuning), LwF, EWC (Fisher sur la perte RMSE, λ et taille
  d'échantillon en grille), OGD (stocke 50 moteurs par ancien sous-jeu C-MAPSS) ; même
  architecture Transformer-MLP pour tous (§5.4). Hyperparamètres par Optuna, 100 essais
  (§5.4).

## Plateforme et implémentation

- Entraînement sur GPU NVIDIA Quadro RTX 5000 (§5.4). Aucune exécution embarquée.
- Précision numérique, mémoire, latence, énergie : n/r.
- Coût théorique (Table 10) : GM ne stocke rien ; surcoût O(n_s + n_head·t), constant en t
  pour le masquage de l'encodeur ; EWC stocke la matrice de Fisher, OGD les gradients.
- Code : non publié.

## Résultats

**Batteries NASA, RMSE de capacité (plus bas = mieux)** :

| Mesure | Vanilla | LwF | EWC | OGD | VGM | MGM-GoW | MGM-GtW |
|---|---|---|---|---|---|---|---|
| Tâche 0 après tâche 2 (Table 29) | 0,079 | 0,106 | 0,139 | 0,077 | **0,024** | 0,065 | 0,058 |
| Tâche 1 après tâche 2 (Table 30) | 0,278 | 0,312 | 0,336 | 0,297 | 0,354 | **0,249** | 0,281 |
| Nouvelle tâche 2 (Table 28) | 0,079 | 0,146 | 0,139 | **0,077** | 0,114 | 0,090 | 0,096 |

**C-MAPSS, score de la tâche source après 3 nouvelles tâches (plus bas = mieux)** :

| Source (ordre) | Vanilla | LwF | EWC | OGD | VGM | MGM-GoW | MGM-GtW |
|---|---|---|---|---|---|---|---|
| FD001 (→ 004 → 002 → 003), Table 16 | 29 466 | 2281 | 1367 | **1261** | 2393 | 1907 | 1763 |
| FD002 (→ 004 → 001 → 003), Table 19 | 522 380 | 4466 | 10 948 | 6716 | 4895 | 4139 | **2335** |
| FD004 (→ 002 → 003 → 001), Table 25 | 133 820 | 3604 | 5826 | 4061 | 3313 | **2800** | 3928 |

- Sur les nouvelles tâches, Vanilla reste le meilleur la plupart du temps ; GM est ensuite
  meilleur que LwF/EWC/OGD dans la plupart des cas, avec de fortes dégradations ponctuelles
  (Δ jusqu'à −590 %, Table 13, tâche 3) (§5.7.2, Tables 12-15).
- MGM > VGM sur l'ancienne tâche dans presque toutes les ablations, en accord avec le
  Théorème 2 (§5.7.1, Fig. 5-7) ; mais VGM est bien meilleur que MGM sur les batteries
  (Table 29).
- EWC domine sur FD001 source (Table 16, tâches 2 et 3) ; OGD sur FD002→FD004 (Table 20).

→ reportés dans `benchmarks.csv` : 6 lignes pour les méthodes des auteurs — VGM, MGM-GoW,
MGM-GtW sur batteries (RMSE tâche 0 après tâche 2, Table 29) et sur C-MAPSS ablation 1
(score FD001 après 3 tâches, Table 16).

## Limites et critique

- **Scénario task-incremental avec une tête par tâche** : l'identité de la tâche est
  connue au test (§3.2) ; cas plus facile que le domain-incremental réaliste d'une machine
  qui dérive sans label de tâche.
- **Δ% incohérent** : il se dit calculé contre la meilleure méthode existante (§5.7), mais
  Table 29 donne +77,3 % pour VGM, ce qui correspond à EWC (0,066) et non à OGD (0,052,
  meilleure : ≈ +71 %) ; en ligne 2, +69,6 % correspond à Vanilla (0,079) (calcul déduit).
- Valeurs identiques entre Tables 28 et 29 à la ligne « tâche 2 » (Vanilla 0,079, EWC 0,139) :
  possible erreur de recopie (déduit).
- Résultats sur un run, sans écart-type ni graine rapportés.
- EWC est appliqué à tout le réseau avec une seule tête (Fisher sur la RMSE), alors que
  LwF et GM disposent de têtes par tâche : comparaison déséquilibrée (§5.4).
- Les théorèmes reposent sur une approximation de Taylor d'ordre 1 et sur « ignoring the
  first term » (‖∇L‖) (§4.1) ; la preuve qu'un masque réduit l'oubli est quasi tautologique
  (moins de mise à jour → moins de dérive des poids), sans lien avec la plasticité.
- Tables 7-9 (baselines supervisés) sans corps à l'extraction.
- Aucune évaluation de coût réel (temps, mémoire) ni embarquée ; Transformer peu adapté
  à un MCU (déduit).

## Pertinence pour la thèse

C'est le travail le plus récent et le plus complet de CL pour la RUL dans la base : il
compare EWC, LwF, OGD et une régularisation par masquage de gradients sur C-MAPSS et sur les
batteries NASA, avec des séquences de tâches proposées comme benchmark (§5.3). Il fournit un
point de comparaison direct pour EWC en régression RUL (Fisher sur la RMSE, sans
discrétisation, contrairement à Maschler 2022). Le masquage de gradients sans stockage
(Table 10) est intéressant pour un MCU, mais nécessite de calculer un critère par poids à
chaque pas : coût mémoire comparable à un second tenseur de gradients (déduit).

## Gaps identifiés

- CL-RUL en domain-incremental (sans identité de tâche au test) : non évalué.
- Coût mémoire et calcul réel du masquage de gradients et de la Fisher sur MCU, en INT8.
- Protocole statistique (plusieurs runs, écarts-types) pour les séquences C-MAPSS proposées.

## Statut de lecture

Papier complet (`fulltext.md` lu en entier). Tables 7-9 sans corps ; certaines lignes des
Tables 13-15 sont mal alignées à l'extraction (valeurs fusionnées) ; titres des Tables 20 et
22 tronqués ; équations partiellement illisibles.
Déduit et non affirmé par les auteurs : incohérence du Δ%, possible erreur de recopie
Tables 28/29, déséquilibre de la comparaison EWC, coût mémoire sur MCU.
