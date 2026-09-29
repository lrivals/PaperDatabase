---
id: arxiv-2311.11420-lifelearner-hardware-aware-meta-continual
fiche: done
date: 2026-09-29
---

# LifeLearner: Hardware-Aware Meta Continual Learning System for Embedded Computing Platforms

Young D. Kwon, Jagmohan Chauhan, Hong Jia, Stylianos I. Venieris, Cecilia Mascolo, 2023, ACM Conference on Embedded Networked Sensor Systems (SenSys). https://doi.org/10.1145/3625687.3625804
Type : conférence

## Problème

L'apprentissage continu sur systèmes embarqués bute sur le peu de données labellisées, la
mémoire et le calcul (Abstract). Les méthodes Meta CL (OML, ANML, ANML+AIM) apprennent avec
peu d'exemples mais se dégradent quand beaucoup de classes s'ajoutent et demandent
135 Mo à 1,5 Go de mémoire (§1, §5.2).

## Méthode

- **Meta CL avec rejeu** : méta-entraînement hors ligne (ANML) pour une bonne initialisation,
  puis, au déploiement, boucle interne (adaptation rapide du classifieur sur 10-30 exemples de
  la nouvelle classe) suivie d'une boucle externe sur les exemples rejoués (§3.1, §3.3).
- **Latent replay** à la sortie du feature extractor, qui est **figé** au déploiement : seul le
  classifieur apprend (§3.2.1).
- **Module de compression** des replays : bitmap creux (plus de 90 % de zéros après ReLU) puis
  **quantification produit (PQ)**, sous-vecteurs de 8 à 128 flottants codés sur 1 octet,
  codebook appris hors ligne et stocké en Flash (§3.2.2).
- Feature extractor quantifié **INT8** (QNNPACK sur Jetson/Pi, TFLM sur MCU) (§4).
- MCU : moteur de rétropropagation maison en C++ (Eigen) pour le classifieur, poids en SRAM,
  replays compressés en SRAM ; 80 Ko de binaire pour compression + rétropropagation ;
  architecture réduite TinyANML (largeurs 0,2 / 0,05 / 0,4) (§4, §5.5).
- Données : CIFAR-100, MiniImageNet, Google Speech Commands v2, 30 exemples par classe (§5.1).

## Plateforme et implémentation

- Jetson Nano (4× Cortex-A57, 4 Go), Raspberry Pi 3B+ (4× Cortex-A53, 1 Go) ; énergie par
  Tegrastats (Jetson) et wattmètre USB (Pi) × temps (§4, §5.2).
- **STM32H747**, un seul cœur Cortex-M7 utilisé, SRAM limitée volontairement à 512 Ko et Flash
  à 1 Mo (§4). Méthode de mesure de l'énergie MCU : n/r.
- Code publié : https://github.com/theyoungkwon/LifeLearner (Abstract).

## Résultats

- Précision (Table 2) : LifeLearner 0,443 / 0,411 / 0,656 (CIFAR-100 / MiniImageNet / GSCv2)
  contre ANML 0,272 / 0,327 / 0,429 ; à 2,8 points en moyenne de l'Oracle iid (§5.2, §5.4).
- Mémoire de pointe : 15,5 / 136,7 / 3,40 Mo, soit 70,8× / 11,4× / 178,7× de moins
  qu'ANML+AIM (Table 1 texte, Table 2).
- Jetson Nano, bout en bout sur toutes les classes : 414,7 s et 1,91 kJ (CIFAR-100) contre
  7 100 s et 32,7 kJ pour ANML+AIM ; GSCv2 83,8 s / 0,39 kJ (§5.2, Table 2).
- Ablation : le rejeu (Latent) apporte +10,6 à +28,4 points à ANML ; la compression ne coûte
  presque rien en précision ; la quantification INT8 réduit mémoire et latence (Table 2).
- **MCU STM32H747**, apprendre une classe avec 10 exemples (Table 3) : Tiny LifeLearner
  CIFAR-100 0,393, SRAM 236 Ko, Flash 825 Ko, 832 ms, 195 mJ ; GSCv2 0,534, 212 Ko / 806 Ko,
  1 160 ms, 271 mJ ; Tiny ANML 0,176 et 0,209. La ligne MiniImageNet est désordonnée à
  l'extraction ; le texte donne pour Tiny LifeLearner 181-281 Ko de SRAM, 725-825 Ko de Flash,
  832-1 204 ms et 195-282 mJ sur les trois jeux (§5.5).
- Rétropropagation seule ajoutée au backbone : 579 ms contre 561 ms, 134 mJ contre 128 mJ,
  +100 Ko SRAM et +260 Ko Flash (CIFAR-100) (§5.5).

→ reportés dans `benchmarks.csv` : 3 lignes (STM32H747 CIFAR-100, `high`, et GSCv2, `medium`
— cellule Flash/latence fusionnée à l'extraction ; Jetson Nano CIFAR-100, `high`).
`latency_ms` = temps d'apprentissage (une classe sur MCU, tout le protocole sur Jetson), pas
une latence d'inférence ; `power_w` n/r (seule l'énergie est donnée).

## Limites et critique

- Seul le classifieur apprend (feature extractor figé) : pas d'adaptation de représentation à
  une dérive des entrées (déduit).
- Précisions absolues faibles sur MCU (0,39 sur CIFAR-100) ; l'« Oracle » dispose aussi de
  30 exemples par classe seulement, ce qui rend l'écart de 2,8 points peu exigeant.
- Méthode de mesure de l'énergie sur STM32H747 non décrite dans le texte extrait.
- Meilleur learning rate choisi parmi 10 en méta-test pour chaque méthode (§5.1.5), ce qui
  suppose un jeu de validation au déploiement.

## Pertinence pour la thèse

Référence MCU récente pour l'apprentissage continu **avec chiffres de SRAM, Flash, latence et
énergie sur Cortex-M7**. Deux idées transposables au stage : figer et quantifier le feature
extractor, et compresser fortement la mémoire de rejeu (bitmap + PQ). Pour une approche par
régularisation, elle fournit un ordre de grandeur de budget (≈ 200-300 Ko de SRAM, < 1,2 s
par classe) (déduit). Le cadre reste classification image/audio, sans séries temporelles de
maintenance.

## Gaps identifiés

- Meta CL + rejeu compressé sur signaux vibratoires / RUL : non évalué (les auteurs citent
  d'autres capteurs comme perspective, §6).
- Pas de comparaison avec une régularisation (EWC/SI) au même budget mémoire sur MCU.

## Statut de lecture

Papier complet (`fulltext.md` lu en entier). Table 1 (mémoire) n'est présente que par sa
légende et le texte ; Table 3 partiellement désordonnée (ligne MiniImageNet, cellules GSCv2).
Déduit et non affirmé par les auteurs : absence d'adaptation à la dérive ; budget transposable
à une approche EWC.
