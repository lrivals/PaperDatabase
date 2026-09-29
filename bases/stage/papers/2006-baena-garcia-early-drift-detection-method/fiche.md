---
id: 2006-baena-garcia-early-drift-detection-method
fiche: done
date: 2026-09-29
---

# Early Drift Detection Method

Manuel Baena-García, José del Campo-Ávila, Raúl Fidalgo-Merino, Albert Bifet, Ricard Gavaldà, Rafael Morales-Bueno, 2006, Fourth International Workshop on Knowledge Discovery from Data Streams (IWKDDS), ECML PKDD 2006. DOI : aucun
Type : conférence (atelier)

## Problème

DDM (Gama 2004) détecte bien les dérives abruptes et graduelles rapides, mais réagit tard aux
**dérives graduelles lentes** : les exemples s'accumulent longtemps après l'alerte et la mémoire
peut déborder (§1, §3.1).

## Méthode

**EDDM (Early Drift Detection Method)** (§3.2) :

- Au lieu du taux d'erreur, EDDM suit la **distance entre deux erreurs de classification** (nombre
  d'exemples entre deux erreurs) : quand le modèle apprend, cette distance augmente ; quand le
  concept dérive, elle diminue.
- On calcule la moyenne p'_i et l'écart-type s'_i de cette distance, et l'on mémorise p'_max et
  s'_max au point où p'_i + 2·s'_i est maximal.
- Après **au moins 30 erreurs** : **alerte** si (p'_i + 2s'_i)/(p'_max + 2s'_max) < α = 0,95,
  **dérive** si ce rapport < β = 0,90 ; à la dérive, le modèle est réappris sur les exemples
  stockés depuis l'alerte, et p'_max, s'_max sont réinitialisés (§3.2).
- Wrapper autour d'un apprenant batch ou intégré dans un apprenant incrémental.
- Évaluation : J48 (C4.5), IB1 et NNge (Weka) sur 4 jeux artificiels (Circles, Gauss, Mixed, Sine1),
  un nouveau jeu à dérive graduelle très lente (Sine1g) et ELEC2 ; erreur prequential et nombre de
  dérives détectées, comparés à DDM (§4).

## Plateforme et implémentation

PC, Weka (§4). Mémoire : quelques registres (moyenne, écart-type, maximum) plus les exemples stockés
entre alerte et dérive. Code : non publié.

## Résultats

- **Dérive graduelle lente** (Sine1g, Table 2) : EDDM a une erreur prequential plus basse que DDM
  avec les trois apprenants (IB1 0,146 contre 0,211 ; J48 0,135 contre 0,152 ; NNge 0,210 contre
  0,233) et détecte beaucoup plus de dérives (28 à 50 contre 12).
- **ELEC2** (Table 3) : EDDM 0,143 à 0,159 d'erreur contre 0,211 à 0,276 pour DDM, avec 171 à 193
  dérives détectées contre 10 à 130.
- **Dérives abruptes** (Table 1) : résultats très proches de DDM (Sine1, Circles, Mixed) ; sur
  **Gauss (bruité)**, EDDM détecte 22 à 32 dérives contre 9 à 12 et son erreur est souvent un peu
  plus haute (J48 : 0,174 contre 0,153).

→ reportés dans `benchmarks.csv` : 2 lignes (EDDM + J48 sur ELEC2, Table 3 ; EDDM + IB1 sur Sine1g,
Table 2), métrique = erreur prequential en %, `high`.

## Limites et critique

- **Supervisé**, comme DDM : l'erreur de classification doit être connue à chaque exemple.
- Beaucoup plus de détections que DDM (jusqu'à 193 sur ELEC2) : sensibilité accrue, et donc
  davantage de fausses alarmes probables sur données bruitées (Gauss) ; aucun taux de fausses
  alarmes ni délai de détection n'est mesuré.
- α et β fixés empiriquement (§3.2) ; leur réglage automatique est laissé en perspective (§5).
- Section de description des jeux artificiels tronquée à l'extraction ; un seul run par
  configuration.

## Pertinence pour la thèse

Complément direct de DDM pour le volet détection de dérive : l'usure d'une machine produit des
dérives graduelles lentes, cas où EDDM réagit plus tôt que DDM (Sine1g). Son coût est aussi faible
que celui de DDM (compteur d'exemples entre erreurs, moyenne et variance incrémentales), donc
embarquable sur MCU (déduit). Sa sensibilité au bruit invite à filtrer les alarmes avant de
déclencher une mise à jour coûteuse (EWC, recalcul de la Fisher) (déduit).

## Gaps identifiés

- EDDM sur séries de capteurs de PdM (dérive lente par usure) et en régression : non évalué.
- Taux de fausses alarmes et délai de détection d'EDDM : non mesurés.
- Réglage automatique de α et β (§5).

## Statut de lecture

Papier complet (`fulltext.md` lu en entier). §4.1 (jeux artificiels) tronqué ; le seuil de dérive β
est reconstitué depuis un fragment déplacé ; figures non disponibles.
Déduit et non affirmé par les auteurs : faux positifs sur données bruitées, embarquabilité MCU,
pertinence pour l'usure.
