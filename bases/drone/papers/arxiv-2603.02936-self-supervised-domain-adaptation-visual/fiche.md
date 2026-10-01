---
id: arxiv-2603.02936-self-supervised-domain-adaptation-visual
fiche: done
date: 2026-10-01
---

# Self-supervised Domain Adaptation for Visual 3D Pose Estimation of Nano-drone Racing Gates by Enforcing Geometric Consistency

Nicholas Carlotti, Michele Antonazzi, Elia Cereda, Mirko Nava, Nicola Basilico, Daniele Palossi, Alessandro Giusti, 2026, arXiv preprint. https://arxiv.org/abs/2603.02936
Type : preprint non relu par les pairs

## Problème

Estimer la pose relative (x, y, z, ψ) d'une porte de drone racing à partir d'une seule image
en niveaux de gris, prise par la caméra d'un nano-drone (Crazyflie 2.1 Brushless), avec un CNN
pré-entraîné en simulation. L'écart sim-to-real (bruit, flou de bougé, vignettage, faible
dynamique de la caméra) dégrade fortement le modèle dans le monde réel (§I). Le fine-tuning
supervisé exige une capture de mouvement ; la généralisation de domaine (PencilNet) et
l'adaptation non supervisée classique (MMD) sont jugées insuffisantes face à un écart aussi
grand (§I, §V).

## Méthode

- Phase 1 : entraînement en simulation (Webots, 75K images, augmentations : flou gaussien,
  vignettage, bruit multiplicatif, exposition) avec une MSE sur la pose ; l'orientation passe
  en représentation 6D de Zhou et al. (§III, §IV-B).
- Phase 2 : fine-tuning sur images réelles seules, sans étiquette de pose. Le drone, piloté
  par un humain sur des trajectoires aléatoires devant la porte, enregistre images et
  odométrie embarquée (EKF fusionnant IMU, flux optique, ToF). Une perte de cohérence d'état
  (State Consistency, L_sc, [12]) impose que les poses prédites sur deux images, ramenées dans
  un même repère grâce à l'odométrie, soient égales (éq. 2, §III).
- Réseau : 4 blocs convolutifs (32, 32, 64, 128 canaux) + batch norm + couche linéaire de
  128 neurones, 6 M de paramètres ; AdamW, lr 1e-3 (sim) puis 1e-6 (réel), 100 epochs chacun
  (§IV-C).
- Déploiement : quantification INT8 par GWT NNTool + AutoTiler, noyaux NE16 pour les
  convolutions et couches linéaires, noyaux CPU parallèles pour le reste (§IV-C).
