---
id: arxiv-2307.10255-land-localize-infrastructure-free-scalable
fiche: done
date: 2026-09-28
benchmarks: none
---

# Land & Localize: An Infrastructure-free and Scalable Nano-Drones Swarm with UWB-based Localization

Mahyar Pourjabar, Ahmed Alkatheeri, Manuele Rusci, Agata Barcis, Vlad Niculescu, Eliseo Ferrante, Daniele Palossi, Luca Benini, 2023, arXiv preprint. https://arxiv.org/abs/2307.10255
Type : preprint non relu par les pairs (arXiv v1, 17 juillet 2023, cs.RO ; venue n/r dans le
texte).

## Problème

La localisation relative d'un essaim de nano-drones (~10 cm) par UWB repose sur une
**infrastructure d'ancres fixes** préinstallées, avec une dégradation jusqu'à 35 cm hors de
la zone délimitée par les ancres (§I). Les approches visuelles sont jugées trop coûteuses
et fragiles pour les nano-drones (§II). Les auteurs veulent un essaim **sans
infrastructure** : une partie de la flotte atterrit et sert d'ancres.

## Méthode

- Rôles : **Anchor Drones (AD)**, qui volent vers un point, atterrissent et servent
  d'ancres UWB, et **Mission Drones (MD)**, qui se localisent par DS-TWR (3 ms par échange)
  avec les AD ; EKF du firmware Crazyflie (Bitcraze) alimenté par UWB + flot optique + IMU
  (§III-A, §IV).
- Trois variantes selon la connaissance de la position d'atterrissage des AD (§IV-A-C) :
  1. **ideal-landing** : AD posés à la main aux coordonnées connues ;
  2. **automatic-landing** : décollage d'un point connu, vol ~2 m à l'estime (IMU + flot
     optique), position d'atterrissage estimée ;
  3. **self-localizing** : les AD mesurent leurs distances mutuelles (100 mesures
     moyennées) puis AD0 calcule les positions relatives par **MDS** (SVD, bibliothèque
     Eigen) avant d'atterrir.
- **USL** (UWB Software Library) open source : primitives haut / bas niveau pour ranging et
  messages sur puces Decawave (§III-B).
- Ordonnancement séquentiel des ranging (décalage i × 3 ms) : coût linéaire en nombre de MD
  (§IV).

## Plateforme et implémentation

- Nano-drones avec MCU **Cortex-M4 monocœur** (§II), module UWB Decawave, IMU, capteur de
  flot optique et d'altitude (§IV) ; firmware Crazyflie (§III-A). Le modèle exact du drone
  (Crazyflie 2.x, deck UWB) n'est pas nommé dans le texte extrait (n/r).
- Puissance **du seul module UWB** mesurée : 357 mW en RX, 342 mW par MD dans un essaim de
  8 MD, 150 mW par AD au sol, jusqu'à 440 mW pour AD0 en réception (§V-C, Abstract). Méthode
  de mesure n/r.
- Référence commerciale : Bitcraze **Loco Positioning System** (6 ancres fixes) (§V-A).
- Code : USL annoncée open source (note de bas de page non extraite, lien n/r).
- **Aucun réseau de neurones, aucune vision.**

## Résultats

Arène intérieure, mocap, 4 AD, cercle de 1,5 m de rayon à 0,95 m/s, 0,8 m de hauteur,
5 répétitions (§V-A) :

| Système | l-RMSE 4 MD | l-RMSE 8 MD | Erreur d'atterrissage AD | Source |
|---|---|---|---|---|
| Ideal-landing | 15,3 cm | 19,7 cm | — | §V-A, Fig. 5 |
| Automatic-landing | 20,0 cm | 24,2 cm | 24,2 cm | §V-A, Fig. 5 |
| Self-localizing | 27,8 cm | 36,4 cm | 38,2 cm | §V-A, Fig. 5 |
| LPS (6 ancres fixes) | n/r | 10,3 cm | — | §V-A |

- c-RMSE (forme de trajectoire, après recalage) : 9,4-9,7 cm (4 MD), 11-12,1 cm (8 MD)
  (§V-B, Fig. 7) ; erreur de distance relative en formation ±15,6 cm (13,7 %) en
  self-localizing (§V-B).
- Auto-localisation des AD : **5,7 s** au total, dont 890 ms de ranging et 4,83 s de
  collecte ; MDS < 1 ms sur le MCU (§V-C).
- Surcoût de puissance UWB des MD : +36,7 % (4 MD) et +42,8 % (8 MD) par rapport à un MD
  seul ; un tour de ranging toutes les 48 ms (4 MD) ou 96 ms (8 MD) (§V-C).

→ reportés dans `benchmarks.csv` : aucune ligne. Le papier ne contient ni modèle de vision
ni inférence : les colonnes du CSV (précision de détection, FPS, GOPS, ressources) ne
s'appliquent pas, et la puissance rapportée est celle du seul module radio.

## Limites et critique

- **Hors du cœur de la base** : localisation radio (UWB), pas de vision embarquée.
- Incohérences de chiffres entre résumé et corps : « 12.3 % » (Abstract) contre « 13.2 % »
  (§V-A) d'erreur relative ; « jusqu'à 27 cm de plus que le COTS » (§VI) contre « 26.1 cm »
  (§V-A et §I).
- Arène intérieure de ~4 × 4 m avec mocap ; la généralisation « deployable anywhere » n'est
  pas testée en extérieur ni sur grande surface (les auteurs le renvoient aux travaux
  futurs, §VI).
- Les AD atterris ne volent plus : une partie de la flotte est sacrifiée à la localisation,
  coût non discuté en termes de mission.
- Puissance limitée au module UWB : consommation totale du drone et impact sur l'autonomie
  n/r ; méthode de mesure non décrite.
- Échelle : 8 MD au maximum ; la latence de ranging croît linéairement (96 ms pour 8 MD).

## Pertinence pour la thèse

- Faible pour la détection embarquée. Intérêt indirect pour l'axe `nano-drone` : ordre de
  grandeur du budget radio (~0,35 W par agent) face au budget de calcul d'un nano-drone,
  et exemple de travail du groupe PULP (ETH / Bologne) sur Crazyflie.
- Pour l'axe `tracking-navigation`, c'est une alternative non visuelle à la localisation
  d'essaim, utile comme point de comparaison si la thèse aborde la navigation coopérative.

## Gaps identifiés

- Fusion UWB + vision (détection de pairs) pour la localisation relative d'essaims de
  nano-drones : non traitée ici.
- Budget énergétique complet (moteurs, calcul, radio) d'un nano-drone en essaim : non
  mesuré.

## Statut de lecture

Papier complet (`fulltext.md` lu en entier, extraction GROBID `ok`). Notes de bas de page
(liens firmware, USL, LPS) et remerciements non extraits ; les chiffres des Fig. 5-7 ne sont
connus que par le texte.

Ce qui suit est déduit et non affirmé par les auteurs :
- le rattachement au groupe PULP et à la plateforme Crazyflie (le texte cite le firmware
  Crazyflie et le LPS Bitcraze, pas le modèle de drone) ;
- la taille de l'arène (déduite des coordonnées d'atterrissage ±2 m) ;
- le coût mission des AD immobilisés.
