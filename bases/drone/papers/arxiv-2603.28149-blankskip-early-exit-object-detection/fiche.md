---
id: arxiv-2603.28149-blankskip-early-exit-object-detection
fiche: done
date: 2026-09-28
---

# BlankSkip: Early-exit Object Detection onboard Nano-drones

Carlo Marra, Beatrice Alessandra Motetti, Alessio Burrello, Enrico Macii, Massimo Poncino, Daniele Jahier Pagliari, 2026, arXiv preprint. https://arxiv.org/abs/2603.28149
Type : preprint non relu par les pairs

## Problème

Sur un nano-drone (moins de 10 MiB de RAM, environ 1 W au total, quelques centaines de mW
pour le calcul), un détecteur même compact tourne à environ 1,5 FPS. Il applique le même
graphe de calcul à chaque image, y compris aux nombreuses images **vides** d'une
exploration (Abstract, §1). L'early-exit (EE) est bien étudié en classification, mais pas
en détection d'objets : les critères d'entropie ne s'appliquent pas à des sorties denses
(§2.2). AdaDet et DynamicDet ciblent des GPU, avec 5 à 10 GFLOPs environ, soit un ordre de
grandeur au-dessus du budget d'un nano-drone (§2.2).

## Méthode

- **BlankSkip** : une branche EE légère (2 conv 3×3 + BN + ReLU6, GAP, 2 FC, 0,078 M de
  paramètres) est attachée à une couche intermédiaire ℓ d'un **SSD-MobileNetV2**. Elle
  classe l'image comme « vide » ou « non vide ». Si P(vide) ≥ τ, l'inférence s'arrête avec
  une sortie vide ; sinon le détecteur complet s'exécute (§3.1-3.2, Éq. 2, Fig. 1).
- Entraînement de bout en bout avec une perte composite : localisation, classification et
  λ·BCE pondérée pour la branche EE. Les poids w0/w1 règlent le compromis entre détections
  manquées et économies de calcul. Les labels EE sont dérivés des annotations (§3.3).
- **Exploration** : HPO bayésienne (TPE, Optuna), une recherche par étage du backbone, sur
  la couche ℓ, le learning rate, le batch, λ et w1. L'objectif est J = mAP × économie de
  FLOPs × précision EE. τ est choisi par recherche ternaire (§3.4, Éq. 7).
- **τ est réglable en vol** : un seul scalaire à changer pour se déplacer sur le front de
  Pareto (§4.2, Fig. 2).
- Déploiement en **INT8 avec QAT** (PLiNIO, poids min-max, activations PaCT), BN repliés,
  code C généré par le compilateur **DORY** sur le cluster de 8 cœurs (§3.5).

## Plateforme et implémentation

- **Bitcraze Crazyflie 2.1** (27 g, 10 cm) avec son **AI-deck GAP8** (GreenWaves, RISC-V,
  1 fabric controller et 8 cœurs de cluster, 64 kB de L1, 512 kB de L2, 8 MB de L3 RAM et
  64 MB de flash via HyperBus). Caméra Himax HM01B0 en niveaux de gris (§2.1).
- Cluster réglé à **160 MHz sous 1,2 V**, comme dans Lamberti et al. [17] (§4.2.1).
- **Puissance non mesurée** : seul le budget de la plateforme est cité (≈ 1 W au total et
  quelques centaines de mW pour le calcul, Abstract et §1, d'après [17]). Pas de mJ par
  image. Gamme : **nano** (mW).
- Code : non publié d'après le texte extrait. PLiNIO et DORY sont open source. Une vidéo de
  vol de [17] est citée (note 1, §4.3).

## Résultats

Himax EE : jeu Himax [17] (2 classes, bouteille et canette, 240×320) augmenté d'images
vides synthétiques, avec 462 images de test dont 183 négatives (§4.1).

| Modèle (INT8, GAP8 @ 160 MHz) | mAP | MMAC | MAC/cycle | Latence (ms) | FPS | Taille (MB) |
|---|---|---|---|---|---|---|
| Static MbV2-SSD 0.5× | 0,415 | 193 | 4,14 | 285,3 | 3,50 | 1,16 |
| Static MbV2-SSD 0.75× | 0,498 | 358 | 4,22 | 523,6 | 1,91 | 2,53 |
| Static MbV2-SSD 1.0× | 0,555 | 534 | 4,96 | 666,7 | 1,50 | 4,41 |
| **BlankSkip, étage 4 (ℓ = 9)** | 0,540 | 414 (moyenne) | 4,87 | 537,1 (moyenne) | 1,86 | 4,49 |

(Table 2)

- BlankSkip : **+24 % de débit moyen** pour −0,015 de mAP face au 1.0× statique. 39,6 %
  des images sortent tôt. Précision EE en INT8 : 90,9 % ; taux de faux positifs : 7,5 %
  (§4.2.1). La passe complète coûte 539 MMAC (+0,9 %) et tourne à 1,48 FPS ; la sortie
  anticipée coûte 230 MMAC (§4.2.1).
- En float32 (Table 1), l'étage 4 donne 0,593 de mAP, 94,4 % de précision EE, 39,8 % de
  sauts et 414 MMAC en moyenne. L'étage 1 est **plus coûteux que le modèle statique**
  (708 MMAC en moyenne) à cause des grandes cartes d'activation. Les étages 1-2 sont moins
  précis (85,3 à 89,6 %).
- **Vidéo réelle de [17]** (simulation hors ligne, 2349 images annotées à la main) : 71,7 %
  d'images vides, 54,83 % de sorties anticipées, soit **2,07 FPS moyens** (+37,7 % face à
  1,50 FPS) (§4.2.1).
