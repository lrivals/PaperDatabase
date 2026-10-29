---
id: arxiv-1909.11915-unsupervised-image-translation-adversarial-networks
fiche: done
date: 2026-10-29
---

# Unsupervised Image Translation using Adversarial Networks for Improved Plant Disease Recognition

Haseeb Nazki, Sook Yoon, Alvaro Fuentes, Dong Sun Park, 2019, arXiv preprint. https://arxiv.org/abs/1909.11915
Type : preprint non relu par les pairs (arXiv 1909.11915, pas de DOI). Extraction GROBID, ok.

## Problème

Jeu de maladies de tomate petit (2 789 images brutes) et très déséquilibré entre 9 classes ; le
déséquilibre biaise la frontière de décision du classifieur (Abstract, 1909.11915#000.0). Les auteurs
cherchent à rééquilibrer par des images synthétiques plutôt que par l'augmentation classique.

## Méthode

- AR-GAN : CycleGAN (pertes adversariale + cohérence cyclique) auquel s'ajoute une perte de
  reconstruction d'activations (ARL) calculée par un réseau d'extraction de traits initialisé
  ImageNet, entre une image et sa traduction (§2.5.1, 1909.11915#008.0). Traduction non
  appariée de classes sources vers une classe maladie (par ex. feuilles saines vers oïdium, Table 2).
- Générateur 9 blocs résiduels (ou U-Net), discriminateur PatchGAN 70x70, 256x256, ~11,3 M de
  paramètres, entraîné sur une Titan X en 3 jours, batch 1 à 3 ; α=10, λ=1 pour la tomate
  (1909.11915#009.1, 1909.11915#009.2). Génération annoncée à 0,0182 ms par image (1909.11915#009.2) : valeur
  suspecte (non expliquée), à ne pas reprendre.
- Les images synthétiques s'ajoutent aux vraies (X + Xs) ; comparées à l'augmentation classique
  (inclinaison, cisaillement, rotation 0-180°, retournement ; X + Xc). Aucune augmentation pour
  'Leaf Mold' et 'Whitefly' (>50 % du jeu) ; effectifs par classe gardés proportionnels entre Xc
  et Xs (1909.11915#024.0, 1909.11915#024.1).
- Classifieur : ResNet50 (~23 M de paramètres), fine-tuning ImageNet, 256x256, batch 32, lr 0,001,
  300 epochs, SGD Nesterov, Keras (1909.11915#010.0).

## Plateforme et implémentation

Aucune cible embarquée. GAN entraîné sur NVIDIA Titan X (1909.11915#009.1) ; plateforme du classifieur
n/r ; puissance n/r ; quantification n/r. Code et poids : non publiés (aucun lien dans le texte).

## Résultats

- Jeu : 2 789 images prises « dans différentes circonstances » (éclairage, saison, lieux, appareils
  simples), 9 classes, annoté par des experts (1909.11915#013.0) ; 5 318 RoI après extraction ;
  "Low Temperature" et "Powdery Mildew" < 5 % (1909.11915#024.0).
- Test : 200 échantillons par classe, « unseen » à l'entraînement (§3.3.5, 1909.11915#025.0).
- Exactitude ResNet50 : X 80,9 % ; X+Xc 81,7 % (+0,8) ; X+Xs 86,1 % (+5,2) (1909.11915#025.0, Fig. 9).
- Qualité GAN, Table 2 (oïdium, saines vers malades) : FID 47,15 pour AR-GAN U-Net contre 75,81 à
  92,26 pour CycleGAN (1909.11915#035.0). FCN-score Cityscapes (Table 1) non repris : tableau sans corps
  utile extrait.
- Avec l'augmentation classique, 'Canker' et 'Powdery mildew' reculent en vrais positifs ; avec la
  synthétique, toutes les classes progressent (Fig. 10, 1909.11915#025.0).
→ reportés dans `benchmarks.csv` : 4 lignes (3 exactitudes ResNet50, 1 FID), à coller par l'agent principal.

## Limites et critique

- Test in-domain : validation tirée du même jeu tomate (200 par classe), aucun test hors domaine.
  Le papier ne dit pas si les images de test viennent des mêmes plantes ou séries que
  l'entraînement ni si les RoI d'une même photo peuvent se retrouver des deux côtés : risque de fuite
  (déduit, non affirmé).
- Un seul run, pas d'écart-type ni d'intervalle : +5,2 points sur 1 800 images de test n'est pas
  accompagné d'un test de significativité.
- Baseline ResNet50 faible (80,9 %) sur un jeu petit et propre ; l'augmentation classique est
  modeste (pas de recadrage ni de couleur) : l'écart avec la synthétique est peut-être surestimé.
- Pas de comparaison avec la pondération des classes, le rééchantillonnage ou le transfert depuis
  PlantVillage. Les images synthétiques viennent des mêmes images : le gain peut venir d'un
  rééquilibrage plutôt que de nouvelle information.
- Aucune évaluation de robustesse au fond ou au décalage de domaine ; les RoI sont recadrées à la
  main sur la zone malade (le fond est donc déjà retiré en bonne partie).
- Pas de code, valeur de latence de génération douteuse.

## Pertinence pour SerreIA

Axe : `disease-classif`. Preprint de 2019, tomate, jeu privé, in-domain : ses chiffres ne sont PAS
comparables à ceux de SerreIA (EfficientNet-B0, PlantVillage+CCMT, test hors domaine PlantDoc :
rappel 0,986, précision 0,679, spécificité 0,50, ECE 0,13/0,30 ; exactitude 80,9 % -> 86,1 %
sur 9 classes tomate in-domain, autre protocole, autre métrique). Aucune de ces métriques ne se
transpose.

Ce que SerreIA peut en reprendre, par ordre de valeur :
1. Une preuve de principe : la traduction d'images non appariée (CycleGAN/AR-GAN) peut rééquilibrer
   des classes rares et gagner 5,2 points contre 0,8 pour l'augmentation classique (1909.11915#025.0).
   Utile pour les classes rares de CCMT/PlantDoc, pas pour l'écart de domaine.
2. Comparaison au remplacement de fond prévu (`data/backgrounds/`, jamais testé) : les deux
   méthodes visent des biais différents. Le remplacement de fond casse la corrélation
   « fond de laboratoire = classe » de PlantVillage et vise le hors domaine ; AR-GAN, ici,
   corrige le déséquilibre de classes et n'est jamais évalué hors domaine. Le papier ne dit rien
   du fond. Le remplacement de fond est donc l'expérience prioritaire pour le gap PlantDoc ; la
   GAN est un complément secondaire (coût : 3 jours de GPU, instabilité d'entraînement, risque
   d'artefacts qui entrent dans le jeu d'entraînement).
3. Expérience à faire : domaine A = images PlantVillage (fond uniforme), domaine B = images PlantDoc
   (terrain), traduction non appariée A->B avec CycleGAN/AR-GAN (traduction de style, pas de
   classe) pour fabriquer des PlantVillage « de terrain », puis réentraînement du classifieur et test
   sur PlantDoc réservé. À comparer au remplacement de fond et à leur combinaison, au même test.
   C'est une extension non faite par les auteurs (inférence).
4. Métrique : suivre FID (et NIMA) entre images synthétiques et PlantDoc comme contrôle de qualité
   (Table 2, 1909.11915#035.0) ; mais la métrique de décision reste celle du projet : précision, spécificité
   et F1 de la classe anormale sur PlantDoc, avec ECE avant/après.
5. Évaluer par classe (vrais et faux positifs, Fig. 10-11) : même lecture que les 42 % de faux
   positifs du pipeline à deux étages sur images saines ; ajouter des images saines synthétiques ou
   réelles de fond varié comme classe négative.
Fichiers concernés côté projet (non vérifiés, SerreIA en lecture seule non consulté) : le script de
préparation/augmentation de `vision/…` et le dossier `data/backgrounds/`. Pas d'impact sur l'edge :
la GAN ne sert qu'à l'entraînement, le HEF INT8 Hailo-8L reste inchangé.

## Gaps identifiés

- Pas d'évaluation hors domaine (terrain) d'une augmentation par GAN : à tester sur PlantDoc.
- Pas de comparaison GAN contre remplacement de fond ou fonds variés.
- Pas de mesure de calibration après augmentation synthétique.

## Statut de lecture

Papier complet (fulltext.md lu par sections : résumé, §2.4-2.5, §3.1, §3.3.3-3.3.5, discussion,
Table 2) ; §2.1-2.3 et FCN-score (Table 1) survolés seulement. Fig. 9 lue via le texte de §3.3.5.
Extraction GROBID, sans avertissement d'extraction autre que les ligatures.
Déduit et non affirmé par les auteurs : risque de fuite entre train et test ; absence de significativité ;
comparabilité avec SerreIA ; extension A->B hors domaine ; coût de la GAN comparé au remplacement de fond ;
suspicion sur 0,0182 ms.
