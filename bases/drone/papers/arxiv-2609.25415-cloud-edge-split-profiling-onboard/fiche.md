---
id: arxiv-2609.25415-cloud-edge-split-profiling-onboard
fiche: done
date: 2026-10-01
---

# Cloud, Edge, or Split? Profiling Onboard and Split Vision-Language Model Deployment for Drone AI

Zoha Azimi, Reza Farahani, Schahram Dustdar, Christian Timmerer, 2026, arXiv preprint. https://arxiv.org/abs/2609.25415
Type : preprint non relu par les pairs

## Problème

Les VLM permettent aux drones d'interpréter des scènes en langage naturel, mais l'inférence embarquée est limitée en calcul, mémoire et énergie, et l'inférence cloud dépend du réseau (latence, bande passante, connectivité) (Abstract, §I). Les auteurs affirment qu'aucune étude ne compare systématiquement, pour un VLM léger, les trois paradigmes (tout embarqué, tout cloud, split UAV-cloud) en latence, ressources, communication et énergie (§I).

## Méthode

Profilage empirique de **SmolVLM-256M** (encodeur SigLIP + projection par pixel shuffle s=4 puis MLP + décodeur SmolLM2-135M) (§II). Réglages de prétraitement par défaut conservés (longest_edge 2048, tuiles 512x512 plus une vignette globale : T = 4⌈4r⌉+1 entrées d'encodeur) (§II-1, §IV-A). Point de coupure unique : après le module de projection ; l'encodeur et la projection tournent à bord, le décodeur dans le cloud ; tenseur transmis [T, 64, 576], soit ~21x moins de valeurs qu'une coupure après l'encodeur [T, 1024, 768] (§II). Les jetons visuels transmis sont quantifiés INT8 (§V-B1). Charge de travail : 18 prompts d'inspection en 4 catégories ; 70 images du jeu simulé de lignes électriques [16] et 150 images CODEBRIM [17] (§IV-E, §IV-F). Réseau : trace 4G/LTE de 500 s [32], trois intervalles bas / moyen / haut débit (Table I, §IV-G). Mesures : tegrastats à 100 ms (Jetson), RAPL et PyNVML (cloud), énergie par requête par intégration de la puissance (§IV-D). Pas de toolflow FPGA ; aucune précision de réponse mesurée.

## Plateforme et implémentation

- Bord : « NVIDIA Jetson » dont le modèle exact n'est pas nommé ; CPU 8 coeurs ARM Cortex-A78AE, GPU Ampere 1024 coeurs CUDA / 32 Tensor Cores (§IV-D). Ces spécifications correspondent à un Orin NX 16 Go (déduit, non affirmé par les auteurs). Mode de puissance, version JetPack, runtime : n/r.
- Cloud : Intel Xeon Gold 5218, NVIDIA RTX A6000, Ubuntu 22.04 (§IV-D).
- Puissance : « module-level power » lue par tegrastats ; portée non précisée au-delà. Aucune puissance en W n'est rapportée, seulement des énergies par requête (Fig. 9).
- Code ou données de mesure publiés : non mentionnés dans le texte.

## Résultats

Gamme de puissance : Jetson (classe ~10 W), pas de mesure en W rapportée.

- Latence de calcul (hors réseau) (§V-A1, Fig. 6) : tout embarqué ~2,76 s ; tout cloud ~0,72 s (x3,8) ; split ~1,41 s à bord + ~0,68 s cloud = ~2,09 s, soit -24 % vs embarqué.
- Utilisation (§V-A2, Fig. 7) : embarqué ~11 % CPU, 55 % GPU, 31 % RAM ; étage embarqué du split ~69 % GPU, ~22 % RAM ; cloud complet ~2 % CPU, 15 % GPU, 2 % mémoire.
- Mémoire GPU (§V-A2, Fig. 8) : embarqué ~572 Mo alloués / ~854 Mo en pic ; étage embarqué du split ~236 Mo / ~472 Mo (-59 % / -45 %).
- Énergie par requête (§V-A3, Fig. 9) : embarqué ~26 J ; split ~15 J à bord (-42 % sur la batterie du drone) + ~130 J cloud ; tout cloud ~150 J.
- Communication (§V-B1, Table II) : charge utile moyenne 821,45 ko (JPEG, tout cloud), 375,84 ko (jetons INT8, split, -54 %), ~10 ko (texte ; Table II indique 0,04 Ko, incohérent avec le texte, voir limites). Latence de transfert bas / moyen / haut débit : cloud 3,20 / 0,155 / 0,104 s ; split 1,47 / 0,071 / 0,047 s ; embarqué 0,001 à 0,040 s.
- Latence bout en bout (§V-B2, Table III) bas / moyen / haut débit : embarqué 2,77 / 2,73 / 2,73 s ; cloud 3,87 / 0,83 / 0,77 s ; split 3,59 / 2,19 / 2,17 s. Le split ne minimise jamais la latence ; il minimise mémoire et énergie à bord.
- Résolution (§V-C, Fig. 10) : charge JPEG croissante avec la résolution (> 20 Mo pour les plus grandes images) ; jetons bornés à ~1,2 Mo (BF16) ou ~0,6 Mo (INT8) à T=17 ; sous ~0,2 mégapixel, le JPEG peut être plus petit que les jetons.
- Lignes de `benchmarks.csv` : 3 lignes (une par stratégie, latence = temps de calcul hors réseau, Fig. 6 lu dans le texte). Énergie, mémoire et latences bout en bout ne rentrent pas dans les colonnes ; elles sont ci-dessus.
→ reportés dans `benchmarks.csv` : 3 lignes (embarqué, cloud, split), `power_w` n/r car seule l'énergie en J est rapportée.

## Limites et critique

- Un seul modèle (SmolVLM-256M), un seul point de coupure, une seule trace réseau 4G/LTE ; pas de 5G, de liaison radio de drone réelle ni de perte de paquets. Les « conditions réalistes » restent émulées.
- Aucune précision / qualité de réponse mesurée ; les auteurs le renvoient aux travaux futurs. Les stratégies sont comparées sans garantie d'équivalence (la quantification INT8 des jetons peut modifier les sorties).
- Énergie comparée entre un Jetson (puissance du module, tegrastats) et un serveur (RAPL + GPU), de portées différentes, et le serveur est partagé ; la comparaison énergétique n'a de sens que pour la part qui vide la batterie du drone (le papier le dit pour le split). Énergie de la radio non mesurée (déduit : la transmission n'est pas incluse).
- Pas de mesure en vol : pas d'impact sur l'autonomie ou la vitesse de vol. Le Jetson est vraisemblablement alimenté sur secteur / banc (déduit).
- Les images du jeu « lignes électriques » sont simulées ; CODEBRIM est un jeu de défauts de béton, photographié et non aérien (§IV-E), donc pas de petits objets ni de VisDrone-like.
- Incohérences de l'extraction : Table I est corrompue (colonnes mélangées) ; Table II donne 0,04 Ko pour le texte alors que le texte dit ~10 kB ; la ligne Table III de lecture ambiguë est lue comme embarqué / cloud / split par recoupement avec le texte (§V-B2).
- Pas de baseline GPU de bureau ni autre VLM ; le « cloud » est un GPU RTX A6000, hors gamme embarquée.
- Hors du périmètre FPGA : tout repose sur GPU Jetson et sur un cloud.

