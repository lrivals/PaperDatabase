---
id: arxiv-1907.07131-boosting-resolution-recovering-texture-micro
fiche: done
date: 2026-11-15
---

# Boosting Resolution and Recovering Texture of micro-CT Images with Deep Learning

Ying Da Wang, Ryan T. Armstrong, Peyman Mostaghimi, 2019, arXiv preprint. https://doi.org/10.1029/2019WR026052 (arXiv 1907.07131)
Type : preprint non relu par les pairs (le DOI pointe vers la version Water Resources Research, à vérifier)

## Problème

Compromis résolution / champ de vue en micro-CT de roches (digital rock) : les SRCNN classiques (L1/L2) donnent un PSNR élevé mais lissent la texture intraphase (carbonates microporeux, charbon fracturé). Les auteurs veulent récupérer à la fois les contours et la texture haute fréquence (Introduction).

## Méthode

- Architecture : générateur EDSR modifié (16 blocs résiduels, 64 filtres, noyau 3, ReLU -> PReLU, sans batch norm, sous-pixel x4) ; discriminateur à 8 blocs conv (64 -> 512 filtres, stride 2, BN), 2 couches denses + sigmoïde (§3.2-3.3, Fig. 2-3).
- Entrées : coupes 2D (pas de 3D) ; patchs 192x192, batch 16 ; réseau entièrement convolutif, applicable à toute taille. Facteur x4.
- Labels : l'image HR elle-même ; LR **synthétique** par imresize (noyaux aléatoires box/triangle/lanczos2/lanczos3), donc **pas de paires recalées réelles** ; les auteurs notent que le recalage réel est fragile (§3.1). Variante « augmentée » : flou gaussien (sigma 0-1) et bruit blanc (variance 0-0,005) (§4.4).
- Entraînement : 100 époques x 1000 itérations en L1 seul (Adam, 1e-4), puis 150 époques en SRGAN ; perte G = L1 + 1e-5 VGG19 + 5e-3 adversaire (§3.2-3.3).

## Plateforme et implémentation

- Scan : sources variées (Tyree X-ray UNSW, ANU CTLab, synchrotron TOMCAT, UGCT HECTOR, Ultratom RXSolutions, UT Austin) ; résolutions 2,7 à 25 µm (§3.1) ; énergie keV : n/r (Table 1 sans valeurs extraites). Échantillons : grès, carbonates, charbon (4000 coupes chacun).
- Calcul : GPU GTX 1080 Ti, TensorFlow 1.12 ; temps d'entraînement n/r.
- Code : non publié ; données (DeepRock-SR) et résultats sur le Digital Rocks Portal (https://www.digitalrocksportal.org/projects/).

## Résultats

- Jeu DeepRock-SR-2D : 12000 coupes 500x500, split 8:1:1 (aléatoire sur coupes mélangées, donc coupes voisines d'un même volume possiblement dans train et test : déduit, non précisé). Test/validation sur 1200 coupes tenues à l'écart.
- SRCNN : +3-5 dB sur bicubique (réduction d'erreur relative 50-70 %) (résumé, §1). Valeurs de Table 3 non extraites.
- PSNR train 32 en L1 seul, 29,7 après SRGAN ; validation ≈29,5 (§4.1, Fig. 7). Le SRGAN a un PSNR inférieur au SRCNN mais une texture plus proche visuellement ; les cartes de différence montrent aucun gain de précision pixel (§4.2, Fig. 9-10).
- Échantillons externes (Bentheimer Equinor, Ketton) : légère baisse de PSNR (Fig. 12). L'augmentation bruit/flou réduit le PSNR, parfois sous le bicubique (Fig. 16), mais aide sur une image réelle 7 µm bruitée (Fig. 18).
- Extrapolation à 1-5 µm (HR -> HR-SR) et comparaison SEM (Mt Simon, 1,7 µm CT vs 0,5 µm SEM) : seulement visuelle, artefacts de convolution signalés (§4.5-4.6).
→ reportés dans `benchmarks.csv` : 3 lignes (PSNR train SRCNN, train SRGAN, validation SRGAN).

## Limites et critique

- Évaluation qualitative pour la texture : le PSNR ne la mesure pas ; la texture générée n'est pas un appariement pixel (aveu des auteurs, §4.2). Aucune mesure perceptuelle ni métrique de fidélité (SSIM, LPIPS) ni test de segmentation aval.
- Extrapolation hors domaine sans vérité terrain ; les auteurs reconnaissent le scepticisme légitime envers la texture générée (Conclusion) : risque d'hallucination.
- 2D seulement, LR synthétique (bicubique/lanczos), pas de paires multi-résolution réelles ; plage 2,7-25 µm.
- Split aléatoire de coupes (fuite possible entre coupes adjacentes : déduit). Preprint, code non publié, pas de temps de calcul.

## Pertinence pour la thèse

Pour le 9 -> 2,4 µm des rouleaux : cadre direct de SR x4 GAN sur micro-CT, résolutions voisines (2,7-25 µm). Apporte surtout un avertissement : un GAN produit une texture plausible sans gain pixelwise, ce qui est dangereux pour l'encre carbonée, dont le signal est justement une texture subtile (déduit). Les paires réelles recalées des rouleaux (9 et 2,4 µm) évitent la LR synthétique critiquée ici. Domaine roches, pas de papyrus. Intérêt moyen-faible : référence méthodologique pour la perte perceptuelle et l'augmentation, pas de preuve de transfert.

## Gaps identifiés

- Absence de métrique de préservation du signal d'encre/texture sous SR (au-delà du PSNR).
- SR GAN 3D sur micro-CT avec paires réelles recalées non couverte ici.
- Quantification de l'hallucination en extrapolation sans vérité terrain.

## Statut de lecture

Papier complet (fulltext.md lu en entier). Extraction pymupdf, `extraction.ok` false : tableaux 1-4 sans valeurs (résolutions, PSNR de Table 3), figures non lues, ligatures partiellement cassées.
Ce qui suit est déduit et non affirmé par les auteurs : fuite possible du split aléatoire ; risque pour l'encre ; sources keV non indiquées.
