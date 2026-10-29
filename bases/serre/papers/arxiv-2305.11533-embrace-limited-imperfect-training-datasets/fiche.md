---
id: arxiv-2305.11533-embrace-limited-imperfect-training-datasets
fiche: done
date: 2026-10-29
benchmarks: none
---

# Embrace Limited and Imperfect Training Datasets: Opportunities and Challenges in Plant Disease Recognition Using Deep Learning

Mingle Xu, Hyongsuk Kim, Jucheng Yang, Alvaro Fuentes, Yao Meng, Sook Yoon, Taehyun Kim, Dong Sun Park, 2023, arXiv preprint (la version publiée porte le DOI https://doi.org/10.3389/fpls.2023.1225409, tel que dans `metadata.json` ; venue à vérifier). https://arxiv.org/abs/2305.11533
Type : preprint non relu par les pairs (d'après `metadata.json`) ; survey de perspective.

## Problème

Le deep learning pour la reconnaissance des maladies des plantes exige des jeux « de qualité » (grande échelle, annotation exclusive, extensive et précise), chers à construire ; les jeux réels sont « pauvres » (§1, `2305.11533#001.1`). Les auteurs veulent définir explicitement les défis posés par des jeux limités et imparfaits, et en proposer une taxonomie, par approche « par défi » plutôt que « par technique » (`2305.11533#001.3`).

## Méthode

Revue narrative, sans protocole de recherche bibliographique décrit dans les passages lus ; pas d'expérience propre. Taxonomie (Table 1, §3, `2305.11533#008.1`) :
- jeu **limité**, niveau classe : few-shot (n_i ≈ M, M de l'ordre de 5 à 10, étendu à 100-500) et déséquilibre de classes (n_i ≫ n_j avec n_j ≤ M) (§4.1, `2305.11533#011.1`, `2305.11533#013.1`) ;
- jeu limité, niveau dataset : classe inconnue (open set / OOD) et décalage de domaine (§4.2) ;
- jeu **imparfait** : annotation incomplète (images non annotées), inexacte (grain grossier) et inaccurate (bruit de labels) (§5).
Pour chaque défi : formalisation, puis stratégies (augmentation, génération CGAN, transfert, méta-/metric learning, seuils OOD, adaptation de domaine, SSL, semi-supervisé, apprentissage actif).

## Plateforme et implémentation

Sans objet (pas de matériel, pas de mesure de puissance). Code/jeux : non publiés par ce papier.

## Résultats

Revue : un seul chiffre est rapporté, et il vient d'un travail cité (Xu et al., 2022c) : exactitude test moyenne de 86,29 % sur 12 jeux de reconnaissance de maladies en 20-shot, avec un ViT pré-entraîné sur PlantCLEF2022 (2 885 052 images, 80 000 classes), soit 12,76 % de plus que l'état de l'art cité (§4.1.1, `2305.11533#011.5`). Autre chiffre cité : une translation d'images fait passer 350 images à 39 010 pour six maladies et les feuilles saines (Gorad et Kotrappa, 2021 ; `2305.11533#011.2`).
Constat des auteurs : peu de travaux sur les défis au niveau dataset et sur l'annotation imparfaite, et pénurie de jeux de référence adaptés au terrain (§6, `2305.11533#022.0`).
→ reportés dans `benchmarks.csv` : aucune ligne (survey ; chiffres des travaux cités non repris).

## Limites et critique

- Revue narrative : pas de méthode de sélection, pas de comparaison chiffrée entre stratégies ; aucune recommandation hiérarchisée par gain mesuré.
- La section décalage de domaine (§4.2.2) reste générale : le papier dit lui-même que le sujet est « à peine étudié » en maladies des plantes (`2305.11533#017.0`) et décrit l'adaptation de domaine de façon qualitative (`2305.11533#016.2`).
- Le 86,29 % est un chiffre d'auteurs sur leur propre travail cité (autocitation), non vérifié ici ; les 12 jeux ne sont pas détaillés dans les passages lus.
- Sur la calibration et le choix de seuil, seul un seuil fixe (95 % des images d'entraînement conservées) est évoqué (`2305.11533#015.1`) : pas de comparaison de méthodes.
- Preprint ; métadonnées à vérifier (avertissement de l'extraction).

## Pour SerreIA

Contexte (lecture seule : docs SerreIA non relus ici, éléments donnés par le prompteur) : EfficientNet-B0 multi-têtes, PlantVillage + CCMT (88 135 images, 16 espèces, 56 classes, splits anti-fuite), test hors domaine PlantDoc : spécificité 0,50, F1 classe 0,264, 42 % de faux positifs sur images saines ; apprentissage actif et annotation semi-automatique prévus. Le papier apporte un cadre de lecture ; les gains chiffrés sont à mesurer chez SerreIA.

Le cas SerreIA relève du **décalage de domaine** (§4.2.2) et de la **classe inconnue / OOD** (§4.2.1), avec une dimension d'**annotation incomplète** (images de serre non annotées, §5.1). Les auteurs rappellent que, même avec 221 000 images, la performance chute sur des champs différents de ceux d'entraînement (covariate shift ; Shibuya et al. 2021, `2305.11533#017.2`) : plus d'images de laboratoire ne suffit pas.

| Recommandation de la revue | Source | S'applique à SerreIA ? | Priorité | Expérience à faire |
|---|---|---|---|---|
| Augmentation par nouveaux fonds (fusionner l'objet malade sur des fonds de terrain) | `2305.11533#011.2` | Oui, c'est la parade directe au biais de fond PlantVillage → PlantDoc | P1 | Entraîner avec/sans remplacement de fond (masque de feuille), comparer spécificité et F1 sur PlantDoc à rappel fixé ; garder le même split anti-fuite |
| Classes de contrôle « fond » et « feuille saine » pour guider l'apprentissage (Fuentes et al. 2021b) | `2305.11533#017.0` | Oui : 42 % de faux positifs sur sain = problème de classe saine mal modélisée | P1 | Ajouter une classe « fond/non-feuille » et renforcer le « sain » par espèce ; mesurer le taux de faux positifs sur images saines PlantDoc |
| Détection préalable des régions d'intérêt avant classification (Shibuya 2021, Fuentes 2021a : détecteur puis adaptation) | `2305.11533#017.1`, `2305.11533#017.2` | Oui, rejoint le pipeline deux étages (détecteur de feuilles + classifieur) | P2 | Comparer classifieur sur image entière vs crops de feuilles sur PlantDoc ; mesurer le coût edge |
| Seuil OOD sur probabilité / énergie, seuil par classe plutôt que global | `2305.11533#015.1` | Oui, pour rejeter crops inexploitables et réduire les fausses alertes | P1 | Comparer softmax max, énergie et seuil par classe ; calibrer sur un jeu de validation hors domaine (et non sur le train) ; courbe fausses alertes vs rappel |
| Pré-entraînement sur source apparentée aux plantes plutôt qu'ImageNet seul (PlantCLEF, ViT) ; chaîne : modèle, jeu source, perte | `2305.11533#011.4`, `2305.11533#011.5` | Partiel : EfficientNet-B0 est déjà pré-entraîné ; la source plantes reste à tester | P2 | Initialiser B0 depuis un pré-entraînement plantes (si poids disponibles) vs ImageNet ; protocole identique |
| Apprentissage actif : choisir les images informatives à faire annoter | `2305.11533#019.1` | Oui, déjà prévu ; la revue note que l'humain dans la boucle est peu pratique | P2 | Annoter par lots les images PlantDoc/serre à plus forte incertitude vs tirage aléatoire ; courbe F1 vs nombre d'annotations |
| Semi-supervisé par pseudo-labels (classifieur entraîné pour annoter les non-annotées) | `2305.11533#019.1` | Oui, annotation semi-automatique prévue | P2 | Pseudo-labelliser les images de serre non annotées avec un seuil de confiance, ré-entraîner, évaluer sur PlantDoc ; surveiller la propagation d'erreurs (§5.2) |
| Auto-supervision (augmentation, Mixup comme tâche prétexte) puis fine-tuning | `2305.11533#019.0`, `2305.11533#019.1` | Utile si beaucoup d'images de serre non annotées | P3 | Pré-entraîner sur images de serre sans labels, fine-tuner sur le jeu annoté |
| Bruit de labels : annotateurs multiples, ré-annotation corrective | `2305.11533#020.0` | Possible : labels CCMT/PlantDoc à auditer ; coûteux | P3 | Auditer un échantillon des erreurs les plus confiantes du modèle ; estimer le taux de labels faux |
| Déséquilibre : rééchantillonnage, perte pondérée, traduction d'image entre classes | `2305.11533#013.2` | Oui : 56 classes, effectifs inégaux probables | P2 | Comparer perte pondérée vs rééchantillonnage ; rapporter le rappel par classe minoritaire |
| Few-shot, méta-/metric learning | `2305.11533#012.0` | Peu : 88 135 images, pas de classe à 5 exemples ; le papier note que les jeux manquent pour le méta-apprentissage | P3 | Seulement pour des maladies nouvelles de serre ; sinon laisser de côté |
| Adaptation de domaine adversariale | `2305.11533#016.2` | À tester en dernier : demande ressources et données cibles ; qualitatif dans le papier | P3 | Après P1/P2, si l'écart PlantDoc persiste |

Point méthodologique : les auteurs proposent de réévaluer l'objectif et le jeu quand des classes ont des motifs visuels trop proches (§6) ; à garder à l'esprit si la F1 par classe reste basse malgré les parades. Toujours noter dataset d'entraînement et de test et indiquer test hors domaine, comme le profil l'exige.

## Gaps identifiés

- Peu de travaux chiffrés sur le décalage de domaine labo → terrain en maladies des plantes (`2305.11533#017.0`).
- Pénurie de jeux de référence orientés terrain (`2305.11533#022.0`).
- Aucune comparaison de méthodes de seuil/calibration pour l'OOD en maladies des plantes (§4.2.1).

## Statut de lecture

Papier complet non relu en entier : sections lues par recherche ciblée et lecture de plages : résumé, §1 (début), §3, §4.1.1, §4.1.2, §4.2.1, §4.2.2, §5.1-5.3, §6. Non lus : §2 (jeu de qualité), légendes de figures, liste de références ; Box 1 et 2 vus en partie. Extraction grobid, ok.
Déduit et non affirmé par les auteurs : tout le tableau « Pour SerreIA » (applicabilité, priorités, expériences), les rapprochements avec le pipeline deux étages et la calibration, et l'idée que « sain » est mal modélisé chez SerreIA.
