---
id: 2004-gama-learning-drift-detection
fiche: done
date: 2026-09-29
---

# Learning with Drift Detection

João Gama, Pedro Medas, Gladys Castillo, Pedro Rodrigues, 2004, Advances in Artificial Intelligence - SBIA 2004 (LNAI 3171), 286-295. https://doi.org/10.1007/978-3-540-28645-5_29
Type : conférence (SBIA 2004, Springer LNAI)

## Problème

En apprentissage en ligne, la distribution des exemples change dans le temps (dérive de concept,
abrupte ou graduelle). Les fenêtres de taille fixe ou les pondérations par âge imposent un
compromis entre réactivité et stabilité ; les méthodes adaptatives existantes (FLORA, Klinkenberg)
demandent beaucoup de paramètres (§1, §2). Les auteurs cherchent une méthode directe pour détecter
les changements de contexte et ne réapprendre que sur les données pertinentes.

## Méthode

**DDM (Drift Detection Method)** (§3) :

- L'erreur en ligne du classifieur est vue comme une suite de tirages de Bernoulli : au pas i, taux
  d'erreur p_i et écart-type s_i = √(p_i(1 − p_i)/i) ; approximation normale pour n > 30.
- On mémorise p_min et s_min au point où p_i + s_i est minimal.
- **Alerte** (warning, confiance 95 %) si p_i + s_i ≥ p_min + 2·s_min ; **dérive** (99 %) si
  p_i + s_i ≥ p_min + 3·s_min.
- À la dérive, un nouveau contexte est déclaré à partir de l'exemple k_w (première alerte) et un
  nouveau modèle est appris sur les exemples de k_w à k_d ; une alerte suivie d'une baisse de
  l'erreur est traitée comme une fausse alarme (Fig. 1).
- Indépendant de l'apprenant : utilisable dans un algorithme incrémental ou comme wrapper d'un
  apprenant batch.
- Évaluation : perceptron, réseau de neurones et arbre de décision sur 8 jeux artificiels
  (STAGGER, SINE1/2, SINIRREL1/2, MIXED, GAUSS, CIRCLES) et sur ELEC2 (marché de l'électricité de
  Nouvelle-Galles du Sud, 45 312 exemples) ; ADULT pour tester les fausses alarmes (§4).

## Plateforme et implémentation

PC ; CART de R pour ELEC2 (§4.3). Mémoire : deux registres (p_min, s_min) et un compteur ; coût
O(1) par exemple (déduit de §3). Code : non publié.

## Résultats

- **Jeux artificiels**, erreur finale sans / avec détection (Table 1) : le réseau de neurones passe
  de 0,351 à 0,002 (STAGGER) et de 0,489 à 0,019 (SINE1) ; l'arbre de décision de 0,490 à 0,081
  (SINE1) ; le perceptron gagne peu (0,126 → 0,115 sur SINE1), voire perd sur MIXED (0,100 → 0,111).
- **ELEC2**, arbre de décision (Table 2) :

| Test | Meilleur segment (a posteriori) | Toutes les données | Dernière année | DDM |
|---|---|---|---|---|
| Dernier jour | 0,104 | 0,187 | 0,125 | **0,104** |
| Dernière semaine | 0,190 | 0,235 | 0,247 | **0,199** |

- Sur ADULT (concept stable), aucune dérive détectée : pas de fausse alarme (§4.3).

→ reportés dans `benchmarks.csv` : 3 lignes (DDM + arbre de décision sur ELEC2 dernier jour et
dernière semaine, Table 2 ; DDM + réseau de neurones sur SINE1, Table 1), métrique = taux d'erreur
en %, `high`.

## Limites et critique

- **Supervisé** : DDM exige le label de chaque exemple pour calculer l'erreur ; inapplicable sans
  retour terrain.
- Détecte mal les dérives graduelles lentes (l'erreur monte peu) — limite qui motivera EDDM
  (Baena-García 2006, dans la base) (déduit).
- Stratégie « oublier et réapprendre » : le modèle précédent est jeté, pas de conservation de
  l'ancien concept.
- Évaluation surtout graphique (Fig. 2-3) ; pas de délai de détection ni de taux de fausses alarmes
  chiffrés sur les jeux artificiels ; résultats d'un seul run.
- Terminologie inversée en Table 2 : « lower bound » désigne la meilleure erreur (obtenue en
  regardant le test), « upper bound » les heuristiques.

## Pertinence pour la thèse

Référence fondatrice du volet détection de dérive, citée par Hurtado 2023 (§3.2) : DDM est le
détecteur le plus simple à embarquer (deux registres, quelques opérations par échantillon), et son
couple alerte / dérive fournit un mécanisme naturel pour déclencher une mise à jour sur MCU. Pour la
PdM, son besoin de labels le limite aux cas où l'erreur de prédiction est observable a posteriori
(par exemple une erreur de RUL constatée à la maintenance) ; sinon, un détecteur sur les entrées ou
sur l'erreur de reconstruction s'impose (déduit). Il suggère l'extension à la régression par la MSE
(§5), non détaillée.

## Gaps identifiés

- DDM en régression (MSE) pour la RUL : annoncé (§5), non documenté ici.
- DDM déclenchant une consolidation (EWC) plutôt qu'une réinitialisation.
- Délai de détection et fausses alarmes de DDM sur séries de capteurs industriels.

## Statut de lecture

Papier complet (`fulltext.md` lu en entier). Description des jeux artificiels (§4.1) en partie
tronquée ; figures non disponibles.
Déduit et non affirmé par les auteurs : coût O(1), faiblesse sur dérive graduelle, usage en PdM.
