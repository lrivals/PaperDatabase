---
id: arxiv-2609.21005-project-scout-interceptor-drone-perimeter
fiche: done
date: 2026-10-01
---

# Project SCOUT: Interceptor Drone for Perimeter Defense

Azmain Yousuf, Siwei Cai, Knut Peterson, Lifeng Zhou, David Han, 2026, arXiv preprint (Drexel University). https://arxiv.org/abs/2609.21005
Type : preprint non relu par les pairs

## Problème

Contre-drone **air → air** : un drone défenseur doit détecter, suivre et contrer un UAV intrus entièrement à bord, sans station sol ni radar externe (jamming-resistant). Les auteurs posent que de bons détecteurs sur jeux statiques ne suffisent pas : de courtes pertes de piste ou des sauts de centre de boîte déstabilisent la commande en boucle fermée, sous contraintes de latence et de puissance d'une plateforme embarquée (§I, §II-C).

## Méthode

- Détecteur YOLO26n pré-entraîné sur 4 jeux (DroneHunter 58,6k, Det-Fly 13,3k, DUT Anti-UAV 10k, LRDDv3 102,5k ; 184,4k images, 50 epochs, AdamW, lr 1e-3, batch 48, RTX 3090), puis fine-tuné 10 epochs sur 3 931 images du drone cible DJI Neo (3 494 train / 437 val) (§III-A).
- Pipeline en 4 couches (§III-B) : ingestion asynchrone avec file à un élément (drop-frame, frame la plus récente) ; TensorRT FP16 (PyTorch → ONNX → engine, fusion de couches, Tensor Cores) ; ByteTrack à deux pools (seuil 0,50, confiance minimale S_min = 0,06) ; filtre géométrique de rejet des sauts (rejet si d_t > 2 D_{t-1} et S_t ≤ max des K = 10 dernières confiances, éq. 3) et compteur de perte (T_stale = 0,5 s).
- Contrôle (§III-C) : « gardien de but » planaire, loi PD saturée sur l'erreur image (v_y, v_z ; v_x = 0, yaw = 0), zones mortes, vitesses limitées à 1,6 m/s (latéral) et 2,0 m/s (vertical) (§IV-B), commandes via MAVROS en mode OFFBOARD. Pas de FPGA : toolflow TensorRT.

## Plateforme et implémentation

Drone défenseur sur mesure : Pixhawk 6C Mini, **NVIDIA Jetson Orin NX 16GB** (mode performance maximale), caméra ZED Mini (VIO), ROS 1 + MAVROS (§IV-A). Mesures : flux 720p, entrée détecteur 736 px, batch 1 (§III-B.2). **Puissance : n/r** (aucune mesure ni budget énergétique). Gamme : Jetson (classe 10-25 W, déduit, non donné par le papier). Code, modèle et jeu DJI Neo : non publiés (seule une vidéo de démonstration est citée).

## Résultats

- Détecteur hors ligne sur la validation DJI Neo : mAP@50 0,878 → 0,955 et mAP@50-95 0,600 → 0,824 après fine-tuning (Table I).
- Ablation sur 1 827 frames (Table II, corps de tableau mal extrait) : le texte indique 30 faux positifs avec le seuil 0,06 pour YOLO et YOLO+ByteTrack, 0 avec le filtre, au prix d'un seul vrai positif (détections 1 195 → 1 164, soit -31, cohérent mais déduit) (§IV-C).
- Débit pipeline complet sur Orin NX : PyTorch 22,5 fps → TensorRT 48 fps (« +114 % ») (§III-B.2) ; latence détecteur (sous-total) 44,5 ms → 20,8 ms, max 70,0 → 41,7 ms ; inférence 26,1 → 7,9 ms ; NMS + ByteTrack 2,5 ms moyen, max 10,8 ms (Table IV, 100 dernières frames, hors SDK caméra et transport image).
- Vol représentatif de 104,53 s (Table III) : 31,82 FPS de publication, écart médian entre messages 30,29 ms, maximum 100,72 ms, détections valides 3 065 / 3 326 (92,2 %), confiance moyenne 0,813. RMSE d'erreur de centrage 0,134 (horizontal) et 0,107 (vertical) en coordonnées image normalisées sur t = 20-60 s (Fig. 5).
- Pas de taux de réussite d'interception (§IV-B, §IV-D).
→ reportés dans `benchmarks.csv` : 3 lignes (TensorRT, PyTorch, en vol), écrites dans le fichier de lots (scratchpad) et non dans le CSV de la base.

## Limites et critique

- Vol indoor (20 × 40 × 5 m), cible DJI Neo pilotée à la main, un seul type de cible ; aucune métrique d'interception (taux de blocage, marge de pénétration) : les auteurs le reconnaissent (§IV-D). Le succès est « qualitatif ».
- Incohérence de débit : 48 fps (pipeline mesuré sur banc, §III-B.2) vs 31,82 FPS (Table III, en vol) vs « 31,85 FPS » (conclusion) ; le premier exclut SDK caméra et transport, le deuxième est un débit de publication en vol. Non comparables sans précision. L'ajout de latence camera -> commande n'est pas mesuré de bout en bout.
- Le mAP est mesuré sur une validation de 437 images du même domaine que le fine-tuning (même séquences probables, déduit) : risque de fuite ; pas de mAP_small ni de performance par distance malgré l'argument du « long range ».
- Aucune puissance, aucune charge CPU/GPU, aucune autonomie : pas de co-design énergie ↔ vol. Le PyTorch de référence n'a pas de précision déclarée (FP32 présumé, non affirmé). La comparaison PyTorch/TensorRT mélange aussi la charge du système de vol sur le même module.
- Table II mal extraite (colonnes manquantes) : lecture croisée avec le texte. Preprint, aucun code publié.
- Comparaison à Wyder et al. (Tiny YOLO, 8 FPS, 77 %) seulement qualitative, jeux et protocoles différents.

## Pertinence pour la thèse

Axe `counter-uav` **air → air** (relève de l'IA embarquée selon profile.md), avec `tracking-navigation` et `system-codesign` : exemple concret de chaîne perception → contrôle en gamme Jetson, avec décomposition de la latence par étage (utile comme référence de latence perception → contrôle, à côté du vol agile). Hors FPGA : peut servir de baseline GPU/Jetson pour comparer un portage FPGA de YOLO sur drone, mais sans puissance ni mAP_small.

## Gaps identifiés

- Aucune mesure de puissance / autonomie pour un intercepteur embarqué air → air ; pas de lien entre latence de perception et vitesse de vol / de fermeture sûre.
- Pas de métrique d'interception normalisée ni de protocole outdoor ; pas de détection de petits objets à longue portée évaluée à bord.
- Pas de portage FPGA ou ASIC de ce type de pipeline détection + ByteTrack + commande ; variabilité de l'étape NMS + association (max 10,8 ms) non étudiée.

## Statut de lecture

Papier complet (fulltext.md en entier). Extraction PyMuPDF (`extraction.ok` faux) : Table II a perdu des colonnes (faux positifs absents du corps), Table III a un corps partiel (nombre total de messages, frames manquantes et sauts de trajectoire sans valeur). Ce qui est déduit et non affirmé par les auteurs : la lecture de Table II (1 195 → 1 164 incluant les faux positifs), la précision FP32 du PyTorch, la gamme de puissance Jetson, le risque de fuite entre fine-tuning et validation.
