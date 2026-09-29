---
id: arxiv-2409.01872-latent-distillation-continual-object-detection
fiche: done
date: 2026-09-29
benchmarks: none
---

# Latent Distillation for Continual Object Detection at the Edge

Francesco Pasti, Marina Ceccon, Davide Dalle Pezze, Francesco Paissan, Elisabetta Farella, Gian Antonio Susto, Nicola Bellotto, 2024, arXiv preprint. https://arxiv.org/abs/2409.01872
Type : preprint non relu par les pairs. La venue n'est pas précisée dans les métadonnées.

## Problème

Apprentissage continu pour la détection d'objets (Continual Learning for Object Detection, CLOD) en class-incremental sur des appareils edge à mémoire et calcul limités, jusqu'aux MCU (tinyML). Les méthodes CLOD existantes reposent sur des détecteurs deux étages lourds (Faster R-CNN) ou sur RetinaNet-ResNet50 (34 M de paramètres) ou YOLOv5s (7,5 M), trop grands pour ces cibles ; les MCU visent environ 2 M de poids int8 (§2). Le replay demande un tampon en mémoire et la distillation classique un modèle enseignant complet (§2, §3.2).

## Méthode

- Détecteur : NanoDet-Plus-m (sans tête auxiliaire ni moyenne de poids pour réduire le coût d'entraînement), anchor-free, backbone ShuffleNetV2, neck GhostPAN, entrée 320x320x3, 1,2 M de paramètres pour l'entraînement, ~27 % mAP sur COCO avec une baisse de 2 % due à la simplification (§3.1). La version Nanodet-Plus-m « à 0,9 GFLOPs » est citée en §2.
- Latent Distillation (LD) : les couches basses (le backbone) sont gelées et partagées entre l'élève et l'enseignant ; seules les couches hautes sont copiées et entraînées, avec une perte de modèle sur les nouvelles classes et une perte de distillation sur les sorties des anciennes (Algorithm 1, §3.2). Effets : moins de calcul (un seul passage sur les couches basses), rétropropagation sur moins de poids, poids gelés stockés une fois (§3.2).
- Comparaison : Joint Training (borne haute), Fine-tuning (borne basse), Replay et Latent Replay (tampon de 250 images, 77 Mo et 81 Mo), LwF, SID (Selective and Inter-related Distillation, adaptée aux FCOS) ; coefficients de distillation à 1 ; AdamW, 100 époques par tâche (§4.2, §4.3).

## Plateforme et implémentation

Aucun déploiement matériel : entraînement/évaluation logiciels, matériel d'expérimentation n/r ; l'implémentation sur tinyML est annoncée en travaux futurs (§6). Puissance, latence, débit : n/r. Code publié (annoncé en §1, note de bas de page 1 ; lien non repris dans le texte extrait).

## Résultats

Scénarios : VOC 10p10, 15p5, 19p1, 15p1 (6 tâches) et COCO 40p40 ; métrique mAP@[0,50:0,95] en Old/New/All (§4.1, §4.2).
- Revendication principale : LD réduit de 74 % les paramètres supplémentaires de distillation et de 56 % les FLOPs par mise à jour par rapport aux méthodes de distillation, sans dégradation « significative » (Abstract, §5.1). Paramètres totaux : SID/LwF 2,4 M, LD 1,5 M ; Replay 1,2 M + 77 Mo de tampon, Latent Replay 1,2 M + 81 Mo (Table 1).
- Multiple Classes (10p10, 15p5, 40p40) : SID est la meilleure stratégie globale, LD est proche (§5.1). Exemples de la Table 2 (COCO 40p40, All) : SID 16, LD 13,6, Latent Replay 7,9, Replay 7 ; Joint Training 25,1 (Table 2 ; corps de tableau de mise en forme dégradée, à recouper). Table 1, 10p10 : SID 24,4 et LD 22,7 en All (extraction du tableau dégradée).
- 19p1 : LD a la meilleure stabilité (backbone gelé), mais une plasticité limitée (nouvelle classe 10,9 contre 15,7 pour SID) (Table 3, §5.2). Dégel progressif du backbone (Table 3) : de 44 % (backbone entier gelé, 309 K paramètres entraînés, All 23,6) à 100 % de FLOPs (SID, 1,2 M, All 22,8) ; le compromis dépend de l'application.
- 15p1 (séquentiel, Table 4) : SID et LD sont le meilleur compromis stabilité/plasticité ; LwF oublie catastrophiquement au fil des tâches ; Latent Replay et Replay souffrent de la taille limitée du tampon (§5.1, §5.3).
→ reportés dans `benchmarks.csv` : aucune ligne (pas de plateforme matérielle ni de FPS/puissance ; résultats en mAP, paramètres et FLOPs relatifs sur un détecteur logiciel). `benchmarks: none`.

## Limites et critique

- Aucune mesure sur cible embarquée (ni MCU, ni FPGA, ni Jetson) : la revendication « edge » repose sur les paramètres, les FLOPs relatifs et la mémoire, pas sur des temps ou une énergie mesurés ; l'implémentation tinyML est renvoyée aux travaux futurs (§6).
- Les FLOPs ne sont pas comptés en absolu dans le texte, seulement en pourcentage par rapport à SID/LwF (Table 3 : 44 % à 100 %).
- Précision absolue faible : NanoDet ~27 % mAP sur COCO (§3.1), joint training à 30,9 sur VOC d'après le texte extrait (§5) ; pas d'étude de faisabilité en détection de petits objets ou de personnes.
- LD perd en plasticité (nouvelles classes apprises moins bien, Table 3) ; le compromis dépend du nombre de couches gelées.
- Seul SID a été réimplémenté comme méthode de distillation adaptée aux FCOS : d'autres méthodes CLOD sont jugées non applicables à NanoDet (§4.3), donc pas de comparaison à l'état de l'art complet.
- Tables 1 à 4 extraites avec une mise en forme dégradée (colonnes décalées par endroits) : les chiffres cités ci-dessus sont ceux qui restent lisibles, à recouper sur le PDF avant citation.

## Pertinence pour la thèse

Axe apprentissage continu embarqué, avec un lien direct avec la détection d'objets (le cas d'usage de la thèse). Intérêt : (i) un détecteur ultra-léger et anchor-free (NanoDet) comme candidat de baseline embarquée pour l'apprentissage continu ; (ii) une méthode de mise à jour où seule la tête est entraînée sur un backbone gelé, ce qui correspond bien à un FPGA où le backbone quantifié peut rester figé et seule une petite partie être reconfigurée/entraînée ; c'est une inférence, non affirmée par les auteurs. Pour la certification : un backbone gelé simplifie la vérification (partie figée et caractérisée une fois). Reste ouvert : mise en œuvre sur FPGA ou MCU, quantification pendant la mise à jour, détection de personnes, et garanties de sûreté après mise à jour en ligne.

## Gaps identifiés

- CLOD (apprentissage continu de détecteurs) évalué sur une cible matérielle réelle (FPGA, MCU) avec latence et énergie, absent de ce papier.
- Apprentissage continu de détecteurs quantifiés (INT8 ou moins) : non traité.
- Apprentissage continu de détection de personnes / EPI en milieu industriel, et garanties de non-régression pour la sûreté.

## Statut de lecture

Papier complet (fulltext.md lu en entier ; extraction GROBID). Les Tables 1, 2 et 4 ont un corps extrait mais dégradé (colonnes mélangées) ; seuls les chiffres du texte et de la Table 3 sont considérés fiables, et les valeurs de Tables 1 et 2 citées ici sont à recouper. Déduit et non affirmé par les auteurs : l'adéquation à un FPGA (backbone gelé), l'intérêt pour la certification, l'absence d'implémentation matérielle (les auteurs l'annoncent en travaux futurs).
