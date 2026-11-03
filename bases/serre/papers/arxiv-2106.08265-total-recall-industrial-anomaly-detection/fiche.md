---
id: arxiv-2106.08265-total-recall-industrial-anomaly-detection
fiche: done
date: 2026-11-03
---

# Towards Total Recall in Industrial Anomaly Detection

Karsten Roth, Latha Pemula, Joaquin Zepeda, Bernhard Schölkopf, Thomas Brox, Peter Gehler, 2021, arXiv preprint. https://arxiv.org/abs/2106.08265 (DOI : n/r ; métadonnées à vérifier ; version lue : arXiv v2, mai 2022)
Type : preprint non relu par les pairs

## Problème

Détection d'anomalies « cold-start » en inspection industrielle : n'entraîner que sur des images nominales (sans défaut) et détecter, puis localiser, les défauts, avec une méthode générique sur de nombreuses classes (§1). Les méthodes à base de caractéristiques ImageNet figées (SPADE, PaDiM) souffrent d'un contexte nominal limité et de caractéristiques de haut niveau mal adaptées à la tâche (§1).

## Méthode

PatchCore (§3) : (1) caractéristiques de patchs de niveau intermédiaire (couches 2 et 3 d'un WideResNet50 pré-entraîné ImageNet, sans adaptation), agrégées sur un voisinage local p = 3 par moyennage adaptatif (§3.1, §4.4.1) ; (2) banque mémoire de tous les patchs des images nominales, réduite par sous-échantillonnage glouton « coreset » (minimax facility location, projection aléatoire de Johnson-Lindenstrauss), notée PatchCore-n% (§3.2) ; (3) score d'anomalie d'une image = distance maximale d'un patch test à son plus proche voisin dans la banque, repondérée par le voisinage de ce voisin (Eq. 6-7) ; la segmentation s'obtient en replaçant les scores de patchs, avec agrandissement bilinéaire et lissage gaussien σ = 4 (§3.3). Pas d'entraînement au sens de la descente de gradient. Pas d'augmentation de données (§4.1).

## Plateforme et implémentation

Matériel d'évaluation, fréquence, puissance, mémoire : n/r dans le texte lu (les détails d'implémentation sont renvoyés au supplément A, absent de `fulltext.md`). Les temps d'inférence sont mesurés « sur GPU là où c'est possible » pour des réimplémentations de SPADE et PaDiM (§4.3), GPU non nommé ici. Code publié : github.com/amazon-research/patchcore-inspection (Abstract). Aucune cible embarquée.

## Résultats

Sur MVTec AD (15 classes, 1725 images de test ; images redimensionnées à 256 puis rognées à 224, §4.1), PatchCore (WideResNet50) :

| Variante | AUROC image | AUROC pixel | PRO | Erreurs image |
|---|---|---|---|---|
| PatchCore-25% | 99.1 (Table 1) | 98.1 (Table 2) | 93.4 (Table 3) | 42 / 1725 (Table 1) |
| PatchCore-10% | 99.0 | 98.1 | 93.5 | 47 |
| PatchCore-1% | 99.0 | 98.0 | 93.1 | 49 |

Baselines (Tables 1-3) : PaDiM 95.3 image / 97.5 pixel / 92.1 PRO ; PaDiM* 97.9 image (backbone choisi par classe, non reproduit par les auteurs) ; SPADE 85.5 image / 96.0 pixel / 91.7 PRO ; DifferNet 94.9 image. Erreur image 2.1 % (PaDiM) à 0.9 % (PatchCore-25 %), soit -57 % (§4.2). Les erreurs sont comptées à un seuil optimal pour F1 (légende Table 1).

Variante coûteuse (PatchCore-1 %, WideResNet101, images 280 px, Table S4) : 99.4 / 98.2 / 94.4 (couches 2+3) et 99.2 / 98.4 / 95.0 (couches 1+2+3). Le texte annonce jusqu'à 99.6 d'AUROC image avec ensembles (Abstract, §4.2, Table 4), mais le corps de la Table 4 est absent de `fulltext.md` : cette valeur n'est pas reportée dans le CSV.

