---
id: 2020-libano-understanding-impact-quantization-accuracy-radiation
fiche: done
date: 2026-09-29
---

# Understanding the Impact of Quantization, Accuracy, and Radiation on the Reliability of Convolutional Neural Networks on FPGAs

F. Libano, B. Wilson, M. Wirthlin, P. Rech, J. Brunhaver, 2020, IEEE Transactions on Nuclear Science 67(7), 1478-1484. DOI 10.1109/TNS.2020.2983662
Type : article de journal.

## Problème

Les FPGA à SRAM sont sensibles aux radiations : un SEU dans la mémoire de configuration corrompt le circuit et peut fausser la sortie (§I). Comment la quantification binaire des couches convolutives d'un CNN sur FPGA change-t-elle sa fiabilité, et comment combiner imprécision du modèle et radiations dans un seul taux de défaillance ?

## Méthode

- Cas d'étude MNIST : CNN de référence (précision ≈ 93 %) et réseau « hybride » HNN, poids binaires dans les couches convolutives seulement, couches denses en pleine précision (précision ≈ 88 %), même topologie (§II-B, §II-C, Fig. 1).
- Injection de fautes dans la mémoire de configuration via le PCAP, depuis l'ARM A53, avec extraction/classification isolées en Pblocks ; ≈ 11 millions de fautes injectées sur ≈ 39 millions possibles, bits CLB (LUT, DSP, FF, interconnexions) (§III-A). 100 images de test par faute (§IV-A).
- Classes d'erreur : tolérable (sortie différente, classe correcte), critique (mauvaise classification), bénigne (le modèle sain se trompait, la faute corrige) (§III-B). Indicateurs : AVF, section efficace dynamique σ = AVF x (bits essentiels) x σ_static / bits CRAM (éq. 1), avec σ_static = 2,67e-16 cm² par bit (données Xilinx) (§IV-B).
- Modèle de défaillance combinant inexactitude et radiation : MEBF(a,c,f,e) = a / (1 + c·f·e − a) (éq. 8) (§IV-B).

## Plateforme et implémentation

- Puce : Zynq UltraScale+ MPSoC ZU9EG (16 nm FinFET), ARM A53 quad-cœur pour piloter l'injection (§III).
- Ressources : Table I sans corps extrait ; le texte donne seulement −41 % de LUT sur l'extraction de caractéristiques pour l'HNN, FF identiques (§III).
- Temps d'exécution des deux réseaux : 233 ns (§IV-B). Puissance : n/r ; aucun essai sous faisceau : la section efficace est estimée à partir de l'injection, pas mesurée en neutrons.
- Code/bitstream : non publiés d'après le texte.

## Résultats

- AVF plus élevé dans l'extraction que dans la classification pour les deux réseaux ; un défaut dans l'extraction de l'HNN a 24 % plus de chances d'être critique que dans le CNN, dans la classification 49 % (§IV-A, Fig. 2). Erreurs bénignes trois fois plus fréquentes pour l'HNN (§IV-A).
- Section efficace estimée 39 % plus basse pour l'HNN (Fig. 4, §IV-B) ; part d'erreurs critiques 26 % (CNN) contre 38 % (HNN) (§IV-B), soit « +12 % » dans le résumé (12 points, pas 12 % relatifs).
- MEBF (éq. 8, niveau de la mer, flux 13 n/(cm²·h), c·f·e ≈ 1e-20) : HNN ≈ 7 à 8 exécutions avant une erreur critique contre 13 à 14 pour le CNN : l'inexactitude domine la radiation (Fig. 5, §IV-B). Chaque « 9 » d'accuracy perdu repousse de 10x le seuil où la radiation compte (Fig. 6, §IV-B).
→ reportés dans `benchmarks.csv` : 2 lignes (CNN et HNN : accuracy et temps d'exécution 233 ns), fournies dans `bench_rows.csv`, confiance `medium` (texte).

## Limites et critique

- MNIST minuscule (réseaux de quelques milliers de poids) : conclusions non transférables à YOLO ; les auteurs l'admettent (§V) : temps d'exécution 233 ns contre des dizaines de ms pour un détecteur, ce qui change l'ordre de grandeur de c·f·e.
- Section efficace estimée par injection et donnée Xilinx, non validée en faisceau ; injection restreinte aux bits CLB (pas BRAM ni logique de contrôle) ; 100 images par faute.
- HNN et CNN diffèrent aussi par l'accuracy (88 contre 93 %) : la comparaison de fiabilité est confondue avec la perte d'accuracy ; pas d'architecture protégée (TMR, ECC, scrubbing).
- MEBF de la Fig. 5 combine des précisions de 88-93 % mesurées sur des données fixes avec une définition de « critique » propre au classifieur ; cela masque que sous radiation réelle au sol le risque vient des autres sources d'erreur.
- Incohérence de présentation : « 12 % » dans le résumé pour un écart de 26 % à 38 % ; l'éq. 2 est présentée comme venant de la communauté détection d'objets sans référence claire.
- Table I absente.

## Pertinence pour la thèse

Référence directe pour l'axe fiabilité (SEU, injection de fautes) d'un accélérateur de réseaux quantifiés sur FPGA : montre que la quantification réduit la vulnérabilité en surface mais augmente la criticité des erreurs, et fournit une équation simple pour comparer l'apport de l'accuracy et de la durcissabilité au taux de défaillance. Utile pour formuler l'argument de sûreté (quel taux d'erreur d'entrée compte, quelle exigence de couverture). Le cas d'usage industriel au sol (flux 13 n/cm²/h) reste dominé par l'inexactitude du modèle, ce que confirme cette étude. Ne traite ni détection d'objets, ni personnes, ni normes.

## Gaps identifiés

- Injection de fautes et MEBF sur des réseaux de détection d'objets (YOLO INT8, DPU ou FINN) : aucun résultat ici.
- Criticité d'une erreur pour un détecteur (personne manquée, fausse détection) à définir : ici, une seule classe.
- Comparaison DPU (moteur programmable, configuration) contre dataflow en logique pure du point de vue SEU.
- Effet de la quantification (au-delà du binaire) sur la criticité.

## Statut de lecture

Papier complet (fulltext.md lu en entier). Table I sans corps extrait ; Fig. 2 à 6 non disponibles (leurs valeurs ne sont pas lisibles, seules celles citées dans le texte sont reprises). Une portion du début de l'introduction (§I) manque dans l'extraction. Déduit et non affirmé par les auteurs : absence de faisceau réel (aucune mention d'essai sous faisceau dans le texte lu), absence de code publié, remarque sur la confusion accuracy/fiabilité.
