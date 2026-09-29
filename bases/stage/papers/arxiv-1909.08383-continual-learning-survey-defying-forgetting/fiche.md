---
id: arxiv-1909.08383-continual-learning-survey-defying-forgetting
fiche: done
date: 2026-09-29
---

# A Continual Learning Survey: Defying Forgetting in Classification Tasks

Matthias De Lange, Rahaf Aljundi, Marc Masana, Sarah Parisot, Xu Jia, Ale\vs Leonardis, Gregory Slabaugh, Tinne Tuytelaars, 2021, IEEE Transactions on Pattern Analysis and Machine Intelligence. https://doi.org/10.1109/TPAMI.2021.3057446
Type : article de journal

## Problème

Pas de consensus sur les protocoles expérimentaux du CL ni de comparaison exhaustive ; les
hyperparamètres de stabilité/plasticité sont souvent réglés par grid search sur les données de
toutes les tâches, ce qui viole l'hypothèse même du CL (§1, §4).

## Méthode

- **Taxonomie** en trois familles (§3, Fig. 1) :
  - *Replay* : rehearsal (iCaRL, ER, CoPE), pseudo-rehearsal (génératif), optimisation
    contrainte (GEM, A-GEM, GSS) ;
  - *Regularization-based* : data-focused (distillation : LwF, LFL, EBLL, DMC) et prior-focused
    (EWC, IMM, SI, R-EWC, MAS, Riemannian Walk) ;
  - *Parameter isolation* : réseau fixe masqué (PackNet, PathNet, Piggyback, HAT) ou
    architecture dynamique (PNN, Expert Gate…).
- Cadre des scénarios : task-, class- et domain-incremental, data-incremental (§2).
- **Cadre de choix des hyperparamètres continu** : recherche du learning rate donnant la
  plasticité maximale sur la nouvelle tâche (fine-tuning), puis décroissance de la stabilité
  (facteur α = 0,5) jusqu'à rester à moins de p = 20 % de cette précision (§4, Alg. 1).
- Comparaison de **11 méthodes + 4 baselines** en task-incremental multi-head : Tiny ImageNet
  (10 tâches équilibrées, modèles VGG SMALL/BASE/WIDE/DEEP), iNaturalist (10 super-catégories
  déséquilibrées, AlexNet pré-entraîné), RecogSeq (8 jeux très différents) ; effets de la
  capacité, du dropout et du weight decay, de l'ordre des tâches (§6).
- Budget de rejeu calé sur la taille du modèle BASE (4,5 k exemplaires), c.-à-d. la mémoire des
  importances d'EWC/SI/MAS (§6.1).

## Plateforme et implémentation

PyTorch, GPU (heatmap relative, Table 9) ; pas de plateforme embarquée. Code publié (lien en
note non extrait) (§1).

## Résultats

- Tiny ImageNet, modèle BASE, précision moyenne (oubli moyen) : fine-tuning 21,30 (26,90) ;
  joint 55,70 ; **PackNet 49,13 (0,00)** ; iCaRL 47,27 (−1,11) ; **MAS 46,90 (1,58)** ;
  EBLL 45,34 (1,44) ; GEM 45,13 (4,96) ; HAT 43,57 (0,00) ; **EWC 42,43 (7,51)** ; LwF 41,91
  (3,08) ; mode-IMM 36,89 (0,98) ; **SI 33,93 (15,77)** (Table 4, Fig. 2).
- EWC est la seule méthode qui gagne à un **petit modèle** (SMALL : 45,13 (0,86)) et se dégrade
  sur WIDE (31,10) ; SI souffre de sur-apprentissage (annexe B.2) (Table 4, §6.3).
- Modèles trop profonds défavorables ; WIDE ≈ +11 % en moyenne à nombre de paramètres de
  feature extractor égal (§6.3).
- Dropout aide surtout le fine-tuning, PackNet et SI mais augmente l'oubli ; weight decay et
  dropout interfèrent avec EWC et MAS (§6.4).
- Meilleures précisions (Tiny ImageNet / iNaturalist / RecogSeq) : PackNet 55,96 / 60,61 /
  64,88 ; MAS 48,98 / 54,59 / 45,72 ; EWC 45,13 / 54,02 / 42,01 ; SI 43,74 / 51,77 / 43,40 ;
  LwF 48,11 / 48,02 / 30,59 (Table 10). LwF s'effondre sous fort décalage de distribution.
- L'ordre des tâches a un effet négligeable (§6.6).
- Coûts relatifs (Table 9) : stockage EWC et MAS 2·M, SI 3·M, iCaRL M + R, GEM T·M + R,
  PackNet T·M bits ; temps d'entraînement GEM ×10,66, iCaRL ×5,63 ; inférence iCaRL ×45,61.

→ reportés dans `benchmarks.csv` : aucune ligne — survey (règle `/paper-fiche`), même si les
auteurs mènent leurs propres expériences comparatives ; les chiffres clés sont ci-dessus.

## Limites et critique

- Uniquement **task-incremental multi-head** (oracle de tâche) ; les auteurs reconnaissent que
  c'est le cadre le plus facile (§1, §7).
- Classification d'images seulement ; aucun coût embarqué (seulement une heatmap GPU relative).
- Le cadre d'hyperparamètres suppose un seuil p et un facteur α eux-mêmes fixés à la main.

## Pertinence pour la thèse

Survey de référence du stage (chapitre état de l'art) : taxonomie reprise, et surtout une
comparaison équitable qui place **EWC en dessous de MAS**, mais **favorisé par les petits
modèles** — précisément le régime d'un MCU. La Table 9 donne le coût mémoire des méthodes par
régularisation (2·M pour EWC et MAS, 3·M pour SI), argument chiffré pour les choisir face au
rejeu quand la RAM est comptée (déduit).

## Gaps identifiés

- Aucune évaluation en class-incremental, en régression ou sur séries temporelles.
- Aucune mesure sur plateforme contrainte ni en précision réduite.

## Statut de lecture

Papier complet (`fulltext.md` lu en entier, annexes A-B). Tables 6, 11-20 absentes ou réduites
à leur légende ; figures non chiffrées ; §7 (desiderata) partiellement tronquée.
Déduit et non affirmé par les auteurs : pertinence du régime « petit modèle » pour le MCU.
