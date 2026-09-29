---
id: arxiv-2105.13127-continual-learning-edge-real-time
fiche: done
date: 2026-09-29
---

# Continual Learning at the Edge: Real-Time Training on Smartphone Devices

Lorenzo Pellegrini, Vincenzo Lomonaco, Gabriele Graffieti, Davide Maltoni, 2021, 29th European Symposium on Artificial Neural Networks (ESANN). https://arxiv.org/abs/2105.13127
Type : conférence

## Problème

Personnaliser un modèle profond directement sur l'appareil (confidentialité, hors
connexion) sans réentraîner sur toutes les données passées, et sans oubli catastrophique
quand on ne met à jour qu'avec les nouvelles données (§1).

## Méthode

- **AR1\*** (stratégie hybride de Lomonaco et al.) : dernière couche en double mémoire (CWR\*)
  + régularisation des poids critiques pour entraîner tout le réseau (§2).
- **Latent replay** : au lieu d'images brutes, on stocke les activations d'une couche
  intermédiaire (« latent replay layer ») ; en avant, on concatène les nouveaux motifs et les
  activations stockées ; en arrière, le gradient des motifs rejoués s'arrête à cette couche
  (§2, Fig. 1).
- Application Android **CORe** (Java + C++, Caffe recompilé) : MobileNetV1-1.0 FP32, entrée
  128×128, 10 catégories pré-apprises (CORe50) + 5 emplacements vides ; acquisition de 100
  images (20 s de vidéo) par nouvelle catégorie ; tampon de rejeu fixe de **500 motifs
  latents**, < 2 Mo au niveau `pool` (§3).
- Proposition d'une consolidation en deux temps : mise à jour rapide de la sortie en temps réel,
  consolidation plus profonde en arrière-plan (§3).
- Benchmark : extension de CORe50 (25 objets, 5 nouvelles catégories, 225 expériences, vidéos
  de plusieurs smartphones) ; comparaison à des rejeux « class balanced » et « unbalanced »
  (ce dernier = l'application TensorFlow-Lite de [8]) (§4).

## Plateforme et implémentation

- Smartphone Android, CPU seul (§1, §3) ; modèle de téléphone : n/r (note de bas de page non
  extraite). FP32 (§3). Consommation : n/r.
- Code de l'application et scripts Avalanche publiés (lien en note non extrait) (§1).

## Résultats

Table 1 (précision finale ; temps d'entraînement pour une nouvelle expérience de
100 motifs, 8 époques) :

| Couche de latent replay | Catégories initiales | Nouvelles catégories | Temps total d'entraînement |
|---|---|---|---|
| pool | 97,54 % | 65,33 % | 0,18 s (+ 8,93 s d'extraction de features pendant l'acquisition) |
| conv5_4/dw | 97,16 % | 73,39 % | 167,08 s (+ 6,70 s) |
| input | 79,07 % | 93,62 % | 500,02 s |

- Rejeu « unbalanced » : apprend bien les nouvelles catégories mais oublie progressivement les
  anciennes ; « class balanced (pool) » retient les anciennes mais apprend moins bien les
  nouvelles (§4, Fig. 2).

→ reportés dans `benchmarks.csv` : 3 lignes (une par couche de rejeu ; `latency_ms` = temps
d'entraînement d'une expérience, pas une latence d'inférence ; Table 1 aplatie à
l'extraction, `medium`).

## Limites et critique

- Modèle de smartphone non précisé dans le texte extrait : temps non comparables.
- Papier court (atelier ESANN) : pas d'écart-type, une seule configuration de tampon.
- Le rejeu depuis l'entrée perd 18 points sur les anciennes catégories (79,07 %) : effet d'un
  tampon trop petit pour des images brutes, non analysé (déduit).
- FP32 uniquement ; pas de mesure énergétique.

## Pertinence pour la thèse

Borne « haute » de l'apprentissage continu embarqué dans la bibliographie du stage :
smartphone et MobileNet, soit plusieurs ordres de grandeur au-dessus d'un MCU. Montre le
compromis central **profondeur de mise à jour ↔ temps d'entraînement ↔ oubli** via le choix
de la couche de rejeu latent, repris ensuite sur MCU par Ravaglia 2021 (déduit).

## Gaps identifiés

- Latent replay quantifié (tampon INT8) sur plateforme sans OS : traité par Ravaglia 2021,
  pas ici.
- Aucun chiffre d'énergie par mise à jour.

## Statut de lecture

Papier complet (`fulltext.md` lu en entier ; papier court de 4 pages). Notes de bas de page
(lien du code, modèle de téléphone) non extraites ; Table 1 aplatie.
Déduit et non affirmé par les auteurs : explication de la chute « input » ; filiation avec
Ravaglia 2021.
