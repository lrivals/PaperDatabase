---
id: arxiv-2401.01010-unsupervised-continual-anomaly-detection-contrastively
fiche: done
date: 2026-09-29
---

# Unsupervised Continual Anomaly Detection with Contrastively-learned Prompt

Jiaqi Liu, Kai Wu, Qiang Nie, Ying Chen, Bin-Bin Gao, Yong Liu, Jinbao Wang, Chengjie Wang, Feng Zheng, 2024, arXiv preprint. https://arxiv.org/abs/2401.01010
Type : preprint non relu par les pairs (version arXiv)

## Problème

En inspection industrielle, la détection d'anomalies non supervisée (UAD) entraîne un modèle
par classe de produit et suppose l'identité de classe connue au test ; entraîner en séquence un
modèle unifié provoque l'oubli, et les méthodes de CL reposent sur des labels. Seul DNE
combinait CL et UAD, sans segmentation (§Introduction).

## Méthode

**UCAD** : ViT pré-entraîné gelé (ViT-B/16, ImageNet-21K) + mémoire « clé-prompt-connaissance »
par tâche (§Methods, Fig. 2) :

- **Continual Prompting Module (CPM)** : pour chaque tâche, une **clé** (features de la
  5ᵉ couche ViT réduites à 196 patchs par *farthest point sampling*), des **prompts**
  apprenables ajoutés aux entrées des couches, et une **connaissance** (features « normales »
  réduites par coreset, comme PatchCore) (Eq. 1-2).
- **Inférence sans identité de tâche** : la tâche est choisie par la clé la plus proche,
  puis score d'anomalie = distance au plus proche voisin dans la connaissance de la tâche,
  repondérée par les voisins (Eq. 4-6) ; score image = max des patchs.
- **Structure-based Contrastive Learning (SCL)** : les masques de SAM servent de pseudo-
  labels de structure ; perte contrastive qui rapproche les patchs d'une même région (Eq. 3).
- Protocole : MVTec AD (15 classes) et VisA (12 classes) en tâches successives ; AUROC image,
  AUPR pixel, forgetting measure FM ; 14 méthodes UAD comparées, dont PatchCore et UniAD avec
  un buffer de rejeu de 100 images (§Experiments).

## Plateforme et implémentation

- Matériel n/r ; batch 8, Adam, 25 époques (Table 8, texte sous Table 4).
- Mémoire de la structure clé-prompt-connaissance : ≈ 23,19 Mo (Annexe « Methods ») ou
  23,28 Mo (texte sous Table 4), en float, pour 15 tâches maximum — chiffres et tailles de prompt
  (5 ou 7 couches) incohérents entre les deux passages.
- Précision numérique : float (n/r au-delà). Aucune implémentation embarquée.
- Code annoncé : https://github.com/shirowalker/UCAD (Abstract).

## Résultats

Moyenne après la dernière tâche (Tables 1, 3, 2, 4) :

| Méthode | MVTec AUROC image / FM | MVTec AUPR pixel | VisA AUROC image / FM | VisA AUPR pixel |
|---|---|---|---|---|
| PatchCore | 0,602 / 0,383 | 0,190 | 0,589 / 0,361 | 0,090 |
| UniAD | 0,774 / 0,229 | 0,086 | 0,639 / 0,297 | 0,080 |
| DNE | 0,870 / 0,116 | – | 0,610 / 0,179 | – |
| UniAD* (rejeu 100) | 0,904 / 0,076 | 0,393 | 0,825 / 0,125 | 0,283 |
| **UCAD** | **0,930 / 0,010** | **0,456** | **0,874 / 0,039** | **0,300** |

- Ablation : sans CPM ni SCL 0,693 (MVTec) ; CPM seul 0,894 (+20 points) ; + SCL 0,930
  (Table 5).
- Connaissance 4× plus grande : +0,8 point avec SCL, +3,5 sans (Table 6).
- Les couches intermédiaires du ViT (3-7) sont les meilleures (Table 7).

→ reportés dans `benchmarks.csv` : 2 lignes (UCAD, AUROC image moyen sur MVTec AD et VisA,
Tables 1 et 3), `high`.

## Limites et critique

- L'identité de tâche est inférée, mais une **clé et une connaissance par tâche** sont
  stockées : la mémoire croît linéairement avec le nombre de classes (≈ 1,5 Mo par tâche,
  calcul déduit de 23 Mo / 15) ; c'est une forme de mémoire épisodique de features.
- Le backbone ViT reste gelé ; seuls les prompts apprennent : « pas d'oubli » en partie
  structurel.
- SAM est requis à l'entraînement : coût très élevé, non chiffré.
- Baselines UAD non conçues pour le CL (hors DNE) ; rejeu limité à 100 images pour PatchCore et
  UniAD.
- Incohérences de description de la mémoire (23,19 vs 23,28 Mo ; prompts de 5 ou 7 couches).
- Images seulement ; tâches = classes de produit, pas dérive d'un même équipement.

## Pertinence pour la thèse

Référence pour l'axe détection d'anomalies × CL : il montre qu'un détecteur de type
« mémoire de features normales + distance au plus proche voisin » se prête naturellement au CL
(une connaissance par tâche, sélection par clé), avec un oubli quasi nul. Sur MCU, le principe est
transposable à petite échelle (quelques centaines de vecteurs normaux par régime de
fonctionnement, sélection du régime par distance), mais pas l'architecture ViT + SAM (déduit).

## Gaps identifiés

- CL non supervisé pour la détection d'anomalies sur séries temporelles (vibrations) : non traité.
- Mémoire de features par régime sous budget de quelques dizaines de ko.
- Dérive intra-classe (vieillissement d'une même machine) plutôt que nouvelles classes de
  produits.

## Statut de lecture

Papier complet, annexes comprises (`fulltext.md` lu en entier). Tables 2 et 4 (AUPR pixel) sans
légende propre mais corps extrait ; Table 8 partiellement désalignée ; §Related Work et
§Training Details tronqués.
Déduit et non affirmé par les auteurs : mémoire par tâche (≈ 1,5 Mo), transposition MCU.
