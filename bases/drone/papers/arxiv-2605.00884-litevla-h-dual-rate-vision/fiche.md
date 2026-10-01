---
id: arxiv-2605.00884-litevla-h-dual-rate-vision
fiche: done
date: 2026-10-01
---

# LiteVLA-H: Dual-Rate Vision-Language-Action Inference for Onboard Aerial Guidance and Semantic Perception

Justin Williams, Kishor Datta Gupta, Roy George, Mrinmoy Sarkar, 2026, arXiv preprint. https://arxiv.org/abs/2605.00884 (DOI : n/r)
Type : preprint non relu par les pairs

## Problème

Les modèles vision-langage-action (VLA) sont solides en manipulation, mais un drone exige un guidage en boucle fermée à faible latence sous contrainte de calcul embarqué et de communication (Abstract, §1). Question posée : comment un même VLA compact, sur un seul calculateur embarqué, peut-il servir à la fois un guidage réactif rapide et une description sémantique plus lente (scène, dangers, narration pour l'opérateur) ? (§1, §5.2)

## Méthode

- Modèle LiteVLA-H : VLA de 256M de paramètres, un backbone multimodal partagé interrogé selon un mode `m_t ∈ {act, sem}` (§3, Fig. 1). Le mode action émet 1 à 2 tokens d'action (guidage de boucle externe) ; le mode sémantique émet une phrase (ou plus). Le contrôleur de vol garde la stabilisation d'attitude de boucle interne (§1, §3.1, §9.2).
- Observation centrale : en régime compact à sortie courte, la latence est dominée par le pre-fill multimodal, pas par le décodage : L(n) = P + ΣD_i, avec P ≈ 48 ms et ≈ 1–2 ms par token décodé (§3.3).
- Ordonnanceur à deux cadences : période sémantique Δs = K·Δa, K = 3 retenu, avec rafraîchissements sémantiques déclenchés par événement (danger, baisse de confiance) ; politique « deadline-first » : les requêtes d'action passent immédiatement, les requêtes sémantiques sont opportunistes (§3.2, §6.2).
- Fine-tuning « knowledge-preserving » : perte mixte L = λa·Lact + λs·Lsem + λg·Lgen + λkp·Lkp, Lkp = KL contre le backbone pré-spécialisé ; données : 120 000 échantillons d'action réactive, 45 000 sémantiques aériennes, 85 000 caption/VQA génériques ; 50 000 pas / 10 époques ; lr 3e-4 (Table 1 ; valeurs de λ et batch size absentes du texte extrait).
- Exécution : FP16, contexte tronqué nctx = 2048 (§3.4). Pas de quantification plus fine.

## Plateforme et implémentation

- Plateforme : NVIDIA Jetson AGX Orin (gamme Jetson, ordre de grandeur de dizaines de W ; module exact et mode de puissance : n/r), FP16, 256M paramètres (§3.4, §5.1).
- Ce qui est mesuré : le chemin d'inférence de l'entrée image-prompt préparée jusqu'aux tokens émis ; exposition caméra, transport capteur, ordonnancement du contrôleur de vol, dynamique des actionneurs et de la cellule sont exclus (§5.1).
- Puissance : le texte ne donne qu'un **surcoût** de +3.6 W (dual-rate vs action seule) et +0.1 GB de mémoire (§7.2) ; puissance absolue, méthode de mesure et empreinte mémoire absolue : n/r (le corps de la Table 5 n'est pas dans le texte extrait).
- Runtime d'inférence, framework, modèle de base (nom du backbone 256M) : n/r. Code, poids, jeux de données : non mentionnés, donc non publiés d'après le texte. Pas de FPGA.

## Résultats

