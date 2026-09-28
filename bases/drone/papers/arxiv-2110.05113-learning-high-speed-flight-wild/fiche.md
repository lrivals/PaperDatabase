---
id: arxiv-2110.05113-learning-high-speed-flight-wild
fiche: done
date: 2026-09-28
---

# Learning High-Speed Flight in the Wild

Antonio Loquercio, Elia Kaufmann, René Ranftl, Matthias Müller, Vladlen Koltun, Davide Scaramuzza, 2021, Science Robotics 2021 Vol. 6, Issue 59, abg5810. https://doi.org/10.1126/scirobotics.abg5810
Type : article de journal (Science Robotics ; version arXiv 2110.05113 lue)

## Problème

Le vol autonome d'un quadrirotor à grande vitesse dans un environnement encombré et
inconnu, avec capteurs et calcul **uniquement embarqués**. Les auteurs attribuent la
limite de vitesse des approches classiques à leur découpage séquentiel perception →
cartographie → planification : latence cumulée et erreurs composées d'un module à l'autre
(§1). Les méthodes comparables plafonnent à 2,29 m/s de vitesse moyenne en forêt selon eux
(§2-A, refs [18,31]).

## Méthode

- **Politique sensorimotrice de bout en bout** : un CNN prend une image de profondeur
  640×480 (stéréo SGM en simulation, Intel RealSense D435 sur le drone), la vitesse,
  l'attitude et une direction de consigne, et prédit **M = 3 trajectoires** (10 positions
  sur 1 s) avec leur coût de collision (§4-B).
- Extracteur **MobileNet-V3** pré-entraîné sur la profondeur, puis 1D-conv et MLP
  (§4-B).
- **Privileged learning** : imitation d'un expert en simulation qui a la carte 3D complète
  et l'état exact ; l'expert échantillonne 50 000 trajectoires par **Metropolis-Hastings**
  (B-splines cubiques), biaisé par un planificateur global, et garde les 3 meilleures
  (§4-A). L'expert n'est pas temps réel.
- Perte **Relaxed Winner-Takes-All** pour la multi-modalité ; DAgger ; ~90 K échantillons
  sur 850 environnements Flightmare (arbres, formes convexes), plus 10 K pour le gap étroit
  (§4-B, §4-C).
- Au test : projection sur des polynômes d'ordre 5, sélection par coût de collision puis
  coût d'actionnement, suivi par MPC (§4-B).
- La profondeur comme représentation abstraite réduit l'écart simulation → réel ; transfert
  **zero-shot**, sans ajustement sur données réelles (§4).

## Plateforme et implémentation

- Quadrirotor maison de 890 g, poussée max ~40 N, rapport poussée/poids 4,4 (§S3).
- Calcul embarqué : **NVIDIA Jetson TX2** (carte ConnectTech Quasar) ; GPU pour l'inférence
  (TensorFlow, nœud ROS Python), CPU pour la pile de contrôle ; contrôleur de vol BetaFlight
  (§S3).
- Estimation d'état par Intel RealSense T265 (VIO à 200 Hz) ; profondeur matérielle D435i
  en VGA à 30 Hz (§S3).
- Politique à 24,7 Hz sur le drone (§S3) ; MPC à 100 Hz ; contrôle bas niveau à 2 kHz
  (§S3).
- Puissance : n/r (ni pour la TX2 ni pour le drone). Mode de puissance de la TX2 : n/r.
  Précision numérique de l'inférence : n/r (FP32 TensorFlow probable, déduit).
- Code et données d'entraînement publiés : https://github.com/uzh-rpg/agile_autonomy
  (Abstract). La §S3 dit encore « will be made publicly available upon acceptance ».

## Résultats

Latence de calcul (Table 1 ; desktop i7-8700 + RTX 2080, σ sur 1000 échantillons) :

| Méthode | Plateforme | Latence totale |
|---|---|---|
| FastPlanner [18] | CPU i7-8700 | 65,2 ms |
| Reactive [32] | CPU i7-8700 | 19,1 ms |
| Ours | CPU i7-8700 | 10,3 ms (inférence 10,1 ms) |
| Ours | GPU RTX 2080 | 2,6 ms (inférence 2,4 ms) |
| Ours (Onboard) | Jetson TX2 | **41,6 ms** (inférence 38,9 ms, projection 2,5 ms) → 24,3 Hz (§S4) |

