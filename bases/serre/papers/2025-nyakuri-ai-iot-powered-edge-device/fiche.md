---
id: 2025-nyakuri-ai-iot-powered-edge-device
fiche: done
date: 2026-10-29
---

# AI and IoT-powered edge device optimized for crop pest and disease detection

Jean Pierre Nyakuri, Celestin Nkundineza, Omar Gatera, Kizito Nkurikiyeyezu, Gervais Mwitende, 2025, Scientific Reports 15(1). https://doi.org/10.1038/s41598-025-06452-5
Type : article de journal (relu par les pairs)

## Problème

Les agriculteurs de petites exploitations (Rwanda, cultures céréalières, maïs) n'ont ni connectivité fiable ni matériel cher : les auteurs veulent un appareil portable, à faible consommation, qui classe localement ravageurs et maladies sans passer par le cloud (§Related works, #002.3 ; Conclusion, #022.0).

## Méthode

- Modèle « Tiny-LiteNet » : élève de six blocs depthwise à squeeze-and-excitation plus une couche dense, distillé depuis un MobileNetV2 préentraîné (teacher) ; perte de précision annoncée d'environ 1 point par rapport au teacher (#009.0).
- Deux modèles distincts : maladies du maïs (4 classes, 10 700 images) et ravageurs (5 classes, 12 400 images), sources « PlantVillage + collecte terrain » sans proportion donnée (Table 4, #036.0).
- Prétraitement : 224 x 224, décalages/cisaillement/zoom jusqu'à 30 %, luminosité [0,8 ; 1,2], flip ; découpage 70/15/15 (Table 5, #038.0), et par ailleurs validation croisée 5 plis 80/20 répétée 5 fois (#017.0). Les deux protocoles ne sont pas réconciliés.
- Post-traitement : seuil de confiance, puis texte d'explication fixe (règles préprogrammées, pas de LLM) (Algorithm 1, #016.0 ; Conclusion #022.0). Pas de Grad-CAM : l'« explicabilité » est un texte préécrit par classe.
- Quantification : aucune mentionnée (n/r). Framework, format d'export, runtime : n/r.

## Plateforme et implémentation

- Appareil : Raspberry Pi 5 (BCM2712, Cortex-A76 2,4 GHz, 8 Go), caméra HD, capteurs météo, module GSM/GPRS, panneau solaire et batterie lithium (#006.0). Pas de NPU ni d'accélérateur.
- Banc de six plateformes (Table 7, #039.0) : RPi 5 : 4,7 W, 16 ± 2 ms, 570 Mo, 80 USD ; RPi 4 : 4,5 W, 32 ± 4 ms ; FPGA Artix-7 (HDL) : 3 W, 4 ± 1,2 ms, 150 USD, jugé trop complexe ; RP2040, Nano 33 BLE, ESP32-CAM : incapables d'exécuter le modèle.
- Puissance : colonne « power requirement (W) », méthode de mesure non décrite (donc `unspecified`). Latence : protocole (batch, nombre de passes, préchauffage, pré/post-traitement inclus ou non) n/r.
- Code et poids : aucun lien ni déclaration de disponibilité trouvé dans le texte : non publiés (à confirmer sur la version éditeur).

## Résultats

- Tiny-LiteNet : accuracy 98,6 %, F1 98,4 %, rappel 98,2 %, 1,2 Mo, 1,48 M de paramètres, CV 5 plis 98,5 %, 16 ms (Table 6, #040.0). Courbes : validation ~98,6 % (maladies) et ~99 % (ravageurs) (#019.0).
- Baselines (même table, plateforme non indiquée) : MobileNetV2 98,7 % / 21 ms ; EfficientNetB0 98,3 % / 23 ms ; DenseNet121 98,9 % / 45 ms ; VGG16 98,7 % / 74 ms. Écart de précision entre tous les modèles : 0,6 point, donc non discriminant.
- Résultat principal : le RPi 5 tourne à 16 ms et 4,7 W pour un modèle de 1,2 Mo (Table 7, #039.0).
- Aucun résultat séparé laboratoire / terrain : un seul score agrégé sur un jeu mélangeant PlantVillage et images de terrain.
→ reportés dans `benchmarks.csv` : 4 lignes proposées à l'agent principal (RPi 5, RPi 4, FPGA Artix-7, EfficientNetB0 de référence).

## Limites et critique

- Incohérences internes : la Conclusion annonce « 80 ms » d'inférence alors que Tables 6 et 7 donnent 16 ms (80 est la colonne coût en USD de la ligne RPi 5) ; la taille est 1,2 Mo (Table 6) ou 0,72 Mo (Table 8, #042.0) ; protocole 70/15/15 contre 5 plis 80/20. Les chiffres de la Table 7 sont donc à prendre avec prudence.
- Précision saturée à 98-99 % pour tous les modèles : signature d'un test in-domain, avec fuites probables entre images quasi identiques de PlantVillage ; aucune évaluation hors distribution, aucune calibration (ECE), aucun taux de fausses alertes sur images saines.
- Nature des classes : ravageurs (insectes) et maladies du maïs, pas des feuilles de tomate/laitue ; classification d'image entière, pas de détecteur de feuilles.
- Pas de quantification ni de NPU : la latence de 16 ms est un CPU ARM en précision non précisée. La puissance est une exigence nominale, pas une mesure. Le FPGA est cité sans toolflow ni ressources (LUT/DSP/BRAM n/r).
- Tables 2, 3 sans corps extrait (listes de technologies et de menaces IoT : sans chiffres). Tables 4, 5, 6, 8 reconstruites par PyMuPDF, recoupées avec le texte pour Table 6/7.
- Comparaison de la Table 8 avec d'autres travaux sur des jeux différents : non comparable.

## Pertinence pour la thèse

Apport faible pour la vision, utile seulement comme point de repère edge (voir « Pour SerreIA »). Il ne traite ni l'écart de domaine, ni la calibration, ni le Hailo. Rapproché de l'axe `disease-classif` / `edge-inference` / `iot-greenhouse` du profil.

## Pour SerreIA

- Comparabilité : les chiffres ne sont PAS comparables à ceux de SerreIA. Le test du papier est in-domain (mélange PlantVillage + images terrain, découpage aléatoire 70/15/15 ou 5 plis, #038.0, #017.0), sans jeu de test indépendant. L'accuracy de 98,6 % est du même ordre que celle d'un classifieur PlantVillage sur son propre test, pas du rappel 0,986 / précision 0,679 / spécificité 0,50 de SerreIA sur PlantDoc. Citer ce papier comme exemple de ce qu'une évaluation in-domain annonce, pas comme cible. Le papier lui-même ne sépare pas labo et terrain, et ne documente pas d'écart.
- Latence de référence CPU : EfficientNet-B0 23 ms et MobileNetV2 21 ms (plateforme n/r, Table 6, #040.0) contre Tiny-LiteNet 16 ms sur RPi 5 (#039.0). À SerreIA : comparer aux latences du HEF INT8 sur Hailo-8L ; la valeur du papier donne un plancher CPU « sans accélérateur » à citer dans `docs/17-analyse-systeme.md` §10, avec la réserve du protocole inconnu. Mesure à faire : EfficientNet-B0 ONNX/PyTorch sur RPi 5 seul vs Hailo-8L, mêmes images, même batch, pré/post-traitement inclus.
- Distillation d'un MobileNetV2 vers un élève très petit (1,2 Mo ; perte ~1 point, #009.0) : piste si le HEF EfficientNet-B0 est trop lent ou perd trop après INT8. Expérience : distiller le classifieur multi-têtes (`vision/` entraînement, à partir du checkpoint EfficientNet-B0) et mesurer ECE et spécificité PlantDoc, pas seulement la précision, car le papier n'évalue ni l'un ni l'autre.
- Contre-exemple de méthode : un test à découpage aléatoire sur jeu mélangé produit 98 % sans rien prouver. Garder PlantDoc strictement hors entraînement, rapporter spécificité et fausses alertes sur images saines (42 % pour le pipeline à deux étages), ce que ce papier n'a pas fait.
- Alimentation et déploiement : solaire + batterie lithium + GSM/GPRS (#006.0) ; le Pi 5 consomme 4,7 W nominal (#039.0, méthode n/r) : à mesurer sur le banc SerreIA avec Hailo (`power_scope` board). Le FPGA est écarté ici pour complexité HDL (#020.0), mais sans chiffre de ressources : non exploitable.
- Explicabilité : texte préécrit par classe après seuil de confiance (#016.0) ; équivalent d'un mapping classe -> message pour l'agent LLM de SerreIA, avec validation humaine. Rien de mesuré.

## Gaps identifiés

- Aucune évaluation hors domaine ni terrain séparée dans ce papier : écart de domaine non documenté pour ravageurs/maïs.
- Latence et puissance CPU RPi 5 sans protocole ni quantification ; pas de comparaison Hailo/Coral/Jetson.
- Pas de calibration ni de taux de fausses alertes.

## Statut de lecture

Sections lues par recherche ciblée et `pdb show` (non lecture intégrale de `fulltext.md`, règle de la base) : méthode, données, résultats, Tables 4 à 8, discussion, conclusion ; extraction GROBID correcte. Tables 2 et 3 sans corps. Tables 4 à 8 reconstruites par PyMuPDF (chiffres de la Table 6 recoupés avec #039.0 et le texte).
Déduit et non affirmé par les auteurs : l'absence de quantification, de code publié et de séparation labo/terrain (non trouvés, pas niés) ; l'attribution de « 80 » au coût en USD plutôt qu'à la latence ; le risque de fuite entre images ; la nature CPU de la latence sur RPi 5.