- Action : 1 token en 50.65 ms, soit 19.74 Hz (§6.1, Abstract). Sémantique : 149.90 ms (une phrase, 6.67 Hz) à 164.57 ms (3 phrases + indice d'action, 6.08 Hz) (§6.1, Abstract). Le mode « Guided semantic » (2 phrases) figure dans la Table 2 mais sa latence n'est pas dans le texte extrait.
- Pre-fill : P = 47.8 ms, soit ρ = P/T_act ≈ 0.944 (§6.2). La phrase est ≈ 2.96× plus lente que l'action ; le mode le plus long ajoute 14.67 ms (+9.8 %) au caption (§6.1). 3 × 50.65 = 151.95 ms ≈ 149.90 ms, d'où le choix K = 3 (§6.2).
- Scheduler : dual-rate maintient 19.74 Hz d'action + 6.67 Hz sémantique pour +0.1 GB et +3.6 W par rapport à action seule ; un système mono-cadence sémantique serait plafonné à 6.67 Hz (§7.2). Les variantes de type ReMem-VLA et FutureVLA augmentent le TTFA (§7.2) ; chiffres de la Table 5 absents du texte extrait.
- Rétention (Table 4, chiffres partiels en §7.1) : action seule, CIDEr 0.31 et F1 sémantique aérien 0.42 ; + sémantique aérien, F1 0.81 ; + caption/VQA, CIDEr de 0.45 à 0.76 ; méthode complète 0.82 CIDEr, succès d'action à 1.1 point de la variante action seule (valeurs absolues du succès : n/r).
- Boucle fermée (Table 6) : écarts de trajectoire en simulation (classique 1.2 m, LiteVLA-Edge 0.8 m, ReMem-VLA 0.7 m, LiteVLA-H 0.5 m) et sur obstacle matériel (AnywhereVLA 1.1 m, FutureVLA 0.9 m, LiteVLA-H 0.6 m) ; ces valeurs viennent d'un corps de tableau reconstruit (colonnes manquantes), et le protocole n'est pas décrit : à ne pas citer sans vérifier sur le PDF.
- Baseline : LiteVLA-Edge (même auteurs), OpenVLA-OFT 7B « reproduced », AnywhereVLA 450M, FutureVLA 7B, ReMem-VLA 7B « reported » (Table 8, valeurs absentes).
→ reportés dans `benchmarks.csv` : 3 lignes (action 50.65 ms ; caption 149.90 ms ; contextual awareness 164.57 ms), `confidence: medium` (valeurs lues dans le texte, tables 2 et 5 sans corps extrait) ; lignes écrites dans un fichier intermédiaire, à fusionner par l'agent principal.

## Limites et critique

- Le titre et le résumé annoncent un résultat « aérien », mais la preuve principale est un chronométrage d'inférence sur banc ; les auteurs le reconnaissent : l'évaluation en vol en boucle fermée reste à faire (§9.5). La Table 6 mélange simulation et matériel sans cellule, charge utile ni gains contrôleur identiques (§7.3) : aucune conclusion de robustesse ne peut en être tirée.
- Comparaisons non contrôlées (embodiment, matériel, tâche, espace d'action différents ; §5.4, §9.5) : comparer 19.74 Hz sur Orin avec des chiffres « Reported » de VLA 7B de manipulation n'a pas de valeur de classement. Les variantes « ReMem-VLA style » et « FutureVLA decoupled » sont des réimplémentations maison, non les systèmes originaux (§7.2), donc le désavantage de TTFA leur est en partie imputable.
- Latence mesurée = inférence seule ; latence de bout en bout (capteur → actionneur) exclue (§5.1). Un seul token d'action de boucle externe : la qualité du guidage (success rate, dérive) n'est pas démontrée par des chiffres vérifiables ici.
- Puissance : seul un delta de +3.6 W, sans méthode ni portée ; pas de quantification (FP16 uniquement), pas de comparaison à une autre plateforme ; sensibilité du mode de puissance Orin n/r. Rétention évaluée par des métriques proxy (CIDEr, F1), pas de jugement humain (§9.5).
- Extraction PyMuPDF (`ok: false`) : corps des Tables 1 à 8 en grande partie perdus.
- Pas de baseline Jetson classique (détecteur type YOLO + planificateur) à comparer ; déduit : un détecteur compact sur Orin tourne couramment à des cadences supérieures, mais la tâche est différente (pas de langage).

## Pertinence pour la thèse

Axe `system-codesign` (et `tracking-navigation`, guidage). Apporte une référence de latence perception → guidage en gamme Jetson (~20 Hz pour un VLA 256M en FP16) et la notion de time-to-first-action et de pre-fill fraction comme métriques système, utile à côté des références de vol agile (tag `drone-racing`). Montre qu'un réseau multimodal généraliste est encore loin du budget de latence des pipelines de détection sur FPGA/MCU de la base ; aucune évaluation de la sûreté ni de l'autonomie (énergie de vol) n'est faite. Laisse ouverts : quantification INT8/INT4, portage hors GPU, mesure de puissance à la carte, évaluation en vol réel.

## Gaps identifiés

- Aucun VLA aérien embarqué n'est évalué en vol réel avec latence capteur → actionneur complète et puissance mesurée à la carte (ici : inférence seule, +3.6 W en delta).
- Effet de la quantification (INT8/INT4) sur un VLA embarqué de petite taille : non mesuré (FP16 seul).
- Pas de métrique système (autonomie, vitesse de vol sûre) liant la cadence du guidage à la dynamique du drone ; la cadence 20 Hz est posée, non justifiée par une vitesse maximale sûre.
- Aucun portage FPGA/ASIC/MCU de VLA ; pre-fill dominé par l'encodeur de vision + projecteur : cible naturelle pour un accélérateur dédié.

## Statut de lecture

papier complet (fulltext.md lu en entier), mais extraction PyMuPDF dégradée (`extraction.ok: false`) : les corps des Tables 1 à 8 manquent presque entièrement ; seuls les chiffres cités dans le texte sont utilisables. Métadonnées d'auteurs à vérifier (« williams » en minuscule dans l'extraction, corrigé ici en « Williams » dans cette ligne seulement).
Ce qui suit est déduit et non affirmé par les auteurs : la plage de puissance « dizaines de W » de l'Orin, l'imputation du TTFA supérieur des baselines à leur réimplémentation, la comparaison implicite à un détecteur compact sur Jetson, l'écart de cadence avec les pipelines FPGA/MCU de la base.
