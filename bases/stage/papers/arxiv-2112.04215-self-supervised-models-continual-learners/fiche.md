---
id: arxiv-2112.04215-self-supervised-models-continual-learners
fiche: done
date: 2026-09-29
---

# Self-Supervised Models are Continual Learners

Enrico Fini, Victor G Turrisi Da Costa, Xavier Alameda-Pineda, Elisa Ricci, Karteek Alahari, Julien Mairal, 2021, arXiv preprint. https://arxiv.org/abs/2112.04215
Type : preprint non relu par les pairs (version arXiv)

## Problème

Les méthodes auto-supervisées (SSL) donnent de bonnes représentations hors ligne, mais leur
qualité s'effondre quand les données arrivent en séquence ; réentraîner sur tout l'historique
est coûteux, surtout pour la SSL. Le CL auto-supervisé (CSSL) est peu étudié, et la plupart des
méthodes de CL reposent sur les labels (Abstract, §1, §2).

## Méthode

**CaSSLe** : la perte SSL elle-même sert de perte de distillation (§5, Fig. 2) :

- Au début de chaque tâche, copie gelée de l'encodeur f_{t−1}. Un **prédicteur** g (MLP à
  2 couches, 2048 neurones cachés) projette les features courantes vers l'espace des
  anciennes ; distillation L_D = L_SSL(g(z), z̄), avec z̄ = f_{t−1}(x) détaché (Eq. 4).
- Perte totale L_SSL(z_A, z_B) + L_SSL(g(z_A), z̄_A), **sans pondération** ni réglage
  d'hyperparamètre supplémentaire (Eq. 5).
- Compatible avec les pertes InfoNCE (SimCLR, MoCo), MSE (BYOL, SimSiam, VICReg), entropie
  croisée (SwAV, DINO) et corrélation croisée (Barlow Twins) (§5.1, Annexe B).
- Frontières de tâche supposées connues (§4). Évaluation par classifieur linéaire
  (task-agnostic en class- et data-incremental) ; A, oubli F, forward transfer T (§6.1).
- Protocole : ResNet18, CIFAR100 et ImageNet100 en 5 tâches (class- et data-incremental),
  DomainNet en 6 domaines ; comparaisons EWC (importances calculées avec la perte SSL), POD,
  Less-Forget, ER, DER (buffer 500), LUMP, Lin et al. (§6.1, Annexe C).

## Plateforme et implémentation

Bibliothèque solo-learn, optimiseur LARS, batch 256, 200 à 500 époques par tâche (§6.1).
Matériel n/r. CaSSLe coûte environ **+30 % de mémoire et de temps** d'entraînement (§7). Aucune
implémentation embarquée ; précision numérique n/r. Code publié :
github.com/DonkeyShot21/cassle (Abstract).

## Résultats

CIFAR100, 5 tâches class-incremental, précision linéaire A / oubli F (Table 2) :

| Stratégie | SimCLR | Barlow Twins | BYOL |
|---|---|---|---|
| Fine-tuning | 48,9 / 1,0 | 54,3 / 0,4 | 52,7 / 0,1 |
| EWC | 53,6 / 0,0 | 56,7 / 0,2 | 56,4 / 0,0 |
| ER (A seul) | 50,3 | 54,6 | 54,7 |
| DER (A seul) | 50,7 | 55,3 | 54,8 |
| Less-Forget (A seul) | 52,5 | 56,4 | 58,6 |
| POD (A seul) | 51,3 | 55,9 | 57,9 |
| **CaSSLe** | **58,3 / 0,2** | **60,4 / 0,4** | **62,2 / 0,0** |
| Offline | 65,8 | 70,9 | 70,5 |

- ImageNet100 class-incremental : Barlow Twins 63,1 → 68,2 avec CaSSLe, oubli 10,7 → 1,3
  (Table 4) ; gain moyen +6,8 points sur CIFAR100 et +4 sur ImageNet100 (§6.2).
- Data-incremental (ImageNet100) : +2 points en moyenne, sauf BYOL (74,0 → 73,3) ;
  domain-incremental (DomainNet) : +4,4 points en moyenne (Table 7).
- Le rejeu (ER, DER) n'aide pas en CSSL (surapprentissage du buffer rejoué pendant des
  centaines d'époques) ; **EWC « holds up surprisingly well »** avec des importances calculées
  sur la perte SSL (§6.2).
- Ablation : sans prédicteur, la performance chute (Table 6).

→ reportés dans `benchmarks.csv` : 3 lignes (CaSSLe : SimCLR et BYOL sur CIFAR100, Table 2 ;
Barlow Twins sur ImageNet100, Table 4), `high`.

## Limites et critique

- Frontières de tâche connues (§7) : pas de CL task-free.
- Les SSL oublient déjà peu en class-incremental sur CIFAR100 (F ≤ 1), donc le gain porte
  surtout sur la qualité des représentations, pas sur l'oubli (§6.2).
- Budget de calcul très élevé (centaines d'époques par tâche) ; +30 % mémoire et temps (§7).
- Baselines adaptées par les auteurs (EWC, POD, DER sans labels) avec un réglage limité à
  3-5 valeurs (Annexe C).
- Images seulement ; aucune série temporelle.

## Pertinence pour la thèse

Pertinence indirecte, deux enseignements utiles pour le stage : (1) EWC reste compétitif quand
ses importances sont calculées sur une perte non supervisée (ici la perte SSL), ce qui
justifie de calculer la Fisher sur une perte de reconstruction ou de prédiction quand les
labels de défaut manquent en PdM (déduit) ; (2) le rejeu peut échouer quand le buffer est rejoué
trop souvent (surapprentissage), point à surveiller avec un petit buffer sur MCU (déduit). Le coût
de CaSSLe (copie gelée du modèle, +30 %) le rend peu adapté à un MCU.

## Gaps identifiés

- CL auto-supervisé sur séries temporelles de capteurs sans labels de défaut.
- EWC avec Fisher calculée sur perte non supervisée en PdM : non testé.
- CSSL sans frontière de tâche.

## Statut de lecture

Papier complet, annexes comprises (`fulltext.md` lu en entier). Table 2 en partie désalignée
(ligne fine-tuning tronquée, complétée par Table 4) ; Tables 6 et A reconstruites par PyMuPDF ;
Table D tronquée.
Déduit et non affirmé par les auteurs : transposition à la PdM (Fisher non supervisée), risque de
surapprentissage d'un petit buffer sur MCU.