## Pertinence pour la thèse

Axe `system-codesign` (calcul <-> énergie <-> communication, gamme Jetson ~10 W). Apporte un cadre de mesure de la répartition bord / cloud pour un VLM léger et un chiffre exploitable : couper après la projection réduit énergie bord (-42 %) et mémoire GPU (-45 à -59 %) mais ne gagne pas en latence. Ne traite ni la détection embarquée (YOLO, petits objets), ni les FPGA, ni l'autonomie en vol ; utile comme contraste (offload vs tout embarqué) et comme méthode de mesure d'énergie par requête. Pertinence modérée : le sujet est la sémantique VLM, pas la perception temps réel.

## Gaps identifiés

- Aucun profilage bord / cloud / split de VLM sur FPGA ou MCU ; seul un Jetson est testé.
- Précision absente des compromis latence / énergie (annoncée en travaux futurs, orchestrateur adaptatif).
- Aucune métrique système de vol (autonomie, vitesse de vol sûre) ; l'énergie radio n'est pas mesurée.
- Un seul point de coupure et un seul VLM ; pas de compression des jetons au-delà de l'INT8.

## Statut de lecture

Papier complet (`fulltext.md` lu en entier). Extraction `pymupdf` avec `extraction.ok: false` : le texte est complet mais les tableaux (Table I, II, III) sont mal reconstruits, et les figures n'ont pas de valeurs (Fig. 6 à 9 lues via le texte, pas les barres). Table III lue par recoupement avec le texte (§V-B2).
Ce qui suit est déduit et non affirmé par les auteurs : le modèle de Jetson (Orin NX 16 Go d'après les spécifications) ; l'absence de mesure de l'énergie radio ; l'alimentation sur banc du Jetson ; la portée de la puissance tegrastats.
