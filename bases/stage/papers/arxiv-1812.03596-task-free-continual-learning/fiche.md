---
id: arxiv-1812.03596-task-free-continual-learning
fiche: done
date: 2026-09-29
---

# Task-Free Continual Learning

Rahaf Aljundi, Klaas Kelchtermans, Tinne Tuytelaars, 2018, arXiv preprint. https://arxiv.org/abs/1812.03596
Type : preprint non relu par les pairs (version arXiv ; seule cette version est dans la base)

## Problème

Les méthodes de CL supposent des tâches séparées, aux frontières connues, pendant lesquelles
les données sont i.i.d. ; la consolidation (mise à jour des importances) se fait en fin de
tâche. En pratique, les données arrivent en flux non i.i.d., avec des dérives graduelles ou
brutales et sans frontière annoncée (Abstract, §1).

## Méthode

Version en ligne, sans tâche, de **MAS** (Memory Aware Synapses) (§3, Alg. 1) :

- **Pourquoi MAS** : stockage fixe (une importance par paramètre), indépendant de la tâche
  (fonctionne avec une sortie d'embedding, sans têtes multiples), une seule passe arrière
  pour les importances (§3).
- **Quand consolider** : fenêtre glissante sur les pertes ; mise à jour des importances Ω
  quand la moyenne et la variance de la fenêtre passent sous des seuils (**plateau**) ;
  nouvelle recherche de plateau seulement après un **pic** (moyenne de fenêtre > μ + σ du
  plateau précédent) (§3, Fig. 1).
- **Sur quelles données** : un petit **buffer de cas difficiles** (les échantillons de plus
  forte perte parmi les nouveaux et le buffer), 30 à 100 éléments, sert à la fois au rejeu et
  à l'estimation de Ω (§3, Table 1).
- **Comment cumuler** : moyenne mobile cumulée des Ω pour éviter l'explosion des gradients
  (une moyenne décroissante est testée en ablation) (§3, §4.2.3).
- Objectif : L(X) + L(X_B) + λ/2 Σ Ω_i (θ_i − θ*_i)² (Eq. 5).
- Hyperparamètres (Table 1) : fenêtre de pertes 5 ; seuils moyenne 0,3-0,5 et variance
  0,02-0,1 ; λ = 100 (AlexNet) ou 0,5 (Tiny v2).

Applications : reconnaissance d'acteurs en séries TV (AlexNet pré-entraîné, perte triplet,
embedding de taille 100 ; supervision faible ou auto-supervision) (§4.2) ; évitement de
collisions monoculaire en simulation Gazebo (drone Hector, 4 puis 10 couloirs) et sur
Turtlebot réel, par imitation d'un expert laser (§4.3, §4.4, §8, §9).

## Plateforme et implémentation

- Entraînement sur PC (matériel n/r) ; robot réel Turtlebot dont le calculateur embarqué
  n'est pas décrit (§4.4, §9).
- Réseau « Tiny v2 » pour l'évitement de collisions : 2 couches conv + 2 FC, entrée 128×128
  (§4.3, Fig. 8) ; taille mémoire n/r.
- Précision numérique, latence, énergie : n/r. Code : non publié (n/r dans le texte).

## Résultats

Résultats donnés surtout en figures ; valeurs chiffrées du texte :
- Séries TV, supervision faible : la baseline en ligne gagne 20 % sur le modèle initial
  puis décline après le 3ᵉ épisode ; la méthode atteint la précision de l'entraînement joint
  en ligne i.i.d. et reste à 8 % de l'entraînement joint hors ligne (BBT, §4.2.1, Fig. 3a).
  Sur Breaking Bad : « up to a 100% improvement » sur la baseline en ligne (§4.2.1, Fig. 3b).
- Ablation : sans buffer de cas difficiles ou avec Ω en moyenne décroissante, plus de
  fluctuations et d'oubli (§4.2.3, Fig. 3c).
- 10 couloirs simulés : précision totale ≈ 80 % avec CL contre ≈ 70 % en ligne sans CL ;
  +15 à 20 % par couloir quand la tâche est apprise (§8, Fig. 10, 13).
- Turtlebot : moins de collisions par pas d'entraînement avec CL ; rouler tout droit donne
  0,6 collision par pas (§9, Fig. 7, 11).
- Le CL ralentit l'adaptation quand les nouvelles données sont plus informatives que les
  anciennes ; l'effet est d'autant plus grand que le flux s'éloigne de l'i.i.d. (§5).

→ reportés dans `benchmarks.csv` : 1 ligne (10 couloirs simulés, précision totale, §8,
`medium` : valeur approchée donnée dans le texte).

## Limites et critique

- Évaluation presque entièrement graphique ; pas de tableau de résultats, pas de métrique
  d'oubli (BWT) ni de comparaison à d'autres méthodes de CL (EWC, GEM, rejeu seul) : seules
  des baselines « online » sans régularisation et des bornes joint training.
- Le buffer de cas difficiles est lui-même un rejeu : la part de MAS et celle du rejeu ne sont
  séparées qu'en ablation qualitative (Fig. 3c).
- Seuils de plateau sensibles et réglés sur le premier épisode (§4.2, §10) ; les auteurs
  reconnaissent qu'ils conditionnent tout le comportement.
- Pas de mesure de coût (mémoire du buffer et de Ω, temps) malgré la motivation « online ».

## Pertinence pour la thèse

Référence clé pour le volet « détection de dérive → mise à jour » : le détecteur plateau/pic
sur la perte est un mécanisme simple, sans tâche, qui décide quand recalculer les importances
d'un régularisateur type EWC/MAS. Transposable sur MCU : il ne demande qu'une fenêtre de
5 pertes et deux seuils, et MAS a un stockage fixe (un Ω par poids) (déduit). Il montre aussi
qu'un buffer de 30 à 100 échantillons stabilise l'apprentissage en ligne, taille compatible
avec quelques ko de RAM pour des fenêtres de capteurs (déduit).

## Gaps identifiés

- Détecteur de plateau/pic comparé à des détecteurs de dérive statistiques (Page-Hinkley,
  ADWIN, DDM) pour déclencher la consolidation : non fait.
- Online EWC/MAS task-free sur séries temporelles de capteurs et sur MCU : non testé.
- Métriques d'oubli normalisées en scénario task-free.

## Statut de lecture

Papier complet, suppléments compris (`fulltext.md` lu en entier). Sections du supplément mal
numérotées à l'extraction ; figures non disponibles (résultats majoritairement graphiques).
Déduit et non affirmé par les auteurs : transposition MCU (coût d'une fenêtre de pertes, taille
de buffer), lien avec les détecteurs de dérive statistiques.
