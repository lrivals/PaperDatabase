---
id: arxiv-2506.18689-nova-navigation-object-centric-visual
fiche: done
date: 2026-10-01
---

# NOVA: Navigation via Object-Centric Visual Autonomy for High-Speed Target Tracking in Unstructured GPS-Denied Environments

Alessandro Saviolo, Giuseppe Loianno (NYU), 2025, arXiv preprint. https://arxiv.org/abs/2506.18689
Type : preprint non relu par les pairs

## Problème

Suivre en vol une cible mobile (personne, véhicule) en environnement non structuré et sans GPS,
sans capture de mouvement, carte préalable ni localisation globale par VIO/SLAM, dont les hypothèses
(texture, éclairage stable) cèdent en forêt, en intérieur ou sur sol lisse (exemple cité : crash
d'Ingenuity, §I). Les travaux « object-centric » antérieurs reposent sur la capture de mouvement,
des vitesses < 0,4 à 1,5 m/s ou un seul obstacle (§II-C).

## Méthode

Pipeline entièrement embarqué, stéréo RGB-D + IMU, formulé dans le repère de la cible (§III) :
- Détection : YOLOv11-small entraîné from scratch sur COCO, avec un zoom adaptatif (recadrage
  autour de la boîte précédente, facteur α > 1) pour garder la portée avec une entrée 320x256 ;
  initialisation unique par YOLOv11x (non entraîné ici) puis arrêté (§III-B1, §IV-B).
- Profondeur : complétion par fusion stéréo + DepthAnythingV2 (ViT-S) avec alignement polynomial
  d'ordre 2 en espace de disparité ; distance cible par filtre à mode d'histogramme (bin 0,15 m)
  dans la boîte (§III-B2, §IV-C).
- Estimation : back-projection du centre de boîte + profondeur, UKF à 200 Hz fusionnant IMU et
  détections asynchrones, état relatif 6-DoF cible-centré (§III-B3, §IV-E).
- Évitement : K = 10 points à plus faible TTC (grille 17x17) sur la carte de profondeur, injectés comme
  contraintes de barrières de contrôle (CBF) du second ordre (rayon 0,3 m, λ = 2) (§III-B4, §III-C4).
- Contrôle : NMPC (acados, SQP, horizon N = 10 pas, 2 s, δt = 0,2 s, RK4), poussées moteur en sortie,
  pénalité sur la vitesse latérale corps contre l'orbitage (§III-C, §IV-F).
Pas de FPGA, pas de quantification hors FP16 TensorRT du détecteur.

## Plateforme et implémentation

Quadrotor sur mesure de 1,3 kg, 6S, rapport poussée/poids ~4:1, RealSense D455 (640x480, 60 Hz),
contrôleur PixRacer Pro, calcul sur NVIDIA Jetson Orin NX 16GB (§IV-A). Détecteur : 92 Hz sous
TensorRT FP16 (§IV-B) ; complétion de profondeur : 31,6 ms par image (§IV-C). Gamme de puissance :
Jetson (~10-25 W selon le mode, valeur déduite, non rapportée) ; puissance, mode d'alimentation et
autonomie : n/r. Latence de bout en bout, charge CPU/GPU, fréquence du NMPC : n/r. Code et poids :
non publiés d'après le texte (seule une vidéo YouTube est citée).

## Résultats

Essais en vol réel, un scénario chacun, sans réglage entre scénarios (§V) :
- Urbain (conteneurs) : détections 98,6 %, distance moyenne 8,2 m, minimum 6,2 m (dsafe = 6,0 m) ;
  accélération max 32,4 m/s2, tangage max 15,0° (§V-E).
- Forêt (1 km, cible > 53 km/h) : détections 94,5 %, distance moyenne 10,0 m, minimum 8,4 m
  (dsafe = 8,0 m), tangage max 19,6° (§V-E). Le résumé annonce « > 50 km/h ».
- Transition hangar (perte GPS, leurres) : détections 96,2 %, distance moyenne 9,9 m, minimum
  8,9 m, accélération max 22,6 m/s2 (§V-E).
- Élévation (offset vertical 6 m, ~10 m d'altitude) : détections 93,1 %, distance moyenne 9,4 m,
  minimum 8,8 m, tangage max 28,8°, accélération max 22,8 m/s2 (§V-E).
- Répétabilité : 4 passages du scénario intérieur/extérieur (2 sens, 2 sens inverse), Table 2 ;
  chiffres du corps du tableau non extraits (§V-F).
- Ablations qualitatives : le zoom évite les permutations d'identité entre 3 mannequins
  (Fig. 15) et garde la confiance de détection au-delà de 10-12 m jusqu'à > 20 m (Fig. 16) ; la
  complétion de profondeur restitue rambardes et branches (Fig. 17) ; le mode d'histogramme reste
  stable sous occlusion, contrairement au pixel central et à la moyenne (Fig. 18).
- Le corps de la Table 1 (vitesses, accélérations moyennes) n'est pas extrait ; seuls les
  chiffres cités dans le texte sont repris.
Aucune comparaison chiffrée à une autre méthode de suivi.
→ reportés dans `benchmarks.csv` : 6 lignes
(détecteur 92 FPS, complétion de profondeur 31,6 ms, 4 taux de détection par scénario).

## Limites et critique

- Pas de baseline : ni VIO/SLAM, ni autre suiveur, ni ablation chiffrée ; les ablations sont
  qualitatives (courbes, images) et sur des essais à effectif très faible (un vol par scénario, 4 pour la
  répétabilité).
- « Taux de détection » : définition (image par image ? contre quelle vérité terrain ?) non
  donnée ; ce n'est pas un mAP et ne se compare pas aux mAP VisDrone ou à l'IoU DAC-SDC.
- Cible unique, catégorie connue (COCO : personne, panneau stop) et visible au départ ; dépendance
  à la profondeur stéréo, qui se dégrade au-delà de ~30-40 m et rend la vitesse selon l'axe de visée
  inobservable (§VI). La limite à 50 km/h dépend de l'ATV, pas d'une analyse de marge de vol.
- GPS+IMU (EKF) utilisé seulement comme référence a posteriori ; erreur d'estimation relative
  de NOVA contre cette référence : non rapportée.
- Aucune mesure d'énergie, d'autonomie, de latence perception-contrôle ni de charge calcul :
  impossible de situer le pipeline en budget Jetson. Pipeline lourd (ViT-S + YOLO + NMPC) sur Orin NX,
  donc pas transposable tel quel à un FPGA ou un MCU (déduit).
- Preprint, code non publié, vidéo seule comme preuve complémentaire.

## Pertinence pour la thèse

Axe `tracking-navigation` (vol à haute vitesse, gamme Jetson) : référence de pipeline complet
perception → estimation → contrôle embarqué, avec chiffres partiels de vitesse (53 km/h) et de
fréquence des modules (détecteur 92 Hz, profondeur 31,6 ms ≈ 32 Hz). Utile comme point de
comparaison pour une chaîne équivalente sur FPGA/SoC : le goulot apparent est la complétion de
profondeur (ViT-S), plus lente que le détecteur (déduit des deux temps). Pas de tag `drone-racing`
au sens strict (course), mais même sous-thème de vol agile à latence perception-contrôle ; non
contre-drone.

## Gaps identifiés

- Aucun bilan énergie/latence bout en bout d'une chaîne de suivi à haute vitesse sur Jetson ;
  pas de lien entre latence perception et vitesse de vol sûre atteignable (métrique système absente).
- Complétion de profondeur par réseau ViT embarqué : candidate à l'accélération FPGA/SoC, jamais
  évaluée en puissance ici.
- Suivi mono-cible à catégorie fermée ; pas de suivi en cas de perte de profondeur au-delà de 40 m.

## Statut de lecture

Papier complet (fulltext.md lu en entier ; extraction `pymupdf`, `ok: false`, donc découpage
possiblement imparfait). Les corps des Tables 1 et 2 ne sont pas extraits : seuls les chiffres
du texte (§V-E) sont repris, aucune valeur de tableau n'est reconstruite.
Déduit et non affirmé par les auteurs : plage de puissance de l'Orin NX, absence de code publié
(aucun lien dans le texte lu), goulot de la complétion de profondeur, non-transposabilité FPGA/MCU,
retrait de l'axe datasets-benchmarks (aucun jeu de données publié), axe retenu `tracking-navigation`.