Vol réel (§2-A, Fig. 3) : 56 expériences au total. En forêt (31 essais) : 100 % de succès
à 3 et 5 m/s, 8/10 à 7 m/s, **60 % à 10 m/s**. Environnements construits (19 essais,
3 à 7 m/s) : aucun crash. Sortie d'un hangar par une brèche de ~0,8 m : 6/6 réussis à 3 et
5 m/s, contre 0/3 pour un drone commercial à ~2,7 m/s (§2-A, modèle non nommé dans le texte
extrait, renvoyé en note de bas de page).

Simulation (§2-B, Fig. 4) : taux de succès moyen de 70 % à 10 m/s ; forêt 100 % jusqu'à
5 m/s, 60 % à 10 m/s, aucune baseline ne réussit à 10 m/s ; gap étroit 2 échecs sur 10 à
7 m/s ; urbain 2 échecs sur 10 à 10 m/s. Jusqu'à 12 m/s avec 50 % de succès en forêt peu
dense (§S2). Vitesse max théorique (modèle de Falanga étendu à la rotation) : 13,5 m/s pour
Ours contre 12,0 (FastPlanner) et 13,2 (Reactive) (Table S3, lecture fragmentée).
Avec profondeur stéréo bruitée, perte de seulement 10 points à 10 m/s (§2-D).

→ reportés dans `benchmarks.csv` : 2 lignes — Jetson TX2 embarquée (41,6 ms, 24,3 Hz,
Table 1 / §S4) et desktop RTX 2080 (2,6 ms, Table 1). Tâche « navigation (planification
de trajectoire) », métrique = taux de succès en vol, non comparable à un mAP.

## Limites et critique

- **Pas de puissance mesurée**, ni pour la TX2 ni pour la plateforme ; aucun lien entre
  latence de calcul et autonomie de vol. Gamme de puissance : Jetson (~10 W, ordre de
  grandeur de la classe TX2, déduit, non mesuré par les auteurs).
- **Comparaison de latence biaisée vers le desktop** : les « 25,3× plus rapide que
  FastPlanner » (§2-C) opposent l'inférence GPU RTX 2080 à des baselines CPU. Les baselines
  ne sont pas mesurées sur la TX2, seul Ours l'est.
- **Baselines non conçues pour la vitesse** : FastPlanner n'a été démontré qu'à 3 m/s
  selon les auteurs eux-mêmes (§2-D).
- **Statistiques réelles faibles** : 56 essais au total, ~10 par condition ; pas
  d'intervalle de confiance.
- La perception est une profondeur **stéréo matérielle** (D435) : aucune détection
  d'objets ; l'essentiel du calcul (VIO, stéréo) est délégué aux ASIC des caméras
  RealSense, non comptabilisé dans la latence (déduit).
- Pas de quantification, pas de TensorRT signalé : la latence TX2 est sans doute loin de
  l'optimum (déduit).

## Pertinence pour la thèse

- **Référence pour l'axe `system-codesign`** : le papier relie explicitement latence de
  traitement et **vitesse de vol sûre** (modèle de Falanga étendu, §2-D, §S5, Table S3).
  C'est exactement la « métrique système » absente des papiers YOLO/FPGA (hypothèse de
  `gaps.md`).
- Donne un point de repère « Jetson » (TX2, 41,6 ms de bout en bout) pour situer un
  accélérateur FPGA ou nano dans la boucle perception → action.
- Hors détection d'objets : utile pour la problématique (latence → vitesse), pas comme
  baseline de détecteur.

## Gaps identifiés

- **Latence → vitesse max** : le modèle t_s + t_p + t_rot → v_max (§S5) n'est jamais
  appliqué à un détecteur embarqué sur FPGA ; on pourrait l'utiliser pour convertir des
  gains de latence FPGA en m/s.
- **Énergie** : aucune puissance ni autonomie mesurée pour cette politique ; le couplage
  calcul ↔ énergie ↔ vol reste ouvert.
- **Portage à puissance réduite** (FPGA, nano) d'une politique de navigation de bout en
  bout : non traité.

## Statut de lecture

Papier complet (`fulltext.md` lu en entier, extraction GROBID `ok`). La Table 1 est lisible
mais un peu désordonnée ; la Table S3 est fragmentée (valeurs de v_max lues dans un bloc
mal découpé). Les figures (taux de succès par vitesse) ne sont connues que par le texte. La
note de bas de page nommant le drone commercial n'est pas dans l'extraction.

Ce qui suit est déduit et non affirmé par les auteurs :
- la gamme de puissance (~10 W) de la TX2 ;
- la précision FP32 et l'absence d'optimisation TensorRT ;
- le fait que VIO et stéréo déchargés sur les RealSense ne sont pas comptés dans la
  latence ;
- l'intérêt du modèle latence → vitesse pour les accélérateurs FPGA.
