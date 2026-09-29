---
id: arxiv-2302.00487-comprehensive-survey-continual-learning-theory
fiche: done
date: 2026-09-29
---

# A Comprehensive Survey of Continual Learning: Theory, Method and Application

Zifeng Wang, Zizhao Zhang, Sayna Ebrahimi, Ruoxi Sun, Han Zhang, Chen-Yu Lee, Xiaoqi Yin, Guolong Su, Long Zhao, Tomas Pfister, 2023, IEEE Transactions on Pattern Analysis and Machine Intelligence. https://arxiv.org/abs/2302.00487
Type : article de journal

## Problème

Relier en une seule synthèse les réglages, les fondements théoriques, les méthodes et les
applications de l'apprentissage continu, les surveys existants étant soit anciens, soit
partiels (§1). Objectif général formulé par les auteurs : un bon compromis
stabilité ↔ plasticité et une généralisation intra- et inter-tâches suffisante, sous
contrainte d'efficacité des ressources (Abstract).

## Méthode

- **Scénarios** formalisés (Table 1, §2.2) : instance-, domain-, task-, class-incremental
  (IIL, DIL, TIL, CIL), task-free (TFCL), online (OCL), frontières floues (BBCL), pré-entraînement
  continu (CPT) ; variantes few-shot, semi- et non supervisées.
- **Métriques** (§2.3) : précision moyenne AA et incrémentale moyenne AIA ; stabilité par
  forgetting measure FM et BWT ; plasticité par intransience IM et FWT (éq. 1-7).
- **Théorie** (§3) : inférence bayésienne séquentielle ; approximation de Laplace en ligne
  (Hessien ≈ matrice d'information de Fisher, diagonale ou Kronecker) qui fonde EWC (éq. 8-12) ;
  inférence variationnelle en ligne (VCL) ; projection de gradient (NCL) ; borne de
  dégradation ½ λ_max ‖Δθ‖² liant oubli, **platitude du minimum** et écart entre tâches
  (éq. 19-23).
- **Taxonomie en cinq familles** (§4, Fig. 3) : régularisation (poids : EWC, SI, MAS, RWalk ; 
  fonction : LwF, distillation), rejeu (expérience, génératif, de features), optimisation
  (projection de gradient GEM/A-GEM/OGD/GPM, méta-apprentissage, minima plats),
  représentation (auto-supervision, pré-entraînement, prompts), architecture (allocation de
  paramètres, décomposition, réseaux modulaires).
- Applications (§5-6) : classification (CIL, few-shot, général), détection, segmentation,
  génération conditionnelle, RL, NLP ; au-delà de la performance (efficacité, apprentissage
  fédéré, désapprentissage, robustesse).

## Plateforme et implémentation

Survey sans expérience propre ni plateforme (n/r).

## Résultats

Pas de résultats expérimentaux propres. Constats de synthèse :
- les mesures d'importance de SI, MAS et RWalk reviennent toutes à approximer le Fisher
  (§4.1, réf. [34]) ;
- régularisation et rejeu agissent au final sur la direction du gradient (§3.1, §4.3) ;
- les représentations auto-supervisées ou pré-entraînées oublient moins, en lien avec des
  minima plus plats (§4.3-4.4) ;
- réseaux plus larges plus robustes ; la batch-norm biaise les moments vers la tâche courante
  (§4.5) ;
- tendance récente : passer de la seule stabilité à la plasticité et à la généralisation (§7.1).

→ reportés dans `benchmarks.csv` : aucune ligne (survey).

## Limites et critique

- Très large (500+ références) mais centré sur la vision et le NLP ; les séries temporelles, la
  maintenance prédictive et l'embarqué sont absents (hormis l'efficacité en §6.6).
- Aucune comparaison chiffrée entre familles : il faut revenir à De Lange 2021 pour des
  résultats homogènes.
- Section théorique extraite avec des formules partiellement illisibles.

## Pertinence pour la thèse

Second survey de référence du stage : il fournit le **vocabulaire des scénarios** (le cas
maintenance prédictive relève surtout du domain-incremental ou du task-free, déduit), les
**métriques FM/BWT/FWT/IM** à reporter, et la justification bayésienne d'EWC (Laplace +
Fisher). La borne ½ λ_max‖Δθ‖² éclaire l'intérêt de pénaliser les déplacements de poids dans
les directions de forte courbure, ce que fait EWC (déduit).

## Gaps identifiés

- CL sur séries temporelles industrielles et sous contrainte matérielle : non couvert.
- Pas de discussion de la précision numérique (quantification) des méthodes de CL.

## Statut de lecture

Papier complet (`fulltext.md` lu en entier). Section 3 (théorie) parcourue avec des lignes
tronquées à l'affichage et des formules mal extraites ; Tables 1-3 partiellement extraites.
Déduit et non affirmé par les auteurs : classement du cas PdM en DIL/TFCL ; lecture de la borne
pour EWC.