Ablations : voisinage optimal p = 3 et couches 2+3 (Fig. 4, §4.4.1) ; le coreset bat le sous-échantillonnage aléatoire et les proxies appris (Fig. 5) ; PatchCore sans sous-échantillonnage ≈ coreset 100× plus petit ; stride 2 donne 97.6, stride 3 donne 96.8 d'AUROC image (§4.4.2). Faible nombre d'exemples : le niveau de l'état de l'art précédent est atteint avec un cinquième des données nominales ; 1 à 50 images testées (Fig. 6, §4.5). Autres jeux : état de l'art en localisation sur mSTC et détection sur MTD (Table 6, §4.6) ; le corps de la Table 6 est fragmentaire (quatre nombres sans en-têtes), aucune valeur reprise. Temps d'inférence : PatchCore-100 % plus rapide que SPADE, PatchCore avec coreset plus rapide que PaDiM (§4.3) ; le corps de la Table 5 est absent, aucun chiffre en ms.

→ reportés dans `benchmarks.csv` : 15 lignes proposées (3 variantes × 3 métriques sur MVTec AD, plus 2 configurations haute résolution × 3 métriques, Table S4), `power_scope` n/r, plateforme n/r. Écrites dans un fichier à part, non ajoutées à `benchmarks.csv` à ce stade.

## Limites et critique

- Évaluation sur MVTec AD seulement (objets et textures industriels, images quasi alignées, fond contrôlé) ; aucune donnée de plantes ni de terrain. La généralisation à des feuilles n'est pas testée (déduit).
- Les auteurs notent eux-mêmes la dépendance à la transférabilité des caractéristiques ImageNet (Limitations).
- Comparaisons : PaDiM* utilise un backbone choisi par classe, non reproduit (légende Table 1) ; SPADE et PaDiM sont réimplémentés avec WideResNet50 pour l'inférence et les faibles échantillons (§4.3, Fig. 6), donc les valeurs du papier original ne sont pas toutes comparées à iso-conditions. Le nombre d'erreurs n'est calculé que pour PatchCore (pas de scores des concurrents).
- Seuil F1 optimal choisi sur le jeu de test pour compter les erreurs : cela ne dit pas comment fixer un seuil en déploiement sans anomalies disponibles (déduit).
- Le gain de 0.9 % d'erreur est proche de la saturation du benchmark ; MVTec AD est surévalué par un petit nombre de classes parfaites.
- Coût mémoire et latence en ms, matériel et puissance : n/r dans la partie lue ; aucune mesure edge.
- Pas de comparaison de conditions de mesure à un baseline Jetson/RPi/Hailo ; non pertinent pour ce papier.

## Pertinence pour la thèse

Axe `anomaly` de la base serre. Répond directement à la question « la détection d'anomalies non supervisée (PatchCore) fonctionne-t-elle sur des feuilles ? » : le papier fournit la méthode et son état de l'art industriel, mais pas la réponse sur plantes. Intérêt déduit pour SerreIA : (a) n'exige que des feuilles saines, utile pour le rejet hors distribution et la réduction des fausses alertes « anormal » ; (b) le faible nombre d'échantillons (Fig. 6) convient à une serre peu annotée ; (c) la banque mémoire et le kNN restent à chiffrer sur Raspberry Pi 5 / Hailo (non traité ici). Reste ouvert : écart de domaine PlantVillage vers terrain, variabilité nominale élevée des feuilles (le cas MTD, §4.6, est le plus proche), seuil sans anomalies.

## Gaps identifiés

- Aucune évaluation de PatchCore sur des feuilles ou des cultures dans ce papier (à chercher dans le corpus : travaux appliquant PatchCore aux plantes).
- Pas de latence, mémoire ni puissance sur edge (RPi, Hailo) : mesure propre à faire.
- Choix du seuil de décision sans anomalies disponibles : non traité.
- Sensibilité à l'écart de domaine entre caractéristiques ImageNet et images de feuilles : non étudiée.

## Statut de lecture

papier complet (`fulltext.md` lu en entier, extraction `grobid` ok). Tableaux : corps de la Table 5 absent (« sans corps extrait ») ; Table 4 reconstruite par PyMuPDF, son corps affiché dans `fulltext.md` correspond en réalité aux valeurs PRO de la Table 3 (légendes décalées) ; Table 6 fragmentaire ; chiffres de Tables 1-3 recoupés avec le texte (§4.2) et avec les Tables S1-S3. Le supplément A, B (partiel), C (texte) n'est pas dans `fulltext.md`.
Ce qui suit est déduit et non affirmé par les auteurs : la non-testée généralisation aux plantes, l'intérêt pour le rejet OOD et les fausses alertes, le problème du seuil en déploiement, les remarques sur la saturation de MVTec AD.
