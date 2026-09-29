---
id: arxiv-1902.00829-incremental-learning-maximum-entropy-regularization
fiche: done
date: 2026-09-29
---

# Incremental Learning with Maximum Entropy Regularization: Rethinking Forgetting and Intransigence

Dahyun Kim, Jihwan Bae, Yeonsik Jo, Jonghyun Choi, 2019, arXiv preprint. https://arxiv.org/abs/1902.00829
Type : preprint non relu par les pairs

## Problème

En apprentissage incrémental par classes, le modèle souffre à la fois d'**oubli** et
d'**intransigeance** (incapacité à apprendre les nouvelles classes). Les étiquettes douces
transmises par distillation deviennent incertaines au fil des tâches, et le déséquilibre
anciennes/nouvelles classes pousse au surapprentissage sur les nouvelles (§1). Les métriques
F et I de Chaudhry et al. (2018), fondées sur des différences de précision, confondent oubli
et simple confusion entre classes proches (§3.1).

## Méthode

**MEDIC** = MER + DOS, sur une base distillation + mémoire d'exemples (§3) :

- **MER (Maximum Entropy Regularizer)** : la perte de distillation devient CE(p_k, q) − H(q),
  ce qui pénalise un ajustement trop confiant à des étiquettes douces incertaines (Eq. 3).
- **DOS (DropOut Sampling)** : à chaque mini-batch, exclusion aléatoire d'échantillons des
  nouvelles classes en début d'entraînement, puis de ceux à forte entropie croisée
  (curriculum auto-rythmé) ; réduit le déséquilibre de classes (§3, Alg. 1).
- Mémoire d'exemples tirés au hasard (2000 sur CIFAR100, 1000 en budget réduit, 4000 sur
  TinyImageNet) et *balanced fine-tuning* de Castro et al. (§3, §4.1).
- **Nouvelles métriques Sample Dynamics** : SDF (part des échantillons que le modèle de
  référence classe dans les anciennes classes et que le modèle incrémental envoie vers les
  nouvelles) et SDI (symétrique), en ratios, plus leurs moyennes sur les tâches (Eq. 4-7).
- Protocole : DenseNet121, CIFAR100 en 10 tâches de 10 classes, TinyImageNet en 10 tâches
  de 20 classes, 3 ordres aléatoires + ordres « meilleur d'abord » et « pire d'abord »
  (§4.1).

## Plateforme et implémentation

Matériel d'entraînement n/r. Aucune implémentation embarquée. Précision numérique, mémoire,
latence : n/r. Code : non publié (n/r dans le texte).

## Résultats

Précision moyenne sur les tâches 1-10 (%), classe-incrémental :

| Configuration | MEDIC | EndToEnd | EWC + mémoire | Baseline |
|---|---|---|---|---|
| CIFAR100, ordres aléatoires, mémoire 2000 (Table 2) | 72,51 ± 0,17 | 66,56 | 64,75 | 62,64 |
| CIFAR100, meilleur d'abord (Table 2) | 83,80 | 82,16 | 72,70 | 70,24 |
| CIFAR100, pire d'abord (Table 2) | 63,33 | 55,86 | 50,52 | 44,72 |
| CIFAR100, mémoire 1000 (Table 3) | 69,54 ± 0,44 | 62,73 | 56,63 | 52,49 |
| TinyImageNet, mémoire 4000 (Table 4) | 49,88 ± 0,38 | 45,55 | 43,92 | 42,37 |

- Ablation CIFAR100 (Table 1) : sans MER ni DOS 68,32 ; sans DOS 70,07 ; sans MER 69,65 ;
  complet 72,51 ; SDF10 passe de 10,17 (baseline) à 5,05.
- F10 donne des résultats contre-intuitifs (la baseline sans distillation « oublie » moins
  qu'EndToEnd ou EWC), que SDF corrige (§4.3, §4.5).
- L'écart en faveur de MEDIC grandit quand la mémoire diminue (§4.4).

→ reportés dans `benchmarks.csv` : 3 lignes (MEDIC : CIFAR100 mémoire 2000 et 1000,
TinyImageNet), `medium` (lignes des Tables 2-3 mal alignées, Table 4 reconstruite par PyMuPDF).

## Limites et critique

- « EWC » est une extension des auteurs avec mémoire d'exemples (§4.3), pas l'EWC
  d'origine : la comparaison ne dit rien d'EWC seul.
- Les comparaisons SOTA se limitent à EndToEnd et EWC ; iCaRL, LUCIR et BiC sont absents.
- Les métriques SDF/SDI exigent un modèle de référence entraîné sur toutes les données
  vues : inutilisables en déploiement réel, et coûteuses en recherche.
- Le gain de MER est négatif à la tâche 2 (§4.2, Fig. 1).
- Matériel et temps de calcul non donnés.

## Pertinence pour la thèse

Pertinence indirecte : scénario classe-incrémental sur images, loin du pronostic sur séries
temporelles. Deux apports utiles au stage : (1) la critique des métriques d'oubli en
différence (F, I) au profit de ratios, à garder en tête pour évaluer un EWC sur MCU ;
(2) l'idée qu'une distillation doit tenir compte de l'incertitude des cibles, transposable
aux cibles de rejeu en régression (déduit). La régularisation par entropie ne coûte
presque rien en mémoire, un atout sur MCU (déduit).

## Gaps identifiés

- Métriques d'oubli relatives (ratios) pour la régression et la RUL : non définies.
- Effet d'un régularisateur d'entropie avec un budget mémoire de quelques dizaines
  d'exemples (ordre de grandeur MCU).

## Statut de lecture

Papier complet (`fulltext.md` lu en entier). Tables 1-3 partiellement désalignées à
l'extraction (valeurs des méthodes concurrentes reconstituées d'après l'ordre des colonnes,
à vérifier) ; Table 4 reconstruite par PyMuPDF ; Algorithme 1 tronqué.
Déduit et non affirmé par les auteurs : transposition à la régression et au MCU.
