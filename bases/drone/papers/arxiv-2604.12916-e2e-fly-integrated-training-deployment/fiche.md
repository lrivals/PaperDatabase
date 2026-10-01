---
id: arxiv-2604.12916-e2e-fly-integrated-training-deployment
fiche: done
date: 2026-10-01
benchmarks: none
---

# E2E-Fly: An Integrated Training-to-Deployment System for End-to-End Quadrotor Autonomy

Fangyu Sun, Fanxing Li, Linzuo Zhang, Yu Hu, Renbiao Jin, Shuyu Wu, Wenxian Yu, Danping Zou (Shanghai Jiao Tong University), 2026, arXiv preprint. https://arxiv.org/abs/2604.12916
Type : preprint non relu par les pairs

## Problème

Transférer en zero-shot de la simulation au réel des politiques de contrôle bout en bout pour quadrirotor reste difficile : rendu visuel lent, modèle physique imprécis, écarts capteurs, et absence de plateforme unifiée intégrant l'apprentissage par simulation différentiable dans un flux entraînement - validation - déploiement (Abstract, §I). Les plateformes existantes (Agilicious, AirGym) ne couvrent pas la simulation différentiable ni un guide de conception de récompense (§I, Table I).

## Méthode

- Entraînement : simulateur VisFly (Habitat-sim, dynamique PyTorch différentiable, jusqu'à 6000 FPS en profondeur 256x256 (§IV-A)) ; deux algorithmes, PPO (RL) et BPTT (gradient analytique par simulation différentiable) (§IV-B). Sortie de politique en CTBR (poussée collective normalisée + vitesses angulaires) (§IV-A, §VII-A).
- Guide de conception de récompense (progression, lissage d'action, orientation, vitesse, vitesse angulaire, évitement, sparse but/crash, Eqs. 11-34, Table II) et curriculum pour l'évitement d'obstacles à haute vitesse et la course avec obstacles (Table III).
- Validation en deux temps : sim-to-sim VisFly vers AirSim (§V-A) et hardware-in-the-loop (nœud VIS-HIL, drone réel dans une capture de mouvement Vicon, images simulées à 30 Hz par défaut (§V-B)).
- Alignement sim-to-réel en quatre volets : identification système (masse, inertie par prototype numérique à moins de 10 % d'erreur, banc LY-5KGF pour la poussée et la constante de temps moteur, Table IV), compensation de latence (alignement de réponse indicielle, 3 trames de retard pour VIS-H, 2 pour VIS-R à 30 Hz (§VI-C2)), randomisation de domaine limitée à la configuration initiale et à l'environnement (Table V), modèle de bruit (gaussien sur la profondeur inverse, bruit Redwood pour D435i ; Table VI).
- Pont bas niveau betaflight-ctrl (machine à états, repli automatique en vol stationnaire, §VI-B).

## Plateforme et implémentation

- Deux quadrirotors (cadre OddityRC, contrôleur de vol STM32F7 compatible Betaflight, moteurs 3000KV, hélices 3.5 pouces) : VIS-R embarqué (750 g sans batterie, ordinateur Radxa/Radax X4 avec processeur Intel N100, caméra RealSense D435i RGB-D, environ 630 USD) et VIS-H déporté (470 g, liaison sans fil et caméra FPV, environ 280 USD) (§VI-A).
- Entraînement sur i9-13900K 32 coeurs + RTX 4090 (§VII-B).
- Puissance, consommation, latence d'inférence, taille du réseau politique, quantification : n/r. Aucune mesure embarquée de calcul.
- Code : le paquet betaflight-ctrl est annoncé open source (légende Fig. 1) ; aucun lien dans le texte extrait. Bitstream : sans objet.

## Résultats

- BPTT converge en environ 1200 s en moyenne contre environ 4150 s pour PPO (moins de 30 %), sur quatre tâches d'état (hover, landing, tracking, racing), avec un FPS d'entraînement comparable, 100 environnements parallèles (§VII-C, Table VII). Table VII est mal extraite (valeurs par tâche non attribuables avec certitude) : seules les moyennes du texte sont reprises.
- Atterrissage visuel (segmentation 64x64) par BPTT : environ 1e6 pas (§VII-E). Course avec obstacles (profondeur 64x64) par PPO + curriculum : 100 % de succès sur trois circuits en simulation, vitesse maximale supérieure à 10 m/s (§VII-E, Fig. 11).
- Transfert zero-shot réel sur VIS-R (course avec obstacles aussi validée en HIL sur VIS-H) : résultat qualitatif (Fig. 13-15), pas de taux de succès réel chiffré ; latence de communication d'environ 90 ms (offboard) contre moins de 30 ms (embarqué) (§VI-C2).
- Ablation des composantes de récompense (Fig. 8-9) : courbes seulement.
→ reportés dans `benchmarks.csv` : aucune ligne. Les seuls chiffres sont des temps d'entraînement sur GPU de bureau et des taux de succès en simulation, sans inférence embarquée mesurée (FPS, puissance, latence de politique), donc hors du schéma de `benchmarks.csv`.

## Limites et critique

- Aucune métrique de calcul embarqué : pas de puissance, de latence d'inférence ni de taille de modèle pour le N100 ; la politique est supposée "légère" (§VI-A) sans chiffre.
- Validation réelle essentiellement qualitative (trajectoires, réponses indicielles), sans statistiques de succès sur vol réel ni comparaison à un contrôleur modulaire ou à un baseline publié.
- Comparaison PPO/BPTT : temps d'entraînement sur un seul matériel, une seule graine rapportée (non précisé) ; les auteurs revendiquent la "première comparaison tâche par tâche" sans le démontrer contre la littérature.
- Les tâches sont majoritairement état-seul ; le cas visuel utilise des images basse résolution 64x64 et de la segmentation sémantique fournie par le simulateur (en réel, source de la segmentation non décrite : à vérifier).
- Hors périmètre vision embarquée au sens accélérateur : l'article ne traite pas l'efficacité du calcul. Papier d'un seul groupe, preprint, extraction PyMuPDF (tableaux VII-X partiellement illisibles).
- Portée de puissance : sans objet (aucune puissance rapportée).

## Pertinence pour la thèse

Référence d'axe `tracking-navigation` (vol agile, course de drones, tag `drone-racing`) et lien avec `system-codesign` : quantifie la latence de la boucle perception - contrôle (90 ms offboard vs moins de 30 ms sur N100, 2 à 3 trames à 30 Hz), gamme x86 basse consommation (N100, quelques W à ~10 W, non mesuré ici), au-dessus du FPGA. Utile pour motiver une métrique système (latence de bout en bout vs agilité) et comme cas d'usage de politiques légères portables sur accélérateur. Ouvert : coût énergétique et latence d'une telle politique sur FPGA/MCU, quantification d'une politique de contrôle, robustesse aux erreurs mémoire.

## Gaps identifiés

- Aucune mesure puissance / latence d'inférence pour des politiques end-to-end sur calculateur embarqué (N100 non caractérisé).
- Pas de portage ni de quantification de ces politiques sur FPGA ou MCU.
- Pas de lien chiffré entre latence de calcul et performance de vol (vitesse maximale sûre) au-delà de la compensation de retard.

## Statut de lecture

papier complet (fulltext.md lu en entier ; extraction PyMuPDF, `extraction.ok` à false : Tables VII-X et équations partiellement dégradées, légendes de figures lisibles).
Ce qui suit est déduit et non affirmé par les auteurs : le caractère "léger" de la politique n'est pas chiffré ; l'absence de puissance mesurée est constatée dans le texte extrait ; l'attribution des colonnes de la Table VII par tâche est incertaine (moyennes reprises du texte) ; le lien du code n'a pas été trouvé dans le texte extrait.
