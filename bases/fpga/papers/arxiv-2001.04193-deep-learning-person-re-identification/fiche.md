---
id: arxiv-2001.04193-deep-learning-person-re-identification
fiche: done
date: 2026-09-29
benchmarks: none
---

# Deep Learning for Person Re-identification: A Survey and Outlook

Mang Ye, Jianbing Shen, Gaojie Lin, Tao Xiang, Ling Shao, Steven C H Hoi, 2020, arXiv preprint. https://arxiv.org/abs/2001.04193
Type : preprint non relu par les pairs (survey ; pas de DOI dans `metadata.json`)

## Problème

La ré-identification de personnes (Re-ID) cherche à retrouver une personne d'intérêt à travers des caméras sans recouvrement (§1). Les auteurs constatent un fossé entre les scénarios de recherche (« closed-world » : images d'une seule modalité, boîtes englobantes fournies, annotations abondantes et correctes, requête toujours présente dans la galerie) et les applications réelles (« open-world » : modalités hétérogènes, détection incluse, peu ou pas d'étiquettes, bruit, requête absente de la galerie) (§1, Table 1). Le survey organise la littérature selon les cinq étapes d'un système Re-ID (Fig. 1) et propose une baseline (AGW) et une métrique (mINP).

## Méthode

- Closed-world (§2) : apprentissage de représentations (globales, locales par parties, auxiliaires : attributs, viewpoint, GAN, augmentation ; vidéo ; choix d'architecture dont OSNet, Auto-ReID), *deep metric learning* (pertes identity, verification, triplet, OIM ; stratégies d'échantillonnage), optimisation du classement (re-ranking, fusion). Jeux de données et état de l'art image et vidéo (§2.4, Fig. 5 et 6).
- Open-world (§3) : Re-ID hétérogène (profondeur, texte, visible-infrarouge, cross-résolution), *end-to-end* (person search depuis images brutes, suivi multi-caméras, §3.2), non supervisé et adaptation de domaine (§3.3), robustesse au bruit (occlusion partielle, étiquettes bruitées, §3.4), open-set, groupes, réseau de caméras dynamique (§3.5).
- Outlook (§4) : métrique mINP (*mean Inverse Negative Penalty*, Éq. 6-7) qui mesure l'effort pour trouver la correspondance la plus difficile ; baseline AGW = BagTricks sur ResNet50 + *non-local attention* + pooling GeM + perte triplet pondérée WRT (§4.2, Fig. 8) ; questions ouvertes (§4.3), dont mise à jour dynamique du modèle et déploiement efficace (hashing, modèles légers, DaRe).

## Plateforme et implémentation

Puce / carte : n/r (aucune plateforme matérielle : les expériences AGW sont réalisées sur GPU d'après le cadre du papier, mais le texte principal renvoie aux détails d'implémentation au supplément non lu ; aucune mesure de puissance, latence ni ressources). Code publié : https://github.com/mangye16/ReID-Survey (note de bas de page 3, §4.2) ; bitstream : sans objet.

## Résultats

Résultats du survey, non matériels. Points chiffrés utiles :
- AGW (Full) : Market-1501 Rank-1 95.1 %, mAP 87.8 %, mINP 65.0 % ; DukeMTMC Rank-1 89.0 %, mAP 79.6 %, mINP 45.7 % (Table 4). CUHK03 : 63.6 / 62.0 / 50.3 ; MSMT17 : 68.3 / 49.3 / 14.7 (Table 5). Baseline comparée : BagTricks (Table 4-5) et ABD-Net (Table 4).
- Le Rank-1 sur Market-1501 dépasse le niveau humain de 93.5 % ; la meilleure valeur rapportée en §2.4.2 est VAL (96.2 % Rank-1, mAP 91.6 %). MSMT17 reste bien plus difficile (Rank-1 82.3 %, mAP 60.8 % pour le meilleur état de l'art cité, §2.4.2).
- Non supervisé : SpCL atteint 90.3 % Rank-1 / 76.7 % mAP sur Market-1501 (§3.3.3), contre 96.1 % supervisé (ConsAtt).
- Les auteurs notent que la performance chute fortement en évaluation inter-datasets et sous attaque adverse (§2.4.2).
→ reportés dans `benchmarks.csv` : aucune ligne (survey ; les chiffres AGW sont des métriques de précision GPU sans plateforme FPGA / embarquée, hors périmètre du schéma matériel de `benchmarks.csv`).

## Limites et critique

- Aucune dimension embarquée mesurée : « efficient model deployment » (§4.3.5) n'est traité qu'en quelques lignes (hashing, distillation, OSNet, DaRe) sans chiffres de latence, de puissance ni de quantification. Les FLOPs et le nombre de paramètres sont cités comme métriques utiles (§2.4.1) mais pas comparés dans un tableau.
- Les comparaisons AGW vs état de l'art reposent sur des protocoles hétérogènes (mêmes datasets, mais réglages tirés d'autres papiers, sans re-ranking, §2.4.2) ; AGW est conçue par les auteurs, qui définissent aussi la métrique mINP où elle est favorisée (mINP 45.7 % vs 42.1 % pour ABD-Net sur Duke, §4.2). La limite propre de mINP est reconnue : les écarts sont plus faibles sur grande galerie (§4.1).
- Biais de domaine : jeux de données de campus, rues et aéroports en visible (Table 2) ; aucun jeu en environnement industriel, avec EPI (casque, gilet) ou uniforme. Les Re-ID par apparence supposent que des vêtements distincts existent ; le cas des vêtements changés / uniformes est cité comme non résolu (§4.3.1).
- Tables 2 et 3 sans corps extrait : statistiques des jeux de données et tableau non supervisé non lisibles (voir Statut de lecture). Tables 4 à 8 lues via texte reconstruit, à prendre avec prudence pour Table 8.
- Publié en preprint ; les résultats les plus récents (2019 et début 2020) ne sont pas relus par les pairs dans cette version.

## Pertinence pour la thèse

Axe `person-detection` (cas d'application : identification de personnes en secteur industriel dangereux). Le survey donne le vocabulaire et la chaîne complète de la Re-ID (détection, suivi, extraction de descripteur, recherche, §1, §3.2) et distingue explicitement person search bout-en-bout et Re-ID par boîtes englobantes : c'est le lien avec un détecteur YOLO déjà présent dans le pipeline. Il met aussi en lumière trois verrous qui concernent la thèse : le déficit de généralisation inter-domaines (§4.3.3), la mise à jour dynamique du modèle avec de nouvelles caméras ou identités (§3.5, §4.3.4), qui rejoint l'axe apprentissage continu, et la robustesse aux attaques adverses (§2.4.2), volet *security* secondaire du profil. Ce qui manque : aucune considération de sûreté (taux de faux négatifs garantis, métriques de risque, certification) ni de contraintes matérielles ; la Re-ID est présentée comme outil de surveillance publique, sans hypothèse de zone dangereuse, EPI, ni exigence de temps réel embarqué.

## Gaps identifiés

- Re-ID / person search sur FPGA ou SoC embarqué (latence, puissance, quantification) : le survey n'en cite aucun ; à croiser avec les accélérateurs YOLO de la base.
- Jeux de données et évaluation de la Re-ID en milieu industriel (uniformes, EPI, casques, occlusions par équipements), et mesure de fiabilité utile à un dossier de sûreté (faux négatifs, incertitude), absents de la littérature couverte ici.
- Mise à jour incrémentale de la Re-ID sur la cible (nouveau personnel, nouvelle caméra) : signalé comme peu étudié en deep learning (§3.5, §4.3.4).

## Statut de lecture

papier complet : `fulltext.md` lu en entier (491 lignes), extraction Grobid (`extraction.ok` vrai). Tables 2 (statistiques des jeux de données) et 3 (non supervisé, Market-1501 / DukeMTMC) sans corps extrait : leurs chiffres ne sont pas exploités, seules les valeurs redonnées dans le texte (§2.4.2, §3.3.3) sont citées. Le supplément (détails d'implémentation AGW, comparaison complète) n'est pas dans le texte. Ce qui suit est déduit et non affirmé par les auteurs : l'exécution des expériences AGW sur GPU ; l'absence de jeux industriels ; le rapport avec YOLO, la vidéosurveillance en zone dangereuse et l'axe sûreté / apprentissage continu de la thèse.
