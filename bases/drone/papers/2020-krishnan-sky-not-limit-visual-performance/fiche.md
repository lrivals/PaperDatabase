---
id: 2020-krishnan-sky-not-limit-visual-performance
fiche: done
date: 2026-09-28
---

# The Sky Is Not the Limit: A Visual Performance Model for Cyber-Physical Co-Design in Autonomous Machines

Srivatsan Krishnan, Zishen Wan, Kshitij Bhardwaj, Paul Whatmough, Aleksandra Faust, Gu-Yeon Wei, David Brooks, Vijay Janapa Reddi, 2020, IEEE Computer Architecture Letters 19(1), 38-42. https://doi.org/10.1109/LCA.2020.2981022
Type : article de journal (lettre courte, 4-5 pages)

## Problème

On ne sait pas quelle combinaison **algorithme de contrôle appris × plateforme de calcul
embarquée** donne la meilleure performance **physique** d'un drone (vitesse), en tenant
compte du capteur et de la dynamique (rapport poussée / poids) (§1). Les modèles de
performance d'architecte (roofline, Gables) ignorent le monde physique.

## Méthode

- **Modèle « F-1 » (Formula-1)** : un roofline cyber-physique (§2-3).
  - Latence sense-to-act T = max(T_sensor, T_compute), le contrôle bas niveau (~1 kHz)
    étant négligé (Éq. 1).
  - Vitesse sûre maximale (reprise de [5]) : v = a_max (√(T² + 2d/a_max) − T), avec
    a_max l'accélération maximale et d la portée du capteur (Éq. 3) ; hypothèses :
    planification à court horizon, capacité d'arrêt avant obstacle (§2.3).
  - Tracé log-log vitesse vs « sense-to-act intensity » = 1/T : une pente (fonction de d)
    puis un plafond (dynamique), avec un **point de genou** f_k (§3.1, Fig. 3).
  - Trois régimes : **body-dynamics bound**, **sensor bound**, **compute bound** ; design
    optimal au genou ; sur- ou sous-optimisation sinon (§3.2).
- **Le poids du calcul** entre dans a_max : masse de la carte + masse d'un **radiateur
  estimée à partir du TDP** (volume de dissipateur × densité de l'aluminium) (§4, Table 1).
- Étude de cas : drone de 585 g, poussée / poids = 6, a_max = 60 m/s² sans calcul
  embarqué (« No-Acc ») ; 4 plateformes (Jetson AGX Xavier, TX2, Intel NCS, Raspberry Pi
  3b) × 3 réseaux de contrôle (VGG-16, DroNet, TrailNet) ; caméra à 60 Hz (§4).

## Plateforme et implémentation

Pas de matériel conçu ; latences mesurées en exécutant les réseaux sur les plateformes
(précision numérique, framework, batch n/r). Puissance : seul le TDP (« e.g., 30W » pour
Xavier) sert à dimensionner le radiateur ; aucune mesure (n/r). Pas de vol réel : les
vitesses sont calculées par le modèle. Code non publié.

## Résultats

- VGG-16, sense-to-act intensity : **Xavier 28 Hz**, TX2 10 Hz, NCS 1,3 Hz ; Raspberry
  Pi 3b à court de mémoire (§4, Fig. 4a). Xavier non compute-bound malgré le a_max le plus
  bas ; TX2 et NCS compute-bound.
- DroNet : seul le Raspberry Pi est compute-bound ; **NCS + DroNet donne une vitesse
  maximale plus haute que Xavier + VGG-16**, grâce au poids plus faible (§4, Fig. 4b).
- TrailNet : Raspberry Pi puis NCS plafonnés ; TX2 plus rapide que Xavier (plus léger)
  (§4, Fig. 4c).
- Toutes les accélérations avec calcul embarqué sont < 60 m/s² ; Xavier la plus basse,
  Raspberry Pi / NCS les plus hautes (Table 1 — **absente du texte extrait**, valeurs n/r).
- Une caméra à 30 FPS suffirait pour VGG-16 sur Xavier (~35 Hz) (§4).
- Vitesses maximales en m/s : uniquement dans la Fig. 4 (n/r en valeur).

→ reportés dans `benchmarks.csv` : 3 lignes (VGG-16 sur Xavier, TX2, NCS ; débit =
sense-to-act intensity du texte, `confidence: medium`). DroNet et TrailNet : aucun chiffre
en texte.

## Limites et critique

- **Modèle, pas mesure** : vitesses calculées, jamais validées en vol dans cette lettre ;
  la relation v(T) est reprise de [5].
- **Radiateur estimé par le TDP** : hypothèse forte (TDP ≠ consommation réelle, pas de
  refroidissement actif, pas de masse de la carte porteuse détaillée ici car la Table 1 est
  absente).
- **L'énergie et l'autonomie ne sont pas modélisées** : seul le poids du calcul compte, pas
  sa consommation sur la batterie (le papier parle de « performance-per-watt » mais pour
  le poids).
- **Incohérence** : Xavier + VGG-16 = 28 Hz puis « around 35 Hz (f_c = 35 Hz) » dans le
  même §4.
- Précision des réseaux (qualité de la commande) ignorée : DroNet et VGG-16 ne font pas la
  même tâche avec la même qualité.
- Pas de FPGA ni de MCU / nano-drone dans l'étude ; plateformes de 2018-2019.

## Pertinence pour la thèse

- **Référence clé de l'axe `system-codesign`** : fournit le cadre formel pour relier
  latence de détection ↔ vitesse de vol sûre ↔ poids du calcul, c'est-à-dire la
  « métrique système » absente des papiers YOLO/FPGA (hypothèse de départ de la base).
- Argument directement réutilisable pour un FPGA : à débit suffisant (au-delà du genou),
  c'est la **puissance → masse** qui borne la vitesse ; un FPGA à quelques watts pourrait
  battre un Jetson plus rapide (à démontrer, déduit).
- Version préliminaire du travail étendu dans la base : arxiv-2204.10898 (Roofline Model
  for UAVs) ; voir aussi arxiv-1905.06388 (MAVBench), même groupe (Harvard, Reddi).

## Gaps identifiés

- Placer des accélérateurs **FPGA** et **nano-drone (GAP8)** dans le modèle F-1, avec leur
  poids et leur puissance mesurés : absent.
- Étendre F-1 à l'**énergie** (autonomie de vol) et à la **précision de détection**
  (une détection plus rapide mais moins précise réduit-elle d effectif ?).
- Validation en vol de la vitesse prédite.

## Statut de lecture

Papier complet (`fulltext.md` lu en entier, extraction GROBID `ok`). La section 2 n'est
pas détectée comme titre (début de §2 et §2.1 fusionnés dans §1 : la description des
composants « sensor / compute / flight controller » y est tronquée). **Table 1**
(accélérations par plateforme) totalement absente du texte extrait. Éq. 2 absente (seule
son explication est lue). Les Fig. 1-4 ne sont connues que par leurs légendes.

Ce qui suit est déduit et non affirmé par les auteurs :
- l'avantage potentiel du FPGA dans ce modèle ;
- le lien avec arxiv-2204.10898 comme extension ;
- l'absence de validation en vol (non mentionnée dans le texte).
