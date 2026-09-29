---
id: 2024-besnard-continual-learning-time-series-forecasting
fiche: done
date: 2026-09-29
---

# Continual Learning for Time Series Forecasting: A First Survey

Quentin Besnard, Nicolas Ragot, 2024, Engineering Proceedings (ITISE 2024). https://doi.org/10.3390/engproc2024068049
Type : conférence (actes publiés dans Engineering Proceedings, MDPI) — survey court

## Problème

Le CL est surtout étudié en classification ; pour la régression et la prévision de séries
temporelles, les travaux sont peu nombreux, dispersés par application et sans benchmark
commun (Abstract, §1, §3).

## Méthode

Survey narratif court (≈ 60 références), sans méthode bibliographique décrite :

- Rappel des principes : dilemme plasticité/stabilité, trois familles (rejeu,
  régularisation type EWC, extension d'architecture) et hybrides ; trois scénarios de van de
  Ven (task-, class-, domain-incremental) (§2).
- **Scénarios propres à la prévision** (d'après [38]) : incrémental sur le domaine des
  données (le processus générateur change) et sur le domaine cible (nombre ou propriétés des
  sorties, horizon) ; le task-incremental au sens de la classification n'est pas traité par
  la littérature de régression (§3.1).
- **Découpage des tâches** : la plupart des travaux coupent arbitrairement la série en
  blocs de taille fixe (« task-based ») ; peu d'approches *task-free* détectent les
  transitions, p. ex. par analyse de la perte ([47]) (§3.1).
- Domaines d'application recensés : énergie surtout, puis maintenance industrielle [36, 43],
  climat, trafic (§3.1).
- Analyse de résultats repris d'autres papiers : rejeu vs fine-tuning vs joint training
  ([24], Fig. 1) ; LwF, EWC, Online EWC, SI contre baseline en MSE et en taux d'oubli
  ([41], Fig. 2-3, Eq. 1) ; modèle CLeaR sur 10 parcs éoliens ([35], Tables 1-2) (§3.2).

## Plateforme et implémentation

Sans objet : aucune expérience propre.

## Résultats

Aucun résultat propre ; pas de ligne dans `benchmarks.csv` (survey). Chiffres repris de
[35] (CLeaR), cités pour mémoire :
- MSE moyenne (×10⁻²) sur 10 parcs éoliens : instance standard A 5,138 ; fine-tunée B
  5,442 ; CL (CLeaR) C 2,829 ; baseline 3,190 (Table 1).
- Taux d'oubli moyen : B 3,550 vs C 1,161 pour le prédicteur (Table 2).
- Sur données artificielles très périodiques, seuls 32,1 % des 1120 modèles CL battent le
  modèle standard (§3.2).

Définition du taux d'oubli utilisée (d'après [41]) : max(0, L₂ − L₁)/L₁, avec L₁ la MSE sur
le jeu de *warm-up* en fin de warm-up et L₂ la MSE sur ce même jeu après mise à jour
(Eq. 1).

## Limites et critique

- Survey très court et non systématique : pas de critères d'inclusion, pas de tableau de
  synthèse des travaux recensés.
- Les résultats présentés viennent de trois papiers seulement, avec des métriques
  hétérogènes ; « in all presented application cases, even the lowest performances still
  surpass those of standard baseline models » (§3.1) est contredit par les 32,1 % de [35]
  sur données périodiques (§3.2).
- La maintenance industrielle n'est citée que par deux références, sans détail.
- Aucune mention des contraintes embarquées (MCU, quantification) ; la consommation de
  ressources n'apparaît qu'en perspective (§3.3, §4).

## Pertinence pour la thèse

Utile pour situer le problème du stage (régression / pronostic sur séries temporelles) par
rapport au CL dominant en classification : il nomme les scénarios « data domain » et
« target domain » incremental (§3.1), signale que le découpage arbitraire en tâches est la
norme et plaide pour des approches task-free — ce qui rejoint l'idée d'un détecteur de
dérive qui déclenche la mise à jour. Il fournit une définition simple du taux d'oubli en
régression (Eq. 1), réutilisable (déduit).

## Gaps identifiés

- Pas de benchmark commun de CL pour la prévision / régression de séries temporelles (§3.3).
- Peu d'approches task-free en régression ; détection de transition de tâche peu étudiée
  (§3.1, §3.3).
- Métriques de coût (CPU, mémoire, énergie) des stratégies CL absentes (§3.3).

## Statut de lecture

Papier complet (`fulltext.md` lu en entier). Tables 1 et 2 (reprises de [35]) partiellement
extraites ; figures non disponibles.
Déduit et non affirmé par les auteurs : la contradiction entre §3.1 et §3.2, le lien avec la
détection de dérive déclenchant la mise à jour.