- **Cityscapes découpé en tuiles 512×512** (float32, non déployé) : 0,204 de mAP contre
  0,229 en statique, 1588 contre 1807 MMAC en moyenne (−12 %), 26,7 % de sauts, 82,3 % de
  précision EE (Table 3, §4.3).

→ reportés dans `benchmarks.csv` : 5 lignes. Les quatre configurations INT8 sur GAP8 de la
Table 2 (`high`) et la simulation sur la vidéo réelle à 2,07 FPS (§4.2.1, `medium`).
Puissance `n/r`. Le mAP est reporté en %, sans seuil IoU précisé par les auteurs.

## Limites et critique

- **Le gain dépend entièrement de la proportion d'images vides.** Sur Himax EE, cette
  proportion est **fabriquée** par des recadrages synthétiques (175 négatifs à
  l'entraînement, 183 au test), donc choisie par les auteurs. Le chiffre sur vidéo réelle
  (71,7 % de vide) est plus parlant, mais c'est une **simulation hors ligne** sur une seule
  vidéo. Les boîtes plus petites que le plus petit objet d'entraînement y sont retirées, ce
  qui considère comme vides des images contenant des objets lointains (§4.2.1).
- **Latence variable** : 230 MMAC contre 539 MMAC selon l'image. Le débit moyen augmente,
  mais la latence au pire cas reste celle du modèle complet (déduit). Pour la navigation,
  c'est le pire cas qui compte.
- **Faux « vide » = détection manquée** : 7,5 % de faux positifs de la branche EE en INT8
  (§4.2.1). L'effet sur le rappel des petits objets n'est pas isolé.
- **Aucune mesure de puissance ni d'énergie**, alors que l'argument est l'efficacité. Le
  gain énergétique se déduit au mieux du nombre de MAC.
- **Le mAP n'est pas défini** : seuil IoU et protocole ne sont pas précisés. Il est comparé
  aux chiffres de [17] avec un compilateur différent (DORY contre la chaîne propriétaire
  GAP8), ce que les auteurs signalent (§4.2.1).
- Tâche jouet : 2 classes d'objets posés au sol, en intérieur. Cityscapes n'est pas déployé
  sur GAP8.
- 1,5 à 2 FPS reste très loin du temps réel. Le travail ne mesure pas la vitesse de vol
  permise, bien qu'il cite l'analyse de [17] sur le lien entre vitesse, latence et
  exploration (§3).

## Pertinence pour la thèse

- **Axe nano-drone** : un des rares papiers de détection d'objets déployée sur GAP8 avec des
  chiffres complets de latence, MAC/cycle et taille (Table 2). C'est une référence de débit
  pour la gamme mW : ≈ 1,5 FPS pour un SSD-MbV2 de 534 MMAC.
- **Calcul adaptatif au contenu** : piste transposable aux FPGA, par exemple une porte « vide
  / non vide » avant la tête de détection. Elle est intéressante pour la surveillance
  aérienne, où beaucoup d'images sont vides, et pour les tuiles de haute résolution,
  qu'on retrouve dans SAHI.
- **Laisse ouvert** : l'énergie par image mesurée, la latence au pire cas, les petits objets
  et le lien avec une métrique système (vitesse d'exploration).

## Gaps identifiés

- **Détection adaptative (early-exit, saut de tuiles) sur FPGA ou nano-drone pour
  l'imagerie aérienne de petits objets** : BlankSkip ne traite que 2 classes en intérieur.
- **Énergie par image non mesurée** sur GAP8 : le gain est exprimé en MAC et en FPS
  seulement.
- **Latence au pire cas contre débit moyen** pour les réseaux adaptatifs embarqués : aucune
  analyse temps réel.

## Statut de lecture

Papier complet (`fulltext.md` lu en entier, extraction GROBID `ok`). La liste des
contributions (§1) est tronquée après la première puce. La fin de §3.2 (dimensions de la
branche) est coupée. Les Tables 1-3 ont des colonnes mal alignées mais restent lisibles ;
les valeurs ont été recoupées avec le texte (§4.2, §4.2.1, §4.3). La Fig. 2 (front de
Pareto) n'a pas été lue.

Ce qui suit est déduit et non affirmé par les auteurs :
- la latence au pire cas inchangée et son importance pour la navigation ;
- le rattachement à la gamme de puissance mW (seuls des budgets sont cités, aucune mesure) ;
- la transposabilité au FPGA et au découpage en tuiles façon SAHI.
