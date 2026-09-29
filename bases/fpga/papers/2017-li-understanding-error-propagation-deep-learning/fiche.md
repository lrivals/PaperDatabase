---
id: 2017-li-understanding-error-propagation-deep-learning
fiche: done
date: 2026-09-29
benchmarks: none
---

# Understanding error propagation in deep learning neural network (DNN) accelerators and applications

Guanpeng Li, Siva Kumar Sastry Hari, Michael Sullivan, Timothy Tsai, Karthik Pattabiraman, Joel Emer, Stephen W. Keckler, 2017, Proceedings of the International Conference for High Performance Computing, Networking, Storage and Analysis (SC '17), article 8. https://doi.org/10.1145/3126908.3126964
Type : conférence (avec relecture par les pairs)

## Problème

Les erreurs logicielles transitoires (soft errors, single-event upsets) dans les accélérateurs de DNN peuvent produire des silent data corruptions (SDC), c'est-à-dire des sorties fausses non détectées, dans des systèmes soumis à des normes (ISO 26262 : moins de 10 FIT pour le SoC ; IEC 61508 cité pour l'industrie) (§1, §2.3). Les protections classiques (TMR, duplication d'instructions) ignorent la structure des DNN et coûtent cher. Personne, selon les auteurs, n'avait caractérisé la propagation de ces erreurs dans des DNN sur accélérateurs (§1).

## Méthode

- Injection de fautes dans un simulateur C++ (Tiny-CNN modifié, poids Caffe) de quatre CNN : ConvNet (CIFAR-10), AlexNet, CaffeNet, NiN (ImageNet) (Table 2, §4.4).
- Modèle de fautes : bit-flips uniques transitoires dans les latches du datapath et dans les buffers (hors logique combinatoire, contrôle, CPU, mémoire principale) (§4.3). 3000 fautes par latch/buffer, IC 95 % (§5).
- Six types de données (DOUBLE, FLOAT, FLOAT16, virgule fixe 32b_rb26, 32b_rb10, 16b_rb10) (Table 3). Quatre définitions de SDC : SDC-1 (top-1 changé), SDC-5, SDC-10 %, SDC-20 % (§4.5).
- Taux FIT = R_raw x taille x P(SDC), avec R_raw = 20.49 FIT/Mb extrapolé à 16 nm (§4.7). Étude de cas des buffers sur Eyeriss projeté de 65 nm à 16 nm (x8 en PE et buffers, Table 7).
- Deux protections : symptom-based error detector (SED, bornes de valeurs des activations par couche apprises + marge 10 %, vérification asynchrone par l'hôte) et selective latch hardening (SLH, durcissement des latches les plus sensibles) (§6).

## Plateforme et implémentation

Pas de FPGA ni de matériel réel : simulation logicielle d'un accélérateur canonique (Fig. 1) et de l'architecture Eyeriss (ASIC, paramètres publics), technologie projetée 16 nm. Pas de puissance mesurée. Code du simulateur modifié : non mentionné comme publié.

## Résultats

- SDC-1 dépend fortement du type de données : AlexNet 7.19 % en 32b_rb10 contre 0.38 % en FLOAT ; écart maximal 240x entre 32b_rb10 et 32b_rb26 (§5.1.1).
- Seuls les bits de poids fort (exposant en flottant, partie entière en virgule fixe) provoquent des SDC ; bit 30 de 32b_rb10 : 26.65 % contre 0.22 % en 32b_rb26 (§5.1.2). Les fautes 0 vers 1 sur l'exposant sont les plus dangereuses.
- Plus de 80 % des erreurs à grande déviation de valeur donnent un SDC (§5.1.3, AlexNet FLOAT16) ; les couches LRN atténuent la propagation ; 84.36 % des fautes sont masquées par POOL ou ReLU (§5.1.4, Table 5) ; les couches FC sont plus sensibles ; ConvNet (peu profond, 10 sorties) est bien plus vulnérable.
- FIT du datapath (Table 6) : de 0.002 (AlexNet, 32b_rb26 ou 16b_rb10) à 2.45 (ConvNet, 32b_rb10). Buffers Eyeriss (Table 8) : jusqu'à 87.47 FIT (Global Buffer, ConvNet) ; les buffers de réutilisation peuvent augmenter le FIT de plus de 100x (§1) ; le Filter SRAM (3.9 FIT, NiN) est ~1000x le datapath (0.004) (§6.1).
- SED : précision moyenne 90.21 %, rappel 92.5 % (§6.2, Fig. 8) ; réduit le FIT d'Eyeriss de 8.55 à 0.35 (FLOAT, -96 %) et de 2.63 à 0.79 (FLOAT16, -70 %). SLH : FIT des latches réduit de 100x pour ~20 % (FLOAT16) et ~25 % (16b_rb10) de surcoût de surface de latches (§6.3).
- Sans protection, le FIT d'Eyeriss peut dépasser la limite ISO 26262 de plusieurs ordres de grandeur ; les protections le ramènent dans la limite (§1, sans chiffre détaillé lu ici).
→ reportés dans `benchmarks.csv` : aucune ligne. Simulation de résilience, pas de mesure de performance sur plateforme ; `benchmarks: none`.

## Limites et critique

- Incohérence interne : le §6.2 donne précision 90.21 % / rappel 92.5 %, mais un encart de l'introduction (§1, listes de contributions) dit 97.84 % / 92.08 % (« pour certains DNN et types de données ») ; à recouper avec Fig. 8.
- Simulation et non RTL ni radiations : faute modélisée = un bit-flip transitoire dans des latches/buffers ; pas de faute dans la logique combinatoire, le contrôle, le CPU ou les bus (§4.3). Les FIT dépendent du R_raw extrapolé (20.49 FIT/Mb) et du scaling naïf d'Eyeriss.
- Réseaux petits et anciens (AlexNet, ConvNet, NiN), classification seulement : pas de détecteur d'objets (YOLO), pas de quantification INT8 ni binaire, pas de FPGA (dont les faults de configuration, cœur du sujet SEU FPGA, ne sont pas traités).
- SED : bornes apprises sur un jeu de test ; les données 16b_rb10 et 32b_rb26 (résilientes) et ConvNet ne sont pas couverts par le détecteur (§6.2) ; le détecteur repose sur des valeurs extrêmes, donc aveugle aux corruptions « dans la plage ».
- Tables 1 et 5 reconstruites par PyMuPDF (chiffres à vérifier) ; le SDC est défini par rapport à un golden run, pas par rapport à la vérité terrain.

## Pertinence pour la thèse

Référence directe pour l'axe sûreté et fiabilité : méthode de caractérisation par injection de fautes des DNN (types de données, bits sensibles, couches, réutilisation), argument que la précision réduite ou les plages dynamiques serrées améliorent la résilience (à rapprocher de la quantification INT8 sur FPGA, inférence de ma part), et idée de moniteur d'exécution peu coûteux (bornes d'activations) qui relève à la fois de la détection de fautes matérielles et de l'OOD. Fournit le cadre de raisonnement en FIT face à ISO 26262 / IEC 61508, transposable à un YOLO sur FPGA. À adapter : SEU dans la mémoire de configuration du FPGA, quantification INT8, détecteurs d'objets.

## Gaps identifiés

- Injection de fautes et SED/SLH évalués sur un détecteur type YOLO quantifié sur FPGA (mémoire de configuration incluse) : non couvert.
- Lien entre bornes de valeurs d'activation (SED) et détection OOD / moniteur d'exécution : à explorer.
- Traduction de FIT d'un accélérateur DNN en niveau d'intégrité (SIL / PL) pour un cas industriel.

## Statut de lecture

Papier complet (fulltext.md lu en entier). Tables 1 et 5 reconstruites par PyMuPDF ; certaines figures (Fig. 3-9) sans données chiffrées dans le texte extrait.
Déduit et non affirmé par les auteurs : la transposition à FPGA, INT8 et YOLO, et le lien SED / OOD.
