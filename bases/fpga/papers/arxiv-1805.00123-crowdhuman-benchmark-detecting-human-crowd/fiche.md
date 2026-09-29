---
id: arxiv-1805.00123-crowdhuman-benchmark-detecting-human-crowd
fiche: done
date: 2026-09-29
benchmarks: none
---

# CrowdHuman: A Benchmark for Detecting Human in a Crowd

Shuai Shao, Zijian Zhao, Boxun Li, Tete Xiao, Gang Yu, Xiangyu Zhang, Jian Sun, 2018, arXiv preprint. https://arxiv.org/abs/1805.00123
Type : preprint non relu par les pairs

## Problème

Les benchmarks de détection de personnes (Caltech, KITTI, CityPersons, COCOPersons) sous-représentent les scènes de foule : 0,32 à 6,47 personnes par image et très peu de paires très recouvertes (Table 2, Table 4) ; les foules y sont souvent annotées comme régions ignorées (§1). Les occultations mutuelles perturbent aussi la NMS, sensible au seuil (§1).

## Méthode

Construction d'un jeu de données : ~25 000 images collectées par ~150 mots-clés sur Google Images (dont points de vue « surveillance »), filtrées pour garder les images denses, réparties en 15 000 / 4 370 / 5 000 (train / val / test) (§3.1). Trois boîtes par personne : tête, région visible, corps entier (avec complétion de la partie occultée), plus régions « ignore » pour les objets ressemblant à des humains (§3.2). Double vérification par au moins un second annotateur. Baselines : Faster R-CNN + FPN et RetinaNet + FPN, backbone ResNet-50, images redimensionnées à 800 px de petit côté, entraînement sur 8 GPU, 600 k / 750 k itérations (§4.1, §4.3). Métrique : mMR (log-average miss rate, protocole Caltech), AP et rappel (§4.2). Évaluation de généralisation : préentraînement CrowdHuman puis fine-tuning sur COCOPersons, Caltech, CityPersons, Brainwash (§4.5).

## Plateforme et implémentation

Sans objet (GPU, matériel exact n/r hormis « 8 GPUs », §4.3). Pas de FPGA, ni puissance, ni latence. Données téléchargeables sur https://sshao0516.github.io/CrowdHuman/ (Abstract) ; code et modèles annoncés comme « will be released » (§5), non vérifié.

## Résultats

- Statistiques (train) : 15 000 images, 339 565 personnes, 99 227 régions ignorées, 22,64 personnes par image, 470 k instances en train+val (Table 2, Abstract). Paires avec IoU > 0,5 : 2,40 par image contre 0,32 pour CityPersons (Table 4).
- Occlusion : sous-ensembles « bare » 29,89 % et « partial » 32,13 % (contre 46,79 % et 24,19 % pour CityPersons) (§3.3).
- Baselines sur CrowdHuman : corps entier, FPN AP 84,95 / mMR 50,42 / rappel 90,24 ; RetinaNet AP 80,83 / mMR 63,33 (Table 7). Corps visible : FPN AP 85,60 / mMR 55,94 (Table 6). Tête : FPN AP 77,95 / mMR 52,06 (Table 8).
- Comparaison : FPN sur Caltech mMR 10,08 et sur CityPersons 14,81 (Table 7) : CrowdHuman est nettement plus difficile.
- Généralisation : Caltech mMR 10,08 -> 3,46 avec préentraînement CrowdHuman (Table 10) ; CityPersons 14,81 -> 10,67 (Table 11) ; COCOPersons 41,89 -> 39,79 (Table 9) ; Brainwash 19,77 -> 17,24 (Table 12).
→ reportés dans `benchmarks.csv` : aucune ligne (résultats GPU sur un jeu de données, sans mesure matérielle embarquée) ; `benchmarks: none`.

## Limites et critique

- Images issues du web (Google Images), pas de séquences vidéo ni de conditions industrielles : pas d'EPI, éclairage et angles de caméra de surveillance non caractérisés au-delà du mot-clé « surveillance viewpoint » (§3.1). Domaine industriel dangereux non couvert (déduit).
- Baselines lourdes (ResNet-50 FPN, images 800x1400 px, GPU) : aucune donnée sur des détecteurs légers ou quantifiés (YOLO, MobileNet) ; l'écart entre mMR CrowdHuman (~50) et Caltech (~10) montre la difficulté mais pas la tenue d'un modèle embarqué.
- Le tableau 2 du texte extrait est aplati (corps sans en-têtes de colonnes) ; les valeurs de Table 1-2 ont été lues en recoupant avec le texte du §3.3.
- Annotation du corps entier occulté : variance entre annotateurs reconnue (§4.4). Licence d'usage du jeu de données non discutée dans le papier.
- Absence de métrique de sûreté (taux de non-détection à un instant donné, pire cas), alors que mMR n'est qu'une moyenne sur FPPI.

## Pertinence pour la thèse

Jeu de données de référence pour la détection de personnes en foule/occultation (corps entier, visible, tête), donc candidat pour entraîner ou évaluer un YOLO de détection de personnes, et utile pour tester la robustesse à l'occultation. La boîte « tête » et la boîte visible offrent des signaux redondants utilisables pour un moniteur (déduit). Ce qui reste ouvert : domaine industriel (EPI, machines occultantes), tests sur détecteurs quantifiés FPGA et métriques de sûreté.

## Gaps identifiés

- Absence de jeu de données de personnes en secteur industriel dangereux avec occultations par machines, EPI et prise de vue de surveillance fixe.
- Peu d'évaluations de détecteurs quantifiés/embarqués sur CrowdHuman.

## Statut de lecture

papier complet (fulltext.md lu en entier). Le texte est tronqué en plusieurs endroits (§4.4 « Head Detection », §4.5 fin des paragraphes COCOPersons et Caltech/CityPersons) ; les tableaux 6 à 12 sont présents dans « Figures et tableaux », mais Tables 2, 3, 5 sont sans corps propre exploitable (déclaré dans `extraction.warnings`). Déduit et non affirmé par les auteurs : limites domaine industriel, usage pour un moniteur tête/visible, absence de métrique de sûreté.
