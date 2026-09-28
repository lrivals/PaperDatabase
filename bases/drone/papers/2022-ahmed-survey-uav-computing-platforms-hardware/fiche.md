---
id: 2022-ahmed-survey-uav-computing-platforms-hardware
fiche: done
date: 2026-09-28
---

# A Survey on UAV Computing Platforms: A Hardware Reliability Perspective

Foisal Ahmed, Maksim Jenihhin, 2022, Sensors 22(16), 6286. https://doi.org/10.3390/s22166286
Type : article de journal (survey)

## Problème

Les surveys UAV existants couvrent architecture, coût, énergie, communication et
applications, mais laissent de côté la **fiabilité matérielle des plateformes de calcul
(CP)** embarquées ; seule la revue [15] l'aborde, limitée aux COTS et sans vue système
(§1, §2, Table 1). Les auteurs veulent relier les fautes des CP (soft errors, fautes
permanentes, vieillissement) aux défaillances de mission du drone.

## Méthode

Survey, sans expérience propre. Il couvre :
- les CP par module fonctionnel : Flight Control Computer (bas niveau, haut niveau,
  hybride), charges utiles de calcul intensif (détection/suivi, accélérateurs de réseaux
  de neurones, NNA), module de communication (§3, Tables 2 à 5) ;
- une vue en couches du système UAV : nœud edge, essaim (fog), station sol (cloud) (§3.4,
  Fig. 2) ;
- 12 papiers sur les modes de faute et de défaillance (§4, Table 6, Fig. 3) et 29 papiers
  sur l'amélioration de la fiabilité (§5, Table 7, Fig. 4), classés par technique :
  Bayesian Networks, Markov Chains, Kalman, automates, réseaux de neurones, autres ;
- une liste de défis (§5.2) et un concept de modèle de **fiabilité cross-layer (CLR)**
  avec monitoring de santé sur puce via IJTAG, Health Manager et Decision Manager (§6,
  Fig. 6).

Méthode de sélection bibliographique (requêtes, bases, période) : n/r.

## Plateforme et implémentation

Pas d'implémentation propre. Plateformes recensées : surtout SoC-FPGA Xilinx (Zynq,
ZedBoard, Zynq UltraScale+, ZCU102, PYNQ-Z1/Z2, Virtex-7, KU115), quelques Intel
(Cyclone V, Arria 10, DE0-nano), des µC (Arduino, Cortex-M4, PIC32) et quelques GPU
(Jetson TX1/TX2) (Tables 2 à 7). Code : sans objet.

## Résultats

Constats qualitatifs des auteurs :
- Les SoC-FPGA sont la CP la plus utilisée pour le FCC (Table 2, §3.1.3) et pour les
  études de fautes et de fiabilité (§4 « Analysis », Fig. 3 ; §5.1, Fig. 4).
- La majorité des études de fautes portent sur les capteurs (altimètre, GPS, IMU) ; les
  soft errors (SEU) sont une source montante de défaillances de la CP (Fig. 3, légende).
- Les techniques dominantes sont Bayesian / Markov pour les capteurs et actionneurs,
  Kalman pour la navigation, et la reconfiguration partielle dynamique (DPR) pour les
  accélérateurs CNN (§5.1).

Chiffres cités de travaux tiers (non vérifiés à la source) : une couche CNN quantifiée
39 % moins sensible aux radiations [89] (§5) ; SCYLLA 11,9× de latence en moins et 71,5×
d'énergie en moins face à un CPU [52] (§3.2.2) ; Tiny YOLOv2 sur FPGA 3,19× plus efficace
qu'un GPU en performance/puissance [54] (§3.2.2) ; classification de terrain à 95,14 % [36]
(§3.2.1).

→ reportés dans `benchmarks.csv` : aucune ligne. C'est un survey, sans mesure propre ;
les travaux cités sont à ficher à la source.

## Limites et critique

- **Aucune donnée quantitative de fiabilité** : ni taux de SEU, ni FIT, ni chute de
  précision chiffrée par type de faute, hors deux chiffres épars ([89], §5). Le modèle
  CLR (§6) est conceptuel, sans évaluation.
- **Méthodologie de revue non décrite** : 12 puis 29 papiers, sans critères de sélection
  ni période ; la représentativité du constat « SoC-FPGA majoritaire » est donc
  incertaine (déduit : ce constat reflète peut-être le domaine des auteurs, orienté
  test matériel, plutôt que la pratique industrielle, où les CP sont surtout µC et SoC
  ARM/GPU).
- **Tableaux hétérogènes** : des « CP » mélangent cartes, puces et drones complets (KARI
  EAV-3, TopXGun) (Tables 6, 7) ; les Jetson TX2 et Raspberry Pi sont rangés sous « µC »
  (Table 3), ce qui est discutable.
- **Accélérateurs GPU / Jetson presque absents** de l'analyse de fiabilité, alors que ce
  sont les plateformes des travaux de navigation autonome (déduit).
- **Pas de lien fiabilité ↔ énergie ↔ performance chiffré**, bien que « constrained
  resources » figure parmi les défis (§5.2).

## Pertinence pour la thèse

- **Porte d'entrée de l'axe `reliability`** : taxonomie des fautes (capteurs, actionneurs,
  CP ; transitoires et permanentes) et des techniques d'amélioration, avec des références
  à suivre pour les accélérateurs CNN sur FPGA soumis aux SEU ([89], [90] : injection de
  fautes et faisceau de neutrons sur PYNQ-Z2).
- Motive l'idée que la détection embarquée sur SoC-FPGA doit être évaluée aussi en
  fiabilité (SRAM de configuration sensible aux SEU), point absent des papiers YOLO/FPGA.
- Faible apport pour la détection elle-même ou le co-design énergie ↔ vol.

## Gaps identifiés

- **Fiabilité des détecteurs embarqués sur drone** : aucune étude recensée n'évalue un
  détecteur de type YOLO sur FPGA sous injection de fautes ou radiations en contexte
  drone ; seuls des CNN de classification sont cités [89, 90].
- **Coût de la redondance** (TMR, DPR) en énergie et en autonomie de vol : identifié comme
  défi (§5.2), non quantifié.
- **Modèle cross-layer** reliant faute matérielle → erreur de détection → défaillance de
  mission : proposé comme concept (§6), sans validation.

## Statut de lecture

Papier complet (`fulltext.md` lu en entier, extraction GROBID `ok`). L'avertissement
d'extraction signale la Table 4 « sans corps extrait », mais son corps est en fait présent
dans la section « Figures et tableaux » et a été lu. La Table 1 (comparaison des surveys)
a perdu ses coches : son contenu n'est pas lisible. Plusieurs titres parasites (libellés
de figures) sont intercalés dans le texte.

Ce qui suit est déduit et non affirmé par les auteurs :
- l'hypothèse d'un biais de sélection vers les SoC-FPGA ;
- la quasi-absence des Jetson dans l'analyse de fiabilité comme lacune ;
- l'absence, dans les travaux recensés, de détecteurs YOLO évalués en fiabilité (déduite
  des Tables 6-7, pas une affirmation des auteurs).