- Biais constant résiduel (la perte n'ancre pas la pose au centre de la porte) corrigé par
  une calibration sur un petit lot d'images de position connue (§IV-D).

## Plateforme et implémentation

- Crazyflie 2.1 Brushless (Bitcraze) avec GAP9Shield : SoC GreenWaves GAP9, cluster RISC-V
  à 8 cœurs, accélérateur NE16 (150 MAC/cycle, 8 bits), jusqu'à 220 GOp/s à 370 MHz max,
  « moins de 100 mW » (chiffre constructeur cité dans §IV-A, pas une mesure du papier),
  1,5 Mo de L2, 128 ko de L1, 32 Mo d'OctaSPI RAM et 64 Mo de Flash ; caméra OV5647
  (images collectées en 160×160 à 25 FPS) ; ESP32 ; STM32 pour le vol (§IV-A, §IV-B).
- Modèle : 318 MMAC par inférence, 30,4 ms par image sur NE16, 32,8 images/s (§V).
- Puissance mesurée du modèle déployé : `n/r`. Consommation du vol ou de la charge utile :
  `n/r`. Ressources mémoire (L1/L2) occupées par le modèle : `n/r`.
- Code, données et poids : aucun lien publié dans le texte extrait (non publiés d'après le
  texte).

## Résultats

Jeu de test réel Dtest_real (21K échantillons, vérité terrain par capture de mouvement,
utilisée seulement pour le test), moyenne de 3 entraînements (Table I, §IV-E).

| Méthode | MAE x [cm] | MAE y [cm] | MAE z [cm] | MAE ψ [deg] |
|---|---|---|---|---|
| Mean Predictor | 57.0 | 48.7 | 23.1 | 20.9 |
| Zero-Shot (sim seule) | 51.6 | 41.0 | 24.5 | 33.5 |
| PencilNet | 56.7 | 46.8 | 22.5 | 32.7 |
| DA (MMD, [28]) | 66.0 | 34.7 | 33.0 | 28.8 |
| Ours (odométrie seule) | 25.6 | 28.2 | 10.5 | 13.1 |

- Par rapport au Mean Predictor : -54 % de MAE sur x et z, -42 % sur y, -37 % sur ψ (§V). Le
  résumé annonce « 40 % en position et 37 % en orientation » par rapport à une baseline.
- Table I : la première colonne numérique de chaque ligne (90,7 pour Mean Predictor ; 44,7
  pour Ours) est la MSE agrégée xyz [cm] présumée ; l'extraction PyMuPDF a perdu la
  structure du tableau, et les colonnes de corrélation ρ sont illisibles. Seules les MAE
  recoupées avec l'abstract (26, 28, 10 cm ; 13°) sont fiables.
- Ablation (Fig. 7, §V-A) : 10 séquences de 30 s (850 échantillons chacune, soit environ
  10 minutes de vol) suffisent à dépasser toutes les baselines ; 40 séquences approchent
  les performances du jeu complet (60 séquences).
- Déploiement GAP9 : 30,4 ms, 32,8 FPS, 318 MMAC, INT8 « sans perte de performance de
  régression » (§IV-C, §V). Le gain de précision n'est pas chiffré pour la version INT8.
- Échecs qualitatifs : porte partiellement hors image ou vue sous un angle rasant (Fig. 6).

→ reportés dans `benchmarks.csv` : 1 ligne (modèle déployé sur GAP9). Les lignes des baselines
et de l'ablation ne sont pas ajoutées (pas de plateforme embarquée mesurée, ou chiffres
seulement en figure). Fichier de travail : une ligne, MAE ψ = 13.1 (Table I), confidence
`medium` (tableau reconstruit par PyMuPDF, recoupé avec l'abstract).

## Limites et critique

- Papier preprint, évaluation hors boucle fermée : pas de vol de course autonome validé ; les
  auteurs le prévoient en travaux futurs (§VI). Rien n'indique que 33 FPS suffit à la vitesse
  de vol réelle d'une course (déduit).
- Calibration du biais appliquée sur tout le jeu de test et à toutes les baselines (§IV-D) :
  équitable entre méthodes, mais optimiste par rapport à un déploiement où l'offset doit venir
  d'un petit lot connu.
- Baselines réimplémentées sur la même architecture ; PencilNet et DA sont à peine meilleures
  que le Mean Predictor, voire pires. Cela montre un écart sim-to-real grand mais peut aussi
  refléter un réglage peu poussé de ces baselines (déduit ; réglage non détaillé).
- Une seule porte, un seul laboratoire, une seule caméra : généralisation à d'autres scènes
  non testée. Roll et pitch non évalués (§IV-D).
- Erreurs encore élevées (x 26 cm, y 28 cm) pour une porte de 100×80 cm.
- Puissance et énergie du modèle embarqué non mesurées ; le chiffre « moins de 100 mW » est
  celui du SoC en général. Pas de comparaison à un autre MCU ou à un Jetson.
- Les fps et latences sont donnés pour l'inférence seule (NE16), sans détail sur le prétraitement
  ni l'acquisition caméra (non précisé).
- Pas de code ni de modèle publiés d'après le texte ; extraction PyMuPDF, ρ illisibles.

## Pertinence pour la thèse

Axes `nano-drone` et `tracking-navigation` (vol agile, tag `drone-racing`). Illustre un cycle
complet sim-to-real jusqu'au déploiement sur un MCU de gamme nano (GAP9, de l'ordre de
100 mW au niveau du SoC d'après le constructeur) : réseau de 6 M de paramètres,
318 MMAC, INT8, 33 FPS. Fournit une référence de latence perception pour la course de nano-
drones et une méthode d'adaptation en ligne légère (10 min de vol). Laisse ouvert : l'adaptation
sur la puce (ici le fine-tuning se fait hors ligne), la mesure de puissance à la carte,
l'effet de la quantification sur la pose, le bouclage perception-contrôle.

## Gaps identifiés

- Pas de métrique système (autonomie, vitesse de vol sûre) pour ce nano-drone de course ;
  le lien précision de pose ↔ vitesse de passage de porte est non mesuré.
- Pas de puissance mesurée à la carte pour GAP9 + Crazyflie en inférence.
- Fine-tuning hors ligne uniquement : l'apprentissage continu embarqué sur le nano-drone
  n'est pas abordé.
- Effet de l'INT8 affirmé « sans perte » mais non chiffré.

## Statut de lecture

papier complet (`fulltext.md` lu en entier). Extraction en `pymupdf` avec `extraction.ok =
false` : texte lisible mais Table I reconstruite sans structure (les colonnes de corrélation ρ
sont perdues ; les Fig. 5 et 7 ne sont pas lisibles). Déduit et non affirmé par les auteurs :
l'attribution de la première colonne numérique de la Table I à la MSE agrégée xyz, la portée
« SoC » du chiffre de puissance < 100 mW, la remarque sur le réglage des baselines et sur
l'adéquation de 33 FPS à une course réelle.
