---
id: arxiv-1606.09282-learning-without-forgetting
fiche: done
date: 2026-09-29
---

# Learning Without Forgetting

Zhizhong Li, Derek Hoiem, 2018, IEEE Transactions on Pattern Analysis and Machine Intelligence. https://arxiv.org/abs/1606.09282
Type : article de journal

## Problème

Ajouter une capacité à un CNN existant quand les données d'entraînement des tâches déjà
apprises ne sont plus disponibles (non enregistrées, propriétaires, trop lourdes) (§1). Les
approches usuelles ont chacune un défaut : l'extraction de features sous-performe sur la
nouvelle tâche, le fine-tuning dégrade les anciennes, l'entraînement joint exige les
anciennes données (§1).

## Méthode

- **Learning without Forgetting (LwF)** : avant d'entraîner, on enregistre les sorties
  y_o de l'ancien réseau sur les **images de la nouvelle tâche** ; on ajoute une tête θ_n pour
  la nouvelle tâche (§3, Fig. 3).
- Perte : λ_o · L_old(y_o, ŷ_o) + L_new(y_n, ŷ_n) + R, avec L_old = perte de **distillation**
  (Hinton, température T = 2) et R = weight decay 5·10⁻⁴ ; λ_o = 1 le plus souvent (§3).
- Deux étapes : warm-up (θ_s, θ_o gelés, θ_n seule), puis optimisation conjointe de tous les
  paramètres (§3).
- Paramètres partagés θ_s + une tête par tâche (multi-head) ; pas de données anciennes stockées.
- Coût d'entraînement légèrement supérieur au fine-tuning (rétropropagation dans θ_o), temps
  d'inférence identique (§3).
- Implémentation MatConvNet, SGD momentum 0,9, AlexNet et VGG-16 pré-entraînés
  (ImageNet, Places365) (§3.1, §4).

## Plateforme et implémentation

Aucune plateforme matérielle (n/r). Code : non mentionné dans le texte extrait.

## Résultats

AlexNet, une nouvelle tâche, validation (Table 1(a)) ; LwF puis écarts des autres méthodes :

| Paire | Ancienne tâche | Nouvelle tâche | Fine-tuning (ancienne / nouvelle) | Joint training |
|---|---|---|---|---|
| ImageNet→VOC (mAP) | 56,2 | 76,1 | −0,9 / −0,3 | +0,7 / −0,2 |
| ImageNet→CUB | 54,7 | 57,7 | −3,8 / −0,7 | +0,6 / −1,1 |
| ImageNet→Scenes | 55,9 | 64,5 | −2,0 / −0,8 | +0,5 / −0,6 |
| Places365→VOC | 50,6 | 70,2 | −2,2 / +0,1 | +0,7 / 0,0 |
| Places365→CUB | 47,9 | 34,8 | −4,6 / +1,0 | +2,3 / +1,5 |
| Places365→Scenes | 50,9 | 75,2 | −2,1 / −1,7 | +0,3 / −0,3 |
| ImageNet→MNIST | 49,8 | 99,3 | −2,8 / 0,0 | +7,2 / 0,0 |

- LwF bat le fine-tuning sur la nouvelle tâche sauf ImageNet→MNIST et Places365→CUB ; sur
  l'ancienne, il fait mieux que le fine-tuning mais souvent moins bien que l'extraction de
  features (§4.1).
- VGG : le joint training est systématiquement meilleur (Table 1(c)).
- Plusieurs tâches ajoutées successivement : LwF se dégrade plus lentement que le fine-tuning,
  mais passe sous le joint training sur l'ancienne tâche au fil des ajouts (Fig. 4).
- Warm-up essentiel pour le fine-tuning (ancienne tâche 42,5 sans, 50,9 avec, ImageNet→CUB),
  secondaire pour LwF (Table 2(b)).
- Pénalité L2 sur les poids : entre extraction de features et fine-tuning, moins bonne que LwF
  (Fig. 7) ; distillation légèrement meilleure que L1, L2 ou cross-entropy (§4.2).

→ reportés dans `benchmarks.csv` : 4 lignes (ImageNet→CUB et ImageNet→Scenes, ancienne et
nouvelle tâche, Table 1(a), `high`).

## Limites et critique

- Scénario **task-incremental multi-head** avec label de tâche au test ; hypothèse forte que
  les images de la nouvelle tâche « représentent » l'ancienne distribution : les auteurs le
  reconnaissent (Places365→CUB, ImageNet→MNIST) (§4.1).
- Validation des hyperparamètres sur la seule nouvelle tâche (§3.1) : favorise LwF sur la
  nouvelle tâche.
- Écarts souvent de l'ordre du point, moyenne de 3 essais sans écart-type dans la Table 1.
- Ne concerne que la classification d'images.

## Pertinence pour la thèse

Représentant de la famille « fonctionnelle » (distillation) dans la bibliographie du stage :
aucune donnée ancienne stockée, mais une passe avant de l'ancien modèle sur chaque nouvel
échantillon, et donc un coût de calcul là où EWC/SI/MAS paient en mémoire. Sur séries
temporelles de capteurs, l'hypothèse « nouvelles données représentatives des anciennes »
est fragile quand le régime de fonctionnement change (déduit).

## Gaps identifiés

- Distillation sous dérive de domaine forte (changement de régime machine) : non évaluée.
- Coût mémoire/calcul de LwF comparé aux régularisations par poids sur plateforme contrainte : absent.

## Statut de lecture

Papier complet (`fulltext.md` lu en entier). L'annexe A (tracking MD-Net) n'est présente
que par un résumé dans la discussion ; Tables 1(b)-(c) partiellement désalignées dans
l'extraction.
Déduit et non affirmé par les auteurs : l'arbitrage mémoire/calcul face à EWC ; la fragilité
sur séries temporelles.
